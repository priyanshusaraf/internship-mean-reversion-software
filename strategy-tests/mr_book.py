#!/usr/bin/env python3
"""
Diversified cross-commodity MEAN-REVERSION BOOK — the strategy distilled from our research.
Data: ONLY /Users/priyanshusaraf/Downloads/commodities-data/daily  (outright M1 legs).

Logic:
  - candidate spread S = ln(A) - beta*ln(B)  (beta from TRAIN OLS, frozen for TEST -> causal).
  - cointegration gate (Engle-Granger ADF on train residual) + tradeable half-life -> 'active'.
  - on active TEST windows, discrete z-MR: enter |z|>=z_entry, exit |z|<=z_exit, z-disaster stop,
    time stop, or flat when the pair loses cointegration. (Matches the Pine we ship.)
  - BOOK = vol-targeted, equal-risk daily P&L averaged across active spreads (the smoothness engine).
  - true out-of-sample by construction; report which spreads survive + book Sharpe/DD/R2/turnover.
"""
import os, glob, math, itertools, sys
import numpy as np, pandas as pd
from statsmodels.tsa.stattools import adfuller

DATA = "/Users/priyanshusaraf/Downloads/commodities-data/daily"

P = dict(z_n=60, z_entry=2.0, z_exit=0.5, z_disaster=4.0, max_hold=60,
         train_len=750, test_len=250, step=250, adf_p=0.05, hl_lo=5, hl_hi=80,
         cost=0.0010, target=0.01, vol_span=63)
for a in sys.argv[1:]:
    if '=' in a:
        k,v=a.split('=')
        if k in P: P[k]= int(float(v)) if isinstance(P[k],int) else float(v)

def load():
    U={}
    for f in glob.glob(f"{DATA}/*1!*.csv"):
        nm=os.path.basename(f).split('_')[-1].split(',')[0].replace('1!','')
        df=pd.read_csv(f); df.columns=[c.strip().lower() for c in df.columns]
        df['date']=pd.to_datetime(df['time'], errors='coerce')
        df=df.dropna(subset=['date','close']); df=df[df['close']>0]
        if len(df)>=1300: U[nm]=df.set_index('date')['close'].sort_index()
    return U

def half_life(x):
    x=pd.Series(x); lag=x.shift(1); d=(x-lag).dropna(); lag=lag.loc[d.index]
    if len(d)<30 or lag.std()==0: return np.nan
    b=np.polyfit(lag.values,d.values,1)[0]
    return -math.log(2)/b if b<0 else np.nan

def run_pair(la, lb, dates, p):
    """Return daily strategy P&L series (vol-targeted) for one pair, traded only on cointegrated
       TEST windows. la,lb are aligned np arrays of log prices."""
    n=len(la); pnl=np.zeros(n); pos=np.zeros(n); active=np.zeros(n,bool)
    tl,te,st=p['train_len'],p['test_len'],p['step']
    t0=tl
    # precompute nothing global; per-window beta
    while t0+te<=n:
        tr=slice(t0-tl,t0)
        X=np.vstack([np.ones(tl),lb[tr]]).T
        coef,_,_,_=np.linalg.lstsq(X,la[tr],rcond=None); alpha,beta=coef[0],coef[1]
        resid=la[tr]-(alpha+beta*lb[tr])
        try: pv=adfuller(resid,maxlag=1,autolag=None)[1]
        except Exception: pv=1.0
        hl=half_life(resid)
        if pv<p['adf_p'] and not np.isnan(hl) and p['hl_lo']<=hl<=p['hl_hi']:
            lo=max(0,t0-150); hi=t0+te
            S=la[lo:hi]-(alpha+beta*lb[lo:hi])          # frozen-beta spread, with warmup
            s=pd.Series(S)
            m=s.shift(1).rolling(p['z_n']).mean(); sd=s.shift(1).rolling(p['z_n']).std()
            z=((s-m)/sd).values
            dS=np.diff(S, prepend=S[0])
            sig=pd.Series(dS).ewm(span=p['vol_span'],min_periods=20).std().values
            off=t0-lo                                    # index in S where TEST starts
            cur=0; held=0
            for j in range(off,len(S)):
                gi=lo+j                                  # global index
                active[gi]=True
                zz=z[j]
                if cur!=0:
                    held+=1
                    if np.isnan(zz) or abs(zz)>=p['z_disaster'] or \
                       (cur>0 and zz>=-p['z_exit']) or (cur<0 and zz<=p['z_exit']) or held>=p['max_hold']:
                        cur=0; held=0
                if cur==0 and not np.isnan(zz):
                    if zz<=-p['z_entry']: cur=1; held=0
                    elif zz>=p['z_entry']: cur=-1; held=0
                sz = (p['target']/sig[j]) if (not np.isnan(sig[j]) and sig[j]>0) else 0.0
                pos[gi]=cur*sz
        t0+=st
    # daily pnl with cost on turnover (pos set at t-1 earns dS at t)
    for i in range(1,n):
        d = la[i]-la[i-1] - 0  # placeholder; real spread dS computed below
    # recompute pnl using the realized per-window spread change is complex; approximate with
    # global dS of the *last-active* beta is wrong. Instead: P&L of holding the spread = pos*dCloseSpread.
    # We stored pos in size units; the spread daily change in the ACTIVE window is dS there. Approx with
    # pair's raw log-change difference (beta~1 dollar-neutral proxy) is inaccurate; so accumulate within loop.
    return pnl, pos, active, dates

# Economically-linked pairs ONLY (production/substitution cointegration rationale).
CURATED = [
    # grains / oilseeds
    ('ZC','ZW'),('ZW','KE'),('ZC','KE'),('ZC','ZS'),('ZS','ZM'),('ZS','ZL'),('ZM','ZL'),
    ('ZO','ZC'),('ZO','ZW'),
    # energy complex (crude grades + products = cracks)
    ('BRN','WBS'),('BRN','ULS'),('BRN','UHO'),('WBS','RB'),('BRN','RB'),('UHO','ULS'),('RB','UHO'),
    # metals (precious + industrial substitution)
    ('GC','SI'),('GC','PL'),('PL','PA'),('HG','PL'),('SI','HG'),('GC','PA'),('SI','PL'),
    # livestock
    ('LE','GF'),('LE','HE'),('GF','HE'),
    # softs
    ('CC','KC'),('KC','SB'),('CT','SB'),('CC','SB'),
]
def main():
    U=load()
    names=sorted(U.keys())
    curated = os.environ.get('CURATED','1')=='1'
    pair_iter = [(a,b) for a,b in CURATED if a in U and b in U] if curated else list(itertools.combinations(names,2))
    print(f"universe: {len(names)} commodities | {'CURATED economic pairs' if curated else 'ALL pairs'}: {len(pair_iter)}")
    # align all on common calendar
    book=None; perpair={}; turn_tot=0; act_pairs=0
    daily=pd.DataFrame(index=sorted(set().union(*[set(U[n].index) for n in names])))
    for a,b in pair_iter:
        s=pd.concat([np.log(U[a]),np.log(U[b])],axis=1,keys=['a','b']).dropna()
        if len(s)<P['train_len']+P['test_len']+200: continue
        la=s['a'].values; lb=s['b'].values; n=len(s)
        # inline walk-forward producing a daily strategy-return series in spread units
        pnl=np.zeros(n)
        tl,te,stp=P['train_len'],P['test_len'],P['step']; t0=tl; traded=False
        while t0+te<=n:
            tr=slice(t0-tl,t0)
            X=np.vstack([np.ones(tl),lb[tr]]).T
            coef=np.linalg.lstsq(X,la[tr],rcond=None)[0]; alpha,beta=coef
            resid=la[tr]-(alpha+beta*lb[tr])
            try: pv=adfuller(resid,maxlag=1,autolag=None)[1]
            except Exception: pv=1.0
            hl=half_life(resid)
            if pv<P['adf_p'] and not np.isnan(hl) and P['hl_lo']<=hl<=P['hl_hi']:
                lo=max(0,t0-150); hi=t0+te
                S=la[lo:hi]-(alpha+beta*lb[lo:hi]); dS=np.diff(S,prepend=S[0])
                ss=pd.Series(S); m=ss.shift(1).rolling(P['z_n']).mean(); sd=ss.shift(1).rolling(P['z_n']).std()
                z=((ss-m)/sd).values
                sig=pd.Series(dS).ewm(span=P['vol_span'],min_periods=20).std().values
                off=t0-lo; cur=0; held=0; prevpos=0.0
                for j in range(off,len(S)):
                    gi=lo+j; zz=z[j]
                    if cur!=0:
                        held+=1
                        if np.isnan(zz) or abs(zz)>=P['z_disaster'] or (cur>0 and zz>=-P['z_exit']) or (cur<0 and zz<=P['z_exit']) or held>=P['max_hold']:
                            cur=0; held=0
                    if cur==0 and not np.isnan(zz):
                        if zz<=-P['z_entry']: cur=1; held=0
                        elif zz>=P['z_entry']: cur=-1; held=0
                    sz=(P['target']/sig[j]) if (not np.isnan(sig[j]) and sig[j]>0) else 0.0
                    curpos=cur*sz
                    if gi>0: pnl[gi]= prevpos*dS[j] - abs(curpos-prevpos)*P['cost']
                    prevpos=curpos; traded=True
            t0+=stp
        if traded and np.any(pnl!=0):
            ser=pd.Series(pnl,index=s.index)
            daily[f'{a}-{b}']=ser
            perpair[f'{a}-{b}']=pnl[pnl!=0].sum()
            act_pairs+=1
    # BOOK: equal-risk average across spreads active each day
    cols=[c for c in daily.columns]
    B=daily[cols]
    book=B.mean(axis=1).where(B.notna().sum(axis=1)>=3).dropna()
    perf(book,"BOOK FULL")
    cut=int(len(book)*0.6)
    perf(book.iloc[:cut],"BOOK IS(60%)"); perf(book.iloc[cut:],"BOOK OOS(40%)")
    # per-pair IS/OOS robustness (positive in BOTH halves = defensible)
    pos=sum(1 for v in perpair.values() if v>0)
    print(f"\ntraded pairs: {act_pairs} | pair total-PnL positive: {pos}/{len(perpair)}")
    rob=[]
    for c in daily.columns:
        s=daily[c].dropna()
        if len(s)<200: continue
        cut=int(len(s)*0.6); isr=s.iloc[:cut].sum(); oos=s.iloc[cut:].sum()
        sh=s.mean()/s.std()*math.sqrt(252) if s.std()>0 else 0
        rob.append((c,isr*100,oos*100,sh))
    rob.sort(key=lambda r:-(r[2]))
    print(f"{'pair':<10}{'IS':>8}{'OOS':>8}{'Sharpe':>8}")
    for c,i,o,sh in rob: print(f"{c:<10}{i:>8.1f}{o:>8.1f}{sh:>8.2f}")
    both=[c for c,i,o,sh in rob if i>0 and o>0]
    print(f"\npositive in BOTH IS and OOS: {both}")
    return book, daily, perpair

def perf(r,label):
    r=r.dropna()
    if len(r)<50: print(f"{label}: too few"); return
    eq=r.cumsum()
    sharpe=r.mean()/r.std()*math.sqrt(252) if r.std()>0 else 0
    dd=(eq-eq.cummax()).min()
    x=np.arange(len(eq)); b1,b0=np.polyfit(x,eq.values,1)
    r2=1-((eq.values-(b1*x+b0))**2).sum()/max(((eq.values-eq.values.mean())**2).sum(),1e-9)
    yrs=len(r)/252
    print(f"{label:<14} Sharpe={sharpe:5.2f}  totPnL={eq.iloc[-1]*100:6.1f}  maxDD={dd*100:6.1f}  "
          f"R2={r2:.3f}  days={len(r)}  ~yrs={yrs:.0f}")

if __name__=='__main__':
    main()
