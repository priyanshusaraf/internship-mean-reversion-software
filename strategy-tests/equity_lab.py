#!/usr/bin/env python3
"""
EQUITY LAB — honest, cost-inclusive equity curves for OU-gated spread mean-reversion.
Run:  /usr/bin/python3 strategy-tests/equity_lab.py
Writes PNG equity curves to strategy-tests/equity_curves/ and prints a ranked survivor table.

Construction (standard vol-targeted managed-futures book — the only honest way to read "smooth"):
  - each spread -> synthetic PRICE P_t (for the signal) and a notional-normalized daily RETURN g_t
    (dollar-neutral for ratios, gross-notional-normalized for differences).
  - SIGNAL: OU-gated z-score MR on P_t (half-life gate + z entry + exit-near-mean + disaster/time stop
    + gate-break kill) — identical logic to scripts/ou_spread_mr.pine, fully causal.
  - vol-target each spread to TARGET_VOL; net daily return r = w[t-1]*g[t] - COST*|w[t]-w[t-1]|.
  - COST = 0.0005 per unit weight turnover (your 0.05%); also stress at 0.0010 (2-leg conservative).
  - equity = (1+r).cumprod(). Report Sharpe/CAGR/maxDD/win%/eqR2 for FULL/IS/OOS.
  - SURVIVOR = net-positive (after 0.05%) in BOTH IS and OOS. No argmax: every spread is reported.

Honesty controls: contaminated back-adjusted negative-price era is filtered (legs must be > 0).
"""
import os, glob, math
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = "/Users/priyanshusaraf/Downloads/commodities-data/daily"
OUT  = os.path.join(os.path.dirname(__file__), "equity_curves")
os.makedirs(OUT, exist_ok=True)

# ---- signal / book params (frozen) ----
ZLEN, ZE, ZX, ZS = 40, 2.0, 0.5, 3.0
HLW, HLLO, HLHI, TM = 120, 2, 40, 3.0
TARGET_VOL = 0.10 / math.sqrt(252)     # 10% annual per spread
CAP = 3.0
COST, COST_STRESS = 0.0005, 0.0010
IS_FRAC = 0.6

def load(sym):
    f = glob.glob(f"{DATA}/*_{sym}!*.csv")[0]
    df = pd.read_csv(f); df.columns = [c.strip().lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["time"], errors="coerce")
    s = df.dropna(subset=["date", "close"]).set_index("date")["close"].sort_index()
    return s[s > 0]                     # drop contaminated back-adjusted negative era

def ratio(a, b):
    A, B = load(a), load(b)
    df = pd.concat([A, B], axis=1, keys=["a", "b"]).dropna()
    P = df.a / df.b
    return P, P.pct_change()            # dollar-neutral return = pct change of ratio (1st order)

def diff(legs, coefs):
    S = pd.concat([load(l) for l in legs], axis=1, keys=range(len(legs))).dropna()
    P = sum(c * S[i] for i, c in enumerate(coefs))
    N = sum(abs(c) * S[i] for i, c in enumerate(coefs))    # gross notional posted
    g = P.diff() / N.shift(1)
    return P, g

# economically-motivated universe (fixed weights — NO estimated beta -> no rolling-beta artifact)
SPREADS = {
    "SI_HG silver-copper":   lambda: ratio("SI1", "HG1"),
    "GC_SI gold-silver":     lambda: ratio("GC1", "SI1"),
    "GC_PL gold-platinum":   lambda: ratio("GC1", "PL1"),
    "PL_PA plat-palladium":  lambda: ratio("PL1", "PA1"),
    "HG_PL copper-platinum": lambda: ratio("HG1", "PL1"),
    "BRN_WBS brent-wti":     lambda: diff(["BRN1", "WBS1"], [1, -1]),
    "RBcrack gasoline":      lambda: diff(["RB1", "WBS1"], [42, -1]),
    "crush soybean":         lambda: diff(["ZM1", "ZL1", "ZS1"], [0.022, 0.11, -0.01]),
    "NG_cal natgas M1-M2":   lambda: diff(["NG1", "NG2"], [1, -1]),
    "RB_cal rbob M1-M2":     lambda: diff(["RB1", "RB2"], [1, -1]),
}

def hl(x):
    lag = x[:-1]; d = np.diff(x)
    if len(d) < 20 or lag.std() == 0: return np.nan
    b = np.polyfit(lag, d, 1)[0]
    return -math.log(2) / b if b < 0 else np.nan

def signal_positions(P):
    Pv = P.values; n = len(Pv)
    s = pd.Series(Pv); m = s.shift(1).rolling(ZLEN).mean(); sd = s.shift(1).rolling(ZLEN).std()
    z = ((s - m) / sd).values
    pos = np.zeros(n); cur = 0; entry = 0; held = 0
    for i in range(HLW + ZLEN, n):
        h = hl(Pv[i - HLW:i]); gate = (not np.isnan(h)) and HLLO <= h <= HLHI
        zz = z[i]; tstop = max(5, int(TM * h)) if not np.isnan(h) else 60
        if cur != 0:
            held += 1
            if np.isnan(zz) or abs(zz) >= ZS or held >= tstop or not gate \
               or (cur > 0 and zz >= -ZX) or (cur < 0 and zz <= ZX):
                cur = 0; held = 0
        if cur == 0 and gate and not np.isnan(zz):
            if zz <= -ZE: cur = 1; entry = i; held = 0
            elif zz >= ZE: cur = -1; entry = i; held = 0
        pos[i] = cur
    return pd.Series(pos, index=P.index)

def book(P, g, cost):
    pos = signal_positions(P)
    sig = g.ewm(span=63, min_periods=20).std()
    w = (pos * (TARGET_VOL / sig.replace(0, np.nan))).clip(-CAP, CAP).fillna(0)
    r = w.shift(1) * g - cost * (w - w.shift(1)).abs()
    return r.fillna(0), pos

def metrics(r):
    r = r[r.index >= r[r != 0].index[0]] if (r != 0).any() else r
    if len(r) < 50: return None
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if eq.iloc[-1] > 0 else -1
    sh = r.mean() / r.std() * math.sqrt(252) if r.std() > 0 else 0
    dd = (eq / eq.cummax() - 1).min()
    le = np.log(eq.clip(lower=1e-6).values); x = np.arange(len(le)); b1, b0 = np.polyfit(x, le, 1)
    r2 = 1 - ((le - (b1 * x + b0)) ** 2).sum() / max(((le - le.mean()) ** 2).sum(), 1e-9)
    trades = int((pos_changes := (np.diff((r != 0).astype(int)) != 0).sum()))  # rough
    return dict(eq=eq, sharpe=sh, cagr=cagr, maxdd=dd, r2=r2, n=len(r))

def split_metrics(r):
    cut = int(len(r) * IS_FRAC)
    return metrics(r.iloc[:cut]), metrics(r.iloc[cut:]), metrics(r)

def main():
    rows = []; curves = {}; books = {}
    for name, fn in SPREADS.items():
        try:
            P, g = fn(); g = g.dropna(); P = P.loc[g.index]
        except Exception as e:
            print(f"{name}: load error {e}"); continue
        r, pos = book(P, g, COST)
        rs, _ = book(P, g, COST_STRESS)
        ntr = int((pos.diff().abs() > 0).sum())
        mi, mo, mf = split_metrics(r)
        if mf is None: continue
        msf = metrics(rs)
        survive = (mi and mo and mi["cagr"] > 0 and mo["cagr"] > 0)
        rows.append((name, ntr, mf, mi, mo, msf, survive))
        curves[name] = mf["eq"]; books[name] = r

    rows.sort(key=lambda x: -(x[4]["sharpe"] if x[4] else -9))  # by OOS Sharpe
    print(f"\nOU-gated spread MR — net of cost.  per-spread vol target 10%/yr, "
          f"cost {COST*100:.2f}%/turn (stress {COST_STRESS*100:.2f}%).  IS={IS_FRAC:.0%}/OOS.\n")
    print(f"{'spread':<24}{'trades':>7}{'fullShrp':>9}{'fullCAGR':>9}{'maxDD':>8}"
          f"{'eqR2':>7}{'OOSshrp':>9}{'OOScagr':>9}{'strShrp':>9}  survive")
    for name, ntr, mf, mi, mo, msf, surv in rows:
        print(f"{name:<24}{ntr:>7}{mf['sharpe']:>9.2f}{mf['cagr']*100:>8.1f}%{mf['maxdd']*100:>7.1f}%"
              f"{mf['r2']:>7.2f}{(mo['sharpe'] if mo else 0):>9.2f}"
              f"{(mo['cagr']*100 if mo else 0):>8.1f}%{msf['sharpe']:>9.2f}  {'YES' if surv else '.'}")

    # equity-curve grid
    k = len(curves); cols = 2; rowsn = math.ceil(k / cols)
    fig, ax = plt.subplots(rowsn, cols, figsize=(13, 2.4 * rowsn)); ax = ax.flatten()
    for i, (name, eq) in enumerate(curves.items()):
        cut = int(len(eq) * IS_FRAC)
        ax[i].plot(eq.index, eq.values, lw=1.1, color="navy")
        ax[i].axvline(eq.index[cut], color="gray", ls="--", lw=0.7)
        ax[i].axhline(1.0, color="red", ls=":", lw=0.6)
        ax[i].set_title(name, fontsize=9); ax[i].tick_params(labelsize=7)
    for j in range(k, len(ax)): ax[j].axis("off")
    fig.suptitle(f"OU-gated spread MR — net equity (cost {COST*100:.2f}%/turn) | dashed=IS/OOS split",
                 fontsize=11)
    fig.tight_layout(); p1 = os.path.join(OUT, "equity_grid.png"); fig.savefig(p1, dpi=110); plt.close(fig)

    # survivor book
    surv_names = [name for name, ntr, mf, mi, mo, msf, s in rows if s]
    if surv_names:
        B = pd.DataFrame({n: books[n] for n in surv_names})
        port = B.mean(axis=1).where(B.notna().sum(axis=1) >= 1).fillna(0)
        m = metrics(port)
        fig2, a2 = plt.subplots(figsize=(11, 4))
        a2.plot(m["eq"].index, m["eq"].values, color="darkgreen", lw=1.4)
        a2.axhline(1.0, color="red", ls=":", lw=0.7)
        a2.set_title(f"SURVIVOR BOOK ({', '.join(surv_names)})  "
                     f"Sharpe={m['sharpe']:.2f} CAGR={m['cagr']*100:.1f}% maxDD={m['maxdd']*100:.1f}% "
                     f"eqR2={m['r2']:.2f}", fontsize=10)
        fig2.tight_layout(); p2 = os.path.join(OUT, "survivor_book.png"); fig2.savefig(p2, dpi=120); plt.close(fig2)
        print(f"\nSURVIVORS (net-positive IS AND OOS after {COST*100:.2f}%): {surv_names}")
        print(f"  book: Sharpe={m['sharpe']:.2f} CAGR={m['cagr']*100:.1f}% maxDD={m['maxdd']*100:.1f}% eqR2={m['r2']:.2f}")
        print(f"  -> {p2}")
    else:
        print("\nSURVIVORS: NONE clear the bar (net-positive in BOTH IS and OOS after 0.05%).")
    print(f"equity grid -> {p1}")

if __name__ == "__main__":
    main()
