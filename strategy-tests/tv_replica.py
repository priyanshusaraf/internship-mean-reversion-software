#!/usr/bin/env python3
"""Replicate TradingView EXACTLY to explain the live -60%: fixed qty=1 (no vol targeting),
FULL history (incl. back-adjusted contaminated early era), raw spread-point P&L, Pine costs.
Same signal as scripts/ou_spread_mr.pine. Diagnose backtest-vs-live gap."""
import glob, math, sys
import numpy as np, pandas as pd
DATA = "/Users/priyanshusaraf/Downloads/commodities-data/daily"

def load(sym):
    f = glob.glob(f"{DATA}/*_{sym}!*.csv")[0]
    df = pd.read_csv(f); df.columns = [c.strip().lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["time"], errors="coerce")
    return df.dropna(subset=["date", "close"]).set_index("date")["close"].sort_index()

SPREADS = {
    "SI/HG (silver/copper ratio)": lambda: load("SI1") / load("HG1"),
    "BRN-WBS (Brent-WTI)":         lambda: load("BRN1") - load("WBS1"),
    "NG1-NG2 (NG calendar)":       lambda: load("NG1") - load("NG2"),
    "GC/SI (gold/silver ratio)":   lambda: load("GC1") / load("SI1"),
}
ZLEN, ZE, ZX, ZS, HLW, HLLO, HLHI, TM = 40, 2.0, 0.5, 3.0, 120, 2, 40, 3.0
COST_PCT = 0.0002  # 0.02% Pine commission, per side, on notional ~|spread|

def hl_slope(x):
    lag = x[:-1]; d = np.diff(x)
    if len(d) < 20 or lag.std() == 0: return np.nan
    b = np.polyfit(lag, d, 1)[0]
    return -math.log(2)/b if b < 0 else np.nan

def run(X, start=None):
    X = X.dropna()
    if start: X = X[X.index >= start]
    Xv = X.values; n = len(Xv); idx = X.index
    s = pd.Series(Xv); m = s.shift(1).rolling(ZLEN).mean(); sd = s.shift(1).rolling(ZLEN).std()
    z = ((s - m)/sd).values
    eq = [0.0]; cur = 0; entry = 0; held = 0; trades = []
    for i in range(HLW + ZLEN, n):
        hl = hl_slope(Xv[i-HLW:i])
        gate = (not np.isnan(hl)) and HLLO <= hl <= HLHI
        zz = z[i]; tstop = max(5, int(TM*hl)) if not np.isnan(hl) else 60
        pnl_step = cur * (Xv[i] - Xv[i-1])          # fixed qty=1, raw spread points
        eq.append(eq[-1] + pnl_step)
        if cur != 0:
            held += 1
            ex = np.isnan(zz) or abs(zz) >= ZS or held >= tstop or not gate \
                 or (cur > 0 and zz >= -ZX) or (cur < 0 and zz <= ZX)
            if ex:
                trades.append((Xv[i]-Xv[entry])*cur); cur = 0; held = 0
                eq[-1] -= abs(Xv[i])*COST_PCT
        if cur == 0 and gate and not np.isnan(zz):
            if zz <= -ZE: cur = 1; entry = i; held = 0; eq[-1] -= abs(Xv[i])*COST_PCT
            elif zz >= ZE: cur = -1; entry = i; held = 0; eq[-1] -= abs(Xv[i])*COST_PCT
    eq = np.array(eq); end = eq[-1]
    wr = np.mean([t > 0 for t in trades]) if trades else 0
    dd = (eq - np.maximum.accumulate(eq)).min()
    return dict(start=str(idx[0].date()), n=n, trades=len(trades), win=wr*100,
                totpts=end, maxdd=dd, first=Xv[0], last=Xv[-1])

for name, fn in SPREADS.items():
    X = fn()
    full = run(X); rec = run(X, "2010-01-01")
    print(f"\n== {name} ==  (price range over full history: {X.min():.2f} .. {X.max():.2f})")
    print(f"  FULL   from {full['start']}: trades={full['trades']:4d} win%={full['win']:3.0f} "
          f"totPNL_pts={full['totpts']:+9.1f} maxDD_pts={full['maxdd']:+9.1f}")
    print(f"  2010+  from {rec['start']}: trades={rec['trades']:4d} win%={rec['win']:3.0f} "
          f"totPNL_pts={rec['totpts']:+9.1f} maxDD_pts={rec['maxdd']:+9.1f}")
