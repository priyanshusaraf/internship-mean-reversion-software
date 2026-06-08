#!/usr/bin/env python3
"""Quick evidence check: does TREND-FOLLOWING profit where MR loses on these instruments?
Donchian breakout (Turtle-style) + ATR trailing stop, long&short, R-based, on the outright legs."""
import glob, os, math
import numpy as np, pandas as pd
from backtest_mr import load_csv, atr

def trend_bt(df, don=55, exit_don=20, atr_n=20, atr_trail=3.0, cost_atr=0.05):
    h,l,c,o = df['high'],df['low'],df['close'],df['open']
    a = atr(h,l,c,atr_n)
    hi = h.shift(1).rolling(don).max(); lo = l.shift(1).rolling(don).min()
    xhi = h.shift(1).rolling(exit_don).max(); xlo = l.shift(1).rolling(exit_don).min()
    H,L,C,O,A = h.values,l.values,c.values,o.values,a.values
    HI,LO,XHI,XLO = hi.values,lo.values,xhi.values,xlo.values
    pos=0; entry=np.nan; trail=np.nan; Rr=np.nan; trades=[]
    warm=don+atr_n+2
    for i in range(warm,len(df)-1):
        if pos==0:
            if not np.isnan(A[i]) and A[i]>0:
                if H[i] > HI[i]: pos=1; entry=O[i+1]; Rr=atr_trail*A[i]; trail=entry-Rr
                elif L[i] < LO[i]: pos=-1; entry=O[i+1]; Rr=atr_trail*A[i]; trail=entry+Rr
            continue
        side=pos; exit_px=None
        if side==1:
            trail=max(trail, C[i]-atr_trail*A[i])
            if C[i] < XLO[i] or C[i] < trail: exit_px=C[i]
        else:
            trail=min(trail, C[i]+atr_trail*A[i])
            if C[i] > XHI[i] or C[i] > trail: exit_px=C[i]
        if exit_px is not None:
            trades.append(side*(exit_px-entry)/Rr - cost_atr*A[i]/Rr); pos=0
    return np.array(trades)

def stats(R, yrs):
    if len(R)==0: return None
    eq=np.cumsum(R); dd=-(eq-np.maximum.accumulate(eq)).min()
    pf=R[R>0].sum()/(-R[R<0].sum()) if (R<0).any() else np.inf
    return dict(n=len(R), win=100*(R>0).mean(), totR=eq[-1], pf=pf, dd=dd,
                rdd=eq[-1]/dd if dd>0 else np.inf, tr_yr=len(R)/yrs)

if __name__=='__main__':
    base='data/raw/more-mean-reversion-data'
    files=sorted(glob.glob(f'{base}/*1!*1D*.csv'))+[f'{base}/TVC_SILVER, 1D.csv',f'{base}/SP_SPX, 1D (1).csv']
    allR=[]; rows=[]
    for f in files:
        if not os.path.exists(f): continue
        try:
            df=load_csv(f); df=df[df['close']>0].reset_index(drop=True)
            if len(df)<800: continue
            yrs=(df['date'].iloc[-1]-df['date'].iloc[0]).days/365.25
            R=trend_bt(df); s=stats(R,yrs)
            if s: rows.append((os.path.basename(f).split(',')[0][:18], s)); allR.append((df['date'].iloc[len(df)-len(R):].values if len(R) else [], R))
        except Exception as e: rows.append((os.path.basename(f)[:18], {'err':str(e)[:30]}))
    print(f"{'instrument':<20}{'n':>5}{'tr/yr':>7}{'win%':>7}{'totR':>8}{'PF':>7}{'maxDD':>8}{'totR/DD':>9}")
    print('-'*72); pos=0
    for nm,s in rows:
        if 'err' in s: print(f"{nm:<20} ERR {s['err']}"); continue
        print(f"{nm:<20}{s['n']:>5}{s['tr_yr']:>7.1f}{s['win']:>7.1f}{s['totR']:>8.1f}{s['pf']:>7.2f}{s['dd']:>8.1f}{s['rdd']:>9.2f}")
        if s['totR']>0: pos+=1
    allflat=np.concatenate([r for _,r in allR if len(r)])
    eq=np.cumsum(allflat); dd=-(eq-np.maximum.accumulate(eq)).min()
    print('-'*72)
    print(f"profitable: {pos}/{len([r for r in rows if 'err' not in r[1]])}  |  POOLED book: trades={len(allflat)} "
          f"totR={eq[-1]:.1f} maxDD={dd:.1f} totR/DD={eq[-1]/dd:.2f} win%={100*(allflat>0).mean():.1f}")
