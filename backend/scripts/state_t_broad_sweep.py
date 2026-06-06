"""State T broad sweep — 62-file cross-habitat falsification attempt (2026-06-04).

Operationalizes the FROZEN State T hypothesis (doc 11, KILLED-IN-FORM) across all files in
~/Downloads/mean-reversion-data/ to determine whether the kill verdict holds broadly or whether
any habitat-conditional signal survives.

PRE-REGISTERED T-SIGNATURE (doc 11 §4): ALL THREE descriptors NEGATIVE vs matched OU null.
    innov_var ↓   acf1 ↓   dir_eff ↓

VERDICT rules (per file, at θ=1.0 — most inclusive; confirmed at θ=1.5/2.0 as sensitivity):
    NOISE       : < MIN_ANCHORS valid windows at θ=1.0 OR > 80% NaN descriptors → insufficient
    CONFIRMS    : all 3 Cohen's d < 0 at θ=1.0 (T-signature direction, any magnitude)
    REJECTS     : 2+ descriptors d > 0 (wrong direction)
    INCONCLUSIVE: 1 positive, 2 negative (mixed; does not confirm the universal signature)

STOP RULE: if running NOISE count ≥ ceil(0.30 × total_files) → halt, report partial results.

Run from backend/:
    .venv/bin/python -m scripts.state_t_broad_sweep
"""
import math
import os
import sys
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

from app.services import analytics, analytics_mrscore, analytics_state_t as st
from app.services import synthetic

# ── Config ────────────────────────────────────────────────────────────────────
DATA_DIR = os.path.expanduser("~/Downloads/mean-reversion-data")
W = 30
Z_WINDOW = 60
THETAS = (1.0, 1.5, 2.0)
NULL_SEEDS = list(range(300, 312))   # 12 OU seeds — same as cohort probe
MIN_BARS = 200          # minimum bars to attempt analysis
MIN_ANCHORS = 10        # minimum windows at θ=1.0 to avoid NOISE verdict
NOISE_STOP_FRAC = 0.30  # halt if this fraction of files are NOISE


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_close(fpath: str) -> pd.Series | None:
    """Load close prices from CSV. Returns None if file is unusable."""
    try:
        df = pd.read_csv(fpath)
        df.columns = [c.strip() for c in df.columns]
        # Try to find close column (case-insensitive)
        close_col = next((c for c in df.columns if c.lower() == "close"), None)
        if close_col is None:
            return None
        closes = pd.to_numeric(df[close_col], errors="coerce").dropna()
        if len(closes) < MIN_BARS:
            return None
        return closes.reset_index(drop=True)
    except Exception:
        return None


def make_ou_nulls(close: pd.Series) -> dict[str, pd.Series]:
    """12 scale-matched OU nulls (lam=−0.1, σ matched to close-diff std)."""
    sigma = float(np.std(np.diff(close.to_numpy(dtype=float))))
    base = float(close.mean())
    return {
        f"ou_{s}": pd.Series(
            synthetic.ou(lam=-0.1, sigma=sigma, n=len(close), seed=s, base=base).prices
        )
        for s in NULL_SEEDS
    }


def pooled_null_descriptors(nulls: dict[str, pd.Series], theta: float, desc: str) -> np.ndarray:
    parts = []
    for null_close in nulls.values():
        df = st.extract(null_close, theta=theta, W=W, z_window=Z_WINDOW)
        parts.append(df[desc].dropna().to_numpy(dtype=float))
    if not parts:
        return np.array([])
    return np.concatenate(parts)


def classify_file(fpath: str) -> dict:
    fname = os.path.basename(fpath)
    close = load_close(fpath)

    if close is None:
        return {
            "file": fname, "verdict": "NOISE", "reason": "load_fail_or_too_short",
            "n_bars": 0, "n_anchors_1": 0,
            "d_iv_1": np.nan, "d_ac_1": np.nan, "d_de_1": np.nan,
            "d_iv_15": np.nan, "d_ac_15": np.nan, "d_de_15": np.nan,
            "d_iv_2": np.nan, "d_ac_2": np.nan, "d_de_2": np.nan,
        }

    n_bars = len(close)

    # Extract windows at θ=1.0 to check convergence
    try:
        rdf_10 = st.extract(close, theta=1.0, W=W, z_window=Z_WINDOW)
    except Exception as e:
        return {
            "file": fname, "verdict": "NOISE", "reason": f"extract_error: {e}",
            "n_bars": n_bars, "n_anchors_1": 0,
            "d_iv_1": np.nan, "d_ac_1": np.nan, "d_de_1": np.nan,
            "d_iv_15": np.nan, "d_ac_15": np.nan, "d_de_15": np.nan,
            "d_iv_2": np.nan, "d_ac_2": np.nan, "d_de_2": np.nan,
        }

    n_anchors_1 = len(rdf_10)
    nan_frac = rdf_10[list(st.DESCRIPTORS)].isna().values.mean() if n_anchors_1 > 0 else 1.0

    if n_anchors_1 < MIN_ANCHORS or nan_frac > 0.8:
        return {
            "file": fname, "verdict": "NOISE",
            "reason": f"n_anchors={n_anchors_1}<{MIN_ANCHORS} or nan_frac={nan_frac:.2f}>0.8",
            "n_bars": n_bars, "n_anchors_1": n_anchors_1,
            "d_iv_1": np.nan, "d_ac_1": np.nan, "d_de_1": np.nan,
            "d_iv_15": np.nan, "d_ac_15": np.nan, "d_de_15": np.nan,
            "d_iv_2": np.nan, "d_ac_2": np.nan, "d_de_2": np.nan,
        }

    # Build OU nulls and compute Cohen's d at each theta
    try:
        nulls = make_ou_nulls(close)
    except Exception as e:
        return {
            "file": fname, "verdict": "NOISE", "reason": f"null_build_error: {e}",
            "n_bars": n_bars, "n_anchors_1": n_anchors_1,
            "d_iv_1": np.nan, "d_ac_1": np.nan, "d_de_1": np.nan,
            "d_iv_15": np.nan, "d_ac_15": np.nan, "d_de_15": np.nan,
            "d_iv_2": np.nan, "d_ac_2": np.nan, "d_de_2": np.nan,
        }

    d_by_theta = {}
    for theta in THETAS:
        rdf = rdf_10 if theta == 1.0 else st.extract(close, theta=theta, W=W, z_window=Z_WINDOW)
        key = str(theta).replace(".", "")
        d_by_theta[key] = {}
        for desc in st.DESCRIPTORS:
            null_vals = pooled_null_descriptors(nulls, theta, desc)
            d_by_theta[key][desc] = st.cohens_d(rdf[desc].dropna().to_numpy(), null_vals)

    # Verdict at θ=1.0 (primary)
    d10 = d_by_theta["10"]
    d_vals = [d10["innov_var"], d10["acf1"], d10["dir_eff"]]
    finite_d = [v for v in d_vals if np.isfinite(v)]
    neg_count = sum(1 for v in finite_d if v < 0)
    pos_count = sum(1 for v in finite_d if v > 0)

    if len(finite_d) < 2:
        verdict = "NOISE"
        reason = "too_few_finite_effect_sizes"
    elif neg_count == 3:
        verdict = "CONFIRMS"
        reason = "all_3_d<0 (T-signature direction)"
    elif pos_count >= 2:
        verdict = "REJECTS"
        reason = f"{pos_count}/3 d>0 (wrong direction)"
    else:
        verdict = "INCONCLUSIVE"
        reason = f"neg={neg_count} pos={pos_count} (mixed)"

    d15 = d_by_theta.get("15", {})
    d20 = d_by_theta.get("20", {})

    return {
        "file": fname,
        "verdict": verdict,
        "reason": reason,
        "n_bars": n_bars,
        "n_anchors_1": n_anchors_1,
        # θ=1.0
        "d_iv_1":  d10.get("innov_var", np.nan),
        "d_ac_1":  d10.get("acf1",      np.nan),
        "d_de_1":  d10.get("dir_eff",   np.nan),
        # θ=1.5
        "d_iv_15": d15.get("innov_var", np.nan),
        "d_ac_15": d15.get("acf1",      np.nan),
        "d_de_15": d15.get("dir_eff",   np.nan),
        # θ=2.0
        "d_iv_2":  d20.get("innov_var", np.nan),
        "d_ac_2":  d20.get("acf1",      np.nan),
        "d_de_2":  d20.get("dir_eff",   np.nan),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    files = sorted(
        os.path.join(DATA_DIR, f)
        for f in os.listdir(DATA_DIR)
        if f.endswith(".csv")
    )
    total = len(files)
    noise_stop_at = math.ceil(total * NOISE_STOP_FRAC)

    print(f"State T Broad Sweep — {total} files, stop if NOISE ≥ {noise_stop_at} ({NOISE_STOP_FRAC*100:.0f}%)")
    print(f"Pre-registered T-signature: ALL THREE descriptors NEGATIVE vs OU null at θ=1.0")
    print(f"W={W}  z_window={Z_WINDOW}  null_seeds={len(NULL_SEEDS)}  min_bars={MIN_BARS}  min_anchors={MIN_ANCHORS}")
    print("=" * 110)

    results = []
    noise_count = 0
    confirms = 0
    rejects = 0
    inconclusive = 0
    stopped_early = False

    header = (
        f"{'#':>3}  {'FILE':<40}  {'VERDICT':<13}  {'n_bars':>7}  {'n_anch':>6}  "
        f"{'d_iv@1':>8}  {'d_ac@1':>8}  {'d_de@1':>8}  REASON"
    )
    print(header)
    print("-" * 110)

    for i, fpath in enumerate(files, 1):
        row = classify_file(fpath)
        results.append(row)
        v = row["verdict"]

        if v == "NOISE":
            noise_count += 1
        elif v == "CONFIRMS":
            confirms += 1
        elif v == "REJECTS":
            rejects += 1
        else:
            inconclusive += 1

        d_iv = f"{row['d_iv_1']:+.3f}" if np.isfinite(row['d_iv_1']) else "  nan"
        d_ac = f"{row['d_ac_1']:+.3f}" if np.isfinite(row['d_ac_1']) else "  nan"
        d_de = f"{row['d_de_1']:+.3f}" if np.isfinite(row['d_de_1']) else "  nan"

        flag = " ◄NOISE" if v == "NOISE" else (" ✓" if v == "CONFIRMS" else (" ✗" if v == "REJECTS" else ""))
        print(
            f"{i:>3}  {row['file']:<40}  {v:<13}  {row['n_bars']:>7}  {row['n_anchors_1']:>6}  "
            f"{d_iv:>8}  {d_ac:>8}  {d_de:>8}  {row['reason']}{flag}"
        )

        if noise_count >= noise_stop_at:
            print(f"\n!!! STOP-LOSS TRIGGERED: {noise_count} NOISE files after {i}/{total} processed "
                  f"(≥ {NOISE_STOP_FRAC*100:.0f}% threshold). Halting. !!!")
            stopped_early = True
            results_so_far = i
            break
    else:
        results_so_far = total

    print("=" * 110)
    print(f"\n{'SUMMARY':}")
    print(f"  Files processed : {results_so_far}/{total}")
    print(f"  NOISE           : {noise_count}")
    print(f"  CONFIRMS        : {confirms}  (all 3 d<0 at θ=1.0)")
    print(f"  REJECTS         : {rejects}   (2+ d>0 at θ=1.0)")
    print(f"  INCONCLUSIVE    : {inconclusive}")
    if stopped_early:
        print(f"  *** STOPPED EARLY at file {results_so_far} — NOISE ≥ 30% threshold ***")
    else:
        noise_pct = 100 * noise_count / results_so_far
        confirms_pct = 100 * confirms / results_so_far
        rejects_pct = 100 * rejects / results_so_far
        print(f"\n  NOISE %         : {noise_pct:.1f}%")
        print(f"  CONFIRMS %      : {confirms_pct:.1f}%")
        print(f"  REJECTS %       : {rejects_pct:.1f}%")
        print(f"\n  GLOBAL VERDICT  : ", end="")
        adjudicated = confirms + rejects + inconclusive
        if adjudicated == 0:
            print("ALL NOISE — apparatus failed entirely")
        elif confirms / adjudicated >= 0.5:
            print(f"PARTIAL SIGNAL — T-signature confirms in {confirms}/{adjudicated} analyzable files")
        elif rejects / adjudicated >= 0.5:
            print(f"DEAD — T-signature REJECTS in {rejects}/{adjudicated} analyzable files")
        else:
            print(f"INCONCLUSIVE — no consistent direction across {adjudicated} analyzable files")

    # Dump full results CSV for posterity
    out_path = os.path.join(os.path.dirname(__file__), "..", "..", "data",
                            "state_t_broad_sweep_results.csv")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    pd.DataFrame(results).to_csv(out_path, index=False)
    print(f"\n  Full results → {os.path.abspath(out_path)}")


if __name__ == "__main__":
    main()
