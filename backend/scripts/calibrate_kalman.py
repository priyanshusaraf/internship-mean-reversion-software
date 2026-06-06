"""
One-time SNR calibration for the Anchored Kalman μ* estimator (spec v1, §5.0).

THIS IS THE ONLY PARAMETER SWEEP THE SPEC PERMITS, AND IT TOUCHES SYNTHETIC DATA ONLY.
It selects the single dimensionless knob SNR = q_v / R_p, then that value is hard-coded into
analytics.KALMAN_SNR. No market data, no market outcomes, no per-instrument fitting (§3).

Selection rule (§5.0): pick the SNR that simultaneously
  (a) recovers OU half-life within ±25% of truth, AND
  (b) satisfies the admissible band — G-IDENT and G-ABSORB:
        G-ABSORB: |corr(velocity, true_deviation)| < 0.20  AND  var(eps)/var(dev) ∈ [0.8, 1.2]
        G-IDENT : |mean(eps_kalman)| < 0.3·|mean(eps_ema)| on pure trend  AND impulse_cosine < 0.99

RW persistence (H1) is reported as a sanity column but is a G1 gate, not a selection objective.

Run:  cd backend && source .venv/bin/activate && python scripts/calibrate_kalman.py
"""
from __future__ import annotations

import os
import sys
import warnings

import numpy as np
import pandas as pd

# Run-from-anywhere: ensure the backend root (parent of scripts/) is importable.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Degenerate synthetic windows (e.g. constant slices) make compute_halflife / corrcoef emit
# floods of RuntimeWarnings. They are expected and irrelevant to the metric — silence them so
# the sweep's stderr stays small.
warnings.filterwarnings("ignore")
np.seterr(all="ignore")

from app.services import analytics, synthetic  # noqa: E402

SEEDS = list(range(15))
N = 500
LAM = -0.1
SIGMA = 1.0
SLOPE = 0.1
BURN = 100  # exclude init transient from all metrics
SNR_GRID = np.logspace(-9, 0, 28)  # 1e-9 ... 1e0 (slow filters need very small SNR)


def _steady_state_gain(snr: float, kappa: float) -> tuple[float, float]:
    """Iterate the Riccati recursion (R_p=1) to convergence → steady-state (alpha, beta).
    K depends only on Q/R and the covariance recursion, not on the data, so this is exact."""
    R = 1.0
    q_v = snr * R
    q_mu = kappa * q_v
    F = np.array([[1.0, 1.0], [0.0, 1.0]])
    Q = np.array([[q_mu, 0.0], [0.0, q_v]])
    H = np.array([1.0, 0.0])
    I2 = np.eye(2)
    P = np.diag([10.0, 10.0])
    K = np.array([0.0, 0.0])
    for _ in range(5000):
        P_pred = F @ P @ F.T + Q
        S = P_pred[0, 0] + R
        K_new = (P_pred @ H) / S
        P = (I2 - np.outer(K_new, H)) @ P_pred
        if np.max(np.abs(K_new - K)) < 1e-12:
            K = K_new
            break
        K = K_new
    return float(K[0]), float(K[1])


def _impulse_cosine(snr: float, kappa: float, length: int = 300) -> tuple[float, float]:
    """Cosine similarity between the steady-state μ-impulse-response and the matched-span
    EMA weights (alpha = level gain). Returns (cosine, effective_span)."""
    alpha, beta = _steady_state_gain(snr, kappa)
    # LTI alpha-beta impulse response on the level estimate
    w = np.empty(length)
    mu = 0.0
    v = 0.0
    for k in range(length):
        imp = 1.0 if k == 0 else 0.0
        mu_pred = mu + v
        innov = imp - mu_pred
        mu = mu_pred + alpha * innov
        v = v + beta * innov
        w[k] = mu
    # matched-span EMA weights: w_ema[k] = alpha*(1-alpha)^k
    k_arr = np.arange(length)
    w_ema = alpha * (1.0 - alpha) ** k_arr
    denom = np.linalg.norm(w) * np.linalg.norm(w_ema)
    cos = float(np.dot(w, w_ema) / denom) if denom > 0 else 0.0
    eff_span = analytics.kalman_effective_span(alpha)
    return cos, eff_span


def _metrics_for_snr(snr: float) -> dict:
    kappa = analytics.KALMAN_KAPPA
    true_hl = -np.log(2) / LAM
    true_acf1 = 1.0 + LAM

    ou_hl_errs, ou_acf1s = [], []
    rw_acf1s, rw_notmr = [], []
    abs_corrs, var_ratios = [], []
    trend_bias_ratios = []

    cos, eff_span = _impulse_cosine(snr, kappa)
    ema_span = max(2, int(round(eff_span)))

    for seed in SEEDS:
        # --- OU half-life recovery (H2) ---
        s = synthetic.ou(lam=LAM, sigma=SIGMA, n=N, seed=seed)
        kf = analytics.compute_kalman_mu_star(pd.Series(s.prices), snr=snr)
        eps = kf["epsilon_kalman"].to_numpy()[BURN:]
        hl = analytics.compute_halflife(pd.Series(eps))
        if hl is not None:
            ou_hl_errs.append(abs(hl - true_hl) / true_hl)
        acf = analytics.compute_acf(pd.Series(eps))
        ou_acf1s.append(acf["lag1"])

        # --- RW false-persistence (H1, sanity) ---
        rw = synthetic.random_walk(sigma=SIGMA, n=N, seed=seed)
        kf_rw = analytics.compute_kalman_mu_star(pd.Series(rw.prices), snr=snr)
        eps_rw = kf_rw["epsilon_kalman"].to_numpy()[BURN:]
        rw_acf1s.append(analytics.compute_acf(pd.Series(eps_rw))["lag1"])
        rw_notmr.append(analytics.compute_halflife(pd.Series(eps_rw)) is None)

        # --- OU-in-trend absorption (G-ABSORB) ---
        st = synthetic.ou_in_trend(lam=LAM, sigma=SIGMA, slope=SLOPE, n=N, seed=seed)
        kf_t = analytics.compute_kalman_mu_star(pd.Series(st.prices), snr=snr)
        vel = kf_t["kalman_velocity"].to_numpy()[BURN:]
        eps_t = kf_t["epsilon_kalman"].to_numpy()[BURN:]
        dev = st.deviation[BURN:]
        if np.std(vel) > 1e-9 and np.std(dev) > 1e-9:
            abs_corrs.append(abs(np.corrcoef(vel, dev)[0, 1]))
        if np.var(dev) > 1e-12:
            var_ratios.append(np.var(eps_t) / np.var(dev))

        # --- Trend lag-bias vs matched EMA (G-IDENT) ---
        tr = synthetic.trend(slope=SLOPE, sigma=SIGMA, n=N, seed=seed)
        kf_tr = analytics.compute_kalman_mu_star(pd.Series(tr.prices), snr=snr)
        eps_ktr = kf_tr["epsilon_kalman"].to_numpy()[BURN:]
        ema = analytics.compute_ema(pd.Series(tr.prices), span=ema_span).to_numpy()
        eps_etr = (tr.prices - ema)[BURN:]
        mb_e = abs(np.mean(eps_etr))
        mb_k = abs(np.mean(eps_ktr))
        trend_bias_ratios.append(mb_k / mb_e if mb_e > 1e-9 else np.inf)

    med = lambda a: float(np.median(a)) if len(a) else float("nan")
    return {
        "snr": snr,
        "eff_span": eff_span,
        "impulse_cos": cos,
        "ou_hl_err": med(ou_hl_errs),
        "ou_acf1": med(ou_acf1s),
        "ou_acf1_err": abs(med(ou_acf1s) - true_acf1),
        "rw_acf1": med(rw_acf1s),
        "rw_notmr_frac": float(np.mean(rw_notmr)),
        "absorb": med(abs_corrs),
        "var_ratio": med(var_ratios),
        "trend_bias_ratio": med(trend_bias_ratios),
    }


TABLE_PATH = "/tmp/cal_table.txt"


def main() -> None:
    lines: list[str] = []
    lines.append(f"OU truth: half-life={-np.log(2)/LAM:.3f}, acf1={1.0+LAM:.3f}")
    lines.append(f"seeds={len(SEEDS)} n={N} burn={BURN} kappa={analytics.KALMAN_KAPPA}")
    lines.append("")

    rows = [_metrics_for_snr(snr) for snr in SNR_GRID]

    hdr = (f"{'SNR':>9} {'effSpan':>8} {'impCos':>7} {'OU_hlErr':>9} {'OU_acf1':>8} "
           f"{'RW_acf1':>8} {'RWnotMR':>8} {'absorb':>7} {'varRatio':>9} {'trBias':>7}  band")
    lines.append(hdr)
    lines.append("-" * len(hdr))

    passing = []
    for r in rows:
        hl_ok = r["ou_hl_err"] < 0.25
        absorb_ok = (r["absorb"] < 0.20) and (0.8 <= r["var_ratio"] <= 1.2)
        ident_ok = (r["trend_bias_ratio"] < 0.3) and (r["impulse_cos"] < 0.99)
        in_band = hl_ok and absorb_ok and ident_ok
        flag = "  <== ADMISSIBLE" if in_band else ""
        flags = f"{'H' if hl_ok else '.'}{'A' if absorb_ok else '.'}{'I' if ident_ok else '.'}"
        lines.append(f"{r['snr']:>9.2e} {r['eff_span']:>8.1f} {r['impulse_cos']:>7.3f} "
                     f"{r['ou_hl_err']:>9.2%} {r['ou_acf1']:>8.3f} {r['rw_acf1']:>8.3f} "
                     f"{r['rw_notmr_frac']:>8.0%} {r['absorb']:>7.3f} {r['var_ratio']:>9.3f} "
                     f"{r['trend_bias_ratio']:>7.3f}  {flags}{flag}")
        if in_band:
            passing.append(r)

    lines.append("")
    lines.append("band flags: H=half-life±25%  A=G-ABSORB  I=G-IDENT")

    best = None
    if passing:
        # Prefer the admissible SNR with var_ratio closest to 1.0 (best signal preservation),
        # tie-broken by lowest absorption.
        best = min(passing, key=lambda r: (abs(r["var_ratio"] - 1.0), r["absorb"]))
        lines.append(f"RECOMMENDED KALMAN_SNR = {best['snr']:.4e}")
        lines.append(f"  effective span ~ {best['eff_span']:.1f} bars")
        lines.append(f"  OU half-life err {best['ou_hl_err']:.1%}, OU acf1 {best['ou_acf1']:.3f} "
                     f"(truth {1.0+LAM:.3f})")
        lines.append(f"  absorption {best['absorb']:.3f}, var_ratio {best['var_ratio']:.3f}, "
                     f"trend_bias {best['trend_bias_ratio']:.3f}, impulse_cos {best['impulse_cos']:.3f}")
        lines.append(f"  RW acf1 {best['rw_acf1']:.3f}, RW not-MR {best['rw_notmr_frac']:.0%}")
    else:
        lines.append("NO SNR IN ADMISSIBLE BAND - widen grid or trigger kill-criteria review (§7).")

    with open(TABLE_PATH, "w") as f:
        f.write("\n".join(lines) + "\n")

    # Compact verdict to stdout (full table is in TABLE_PATH).
    n_adm = len(passing)
    if best is not None:
        print(f"DONE adm={n_adm} SNR={best['snr']:.4e} effSpan={best['eff_span']:.1f} "
              f"hlErr={best['ou_hl_err']:.3f} ouAcf1={best['ou_acf1']:.3f} "
              f"absorb={best['absorb']:.3f} varRatio={best['var_ratio']:.3f} "
              f"trBias={best['trend_bias_ratio']:.3f} impCos={best['impulse_cos']:.3f} "
              f"rwAcf1={best['rw_acf1']:.3f} rwNotMR={best['rw_notmr_frac']:.2f}")
    else:
        print(f"DONE adm=0 NO_ADMISSIBLE_BAND table={TABLE_PATH}")


if __name__ == "__main__":
    main()
