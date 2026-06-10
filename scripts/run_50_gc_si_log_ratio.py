"""
Doc 50 — GC-SI Log-Ratio IS VR Pre-Registration.

Pre-registration: docs/research/50_gc_si_log_ratio_prereg.md (REVISION 1 binding)

Object: X_t = ln(GC2!_close) - ln(SI2!_close), beta=1 definitional in log space.
Split: 70/30 row-count chronological on trimmed aligned series.
Primary: IS VR(20) vs RW null, N=500 full, N=200 speed gate.
Alpha: 0.0167 (Bonferroni 3-look), seed 20260612.

REVISION-1 MANDATES (all three must appear in results doc):
  1. PASS leaf is ACTIVE-IS-CONFIRMED-PEEK-CONDITIONED (never clean confirmation).
  2. Mandatory disjoint sub-window check: 1998-07-07 to 2005-07 standalone VR(20).
  3. Run-conditioning statement: alpha partially prices multiplicity, does NOT neutralize
     conditional-existence selection from run-selection on favorable peek.

Frozen engine files used (NOT modified):
  backend/app/services/analytics_arm_a.py
  backend/app/services/analytics_arm_a_v2.py

Writes: data/processed/50_results.json
        docs/research/50_gc_si_log_ratio_results.md
"""
from __future__ import annotations

import sys, os, json, warnings
warnings.filterwarnings("ignore")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(SCRIPT_DIR, "..")
sys.path.insert(0, os.path.join(ROOT, "backend"))

import numpy as np
import pandas as pd
from scipy.signal import lfilter

# Frozen engine imports (read-only — do NOT modify these files)
from app.services.analytics_arm_a_v2 import increment_jump_mask

# ============================================================
# DOC 50 FROZEN CONSTANTS — DO NOT MODIFY AFTER PRE-REGISTRATION
# ============================================================

GC_FILE = os.path.join(ROOT, "data", "raw", "more-mean-reversion-data",
                        "COMEX_DL_GC2!, 1D.csv")
SI_FILE = os.path.join(ROOT, "data", "raw", "more-mean-reversion-data",
                        "COMEX_DL_SI2!, 1D.csv")

TRIM_START_DATE     = "1998-07-07"      # frozen; derived in doc-49 execution
ROLL_MASK_K         = 8.0               # frozen; do NOT adjust
BETA                = 1.0               # definitional; never updated
F_BETA_UPDATE       = 0.000             # identically zero; stated for protocol
F_BETA_UPDATE_HALT  = 0.10              # gate; trivially satisfied

# ADR_003 assertions
ADR003_SI_DATE      = "2026-01-29"      # ±1 day tolerance
ADR003_SI_ROBUST_Z  = 15.45             # confirmed doc-49
ADR003_GC_DATE      = "1999-09-27"      # confirmed doc-49
ADR003_GC_ROBUST_Z  = 19.26             # confirmed doc-49

# IS/OOS split
IS_FRAC             = 0.70

# Primary statistic
VR_Q_PRIMARY        = 20
VR_Q_GRID           = [2, 5, 10, 20, 40]
NULL_FAMILIES       = ["rw", "garch", "ma1", "ou"]

# Surrogate counts
N_SURR_SPEED        = 200
N_SURR_FULL         = 500

# Seed (frozen; all surrogate draws in this prereg)
SEED                = 20260612

# Alpha (3-look Bonferroni)
ALPHA               = 0.05 / 3         # = 0.016667
PASS_P_RW_SPEED     = 0.20
PASS_P_RW_FULL      = ALPHA

# Jackknife
JACKKNIFE_N_BLOCKS  = 5
JACKKNIFE_DROP_MAX  = 3.00

# Power simulation
POWER_REF_VR        = 0.90
POWER_SIM_N_PATHS   = 500
POWER_ALPHA         = ALPHA             # matches gate alpha
POWER_UNDERPOWERED  = 0.30

# Flat-bar gate
FLAT_BAR_THRESHOLD  = 0.05

# Revision-1 Mandate 2: disjoint sub-window end (pre-peek IS segment)
DISJOINT_SUBWINDOW_END = "2005-07-01"  # 1998-07-07 → 2005-07 is the only unpeeked slice

# Cost grid (informational at IS screen stage)
COST_PRIMARY        = 0.005
COST_GRID           = [0.003, 0.005, 0.008]

RESULTS_JSON        = os.path.join(ROOT, "data", "processed", "50_results.json")
RESULTS_DOC         = os.path.join(ROOT, "docs", "research", "50_gc_si_log_ratio_results.md")

# ============================================================
# END FROZEN CONSTANTS
# ============================================================


# ── Loaders ──────────────────────────────────────────────────────────────────

def load_csv_auto(path: str) -> pd.DataFrame:
    """Auto-detect timestamp format (unix or YYYY-MM-DD)."""
    sample = pd.read_csv(path, nrows=2)
    sample.columns = [c.strip().lower() for c in sample.columns]
    t0 = str(sample["time"].iloc[0])
    if "-" in t0 and len(t0) == 10:
        df = pd.read_csv(path)
        df.columns = [c.strip().lower() for c in df.columns]
        df["ts"] = pd.to_datetime(df["time"], utc=False).dt.normalize()
    else:
        df = pd.read_csv(path)
        df.columns = [c.strip().lower() for c in df.columns]
        df["ts"] = (pd.to_datetime(df["time"].astype(np.int64), unit="s", utc=True)
                    .dt.normalize().dt.tz_localize(None))
    return (df.dropna(subset=["ts"])
              .sort_values("ts")
              .drop_duplicates("ts", keep="last")
              .set_index("ts"))


# ── Core statistical functions ────────────────────────────────────────────────

def vr_q(s: np.ndarray, q: int) -> float:
    """Lo-MacKinlay variance ratio at horizon q (overlapping returns)."""
    x = s[np.isfinite(s)]
    n = len(x)
    if n < q + 20:
        return float("nan")
    dr = np.diff(x)
    var1 = np.var(dr, ddof=1)
    if var1 <= 1e-14:
        return float("nan")
    ret_q = x[q:] - x[:-q]
    varq = np.var(ret_q, ddof=1)
    return float(varq / (q * var1))


def surrogate_pval(s: np.ndarray, q: int, n_surr: int, seed: int,
                   null_type: str = "rw") -> tuple[float, float, list[float]]:
    """
    Compute VR(q) and surrogate p-value.
    p_value = fraction of surrogate VRs <= real VR (one-sided lower test, sub-diffusion).
    Returns (real_vr, p_value, surr_vrs_list).
    """
    real_vr = vr_q(s, q)
    if not np.isfinite(real_vr):
        return float("nan"), float("nan"), []
    x   = s[np.isfinite(s)]
    n   = len(x)
    dr  = np.diff(x)
    rng = np.random.default_rng(seed)
    surr_vrs: list[float] = []

    if null_type == "rw":
        mu_  = float(np.mean(dr))
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
            # GARCH fallback: heteroskedastic bootstrap
            sd_roll = (pd.Series(dr).rolling(20, min_periods=5).std()
                       .ffill().bfill().to_numpy())
            for _ in range(n_surr):
                rets = rng.normal(np.mean(dr), sd_roll)
                path = np.concatenate([[0.0], np.cumsum(rets)])
                v = vr_q(path, q)
                if np.isfinite(v):
                    surr_vrs.append(v)

    elif null_type == "ma1":
        theta_ma = float(np.corrcoef(dr[:-1], dr[1:])[0, 1])
        theta_ma = float(np.clip(theta_ma, -0.99, 0.99))
        sig_ = float(np.std(dr, ddof=1))
        for _ in range(n_surr):
            eps = rng.normal(0, sig_, n)
            ma1 = lfilter([1, theta_ma], [1], eps)
            path = np.concatenate([[0.0], np.cumsum(ma1[1:])])
            v = vr_q(path, q)
            if np.isfinite(v):
                surr_vrs.append(v)

    elif null_type == "ou":
        x_c = x - x.mean()
        phi = float(np.clip(np.corrcoef(x_c[:-1], x_c[1:])[0, 1], -0.9999, 0.9999))
        theta_ou = -np.log(max(phi, 1e-9))
        sig_ou = float(np.std(x_c[1:] - phi * x_c[:-1], ddof=1))
        mu_ou  = float(x.mean())
        for _ in range(n_surr):
            path = np.empty(n)
            path[0] = x[0]
            eps = rng.normal(0, sig_ou, n - 1)
            for t in range(1, n):
                path[t] = path[t-1] + theta_ou * (mu_ou - path[t-1]) + eps[t-1]
            v = vr_q(path, q)
            if np.isfinite(v):
                surr_vrs.append(v)
    else:
        raise ValueError(f"unknown null_type: {null_type}")

    if not surr_vrs:
        return real_vr, float("nan"), []
    pv = (1.0 + sum(v <= real_vr for v in surr_vrs)) / (len(surr_vrs) + 1.0)
    return real_vr, float(pv), surr_vrs


def dist_stats(surr_vrs: list[float]) -> dict:
    """5th, 50th, 95th percentiles of surrogate distribution."""
    if not surr_vrs:
        return {"p5": None, "p50": None, "p95": None, "n": 0}
    arr = np.array(surr_vrs)
    return {
        "p5":  round(float(np.percentile(arr, 5)),  4),
        "p50": round(float(np.percentile(arr, 50)), 4),
        "p95": round(float(np.percentile(arr, 95)), 4),
        "n":   len(arr),
    }


# ── Power simulation (corrected AR(1)-increments pattern, doc 48/49) ─────────

def vr_ar1_theoretical(phi: float, q: int = 20) -> float:
    """Theoretical VR(q) for path whose increments are AR(1) with parameter phi."""
    total = 1.0
    for k in range(1, q):
        total += 2.0 * (1.0 - k / q) * (phi ** k)
    return total


def run_power_sim(vr_target: float, n_is_valid: int, seed: int,
                  alpha: float, n_paths: int = POWER_SIM_N_PATHS,
                  label: str = "") -> dict:
    """
    Corrected AR(1)-increments power simulation (doc 48 fix):
      dr[0] = eps[0]
      dr[t] = phi * dr[t-1] + eps[t]
      path  = cumsum(dr)
    Binary-search phi to match vr_target at q=20. Verify realized VR within ±0.01.
    """
    phi_lo, phi_hi = -0.999, 0.999
    for _ in range(60):
        phi_mid = (phi_lo + phi_hi) / 2.0
        if vr_ar1_theoretical(phi_mid) < vr_target:
            phi_lo = phi_mid
        else:
            phi_hi = phi_mid
    phi_target = (phi_lo + phi_hi) / 2.0
    vr_check = vr_ar1_theoretical(phi_target)
    print(f"  [{label}] Power sim: target_vr={vr_target:.4f}, phi={phi_target:.6f}, "
          f"theoretical_vr={vr_check:.4f} (error={abs(vr_check-vr_target):.5f})")
    calibration_ok = abs(vr_check - vr_target) <= 0.011
    if not calibration_ok:
        print(f"  WARNING: power sim calibration error > 0.01: target={vr_target}, got={vr_check}")

    rng_pow = np.random.default_rng(seed + 9999)
    sig_pow = 1.0  # scale-invariant; VR is scale-free
    n_pow = max(n_is_valid, 100)
    rejections = 0
    realized_vrs = []
    for i in range(n_paths):
        eps_pow = rng_pow.normal(0, sig_pow, n_pow - 1)
        dr_pow = np.empty(n_pow - 1)
        dr_pow[0] = eps_pow[0]
        for t in range(1, n_pow - 1):
            dr_pow[t] = phi_target * dr_pow[t - 1] + eps_pow[t]
        path_pow = np.concatenate(([0.0], np.cumsum(dr_pow)))
        realized_vrs.append(vr_q(path_pow, VR_Q_PRIMARY))
        # Speed inner test at N=200
        _, p_pow, _ = surrogate_pval(path_pow, VR_Q_PRIMARY, 200,
                                     seed + 10000 + i, "rw")
        if np.isfinite(p_pow) and p_pow < alpha:
            rejections += 1

    realized_vrs_finite = [v for v in realized_vrs if np.isfinite(v)]
    mean_realized_vr = float(np.mean(realized_vrs_finite)) if realized_vrs_finite else float("nan")
    empirical_power = rejections / n_paths
    print(f"  [{label}] Power @ α={alpha}: {rejections}/{n_paths} = {empirical_power:.3f}  "
          f"mean_realized_vr={mean_realized_vr:.4f}")
    return {
        "vr_target":          round(vr_target, 4),
        "phi_target_ar1":     round(phi_target, 6),
        "vr_ar1_theoretical": round(vr_check, 4),
        "mean_realized_vr":   round(mean_realized_vr, 4),
        "vr_calibration_ok":  calibration_ok,
        "n_is_valid":         n_pow,
        "n_paths":            n_paths,
        "alpha":              alpha,
        "rejections":         rejections,
        "empirical_power":    round(empirical_power, 3),
    }


# ── Jackknife (5-block, pre-registration spec) ────────────────────────────────

def run_jackknife(s_is: np.ndarray, full_vr20: float) -> dict:
    """
    5-block leave-one-out jackknife.
    Kill if any jk VR is more than 300% deviation from full_vr20 relative to |full_vr20 - 1|.
    """
    x_is = s_is[np.isfinite(s_is)]
    n_blocks = JACKKNIFE_N_BLOCKS
    ep_size = len(x_is) // n_blocks
    jk_vrs = []
    for ep in range(n_blocks):
        ep_start = ep * ep_size
        ep_end   = (ep + 1) * ep_size if ep < n_blocks - 1 else len(x_is)
        idx_excl = list(range(ep_start)) + list(range(ep_end, len(x_is)))
        s_jk = x_is[idx_excl]
        v = vr_q(s_jk, VR_Q_PRIMARY)
        if np.isfinite(v):
            jk_vrs.append(v)
    if not jk_vrs:
        return {"jk_vrs": [], "jk_min": None, "jk_med": None, "jk_max": None,
                "kill": False, "note": "insufficient data"}
    jk_arr = np.array(jk_vrs)
    jk_min = float(np.min(jk_arr))
    jk_med = float(np.median(jk_arr))
    jk_max = float(np.max(jk_arr))
    deviation = abs(full_vr20 - 1.0)
    kill_upper = full_vr20 + JACKKNIFE_DROP_MAX * deviation
    kill_lower = full_vr20 - JACKKNIFE_DROP_MAX * deviation
    kill = bool(jk_max > kill_upper or jk_min < kill_lower)
    print(f"  Jackknife: full_vr20={full_vr20:.4f}  deviation={deviation:.4f}  "
          f"kill_range=[{kill_lower:.4f}, {kill_upper:.4f}]")
    print(f"  JK min={jk_min:.4f}  med={jk_med:.4f}  max={jk_max:.4f}  "
          f">> {'KILL (CONCENTRATION-UNSTABLE)' if kill else 'PASS'}")
    return {
        "full_vr20":  round(full_vr20, 4),
        "jk_min":     round(jk_min, 4),
        "jk_med":     round(jk_med, 4),
        "jk_max":     round(jk_max, 4),
        "jk_vrs":     [round(v, 4) for v in jk_vrs],
        "kill_lower": round(kill_lower, 4),
        "kill_upper": round(kill_upper, 4),
        "kill":       kill,
    }


# ── ADR_003 robust Z-score helper ─────────────────────────────────────────────

def compute_robust_z_at_date(prices: np.ndarray, idx_arr: pd.DatetimeIndex,
                              target_start: str, target_end: str,
                              window: int = 252) -> tuple[bool, str | None, float | None, float | None]:
    """
    Compute robust Z-score for a known large-move event near target_start/target_end.
    Uses LOG-RETURNS (ln(P_t/P_{t-1})) as required by doc-50 ADR_003 spec.
    Returns (caught, event_date, raw_log_return, robust_z).
    """
    log_rets = np.full(len(prices), np.nan)
    for t in range(1, len(prices)):
        if prices[t] > 0 and prices[t-1] > 0:
            log_rets[t] = np.log(prices[t] / prices[t-1])

    t_start = pd.Timestamp(target_start)
    t_end   = pd.Timestamp(target_end)
    locs    = np.where((idx_arr >= t_start) & (idx_arr <= t_end))[0]

    # Apply increment_jump_mask to log-returns to find masked bars in window
    # But we need robust Z on LOG-RETURNS — compute manually per spec
    caught = False
    event_date = None
    raw_lr = None
    robust_z = None

    for loc in locs:
        if loc < 1:
            continue
        # Trailing window of log-returns ending at loc-1
        lo = max(1, loc - window)
        ref = log_rets[lo:loc]
        ref = ref[np.isfinite(ref)]
        if len(ref) < 10:
            continue
        med  = float(np.median(ref))
        mad  = float(np.median(np.abs(ref - med)))
        if mad <= 0:
            continue
        z = float(abs(log_rets[loc] - med) / (1.4826 * mad))
        if z > ROLL_MASK_K:
            caught = True
            event_date = str(idx_arr[loc].date())
            raw_lr  = float(log_rets[loc]) if np.isfinite(log_rets[loc]) else None
            robust_z = z
            break

    return caught, event_date, raw_lr, robust_z


def apply_per_leg_log_return_mask(prices: np.ndarray, k: float = 8.0,
                                   window: int = 252) -> np.ndarray:
    """
    Per spec: mask bar t if |r_t − trailing_median(r, 252)| > k * 1.4826 * trailing_MAD(r, 252)
    where r_t = ln(P_t / P_{t-1}).
    Returns boolean mask (True = masked/NaN-out).
    NOTE: this is the ADR_003 per-leg log-return mask per doc-50 construction spec.
    """
    n = len(prices)
    mask = np.zeros(n, dtype=bool)
    log_rets = np.full(n, np.nan)
    for t in range(1, n):
        if prices[t] > 0 and prices[t-1] > 0:
            log_rets[t] = np.log(prices[t] / prices[t-1])

    for t in range(1, n):
        if not np.isfinite(log_rets[t]):
            mask[t] = True
            continue
        lo = max(1, t - window)
        ref = log_rets[lo:t]
        ref = ref[np.isfinite(ref)]
        if len(ref) < 10:
            continue
        med = float(np.median(ref))
        mad = float(np.median(np.abs(ref - med)))
        if mad <= 0:
            continue
        z = float(abs(log_rets[t] - med) / (1.4826 * mad))
        if z > k:
            mask[t] = True
    return mask


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_doc50() -> dict:
    print("\n" + "=" * 72)
    print("DOC 50 — GC-SI Log-Ratio IS VR Pre-Registration")
    print(f"  Object: X_t = ln(GC2!) - ln(SI2!), beta=1 definitional")
    print(f"  Trim start (frozen): {TRIM_START_DATE}")
    print(f"  Alpha: {ALPHA:.6f} (Bonferroni 3-look, seed={SEED})")
    print(f"  PASS: p_rw(N={N_SURR_FULL}, q={VR_Q_PRIMARY}) < {PASS_P_RW_FULL:.6f}")
    print("=" * 72)

    result: dict = {}

    # ── Gate 0: File readability ───────────────────────────────────────────────
    print("\n--- GATE 0: FILE READABILITY ---")
    for fname, fpath in [("GC2!", GC_FILE), ("SI2!", SI_FILE)]:
        if not os.path.exists(fpath):
            msg = f"BUG — infrastructure failure (file missing): {fpath}"
            print(f"  !! {msg}")
            result["verdict"] = "BUG"
            result["bug_message"] = msg
            return result
        try:
            open(fpath, "r").close()
        except Exception as e:
            msg = f"BUG — infrastructure failure (unreadable): {fpath}: {e}"
            print(f"  !! {msg}")
            result["verdict"] = "BUG"
            result["bug_message"] = msg
            return result
        print(f"  {fname}: readable — OK")

    # ── Step 1: Load data ──────────────────────────────────────────────────────
    print("\n--- STEP 1: LOAD DATA ---")
    gc_df = load_csv_auto(GC_FILE)
    si_df = load_csv_auto(SI_FILE)
    print(f"  GC2! raw rows: {len(gc_df)}  ({gc_df.index[0].date()} → {gc_df.index[-1].date()})")
    print(f"  SI2! raw rows: {len(si_df)}  ({si_df.index[0].date()} → {si_df.index[-1].date()})")

    # ── Step 2: Inner-join, drop NaN/zero/negative ─────────────────────────────
    print("\n--- STEP 2: ALIGN AND FILTER ---")
    # Identify available OHLC columns for flat-bar check
    gc_cols = list(gc_df.columns)
    si_cols = list(si_df.columns)
    gc_has_ohlc = all(c in gc_cols for c in ["open", "high", "low", "close"])
    si_has_ohlc = all(c in si_cols for c in ["open", "high", "low", "close"])

    if gc_has_ohlc and si_has_ohlc:
        merged_raw = (gc_df[["open", "high", "low", "close"]].join(
                      si_df[["open", "high", "low", "close"]],
                      how="inner", lsuffix="_gc", rsuffix="_si")
                      .dropna())
    else:
        merged_raw = (gc_df[["close"]].join(si_df[["close"]],
                      how="inner", lsuffix="_gc", rsuffix="_si").dropna())
        gc_has_ohlc = False
        si_has_ohlc = False
    print(f"  Pre-filter aligned rows: {len(merged_raw)}")

    # Drop rows where either close is non-positive (log undefined)
    gc_close_all = merged_raw["close_gc"].to_numpy(float)
    si_close_all = merged_raw["close_si"].to_numpy(float)
    valid_mask = (gc_close_all > 0) & (si_close_all > 0)
    n_dropped_nonpos = int((~valid_mask).sum())
    merged_raw = merged_raw[valid_mask].copy()
    print(f"  Dropped non-positive close rows: {n_dropped_nonpos}")
    print(f"  Post-filter aligned rows: {len(merged_raw)}")

    # ── Step 3: Apply trim start (frozen at 1998-07-07) ───────────────────────
    print(f"\n--- STEP 3: APPLY TRIM (frozen start: {TRIM_START_DATE}) ---")
    trim_ts = pd.Timestamp(TRIM_START_DATE)
    merged_trimmed = merged_raw[merged_raw.index >= trim_ts].copy()
    n_rows_dropped_trim = len(merged_raw) - len(merged_trimmed)
    print(f"  Rows dropped by trim: {n_rows_dropped_trim}")
    print(f"  Post-trim rows: {len(merged_trimmed)}")
    print(f"  Assert start >= {TRIM_START_DATE}: "
          f"{merged_trimmed.index[0].date()} — "
          f"{'OK' if merged_trimmed.index[0] >= trim_ts else 'FAIL'}")
    assert merged_trimmed.index[0] >= trim_ts, (
        f"Trim assertion failed: series starts at {merged_trimmed.index[0].date()} "
        f"< {TRIM_START_DATE}")

    gc_close = merged_trimmed["close_gc"].to_numpy(float)
    si_close = merged_trimmed["close_si"].to_numpy(float)
    idx_arr  = merged_trimmed.index
    n_aligned = len(merged_trimmed)

    # ── Gate 0b: Flat-bar gate (IS window) ────────────────────────────────────
    print(f"\n--- GATE 0b: FLAT-BAR CHECK (IS window, threshold {FLAT_BAR_THRESHOLD*100:.0f}%) ---")
    n_is_total = int(n_aligned * IS_FRAC)
    is_flat_gc = 0.0
    is_flat_si = 0.0

    if gc_has_ohlc and si_has_ohlc:
        gc_open_is  = merged_trimmed["open_gc"].iloc[:n_is_total].to_numpy(float)
        gc_high_is  = merged_trimmed["high_gc"].iloc[:n_is_total].to_numpy(float)
        gc_low_is   = merged_trimmed["low_gc"].iloc[:n_is_total].to_numpy(float)
        gc_close_is = merged_trimmed["close_gc"].iloc[:n_is_total].to_numpy(float)
        si_open_is  = merged_trimmed["open_si"].iloc[:n_is_total].to_numpy(float)
        si_high_is  = merged_trimmed["high_si"].iloc[:n_is_total].to_numpy(float)
        si_low_is   = merged_trimmed["low_si"].iloc[:n_is_total].to_numpy(float)
        si_close_is = merged_trimmed["close_si"].iloc[:n_is_total].to_numpy(float)

        gc_flat = ((gc_open_is == gc_high_is) & (gc_high_is == gc_low_is) &
                   (gc_low_is  == gc_close_is))
        si_flat = ((si_open_is == si_high_is) & (si_high_is == si_low_is) &
                   (si_low_is  == si_close_is))
        is_flat_gc = float(gc_flat.sum()) / n_is_total
        is_flat_si = float(si_flat.sum()) / n_is_total
        print(f"  IS window rows: {n_is_total}")
        print(f"  GC2! flat bars in IS: {int(gc_flat.sum())} / {n_is_total} = {is_flat_gc*100:.3f}%")
        print(f"  SI2! flat bars in IS: {int(si_flat.sum())} / {n_is_total} = {is_flat_si*100:.3f}%")
    else:
        print(f"  OHLC columns not available — flat-bar check uses close-only proxy (0%)")
        print(f"  GC2! flat bars in IS: 0 / {n_is_total} = 0.000%  (OHLC unavailable)")
        print(f"  SI2! flat bars in IS: 0 / {n_is_total} = 0.000%  (OHLC unavailable)")

    flat_bar_result = {
        "is_window_rows": n_is_total,
        "GC2!_flat_pct_is": round(is_flat_gc * 100, 3),
        "SI2!_flat_pct_is": round(is_flat_si * 100, 3),
        "ohlc_available": bool(gc_has_ohlc and si_has_ohlc),
        "threshold_pct": FLAT_BAR_THRESHOLD * 100,
    }

    if is_flat_gc > FLAT_BAR_THRESHOLD or is_flat_si > FLAT_BAR_THRESHOLD:
        msg = (f"MEASUREMENT-INADMISSIBLE: flat bars exceed 5% in IS window — "
               f"GC2!={is_flat_gc*100:.3f}% SI2!={is_flat_si*100:.3f}%. "
               f"Trim start is frozen at {TRIM_START_DATE}; no further trim DOF. Terminal halt.")
        print(f"  !! {msg}")
        result["verdict"] = "MEASUREMENT-INADMISSIBLE"
        result["flat_bar"] = {**flat_bar_result, "gate": "HALT"}
        result["bug_message"] = msg
        return result
    print(f"  Flat-bar gate: PASS (both legs < 5% in IS window)")
    flat_bar_result["gate"] = "PASS"
    result["flat_bar"] = flat_bar_result

    # ── Step 4: ADR_003 increment-jump mask on log-returns per leg ─────────────
    print(f"\n--- STEP 4: ADR_003 INCREMENT-JUMP MASK (k={ROLL_MASK_K}, log-returns per leg) ---")

    # Per doc-50 spec: mask bar t if |r_t - trailing_median(r,252)| > k * 1.4826 * trailing_MAD(r,252)
    # where r_t = ln(P_t / P_{t-1}) — this is on log-returns per leg independently
    gc_log_mask = apply_per_leg_log_return_mask(gc_close, k=ROLL_MASK_K, window=252)
    si_log_mask = apply_per_leg_log_return_mask(si_close, k=ROLL_MASK_K, window=252)
    combined_mask = gc_log_mask | si_log_mask

    n_gc_masked = int(gc_log_mask.sum())
    n_si_masked = int(si_log_mask.sum())
    n_combined_masked = int(combined_mask.sum())
    print(f"  GC2! masked bars: {n_gc_masked} / {n_aligned} ({100*n_gc_masked/n_aligned:.2f}%)")
    print(f"  SI2! masked bars: {n_si_masked} / {n_aligned} ({100*n_si_masked/n_aligned:.2f}%)")
    print(f"  Combined masked (either leg): {n_combined_masked} / {n_aligned} "
          f"({100*n_combined_masked/n_aligned:.2f}%)")

    # ADR_003 assertion: SI2! 2026-01-29 event must be caught
    print(f"\n  ADR_003 Assertion 1: SI2! event near {ADR003_SI_DATE} (robust_Z ≥ {ROLL_MASK_K})")
    si2_caught, si2_date, si2_lr, si2_z = compute_robust_z_at_date(
        si_close, idx_arr, "2026-01-28", "2026-01-31", window=252)
    si2_lr_str = f"{si2_lr:.5f}" if si2_lr is not None else "N/A"
    si2_z_str  = f"{si2_z:.2f}"  if si2_z  is not None else "N/A"
    print(f"    date={si2_date}  log_ret={si2_lr_str}  robust_Z={si2_z_str}  "
          f"{'CAUGHT' if si2_caught else 'NOT CAUGHT — ASSERTION FAILURE'}")

    if not si2_caught:
        msg = (f"ADR_003 assertion failed — SI2! event near {ADR003_SI_DATE} NOT caught "
               f"by robust Z-score k={ROLL_MASK_K} on log-returns. "
               f"Construction integrity violated.")
        print(f"  !! {msg}")
        result["verdict"] = "BUG"
        result["bug_message"] = msg
        result["adr003"] = {
            "SI2!_caught": False, "SI2!_date": si2_date,
            "SI2!_log_ret": si2_lr, "SI2!_robust_z": si2_z,
        }
        return result

    # ADR_003 assertion: GC2! 1999-09-27 event must be caught
    print(f"  ADR_003 Assertion 2: GC2! event near {ADR003_GC_DATE} (robust_Z ≥ {ROLL_MASK_K})")
    gc2_caught, gc2_date, gc2_lr, gc2_z = compute_robust_z_at_date(
        gc_close, idx_arr, "1999-09-26", "1999-09-28", window=252)
    gc2_lr_str = f"{gc2_lr:.5f}" if gc2_lr is not None else "N/A"
    gc2_z_str  = f"{gc2_z:.2f}"  if gc2_z  is not None else "N/A"
    print(f"    date={gc2_date}  log_ret={gc2_lr_str}  robust_Z={gc2_z_str}  "
          f"{'CAUGHT' if gc2_caught else 'NOT CAUGHT — ASSERTION FAILURE'}")

    if not gc2_caught:
        msg = (f"ADR_003 assertion failed — GC2! event near {ADR003_GC_DATE} NOT caught "
               f"by robust Z-score k={ROLL_MASK_K} on log-returns. "
               f"Construction integrity violated.")
        print(f"  !! {msg}")
        result["verdict"] = "BUG"
        result["bug_message"] = msg
        result["adr003"] = {
            "SI2!_caught": True,  "SI2!_date": si2_date,
            "SI2!_log_ret": round(si2_lr, 5) if si2_lr else None,
            "SI2!_robust_z": round(si2_z, 2) if si2_z else None,
            "GC2!_caught": False, "GC2!_date": gc2_date,
            "GC2!_log_ret": gc2_lr, "GC2!_robust_z": gc2_z,
        }
        return result

    print(f"  ADR_003 assertions: BOTH PASS")
    adr003_result = {
        "SI2!_caught":    True,
        "SI2!_date":      si2_date,
        "SI2!_log_ret":   round(si2_lr, 5) if si2_lr is not None else None,
        "SI2!_robust_z":  round(si2_z,  2) if si2_z  is not None else None,
        "SI2!_target":    ADR003_SI_DATE,
        "SI2!_prereg_z":  ADR003_SI_ROBUST_Z,
        "GC2!_caught":    True,
        "GC2!_date":      gc2_date,
        "GC2!_log_ret":   round(gc2_lr, 5) if gc2_lr is not None else None,
        "GC2!_robust_z":  round(gc2_z,  2) if gc2_z  is not None else None,
        "GC2!_target":    ADR003_GC_DATE,
        "GC2!_prereg_z":  ADR003_GC_ROBUST_Z,
    }
    result["adr003"] = adr003_result

    # ── Step 5: Construct X_t = ln(GC2!) - ln(SI2!) ───────────────────────────
    print(f"\n--- STEP 5: CONSTRUCT X_t = ln(GC2!) - ln(SI2!) ---")
    X_full = np.full(n_aligned, np.nan)
    for t in range(n_aligned):
        if gc_close[t] > 0 and si_close[t] > 0 and not combined_mask[t]:
            X_full[t] = np.log(gc_close[t]) - np.log(si_close[t])

    n_valid_total = int(np.sum(np.isfinite(X_full)))
    print(f"  Total aligned rows: {n_aligned}")
    print(f"  Combined masked (NaN'd out): {n_combined_masked}")
    print(f"  Valid X_t bars: {n_valid_total}")
    print(f"  Date range: {idx_arr[0].date()} → {idx_arr[-1].date()}")

    # f_βupdate = 0 (stated for protocol completeness)
    print(f"\n  β-mode: β=1.0 DEFINITIONAL (log space); f_βupdate=0.000 identically")
    print(f"  f_βupdate gate: PASS (0.000 < {F_BETA_UPDATE_HALT})")

    # ── IS/OOS split (70/30 row-count rule) ───────────────────────────────────
    print(f"\n--- STEP 6: IS/OOS SPLIT (70/30 row-count chronological) ---")
    n_oos_total = n_aligned - n_is_total
    X_is  = X_full[:n_is_total]
    X_oos = X_full[n_is_total:]
    idx_is  = idx_arr[:n_is_total]
    idx_oos = idx_arr[n_is_total:]

    n_is_valid  = int(np.sum(np.isfinite(X_is)))
    n_oos_valid = int(np.sum(np.isfinite(X_oos)))

    print(f"  n_aligned_total: {n_aligned}")
    print(f"  IS rows: {n_is_total}  ({idx_is[0].date()} → {idx_is[-1].date()})")
    print(f"  OOS rows: {n_oos_total}  ({idx_oos[0].date()} → {idx_oos[-1].date()})")
    print(f"  IS valid (non-NaN): {n_is_valid}")
    print(f"  OOS valid (non-NaN): {n_oos_valid}")

    construction = {
        "n_bars_raw_gc": len(gc_df),
        "n_bars_raw_si": len(si_df),
        "n_aligned_pre_trim": int(len(merged_raw)) + n_rows_dropped_trim,
        "n_rows_dropped_trim": n_rows_dropped_trim,
        "n_aligned_post_trim": n_aligned,
        "trim_start_date": TRIM_START_DATE,
        "actual_start_date": str(idx_arr[0].date()),
        "actual_end_date": str(idx_arr[-1].date()),
        "n_gc_masked": n_gc_masked,
        "n_si_masked": n_si_masked,
        "n_combined_masked": n_combined_masked,
        "n_valid_total": n_valid_total,
        "n_is_rows": n_is_total,
        "n_oos_rows": n_oos_total,
        "n_is_valid": n_is_valid,
        "n_oos_valid": n_oos_valid,
        "is_start": str(idx_is[0].date()),
        "is_end":   str(idx_is[-1].date()),
        "oos_start": str(idx_oos[0].date()),
        "oos_end":   str(idx_oos[-1].date()),
        "beta_mode": "β=1.0 definitional (log space)",
        "f_betaupdate": 0.000,
    }
    result["construction"] = construction

    # ── Gate 1: f_βupdate (trivially PASS) ────────────────────────────────────
    # Stated for protocol completeness per pre-registration Part III

    # ── Gate 2: Speed gate N=200 ──────────────────────────────────────────────
    print(f"\n--- GATE 2: SPEED GATE (N={N_SURR_SPEED}): IS VR({VR_Q_PRIMARY}) vs RW ---")
    vr20_is_speed, p_rw_speed, surr_speed_list = surrogate_pval(
        X_is, VR_Q_PRIMARY, N_SURR_SPEED, SEED, "rw")
    dist_speed = dist_stats(surr_speed_list)
    print(f"  VR({VR_Q_PRIMARY}) = {vr20_is_speed:.6f}  p_rw(N={N_SURR_SPEED}) = {p_rw_speed:.6f}")
    print(f"  Surr dist [p5={dist_speed['p5']}, p50={dist_speed['p50']}, "
          f"p95={dist_speed['p95']}]")

    speed_gate_kill = (p_rw_speed > PASS_P_RW_SPEED)
    if speed_gate_kill:
        print(f"  >> SPEED GATE KILL: p_rw={p_rw_speed:.6f} > {PASS_P_RW_SPEED}")
        print(f"  Evaluate power branch (UNIVERSAL underpowered rule)...")
    else:
        print(f"  >> SPEED GATE PASS: p_rw={p_rw_speed:.6f} <= {PASS_P_RW_SPEED}")

    # ── Power simulation (MANDATORY regardless of speed gate) ─────────────────
    print(f"\n--- POWER SIMULATION (mandatory; corrected AR(1)-increments pattern) ---")
    print(f"  Reference VR = {POWER_REF_VR}, n_is_valid = {n_is_valid}, alpha = {POWER_ALPHA}")

    power_ref = run_power_sim(
        POWER_REF_VR, n_is_valid, SEED, POWER_ALPHA,
        POWER_SIM_N_PATHS, label="ref_vr=0.90")

    # Also run at observed IS VR if finite and in range
    power_obs = None
    vr20_for_power = float(vr20_is_speed)  # use the IS VR we already have
    if np.isfinite(vr20_for_power) and 0.01 < vr20_for_power < 1.50:
        power_obs = run_power_sim(
            vr20_for_power, n_is_valid, SEED + 1, POWER_ALPHA,
            POWER_SIM_N_PATHS, label=f"obs_vr={vr20_for_power:.4f}")
    else:
        power_obs = {"vr_target": vr20_for_power,
                     "note": "VR out of power sim range (>1.5 means trending; power irrelevant)"}

    ref_power = power_ref.get("empirical_power", 0.0)
    underpowered = (ref_power < POWER_UNDERPOWERED)
    print(f"\n  Power at ref VR={POWER_REF_VR}: {ref_power:.3f}  "
          f"underpowered threshold: {POWER_UNDERPOWERED}  "
          f"{'UNDERPOWERED' if underpowered else 'ADEQUATE'}")

    if speed_gate_kill:
        if underpowered:
            verdict_label = "INCONCLUSIVE-UNDERPOWERED"
            print(f"\n  SPEED GATE KILL + UNDERPOWERED (power={ref_power:.3f} < {POWER_UNDERPOWERED})")
            print(f"  >> Verdict leaf: INCONCLUSIVE-UNDERPOWERED")
            print(f"  >> Data-depth: n_is_valid={n_is_valid} bars insufficient for power >= {POWER_UNDERPOWERED}")
        else:
            verdict_label = "SCREENED-NEGATIVE"
            print(f"\n  SPEED GATE KILL + POWERED (power={ref_power:.3f} >= {POWER_UNDERPOWERED})")
            print(f"  >> Verdict leaf: SCREENED-NEGATIVE")

        result["verdict"] = verdict_label
        result["vr_speed_gate"] = {
            "vr20": round(vr20_is_speed, 6) if np.isfinite(vr20_is_speed) else None,
            "p_rw_N200": round(p_rw_speed, 6) if np.isfinite(p_rw_speed) else None,
            "surr_dist_N200": dist_speed,
            "kill": True,
        }
        result["power"] = {
            "ref_vr": power_ref,
            "obs_vr": power_obs,
            "underpowered": underpowered,
        }
        result["kill_gates"] = {
            "f_betaupdate":     "PASS (0.000 by construction)",
            "flat_bar":         "PASS",
            "adr003":           "PASS",
            "speed_gate_N200":  f"KILL (p_rw={p_rw_speed:.6f} > {PASS_P_RW_SPEED})",
            "power_branch":     f"{'UNDERPOWERED' if underpowered else 'POWERED'} (power={ref_power:.3f})",
            "jackknife":        "NOT REACHED",
            "full_test_N500":   "NOT REACHED",
            "oos_sign_reversal": "NOT REACHED",
        }
        # Write JSON now (partial), then continue with disjoint sub-window and OOS
        # (must still complete Revision-1 Mandate 2 disjoint sub-window check)
        # We will add disjoint + OOS below regardless of verdict
        _finalize_and_write(result, X_is, idx_is, X_oos, idx_oos,
                            power_ref, power_obs, n_is_valid, n_oos_valid,
                            vr20_is_speed, p_rw_speed, dist_speed,
                            speed_gate_kill=True)
        return result

    # ── Full test N=500 (all null families, full q grid) ──────────────────────
    print(f"\n--- FULL TEST (N={N_SURR_FULL}): IS VR, all null families, full q grid ---")

    null_results: dict = {}
    p_rw_full   = float("nan")
    p_garch_full = float("nan")
    p_ma1_full  = float("nan")
    p_ou_full   = float("nan")
    vr20_full   = float("nan")

    for null_t, seed_off, label in [
        ("rw",    0, "RW (PRIMARY GATE)"),
        ("garch", 1, "GARCH(1,1) supporting"),
        ("ma1",   2, "MA(1)-noise supporting"),
        ("ou",    3, "OU reference"),
    ]:
        vr_val, pv, surr_list = surrogate_pval(
            X_is, VR_Q_PRIMARY, N_SURR_FULL, SEED + seed_off, null_t)
        ds = dist_stats(surr_list)
        null_results[null_t] = {
            "vr20":    round(vr_val, 6) if np.isfinite(vr_val) else None,
            "p_val":   round(pv, 6)     if np.isfinite(pv) else None,
            "surr_dist": ds,
        }
        gate_note = ""
        if null_t == "rw":
            p_rw_full = pv
            vr20_full = vr_val
            if np.isfinite(pv):
                if pv < PASS_P_RW_FULL:
                    gate_note = f"  -> PASS (p={pv:.6f} < {PASS_P_RW_FULL:.6f})"
                elif pv < 0.05:
                    gate_note = f"  -> INCONCLUSIVE-LEANING-FAIL (p∈[{PASS_P_RW_FULL:.6f}, 0.05))"
                else:
                    gate_note = f"  -> FAIL (p={pv:.6f} >= 0.05)"
        elif null_t == "garch":
            p_garch_full = pv
        elif null_t == "ma1":
            p_ma1_full = pv
        elif null_t == "ou":
            p_ou_full = pv
        print(f"  null={label:30s}  VR(20)={vr_val:.6f}  p={pv:.6f}  "
              f"surr[p5={ds['p5']}, p50={ds['p50']}, p95={ds['p95']}]{gate_note}")

    # Full q grid (RW, N=500)
    print(f"\n  Full q grid (IS, RW, N={N_SURR_FULL}):")
    vr_grid   = {}
    p_rw_grid = {}
    for q in VR_Q_GRID:
        vr_val, pv, _ = surrogate_pval(X_is, q, N_SURR_FULL, SEED + 10 + q, "rw")
        vr_grid[q]   = round(vr_val, 6) if np.isfinite(vr_val) else None
        p_rw_grid[q] = round(pv, 6)     if np.isfinite(pv) else None
        flag = " *** PRIMARY ***" if q == VR_Q_PRIMARY else ""
        print(f"    VR({q:2d}) = {vr_val:.6f}  p_rw = {pv:.6f}{flag}")

    result["vr_is_full"] = {
        "primary_q": VR_Q_PRIMARY,
        "vr20": round(vr20_full, 6) if np.isfinite(vr20_full) else None,
        "p_rw_N500":   round(p_rw_full,   6) if np.isfinite(p_rw_full)   else None,
        "p_garch_N500": round(p_garch_full, 6) if np.isfinite(p_garch_full) else None,
        "p_ma1_N500":  round(p_ma1_full,  6) if np.isfinite(p_ma1_full)  else None,
        "p_ou_N500":   round(p_ou_full,   6) if np.isfinite(p_ou_full)   else None,
        "null_distributions": null_results,
        "vr_grid":   {str(k): v for k, v in vr_grid.items()},
        "p_rw_grid": {str(k): v for k, v in p_rw_grid.items()},
        "p_rw_N200": round(p_rw_speed, 6) if np.isfinite(p_rw_speed) else None,
    }
    result["power"] = {
        "ref_vr": power_ref,
        "obs_vr": power_obs,
        "underpowered": underpowered,
    }

    # ── Gate 3: Jackknife (5-block) ────────────────────────────────────────────
    print(f"\n--- GATE 3: JACKKNIFE (5-block, max-drop <= 300%) ---")
    vr20_for_jk = vr20_full if np.isfinite(vr20_full) else vr20_is_speed
    jk_result = run_jackknife(X_is, float(vr20_for_jk))
    result["jackknife"] = jk_result
    jk_kill = jk_result.get("kill", False)

    if jk_kill:
        result["verdict"] = "CONCENTRATION-UNSTABLE"
        result["kill_gates"] = {
            "f_betaupdate":    "PASS (0.000 by construction)",
            "flat_bar":        "PASS",
            "adr003":          "PASS",
            "speed_gate_N200": f"PASS (p_rw={p_rw_speed:.6f})",
            "jackknife":       "KILL (CONCENTRATION-UNSTABLE)",
            "full_test_N500":  "NOT REACHED",
            "oos_sign_reversal": "NOT REACHED",
        }
        _finalize_and_write(result, X_is, idx_is, X_oos, idx_oos,
                            power_ref, power_obs, n_is_valid, n_oos_valid,
                            vr20_full, p_rw_full, dist_stats([]),
                            speed_gate_kill=False)
        return result

    print(f"  Jackknife: PASS")

    # ── Gate 4: Full test verdict ──────────────────────────────────────────────
    print(f"\n--- GATE 4: FULL TEST VERDICT ---")
    print(f"  IS VR(20) = {vr20_full:.6f}  p_rw(N={N_SURR_FULL}) = {p_rw_full:.6f}")
    print(f"  Alpha = {PASS_P_RW_FULL:.6f}  Inconclusive zone: [{PASS_P_RW_FULL:.6f}, 0.05)")

    if np.isfinite(p_rw_full) and p_rw_full < PASS_P_RW_FULL:
        # Sub-diffusion direction check
        if np.isfinite(vr20_full) and vr20_full >= 1.0:
            # Impossible if p_rw < alpha on lower tail — flag as runner error
            verdict_label = "RUNNER_ERROR_VR_GE_1_WITH_LOW_P"
            print(f"  !! RUNNER ERROR: VR={vr20_full:.6f} >= 1.0 but p_rw < alpha — impossible on one-sided lower test")
        else:
            # Check power
            if underpowered:
                verdict_label = "INCONCLUSIVE-LEANING-PASS"
                print(f"  p_rw < alpha BUT power={ref_power:.3f} < {POWER_UNDERPOWERED} -> INCONCLUSIVE-LEANING-PASS")
            else:
                verdict_label = "PASS_PENDING_OOS_CHECK"
                print(f"  p_rw < alpha AND power adequate -> PASS (pending OOS sign-reversal check)")
    elif np.isfinite(p_rw_full) and p_rw_full < 0.05:
        verdict_label = "INCONCLUSIVE-LEANING-FAIL"
        print(f"  p_rw ∈ [{PASS_P_RW_FULL:.6f}, 0.05) -> INCONCLUSIVE-LEANING-FAIL")
    else:
        if underpowered:
            verdict_label = "INCONCLUSIVE-UNDERPOWERED"
            print(f"  p_rw >= 0.05 AND underpowered -> INCONCLUSIVE-UNDERPOWERED")
        else:
            verdict_label = "SCREENED-NEGATIVE"
            print(f"  p_rw >= 0.05 AND powered -> SCREENED-NEGATIVE")

    # ── Revision-1 Mandate 2: Disjoint sub-window check ───────────────────────
    print(f"\n--- REVISION-1 MANDATE 2: DISJOINT SUB-WINDOW 1998-07-07 to 2005-07 ---")
    disjoint_end_ts = pd.Timestamp(DISJOINT_SUBWINDOW_END)
    disjoint_mask = idx_is <= disjoint_end_ts
    # Only include dates >= TRIM_START_DATE (already handled by trim)
    X_disjoint = X_is[disjoint_mask]
    idx_disjoint = idx_is[disjoint_mask]
    n_disjoint = int(np.sum(np.isfinite(X_disjoint)))
    print(f"  Disjoint IS segment: {idx_disjoint[0].date()} → {idx_disjoint[-1].date()}")
    print(f"  Rows: {len(X_disjoint)}  Valid: {n_disjoint}")

    vr20_dj, p_rw_dj, surr_dj = surrogate_pval(
        X_disjoint, VR_Q_PRIMARY, N_SURR_FULL, SEED + 50, "rw")
    dist_dj = dist_stats(surr_dj)
    print(f"  VR(20) = {vr20_dj:.6f}  p_rw(N={N_SURR_FULL}) = {p_rw_dj:.6f}  "
          f"surr[p5={dist_dj['p5']}, p50={dist_dj['p50']}, p95={dist_dj['p95']}]")
    if np.isfinite(p_rw_dj):
        if p_rw_dj < PASS_P_RW_FULL:
            dj_interpretation = f"PASS at alpha={PASS_P_RW_FULL:.6f} — unpeeked slice shows sub-diffusion"
        elif p_rw_dj < 0.05:
            dj_interpretation = f"BORDERLINE (p∈[{PASS_P_RW_FULL:.6f}, 0.05))"
        else:
            dj_interpretation = "FAIL at alpha=0.05 — sub-diffusion absent in unpeeked slice"
    else:
        dj_interpretation = "insufficient data for VR computation"
    print(f"  Interpretation: {dj_interpretation}")

    disjoint_subwindow = {
        "start": str(idx_disjoint[0].date()) if len(idx_disjoint) > 0 else None,
        "end":   str(idx_disjoint[-1].date()) if len(idx_disjoint) > 0 else None,
        "n_rows": int(len(X_disjoint)),
        "n_valid": n_disjoint,
        "vr20":  round(vr20_dj, 6) if np.isfinite(vr20_dj) else None,
        "p_rw_N500": round(p_rw_dj, 6) if np.isfinite(p_rw_dj) else None,
        "surr_dist": dist_dj,
        "interpretation": dj_interpretation,
        "mandate": "Revision-1 Mandate 2 — the only unpeeked VR look in existence",
    }
    result["disjoint_subwindow"] = disjoint_subwindow

    # ── Gate 5: OOS sign-reversal check ───────────────────────────────────────
    print(f"\n--- OOS SECONDARY CHARACTERISATION (NON-PROMOTABLE) ---")
    print(f"  NOTE: OOS was peeked during doc-49 defect diagnosis (VR=0.797 observed).")
    print(f"  OOS is NON-PROMOTABLE as confirmation. OOS sign-reversal veto still applies.")
    vr20_oos, p_rw_oos, surr_oos = surrogate_pval(
        X_oos, VR_Q_PRIMARY, N_SURR_FULL, SEED + 200, "rw")
    dist_oos = dist_stats(surr_oos)
    print(f"  OOS VR(20) = {vr20_oos:.6f}  p_rw(N={N_SURR_FULL}) = {p_rw_oos:.6f}  "
          f"surr[p5={dist_oos['p5']}, p50={dist_oos['p50']}, p95={dist_oos['p95']}]")

    # OOS sign-reversal kill flag: VR_oos > 1 AND p_rw_oos < 0.05 (upper tail, super-diffusive)
    # p_rw_oos is fraction of surrogates <= real VR; for super-diffusive (VR>1), we need
    # the UPPER tail: fraction of surrogates >= real VR = 1 - p_rw_oos (approximately)
    oos_sign_reversal = False
    oos_sign_reversal_p = float("nan")
    if np.isfinite(vr20_oos) and vr20_oos > 1.0 and np.isfinite(p_rw_oos):
        # p_rw is fraction of surrogates <= real_vr (lower tail)
        # For upper-tail check: compute fraction of surrogates >= real_vr
        if surr_oos:
            surr_arr = np.array(surr_oos)
            n_gte = int(np.sum(surr_arr >= vr20_oos))
            p_upper = (n_gte + 1.0) / (len(surr_arr) + 1.0)
            oos_sign_reversal_p = p_upper
            if p_upper < 0.05:
                oos_sign_reversal = True
                print(f"  !! OOS SIGN-REVERSAL KILL FLAG: VR_oos={vr20_oos:.6f} > 1 AND "
                      f"p_upper={p_upper:.6f} < 0.05")
    if not oos_sign_reversal:
        print(f"  OOS sign-reversal kill: NOT TRIGGERED "
              f"(VR_oos={vr20_oos:.6f}, p_upper={oos_sign_reversal_p:.6f})")

    result["oos_secondary"] = {
        "n_rows": int(len(X_oos)),
        "n_valid": n_oos_valid,
        "oos_start": str(idx_oos[0].date()),
        "oos_end":   str(idx_oos[-1].date()),
        "vr20":  round(vr20_oos, 6) if np.isfinite(vr20_oos) else None,
        "p_rw_N500_lower_tail": round(p_rw_oos, 6) if np.isfinite(p_rw_oos) else None,
        "p_upper_tail": round(oos_sign_reversal_p, 6) if np.isfinite(oos_sign_reversal_p) else None,
        "surr_dist": dist_oos,
        "oos_sign_reversal_flag": oos_sign_reversal,
        "note": "NON-PROMOTABLE (OOS was peeked at VR=0.797 during doc-49 defect diagnosis)",
    }

    # ── Final verdict ──────────────────────────────────────────────────────────
    print(f"\n--- FINAL VERDICT ---")
    if verdict_label == "PASS_PENDING_OOS_CHECK":
        if oos_sign_reversal:
            final_verdict = "CANDIDATE-OOS-SIGNAL"
            print(f"  IS PASS but OOS SIGN-REVERSAL KILL FLAG triggered")
            print(f"  -> CANDIDATE-OOS-SIGNAL (requires researcher decision before advancing)")
        else:
            final_verdict = "ACTIVE-IS-CONFIRMED-PEEK-CONDITIONED"
            print(f"  IS PASS + no OOS sign-reversal")
            print(f"  -> ACTIVE-IS-CONFIRMED-PEEK-CONDITIONED (Revision-1 Mandate 1)")
            print(f"  NEVER 'clean' confirmation — peeked doc-49 IS slice is ~64% of this IS window")
    elif verdict_label == "INCONCLUSIVE-LEANING-PASS":
        if oos_sign_reversal:
            final_verdict = "CANDIDATE-OOS-SIGNAL"
        else:
            final_verdict = "INCONCLUSIVE-LEANING-PASS"
        print(f"  -> {final_verdict}")
    else:
        final_verdict = verdict_label

    print(f"\n  FINAL VERDICT: {final_verdict}")

    result["verdict"] = final_verdict
    result["kill_gates"] = {
        "f_betaupdate":     "PASS (0.000 by construction)",
        "flat_bar":         "PASS",
        "adr003":           "PASS",
        "speed_gate_N200":  f"PASS (p_rw={p_rw_speed:.6f} <= {PASS_P_RW_SPEED})",
        "jackknife":        f"{'KILL' if jk_kill else 'PASS'}",
        "full_test_N500":   (f"p_rw={p_rw_full:.6f}"
                             if np.isfinite(p_rw_full) else "N/A"),
        "oos_sign_reversal": ("KILL" if oos_sign_reversal else "PASS"),
        "power_branch":     (f"{'UNDERPOWERED' if underpowered else 'ADEQUATE'} "
                             f"(power@ref_vr0.90={ref_power:.3f})"),
    }

    # Write results
    _write_results(result)
    _write_results_doc(result, X_is, idx_is)
    return result


def _finalize_and_write(result: dict, X_is: np.ndarray, idx_is: pd.DatetimeIndex,
                         X_oos: np.ndarray, idx_oos: pd.DatetimeIndex,
                         power_ref: dict, power_obs: dict | None,
                         n_is_valid: int, n_oos_valid: int,
                         vr20_is: float, p_rw_is: float, dist_is: dict,
                         speed_gate_kill: bool) -> None:
    """Complete the remaining mandatory checks (disjoint sub-window, OOS) for early-exit paths."""

    # Revision-1 Mandate 2: Disjoint sub-window (even on speed gate kill)
    print(f"\n--- REVISION-1 MANDATE 2: DISJOINT SUB-WINDOW (running despite early exit) ---")
    disjoint_end_ts = pd.Timestamp(DISJOINT_SUBWINDOW_END)
    disjoint_mask = idx_is <= disjoint_end_ts
    X_disjoint = X_is[disjoint_mask]
    idx_disjoint = idx_is[disjoint_mask]
    n_disjoint = int(np.sum(np.isfinite(X_disjoint)))
    print(f"  Disjoint IS: {idx_disjoint[0].date() if len(idx_disjoint) else 'N/A'} → "
          f"{idx_disjoint[-1].date() if len(idx_disjoint) else 'N/A'}  "
          f"rows={len(X_disjoint)}  valid={n_disjoint}")

    vr20_dj, p_rw_dj, surr_dj = surrogate_pval(
        X_disjoint, VR_Q_PRIMARY, N_SURR_FULL, SEED + 50, "rw")
    dist_dj = dist_stats(surr_dj)
    print(f"  VR(20)={vr20_dj:.6f}  p_rw={p_rw_dj:.6f}  "
          f"surr[p5={dist_dj['p5']}, p50={dist_dj['p50']}, p95={dist_dj['p95']}]")

    if np.isfinite(p_rw_dj):
        if p_rw_dj < PASS_P_RW_FULL:
            dj_interp = "PASS at alpha — unpeeked slice shows sub-diffusion"
        elif p_rw_dj < 0.05:
            dj_interp = "BORDERLINE"
        else:
            dj_interp = "FAIL — sub-diffusion absent in unpeeked slice"
    else:
        dj_interp = "insufficient data"

    result["disjoint_subwindow"] = {
        "start": str(idx_disjoint[0].date()) if len(idx_disjoint) > 0 else None,
        "end":   str(idx_disjoint[-1].date()) if len(idx_disjoint) > 0 else None,
        "n_rows": int(len(X_disjoint)),
        "n_valid": n_disjoint,
        "vr20": round(vr20_dj, 6) if np.isfinite(vr20_dj) else None,
        "p_rw_N500": round(p_rw_dj, 6) if np.isfinite(p_rw_dj) else None,
        "surr_dist": dist_dj,
        "interpretation": dj_interp,
        "mandate": "Revision-1 Mandate 2",
    }

    # OOS secondary (informational)
    print(f"\n--- OOS SECONDARY (informational, early-exit path) ---")
    vr20_oos, p_rw_oos, surr_oos = surrogate_pval(
        X_oos, VR_Q_PRIMARY, N_SURR_FULL, SEED + 200, "rw")
    dist_oos_r = dist_stats(surr_oos)
    print(f"  OOS VR(20)={vr20_oos:.6f}  p_rw={p_rw_oos:.6f}")

    oos_sign_reversal = False
    oos_sign_reversal_p = float("nan")
    if np.isfinite(vr20_oos) and vr20_oos > 1.0 and surr_oos:
        surr_arr = np.array(surr_oos)
        n_gte = int(np.sum(surr_arr >= vr20_oos))
        p_upper = (n_gte + 1.0) / (len(surr_arr) + 1.0)
        oos_sign_reversal_p = p_upper
        if p_upper < 0.05:
            oos_sign_reversal = True
            print(f"  OOS SIGN-REVERSAL (informational; speed gate killed IS already)")

    result["oos_secondary"] = {
        "n_rows": int(len(X_oos)),
        "n_valid": n_oos_valid,
        "oos_start": str(idx_oos[0].date()),
        "oos_end":   str(idx_oos[-1].date()),
        "vr20": round(vr20_oos, 6) if np.isfinite(vr20_oos) else None,
        "p_rw_N500_lower_tail": round(p_rw_oos, 6) if np.isfinite(p_rw_oos) else None,
        "p_upper_tail": round(oos_sign_reversal_p, 6) if np.isfinite(oos_sign_reversal_p) else None,
        "surr_dist": dist_oos_r,
        "oos_sign_reversal_flag": oos_sign_reversal,
        "note": "NON-PROMOTABLE (OOS peeked); informational for early-exit path",
    }

    _write_results(result)
    _write_results_doc(result, X_is, idx_is)


def _write_results(result: dict) -> None:
    """Write JSON results file."""
    os.makedirs(os.path.dirname(RESULTS_JSON), exist_ok=True)
    with open(RESULTS_JSON, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n  Results JSON written: {RESULTS_JSON}")


def _write_results_doc(result: dict, X_is: np.ndarray, idx_is: pd.DatetimeIndex) -> None:
    """Write the dense results markdown document satisfying all three Revision-1 mandates."""

    verdict = result.get("verdict", "UNKNOWN")
    c = result.get("construction", {})
    vr_is = result.get("vr_is_full", result.get("vr_speed_gate", {}))
    power = result.get("power", {})
    jk = result.get("jackknife", {})
    oos = result.get("oos_secondary", {})
    dj  = result.get("disjoint_subwindow", {})
    kg  = result.get("kill_gates", {})
    adr = result.get("adr003", {})
    fb  = result.get("flat_bar", {})

    power_ref = power.get("ref_vr", {})
    power_obs_d = power.get("obs_vr", {})
    ref_power_val = power_ref.get("empirical_power", "N/A")
    obs_power_val = power_obs_d.get("empirical_power", "N/A") if isinstance(power_obs_d, dict) else "N/A"

    vr20_is_val  = vr_is.get("vr20", "N/A")
    p_rw_200     = vr_is.get("p_rw_N200", "N/A")
    p_rw_500     = vr_is.get("p_rw_N500", "N/A")
    p_garch      = vr_is.get("p_garch_N500", "N/A")
    p_ma1        = vr_is.get("p_ma1_N500", "N/A")
    p_ou         = vr_is.get("p_ou_N500", "N/A")

    null_dists   = vr_is.get("null_distributions", {})
    vr_grid_str  = vr_is.get("vr_grid", {})
    p_rw_grid_str = vr_is.get("p_rw_grid", {})

    doc_lines = []
    doc_lines.append("# Doc 50 — GC-SI Log-Ratio IS VR Results")
    doc_lines.append("")
    doc_lines.append(f"**Date executed:** 2026-06-10")
    doc_lines.append(f"**Pre-registration:** docs/research/50_gc_si_log_ratio_prereg.md (REVISION 1 binding)")
    doc_lines.append(f"**Runner:** scripts/run_50_gc_si_log_ratio.py")
    doc_lines.append(f"**Results JSON:** data/processed/50_results.json")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## REVISION-1 MANDATE 3 — RUN-CONDITIONING STATEMENT (binding)")
    doc_lines.append("")
    doc_lines.append("> α=0.0167 (Bonferroni 3-look) **partially prices multiplicity** across the")
    doc_lines.append("> three-look family (L1=doc-49 level-β screen; L2=2026-06-10 diagnostic peek")
    doc_lines.append("> at VR=0.947/0.797; L3=this test). However, α=0.0167 does **NOT** neutralize")
    doc_lines.append("> **conditional-existence selection**: this test was initiated BECAUSE the peek")
    doc_lines.append("> (L2) was favorable. That run-selection inflates the probability of a spurious")
    doc_lines.append("> pass in a manner Bonferroni does not fully correct. Therefore, **no claim that")
    doc_lines.append("> the peek contamination is fully corrected is permitted**. A PASS here registers")
    doc_lines.append("> as ACTIVE-IS-CONFIRMED-PEEK-CONDITIONED, not a clean confirmation. Clean")
    doc_lines.append("> confirmation requires either: (a) forward data post-2026-06 with a new prereg,")
    doc_lines.append("> or (b) the economics-stage trade statistic from a separate prereg.")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## Verdict")
    doc_lines.append("")
    doc_lines.append(f"**{verdict}**")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## Step 0 — Pre-Registration Restatement")
    doc_lines.append("")
    doc_lines.append("- **Hypothesis:** IS log-ratio X_t = ln(GC2!) − ln(SI2!) exhibits VR(20) < 1 relative to RW null")
    doc_lines.append("- **Object:** β=1 definitional in log space; f_βupdate=0 identically")
    doc_lines.append(f"- **Trim start (frozen):** {c.get('trim_start_date', TRIM_START_DATE)}")
    doc_lines.append("- **Split:** 70/30 row-count chronological")
    doc_lines.append("- **Primary statistic:** IS VR(20), p_rw(N=500) < 0.0167 (Bonferroni 3-look)")
    doc_lines.append("- **q grid:** {2, 5, 10, 20, 40}; q=20 primary, no argmax")
    doc_lines.append("- **Null families:** RW (gating), GARCH (supporting), MA(1) (supporting), OU (reference)")
    doc_lines.append("- **N:** 200 speed gate, 500 full; seed=20260612")
    doc_lines.append("- **α:** 0.0167 (3-look Bonferroni); PASS=p<0.0167; INCONCLUSIVE=[0.0167,0.05)")
    doc_lines.append("- **Power sim:** AR(1)-increments cumulated (corrected doc-48 pattern); ref VR=0.90")
    doc_lines.append("- **OOS:** NON-PROMOTABLE (peeked); sign-reversal veto applies")
    doc_lines.append("- **Jackknife:** 5-block, max-drop ≤ 300%")
    doc_lines.append(f"- **Kill criteria (ordered):** FileNotFoundError → MEASUREMENT-INADMISSIBLE → ADR_003 → f_βupdate → speed_gate → jackknife → full_test → OOS_sign_reversal")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## Step 1 — Data Availability and Construction")
    doc_lines.append("")
    doc_lines.append(f"| Field | Value |")
    doc_lines.append(f"|---|---|")
    doc_lines.append(f"| GC2! raw bars | {c.get('n_bars_raw_gc', 'N/A')} |")
    doc_lines.append(f"| SI2! raw bars | {c.get('n_bars_raw_si', 'N/A')} |")
    doc_lines.append(f"| Aligned pre-trim | {c.get('n_aligned_pre_trim', 'N/A')} |")
    doc_lines.append(f"| Dropped by trim | {c.get('n_rows_dropped_trim', 'N/A')} |")
    doc_lines.append(f"| n_aligned post-trim | {c.get('n_aligned_post_trim', 'N/A')} |")
    doc_lines.append(f"| Actual date range | {c.get('actual_start_date', 'N/A')} → {c.get('actual_end_date', 'N/A')} |")
    doc_lines.append(f"| GC2! masked (log-ret, k=8) | {c.get('n_gc_masked', 'N/A')} |")
    doc_lines.append(f"| SI2! masked (log-ret, k=8) | {c.get('n_si_masked', 'N/A')} |")
    doc_lines.append(f"| Combined masked | {c.get('n_combined_masked', 'N/A')} |")
    doc_lines.append(f"| n_valid X_t bars | {c.get('n_valid_total', 'N/A')} |")
    doc_lines.append(f"| IS rows / valid | {c.get('n_is_rows', 'N/A')} / {c.get('n_is_valid', 'N/A')} |")
    doc_lines.append(f"| OOS rows / valid | {c.get('n_oos_rows', 'N/A')} / {c.get('n_oos_valid', 'N/A')} |")
    doc_lines.append(f"| IS date range | {c.get('is_start', 'N/A')} → {c.get('is_end', 'N/A')} |")
    doc_lines.append(f"| OOS date range | {c.get('oos_start', 'N/A')} → {c.get('oos_end', 'N/A')} |")
    doc_lines.append(f"| β-mode | {c.get('beta_mode', 'N/A')} |")
    doc_lines.append(f"| f_βupdate | {c.get('f_betaupdate', 'N/A')} (identically zero; gate PASS) |")
    doc_lines.append("")
    doc_lines.append("### ADR_003 Assertions")
    doc_lines.append("")
    doc_lines.append(f"| Event | Caught | Date | Log-ret | Robust Z |")
    doc_lines.append(f"|---|---|---|---|---|")
    doc_lines.append(f"| SI2! {ADR003_SI_DATE} | {adr.get('SI2!_caught', 'N/A')} | {adr.get('SI2!_date', 'N/A')} | {adr.get('SI2!_log_ret', 'N/A')} | {adr.get('SI2!_robust_z', 'N/A')} |")
    doc_lines.append(f"| GC2! {ADR003_GC_DATE} | {adr.get('GC2!_caught', 'N/A')} | {adr.get('GC2!_date', 'N/A')} | {adr.get('GC2!_log_ret', 'N/A')} | {adr.get('GC2!_robust_z', 'N/A')} |")
    doc_lines.append(f"| Gate | {kg.get('adr003', 'N/A')} |||")
    doc_lines.append("")
    doc_lines.append("### Flat-Bar Gate")
    doc_lines.append("")
    doc_lines.append(f"| Leg | Flat-bar % in IS | Gate |")
    doc_lines.append(f"|---|---|---|")
    doc_lines.append(f"| GC2! | {fb.get('GC2!_flat_pct_is', 'N/A')}% | {fb.get('gate', 'N/A')} |")
    doc_lines.append(f"| SI2! | {fb.get('SI2!_flat_pct_is', 'N/A')}% | {fb.get('gate', 'N/A')} |")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## Step 2 — Speed Gate (N=200)")
    doc_lines.append("")
    doc_lines.append(f"- IS VR(20) = {vr20_is_val}")
    doc_lines.append(f"- p_rw(N=200) = {p_rw_200}")
    doc_lines.append(f"- Kill threshold: p > 0.20")
    doc_lines.append(f"- Gate: {kg.get('speed_gate_N200', 'N/A')}")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## Step 3 — Power Simulation (MANDATORY)")
    doc_lines.append("")
    doc_lines.append("Pattern: AR(1)-increments cumulated (corrected doc-48 block); α=0.0167; n=n_IS_valid.")
    doc_lines.append("")
    doc_lines.append(f"| Target VR | phi | Theoretical VR | Mean realized VR | Empirical power |")
    doc_lines.append(f"|---|---|---|---|---|")
    doc_lines.append(f"| {power_ref.get('vr_target','N/A')} (ref) | {power_ref.get('phi_target_ar1','N/A')} | {power_ref.get('vr_ar1_theoretical','N/A')} | {power_ref.get('mean_realized_vr','N/A')} | **{ref_power_val}** |")
    if isinstance(power_obs_d, dict) and "vr_target" in power_obs_d:
        doc_lines.append(f"| {power_obs_d.get('vr_target','N/A')} (obs) | {power_obs_d.get('phi_target_ar1','N/A')} | {power_obs_d.get('vr_ar1_theoretical','N/A')} | {power_obs_d.get('mean_realized_vr','N/A')} | {obs_power_val} |")
    doc_lines.append("")
    doc_lines.append(f"**Underpowered branch (power < 0.30): {'YES' if power.get('underpowered', False) else 'NO'}**")
    doc_lines.append("")
    doc_lines.append("*Ex ante disclosure: With n_IS ≈ 4,911 bars, α=0.0167, ref VR=0.90, the corrected")
    doc_lines.append("AR(1)-increments power simulation was expected to yield ~0.20–0.35. This range was")
    doc_lines.append("known and disclosed in the pre-registration before execution.*")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")

    if "vr_is_full" in result:
        doc_lines.append("## Step 4 — Full Test (N=500): IS VR, All Nulls, Full q Grid")
        doc_lines.append("")
        doc_lines.append("### Primary null results at q=20")
        doc_lines.append("")
        doc_lines.append(f"| Null | VR(20) | p-value | Surr p5 | Surr p50 | Surr p95 | Role |")
        doc_lines.append(f"|---|---|---|---|---|---|---|")
        for null_t, label_str, role in [
            ("rw",    "RW",         "PRIMARY GATE"),
            ("garch", "GARCH(1,1)", "supporting"),
            ("ma1",   "MA(1)",      "supporting"),
            ("ou",    "OU",         "reference"),
        ]:
            nd = null_dists.get(null_t, {})
            vr_v = nd.get("vr20", "N/A")
            pv   = nd.get("p_val", "N/A")
            d    = nd.get("surr_dist", {})
            doc_lines.append(f"| {label_str} | {vr_v} | {pv} | {d.get('p5','N/A')} | {d.get('p50','N/A')} | {d.get('p95','N/A')} | {role} |")
        doc_lines.append("")
        doc_lines.append(f"Also: p_rw(N=200)={p_rw_200}  p_rw(N=500)={p_rw_500}  p_garch={p_garch}  p_ma1={p_ma1}  p_ou={p_ou}")
        doc_lines.append("")
        doc_lines.append("### Full q grid (IS, RW null, N=500) — FULL SEARCH REPORTED (no argmax)")
        doc_lines.append("")
        doc_lines.append(f"| q | VR(q) | p_rw | Note |")
        doc_lines.append(f"|---|---|---|---|")
        for q in VR_Q_GRID:
            vr_v = vr_grid_str.get(str(q), "N/A")
            pv   = p_rw_grid_str.get(str(q), "N/A")
            note = "**PRIMARY**" if q == VR_Q_PRIMARY else ""
            doc_lines.append(f"| {q} | {vr_v} | {pv} | {note} |")
        doc_lines.append("")
        doc_lines.append("---")
        doc_lines.append("")

    if "jackknife" in result and jk:
        doc_lines.append("## Step 5 — Jackknife (5-block)")
        doc_lines.append("")
        doc_lines.append(f"- Full IS VR(20): {jk.get('full_vr20', 'N/A')}")
        doc_lines.append(f"- Kill range: [{jk.get('kill_lower','N/A')}, {jk.get('kill_upper','N/A')}]")
        doc_lines.append(f"- JK values: {jk.get('jk_vrs', [])}")
        doc_lines.append(f"- JK min/med/max: {jk.get('jk_min','N/A')} / {jk.get('jk_med','N/A')} / {jk.get('jk_max','N/A')}")
        doc_lines.append(f"- Kill: {'YES (CONCENTRATION-UNSTABLE)' if jk.get('kill') else 'NO (PASS)'}")
        doc_lines.append("")
        doc_lines.append("---")
        doc_lines.append("")

    doc_lines.append("## REVISION-1 MANDATE 2 — Disjoint Sub-Window Check (binding)")
    doc_lines.append("")
    doc_lines.append("**The 1998-07-07 → 2005-07 segment is the ONLY unpeeked slice in existence.**")
    doc_lines.append("Doc-49 peek covered the 2005-2018 IS slice; this segment was not seen.")
    doc_lines.append("A PASS whose significance is absent here carries the PEEK-CONDITIONED label with explicit warning.")
    doc_lines.append("")
    doc_lines.append(f"| Field | Value |")
    doc_lines.append(f"|---|---|")
    doc_lines.append(f"| Segment | {dj.get('start','N/A')} → {dj.get('end','N/A')} |")
    doc_lines.append(f"| Rows / valid | {dj.get('n_rows','N/A')} / {dj.get('n_valid','N/A')} |")
    doc_lines.append(f"| VR(20) | {dj.get('vr20','N/A')} |")
    doc_lines.append(f"| p_rw(N=500) | {dj.get('p_rw_N500','N/A')} |")
    doc_lines.append(f"| Surr p5/p50/p95 | {dj.get('surr_dist',{}).get('p5','N/A')} / {dj.get('surr_dist',{}).get('p50','N/A')} / {dj.get('surr_dist',{}).get('p95','N/A')} |")
    doc_lines.append(f"| Interpretation | {dj.get('interpretation','N/A')} |")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## OOS Secondary Characterisation (NON-PROMOTABLE)")
    doc_lines.append("")
    doc_lines.append("**OOS was peeked during doc-49 defect diagnosis (VR(20)=0.797 observed).**")
    doc_lines.append("OOS is NON-PROMOTABLE as a confirmation statistic within this prereg.")
    doc_lines.append("OOS confirmation for GC-SI can only come from the subsequent economics prereg.")
    doc_lines.append("")
    doc_lines.append(f"| Field | Value |")
    doc_lines.append(f"|---|---|")
    doc_lines.append(f"| OOS dates | {oos.get('oos_start','N/A')} → {oos.get('oos_end','N/A')} |")
    doc_lines.append(f"| OOS rows / valid | {oos.get('n_rows','N/A')} / {oos.get('n_valid','N/A')} |")
    doc_lines.append(f"| OOS VR(20) | {oos.get('vr20','N/A')} |")
    doc_lines.append(f"| OOS p_rw (lower tail) | {oos.get('p_rw_N500_lower_tail','N/A')} |")
    doc_lines.append(f"| OOS p_upper (super-diff veto) | {oos.get('p_upper_tail','N/A')} |")
    doc_lines.append(f"| Surr p5/p50/p95 | {oos.get('surr_dist',{}).get('p5','N/A')} / {oos.get('surr_dist',{}).get('p50','N/A')} / {oos.get('surr_dist',{}).get('p95','N/A')} |")
    doc_lines.append(f"| OOS sign-reversal kill flag | {'YES' if oos.get('oos_sign_reversal_flag') else 'NO'} |")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## Kill Gates Summary")
    doc_lines.append("")
    doc_lines.append("Gates applied in pre-registered order. First triggered terminates test.")
    doc_lines.append("")
    doc_lines.append(f"| Gate | Result |")
    doc_lines.append(f"|---|---|")
    for gate_name, gate_val in kg.items():
        doc_lines.append(f"| {gate_name} | {gate_val} |")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## Registry Transition")
    doc_lines.append("")
    if verdict == "ACTIVE-IS-CONFIRMED-PEEK-CONDITIONED":
        doc_lines.append("**GC-SI log-ratio → ACTIVE-IS-CONFIRMED-PEEK-CONDITIONED (second-sleeve candidate)**")
        doc_lines.append("")
        doc_lines.append("- IS VR confirmed at p<0.0167 (Bonferroni-3-look).")
        doc_lines.append("- PEEK-CONDITIONED label is permanent for this test: ~64% of IS rows were peeked.")
        doc_lines.append("- Next gate: economics pre-registration (OOS Sharpe > 0.50, n ≥ 30 trades, cost 0.005).")
        doc_lines.append("- Combination gate (LE-GF + GC-SI two-sleeve book) remains BLOCKED pending economics prereg.")
        doc_lines.append("- Clean confirmation requires economics prereg or forward data post-2026-06.")
    elif verdict == "SCREENED-NEGATIVE":
        doc_lines.append("**GC-SI log-ratio → SCREENED-NEGATIVE**")
        doc_lines.append("")
        doc_lines.append("- Apparatus powered (power ≥ 0.30 at ref VR=0.90); absence is informative.")
        doc_lines.append("- Cohort remains thin. Single-sleeve LE-GF unchanged.")
        doc_lines.append("- Named options: (a) pre-1998 data; (b) accept single-sleeve; (c) other pairs.")
    elif "INCONCLUSIVE-UNDERPOWERED" in verdict:
        doc_lines.append("**GC-SI log-ratio → INCONCLUSIVE-UNDERPOWERED**")
        doc_lines.append("")
        doc_lines.append(f"- Power < 0.30 at ref VR=0.90 (observed: {ref_power_val}).")
        doc_lines.append("- Cannot distinguish trending from moderately-mean-reverting.")
        doc_lines.append("- Data-depth options: (a) pre-1998 GC2!/SI2! history; (b) accept single-sleeve LE-GF; (c) different platinum data source.")
    elif "INCONCLUSIVE" in verdict:
        doc_lines.append(f"**GC-SI log-ratio → {verdict}**")
        doc_lines.append("")
        doc_lines.append("- Not a pass; not a clean negative.")
        doc_lines.append("- Stricter α due to peek; bare-α pass would be p<0.05.")
        doc_lines.append("- Surface to researcher for decision.")
    else:
        doc_lines.append(f"**GC-SI log-ratio → {verdict}**")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## Programme Status")
    doc_lines.append("")
    doc_lines.append("- **LE-GF:** IS-ONLY CONFIRMED (p=0.024, doc 46); OOS-STRUCTURAL-WEAKNESS (doc 48).")
    doc_lines.append("- **RB-CL:** PERMANENTLY ARCHIVED (third look p=0.0798, doc 48).")
    doc_lines.append("- **NG selectivity:** KILLED (docs 23/31).")
    doc_lines.append("- **BRN calendar:** MERELY-TRUE (doc 36).")
    doc_lines.append(f"- **GC-SI log-ratio (this doc):** {verdict}")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("*Pre-registration frozen 2026-06-10. No parameters revised post-execution.*")

    os.makedirs(os.path.dirname(RESULTS_DOC), exist_ok=True)
    with open(RESULTS_DOC, "w") as f:
        f.write("\n".join(doc_lines) + "\n")
    print(f"  Results doc written: {RESULTS_DOC}")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    result = run_doc50()
    print(f"\n{'='*72}")
    print(f"DOC 50 COMPLETE — VERDICT: {result.get('verdict', 'UNKNOWN')}")
    print(f"JSON: {RESULTS_JSON}")
    print(f"DOC:  {RESULTS_DOC}")
    print(f"{'='*72}")
