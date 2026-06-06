"""State T existence — REAL COHORT probe (doc 11 §7). NOT 'prove State T' — a falsification attempt.

Characterizes each real instrument under the validated Arm-1 method via TWO comparisons:
  A. vs SCALE-MATCHED OU null (lam=−0.1, σ matched to close-diff std, length matched, pooled seeds)
  B. WITHIN-INSTRUMENT high-|z| vs low-|z| (controls scale AND microstructure confounds)
acf1 & dir_eff are scale-free (trustworthy); innov_var is scale-sensitive (flagged).

Pre-registered T-signature (doc 11 §4): ALL THREE descriptors NEGATIVE (innov_var↓ acf1↓ dir_eff↓).
Instruments live in data/raw/. Cohort spans daily (ADANIENT/g1/ng12/rb23) and 60-min intraday
(DELL/AAPL/CL-BRN) — resolution contrast is itself informative.

Run:  .venv/bin/python -m scripts.state_t_cohort_probe
"""
import os

import numpy as np
import pandas as pd

from app.services import analytics, analytics_mrscore, analytics_state_t as st
from app.services import synthetic

RAW = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
THETAS = (1.0, 1.5, 2.0)
W = 30
NULL_SEEDS = range(300, 312)

# (label, file, date_col, close_col, dayfirst, habitat, resolution)
COHORT = [
    ("ADANIENT", "adanient.csv",        "Date", "Close", True,  "trend equity (CONTROL)", "daily"),
    ("g1_gold",  "g1_gold.csv",         "time", "close", False, "commodity outright",     "daily"),
    ("ng12",     "ng12_spread.csv",     "time", "close", False, "spread (deployment)",    "daily"),
    ("rb23",     "rb23_spread.csv",     "time", "close", False, "spread (deployment)",    "daily"),
    ("DELL",     "dell_60.csv",         "time", "close", False, "equity REPRICING",       "60min"),
    ("AAPL",     "aapl_60.csv",         "time", "close", False, "equity mixed",           "60min"),
    ("CL-BRN",   "cl_brn_spread_60.csv","time", "close", False, "crude-brent SPREAD",     "60min"),
    ("EURUSD",   "eurusd_1d.csv",       "time", "close", False, "FX major",               "daily"),
    ("EURUSD",   "eurusd_60.csv",       "time", "close", False, "FX major",               "60min"),
    ("BANKNIFTY","banknifty_1d.csv",    "time", "close", False, "index",                  "daily"),
    ("HDFC-ICICI","hdfc_icici_spread_1d.csv","time","close", False, "PAIR SPREAD (canonical MR)", "daily"),
    ("HDFC-ICICI","hdfc_icici_spread_15.csv","time","close", False, "PAIR SPREAD (canonical MR)", "15min"),
    ("COCOA-COFFEE","coffee_cocoa_spread_1d.csv","time","close", False, "COMMODITY SPREAD", "daily"),
    ("COCOA-COFFEE","coffee_cocoa_spread_60.csv","time","close", False, "COMMODITY SPREAD", "60min"),
    ("COCOA-COFFEE","coffee_cocoa_spread_15.csv","time","close", False, "COMMODITY SPREAD", "15min"),
]


def read_close(fname, date_col, close_col, dayfirst):
    df = pd.read_csv(os.path.join(RAW, fname))
    df.columns = [c.strip() for c in df.columns]
    dt = pd.to_datetime(df[date_col], dayfirst=dayfirst, errors="coerce", utc=True)
    df = df.assign(_dt=dt).dropna(subset=["_dt"]).sort_values("_dt")  # ascending = causal order
    return pd.to_numeric(df[close_col], errors="coerce").dropna().reset_index(drop=True)


def matched_ou_null(real, seeds):
    sigma = float(np.std(np.diff(real.to_numpy(dtype=float))))
    base = float(real.mean())
    return [pd.Series(synthetic.ou(lam=-0.1, sigma=sigma, n=len(real), seed=s, base=base).prices)
            for s in seeds]


def _pooled(series_list, theta, desc):
    cat = pd.concat([st.extract(s, theta=theta, W=W) for s in series_list], ignore_index=True)
    return cat[desc].to_numpy(dtype=float)


def _within_instrument(close, theta):
    kf = analytics.compute_kalman_mu_star(close)
    eps = kf["epsilon_kalman"].to_numpy(dtype=float)
    cv = np.asarray(close, dtype=float)
    resid = pd.Series(cv - kf["mu_star_kalman"].to_numpy(dtype=float))
    z = analytics_mrscore.causal_zscore(resid, window=60).to_numpy(dtype=float)
    fin = np.isfinite(z)
    out = {}
    for key, mask in {"hi": fin & (np.abs(z) >= theta), "lo": fin & (np.abs(z) < theta)}.items():
        rows = [st.window_descriptors(eps[t - W + 1:t + 1], cv[t - W + 1:t + 1])
                for t in np.flatnonzero(mask) if t - W + 1 >= 0]
        out[key] = pd.DataFrame(rows)
    return {c: st.cohens_d(out["hi"][c], out["lo"][c]) for c in st.DESCRIPTORS}, len(out["hi"]), len(out["lo"])


def main():
    print("############ A. vs SCALE-MATCHED OU-NULL  (T-signature = ALL NEGATIVE) ############")
    for label, fname, dcol, ccol, dayfirst, habitat, res in COHORT:
        real = read_close(fname, dcol, ccol, dayfirst)
        ou_null = matched_ou_null(real, NULL_SEEDS)
        print(f"\n=== {label} [{habitat}/{res}] n={len(real)} "
              f"close[min={real.min():.4g} max={real.max():.4g} mean={real.mean():.4g}] ===")
        print(f"{'theta':>6} {'innov_var':>11} {'acf1*':>9} {'dir_eff*':>9} {'n_real':>8}")
        for theta in THETAS:
            rdf = st.extract(real, theta=theta, W=W)
            d_iv = st.cohens_d(rdf["innov_var"], _pooled(ou_null, theta, "innov_var"))
            d_ac = st.cohens_d(rdf["acf1"], _pooled(ou_null, theta, "acf1"))
            d_de = st.cohens_d(rdf["dir_eff"], _pooled(ou_null, theta, "dir_eff"))
            print(f"{theta:>6} {d_iv:>+11.3f} {d_ac:>+9.3f} {d_de:>+9.3f} {len(rdf):>8}")

    print("\n\n############ B. WITHIN-INSTRUMENT high-|z| vs low-|z|  (confound-controlled; T-sig = NEGATIVE) ############")
    print(f"{'inst':>10} {'res':>6} {'theta':>6} {'innov_var':>11} {'acf1':>9} {'dir_eff':>9} {'n_hi':>7} {'n_lo':>7}")
    for label, fname, dcol, ccol, dayfirst, habitat, res in COHORT:
        real = read_close(fname, dcol, ccol, dayfirst)
        for theta in THETAS:
            d, n_hi, n_lo = _within_instrument(real, theta)
            print(f"{label:>10} {res:>6} {theta:>6} {d['innov_var']:>+11.3f} {d['acf1']:>+9.3f} "
                  f"{d['dir_eff']:>+9.3f} {n_hi:>7} {n_lo:>7}")


if __name__ == "__main__":
    main()
