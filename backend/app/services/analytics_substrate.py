"""
Substrate Observatory v1 — "what kind of market are we currently looking at?"

The observational substrate layer beneath State T. It characterises an instrument's CHARACTER over a
trailing window as resemblance to coarse archetypes — it does NOT detect events or predict the future.

    descriptors(window) → (DE, VR, RV/VP) ──► character_scores(DE, VR) → {OU·Trend·RW·Ambiguous}

CONSTITUTIONAL STATUS (CLAUDE.md §10 freeze-break, authorized this session; docs/research/10):
  An OBSERVATORY DIAGNOSTIC — observe/falsify, NOT a signal — and STRUCTURALLY TERMINAL: nothing here
  feeds μ*, MRScore, a validity gate, or any State T logic. It is descriptive, so it trips no reopen
  trigger. CHARACTER, NOT TIMING: scores say what an instrument *resembles* over the window, NEVER that
  a regime is "igniting now" (that is State T detection — FROZEN, doc 04 §1.2.2/§1.3.1). Exhaustion and
  trend etiology are deliberately EXCLUDED from v1 — they are episode-level / the deferred State-T
  conditioning gate (doc 04 §2.6.4), not substrate character.

DAG DISCIPLINE (one-way): self-contained on top of raw OHLCV. Imports nothing from the μ*/Kalman/
MRScore paths and is never imported back into them. (It intentionally re-derives its own small vol
helper rather than coupling to the MRScore observatory — two terminal observatories stay independent.)

TEMPORAL HONESTY (each guarded by a test):
  • every descriptor at bar t uses only data in [t-W+1, t] — forward bars are never read.
  • the realized-vol percentile ranks today's vol within its TRAILING history only.
  • the character map is a pure pointwise function of (DE, VR) — no windowing, no leakage surface.

DESIGN POSTURE: cheap · interpretable · frozen. The descriptor→score map is a transparent, monotone,
hand-set-threshold function (NO fitting, NO HMM, NO ML). v1 is causal mode only (full-information is a
one-line window swap, deferred — see docs/research/10 §"deferred"). Hurst was removed deliberately
(window/method-sensitive, the "easy to hallucinate" estimator MRScore warned against); the Variance
Ratio carries the OU↔RW↔trend axis with a closed-form null and far better interpretability.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


# ── P1: descriptor primitives ─────────────────────────────────────────────────

# Variance-ratio horizons. Mean across horizons (not min) gives a NEUTRAL representative read — min
# would bias every instrument toward "mean-reverting" (cf. MRScore's deliberate min_q MR-favourable
# choice, which is the wrong default for a character question).
VR_HORIZONS: tuple[int, ...] = (2, 5, 10)


def directional_efficiency(prices: np.ndarray) -> float:
    """DE = |P_last − P_first| / Σ|ΔP|  ∈ [0, 1]  (net displacement / total path length).

    1.0 = a perfectly straight move (maximally efficient / trending); ~0 = pure chop that goes nowhere
    (mean-reverting or directionless). Independent of log/scale — works on spreads too. Returns NaN on
    a flat window (zero path length) where efficiency is undefined."""
    p = np.asarray(prices, dtype=float)
    p = p[np.isfinite(p)]
    if p.size < 2:
        return float("nan")
    path = float(np.abs(np.diff(p)).sum())
    if path <= 0.0:
        return float("nan")
    return abs(float(p[-1] - p[0])) / path


def _variance_ratios(logprice: np.ndarray, qs: tuple[int, ...] = VR_HORIZONS) -> dict[int, float]:
    """VR(q) = Var(X_t − X_{t-q}) / (q · Var(X_t − X_{t-1})) on log-prices X (Lo–MacKinlay).
    Random walk → 1, mean reversion → <1, trend/persistence → >1."""
    x = np.asarray(logprice, dtype=float)
    x = x[np.isfinite(x)]
    out: dict[int, float] = {}
    if len(x) < 3:
        return {q: float("nan") for q in qs}
    v1 = float(np.var(np.diff(x), ddof=1))
    for q in qs:
        if len(x) <= q or v1 <= 0:
            out[q] = float("nan")
            continue
        dq = x[q:] - x[:-q]
        out[q] = float(np.var(dq, ddof=1) / (q * v1))
    return out


def variance_ratio_mean(logprice: np.ndarray, qs: tuple[int, ...] = VR_HORIZONS) -> float:
    """Representative VR = mean of VR(q) over horizons (neutral central read). NaN if none defined."""
    vals = [v for v in _variance_ratios(logprice, qs).values() if np.isfinite(v)]
    return float(np.mean(vals)) if vals else float("nan")


def realized_vol(closes: pd.Series, window: int = 20, periods_per_year: int = 252) -> pd.Series:
    """Annualized trailing realized vol: RV_t = sqrt(periods_per_year/w · Σ_{i<w} r²_{t-i}), r = log
    returns. Causal (last w returns ending at t). NaN on non-positive prices (log undefined; flagged
    upstream by the endpoint's data_warning)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.log(closes).diff()
    sq_sum = (r ** 2).rolling(window=window, min_periods=window).sum()
    return np.sqrt(periods_per_year / window * sq_sum)


def realized_vol_percentile(closes: pd.Series, rv_window: int = 20, vp_window: int = 252,
                            min_periods: int = 20) -> pd.Series:
    """VP_t ∈ [0,100] — percentile rank of today's realized vol within its TRAILING vp_window history
    (includes the current bar: "where does today's vol sit in its own recent range"). CONTEXT ONLY —
    vol is NOT a character driver in v1 (it would be gameable); it is surfaced for interpretation."""
    rv = realized_vol(closes, window=rv_window).to_numpy()
    n = len(rv)
    out = np.full(n, np.nan)
    for t in range(n):
        cur = rv[t]
        if not np.isfinite(cur):
            continue
        ref = rv[max(0, t - vp_window + 1): t + 1]
        ref = ref[np.isfinite(ref)]
        if ref.size < min_periods:
            continue
        below = float(np.mean(ref < cur))
        equal = float(np.mean(ref == cur))
        out[t] = 100.0 * (below + 0.5 * equal)
    return pd.Series(out, index=closes.index)


# ── P2: character map (pure · frozen · monotone · hand-set thresholds — NEVER fit) ─
#
# Buckets are independent RESEMBLANCE scores in [0,1] (NOT a probability partition — they may overlap).
# Built from two bounded, monotone primitives. KEY EMPIRICAL CONSTRAINT (verified, docs/research/10):
# a DETERMINISTIC-drift trend has VR ≈ 1 (drift adds to the mean, not the variance — VR detects only
# *stochastic* persistence). So VR CANNOT carry the trend axis; directional efficiency must. VR's job
# is to split OU from RW *within* the choppy (low-DE) region. Geometry of (DE, VR) space:
#   • high DE              → Trend-like   (deterministic drift OR momentum; both go straight)
#   • low DE & VR < 1      → OU-like      (choppy, sub-diffusive)
#   • low DE & VR ≈ 1      → RW-Null      (choppy, diffuses like a random walk)
#
#   t_vr = clip((VR − 1)/1.0, 0, 1)     momentum bonus only          (1 at VR≥2)
#   m_vr = clip((1 − VR)/0.5, 0, 1)     MR-ness from variance scaling (1 at VR≤0.5)
#   rw_vr = max(0, 1 − |VR − 1|/0.5)    RW-ness — peaks at VR=1, 0 by VR≤0.5 or ≥1.5
#
#   Trend_like = min(1, DE + 0.30·t_vr)  (DE-primary; VR>1 is a momentum bonus, never a requirement)
#   OU_like    = (1 − DE) · m_vr         (choppy AND sub-diffusive — product: BOTH must hold)
#   RW_null    = (1 − DE) · rw_vr        (choppy AND diffusion ≈ random walk)
#   Ambiguous  = 1 − max(Trend, OU, RW)  (honest "no archetype dominates")
#
# `dominant` = argmax over all four. `confidence` from the top-two margin (frozen thresholds):
#   clear (margin ≥ 0.20) · weak (≥ 0.08) · ambiguous (< 0.08, or dominant == ambiguous).
# Thresholds are economic/structural priors, FROZEN — they are never optimised against outcomes.

_CONF_CLEAR: float = 0.20
_CONF_WEAK: float = 0.08


def character_scores(de: float, vr: float) -> dict[str, float | str]:
    """Pointwise resemblance of (directional efficiency, variance ratio) to the 4 substrate archetypes.
    Pure & frozen — no windowing, no fitting. NaN descriptors → fully ambiguous (honest abstention)."""
    if not (np.isfinite(de) and np.isfinite(vr)):
        return {"ou_like": float("nan"), "trend_like": float("nan"), "rw_null": float("nan"),
                "ambiguous": 1.0, "dominant": "ambiguous", "confidence": "ambiguous"}

    de = float(min(1.0, max(0.0, de)))
    t_vr = min(1.0, max(0.0, (vr - 1.0) / 1.0))
    m_vr = min(1.0, max(0.0, (1.0 - vr) / 0.5))
    rw_vr = max(0.0, 1.0 - abs(vr - 1.0) / 0.5)

    trend_like = min(1.0, de + 0.30 * t_vr)
    ou_like = (1.0 - de) * m_vr
    rw_null = (1.0 - de) * rw_vr
    ambiguous = 1.0 - max(trend_like, ou_like, rw_null)

    scored = {"ou_like": ou_like, "trend_like": trend_like, "rw_null": rw_null, "ambiguous": ambiguous}
    ranked = sorted(scored.items(), key=lambda kv: kv[1], reverse=True)
    dominant, top = ranked[0]
    margin = top - ranked[1][1]
    if dominant == "ambiguous" or margin < _CONF_WEAK:
        confidence = "ambiguous"
    elif margin < _CONF_CLEAR:
        confidence = "weak"
    else:
        confidence = "clear"
    return {**scored, "dominant": dominant, "confidence": confidence}


# ── P3: per-bar descriptors (causal, trailing window W) ────────────────────────

def substrate_descriptors(
    closes: pd.Series,
    window: int = 120,
    vr_qs: tuple[int, ...] = VR_HORIZONS,
    rv_window: int = 20,
    vp_window: int = 252,
) -> pd.DataFrame:
    """Per-bar descriptors (de, vr, rv, vp) over a trailing estimation `window`. Causal by construction:
    DE and VR at bar t use only [t-window+1, t]; nothing reads bars > t (firewall test pins this)."""
    price = closes.to_numpy(dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):  # non-positive → NaN (flagged upstream)
        logp = np.log(price)
    n = len(closes)
    de = np.full(n, np.nan)
    vr = np.full(n, np.nan)
    for t in range(n):
        lo = t - window + 1
        if lo < 0:
            continue
        de[t] = directional_efficiency(price[lo : t + 1])
        vr[t] = variance_ratio_mean(logp[lo : t + 1], vr_qs)
    rv = realized_vol(closes, window=rv_window)
    vp = realized_vol_percentile(closes, rv_window=rv_window, vp_window=vp_window)
    return pd.DataFrame({"de": de, "vr": vr, "rv": rv.to_numpy(), "vp": vp.to_numpy()}, index=closes.index)


# ── P4: master compute (descriptors + character) ───────────────────────────────

def compute_substrate(
    closes: pd.Series,
    window: int = 120,
    vr_qs: tuple[int, ...] = VR_HORIZONS,
    rv_window: int = 20,
    vp_window: int = 252,
) -> pd.DataFrame:
    """Substrate Observatory per bar, causal. Returns the 3 descriptors (de, vr, vp; rv for reference)
    plus the 4 resemblance scores and the (dominant, confidence) read. vp is context only — the
    character map is a pure function of (de, vr). Structurally terminal; never feeds μ*/MRScore/gates."""
    d = substrate_descriptors(closes, window=window, vr_qs=vr_qs, rv_window=rv_window, vp_window=vp_window)
    chars = [character_scores(de, vr) for de, vr in zip(d["de"].to_numpy(), d["vr"].to_numpy())]
    ch = pd.DataFrame(chars, index=closes.index)
    return pd.DataFrame(
        {
            "de": d["de"], "vr": d["vr"], "rv": d["rv"], "vp": d["vp"],
            "ou_like": ch["ou_like"], "trend_like": ch["trend_like"],
            "rw_null": ch["rw_null"], "ambiguous": ch["ambiguous"],
            "dominant": ch["dominant"], "confidence": ch["confidence"],
        },
        index=closes.index,
    )
