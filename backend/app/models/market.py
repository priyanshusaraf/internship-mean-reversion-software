from pydantic import BaseModel


class OHLCVBar(BaseModel):
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: float


class InstrumentMeta(BaseModel):
    instrument_id: str
    display_name: str
    row_count: int
    start_date: str
    end_date: str
    file_path: str


class LoadRequest(BaseModel):
    file_path: str
    instrument_id: str
    display_name: str | None = None


class SpreadRequest(BaseModel):
    instrument_a: str
    instrument_b: str
    beta: float
    spread_id: str | None = None  # auto-generated if omitted


class LoadResponse(BaseModel):
    instrument_id: str
    row_count: int
    start_date: str
    end_date: str
    columns: list[str]


class OHLCVResponse(BaseModel):
    instrument_id: str
    bars: list[OHLCVBar]


class EstimatorBar(BaseModel):
    time: str
    value: float


class EstimatorResponse(BaseModel):
    instrument_id: str
    estimator: str
    window: int
    bars: list[EstimatorBar]


class ResearchRow(BaseModel):
    date: str
    close: float
    mu_star: float
    epsilon: float


class ResearchStats(BaseModel):
    epsilon_mean: float
    epsilon_std: float
    n: int


class ResearchResponse(BaseModel):
    instrument_id: str
    estimator: str
    window: int
    rows: list[ResearchRow]
    stats: ResearchStats


# ── Diagnostics (workbench) ───────────────────────────────────────────────────

class DiagnosticsRow(BaseModel):
    date: str
    close: float

    # Estimator — causal EMA and adjusted EMA, both firewalled to data <= end
    mu_star: float           # causal EMA (adjust=False): ewm recurrence, bar-by-bar
    mu_star_adj: float       # adjusted EMA (adjust=True): differs only in warmup weighting
    mu_star_diff: float      # mu_star_adj - mu_star (EMA initialization gap)

    # Residuals
    epsilon: float           # close - mu_star (causal residual)
    epsilon_adj: float       # close - mu_star_adj (adjusted residual)

    # Rolling statistics on causal epsilon
    epsilon_rolling_mean: float
    epsilon_rolling_std: float
    epsilon_zscore: float | None

    # Innovation: close[t] - mu_star[t-1] (causal one-step prediction error)
    innovation: float | None

    # ── Kalman μ* — research comparison estimator (frozen 2-state filter; see
    #    analytics.compute_kalman_mu_star and docs/research/06). Causal by construction.
    #    Not the production μ*; exposed alongside EMA to falsify the centering advantage. ──
    mu_star_kalman: float        # posterior equilibrium μ_{t|t} (for charting/overlay)
    epsilon_kalman: float        # innovation residual P_t − μ_{t|t−1} (the research residual)
    kalman_velocity: float       # v_{t|t} — equilibrium drift estimate
    kalman_gain: float           # K_t[0] — gain on the level component
    kalman_state_var: float      # P_{t|t}[0,0] — equilibrium posterior variance (uncertainty)


class DiagnosticsStats(BaseModel):
    # Residual distribution
    epsilon_mean: float
    epsilon_std: float
    epsilon_skew: float
    epsilon_kurt: float

    # Autocorrelation of causal epsilon at standard lags
    acf_lag1: float
    acf_lag5: float
    acf_lag10: float
    acf_lag20: float

    # OU half-life estimate via OLS with intercept (None if not mean-reverting)
    halflife_bars: float | None

    # EMA initialization gap statistics (causal vs adjusted warmup difference)
    mu_star_diff_mean: float
    mu_star_diff_max: float

    n: int


class DiagnosticsResponse(BaseModel):
    instrument_id: str
    estimator: str
    window: int
    rows: list[DiagnosticsRow]
    stats: DiagnosticsStats


# ── Step 2A: velocity-absorption instrumentation (false-centering falsification) ──────
class ReversionStat(BaseModel):
    """Walk-forward predictive-decay result for one residual system at one horizon."""
    horizon: int
    beta: float | None     # train-half OLS slope; β<0 ⇒ deviations predict snapback
    r2: float | None       # out-of-sample R² on the held-out future half (may be < 0)
    n: int                 # held-out test pairs


class VelocityAbsorptionRow(BaseModel):
    date: str
    price: float
    delta: float | None    # velocity contribution δ = μ_K(pred) − EMA_match(pred); None at t=0


class VelocityAbsorptionResponse(BaseModel):
    instrument_id: str
    matched_span: int                # EMA span matched to frozen Kalman responsiveness
    steady_state_gain: float
    burn: int                        # warmup bars dropped before the decay test
    n: int
    horizons: list[int]
    # Predictive-decay (walk-forward) per residual system, keyed by system name.
    reversion_kalman: list[ReversionStat]    # velocity-ON  (ε^K)
    reversion_restored: list[ReversionStat]  # velocity-OFF (ε^R ≡ matched-EMA pred)
    rows: list[VelocityAbsorptionRow]        # δ vs price (Surface 2)


# ── MRScore (observatory diagnostic) ──────────────────────────────────────────
# A faithful per-bar implementation of the frozen spec (doc 01 §3, eq. 13–34). OBSERVATORY ONLY —
# observe/falsify, NOT a signal; structurally terminal. All score fields are nullable: MRScore is
# undefined during warmup (needs the estimation + rank windows) and where a feature is excluded.

class MRScoreRow(BaseModel):
    date: str
    close: float
    mu_star: float                   # production causal EMA μ* (the reference; descriptive use)
    mrscore: float | None            # 0.20·B1 + 0.60·B2 + 0.20·B3, ∈ [0,100]
    b1: float | None                 # Mean Reliability
    b2: float | None                 # Mean Reversion Strength (60%)
    b3: float | None                 # Tradability
    # Feature ranks (the contribution decomposition; each ∈ [0,100], directionally adjusted)
    r_adf: float | None
    r_kpss: float | None
    r_msi: float | None
    r_vsi: float | None
    r_drc: float | None
    r_hit_rate: float | None
    r_vr: float | None
    r_hl: float | None
    r_vc: float | None
    r_tcf: float | None
    # Raw Block-2 features — the artifact-resistant CROSS-instrument discriminators. The self-ranked
    # score is within-instrument relative (see the normalization finding); these raw values are what
    # actually separate reverters from nulls, so they are surfaced explicitly.
    drc: float | None                # min_h Newey-West t (strongly negative = strong reversion)
    hit_rate: float | None
    vr_agg: float | None


class MRScoreStats(BaseModel):
    n: int
    n_scored: int                    # bars with a defined MRScore (post-warmup)
    mrscore_last: float | None
    b1_last: float | None
    b2_last: float | None
    b3_last: float | None


class MRScoreResponse(BaseModel):
    instrument_id: str
    window: int                      # EMA span used for μ*
    weights: dict[str, float]        # frozen block weights {b1,b2,b3}
    mode: str                        # "causal" (full-information deferred — no genuine future-μ* yet)
    regime_warning: str              # epistemic gate (ADANIENT trend-regime / not-a-signal caveat)
    data_warning: str | None = None  # set when the instrument is structurally incompatible (e.g.
                                     # non-positive/spread prices → log-based features undefined → no score)
    rows: list[MRScoreRow]
    stats: MRScoreStats


# ── Substrate Observatory (observatory diagnostic; docs/research/10) ───────────
# "What kind of market are we looking at?" — instrument CHARACTER over a trailing window, as
# resemblance to 4 coarse archetypes. OBSERVATORY ONLY — observe/falsify, NOT a signal; structurally
# terminal. CHARACTER, NOT TIMING (never "a regime is igniting" — that is State T detection, frozen).
# Score/descriptor fields are nullable: undefined during the trailing-window warmup.

class SubstrateRow(BaseModel):
    date: str
    close: float
    # Descriptors (causal, trailing window). vp/rv are CONTEXT only — not character drivers.
    de: float | None                 # directional efficiency ∈ [0,1] (1 = straight/trend, ~0 = chop)
    vr: float | None                 # representative variance ratio (<1 MR · ≈1 RW · >1 momentum)
    rv: float | None                 # annualized realized vol (reference)
    vp: float | None                 # realized-vol percentile ∈ [0,100] (context)
    # Resemblance scores ∈ [0,1] (independent, not a partition) + the read.
    ou_like: float | None
    trend_like: float | None
    rw_null: float | None
    ambiguous: float | None
    dominant: str | None             # argmax bucket name
    confidence: str | None           # clear · weak · ambiguous (top-two margin)


class SubstrateStats(BaseModel):
    n: int
    n_scored: int                    # bars with a defined character read (post warmup)
    dominant_last: str | None
    confidence_last: str | None
    ou_like_last: float | None
    trend_like_last: float | None
    rw_null_last: float | None
    ambiguous_last: float | None


class SubstrateResponse(BaseModel):
    instrument_id: str
    window: int                      # trailing estimation window for descriptors
    mode: str                        # "causal" (full-information deferred — one-line window swap)
    buckets: list[str]               # the frozen v1 archetype set
    regime_warning: str              # epistemic gate (observatory / character-not-timing caveat)
    data_warning: str | None = None  # structural incompatibility (non-positive/spread → VR undefined)
    rows: list[SubstrateRow]
    stats: SubstrateStats
