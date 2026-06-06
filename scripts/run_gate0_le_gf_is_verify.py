"""
Gate 0 — LE-GF IS-Only Anchor Verification
Pre-registration: docs/research/gate0_le_gf_is_verify_prereg.md (written BEFORE this script).

Tests whether LE-GF's VR sub-diffusion survives IS-only (not full-period) evaluation.
Doc-45 lesson: full-period VR can manufacture significance that IS alone doesn't support.
"""
from __future__ import annotations
import sys, os, json, warnings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

try:
    from app.services.analytics_arm_a_v2 import deseasonalize_causal, increment_jump_mask
    from app.services.analytics_arm_a_v2_beta import presample_ols_beta
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

# ── Frozen pre-reg constants ────────────────────────────────────────────────────
SEED_GATE0      = 20260606
OOS_SPLIT       = 0.70
PRE_FRAC        = 0.25
JUMP_K          = 8.0
JUMP_W          = 60
LB              = 60
MH              = 40
PRIMARY_THETA   = 1.0
COST_LEGF       = 0.20          # ¢/lb
NS_SURR         = 500
DATE_MIN_LEGF   = "1995-01-01"
DATE_MAX        = "2026-06-03"
VR_Q_PRIMARY    = 20
VR_Q_SECONDARY  = [5, 10, 40]
PASS_P_RW       = 0.050
WARN_P_OTHER    = 0.100

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw",
                    "more-mean-reversion-data")


# ── Data loading ────────────────────────────────────────────────────────────────

def load_u(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["ts"] = pd.to_datetime(df["time"].astype(np.int64), unit="s", utc=True)
    df["ts"] = df["ts"].dt.normalize().dt.tz_localize(None)  # date-only, no tz
    return df.dropna(subset=["ts"]).sort_values("ts").drop_duplicates("ts", keep="last").set_index("ts")


# ── Spread construction ──────────────────────────────────────────────────────────

def build_le_gf_spread() -> tuple[np.ndarray, np.ndarray, pd.DatetimeIndex, float]:
    """
    Returns (s_raw_clean, s_ds_clean, idx, beta_val).
    F5: presample OLS β (first PRE_FRAC), frozen thereafter.
    """
    A_raw = load_u(os.path.join(DATA, "CME_DL_LE2!, 1D.csv"))
    B_raw = load_u(os.path.join(DATA, "CME_DL_GF2!, 1D.csv"))
    A_raw = A_raw[(A_raw.index >= DATE_MIN_LEGF) & (A_raw.index <= DATE_MAX)]
    B_raw = B_raw[(B_raw.index >= DATE_MIN_LEGF) & (B_raw.index <= DATE_MAX)]
    merged = A_raw[["close"]].join(B_raw[["close"]], how="inner",
                                   lsuffix="_a", rsuffix="_b").dropna()
    idx = merged.index
    A = merged.close_a.to_numpy(float)
    B = merged.close_b.to_numpy(float)
    n = len(idx)

    beta = presample_ols_beta(A, B, pre_sample_fraction=PRE_FRAC)
    beta_val = float(np.nanmedian(beta[int(n * PRE_FRAC):]))

    s_raw_arr = np.where(np.isfinite(beta), A - beta * B, np.nan)
    s_ds_arr  = deseasonalize_causal(s_raw_arr, idx)

    roll = increment_jump_mask(s_raw_arr, k=JUMP_K, window=JUMP_W)
    inv  = ~np.isfinite(beta) | roll

    s_raw_clean = np.where(inv, np.nan, s_raw_arr)
    s_ds_clean  = np.where(inv, np.nan, s_ds_arr)

    return s_raw_clean, s_ds_clean, idx, beta_val


# ── VR helpers ───────────────────────────────────────────────────────────────────

def vr_q(s: np.ndarray, q: int = 20) -> float:
    x = s[np.isfinite(s)]
    n = len(x)
    if n < q + 20:
        return float("nan")
    dr = np.diff(x)
    var1 = np.var(dr, ddof=1)
    if var1 <= 1e-14:
        return float("nan")
    ret_q = x[q:] - x[:-q]
    varq  = np.var(ret_q, ddof=1)
    return float(varq / (q * var1))


def surrogate_pval(s: np.ndarray, q: int, n_surr: int, seed: int,
                   null_type: str = "rw") -> tuple[float, float]:
    real_vr = vr_q(s, q)
    if not np.isfinite(real_vr):
        return float("nan"), float("nan")
    x   = s[np.isfinite(s)]
    n   = len(x)
    dr  = np.diff(x)
    rng = np.random.default_rng(seed)
    surr_vrs = []

    if null_type == "rw":
        mu_ = float(np.mean(dr))
        sig_ = float(np.std(dr, ddof=1))
        for _ in range(n_surr):
            path = np.concatenate([[0.0], np.cumsum(rng.normal(mu_, sig_, n - 1))])
            v = vr_q(path, q)
            if np.isfinite(v):
                surr_vrs.append(v)

    elif null_type == "garch":
        try:
            from arch import arch_model
            am = arch_model(dr, vol="GARCH", p=1, q=1, dist="normal", rescale=True)
            res = am.fit(disp="off", show_warning=False)
            scale = res.scale
            for _ in range(n_surr):
                sim = res.model.simulate(res.params, nobs=n - 1)
                rets = np.array(sim["data"]) / scale
                path = np.concatenate([[0.0], np.cumsum(rets)])
                v = vr_q(path, q)
                if np.isfinite(v):
                    surr_vrs.append(v)
        except Exception:
            # fallback: GARCH not available or failed — use heteroskedastic RW
            sd_roll = pd.Series(dr).rolling(20, min_periods=5).std().fillna(method="bfill").to_numpy()
            for _ in range(n_surr):
                rets = rng.normal(np.mean(dr), sd_roll)
                path = np.concatenate([[0.0], np.cumsum(rets)])
                v = vr_q(path, q)
                if np.isfinite(v):
                    surr_vrs.append(v)

    elif null_type == "ma1":
        # MA(1) on first differences
        from scipy.signal import lfilter
        theta_ma = float(np.corrcoef(dr[:-1], dr[1:])[0, 1])  # moment estimate
        theta_ma = np.clip(theta_ma, -0.99, 0.99)
        sig_ = float(np.std(dr, ddof=1))
        for _ in range(n_surr):
            eps = rng.normal(0, sig_, n)
            ma1 = lfilter([1, theta_ma], [1], eps)  # MA(1) process
            path = np.concatenate([[0.0], np.cumsum(ma1[1:])])
            v = vr_q(path, q)
            if np.isfinite(v):
                surr_vrs.append(v)

    elif null_type == "ou":
        # OU: estimate θ_ou, μ_ou, σ_ou from spread levels
        x_ou = x - x.mean()
        if len(x_ou) > 10:
            dt = 1.0
            # MLE-ish: regress x_t on x_{t-1}
            phi = float(np.corrcoef(x_ou[:-1], x_ou[1:])[0, 1])
            phi = np.clip(phi, -0.9999, 0.9999)
            theta_ou = -np.log(phi) / dt if phi > 0 else 0.01
            sig_ou   = float(np.std(x_ou[1:] - phi * x_ou[:-1], ddof=1))
            mu_ou    = float(x.mean())
            for _ in range(n_surr):
                path = np.empty(n)
                path[0] = x[0]
                eps = rng.normal(0, sig_ou, n - 1)
                for t in range(1, n):
                    path[t] = path[t-1] + theta_ou * (mu_ou - path[t-1]) * dt + eps[t-1]
                v = vr_q(path, q)
                if np.isfinite(v):
                    surr_vrs.append(v)
        else:
            return float("nan"), float("nan")
    else:
        raise ValueError(f"unknown null_type: {null_type}")

    if not surr_vrs:
        return real_vr, float("nan")
    pv = (1.0 + sum(v <= real_vr for v in surr_vrs)) / (len(surr_vrs) + 1.0)
    return real_vr, float(pv)


# ── Economic fade ────────────────────────────────────────────────────────────────

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
    return {
        "n_trades": len(trades),
        "n_years":  round(n_yrs, 1),
        "trades_per_year": round(t_yr, 1),
        "mean_gross": round(float(np.mean(gross)), 5),
        "mean_net":   round(float(np.mean(nets)),  5),
        "median_net": round(float(np.median(nets)), 5),
        "std_net":    round(float(np.std(nets, ddof=1)), 5),
        "annualized_sharpe": round(sharpe, 3),
        "max_drawdown_units": round(float(np.min(dd)), 4),
        "hit_rate": round(float(np.mean(nets > 0)), 3),
    }


# ── Main ─────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("Gate 0 — LE-GF IS-Only Anchor Verification")
    print("Pre-reg: docs/research/gate0_le_gf_is_verify_prereg.md")
    print("=" * 60)

    # Build spread
    s_raw, s_ds, idx, beta_val = build_le_gf_spread()
    n_total = len(idx)
    n_is    = int(n_total * OOS_SPLIT)
    n_oos   = n_total - n_is

    s_raw_full = s_raw
    s_raw_is   = s_raw[:n_is]
    s_raw_oos  = s_raw[n_is:]
    s_ds_is    = s_ds[:n_is]
    idx_is     = idx[:n_is]
    idx_oos    = idx[n_is:]

    print(f"\nDataset: {n_total} bars  |  IS: {n_is} ({idx_is[0].date()} – {idx_is[-1].date()})  |  OOS: {n_oos} ({idx_oos[0].date()} – {idx_oos[-1].date()})")
    print(f"β (F5, frozen after pre-sample): {beta_val:.4f}")
    print(f"IS valid bars (raw, non-NaN): {np.sum(np.isfinite(s_raw_is))}")

    results: dict = {
        "meta": {
            "instrument": "LE-GF F5",
            "n_total": n_total,
            "n_is": n_is,
            "n_oos": n_oos,
            "is_start": str(idx_is[0].date()),
            "is_end":   str(idx_is[-1].date()),
            "oos_start": str(idx_oos[0].date()),
            "oos_end":   str(idx_oos[-1].date()),
            "beta_val": round(beta_val, 5),
        }
    }

    # ── PRIMARY GATE: IS-only VR(20) vs all surrogates ──────────────────────────
    print(f"\n--- PRIMARY GATE: IS-only VR(20) surrogate tests (n_surr={NS_SURR}) ---")
    surr_results = {}
    for null_t, seed_offset in [("rw", 0), ("garch", 1), ("ma1", 2), ("ou", 3)]:
        vr_val, pv = surrogate_pval(s_raw_is, VR_Q_PRIMARY, NS_SURR,
                                     SEED_GATE0 + seed_offset, null_t)
        surr_results[null_t] = {"vr": round(vr_val, 4), "p": round(pv, 4)}
        flag = ""
        if null_t == "rw":
            flag = "  *** GATE ***"
            if pv < PASS_P_RW:
                flag += f"  PASS (p={pv:.4f} < {PASS_P_RW})"
            else:
                flag += f"  FAIL (p={pv:.4f} ≥ {PASS_P_RW})"
        print(f"  null={null_t:6s}  VR(20)={vr_val:.4f}  p={pv:.4f}{flag}")
    results["is_vr_primary"] = surr_results

    # ── SECONDARY: multi-lag VR profile IS-only ──────────────────────────────────
    print(f"\n--- SECONDARY: IS-only multi-lag VR profile (RW surrogate) ---")
    vr_profile = {}
    for q in [5, 10, 20, 40]:
        vr_val, pv = surrogate_pval(s_raw_is, q, NS_SURR, SEED_GATE0 + 10, "rw")
        vr_profile[f"q{q}"] = {"vr": round(vr_val, 4), "p_rw": round(pv, 4)}
        print(f"  VR({q:2d})={vr_val:.4f}  p_rw={pv:.4f}")
    results["is_vr_profile"] = vr_profile

    # ── COMPARISON: full-period vs IS-only (doc-45 lens) ─────────────────────────
    print(f"\n--- COMPARISON: Full-period vs IS-only VR(20) ---")
    vr_full, p_full = surrogate_pval(s_raw_full, VR_Q_PRIMARY, NS_SURR, SEED_GATE0 + 20, "rw")
    vr_is,   p_is   = surr_results["rw"]["vr"], surr_results["rw"]["p"]
    print(f"  Full-period ({n_total} bars): VR(20)={vr_full:.4f}  p_rw={p_full:.4f}")
    print(f"  IS-only     ({n_is} bars):  VR(20)={vr_is:.4f}  p_rw={p_is:.4f}")
    results["comparison"] = {
        "full_period": {"n": n_total, "vr20": round(vr_full, 4), "p_rw": round(p_full, 4)},
        "is_only":     {"n": n_is,    "vr20": round(vr_is,   4), "p_rw": round(p_is,   4)},
    }

    # ── POWER ANALYSIS ──────────────────────────────────────────────────────────
    n_valid_is = int(np.sum(np.isfinite(s_raw_is)))
    se_is = (2 * VR_Q_PRIMARY / n_valid_is) ** 0.5
    z_stat_is = (vr_is - 1.0) / se_is
    from scipy.stats import norm as _norm
    power_is = float(_norm.cdf(-1.645 - z_stat_is) + _norm.cdf(z_stat_is + 1.645))  # approx
    power_is = float(_norm.cdf(z_stat_is + 1.645))  # one-sided
    print(f"\n--- POWER ANALYSIS (IS-only) ---")
    print(f"  n_valid_is={n_valid_is}  SE={se_is:.4f}  z={z_stat_is:.3f}  "
          f"power@α=0.05 (one-sided) ≈ {power_is:.2f}")
    results["power_analysis"] = {
        "n_valid_is": n_valid_is,
        "se": round(se_is, 5),
        "z_stat": round(z_stat_is, 3),
        "power_at_alpha005": round(power_is, 3),
    }

    # ── IS FADE ECONOMICS (deseasonalized, primary θ) ───────────────────────────
    print(f"\n--- IS FADE ECONOMICS (deseasonalized, θ={PRIMARY_THETA}, LB={LB}, MH={MH}) ---")
    trades_is_ds = run_fade(s_ds_is, PRIMARY_THETA, COST_LEGF)
    bm_is_ds = book_metrics(trades_is_ds, n_is)
    print(f"  IS DS: n_trades={bm_is_ds.get('n_trades',0)}  mean_net={bm_is_ds.get('mean_net','n/a')}  "
          f"Sharpe={bm_is_ds.get('annualized_sharpe','n/a')}")
    results["is_economics"] = bm_is_ds

    # IS fade on raw spread (sanity)
    trades_is_raw = run_fade(s_raw_is, PRIMARY_THETA, COST_LEGF)
    bm_is_raw = book_metrics(trades_is_raw, n_is)
    print(f"  IS RAW: n_trades={bm_is_raw.get('n_trades',0)}  mean_net={bm_is_raw.get('mean_net','n/a')}  "
          f"Sharpe={bm_is_raw.get('annualized_sharpe','n/a')}")
    results["is_economics_raw"] = bm_is_raw

    # ── GATE VERDICT ────────────────────────────────────────────────────────────
    p_rw_is = surr_results["rw"]["p"]
    gate_pass = p_rw_is < PASS_P_RW
    print(f"\n{'='*60}")
    print(f"GATE 0 VERDICT: {'PASS' if gate_pass else 'FAIL'}")
    print(f"  IS-only VR(20) p_rw = {p_rw_is:.4f}  (threshold = {PASS_P_RW})")
    if gate_pass:
        print(f"  LE-GF anchor HOLDS. Proceed to Track 1 + Track 2.")
    else:
        print(f"  STOP. Escalate to owner. LE-GF IS-only sub-diffusion not confirmed.")
        print(f"  Do NOT start Track 1, Track 2, or any build.")
    results["gate_verdict"] = {
        "pass": gate_pass,
        "p_rw_is": round(p_rw_is, 4),
        "threshold": PASS_P_RW,
        "action": "PROCEED" if gate_pass else "STOP_ESCALATE",
    }

    # ── Save results ────────────────────────────────────────────────────────────
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                            "data", "processed", "gate0_le_gf_is_verify_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved: {out_path}")


if __name__ == "__main__":
    main()
