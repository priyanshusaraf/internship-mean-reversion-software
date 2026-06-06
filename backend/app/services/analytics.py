import numpy as np
import pandas as pd


# ── Estimator layer ───────────────────────────────────────────────────────────

def compute_ema(closes: pd.Series, span: int) -> pd.Series:
    """Causal EMA: adjust=False ensures no future information leaks into bar t."""
    return closes.ewm(span=span, adjust=False).mean()


def compute_full_ema(closes: pd.Series, span: int) -> pd.Series:
    """Full-information EMA: adjust=True re-weights using all observations.
    Still temporally firewalled — only operates on the data passed in.
    Larger gap vs compute_ema → the causal estimator is "behind" hindsight."""
    return closes.ewm(span=span, adjust=True).mean()


# ── Residual layer ────────────────────────────────────────────────────────────

def compute_residual(close: pd.Series, mu_star: pd.Series) -> pd.Series:
    return close - mu_star


def compute_zscore(residual: pd.Series, window: int) -> pd.Series:
    mu = residual.rolling(window=window, min_periods=1).mean()
    sigma = residual.rolling(window=window, min_periods=2).std()
    return (residual - mu) / sigma


# ── Diagnostics ───────────────────────────────────────────────────────────────

def compute_acf(series: pd.Series, lags: list[int] | None = None) -> dict[str, float]:
    """Autocorrelation at specified lags. Uses statsmodels FFT-based ACF."""
    from statsmodels.tsa.stattools import acf as _acf

    if lags is None:
        lags = [1, 5, 10, 20]

    clean = series.dropna()
    required = max(lags) + 2
    if len(clean) < required:
        return {f"lag{lag}": 0.0 for lag in lags}

    result = _acf(clean, nlags=max(lags), fft=True, alpha=None)
    return {f"lag{lag}": float(result[lag]) for lag in lags}


def compute_halflife(residuals: pd.Series) -> float | None:
    """OU half-life via OLS with intercept: Δy = λ·y[t-1] + μ + ε.
    λ < 0 → mean-reverting. half-life = -ln(2)/λ.
    The intercept (μ) is required to avoid bias when residuals have a nonzero mean
    (which occurs whenever EMA lags a trend). Without it, lambda is pulled toward
    zero by the mean-squared level of the series rather than its mean-reversion speed.
    Returns None if series is not mean-reverting or too short."""
    y = residuals.dropna()
    if len(y) < 10:
        return None

    delta_y = y.diff().dropna().values
    y_lagged = y.iloc[:-1].values

    n = min(len(delta_y), len(y_lagged))
    y_lagged, delta_y = y_lagged[:n], delta_y[:n]

    # OLS with intercept: design matrix [y_lagged | 1]
    X = np.column_stack([y_lagged, np.ones(n)])
    try:
        coeffs, _, _, _ = np.linalg.lstsq(X, delta_y, rcond=None)
    except np.linalg.LinAlgError:
        return None

    lam = float(coeffs[0])

    if lam >= 0 or np.isnan(lam):
        return None  # not mean-reverting

    # Apply ADF significance cutoff: reject the null of no mean-reversion only when
    # the t-statistic is below the 5% critical value (≈ -2.86 with intercept, MacKinnon 1994).
    # Without this, finite-sample bias can return a weakly negative lambda for random walks.
    y_hat = X @ coeffs
    err = delta_y - y_hat
    sigma2 = np.sum(err ** 2) / max(n - 2, 1)
    if sigma2 <= 0:
        return None
    try:
        var_lam = sigma2 * float(np.linalg.inv(X.T @ X)[0, 0])
    except np.linalg.LinAlgError:
        return None
    if var_lam <= 0:
        return None
    t_stat = lam / np.sqrt(var_lam)
    if t_stat > -2.86:
        return None  # not significant at 5% — treat as non-mean-reverting

    return float(-np.log(2) / lam)


def compute_innovation(close: pd.Series, mu_star: pd.Series) -> pd.Series:
    """One-step prediction error: close[t] - mu_star[t-1].
    Measures how surprised the causal estimator is at each new bar."""
    return close - mu_star.shift(1)


# ── Anchored Kalman μ* (2-state local-linear-trend) — spec v1 ──────────────────
#
# State:        x_t = [μ_t, v_t]ᵀ   (latent equilibrium level, equilibrium velocity)
# Transition:   F = [[1, 1], [0, 1]],  Q = diag(q_μ, q_v),  q_μ = κ·q_v
# Observation:  P_t = μ_t + ε,        H = [1, 0],  noise R_p (scalar)
#
# The velocity state is the ONLY thing distinguishing this from an EMA: a local-LEVEL
# Kalman filter is algebraically an EMA at steady state (spec §2.1). Velocity lets the
# equilibrium track a trend, so deviations are measured against a trend-adjusted μ* —
# the literal definition of "mean reversion inside trendy markets".
#
# Research residual = the one-step-ahead INNOVATION (P_t − μ_{t|t−1}), NOT the filtered
# residual (P_t − μ_{t|t}). The filtered residual has already absorbed P_t and would look
# circularly mean-reverting. Innovation is causal and white for a correct filter (spec §2.3).
#
# Parameter discipline (spec §2.4): exactly ONE dimensionless knob, SNR = q_v / R_p, frozen
# after a one-time calibration on synthetic OU. R_p is normalized once per series from a
# causal robust scale of returns — a unit normalization, NOT a fit.

KALMAN_KAPPA: float = 0.05  # FROZEN. q_μ = κ·q_v — small level "release valve" vs I(2) ringing.

# SNR (q_v / R_p) swept once on synthetic OU via scripts/calibrate_kalman.py over
# logspace(-9, 0, 28). The H2-admissible band (OU half-life recovery within tolerance) is
# SNR ≲ 4.6e-7 (effective span ≳ 54 bars); 1e-8 (effective span ≈ 141) sits inside it.
#
# HISTORY OF VERDICT (see docs/research/ for the full epistemic record):
#   • 05_kalman_v1_results_memo.md REJECTED this estimator on KC4 (alpha absorption) primary /
#     KC1 (no artifact reduction) secondary, citing the G-ABSORB gate (min 0.208 > 0.20).
#   • 06_kalman_equilibrium_research_update.md OVERTURNS that rejection. The replication audit
#     showed G-ABSORB is contaminated (trend-invariant AND κ-invariant — see scripts/audit_kalman.py)
#     and KC1's H1 gate is unsatisfiable by ANY causal smoother including EMA. The confirmatory
#     test (scripts/confirm_kalman.py, 360 paired conditions) found the real, robust advantage:
#     trend-adjusted residual CENTERING. EMA's innovation carries a deterministic lag bias
#     slope·span/2 (sign-agreement with true deviation ≈ 0.49); the velocity state removes it
#     (≈ 0.85). Signal is preserved (corr(ε,dev) ≈ 0.92, var_ratio ≈ 1.0), not absorbed.
#
# STATUS: AUTHORIZED for Step 1 (controlled real-market integration). The filter is wired into
# /diagnostics as a RESEARCH COMPARISON estimator alongside EMA — it is NOT the production μ*
# (EMA remains the default). Equations below are FROZEN per the v1 spec; this integration does
# not tune SNR, change κ, or alter the model. Step 1 falsification-tests whether the synthetic
# centering advantage survives real markets (false centering, violent regimes); see doc 06 §11.
KALMAN_SNR: float = 1e-8

KALMAN_WARMUP: int = 60  # bars used for the one-time R_p (returns MAD) normalization.


def _robust_return_scale(prices: np.ndarray, warmup: int) -> float:
    """R_p = (1.4826 · MAD(ΔP over warmup window))² — causal, one-time unit normalization.

    1.4826 makes MAD a consistent estimator of σ for Gaussian data. Using returns (ΔP)
    rather than levels keeps the scale meaningful for trending series."""
    w = min(warmup, len(prices))
    if w < 2:
        return 1.0
    dP = np.diff(prices[:w])
    if dP.size == 0:
        return 1.0
    mad = float(np.median(np.abs(dP - np.median(dP))))
    R_p = (1.4826 * mad) ** 2
    return max(R_p, 1e-12)


def compute_kalman_mu_star(
    closes: pd.Series,
    snr: float = KALMAN_SNR,
    kappa: float = KALMAN_KAPPA,
    warmup: int = KALMAN_WARMUP,
) -> pd.DataFrame:
    """Forward-only 2-state Kalman filter (spec §2.5). Causal by construction — at bar t it
    consumes only prices[0..t], so the temporal firewall is satisfied automatically.

    Returns a DataFrame indexed like `closes` with columns:
        mu_star_kalman   — published μ* = μ_{t|t} (posterior equilibrium, for charting)
        epsilon_kalman   — innovation P_t − μ_{t|t−1} (the RESEARCH residual; all stats use this)
        kalman_velocity  — v_{t|t}
        kalman_gain      — K_t[0] (gain on the level component)
        kalman_state_var — P_{t|t}[0,0] (equilibrium posterior variance)
    """
    n = len(closes)
    idx = closes.index
    cols = ["mu_star_kalman", "epsilon_kalman", "kalman_velocity",
            "kalman_gain", "kalman_state_var"]
    if n == 0:
        return pd.DataFrame({c: [] for c in cols}, index=idx)

    prices = closes.to_numpy(dtype=float)

    R_p = _robust_return_scale(prices, warmup)
    q_v = snr * R_p
    q_mu = kappa * q_v

    F = np.array([[1.0, 1.0], [0.0, 1.0]])
    Q = np.array([[q_mu, 0.0], [0.0, q_v]])
    H = np.array([1.0, 0.0])
    I2 = np.eye(2)

    # Diffuse initialization (spec §2.5): μ_0 = P_0, v_0 = 0, large prior variance.
    x = np.array([prices[0], 0.0])
    P = np.diag([10.0 * R_p, 10.0 * R_p])

    mu_filt = np.empty(n)
    eps = np.empty(n)
    vel = np.empty(n)
    gain = np.empty(n)
    state_var = np.empty(n)

    for t in range(n):
        # Predict
        x_pred = F @ x
        P_pred = F @ P @ F.T + Q
        # Innovation (research residual): one-step-ahead, pre-update
        y = prices[t] - x_pred[0]
        S = P_pred[0, 0] + R_p
        K = (P_pred @ H) / S  # 2-vector
        # Update
        x = x_pred + K * y
        P = (I2 - np.outer(K, H)) @ P_pred
        # Store
        mu_filt[t] = x[0]
        eps[t] = y
        vel[t] = x[1]
        gain[t] = K[0]
        state_var[t] = P[0, 0]

    return pd.DataFrame(
        {
            "mu_star_kalman": mu_filt,
            "epsilon_kalman": eps,
            "kalman_velocity": vel,
            "kalman_gain": gain,
            "kalman_state_var": state_var,
        },
        index=idx,
    )


def kalman_effective_span(gain_inf: float) -> float:
    """Translate a steady-state level gain K_∞ into the EMA span with the same gain
    (α = K_∞ ⇒ span = 2/α − 1). Used to express "3× effective span" warmup/recovery
    windows in the validation gates (spec §5, OP-1 / V-BRK)."""
    if gain_inf <= 0 or gain_inf >= 1:
        return float("inf")
    return 2.0 / gain_inf - 1.0


def kalman_steady_state_gain(snr: float = KALMAN_SNR, kappa: float = KALMAN_KAPPA) -> float:
    """Steady-state level gain K_∞[0] of the FROZEN 2-state filter, via Riccati iteration
    with R_p = 1 (gain is scale-invariant in R_p). Deterministic function of the frozen
    constants — NOT a fit, NOT a tuning knob. Used only to derive the matched-effective-span
    EMA (the velocity-OFF counterfactual, doc 06 §7.1) for instrumentation."""
    R = 1.0
    q_v = snr * R
    q_mu = kappa * q_v
    F = np.array([[1.0, 1.0], [0.0, 1.0]])
    Q = np.array([[q_mu, 0.0], [0.0, q_v]])
    H = np.array([1.0, 0.0])
    I2 = np.eye(2)
    P = np.diag([10.0, 10.0])
    K = np.zeros(2)
    for _ in range(8000):
        P_pred = F @ P @ F.T + Q
        S = P_pred[0, 0] + R
        K_new = (P_pred @ H) / S
        P = (I2 - np.outer(K_new, H)) @ P_pred
        if np.max(np.abs(K_new - K)) < 1e-13:
            K = K_new
            break
        K = K_new
    return float(K[0])


# ── Velocity-absorption instrumentation (Step 2A — false-centering falsification) ───────
# Single research question: did the Kalman velocity state remove economically useful
# mean-reversion signal (Hypothesis B), or only local drift/lag (Hypothesis A)?
#
# The discriminator is the "restoration" identity. With the matched-span EMA prediction
# emap[t] = EMA_m[t−1] and the recovered Kalman one-step prediction μK_pred[t] = close[t] −
# ε_kalman[t] (= μ_{t|t−1}, derived from the FROZEN output — the filter is NOT recomputed):
#     δ[t]  = μK_pred[t] − emap[t]                 (velocity contribution at matched responsiveness)
#     εK[t] = ε_kalman[t]                          (velocity-ON residual)
#     εR[t] = εK[t] + δ[t] = close[t] − emap[t]    (velocity-OFF residual ≡ matched-EMA pred)
# If εR predicts its own decay materially better than εK (β more negative), the velocity
# removed reversion → evidence for B. If εK ≈ εR, velocity removed only trend → supports A.


def _walk_forward_decay(eps: np.ndarray, h: int, min_train: int = 30) -> tuple[float, float, int]:
    """Minimal walk-forward predictive-decay test for one residual series.

    Pairs (x_s = ε_s, y_s = ε_{s+h} − ε_s) describe h-step decay. Split the series CHRONOLOGICALLY
    in half: fit OLS (α, β) on the FIRST half (the past) only, then predict decay on the held-out
    SECOND half (the future). β < 0 ⇒ larger deviations predict snapback. Returns
    (β_train, R²_oos, n_test).

    Causal by construction: training strictly precedes the test; the predictor x_t = ε_t is known
    at t, the target ε_{t+h} realizes later. R²_oos is out-of-sample (skill vs predicting the
    test-period mean decay) and MAY be negative — not clamped. β is scale-free. A single split is
    the minimal honest walk-forward; expanding-window / multi-fold is the deferred upgrade. No
    surrogate, bootstrap, or significance machinery (deferred)."""
    n = len(eps)
    m = n - h                                   # usable pairs: s in [0, m)
    if m < 2 * min_train:
        return float("nan"), float("nan"), 0
    x_all = eps[:m]
    y_all = eps[h:h + m] - eps[:m]
    finite = np.isfinite(x_all) & np.isfinite(y_all)
    split = m // 2                              # train = [0, split), test = [split, m)
    tr = finite.copy(); tr[split:] = False
    te = finite.copy(); te[:split] = False
    xtr, ytr = x_all[tr], y_all[tr]
    xte, yte = x_all[te], y_all[te]
    if len(xtr) < min_train or len(xte) < min_train or np.var(xtr) < 1e-18:
        return float("nan"), float("nan"), int(len(xte))
    ntr = len(xtr)
    denom = ntr * np.sum(xtr * xtr) - np.sum(xtr) ** 2
    if abs(denom) < 1e-18:
        return float("nan"), float("nan"), int(len(xte))
    beta = float((ntr * np.sum(xtr * ytr) - np.sum(xtr) * np.sum(ytr)) / denom)
    alpha = float((np.sum(ytr) - beta * np.sum(xtr)) / ntr)
    pred = alpha + beta * xte
    ss_res = float(np.sum((yte - pred) ** 2))
    ss_tot = float(np.sum((yte - np.mean(yte)) ** 2))
    r2 = (1.0 - ss_res / ss_tot) if ss_tot > 1e-18 else float("nan")
    return beta, r2, int(len(xte))


def compute_velocity_absorption(
    closes: pd.Series,
    snr: float = KALMAN_SNR,
    kappa: float = KALMAN_KAPPA,
    warmup: int = KALMAN_WARMUP,
    horizons: tuple[int, ...] = (1, 5),
) -> dict:
    """Step 2A structural instrumentation. Returns δ (velocity contribution) aligned to the
    input, and the predictive-decay β/R²/n for the velocity-ON (Kalman) and velocity-OFF
    (restored ≡ matched-EMA pred) residuals at each horizon. Frozen estimator is untouched —
    μK_pred is recovered from its output by subtraction."""
    n = len(closes)
    prices = closes.to_numpy(dtype=float)

    gain_inf = kalman_steady_state_gain(snr, kappa)
    span_m = max(2, int(round(kalman_effective_span(gain_inf))))

    # Matched-responsiveness EMA and its one-step prediction (info ≤ t−1).
    ema_m = compute_ema(closes, span=span_m).to_numpy()
    emap = np.full(n, np.nan)
    emap[1:] = ema_m[:-1]

    # Frozen Kalman output; recover μ_{t|t−1} = close − innovation. No recomputation of the filter.
    kf = compute_kalman_mu_star(closes, snr=snr, kappa=kappa, warmup=warmup)
    eps_k = kf["epsilon_kalman"].to_numpy()
    muk_pred = prices - eps_k

    delta = muk_pred - emap                      # velocity contribution (NaN at t=0)
    eps_restored = prices - emap                 # = eps_k + delta  (identity)

    burn = max(warmup, span_m)
    sl = slice(burn, n)
    ek = eps_k[sl]
    er = eps_restored[sl]

    reversion = {"kalman": {}, "restored": {}}
    for h in horizons:
        bk, r2k, nk = _walk_forward_decay(ek, h)
        br, r2r, nr = _walk_forward_decay(er, h)
        reversion["kalman"][h] = {"beta": bk, "r2": r2k, "n": nk}
        reversion["restored"][h] = {"beta": br, "r2": r2r, "n": nr}

    return {
        "matched_span": span_m,
        "steady_state_gain": gain_inf,
        "burn": burn,
        "n": n,
        "delta": delta,            # full-length, aligned to closes.index (NaN at t=0)
        "price": prices,
        "eps_kalman": eps_k,
        "eps_restored": eps_restored,
        "reversion": reversion,
        "horizons": list(horizons),
    }
