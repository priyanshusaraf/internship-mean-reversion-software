"""
MRScore v1 — observatory diagnostic engine.

A faithful implementation of the frozen MRScore specification (docs/research/01_amr_framework.md
§3, eq. 13–34): a scalar summary of how favourable current conditions are for mean reversion.

    MRScore_t = 0.20·B1_t + 0.60·B2_t + 0.20·B3_t                                   (eq. 13)

CONSTITUTIONAL STATUS (CLAUDE.md §10 freeze-break, authorized this session):
  MRScore is an OBSERVATORY DIAGNOSTIC — observe/falsify, NOT a signal — and is STRUCTURALLY
  TERMINAL: nothing here feeds a validity gate, RFI, position sizing, or μ* recalibration. This is
  a *descriptive* measurement of reversion, so it does NOT trip the μ* reversion-fidelity reopen
  trigger (CONTINUATION_STATE §1). Doc 01 §3.1: "a detection instrument, not a prediction instrument."

DAG DISCIPLINE (one-way, structurally enforced):
  This module imports FROM `analytics` and must NEVER be imported back into the μ*/Kalman/velocity-
  absorption paths. Functions take μ* (and price) as INPUT series — they never recompute or feed
  back into the equilibrium estimate.

TEMPORAL HONESTY (the ways we could fool ourselves — each guarded by a test):
  • causal z standardizes by trailing (shifted) μ,σ — never the contemporaneous bar (doc 01:622).
  • forward-return features (DRC, HitRate) trim the last h bars (no unrealized returns).
  • percentile ranks compare the current feature only against the PRIOR W bars (eq. 14).
  • Newey-West HAC on DRC is mandatory for valid inference (orthogonal to lookahead).

v1 SCOPE: causal mode only (no genuine full-information μ* exists yet — see CONTINUATION_STATE §3);
EMA μ* only (Kalman is reversion-fidelity-unresolved); c-free transaction-cost fallback.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


# ── P1: primitives + causal z ─────────────────────────────────────────────────

def causal_zscore(residual: pd.Series, window: int = 60) -> pd.Series:
    """Causal z-score: standardize the current deviation by its TRAILING distribution.

        z_t = (ε_t − mean(ε_{t-window..t-1})) / std(ε_{t-window..t-1})

    The standardizing mean/std use only data strictly before t (`.shift(1)`), so z_t carries no
    contemporaneous σ contamination (doc 01 lines 622–625). The numerator keeps ε_t — z_t is meant
    to express how many trailing-σ the *current* deviation is. NOT a drop-in for analytics.compute_zscore
    (which includes the current bar in its rolling stats — a leak for MRScore's purposes)."""
    mu = residual.rolling(window=window, min_periods=2).mean().shift(1)
    sd = residual.rolling(window=window, min_periods=2).std().shift(1)
    return (residual - mu) / sd


def rolling_percentile_rank(
    series: pd.Series,
    window: int = 252,
    min_periods: int = 20,
    include_current: bool = False,
) -> pd.Series:
    """Percentile rank of each value within its trailing window, scaled to [0, 100] (eq. 14).

    `include_current=False` (default, the eq. 14 feature-rank convention): rank f_t against the
    PRIOR `window` bars {f_{t-window}..f_{t-1}} — the current bar is excluded, so the rank is causal
    and self-referential bias is avoided. `include_current=True` is used for the volatility
    percentile VP_t (where "is today's vol high in its history" naturally includes today).

    Rank = 100 · (fraction of the comparison window strictly less than the current value). The caller
    is responsible for directional adjustment (e.g. ranking on −DRC) so that 100 = most MR-favourable.
    Returns NaN until at least `min_periods` finite comparison values are available."""
    vals = series.to_numpy(dtype=float)
    n = len(vals)
    out = np.full(n, np.nan)
    for t in range(n):
        cur = vals[t]
        if not np.isfinite(cur):
            continue
        if include_current:
            ref = vals[max(0, t - window + 1): t + 1]
        else:
            ref = vals[max(0, t - window): t]
        ref = ref[np.isfinite(ref)]
        if ref.size < min_periods:
            continue
        # Mid-rank: count ties as half. Strict `<` alone pushes saturated/capped features (e.g.
        # MeanStab=1.0, TCF=1.0) to rank 0 (= "worst"), inverting their meaning. Mid-rank puts a
        # constant/ceiling feature at ~50 (neutral) while preserving 0/100 for true extremes.
        below = float(np.mean(ref < cur))
        equal = float(np.mean(ref == cur))
        out[t] = 100.0 * (below + 0.5 * equal)
    return pd.Series(out, index=series.index)


def realized_vol(closes: pd.Series, window: int = 20, periods_per_year: int = 252) -> pd.Series:
    """Annualized realized volatility over a trailing window (eq. 29):

        RV_t = sqrt(periods_per_year / w · Σ_{i<w} r²_{t-i}),   r = log returns.

    Causal: uses only the last `w` returns ending at t. NOTE: log-prices require positive prices —
    non-positive/spread series yield NaN here (handled explicitly upstream via the endpoint's
    data_warning; the errstate just keeps that expected case quiet rather than spamming the log)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.log(closes).diff()
    sq_sum = (r ** 2).rolling(window=window, min_periods=window).sum()
    return np.sqrt(periods_per_year / window * sq_sum)


def vol_percentile(rv: pd.Series, window: int = 252, min_periods: int = 20) -> pd.Series:
    """VP_t — percentile rank of current realized vol within its trailing W-bar history, in [0,100].
    Includes the current bar (descriptive "where does today's vol sit"). Used by VCscore and TCF."""
    return rolling_percentile_rank(rv, window=window, min_periods=min_periods, include_current=True)


# ── P2: Block 2 — Mean Reversion Strength (doc 01 §B2, eq. 21–27) ──────────────
#
# Block 2 (60% of MRScore) is the heart of the framework AND the highest temporal-risk code.
# It directly answers "does price snap back toward μ* after deviating?" Three guards apply:
#   1. forward-return features trim the last h bars (no unrealized returns at the right edge);
#   2. Newey-West HAC is mandatory — overlapping h>1 returns are serially correlated, so OLS SEs
#      inflate t-stats (doc 01:617–620). HAC is orthogonal to lookahead; both are required;
#   3. z_s is the causal z (above) — μ,σ from data strictly before s.

VR_HORIZONS: tuple[int, ...] = (2, 5, 10, 20)


def _nw_lag(h: int) -> int:
    """Newey-West truncation lag ℓ_NW = ⌊1.3·h^(2/3)⌋ (Andrews 1991 plug-in, doc 01 eq. 22)."""
    return int(np.floor(1.3 * h ** (2.0 / 3.0)))


def newey_west_tstat(x: np.ndarray, y: np.ndarray, lag: int) -> float:
    """t-statistic on the slope of OLS y = a + b·x, using Newey-West HAC standard errors.
    Returns NaN on degenerate input (too few points, no variance in x, solver failure)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if x.size < 3 or np.var(x) < 1e-18:
        return float("nan")
    try:
        res = sm.OLS(y, sm.add_constant(x)).fit(
            cov_type="HAC", cov_kwds={"maxlags": max(0, int(lag))}
        )
        return float(res.tvalues[1])
    except Exception:
        return float("nan")


def drc_window(
    z: np.ndarray,
    logprice: np.ndarray,
    horizons: tuple[int, ...] = (1, 3, 5),
    min_obs: int = 120,
) -> float:
    """Direct Reversion Coefficient over one estimation window (eq. 21–23):

        r_{s+h} = α + β·z_s + ε,   t_β(h) = β̂(h)/SE_NW,   DRC = min_{h} t_β(h).

    Forward return r_{s+h} = logP_{s+h} − logP_s, so only pairs with s+h inside the window are used
    (the last h bars are trimmed). Rank direction is on −DRC (most negative = most MR-favourable), so
    a strongly negative DRC = strong evidence of reversion. NaN if any horizon lacks ≥`min_obs` pairs."""
    z = np.asarray(z, dtype=float)
    lp = np.asarray(logprice, dtype=float)
    n = len(z)
    tstats: list[float] = []
    for h in horizons:
        if n - h < min_obs:
            return float("nan")
        zs = z[: n - h]
        fwd = lp[h:] - lp[: n - h]
        valid = np.isfinite(zs) & np.isfinite(fwd)
        if valid.sum() < min_obs:
            return float("nan")
        t = newey_west_tstat(zs[valid], fwd[valid], _nw_lag(h))
        if not np.isfinite(t):
            return float("nan")
        tstats.append(t)
    return float(min(tstats)) if tstats else float("nan")


def hit_rate_window(
    z: np.ndarray,
    price: np.ndarray,
    theta: float = 1.0,
    h: int = 5,
    min_events: int = 20,
) -> float:
    """Mean Reversion Hit Rate over one window (eq. 24): of the bars with |z_s| > θ (and a valid
    forward bar s+h), the fraction whose move P_{s+h}−P_s opposes the sign of z_s (i.e. reverts).
    θ = 1.0 is FIXED (not optimised). Excluded (NaN) if fewer than `min_events` qualifying events."""
    z = np.asarray(z, dtype=float)
    p = np.asarray(price, dtype=float)
    n = len(z)
    if n - h < 1:
        return float("nan")
    zs = z[: n - h]
    p0 = p[: n - h]
    ph = p[h:]
    qualifies = np.isfinite(zs) & np.isfinite(p0) & np.isfinite(ph) & (np.abs(zs) > theta)
    if qualifies.sum() < min_events:
        return float("nan")
    reverted = np.sign(ph[qualifies] - p0[qualifies]) == -np.sign(zs[qualifies])
    return float(reverted.mean())


def variance_ratios(logprice: np.ndarray, qs: tuple[int, ...] = VR_HORIZONS) -> dict[int, float]:
    """VR(q) = Var̂(X_t − X_{t-q}) / (q · Var̂(X_t − X_{t-1})) on log-prices X (eq. 25).
    Random walk → 1, mean reversion → <1, trend → >1."""
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


def variance_ratio_agg(logprice: np.ndarray, qs: tuple[int, ...] = VR_HORIZONS) -> float:
    """VR_agg = min_q VR(q) (eq. 26) — the most mean-reverting horizon. Rank direction: (1 − VR_agg)."""
    vals = [v for v in variance_ratios(logprice, qs).values() if np.isfinite(v)]
    return float(min(vals)) if vals else float("nan")


def block2_features(
    closes: pd.Series,
    mu_star: pd.Series,
    window: int = 252,
    z_window: int = 60,
    horizons: tuple[int, ...] = (1, 3, 5),
    theta: float = 1.0,
    hit_h: int = 5,
    min_obs: int = 120,
    min_events: int = 20,
    vr_qs: tuple[int, ...] = VR_HORIZONS,
) -> pd.DataFrame:
    """Per-bar raw Block-2 features (DRC, HitRate, VR_agg) over a trailing estimation `window`.

    Causal by construction: the value at bar t uses only data in [t-window+1, t]; forward-return
    features trim the last h bars inside that window, so nothing reads bars > t. `mu_star` is supplied
    by the caller (EMA, causal) — this function never recomputes or feeds back into μ* (one-way DAG)."""
    resid = closes - mu_star
    z = causal_zscore(resid, z_window).to_numpy()
    price = closes.to_numpy(dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):  # non-positive prices → NaN (flagged upstream)
        logp = np.log(price)
    n = len(closes)
    drc = np.full(n, np.nan)
    hr = np.full(n, np.nan)
    vr = np.full(n, np.nan)
    for t in range(n):
        lo = t - window + 1
        if lo < 0:
            continue
        zz = z[lo : t + 1]
        lpp = logp[lo : t + 1]
        pp = price[lo : t + 1]
        drc[t] = drc_window(zz, lpp, horizons, min_obs)
        hr[t] = hit_rate_window(zz, pp, theta, hit_h, min_events)
        vr[t] = variance_ratio_agg(lpp, vr_qs)
    return pd.DataFrame({"drc": drc, "hit_rate": hr, "vr_agg": vr}, index=closes.index)


def block2_score(
    closes: pd.Series,
    mu_star: pd.Series,
    rank_window: int = 252,
    **feature_kwargs,
) -> pd.DataFrame:
    """B2 = 0.50·R_DRC + 0.30·R_HitRate + 0.20·R_VR (eq. 27). Each feature is directionally adjusted
    (−DRC, HitRate, 1−VR_agg) then percentile-ranked over the prior `rank_window` bars. Returns the
    raw features, their ranks, and B2. (Rank is intra-instrument & temporal — see the module note.)"""
    f = block2_features(closes, mu_star, **feature_kwargs)
    r_drc = rolling_percentile_rank(-f["drc"], window=rank_window)
    r_hit = rolling_percentile_rank(f["hit_rate"], window=rank_window)
    r_vr = rolling_percentile_rank(1.0 - f["vr_agg"], window=rank_window)
    b2 = 0.50 * r_drc + 0.30 * r_hit + 0.20 * r_vr
    return pd.DataFrame(
        {
            "drc": f["drc"], "hit_rate": f["hit_rate"], "vr_agg": f["vr_agg"],
            "r_drc": r_drc, "r_hit_rate": r_hit, "r_vr": r_vr, "b2": b2,
        },
        index=closes.index,
    )


# ── P3: Block 1 — Mean Reliability (doc 01 §B1, eq. 15–20) ─────────────────────
#
# "Is the equilibrium mean μ* trustworthy enough to anchor analysis?" All Block-1 features are
# causal historical computations (no forward returns), so the only temporal risk is window
# off-by-one. σ here is the residual scale (the z-score denominator) — the quantity whose drift /
# regime-shift would invalidate z-construction.
import warnings  # noqa: E402

from statsmodels.tsa.stattools import adfuller, kpss  # noqa: E402

from app.services import analytics  # noqa: E402

HL_OPT: float = 10.0  # FROZEN optimal half-life for daily strategies (doc 01 eq. 28).


def mean_stability(closes: pd.Series, mu_star: pd.Series, w: int = 60, k: int = 20) -> pd.Series:
    """Mean Stability Index (eq. 17–18), the dominant Block-1 feature:

        MeanDrift_t = |μ_t − μ_{t-k}| / σ_t  (clipped at 3.0),   MeanStab_t = 1/(1+MeanDrift_t).

    μ_t = trailing arithmetic mean of price over w; σ_t = trailing std of the residual ε = P−μ* over
    w (the z-score denominator — drift measured in deviation-σ, matching the doc's "0.5σ" language).
    A drifting trading mean → large drift → MeanStab → 0. Returns NaN during warmup; if σ=0 with no
    drift, stability is 1 (perfectly stable)."""
    mu_roll = closes.rolling(window=w, min_periods=2).mean().to_numpy()
    sigma = (closes - mu_star).rolling(window=w, min_periods=2).std().to_numpy()
    n = len(closes)
    num = np.full(n, np.nan)
    num[k:] = np.abs(mu_roll[k:] - mu_roll[:-k])
    with np.errstate(divide="ignore", invalid="ignore"):
        drift = num / sigma
    zero_sigma = sigma <= 0
    drift = np.where(zero_sigma, np.where(num == 0, 0.0, 3.0), drift)
    drift = np.clip(drift, 0.0, 3.0)
    stab = 1.0 / (1.0 + drift)
    stab[~np.isfinite(num) | ~np.isfinite(sigma)] = np.nan
    # restore the legitimate σ=0,drift=0 → stab=1 case zeroed by the finite mask above
    fixable = (np.isfinite(num)) & zero_sigma & (num == 0)
    stab[fixable] = 1.0
    return pd.Series(stab, index=closes.index)


def variance_stability(closes: pd.Series, mu_star: pd.Series, w: int = 20, k: int = 20) -> pd.Series:
    """Variance Stability Index (eq. 19): VarStab_t = 1 − |σ_t/σ_{t-k} − 1|, clipped at 0. σ = trailing
    std of the residual over w. 1 = σ unchanged vs k bars ago; 0 = σ doubled/halved (regime shift)."""
    sigma = (closes - mu_star).rolling(window=w, min_periods=2).std().to_numpy()
    n = len(closes)
    out = np.full(n, np.nan)
    for t in range(k, n):
        s_now, s_prev = sigma[t], sigma[t - k]
        if not (np.isfinite(s_now) and np.isfinite(s_prev)) or s_prev <= 0:
            continue
        out[t] = max(0.0, 1.0 - abs(s_now / s_prev - 1.0))
    return pd.Series(out, index=closes.index)


def adf_kpss_pvalues(closes: pd.Series, w: int = 60) -> pd.DataFrame:
    """Rolling ADF and KPSS p-values on the trailing w-bar PRICE window (eq. 15–16).
    ADF lag p = ⌊(w/100)^¼⌋ (Schwert), KPSS lag ℓ = ⌊4(T/100)^¼⌋. Both regression='c'.
    Rank directions (applied by caller): −p_ADF (lower = more stationary), +p_KPSS (higher = fails to
    reject stationarity). Low-power at small w by design (doc 01 §B1.1 — supporting evidence only)."""
    x = closes.to_numpy(dtype=float)
    n = len(x)
    p_adf = np.full(n, np.nan)
    p_kpss = np.full(n, np.nan)
    adf_lag = int((w / 100.0) ** 0.25)
    kpss_lag = int(4.0 * (w / 100.0) ** 0.25)
    for t in range(n):
        if t + 1 < w:
            continue
        win = x[t - w + 1 : t + 1]
        if np.std(win) <= 0:
            continue
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")  # KPSS p-value interpolation warnings
                p_adf[t] = float(adfuller(win, maxlag=adf_lag, autolag=None, regression="c")[1])
                p_kpss[t] = float(kpss(win, regression="c", nlags=kpss_lag)[1])
        except Exception:
            continue
    return pd.DataFrame({"p_adf": p_adf, "p_kpss": p_kpss}, index=closes.index)


def block1_score(
    closes: pd.Series, mu_star: pd.Series, rank_window: int = 252,
    msi_w: int = 60, vsi_w: int = 20, k: int = 20, adf_w: int = 60,
) -> pd.DataFrame:
    """B1 = 0.30·(R_ADF+R_KPSS)/2 + 0.50·R_MSI + 0.20·R_VSI (eq. 20)."""
    msi = mean_stability(closes, mu_star, msi_w, k)
    vsi = variance_stability(closes, mu_star, vsi_w, k)
    pv = adf_kpss_pvalues(closes, adf_w)
    r_adf = rolling_percentile_rank(-pv["p_adf"], window=rank_window)
    r_kpss = rolling_percentile_rank(pv["p_kpss"], window=rank_window)
    r_msi = rolling_percentile_rank(msi, window=rank_window)
    r_vsi = rolling_percentile_rank(vsi, window=rank_window)
    b1 = 0.30 * (r_adf + r_kpss) / 2.0 + 0.50 * r_msi + 0.20 * r_vsi
    return pd.DataFrame(
        {"msi": msi, "vsi": vsi, "p_adf": pv["p_adf"], "p_kpss": pv["p_kpss"],
         "r_adf": r_adf, "r_kpss": r_kpss, "r_msi": r_msi, "r_vsi": r_vsi, "b1": b1},
        index=closes.index,
    )


# ── P3: Block 3 — Tradability (doc 01 §B3, eq. 28–34) ──────────────────────────
#
# "Even if reversion exists, can it be extracted now?" Block 3 modulates timing/sizing — it must NOT
# suppress a strong Block-2 signal (doc 01 §B3 intro). Transaction-cost filter uses the c-free
# fallback (eq. doc 01:714) since spread data is unavailable — no unfrozen `c` knob introduced.


# DOC INCONSISTENCY (surfaced, resolved toward prose intent):
# eq. 28 is typed `max(0, 1 − |ln HL − ln HL_opt| / ln 2)`, but that hits 0 at HL=5 and HL=20. The
# SAME paragraph (doc 01 §B3.1) states the score "reaches 0 at HL ≤ 2.5 or HL ≥ 40" — a factor-of-4
# band each side of HL_opt=10, with explicit economic reasoning (HL<2.5 microstructure noise, HL>40
# costs erode). The 2.5/40 zeros require denominator ln 4 (= 2·ln 2); the `/ln 2` coefficient is a
# typo. We implement the prose-stated band (`/ln 4`). Flagged for the record.
_HL_BAND_DENOM: float = np.log(4.0)


def hl_proximity_value(hl: float | None, hl_opt: float = HL_OPT) -> float:
    """Pure half-life proximity score (doc 01 §B3.1 prose band): 1.0 at HL=HL_opt, down in log-space
    to 0 at HL_opt/4 and HL_opt·4 (2.5 and 40 for HL_opt=10). 0 when HL is None/≤0 (κ̂≤0)."""
    if hl is None or hl <= 0:
        return 0.0
    return max(0.0, 1.0 - abs(np.log(hl) - np.log(hl_opt)) / _HL_BAND_DENOM)


def halflife_proximity(
    closes: pd.Series, mu_star: pd.Series, window: int = 120, hl_opt: float = HL_OPT,
) -> pd.Series:
    """Per-bar OU Half-Life Proximity (eq. 28, prose band). HL is recovered by reusing
    analytics.compute_halflife on the trailing residual ε = P − μ*. NOTE: the residual half-life is
    biased shorter than the underlying process half-life by the μ* smoother (a known μ*-dependent
    estimation effect — cf. the EMA-residual artifact in test_analytics_validation)."""
    resid = (closes - mu_star).to_numpy()
    n = len(closes)
    out = np.full(n, np.nan)
    for t in range(n):
        lo = t - window + 1
        if lo < 0:
            continue
        hl = analytics.compute_halflife(pd.Series(resid[lo : t + 1]))
        out[t] = hl_proximity_value(hl, hl_opt)
    return pd.Series(out, index=closes.index)


def vol_compression(closes: pd.Series, w: int = 20, k: int = 5, vp_window: int = 252) -> pd.DataFrame:
    """Volatility Compression (eq. 29–30): VC = −(RV_t − RV_{t-k})/RV_{t-k} (positive = vol falling);
    VCscore = VC·(1 − VP/100), penalising compression from an already-extreme vol level."""
    rv = realized_vol(closes, window=w)
    vc = -(rv - rv.shift(k)) / rv.shift(k)
    vp = vol_percentile(rv, window=vp_window)
    vcscore = vc * (1.0 - vp / 100.0)
    return pd.DataFrame({"rv": rv, "vc": vc, "vp": vp, "vcscore": vcscore}, index=closes.index)


def tcf_score(closes: pd.Series, w: int = 20, vp_window: int = 252) -> pd.Series:
    """Transaction Cost Filter — c-free fallback (doc 01:714, spread data unavailable):
    TCFscore = max(0, 1 − VP/100). High realized-vol percentile → costs more likely to dominate → low score."""
    rv = realized_vol(closes, window=w)
    vp = vol_percentile(rv, window=vp_window)
    return (1.0 - vp / 100.0).clip(lower=0.0)


def block3_score(closes: pd.Series, mu_star: pd.Series, rank_window: int = 252,
                 hl_window: int = 120) -> pd.DataFrame:
    """B3 = (1/3)·(R_HL + R_VC + R_TCF) (eq. 34)."""
    hl = halflife_proximity(closes, mu_star, window=hl_window)
    vcf = vol_compression(closes)
    tcf = tcf_score(closes)
    r_hl = rolling_percentile_rank(hl, window=rank_window)
    r_vc = rolling_percentile_rank(vcf["vcscore"], window=rank_window)
    r_tcf = rolling_percentile_rank(tcf, window=rank_window)
    b3 = (r_hl + r_vc + r_tcf) / 3.0
    return pd.DataFrame(
        {"hl_score": hl, "vc_score": vcf["vcscore"], "tcf_score": tcf,
         "r_hl": r_hl, "r_vc": r_vc, "r_tcf": r_tcf, "b3": b3},
        index=closes.index,
    )


# ── P4: Master aggregation (doc 01 eq. 13) ─────────────────────────────────────

def compute_mrscore(
    closes: pd.Series,
    mu_star: pd.Series,
    rank_window: int = 252,
    est_window: int = 252,
    z_window: int = 60,
    horizons: tuple[int, ...] = (1, 3, 5),
    min_obs: int = 120,
    hl_window: int = 120,
    adf_w: int = 60,
) -> pd.DataFrame:
    """MRScore_t = 0.20·B1_t + 0.60·B2_t + 0.20·B3_t (eq. 13), per bar, causal.

    `mu_star` is supplied by the caller (EMA, causal) — one-way DAG: MRScore never recomputes or
    feeds back into μ*. Returns blocks, master score, the directionally-adjusted feature ranks (for
    the contribution decomposition), AND the raw artifact-resistant Block-2 features (drc/hit_rate/
    vr_agg) — the latter are the genuine cross-instrument discriminators (the self-ranked score is
    within-instrument relative; see the normalization finding, docs/research)."""
    b1 = block1_score(closes, mu_star, rank_window=rank_window, adf_w=adf_w)
    b2 = block2_score(closes, mu_star, rank_window=rank_window, window=est_window,
                      z_window=z_window, horizons=horizons, min_obs=min_obs)
    b3 = block3_score(closes, mu_star, rank_window=rank_window, hl_window=hl_window)

    mrscore = 0.20 * b1["b1"] + 0.60 * b2["b2"] + 0.20 * b3["b3"]
    return pd.DataFrame(
        {
            "mrscore": mrscore,
            "b1": b1["b1"], "b2": b2["b2"], "b3": b3["b3"],
            # Block-1 feature ranks
            "r_adf": b1["r_adf"], "r_kpss": b1["r_kpss"], "r_msi": b1["r_msi"], "r_vsi": b1["r_vsi"],
            # Block-2 feature ranks
            "r_drc": b2["r_drc"], "r_hit_rate": b2["r_hit_rate"], "r_vr": b2["r_vr"],
            # Block-3 feature ranks
            "r_hl": b3["r_hl"], "r_vc": b3["r_vc"], "r_tcf": b3["r_tcf"],
            # Raw Block-2 features (artifact-resistant cross-instrument discriminators)
            "drc": b2["drc"], "hit_rate": b2["hit_rate"], "vr_agg": b2["vr_agg"],
        },
        index=closes.index,
    )
