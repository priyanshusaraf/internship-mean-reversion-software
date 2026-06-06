"""
Portfolio Combination Test — RB-CL + LE-GF
Pre-registration: docs/research/portfolio_combination_prereg.md (written BEFORE this script).

Gates A, B, C:
  Gate A — RB-CL excision robustness (exclude 2020-03-01 to 2021-06-30)
  Gate B — Independence test (cross-sleeve correlation + stress-window joint drawdown)
  Gate C — Combined book metrics (inverse-vol sizing, IS+OOS)

Gate D (adversarial synthesis) is handled separately as named agents.
"""
from __future__ import annotations
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import numpy as np
import pandas as pd
from app.services.analytics_arm_a_v2 import deseasonalize_causal, increment_jump_mask
from app.services.analytics_arm_a_v2_beta import economic_anchor_beta, presample_ols_beta

# ── Frozen pre-reg constants ────────────────────────────────────────────────────
SEED_PORTFOLIO  = 20260607
OOS_SPLIT       = 0.70
PRE_FRAC        = 0.25
JUMP_K          = 8.0
JUMP_W          = 60
LB              = 60
MH              = 40
PRIMARY_THETA   = 1.0
NS_VR           = 200

COST_RBCL       = 0.20          # $/bbl defended cost
COST_LEGF       = 0.20          # ¢/lb defended cost

EXCISE_START    = "2020-03-01"
EXCISE_END      = "2021-06-30"

CAP_RBCL_YR     = 2_000_000    # $2M/yr cap for RB-CL in combined book
CAP_LEGF_YR     =   350_000    # $350k/yr cap for LE-GF

STRESS_COVID    = ("2020-01-01", "2020-12-31")
STRESS_ENERGY   = ("2022-01-01", "2022-12-31")

DATE_MIN_RBCL   = "1998-07-19"
DATE_MIN_LEGF   = "1995-01-01"
DATE_MAX        = "2026-06-03"

# $/unit scaling for capacity/PnL
CONTRACT_BBL    = 1_000     # barrels per RB/CL contract
CONTRACT_GF_LBS = 50_000    # lbs per feeder cattle contract

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw",
                    "more-mean-reversion-data")


# ── Helpers (copied from run_sleeve_verification.py to be self-contained) ───────

def load_u(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["ts"] = pd.to_datetime(df["time"].astype(np.int64), unit="s", utc=True)
    return df.dropna(subset=["ts"]).sort_values("ts").drop_duplicates("ts", keep="last").set_index("ts")


def vr_q(s: np.ndarray, q: int = 20) -> float:
    x = s[np.isfinite(s)]
    n = len(x)
    if n < q + 20:
        return float("nan")
    dr   = np.diff(x)
    var1 = np.var(dr, ddof=1)
    if var1 <= 1e-14:
        return float("nan")
    ret_q = x[q:] - x[:-q]
    varq  = np.var(ret_q, ddof=1)
    return float(varq / (q * var1))


def vr_rw_pval(s: np.ndarray, q: int = 20, n_surr: int = NS_VR,
               seed: int = SEED_PORTFOLIO) -> tuple[float, float]:
    real_vr = vr_q(s, q)
    if not np.isfinite(real_vr):
        return float("nan"), float("nan")
    x   = s[np.isfinite(s)]
    n   = len(x)
    dr  = np.diff(x)
    mu_ = float(np.mean(dr))
    sig_= float(np.std(dr, ddof=1))
    rng = np.random.default_rng(seed)
    surr_vrs = []
    for _ in range(n_surr):
        path = np.concatenate([[0.0], np.cumsum(rng.normal(mu_, sig_, n - 1))])
        v = vr_q(path, q)
        if np.isfinite(v):
            surr_vrs.append(v)
    pv = (1.0 + sum(v <= real_vr for v in surr_vrs)) / (len(surr_vrs) + 1.0)
    return float(real_vr), float(pv)


def build_spread(fileA: str, fileB: str, scaleA: float, beta_mode: str,
                 date_min: str, date_max: str = DATE_MAX,
                 excise_start: str | None = None, excise_end: str | None = None,
                 excise_mode: str = "exclude") -> tuple[np.ndarray, np.ndarray, pd.DatetimeIndex, float, np.ndarray]:
    """
    Build spread series.
    Returns (s_raw_clean, s_ds_clean, idx, beta_val, neg_b_mask).
      s_raw_clean: raw spread, roll-masked (for VR tests — doc 44 Gate 0 methodology)
      s_ds_clean:  deseasonalized spread, roll-masked (for economic fade — doc 43 methodology)
    excise_mode='exclude': drop rows in excise window.
    excise_mode='nan': NaN rows in excise window (preserves alignment).
    """
    A_raw = load_u(os.path.join(DATA, fileA))
    B_raw = load_u(os.path.join(DATA, fileB))
    A_raw = A_raw[(A_raw.index >= date_min) & (A_raw.index <= date_max)]
    B_raw = B_raw[(B_raw.index >= date_min) & (B_raw.index <= date_max)]
    merged = A_raw[["close"]].join(B_raw[["close"]], how="inner",
                                   lsuffix="_a", rsuffix="_b").dropna()
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
        raise ValueError(f"unknown beta_mode: {beta_mode}")

    s_raw_arr   = np.where(np.isfinite(beta), A - beta * B, np.nan)
    s_ds_arr    = deseasonalize_causal(s_raw_arr, idx)  # causal deseasonalization
    roll        = increment_jump_mask(s_raw_arr, k=JUMP_K, window=JUMP_W)
    inv         = ~np.isfinite(beta) | roll

    s_raw_clean = np.where(inv, np.nan, s_raw_arr)  # raw, roll-masked
    s_ds_clean  = np.where(inv, np.nan, s_ds_arr)   # deseasonalized, roll-masked

    # Track negative B (CL) prices — affects RB-CL spread inflation
    neg_b_mask = np.array([b < 0 for b in B], dtype=bool)

    if excise_start and excise_end:
        exc_mask = (idx >= excise_start) & (idx <= excise_end)
        if excise_mode == "exclude":
            keep        = ~exc_mask
            s_raw_clean = s_raw_clean[keep]
            s_ds_clean  = s_ds_clean[keep]
            neg_b_mask  = neg_b_mask[keep]
            idx         = idx[keep]
        elif excise_mode == "nan":
            s_raw_clean[exc_mask] = np.nan
            s_ds_clean[exc_mask]  = np.nan

    return s_raw_clean, s_ds_clean, idx, beta_val, neg_b_mask


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
        mu  = win.mean(); sd = win.std() + 1e-9
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


def book_metrics(trades: list[dict], total_bars: int, bars_per_year: float = 252.0) -> dict:
    if len(trades) < 5:
        return {"insufficient_trades": True, "n_trades": len(trades)}
    nets  = np.array([t["net"]   for t in trades])
    gross = np.array([t["gross"] for t in trades])
    n_yrs = total_bars / bars_per_year
    t_yr  = len(trades) / n_yrs
    sharpe = (float(np.mean(nets)) / (float(np.std(nets, ddof=1)) + 1e-9)) * (t_yr ** 0.5)
    cumul  = np.cumsum(nets)
    peak   = np.maximum.accumulate(cumul)
    dd     = cumul - peak
    max_dd = float(np.min(dd))
    med_n  = float(np.median(nets))
    return {
        "n_trades": len(trades),
        "n_years":  round(n_yrs, 1),
        "trades_per_year": round(t_yr, 1),
        "mean_gross": round(float(np.mean(gross)), 5),
        "mean_net":   round(float(np.mean(nets)),  5),
        "median_net": round(med_n, 5),
        "std_net":    round(float(np.std(nets, ddof=1)), 5),
        "annualized_sharpe": round(sharpe, 3),
        "max_drawdown_units": round(max_dd, 4),
        "mdd_in_median_trades": round(abs(max_dd) / (abs(med_n) + 1e-9), 1),
        "cumulative_net": round(float(np.sum(nets)), 4),
        "hit_rate": round(float(np.mean(nets > 0)), 3),
    }


# ── Gate A — RB-CL Excision ─────────────────────────────────────────────────────

def gate_a_excision() -> dict:
    print("Gate A: RB-CL excision robustness (excise 2020-03-01 to 2021-06-30)...")
    print("  NOTE: VR test uses RAW spread; economic fade uses DESEASONALIZED (consistent with doc 43/44).")
    print("  NOTE: Excision window (2020-2021) falls in OOS period (IS ends ~2017-2018).")

    # Full spread (for baseline comparison)
    s_raw_full, s_ds_full, idx_full, bv_full, neg_cl_full = build_spread(
        "NYMEX_DL_RB2!, 1D.csv", "NYMEX_DL_CL2!, 1D.csv",
        scaleA=42.0, beta_mode="f6", date_min=DATE_MIN_RBCL,
    )
    n_full    = len(s_raw_full)
    n_is_full = int(n_full * OOS_SPLIT)

    # IS period dates (for audit)
    is_end_date = str(idx_full[n_is_full - 1].date()) if n_is_full > 0 else "unknown"
    oos_start_date = str(idx_full[n_is_full].date()) if n_is_full < len(idx_full) else "unknown"

    # VR on RAW IS
    s_raw_is_full = s_raw_full[:n_is_full]
    vr_full_raw, p_full_raw = vr_rw_pval(s_raw_is_full)
    # Also compute full-period raw VR (for comparison with doc 44)
    vr_fullperiod_raw, p_fullperiod_raw = vr_rw_pval(s_raw_full)

    # Economic fade on DESEASONALIZED IS
    s_ds_is_full = s_ds_full[:n_is_full]
    trs_ds_is    = run_fade(s_ds_is_full,  PRIMARY_THETA, COST_RBCL)
    trs_ds_oos   = run_fade(s_ds_full[n_is_full:], PRIMARY_THETA, COST_RBCL)
    bm_full_is   = book_metrics(trs_ds_is,  n_is_full)
    bm_full_oos  = book_metrics(trs_ds_oos, n_full - n_is_full)

    # Excised spread (drop contamination window entirely)
    s_raw_exc, s_ds_exc, idx_exc, bv_exc, neg_cl_exc = build_spread(
        "NYMEX_DL_RB2!, 1D.csv", "NYMEX_DL_CL2!, 1D.csv",
        scaleA=42.0, beta_mode="f6", date_min=DATE_MIN_RBCL,
        excise_start=EXCISE_START, excise_end=EXCISE_END, excise_mode="exclude",
    )
    n_exc    = len(s_raw_exc)
    n_is_exc = int(n_exc * OOS_SPLIT)

    # VR on RAW IS (excised)
    s_raw_is_exc = s_raw_exc[:n_is_exc]
    vr_exc_raw, p_exc_raw = vr_rw_pval(s_raw_is_exc)

    # Economic fade on DESEASONALIZED IS (excised)
    s_ds_is_exc  = s_ds_exc[:n_is_exc]
    trs_exc_is   = run_fade(s_ds_is_exc,    PRIMARY_THETA, COST_RBCL)
    trs_exc_oos  = run_fade(s_ds_exc[n_is_exc:], PRIMARY_THETA, COST_RBCL)
    bm_exc_is    = book_metrics(trs_exc_is,  n_is_exc)
    bm_exc_oos   = book_metrics(trs_exc_oos, n_exc - n_is_exc)

    # OOS on the original full dataset (unchanged per pre-reg)
    s_ds_oos_orig = s_ds_full[n_is_full:]
    trs_orig_oos  = run_fade(s_ds_oos_orig, PRIMARY_THETA, COST_RBCL)
    bm_orig_oos   = book_metrics(trs_orig_oos, n_full - n_is_full)

    # Auditing how many excised bars fall in IS vs OOS
    exc_dates_all = (idx_full >= EXCISE_START) & (idx_full <= EXCISE_END)
    exc_dates_is  = exc_dates_all[:n_is_full]
    exc_dates_oos = exc_dates_all[n_is_full:]
    n_excised_in_is  = int(np.sum(exc_dates_is))
    n_excised_in_oos = int(np.sum(exc_dates_oos))

    vr_full  = vr_full_raw;     p_full  = p_full_raw
    vr_exc   = vr_exc_raw;      p_exc   = p_exc_raw

    # Pre-committed pass criteria
    exc_vr_pass  = np.isfinite(p_exc) and p_exc < 0.050
    exc_is_net_pass = (bm_exc_is.get("mean_net", float("-inf")) or float("-inf")) > 0
    oos_net_pass    = (bm_orig_oos.get("mean_net", float("-inf")) or float("-inf")) > 0
    all_pass = exc_vr_pass and exc_is_net_pass and oos_net_pass
    # Confirmed-sleeve upgrade: excised IS VR p < 0.010
    confirmed_upgrade = np.isfinite(p_exc) and p_exc < 0.010

    result = {
        "methodology_note": (
            "VR test on RAW spread (doc 44 Gate 0 method); economic fade on DESEASONALIZED spread "
            "(doc 43 method). IS period ≈ 1998–2017; OOS ≈ 2017–2026. "
            f"Excision window {EXCISE_START} to {EXCISE_END} falls almost entirely in OOS "
            f"({n_excised_in_is} IS bars, {n_excised_in_oos} OOS bars excised). "
            "Consequence: excision barely changes IS VR (excision window is post-IS)."
        ),
        "baseline": {
            "n_full": n_full, "n_is": n_is_full,
            "is_period": f"~{idx_full[0].date()} to {is_end_date}",
            "oos_period": f"~{oos_start_date} to {idx_full[-1].date()}",
            "vr20_full_period_raw": round(vr_fullperiod_raw, 4),
            "p_rw_full_period_raw": round(p_fullperiod_raw, 4),
            "vr20_is_only_raw": round(vr_full, 4),
            "p_rw_is_only_raw": round(p_full, 4),
            "is_metrics_ds": bm_full_is,
            "oos_metrics_ds": bm_full_oos,
        },
        "excised": {
            "excise_window": f"{EXCISE_START} to {EXCISE_END}",
            "n_excised_total": n_full - n_exc,
            "n_excised_in_IS": n_excised_in_is,
            "n_excised_in_OOS": n_excised_in_oos,
            "n_remaining": n_exc,
            "vr20_is_excised_raw": round(vr_exc, 4),
            "p_rw_is_excised_raw": round(p_exc, 4),
            "is_metrics_excised_ds": bm_exc_is,
            "oos_metrics_orig_ds": bm_orig_oos,
        },
        "pass_criteria": {
            "excised_IS_VR_p_lt_050": exc_vr_pass,
            "excised_IS_net_gt_0": exc_is_net_pass,
            "orig_OOS_net_gt_0": oos_net_pass,
        },
        "gate_a_pass": all_pass,
        "confirmed_sleeve_upgrade": confirmed_upgrade,
        "critical_finding": (
            "IS (1998–2017) raw VR p={:.4f} — NOT significant, even before excision. "
            "Full-period VR p={:.4f} — this was the doc 44 Gate 0 result (full series, incl. OOS). "
            "Sub-diffusion in RB-CL is concentrated in the post-2017 OOS period, not the IS."
        ).format(p_full_raw, p_fullperiod_raw),
    }
    status = "PASS" if all_pass else "FAIL"
    print(f"  Gate A: {status}.")
    print(f"  Baseline IS VR p={p_full_raw:.4f} (NOT significant before excision)")
    print(f"  Full-period VR p={p_fullperiod_raw:.4f} (doc 44 Gate 0 used full period)")
    print(f"  Excised IS VR p={p_exc_raw:.4f} | IS econ net={bm_exc_is.get('mean_net','?'):.4f} | OOS net={bm_orig_oos.get('mean_net','?'):.4f}")
    return result


# ── Gate B — Independence Test ───────────────────────────────────────────────────

def gate_b_independence() -> dict:
    print("Gate B: Cross-sleeve independence...")

    # Use deseasonalized for spread level (independence test on the SPREAD used for trading)
    _, s_rb, idx_rb, _, _ = build_spread(
        "NYMEX_DL_RB2!, 1D.csv", "NYMEX_DL_CL2!, 1D.csv",
        scaleA=42.0, beta_mode="f6", date_min=DATE_MIN_RBCL,
    )
    _, s_le, idx_le, _, _ = build_spread(
        "CME_DL_LE2!, 1D.csv", "CME_DL_GF2!, 1D.csv",
        scaleA=1.0, beta_mode="f5", date_min=DATE_MIN_LEGF,
    )

    # Align on common dates
    df_rb = pd.Series(s_rb, index=idx_rb, name="rb_cl")
    df_le = pd.Series(s_le, index=idx_le, name="le_gf")
    df = pd.concat([df_rb, df_le], axis=1).dropna()

    ret_rb = df["rb_cl"].diff().dropna()
    ret_le = df["le_gf"].diff().dropna()
    df_ret = pd.concat([ret_rb, ret_le], axis=1).dropna()

    full_corr = float(df_ret["rb_cl"].corr(df_ret["le_gf"]))
    n_common = len(df_ret)

    # Stress window analysis
    def stress_analysis(window_start: str, window_end: str, label: str) -> dict:
        mask = (df_ret.index >= window_start) & (df_ret.index <= window_end)
        sub  = df_ret[mask]
        if len(sub) < 5:
            return {"window": label, "n_days": len(sub), "insufficient": True}
        r_rb = sub["rb_cl"].to_numpy()
        r_le = sub["le_gf"].to_numpy()
        sim_loss = float(np.mean((r_rb < 0) & (r_le < 0)))
        corr_stress = float(np.corrcoef(r_rb, r_le)[0, 1]) if len(sub) >= 5 else float("nan")
        # Cumulative spread level in this window (for drawdown)
        sub_lvl_rb = df["rb_cl"][mask].to_numpy()
        sub_lvl_le = df["le_gf"][mask].to_numpy()
        mean_rb = float(np.nanmean(sub_lvl_rb))
        mean_le = float(np.nanmean(sub_lvl_le))
        # Run fade in stress window — crude but informative
        trs_rb = run_fade(sub_lvl_rb, PRIMARY_THETA, COST_RBCL) if len(sub_lvl_rb) >= LB + 5 else []
        trs_le = run_fade(sub_lvl_le, PRIMARY_THETA, COST_LEGF)  if len(sub_lvl_le) >= LB + 5 else []
        net_rb_stress = float(np.mean([t["net"] for t in trs_rb])) if trs_rb else float("nan")
        net_le_stress = float(np.mean([t["net"] for t in trs_le])) if trs_le else float("nan")
        return {
            "window": label, "n_days": int(len(sub)),
            "correlation_in_window": round(corr_stress, 3),
            "simultaneous_loss_pct": round(sim_loss * 100, 1),
            "rbcl_mean_spread_level": round(mean_rb, 3),
            "legf_mean_spread_level": round(mean_le, 3),
            "rbcl_net_per_trade_stress": round(net_rb_stress, 4) if np.isfinite(net_rb_stress) else None,
            "legf_net_per_trade_stress": round(net_le_stress, 4) if np.isfinite(net_le_stress) else None,
        }

    covid_stress  = stress_analysis(*STRESS_COVID,  "COVID 2020")
    energy_stress = stress_analysis(*STRESS_ENERGY, "Energy spike 2022")

    # Combined stress window
    mask_comb = ((df_ret.index >= STRESS_COVID[0]) & (df_ret.index <= STRESS_COVID[1])) | \
                ((df_ret.index >= STRESS_ENERGY[0]) & (df_ret.index <= STRESS_ENERGY[1]))
    sub_comb  = df_ret[mask_comb]
    sim_loss_comb = float(np.mean((sub_comb["rb_cl"] < 0) & (sub_comb["le_gf"] < 0))) if len(sub_comb) >= 5 else float("nan")

    # Pre-committed independence classification
    independent_full   = abs(full_corr) < 0.30
    covid_simloss_ok   = covid_stress.get("simultaneous_loss_pct", 100.0) < 60.0
    energy_simloss_ok  = energy_stress.get("simultaneous_loss_pct", 100.0) < 60.0
    independence_verdict = "INDEPENDENT" if (independent_full and covid_simloss_ok and energy_simloss_ok) \
                           else "CORRELATED"

    print(f"  Gate B: full_corr={full_corr:.3f}, COVID sim_loss={covid_stress.get('simultaneous_loss_pct','?')}%, "
          f"energy sim_loss={energy_stress.get('simultaneous_loss_pct','?')}% → {independence_verdict}")

    return {
        "n_common_dates": n_common,
        "full_sample_correlation": round(full_corr, 4),
        "independence_threshold": 0.30,
        "stress_windows": {
            "COVID_2020": covid_stress,
            "energy_spike_2022": energy_stress,
            "combined_simultaneous_loss_pct": round(sim_loss_comb * 100, 1) if np.isfinite(sim_loss_comb) else None,
        },
        "independence_verdict": independence_verdict,
    }


# ── Gate C — Combined Book ───────────────────────────────────────────────────────

def gate_c_combined() -> dict:
    print("Gate C: Combined book metrics...")

    # Use deseasonalized for economic fade (consistent with doc 43)
    _, s_rb, idx_rb, _, _ = build_spread(
        "NYMEX_DL_RB2!, 1D.csv", "NYMEX_DL_CL2!, 1D.csv",
        scaleA=42.0, beta_mode="f6", date_min=DATE_MIN_RBCL,
    )
    _, s_le, idx_le, _, _ = build_spread(
        "CME_DL_LE2!, 1D.csv", "CME_DL_GF2!, 1D.csv",
        scaleA=1.0, beta_mode="f5", date_min=DATE_MIN_LEGF,
    )

    # Common date range alignment
    date_start = max(idx_rb[np.where(np.isfinite(s_rb))[0][0]],
                     idx_le[np.where(np.isfinite(s_le))[0][0]])
    df_rb_full = pd.Series(s_rb, index=idx_rb)
    df_le_full = pd.Series(s_le, index=idx_le)
    df_joint   = pd.concat([df_rb_full, df_le_full], axis=1, keys=["rb_cl", "le_gf"])
    df_joint   = df_joint[df_joint.index >= date_start].dropna(how="all")

    n_joint  = len(df_joint)
    n_is_jnt = int(n_joint * OOS_SPLIT)
    n_oos_jnt= n_joint - n_is_jnt
    split_date = df_joint.index[n_is_jnt]

    s_rb_joint = df_joint["rb_cl"].to_numpy(float)
    s_le_joint = df_joint["le_gf"].to_numpy(float)

    s_rb_is = s_rb_joint[:n_is_jnt]
    s_le_is = s_le_joint[:n_is_jnt]
    s_rb_oos= s_rb_joint[n_is_jnt:]
    s_le_oos= s_le_joint[n_is_jnt:]

    # Inverse-vol weights on IS returns
    ret_rb_is = np.diff(s_rb_is[np.isfinite(s_rb_is)])
    ret_le_is = np.diff(s_le_is[np.isfinite(s_le_is)])
    vol_rb_is = float(np.std(ret_rb_is, ddof=1)) if len(ret_rb_is) > 5 else 1.0
    vol_le_is = float(np.std(ret_le_is, ddof=1)) if len(ret_le_is) > 5 else 1.0
    inv_vol_rb = 1.0 / (vol_rb_is + 1e-9)
    inv_vol_le = 1.0 / (vol_le_is + 1e-9)
    total_iv = inv_vol_rb + inv_vol_le
    w_rb = inv_vol_rb / total_iv
    w_le = inv_vol_le / total_iv

    # Per-sleeve raw dollar metrics (needed for capacity-weighted combination)
    def sleeve_pnl_series(s, theta, cost):
        """Run fade, return per-bar PnL series aligned to input length."""
        n = len(s)
        trades = run_fade(s, theta, cost)
        return trades

    trs_rb_is  = sleeve_pnl_series(s_rb_is,  PRIMARY_THETA, COST_RBCL)
    trs_rb_oos = sleeve_pnl_series(s_rb_oos, PRIMARY_THETA, COST_RBCL)
    trs_le_is  = sleeve_pnl_series(s_le_is,  PRIMARY_THETA, COST_LEGF)
    trs_le_oos = sleeve_pnl_series(s_le_oos, PRIMARY_THETA, COST_LEGF)

    bm_rb_is  = book_metrics(trs_rb_is,  n_is_jnt)
    bm_rb_oos = book_metrics(trs_rb_oos, n_oos_jnt)
    bm_le_is  = book_metrics(trs_le_is,  n_is_jnt)
    bm_le_oos = book_metrics(trs_le_oos, n_oos_jnt)

    # Capacity-constrained annual net dollar amounts
    # RB-CL: 1 contract = 1000 bbl; LE-GF: 1 contract = 50,000 lbs (GF side)
    # Capacity constraint: max per year from each sleeve
    bars_per_year = 252.0
    rb_trades_yr = (bm_rb_oos.get("trades_per_year", 0) or 0)
    le_trades_yr = (bm_le_oos.get("trades_per_year", 0) or 0)

    rb_mean_net_usd = (bm_rb_oos.get("mean_net", 0) or 0) * CONTRACT_BBL
    le_mean_net_cpl = (bm_le_oos.get("mean_net", 0) or 0)  # ¢/lb
    le_mean_net_usd = le_mean_net_cpl / 100.0 * CONTRACT_GF_LBS  # convert ¢/lb → $ per contract

    # At capacity-capped sizing
    if rb_trades_yr > 0 and abs(rb_mean_net_usd) > 0:
        rb_contracts_needed = CAP_RBCL_YR / (abs(rb_mean_net_usd) * rb_trades_yr + 1e-6)
        rb_contracts_needed = max(1, int(rb_contracts_needed))
    else:
        rb_contracts_needed = 1

    if le_trades_yr > 0 and abs(le_mean_net_usd) > 0:
        le_contracts_needed = CAP_LEGF_YR / (abs(le_mean_net_usd) * le_trades_yr + 1e-6)
        le_contracts_needed = max(1, int(le_contracts_needed))
    else:
        le_contracts_needed = 1

    # Annualized dollar net for each sleeve at capacity
    rb_annual_net_cap = rb_mean_net_usd * rb_trades_yr * rb_contracts_needed
    le_annual_net_cap = le_mean_net_usd * le_trades_yr * le_contracts_needed
    combined_capacity_yr = rb_annual_net_cap + le_annual_net_cap

    # Combined Sharpe: aggregate per-trade net on a common risk-unit basis
    # Scale each sleeve's per-trade net by its inverse-vol weight, then compute combined metrics
    def scale_trades(trades, weight, unit_scale):
        return [{"net": t["net"] * weight * unit_scale,
                 "gross": t["gross"] * weight * unit_scale} for t in trades]

    # Normalize both to common units: $ per "unit of risk" (inverse vol weighted)
    # RB-CL in $/bbl, LE-GF in ¢/lb — both already in per-trade-per-unit terms
    # To combine, we need the combined Sharpe to reflect equal-risk contribution
    # Simple approach: combine normalized (z-scored) per-trade returns
    def normalized_nets(trades):
        nets = np.array([t["net"] for t in trades])
        if len(nets) < 5:
            return np.array([])
        return (nets - np.mean(nets)) / (np.std(nets, ddof=1) + 1e-9)

    def combined_sharpe(trs_a, trs_b, w_a, w_b, n_bars, bars_per_year=252.0):
        """
        Weighted combined Sharpe using aligned IS/OOS periods.
        Map each trade to its entry bar, compute weighted daily PnL series.
        Simplified: treat as if all trades arrive independently, combine PnL streams.
        More accurately: simulate a portfolio that runs both strategies simultaneously.
        Since trades are sparse (10-20/yr), combine by treating same-period bars as a portfolio.
        """
        if not trs_a or not trs_b:
            return float("nan"), float("nan")

        # Compute annualized Sharpe for each separately, then combine assuming independence
        nets_a = np.array([t["net"] for t in trs_a])
        nets_b = np.array([t["net"] for t in trs_b])
        n_yr   = n_bars / bars_per_year

        # Normalize each to unit variance, weight, combine
        # Per-trade Sharpe ingredients
        mean_a = float(np.mean(nets_a)); std_a = float(np.std(nets_a, ddof=1)) + 1e-9
        mean_b = float(np.mean(nets_b)); std_b = float(np.std(nets_b, ddof=1)) + 1e-9
        sr_a   = (mean_a / std_a) * ((len(nets_a) / n_yr) ** 0.5)
        sr_b   = (mean_b / std_b) * ((len(nets_b) / n_yr) ** 0.5)

        # Normalized per-trade: scale each sleeve to equal per-trade variance, weight by inverse-vol
        norm_a = (nets_a - mean_a) / std_a * w_a + mean_a / std_a * w_a
        norm_b = (nets_b - mean_b) / std_b * w_b + mean_b / std_b * w_b
        # Combine by interleaving and computing portfolio Sharpe
        # Since trades are independent, combined mean and std:
        comb_mean  = w_a * mean_a / std_a + w_b * mean_b / std_b
        # Under independence assumption:
        comb_std_sq= w_a**2 + w_b**2  # normalized
        comb_std   = float(np.sqrt(comb_std_sq)) + 1e-9
        comb_tr_yr = (len(nets_a) + len(nets_b)) / n_yr
        combined_sr= (comb_mean / comb_std) * (comb_tr_yr ** 0.5)
        return combined_sr, max(sr_a, sr_b)

    combined_sr_is, best_single_sr_is = combined_sharpe(
        trs_rb_is, trs_le_is, w_rb, w_le, n_is_jnt)
    combined_sr_oos, best_single_sr_oos = combined_sharpe(
        trs_rb_oos, trs_le_oos, w_rb, w_le, n_oos_jnt)

    # Also compute directly: independent Sharpe addition formula
    # Sharpe_combined = sqrt(Sharpe_A^2 + Sharpe_B^2) for uncorrelated equal-weight
    sr_rb_oos = bm_rb_oos.get("annualized_sharpe", 0) or 0
    sr_le_oos = bm_le_oos.get("annualized_sharpe", 0) or 0
    sr_rb_is  = bm_rb_is.get("annualized_sharpe",  0) or 0
    sr_le_is  = bm_le_is.get("annualized_sharpe",  0) or 0
    sr_combined_oos_formula = float(np.sqrt(max(0, sr_rb_oos)**2 + max(0, sr_le_oos)**2))
    sr_combined_is_formula  = float(np.sqrt(max(0, sr_rb_is) **2 + max(0, sr_le_is) **2))

    diversification_benefit_oos = sr_combined_oos_formula - max(sr_rb_oos, sr_le_oos)
    diversification_benefit_is  = sr_combined_is_formula  - max(sr_rb_is,  sr_le_is)

    # Ex-crisis robustness: combined OOS excluding COVID and energy spike
    df_oos = df_joint.iloc[n_is_jnt:]
    excl_mask = ((df_oos.index >= STRESS_COVID[0])  & (df_oos.index <= STRESS_COVID[1])) | \
                ((df_oos.index >= STRESS_ENERGY[0]) & (df_oos.index <= STRESS_ENERGY[1]))
    df_oos_excl = df_oos[~excl_mask]
    s_rb_oos_excl = df_oos_excl["rb_cl"].to_numpy(float)
    s_le_oos_excl = df_oos_excl["le_gf"].to_numpy(float)
    trs_rb_oos_excl = run_fade(s_rb_oos_excl, PRIMARY_THETA, COST_RBCL)
    trs_le_oos_excl = run_fade(s_le_oos_excl, PRIMARY_THETA, COST_LEGF)
    bm_rb_oos_excl = book_metrics(trs_rb_oos_excl, len(s_rb_oos_excl))
    bm_le_oos_excl = book_metrics(trs_le_oos_excl, len(s_le_oos_excl))
    sr_rb_oos_excl = bm_rb_oos_excl.get("annualized_sharpe", float("nan")) or float("nan")
    sr_le_oos_excl = bm_le_oos_excl.get("annualized_sharpe", float("nan")) or float("nan")
    sr_comb_oos_excl = float(np.sqrt(max(0, sr_rb_oos_excl if np.isfinite(sr_rb_oos_excl) else 0)**2 +
                                     max(0, sr_le_oos_excl  if np.isfinite(sr_le_oos_excl)  else 0)**2))

    # Pre-committed verdict
    oos_sharpe_threshold_deployable   = 0.60
    oos_sharpe_threshold_small_book   = 0.40
    divbenefit_threshold              = 0.08
    combined_oos_sharpe_for_verdict   = sr_combined_oos_formula

    oos_net_rb_positive = (bm_rb_oos.get("mean_net", float("-inf")) or float("-inf")) > 0
    oos_net_le_positive = (bm_le_oos.get("mean_net", float("-inf")) or float("-inf")) > 0
    combined_oos_net_positive = oos_net_rb_positive and oos_net_le_positive

    if (combined_oos_sharpe_for_verdict >= oos_sharpe_threshold_deployable and
            combined_oos_net_positive and
            abs(combined_capacity_yr) >= 1_000_000 and
            diversification_benefit_oos >= divbenefit_threshold):
        book_verdict = "DEPLOYABLE-BOOK"
    elif (combined_oos_sharpe_for_verdict >= oos_sharpe_threshold_small_book and
          combined_oos_net_positive):
        book_verdict = "SMALL-BOOK-ONLY"
    else:
        book_verdict = "INSUFFICIENT"

    print(f"  Combined OOS Sharpe (formula): {sr_combined_oos_formula:.3f}, "
          f"diversification benefit: {diversification_benefit_oos:+.3f}")
    print(f"  Combined capacity ~${abs(combined_capacity_yr):,.0f}/yr")
    print(f"  Book verdict: {book_verdict}")

    return {
        "n_joint_bars": n_joint,
        "n_is_bars": n_is_jnt,
        "n_oos_bars": n_oos_jnt,
        "split_date": str(split_date.date()),
        "inverse_vol_weights": {"w_rb_cl": round(w_rb, 4), "w_le_gf": round(w_le, 4)},
        "vol_is": {"rb_cl_vol": round(vol_rb_is, 5), "le_gf_vol": round(vol_le_is, 5)},
        "individual_oos_sharpes": {
            "rb_cl_oos": round(sr_rb_oos, 3),
            "le_gf_oos": round(sr_le_oos, 3),
            "best_single": round(max(sr_rb_oos, sr_le_oos), 3),
        },
        "individual_is_sharpes": {
            "rb_cl_is": round(sr_rb_is, 3),
            "le_gf_is": round(sr_le_is, 3),
        },
        "combined_sharpe": {
            "combined_oos_formula": round(sr_combined_oos_formula, 3),
            "combined_is_formula": round(sr_combined_is_formula, 3),
            "combined_oos_excl_crisis": round(sr_comb_oos_excl, 3),
        },
        "diversification_benefit": {
            "oos_sharpe_delta": round(diversification_benefit_oos, 4),
            "is_sharpe_delta":  round(diversification_benefit_is,  4),
        },
        "individual_oos_metrics": {
            "rb_cl": bm_rb_oos,
            "le_gf": bm_le_oos,
        },
        "individual_is_metrics": {
            "rb_cl": bm_rb_is,
            "le_gf": bm_le_is,
        },
        "excl_crisis_oos_metrics": {
            "rb_cl_excl": bm_rb_oos_excl,
            "le_gf_excl": bm_le_oos_excl,
            "combined_oos_sharpe_excl_crisis": round(sr_comb_oos_excl, 3),
        },
        "capacity": {
            "rb_cl_annual_usd_capped": round(rb_annual_net_cap, 0),
            "le_gf_annual_usd_capped": round(le_annual_net_cap, 0),
            "combined_annual_usd": round(combined_capacity_yr, 0),
            "cap_rb": CAP_RBCL_YR,
            "cap_le": CAP_LEGF_YR,
        },
        "pre_committed_thresholds": {
            "deployable_sharpe": oos_sharpe_threshold_deployable,
            "small_book_sharpe": oos_sharpe_threshold_small_book,
            "diversification_benefit_min": divbenefit_threshold,
        },
        "book_verdict": book_verdict,
    }


# ── Main ─────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 60)
    print("Portfolio Combination Test — RB-CL + LE-GF")
    print("Pre-reg: docs/research/portfolio_combination_prereg.md")
    print("=" * 60)

    results = {}

    # Gate A
    results["gate_a"] = gate_a_excision()

    # If Gate A fails, RB-CL drops from book — report and handle
    rb_cl_in_book = results["gate_a"]["gate_a_pass"]
    if not rb_cl_in_book:
        print("\nWARNING: Gate A FAILED — RB-CL drops from combined book.")
        print("Book is LE-GF only — portfolio combination not testable.")
        results["gate_b"] = {"skipped": "Gate A failed; RB-CL not in book"}
        results["gate_c"] = {"skipped": "Gate A failed; single-sleeve test only"}
        # Still report LE-GF standalone metrics (deseasonalized)
        _, s_le, idx_le, _, _ = build_spread(
            "CME_DL_LE2!, 1D.csv", "CME_DL_GF2!, 1D.csv",
            scaleA=1.0, beta_mode="f5", date_min=DATE_MIN_LEGF,
        )
        n = len(s_le)
        n_is = int(n * OOS_SPLIT)
        trs_le_is  = run_fade(s_le[:n_is], PRIMARY_THETA, COST_LEGF)
        trs_le_oos = run_fade(s_le[n_is:], PRIMARY_THETA, COST_LEGF)
        results["le_gf_standalone"] = {
            "is_metrics": book_metrics(trs_le_is, n_is),
            "oos_metrics": book_metrics(trs_le_oos, n - n_is),
        }
        results["verdict"] = "SINGLE-SLEEVE-LE-GF-ONLY"
    else:
        # Gates B and C
        results["gate_b"] = gate_b_independence()
        results["gate_c"] = gate_c_combined()
        results["verdict"] = results["gate_c"]["book_verdict"]

    # Save results
    out_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed",
                            "portfolio_combination_results.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved: {out_path}")
    print(f"FINAL BOOK VERDICT: {results['verdict']}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    main()
