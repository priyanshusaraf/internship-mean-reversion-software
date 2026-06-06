"""
Arm A — diagnostic probe (NOT a verdict change; the frozen W=60 verdict stands). Tests whether the
rolling-β spreads' VR≫1 is a CONSTRUCTION artifact (short-window OLS β on levels fails to produce a
stationary spread) vs a real market property, and whether the USD/INR "confirm" is a flat-bar
variance-deflation artifact. Diagnostic β variants are labelled causal/non-causal explicitly.
"""
from __future__ import annotations
import os, sys, warnings
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
from app.services import analytics_arm_a as A  # noqa: E402
from statsmodels.tsa.stattools import adfuller  # noqa: E402

D = os.path.expanduser("~/Downloads/mean-reversion-data")
def lg(f): return A.load_leg(os.path.join(D, f))


def vr10(s, invalid):
    return A.level_vr(s, invalid, (2, 5, 10, 20))


def diag_pair(name, fa, fb, ca, cb, dmin=None, dfa=False, dfb=False):
    print(f"\n=== {name} — is VR≫1 a β-construction artifact? ===")
    a, b = lg(fa), lg(fb)
    if dfa: a = a[~((a.open == a.high) & (a.high == a.low) & (a.low == a.close))]
    if dfb: b = b[~((b.open == b.high) & (b.high == b.low) & (b.low == b.close))]
    if dmin:
        cut = __import__("pandas").Timestamp(dmin, tz="UTC"); a, b = a[a.index >= cut], b[b.index >= cut]
    j = a.join(b, how="inner", lsuffix="_a", rsuffix="_b")
    ca_, cb_ = j["close_a"].to_numpy(), j["close_b"].to_numpy()
    roll = (A.roll_transition_mask(ca_) if ca else np.zeros(len(j), bool)) | \
           (A.roll_transition_mask(cb_) if cb else np.zeros(len(j), bool))

    variants = {
        "beta=1 (raw diff)": np.ones(len(j)),
        "roll-OLS W=60 (FROZEN verdict)": A.causal_rolling_beta(ca_, cb_, 60),
        "roll-OLS W=120": A.causal_rolling_beta(ca_, cb_, 120),
        "roll-OLS W=250": A.causal_rolling_beta(ca_, cb_, 250),
        "FULL-SAMPLE OLS β (NON-causal, diag)": None,
        "log-ratio ln(A)-ln(B) (legs+, NP-2)": "logratio",
    }
    fb_ols = np.polyfit(cb_, ca_, 1)[0]   # full-sample slope (lookahead — diagnostic only)
    for label, beta in variants.items():
        if label.startswith("log-ratio"):
            with np.errstate(all="ignore"):
                s = np.log(ca_) - np.log(cb_)
            inv = roll.copy()
        elif beta is None:
            s = ca_ - fb_ols * cb_; inv = roll.copy()
        else:
            s = ca_ - beta * cb_; inv = roll | ~np.isfinite(beta)
        v = vr10(s, inv)
        sclean = s[np.isfinite(s) & ~inv]
        adf = adfuller(sclean, maxlag=20, autolag=None)[0] if len(sclean) > 60 else np.nan
        bdesc = (f"β~{np.nanmedian(beta):.3f}" if isinstance(beta, np.ndarray) else
                 (f"β={fb_ols:.3f}" if beta is None else "—"))
        print(f"  {label:38s} {bdesc:12s} VR(2,5,10,20)="
              f"{[round(v[q]['vr'],2) for q in (2,5,10,20)]}  ADF={adf:6.2f}")
    print("  (ADF < -2.86 ⇒ stationary at 5%. VR<1 ⇒ sub-diffusive.)")


def diag_flat(name, fa, fb, ca, cb):
    print(f"\n=== {name} — is the 'confirm' a flat-bar / zero-increment artifact? ===")
    a, b = lg(fa), lg(fb)
    j = a.join(b, how="inner", lsuffix="_a", rsuffix="_b")
    ca_, cb_ = j["close_a"].to_numpy(), j["close_b"].to_numpy()
    s = ca_ - cb_                      # β=1 calendar
    d = np.diff(s)
    flat = ((j["open_a"] == j["close_a"]) & (j["high_a"] == j["low_a"])).to_numpy() | \
           ((j["open_b"] == j["close_b"]) & (j["high_b"] == j["low_b"])).to_numpy()
    roll = (A.roll_transition_mask(ca_) if ca else np.zeros(len(j), bool)) | \
           (A.roll_transition_mask(cb_) if cb else np.zeros(len(j), bool))
    print(f"  n={len(j)}  flat-bar frac={flat.mean():.1%}  zero-increment frac={(d==0).mean():.1%}")
    v_all = vr10(s, roll)
    v_ft = vr10(s, roll | flat)
    print(f"  VR roll-clean         : {[round(v_all[q]['vr'],3) for q in (2,5,10,20)]}")
    print(f"  VR roll-clean+flat-trim: {[round(v_ft[q]['vr'],3) for q in (2,5,10,20)]}  (n_incr={int((~(roll|flat)[1:]).sum())})")


if __name__ == "__main__":
    diag_pair("HDFC-ICICI", "BSE_DLY_HDFCBANK, 1D.csv", "BSE_DLY_ICICIBANK, 1D.csv", False, False)
    diag_pair("Gold-Silver", "COMEX_DL_GC2!, 1D.csv", "COMEX_DL_SI2!, 1D.csv", True, True)
    diag_pair("TCS-INFY", "BSE_DLY_TCS, 1D.csv", "NSE_DLY_INFY, 1D.csv", False, False)
    diag_pair("WTI-Brent", "CFI_WTI, 1D.csv", "ICEEUR_DLY_BRN1!, 1D.csv", False, True, dmin="2011-01-01")
    diag_flat("USDINR-calendar", "CME_MINI_DL_MIR1!, 1D.csv", "CME_MINI_DL_MIR2!, 1D.csv", True, True)
