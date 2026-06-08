#!/usr/bin/env python3
"""
OU-gated spread mean-reversion — the method distilled from deep-research (2026-06-09).
Replaces "stack indicators and hope" with the verified practitioner pipeline:

  1. SPREAD  X (economic weights where they exist -> NO rolling-beta artifact; else frozen-train beta).
  2. OU GATE  estimate mean-reversion speed on a rolling window: regress dX on X_lag -> b<0,
              half-life HL = -ln2/b. Trade ONLY when b<0 and HL in [hl_lo, hl_hi].
              When HL blows out / b>=0 -> FLATTEN + no new entries (this IS the OOS-break kill).
  3. SIGNAL  z = (X - mean(X,n)) / std(X,n)  on PAST bars only (causal).
  4. ENTRY   |z| >= z_entry (gate ON, flat).
  5. EXIT    |z| <= z_exit (near the mean — the verified win-rate lever), OR held >= time_stop,
              OR |z| >= z_stop (disaster), OR gate turns OFF.
  6. Report per-trade win rate, daily-PnL Sharpe, maxDD, equity R^2 (smoothness), IS vs OOS,
     and the exit-near-mean A/B (z_exit=0.3 vs sign-flip).

Causal by construction: every stat uses shift(1)+rolling; position set at t-1 earns dX at t.
Data: /Users/priyanshusaraf/Downloads/commodities-data/daily  (back-adjusted continuous M1/M2 legs).
"""
import os, glob, math, sys
import numpy as np, pandas as pd

DATA = "/Users/priyanshusaraf/Downloads/commodities-data/daily"

P = dict(
    z_n=40, z_entry=2.0, z_exit=0.3, z_stop=4.0,
    hl_win=120, hl_lo=2, hl_hi=40, time_mult=3.0,
    start="2006-01-01", cost=0.0,            # cost in spread-vol units per turn (set >0 to stress)
    is_frac=0.6,
)
for a in sys.argv[1:]:
    if "=" in a:
        k, v = a.split("=")
        if k in P:
            P[k] = type(P[k])(v) if not isinstance(P[k], str) else v

def load(sym):
    """Load one leg by ticker (e.g. 'ZS1'), return close Series indexed by date."""
    hit = glob.glob(f"{DATA}/*_{sym}!*.csv")
    if not hit:
        return None
    df = pd.read_csv(hit[0])
    df.columns = [c.strip().lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.dropna(subset=["date", "close"]).set_index("date")["close"].sort_index()
    return df

def half_life(x):
    """OU speed on a window: dX = a + b*X_lag; HL=-ln2/b (b<0 reverts). Returns (b, HL)."""
    x = np.asarray(x, float)
    lag = x[:-1]; d = np.diff(x)
    if len(d) < 20 or lag.std() == 0:
        return np.nan, np.nan
    b = np.polyfit(lag, d, 1)[0]
    hl = -math.log(2) / b if b < 0 else np.nan
    return b, hl

def build_spread(name):
    """Return (X series, hedge-mode str). Economic spreads -> fixed weights, no beta artifact."""
    if name == "crush":                       # soybean board GPM ($/bu): ZM*0.022 + ZL*0.11 - ZS*0.01
        zm, zl, zs = load("ZM1"), load("ZL1"), load("ZS1")
        df = pd.concat([zm, zl, zs], axis=1, keys=["zm", "zl", "zs"]).dropna()
        X = df.zm * 0.022 + df.zl * 0.11 - df.zs * 0.01
        return X, "economic"
    if name == "rbcrack":                      # RBOB crack ($/bbl): RB*42 - WTI
        rb, wti = load("RB1"), load("WBS1")
        df = pd.concat([rb, wti], axis=1, keys=["rb", "wti"]).dropna()
        X = df.rb * 42.0 - df.wti
        return X, "economic"
    if name == "brmiwti":                      # Brent - WTI ($/bbl)
        brn, wti = load("BRN1"), load("WBS1")
        df = pd.concat([brn, wti], axis=1, keys=["brn", "wti"]).dropna()
        X = df.brn - df.wti
        return X, "economic"
    if name == "ngcal":                        # NG calendar M1-M2 (seasonal)
        a, b = load("NG1"), load("NG2")
        df = pd.concat([a, b], axis=1, keys=["a", "b"]).dropna()
        X = df.a - df.b
        return X, "economic"
    if name == "rbcal":                        # RBOB calendar M1-M2
        a, b = load("RB1"), load("RB2")
        df = pd.concat([a, b], axis=1, keys=["a", "b"]).dropna()
        X = df.a - df.b
        return X, "economic"
    # beta-estimated log pairs (frozen train beta in run())
    pairs = {"goldsilver": ("GC1", "SI1"), "silvercopper": ("SI1", "HG1"),
             "goldplat": ("GC1", "PL1"), "brentgasoil": ("BRN1", "ULS1")}
    a, b = pairs[name]
    sa, sb = load(a), load(b)
    df = pd.concat([np.log(sa), np.log(sb)], axis=1, keys=["a", "b"]).dropna()
    return df, "beta"   # returns frame; beta applied per-window in run()

def run(name, p, exit_mode="mean"):
    """exit_mode: 'mean' -> close at |z|<=z_exit; 'flip' -> hold to opposite-sign z_entry."""
    obj, mode = build_spread(name)
    if mode == "beta":
        la, lb = obj["a"].values, obj["b"].values
        idx = obj.index
    else:
        X = obj[obj.index >= p["start"]] if isinstance(obj, pd.Series) else obj
        idx = X.index
    # build spread vector
    if mode == "economic":
        Xv = X.values
    else:
        # frozen-train beta, refit every 250 on trailing 750 (causal), spread = la - (a+beta*lb)
        n = len(la); Xv = np.full(n, np.nan)
        tl, step = 750, 250; t0 = tl
        while t0 < n:
            tr = slice(t0 - tl, t0)
            A = np.vstack([np.ones(tl), lb[tr]]).T
            alpha, beta = np.linalg.lstsq(A, la[tr], rcond=None)[0]
            hi = min(n, t0 + step)
            Xv[t0:hi] = la[t0:hi] - (alpha + beta * lb[t0:hi])
            t0 += step
        mask = ~np.isnan(Xv)
        Xv, idx = Xv[mask], idx[mask]
        cut = np.searchsorted(idx, np.datetime64(p["start"]))
        Xv, idx = Xv[cut:], idx[cut:]

    n = len(Xv)
    s = pd.Series(Xv)
    m = s.shift(1).rolling(p["z_n"]).mean()
    sd = s.shift(1).rolling(p["z_n"]).std()
    z = ((s - m) / sd).values
    dX = np.diff(Xv, prepend=Xv[0])
    # spread daily vol for vol-targeted book PnL + per-trade normalization
    vol = pd.Series(dX).ewm(span=63, min_periods=20).std().values

    pos = np.zeros(n); cur = 0; held = 0; entry_z = 0.0; entry_i = 0
    trades = []                                   # (pnl_volunits, bars, side)
    pnl = np.zeros(n)
    Wlo, Whi = p["hl_win"], 0
    for i in range(p["hl_win"] + p["z_n"], n):
        # rolling OU gate on past window
        b, hl = half_life(Xv[i - p["hl_win"]:i])
        gate = (b is not np.nan) and (not np.isnan(hl)) and (p["hl_lo"] <= hl <= p["hl_hi"])
        zz = z[i]
        tstop = max(5, int(p["time_mult"] * hl)) if not np.isnan(hl) else 60
        if cur != 0:
            held += 1
            exit_now = False
            if np.isnan(zz) or abs(zz) >= p["z_stop"] or held >= tstop or not gate:
                exit_now = True
            elif exit_mode == "mean" and abs(zz) <= p["z_exit"]:
                exit_now = True
            elif exit_mode == "flip" and ((cur > 0 and zz >= p["z_entry"]) or (cur < 0 and zz <= -p["z_entry"])):
                exit_now = True
            if exit_now:
                seg = (Xv[i] - Xv[entry_i]) * cur
                vnorm = vol[entry_i] if vol[entry_i] > 0 else np.nan
                trades.append((seg / vnorm if vnorm == vnorm else 0.0, held, cur))
                cur = 0; held = 0
        if cur == 0 and gate and not np.isnan(zz):
            if zz <= -p["z_entry"]:
                cur = 1; entry_i = i; held = 0          # long spread (expect rise)
            elif zz >= p["z_entry"]:
                cur = -1; entry_i = i; held = 0
        pos[i] = cur
    # daily vol-targeted PnL (position at i-1 earns dX at i, scaled to target risk)
    tgt = 0.01
    for i in range(1, n):
        sz = (tgt / vol[i - 1]) if (vol[i - 1] == vol[i - 1] and vol[i - 1] > 0) else 0.0
        turn = abs(pos[i] - pos[i - 1]) * sz
        pnl[i] = pos[i - 1] * sz * dX[i] - turn * p["cost"]
    ret = pd.Series(pnl, index=idx)
    return ret, trades

def stats(ret, trades, label):
    r = ret[ret != 0].dropna() if len(ret) else ret
    if len(trades) == 0:
        print(f"{label:<26} no trades"); return
    wins = [t for t in trades if t[0] > 0]
    wr = len(wins) / len(trades)
    avg_w = np.mean([t[0] for t in wins]) if wins else 0
    losses = [t[0] for t in trades if t[0] <= 0]
    avg_l = np.mean(losses) if losses else 0
    eq = ret.cumsum()
    sh = ret.mean() / ret.std() * math.sqrt(252) if ret.std() > 0 else 0
    dd = (eq - eq.cummax()).min()
    x = np.arange(len(eq)); b1, b0 = np.polyfit(x, eq.values, 1)
    r2 = 1 - ((eq.values - (b1 * x + b0)) ** 2).sum() / max(((eq.values - eq.values.mean()) ** 2).sum(), 1e-9)
    avg_bars = np.mean([t[1] for t in trades])
    print(f"{label:<26} trades={len(trades):4d}  win%={wr*100:4.0f}  avgW={avg_w:+.2f} avgL={avg_l:+.2f}  "
          f"Sharpe={sh:5.2f}  maxDD={dd*100:6.1f}  eqR2={r2:.3f}  ~bars/trade={avg_bars:.0f}")

SPREADS = ["crush", "rbcrack", "brmiwti", "ngcal", "rbcal",
           "goldsilver", "silvercopper", "goldplat", "brentgasoil"]

def main():
    sel = [a for a in sys.argv[1:] if "=" not in a] or SPREADS
    print(f"OU-gated spread MR | z_entry={P['z_entry']} z_exit={P['z_exit']} hl=[{P['hl_lo']},{P['hl_hi']}] "
          f"win={P['hl_win']} start={P['start']} cost={P['cost']}\n")
    book = {}
    for nm in sel:
        try:
            ret_m, tr_m = run(nm, P, "mean")
            ret_f, tr_f = run(nm, P, "flip")
        except Exception as e:
            print(f"{nm}: ERROR {e}"); continue
        print(f"== {nm} ==")
        stats(ret_m, tr_m, "  exit-near-mean")
        stats(ret_f, tr_f, "  exit-on-signflip")
        # IS/OOS on the exit-near-mean variant
        cut = int(len(ret_m) * P["is_frac"])
        tr_sorted = tr_m  # trades already chronological
        # split trades by index position approx via time fraction of dataset
        stats(ret_m.iloc[:cut], [t for t in tr_m[:int(len(tr_m)*P['is_frac'])]], "  IS(60%) near-mean")
        stats(ret_m.iloc[cut:], [t for t in tr_m[int(len(tr_m)*P['is_frac']):]], "  OOS(40%) near-mean")
        book[nm] = ret_m
        print()
    # equal-risk BOOK across spreads (the smoothness engine)
    B = pd.DataFrame(book)
    port = B.mean(axis=1).where(B.notna().sum(axis=1) >= 3).dropna()
    if len(port) > 100:
        print("== BOOK (equal-risk mean across spreads, >=3 active) ==")
        stats(port, [(v, 1, 1) for v in port[port != 0]], "  BOOK full")
        cut = int(len(port) * P["is_frac"])
        stats(port.iloc[:cut], [(v, 1, 1) for v in port.iloc[:cut][port.iloc[:cut] != 0]], "  BOOK IS(60%)")
        stats(port.iloc[cut:], [(v, 1, 1) for v in port.iloc[cut:][port.iloc[cut:] != 0]], "  BOOK OOS(40%)")

if __name__ == "__main__":
    main()
