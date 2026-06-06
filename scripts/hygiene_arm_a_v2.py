"""
Arm A v2 — pre-registration HYGIENE screen for candidate pre-built calendar spreads.

PURPOSE: pure data-integrity + stale-quote screening (the USD/INR lesson, doc 19 §2). Reports ONLY
admissibility-relevant hygiene metrics — NO VR(q), NO surrogate, NO increment autocorrelation. These
are explicitly pre-registered *reportables* (doc 18a) and are independent of the verdict statistic, so
computing them before the freeze does not violate pre-registration discipline.

Run: backend/.venv/bin/python scripts/hygiene_arm_a_v2.py
"""
from __future__ import annotations
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
import numpy as np
from app.services.analytics_arm_a import load_leg  # identical parsing to the engine

CANDIDATES = {
    "NG_calendar (ng12)":   "data/raw/ng12_spread.csv",
    "RB_calendar (rb23)":   "data/raw/rb23_spread.csv",
    "WTI_Brent (cl_brn 60m)": "data/raw/cl_brn_spread_60.csv",
}

def longest_run(mask: np.ndarray) -> int:
    best = cur = 0
    for v in mask:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best

def screen(name: str, path: str) -> dict:
    df = load_leg(path)
    c = df["close"].to_numpy(dtype=float)
    n = len(df)
    has_ohlc = {"open", "high", "low", "close"}.issubset(df.columns)
    if has_ohlc:
        o, h, l = (df[k].to_numpy(dtype=float) for k in ("open", "high", "low"))
        flat = (o == h) & (h == l) & (l == c)
    else:
        flat = np.zeros(n, dtype=bool)
    dS = np.diff(c)
    zero_incr = (dS == 0.0)
    finite = np.isfinite(c)
    idx = df.index
    # ascending check + duplicate timestamps + calendar gap stats (trading-day cadence sanity)
    ascending = bool((idx.values[1:] >= idx.values[:-1]).all())
    gaps_days = np.diff(idx.values).astype("timedelta64[D]").astype(float)
    return {
        "name": name, "path": path, "n_bars": int(n),
        "date_start": str(idx[0].date()), "date_end": str(idx[-1].date()),
        "ascending_sorted": ascending,
        "has_ohlc": bool(has_ohlc),
        "n_nonfinite_close": int((~finite).sum()),
        "flat_bar_pct": round(100.0 * flat.mean(), 2),
        "zero_increment_pct": round(100.0 * zero_incr.mean(), 2),
        "longest_zero_incr_run": int(longest_run(zero_incr)),
        "longest_flat_run": int(longest_run(flat)),
        "dS_sd": float(np.nanstd(dS, ddof=1)),
        "dS_mad": float(np.nanmedian(np.abs(dS - np.nanmedian(dS)))),
        "close_min": float(np.nanmin(c)), "close_max": float(np.nanmax(c)),
        "crosses_zero": bool(np.nanmin(c) < 0 < np.nanmax(c)),
        "median_gap_days": float(np.nanmedian(gaps_days)),
        "max_gap_days": float(np.nanmax(gaps_days)),
        # USD/INR trap threshold: v1 UNUSABLE had flat=75.6%, zero-incr=14.4% clustered. Flag if comparable.
        "STALE_QUOTE_FLAG": bool((100.0 * flat.mean() > 20.0) or (100.0 * zero_incr.mean() > 8.0)),
    }

if __name__ == "__main__":
    out = []
    for name, path in CANDIDATES.items():
        try:
            out.append(screen(name, path))
        except Exception as e:
            out.append({"name": name, "path": path, "ERROR": repr(e)})
    print(json.dumps(out, indent=2))
