#!/usr/bin/env python3
"""
Regime-switch HYBRID — single-instrument, OHLC, causal, R-based.
  ADX >= adx_trend  -> TREND regime: Donchian breakout + ATR trailing stop (ride it).
  ADX <  adx_trend  -> RANGE regime: z-score fade, mean target, entry-rel stop, time stop.
Each sub-strategy covers the other's failure mode (MR dies in trends; trend whipsaws in ranges).
R = risk unit per trade (trend: atr_trail*ATR; MR: stop_sig*sigma) -> equity in R, comparable.
"""
import sys, glob, os, math
import numpy as np, pandas as pd
from backtest_mr import load_csv, atr, adx, supertrend

D = dict(adx_n=14, adx_trend=25, adx_hyst=5,
         don=55, exit_don=20, atr_n=20, atr_trail=3.0,
         z_n=40, z_entry=2.0, z_exit=0.5, stop_sig=2.5, time_stop=30,
         use_st_exit=True, cost_atr=0.05, use_mr=True)

def run(df, p):
    h,l,c,o = df['high'],df['low'],df['close'],df['open']
    a = atr(h,l,c,p['atr_n']); ad = adx(h,l,c,p['adx_n'])
    [stdir] = [supertrend(h,l,c,3.0,10)]
    don_hi = h.shift(1).rolling(p['don']).max(); don_lo = l.shift(1).rolling(p['don']).min()
    xhi = h.shift(1).rolling(p['exit_don']).max(); xlo = l.shift(1).rolling(p['exit_don']).min()
    zmean = c.shift(1).rolling(p['z_n']).mean(); zstd = c.shift(1).rolling(p['z_n']).std()
    z = (c - zmean)/zstd.replace(0,np.nan)
    H,L,C,O,A,AD = h.values,l.values,c.values,o.values,a.values,ad.values
    DH,DL,XH,XL = don_hi.values,don_lo.values,xhi.values,xlo.values
    Z,ZS,ST = z.values,zstd.values,stdir.values
    warm = max(p['don']+5, p['z_n']+5, p['adx_n']*3, p['atr_n']*3)
    pos=0; kind=''; entry=np.nan; R=np.nan; trail=np.nan; bar=0; esig=np.nan; eatr=np.nan
    trades=[]
    for i in range(warm, len(df)-1):
        trending = AD[i] >= p['adx_trend']
        if pos==0:
            if np.isnan(A[i]) or A[i]<=0: continue
            if trending:                                  # TREND breakout
                if H[i] > DH[i]: pos=1; kind='T'; entry=O[i+1]; R=p['atr_trail']*A[i]; trail=entry-R; eatr=A[i]; bar=0
                elif L[i] < DL[i]: pos=-1; kind='T'; entry=O[i+1]; R=p['atr_trail']*A[i]; trail=entry+R; eatr=A[i]; bar=0
            elif p['use_mr']:                             # RANGE fade (only if MR leg enabled)
                trapL = AD[i]>=20 and ST[i]>0; trapS = AD[i]>=20 and ST[i]<0
                if not np.isnan(Z[i]) and not np.isnan(ZS[i]) and ZS[i]>0:
                    if Z[i] <= -p['z_entry'] and not trapL: pos=1; kind='M'; entry=O[i+1]; esig=ZS[i]; R=p['stop_sig']*ZS[i]; eatr=A[i]; bar=0
                    elif Z[i] >= p['z_entry'] and not trapS: pos=-1; kind='M'; entry=O[i+1]; esig=ZS[i]; R=p['stop_sig']*ZS[i]; eatr=A[i]; bar=0
            continue
        bar+=1; side=pos; exit_px=None
        if kind=='T':                                     # trend: ATR trail + opposite donchian + ST flip
            if side==1:
                trail=max(trail, C[i]-p['atr_trail']*A[i])
                if C[i] < XL[i] or C[i] < trail or (p['use_st_exit'] and ST[i]>0): exit_px=C[i]
            else:
                trail=min(trail, C[i]+p['atr_trail']*A[i])
                if C[i] > XH[i] or C[i] > trail or (p['use_st_exit'] and ST[i]<0): exit_px=C[i]
        else:                                             # MR: mean target | entry-rel stop | time
            if side==1:
                if (entry-C[i]) >= p['stop_sig']*esig: exit_px=C[i]
                elif not np.isnan(Z[i]) and Z[i] >= -p['z_exit']: exit_px=C[i]
            else:
                if (C[i]-entry) >= p['stop_sig']*esig: exit_px=C[i]
                elif not np.isnan(Z[i]) and Z[i] <= p['z_exit']: exit_px=C[i]
            if exit_px is None and bar >= p['time_stop']: exit_px=C[i]
        if exit_px is not None:
            pnl = side*(exit_px-entry)/R - p['cost_atr']*eatr/R
            trades.append({'pnl_R':pnl,'kind':kind,'date':df['date'].iloc[i]}); pos=0
    return pd.DataFrame(trades)

def stat(tr, yrs, lab=''):
    if len(tr)==0: return None
    R=tr['pnl_R'].values; eq=np.cumsum(R); dd=-(eq-np.maximum.accumulate(eq)).min()
    pf=R[R>0].sum()/(-R[R<0].sum()) if (R<0).any() else np.inf
    x=np.arange(len(eq)); b1,b0=np.polyfit(x,eq,1)
    r2=1-((eq-(b1*x+b0))**2).sum()/max(((eq-eq.mean())**2).sum(),1e-9)
    return dict(n=len(R),win=100*(R>0).mean(),totR=eq[-1],pf=pf,dd=dd,
               rdd=eq[-1]/dd if dd>0 else np.inf, r2=r2, tr_yr=len(R)/yrs if yrs else 0)

if __name__=='__main__':
    p=dict(D)
    for a in sys.argv[1:]:
        if '=' in a:
            k,v=a.split('=')
            if k in p: p[k]=(v.lower() in('1','true')) if isinstance(p[k],bool) else int(float(v)) if isinstance(p[k],int) else float(v)
    base='data/raw/more-mean-reversion-data'
    files=sorted(glob.glob(f'{base}/*1!*1D*.csv'))+[f'{base}/TVC_SILVER, 1D.csv',f'{base}/SP_SPX, 1D (1).csv']
    print(f"{'instrument':<18}{'n':>5}{'tr/yr':>6}{'win%':>6}{'totR':>7}{'PF':>6}{'rdd':>6}{'R2':>6}{'OOSr':>7}")
    print('-'*68)
    allis=[]; alloos=[]; pos=0; ninst=0
    for f in files:
        if not os.path.exists(f): continue
        try:
            df=load_csv(f); df=df[df['close']>0].reset_index(drop=True)
            if len(df)<800: continue
            yrs=(df['date'].iloc[-1]-df['date'].iloc[0]).days/365.25
            tr=run(df,p); s=stat(tr,yrs)
            if s is None: continue
            ninst+=1
            cut=df['date'].iloc[0]+(df['date'].iloc[-1]-df['date'].iloc[0])*0.7
            oos=tr[tr['date']>=cut]; oosR=oos['pnl_R'].sum()
            allis.append(tr); alloos.append(oos)
            if s['totR']>0: pos+=1
            print(f"{os.path.basename(f).split(',')[0][:16]:<18}{s['n']:>5}{s['tr_yr']:>6.1f}{s['win']:>6.1f}"
                  f"{s['totR']:>7.1f}{s['pf']:>6.2f}{s['rdd']:>6.2f}{s['r2']:>6.2f}{oosR:>7.1f}")
        except Exception as e: print(f"{os.path.basename(f)[:16]:<18} ERR {str(e)[:30]}")
    P=pd.concat(allis).sort_values('date'); O=pd.concat(alloos).sort_values('date')
    sP=stat(P,(P['date'].iloc[-1]-P['date'].iloc[0]).days/365.25); sO=stat(O,(O['date'].iloc[-1]-O['date'].iloc[0]).days/365.25)
    print('-'*68)
    print(f"profitable: {pos}/{ninst}")
    print(f"POOLED ALL : trades={sP['n']} totR={sP['totR']:.0f} totR/DD={sP['rdd']:.2f} win%={sP['win']:.0f} R2={sP['r2']:.2f}")
    print(f"POOLED OOS : trades={sO['n']} totR={sO['totR']:.0f} totR/DD={sO['rdd']:.2f} win%={sO['win']:.0f} R2={sO['r2']:.2f}")
    bk=P.groupby('kind')['pnl_R'].agg(['count','sum'])
    print(f"by regime  : {dict(zip(bk.index, [f'n={int(r[0])} totR={r[1]:.0f}' for r in bk.values]))}")
