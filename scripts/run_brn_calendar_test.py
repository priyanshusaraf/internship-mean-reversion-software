"""
BRN M1-M2 Daily Calendar Test — executes brn_calendar_prereg.md EXACTLY.
Phase 1: surrogate-relative VR(q) at N=200 speed gate; if survives, N=500 full + Tier-1 book sim.
Writes data/processed/brn_results.json with full search.

FROZEN PARAMETERS (from brn_calendar_prereg.md):
  DATE_MIN = 1997-10-22, DATE_MAX = 2026-06-04
  SPREAD = BRN1! - BRN2! (β=1 definitional, inner join on UTC date)
  JUMP_K = 8.0 (ADR_003 roll-masking via increment_jump_mask)
  SEED = 20260604
  Q_GRID = (5, 10, 20, 40, 60) — primary statistic VR(20)
  SPEED_GATE_N = 200, KILL_PVAL = 0.20
  FULL_N = 500
  COST_GRID = (0.003, 0.005, 0.008)
  HALF_LIFE_BAND = (5, 60) bars
  CRISIS_YEARS = {2020, 2022}
  ENTRY_Z = 1.0, STOP_BARS = 20, LOOKBACK = 60

DO NOT MODIFY analytics_arm_a.py or analytics_arm_a_v2.py.
"""
from __future__ import annotations
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import numpy as np
import pandas as pd

from app.services.analytics_arm_a import (
    Spread, level_vr, surrogate_vr_ensemble, _valid_increment_mask,
    VR_Q_GRID,
)
from app.services.analytics_arm_a_v2 import (
    spread_from_series, deseasonalize_causal, ma1_vr_ensemble,
    _fit_ma1noise, _family_pvalue, SEED, JUMP_W,
    increment_jump_mask,
)

# ── FROZEN PARAMETERS (do not change after this line) ──────────────────────────
DATE_MIN = "1997-10-22"
DATE_MAX = "2026-06-04"
JUMP_K = 8.0
BRN_SEED = 20260604
Q_GRID = (5, 10, 20, 40, 60)   # extended grid; primary = VR(20)
SPEED_GATE_N = 200
SPEED_GATE_KILL_PVAL = 0.20
FULL_N = 500
COST_GRID = (0.003, 0.005, 0.008)
PRIMARY_COST = 0.005
HALF_LIFE_BAND = (5.0, 60.0)   # bars
CRISIS_YEARS = {2020, 2022}
ENTRY_Z = 1.0
STOP_BARS = 20
LOOKBACK = 60
SURR_PCTILE = 5.0


# ── Unix-timestamp-aware leg loader (BRN TVView export format) ──────────────────

def load_leg_unix(path: str) -> pd.DataFrame:
    """Load TradingView CSV where `time` is a Unix epoch integer (seconds).
    Returns DataFrame indexed by UTC DatetimeTZDtype, ascending, deduped.
    Does NOT modify load_leg — this is a standalone loader for the Unix format."""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["ts"] = pd.to_datetime(df["time"], unit="s", utc=True, errors="coerce")
    df = df.dropna(subset=["ts"]).sort_values("ts")
    df = df.drop_duplicates(subset=["ts"], keep="last").set_index("ts")
    for col in ("open", "high", "low", "close"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    keep = [c for c in ("open", "high", "low", "close") if c in df.columns]
    return df[keep]


# ── Build BRN spread DataFrame (β=1 definitional) ──────────────────────────────

def build_brn_spread(brn1_path: str, brn2_path: str, date_min: str, date_max: str) -> pd.DataFrame:
    """Load BRN1! and BRN2!, inner-join on UTC date, compute spread = close_1 - close_2."""
    brn1 = load_leg_unix(brn1_path)
    brn2 = load_leg_unix(brn2_path)
    # Inner join on UTC datetime index
    joined = brn1.join(brn2, how="inner", lsuffix="_1", rsuffix="_2")
    joined = joined[(joined.index >= pd.Timestamp(date_min, tz="UTC")) &
                    (joined.index <= pd.Timestamp(date_max, tz="UTC"))]
    # Spread = BRN1! close - BRN2! close (β=1 definitional)
    s_close = joined["close_1"] - joined["close_2"]
    s_open = joined.get("open_1", joined["close_1"]) - joined.get("open_2", joined["close_2"])
    spread_df = pd.DataFrame({
        "open":  s_open.values,
        "close": s_close.values,
    }, index=joined.index)
    spread_df = spread_df.dropna(subset=["close"])
    return spread_df


# ── VR test with custom N (without calling evaluate_v2 which uses frozen N=200) ─

def evaluate_brn_vr(spread: Spread, n_draws: int, seed: int = BRN_SEED) -> dict:
    """Surrogate-relative VR(q) test on a BRN spread. Returns full result dict.
    Uses Q_GRID = (5,10,20,40,60) — the extended grid for the prereg.
    Primary statistic: VR(20). Headline: RW ∧ GARCH ∧ MA(1). OU non-gating reference."""
    qs = Q_GRID
    invalid = spread.roll_transition | ~np.isfinite(spread.beta)
    real = level_vr(spread.s_close, invalid, qs)
    real_vr = {q: real[q]["vr"] for q in qs}
    real_min = float(np.nanmin([real_vr[q] for q in qs])) if any(np.isfinite(real_vr[q]) for q in qs) else float("nan")
    per_family = {}
    for fam in ("rw", "garch", "ou"):
        ens = surrogate_vr_ensemble(spread, fam, qs=qs, n_draws=n_draws, seed=seed)
        per_family[fam] = _family_pvalue(ens, qs, real_vr, real_min)
    ma1_ens, ma1_params = ma1_vr_ensemble(spread, qs=qs, n_draws=n_draws, seed=seed)
    per_family["ma1"] = _family_pvalue(ma1_ens, qs, real_vr, real_min)
    per_family["ma1"]["fit"] = ma1_params
    sep = {f: per_family[f]["separated_corrected"] for f in ("rw", "garch", "ma1", "ou")}
    confirmed_gate = sep["rw"] and sep["garch"] and sep["ma1"]
    return {
        "real_vr": {str(q): round(float(real_vr[q]), 5) for q in qs},
        "real_min_vr": round(float(real_min), 5),
        "p_rw": round(float(per_family["rw"]["min_vr_p_value"]), 4),
        "p_garch": round(float(per_family["garch"]["min_vr_p_value"]), 4),
        "p_ma1": round(float(per_family["ma1"]["min_vr_p_value"]), 4),
        "p_ou": round(float(per_family["ou"]["min_vr_p_value"]), 4),
        "confirmed_rw_garch_ma1": bool(confirmed_gate),
        "sep": sep,
        "per_family_detail": {
            f: {
                "min_vr_p_value": round(float(per_family[f]["min_vr_p_value"]), 4),
                "separated": bool(per_family[f]["separated_corrected"]),
                "per_horizon": {
                    str(q): {
                        "p5": round(float(per_family[f]["per_horizon"][q]["p5"]), 5),
                        "real_below_p5": bool(per_family[f]["per_horizon"][q]["real_below_p5"]),
                        "surr_median": round(float(per_family[f]["per_horizon"][q]["surr_median"]), 5),
                    }
                    for q in qs
                },
            }
            for f in ("rw", "garch", "ma1", "ou")
        },
        "ma1_fit": {k: round(float(v), 6) for k, v in ma1_params.items()},
        "n_draws": n_draws,
        "seed": seed,
    }


# ── Half-life (AR1) ─────────────────────────────────────────────────────────────

def compute_half_life(s: np.ndarray) -> float:
    s = np.asarray(s, float)
    finite = s[np.isfinite(s)]
    if len(finite) < 30:
        return float("nan")
    x0, x1 = finite[:-1], finite[1:]
    X = np.column_stack([np.ones_like(x0), x0])
    coef, *_ = np.linalg.lstsq(X, x1, rcond=None)
    phi = float(coef[1])
    if 0 < phi < 1:
        return float(np.log(0.5) / np.log(phi))
    return float("inf")


# ── Per-window VR(20) z-score (doc-22 / doc-23 frame) ──────────────────────────

def window_vr20_z(s_close: np.ndarray, n_draws: int = SPEED_GATE_N, seed: int = BRN_SEED) -> dict:
    n = len(s_close)
    if n < 100:
        return {"vr20": float("nan"), "z": float("nan"), "below_rwmed": False, "n": n}
    sp = Spread(
        name="w", s_close=np.asarray(s_close, float),
        s_open=np.asarray(s_close, float).copy(),
        beta=np.ones(n), roll_transition=np.zeros(n, bool),
        flat_bar=np.zeros(n, bool),
        index=pd.date_range("2000-01-03", periods=n, freq="B", tz="UTC"),
        meta={},
    )
    vr = level_vr(sp.s_close, sp.roll_transition, (20,))
    vr20 = vr[20]["vr"]
    ens = surrogate_vr_ensemble(sp, "rw", qs=(20,), n_draws=n_draws, seed=seed)[20]
    ens = ens[np.isfinite(ens)]
    mu, sd = float(np.mean(ens)), float(np.std(ens) + 1e-9)
    rwmed = float(np.median(ens))
    return {
        "vr20": round(float(vr20), 4),
        "z": round(float((vr20 - mu) / sd), 3),
        "below_rwmed": bool(vr20 < rwmed),
        "n": int(n),
    }


# ── Causal z-entry trade proxy ──────────────────────────────────────────────────

def trade_proxy(s: np.ndarray, cost: float = PRIMARY_COST) -> dict:
    s = np.asarray(s, float)
    n = len(s)
    pnls, gross_pnls = [], []
    in_pos = 0; entry_px = 0.0; bars_held = 0
    for t in range(LOOKBACK, n):
        win = s[t - LOOKBACK:t]
        mu, sd_ = win.mean(), win.std() + 1e-9
        z = (s[t] - mu) / sd_
        if in_pos == 0:
            if z >= ENTRY_Z:   in_pos = +1; entry_px = s[t]; bars_held = 0
            elif z <= -ENTRY_Z: in_pos = -1; entry_px = s[t]; bars_held = 0
        else:
            bars_held += 1
            zc = (s[t] - mu) / sd_
            cross0 = (in_pos == +1 and zc <= 0) or (in_pos == -1 and zc >= 0)
            if cross0 or bars_held >= STOP_BARS:
                gross = in_pos * (entry_px - s[t])
                pnls.append(gross - cost)
                gross_pnls.append(gross)
                in_pos = 0
    if len(pnls) == 0:
        return {"n_trades": 0, "avg_net": float("nan"), "avg_gross": float("nan"),
                "hit_rate": float("nan"), "total_net": float("nan")}
    pnls_arr = np.array(pnls)
    gross_arr = np.array(gross_pnls)
    # Episode jackknife: drop 3 largest gross trades
    top3_idx = np.argsort(np.abs(gross_arr))[-3:]
    mask = np.ones(len(pnls_arr), bool); mask[top3_idx] = False
    jk_gross = float(np.mean(gross_arr[mask])) if mask.sum() > 0 else float("nan")
    jk_net = float(np.mean(pnls_arr[mask])) if mask.sum() > 0 else float("nan")
    return {
        "n_trades": int(len(pnls_arr)),
        "avg_net": round(float(pnls_arr.mean()), 6),
        "avg_gross": round(float(gross_arr.mean()), 6),
        "hit_rate": round(float(np.mean(pnls_arr > 0)), 4),
        "total_net": round(float(pnls_arr.sum()), 6),
        "jackknife_avg_gross": round(float(jk_gross), 6),
        "jackknife_avg_net": round(float(jk_net), 6),
        "jackknife_retention_pct": round(100 * jk_gross / max(abs(gross_arr.mean()), 1e-9), 1) if gross_arr.mean() != 0 else float("nan"),
    }


# ── Rolling-local book sim (pooled mean-z + cost-aware, doc-23 frame) ───────────

def rolling_book_sim(s: np.ndarray, index: pd.DatetimeIndex, n_rw: int = SPEED_GATE_N) -> dict:
    """Yearly windows (primary), pooled mean-z, crisis isolation, full cost grid."""
    years = index.year.to_numpy()
    all_years = sorted(set(years))
    # Only full years with ≥ 100 bars
    yearly_windows = []
    for Y in all_years:
        seg_idx = np.where(years == Y)[0]
        if len(seg_idx) < 100:
            continue
        seg_s = s[seg_idx]
        winfo = window_vr20_z(seg_s, n_draws=n_rw, seed=BRN_SEED)
        hl = compute_half_life(seg_s)
        proxy = trade_proxy(seg_s, cost=PRIMARY_COST)
        proxies_all_costs = {str(c): trade_proxy(seg_s, cost=c) for c in COST_GRID}
        yearly_windows.append({
            "year": int(Y),
            "is_crisis": bool(Y in CRISIS_YEARS),
            **winfo,
            "half_life": round(float(hl), 1),
            "trade_proxy": proxy,
            "trade_proxy_cost_grid": proxies_all_costs,
        })

    def pooled_stats(windows: list[dict]) -> dict:
        zs = [w["z"] for w in windows if np.isfinite(w["z"])]
        if not zs:
            return {"mean_z": float("nan"), "n_windows": 0, "n_below_rwmed": 0,
                    "z_trajectory": [], "vr20_trajectory": []}
        below = sum(w["below_rwmed"] for w in windows)
        avg_gross = {str(c): round(np.nanmean([w["trade_proxy_cost_grid"][str(c)]["avg_gross"]
                                               for w in windows if w["trade_proxy_cost_grid"][str(c)]["n_trades"] > 0]), 6)
                    if any(w["trade_proxy_cost_grid"][str(c)]["n_trades"] > 0 for w in windows)
                    else float("nan")
                    for c in COST_GRID}
        avg_net = {str(c): round(np.nanmean([w["trade_proxy_cost_grid"][str(c)]["avg_net"]
                                             for w in windows if w["trade_proxy_cost_grid"][str(c)]["n_trades"] > 0]), 6)
                  if any(w["trade_proxy_cost_grid"][str(c)]["n_trades"] > 0 for w in windows)
                  else float("nan")
                  for c in COST_GRID}
        return {
            "mean_z": round(float(np.mean(zs)), 4),
            "n_windows": len(zs),
            "n_below_rwmed": int(below),
            "avg_gross_by_cost": avg_gross,
            "avg_net_by_cost": avg_net,
            "z_trajectory": [round(w["z"], 3) for w in windows],
            "vr20_trajectory": [round(w["vr20"], 3) for w in windows],
            "year_list": [w["year"] for w in windows],
        }

    non_crisis = [w for w in yearly_windows if not w["is_crisis"]]
    crisis_only = [w for w in yearly_windows if w["is_crisis"]]

    return {
        "full_sample": pooled_stats(yearly_windows),
        "ex_crisis": pooled_stats(non_crisis),
        "crisis_only": pooled_stats(crisis_only),
        "yearly_detail": [
            {k: v for k, v in w.items() if k != "trade_proxy_cost_grid"}
            | {"cost_grid_gross": {str(c): w["trade_proxy_cost_grid"][str(c)]["avg_gross"] for c in COST_GRID},
               "cost_grid_net": {str(c): w["trade_proxy_cost_grid"][str(c)]["avg_net"] for c in COST_GRID}}
            for w in yearly_windows
        ],
    }


# ── OOS split (70/30 by date) ───────────────────────────────────────────────────

def oos_split_vr20(spread: Spread, n_draws: int = SPEED_GATE_N, seed: int = BRN_SEED) -> dict:
    n = len(spread.s_close)
    train_n = int(n * 0.70)
    s_train = spread.s_close[:train_n]
    s_oos = spread.s_close[train_n:]
    vr_train = level_vr(s_train, np.zeros(train_n, bool), (20,))[20]["vr"]
    vr_oos = level_vr(s_oos, np.zeros(len(s_oos), bool), (20,))[20]["vr"]
    return {
        "vr20_train": round(float(vr_train), 5),
        "vr20_oos": round(float(vr_oos), 5),
        "sign_flip": bool(vr_oos > vr_train + 0.15),
        "train_n": train_n,
        "oos_n": len(s_oos),
    }


# ── MAIN ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    np.seterr(all="ignore")
    base = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(base, "..")
    DATA_DIR = os.path.join(root, "data", "raw", "more-mean-reversion-data")
    OUT_PATH = os.path.join(root, "data", "processed", "brn_results.json")

    print("=" * 80)
    print("BRN M1-M2 Calendar Test — executing brn_calendar_prereg.md")
    print(f"Frozen seed={BRN_SEED}, jump_k={JUMP_K}, date_min={DATE_MIN}, date_max={DATE_MAX}")
    print("=" * 80)

    # Step 1: Build spread
    print("\n[1] Building β=1 BRN1!−BRN2! spread...")
    brn1_path = os.path.join(DATA_DIR, "ICEEUR_DLY_BRN1!, 1D.csv")
    brn2_path = os.path.join(DATA_DIR, "ICEEUR_DLY_BRN2!, 1D.csv")
    spread_df = build_brn_spread(brn1_path, brn2_path, DATE_MIN, DATE_MAX)
    print(f"  Spread rows: {len(spread_df)}, {spread_df.index[0].date()} → {spread_df.index[-1].date()}")
    print(f"  Spread stats: mean={spread_df['close'].mean():.3f}, std={spread_df['close'].std():.3f}, "
          f"min={spread_df['close'].min():.3f}, max={spread_df['close'].max():.3f}")

    # Step 2: Wrap in Spread object with jump masking (k=8.0)
    print(f"\n[2] Wrapping with spread_from_series (jump_k={JUMP_K})...")
    brn_spread_raw = spread_from_series("BRN_M1M2", spread_df, jump_k=JUMP_K)
    print(f"  Roll-masked bars: {int(brn_spread_raw.roll_transition.sum())} of {len(brn_spread_raw.s_close)}")
    print(f"  Flat bars: {int(brn_spread_raw.flat_bar.sum())}")

    # Step 3: Deseasonalize (causal trailing month-of-year mean)
    print("\n[3] Causal deseasonalization...")
    s_deseason = deseasonalize_causal(brn_spread_raw.s_close, brn_spread_raw.index)
    # Wrap deseasonalized series into a new Spread
    brn_spread = Spread(
        name="BRN_M1M2_deseason",
        s_close=s_deseason,
        s_open=s_deseason.copy(),
        beta=brn_spread_raw.beta,
        roll_transition=brn_spread_raw.roll_transition,
        flat_bar=brn_spread_raw.flat_bar,
        index=brn_spread_raw.index,
        meta=brn_spread_raw.meta,
    )

    # Step 4: Half-life
    hl_global = compute_half_life(s_deseason)
    print(f"  Global half-life: {hl_global:.1f} bars")
    in_band = HALF_LIFE_BAND[0] <= hl_global <= HALF_LIFE_BAND[1]
    print(f"  Tradeable band [{HALF_LIFE_BAND[0]}, {HALF_LIFE_BAND[1]}]: {'PASS' if in_band else 'FAIL'}")

    # Step 5: SPEED GATE — N=200
    print(f"\n[4] SPEED GATE: VR(q) at N={SPEED_GATE_N}...")
    speed_result = evaluate_brn_vr(brn_spread, n_draws=SPEED_GATE_N, seed=BRN_SEED)
    p_rw_200 = speed_result["p_rw"]
    print(f"  VR(20) = {speed_result['real_vr']['20']:.4f}")
    print(f"  p_rw(N=200) = {p_rw_200:.4f}  [KILL threshold: > {SPEED_GATE_KILL_PVAL}]")
    vr_profile_str = ', '.join('q=%d:%.4f' % (q, speed_result["real_vr"][str(q)]) for q in Q_GRID)
    print(f"  VR profile: {vr_profile_str}")

    speed_gate_killed = (p_rw_200 > SPEED_GATE_KILL_PVAL) or (speed_result["real_vr"]["20"] >= 1.0)
    if speed_gate_killed:
        if speed_result["real_vr"]["20"] >= 1.0:
            print(f"  *** KILL: VR(20) >= 1.0 (VR={speed_result['real_vr']['20']:.4f}) — no MR signal ***")
            kill_reason = f"VR(20)={speed_result['real_vr']['20']:.4f} >= 1.0"
        else:
            print(f"  *** KILL: p_rw={p_rw_200:.4f} > {SPEED_GATE_KILL_PVAL} at N=200 — cannot reach significance at N=500 ***")
            kill_reason = f"p_rw={p_rw_200:.4f} > {SPEED_GATE_KILL_PVAL} at N=200"

    # Step 6: OOS split
    oos = oos_split_vr20(brn_spread, n_draws=SPEED_GATE_N, seed=BRN_SEED)
    print(f"\n[5] OOS split (70/30 by date):")
    print(f"  VR(20) train={oos['vr20_train']:.4f}, OOS={oos['vr20_oos']:.4f}, sign_flip={oos['sign_flip']}")

    # Step 7: Rolling-local book sim (even if speed gate killed — report for adjudication)
    print(f"\n[6] Rolling-local book sim (doc-23 frame, crisis isolation)...")
    book_sim = rolling_book_sim(s_deseason, brn_spread.index, n_rw=SPEED_GATE_N)
    print(f"  Full-sample pooled mean-z = {book_sim['full_sample']['mean_z']:.4f} ({book_sim['full_sample']['n_windows']} windows)")
    print(f"  Ex-crisis pooled mean-z = {book_sim['ex_crisis']['mean_z']:.4f} ({book_sim['ex_crisis']['n_windows']} windows)")
    ex_gross_005 = book_sim["ex_crisis"]["avg_gross_by_cost"].get("0.005", float("nan"))
    ex_net_005 = book_sim["ex_crisis"]["avg_net_by_cost"].get("0.005", float("nan"))
    print(f"  Ex-crisis avg gross @K=0.005: {ex_gross_005:.6f}, avg net: {ex_net_005:.6f}")

    # Step 8: Full N=500 (only if speed gate passes)
    full_result = None
    if not speed_gate_killed:
        print(f"\n[7] FULL TEST: VR(q) at N={FULL_N}...")
        full_result = evaluate_brn_vr(brn_spread, n_draws=FULL_N, seed=BRN_SEED)
        p_rw_500 = full_result["p_rw"]
        print(f"  VR(20) = {full_result['real_vr']['20']:.4f}")
        print(f"  p_rw(N=500) = {p_rw_500:.4f}  [significance threshold: <= 0.05]")
        print(f"  p_garch={full_result['p_garch']:.4f}, p_ma1={full_result['p_ma1']:.4f}, p_ou={full_result['p_ou']:.4f}")
        print(f"  RW∧GARCH∧MA(1) gate: {'PASS' if full_result['confirmed_rw_garch_ma1'] else 'FAIL'}")
    else:
        print(f"\n[7] Full N={FULL_N} test SKIPPED (speed gate killed).")

    # Step 9: Trader gate evaluation
    print("\n[8] Trader gate evaluation:")
    trader_pass = False
    trader_verdict = "N/A"
    if not speed_gate_killed:
        p_rw_full = full_result["p_rw"] if full_result else float("nan")
        quant_pass = (p_rw_full <= 0.05) and (full_result["real_vr"]["20"] < 1.0) if full_result else False
        quant_borderline = (0.05 < p_rw_full <= 0.20) if full_result else False
        jk_detail = []
        for w in book_sim["yearly_detail"]:
            if not w["is_crisis"] and w["trade_proxy"]["n_trades"] > 0:
                jk_detail.append(w["trade_proxy"].get("jackknife_avg_gross", float("nan")))
        pooled_jk_gross = float(np.nanmean(jk_detail)) if jk_detail else float("nan")
        gross_clears = float(ex_gross_005) >= PRIMARY_COST if np.isfinite(ex_gross_005) else False
        hl_in_band = HALF_LIFE_BAND[0] <= hl_global <= HALF_LIFE_BAND[1]
        jk_stable = (abs(pooled_jk_gross) >= 0.5 * abs(float(ex_gross_005))) if (np.isfinite(pooled_jk_gross) and np.isfinite(ex_gross_005) and ex_gross_005 != 0) else False
        print(f"  Quant gate (p_rw<=0.05): {'PASS' if quant_pass else ('BORDERLINE' if quant_borderline else 'FAIL')}")
        print(f"  Ex-crisis avg gross @0.005: {ex_gross_005:.6f} >= 0.005? {'YES' if gross_clears else 'NO'}")
        print(f"  Half-life {hl_global:.1f} in [{HALF_LIFE_BAND[0]},{HALF_LIFE_BAND[1]}]? {'YES' if hl_in_band else 'NO'}")
        print(f"  Jackknife pooled gross: {pooled_jk_gross:.6f}, stable (>=50% of gross)? {'YES' if jk_stable else 'NO'}")
        if quant_pass and gross_clears and hl_in_band and jk_stable:
            trader_verdict = "SLEEVE_CANDIDATE"
            trader_pass = True
        elif quant_pass or quant_borderline:
            trader_verdict = "MERELY_TRUE"
        else:
            trader_verdict = "DEAD_CALENDAR_VR"
    else:
        trader_verdict = "DEAD_CALENDAR_SPEED_GATE"

    # Final verdict
    if speed_gate_killed:
        final_verdict = "DEAD_CALENDAR"
        verdict_reason = kill_reason
    elif trader_verdict == "SLEEVE_CANDIDATE":
        final_verdict = "SLEEVE_CANDIDATE"
        verdict_reason = f"quant+trader both pass: p_rw={full_result['p_rw']:.4f}, gross={ex_gross_005:.6f}, hl={hl_global:.1f}"
    elif "MERELY_TRUE" in trader_verdict:
        final_verdict = "MERELY_TRUE"
        verdict_reason = f"MR confirmed but sub-cost or non-deployable"
    else:
        final_verdict = "DEAD_CALENDAR"
        verdict_reason = trader_verdict

    print(f"\n{'='*80}")
    print(f"VERDICT: {final_verdict}")
    print(f"REASON:  {verdict_reason}")
    print(f"{'='*80}")

    # Assemble output
    out = {
        "meta": {
            "instrument": "BRN_M1M2",
            "prereg_doc": "brn_calendar_prereg.md",
            "date_min": DATE_MIN,
            "date_max": DATE_MAX,
            "n_bars": len(brn_spread.s_close),
            "seed": BRN_SEED,
            "jump_k": JUMP_K,
            "q_grid": list(Q_GRID),
            "cost_grid": list(COST_GRID),
            "primary_cost": PRIMARY_COST,
            "half_life_band": list(HALF_LIFE_BAND),
            "crisis_years": sorted(CRISIS_YEARS),
            "speed_gate_n": SPEED_GATE_N,
            "full_n": FULL_N,
            "execution_date": "2026-06-05",
        },
        "spread_stats": {
            "mean": round(float(spread_df["close"].mean()), 4),
            "std": round(float(spread_df["close"].std()), 4),
            "min": round(float(spread_df["close"].min()), 4),
            "max": round(float(spread_df["close"].max()), 4),
            "n_roll_masked": int(brn_spread_raw.roll_transition.sum()),
            "n_flat": int(brn_spread_raw.flat_bar.sum()),
        },
        "global_half_life_bars": round(float(hl_global), 2),
        "half_life_in_band": bool(in_band),
        "oos_split": oos,
        "speed_gate_N200": speed_result,
        "speed_gate_killed": bool(speed_gate_killed),
        "speed_gate_kill_reason": kill_reason if speed_gate_killed else None,
        "full_N500": full_result,
        "rolling_book_sim": book_sim,
        "trader_gate": {
            "verdict": trader_verdict,
            "ex_crisis_gross_at_primary_cost": round(float(ex_gross_005), 6),
            "ex_crisis_net_at_primary_cost": round(float(ex_net_005), 6),
            "half_life_in_band": bool(in_band),
        },
        "final_verdict": final_verdict,
        "verdict_reason": verdict_reason,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2, allow_nan=True)
    print(f"\nResults written to: {OUT_PATH}")
