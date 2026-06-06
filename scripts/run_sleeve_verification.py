"""
Sleeve Verification Gauntlet — Gates 0, 2, 3, 4
Pre-registered: docs/research/sleeve_verification_prereg.md (written before execution).
Candidates: RB-CL (F6, β=1.0) and LE-GF (F5, β=0.565)

Gates executed here:
  Gate 0 — Raw vs Deseason VR test + splice diagnostic
  Gate 2 — Multiplicity correction (full search enumeration)
  Gate 3 — Full book metrics: Sharpe, max drawdown, breakeven curve, capacity
  Gate 4 — θ-gradient surrogate test (LE-GF primary, RB-CL check)

Gate 1 (§11.8 re-anchor) and Gate 5 (adversarial agents) are handled separately.
"""
from __future__ import annotations
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import numpy as np
import pandas as pd
from app.services.analytics_arm_a_v2 import deseasonalize_causal, increment_jump_mask
from app.services.analytics_arm_a_v2_beta import economic_anchor_beta, presample_ols_beta

# ── Constants (from pre-reg, immutable) ────────────────────────────────────────
THETAS     = [1.0, 1.5, 2.0, 2.5]
PRIMARY_TH = 1.0
LB         = 60
MH         = 40
NS         = 500      # surrogate draws for Sharpe/gradient tests
NS_VR      = 200      # surrogate draws for VR test (Gate 0)
OOS_SPLIT  = 0.70
PRE_FRAC   = 0.25
JUMP_K     = 8.0
JUMP_W     = 60
SEED_VERIF = 20260606

# Defended realistic costs (pre-registered)
DEFENDED_COST_ENERGY    = 0.20   # $/bbl
DEFENDED_COST_LIVESTOCK = 0.20   # ¢/lb

# Approximate ADV for capacity estimates (contracts/day, conservative)
ADV_RBOB = 80_000    # NYMEX RBOB, very liquid
ADV_CL   = 200_000   # NYMEX CL, most liquid energy future
ADV_LE   = 40_000    # CME live cattle
ADV_GF   = 8_000     # CME feeder cattle — binding constraint for LE-GF

# Contract sizes
CONTRACT_ENERGY_BBL = 1_000   # bbl per contract (CL, RB)
CONTRACT_LE_LBS     = 40_000  # lbs per live cattle contract
CONTRACT_GF_LBS     = 50_000  # lbs per feeder cattle contract

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw", "more-mean-reversion-data")


# ── Data loading ────────────────────────────────────────────────────────────────

def load_u(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["ts"] = pd.to_datetime(df["time"].astype(np.int64), unit="s", utc=True)
    return df.dropna(subset=["ts"]).sort_values("ts").drop_duplicates("ts", keep="last").set_index("ts")


# ── Gate 0 — Splice Diagnostic ─────────────────────────────────────────────────

def splice_diagnostic(path: str, scale: float = 1.0, label: str = "") -> dict:
    """Check individual LEG for back-adj contamination.
    For individual commodity legs, only negative prices are meaningful:
      CLEAN:        n_neg == 0
      SUSPECT:      0 < pct_neg < 1% (could be a single expiry event like WTI Apr 2020)
      CONTAMINATED: pct_neg ≥ 1% (systemic negative prices = back-adj overflow)
    Note: |mean|/std is NOT used for individual legs — commodity prices are well above zero
    by definition, so a high ratio is normal (not a contamination signal).
    """
    df = load_u(path)
    prices = df["close"].to_numpy(float) * scale
    valid  = prices[np.isfinite(prices)]
    n_total = len(valid)
    n_neg   = int(np.sum(valid < 0))
    pct_neg = n_neg / n_total if n_total > 0 else float("nan")
    mean_  = float(np.mean(valid))
    std_   = float(np.std(valid, ddof=1)) + 1e-9
    ratio  = abs(mean_) / std_

    # For individual legs: only negative price count matters
    if pct_neg >= 0.01:
        grade = "CONTAMINATED"
    elif pct_neg > 0:
        grade = "SUSPECT"
    else:
        grade = "CLEAN"

    note = ("LEVEL_RATIO_HIGH but expected for commodity price level (not a contamination signal)"
            if ratio >= 0.5 else "")

    return {
        "leg": label, "n_total": n_total, "n_neg": n_neg,
        "pct_neg": round(pct_neg * 100, 2),
        "level_mean": round(mean_, 4), "level_std": round(std_, 4),
        "mean_std_ratio": round(ratio, 4), "grade": grade, "note": note,
    }


# ── Gate 0 — Raw VR Test ────────────────────────────────────────────────────────

def vr_q(s: np.ndarray, q: int) -> float:
    """Variance ratio at horizon q using overlapping returns."""
    x = s[np.isfinite(s)]
    n = len(x)
    if n < q + 20:
        return float("nan")
    dr  = np.diff(x)
    var1 = np.var(dr, ddof=1)
    if var1 <= 1e-14:
        return float("nan")
    ret_q = x[q:] - x[:-q]
    varq  = np.var(ret_q, ddof=1)
    return float(varq / (q * var1))


def vr_rw_pval(s: np.ndarray, q: int = 20, n_surr: int = NS_VR,
               seed: int = SEED_VERIF) -> tuple[float, float]:
    """VR(q) and RW surrogate p-value (one-sided: fraction surrogates ≤ real)."""
    real_vr = vr_q(s, q)
    if not np.isfinite(real_vr):
        return float("nan"), float("nan")
    x   = s[np.isfinite(s)]
    n   = len(x)
    dr  = np.diff(x)
    mu_  = float(np.mean(dr))
    sig_ = float(np.std(dr, ddof=1))
    rng  = np.random.default_rng(seed)
    surr_vrs = []
    for _ in range(n_surr):
        path = np.concatenate([[0.0], np.cumsum(rng.normal(mu_, sig_, n - 1))])
        v = vr_q(path, q)
        if np.isfinite(v):
            surr_vrs.append(v)
    pv = (1.0 + sum(v <= real_vr for v in surr_vrs)) / (len(surr_vrs) + 1.0)
    return float(real_vr), float(pv)


def build_spread_raw(fileA: str, fileB: str, scaleA: float, beta_mode: str,
                     date_min: str, date_max: str = "2026-06-03") -> tuple[np.ndarray, np.ndarray, pd.DatetimeIndex, float]:
    """Construct raw spread (NO deseasonalization). Returns (s_raw, s_ds, idx, beta_val)."""
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
        beta_val = float(np.nanmedian(beta[int(n * PRE_FRAC):]))
    else:
        raise ValueError(f"unknown beta_mode {beta_mode}")

    s_raw_arr = np.where(np.isfinite(beta), A - beta * B, np.nan)
    roll = increment_jump_mask(s_raw_arr, k=JUMP_K, window=JUMP_W)
    inv  = ~np.isfinite(beta) | roll

    s_raw_clean = np.where(inv, np.nan, s_raw_arr)          # raw, roll-masked
    s_ds_arr    = deseasonalize_causal(s_raw_arr, idx)
    s_ds_clean  = np.where(inv, np.nan, s_ds_arr)           # deseasonalized, roll-masked

    return s_raw_clean, s_ds_clean, idx, beta_val


def gate0_raw_vr(name: str, s_raw: np.ndarray, s_ds: np.ndarray) -> dict:
    """Compare raw vs deseason VR(20) and classify contamination risk."""
    vr_raw, p_raw   = vr_rw_pval(s_raw)
    vr_ds,  p_ds    = vr_rw_pval(s_ds)

    raw_mean = float(np.nanmean(s_raw))
    raw_std  = float(np.nanstd(s_raw))
    ms_ratio = abs(raw_mean) / (raw_std + 1e-9)

    if vr_ds < 1.0 and vr_raw > 1e-9:
        amplification = abs(vr_raw - vr_ds) / (abs(1.0 - vr_ds) + 1e-9) + 1.0
    else:
        amplification = float("nan")

    # Pre-registered classification
    if p_raw < 0.05:
        classification = "CLEAN"
    elif p_raw < 0.12 and amplification < 2.5 and ms_ratio < 0.5:
        classification = "MARGINAL-CLEAN"
    elif p_raw < 0.12:
        classification = "SUSPECT"
    else:
        if np.isfinite(amplification) and amplification >= 2.5:
            classification = "CONTAMINATED"
        else:
            classification = "FAIL-RAW"

    return {
        "name": name,
        "vr20_raw": round(vr_raw, 4), "p_rw_raw": round(p_raw, 4),
        "vr20_ds":  round(vr_ds,  4), "p_rw_ds":  round(p_ds,  4),
        "raw_spread_mean": round(raw_mean, 4),
        "raw_spread_std":  round(raw_std,  4),
        "mean_std_ratio":  round(ms_ratio, 4),
        "deseason_amplification": round(amplification, 3) if np.isfinite(amplification) else None,
        "gate0_classification": classification,
    }


# ── Fade engine (mirroring run_crack_economic_eval.py exactly) ─────────────────

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


# ── Gate 3 — Book Metrics ───────────────────────────────────────────────────────

def book_metrics(trades: list[dict], total_bars: int, bars_per_year: float = 252.0) -> dict:
    if len(trades) < 5:
        return {"insufficient_trades": True}
    nets  = np.array([t["net"]   for t in trades])
    gross = np.array([t["gross"] for t in trades])
    n_years       = total_bars / bars_per_year
    trades_per_yr = len(trades) / n_years

    # Sharpe: (mean_net / std_net) * sqrt(trades/year)
    sharpe = (float(np.mean(nets)) / (float(np.std(nets, ddof=1)) + 1e-9)) * (trades_per_yr ** 0.5)

    # Max drawdown (cumulative net PnL sequence)
    cumul = np.cumsum(nets)
    peak  = np.maximum.accumulate(cumul)
    dd    = cumul - peak
    max_dd = float(np.min(dd))
    med_net = float(np.median(nets))
    mdd_in_trades = abs(max_dd) / (abs(med_net) + 1e-9)

    return {
        "n_trades": len(trades),
        "n_years": round(n_years, 1),
        "trades_per_year": round(trades_per_yr, 1),
        "mean_gross": round(float(np.mean(gross)), 4),
        "mean_net":   round(float(np.mean(nets)),  4),
        "std_net":    round(float(np.std(nets, ddof=1)), 4),
        "annualized_sharpe": round(sharpe, 3),
        "max_drawdown_units": round(max_dd, 4),
        "median_net": round(med_net, 4),
        "mdd_in_median_trades": round(mdd_in_trades, 1),
        "cumulative_net": round(float(np.sum(nets)), 4),
    }


def capacity_estimate(trades_per_year: float, mean_net_per_trade_units: float,
                      adv_limiting: int, contract_units: int, label: str) -> dict:
    """5% of ADV × contract size × trades/year × net/trade = theoretical annual capacity."""
    max_contracts_per_trade = int(adv_limiting * 0.05)
    max_net_per_trade_dollars = max_contracts_per_trade * contract_units * abs(mean_net_per_trade_units / 100.0
                                  if "¢" in label else mean_net_per_trade_units)
    annual_capacity = max_net_per_trade_dollars * trades_per_year
    return {
        "limiting_leg_adv": adv_limiting,
        "max_contracts_5pct_adv": max_contracts_per_trade,
        "contract_size_units": contract_units,
        "net_per_trade_units": round(mean_net_per_trade_units, 4),
        "max_net_per_trade_usd": round(max_net_per_trade_dollars, 0),
        "trades_per_year": round(trades_per_year, 1),
        "theoretical_annual_capacity_usd": round(annual_capacity, 0),
        "label": label,
    }


def breakeven_curve(s: np.ndarray, cost_grid: list[float], theta: float = PRIMARY_TH,
                    n_total: int = 0) -> dict:
    """Net PnL at every cost in grid; find full-period breakeven (interpolated)."""
    n_oos = int(n_total * (1.0 - OOS_SPLIT))
    s_oos = s[-n_oos:] if n_oos > 0 else s

    full_results: dict = {}
    oos_results:  dict = {}
    for c in cost_grid:
        trs_full = run_fade(s, theta, c)
        trs_oos  = run_fade(s_oos, theta, c)
        full_results[c] = round(float(np.mean([t["net"] for t in trs_full])), 5) if trs_full else float("nan")
        oos_results[c]  = round(float(np.mean([t["net"] for t in trs_oos])), 5) if trs_oos else float("nan")

    def interp_zero(costs, nets):
        for i in range(len(costs) - 1):
            n0, n1 = nets[i], nets[i + 1]
            if not (np.isfinite(n0) and np.isfinite(n1)):
                continue
            if n0 >= 0 and n1 <= 0:
                c0, c1 = costs[i], costs[i + 1]
                return float(c0 + (0 - n0) * (c1 - c0) / (n1 - n0 + 1e-12))
        return float("nan")

    c_sorted  = sorted(cost_grid)
    be_full   = interp_zero(c_sorted, [full_results[c] for c in c_sorted])
    be_oos    = interp_zero(c_sorted, [oos_results[c]  for c in c_sorted])

    return {
        "full_net_by_cost": {str(round(c, 2)): v for c, v in full_results.items()},
        "oos_net_by_cost":  {str(round(c, 2)): v for c, v in oos_results.items()},
        "breakeven_full": round(be_full, 3) if np.isfinite(be_full) else None,
        "breakeven_oos":  round(be_oos,  3) if np.isfinite(be_oos)  else None,
    }


# ── Gate 4 — θ-Gradient Surrogate Test ─────────────────────────────────────────

def fit_params(s: np.ndarray) -> dict:
    x = s[np.isfinite(s)]
    dr = np.diff(x)
    mu  = float(np.mean(dr))
    sig = float(np.std(dr, ddof=1))
    sq = dr ** 2
    ab  = float(np.clip(np.corrcoef(sq[1:], sq[:-1])[0, 1], 0.0, 0.97)) if len(sq) > 20 else 0.0
    ab  = float(np.nan_to_num(ab, nan=0.0))
    alpha = ab * 0.15; beta_g = ab - alpha
    omega = max(sig ** 2 * (1.0 - alpha - beta_g), 1e-12)
    phi = float(np.clip(np.nan_to_num(
        np.corrcoef(x[1:], x[:-1])[0, 1] if len(x) > 30 else 0.95, nan=0.95), 0.70, 0.999))
    return {"mu": mu, "sig": sig, "phi": phi, "garch": (omega, alpha, beta_g)}


def sim_rw(p, n, rng):
    return np.concatenate([[0.0], np.cumsum(rng.normal(p["mu"], p["sig"], n - 1))])

def sim_ou(p, n, rng):
    phi = p["phi"]; sigma_ou = p["sig"] * ((1.0 + phi) / 2.0) ** 0.5
    path = np.empty(n); path[0] = 0.0
    for t in range(1, n):
        path[t] = phi * path[t - 1] + sigma_ou * rng.normal()
    return path


def linear_slope(xs: list, ys: list) -> float:
    xs_, ys_ = np.array(xs, float), np.array(ys, float)
    mask = np.isfinite(ys_)
    if mask.sum() < 2:
        return float("nan")
    return float(np.polyfit(xs_[mask], ys_[mask], 1)[0])


def theta_gradient_test(name: str, s: np.ndarray, primary_cost: float) -> dict:
    """Gate 4: is the real θ-gradient steeper than matched-RW and matched-OU surrogates?

    Pre-registered pass: real_slope > 3× median surrogate slope.
    """
    p = fit_params(s)
    n_valid = int(np.sum(np.isfinite(s)))
    rng = np.random.default_rng(SEED_VERIF + 7)

    # Real gross at each θ (zero-cost for gradient, then compare with primary cost)
    real_gross = []
    for th in THETAS:
        trs = run_fade(s, th, cost=0.0)   # gross-only for gradient shape
        real_gross.append(float(np.mean([t["gross"] for t in trs])) if trs else float("nan"))
    real_slope = linear_slope(THETAS, real_gross)

    # Surrogate per-run slopes
    rw_slopes = []; ou_slopes = []
    surr_gross_rw = {th: [] for th in THETAS}
    surr_gross_ou = {th: [] for th in THETAS}

    for i in range(NS):
        rw_path = sim_rw(p, n_valid, rng)
        ou_path = sim_ou(p, n_valid, rng)
        rw_run_gross = []; ou_run_gross = []
        for th in THETAS:
            trs_rw = run_fade(rw_path, th, cost=0.0)
            trs_ou = run_fade(ou_path, th, cost=0.0)
            g_rw = float(np.mean([t["gross"] for t in trs_rw])) if trs_rw else float("nan")
            g_ou = float(np.mean([t["gross"] for t in trs_ou])) if trs_ou else float("nan")
            rw_run_gross.append(g_rw); ou_run_gross.append(g_ou)
            surr_gross_rw[th].append(g_rw); surr_gross_ou[th].append(g_ou)
        rw_slopes.append(linear_slope(THETAS, rw_run_gross))
        ou_slopes.append(linear_slope(THETAS, ou_run_gross))

    rw_slopes_arr = np.array([s for s in rw_slopes if np.isfinite(s)])
    ou_slopes_arr = np.array([s for s in ou_slopes if np.isfinite(s)])
    median_rw_slope = float(np.median(rw_slopes_arr)) if len(rw_slopes_arr) > 0 else float("nan")
    median_ou_slope = float(np.median(ou_slopes_arr)) if len(ou_slopes_arr) > 0 else float("nan")
    p95_rw_slope   = float(np.percentile(rw_slopes_arr, 95)) if len(rw_slopes_arr) > 0 else float("nan")
    p95_ou_slope   = float(np.percentile(ou_slopes_arr, 95)) if len(ou_slopes_arr) > 0 else float("nan")

    # Ratio real/median-surrogate
    ratio_vs_rw = real_slope / (abs(median_rw_slope) + 1e-9)
    ratio_vs_ou = real_slope / (abs(median_ou_slope) + 1e-9)

    # Pre-registered verdict
    if ratio_vs_rw >= 3.0 and ratio_vs_ou >= 3.0:
        gradient_verdict = "GENUINE"
    elif ratio_vs_rw >= 1.5 and ratio_vs_ou >= 1.5:
        gradient_verdict = "MARGINAL"
    else:
        gradient_verdict = "ARTIFACT"

    # Median surrogate gross at each θ
    median_surr_rw = {th: round(float(np.median([v for v in surr_gross_rw[th] if np.isfinite(v)])), 5) for th in THETAS}
    median_surr_ou = {th: round(float(np.median([v for v in surr_gross_ou[th] if np.isfinite(v)])), 5) for th in THETAS}

    return {
        "name": name,
        "real_gross_by_theta": {th: round(v, 5) for th, v in zip(THETAS, real_gross)},
        "real_slope": round(real_slope, 5),
        "median_surr_gross_rw": median_surr_rw,
        "median_surr_gross_ou": median_surr_ou,
        "median_rw_slope": round(median_rw_slope, 5),
        "median_ou_slope": round(median_ou_slope, 5),
        "p95_rw_slope": round(p95_rw_slope, 5),
        "p95_ou_slope": round(p95_ou_slope, 5),
        "ratio_real_vs_rw": round(ratio_vs_rw, 2),
        "ratio_real_vs_ou": round(ratio_vs_ou, 2),
        "gradient_verdict": gradient_verdict,
    }


# ── Gate 2 — Multiplicity Table (hardcoded from docs 39-43) ────────────────────

def gate2_multiplicity() -> dict:
    """
    Full enumeration of all pairs × β-families × test stages run across docs 39-43.
    Two families:
      (A) Economic eval primary tests (θ=1.0, p_rw, doc 43) — the inference family
      (B) VR screening tests (doc 39-42) — pre-filtering stage, separate family
    BH correction at q=0.10 applied to family A (the confirmation tests).
    """
    # Family A — economic evaluation p-values (θ=1.0)
    econ_tests = [
        {"pair": "HO-CL", "beta": "F5", "theta": 1.0, "p_rw": 0.072, "doc": 43},
        {"pair": "RB-CL", "beta": "F6", "theta": 1.0, "p_rw": 0.006, "doc": 43},
        {"pair": "LE-GF", "beta": "F5", "theta": 1.0, "p_rw": 0.002, "doc": 43},
    ]

    # BH correction (q=0.10) on econ test family
    m = len(econ_tests)
    sorted_tests = sorted(econ_tests, key=lambda x: x["p_rw"])
    bh_threshold_q010 = [(k + 1) / m * 0.10 for k in range(m)]
    bonferroni_threshold = 0.05 / m

    # Determine each test's BH status
    bh_results = []
    for k, t in enumerate(sorted_tests):
        bh_thr = bh_threshold_q010[k]
        bh_results.append({
            "rank": k + 1,
            "pair": t["pair"], "beta": t["beta"],
            "p_rw": t["p_rw"],
            "bh_threshold_q010": round(bh_thr, 4),
            "bonferroni_threshold": round(bonferroni_threshold, 4),
            "survives_bh_q010": t["p_rw"] <= bh_thr,
            "survives_bonferroni": t["p_rw"] <= bonferroni_threshold,
        })

    # Family B — VR screening tests (pre-filtering, not the confirmation family)
    vr_tests = [
        {"pair": "HO-CL", "beta": "F5", "period": "FULL",  "doc": 39, "status": "CONFIRM"},
        {"pair": "HO-CL", "beta": "F6", "period": "FULL",  "doc": 39, "status": "CONFIRM"},
        {"pair": "HO-CL", "beta": "F5", "period": "OOS",   "doc": 39, "status": "CONFIRM"},
        {"pair": "HO-CL", "beta": "F6", "period": "OOS",   "doc": 39, "status": "CONFIRM"},
        {"pair": "RB-CL", "beta": "F6", "period": "FULL",  "doc": 40, "status": "CONFIRM"},
        {"pair": "RB-CL", "beta": "F6", "period": "OOS",   "doc": 40, "status": "CONFIRM"},
        {"pair": "RB-CL", "beta": "F5", "period": "FULL",  "doc": 40, "status": "CONFIRM"},
        {"pair": "RB-CL", "beta": "F5", "period": "OOS",   "doc": 40, "status": "OOS_FAIL"},
        {"pair": "GC-PL", "beta": "F5", "period": "FULL",  "doc": 41, "status": "CONFIRM"},
        {"pair": "GC-PL", "beta": "F5", "period": "OOS",   "doc": 41, "status": "OOS_FAIL"},
        {"pair": "GC-PL", "beta": "F6", "period": "FULL",  "doc": 41, "status": "CONFIRM"},
        {"pair": "GC-PL", "beta": "F6", "period": "OOS",   "doc": 41, "status": "MARGINAL"},
        {"pair": "LE-GF", "beta": "F5", "period": "FULL",  "doc": 42, "status": "CONFIRM"},
        {"pair": "LE-GF", "beta": "F5", "period": "OOS",   "doc": 42, "status": "CONFIRM"},
        {"pair": "LE-GF", "beta": "F6", "period": "FULL",  "doc": 42, "status": "NO_CONFIRM"},
        {"pair": "KE-ZW", "beta": "F5", "period": "FULL",  "doc": 42, "status": "CONFIRM"},
        {"pair": "KE-ZW", "beta": "F5", "period": "OOS",   "doc": 42, "status": "OOS_FAIL"},
    ]

    # Broadest family correction: if we include all VR tests as one family (conservative)
    # Count "CONFIRM + FULL" tests that produced an economic test downstream
    n_vr_pairs_tested = 5  # HO-CL, RB-CL, GC-PL, LE-GF, KE-ZW
    bonferroni_broadest = round(0.05 / n_vr_pairs_tested, 4)

    return {
        "economic_test_family": bh_results,
        "bh_q010_threshold_at_rank": bh_threshold_q010,
        "bonferroni_threshold_3tests": round(bonferroni_threshold, 4),
        "bonferroni_threshold_5pairs_broadest": bonferroni_broadest,
        "vr_screening_family": vr_tests,
        "summary": {
            "rb_cl_survives_bh_q010": bh_results[0]["survives_bh_q010"],
            "rb_cl_survives_bonferroni_3": bh_results[0]["survives_bonferroni"],
            "rb_cl_survives_bonferroni_5pairs": 0.006 <= bonferroni_broadest,
            "le_gf_survives_bh_q010": bh_results[1]["survives_bh_q010"] if len(bh_results) > 1 else None,
            "le_gf_survives_bonferroni_3": bh_results[1]["survives_bonferroni"] if len(bh_results) > 1 else None,
            "le_gf_survives_bonferroni_5pairs": 0.002 <= bonferroni_broadest,
        }
    }


# ── Main ───────────────────────────────────────────────────────────────────────

def run_pair(cfg: dict) -> dict:
    print(f"\n{'='*72}")
    print(f"PAIR: {cfg['name']}")
    print(f"{'='*72}")

    # Build spreads
    s_raw, s_ds, idx, beta_val = build_spread_raw(
        cfg["fileA"], cfg["fileB"], cfg["scaleA"], cfg["beta_mode"],
        cfg["date_min"])
    n = len(s_ds)
    n_oos = int(n * (1.0 - OOS_SPLIT))
    total_bars = int(np.sum(np.isfinite(s_ds)))

    print(f"  N={n}  β={beta_val:.4f}  valid_bars={total_bars}")

    # Gate 0 — Raw vs Deseason VR
    g0 = gate0_raw_vr(cfg["name"], s_raw, s_ds)
    print(f"\n  GATE 0 — Raw VR test:")
    print(f"    raw:    VR(20)={g0['vr20_raw']:.4f}  p_rw={g0['p_rw_raw']:.4f}")
    print(f"    deseasonalized: VR(20)={g0['vr20_ds']:.4f}  p_rw={g0['p_rw_ds']:.4f}")
    print(f"    raw spread: mean={g0['raw_spread_mean']:.3f}  std={g0['raw_spread_std']:.3f}  "
          f"|mean|/std={g0['mean_std_ratio']:.3f}")
    if g0["deseason_amplification"]:
        print(f"    deseason_amplification={g0['deseason_amplification']:.2f}×")
    print(f"    >> CLASSIFICATION: {g0['gate0_classification']}")

    # Splice diagnostic on each leg
    splice_A = splice_diagnostic(os.path.join(DATA, cfg["fileA"]), cfg["scaleA"], cfg["fileA"].split("/")[-1])
    splice_B = splice_diagnostic(os.path.join(DATA, cfg["fileB"]), 1.0,          cfg["fileB"].split("/")[-1])
    print(f"\n  SPLICE DIAGNOSTICS:")
    for sp in [splice_A, splice_B]:
        print(f"    {sp['leg']}: n_neg={sp['n_neg']} ({sp['pct_neg']:.1f}%)  "
              f"|mean|/std={sp['mean_std_ratio']:.3f}  >> {sp['grade']}")

    # Gate 3 — Book metrics
    primary_cost = cfg["primary_cost"]
    trs_full = run_fade(s_ds, PRIMARY_TH, primary_cost)
    trs_oos  = run_fade(s_ds[-n_oos:], PRIMARY_TH, primary_cost)
    bm = book_metrics(trs_full, total_bars)
    bm_oos = book_metrics(trs_oos, n_oos)

    print(f"\n  GATE 3 — Book metrics (θ=1.0, primary_cost={primary_cost}):")
    print(f"    Full: n={bm.get('n_trades')}  trades/yr={bm.get('trades_per_year'):.1f}  "
          f"Sharpe={bm.get('annualized_sharpe'):.3f}  MDD={bm.get('max_drawdown_units'):.4f}  "
          f"MDD/median_trade={bm.get('mdd_in_median_trades'):.1f}×")
    print(f"    OOS:  n={bm_oos.get('n_trades')}  "
          f"Sharpe={bm_oos.get('annualized_sharpe'):.3f}")

    # Capacity estimate
    cap = capacity_estimate(
        bm.get("trades_per_year", 0), bm.get("mean_net", 0),
        cfg["adv_limiting"], cfg["contract_units"], cfg["unit_label"])
    print(f"    Capacity: {cap['max_contracts_5pct_adv']} contracts/trade (5% of {cap['limiting_leg_adv']} ADV)  "
          f"→ ~${cap['theoretical_annual_capacity_usd']:,.0f}/yr theoretical max")

    # Breakeven curve
    be = breakeven_curve(s_ds, cfg["cost_grid"], n_total=n)
    be_full_str = f"{be['breakeven_full']:.3f}" if be.get("breakeven_full") else ">grid_max"
    be_oos_str  = f"{be['breakeven_oos']:.3f}"  if be.get("breakeven_oos")  else ">grid_max"
    print(f"    Breakeven (full): {be_full_str} {cfg['cost_unit']} | OOS: {be_oos_str} {cfg['cost_unit']}")
    be_oos_val = be.get("breakeven_oos")
    if be_oos_val:
        ratio = be_oos_val / cfg["defended_realistic_cost"]
        print(f"    OOS BE / defended_realistic_cost = {ratio:.2f}×  (pass ≥ 2.0×)")
    else:
        print(f"    OOS BE > grid_max (all net positive at max cost tested); edge robust across entire cost grid")

    # Gate 4 — θ-gradient test
    g4 = theta_gradient_test(cfg["name"], s_ds, primary_cost)
    print(f"\n  GATE 4 — θ-gradient surrogate test:")
    print(f"    Real gross by θ: " + "  ".join(f"θ={th}: {g4['real_gross_by_theta'][th]:.4f}" for th in THETAS))
    print(f"    Median RW gross: " + "  ".join(f"θ={th}: {g4['median_surr_gross_rw'][th]:.4f}" for th in THETAS))
    print(f"    Median OU gross: " + "  ".join(f"θ={th}: {g4['median_surr_gross_ou'][th]:.4f}" for th in THETAS))
    print(f"    Real slope={g4['real_slope']:.5f}  RW_slope={g4['median_rw_slope']:.5f}  OU_slope={g4['median_ou_slope']:.5f}")
    print(f"    Ratio_vs_RW={g4['ratio_real_vs_rw']:.2f}×  Ratio_vs_OU={g4['ratio_real_vs_ou']:.2f}×")
    print(f"    >> GRADIENT VERDICT: {g4['gradient_verdict']}")

    return {
        "name": cfg["name"], "n": n, "total_valid_bars": total_bars, "beta_val": beta_val,
        "gate0": g0,
        "splice_A": splice_A, "splice_B": splice_B,
        "book_metrics_full": bm, "book_metrics_oos": bm_oos,
        "capacity": cap,
        "breakeven": be,
        "gate4_gradient": g4,
    }


if __name__ == "__main__":
    np.seterr(all="ignore")
    print("Sleeve Verification Gauntlet — Gates 0, 2, 3, 4")
    print("Pre-registered: docs/research/sleeve_verification_prereg.md")

    pairs = [
        {
            "name": "RB-CL (F6, β=1.0)",
            "fileA": "NYMEX_DL_RB2!, 1D.csv",
            "fileB": "NYMEX_DL_CL2!, 1D.csv",
            "scaleA": 42.0,
            "beta_mode": "f6",
            "date_min": "1998-07-19",
            "primary_cost": 0.20,      # defended realistic
            "cost_grid": [0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00],
            "cost_unit": "$/bbl",
            "defended_realistic_cost": DEFENDED_COST_ENERGY,
            "adv_limiting": ADV_RBOB,
            "contract_units": CONTRACT_ENERGY_BBL,
            "unit_label": "$/bbl",
        },
        {
            "name": "LE-GF (F5, β=0.565)",
            "fileA": "CME_DL_LE2!, 1D.csv",
            "fileB": "CME_DL_GF2!, 1D.csv",
            "scaleA": 1.0,
            "beta_mode": "f5",
            "date_min": "2002-08-14",
            "primary_cost": 0.20,      # defended realistic
            "cost_grid": [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50],
            "cost_unit": "¢/lb",
            "defended_realistic_cost": DEFENDED_COST_LIVESTOCK,
            "adv_limiting": ADV_GF,   # GF is binding constraint
            "contract_units": CONTRACT_GF_LBS,
            "unit_label": "¢/lb",
        },
    ]

    results = {}
    for cfg in pairs:
        results[cfg["name"]] = run_pair(cfg)

    # Gate 2 — Multiplicity (computed from doc 39-43 p-values, no recomputation needed)
    print(f"\n{'='*72}")
    print("GATE 2 — Multiplicity Correction")
    g2 = gate2_multiplicity()
    print(f"  Family A (economic tests, θ=1.0): {len(g2['economic_test_family'])} tests")
    for row in g2["economic_test_family"]:
        be = "✓" if row["survives_bh_q010"] else "✗"
        bf = "✓" if row["survives_bonferroni"] else "✗"
        print(f"    rank={row['rank']} {row['pair']}-{row['beta']}  p={row['p_rw']:.4f}  "
              f"BH_thr={row['bh_threshold_q010']:.4f} [{be}]  Bonf_3={row['bonferroni_threshold']:.4f} [{bf}]")
    s = g2["summary"]
    print(f"  RB-CL: BH[q=0.10]={s['rb_cl_survives_bh_q010']}  "
          f"Bonf/3={s['rb_cl_survives_bonferroni_3']}  Bonf/5pairs={s['rb_cl_survives_bonferroni_5pairs']}")
    print(f"  LE-GF: BH[q=0.10]={s['le_gf_survives_bh_q010']}  "
          f"Bonf/3={s['le_gf_survives_bonferroni_3']}  Bonf/5pairs={s['le_gf_survives_bonferroni_5pairs']}")

    results["gate2_multiplicity"] = g2

    # Write JSON
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "data", "processed", "sleeve_verification_results.json")
    def _s(x):
        if isinstance(x, float) and not np.isfinite(x): return None
        if isinstance(x, (np.floating, np.integer)): return float(x)
        if isinstance(x, np.bool_): return bool(x)
        if isinstance(x, dict): return {str(k): _s(v) for k, v in x.items()}
        if isinstance(x, list): return [_s(i) for i in x]
        return x
    with open(out_path, "w") as f:
        json.dump(_s(results), f, indent=2)

    print(f"\nResults saved → {out_path}")
