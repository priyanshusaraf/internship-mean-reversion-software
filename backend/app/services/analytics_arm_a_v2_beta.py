"""
Arm A v2 — Cycle 2: Controlled-β admissibility engine.

Additive layer over the frozen v1/v2 primitives (analytics_arm_a.py + analytics_arm_a_v2.py).
Implements doc 30 §3 B1–B5 + the crack_beta_execution_prereg.md frozen protocol.

DOES NOT MODIFY analytics_arm_a.py or analytics_arm_a_v2.py.

B1  economic_anchor_beta     — β fixed at 1.0; zero β-update-noise by construction (F6)
B2  presample_ols_beta       — OLS on a pre-sample window, then FROZEN (F5)
B3  kalman_beta              — random-walk-β state space, FROZEN tiny q_beta (F1)
B4  longwindow_ols_beta      — causal_rolling_beta at frozen large W (F3, thin wrapper)
B5  ridge_beta               — rolling OLS shrunk toward target=1.0 with L2 penalty (F2)
B6  beta_update_variance_fraction — doc-19 decomposition gate (f_βupdate = M gate)
B7  synthetic_pair           — OU-pair / martingale / stress-null generators for §2.2-2.3
B8  run_synthetic_calibration_gate — orchestration: controls → per-family (P,N,M,C)

All β functions return a length-n float array with β[t] = the CAUSAL estimate used at bar t.
Convention: β[0..warm-1] = NaN (warm-up; masked in spread construction).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from app.services.analytics_arm_a import (
    Spread, level_vr, surrogate_vr_ensemble,
    causal_rolling_beta, VR_Q_GRID,
)
from app.services.analytics_arm_a_v2 import (
    evaluate_v2, ma1_vr_ensemble, _family_pvalue,
    SEED, MARTINGALE_GATE_V2,
)

# ── Frozen protocol constants (crack_beta_execution_prereg.md) ─────────────────
TAU_FUPDATE = 0.10                 # f_βupdate bound (M gate)
NO_MFG_BAND = (0.80, 1.20)        # VR(20) must stay within this on martingale pairs
SYNTH_N = 200                     # surrogate draws for synthetic gate
SYNTH_SEED = SEED                  # frozen seed
Q_GRID_CYCLE2 = (2, 5, 10, 20)    # frozen q grid (consistent with v1/v2)


# ── B1 — Economic anchor (F6): β ≡ 1.0, zero update noise ──────────────────────

def economic_anchor_beta(n: int) -> np.ndarray:
    """β fixed at 1.0 for all bars. Zero β-update variance. The definitional F6 family.
    In the normalized crack-spread context (both legs in $/barrel), this gives the crack
    margin at unit β — functionally identical to β=1 definitional calendars."""
    return np.ones(n, dtype=float)


# ── B2 — Pre-sample OLS (F5): estimated once, then frozen ─────────────────────

def presample_ols_beta(a: np.ndarray, b: np.ndarray,
                        pre_sample_fraction: float = 0.25) -> np.ndarray:
    """Estimate β via OLS on the first `pre_sample_fraction` of data, then apply that
    fixed β to all bars. Zero β-update variance during the test window (after pre-sample).
    Warm-up: the pre-sample window itself is warm-up (NaN). Causal: β_{pre-sample OLS}
    is estimated on data ≤ pre_sample_end, applied from bar (pre_sample_end + 1) onward."""
    n = len(a)
    pre_n = max(10, int(n * pre_sample_fraction))
    a_pre, b_pre = a[:pre_n], b[:pre_n]
    # OLS β = Cov(A,B) / Var(B) on pre-sample
    mask = np.isfinite(a_pre) & np.isfinite(b_pre)
    if mask.sum() < 10:
        return np.full(n, float("nan"))
    a_v, b_v = a_pre[mask], b_pre[mask]
    beta_hat = (np.cov(a_v, b_v, ddof=1)[0, 1] / np.var(b_v, ddof=1)
                if np.var(b_v, ddof=1) > 0 else 1.0)
    beta = np.full(n, float("nan"))
    beta[pre_n:] = beta_hat    # frozen β applied post-pre-sample
    return beta


# ── B3 — Kalman β (F1): random-walk-β state space, tiny process noise ─────────

def kalman_beta(a: np.ndarray, b: np.ndarray,
                q_beta: float = 0.0001) -> np.ndarray:
    """Causal Kalman filter for β under a random-walk-β model:
        β_t = β_{t-1} + w_t,  w_t ~ N(0, q_beta)
        A_t = β_t * B_t + v_t,  v_t ~ N(0, R_t)
    Where R_t = rolling residual variance (estimated from trailing 60 bars).
    β_{t|t-1} is used (one-step prediction before observing the bar) → strictly causal.
    Warm-up: first 30 bars NaN (insufficient for initial R estimation)."""
    n = len(a)
    beta = np.full(n, float("nan"))
    # Initialize
    warm = 30
    if n <= warm:
        return beta
    # Robust initialization: pre-warm OLS
    a_w, b_w = a[:warm], b[:warm]
    mask_w = np.isfinite(a_w) & np.isfinite(b_w)
    if mask_w.sum() < 5:
        return beta
    a_wv, b_wv = a_w[mask_w], b_w[mask_w]
    beta_hat = (np.cov(a_wv, b_wv, ddof=1)[0, 1] / np.var(b_wv, ddof=1)
                if np.var(b_wv, ddof=1) > 0 else 1.0)
    P = 1.0  # initial state variance
    b_hat = float(beta_hat)
    R_window = 60
    for t in range(warm, n):
        if not (np.isfinite(a[t]) and np.isfinite(b[t])):
            beta[t] = b_hat  # carry forward
            continue
        # Prediction step (causal: use previous estimate)
        b_pred = b_hat
        P_pred = P + q_beta
        # Output the causal prediction β_{t|t-1} for this bar
        beta[t] = b_pred
        # Measurement update (using current bar)
        B_t = b[t]
        # Estimate observation noise R from trailing residuals
        lo = max(warm, t - R_window)
        resid = a[lo:t] - beta[lo:t] * b[lo:t]
        resid = resid[np.isfinite(resid)]
        R = float(np.var(resid, ddof=1)) if len(resid) >= 5 else 1.0
        R = max(R, 1e-8)
        innov = a[t] - b_pred * B_t
        S = P_pred * B_t ** 2 + R
        K = P_pred * B_t / S if S > 0 else 0.0
        b_hat = b_pred + K * innov
        P = (1 - K * B_t) * P_pred
    return beta


# ── B4 — Long-window causal OLS (F3): thin wrapper over existing primitive ────

def longwindow_ols_beta(a: np.ndarray, b: np.ndarray,
                         W: int = 500) -> np.ndarray:
    """Causal rolling OLS at frozen large W. Delegates entirely to the frozen primitive
    analytics_arm_a.causal_rolling_beta — no new logic, just a frozen W parameter.
    β_{t|t-1} (shifted by 1 inside causal_rolling_beta) is used at bar t."""
    return causal_rolling_beta(a, b, window=W)


# ── B5 — Ridge shrinkage-β (F2): L2 penalty toward target ────────────────────

def ridge_beta(a: np.ndarray, b: np.ndarray,
               lam: float = 10.0, target: float = 1.0,
               W_base: int = 126) -> np.ndarray:
    """Ridge β: causal rolling OLS with L2 shrinkage toward `target`.
    β_ridge = (X'X + λI)^{-1} (X'y + λ·target) in scalar form
             = [Cov(A,B) + λ·target] / [Var(B) + λ]  (mean-centered, scalar B)
    Applied at t using data [t-W_base, t-1] — strictly causal.
    Warm-up: first W_base bars NaN."""
    n = len(a)
    beta = np.full(n, float("nan"))
    for t in range(W_base, n):
        lo = t - W_base
        a_w, b_w = a[lo:t], b[lo:t]
        mask = np.isfinite(a_w) & np.isfinite(b_w)
        if mask.sum() < max(10, W_base // 5):
            continue
        a_v, b_v = a_w[mask], b_w[mask]
        cov_ab = np.cov(a_v, b_v, ddof=1)[0, 1]
        var_b = np.var(b_v, ddof=1)
        beta_ols = cov_ab / var_b if var_b > 0 else target
        # Ridge formula: shrink ols toward target
        beta[t] = (var_b * beta_ols + lam * target) / (var_b + lam)
    # Shift one step for causality (use β estimated on ≤t-1 at bar t)
    beta = pd.Series(beta).shift(1).to_numpy()
    return beta


# ── B6 — β-update variance fraction (f_βupdate, the M gate) ──────────────────

def beta_update_variance_fraction(s_close: np.ndarray, beta: np.ndarray,
                                   b_close: np.ndarray) -> float:
    """Compute f_βupdate = Var[(β_{t-1} - β_{t-2}) × B_{t-1}] / Var[ΔS_t].
    The doc-19 decomposition: ΔS_t = (ΔA_t - β_{t-1}×ΔB_t) - (β_{t-1}-β_{t-2})×B_{t-1}.
    The second term is the β-update noise. Its variance share vs total spread increment
    variance is the M-gate statistic. Values near 0 = clean; values near 1 = artifact.
    Uses valid increments only (finite β, finite prices)."""
    n = len(s_close)
    # β-update term: (β_{t-1} - β_{t-2}) × B_{t-1}
    beta_diff = np.diff(beta)    # β[t-1] - β[t-2], length n-1
    b_lag = b_close[:-1]         # B_{t-1}, length n-1
    beta_update_term = beta_diff * b_lag  # length n-1
    # Total spread increment
    ds = np.diff(s_close)        # ΔS_t, length n-1
    # Valid mask: both must be finite
    valid = (np.isfinite(beta_update_term) & np.isfinite(ds) &
             np.isfinite(b_close[:-1]) & np.isfinite(beta[:-1]) & np.isfinite(beta[1:]))
    if valid.sum() < 20:
        return float("nan")
    ds_v = ds[valid]
    bu_v = beta_update_term[valid]
    var_ds = float(np.var(ds_v, ddof=1))
    var_bu = float(np.var(bu_v, ddof=1))
    if var_ds <= 0:
        return float("nan")
    return float(var_bu / var_ds)


# ── B7 — Synthetic pair generators ────────────────────────────────────────────

def gen_ou_pair(beta_star: float = 1.0, phi: float = 0.95, sigma_ou: float = 0.02,
                n: int = 5000, trend_b: float = 0.005, sigma_b: float = 0.05,
                seed: int = SYNTH_SEED) -> tuple[np.ndarray, np.ndarray]:
    """Positive control: A = β*×B + OU_deviation; B = trending RW + drift.
    The β-update-noise stress configuration: B trends strongly, so any β-update × B
    creates large spurious variance (the doc-19 failure mode). True spread = OU with VR<1."""
    rng = np.random.default_rng(seed)
    # B: trending random walk (the dangerous leg)
    B = np.cumsum(rng.normal(trend_b, sigma_b, n))
    # OU deviation: u_t = phi×u_{t-1} + eps; true spread = u
    u = np.zeros(n)
    u[0] = 0.0
    for t in range(1, n):
        u[t] = phi * u[t - 1] + rng.normal(0, sigma_ou)
    A = beta_star * B + u
    return A, B


def gen_martingale_pair(beta_star: float = 1.0, sigma_dev: float = 0.05,
                         n: int = 5000, trend_b: float = 0.005, sigma_b: float = 0.05,
                         seed: int = SYNTH_SEED) -> tuple[np.ndarray, np.ndarray]:
    """Z1 true-martingale: spread = pure RW (no MR). A = β*×B + RW_deviation."""
    rng = np.random.default_rng(seed)
    B = np.cumsum(rng.normal(trend_b, sigma_b, n))
    dev = np.cumsum(rng.normal(0, sigma_dev, n))  # pure RW deviation
    A = beta_star * B + dev
    return A, B


def gen_stress_null(beta_star: float = 1.0, sigma_dev: float = 0.05,
                     n: int = 5000, trend_b: float = 0.05, sigma_b: float = 0.05,
                     seed: int = SYNTH_SEED) -> tuple[np.ndarray, np.ndarray]:
    """Z2 doc-19 stress: B is STRONGLY trending (large drift).
    This is the exact configuration that makes (β_{t-1}-β_{t-2})×B_{t-1} huge, causing
    rolling-β to manufacture super-diffusion. True spread = RW (no MR)."""
    rng = np.random.default_rng(seed)
    # B: very strongly trending (drift = 10× normal)
    B = np.cumsum(rng.normal(trend_b, sigma_b, n))
    dev = np.cumsum(rng.normal(0, sigma_dev, n))  # true spread = RW
    A = beta_star * B + dev
    return A, B


def gen_independent_pair(n: int = 5000, sigma: float = 0.05,
                          seed: int = SYNTH_SEED) -> tuple[np.ndarray, np.ndarray]:
    """Z3 independent legs: A and B are independent RWs, β* = 0."""
    rng = np.random.default_rng(seed)
    A = np.cumsum(rng.normal(0, sigma, n))
    B = np.cumsum(rng.normal(0, sigma, n))
    return A, B


# ── B8 — Synthetic calibration gate ───────────────────────────────────────────

def _build_spread_from_beta(name: str, a: np.ndarray, b: np.ndarray,
                              beta: np.ndarray, n: int = 5000) -> Spread:
    """Construct a Spread object from pre-computed β array (no roll masking for synthetic data)."""
    s_close = a - beta * b
    invalid = ~np.isfinite(beta) | ~np.isfinite(s_close)
    return Spread(
        name=name,
        s_close=np.where(invalid, 0.0, s_close),  # zero-fill for VR (but invalid mask covers them)
        s_open=np.where(invalid, 0.0, s_close).copy(),
        beta=np.where(np.isfinite(beta), beta, 1.0),
        roll_transition=invalid.astype(bool),
        flat_bar=np.zeros(n, bool),
        index=pd.date_range("2000-01-03", periods=n, freq="B", tz="UTC"),
        meta={"synthetic": True, "n_invalid": int(invalid.sum())},
    )


def _eval_family_on_spread(sp: Spread, n_draws: int = SYNTH_N,
                            seed: int = SYNTH_SEED) -> dict:
    """Run RW/GARCH/MA1/OU evaluation on a Spread. Returns simplified result dict."""
    from app.services.analytics_arm_a_v2 import _family_pvalue, ma1_vr_ensemble
    qs = Q_GRID_CYCLE2
    invalid = sp.roll_transition | ~np.isfinite(sp.beta)
    real = level_vr(sp.s_close, invalid, qs)
    real_vr = {q: real[q]["vr"] for q in qs}
    real_min = float(np.nanmin([real_vr[q] for q in qs]))
    per_fam = {}
    for fam in ("rw", "garch", "ou"):
        ens = surrogate_vr_ensemble(sp, fam, qs=qs, n_draws=n_draws, seed=seed)
        per_fam[fam] = _family_pvalue(ens, qs, real_vr, real_min)
    ma1_ens, ma1_params = ma1_vr_ensemble(sp, qs=qs, n_draws=n_draws, seed=seed)
    per_fam["ma1"] = _family_pvalue(ma1_ens, qs, real_vr, real_min)
    confirmed = per_fam["rw"]["separated_corrected"] and per_fam["garch"]["separated_corrected"] and per_fam["ma1"]["separated_corrected"]
    vr20 = real_vr.get(20, float("nan"))
    return {
        "vr20": round(float(vr20), 4),
        "real_vr": {str(q): round(float(real_vr[q]), 4) for q in qs},
        "p_rw": round(float(per_fam["rw"]["min_vr_p_value"]), 4),
        "p_garch": round(float(per_fam["garch"]["min_vr_p_value"]), 4),
        "p_ma1": round(float(per_fam["ma1"]["min_vr_p_value"]), 4),
        "p_ou": round(float(per_fam["ou"]["min_vr_p_value"]), 4),
        "confirmed_rw_garch_ma1": bool(confirmed),
    }


def run_synthetic_calibration_gate(n: int = 5000, n_draws: int = SYNTH_N,
                                     seed: int = SYNTH_SEED) -> dict:
    """
    Full synthetic calibration gate per crack_beta_execution_prereg.md §C.
    Tests families F6, F5, F1, F3, F2 on 4 synthetic controls.
    Returns per-family P/N/M/C verdicts and admissibility.

    Families tested: economic_anchor (F6), presample_ols (F5), kalman (F1),
                     longwindow_ols (F3), ridge (F2).
    Controls: positive_control (P), Z1_martingale, Z2_stress, Z3_independent.
    """
    import numpy as np

    families = {
        "F6_economic_anchor": lambda a, b: economic_anchor_beta(len(a)),
        "F5_presample_ols":   lambda a, b: presample_ols_beta(a, b, 0.25),
        "F1_kalman":          lambda a, b: kalman_beta(a, b, q_beta=0.0001),
        "F3_longwindow_ols":  lambda a, b: longwindow_ols_beta(a, b, W=500),
        "F2_ridge":           lambda a, b: ridge_beta(a, b, lam=10.0, target=1.0, W_base=126),
    }

    controls = {
        "P_positive_control": gen_ou_pair(n=n, seed=seed),
        "Z1_martingale":      gen_martingale_pair(n=n, seed=seed + 1),
        "Z2_stress_null":     gen_stress_null(n=n, seed=seed + 2),
        "Z3_independent":     gen_independent_pair(n=n, seed=seed + 3),
    }

    results = {}

    for fname, beta_fn in families.items():
        fam_result = {}
        admissible_flags = {}

        for cname, (A, B) in controls.items():
            beta = beta_fn(A, B)
            sp = _build_spread_from_beta(f"{fname}_{cname}", A, B, beta, n)
            # VR evaluation
            ev = _eval_family_on_spread(sp, n_draws=n_draws, seed=seed)
            # f_βupdate (M gate) — only meaningful when β varies
            f_bu = beta_update_variance_fraction(sp.s_close, beta, B)
            ev["f_betaupdate"] = round(float(f_bu), 5) if np.isfinite(f_bu) else None
            ev["vr20_in_band"] = bool(
                ev["vr20"] is not None and np.isfinite(ev["vr20"]) and
                NO_MFG_BAND[0] <= ev["vr20"] <= NO_MFG_BAND[1]
            ) if cname.startswith("Z") else None
            ev["f_below_tau"] = bool(
                ev["f_betaupdate"] is not None and
                np.isfinite(ev["f_betaupdate"]) and
                ev["f_betaupdate"] < TAU_FUPDATE
            )
            fam_result[cname] = ev

            # Gate flags per control
            if cname == "P_positive_control":
                admissible_flags["P"] = bool(ev["confirmed_rw_garch_ma1"] and ev["vr20"] < 0.80)
            elif cname.startswith("Z"):
                admissible_flags[f"N_{cname}"] = bool(ev["vr20_in_band"])
                admissible_flags[f"M_{cname}"] = bool(ev["f_below_tau"])

        # Overall admissibility: P AND all N AND all M
        p_pass = admissible_flags.get("P", False)
        n_pass = all(v for k, v in admissible_flags.items() if k.startswith("N_"))
        m_pass = all(v for k, v in admissible_flags.items() if k.startswith("M_"))
        admissible = bool(p_pass and n_pass and m_pass)

        results[fname] = {
            "admissible": admissible,
            "P_pass": p_pass, "N_pass": n_pass, "M_pass": m_pass,
            "gate_flags": admissible_flags,
            "per_control": fam_result,
        }

    return results
