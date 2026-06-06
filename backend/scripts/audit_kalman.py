"""
ADVERSARIAL REPLICATION AUDIT of the Kalman μ* rejection.

Not implementing, not rescuing. Testing whether the G-ABSORB-driven kill is trustworthy.

Each experiment writes a full table to /tmp and prints a compact verdict line. No threshold is
moved; we test whether the gate MEASURES what it claims.
"""
from __future__ import annotations
import os, sys, warnings
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
from app.services import analytics, synthetic  # noqa: E402

SEEDS = list(range(30))
N, BURN, LAM, SIGMA, SLOPE = 600, 120, -0.1, 1.0, 0.1
TRUE_HL = -np.log(2) / LAM
GRID = np.logspace(-9, 0, 19)


def kf(prices, snr):
    return analytics.compute_kalman_mu_star(pd.Series(prices), snr=snr)


def med_abs_corr(a, b):
    if np.std(a) < 1e-12 or np.std(b) < 1e-12:
        return np.nan
    return abs(np.corrcoef(a, b)[0, 1])


def exp1_absorption_null():
    """CRITICAL: does corr(velocity, deviation) have a mechanical floor with NO alpha to absorb?

    signal  = ou_in_trend (persistent OU deviation around a trend) — the actual gate
    null_wn = trend + iid noise (deviation = white noise; nothing reverting to absorb)
    pure_ou = ou, slope 0 (velocity SHOULD be ~0; tests absorption when there is no trend)
    shuffle = corr(velocity, shuffled deviation) — must be ~0 if the metric is sane
    """
    rows = []
    for snr in GRID:
        a_sig, a_wn, a_ou, a_shuf, vratio = [], [], [], [], []
        for sd in SEEDS:
            st = synthetic.ou_in_trend(lam=LAM, sigma=SIGMA, slope=SLOPE, n=N, seed=sd)
            d = kf(st.prices, snr); vel = d["kalman_velocity"].to_numpy()[BURN:]
            dev = st.deviation[BURN:]; eps = d["epsilon_kalman"].to_numpy()[BURN:]
            a_sig.append(med_abs_corr(vel, dev))
            if np.var(dev) > 1e-12: vratio.append(np.var(eps) / np.var(dev))
            rng = np.random.default_rng(1000 + sd)
            a_shuf.append(med_abs_corr(vel, rng.permutation(dev)))

            tr = synthetic.trend(slope=SLOPE, sigma=SIGMA, n=N, seed=sd)
            dt = kf(tr.prices, snr); velt = dt["kalman_velocity"].to_numpy()[BURN:]
            a_wn.append(med_abs_corr(velt, tr.deviation[BURN:]))

            ou = synthetic.ou(lam=LAM, sigma=SIGMA, n=N, seed=sd)
            do = kf(ou.prices, snr); velo = do["kalman_velocity"].to_numpy()[BURN:]
            a_ou.append(med_abs_corr(velo, ou.deviation[BURN:]))
        rows.append((snr, np.nanmedian(a_sig), np.nanmedian(a_wn), np.nanmedian(a_ou),
                     np.nanmedian(a_shuf), np.nanmedian(vratio)))
    lines = ["exp1: absorption metric — signal vs nulls (median |corr(vel,dev)| over 30 seeds)",
             f"{'SNR':>9} {'OUtrend':>8} {'WNnull':>8} {'pureOU':>8} {'shuffle':>8} {'varRatio':>9}  excess=OUtrend-WNnull"]
    for snr, sig, wn, ou, shuf, vr in rows:
        lines.append(f"{snr:>9.2e} {sig:>8.3f} {wn:>8.3f} {ou:>8.3f} {shuf:>8.3f} {vr:>9.3f}  {sig-wn:>+.3f}")
    open("/tmp/audit_exp1.txt", "w").write("\n".join(lines) + "\n")
    # verdict: at the slow band where H2 passes (snr<=4.6e-7), is signal materially > null?
    band = [(s, sig, wn) for s, sig, wn, *_ in rows if s <= 4.6e-7]
    excess = np.median([sig - wn for _, sig, wn in band])
    floor = np.median([wn for _, _, wn in band])
    print(f"EXP1 floor(WNnull,slowband)={floor:.3f} excess(signal-null)={excess:+.3f} "
          f"-> {'METRIC_ARTIFACT' if floor>=0.20 else ('REAL_ABSORPTION' if excess>0.10 else 'AMBIGUOUS')}")


def exp2_slope_sensitivity():
    """Is ou_in_trend fairly parameterized? Sweep slope at the H2-admissible SNR=1e-8.

    slope=0  -> pure OU (correct velocity is 0); high absorb here = velocity fits OU, not trend.
    large slope -> trend dominates; if model is fair, velocity locks to slope, absorb should fall.
    Report SNR (deviation std ~2.29) vs trend movement per half-life.
    """
    snr = 1e-8
    dev_std = SIGMA / np.sqrt(1 - (1 + LAM) ** 2)
    rows = []
    for slope in [0.0, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0]:
        ac, vr = [], []
        for sd in SEEDS:
            st = synthetic.ou_in_trend(lam=LAM, sigma=SIGMA, slope=slope, n=N, seed=sd)
            d = kf(st.prices, snr); vel = d["kalman_velocity"].to_numpy()[BURN:]
            dev = st.deviation[BURN:]; eps = d["epsilon_kalman"].to_numpy()[BURN:]
            ac.append(med_abs_corr(vel, dev))
            if np.var(dev) > 1e-12: vr.append(np.var(eps) / np.var(dev))
        trend_per_hl = slope * TRUE_HL
        rows.append((slope, trend_per_hl / dev_std, np.nanmedian(ac), np.nanmedian(vr)))
    lines = [f"exp2: slope sensitivity at SNR={snr:.0e}  (dev_std={dev_std:.2f}, true_hl={TRUE_HL:.2f})",
             f"{'slope':>6} {'trendHL/devStd':>14} {'absorb':>7} {'varRatio':>9}"]
    for sl, ratio, ab, vr in rows:
        lines.append(f"{sl:>6.2f} {ratio:>14.3f} {ab:>7.3f} {vr:>9.3f}")
    open("/tmp/audit_exp2.txt", "w").write("\n".join(lines) + "\n")
    ab0 = rows[0][2]; abbig = rows[-1][2]
    print(f"EXP2 absorb@slope0={ab0:.3f} absorb@slope2.0={abbig:.3f} "
          f"-> {'ABSORB_INDEP_OF_TREND(metric fits OU regardless)' if abs(ab0-abbig)<0.07 else 'TREND_DEPENDENT'}")


def exp3_kappa_sensitivity():
    """Is the kill driven by the frozen kappa=0.05? Re-run absorption at SNR=1e-8 across kappa.
    Audit only — spec freezes kappa; this tests 'bad param vs bad model class'."""
    snr = 1e-8
    rows = []
    for kappa in [0.0, 0.01, 0.05, 0.2, 0.5, 1.0]:
        ac, hlerr = [], []
        for sd in SEEDS:
            st = synthetic.ou_in_trend(lam=LAM, sigma=SIGMA, slope=SLOPE, n=N, seed=sd)
            d = analytics.compute_kalman_mu_star(pd.Series(st.prices), snr=snr, kappa=kappa)
            ac.append(med_abs_corr(d["kalman_velocity"].to_numpy()[BURN:], st.deviation[BURN:]))
            ou = synthetic.ou(lam=LAM, sigma=SIGMA, n=N, seed=sd)
            do = analytics.compute_kalman_mu_star(pd.Series(ou.prices), snr=snr, kappa=kappa)
            hl = analytics.compute_halflife(pd.Series(do["epsilon_kalman"].to_numpy()[BURN:]))
            if hl is not None: hlerr.append(abs(hl - TRUE_HL) / TRUE_HL)
        rows.append((kappa, np.nanmedian(ac), np.nanmedian(hlerr) if hlerr else np.nan))
    lines = [f"exp3: kappa sensitivity at SNR={snr:.0e}",
             f"{'kappa':>6} {'absorb':>7} {'OUhlErr':>8}"]
    for kp, ab, he in rows:
        lines.append(f"{kp:>6.2f} {ab:>7.3f} {he:>8.3f}")
    open("/tmp/audit_exp3.txt", "w").write("\n".join(lines) + "\n")
    best = min(rows, key=lambda r: r[1])
    print(f"EXP3 min_absorb={best[1]:.3f} @kappa={best[0]} "
          f"-> {'KAPPA_CANNOT_SAVE' if best[1]>=0.20 else 'KAPPA_MATTERS'}")


def exp4_disjointness():
    """Independently reconstruct the disjoint-region claim: H2, G-IDENT, G-ABSORB vs SNR.
    Confirms or refutes 'no admissible band'."""
    rows = []
    for snr in GRID:
        hlerr, absb = [], []
        for sd in SEEDS:
            ou = synthetic.ou(lam=LAM, sigma=SIGMA, n=N, seed=sd)
            hl = analytics.compute_halflife(pd.Series(kf(ou.prices, snr)["epsilon_kalman"].to_numpy()[BURN:]))
            if hl is not None: hlerr.append(abs(hl - TRUE_HL) / TRUE_HL)
            st = synthetic.ou_in_trend(lam=LAM, sigma=SIGMA, slope=SLOPE, n=N, seed=sd)
            d = kf(st.prices, snr)
            absb.append(med_abs_corr(d["kalman_velocity"].to_numpy()[BURN:], st.deviation[BURN:]))
        cos, span = analytics_cos(snr)
        rows.append((snr, span, np.nanmedian(hlerr), cos, np.nanmedian(absb)))
    lines = ["exp4: disjointness reconstruction",
             f"{'SNR':>9} {'effSpan':>8} {'OUhlErr':>8} {'impCos':>7} {'absorb':>7}  H2/IDENT/ABSORB"]
    any_admissible = False
    for snr, span, he, cos, ab in rows:
        h2 = he < 0.25; ident = cos < 0.99; absb = ab < 0.20
        if h2 and ident and absb: any_admissible = True
        lines.append(f"{snr:>9.2e} {span:>8.1f} {he:>8.3f} {cos:>7.3f} {ab:>7.3f}  "
                     f"{'H' if h2 else '.'}{'I' if ident else '.'}{'A' if absb else '.'}")
    open("/tmp/audit_exp4.txt", "w").write("\n".join(lines) + "\n")
    print(f"EXP4 admissible_band_exists={any_admissible}")


def analytics_cos(snr):
    """Replicate impulse cosine + eff span (independent of calibrate script)."""
    kappa = analytics.KALMAN_KAPPA
    R = 1.0; q_v = snr * R; q_mu = kappa * q_v
    F = np.array([[1.0, 1.0], [0.0, 1.0]]); Q = np.array([[q_mu, 0.0], [0.0, q_v]])
    H = np.array([1.0, 0.0]); I2 = np.eye(2); P = np.diag([10.0, 10.0]); K = np.zeros(2)
    for _ in range(5000):
        Pp = F @ P @ F.T + Q; S = Pp[0, 0] + R; Kn = (Pp @ H) / S
        P = (I2 - np.outer(Kn, H)) @ Pp
        if np.max(np.abs(Kn - K)) < 1e-12: K = Kn; break
        K = Kn
    alpha = float(K[0]); L = 300
    w = np.empty(L); mu = 0.0; v = 0.0
    for k in range(L):
        imp = 1.0 if k == 0 else 0.0; mp = mu + v; inn = imp - mp
        mu = mp + alpha * inn; v = v + float(K[1]) * inn; w[k] = mu
    we = alpha * (1 - alpha) ** np.arange(L)
    den = np.linalg.norm(w) * np.linalg.norm(we)
    cos = float(np.dot(w, we) / den) if den > 0 else 0.0
    return cos, analytics.kalman_effective_span(alpha)


if __name__ == "__main__":
    exp1_absorption_null()
    exp2_slope_sensitivity()
    exp3_kappa_sensitivity()
    exp4_disjointness()
    print("tables: /tmp/audit_exp1.txt exp2 exp3 exp4")
