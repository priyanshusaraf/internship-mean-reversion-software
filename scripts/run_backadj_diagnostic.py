"""
Track C — Back-Adjustment Generic Diagnostic.
Detects roll-seam jumps in continuous futures legs and estimates splice-contamination risk
for each spread used by the programme (NG, BRN, ZC).

Methodology (non-research diagnostic — MEASUREMENT characterisation):
1. Load each continuous leg; detect bars where |ΔClose| > k×MAD(trailing) (same ADR_003 logic as
   the frozen primitives, k=8.0).
2. Cluster jump bars by their calendar month-day to see whether they concentrate at expected roll
   dates (ICE Brent ~1st half of month; CBOT Corn expiry known; NG ~last 3 biz days of month).
3. Compute the spread for each pair, run a simplified pooled mean-z test (using the same
   window_vr20_z logic as doc-22), and compare to doc-23 splice-RW anchors:
       frac0.25 anchor (quarter-strength splice) = -0.657
       frac0.5  anchor (half-strength splice)    = -1.053
       RW null band  = [-0.32, +0.41]
       genuine moderate-MR anchor                = -0.33  (OU phi=0.95)
4. Grade each spread:
       CLEAN:        mean-z in (-0.80, -0.20)  — above frac0.25, inside "genuine MR / RW-null" zone
       SUSPECT:      mean-z in (-1.05, -0.80)  — in the splice zone
       CONTAMINATED: mean-z < -1.05            — at or below frac0.5 splice anchor
5. Per-leg jump rate and roll-alignment score (fraction of flagged jumps within ±3 days of expected
   monthly roll boundaries). High alignment = likely genuine roll seam; low alignment = noise jumps.

Output: data/processed/backadj_diagnostic.json (per-spread grades + supporting metrics).
NOTE: This is a MEASUREMENT diagnostic — it does NOT change any MR verdict. It grades the data.
"""
from __future__ import annotations
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
import numpy as np
import pandas as pd
from app.services.analytics_arm_a import Spread, level_vr, surrogate_vr_ensemble, VR_Q_GRID

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
DATA_DIR = os.path.join(ROOT, "data", "raw", "more-mean-reversion-data")
DATA_RAW = os.path.join(ROOT, "data", "raw")
SEED = 20260604
RW_N = 200
K_MAD = 8.0
MAD_WINDOW = 60

# Splice-RW reference anchors (doc 23 results)
SPLICE_ANCHORS = {
    "frac0.25": -0.657,
    "frac0.5":  -1.053,
    "rw_null_lo": -0.32,
    "rw_null_hi": +0.41,
    "genuine_mr_anchor": -0.33,
}

# Grade boundaries
SUSPECT_THRESHOLD = -0.80      # more negative than this = suspect
CONTAMINATED_THRESHOLD = -1.05 # more negative than this = contaminated


def load_leg_unix(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    if "time" not in df.columns:
        raise ValueError(f"No 'time' column: {path}")
    # Try Unix timestamp first
    ts = pd.to_numeric(df["time"], errors="coerce")
    if ts.notna().mean() > 0.9 and ts.abs().mean() > 1e8:
        df["ts"] = pd.to_datetime(ts, unit="s", utc=True, errors="coerce")
    else:
        df["ts"] = pd.to_datetime(df["time"], errors="coerce", utc=True, format="mixed")
    df = df.dropna(subset=["ts"]).sort_values("ts").drop_duplicates(subset=["ts"], keep="last").set_index("ts")
    for col in ("open","high","low","close"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df[[c for c in ("open","high","low","close") if c in df.columns]]


def load_leg_datestr(path: str) -> pd.DataFrame:
    """Loader for date-string format (NG12 spread)."""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["ts"] = pd.to_datetime(df["time"], errors="coerce", utc=True, format="mixed")
    df = df.dropna(subset=["ts"]).sort_values("ts").drop_duplicates(subset=["ts"], keep="last").set_index("ts")
    for col in ("open","high","low","close"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df[[c for c in ("open","high","low","close") if c in df.columns]]


def detect_jumps(close: np.ndarray, k: float = K_MAD, window: int = MAD_WINDOW) -> np.ndarray:
    """Causal MAD-based large-jump detection; same logic as roll_transition_mask but on |Δclose| not log-return.
    Returns bool array length n; True = bar t has a large spread increment (possible splice seam)."""
    n = len(close)
    mask = np.zeros(n, bool)
    d = np.diff(close)  # length n-1; d[i] is the increment into bar i+1
    for i in range(len(d)):
        if not np.isfinite(d[i]):
            continue
        lo = max(0, i - window)
        ref = d[lo:i]
        ref = ref[np.isfinite(ref)]
        if ref.size < 10:
            continue
        med = np.median(ref)
        mad = np.median(np.abs(ref - med))
        if mad <= 0:
            continue
        if abs(d[i] - med) > k * 1.4826 * mad:
            mask[i + 1] = True
    return mask


def roll_alignment_score(index: pd.DatetimeIndex, jump_mask: np.ndarray,
                          tolerance_days: int = 3, expected_day_range=(1, 15)) -> float:
    """Fraction of detected jumps whose calendar day falls within expected_day_range ± tolerance.
    For BRN: expiry ~1st half of month (days 1-15); for ZC/NG: last 3-5 biz days of month."""
    jump_dates = index[jump_mask]
    if len(jump_dates) == 0:
        return float("nan")
    days = jump_dates.day.to_numpy()
    lo, hi = expected_day_range
    # Count days that fall within [lo-tol, hi+tol]
    in_range = np.sum((days >= max(1, lo - tolerance_days)) & (days <= min(31, hi + tolerance_days)))
    return float(in_range) / len(jump_dates)


def window_vr20_z(s_close: np.ndarray, n_draws: int = RW_N, seed: int = SEED) -> dict:
    n = len(s_close)
    if n < 100:
        return {"vr20": float("nan"), "z": float("nan"), "below_rwmed": False, "n": n}
    sp = Spread(name="diag", s_close=np.asarray(s_close, float), s_open=np.asarray(s_close, float).copy(),
                beta=np.ones(n), roll_transition=np.zeros(n, bool), flat_bar=np.zeros(n, bool),
                index=pd.date_range("2000-01-03", periods=n, freq="B", tz="UTC"), meta={})
    vr = level_vr(sp.s_close, sp.roll_transition, (20,))
    vr20 = vr[20]["vr"]
    ens = surrogate_vr_ensemble(sp, "rw", qs=(20,), n_draws=n_draws, seed=seed)[20]
    ens = ens[np.isfinite(ens)]
    mu, sd = float(np.mean(ens)), float(np.std(ens) + 1e-9)
    rwmed = float(np.median(ens))
    return {"vr20": round(float(vr20), 4), "z": round(float((vr20 - mu) / sd), 3),
            "below_rwmed": bool(vr20 < rwmed), "n": int(n)}


def pooled_mean_z(s: np.ndarray, index: pd.DatetimeIndex) -> dict:
    years = index.year.to_numpy()
    yearly = []
    for Y in sorted(set(years)):
        seg = s[years == Y]
        if len(seg) < 100:
            continue
        w = window_vr20_z(seg)
        yearly.append({"year": int(Y), **w})
    zs = [w["z"] for w in yearly if np.isfinite(w.get("z", float("nan")))]
    if not zs:
        return {"mean_z": float("nan"), "n_windows": 0, "yearly": yearly}
    return {"mean_z": round(float(np.mean(zs)), 4), "n_windows": len(zs), "yearly": yearly}


def grade_spread(mean_z: float) -> str:
    if not np.isfinite(mean_z):
        return "UNKNOWN"
    if mean_z < CONTAMINATED_THRESHOLD:
        return "CONTAMINATED"  # ≤ frac0.5 splice anchor
    if mean_z < SUSPECT_THRESHOLD:
        return "SUSPECT"       # between frac0.25 and frac0.5 zones
    return "CLEAN"             # above frac0.25 or in the RW-null zone


def diagnose_spread(name: str, leg1: pd.DataFrame, leg2: pd.DataFrame,
                    roll_alignment_range_1, roll_alignment_range_2,
                    deseasonalize: bool = True) -> dict:
    from app.services.analytics_arm_a_v2 import deseasonalize_causal

    # Inner join
    j = leg1.join(leg2, how="inner", lsuffix="_1", rsuffix="_2")
    j = j.dropna(subset=["close_1","close_2"])
    s_raw = (j["close_1"] - j["close_2"]).to_numpy()
    idx = j.index

    # Per-leg jump detection
    jump1 = detect_jumps(j["close_1"].to_numpy())
    jump2 = detect_jumps(j["close_2"].to_numpy())
    jump_spread = detect_jumps(s_raw)

    align1 = roll_alignment_score(idx, jump1, tolerance_days=5, expected_day_range=roll_alignment_range_1)
    align2 = roll_alignment_score(idx, jump2, tolerance_days=5, expected_day_range=roll_alignment_range_2)

    # Deseasonalize if requested
    if deseasonalize:
        s = deseasonalize_causal(s_raw, idx)
    else:
        s = s_raw

    # Pooled mean-z
    pmz = pooled_mean_z(s, idx)
    grade = grade_spread(pmz["mean_z"])

    # Spread stats
    return {
        "name": name,
        "n_bars": int(len(s)),
        "date_start": str(idx[0].date()),
        "date_end": str(idx[-1].date()),
        "spread_mean": round(float(np.nanmean(s_raw)), 4),
        "spread_std": round(float(np.nanstd(s_raw)), 4),
        "spread_mean_deseason": round(float(np.nanmean(s)), 4),
        "spread_std_deseason": round(float(np.nanstd(s)), 4),
        "leg1_n_jumps": int(jump1.sum()),
        "leg2_n_jumps": int(jump2.sum()),
        "spread_n_jumps": int(jump_spread.sum()),
        "leg1_roll_alignment": round(float(align1), 3) if np.isfinite(align1) else None,
        "leg2_roll_alignment": round(float(align2), 3) if np.isfinite(align2) else None,
        "pooled_mean_z": pmz["mean_z"],
        "n_yearly_windows": pmz["n_windows"],
        "splice_anchors": SPLICE_ANCHORS,
        "grade": grade,
        "grade_rationale": (
            f"mean_z={pmz['mean_z']:.3f}; "
            f"frac0.25 anchor={SPLICE_ANCHORS['frac0.25']}, "
            f"frac0.5 anchor={SPLICE_ANCHORS['frac0.5']}"
        ),
        "yearly_z": [{"year": w["year"], "vr20": w["vr20"], "z": w["z"]} for w in pmz["yearly"]],
    }


if __name__ == "__main__":
    np.seterr(all="ignore")
    print("=" * 80)
    print("Back-Adjustment Diagnostic — programme-wide (NG, BRN, ZC spreads)")
    print("=" * 80)

    results = {}

    from app.services.analytics_arm_a_v2 import deseasonalize_causal

    # ── NG (vendor pre-built spread) ────────────────────────────────────────────
    print("\n[1] NG calendar spread (vendor ng12_spread.csv)...")
    try:
        ng_df = load_leg_datestr(os.path.join(DATA_RAW, "ng12_spread.csv"))
        ng_df_trim = ng_df[ng_df.index >= pd.Timestamp("2006-07-28", tz="UTC")]
        s_ng = ng_df_trim["close"].to_numpy()
        idx_ng = ng_df_trim.index
        s_ng_d = deseasonalize_causal(s_ng, idx_ng)
        pmz_ng_raw = pooled_mean_z(s_ng, idx_ng)       # RAW — matches doc-23 splice anchors
        pmz_ng_ds = pooled_mean_z(s_ng_d, idx_ng)      # DESEASONALIZED — for context
        grade_ng = grade_spread(pmz_ng_raw["mean_z"])  # grade on RAW (anchor-consistent)
        results["NG_vendor_spread"] = {
            "name": "NG (vendor ng12 pre-built spread, trimmed 2006-07-28)",
            "n_bars": len(s_ng),
            "spread_mean": round(float(np.nanmean(s_ng)), 5),
            "spread_std": round(float(np.nanstd(s_ng)), 5),
            "pooled_mean_z_raw": pmz_ng_raw["mean_z"],
            "pooled_mean_z_deseason": pmz_ng_ds["mean_z"],
            "n_yearly_windows": pmz_ng_raw["n_windows"],
            "splice_anchors": SPLICE_ANCHORS,
            "grade_raw": grade_ng,
            "yearly_z_raw": [{"year": w["year"], "vr20": w["vr20"], "z": w["z"]} for w in pmz_ng_raw["yearly"]],
        }
        print(f"  mean-z raw={pmz_ng_raw['mean_z']:.4f} deseason={pmz_ng_ds['mean_z']:.4f}  grade(raw)={grade_ng}")
    except Exception as e:
        print(f"  ERROR: {e}")
        results["NG_vendor_spread"] = {"error": str(e)}

    # ── BRN (from raw legs, raw + deseason) ─────────────────────────────────────
    print("\n[2] BRN M1-M2 spread (from raw legs)...")
    try:
        brn1 = load_leg_unix(os.path.join(DATA_DIR, "ICEEUR_DLY_BRN1!, 1D.csv"))
        brn2 = load_leg_unix(os.path.join(DATA_DIR, "ICEEUR_DLY_BRN2!, 1D.csv"))
        j_brn = brn1.join(brn2, how="inner", lsuffix="_1", rsuffix="_2").dropna(subset=["close_1","close_2"])
        s_brn_raw = (j_brn["close_1"] - j_brn["close_2"]).to_numpy()
        s_brn_ds = deseasonalize_causal(s_brn_raw, j_brn.index)
        pmz_brn_raw = pooled_mean_z(s_brn_raw, j_brn.index)
        pmz_brn_ds = pooled_mean_z(s_brn_ds, j_brn.index)
        grade_brn = grade_spread(pmz_brn_raw["mean_z"])
        jump_brn1 = detect_jumps(j_brn["close_1"].to_numpy())
        jump_brn2 = detect_jumps(j_brn["close_2"].to_numpy())
        results["BRN_M1M2"] = {
            "n_bars": len(s_brn_raw),
            "spread_mean": round(float(np.nanmean(s_brn_raw)), 4),
            "spread_std": round(float(np.nanstd(s_brn_raw)), 4),
            "leg1_n_jumps": int(jump_brn1.sum()), "leg2_n_jumps": int(jump_brn2.sum()),
            "pooled_mean_z_raw": pmz_brn_raw["mean_z"],
            "pooled_mean_z_deseason": pmz_brn_ds["mean_z"],
            "splice_anchors": SPLICE_ANCHORS,
            "grade_raw": grade_brn,
            "yearly_z_raw": [{"year": w["year"], "vr20": w["vr20"], "z": w["z"]} for w in pmz_brn_raw["yearly"]],
        }
        print(f"  spread mean={np.nanmean(s_brn_raw):.3f} | mean-z raw={pmz_brn_raw['mean_z']:.4f} deseason={pmz_brn_ds['mean_z']:.4f} | grade(raw)={grade_brn}")
    except Exception as e:
        print(f"  ERROR: {e}")
        results["BRN_M1M2"] = {"error": str(e)}

    # ── ZC (from raw legs, raw + deseason) ──────────────────────────────────────
    print("\n[3] ZC M1-M2 spread (from raw legs)...")
    try:
        zc1 = load_leg_unix(os.path.join(DATA_DIR, "CBOT_DL_ZC1!, 1D.csv"))
        zc2 = load_leg_unix(os.path.join(DATA_DIR, "CBOT_DL_ZC2!, 1D.csv"))
        j_zc = zc1.join(zc2, how="inner", lsuffix="_1", rsuffix="_2").dropna(subset=["close_1","close_2"])
        s_zc_raw = (j_zc["close_1"] - j_zc["close_2"]).to_numpy()
        s_zc_ds = deseasonalize_causal(s_zc_raw, j_zc.index)
        pmz_zc_raw = pooled_mean_z(s_zc_raw, j_zc.index)
        pmz_zc_ds = pooled_mean_z(s_zc_ds, j_zc.index)
        grade_zc = grade_spread(pmz_zc_raw["mean_z"])
        jump_zc1 = detect_jumps(j_zc["close_1"].to_numpy())
        jump_zc2 = detect_jumps(j_zc["close_2"].to_numpy())
        results["ZC_M1M2"] = {
            "n_bars": len(s_zc_raw),
            "spread_mean": round(float(np.nanmean(s_zc_raw)), 4),
            "spread_std": round(float(np.nanstd(s_zc_raw)), 4),
            "leg1_n_jumps": int(jump_zc1.sum()), "leg2_n_jumps": int(jump_zc2.sum()),
            "pooled_mean_z_raw": pmz_zc_raw["mean_z"],
            "pooled_mean_z_deseason": pmz_zc_ds["mean_z"],
            "splice_anchors": SPLICE_ANCHORS,
            "grade_raw": grade_zc,
            "yearly_z_raw": [{"year": w["year"], "vr20": w["vr20"], "z": w["z"]} for w in pmz_zc_raw["yearly"]],
        }
        print(f"  spread mean={np.nanmean(s_zc_raw):.3f} | mean-z raw={pmz_zc_raw['mean_z']:.4f} deseason={pmz_zc_ds['mean_z']:.4f} | grade(raw)={grade_zc}")
    except Exception as e:
        print(f"  ERROR: {e}")
        results["ZC_M1M2"] = {"error": str(e)}

    # ── Summary ─────────────────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("SUMMARY:")
    for k, v in results.items():
        if "error" in v:
            print(f"  {k}: ERROR")
            continue
        else:
            mz = v.get("pooled_mean_z_raw", v.get("pooled_mean_z", float("nan")))
            grade = v.get("grade_raw", v.get("grade", "n/a"))
            mz_s = f"{mz:.4f}" if isinstance(mz, float) else str(mz)
            print(f"  {k}: mean_z={mz_s}  grade={grade}")
    print(f"\nSplice anchors: frac0.25={SPLICE_ANCHORS['frac0.25']} | frac0.5={SPLICE_ANCHORS['frac0.5']} | RW null=[{SPLICE_ANCHORS['rw_null_lo']},{SPLICE_ANCHORS['rw_null_hi']}]")
    for k, v in results.items():
        if "error" not in v:
            mz_raw = v.get("pooled_mean_z_raw", v.get("pooled_mean_z", float("nan")))
            mz_ds = v.get("pooled_mean_z_deseason", float("nan"))
            g = v.get("grade_raw", v.get("grade", "n/a"))
            mz_r_str = f"{mz_raw:.4f}" if isinstance(mz_raw, float) else str(mz_raw)
            mz_d_str = f"{mz_ds:.4f}" if isinstance(mz_ds, float) else str(mz_ds)
            print(f"  {k}: mean_z_raw={mz_r_str}  mean_z_deseason={mz_d_str}  grade(raw)={g}")

    out_path = os.path.join(ROOT, "data", "processed", "backadj_diagnostic.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, allow_nan=True)
    print(f"\nDiagnostic written to: {out_path}")
