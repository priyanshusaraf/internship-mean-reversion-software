"""Habitat score engine — the SINGLE null-generating code path (contract M3, D3).

The VR + RW + MA(1) null math here is copied VERBATIM from the frozen
`scripts/calibrate_habitat_score.py` (constants VR_QS=[5,10,20], NS_NULL=2000, the exact
seed/order/vol-matching). `habitat_score_full` is the one place the null cloud is built;
`scripts/calibrate_habitat_score.py::habitat_score` now calls into here so there is ONE path
(contract M3 — a second null loop would let the calibration badge drift from live scoring).

Frozen constants are NOT changed. This module is a wrapper that *returns* the arrays the
calibration already computed internally and then discarded.
"""
from __future__ import annotations
import numpy as np

# Habitat score parameters — FROZEN (mirror scripts/calibrate_habitat_score.py).
VR_QS = [5, 10, 20]          # lags for min-VR
NS_NULL = 2000               # surrogates per score evaluation
SEED_CAL = 20260606          # calibration seed (default)


# ── VR helpers (VERBATIM from calibrate_habitat_score.py) ──────────────────────────

def vr_q(x: np.ndarray, q: int) -> float:
    """Variance ratio at lag q. x is a level series."""
    x = x[np.isfinite(x)]
    n = len(x)
    if n < q + 5:
        return float("nan")
    dr = np.diff(x)
    var1 = np.var(dr, ddof=1)
    if var1 <= 1e-14:
        return float("nan")
    ret_q = x[q:] - x[:-q]
    return float(np.var(ret_q, ddof=1) / (q * var1))


def min_vr(x: np.ndarray, qs: list[int] = VR_QS) -> float:
    """Min VR over a set of lags."""
    vals = [vr_q(x, q) for q in qs]
    vals = [v for v in vals if np.isfinite(v)]
    return min(vals) if vals else float("nan")


# ── Habitat score (full) — the SINGLE null path ────────────────────────────────────

def habitat_score_full(x: np.ndarray, seed: int = SEED_CAL) -> dict:
    """Surrogate-relative MR habitat score for window x, returning the FULL cloud.

    Returns {score, real_min_vr, null_min_vr (list), vr_curve (list of {q,vr}), n}.
    score = 100 * mean(null_min_vr >= real_min_vr); high = more reverting than null.
    score/real_min_vr are NaN (callers map to null) when the window is too short / degenerate.

    The math below is VERBATIM the body of the frozen `habitat_score`; the only addition is
    that the per-surrogate `null_mvrs` and the per-q VR curve are returned rather than discarded.
    """
    x = np.asarray(x, dtype=float)
    real_mvr = min_vr(x)

    # vr_curve over the real window (per-q), for rendering — does not affect the score.
    vr_curve = [{"q": int(q), "vr": vr_q(x, q)} for q in VR_QS]

    x_fin = x[np.isfinite(x)]
    n = len(x_fin)

    if not np.isfinite(real_mvr) or n < max(VR_QS) + 5:
        return {
            "score": float("nan"),
            "real_min_vr": real_mvr,
            "null_min_vr": [],
            "vr_curve": vr_curve,
            "n": int(n),
        }

    dr = np.diff(x_fin)
    mu_dr = float(np.mean(dr))
    sig_dr = float(np.std(dr, ddof=1))
    rng = np.random.default_rng(seed)

    null_mvrs: list[float] = []

    # Null 1: RW (iid, vol-matched)
    for _ in range(NS_NULL // 2):
        path = np.concatenate([[x_fin[0]], x_fin[0] + np.cumsum(rng.normal(mu_dr, sig_dr, n - 1))])
        v = min_vr(path)
        if np.isfinite(v):
            null_mvrs.append(v)

    # Null 2: MA(1) (vol-matched, decorrelation-free at q>=2 asymptotically)
    if len(dr) > 5:
        acf1 = float(np.corrcoef(dr[:-1], dr[1:])[0, 1])
        theta_ma = np.clip(acf1, -0.95, 0.95)
    else:
        theta_ma = 0.0

    for _ in range(NS_NULL // 2):
        eps = rng.normal(0, sig_dr, n + 1)
        ma1_rets = eps[1:] + theta_ma * eps[:-1]
        ma1_rets *= sig_dr / (np.std(ma1_rets, ddof=1) + 1e-12)  # re-scale to match vol
        path = np.concatenate([[x_fin[0]], x_fin[0] + np.cumsum(ma1_rets[:n - 1])])
        v = min_vr(path)
        if np.isfinite(v):
            null_mvrs.append(v)

    if not null_mvrs:
        return {
            "score": float("nan"),
            "real_min_vr": real_mvr,
            "null_min_vr": [],
            "vr_curve": vr_curve,
            "n": int(n),
        }

    score = 100.0 * float(np.mean(np.array(null_mvrs) >= real_mvr))
    return {
        "score": score,
        "real_min_vr": float(real_mvr),
        "null_min_vr": [float(v) for v in null_mvrs],
        "vr_curve": vr_curve,
        "n": int(n),
    }
