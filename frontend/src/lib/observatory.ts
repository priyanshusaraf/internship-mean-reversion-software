/**
 * Observatory v2 API client — typed against docs/build/api_contract.md (FROZEN).
 *
 * Thin client. NO statistic is computed here. Every number (μ*, z, VR, habitat score,
 * percentiles, frac_ge_real) comes from the v2 endpoints verbatim. The only array work
 * permitted on the frontend is BINNING null_min_vr[] into histogram bars for rendering
 * (display only) — never deriving a scalar (contract M5).
 *
 * Additive & isolated: this module does NOT touch src/lib/api.ts (the legacy /api/v1 client).
 */

const BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

// ── §1 Dataset ──────────────────────────────────────────────────────────────────────

export interface DateRange {
  start: string | null;
  end: string | null;
}

export interface ColumnMap {
  timestamp: string | null;
  close: string | null;
  open: string | null;
  high: string | null;
  low: string | null;
  volume: string | null;
}

export type BetaMode = 'none' | 'definitional' | 'frozen-ols' | 'rolling-INADMISSIBLE';

export interface Construction {
  beta_mode: BetaMode;
  roll_masked: boolean | null;
}

export type Frequency = 'daily' | 'intraday' | 'unknown';
export type DateFormat = 'auto' | 'unix' | 'iso' | 'dd-mm-yyyy';

export interface Dataset {
  dataset_id: string;
  name: string;
  source_file: string;
  frequency: Frequency;
  row_count: number;
  date_range: DateRange;
  columns: string[];
  column_map: ColumnMap;
  date_format: DateFormat;
  timezone: string | null;
  is_spread: boolean;
  construction: Construction;
  created_at: string;
}

// ── §3 QualityReport ──────────────────────────────────────────────────────────────────

export interface Gap {
  from: string;
  to: string;
  missing_bars: number;
}

export interface NonPositiveExample {
  time: string;
  close: number | null;
}

export interface ExcisionWindow {
  from: string;
  to: string;
}

export interface NonPositivePrices {
  count: number;
  examples: NonPositiveExample[];
  suggested_excision: ExcisionWindow | null;
}

export interface BackAdjustmentSeam {
  time: string;
  jump: number | null;
}

export interface QualityReport {
  row_count: number;
  date_range: DateRange;
  frequency: Frequency;
  median_delta_days: number | null;
  gaps: Gap[];
  n_gaps: number;
  duplicate_timestamps: number;
  non_positive_prices: NonPositivePrices;
  nan_rows_dropped: number;
  back_adjustment_seams: BackAdjustmentSeam[];
  warnings: string[];
}

// ── §6 Provenance ─────────────────────────────────────────────────────────────────────

export type Mode = 'research' | 'verification';

export interface Provenance {
  dataset_id: string;
  dataset_hash: string;
  as_of: string | null;
  params: Record<string, unknown>;
  mode: Mode;
  prereg_id: string | null;
  exploratory_watermark: boolean;
  engine: string;
  engine_version: string;
  computed_at: string;
}

// ── §2 ingestion & series ─────────────────────────────────────────────────────────────

export interface IngestResponse {
  dataset: Dataset;
  quality: QualityReport;
}

export interface DatasetList {
  datasets: Dataset[];
}

export interface Bar {
  time: string;
  open: number | null;
  high: number | null;
  low: number | null;
  close: number | null;
  volume: number | null;
}

export interface SeriesResponse {
  dataset_id: string;
  as_of: string | null;
  bars: Bar[];
  forward_bars: Bar[];
}

// ── §4.1 equilibrium ──────────────────────────────────────────────────────────────────

export interface EquilibriumParams {
  snr: number;
  kappa: number;
  warmup: number;
}

export interface EquilibriumRequest {
  dataset_id: string;
  as_of?: string | null;
  start?: string | null;
  end?: string | null;
  params?: EquilibriumParams | null;
  mode?: Mode;
  prereg_id?: string | null;
}

export interface EquilibriumRow {
  time: string;
  close: number | null;
  mu_star: number | null;
  velocity: number | null;
  innovation: number | null;
  z: number | null;
  gain: number | null;
  state_var: number | null;
}

export interface EquilibriumResponse {
  dataset_id: string;
  as_of: string | null;
  params: EquilibriumParams;
  series: EquilibriumRow[];
  z_sigma_basis: string;
  provenance: Provenance;
}

// ── §4.2 habitat ──────────────────────────────────────────────────────────────────────

export interface HabitatWindow {
  start: string;
  end: string;
}

export interface HabitatParams {
  vr_qs: number[];
  ns_null: number;
  seed: number;
}

export interface HabitatRequest {
  dataset_id: string;
  window: HabitatWindow;
  as_of?: string | null;
  deseason?: boolean;
  params?: HabitatParams | null;
  mode?: Mode;
  prereg_id?: string | null;
}

export interface VRPoint {
  q: number;
  vr: number | null;
}

export interface SurrogateDistribution {
  null_min_vr: number[];
  n: number;
  p10: number | null;
  p50: number | null;
  p90: number | null;
  frac_ge_real: number | null;
}

export interface CalibrationBadge {
  ou: number;
  rw: number;
  trend: number;
  status: string;
}

export interface RawVsDeseason {
  raw_score: number | null;
  deseason_score: number | null;
  verdict_changed: boolean | null;
}

export interface HabitatResponse {
  dataset_id: string;
  window: HabitatWindow;
  deseason: boolean;
  score: number | null;
  real_min_vr: number | null;
  vr_curve: VRPoint[];
  surrogate_distribution: SurrogateDistribution;
  calibration_badge: CalibrationBadge;
  raw_vs_deseason: RawVsDeseason | null;
  data_warning: string | null;
  provenance: Provenance;
}

// ── transport ─────────────────────────────────────────────────────────────────────────

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error((err as { detail?: string }).detail ?? 'Request failed');
  }
  return res.json() as Promise<T>;
}

export interface IngestMapping {
  name?: string | null;
  column_map?: Partial<ColumnMap>;
  date_format?: DateFormat;
  timezone?: string | null;
}

export const observatory = {
  // §2 — upload CSV + explicit column mapping
  createDataset: async (file: File, mapping: IngestMapping): Promise<IngestResponse> => {
    const form = new FormData();
    form.append('file', file);
    form.append('mapping', JSON.stringify(mapping));
    const res = await fetch(`${BASE}/api/v2/datasets`, { method: 'POST', body: form });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error((err as { detail?: string }).detail ?? 'Upload failed');
    }
    return res.json() as Promise<IngestResponse>;
  },

  listDatasets: () => request<DatasetList>('/api/v2/datasets'),

  getDataset: (id: string) => request<Dataset>(`/api/v2/datasets/${encodeURIComponent(id)}`),

  // §2 — parsed bars + forward (evaluation-only) overlay, causal to as_of
  getSeries: (id: string, opts?: { as_of?: string | null; start?: string | null; end?: string | null }) => {
    const p = new URLSearchParams();
    if (opts?.as_of) p.set('as_of', opts.as_of);
    if (opts?.start) p.set('start', opts.start);
    if (opts?.end) p.set('end', opts.end);
    const qs = p.toString();
    return request<SeriesResponse>(`/api/v2/datasets/${encodeURIComponent(id)}/series${qs ? `?${qs}` : ''}`);
  },

  getQuality: (id: string) => request<QualityReport>(`/api/v2/datasets/${encodeURIComponent(id)}/quality`),

  // §4.1 — Kalman μ* + causal z
  equilibrium: (body: EquilibriumRequest) =>
    request<EquilibriumResponse>('/api/v2/analysis/equilibrium', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  // §4.2 — surrogate-relative habitat score (cloud is mandatory in the response)
  habitat: (body: HabitatRequest) =>
    request<HabitatResponse>('/api/v2/analysis/habitat', {
      method: 'POST',
      body: JSON.stringify(body),
    }),
};

// ── display-only helper: bin null_min_vr[] into histogram BARS (NOT a scalar). ──────────
// Per M5 this is permitted for RENDERING only; it derives no displayed number.
export interface HistogramBin {
  x0: number;
  x1: number;
  count: number;
}

export function binForHistogram(values: number[], nbins = 24): HistogramBin[] {
  const finite = values.filter((v) => Number.isFinite(v));
  if (finite.length === 0) return [];
  let lo = Math.min(...finite);
  let hi = Math.max(...finite);
  if (lo === hi) {
    hi = lo + 1e-9;
  }
  const width = (hi - lo) / nbins;
  const bins: HistogramBin[] = Array.from({ length: nbins }, (_, i) => ({
    x0: lo + i * width,
    x1: lo + (i + 1) * width,
    count: 0,
  }));
  for (const v of finite) {
    let idx = Math.floor((v - lo) / width);
    if (idx >= nbins) idx = nbins - 1;
    if (idx < 0) idx = 0;
    bins[idx].count += 1;
  }
  return bins;
}
