"""
Arm A v2 — Selectivity Test (doc 30 pre-registration).
Adversarial surrogate-relative test: does NG calendar selectivity survive falsification?
Pre-registration frozen in docs/research/30_ng_selectivity_prereg.md BEFORE this script ran.

Run: backend/.venv/bin/python scripts/run_selectivity_test.py
"""
from __future__ import annotations
import sys, os, json
import numpy as np
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from app.services.analytics_arm_a import load_leg
from app.services.analytics_arm_a_v2 import spread_from_series

# ══════════════════════════════════════════════════════════════════════════════
# PRE-REGISTERED CONSTANTS (mirror doc 30; do not modify after first run)
# ══════════════════════════════════════════════════════════════════════════════
THETAS      = [1.0, 1.5, 2.0, 2.5]
PRIMARY_TH  = 1.0
LB          = 60          # z-score rolling lookback (bars)
MH          = 40          # max hold (bars)
PC          = 0.003       # primary cost (round-trip)
ALL_COSTS   = [0.0015, 0.003, 0.0045]
NS          = 500         # surrogates per type
SEED        = 20260604
OU_PHI      = 0.94771     # exp(-ln2/12.9)
DATE_TRIM   = "2006-07-28"
TRAIN_END   = "2017-12-31"
OOS_START   = "2018-01-01"
NG_PATH     = "data/raw/ng12_spread.csv"

# ══════════════════════════════════════════════════════════════════════════════
# FADE LOGIC
# ══════════════════════════════════════════════════════════════════════════════

def run_fade(s: np.ndarray, theta: float, cost: float,
             lookback: int = LB, max_hold: int = MH) -> list[dict]:
    """
    Causal selective fade at threshold theta. Exit: z crosses 0 (same rolling window) or max_hold.
    Surrogate and real paths receive bit-identical logic — selection-on-deviation artifact cancels.
    """
    s = np.asarray(s, float)
    n = len(s)
    trades: list[dict] = []
    pos = 0; epx = 0.0; bh = 0

    for t in range(lookback, n):
        win = s[t - lookback : t]
        mu = win.mean()
        sd = win.std() + 1e-9
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
                "hit": float("nan"), "avg_hold": float("nan"), "sharpe": float("nan"),
                "max_loss": float("nan"), "top3_pct": float("nan")}
    g  = np.array([t["gross"] for t in trades])
    nn = np.array([t["net"]   for t in trades])
    h  = np.array([t["hold"]  for t in trades])
    sd_nn = float(np.std(nn, ddof=1)) + 1e-9
    sharpe = float(np.mean(nn) / sd_nn * len(nn) ** 0.5)   # per-trade Sharpe

    sorted_g = np.sort(g)[::-1]
    total_abs = np.sum(np.abs(g)) + 1e-9
    top3_pct = float(sorted_g[:3].sum() / total_abs) if len(g) >= 3 else float("nan")

    return {
        "n":         int(len(trades)),
        "gross":     float(np.mean(g)),
        "net":       float(np.mean(nn)),
        "hit":       float(np.mean(nn > 0)),
        "avg_hold":  float(np.mean(h)),
        "sharpe":    float(sharpe),
        "max_loss":  float(np.min(nn)),
        "top3_pct":  float(top3_pct),
    }


# ══════════════════════════════════════════════════════════════════════════════
# SURROGATE GENERATION
# ══════════════════════════════════════════════════════════════════════════════

def fit_incr_params(incr: np.ndarray) -> dict:
    """Fit model parameters from real increments."""
    mu  = float(np.mean(incr))
    sig = float(np.std(incr, ddof=1))

    # GARCH(1,1): moment-match alpha+beta from autocorr of squared increments
    sq  = incr ** 2
    ab  = float(np.clip(np.corrcoef(sq[1:], sq[:-1])[0, 1], 0.0, 0.97)) \
          if len(sq) > 20 else 0.0
    ab  = float(np.nan_to_num(ab, nan=0.0))
    alpha = ab * 0.15
    beta  = ab - alpha
    omega = max(sig ** 2 * (1.0 - alpha - beta), 1e-12)

    return {"mu": mu, "sig": sig, "garch": (omega, alpha, beta)}


def sim_rw(params: dict, n: int, rng: np.random.Generator) -> np.ndarray:
    increments = rng.normal(params["mu"], params["sig"], n - 1)
    return np.concatenate([[0.0], np.cumsum(increments)])


def sim_garch(params: dict, n: int, rng: np.random.Generator) -> np.ndarray:
    omega, alpha, beta = params["garch"]
    mu = params["mu"]; h = params["sig"] ** 2
    out = np.empty(n - 1)
    for t in range(n - 1):
        e = rng.normal() * h ** 0.5
        out[t] = mu + e
        h = max(omega + alpha * e ** 2 + beta * h, 1e-12)
    return np.concatenate([[0.0], np.cumsum(out)])


def sim_ou(phi: float, params: dict, n: int, rng: np.random.Generator) -> np.ndarray:
    """AR(1) OU with sigma calibrated to match real increment std."""
    # var(delta) = 2*sigma_ou^2*(1-phi)/(1+phi)  => sigma_ou = sig*sqrt((1+phi)/2)
    sigma_ou = params["sig"] * ((1.0 + phi) / 2.0) ** 0.5
    path = np.empty(n); path[0] = 0.0
    for t in range(1, n):
        path[t] = phi * path[t - 1] + sigma_ou * rng.normal()
    return path


def sim_splice(params: dict, n: int, rng: np.random.Generator,
               cadence: int = 21, frac: float = 0.25) -> np.ndarray:
    """RW + periodic partial-reversal jump at cadence-bar seams (back-adjustment artifact null)."""
    s = np.empty(n); s[0] = 0.0
    for t in range(1, n):
        s[t] = s[t - 1] + rng.normal(params["mu"], params["sig"])
        if t % cadence == 0:
            drift = s[t] - s[max(0, t - cadence)]
            s[t] -= frac * drift
    return s


def surrogate_ensemble(s_real: np.ndarray, params: dict, rng: np.random.Generator) -> dict:
    """Run all surrogate types (N=NS paths each). Return gross distributions keyed by type and theta."""
    n = len(s_real)
    results: dict = {st: {th: [] for th in THETAS} for st in ["rw", "garch", "ou", "splice"]}

    generators = {
        "rw":     lambda: sim_rw(params, n, rng),
        "garch":  lambda: sim_garch(params, n, rng),
        "ou":     lambda: sim_ou(OU_PHI, params, n, rng),
        "splice": lambda: sim_splice(params, n, rng),
    }

    for _ in range(NS):
        for stype, gen in generators.items():
            path = gen()
            for th in THETAS:
                trs = run_fade(path, th, PC)
                g   = float(np.mean([t["gross"] for t in trs])) if trs else float("nan")
                results[stype][th].append(g)

    return results


# ══════════════════════════════════════════════════════════════════════════════
# P-VALUE
# ══════════════════════════════════════════════════════════════════════════════

def pval(real: float, dist: list) -> float:
    d = np.array([x for x in dist if np.isfinite(x)])
    if d.size == 0 or not np.isfinite(real):
        return float("nan")
    return float((1.0 + np.sum(d >= real)) / (d.size + 1.0))


def pctiles(dist: list) -> dict:
    d = np.array([x for x in dist if np.isfinite(x)])
    if d.size == 0:
        return {}
    ps = [5, 25, 50, 75, 95]
    return {f"p{p}": float(np.percentile(d, p)) for p in ps}


# ══════════════════════════════════════════════════════════════════════════════
# JACKKNIFE
# ══════════════════════════════════════════════════════════════════════════════

def jackknife(trades_by_theta: dict) -> dict:
    jk: dict = {}
    for th in THETAS:
        trs = trades_by_theta[th]
        if len(trs) < 3:
            jk[str(th)] = {"n": len(trs), "gross": float("nan"), "gross_drop_pct": float("nan")}
            continue
        max_i = int(np.argmax([abs(t["gross"]) for t in trs]))
        reduced = [t for i, t in enumerate(trs) if i != max_i]
        s_full = stats(trs)["gross"]
        s_red  = stats(reduced)["gross"]
        drop = abs(s_full - s_red) / (abs(s_full) + 1e-9)
        jk[str(th)] = {**stats(reduced), "dropped_gross": float(trs[max_i]["gross"]),
                       "gross_drop_pct": float(drop)}
    return jk


# ══════════════════════════════════════════════════════════════════════════════
# VERDICT
# ══════════════════════════════════════════════════════════════════════════════

def determine_verdict(pv_full: dict, st_full: dict, jk: dict, st_oos: dict) -> tuple[str, str]:
    """Frozen verdict logic from doc 30 §4. Returns (verdict_code, rationale)."""
    p_rw_primary   = pv_full.get(str(PRIMARY_TH), {}).get("rw", float("nan"))
    net_primary    = st_full.get(str(PRIMARY_TH), {}).get("net", float("nan"))
    gross_primary  = st_full.get(str(PRIMARY_TH), {}).get("gross", float("nan"))

    jk_drop     = jk.get(str(PRIMARY_TH), {}).get("gross_drop_pct", float("nan"))
    oos_gross   = st_oos.get(str(PRIMARY_TH), {}).get("gross", float("nan"))

    # Stability checks
    jk_unstable  = np.isfinite(jk_drop) and jk_drop > 0.50
    oos_sign_flip = np.isfinite(oos_gross) and np.isfinite(gross_primary) and (
        (gross_primary > 0 and oos_gross < 0) or (gross_primary < 0 and oos_gross > 0)
    )

    if not np.isfinite(p_rw_primary) or p_rw_primary >= 0.05:
        return ("A_FALSE_RESCUE",
                f"p_rw(θ=1.0)={p_rw_primary:.3f} ≥ 0.05: no surrogate-relative significance at primary threshold. "
                "Selectivity gradient is indistinguishable from the selection-on-deviation artifact.")

    # p_rw_primary < 0.05 from here
    if not np.isfinite(net_primary) or net_primary <= 0.0:
        return ("B_GENUINE_SUBCOST",
                f"p_rw(θ=1.0)={p_rw_primary:.3f} < 0.05 (genuine vs RW) but "
                f"net={net_primary:.4f} ≤ 0 after cost={PC}: real above artifact but below cost floor.")

    # p < 0.05 and net > 0
    if jk_unstable or oos_sign_flip:
        reason = []
        if jk_unstable: reason.append(f"jackknife collapses gross by {jk_drop:.0%}")
        if oos_sign_flip: reason.append(f"OOS gross sign-flips ({oos_gross:.4f})")
        return ("D_INCONCLUSIVE", "Apparent primary significance but unstable: " + "; ".join(reason))

    return ("C_GENUINE_ECONOMIC",
            f"p_rw(θ=1.0)={p_rw_primary:.3f}, net={net_primary:.4f} > 0, "
            "stable to jackknife and OOS. Selectivity is genuine and cost-clearing.")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    np.seterr(all="ignore")
    print("=" * 100)
    print("ARM A v2 — SELECTIVITY TEST (doc 30 pre-registration)")
    print("=" * 100)

    # ── 1. Load data ─────────────────────────────────────────────────────────
    ng  = spread_from_series("NG", load_leg(NG_PATH), date_min=DATE_TRIM, jump_k=float("inf"))
    s   = ng.s_close
    idx = ng.index
    print(f"\nData: {len(s)} bars  {idx[0].date()} → {idx[-1].date()}")

    # Fit model parameters on FULL series (causal — only used to parameterise surrogates)
    incr    = np.diff(s[np.isfinite(s)])
    params  = fit_incr_params(incr)
    print(f"Fitted: mu_incr={params['mu']:.5f}  sig_incr={params['sig']:.4f}")
    print(f"GARCH: omega={params['garch'][0]:.6f}  alpha={params['garch'][1]:.4f}  beta={params['garch'][2]:.4f}")
    print(f"OU phi (pre-reg): {OU_PHI:.5f}  half-life: {np.log(2)/(-np.log(OU_PHI)):.1f} bars")

    # ── 2. Full-sample real results ──────────────────────────────────────────
    trades_full = {th: run_fade(s, th, PC) for th in THETAS}
    st_full     = {str(th): stats(trades_full[th]) for th in THETAS}

    # ── 3. Train / OOS split ─────────────────────────────────────────────────
    train_mask  = idx <= pd.Timestamp(TRAIN_END, tz="UTC")
    oos_mask    = idx >= pd.Timestamp(OOS_START, tz="UTC")
    s_train     = s[train_mask]
    s_oos       = s[oos_mask]

    trades_train = {th: run_fade(s_train, th, PC) for th in THETAS}
    trades_oos   = {th: run_fade(s_oos,   th, PC) for th in THETAS}
    st_train     = {str(th): stats(trades_train[th]) for th in THETAS}
    st_oos       = {str(th): stats(trades_oos[th])   for th in THETAS}

    # ── 4. Episode jackknife ─────────────────────────────────────────────────
    jk = jackknife(trades_full)

    # ── 5. Cost grid (full sample) ───────────────────────────────────────────
    st_costs: dict = {}
    for c in ALL_COSTS:
        trades_c = {th: run_fade(s, th, c) for th in THETAS}
        st_costs[str(c)] = {str(th): stats(trades_c[th]) for th in THETAS}

    # ── 6. Surrogate ensemble ────────────────────────────────────────────────
    print(f"\nGenerating {NS} surrogate paths per type (rw, garch, ou, splice) …")
    rng  = np.random.default_rng(SEED)
    surr = surrogate_ensemble(s, params, rng)
    print("Done.")

    # ── 7. P-values and percentiles ──────────────────────────────────────────
    pv_full: dict = {}
    pct_full: dict = {}
    for th in THETAS:
        real_gross = st_full[str(th)].get("gross", float("nan"))
        pv_full[str(th)] = {
            stype: pval(real_gross, surr[stype][th])
            for stype in ["rw", "garch", "ou", "splice"]
        }
        pct_full[str(th)] = {
            stype: pctiles(surr[stype][th])
            for stype in ["rw", "garch", "ou", "splice"]
        }

    # ── 8. Verdict ───────────────────────────────────────────────────────────
    verdict, rationale = determine_verdict(pv_full, st_full, jk, st_oos)

    # ── 9. Assemble output ───────────────────────────────────────────────────
    def _safe(x):
        if isinstance(x, float) and not np.isfinite(x): return None
        if isinstance(x, (np.floating, np.integer)): return float(x)
        return x

    out = {
        "VERDICT": verdict,
        "RATIONALE": rationale,
        "primary_theta": PRIMARY_TH,
        "primary_cost": PC,
        "primary_p_rw": _safe(pv_full.get(str(PRIMARY_TH), {}).get("rw", float("nan"))),
        "primary_gross": _safe(st_full.get(str(PRIMARY_TH), {}).get("gross", float("nan"))),
        "primary_net": _safe(st_full.get(str(PRIMARY_TH), {}).get("net", float("nan"))),
        "n_bars": int(len(s)),
        "date_range": [str(idx[0].date()), str(idx[-1].date())],
        "model_params": {"mu_incr": params["mu"], "sig_incr": params["sig"],
                         "ou_phi": OU_PHI, "garch_params": list(params["garch"])},
        "stats_full":  st_full,
        "stats_train": st_train,
        "stats_oos":   st_oos,
        "jackknife":   jk,
        "stats_costs": st_costs,
        "pvalues":     pv_full,
        "surrogate_pctiles": pct_full,
    }

    out_path = "data/processed/ng_selectivity_results.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=_safe)
    print(f"\nWrote {out_path}")

    # ── 10. Print report ─────────────────────────────────────────────────────
    print("\n" + "─" * 100)
    print("FULL RESULTS GRID (full sample, cost=0.003)")
    print("─" * 100)
    hdr = f"{'θ':>5}  {'n':>5}  {'gross':>9}  {'net':>9}  {'hit':>6}  "
    hdr += f"{'hold':>6}  {'top3%':>7}  {'p_rw':>7}  {'p_garch':>8}  {'p_ou':>7}  {'p_splice':>9}"
    print(hdr)
    for th in THETAS:
        s_ = st_full[str(th)]
        pv = pv_full[str(th)]
        mark_rw = "*" if (np.isfinite(pv["rw"]) and pv["rw"] < 0.05) else " "
        print(
            f"{th:>5.1f}  {s_['n']:>5}  {s_['gross']:>+9.4f}  {s_['net']:>+9.4f}  "
            f"{s_['hit']:>6.2f}  {s_['avg_hold']:>6.1f}  {s_['top3_pct']:>7.2f}  "
            f"{pv['rw']:>6.3f}{mark_rw}  {pv['garch']:>8.3f}  {pv['ou']:>7.3f}  {pv['splice']:>9.3f}"
        )

    print("\nSURROGATE PERCENTILE TABLE (RW null, gross distribution per θ)")
    print(f"{'θ':>5}  {'p5':>8}  {'p25':>8}  {'p50':>8}  {'p75':>8}  {'p95':>8}  {'real':>9}")
    for th in THETAS:
        pc_ = pct_full[str(th)]["rw"]
        real_g = st_full[str(th)].get("gross", float("nan"))
        print(f"{th:>5.1f}  {pc_.get('p5',float('nan')):>8.4f}  {pc_.get('p25',float('nan')):>8.4f}  "
              f"{pc_.get('p50',float('nan')):>8.4f}  {pc_.get('p75',float('nan')):>8.4f}  "
              f"{pc_.get('p95',float('nan')):>8.4f}  {real_g:>+9.4f}")

    print("\nJACKKNIFE (drop largest single trade)")
    print(f"{'θ':>5}  {'full gross':>11}  {'jk gross':>10}  {'drop%':>7}  {'gross_drop':>11}")
    for th in THETAS:
        jk_ = jk[str(th)]
        full_g = st_full[str(th)].get("gross", float("nan"))
        print(f"{th:>5.1f}  {full_g:>+11.4f}  {jk_.get('gross',float('nan')):>+10.4f}  "
              f"{jk_.get('gross_drop_pct',float('nan'))*100:>6.1f}%  "
              f"{jk_.get('dropped_gross',float('nan')):>+11.4f}")

    print("\nOOS SPLIT (post-2018)")
    print(f"{'θ':>5}  {'full_gross':>11}  {'oos_gross':>10}  {'oos_net':>9}  {'oos_n':>7}")
    for th in THETAS:
        sf = st_full[str(th)]; so = st_oos[str(th)]
        print(f"{th:>5.1f}  {sf.get('gross',float('nan')):>+11.4f}  "
              f"{so.get('gross',float('nan')):>+10.4f}  "
              f"{so.get('net',float('nan')):>+9.4f}  {so.get('n',0):>7}")

    print("\nCOST GRID (gross only shown; primary θ=1.0)")
    print(f"{'cost':>8}  " + "  ".join(f"θ={th}" for th in THETAS))
    for c in ALL_COSTS:
        row = "  ".join(f"{st_costs[str(c)][str(th)].get('gross',float('nan')):>+9.4f}" for th in THETAS)
        print(f"{c:>8.4f}  {row}")

    print("\n" + "═" * 100)
    print(f"VERDICT: {verdict}")
    print(f"RATIONALE: {rationale}")
    print("═" * 100)
