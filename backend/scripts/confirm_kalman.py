"""
SINGLE CONFIRMATORY TEST — Kalman μ* vs matched-effective-span EMA on OU-in-trend.

The only remaining question: does Kalman produce materially superior RESIDUALS than EMA when
compared at the SAME responsiveness (no speed mismatch)? Fair match: for a given Kalman SNR,
the steady-state level gain α = K∞[0] defines effective span = 2/α − 1; EMA uses that span, so
both estimators have identical one-step responsiveness and differ ONLY by the velocity state.

Paired design: same seeds feed both estimators, so we test paired deltas (Kalman − EMA) and
their significance directly. Metrics are exactly the four the thesis cares about.
"""
from __future__ import annotations
import sys, warnings
import numpy as np, pandas as pd
sys.path.insert(0, ".")
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
from app.services import analytics, synthetic  # noqa: E402

SEEDS = list(range(30))
N, BURN = 800, 150
SLOPES = [0.05, 0.1, 0.25, 0.5]
LAMS = [-0.05, -0.1, -0.2]          # true half-lives ~13.5, 6.93, 3.11
SIGMA = 1.0
# H2-admissible band only (where Kalman recovers OU). Outside it Kalman fails H2 outright,
# so a residual-quality comparison there is moot. effSpan ~ 251 / 141 / 80 / 60.
SNRS = [1e-9, 1e-8, 1e-7, 3.16e-7]


def matched_span(snr: float, kappa: float = analytics.KALMAN_KAPPA) -> tuple[int, float]:
    """Steady-state level gain α (R_p=1 Riccati) → matched EMA span = 2/α − 1."""
    R = 1.0; q_v = snr * R; q_mu = kappa * q_v
    F = np.array([[1.0, 1.0], [0.0, 1.0]]); Q = np.array([[q_mu, 0.0], [0.0, q_v]])
    H = np.array([1.0, 0.0]); I2 = np.eye(2); P = np.diag([10.0, 10.0]); K = np.zeros(2)
    for _ in range(8000):
        Pp = F @ P @ F.T + Q; S = Pp[0, 0] + R; Kn = (Pp @ H) / S
        P = (I2 - np.outer(Kn, H)) @ Pp
        if np.max(np.abs(Kn - K)) < 1e-13: K = Kn; break
        K = Kn
    alpha = float(K[0])
    return max(2, int(round(2.0 / alpha - 1.0))), alpha


def resid_metrics(eps: np.ndarray, dev: np.ndarray, true_hl: float) -> dict:
    s = pd.Series(eps)
    hl = analytics.compute_halflife(s)
    acf = analytics.compute_acf(s, lags=[1, 5, 10])
    return {
        "hl": hl,
        "hl_err": (abs(hl - true_hl) / true_hl) if hl is not None else np.nan,
        "acf1": acf["lag1"], "acf5": acf["lag5"],
        "abs_mean": abs(float(np.mean(eps))),          # centering / trend-lag bias
        "corr_dev": float(np.corrcoef(eps, dev)[0, 1]) if np.std(eps) > 1e-12 else np.nan,
        "var_ratio": float(np.var(eps) / np.var(dev)) if np.var(dev) > 1e-12 else np.nan,
    }


def paired_stats(deltas: list[float]) -> tuple[float, float, float]:
    """Return (median_delta, mean_delta, approx two-sided p via sign test on nonzero deltas)."""
    d = np.array([x for x in deltas if np.isfinite(x)])
    if len(d) < 3:
        return np.nan, np.nan, np.nan
    from scipy import stats  # paired test only; NOT optimization (spec §3 forbids fitting, not stats)
    try:
        _, p = stats.wilcoxon(d, zero_method="wilcox")
    except Exception:
        p = np.nan
    return float(np.median(d)), float(np.mean(d)), float(p)


def run():
    out = ["CONFIRMATORY TEST — Kalman vs matched-span EMA on OU-in-trend",
           f"seeds={len(SEEDS)} n={N} burn={BURN} slopes={SLOPES} lams={LAMS}", ""]
    # Aggregate paired deltas across ALL conditions per SNR.
    for snr in SNRS:
        span, alpha = matched_span(snr)
        true_hls = {lam: -np.log(2) / lam for lam in LAMS}
        agg = {k: {"K": [], "E": [], "d": []} for k in
               ["hl_err", "acf1", "acf5", "abs_mean", "corr_dev", "var_ratio"]}
        for lam in LAMS:
            for slope in SLOPES:
                for sd in SEEDS:
                    st = synthetic.ou_in_trend(lam=lam, sigma=SIGMA, slope=slope, n=N, seed=sd)
                    dev = st.deviation[BURN:]
                    epsK = analytics.compute_kalman_mu_star(pd.Series(st.prices), snr=snr)[
                        "epsilon_kalman"].to_numpy()[BURN:]
                    ema = analytics.compute_ema(pd.Series(st.prices), span=span).to_numpy()
                    epsE = (st.prices - ema)[BURN:]
                    mK = resid_metrics(epsK, dev, true_hls[lam])
                    mE = resid_metrics(epsE, dev, true_hls[lam])
                    for k in agg:
                        if np.isfinite(mK[k]) and np.isfinite(mE[k]):
                            agg[k]["K"].append(mK[k]); agg[k]["E"].append(mE[k])
                            agg[k]["d"].append(mK[k] - mE[k])
        out.append(f"SNR={snr:.2e}  matched EMA span={span}  (alpha={alpha:.4f})  "
                   f"n_cond={len(LAMS)*len(SLOPES)*len(SEEDS)}")
        out.append(f"  {'metric':>10} {'Kalman_med':>11} {'EMA_med':>9} {'median_d':>9} "
                   f"{'mean_d':>8} {'wilcox_p':>9}  note")
        for k in ["hl_err", "acf1", "acf5", "abs_mean", "corr_dev", "var_ratio"]:
            Kmed = np.median(agg[k]["K"]); Emed = np.median(agg[k]["E"])
            md, mn, p = paired_stats(agg[k]["d"])
            sig = "SIG" if (np.isfinite(p) and p < 0.01) else "ns"
            # interpret direction: for hl_err/acf/abs_mean lower=better; corr_dev/var_ratio higher(~1)=better
            out.append(f"  {k:>10} {Kmed:>11.4f} {Emed:>9.4f} {md:>9.4f} {mn:>8.4f} "
                       f"{p:>9.2e}  {sig}")
        out.append("")
    open("/tmp/confirm.txt", "w").write("\n".join(out) + "\n")

    # Compact decisive summary at the most-favorable (slowest, best-H2) SNR=1e-8.
    snr = 1e-8; span, alpha = matched_span(snr)
    dhl, dabsmean, dcorr = [], [], []
    for lam in LAMS:
        thl = -np.log(2) / lam
        for slope in SLOPES:
            for sd in SEEDS:
                st = synthetic.ou_in_trend(lam=lam, sigma=SIGMA, slope=slope, n=N, seed=sd)
                dev = st.deviation[BURN:]
                epsK = analytics.compute_kalman_mu_star(pd.Series(st.prices), snr=snr)[
                    "epsilon_kalman"].to_numpy()[BURN:]
                ema = analytics.compute_ema(pd.Series(st.prices), span=span).to_numpy()
                epsE = (st.prices - ema)[BURN:]
                mK = resid_metrics(epsK, dev, thl); mE = resid_metrics(epsE, dev, thl)
                if np.isfinite(mK["hl_err"]) and np.isfinite(mE["hl_err"]):
                    dhl.append(mK["hl_err"] - mE["hl_err"])
                dabsmean.append(mK["abs_mean"] - mE["abs_mean"])
                dcorr.append(mK["corr_dev"] - mE["corr_dev"])
    md_hl, _, p_hl = paired_stats(dhl)
    md_am, _, p_am = paired_stats(dabsmean)
    md_co, _, p_co = paired_stats(dcorr)
    print(f"SNR=1e-8 span={span}: "
          f"d_hlErr={md_hl:+.4f}(p={p_hl:.1e}) "
          f"d_absMean={md_am:+.4f}(p={p_am:.1e}) "
          f"d_corrDev={md_co:+.4f}(p={p_co:.1e})")
    print("(negative d_hlErr/d_absMean = Kalman better; positive d_corrDev = Kalman better)")
    print("full table: /tmp/confirm.txt")


if __name__ == "__main__":
    run()
