"""
Arm A v2 — Cycle 1b runner. Executes doc 22 EXACTLY (rolling-local trader-persistence of NG calendar MR).
Primary statistic: pooled mean-z of VR(20) vs within-window RW band. Construction-controlled corroboration:
self-built Brent calendar. Plus splice-RW diagnostic, half-life, causal trade proxy, calm/shock diagnostic.

Run: backend/.venv/bin/python scripts/run_arm_a_v2_rolling.py
"""
from __future__ import annotations
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
import numpy as np, pandas as pd
from app.services.analytics_arm_a import Spread, load_leg, construct_spread, level_vr, surrogate_vr_ensemble, VR_Q_GRID
from app.services.analytics_arm_a_v2 import spread_from_series, SEED

NG_TRIM = "2006-07-28"; RAW = os.path.expanduser("~/Downloads/mean-reversion-data")
RW_N = 200; HL_BAND = (3.0, 40.0); COST = 0.003; ENTRY_Z = 1.0; STOP = 20; LOOKBACK = 60

# ---- per-window z ----
def window_z(s_close: np.ndarray) -> dict:
    n = len(s_close)
    sp = Spread(name="w", s_close=np.asarray(s_close, float), s_open=np.asarray(s_close, float).copy(),
                beta=np.ones(n), roll_transition=np.zeros(n, bool), flat_bar=np.zeros(n, bool),
                index=pd.date_range("2007-01-02", periods=n, freq="B", tz="UTC"), meta={})
    inv = sp.roll_transition | ~np.isfinite(sp.beta)
    vr = level_vr(sp.s_close, inv, VR_Q_GRID)
    vr20 = vr[20]["vr"]
    ens = surrogate_vr_ensemble(sp, "rw", qs=VR_Q_GRID, n_draws=RW_N, seed=SEED)[20]
    ens = ens[np.isfinite(ens)]
    mu, sd = float(np.mean(ens)), float(np.std(ens) + 1e-9)
    rwmed = float(np.median(ens))
    return {"vr20": vr20, "vr_curve": {q: vr[q]["vr"] for q in VR_Q_GRID}, "z": (vr20 - mu) / sd,
            "below_rwmed": bool(vr20 < rwmed), "n": int(n)}

def pooled(windows: list[dict]) -> dict:
    zs = [w["z"] for w in windows if np.isfinite(w["z"])]
    below = sum(w["below_rwmed"] for w in windows)
    return {"mean_z": float(np.mean(zs)), "n_windows": len(zs), "below_rwmed_count": int(below),
            "z_trajectory": [round(w["z"], 3) for w in windows], "vr20_trajectory": [round(w["vr20"], 3) for w in windows]}

def half_life(s: np.ndarray) -> float:
    s = np.asarray(s, float); x0, x1 = s[:-1], s[1:]
    X = np.column_stack([np.ones_like(x0), x0]); coef, *_ = np.linalg.lstsq(X, x1, rcond=None)
    phi = float(coef[1])
    return float(np.log(0.5) / np.log(phi)) if 0 < phi < 1 else float("inf")

# ---- causal z-entry trade proxy ----
def trade_proxy(s: np.ndarray, mask=None) -> dict:
    s = np.asarray(s, float); n = len(s)
    pnls = []; in_pos = 0; entry_px = 0.0; bars_held = 0
    for t in range(LOOKBACK, n):
        if mask is not None and not mask[t]:
            if in_pos: pnls.append(in_pos * (entry_px - s[t]) - COST); in_pos = 0
            continue
        win = s[t - LOOKBACK:t]; mu, sd = win.mean(), win.std() + 1e-9
        z = (s[t] - mu) / sd
        if in_pos == 0:
            if z >= ENTRY_Z: in_pos = +1; entry_px = s[t]; bars_held = 0   # short the spread (fade up)
            elif z <= -ENTRY_Z: in_pos = -1; entry_px = s[t]; bars_held = 0  # long the spread (fade down)
        else:
            bars_held += 1
            zc = (s[t] - mu) / sd
            cross0 = (in_pos == +1 and zc <= 0) or (in_pos == -1 and zc >= 0)
            if cross0 or bars_held >= STOP:
                pnls.append(in_pos * (entry_px - s[t]) - COST); in_pos = 0
    pnls = np.array(pnls)
    if len(pnls) == 0: return {"n_trades": 0, "avg_net_pnl": float("nan"), "hit_rate": float("nan")}
    return {"n_trades": int(len(pnls)), "avg_net_pnl": float(pnls.mean()),
            "avg_gross_pnl": float(pnls.mean() + COST), "hit_rate": float(np.mean(pnls > 0)),
            "total_net_pnl": float(pnls.sum())}

def splice_pooled_z(template_lengths, frac, seed=SEED):
    """Pooled mean-z of a splice-injected RW with the SAME window lengths as NG yearly (back-adjustment ref)."""
    rng = np.random.default_rng(seed); R = 21; ws = []
    for L in template_lengths:
        d = rng.normal(0, 0.05, L - 1)
        for t in range(R, L - 1, R): d[t] = -frac * np.sum(d[t - R:t])
        s = np.concatenate([[0.0], np.cumsum(d)])
        ws.append(window_z(s))
    return pooled(ws)["mean_z"]

# ---- shock spans (sub-year intervals) ----
SHOCKS = [("S1", "2008-01-01", "2009-06-30"), ("S2", "2014-07-01", "2016-02-29"),
          ("S3", "2020-01-01", "2020-12-31"), ("S4", "2021-09-01", "2022-12-31")]
def shock_mask(index: pd.DatetimeIndex) -> np.ndarray:
    m = np.zeros(len(index), bool)
    for _, a, b in SHOCKS:
        m |= (index >= pd.Timestamp(a, tz="UTC")) & (index <= pd.Timestamp(b, tz="UTC"))
    return m

if __name__ == "__main__":
    np.seterr(all="ignore")
    out = {}
    # ===== NG =====
    ng = spread_from_series("NG", load_leg("data/raw/ng12_spread.csv"), date_min=NG_TRIM, jump_k=float("inf"))
    idx, s = ng.index, ng.s_close
    yr = idx.year.to_numpy()
    # A — yearly 2007..2025
    yearly = []
    yrs = list(range(2007, 2026))
    for Y in yrs:
        seg = s[yr == Y]
        yearly.append({"year": Y, **window_z(seg), "hl": half_life(seg)})
    A = pooled(yearly)
    # B — disjoint 2-yr blocks
    blocks = [(2007,2008),(2009,2010),(2011,2012),(2013,2014),(2015,2016),(2017,2018),(2019,2020),(2021,2022),(2023,2024),(2025,2026)]
    twoyr = [window_z(s[(yr>=a)&(yr<=b)]) for a,b in blocks]
    B = pooled(twoyr)
    # C — pre/post 2020 (post = 2020..2025, 6 yrs)
    pre = pooled([w for w in yearly if w["year"] <= 2019])
    post = pooled([w for w in yearly if 2020 <= w["year"] <= 2025])
    out["NG"] = {"yearly_A": A, "twoyr_B": B, "pre2020": pre, "post2020": post,
                 "yearly_detail": [{"year": w["year"], "vr20": round(w["vr20"],3), "z": round(w["z"],3),
                                    "below_rwmed": w["below_rwmed"], "hl": round(w["hl"],1), "n": w["n"]} for w in yearly],
                 "global_half_life": round(half_life(s), 1)}
    # splice diagnostic (same yearly window lengths)
    Ls = [w["n"] for w in yearly]
    out["splice_diagnostic"] = {"frac_0.25": round(splice_pooled_z(Ls, 0.25), 3),
                                "frac_0.5": round(splice_pooled_z(Ls, 0.5), 3)}
    # ===== Brent construction-controlled (self-built from raw legs) =====
    try:
        b1 = load_leg(f"{RAW}/ICEEUR_DLY_BRN1!, 60 (1).csv"); b2 = load_leg(f"{RAW}/ICEEUR_DLY_BRN2!, 60.csv")
        bsp = construct_spread("Brent_cal", b1, b2, beta_mode="one", continuous_a=True, continuous_b=True)
        bs = bsp.s_close; nB = len(bs); nblk = 8; L = nB // nblk
        bwins = [window_z(bs[i*L:(i+1)*L]) for i in range(nblk)]
        out["Brent_control"] = {"pooled": pooled(bwins), "n_total": nB, "global_half_life": round(half_life(bs), 1)}
    except Exception as e:
        out["Brent_control"] = {"ERROR": repr(e)}
    # ===== trade proxy (NG, full + calm/shock) =====
    sm = shock_mask(idx); calm = ~sm
    out["trade_proxy"] = {"all": trade_proxy(s), "calm": trade_proxy(s, calm), "shock": trade_proxy(s, sm),
                          "years_per_sample": round(len(s)/252, 1)}
    # ===== calm/shock pooled-z diagnostic (yearly) =====
    shock_years = {2008,2009,2014,2015,2016,2020,2021,2022}
    calm_z = pooled([w for w in yearly if w["year"] not in shock_years])
    shock_z = pooled([w for w in yearly if w["year"] in shock_years])
    out["calm_shock_diagnostic"] = {"calm_mean_z": calm_z["mean_z"], "shock_mean_z": shock_z["mean_z"],
                                    "calm_n": calm_z["n_windows"], "shock_n": shock_z["n_windows"]}

    # ===== VERDICT (doc 22 §4) =====
    mz = A["mean_z"]; brent_mz = out["Brent_control"].get("pooled", {}).get("mean_z", None)
    post_mz = post["mean_z"]; gl_hl = out["NG"]["global_half_life"]
    persist = mz < -0.32 and B["mean_z"] < -0.32 and (brent_mz is not None and brent_mz < -0.32)
    recency = post_mz < -0.32
    back_adj_suspect = mz < -0.80 and (brent_mz is None or brent_mz > -0.40)
    hl_ok = HL_BAND[0] <= gl_hl <= HL_BAND[1]
    tp = out["trade_proxy"]["all"]; tp_pos = np.isfinite(tp["avg_net_pnl"]) and tp["avg_net_pnl"] > 0
    if back_adj_suspect: verdict = "BACK-ADJUSTMENT-SUSPECT"
    elif not (persist and recency): verdict = "NOT-PERSISTENT"
    elif hl_ok and tp_pos: verdict = "PERSISTENT-DEPLOYABLE"
    else: verdict = "PERSISTENT-BUT-UNECONOMIC"
    out["VERDICT"] = {"verdict": verdict, "ng_mean_z": round(mz,3), "twoyr_mean_z": round(B["mean_z"],3),
                      "brent_mean_z": (round(brent_mz,3) if brent_mz is not None else None),
                      "post2020_mean_z": round(post_mz,3), "global_half_life": gl_hl, "hl_in_band": hl_ok,
                      "trade_proxy_net_positive": bool(tp_pos), "back_adj_suspect": bool(back_adj_suspect)}

    with open("data/processed/arm_a_v2_rolling_results.json", "w") as f:
        json.dump(out, f, indent=2, default=lambda x: None if (isinstance(x,float) and not np.isfinite(x)) else (float(x) if isinstance(x,(np.floating,np.integer)) else x))

    # ---- print ----
    print("="*100); print("ARM A v2 CYCLE-1b — NG CALENDAR ROLLING-LOCAL TRADER-PERSISTENCE"); print("="*100)
    print(f"\nFROZEN templates: RW null mean-z≈0 [−0.32,+0.41] | genuine MR≈−0.33 | OU.97≈−0.52 | back-adj(splice)≈−0.99")
    print(f"\nNG yearly (A, PRIMARY): pooled mean-z = {mz:+.3f}  (below RW band −0.32? {mz<-0.32})  below-RWmed {A['below_rwmed_count']}/19")
    print(f"NG 2-yr (B):            pooled mean-z = {B['mean_z']:+.3f}  below-RWmed {B['below_rwmed_count']}/10")
    print(f"NG pre-2020:  mean-z = {pre['mean_z']:+.3f} ({pre['n_windows']}w)   post-2020: mean-z = {post_mz:+.3f} ({post['n_windows']}w)")
    print(f"Brent control (self-built, no back-adj): mean-z = {brent_mz}  (must also persist for STABLE)")
    print(f"splice-RW diagnostic: frac0.25={out['splice_diagnostic']['frac_0.25']}  frac0.5={out['splice_diagnostic']['frac_0.5']}  (back-adj reference)")
    print(f"calm/shock diagnostic: calm mean-z={calm_z['mean_z']:+.3f}  shock mean-z={shock_z['mean_z']:+.3f}")
    print(f"global half-life = {gl_hl} bars (band {HL_BAND})")
    print(f"trade proxy ALL: n={tp['n_trades']} avg_net={tp['avg_net_pnl']:.4f} gross={tp.get('avg_gross_pnl',float('nan')):.4f} hit={tp.get('hit_rate',float('nan')):.2f} total={tp.get('total_net_pnl',float('nan')):.3f}")
    print(f"   calm: n={out['trade_proxy']['calm']['n_trades']} net={out['trade_proxy']['calm']['avg_net_pnl']:.4f} | shock: n={out['trade_proxy']['shock']['n_trades']} net={out['trade_proxy']['shock']['avg_net_pnl']:.4f}")
    print(f"\nyearly z trajectory: " + " ".join(f"{w['year']}:{w['z']:+.2f}{'*' if w['below_rwmed'] else ''}" for w in yearly))
    print(f"yearly half-lives:   " + " ".join(f"{w['year']}:{w['hl'] if np.isfinite(w['hl']) else 'inf'}" for w in yearly))
    print(f"\n>>> VERDICT: {verdict}")
    print(f"    persist={persist} recency={recency} hl_ok={hl_ok} trade_pos={tp_pos} back_adj_suspect={back_adj_suspect}")
    print("\nwrote data/processed/arm_a_v2_rolling_results.json")
