"""Focused H1 verification (spec §5, G1) over the admissible SNR band.

H1 per-seed (random walk): acf_kalman_lag1 < 0.20 AND half-life classified not-MR.
Pass requires this on >=90% of >=20 seeds. Also reports OU half-life recovery (H2) at the
same SNRs for context. Compact stdout only.
"""
from __future__ import annotations
import os, sys, warnings
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
from app.services import analytics, synthetic  # noqa: E402

SEEDS = list(range(20))
N, LAM, SIGMA, BURN = 500, -0.1, 1.0, 100
TRUE_HL = -np.log(2) / LAM
SNRS = [1.78e-3, 2.3714e-3, 3.16e-3, 5.62e-3, 1.0e-2, 1.78e-2, 3.16e-2]

for snr in SNRS:
    h1_pass = 0
    ou_errs = []
    for seed in SEEDS:
        rw = synthetic.random_walk(sigma=SIGMA, n=N, seed=seed)
        eps_rw = analytics.compute_kalman_mu_star(pd.Series(rw.prices), snr=snr)["epsilon_kalman"].to_numpy()[BURN:]
        acf1 = analytics.compute_acf(pd.Series(eps_rw))["lag1"]
        not_mr = analytics.compute_halflife(pd.Series(eps_rw)) is None
        if acf1 < 0.20 and not_mr:
            h1_pass += 1
        ou = synthetic.ou(lam=LAM, sigma=SIGMA, n=N, seed=seed)
        eps_ou = analytics.compute_kalman_mu_star(pd.Series(ou.prices), snr=snr)["epsilon_kalman"].to_numpy()[BURN:]
        hl = analytics.compute_halflife(pd.Series(eps_ou))
        if hl is not None:
            ou_errs.append(abs(hl - TRUE_HL) / TRUE_HL)
    frac = h1_pass / len(SEEDS)
    ou_med = float(np.median(ou_errs)) if ou_errs else float("nan")
    h2_ok = "H2ok" if ou_med < 0.25 else "H2FAIL"
    h1_ok = "H1ok" if frac >= 0.90 else "H1FAIL"
    print(f"snr={snr:.3e} H1pass={frac:.2f} {h1_ok} | OUhlErr={ou_med:.3f} {h2_ok}")
