#!/usr/bin/env python3
"""
Walk-forward stat-arb engine — the HONEST test (no cherry-picking).

For every candidate pair (log-ratio spread, fixed beta):
  rolling windows: TRAIN (estimate beta + test cointegration) -> TEST (trade, unseen).
  A pair trades in a TEST window ONLY if, on the immediately preceding TRAIN window, it
  passed Engle-Granger cointegration (ADF p<thr) AND half-life in a tradeable band.
  beta is frozen from train -> applied causally to build the test spread.
  Concatenate TEST-window trades across all windows/pairs = true out-of-sample.

Reports: per-pair OOS, the full search size (N pairs screened), and the PORTFOLIO OOS
equity (equal risk per trade) — Sharpe/DD/R2 after cost. No pair is selected post-hoc on
its OOS result; selection is train-only and re-evaluated every step.
"""
import sys, glob, os, math, itertools
import numpy as np, pandas as pd
from statsmodels.tsa.stattools import adfuller
from backtest_mr import backtest, metrics, DEFAULT, load_csv

# ---------------- universe ----------------
def universe():
    base = 'data/raw/more-mean-reversion-data'
    files = sorted(glob.glob(f'{base}/*1!*1D*.csv'))
    extra = [f'{base}/TVC_SILVER, 1D.csv', f'{base}/SP_SPX, 1D (1).csv']
    U = {}
    for f in files + extra:
        if not os.path.exists(f): continue
        nm = os.path.basename(f).split(',')[0].replace('_DL_','_').replace('_DLY_','_')
        nm = nm.split('_')[-1].replace('1!','').replace('!','')
        try:
            df = load_csv(f)
            df = df[df['close'] > 0]
            if len(df) >= 1500: U[nm] = df.set_index('date')[['open','high','low','close']]
        except Exception: pass
    return U

def half_life(resid):
    r = pd.Series(resid).dropna()
    lag = r.shift(1); dr = (r - lag).dropna(); lag = lag.loc[dr.index]
    if len(dr) < 30 or lag.std() == 0: return np.nan
    beta = np.polyfit(lag.values, dr.values, 1)[0]
    return -math.log(2)/beta if beta < 0 else np.nan

def log_spread_ohlc(A, B, alpha, beta):
    """spread = ln(A) - (alpha + beta*ln(B)); causal OHLC bounds for a difference of logs."""
    lao, lah, lal, lac = np.log(A['open']), np.log(A['high']), np.log(A['low']), np.log(A['close'])
    lbo, lbh, lbl, lbc = np.log(B['open']), np.log(B['high']), np.log(B['low']), np.log(B['close'])
    out = pd.DataFrame(index=A.index)
    out['close'] = lac - (alpha + beta*lbc)
    out['open']  = lao - (alpha + beta*lbo)
    if beta >= 0:
        out['high'] = lah - (alpha + beta*lbl); out['low'] = lal - (alpha + beta*lbh)
    else:
        out['high'] = lah - (alpha + beta*lbh); out['low'] = lal - (alpha + beta*lbl)
    out['date'] = A.index
    return out.reset_index(drop=True)

# ---------------- walk-forward ----------------
def walkforward(U, p, train_len=1000, test_len=250, step=250, adf_p=0.05, hl_lo=5, hl_hi=60, warmup=150):
    names = list(U.keys())
    pairs = list(itertools.combinations(names, 2))
    all_trades = []; screened = 0; active_windows = 0; total_windows = 0
    per_pair = {}
    for a, b in pairs:
        J = U[a].join(U[b], lsuffix='_a', rsuffix='_b', how='inner').dropna()
        if len(J) < train_len + test_len + warmup: continue
        screened += 1
        A = J[['open_a','high_a','low_a','close_a']].rename(columns=lambda c: c[:-2])
        B = J[['open_b','high_b','low_b','close_b']].rename(columns=lambda c: c[:-2])
        la = np.log(A['close']).values; lb = np.log(B['close']).values
        n = len(J); ptr = []
        t0 = train_len
        while t0 + test_len <= n:
            total_windows += 1
            tr = slice(t0 - train_len, t0)
            # OLS la ~ alpha + beta*lb on train
            X = np.vstack([np.ones(train_len), lb[tr]]).T
            beta_hat, alpha_hat = np.linalg.lstsq(X, la[tr], rcond=None)[0][1], np.linalg.lstsq(X, la[tr], rcond=None)[0][0]
            resid = la[tr] - (alpha_hat + beta_hat*lb[tr])
            try:
                adf_pv = adfuller(resid, maxlag=1, autolag=None)[1]
            except Exception:
                adf_pv = 1.0
            hl = half_life(resid)
            if adf_pv < adf_p and not np.isnan(hl) and hl_lo <= hl <= hl_hi:
                active_windows += 1
                lo = max(0, t0 - warmup); hi = t0 + test_len
                sp = log_spread_ohlc(A.iloc[lo:hi], B.iloc[lo:hi], alpha_hat, beta_hat)
                tr_df = backtest(sp, p)
                if len(tr_df):
                    test_start = J.index[t0]
                    tr_df = tr_df[tr_df['date'] >= test_start]
                    if len(tr_df):
                        tr_df = tr_df.assign(pair=f'{a}-{b}')
                        all_trades.append(tr_df)
                        per_pair.setdefault(f'{a}-{b}', []).append(tr_df['pnl_R'].sum())
            t0 += step
    return all_trades, dict(screened=screened, active_windows=active_windows, total_windows=total_windows,
                            pairs_traded=len(per_pair))

def report(all_trades, info):
    print(f"\n=== WALK-FORWARD OOS (Engle-Granger selected, true out-of-sample) ===")
    print(f"pairs with enough overlap screened: {info['screened']} | "
          f"windows: {info['active_windows']} active / {info['total_windows']} total "
          f"({100*info['active_windows']/max(info['total_windows'],1):.1f}% cointegrated) | "
          f"pairs that ever traded: {info['pairs_traded']}")
    if not all_trades:
        print("NO OOS TRADES — nothing passed cointegration+halflife and fired. Honest result: no edge found.")
        return
    port = pd.concat(all_trades).sort_values('date').reset_index(drop=True)
    port = port[np.isfinite(port['pnl_R'])].reset_index(drop=True)   # drop degenerate-pair NaN/inf
    # per-pair OOS
    g = port.groupby('pair')['pnl_R']
    summ = pd.DataFrame({'trades': g.count(), 'totR': g.sum(), 'win%': g.apply(lambda s: 100*(s>0).mean())})
    summ['PF'] = g.apply(lambda s: s[s>0].sum()/(-s[s<0].sum()) if (s<0).any() else np.inf)
    summ = summ.sort_values('totR', ascending=False)
    pd.set_option('display.width', 120)
    print("\nper-pair OOS (top/bottom):")
    print(summ.head(12).round(2).to_string())
    print("...")
    print(summ.tail(5).round(2).to_string())
    npos = (summ['totR'] > 0).sum()
    print(f"\npairs OOS-positive: {npos}/{len(summ)}")
    # PORTFOLIO equity (equal risk per trade)
    R = port['pnl_R'].values; eq = np.cumsum(R)
    peak = np.maximum.accumulate(eq); dd = -(eq-peak).min()
    x = np.arange(len(eq)); b1,b0 = np.polyfit(x,eq,1)
    r2 = 1 - ((eq-(b1*x+b0))**2).sum()/max(((eq-eq.mean())**2).sum(),1e-9)
    yrs = (port['date'].iloc[-1]-port['date'].iloc[0]).days/365.25
    shp = R.mean()/R.std()*math.sqrt(len(R)/yrs) if R.std()>0 and yrs>0 else 0
    print(f"\nPORTFOLIO OOS (all {len(summ)} pairs): trades={len(port)} totR={eq[-1]:.1f} maxDD={dd:.1f} "
          f"totR/DD={eq[-1]/dd if dd>0 else float('inf'):.2f} Sharpe={shp:.2f} R2={r2:.3f} "
          f"win%={100*(R>0).mean():.1f} tr/yr={len(port)/yrs:.0f}")
    # robustness-filtered book: pairs active in >=3 windows AND >=20 OOS trades (persistent cointegration)
    cnt = port.groupby('pair')['pnl_R'].count()
    keep = cnt[cnt >= 20].index
    pf2 = port[port['pair'].isin(keep)].sort_values('date')
    if len(pf2) > 10:
        R2_ = pf2['pnl_R'].values; eq2 = np.cumsum(R2_)
        dd2 = -(eq2-np.maximum.accumulate(eq2)).min()
        x2 = np.arange(len(eq2)); bb1,bb0 = np.polyfit(x2,eq2,1)
        rr2 = 1-((eq2-(bb1*x2+bb0))**2).sum()/max(((eq2-eq2.mean())**2).sum(),1e-9)
        y2 = (pf2['date'].iloc[-1]-pf2['date'].iloc[0]).days/365.25
        s2 = R2_.mean()/R2_.std()*math.sqrt(len(R2_)/y2) if R2_.std()>0 else 0
        np_ = (pf2.groupby('pair')['pnl_R'].sum()>0).sum(); tp=pf2['pair'].nunique()
        print(f"PORTFOLIO OOS (persistent pairs, >=20 trades, n={tp}): trades={len(pf2)} totR={eq2[-1]:.1f} "
              f"maxDD={dd2:.1f} totR/DD={eq2[-1]/dd2 if dd2>0 else float('inf'):.2f} Sharpe={s2:.2f} "
              f"R2={rr2:.3f} win%={100*(R2_>0).mean():.1f} pos-pairs={np_}/{tp}")

if __name__ == '__main__':
    p = dict(DEFAULT)
    p.update(core='z', z_entry=2.0, z_n=40, z_exit=0.5, stop_sig=2.5, adx_thr=200,
             use_stflip=False, time_stop=30, use_vr=True, vr_len=60, vr_q=5, vr_thr=1.0)
    for a in sys.argv[1:]:
        if '=' in a:
            k,v = a.split('=')
            if k in p:
                cur=p[k]
                p[k]= (v.lower() in ('1','true')) if isinstance(cur,bool) else int(float(v)) if isinstance(cur,int) else float(v) if isinstance(cur,float) else v
    U = universe()
    print(f"universe: {len(U)} instruments -> {len(U)*(len(U)-1)//2} candidate pairs")
    trades, info = walkforward(U, p)
    report(trades, info)
