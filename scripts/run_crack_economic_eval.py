"""
Economic Evaluation — Confirmed Crack-β Habitats.

Runs the selectivity/fade analysis (same framework as run_selectivity_test.py / doc 31)
on three confirmed OOS habitats:
  HO-CL (doc 39, F5 β=1.054)
  RB-CL (doc 40, F6 β=1.0)
  LE-GF (doc 42, F5 β=0.565)

QUESTION: does naive z-entry reversion clear transaction costs?

Cost assumptions (conservative, round-trip per spread unit):
  Energy crack ($/bbl): LOW=0.20  MED=0.50  HIGH=1.00
  Livestock (¢/lb):     LOW=0.10  MED=0.20  HIGH=0.35

Same fade logic as doc 31:
  Entry: z < -θ (long spread) or z > +θ (short spread), rolling z over LB bars
  Exit:  z crosses 0 OR max_hold bars
  Verdict: A_FALSE_RESCUE / B_GENUINE_SUBCOST / C_GENUINE_ECONOMIC / D_INCONCLUSIVE
"""
from __future__ import annotations
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import numpy as np
import pandas as pd
from app.services.analytics_arm_a import Spread
from app.services.analytics_arm_a_v2 import deseasonalize_causal, increment_jump_mask, SEED
from app.services.analytics_arm_a_v2_beta import (
    economic_anchor_beta, presample_ols_beta, beta_update_variance_fraction,
)

# ── Frozen analysis constants (mirroring doc 31 framework) ────────────────────
THETAS     = [1.0, 1.5, 2.0, 2.5]
PRIMARY_TH = 1.0
LB         = 60       # rolling z lookback (bars)
MH         = 40       # max hold (bars)
NS         = 500      # surrogate draws per type
SEED_ECON  = 20260604
JUMP_K     = 8.0
JUMP_W     = 60
OOS_SPLIT  = 0.70
PRE_FRAC   = 0.25

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw", "more-mean-reversion-data")

# Cost grids per asset class
COSTS_ENERGY    = {"low": 0.20, "med": 0.50, "high": 1.00}   # $/bbl round-trip
COSTS_LIVESTOCK = {"low": 0.10, "med": 0.20, "high": 0.35}   # ¢/lb round-trip
PRIMARY_COST_ENERGY    = COSTS_ENERGY["med"]
PRIMARY_COST_LIVESTOCK = COSTS_LIVESTOCK["med"]


# ── Data loading ──────────────────────────────────────────────────────────────

def load_u(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["ts"] = pd.to_datetime(df["time"].astype(np.int64), unit="s", utc=True)
    return df.dropna(subset=["ts"]).sort_values("ts").drop_duplicates("ts", keep="last").set_index("ts")


def build_spread_ds(fileA: str, fileB: str, scaleA: float, beta_mode: str,
                    date_min: str, date_max: str = "2026-06-03") -> tuple[np.ndarray, pd.DatetimeIndex, float]:
    """Load pair, construct deseasonalized spread, return (s_ds, idx, beta_val)."""
    A_raw = load_u(os.path.join(DATA, fileA))
    B_raw = load_u(os.path.join(DATA, fileB))
    A_raw = A_raw[(A_raw.index >= date_min) & (A_raw.index <= date_max)]
    B_raw = B_raw[(B_raw.index >= date_min) & (B_raw.index <= date_max)]
    merged = A_raw[["close"]].join(B_raw[["close"]], how="inner", lsuffix="_a", rsuffix="_b").dropna()
    idx = merged.index
    A = merged.close_a.to_numpy(float) * scaleA
    B = merged.close_b.to_numpy(float)
    n = len(idx)

    if beta_mode == "f6":
        beta = economic_anchor_beta(n)
        beta_val = 1.0
    elif beta_mode == "f5":
        beta = presample_ols_beta(A, B, pre_sample_fraction=PRE_FRAC)
        pre_n = int(n * PRE_FRAC)
        beta_val = float(np.nanmedian(beta[pre_n:]))
    else:
        raise ValueError(f"unknown beta_mode {beta_mode}")

    s_raw = np.where(np.isfinite(beta), A - beta * B, np.nan)
    s_ds = deseasonalize_causal(s_raw, idx)
    # Mask pre-sample NaN and roll transitions
    roll = increment_jump_mask(s_ds, k=JUMP_K, window=JUMP_W)
    inv = ~np.isfinite(beta) | roll
    s_ds = np.where(inv, np.nan, s_ds)
    return s_ds, idx, beta_val


# ── Fade engine (identical to doc 31) ─────────────────────────────────────────

def run_fade(s: np.ndarray, theta: float, cost: float,
             lookback: int = LB, max_hold: int = MH) -> list[dict]:
    s = np.asarray(s, float)
    n = len(s)
    trades: list[dict] = []
    pos = 0; epx = 0.0; bh = 0
    for t in range(lookback, n):
        win = s[max(0, t - lookback):t]
        win = win[np.isfinite(win)]
        if len(win) < lookback // 2:
            continue
        mu = win.mean(); sd = win.std() + 1e-9
        if not np.isfinite(s[t]):
            continue
        z = (s[t] - mu) / sd
        if pos:
            bh += 1
            cross = (pos > 0 and z <= 0.0) or (pos < 0 and z >= 0.0)
            if cross or bh >= max_hold:
                gross = pos * (epx - s[t])
                trades.append({"gross": gross, "net": gross - cost, "hold": bh})
                pos = 0; bh = 0
        if not pos:
            if z >= theta:
                pos = 1; epx = s[t]; bh = 0
            elif z <= -theta:
                pos = -1; epx = s[t]; bh = 0
    return trades


def stats(trades: list[dict]) -> dict:
    if len(trades) < 5:
        return {"n": len(trades), "gross": float("nan"), "net": float("nan"),
                "hit": float("nan"), "avg_hold": float("nan"),
                "sharpe": float("nan"), "top3_pct": float("nan")}
    g  = np.array([t["gross"] for t in trades])
    nn = np.array([t["net"]   for t in trades])
    h  = np.array([t["hold"]  for t in trades])
    sd_nn = float(np.std(nn, ddof=1)) + 1e-9
    sharpe = float(np.mean(nn) / sd_nn * len(nn) ** 0.5)
    top3_pct = float(np.sort(g)[::-1][:3].sum() / (np.sum(np.abs(g)) + 1e-9)) if len(g) >= 3 else float("nan")
    return {"n": int(len(trades)), "gross": float(np.mean(g)), "net": float(np.mean(nn)),
            "hit": float(np.mean(nn > 0)), "avg_hold": float(np.mean(h)),
            "sharpe": float(sharpe), "top3_pct": float(top3_pct)}


# ── Surrogate generation ──────────────────────────────────────────────────────

def fit_params(s: np.ndarray) -> dict:
    incr = np.diff(s[np.isfinite(s)])
    mu  = float(np.mean(incr))
    sig = float(np.std(incr, ddof=1))
    sq = incr ** 2
    ab = float(np.clip(np.corrcoef(sq[1:], sq[:-1])[0, 1], 0.0, 0.97)) if len(sq) > 20 else 0.0
    ab = float(np.nan_to_num(ab, nan=0.0))
    alpha = ab * 0.15; beta_g = ab - alpha
    omega = max(sig**2 * (1.0 - alpha - beta_g), 1e-12)
    # OU phi: calibrate from ACF(1) of the series levels
    valid = s[np.isfinite(s)]
    if len(valid) > 30:
        phi = float(np.corrcoef(valid[1:], valid[:-1])[0, 1])
        phi = float(np.clip(np.nan_to_num(phi, nan=0.95), 0.70, 0.999))
    else:
        phi = 0.95
    return {"mu": mu, "sig": sig, "phi": phi, "garch": (omega, alpha, beta_g)}


def sim_rw(p, n, rng):
    return np.concatenate([[0.0], np.cumsum(rng.normal(p["mu"], p["sig"], n-1))])

def sim_garch(p, n, rng):
    o, a, b = p["garch"]; mu = p["mu"]; h = p["sig"]**2
    out = np.empty(n-1)
    for t in range(n-1):
        e = rng.normal() * h**0.5; out[t] = mu + e
        h = max(o + a*e**2 + b*h, 1e-12)
    return np.concatenate([[0.0], np.cumsum(out)])

def sim_ou(p, n, rng):
    phi = p["phi"]; sigma_ou = p["sig"] * ((1.0 + phi)/2.0)**0.5
    path = np.empty(n); path[0] = 0.0
    for t in range(1, n):
        path[t] = phi*path[t-1] + sigma_ou*rng.normal()
    return path

def surrogate_ensemble(s: np.ndarray, p: dict, rng: np.random.Generator, primary_cost: float) -> dict:
    n_valid = np.sum(np.isfinite(s))
    results = {st: {th: [] for th in THETAS} for st in ["rw", "garch", "ou"]}
    for _ in range(NS):
        for stype, gen in [("rw", lambda: sim_rw(p, n_valid, rng)),
                            ("garch", lambda: sim_garch(p, n_valid, rng)),
                            ("ou", lambda: sim_ou(p, n_valid, rng))]:
            path = gen()
            for th in THETAS:
                trs = run_fade(path, th, primary_cost)
                results[stype][th].append(
                    float(np.mean([t["gross"] for t in trs])) if trs else float("nan"))
    return results


def pval(real: float, dist: list) -> float:
    d = np.array([x for x in dist if np.isfinite(x)])
    if d.size == 0 or not np.isfinite(real): return float("nan")
    return float((1.0 + np.sum(d >= real)) / (d.size + 1.0))


def jackknife(trades_by_theta: dict) -> dict:
    jk: dict = {}
    for th in THETAS:
        trs = trades_by_theta[th]
        if len(trs) < 3:
            jk[str(th)] = {"gross_drop_pct": float("nan")}; continue
        max_i = int(np.argmax([abs(t["gross"]) for t in trs]))
        reduced = [t for i, t in enumerate(trs) if i != max_i]
        s_full = stats(trs)["gross"]; s_red = stats(reduced)["gross"]
        drop = abs(s_full - s_red) / (abs(s_full) + 1e-9)
        jk[str(th)] = {**stats(reduced), "dropped_gross": float(trs[max_i]["gross"]),
                       "gross_drop_pct": float(drop)}
    return jk


def determine_verdict(pv_full: dict, st_full: dict, jk: dict,
                      st_oos: dict, primary_cost: float) -> tuple[str, str]:
    p_rw   = pv_full.get(str(PRIMARY_TH), {}).get("rw", float("nan"))
    net    = st_full.get(str(PRIMARY_TH), {}).get("net", float("nan"))
    gross  = st_full.get(str(PRIMARY_TH), {}).get("gross", float("nan"))
    jk_drop = jk.get(str(PRIMARY_TH), {}).get("gross_drop_pct", float("nan"))
    oos_g  = st_oos.get(str(PRIMARY_TH), {}).get("gross", float("nan"))
    jk_unstable  = np.isfinite(jk_drop) and jk_drop > 0.50
    oos_flip = np.isfinite(oos_g) and np.isfinite(gross) and (gross * oos_g < 0)
    if not np.isfinite(p_rw) or p_rw >= 0.05:
        return "A_FALSE_RESCUE", f"p_rw(θ=1.0)={p_rw:.3f} ≥ 0.05: indistinguishable from selection-on-deviation artifact"
    if not np.isfinite(net) or net <= 0.0:
        return "B_GENUINE_SUBCOST", f"p_rw={p_rw:.3f} (genuine vs RW) but net={net:.4f} ≤ 0 after cost={primary_cost}"
    if jk_unstable or oos_flip:
        reasons = []
        if jk_unstable: reasons.append(f"jackknife drop={jk_drop:.0%}")
        if oos_flip: reasons.append(f"OOS gross sign-flips ({oos_g:.4f})")
        return "D_INCONCLUSIVE", "Primary p<0.05, net>0 but unstable: " + "; ".join(reasons)
    return "C_GENUINE_ECONOMIC", f"p_rw={p_rw:.3f}, net={net:.4f} > 0, stable to jackknife+OOS"


# ── Per-pair analysis ─────────────────────────────────────────────────────────

def analyse_pair(name: str, s_ds: np.ndarray, idx: pd.DatetimeIndex,
                 primary_cost: float, cost_grid: dict) -> dict:
    n = len(s_ds)
    n_is = int(n * OOS_SPLIT)
    s_is  = s_ds[:n_is]
    s_oos = s_ds[n_is:]

    # Full, IS, OOS trade stats
    trades_full = {th: run_fade(s_ds, th, primary_cost) for th in THETAS}
    trades_oos  = {th: run_fade(s_oos, th, primary_cost) for th in THETAS}
    st_full = {str(th): stats(trades_full[th]) for th in THETAS}
    st_oos  = {str(th): stats(trades_oos[th])  for th in THETAS}

    # Jackknife
    jk = jackknife(trades_full)

    # Cost grid (full, primary theta only)
    cost_results = {}
    for clabel, c in cost_grid.items():
        trs = run_fade(s_ds, PRIMARY_TH, c)
        cost_results[clabel] = stats(trs)

    # Surrogate ensemble
    p = fit_params(s_ds)
    rng = np.random.default_rng(SEED_ECON)
    surr = surrogate_ensemble(s_ds, p, rng, primary_cost)

    # P-values
    pv_full: dict = {}
    pct_full: dict = {}
    for th in THETAS:
        real_g = st_full[str(th)].get("gross", float("nan"))
        pv_full[str(th)] = {st: pval(real_g, surr[st][th]) for st in ["rw", "garch", "ou"]}
        pct_full[str(th)] = {st: {
            f"p{p_}": float(np.percentile([x for x in surr[st][th] if np.isfinite(x)], p_))
            for p_ in [5, 25, 50, 75, 95]
        } for st in ["rw", "garch", "ou"]}

    verdict, rationale = determine_verdict(pv_full, st_full, jk, st_oos, primary_cost)

    return {
        "name": name, "n": n, "n_is": n_is, "n_oos": n - n_is,
        "oos_start": str(idx[n_is].date()),
        "primary_cost": primary_cost,
        "model_params": {"mu": round(p["mu"], 6), "sig": round(p["sig"], 4),
                         "phi": round(p["phi"], 4)},
        "verdict": verdict, "rationale": rationale,
        "stats_full": st_full, "stats_oos": st_oos,
        "jackknife": jk, "cost_grid": cost_results,
        "pvalues": pv_full, "pctiles": pct_full,
    }


# ── Report printer ─────────────────────────────────────────────────────────────

def print_report(r: dict) -> None:
    print(f"\n{'='*75}")
    print(f"PAIR: {r['name']}  N={r['n']}  OOS>={r['oos_start']}  primary_cost={r['primary_cost']}")
    print(f"  phi={r['model_params']['phi']:.4f}  sig={r['model_params']['sig']:.4f}")
    print(f"{'='*75}")
    print(f"{'θ':>5}  {'n':>5}  {'gross':>9}  {'net':>9}  {'hit%':>6}  {'hold':>5}  "
          f"{'p_rw':>7}  {'p_garch':>8}  {'p_ou':>6}  {'jk_drop':>8}")
    for th in THETAS:
        sf = r["stats_full"].get(str(th), {})
        pv = r["pvalues"].get(str(th), {})
        jk_ = r["jackknife"].get(str(th), {})
        mark = "*" if pv.get("rw", 1) < 0.05 else " "
        print(f"{th:>5.1f}  {sf.get('n',0):>5}  {sf.get('gross',float('nan')):>+9.4f}  "
              f"{sf.get('net',float('nan')):>+9.4f}  {sf.get('hit',float('nan'))*100:>5.1f}%  "
              f"{sf.get('avg_hold',float('nan')):>5.1f}  "
              f"{pv.get('rw',float('nan')):>6.3f}{mark}  {pv.get('garch',float('nan')):>8.3f}  "
              f"{pv.get('ou',float('nan')):>6.3f}  {jk_.get('gross_drop_pct',float('nan'))*100:>7.1f}%")
    print(f"\n  OOS (θ=1.0): gross={r['stats_oos'].get('1.0',{}).get('gross',float('nan')):+.4f}  "
          f"net={r['stats_oos'].get('1.0',{}).get('net',float('nan')):+.4f}  "
          f"n={r['stats_oos'].get('1.0',{}).get('n',0)}")
    print(f"\n  COST GRID (θ=1.0, full period):")
    for clabel, cs in r["cost_grid"].items():
        print(f"    {clabel}: gross={cs.get('gross',float('nan')):+.4f}  "
              f"net={cs.get('net',float('nan')):+.4f}  n={cs.get('n',0)}")
    print(f"\n  VERDICT: {r['verdict']}")
    print(f"  {r['rationale']}")


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    np.seterr(all="ignore")
    print("Economic Evaluation — Confirmed Crack-β Habitats")
    print("HO-CL (F5) · RB-CL (F6) · LE-GF (F5)")
    print(f"LB={LB}  MH={MH}  NS={NS} surrogates  OOS_SPLIT={OOS_SPLIT:.0%}\n")

    pairs = [
        {
            "name": "HO-CL (F5, β≈1.054)",
            "fileA": "NYMEX_DL_HO2!, 1D.csv",
            "fileB": "NYMEX_DL_CL2!, 1D.csv",
            "scaleA": 42.0,
            "beta_mode": "f5",
            "date_min": "1998-07-19",
            "primary_cost": PRIMARY_COST_ENERGY,
            "cost_grid": COSTS_ENERGY,
        },
        {
            "name": "RB-CL (F6, β=1.0)",
            "fileA": "NYMEX_DL_RB2!, 1D.csv",
            "fileB": "NYMEX_DL_CL2!, 1D.csv",
            "scaleA": 42.0,
            "beta_mode": "f6",
            "date_min": "1998-07-19",
            "primary_cost": PRIMARY_COST_ENERGY,
            "cost_grid": COSTS_ENERGY,
        },
        {
            "name": "LE-GF (F5, β≈0.565)",
            "fileA": "CME_DL_LE2!, 1D.csv",
            "fileB": "CME_DL_GF2!, 1D.csv",
            "scaleA": 1.0,
            "beta_mode": "f5",
            "date_min": "2002-08-14",
            "primary_cost": PRIMARY_COST_LIVESTOCK,
            "cost_grid": COSTS_LIVESTOCK,
        },
    ]

    all_results = {}
    for cfg in pairs:
        print(f"\nBuilding spread: {cfg['name']} ...")
        s_ds, idx, beta_val = build_spread_ds(
            cfg["fileA"], cfg["fileB"], cfg["scaleA"],
            cfg["beta_mode"], cfg["date_min"])
        n_valid = int(np.sum(np.isfinite(s_ds)))
        spread_std = float(np.nanstd(s_ds))
        print(f"  β={beta_val:.4f}  n_valid={n_valid}  spread_std={spread_std:.4f}  "
              f"cost/σ={cfg['primary_cost']/spread_std:.4f}")
        print(f"  Running fade + {NS} surrogates ...")
        result = analyse_pair(cfg["name"], s_ds, idx, cfg["primary_cost"], cfg["cost_grid"])
        print_report(result)
        all_results[cfg["name"]] = result

    # Summary
    print(f"\n{'='*75}")
    print("SUMMARY")
    print(f"{'Pair':30s}  {'Verdict':22s}  {'p_rw':>6}  {'gross(θ=1)':>11}  {'net(θ=1)':>10}  {'OOS_gross':>10}")
    print(f"{'-'*75}")
    for name, r in all_results.items():
        pv_rw = r["pvalues"].get("1.0", {}).get("rw", float("nan"))
        gross = r["stats_full"].get("1.0", {}).get("gross", float("nan"))
        net   = r["stats_full"].get("1.0", {}).get("net", float("nan"))
        oos_g = r["stats_oos"].get("1.0", {}).get("gross", float("nan"))
        print(f"{name:30s}  {r['verdict']:22s}  {pv_rw:>6.3f}  {gross:>+11.4f}  {net:>+10.4f}  {oos_g:>+10.4f}")

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "data", "processed", "crack_economic_eval.json")
    def _s(x):
        if isinstance(x, float) and not np.isfinite(x): return None
        if isinstance(x, (np.floating, np.integer)): return float(x)
        if isinstance(x, np.bool_): return bool(x)
        if isinstance(x, dict): return {k: _s(v) for k, v in x.items()}
        if isinstance(x, list): return [_s(i) for i in x]
        return x
    with open(out_path, "w") as f:
        json.dump(_s(all_results), f, indent=2)
    print(f"\nResults saved → {out_path}")
