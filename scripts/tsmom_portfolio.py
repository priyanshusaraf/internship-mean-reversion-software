#!/usr/bin/env python3
"""
Diversified vol-targeted TREND portfolio (time-series momentum, Moskowitz-Ooi-Pedersen).
THE smoothness engine: each instrument runs a multi-horizon trend signal, vol-targeted to
equal risk; the BOOK = average across instruments by calendar date. Diversification across
low-correlation trend bets is what produces a smooth equity curve (the CTA shape).

Causal: signal & vol use only past data; position set at t-1 earns return at t.
Reports portfolio Sharpe / CAGR / maxDD / R^2, IS vs OOS, per-instrument contribution.
"""
import glob, os, math, sys
import numpy as np, pandas as pd
from backtest_mr import load_csv

SIGNAL = os.environ.get('SIGNAL', 'tsmom')   # 'tsmom' or 'donchian'

def donchian_state(df, don=55, exit_don=20):
    h, l, c = df.set_index('date')['high'], df.set_index('date')['low'], df.set_index('date')['close']
    hi = h.shift(1).rolling(don).max(); lo = l.shift(1).rolling(don).min()
    xhi = h.shift(1).rolling(exit_don).max(); xlo = l.shift(1).rolling(exit_don).min()
    H, L, C = h.values, l.values, c.values
    HI, LO, XH, XL = hi.values, lo.values, xhi.values, xlo.values
    st = np.zeros(len(C)); s = 0
    for i in range(len(C)):
        if np.isnan(HI[i]): st[i] = 0; continue
        if s <= 0 and C[i] > HI[i]: s = 1
        elif s >= 0 and C[i] < LO[i]: s = -1
        elif s == 1 and C[i] < XL[i]: s = 0
        elif s == -1 and C[i] > XH[i]: s = 0
        st[i] = s
    return pd.Series(st, index=c.index)

TARGET_VOL = 0.15           # annualized vol target per instrument
LOOKBACKS  = [21, 63, 126, 252]   # 1,3,6,12-month time-series momentum
COST_BPS   = 1.0            # per unit of position turnover (1bp)
POS_CAP    = 2.0

def instrument_positions(df):
    """Return a daily Series of target positions (signed, vol-scaled) indexed by date."""
    c = df.set_index('date')['close'].astype(float)
    ret = c.pct_change()
    vol = ret.ewm(span=63, min_periods=20).std() * math.sqrt(252)
    if SIGNAL == 'donchian':
        sig = donchian_state(df).reindex(c.index)
    else:
        sig = pd.Series(0.0, index=c.index)        # multi-horizon TSMOM sign in [-1,1]
        for L in LOOKBACKS:
            sig = sig + np.sign(c / c.shift(L) - 1.0)
        sig = (sig / len(LOOKBACKS)).clip(-1, 1)
    pos = (sig * (TARGET_VOL / vol.replace(0, np.nan))).clip(-POS_CAP, POS_CAP)
    return pos.shift(1), ret          # shift(1): position known at t-1 (causal)

def build():
    base = 'data/raw/more-mean-reversion-data'
    files = sorted(glob.glob(f'{base}/*1!*1D*.csv')) + [f'{base}/TVC_SILVER, 1D.csv', f'{base}/SP_SPX, 1D (1).csv']
    pnl_cols = {}
    for f in files:
        if not os.path.exists(f): continue
        try:
            df = load_csv(f); df = df[df['close'] > 0]
            if len(df) < 800: continue
            pos, ret = instrument_positions(df)
            gross = pos * ret
            turn = pos.diff().abs().fillna(0)
            net = gross - turn * (COST_BPS / 1e4)
            nm = os.path.basename(f).split(',')[0].split('_')[-1].replace('1!','').replace('!','')
            pnl_cols[nm] = net
        except Exception:
            pass
    P = pd.DataFrame(pnl_cols).sort_index()
    # portfolio = mean across instruments available each day (equal risk), require >=5 active
    active = P.notna().sum(axis=1)
    port = P.mean(axis=1).where(active >= 5)
    return P, port.dropna()

def perf(r, label):
    r = r.dropna()
    if len(r) < 50: return
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    cagr = eq.iloc[-1] ** (1/yrs) - 1
    sharpe = r.mean() / r.std() * math.sqrt(252)
    dd = (eq / eq.cummax() - 1).min()
    le = np.log(eq.values); x = np.arange(len(le)); b1, b0 = np.polyfit(x, le, 1)
    r2 = 1 - ((le - (b1*x + b0))**2).sum() / max(((le - le.mean())**2).sum(), 1e-9)
    pos_yrs = (r.resample('YE').sum() > 0).mean() if hasattr(r.index, 'resample') else np.nan
    print(f"{label:<14} Sharpe={sharpe:5.2f}  CAGR={cagr*100:6.1f}%  maxDD={dd*100:6.1f}%  "
          f"R2(logeq)={r2:.3f}  +years={pos_yrs*100:.0f}%  n={len(r)}")

if __name__ == '__main__':
    P, port = build()
    port.index = pd.to_datetime(port.index)
    print(f"instruments in book: {P.shape[1]}   portfolio days: {len(port)}\n")
    perf(port, "FULL")
    cut = int(len(port) * 0.7)
    perf(port.iloc[:cut], "IS (70%)")
    perf(port.iloc[cut:], "OOS (30%)")
    # per-instrument standalone Sharpe (contribution sanity)
    print("\nper-instrument standalone Sharpe:")
    s = {c: (P[c].mean()/P[c].std()*math.sqrt(252) if P[c].std()>0 else 0) for c in P.columns}
    s = dict(sorted(s.items(), key=lambda kv: -kv[1]))
    line = "  ".join(f"{k}:{v:.2f}" for k, v in s.items())
    print(line)
    npos = sum(1 for v in s.values() if v > 0)
    print(f"\ninstruments with positive standalone Sharpe: {npos}/{len(s)}")
