"""
T2.5 — Trend-Death Detector: Minimal First Test
Pre-registration: docs/research/t2_5_trend_death_prereg.md (written BEFORE this script).

Optimization note: test statistic uses raw forward min-VR (fast, no per-bar surrogates).
Habitat scores computed for fire bars only (small set). Permutation test is valid since it
conditions on the same instrument's own dynamics. Per pre-reg §4, Δ = mean(habitat|fire) −
mean(habitat|permuted); here we use min-VR as the quantity (lower = more sub-diffusive = better).
So Δ_vr = mean(min-VR|permuted) - mean(min-VR|fire) > 0 means fires are more MR.
"""
from __future__ import annotations
import sys, os, json, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import numpy as np
import pandas as pd
from scipy.stats import linregress

# ── Frozen pre-reg constants ────────────────────────────────────────────────────
SEED_T25          = 20260606
W_PRIMARY         = 60
W_ROBUST          = 120
T_STAT_ESTABLISH  = 2.0
T_STAT_DYING      = 0.5
K_FLIP            = 10
H_FORWARD         = 40
VR_QS             = [5, 10, 20]
NS_NULL_SCORE     = 200   # for habitat score on fire bars only
N_PERM            = 2000
OOS_SPLIT         = 0.70
MIN_BARS          = 500
EFFECT_FLOOR      = 0.10  # mean(min-VR | all) - mean(min-VR | fire) ≥ 0.10 for hit
P_HIT             = 0.05
P_PROGRAMME       = 0.0125  # Bonferroni: 0.05 / 4 instruments
MAJORITY_N        = 3

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_MRM = os.path.join(BASE, "..", "data", "raw", "more-mean-reversion-data")
DATA_RAW = os.path.join(BASE, "..", "data", "raw")


# ── Data loaders ─────────────────────────────────────────────────────────────────

def load_unix_csv(path: str) -> pd.Series:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["ts"] = pd.to_datetime(df["time"].astype(np.int64), unit="s", utc=True)
    df["ts"] = df["ts"].dt.normalize().dt.tz_localize(None)
    df = df.dropna(subset=["ts"]).sort_values("ts").drop_duplicates("ts", keep="last")
    return df.set_index("ts")["close"].astype(float)


def load_adanient() -> pd.Series:
    df = pd.read_csv(os.path.join(DATA_RAW, "adanient.csv"))
    df.columns = [c.strip().lower() for c in df.columns]
    df["ts"] = pd.to_datetime(df["date"], dayfirst=True)
    df = df.dropna(subset=["ts"]).sort_values("ts").drop_duplicates("ts", keep="last")
    return df.set_index("ts")["close"].astype(float)


def load_aapl_daily() -> pd.Series:
    df = pd.read_csv(os.path.join(DATA_RAW, "aapl_60.csv"))
    df.columns = [c.strip().lower() for c in df.columns]
    df["ts"] = pd.to_datetime(df["time"], utc=True)
    df = df.dropna(subset=["ts"]).sort_values("ts")
    df["date"] = df["ts"].dt.normalize().dt.tz_localize(None)
    daily = df.groupby("date")["close"].last().astype(float)
    daily.index.name = "ts"
    return daily


INSTRUMENTS = {
    "CL":       lambda: load_unix_csv(os.path.join(DATA_MRM, "NYMEX_DL_CL1!, 1D.csv")),
    "SPX":      lambda: load_unix_csv(os.path.join(DATA_MRM, "SP_SPX, 1D (1).csv")),
    "ADANIENT": load_adanient,
    "AAPL":     load_aapl_daily,
}


# ── VR helpers ───────────────────────────────────────────────────────────────────

def vr_q(x: np.ndarray, q: int) -> float:
    x = x[np.isfinite(x)]
    n = len(x)
    if n < q + 5:
        return float("nan")
    dr = np.diff(x)
    var1 = np.var(dr, ddof=1)
    if var1 <= 1e-14:
        return float("nan")
    ret_q = x[q:] - x[:-q]
    return float(np.var(ret_q, ddof=1) / (q * var1))


def min_vr(x: np.ndarray) -> float:
    vals = [vr_q(x, q) for q in VR_QS]
    vals = [v for v in vals if np.isfinite(v)]
    return min(vals) if vals else float("nan")


def habitat_score_single(x: np.ndarray, seed: int) -> float:
    """Compute habitat score for a single window. Used for fire bars only."""
    real_mvr = min_vr(x)
    if not np.isfinite(real_mvr):
        return float("nan")
    x_fin = x[np.isfinite(x)]
    n = len(x_fin)
    if n < max(VR_QS) + 5:
        return float("nan")
    dr = np.diff(x_fin)
    mu_dr  = float(np.mean(dr))
    sig_dr = float(np.std(dr, ddof=1))
    if sig_dr <= 1e-12:
        return float("nan")
    rng = np.random.default_rng(seed)
    null_mvrs = []
    for _ in range(NS_NULL_SCORE // 2):
        path = np.concatenate([[x_fin[0]], x_fin[0] + np.cumsum(rng.normal(mu_dr, sig_dr, n - 1))])
        v = min_vr(path)
        if np.isfinite(v):
            null_mvrs.append(v)
    if len(dr) > 5:
        acf1 = float(np.corrcoef(dr[:-1], dr[1:])[0, 1])
        theta_ma = np.clip(acf1, -0.95, 0.95)
    else:
        theta_ma = 0.0
    for _ in range(NS_NULL_SCORE // 2):
        eps = rng.normal(0, sig_dr, n + 1)
        ma1 = eps[1:] + theta_ma * eps[:-1]
        std_ma1 = np.std(ma1, ddof=1)
        if std_ma1 > 1e-12:
            ma1 *= sig_dr / std_ma1
        path = np.concatenate([[x_fin[0]], x_fin[0] + np.cumsum(ma1[:n - 1])])
        v = min_vr(path)
        if np.isfinite(v):
            null_mvrs.append(v)
    if not null_mvrs:
        return float("nan")
    return 100.0 * float(np.mean(np.array(null_mvrs) >= real_mvr))


# ── Stage-1 signal ────────────────────────────────────────────────────────────────

def compute_rolling_trend(log_px: np.ndarray, W: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = len(log_px)
    beta  = np.full(n, np.nan)
    tstat = np.full(n, np.nan)
    resid = np.full(n, np.nan)
    t_idx = np.arange(W, dtype=float)
    for t in range(W, n):
        y = log_px[t - W: t]
        if not np.all(np.isfinite(y)):
            continue
        slope, intercept, r, p, se = linregress(t_idx, y)
        beta[t]  = slope
        tstat[t] = slope / (se + 1e-15)
        resid[t] = y[-1] - (intercept + slope * (W - 1))
    return beta, tstat, resid


def fire_primary(beta: np.ndarray, tstat: np.ndarray, resid: np.ndarray, W: int,
                 n_eval: int) -> np.ndarray:
    """Primary: condition 1 (slope death) AND condition 2 (residual flip)."""
    fires = np.zeros(n_eval, dtype=bool)
    for t in range(W, n_eval - H_FORWARD):
        if not np.isfinite(tstat[t]) or not np.isfinite(tstat[t - W]):
            continue
        established = abs(tstat[t - W]) >= T_STAT_ESTABLISH
        dying = (abs(tstat[t]) < T_STAT_DYING or
                 (np.isfinite(beta[t]) and np.isfinite(beta[t - W]) and
                  np.sign(beta[t]) != np.sign(beta[t - W])))
        if not (established and dying):
            continue
        r_window = resid[max(0, t - K_FLIP + 1): t + 1]
        r_fin = r_window[np.isfinite(r_window)]
        if len(r_fin) >= 2 and np.any(np.diff(np.sign(r_fin)) != 0):
            fires[t] = True
    return fires


def fire_ablation(beta: np.ndarray, tstat: np.ndarray, W: int, n_eval: int) -> np.ndarray:
    """Ablation: condition 1 only (slope death)."""
    fires = np.zeros(n_eval, dtype=bool)
    for t in range(W, n_eval - H_FORWARD):
        if not np.isfinite(tstat[t]) or not np.isfinite(tstat[t - W]):
            continue
        established = abs(tstat[t - W]) >= T_STAT_ESTABLISH
        dying = (abs(tstat[t]) < T_STAT_DYING or
                 (np.isfinite(beta[t]) and np.isfinite(beta[t - W]) and
                  np.sign(beta[t]) != np.sign(beta[t - W])))
        if established and dying:
            fires[t] = True
    return fires


# ── Forward min-VR (vectorized for all eligible bars) ───────────────────────────

def compute_all_forward_mvrs(px_log: np.ndarray, bar_range: range) -> tuple[np.ndarray, list]:
    """
    Pre-compute forward min-VR for all eligible bars (fast, no surrogates).
    Returns (mvrs array indexed same as bar_range, list of eligible bar indices).
    """
    eligible = []
    mvrs = []
    for t in bar_range:
        fwd = np.exp(px_log[t + 1: t + 1 + H_FORWARD])
        if len(fwd) < H_FORWARD:
            continue
        mv = min_vr(fwd)
        if np.isfinite(mv):
            eligible.append(t)
            mvrs.append(mv)
    return np.array(mvrs), eligible


# ── Permutation test ──────────────────────────────────────────────────────────────

def permutation_test(all_mvrs: np.ndarray, fire_idx_in_eligible: list,
                     seed: int) -> dict:
    """
    Test: do fire bars have lower forward min-VR (more MR) than chance?
    Δ = mean(min-VR|all) - mean(min-VR|fire)  [positive = fires more MR]
    Permutation: randomly shuffle fire labels among eligible bars.
    """
    n_fire = len(fire_idx_in_eligible)
    n_elig = len(all_mvrs)
    unc_mean = float(np.nanmean(all_mvrs))

    if n_fire < 3 or n_elig < n_fire + 5:
        return {
            "n_fire": n_fire, "n_eligible": n_elig,
            "fire_mean_mvr": float("nan"), "unc_mean_mvr": round(unc_mean, 4),
            "delta_vr": float("nan"), "p_perm": float("nan"),
            "insufficient_fires": True,
        }

    fire_mvrs = all_mvrs[fire_idx_in_eligible]
    fire_mean = float(np.nanmean(fire_mvrs))
    delta_obs = unc_mean - fire_mean  # positive = fires have lower (more MR) min-VR

    rng = np.random.default_rng(seed)
    null_deltas = []
    for _ in range(N_PERM):
        perm_fire = rng.choice(n_elig, size=n_fire, replace=False)
        perm_mean = float(np.nanmean(all_mvrs[perm_fire]))
        null_deltas.append(unc_mean - perm_mean)

    p_perm = float(np.mean(np.array(null_deltas) >= delta_obs))

    return {
        "n_fire": n_fire,
        "n_eligible": n_elig,
        "fire_rate": round(n_fire / max(n_elig, 1), 4),
        "fire_mean_mvr": round(fire_mean, 4),
        "unc_mean_mvr": round(unc_mean, 4),
        "delta_vr": round(delta_obs, 4),
        "p_perm": round(p_perm, 4),
        "hit_p": bool(p_perm < P_HIT),
        "hit_effect": bool(delta_obs >= EFFECT_FLOOR),
        "hit_both": bool(p_perm < P_HIT and delta_obs >= EFFECT_FLOOR),
    }


# ── Per-instrument analysis ───────────────────────────────────────────────────────

def analyze_instrument(name: str, px: pd.Series, W: int, variant: str) -> dict:
    px_clean = px.dropna()
    n_total  = len(px_clean)
    n_is     = int(n_total * OOS_SPLIT)
    log_px   = np.log(px_clean.to_numpy(float))

    beta, tstat, resid = compute_rolling_trend(log_px, W)

    if variant == "primary":
        fires = fire_primary(beta, tstat, resid, W, n_total)
    else:
        fires = fire_ablation(beta, tstat, W, n_total)

    results = {}
    for split_name, bar_start, bar_end in [
        ("IS",  W, n_is),
        ("OOS", n_is, n_total),
    ]:
        bar_range = range(bar_start, bar_end - H_FORWARD)
        all_mvrs, eligible = compute_all_forward_mvrs(log_px, bar_range)

        # Map fire positions to eligible-bar indices
        fire_set = set(np.where(fires[bar_start: bar_end - H_FORWARD])[0] + 0)
        # Need absolute bar indices in eligible list
        fire_idx_in_eligible = [i for i, t in enumerate(eligible)
                                 if fires[t]]

        seed_i = SEED_T25 + hash(f"{name}{W}{variant}{split_name}") % 100_000
        ptest = permutation_test(all_mvrs, fire_idx_in_eligible, seed=seed_i)

        # Habitat scores for fire bars only (characterization)
        fire_hab_scores = []
        for i, t in enumerate(eligible):
            if not fires[t]:
                continue
            fwd = np.exp(log_px[t + 1: t + 1 + H_FORWARD])
            sc = habitat_score_single(fwd, seed=seed_i + i)
            if np.isfinite(sc):
                fire_hab_scores.append(sc)

        ptest["fire_mean_habitat"] = round(float(np.nanmean(fire_hab_scores)), 2) if fire_hab_scores else float("nan")
        ptest["n_fire_hab_scored"] = len(fire_hab_scores)
        results[split_name] = ptest

    return results


# ── Main ─────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("T2.5 — Trend-Death Detector: Minimal First Test")
    print("Pre-reg: docs/research/t2_5_trend_death_prereg.md")
    print("=" * 70)
    print(f"Instruments: {list(INSTRUMENTS.keys())}")
    print(f"W_primary={W_PRIMARY}, W_robust={W_ROBUST}, H={H_FORWARD}, N_perm={N_PERM}")

    all_results = {}
    hit_summary = {}

    for inst_name, loader in INSTRUMENTS.items():
        print(f"\n--- {inst_name} ---")
        try:
            px = loader()
        except Exception as e:
            print(f"  LOAD ERROR: {e}")
            continue

        px_clean = px.dropna()
        n = len(px_clean)
        n_is = int(n * OOS_SPLIT)
        print(f"  n={n}  IS={n_is}  OOS={n-n_is}  "
              f"{px_clean.index[0].date()} – {px_clean.index[-1].date()}")

        if n < MIN_BARS:
            print(f"  SKIP: n={n} < {MIN_BARS}")
            continue

        inst_results = {}

        for W in [W_PRIMARY, W_ROBUST]:
            for variant in ["primary", "ablation"]:
                key = f"W{W}_{variant}"
                r = analyze_instrument(inst_name, px_clean, W, variant)
                inst_results[key] = r
                is_r = r["IS"]
                if not is_r.get("insufficient_fires"):
                    hit_mark = ("HIT" if is_r.get("hit_both") else
                                ("p-only" if is_r.get("hit_p") else
                                 ("eff-only" if is_r.get("hit_effect") else "miss")))
                    print(f"  [{key}] n_fire={is_r['n_fire']:3d} "
                          f"Δ_vr={is_r['delta_vr']:+.4f} p={is_r['p_perm']:.3f} "
                          f"fire_mvr={is_r['fire_mean_mvr']:.3f} unc_mvr={is_r['unc_mean_mvr']:.3f} "
                          f"hab={is_r.get('fire_mean_habitat', float('nan')):.1f} → {hit_mark}")
                else:
                    print(f"  [{key}] insufficient fires ({is_r.get('n_fire', 0)})")

        all_results[inst_name] = inst_results

        # Primary W=60 IS result for programme verdict
        prim_is = inst_results.get(f"W{W_PRIMARY}_primary", {}).get("IS", {})
        hit_summary[inst_name] = {
            "hit_both":  bool(prim_is.get("hit_both", False)),
            "hit_p":     bool(prim_is.get("hit_p", False)),
            "hit_effect":bool(prim_is.get("hit_effect", False)),
            "delta_vr":  prim_is.get("delta_vr", float("nan")),
            "p_perm":    prim_is.get("p_perm", float("nan")),
            "n_fire":    prim_is.get("n_fire", 0),
            "fire_mvr":  prim_is.get("fire_mean_mvr", float("nan")),
            "unc_mvr":   prim_is.get("unc_mean_mvr", float("nan")),
        }

    # ── Programme-level verdict ───────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"PROGRAMME VERDICT (pre-committed §5, primary W={W_PRIMARY} IS)")
    print(f"{'='*70}")
    hits = []
    deltas = []
    p_vals = []
    for inst, h in hit_summary.items():
        mark = ("HIT" if h["hit_both"] else
                "p-only" if h["hit_p"] else
                "eff-only" if h["hit_effect"] else "miss")
        print(f"  {inst:10s}: n_fire={h['n_fire']:3d}  Δ_vr={h['delta_vr']:+.4f}  "
              f"p={h['p_perm']:.3f}  → {mark}")
        if h["hit_both"]:
            hits.append(inst)
        if np.isfinite(h.get("delta_vr", float("nan"))):
            deltas.append(h["delta_vr"])
        if np.isfinite(h.get("p_perm", float("nan"))):
            p_vals.append(h["p_perm"])

    n_hits          = len(hits)
    sign_consistent = all(d > 0 for d in deltas) if deltas else False
    p_min           = min(p_vals) if p_vals else float("nan")
    pooled_sig      = p_min < P_PROGRAMME if np.isfinite(p_min) else False

    print(f"\n  Full-hits: {n_hits}/{len(hit_summary)}  needed ≥{MAJORITY_N}")
    print(f"  Sign consistent (Δ>0 on all): {sign_consistent}")
    print(f"  Min IS p across instruments: {p_min:.4f}" if np.isfinite(p_min) else "  Min p: nan")
    print(f"  Bonferroni threshold (0.05/4): {P_PROGRAMME}  pooled_sig: {pooled_sig}")

    content = (n_hits >= MAJORITY_N and sign_consistent and pooled_sig)
    verdict = "CONTENT" if content else "NO_CONTENT"
    print(f"\n  VERDICT: {verdict}")

    # Save results
    out = {
        "meta": {
            "W_primary": W_PRIMARY, "W_robust": W_ROBUST, "H_forward": H_FORWARD,
            "N_perm": N_PERM, "effect_floor": EFFECT_FLOOR,
            "p_hit": P_HIT, "p_programme": P_PROGRAMME,
        },
        "hit_summary": hit_summary,
        "verdict": verdict,
        "verdict_criteria": {
            "n_hits": n_hits, "majority_needed": MAJORITY_N,
            "sign_consistent": sign_consistent,
            "pooled_bonferroni_significant": pooled_sig,
            "min_p": round(p_min, 4) if np.isfinite(p_min) else None,
        },
        "detailed": all_results,
    }
    out_path = os.path.join(BASE, "..", "data", "processed", "t2_5_trend_death_results.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nResults saved: {out_path}")


if __name__ == "__main__":
    main()
