"""
Track B — Crack-β Real Data Execution.

Runs F6 (β=1.0) and F5 (pre-sample OLS, frozen) on real HO2!-CL2! data.
Pre-registration: crack_beta_execution_prereg.md §D.
Gate: synthetic calibration gate cleared (doc 37) — F6 + F5 ADMISSIBLE.

Outputs: data/processed/crack_beta_real_results.json

CAUSAL FIREWALL: β is frozen before the test window (F5: pre-sample OLS; F6: definitional).
No hyperparameter tuning on real data. Deseasonalization is causal (trailing month mean).
"""
from __future__ import annotations
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import numpy as np
import pandas as pd
from app.services.analytics_arm_a import (
    Spread, load_leg, level_vr, surrogate_vr_ensemble, VR_Q_GRID,
)
from app.services.analytics_arm_a_v2 import (
    evaluate_v2, deseasonalize_causal, increment_jump_mask,
    SEED, N_SURROGATE, MARTINGALE_GATE_V2,
)
from app.services.analytics_arm_a_v2_beta import (
    economic_anchor_beta, presample_ols_beta,
    beta_update_variance_fraction, Q_GRID_CYCLE2,
    TAU_FUPDATE, NO_MFG_BAND,
    _eval_family_on_spread,
)

# ── Frozen protocol constants (crack_beta_execution_prereg.md) ─────────────────
DATE_MIN = "1998-07-19"
DATE_MAX = "2026-06-03"
OOS_SPLIT = 0.70           # first 70% = IS, last 30% = OOS
PRE_SAMPLE_FRACTION = 0.25 # F5: OLS on first 25% of data
GALLONS_PER_BARREL = 42.0  # physical constant — not estimated
JUMP_K = 8.0               # roll-detection multiplier (frozen, same as calendars)
JUMP_W = 60                # roll-detection window (frozen)
N_DRAWS = 200              # surrogate draws (frozen)
SEED_REAL = SEED           # frozen seed

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA_DIR = os.path.join(ROOT, "data", "raw", "more-mean-reversion-data")
OUT_PATH = os.path.join(ROOT, "data", "processed", "crack_beta_real_results.json")


def _load_unix_leg(path: str) -> pd.DataFrame:
    """Load a raw NYMEX leg CSV with Unix-timestamp `time` column."""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["ts"] = pd.to_datetime(df["time"].astype(np.int64), unit="s", utc=True)
    df = df.dropna(subset=["ts"]).sort_values("ts")
    df = df.drop_duplicates(subset=["ts"], keep="last").set_index("ts")
    return df


def load_and_merge() -> tuple[pd.DatetimeIndex, np.ndarray, np.ndarray]:
    """Load HO2! and CL2!, normalize to $/barrel, merge on common dates."""
    ho_path = os.path.join(DATA_DIR, "NYMEX_DL_HO2!, 1D.csv")
    cl_path = os.path.join(DATA_DIR, "NYMEX_DL_CL2!, 1D.csv")
    ho = _load_unix_leg(ho_path)
    cl = _load_unix_leg(cl_path)

    # Trim to pre-reg date range
    ho = ho[(ho.index >= pd.Timestamp(DATE_MIN, tz="UTC")) &
            (ho.index <= pd.Timestamp(DATE_MAX, tz="UTC"))]
    cl = cl[(cl.index >= pd.Timestamp(DATE_MIN, tz="UTC")) &
            (cl.index <= pd.Timestamp(DATE_MAX, tz="UTC"))]

    # Merge on common dates
    merged = ho[["close"]].join(cl[["close"]], how="inner", lsuffix="_ho", rsuffix="_cl")
    merged = merged.dropna()
    idx = merged.index
    A_barrel = merged["close_ho"].to_numpy(float) * GALLONS_PER_BARREL  # HO → $/bbl
    B_barrel = merged["close_cl"].to_numpy(float)                        # CL already $/bbl
    return idx, A_barrel, B_barrel


def build_spread_object(name: str, idx: pd.DatetimeIndex,
                         s_raw: np.ndarray, beta: np.ndarray) -> Spread:
    """Construct a Spread from a raw (undeseasonalized) spread + beta array.
    Roll detection on the spread itself (consistent with calendar treatment).
    Deseasonalization is applied here (causal trailing month mean)."""
    n = len(s_raw)
    # Deseasonalize causally
    s_close = deseasonalize_causal(s_raw, idx)
    # Roll detection on deseasonalized spread
    roll = increment_jump_mask(s_close, k=JUMP_K, window=JUMP_W)
    # Flat-bar mask: all four OHLC equal — not available for constructed spread; set False
    flat = np.zeros(n, bool)
    # Invalid: NaN beta or pre-sample warm-up (NaN entries)
    invalid_beta = ~np.isfinite(beta)
    return Spread(
        name=name,
        s_close=np.where(invalid_beta, 0.0, s_close),
        s_open=np.where(invalid_beta, 0.0, s_close).copy(),
        beta=np.where(np.isfinite(beta), beta, 1.0),
        roll_transition=roll | invalid_beta,
        flat_bar=flat,
        index=idx,
        meta={
            "beta_mode": name, "n": int(n),
            "jump_k": JUMP_K, "n_jump_masked": int(roll.sum()),
            "n_invalid_beta": int(invalid_beta.sum()),
            "date_start": str(idx[0].date()), "date_end": str(idx[-1].date()),
        },
    )


def eval_full_and_oos(sp: Spread, n_is: int) -> dict:
    """Run evaluate_v2 on full period AND OOS sub-period.
    OOS slice: keep roll_transition and invalid masks consistent."""
    r_full = evaluate_v2(sp, seed=SEED_REAL)

    # OOS-only: slice the last (1-OOS_SPLIT) fraction
    n = len(sp.s_close)
    oos_start = n_is  # first OOS bar index
    sp_oos = Spread(
        name=sp.name + "_OOS",
        s_close=sp.s_close[oos_start:],
        s_open=sp.s_open[oos_start:],
        beta=sp.beta[oos_start:],
        roll_transition=sp.roll_transition[oos_start:],
        flat_bar=sp.flat_bar[oos_start:],
        index=sp.index[oos_start:],
        meta={**sp.meta, "oos_only": True, "oos_n": n - oos_start},
    )
    r_oos = evaluate_v2(sp_oos, seed=SEED_REAL)
    return {"full": r_full, "oos": r_oos}


def _summarise(r: dict) -> dict:
    """Compact summary dict for printing and JSON output."""
    vr = r["real_vr"]
    pf = r["per_family"]
    return {
        "confirmed_rw_garch_ma1": r["confirmed_gate_rw_garch_ma1"],
        "vr": {str(q): round(float(vr[q]), 4) for q in VR_Q_GRID},
        "p_rw":    round(float(pf["rw"]["min_vr_p_value"]), 4),
        "p_garch": round(float(pf["garch"]["min_vr_p_value"]), 4),
        "p_ma1":   round(float(pf["ma1"]["min_vr_p_value"]), 4),
        "p_ou":    round(float(pf["ou"]["min_vr_p_value"]), 4),
    }


if __name__ == "__main__":
    np.seterr(all="ignore")
    print("=" * 80)
    print("Crack-β Real Data Execution — doc 37 next action")
    print(f"Pair: HO2!×42 (A_barrel) vs CL2! (B_barrel)")
    print(f"Date range: {DATE_MIN} → {DATE_MAX}, OOS split: {OOS_SPLIT:.0%}")
    print(f"Families: F6 (β=1.0), F5 (pre-sample OLS, frozen at {PRE_SAMPLE_FRACTION:.0%})")
    print("=" * 80)

    # ── 1. Load data ───────────────────────────────────────────────────────────
    idx, A_barrel, B_barrel = load_and_merge()
    n = len(idx)
    n_is = int(n * OOS_SPLIT)
    n_oos = n - n_is
    oos_date = str(idx[n_is].date())
    print(f"\nData loaded: {n} bars | IS={n_is} (≤{str(idx[n_is-1].date())}) | OOS={n_oos} (≥{oos_date})")
    print(f"A_barrel (HO×42): range [{A_barrel.min():.2f}, {A_barrel.max():.2f}]")
    print(f"B_barrel (CL):    range [{B_barrel.min():.2f}, {B_barrel.max():.2f}]")
    print(f"Back-adj note: {(A_barrel < 0).sum()} negative A_barrel values (back-adj offset); "
          f"increments (VR basis) unaffected except at roll dates (masked).")

    # ── 2. β construction ──────────────────────────────────────────────────────
    beta_f6 = economic_anchor_beta(n)
    beta_f5 = presample_ols_beta(A_barrel, B_barrel, pre_sample_fraction=PRE_SAMPLE_FRACTION)
    pre_n = int(n * PRE_SAMPLE_FRACTION)
    beta_f5_val = float(np.nanmedian(beta_f5[pre_n:]))  # should be constant post-pre-sample
    f_bu_f6 = beta_update_variance_fraction(
        A_barrel - beta_f6 * B_barrel, beta_f6, B_barrel)
    f_bu_f5 = beta_update_variance_fraction(
        A_barrel - beta_f5 * B_barrel, beta_f5, B_barrel)
    print(f"\nβ construction:")
    print(f"  F6 β = 1.0 (fixed); f_βupdate = {f_bu_f6:.4f} (expect 0.000)")
    print(f"  F5 β = {beta_f5_val:.4f} (pre-sample OLS on first {pre_n} bars ≈ {pre_n/252:.1f} yr, then frozen)")
    print(f"  F5 f_βupdate = {f_bu_f5:.4f} (expect 0.000)")
    assert f_bu_f6 < TAU_FUPDATE, f"F6 f_βupdate={f_bu_f6} exceeds τ={TAU_FUPDATE}"
    assert f_bu_f5 < TAU_FUPDATE, f"F5 f_βupdate={f_bu_f5} exceeds τ={TAU_FUPDATE}"
    print("  Both f_βupdate < τ=0.10 ✓")

    # ── 3. Raw spread statistics ───────────────────────────────────────────────
    s_raw_f6 = A_barrel - beta_f6 * B_barrel
    s_raw_f5 = A_barrel - beta_f5 * B_barrel
    print(f"\nRaw spread (pre-deseason):")
    print(f"  F6 spread range: [{np.nanmin(s_raw_f6):.2f}, {np.nanmax(s_raw_f6):.2f}]  "
          f"mean={np.nanmean(s_raw_f6):.2f}  std={np.nanstd(s_raw_f6):.2f}")
    print(f"  F5 spread range: [{np.nanmin(s_raw_f5):.2f}, {np.nanmax(s_raw_f5):.2f}]  "
          f"mean={np.nanmean(s_raw_f5):.2f}  std={np.nanstd(s_raw_f5):.2f}")

    # ── 4. Build Spread objects ────────────────────────────────────────────────
    sp_f6 = build_spread_object("F6_crack_HO_CL", idx, s_raw_f6, beta_f6)
    sp_f5 = build_spread_object("F5_crack_HO_CL", idx, s_raw_f5, beta_f5)
    print(f"\nSpread objects:")
    print(f"  F6: n={len(sp_f6.s_close)}, roll_masked={sp_f6.roll_transition.sum()}, "
          f"invalid_beta={sp_f6.meta['n_invalid_beta']}")
    print(f"  F5: n={len(sp_f5.s_close)}, roll_masked={sp_f5.roll_transition.sum()}, "
          f"invalid_beta={sp_f5.meta['n_invalid_beta']}")

    # ── 5. Evaluate (full + OOS) ───────────────────────────────────────────────
    print(f"\nRunning evaluate_v2 (N={N_DRAWS} surrogates × 2 families × 2 windows = ~{N_DRAWS*2*2} draws)...")

    results_f6 = eval_full_and_oos(sp_f6, n_is)
    results_f5 = eval_full_and_oos(sp_f5, n_is)

    # ── 6. Print results ───────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("RESULTS:")
    for fname, res in [("F6 (β=1.0)", results_f6), ("F5 (pre-sample OLS)", results_f5)]:
        print(f"\n  {fname}:")
        for period in ("full", "oos"):
            s = _summarise(res[period])
            confirm = "CONFIRM" if s["confirmed_rw_garch_ma1"] else "NO_CONFIRM"
            print(f"    {period.upper():4s}: {confirm}  "
                  f"VR(20)={s['vr']['20']}  "
                  f"p_rw={s['p_rw']:.3f}  p_garch={s['p_garch']:.3f}  "
                  f"p_ma1={s['p_ma1']:.3f}  p_ou={s['p_ou']:.3f}")
            print(f"          VR(q): {s['vr']}")

    # ── 7. Cycle-2 verdict ─────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    cycle2_confirm = (
        results_f6["full"]["confirmed_gate_rw_garch_ma1"] or
        results_f5["full"]["confirmed_gate_rw_garch_ma1"]
    )
    oos_confirm = (
        results_f6["oos"]["confirmed_gate_rw_garch_ma1"] or
        results_f5["oos"]["confirmed_gate_rw_garch_ma1"]
    )
    print(f"Cycle-2 CONFIRM (≥1 family, full period): {'YES' if cycle2_confirm else 'NO'}")
    print(f"OOS  CONFIRM   (≥1 family, OOS period):  {'YES' if oos_confirm else 'NO'}")
    print(f"f_βupdate check: F6={f_bu_f6:.4f} F5={f_bu_f5:.4f} (both < τ={TAU_FUPDATE})")

    # Construction-controlled corroboration: F5 and F6 should agree in direction
    f6_vr20_full = results_f6["full"]["real_vr"][20]
    f5_vr20_full = results_f5["full"]["real_vr"][20]
    corroboration = "AGREE" if (f6_vr20_full < 1.0) == (f5_vr20_full < 1.0) else "DISAGREE"
    print(f"Construction-controlled corroboration (F6 vs F5): {corroboration}  "
          f"(F6 VR20={f6_vr20_full:.4f}, F5 VR20={f5_vr20_full:.4f})")

    # ── 8. Save results ────────────────────────────────────────────────────────
    def _make_serialisable(obj):
        if isinstance(obj, dict):
            return {k: _make_serialisable(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_make_serialisable(x) for x in obj]
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
        return obj

    out = {
        "meta": {
            "date_min": DATE_MIN, "date_max": DATE_MAX,
            "n_bars": n, "n_is": n_is, "n_oos": n_oos,
            "oos_split": OOS_SPLIT, "oos_start_date": oos_date,
            "gallons_per_barrel": GALLONS_PER_BARREL,
            "pre_sample_fraction": PRE_SAMPLE_FRACTION,
            "beta_f5_estimated": round(beta_f5_val, 6),
            "f_betaupdate_f6": round(float(f_bu_f6), 6),
            "f_betaupdate_f5": round(float(f_bu_f5), 6),
            "tau_fupdate": TAU_FUPDATE,
            "jump_k": JUMP_K, "jump_window": JUMP_W,
            "n_draws": N_DRAWS, "seed": SEED_REAL,
            "n_roll_masked_f6": int(sp_f6.roll_transition.sum()),
            "n_roll_masked_f5": int(sp_f5.roll_transition.sum()),
        },
        "cycle2_confirm_full": bool(cycle2_confirm),
        "cycle2_confirm_oos": bool(oos_confirm),
        "corroboration": corroboration,
        "F6": _make_serialisable(results_f6),
        "F5": _make_serialisable(results_f5),
    }
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2, allow_nan=True)
    print(f"\nResults written to: {OUT_PATH}")
