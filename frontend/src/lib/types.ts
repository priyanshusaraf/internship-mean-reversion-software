export interface OHLCVBar {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface InstrumentMeta {
  instrument_id: string;
  display_name: string;
  row_count: number;
  start_date: string;
  end_date: string;
  file_path: string;
}

export interface LoadRequest {
  file_path: string;
  instrument_id: string;
  display_name?: string;
}

export interface SpreadRequest {
  instrument_a: string;
  instrument_b: string;
  beta: number;
  spread_id?: string;
}

export interface LoadResponse {
  instrument_id: string;
  row_count: number;
  start_date: string;
  end_date: string;
  columns: string[];
}

export interface OHLCVResponse {
  instrument_id: string;
  bars: OHLCVBar[];
}

export interface EstimatorBar {
  time: string;
  value: number;
}

export interface EstimatorResponse {
  instrument_id: string;
  estimator: string;
  window: number;
  bars: EstimatorBar[];
}

export interface ResearchRow {
  date: string;
  close: number;
  mu_star: number;
  epsilon: number;
}

export interface ResearchStats {
  epsilon_mean: number;
  epsilon_std: number;
  n: number;
}

export interface ResearchResponse {
  instrument_id: string;
  estimator: string;
  window: number;
  rows: ResearchRow[];
  stats: ResearchStats;
}

export interface DiagnosticsRow {
  date: string;
  close: number;
  mu_star: number;
  mu_star_adj: number;     // adjusted EMA (adjust=True) — differs from causal only during warmup
  mu_star_diff: number;    // initialization gap (mu_star_adj - mu_star), near-zero for long series
  epsilon: number;
  epsilon_adj: number;     // residual vs adjusted EMA
  epsilon_rolling_mean: number;
  epsilon_rolling_std: number;
  epsilon_zscore: number | null;
  innovation: number | null;
  // Kalman μ* — research comparison estimator (frozen 2-state filter; see docs/research/06)
  mu_star_kalman: number;   // posterior equilibrium μ_{t|t} (overlay)
  epsilon_kalman: number;   // innovation residual P_t − μ_{t|t−1} (research residual)
  kalman_velocity: number;  // v_{t|t} equilibrium drift estimate
  kalman_gain: number;      // K_t level gain
  kalman_state_var: number; // P_{t|t} equilibrium posterior variance
}

export interface DiagnosticsStats {
  epsilon_mean: number;
  epsilon_std: number;
  epsilon_skew: number;
  epsilon_kurt: number;
  acf_lag1: number;
  acf_lag5: number;
  acf_lag10: number;
  acf_lag20: number;
  halflife_bars: number | null;
  mu_star_diff_mean: number;
  mu_star_diff_max: number;
  n: number;
}

export interface DiagnosticsResponse {
  instrument_id: string;
  estimator: string;
  window: number;
  rows: DiagnosticsRow[];
  stats: DiagnosticsStats;
}

// ── Step 2A: velocity-absorption (false-centering falsification) ──
export interface ReversionStat {
  horizon: number;
  beta: number | null;   // train-half OLS slope; β<0 ⇒ deviations predict snapback
  r2: number | null;     // out-of-sample R² on held-out future half (may be < 0)
  n: number;             // held-out test pairs
}

export interface VelocityAbsorptionRow {
  date: string;
  price: number;
  delta: number | null;  // velocity contribution δ (None at t=0)
}

export interface VelocityAbsorptionResponse {
  instrument_id: string;
  matched_span: number;
  steady_state_gain: number;
  burn: number;
  n: number;
  horizons: number[];
  reversion_kalman: ReversionStat[];    // velocity-ON
  reversion_restored: ReversionStat[];  // velocity-OFF ≡ matched-EMA pred
  rows: VelocityAbsorptionRow[];
}

// ── MRScore (observatory diagnostic; doc 01 §3, eq. 13–34) ──────────────────
export interface MRScoreRow {
  date: string;
  close: number;
  mu_star: number;              // causal EMA μ* reference
  mrscore: number | null;       // 0.20·B1 + 0.60·B2 + 0.20·B3, ∈ [0,100]
  b1: number | null;            // Mean Reliability
  b2: number | null;            // Mean Reversion Strength (60%)
  b3: number | null;            // Tradability
  r_adf: number | null;
  r_kpss: number | null;
  r_msi: number | null;
  r_vsi: number | null;
  r_drc: number | null;
  r_hit_rate: number | null;
  r_vr: number | null;
  r_hl: number | null;
  r_vc: number | null;
  r_tcf: number | null;
  // Raw artifact-resistant Block-2 features (the genuine cross-instrument discriminators)
  drc: number | null;
  hit_rate: number | null;
  vr_agg: number | null;
}

export interface MRScoreStats {
  n: number;
  n_scored: number;
  mrscore_last: number | null;
  b1_last: number | null;
  b2_last: number | null;
  b3_last: number | null;
}

export interface MRScoreResponse {
  instrument_id: string;
  window: number;
  weights: { b1: number; b2: number; b3: number };
  mode: string;                 // "causal"
  regime_warning: string;
  data_warning: string | null;  // structural incompatibility (e.g. non-positive/spread prices)
  rows: MRScoreRow[];
  stats: MRScoreStats;
}

// ── Substrate Observatory (character, not timing; docs/research/10) ──────────
export interface SubstrateRow {
  date: string;
  close: number;
  de: number | null;            // directional efficiency ∈ [0,1] (1 = straight/trend, ~0 = chop)
  vr: number | null;            // representative variance ratio (<1 MR · ≈1 RW · >1 momentum)
  rv: number | null;            // annualized realized vol (reference)
  vp: number | null;            // realized-vol percentile ∈ [0,100] (context only)
  ou_like: number | null;       // resemblance scores ∈ [0,1] (independent, not a partition)
  trend_like: number | null;
  rw_null: number | null;
  ambiguous: number | null;
  dominant: string | null;      // argmax bucket
  confidence: string | null;    // clear · weak · ambiguous
}

export interface SubstrateStats {
  n: number;
  n_scored: number;
  dominant_last: string | null;
  confidence_last: string | null;
  ou_like_last: number | null;
  trend_like_last: number | null;
  rw_null_last: number | null;
  ambiguous_last: number | null;
}

export interface SubstrateResponse {
  instrument_id: string;
  window: number;
  mode: string;                 // "causal"
  buckets: string[];
  regime_warning: string;
  data_warning: string | null;  // structural incompatibility (non-positive/spread → VR undefined)
  rows: SubstrateRow[];
  stats: SubstrateStats;
}

// ── Backtest (P&L Cockpit) — MIRRORS backend/app/services/backtest_engine.py 1:1 ─────
// Source of truth is the pydantic models there. Do NOT invent or rename fields. The engine
// is a FROZEN PLACEHOLDER (MR_PLACEHOLDER_V1, slippage=0) — execution/measurement only.
export interface BacktestConfig {
  instrument_id: string;
  start: string;                  // ISO date
  end: string;                    // ISO date — hard firewall upper bound
  strategy_id?: string;           // default "MR_PLACEHOLDER_V1" (server-side)
  round_trip_cost?: number;       // default 0.003 (server-side)
  mode?: string;                  // "research" | "verification" — defaults research, never surfaced
  prereg_params?: Record<string, unknown>;
}

export interface BacktestTrade {
  trade_id: number;
  direction: string;              // "LONG" | "SHORT"
  entry_bar: string;              // ISO date of signal bar
  entry_price: number;
  exit_bar: string;               // ISO date of signal bar
  exit_price: number;
  exit_reason: string;            // "Z_CROSS" | "TIME_STOP"
  gross_pnl: number;
  cost: number;
  net_pnl: number;
  bars_held: number;
  entry_z: number;
  exit_z: number;
}

export interface EquityPoint {
  date: string;
  cumulative_pnl: number;
}

export interface BacktestResult {
  instrument_id: string;
  strategy_id: string;
  start: string;
  end: string;
  n_bars: number;
  n_trades: number;
  win_rate: number;               // fraction ∈ [0,1]
  avg_net_pnl: number;
  total_net_pnl: number;
  sharpe_ratio: number;
  max_drawdown: number;           // ≤ 0 (loss magnitude)
  profit_factor: number;
  avg_bars_held: number;
  pct_time_stop: number;
  trades: BacktestTrade[];
  equity_curve: EquityPoint[];    // one per bar
  slippage_note: string;          // "slippage=0, placeholder rule, not deployable"
  strategy_params: Record<string, unknown>;
  verification_watermark: boolean;
}
