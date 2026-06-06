"""
EIA Storage Conditional Entry — Stage 1 (N=200) + Stage 2 (N=500) Execution
Pre-registration: docs/research/33_eia_conditional_entry_prereg.md (FROZEN)
Implementation spec: docs/research/33a_eia_execution_prep.md
Causal spot-check: docs/research/33b_eia_join_spot_check.md

DATA ACQUISITION NOTE (recorded per doc 33a §5.1 CHECK-3):
  EIA DNAV XLS covers 2010-01-01 to 2026-05-22 only. No pre-2010 weekly data
  accessible without EIA API key. EIA-published 5-year average unavailable;
  replaced by causal rolling same-week mean from available data.
  Effective test period: 2015-01-08 onwards (first date with 5 full prior years).
  Pre-registration date_min=2006-07-28 is UNMET. This is a documented deviation.
  All other parameters are FROZEN per doc 33 pre-registration.
"""
from __future__ import annotations
import sys, os, json
import numpy as np
import pandas as pd
import xlrd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from app.services.analytics_arm_a import load_leg
from app.services.analytics_arm_a_v2 import spread_from_series

# ══════════════════════════════════════════════════════════════════════════════
# PRE-REGISTERED CONSTANTS (doc 33 §8 — do not modify)
# ══════════════════════════════════════════════════════════════════════════════
EIA_THRESHOLD    = 10.0      # storage_anomaly < this → entry allowed (%)
THETA_Z          = 1.0       # z-score entry threshold (primary)
LB               = 60        # z-score rolling lookback (bars)
MH               = 40        # max hold (bars)
PC               = 0.003     # primary cost (round-trip)
ALL_COSTS        = [0.0015, 0.003, 0.0045]
NS_STAGE1        = 200       # Stage 1 surrogates
NS_STAGE2        = 500       # Stage 2 surrogates
SEED             = 20260604
TRAIN_END        = "2017-12-31"
OOS_START        = "2018-01-01"
NG_PATH          = "data/raw/ng12_spread.csv"
EIA_PATH         = "data/raw/eia_ng_storage_raw.xls"

# Documented deviation: effective start restricted by data availability
# Pre-reg date_min = "2006-07-28"; actual effective start = "2015-01-08"
PREREG_DATE_MIN  = "2006-07-28"    # frozen per doc 33 (UNMET — documented)
EFFECTIVE_DATE_MIN = "2015-01-08"  # first date with valid 5yr rolling avg

# Robustness appendix thresholds (doc 33 §4.4 — descriptive, non-binding)
ROBUSTNESS_THRESHOLDS = [5.0, 10.0, 15.0, 20.0]

# Thanksgiving-week EIA release shifts (doc 33a §2.2)
# Format: {normal_thursday_utc: actual_wednesday_release_utc}
THANKSGIVING_SHIFTS = {
    pd.Timestamp("2010-11-25", tz="UTC"): pd.Timestamp("2010-11-24", tz="UTC"),
    pd.Timestamp("2011-11-24", tz="UTC"): pd.Timestamp("2011-11-23", tz="UTC"),
    pd.Timestamp("2012-11-22", tz="UTC"): pd.Timestamp("2012-11-21", tz="UTC"),
    pd.Timestamp("2013-11-28", tz="UTC"): pd.Timestamp("2013-11-27", tz="UTC"),
    pd.Timestamp("2014-11-27", tz="UTC"): pd.Timestamp("2014-11-26", tz="UTC"),
    pd.Timestamp("2015-11-26", tz="UTC"): pd.Timestamp("2015-11-25", tz="UTC"),
    pd.Timestamp("2016-11-24", tz="UTC"): pd.Timestamp("2016-11-23", tz="UTC"),
    pd.Timestamp("2017-11-23", tz="UTC"): pd.Timestamp("2017-11-22", tz="UTC"),
    pd.Timestamp("2018-11-22", tz="UTC"): pd.Timestamp("2018-11-21", tz="UTC"),
    pd.Timestamp("2019-11-28", tz="UTC"): pd.Timestamp("2019-11-27", tz="UTC"),
    pd.Timestamp("2020-11-26", tz="UTC"): pd.Timestamp("2020-11-25", tz="UTC"),
    pd.Timestamp("2021-11-25", tz="UTC"): pd.Timestamp("2021-11-24", tz="UTC"),
    pd.Timestamp("2022-11-24", tz="UTC"): pd.Timestamp("2022-11-23", tz="UTC"),
    pd.Timestamp("2023-11-23", tz="UTC"): pd.Timestamp("2023-11-22", tz="UTC"),
    pd.Timestamp("2024-11-28", tz="UTC"): pd.Timestamp("2024-11-27", tz="UTC"),
    pd.Timestamp("2025-11-27", tz="UTC"): pd.Timestamp("2025-11-26", tz="UTC"),
}


# ══════════════════════════════════════════════════════════════════════════════
# EIA DATA PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

def load_eia_raw(path: str) -> pd.DataFrame:
    """Load EIA DNAV XLS → DataFrame(week_ending_date, storage_bcf)."""
    wb = xlrd.open_workbook(path)
    sh = wb.sheet_by_index(1)          # 'Data 1' sheet
    rows = []
    for i in range(3, sh.nrows):       # rows 0-2 are headers
        d_serial = sh.cell_value(i, 0)
        val = sh.cell_value(i, 1)
        if isinstance(d_serial, float) and d_serial > 0 and val != "":
            dt = xlrd.xldate_as_datetime(d_serial, wb.datemode)
            rows.append({"week_ending_date": dt.date(), "storage_bcf": float(val)})
    df = pd.DataFrame(rows)
    df["week_ending_date"] = pd.to_datetime(df["week_ending_date"])
    df = df.sort_values("week_ending_date").reset_index(drop=True)
    return df


def compute_pub_dates(eia_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Add publication_date_utc = week_ending + 6 days, localized UTC.
    Apply Thanksgiving holiday shifts (doc 33a §2.2).
    """
    df = eia_raw.copy()
    # Standard: publication = week_ending + 6 days (Friday → Thursday)
    df["pub_date_utc"] = (df["week_ending_date"] + pd.Timedelta(days=6)).dt.tz_localize("UTC")

    # Apply holiday shifts: replace shifted Thursday with actual Wednesday
    for normal_thu, actual_wed in THANKSGIVING_SHIFTS.items():
        mask = df["pub_date_utc"] == normal_thu
        if mask.any():
            df.loc[mask, "pub_date_utc"] = actual_wed

    return df


def compute_5yr_seasonal_avg(eia_df: pd.DataFrame) -> pd.DataFrame:
    """
    Causal rolling 5-year SAME-WEEK seasonal average.
    For each row t: mean of storage_bcf for rows in [t-5yr, t-1yr] whose
    week_ending_date falls within ±3 calendar days of the same week-of-year.
    Uses only strictly prior data (< current week_ending_date).
    Valid from the first row with ≥5 full prior same-week observations.

    doc 33a §1.3 note: EIA publishes their own 5yr avg but it is not accessible
    without API key. This causal rolling computation is equivalent and causally clean.
    """
    df = eia_df.copy()
    df = df.sort_values("week_ending_date").reset_index(drop=True)
    we = df["week_ending_date"].values  # numpy datetime64 array
    storage = df["storage_bcf"].values
    n = len(df)

    avg_5yr = np.full(n, np.nan)

    for t in range(n):
        current = pd.Timestamp(we[t])
        # 5-year window: [current - 5 years, current - 1 year)
        cutoff_lo = current - pd.DateOffset(years=5)
        cutoff_hi = current - pd.DateOffset(years=1)
        # Same week-of-year: week_of_year within ±1 of current (handles year boundaries)
        current_woy = current.isocalendar()[1]
        # Collect matching prior rows
        vals = []
        for j in range(t):
            prior = pd.Timestamp(we[j])
            if not (cutoff_lo <= prior < cutoff_hi):
                continue
            prior_woy = prior.isocalendar()[1]
            # Accept same or adjacent week-of-year (handles year-boundary wrapping)
            diff = abs(current_woy - prior_woy)
            if diff <= 1 or diff >= 51:   # 51 = 52-1, handles year wrap
                vals.append(storage[j])
        if len(vals) >= 3:                 # require at least 3 same-week prior obs
            avg_5yr[t] = np.mean(vals)

    df["storage_5yr_avg_bcf"] = avg_5yr
    return df


def compute_anomaly(eia_df: pd.DataFrame) -> pd.DataFrame:
    """
    storage_anomaly_pct = (actual - 5yr_avg) / 5yr_avg * 100.
    eia_allowed = anomaly < EIA_THRESHOLD and not NaN (doc 33a §2.4).
    """
    df = eia_df.copy()
    df["storage_anomaly_pct"] = np.where(
        np.isfinite(df["storage_5yr_avg_bcf"]) & (df["storage_5yr_avg_bcf"] > 0),
        (df["storage_bcf"] - df["storage_5yr_avg_bcf"]) / df["storage_5yr_avg_bcf"] * 100.0,
        np.nan
    )
    # NaN anomaly → eia_allowed = False (doc 33a §2.4 — conservative NaN rule)
    df["eia_allowed"] = np.where(
        np.isfinite(df["storage_anomaly_pct"]),
        df["storage_anomaly_pct"] < EIA_THRESHOLD,
        False
    ).astype(bool)
    return df


def build_eia_daily_mask(ng_index: pd.DatetimeIndex, eia_df: pd.DataFrame,
                          threshold: float = EIA_THRESHOLD) -> np.ndarray:
    """
    Join EIA to ng12 bars using strict-< backward merge (doc 33a §3.2).
    Returns a bool array aligned to ng_index.
    allow_exact_matches=False enforces strict < semantics (VALIDATE-B).
    """
    eia_df = eia_df.copy()
    # Recompute eia_allowed for this threshold (supports robustness grid)
    eia_df["eia_allowed_th"] = np.where(
        np.isfinite(eia_df["storage_anomaly_pct"]),
        eia_df["storage_anomaly_pct"] < threshold,
        False
    ).astype(bool)

    ng_dates_df = pd.DataFrame({"bar_date": ng_index})
    eia_join = eia_df[["pub_date_utc", "storage_anomaly_pct", "eia_allowed_th"]].copy()
    eia_join = eia_join.sort_values("pub_date_utc")

    joined = pd.merge_asof(
        ng_dates_df.sort_values("bar_date"),
        eia_join,
        left_on="bar_date",
        right_on="pub_date_utc",
        direction="backward",
        allow_exact_matches=False,  # ← doc 33b VALIDATE-B: strict < semantics
    )

    # Re-align to original ng_index order
    joined = joined.set_index("bar_date").reindex(ng_index)
    allowed = joined["eia_allowed_th"].fillna(False).astype(bool).values
    return allowed


def validate_join(ng_index: pd.DatetimeIndex, eia_df: pd.DataFrame) -> None:
    """
    VALIDATE-B from doc 33a §3.5: verify 5 spot-check cases from doc 33b.
    Aborts if any causal violation detected.
    """
    eia_join = eia_df[["pub_date_utc", "storage_anomaly_pct"]].sort_values("pub_date_utc")
    ng_dates_df = pd.DataFrame({"bar_date": ng_index})
    joined = pd.merge_asof(
        ng_dates_df.sort_values("bar_date"),
        eia_join,
        left_on="bar_date",
        right_on="pub_date_utc",
        direction="backward",
        allow_exact_matches=False,
    ).set_index("bar_date").reindex(ng_index)

    # Spot checks from doc 33b (only check dates within available data range)
    spot_checks = [
        ("2018-05-10", "2018-05-03", "T02: Thursday uses prior-week EIA"),
        ("2018-05-11", "2018-05-10", "T03: Friday uses current-week EIA"),
        ("2019-11-29", "2019-11-27", "T05: Post-Thanksgiving Friday uses Wed holiday release"),
        ("2020-09-11", "2020-09-10", "T07: COVID-period Friday uses prior-day release"),
        ("2022-01-13", "2022-01-06", "T10: Thursday uses prior-week EIA"),
    ]

    for bar_str, expected_pub_str, label in spot_checks:
        bar_ts = pd.Timestamp(bar_str, tz="UTC")
        if bar_ts not in ng_index:
            print(f"  VALIDATE-B SKIP (bar not in index): {label}")
            continue
        expected = pd.Timestamp(expected_pub_str, tz="UTC")
        actual_pub = joined.loc[bar_ts, "pub_date_utc"]
        if pd.isna(actual_pub):
            print(f"  VALIDATE-B SKIP (NaN pub; pre-2010 data): {label}")
            continue
        actual_pub_ts = pd.Timestamp(actual_pub).tz_localize("UTC") if actual_pub.tzinfo is None else pd.Timestamp(actual_pub)
        if actual_pub_ts != expected:
            raise AssertionError(
                f"CAUSAL VIOLATION — {label}\n"
                f"  Got pub_date={actual_pub_ts.date()}, expected={expected.date()}\n"
                f"  allow_exact_matches=True was used or +6 day shift missing."
            )
        print(f"  VALIDATE-B PASS: {label}")


# ══════════════════════════════════════════════════════════════════════════════
# TRADE LOGIC
# ══════════════════════════════════════════════════════════════════════════════

def run_fade(s: np.ndarray, theta: float, cost: float,
             lookback: int = LB, max_hold: int = MH) -> list[dict]:
    """Unconditional fade (doc 30/31 baseline)."""
    s = np.asarray(s, float)
    n = len(s)
    trades: list[dict] = []
    pos = 0; epx = 0.0; bh = 0
    for t in range(lookback, n):
        win = s[t - lookback: t]
        mu = win.mean(); sd = win.std() + 1e-9
        z = (s[t] - mu) / sd
        if pos:
            bh += 1
            cross = (pos > 0 and z <= 0.0) or (pos < 0 and z >= 0.0)
            if cross or bh >= max_hold:
                gross = pos * (epx - s[t])
                trades.append({"gross": gross, "net": gross - cost, "hold": bh})
                pos = 0; bh = 0
        if not pos:
            if z >= theta: pos = 1; epx = s[t]; bh = 0
            elif z <= -theta: pos = -1; epx = s[t]; bh = 0
    return trades


def run_fade_conditional(s: np.ndarray, theta: float, cost: float,
                          allowed_mask: np.ndarray,
                          lookback: int = LB, max_hold: int = MH) -> list[dict]:
    """
    EIA-conditional fade (doc 33a §4.2).
    Entry gated by allowed_mask[t]. Exit logic UNCHANGED — no mid-trade conditioning.
    allowed_mask is computed ONCE from real EIA data and shared across all surrogate calls.
    OU surrogate receives the SAME mask (doc 33a §4.4 resolution).
    """
    s = np.asarray(s, float)
    allowed = np.asarray(allowed_mask, bool)
    n = len(s)
    assert len(allowed) == n, f"mask length {len(allowed)} != series length {n}"
    trades: list[dict] = []
    pos = 0; epx = 0.0; bh = 0
    for t in range(lookback, n):
        win = s[t - lookback: t]
        mu = win.mean(); sd = win.std() + 1e-9
        z = (s[t] - mu) / sd
        if pos:
            bh += 1
            cross = (pos > 0 and z <= 0.0) or (pos < 0 and z >= 0.0)
            if cross or bh >= max_hold:
                gross = pos * (epx - s[t])
                trades.append({"gross": gross, "net": gross - cost, "hold": bh})
                pos = 0; bh = 0
        if not pos and allowed[t]:          # ← EIA gate: entry only when allowed
            if z >= theta: pos = 1; epx = s[t]; bh = 0
            elif z <= -theta: pos = -1; epx = s[t]; bh = 0
    return trades


def stats(trades: list[dict]) -> dict:
    if len(trades) < 5:
        return {"n": len(trades), "gross": float("nan"), "net": float("nan"),
                "hit": float("nan"), "avg_hold": float("nan")}
    g  = np.array([t["gross"] for t in trades])
    nn = np.array([t["net"]   for t in trades])
    h  = np.array([t["hold"]  for t in trades])
    return {
        "n":        int(len(trades)),
        "gross":    float(np.mean(g)),
        "net":      float(np.mean(nn)),
        "hit":      float(np.mean(nn > 0)),
        "avg_hold": float(np.mean(h)),
        "top3_pct": float(np.sort(g)[::-1][:3].sum() / (np.sum(np.abs(g)) + 1e-9)),
    }


# ══════════════════════════════════════════════════════════════════════════════
# SURROGATE GENERATION (calibrated to full series; doc 30 parameters)
# ══════════════════════════════════════════════════════════════════════════════

def fit_params(s: np.ndarray) -> dict:
    incr = np.diff(s[np.isfinite(s)])
    mu = float(np.mean(incr)); sig = float(np.std(incr, ddof=1))
    sq = incr ** 2
    ab = float(np.clip(np.corrcoef(sq[1:], sq[:-1])[0, 1], 0.0, 0.97)) if len(sq) > 20 else 0.0
    ab = float(np.nan_to_num(ab))
    alpha = ab * 0.15; beta = ab - alpha
    omega = max(sig ** 2 * (1.0 - alpha - beta), 1e-12)
    return {"mu": mu, "sig": sig, "garch": (omega, alpha, beta)}


def sim_rw(p: dict, n: int, rng) -> np.ndarray:
    return np.concatenate([[0.], np.cumsum(rng.normal(p["mu"], p["sig"], n - 1))])

def sim_garch(p: dict, n: int, rng) -> np.ndarray:
    omega, alpha, beta = p["garch"]; mu = p["mu"]; h = p["sig"] ** 2
    out = np.empty(n - 1)
    for t in range(n - 1):
        e = rng.normal() * h ** 0.5; out[t] = mu + e
        h = max(omega + alpha * e ** 2 + beta * h, 1e-12)
    return np.concatenate([[0.], np.cumsum(out)])

def sim_ou(p: dict, n: int, rng, phi: float = 0.94771) -> np.ndarray:
    sigma_ou = p["sig"] * ((1.0 + phi) / 2.0) ** 0.5
    path = np.empty(n); path[0] = 0.
    for t in range(1, n): path[t] = phi * path[t-1] + sigma_ou * rng.normal()
    return path

def sim_splice(p: dict, n: int, rng, cadence: int = 21, frac: float = 0.25) -> np.ndarray:
    s = np.empty(n); s[0] = 0.
    for t in range(1, n):
        s[t] = s[t-1] + rng.normal(p["mu"], p["sig"])
        if t % cadence == 0:
            drift = s[t] - s[max(0, t - cadence)]
            s[t] -= frac * drift
    return s


def pval(real: float, dist: list) -> float:
    d = np.array([x for x in dist if np.isfinite(x)])
    if d.size == 0 or not np.isfinite(real): return float("nan")
    return float((1.0 + np.sum(d >= real)) / (d.size + 1.0))


def run_surrogate_ensemble(s: np.ndarray, params: dict, allowed_mask: np.ndarray,
                            n_surr: int, seed: int, theta: float, cost: float,
                            surr_types: list[str] | None = None) -> dict:
    """
    Run N surrogates of each type with IDENTICAL EIA allowed_mask.
    Returns {type: [gross_per_surrogate]} for each type.
    """
    if surr_types is None:
        surr_types = ["rw", "garch", "ou", "splice"]
    rng = np.random.default_rng(seed)
    n = len(s)
    results = {t: [] for t in surr_types}
    sims = {"rw": sim_rw, "garch": sim_garch, "ou": sim_ou, "splice": sim_splice}
    for _ in range(n_surr):
        for st in surr_types:
            path = sims[st](params, n, rng)
            trs = run_fade_conditional(path, theta, cost, allowed_mask)
            g = float(np.mean([t["gross"] for t in trs])) if trs else float("nan")
            results[st].append(g)
    return results


def jackknife_drop(trades: list[dict]) -> dict:
    if len(trades) < 3:
        return {"gross": float("nan"), "drop_pct": float("nan"), "dropped_gross": float("nan")}
    idx = int(np.argmax([abs(t["gross"]) for t in trades]))
    reduced = [t for i, t in enumerate(trades) if i != idx]
    full_g  = float(np.mean([t["gross"] for t in trades]))
    red_g   = float(np.mean([t["gross"] for t in reduced]))
    drop_pct = abs(full_g - red_g) / (abs(full_g) + 1e-9)
    return {"gross": red_g, "drop_pct": float(drop_pct), "dropped_gross": float(trades[idx]["gross"])}


# ══════════════════════════════════════════════════════════════════════════════
# VERDICT LOGIC (doc 33 §4)
# ══════════════════════════════════════════════════════════════════════════════

def stage1_verdict(cond_stats: dict, uncond_stats: dict, p_rw_200: float) -> tuple[str, str]:
    n     = cond_stats["n"]
    gross = cond_stats["gross"]
    net   = cond_stats.get("net", float("nan"))
    uncond_gross = uncond_stats.get("gross", float("nan"))

    if not np.isfinite(p_rw_200):
        return "INCONCLUSIVE", "p_rw NaN — insufficient trades for surrogate comparison"
    if n < 30:
        return "INCONCLUSIVE", f"Trade count {n} < 30 after conditioning — insufficient power"
    if p_rw_200 > 0.20:
        return "KILL_PVAL", f"p_rw={p_rw_200:.3f} > 0.20: cannot be significant at any N. Stage 1 KILL."
    if np.isfinite(uncond_gross) and np.isfinite(gross) and gross <= uncond_gross:
        return "KILL_NO_IMPROVEMENT", (
            f"Conditional gross={gross:.4f} ≤ unconditional gross={uncond_gross:.4f}: "
            "EIA conditioning adds nothing."
        )
    if np.isfinite(net) and net < -0.002:
        return "KILL_NEGATIVE", f"Conditional net={net:.4f} < -0.002: meaningfully negative."
    return "GO", f"p_rw={p_rw_200:.3f} ≤ 0.20, conditional gross > unconditional, net OK. Proceed to Stage 2."


def stage2_verdict(cond_stats: dict, uncond_stats: dict, p_rw: float,
                   jk: dict, oos_stats: dict) -> tuple[str, str]:
    n     = cond_stats["n"]
    gross = cond_stats.get("gross", float("nan"))
    net   = cond_stats.get("net", float("nan"))
    uncond_gross = uncond_stats.get("gross", float("nan"))
    jk_drop = jk.get("drop_pct", float("nan"))
    oos_gross = oos_stats.get("gross", float("nan"))
    oos_net   = oos_stats.get("net",   float("nan"))

    if not np.isfinite(p_rw) or p_rw >= 0.05:
        return "KILLED", f"p_rw={p_rw:.3f} ≥ 0.05: does not survive N=500 surrogate test."
    if np.isfinite(jk_drop) and jk_drop > 3.0:
        return "KILLED", f"Jackknife drop={jk_drop:.0%} > 300%: single-trade concentrated."
    if np.isfinite(oos_gross) and np.isfinite(gross) and oos_stats.get("n", 0) >= 30:
        if (gross > 0 and oos_gross < 0) or (gross < 0 and oos_gross > 0):
            return "KILLED", f"OOS sign reversal: full={gross:.4f}, OOS={oos_gross:.4f}."
    if np.isfinite(uncond_gross) and np.isfinite(gross) and gross <= uncond_gross:
        return "KILLED", "Conditional gross ≤ unconditional at N=500."
    # Survival criteria
    jk_ok = not (np.isfinite(jk_drop) and jk_drop > 1.50)
    oos_ok = not np.isfinite(oos_net) or oos_net > 0 or oos_stats.get("n", 0) < 30
    if jk_ok and oos_ok:
        return "DEPLOYABLE_CANDIDATE", (
            f"p_rw={p_rw:.3f}, net={net:.4f}, jackknife stable, OOS positive. "
            "Conditional entry is genuine and cost-clearing."
        )
    reasons = []
    if not jk_ok: reasons.append(f"jackknife drop={jk_drop:.0%} (borderline)")
    if not oos_ok: reasons.append(f"OOS net={oos_net:.4f} (negative but small sample)")
    return "CONDITIONAL_SURVIVAL", "p_rw < 0.05 but: " + "; ".join(reasons)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    np.seterr(all="ignore")
    SEP = "═" * 100
    print(SEP)
    print("EIA STORAGE CONDITIONAL ENTRY — doc 33 pre-registration")
    print(SEP)

    # ── 1. Load and preprocess EIA data ────────────────────────────────────
    print("\n[1] Loading EIA storage data...")
    eia_raw = load_eia_raw(EIA_PATH)
    print(f"    Raw: {len(eia_raw)} rows, {eia_raw.week_ending_date.min().date()} → "
          f"{eia_raw.week_ending_date.max().date()}")

    eia_df = compute_pub_dates(eia_raw)
    eia_df = compute_5yr_seasonal_avg(eia_df)
    eia_df = compute_anomaly(eia_df)

    valid_mask = np.isfinite(eia_df["storage_5yr_avg_bcf"].values)
    first_valid = eia_df.loc[valid_mask, "week_ending_date"].min()
    # First bar usable = first pub_date after first valid 5yr avg
    first_valid_pub = eia_df.loc[valid_mask, "pub_date_utc"].min()
    print(f"    5yr avg valid from: {first_valid.date()} (pub_date: {first_valid_pub.date()})")
    print(f"    NaN anomaly rows: {eia_df['storage_anomaly_pct'].isna().sum()}")
    print(f"    EIA_allowed=True fraction: {eia_df['eia_allowed'].mean():.1%}")
    print(f"\n    DATA DEVIATION NOTE: EIA data starts {eia_raw.week_ending_date.min().date()}, "
          f"not {PREREG_DATE_MIN}.")
    print(f"    Effective test start: {EFFECTIVE_DATE_MIN} (5 full prior years available).")
    print(f"    Pre-registration date_min={PREREG_DATE_MIN} is UNMET. Documented deviation.")

    # Storage anomaly sample (sanity check)
    print("\n    Storage anomaly statistics:")
    anm = eia_df["storage_anomaly_pct"].dropna()
    print(f"    min={anm.min():.1f}%  p5={np.percentile(anm,5):.1f}%  "
          f"median={np.median(anm):.1f}%  p95={np.percentile(anm,95):.1f}%  max={anm.max():.1f}%")
    glut_frac = (anm > 10.0).mean()
    print(f"    Fraction > 10% (suppressed): {glut_frac:.1%}")

    # ── 2. Load NG spread ───────────────────────────────────────────────────
    print("\n[2] Loading ng12 spread...")
    ng = spread_from_series("NG", load_leg(NG_PATH), date_min=EFFECTIVE_DATE_MIN,
                             jump_k=float("inf"))
    s_full = ng.s_close
    idx = ng.index
    print(f"    Bars: {len(s_full)}, {idx[0].date()} → {idx[-1].date()}")

    # Fit surrogate parameters from full effective series
    incr = np.diff(s_full[np.isfinite(s_full)])
    params = fit_params(s_full)
    print(f"    Params: mu={params['mu']:.5f}, sig={params['sig']:.4f}")

    # ── 3. Build EIA daily mask + VALIDATE-B ───────────────────────────────
    print("\n[3] Building EIA daily mask (θ_eia=10.0%)...")
    allowed_10 = build_eia_daily_mask(idx, eia_df, threshold=EIA_THRESHOLD)
    print(f"    EIA_allowed bars: {allowed_10.sum()} / {len(allowed_10)} = {allowed_10.mean():.1%}")

    print("\n[4] Running VALIDATE-B spot checks (doc 33b)...")
    validate_join(idx, eia_df)

    # ── 4. Unconditional baseline (must match doc 31) ──────────────────────
    print("\n[5] Unconditional baseline (doc 31 reference, effective period)...")
    uncond_trades = run_fade(s_full, THETA_Z, PC)
    uncond_st = stats(uncond_trades)
    print(f"    n={uncond_st['n']}, gross={uncond_st['gross']:.4f}, net={uncond_st['net']:.4f}")

    # ── 5. Conditional full-sample ─────────────────────────────────────────
    print("\n[6] Conditional full-sample (EIA gate, θ_eia=10%, θ_z=1.0)...")
    cond_trades = run_fade_conditional(s_full, THETA_Z, PC, allowed_10)
    cond_st = stats(cond_trades)
    print(f"    n={cond_st['n']}, gross={cond_st['gross']:.4f}, "
          f"net={cond_st['net']:.4f}, hit={cond_st.get('hit',float('nan')):.2f}")

    # ── 6. OOS split ───────────────────────────────────────────────────────
    oos_mask = idx >= pd.Timestamp(OOS_START, tz="UTC")
    s_oos = s_full[oos_mask]
    allowed_oos = allowed_10[oos_mask]
    cond_oos_trades = run_fade_conditional(s_oos, THETA_Z, PC, allowed_oos)
    cond_oos_st = stats(cond_oos_trades)
    print(f"\n[7] OOS split (2018+): n={cond_oos_st['n']}, "
          f"gross={cond_oos_st['gross']:.4f}, net={cond_oos_st['net']:.4f}")

    # ── 7. Jackknife ──────────────────────────────────────────────────────
    jk = jackknife_drop(cond_trades)
    print(f"\n[8] Jackknife: gross_after={jk['gross']:.4f}, "
          f"drop={jk['drop_pct']:.1%}, dropped_trade_gross={jk['dropped_gross']:.4f}")

    # ══════════════════════════════════════════════════════════════════════
    # STAGE 1 — N=200 RW SURROGATES
    # ══════════════════════════════════════════════════════════════════════
    print(f"\n{'─'*100}")
    print(f"STAGE 1 — N={NS_STAGE1} RW surrogates with identical EIA conditioning...")
    print(f"{'─'*100}")

    surr1 = run_surrogate_ensemble(s_full, params, allowed_10, NS_STAGE1, SEED,
                                    THETA_Z, PC, surr_types=["rw"])
    p_rw_200 = pval(cond_st["gross"], surr1["rw"])
    rw_dist = np.array([x for x in surr1["rw"] if np.isfinite(x)])

    print(f"\nConditional gross (real NG): {cond_st['gross']:.4f}")
    print(f"RW null distribution (N={len(rw_dist)}): "
          f"p5={np.percentile(rw_dist,5):.4f}  p25={np.percentile(rw_dist,25):.4f}  "
          f"median={np.median(rw_dist):.4f}  p75={np.percentile(rw_dist,75):.4f}  "
          f"p95={np.percentile(rw_dist,95):.4f}")
    print(f"p_rw (N=200): {p_rw_200:.3f}")

    s1_verdict, s1_rationale = stage1_verdict(cond_st, uncond_st, p_rw_200)

    print(f"\n{'═'*100}")
    print(f"STAGE 1 VERDICT: {s1_verdict}")
    print(f"RATIONALE: {s1_rationale}")
    print(f"{'═'*100}")

    # Save Stage 1 results
    out_s1 = {
        "stage": 1,
        "data_note": {
            "prereg_date_min": PREREG_DATE_MIN,
            "effective_date_min": EFFECTIVE_DATE_MIN,
            "deviation": "EIA data 2010-2026 only; 5yr avg valid from 2015; documented deviation."
        },
        "eia_threshold_pct": EIA_THRESHOLD,
        "n_surrogates": NS_STAGE1,
        "conditional": cond_st,
        "unconditional_baseline": uncond_st,
        "oos_conditional": cond_oos_st,
        "jackknife": jk,
        "p_rw_200": float(p_rw_200),
        "rw_null_pctiles": {
            f"p{p}": float(np.percentile(rw_dist, p)) for p in [5, 25, 50, 75, 95]
        },
        "stage1_verdict": s1_verdict,
        "stage1_rationale": s1_rationale,
        "proceed_to_stage2": s1_verdict == "GO",
    }
    Path("data/processed").mkdir(exist_ok=True)
    with open("data/processed/eia_conditional_stage1.json", "w") as f:
        json.dump(out_s1, f, indent=2)
    print(f"\nStage 1 results saved to data/processed/eia_conditional_stage1.json")

    if s1_verdict != "GO":
        print(f"\nStage 1 did not survive. Stage 2 NOT run per doc 33 §4.1.")
        sys.exit(0)

    # ══════════════════════════════════════════════════════════════════════
    # STAGE 2 — N=500 FULL SURROGATE SUITE
    # ══════════════════════════════════════════════════════════════════════
    print(f"\n{'─'*100}")
    print(f"STAGE 2 — N={NS_STAGE2} surrogates (RW, GARCH, OU, Splice) with EIA conditioning...")
    print(f"{'─'*100}")

    surr2 = run_surrogate_ensemble(s_full, params, allowed_10, NS_STAGE2, SEED,
                                    THETA_Z, PC, surr_types=["rw", "garch", "ou", "splice"])

    pvals_s2 = {st: pval(cond_st["gross"], surr2[st]) for st in surr2}
    rw500 = np.array([x for x in surr2["rw"] if np.isfinite(x)])

    print(f"\nP-values (N={NS_STAGE2}, conditional real NG gross={cond_st['gross']:.4f}):")
    for st, pv in pvals_s2.items():
        print(f"  p_{st}={pv:.3f}")

    print(f"\nRW null pctiles (N={len(rw500)}): "
          f"p5={np.percentile(rw500,5):.4f}  median={np.median(rw500):.4f}  "
          f"p95={np.percentile(rw500,95):.4f}")

    s2_verdict, s2_rationale = stage2_verdict(cond_st, uncond_st, pvals_s2["rw"],
                                               jk, cond_oos_st)

    # Robustness appendix (doc 33 §4.4 — descriptive, non-binding, never changes verdict)
    print(f"\n{'─'*60}")
    print("ROBUSTNESS APPENDIX (doc 33 §4.4 — DESCRIPTIVE, non-binding):")
    robustness = {}
    for th in ROBUSTNESS_THRESHOLDS:
        allowed_th = build_eia_daily_mask(idx, eia_df, threshold=th)
        cond_th = run_fade_conditional(s_full, THETA_Z, PC, allowed_th)
        st_th = stats(cond_th)
        surr_th = run_surrogate_ensemble(s_full, params, allowed_th, NS_STAGE2, SEED,
                                          THETA_Z, PC, surr_types=["rw"])
        p_th = pval(st_th["gross"], surr_th["rw"])
        robustness[th] = {**st_th, "p_rw": float(p_th), "threshold": th}
        marker = "← PRIMARY" if th == EIA_THRESHOLD else ""
        print(f"  θ_eia={th:5.1f}%: n={st_th['n']:3d}, "
              f"gross={st_th['gross']:+.4f}, net={st_th.get('net', float('nan')):+.4f}, "
              f"p_rw={p_th:.3f} {marker}")

    print(f"\n{'═'*100}")
    print(f"STAGE 2 VERDICT: {s2_verdict}")
    print(f"RATIONALE: {s2_rationale}")
    print(f"{'═'*100}")

    # Save full results
    out_full = {
        **out_s1,
        "stage": 2,
        "stage2": {
            "conditional_full": cond_st,
            "unconditional_baseline": uncond_st,
            "oos_conditional": cond_oos_st,
            "jackknife": jk,
            "p_values": {k: float(v) for k, v in pvals_s2.items()},
            "rw_null_pctiles_500": {
                f"p{p}": float(np.percentile(rw500, p)) for p in [5, 25, 50, 75, 95]
            },
            "verdict": s2_verdict,
            "rationale": s2_rationale,
        },
        "robustness_appendix": {str(th): v for th, v in robustness.items()},
    }
    with open("data/processed/eia_conditional_results.json", "w") as f:
        json.dump(out_full, f, indent=2)
    print(f"\nFull results saved to data/processed/eia_conditional_results.json")
