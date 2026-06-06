"""
Arm A — Deployment-Domain Habitat Discovery engine.

Implements doc 18 (pre-registration) + doc 18a (execution freeze) EXACTLY. Answers one question per
spread, at the corpus level, never per-bar:

    Is a causally-constructed, roll-handled spread's level-difference variance-ratio curve VR(q)
    distinguishable from its OWN matched surrogate null in the mean-reverting direction
    (VR < 1 AND VR < surrogate), robust across {RW, GARCH, OU} families and roll-clean subsamples?

CONSTITUTIONAL STATUS (CLAUDE.md §10; doc 18 §6): an OBSERVATORY VERDICT — distributional, corpus-level,
surrogate-relative. NOT a detector/score/timing object. Emits no per-bar series, no "T" column. It does NOT
touch μ*/Kalman/EMA residual, so it does not trip the doc-06 §15.8 reopen trigger.

DAG DISCIPLINE (one-way): self-contained on raw OHLCV legs. Imports nothing from μ*/Kalman/MRScore/State-T
paths and is never imported back into them. Mirrors analytics_substrate.py's terminal-observatory posture.

CAUSALITY (each guarded by a test in test_arm_a.py):
  • rolling β at bar t uses only data ≤ t-1 (C-3); future-injection leaves earlier β/spread bit-identical.
  • roll-transition detection uses a trailing (causal) robust scale with a FROZEN multiplier (ADR_003 R-6).
  • VR is computed in LEVEL-difference space (NP-1): defined through zero, never log/return on the spread.

FROZEN PARAMETERS (doc 18a — do not tune; changing post-result is a freeze-break):
  ROLL_BETA_W=60, ROLL_BETA_CADENCE=every-bar, β lagged 1 (C-3), warm-up mask W bars.
  VR_Q_GRID=(2,5,10,20), level-difference estimator, surrogate-relative verdict.
  Surrogates: RW / GARCH(1,1) / OU, N=200 each, causal fits, identical length+mask+extraction.
  Roll mask: continuous-futures leg |log-ret| > 8 × trailing-60 MAD → masked.
  Verdict: real VR(q) < 5th pct of ensemble at ≥1 q, robust across all 3 families + roll-clean.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

# ── FROZEN constants (doc 18 / doc 18a) ───────────────────────────────────────
VR_Q_GRID: tuple[int, ...] = (2, 5, 10, 20)
ROLL_BETA_W: int = 60
ROLL_BETA_W_ROBUST: int = 120          # non-verdict robustness display only
ROLL_MAD_WINDOW: int = 60
ROLL_MAD_K: float = 8.0                # frozen multiplier (ADR_003 R-6)
N_SURROGATE: int = 200
SURR_PCTILE: float = 5.0               # 5th-percentile gate (doc 18 §5)
SURR_FAMILIES: tuple[str, ...] = ("rw", "garch", "ou")


# ── Leg loading ───────────────────────────────────────────────────────────────

def load_leg(path: str) -> pd.DataFrame:
    """Load a TradingView-export leg CSV (`time,open,high,low,close`) → DataFrame indexed by UTC
    timestamp, ascending, deduped. Open/Close are the only trusted observables for spread construction
    (OHLC-1/2); High/Low are carried for the degenerate-bar (O=H=L=C) hygiene check only, never differenced."""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    if "time" not in df.columns:
        raise ValueError(f"{path}: no 'time' column (cols={list(df.columns)})")
    ts = pd.to_datetime(df["time"].astype(str), errors="coerce", utc=True, format="mixed")
    df = df.assign(ts=ts).dropna(subset=["ts"]).sort_values("ts")
    df = df.drop_duplicates(subset=["ts"], keep="last").set_index("ts")
    for col in ("open", "high", "low", "close"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df[[c for c in ("open", "high", "low", "close") if c in df.columns]]


def _is_flat_bar(df: pd.DataFrame) -> np.ndarray:
    """O=H=L=C degenerate/proxy bar (no genuine intrabar range) — manifest hygiene flag."""
    if not {"open", "high", "low", "close"}.issubset(df.columns):
        return np.zeros(len(df), dtype=bool)
    o, h, l, c = (df[k].to_numpy() for k in ("open", "high", "low", "close"))
    return (o == h) & (h == l) & (l == c)


# ── Roll-jump detection (ADR_003 R-1; causal, frozen threshold) ────────────────

def roll_transition_mask(close: np.ndarray, window: int = ROLL_MAD_WINDOW,
                         k: float = ROLL_MAD_K) -> np.ndarray:
    """Flag raw-stitched continuous-futures roll seams: bar t is a roll transition iff the leg's 1-bar
    log-return |r_t| exceeds k × (trailing `window`-bar MAD of r), using only data ≤ t (causal). The
    multiplier k is FROZEN (not fitted to the realized path — ADR_003 R-6). Returns bool length n
    (mask[t]=True ⇒ the increment landing on bar t is a roll artifact, to be excluded from VR)."""
    close = np.asarray(close, dtype=float)
    n = len(close)
    mask = np.zeros(n, dtype=bool)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.diff(np.log(close))          # length n-1; r[i] is the return into bar i+1
    for i in range(len(r)):
        lo = max(0, i - window)
        ref = r[lo:i]                        # strictly trailing (≤ t-1 returns), causal
        ref = ref[np.isfinite(ref)]
        if ref.size < 10:
            continue
        med = np.median(ref)
        mad = np.median(np.abs(ref - med))
        if mad <= 0 or not np.isfinite(r[i]):
            continue
        if abs(r[i] - med) > k * 1.4826 * mad:
            mask[i + 1] = True               # the seam lands on bar i+1
    return mask


# ── Causal rolling hedge ratio (C-1..C-3; vectorized, lagged) ──────────────────

def causal_rolling_beta(a: np.ndarray, b: np.ndarray, window: int = ROLL_BETA_W) -> np.ndarray:
    """β_t = Cov(A,B) / Var(B) over the trailing window ending at t-1, applied at t (C-3). OLS of A on B.
    Warm-up bars (window not full at t-1) are NaN (C-2 — masked, never imputed). Vectorized via rolling
    moments; the single .shift(1) IS the causal firewall (future bars cannot move an earlier β)."""
    sa, sb = pd.Series(a, dtype=float), pd.Series(b, dtype=float)
    mA = sa.rolling(window, min_periods=window).mean()
    mB = sb.rolling(window, min_periods=window).mean()
    mAB = (sa * sb).rolling(window, min_periods=window).mean()
    mBB = (sb * sb).rolling(window, min_periods=window).mean()
    cov = mAB - mA * mB
    var = mBB - mB * mB
    beta_hat = cov / var.where(var > 0)      # β̂_t uses data ≤ t
    return beta_hat.shift(1).to_numpy()      # apply at t using ≤ t-1  → C-3


# ── Spread construction (inner-join, level space, Open/Close only) ─────────────

@dataclass
class Spread:
    name: str
    s_close: np.ndarray                      # canonical observable (OHLC-2), level units
    s_open: np.ndarray                       # cross-check (OHLC-1)
    beta: np.ndarray
    roll_transition: np.ndarray              # bool; increment landing here is invalid
    flat_bar: np.ndarray                     # bool; degenerate leg bar (hygiene)
    index: pd.DatetimeIndex
    meta: dict = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.s_close)


def construct_spread(name: str, leg_a: pd.DataFrame, leg_b: pd.DataFrame, *,
                     beta_mode: str, window: int = ROLL_BETA_W,
                     continuous_a: bool = False, continuous_b: bool = False,
                     date_min: str | None = None, drop_flat_a: bool = False,
                     drop_flat_b: bool = False) -> Spread:
    """Construct S = A − β·B per doc 13/ADR_003: inner-join on UTC timestamps (AL-1, never positional),
    causal lagged β (β=1 or rolling, C-3), level differences (NP-1), Open/Close only (OHLC-1/2). Roll
    transitions on continuous-futures legs are flagged (union of both legs). `date_min` trims (WTI post-2011);
    `drop_flat_*` removes O=H=L=C proxy bars from a composite leg before alignment (Pt–Pd)."""
    if beta_mode not in ("one", "rolling"):
        raise ValueError("beta_mode ∈ {'one','rolling'}")
    a, b = leg_a.copy(), leg_b.copy()
    if drop_flat_a:
        a = a[~_is_flat_bar(a)]
    if drop_flat_b:
        b = b[~_is_flat_bar(b)]
    if date_min is not None:
        cut = pd.Timestamp(date_min, tz="UTC")
        a, b = a[a.index >= cut], b[b.index >= cut]

    # per-leg roll masks computed on each leg's OWN clock BEFORE the join (seam is a leg property)
    a = a.assign(_roll=roll_transition_mask(a["close"].to_numpy()) if continuous_a else False,
                 _flat=_is_flat_bar(a))
    b = b.assign(_roll=roll_transition_mask(b["close"].to_numpy()) if continuous_b else False,
                 _flat=_is_flat_bar(b))

    j = a.join(b, how="inner", lsuffix="_a", rsuffix="_b")   # AL-1 inner-join on synchronized timestamps
    if len(j) < window + max(VR_Q_GRID) + 5:
        raise ValueError(f"{name}: only {len(j)} joined bars — below power floor")

    ca, cb = j["close_a"].to_numpy(), j["close_b"].to_numpy()
    oa, ob = j["open_a"].to_numpy(), j["open_b"].to_numpy()
    if beta_mode == "one":
        beta = np.ones(len(j))
    else:
        beta = causal_rolling_beta(ca, cb, window=window)

    s_close = ca - beta * cb
    s_open = oa - beta * ob
    roll_transition = (j["_roll_a"].to_numpy().astype(bool) | j["_roll_b"].to_numpy().astype(bool))
    flat_bar = (j["_flat_a"].to_numpy().astype(bool) | j["_flat_b"].to_numpy().astype(bool))

    return Spread(
        name=name, s_close=s_close, s_open=s_open, beta=beta,
        roll_transition=roll_transition, flat_bar=flat_bar, index=j.index,
        meta={"beta_mode": beta_mode, "window": window, "n_joined": int(len(j)),
              "n_roll_masked": int(roll_transition.sum()), "n_flat": int(flat_bar.sum()),
              "date_start": str(j.index[0].date()), "date_end": str(j.index[-1].date())},
    )


# ── Level-difference VR(q) (negative-safe; mask-aware) ─────────────────────────

def _valid_increment_mask(s: np.ndarray, invalid_bar: np.ndarray) -> np.ndarray:
    """Increment k (= s[k+1]-s[k]) is valid iff both endpoints finite AND bar k+1 is not invalidated
    (roll transition / NaN β warm-up). Length n-1."""
    incr = np.diff(s)
    valid = np.isfinite(incr)
    valid &= ~np.asarray(invalid_bar, dtype=bool)[1:]
    return valid


def level_vr(s: np.ndarray, invalid_bar: np.ndarray,
             qs: tuple[int, ...] = VR_Q_GRID) -> dict[int, dict]:
    """VR(q) = Var(S_t − S_{t−q}) / (q · Var(ΔS)) on LEVELS (NP-1, sign-safe). Overlapping q-differences
    are used only over spans with NO invalid (roll/warm-up) increment. Returns per q: {vr, z_star, n1, nq}.
    z_star = Lo–MacKinlay heteroskedasticity-robust statistic on the valid 1-increment series (context
    only — the VERDICT rests on the surrogate ensemble, not z_star; doc 18a F3)."""
    s = np.asarray(s, dtype=float)
    incr = np.diff(s)
    valid1 = _valid_increment_mask(s, invalid_bar)
    out: dict[int, dict] = {}
    if valid1.sum() < 30:
        return {q: {"vr": np.nan, "z_star": np.nan, "n1": int(valid1.sum()), "nq": 0} for q in qs}
    v1 = float(np.var(incr[valid1], ddof=1))
    # cumulative count of INVALID increments → fast "is this q-span clean?" test
    invalid_cum = np.concatenate([[0], np.cumsum(~valid1)])    # length n
    for q in qs:
        if len(s) <= q or v1 <= 0:
            out[q] = {"vr": np.nan, "z_star": np.nan, "n1": int(valid1.sum()), "nq": 0}
            continue
        qdiff = s[q:] - s[:-q]                                 # length n-q; span k uses incr[k..k+q-1]
        clean = (invalid_cum[q:] - invalid_cum[:len(s) - q]) == 0   # no invalid increment in the span
        clean &= np.isfinite(qdiff)
        if clean.sum() < 10:
            out[q] = {"vr": np.nan, "z_star": np.nan, "n1": int(valid1.sum()), "nq": int(clean.sum())}
            continue
        vq = float(np.var(qdiff[clean], ddof=1))
        vr = vq / (q * v1)
        out[q] = {"vr": vr, "z_star": _lm_zstar(incr[valid1], q, vr), "n1": int(valid1.sum()),
                  "nq": int(clean.sum())}
    return out


def _lm_zstar(r: np.ndarray, q: int, vr: float) -> float:
    """Lo–MacKinlay (1988) heteroskedasticity-robust z* on increment series r (treated contiguous —
    documented approximation, context only). z* = (VR(q)-1)/sqrt(θ*), θ* = Σ_{j=1}^{q-1}[2(q-j)/q]^2 δ_j."""
    r = np.asarray(r, dtype=float)
    n = len(r)
    if n < q + 2 or not np.isfinite(vr):
        return float("nan")
    mu = r.mean()
    d = r - mu
    denom = float((d ** 2).sum())
    if denom <= 0:
        return float("nan")
    theta = 0.0
    for j in range(1, q):
        delta_j = float((d[j:] ** 2 * d[:-j] ** 2).sum()) / (denom ** 2)   # δ_j ~ O(1/T)
        theta += (2.0 * (q - j) / q) ** 2 * delta_j
    if theta <= 0:
        return float("nan")
    return (vr - 1.0) / np.sqrt(theta)


# ── Surrogate fits + generators (causal; level series; same mask) ──────────────

def _fit_rw(incr: np.ndarray) -> dict:
    return {"sigma": float(np.std(incr, ddof=1))}


def _sim_rw(params: dict, n: int, rng: np.random.Generator) -> np.ndarray:
    return np.concatenate([[0.0], np.cumsum(rng.normal(0.0, params["sigma"], n - 1))])


def _fit_ou(s_levels_clean: np.ndarray) -> dict:
    """AR(1) on the LEVEL: S_t = c + φ S_{t-1} + e. Generic reverting null, parameters fit on a CAUSAL
    PRE-SAMPLE (first third) — NOT the full sample (doc 18 §5: "estimated causally (trailing/pre-sample),
    never full-sample-tuned to mimic the real"). A full-sample AR(1) MLE would reproduce the real's own
    autocorrelation and be unbeatable by construction; the pre-sample fit is a genuine, beatable null."""
    pre = s_levels_clean[: max(ROLL_BETA_W, len(s_levels_clean) // 3)]
    x0, x1 = pre[:-1], pre[1:]
    X = np.column_stack([np.ones_like(x0), x0])
    coef, *_ = np.linalg.lstsq(X, x1, rcond=None)
    c, phi = float(coef[0]), float(coef[1])
    resid = x1 - (c + phi * x0)
    phi = max(-0.999, min(0.999, phi))
    return {"c": c, "phi": phi, "sigma_e": float(np.std(resid, ddof=1)), "x0": float(pre[0])}


def _sim_ou(params: dict, n: int, rng: np.random.Generator) -> np.ndarray:
    c, phi, sig = params["c"], params["phi"], params["sigma_e"]
    s = np.empty(n)
    s[0] = params["x0"]
    e = rng.normal(0.0, sig, n)
    for t in range(1, n):
        s[t] = c + phi * s[t - 1] + e[t]
    return s


def _fit_garch(incr: np.ndarray) -> dict:
    """Zero-mean GARCH(1,1) QMLE on increments (arch 8.0.0). Simulated as a MARTINGALE level (no
    reversion injected) → isolates whether sub-diffusion is a volatility-clustering artifact."""
    from arch import arch_model
    scale = float(np.std(incr, ddof=1)) or 1.0
    y = incr / scale
    try:
        res = arch_model(y, mean="Zero", vol="GARCH", p=1, q=1, dist="normal", rescale=False
                         ).fit(disp="off", show_warning=False)
        w = float(res.params.get("omega", np.nan))
        al = float(res.params.get("alpha[1]", np.nan))
        be = float(res.params.get("beta[1]", np.nan))
        # Allow IGARCH (α+β=1, persistent variance — common on daily data, a VALID vol-clustering null);
        # reject only explosive / non-finite / negative fits. (Prior `α+β≥0.999` guard wrongly collapsed
        # IGARCH fits to a pure-RW fallback, so the GARCH family silently duplicated the RW null — audit
        # Team D D1. Variance-targeted simulation (_sim_garch) handles the α+β→1 boundary.)
        if not all(np.isfinite([w, al, be])) or w <= 0 or al < 0 or be < 0 or al + be > 1.0 + 1e-6:
            raise ValueError("explosive/degenerate GARCH fit")
    except Exception:                                  # fall back to RW-equivalent (honest, not silent)
        return {"omega": 1.0, "alpha": 0.0, "beta": 0.0, "scale": scale, "degenerate": True}
    return {"omega": w, "alpha": al, "beta": be, "scale": scale, "degenerate": False}


def _sim_garch(params: dict, n: int, rng: np.random.Generator) -> np.ndarray:
    w, al, be, scale = params["omega"], params["alpha"], params["beta"], params["scale"]
    eps = np.empty(n - 1)
    s2 = np.empty(n - 1)
    persist = al + be
    # variance-targeting init: increments were scaled to unit variance before fitting, so the target
    # unconditional variance is 1.0; use it directly when α+β→1 (IGARCH) where ω/(1−α−β) diverges.
    s2[0] = (w / (1.0 - persist)) if persist < 0.995 else 1.0
    eps[0] = rng.normal(0.0, np.sqrt(s2[0]))
    for t in range(1, n - 1):
        s2[t] = w + al * eps[t - 1] ** 2 + be * s2[t - 1]
        eps[t] = rng.normal(0.0, np.sqrt(s2[t]))
    return np.concatenate([[0.0], np.cumsum(eps * scale)])


_FIT = {"rw": _fit_rw, "garch": _fit_garch}
_SIM = {"rw": _sim_rw, "garch": _sim_garch, "ou": _sim_ou}


def surrogate_vr_ensemble(spread: Spread, family: str, *, qs: tuple[int, ...] = VR_Q_GRID,
                          n_draws: int = N_SURROGATE, seed: int = 0) -> dict[int, np.ndarray]:
    """N matched-surrogate VR(q) draws. Surrogate level series share the real spread's LENGTH and the
    SAME invalid-bar mask, and pass through the IDENTICAL VR extraction — so each carries the same
    finite-sample / overlapping bias as the real (red-team: real−surrogate nets the bias out)."""
    s = spread.s_close
    invalid = spread.roll_transition | ~np.isfinite(spread.beta)
    valid1 = _valid_increment_mask(s, invalid)
    incr_clean = np.diff(s)[valid1]
    n = len(s)
    if family == "ou":
        params = _fit_ou(s[np.isfinite(s)])
    else:
        params = _FIT[family](incr_clean)
    sim = _SIM[family]
    rng = np.random.default_rng(seed)
    ens = {q: np.full(n_draws, np.nan) for q in qs}
    for d in range(n_draws):
        surr = sim(params, n, rng)
        vr_d = level_vr(surr, invalid, qs)            # SAME mask, SAME estimator
        for q in qs:
            ens[q][d] = vr_d[q]["vr"]
    return ens


# ── Per-spread verdict (doc 18 §5) ─────────────────────────────────────────────

# Verdict policy (doc 18a F2 — the one genuinely ambiguous clause, ruled before real data):
#   "martingale" → CONFIRMED iff real VR < 5th pct of the RW *and* GARCH martingale nulls at a shared
#                  horizon. (OU reported as a stringency reference; an OU surrogate fit to the series is
#                  near-unbeatable by a genuine OU, so it cannot be the verdict gate without making the
#                  test vacuous — no achievable positive control.)
#   "all_three"  → literal doc-18-§5 conjunction across RW, GARCH, AND OU.
# Both are always computed and reported; this only selects the headline `confirmed`.
VERDICT_POLICY: str = "martingale"
MARTINGALE_FAMILIES: tuple[str, ...] = ("rw", "garch")


@dataclass
class SpreadVerdict:
    name: str
    real_vr: dict[int, float]
    real_z: dict[int, float]
    per_family: dict[str, dict[int, dict]]            # family → q → {p5, real_below_p5, surr_median}
    confirmed: bool                                   # headline, per VERDICT_POLICY
    confirmed_martingale: bool
    confirmed_all_three: bool
    separated_horizons: dict[str, list[int]]
    meta: dict


def evaluate_spread(spread: Spread, *, seed: int = 0, qs: tuple[int, ...] = VR_Q_GRID,
                    policy: str = VERDICT_POLICY) -> SpreadVerdict:
    """Full doc-18 §5 read for one spread: real VR(q), three matched-surrogate ensembles (RW/GARCH/OU),
    5th-pct gate per family. Reports BOTH the martingale-null verdict (RW & GARCH shared horizon) and the
    literal all-three conjunction; `confirmed` follows `policy`. Surrogate-relative only — raw VR never
    used as evidence."""
    invalid = spread.roll_transition | ~np.isfinite(spread.beta)
    real = level_vr(spread.s_close, invalid, qs)
    real_vr = {q: real[q]["vr"] for q in qs}
    real_z = {q: real[q]["z_star"] for q in qs}

    real_min = float(np.nanmin([real_vr[q] for q in qs])) if any(np.isfinite(real_vr[q]) for q in qs) else np.nan
    per_family: dict[str, dict] = {}
    sep_naive: dict[str, list[int]] = {}       # per-horizon ≥1-of-grid (uncorrected; FPR-inflated)
    sep_corr: dict[str, bool] = {}             # multiplicity-corrected min-VR statistic (calibrated 5%)
    for fam in SURR_FAMILIES:
        ens = surrogate_vr_ensemble(spread, fam, qs=qs, n_draws=N_SURROGATE, seed=seed)
        mat = np.column_stack([ens[q] for q in qs])             # N × |q|
        per_horizon: dict[int, dict] = {}
        sep_naive[fam] = []
        for j, q in enumerate(qs):
            col = mat[:, j][np.isfinite(mat[:, j])]
            p5 = float(np.percentile(col, SURR_PCTILE)) if col.size >= 20 else np.nan
            below = bool(np.isfinite(real_vr[q]) and np.isfinite(p5) and real_vr[q] < p5 and real_vr[q] < 1.0)
            per_horizon[q] = {"p5": p5, "real_below_p5": below,
                              "surr_median": float(np.median(col)) if col.size else np.nan}
            if below:
                sep_naive[fam].append(q)
        # multiplicity-corrected: compare real's best-horizon VR to the surrogate's OWN best-horizon null
        surr_min = np.nanmin(mat, axis=1)
        surr_min = surr_min[np.isfinite(surr_min)]
        if surr_min.size >= 20 and np.isfinite(real_min):
            p_val = (1.0 + float(np.sum(surr_min <= real_min))) / (surr_min.size + 1.0)
        else:
            p_val = np.nan
        sep_corr[fam] = bool(np.isfinite(p_val) and p_val < SURR_PCTILE / 100.0 and real_min < 1.0)
        per_family[fam] = {"per_horizon": per_horizon, "min_vr_p_value": p_val,
                           "separated_corrected": sep_corr[fam],
                           "surr_min_p5": float(np.percentile(surr_min, SURR_PCTILE)) if surr_min.size else np.nan}

    # Headline = multiplicity-corrected separation; martingale = RW & GARCH, all_three adds OU.
    confirmed_martingale = all(sep_corr[f] for f in MARTINGALE_FAMILIES)
    confirmed_all_three = all(sep_corr[f] for f in SURR_FAMILIES)
    shared_mart_naive = [q for q in qs if all(q in sep_naive[f] for f in MARTINGALE_FAMILIES)]
    shared_all_naive = [q for q in qs if all(q in sep_naive[f] for f in SURR_FAMILIES)]
    confirmed = confirmed_all_three if policy == "all_three" else confirmed_martingale
    return SpreadVerdict(
        name=spread.name, real_vr=real_vr, real_z=real_z, per_family=per_family,
        confirmed=confirmed, confirmed_martingale=confirmed_martingale,
        confirmed_all_three=confirmed_all_three,
        separated_horizons={**sep_naive, "MARTINGALE_naive": shared_mart_naive,
                            "ALL_FAMILIES_naive": shared_all_naive,
                            "corrected": {f: sep_corr[f] for f in SURR_FAMILIES}},
        meta={**spread.meta, "seed": seed, "policy": policy, "real_min_vr": real_min},
    )
