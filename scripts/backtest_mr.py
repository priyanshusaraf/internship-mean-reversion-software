#!/usr/bin/env python3
"""
Single-instrument mean-reversion backtest — causal, R-based, instrument-agnostic.
Validates the strategy BEFORE porting to Pine. Trades the chart's own OHLC.

Strategy (matches the Pine we will ship):
  core    : RSI-2 extreme (loose, so it actually fires)  [+ optional z-score / %b]
  regime  : trade only in a RANGING tape  -> ADX<thr  OR  price in/near Ichimoku Kumo
  veto    : don't fade a CONFIRMED counter-trend (ADX>=20 AND Supertrend opposes)
  exits   : mean-touch (SMA) | ATR target | ATR stop | Supertrend flip | time stop
  sizing  : constant risk 1R per trade, R = atr_stop_mult * ATR  -> P&L measured in R
            (instrument-agnostic; works for outrights AND spread series alike)

Causality: every indicator uses only past/current bars; decisions act on NEXT bar's
open; intrabar stops/targets checked against subsequent highs/lows. No lookahead.
"""
import sys, glob, os, math
import numpy as np
import pandas as pd

# ----------------------------- data loading --------------------------------
def load_csv(path):
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    t = df['time']
    if pd.api.types.is_numeric_dtype(t):
        df['date'] = pd.to_datetime(t, unit='s')
    else:
        df['date'] = pd.to_datetime(t, format='mixed', utc=True, errors='coerce').dt.tz_localize(None)
    df = df[['date','open','high','low','close']].dropna()
    return df.sort_values('date').reset_index(drop=True)

def build_spread(path_a, path_b):
    """Calendar/cross spread OHLC = legA - legB, aligned on date.
       Correct intrabar bounds for a difference: H=Ha-Lb, L=La-Hb."""
    a = load_csv(path_a).set_index('date'); b = load_csv(path_b).set_index('date')
    j = a.join(b, lsuffix='_a', rsuffix='_b', how='inner').dropna()
    out = pd.DataFrame({'date': j.index,
        'open':  j['open_a']  - j['open_b'],
        'high':  j['high_a']  - j['low_b'],
        'low':   j['low_a']   - j['high_b'],
        'close': j['close_a'] - j['close_b']})
    return out.reset_index(drop=True)

# ----------------------------- indicators (causal) -------------------------
def rma(s, n):
    return s.ewm(alpha=1/n, adjust=False).mean()

def rsi(close, n=2):
    d = close.diff()
    up = d.clip(lower=0); dn = (-d).clip(lower=0)
    rs = rma(up, n) / rma(dn, n).replace(0, np.nan)
    return (100 - 100/(1+rs)).fillna(50)

def true_range(h, l, c):
    pc = c.shift(1)
    return pd.concat([h-l, (h-pc).abs(), (l-pc).abs()], axis=1).max(axis=1)

def atr(h, l, c, n=14):
    return rma(true_range(h, l, c), n)

def adx(h, l, c, n=14):
    up = h.diff(); dn = -l.diff()
    plus = ((up > dn) & (up > 0)) * up
    minus = ((dn > up) & (dn > 0)) * dn
    tr = true_range(h, l, c)
    atr_ = rma(tr, n).replace(0, np.nan)
    pdi = 100 * rma(plus, n) / atr_
    mdi = 100 * rma(minus, n) / atr_
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi).replace(0, np.nan)
    return rma(dx.fillna(0), n)

def supertrend(h, l, c, factor=3.0, n=10):
    a = atr(h, l, c, n)
    hl2 = (h + l) / 2
    upper = hl2 + factor * a
    lower = hl2 - factor * a
    n_ = len(c)
    fu = np.full(n_, np.nan); fl = np.full(n_, np.nan)
    dir_ = np.ones(n_)  # +1 down, -1 up  (Pine v6 convention: -1 up, +1 down)
    st = np.full(n_, np.nan)
    cc = c.values; uu = upper.values; ll = lower.values
    for i in range(n_):
        if i == 0 or np.isnan(uu[i]):
            fu[i] = uu[i]; fl[i] = ll[i]; dir_[i] = 1; st[i] = uu[i]; continue
        fu[i] = uu[i] if (uu[i] < fu[i-1] or cc[i-1] > fu[i-1]) else fu[i-1]
        fl[i] = ll[i] if (ll[i] > fl[i-1] or cc[i-1] < fl[i-1]) else fl[i-1]
        if st[i-1] == fu[i-1]:
            dir_[i] = -1 if cc[i] > fu[i] else 1
        else:
            dir_[i] = 1 if cc[i] < fl[i] else -1
        st[i] = fl[i] if dir_[i] == -1 else fu[i]
    return pd.Series(dir_, index=c.index)  # -1 up, +1 down

def ichimoku_cloud(h, l, c, t=9, k=26, s=52, disp=26):
    don = lambda n: (h.rolling(n).max() + l.rolling(n).min()) / 2
    tenkan = don(t); kijun = don(k)
    spanA = (tenkan + kijun) / 2
    spanB = don(s)
    # cloud sitting OVER the current bar = spans computed disp bars ago (causal)
    top = pd.concat([spanA.shift(disp), spanB.shift(disp)], axis=1).max(axis=1)
    bot = pd.concat([spanA.shift(disp), spanB.shift(disp)], axis=1).min(axis=1)
    return top, bot

# ----------------------------- backtest ------------------------------------
def backtest(df, p):
    h, l, c = df['high'], df['low'], df['close']
    r = rsi(c, p['rsi_n'])
    a = atr(h, l, c, p['atr_n'])
    adx_ = adx(h, l, c, p['adx_n'])
    stdir = supertrend(h, l, c, p['st_factor'], p['st_n'])
    ctop, cbot = ichimoku_cloud(h, l, c)
    sma_exit = c.rolling(p['exit_ma']).mean()
    zmean = c.shift(1).rolling(p['z_n']).mean()
    zstd = c.shift(1).rolling(p['z_n']).std()
    z = (c - zmean) / zstd.replace(0, np.nan)

    near = p['kumo_tol'] * a
    price_in_near_cloud = (c >= cbot - near) & (c <= ctop + near)
    ranging = (adx_ < p['adx_thr']) | price_in_near_cloud
    st_up = stdir < 0; st_down = stdir > 0
    # variance-ratio MR-regime gate (causal): VR(q)<1 => sub-diffusive => mean-reverting
    dc = c.diff()
    var1 = dc.rolling(p['vr_len']).var()
    varq = (c - c.shift(p['vr_q'])).rolling(p['vr_len']).var()
    vr = varq / (p['vr_q'] * var1.replace(0, np.nan))
    mr_regime = (vr < p['vr_thr']) if p['use_vr'] else pd.Series(True, index=c.index)
    # long-horizon trend veto: don't fade when far from the SLOW mean in trend direction
    slow = c.rolling(p['slow_n']).mean()
    slow_sd = c.rolling(p['slow_n']).std()
    far_below = (c - slow) < -p['slow_k'] * slow_sd   # spread in a sustained down-drift
    far_above = (c - slow) >  p['slow_k'] * slow_sd

    if p['core'] == 'z':
        rsi_long = z < -p['z_entry']; rsi_short = z > p['z_entry']
    else:
        rsi_long = r < p['rsi_long']; rsi_short = r > p['rsi_short']
        if p['use_z']:
            rsi_long &= z < -p['z_entry']; rsi_short &= z > p['z_entry']

    # counter-trend veto only in a confirmed trend
    trap_long = (adx_ >= 20) & st_down
    trap_short = (adx_ >= 20) & st_up

    warm = max(p['z_n'], 52 + 26, p['adx_n'] * 3, p['atr_n'] * 3, p['slow_n'] if p['use_slow'] else 0)
    n = len(df)
    long_sig = rsi_long & ranging & ~trap_long & mr_regime
    short_sig = rsi_short & ranging & ~trap_short & mr_regime
    if p['use_slow']:                      # veto fading into a sustained slow-mean drift
        long_sig = long_sig & ~far_below
        short_sig = short_sig & ~far_above

    C, O = c.values, df['open'].values
    A = a.values; SMA = sma_exit.values; STd = stdir.values; Z = z.values; ZS = zstd.values
    pos = 0; entry = np.nan; Rrisk = np.nan; bars_in = 0; entry_atr = np.nan; entry_zs = np.nan
    trades = []
    rt_cost = p['cost_atr']  # round-trip cost in ATR units at entry

    for i in range(warm, n - 1):
        if pos == 0:
            go_long = bool(long_sig.iloc[i]); go_short = bool(short_sig.iloc[i])
            if (go_long or go_short) and not np.isnan(A[i]) and A[i] > 0:
                side = 1 if go_long else -1
                entry = O[i+1]  # fill next open
                entry_zs = ZS[i]
                # risk unit R: z-core => entry-relative price stop (caps drift tail); rsi-core => ATR stop
                if p['core'] == 'z' and not np.isnan(entry_zs) and entry_zs > 0:
                    Rrisk = p['stop_sig'] * entry_zs
                else:
                    Rrisk = p['atr_stop'] * A[i]
                pos = side; bars_in = 0; entry_atr = A[i]
            continue
        # in position: ALL exits checked on CLOSE (avoids synthetic-spread H/L noise)
        bars_in += 1; side = pos; exit_px = None; reason = None
        if p['core'] == 'z' and not np.isnan(Z[i]):
            # entry-relative hard stop = stop_sig * sigma(at entry) in PRICE terms.
            # This caps the structural-drift tail (mean chases price, z never hits disaster).
            if side == 1:
                if (entry - C[i]) >= p['stop_sig'] * entry_zs: exit_px, reason = C[i], 'stop'
                elif Z[i] >= -p['z_exit']:                      exit_px, reason = C[i], 'mean'
            else:
                if (C[i] - entry) >= p['stop_sig'] * entry_zs: exit_px, reason = C[i], 'stop'
                elif Z[i] <= p['z_exit']:                       exit_px, reason = C[i], 'mean'
        else:
            stop = entry - side * Rrisk; tgt = entry + side * p['atr_tgt'] * entry_atr
            if side == 1:
                if C[i] <= stop: exit_px, reason = C[i], 'stop'
                elif C[i] >= tgt: exit_px, reason = C[i], 'target'
                elif C[i] >= SMA[i]: exit_px, reason = C[i], 'mean'
            else:
                if C[i] >= stop: exit_px, reason = C[i], 'stop'
                elif C[i] <= tgt: exit_px, reason = C[i], 'target'
                elif C[i] <= SMA[i]: exit_px, reason = C[i], 'mean'
        if exit_px is None:
            st_flip = (side == 1 and STd[i] > 0) or (side == -1 and STd[i] < 0)
            if p['use_stflip'] and st_flip: exit_px, reason = C[i], 'stflip'
            elif bars_in >= p['time_stop']: exit_px, reason = C[i], 'time'
        if exit_px is not None:
            pnl_R = side * (exit_px - entry) / Rrisk - rt_cost * entry_atr / Rrisk
            trades.append({'pnl_R': pnl_R, 'reason': reason, 'bars': bars_in,
                           'date': df['date'].iloc[i]})
            pos = 0
    return pd.DataFrame(trades)

# ----------------------------- metrics -------------------------------------
def metrics(tr, df):
    if len(tr) == 0:
        return None
    years = (df['date'].iloc[-1] - df['date'].iloc[0]).days / 365.25
    R = tr['pnl_R'].values
    eq = np.cumsum(R)
    peak = np.maximum.accumulate(eq)
    dd = eq - peak
    maxdd = -dd.min() if len(dd) else 0
    wins = R[R > 0]; losses = R[R < 0]
    pf = wins.sum() / -losses.sum() if losses.sum() != 0 else np.inf
    # smoothness: R^2 of equity vs linear trend
    x = np.arange(len(eq))
    if len(eq) > 2 and eq.std() > 0:
        b1, b0 = np.polyfit(x, eq, 1)
        ss_res = ((eq - (b1 * x + b0)) ** 2).sum()
        ss_tot = ((eq - eq.mean()) ** 2).sum()
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    else:
        r2 = 0
    sharpe = R.mean() / R.std() * math.sqrt(len(R) / years) if R.std() > 0 and years > 0 else 0
    return {'trades': len(tr), 'tr_yr': len(tr) / years if years else 0,
            'win%': 100 * len(wins) / len(tr), 'totR': eq[-1], 'avgR': R.mean(),
            'PF': pf, 'maxDD_R': maxdd, 'totR/DD': eq[-1] / maxdd if maxdd > 0 else np.inf,
            'sharpe': sharpe, 'R2': r2}

# ----------------------------- main ----------------------------------------
DEFAULT = dict(core='rsi', rsi_n=2, rsi_long=15, rsi_short=85, use_z=False,
               z_n=20, z_entry=1.0, z_exit=0.0, z_disaster=4.0, stop_sig=2.0,
               atr_n=14, adx_n=14, adx_thr=25, st_factor=3.0, st_n=10, use_stflip=True,
               kumo_tol=0.25, exit_ma=5, atr_stop=2.5, atr_tgt=2.0, time_stop=6,
               cost_atr=0.05, use_vr=False, vr_len=60, vr_q=5, vr_thr=1.0,
               use_slow=False, slow_n=100, slow_k=2.5)

def build_ratio(path_a, path_b):
    """Log-ratio spread = ln(A) - ln(B), aligned on date (scale-free, for cointegrated pairs)."""
    a = load_csv(path_a).set_index('date'); b = load_csv(path_b).set_index('date')
    j = a.join(b, lsuffix='_a', rsuffix='_b', how='inner').dropna()
    j = j[(j[['open_a','high_a','low_a','close_a','open_b','high_b','low_b','close_b']] > 0).all(axis=1)]
    la, lb = np.log, np.log
    out = pd.DataFrame({'date': j.index,
        'open':  la(j['open_a'])  - lb(j['open_b']),
        'high':  la(j['high_a'])  - lb(j['low_b']),
        'low':   la(j['low_a'])   - lb(j['high_b']),
        'close': la(j['close_a']) - lb(j['close_b'])})
    return out.reset_index(drop=True)

def ratio_pairs():
    """Economically cointegrated cross-commodity pairs (the genuine MR objects)."""
    base = 'data/raw/more-mean-reversion-data'
    P = lambda r: f'{base}/{r}1!, 1D.csv'
    pairs = [('LE-GF','CME_DL_LE','CME_DL_GF'), ('GC-SI','COMEX_DL_GC','COMEX_DL_SI'),
             ('PL-GC','NYMEX_DL_PL','COMEX_DL_GC'), ('HO-CL','NYMEX_DL_HO','NYMEX_DL_CL'),
             ('RB-CL','NYMEX_DL_RB','NYMEX_DL_CL'), ('ZW-ZC','CBOT_DL_ZW','CBOT_DL_ZC'),
             ('KE-ZW','CBOT_DL_KE','CBOT_DL_ZW'), ('ZM-ZW','CBOT_DL_ZM','CBOT_DL_ZW'),
             ('CC-KC','ICEUS_DLY_CC','ICEUS_DLY_KC'), ('CT-SB','ICEUS_DLY_CT','ICEUS_DLY_SB'),
             ('HG-PL','COMEX_DL_HG','NYMEX_DL_PL'), ('SI-HG','COMEX_DL_SI','COMEX_DL_HG'),
             ('HO-RB','NYMEX_DL_HO','NYMEX_DL_RB'), ('PL-SI','NYMEX_DL_PL','COMEX_DL_SI'),
             ('BRN-CL','ICEEUR_DLY_BRN','NYMEX_DL_CL'), ('KC-SB','ICEUS_DLY_KC','ICEUS_DLY_SB')]
    only = os.environ.get('PAIRS', '')
    only = set(only.split(',')) if only else None
    out = {}
    for name, a, b in pairs:
        if only and name not in only: continue
        pa, pb = P(a), P(b)
        if os.path.exists(pa) and os.path.exists(pb):
            try:
                df = build_ratio(pa, pb)
                if len(df) >= 300: out[name] = df
            except Exception:
                pass
    return out

def calendar_spreads():
    """Construct M1-M2 calendar spreads (the mean-reverting objects) from legs."""
    base = 'data/raw/more-mean-reversion-data'
    roots = ['ICEEUR_DLY_BRN','NYMEX_DL_CL','NYMEX_DL_HO','NYMEX_DL_RB','COMEX_DL_GC',
             'COMEX_DL_SI','COMEX_DL_HG','NYMEX_DL_PL','ICEUS_DLY_KC','ICEUS_DLY_CC',
             'ICEUS_DLY_CT','ICEUS_DLY_SB','CME_DL_LE','CME_DL_HE','CBOT_DL_ZC','CBOT_DL_ZW']
    out = {}
    for r in roots:
        a = f'{base}/{r}1!, 1D.csv'; b = f'{base}/{r}2!, 1D.csv'
        if os.path.exists(a) and os.path.exists(b):
            try:
                df = build_spread(a, b)
                if len(df) >= 300: out[r.split("_")[-1] + ' M1-M2'] = df
            except Exception:
                pass
    # pre-built cross/calendar spread CSVs
    for name, pth in [('NG M1-M2(file)','data/raw/ng12_spread.csv'),
                      ('CL-BRN','data/raw/cl_brn_spread_60.csv'),
                      ('COFFEE-COCOA','data/raw/coffee_cocoa_spread_1d.csv'),
                      ('RB M2-M3','data/raw/rb23_spread.csv')]:
        if os.path.exists(pth):
            try:
                df = load_csv(pth)
                if len(df) >= 300: out[name] = df
            except Exception:
                pass
    return out

if __name__ == '__main__':
    p = dict(DEFAULT)
    # allow CLI param overrides: key=val
    for a in sys.argv[1:]:
        if '=' in a:
            k, v = a.split('=')
            if k in p:
                cur = p[k]
                if isinstance(cur, bool): p[k] = v.lower() in ('1','true')
                elif isinstance(cur, int): p[k] = int(float(v))
                elif isinstance(cur, float): p[k] = float(v)
                else: p[k] = v
    universe = os.environ.get('UNIVERSE', 'ratio')
    insts = ratio_pairs() if universe == 'ratio' else calendar_spreads()
    hdr = ['instrument','trades','tr/yr','win%','totR','PF','maxDD_R','totR/DD','R2','OOS_R','OOS_PF']
    print(f"{hdr[0]:<22}" + "".join(f"{h:>9}" for h in hdr[1:]))
    print('-'*108)
    prof = 0; prof_oos = 0; all_tr = []
    for name, df in insts.items():
        tr = backtest(df, p)
        if len(tr) == 0:
            print(f"{name:<22}{'0':>9}"); continue
        m = metrics(tr, df)
        # OOS = trades in last 30% of the date span
        span0, span1 = df['date'].iloc[0], df['date'].iloc[-1]
        cut = span0 + (span1 - span0) * 0.7
        oos = tr[tr['date'] >= cut]
        oR = oos['pnl_R'].sum()
        ow = oos[oos['pnl_R'] > 0]['pnl_R'].sum(); ol = -oos[oos['pnl_R'] < 0]['pnl_R'].sum()
        oPF = ow/ol if ol > 0 else (np.inf if ow > 0 else 0)
        all_tr.append(tr.assign(inst=name))
        good = m['totR'] > 0 and m['PF'] > 1
        if good: prof += 1
        if oR > 0 and oPF > 1: prof_oos += 1
        mark = '*' if (good and oR > 0 and oPF > 1) else ''
        print(f"{name:<22}{m['trades']:>9}{round(m['tr_yr'],1):>9}{round(m['win%'],1):>9}"
              f"{round(m['totR'],1):>9}{round(m['PF'],2):>9}{round(m['maxDD_R'],1):>9}"
              f"{round(m['totR/DD'],2):>9}{round(m['R2'],2):>9}{round(oR,1):>9}{round(oPF,2):>8}{mark}")
    print('-'*108)
    # PORTFOLIO: pool all pair trades by date, equal risk per trade -> combined equity
    if all_tr:
        port = pd.concat(all_tr).sort_values('date').reset_index(drop=True)
        R = port['pnl_R'].values; eq = np.cumsum(R)
        peak = np.maximum.accumulate(eq); dd = -(eq-peak).min()
        x = np.arange(len(eq)); b1,b0 = np.polyfit(x,eq,1)
        r2 = 1 - ((eq-(b1*x+b0))**2).sum()/max(((eq-eq.mean())**2).sum(),1e-9)
        yrs = (port['date'].iloc[-1]-port['date'].iloc[0]).days/365.25
        shp = R.mean()/R.std()*math.sqrt(len(R)/yrs) if R.std()>0 else 0
        print(f"PORTFOLIO ({len(all_tr)} pairs): trades={len(port)} totR={eq[-1]:.1f} "
              f"maxDD={dd:.1f} totR/DD={eq[-1]/dd:.2f} Sharpe={shp:.2f} R2={r2:.3f} win%={100*(R>0).mean():.1f}")
    print(f"profitable IS: {prof}/{len(insts)}   profitable BOTH IS&OOS(*): {prof_oos}/{len(insts)}   "
          f"[core={p['core']} z_entry={p['z_entry']} z_n={p['z_n']} stop_sig={p['stop_sig']} time={p['time_stop']}]")
