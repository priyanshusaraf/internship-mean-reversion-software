"""
Arm A v2 — Cycle 1: real-data POSITIVE CONTROL on β=1 definitional calendar spreads.

Implements doc 20 (pre-registration + freeze) EXACTLY. ADDITIVE & ISOLATED: imports the FROZEN v1 primitives
from analytics_arm_a (load_leg, Spread, level_vr, surrogate_vr_ensemble, OU/RW/GARCH fits, the min-VR
multiplicity correction constants) and adds only what doc 20 requires:

  • spread_from_series      — wrap a VENDOR PRE-BUILT calendar (single already-differenced OHLC series, β=1)
                              into a v1 Spread. Headline is UNMASKED (vendor calendars have no leg seam to
                              remove; doc 20 §4 — the increment jump filter is a verdict-FLIPPING one-sided
                              lever toward VR→1, demonstrated in the doc-20 pre-freeze review). Optional
                              increment-MAD jump mask is provided for the ABLATION sweep ONLY.
  • _fit_ma1noise/_sim..    — MA(1) MICROSTRUCTURE-NOISE null (doc 20 §5, NEW gate family): a latent RANDOM
                              WALK + i.i.d. observation noise → ΔS = ε_t + (η_t−η_{t-1}), an MA(1) with the
                              real's negative incr ACF(1). NO mean reversion, but reproduces bid-ask bounce.
                              Beating it ⇒ sub-diffusion is MORE than bounce (genuine MR).
  • deseasonalize_causal    — subtract a CAUSAL trailing month-of-year seasonal mean (≤ t-1; §6.1 firewall).
  • evaluate_v2             — RW ∧ GARCH ∧ MA(1) headline gate (martingale-class), OU as non-gating reference,
                              multiplicity-corrected min-VR (inherited from doc 18a). Returns plain dicts.

The v1 analytics_arm_a.py is NOT modified.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from app.services.analytics_arm_a import (
    Spread, level_vr, surrogate_vr_ensemble, _valid_increment_mask,
    VR_Q_GRID, N_SURROGATE, SURR_PCTILE, load_leg,
)

# Frozen (doc 20 §5)
SEED: int = 20260604
MARTINGALE_GATE_V2: tuple[str, ...] = ("rw", "garch", "ma1")   # headline gate (doc 20 §6)
REPORT_FAMILIES_V2: tuple[str, ...] = ("rw", "garch", "ma1", "ou")
JUMP_K_SWEEP: tuple[float, ...] = (6.0, 8.0, 10.0, float("inf"))  # ∞ = unmasked (headline)
JUMP_W: int = 60


# ── Pre-built calendar adapter (β=1; UNMASKED headline) ────────────────────────

def increment_jump_mask(s: np.ndarray, k: float = 8.0, window: int = JUMP_W) -> np.ndarray:
    """ABLATION-ONLY (doc 20 §4). Causal increment-space robust-scale gate on a zero-crossing spread:
    flag bar t (the increment landing on t) iff |ΔS_t| > k · 1.4826 · trailing-MAD(ΔS over ≤ t-1). Returns a
    bool length n with mask[t]=True ⇒ the increment into bar t is excluded. k=∞ ⇒ no masking. Strictly
    trailing (≤ t-1) → §6.1 causal. This is NEVER the headline; doc 20 demonstrated it can only bias VR→1."""
    s = np.asarray(s, dtype=float)
    n = len(s)
    mask = np.zeros(n, dtype=bool)
    if not np.isfinite(k):
        return mask
    d = np.diff(s)                       # d[i] is the increment into bar i+1
    for i in range(len(d)):
        lo = max(0, i - window)
        ref = d[lo:i]                    # strictly trailing increments (≤ t-1)
        ref = ref[np.isfinite(ref)]
        if ref.size < 10 or not np.isfinite(d[i]):
            continue
        med = np.median(ref)
        mad = np.median(np.abs(ref - med))
        if mad <= 0:
            continue
        if abs(d[i] - med) > k * 1.4826 * mad:
            mask[i + 1] = True
    return mask


def spread_from_series(name: str, df: pd.DataFrame, *, date_min: str | None = None,
                       jump_k: float = float("inf"), jump_window: int = JUMP_W) -> Spread:
    """Wrap a vendor PRE-BUILT calendar (β=1) into a v1 Spread. NaN closes dropped (never imputed; doc 20 §4).
    `date_min` applies the frozen dense-era trim. `jump_k=∞` (default) = UNMASKED headline; finite jump_k is
    the ablation. beta≡1 (definitional → zero rolling-β DOF → cannot carry the v1 β-update artifact)."""
    d = df.copy()
    if date_min is not None:
        d = d[d.index >= pd.Timestamp(date_min, tz="UTC")]
    d = d[np.isfinite(d["close"].to_numpy(dtype=float))]      # drop NaN closes
    n = len(d)
    s_close = d["close"].to_numpy(dtype=float)
    s_open = d["open"].to_numpy(dtype=float) if "open" in d.columns else s_close.copy()
    roll = increment_jump_mask(s_close, k=jump_k, window=jump_window)   # all-False when unmasked
    if {"open", "high", "low", "close"}.issubset(d.columns):
        o, h, l, c = (d[k_].to_numpy(dtype=float) for k_ in ("open", "high", "low", "close"))
        flat = (o == h) & (h == l) & (l == c)
    else:
        flat = np.zeros(n, dtype=bool)
    return Spread(
        name=name, s_close=s_close, s_open=s_open, beta=np.ones(n),
        roll_transition=roll, flat_bar=flat, index=d.index,
        meta={"beta_mode": "one_definitional", "n": int(n), "jump_k": jump_k,
              "n_jump_masked": int(roll.sum()), "date_start": str(d.index[0].date()),
              "date_end": str(d.index[-1].date()), "flat_pct": round(100.0 * float(flat.mean()), 3)},
    )


# ── Causal deseasonalization (trailing month-of-year mean; ≤ t-1) ──────────────

def deseasonalize_causal(s: np.ndarray, index: pd.DatetimeIndex, min_prior: int = 2) -> np.ndarray:
    """S_deseason[t] = S[t] − (causal trailing mean of S over STRICTLY-PRIOR bars in the same calendar month).
    Uses only data ≤ t-1 (§6.1). Until `min_prior` prior same-month bars exist, falls back to the causal
    running overall mean (also ≤ t-1). Removes the deterministic month-of-year cycle without lookahead."""
    s = np.asarray(s, dtype=float)
    months = index.month.to_numpy()
    out = np.empty_like(s)
    sum_m = np.zeros(13); cnt_m = np.zeros(13)
    run_sum = 0.0; run_cnt = 0
    for t in range(len(s)):
        m = int(months[t])
        seasonal = (sum_m[m] / cnt_m[m]) if cnt_m[m] >= min_prior else (run_sum / run_cnt if run_cnt else 0.0)
        out[t] = s[t] - seasonal
        if np.isfinite(s[t]):
            sum_m[m] += s[t]; cnt_m[m] += 1
            run_sum += s[t]; run_cnt += 1
    return out


# ── MA(1) microstructure-noise null (NEW gate family, doc 20 §5) ───────────────

def _fit_ma1noise(incr: np.ndarray) -> dict:
    """Latent-RW + i.i.d.-observation-noise (bid-ask bounce) null. Solve so the simulated ΔS reproduces the
    real Var(ΔS)=v1 and incr ACF(1)=ρ:  ΔS_t = ε_t + (η_t − η_{t-1}),  σ_η² = −ρ·v1,  σ_w² = v1·(1+2ρ).
    ρ clamped to (−0.49, 0]: a positive/zero ACF(1) means no bounce to model → degenerates to pure RW
    (σ_η=0), i.e. the MA(1) null is then identical to RW (honest, not silent)."""
    incr = np.asarray(incr, dtype=float)
    incr = incr[np.isfinite(incr)]
    v1 = float(np.var(incr, ddof=1))
    if v1 <= 0 or incr.size < 30:
        return {"sigma_w": float(np.sqrt(max(v1, 0.0))), "sigma_eta": 0.0, "rho": 0.0}
    rho = float(np.corrcoef(incr[1:], incr[:-1])[0, 1]) if incr.size > 2 else 0.0
    rho = float(np.nan_to_num(rho, nan=0.0))
    rho = min(0.0, max(-0.49, rho))                 # only model NEGATIVE (bounce) autocorr; clamp to MA(1) range
    sig_eta2 = -rho * v1
    sig_w2 = v1 * (1.0 + 2.0 * rho)                 # ≥ v1·0.02 > 0 for rho ≥ -0.49
    sig_eta2 = sig_eta2 if sig_eta2 > 0 else 0.0     # coerce -0.0 / negative → positive 0.0
    sig_w2 = sig_w2 if sig_w2 > 0 else 0.0
    return {"sigma_w": float(np.sqrt(sig_w2)), "sigma_eta": float(np.sqrt(sig_eta2)), "rho": rho}


def _sim_ma1noise(params: dict, n: int, rng: np.random.Generator) -> np.ndarray:
    """Latent RW (innovation σ_w) + i.i.d. observation noise (σ_η). Observed level S = W + η. A MARTINGALE in
    the latent level (NO mean reversion) whose increments carry the real's negative ACF(1)."""
    sw = float(params["sigma_w"]); sw = sw if (np.isfinite(sw) and sw > 0) else 0.0
    se = float(params["sigma_eta"]); se = se if (np.isfinite(se) and se > 0) else 0.0
    w = np.concatenate([[0.0], np.cumsum(rng.normal(0.0, sw, n - 1))])
    eta = rng.normal(0.0, se, n)
    return w + eta


def ma1_vr_ensemble(spread: Spread, *, qs=VR_Q_GRID, n_draws: int = N_SURROGATE, seed: int = SEED):
    """N matched MA(1)-noise VR(q) draws — same length, SAME invalid mask, IDENTICAL VR extraction as the
    real (bias-cancel), mirroring v1 surrogate_vr_ensemble for the rw/garch/ou families."""
    s = spread.s_close
    invalid = spread.roll_transition | ~np.isfinite(spread.beta)
    valid1 = _valid_increment_mask(s, invalid)
    params = _fit_ma1noise(np.diff(s)[valid1])
    n = len(s)
    rng = np.random.default_rng(seed)
    ens = {q: np.full(n_draws, np.nan) for q in qs}
    for d in range(n_draws):
        surr = _sim_ma1noise(params, n, rng)
        vr_d = level_vr(surr, invalid, qs)
        for q in qs:
            ens[q][d] = vr_d[q]["vr"]
    return ens, params


# ── v2 verdict (RW ∧ GARCH ∧ MA1 gate; OU reference; min-VR corrected) ─────────

def _family_pvalue(ens: dict, qs, real_vr: dict, real_min: float) -> dict:
    """Per-family: 5th-pct per horizon + multiplicity-corrected min-VR p (real best-horizon VR vs surrogate's
    OWN best-horizon null) — identical statistic to v1 evaluate_spread."""
    mat = np.column_stack([ens[q] for q in qs])
    per_h = {}
    for j, q in enumerate(qs):
        col = mat[:, j][np.isfinite(mat[:, j])]
        p5 = float(np.percentile(col, SURR_PCTILE)) if col.size >= 20 else np.nan
        below = bool(np.isfinite(real_vr[q]) and np.isfinite(p5) and real_vr[q] < p5 and real_vr[q] < 1.0)
        per_h[q] = {"p5": p5, "real_below_p5": below,
                    "surr_median": float(np.median(col)) if col.size else np.nan}
    surr_min = np.nanmin(mat, axis=1); surr_min = surr_min[np.isfinite(surr_min)]
    if surr_min.size >= 20 and np.isfinite(real_min):
        p_val = (1.0 + float(np.sum(surr_min <= real_min))) / (surr_min.size + 1.0)
    else:
        p_val = np.nan
    return {"per_horizon": per_h, "min_vr_p_value": p_val,
            "separated_corrected": bool(np.isfinite(p_val) and p_val < SURR_PCTILE / 100.0 and real_min < 1.0)}


def evaluate_v2(spread: Spread, *, qs=VR_Q_GRID, seed: int = SEED) -> dict:
    """doc 20 §6 read for one β=1 calendar. Headline confirm = RW ∧ GARCH ∧ MA(1) (multiplicity-corrected
    min-VR, 5th pct, real_min<1). OU reported as a non-gating stringency reference. Plain-dict output."""
    real = level_vr(spread.s_close, spread.roll_transition | ~np.isfinite(spread.beta), qs)
    real_vr = {q: real[q]["vr"] for q in qs}
    real_min = float(np.nanmin([real_vr[q] for q in qs])) if any(np.isfinite(real_vr[q]) for q in qs) else np.nan

    per_family = {}
    for fam in ("rw", "garch", "ou"):
        ens = surrogate_vr_ensemble(spread, fam, qs=qs, n_draws=N_SURROGATE, seed=seed)
        per_family[fam] = _family_pvalue(ens, qs, real_vr, real_min)
    ma1_ens, ma1_params = ma1_vr_ensemble(spread, qs=qs, n_draws=N_SURROGATE, seed=seed)
    per_family["ma1"] = _family_pvalue(ma1_ens, qs, real_vr, real_min)
    per_family["ma1"]["fit"] = ma1_params

    sep = {f: per_family[f]["separated_corrected"] for f in REPORT_FAMILIES_V2}
    confirmed_gate = all(sep[f] for f in MARTINGALE_GATE_V2)            # RW ∧ GARCH ∧ MA1
    confirmed_rw_garch_only = sep["rw"] and sep["garch"]               # diagnostic: what MA(1) adds
    return {
        "name": spread.name, "real_vr": real_vr, "real_min_vr": real_min,
        "separated": sep, "confirmed_gate_rw_garch_ma1": confirmed_gate,
        "confirmed_rw_garch_only": confirmed_rw_garch_only,
        "ma1_adds_kill": bool(confirmed_rw_garch_only and not sep["ma1"]),
        "per_family": {f: {"min_vr_p_value": per_family[f]["min_vr_p_value"],
                           "separated_corrected": per_family[f]["separated_corrected"],
                           "per_horizon": per_family[f]["per_horizon"]} for f in REPORT_FAMILIES_V2},
        "ma1_fit": ma1_params, "meta": spread.meta, "seed": seed,
    }
