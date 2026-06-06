"""State T — Observational Existence Programme v1 (doc 11). ARM 1: CAUSAL, verdict-bearing.

This module asks ONE thing: *is the distribution of residual morphology inside high-deviation
windows distinguishable from matched synthetic nulls?* It is observational existence research —
NOT State T, NOT a detector, NOT timing, NOT hazard, NOT a score/label. Output is a distributional
effect-size comparison, never a per-bar quantity.

Causal by construction (doc 11 §2/§6): windows are selected by a SYMMETRIC partition on the causal
z-score (|z| ≥ θ), evaluable at t, over the Kalman residual. Everything at anchor bar t depends only
on data ≤ t. Structurally terminal — reads the residual stream and feeds nothing back.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from app.services import analytics, analytics_mrscore
from app.services.analytics_substrate import directional_efficiency

DESCRIPTORS = ("innov_var", "acf1", "dir_eff")


# ── window selection (causal, outcome-blind) ──────────────────────────────────

def partition_anchors(z: pd.Series, theta: float) -> np.ndarray:
    """Positional indices where |z| ≥ θ — a symmetric partition of all bars (both signs), NOT a
    trigger. NaN z is never anchored."""
    zv = np.asarray(z, dtype=float)
    mask = np.isfinite(zv) & (np.abs(zv) >= theta)
    return np.flatnonzero(mask)


def causal_windows(values: np.ndarray, anchors: np.ndarray, W: int) -> list[np.ndarray]:
    """Trailing inclusive pre-window [t−W+1, t] (length W) for each anchor t with enough history.
    Anchors lacking W bars of history are dropped — never padded with anything."""
    v = np.asarray(values, dtype=float)
    out: list[np.ndarray] = []
    for t in np.asarray(anchors, dtype=int):
        if t - W + 1 < 0:
            continue
        out.append(v[t - W + 1: t + 1])
    return out


# ── descriptors ───────────────────────────────────────────────────────────────

def _acf1(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if x.size < 2:
        return float("nan")
    a, b = x[:-1], x[1:]
    if np.std(a) == 0 or np.std(b) == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def window_descriptors(eps_win: np.ndarray, close_win: np.ndarray) -> dict[str, float]:
    """The 3 frozen morphology descriptors (doc 11 §3): innovation variance, innovation lag-1
    autocorrelation, and close-path directional efficiency. No score, no label, no weighting."""
    eps = np.asarray(eps_win, dtype=float)
    return {
        "innov_var": float(np.std(eps, ddof=1)) if eps.size >= 2 else float("nan"),
        "acf1": _acf1(eps),
        "dir_eff": float(directional_efficiency(np.asarray(close_win, dtype=float))),
    }


# ── causal extraction pipeline ────────────────────────────────────────────────

def extract(close: pd.Series, theta: float, W: int, z_window: int = 60) -> pd.DataFrame:
    """Causal Arm-1 extraction: Kalman residual → causal z → |z| ≥ θ anchors → per-window
    descriptors. Returns one row per valid anchor (cols: anchor, innov_var, acf1, dir_eff), sorted
    by anchor. Every value at anchor t uses only data ≤ t."""
    kf = analytics.compute_kalman_mu_star(close)
    mu_star = kf["mu_star_kalman"]
    eps = kf["epsilon_kalman"].to_numpy(dtype=float)
    close_v = np.asarray(close, dtype=float)

    residual = pd.Series(close_v - mu_star.to_numpy(dtype=float))
    z = analytics_mrscore.causal_zscore(residual, window=z_window)
    anchors = partition_anchors(z, theta)

    rows: list[dict] = []
    for t in anchors:
        if t - W + 1 < 0:
            continue
        d = window_descriptors(eps[t - W + 1: t + 1], close_v[t - W + 1: t + 1])
        rows.append({"anchor": int(t), **d})

    cols = ["anchor", *DESCRIPTORS]
    if not rows:
        return pd.DataFrame({c: pd.Series(dtype=float) for c in cols})
    return pd.DataFrame(rows, columns=cols).sort_values("anchor").reset_index(drop=True)


# ── distributional comparison vs nulls ────────────────────────────────────────

def cohens_d(a, b) -> float:
    """Standardized mean difference (a − b) / pooled-SD. Descriptive effect size — NOT a verdict
    threshold. NaN if either side has < 2 finite values or pooled SD is 0."""
    a = np.asarray(a, dtype=float); a = a[np.isfinite(a)]
    b = np.asarray(b, dtype=float); b = b[np.isfinite(b)]
    if a.size < 2 or b.size < 2:
        return float("nan")
    pooled = np.sqrt(((a.size - 1) * a.var(ddof=1) + (b.size - 1) * b.var(ddof=1)) / (a.size + b.size - 2))
    if pooled == 0:
        return 0.0 if a.mean() == b.mean() else float("nan")
    return float((a.mean() - b.mean()) / pooled)


def compare_to_nulls(
    real_close: pd.Series,
    nulls: dict[str, pd.Series],
    thetas: tuple[float, ...] = (1.0, 1.5, 2.0),
    W: int = 30,
    z_window: int = 60,
) -> pd.DataFrame:
    """For each (θ, null, descriptor), effect size of real high-|z| window morphology vs the null's
    high-|z| window morphology under IDENTICAL extraction. Returns a long DataFrame; the existence
    signal is direction-agreement with the pre-registration (doc 11 §4), magnitude secondary."""
    rows: list[dict] = []
    for theta in thetas:
        real_df = extract(real_close, theta=theta, W=W, z_window=z_window)
        for null_name, null_close in nulls.items():
            null_df = extract(null_close, theta=theta, W=W, z_window=z_window)
            for desc in DESCRIPTORS:
                rows.append({
                    "theta": float(theta),
                    "null": null_name,
                    "descriptor": desc,
                    "d": cohens_d(real_df[desc], null_df[desc]),
                    "n_real": int(real_df[desc].notna().sum()),
                    "n_null": int(null_df[desc].notna().sum()),
                })
    return pd.DataFrame(rows, columns=["theta", "null", "descriptor", "d", "n_real", "n_null"])
