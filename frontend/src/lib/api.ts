import type { LoadRequest, LoadResponse, SpreadRequest, InstrumentMeta, OHLCVResponse, EstimatorResponse, ResearchResponse, DiagnosticsResponse, VelocityAbsorptionResponse, MRScoreResponse, SubstrateResponse } from './types';

const BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

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

export const api = {
  loadInstrument: (body: LoadRequest) =>
    request<LoadResponse>('/api/v1/market/load', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  listInstruments: () =>
    request<InstrumentMeta[]>('/api/v1/market/instruments'),

  suggestPaths: (prefix: string) =>
    request<{ suggestions: string[] }>(
      `/api/v1/market/suggest-paths?prefix=${encodeURIComponent(prefix)}`
    ),

  createSpread: (body: SpreadRequest) =>
    request<LoadResponse>('/api/v1/market/spread', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  uploadInstruments: async (files: File[]): Promise<LoadResponse[]> => {
    const form = new FormData();
    files.forEach(f => form.append('files', f));
    const res = await fetch(`${BASE}/api/v1/market/upload`, { method: 'POST', body: form });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error((err as { detail?: string }).detail ?? 'Upload failed');
    }
    return res.json() as Promise<LoadResponse[]>;
  },

  getOHLCV: (instrumentId: string, start?: string, end?: string) => {
    const params = new URLSearchParams();
    if (start) params.set('start', start);
    if (end) params.set('end', end);
    const qs = params.toString();
    return request<OHLCVResponse>(
      `/api/v1/market/${instrumentId}/ohlcv${qs ? `?${qs}` : ''}`
    );
  },

  getEstimator: (instrumentId: string, window: number, start?: string, end?: string) => {
    const params = new URLSearchParams({ estimator: 'ema', window: String(window) });
    if (start) params.set('start', start);
    if (end) params.set('end', end);
    return request<EstimatorResponse>(
      `/api/v1/market/${instrumentId}/estimator?${params.toString()}`
    );
  },

  getResearch: (instrumentId: string, window: number, start?: string, end?: string) => {
    const params = new URLSearchParams({ estimator: 'ema', window: String(window) });
    if (start) params.set('start', start);
    if (end) params.set('end', end);
    return request<ResearchResponse>(
      `/api/v1/market/${instrumentId}/research?${params.toString()}`
    );
  },

  getDiagnostics: (instrumentId: string, window: number, start?: string, end?: string) => {
    const params = new URLSearchParams({ estimator: 'ema', window: String(window) });
    if (start) params.set('start', start);
    if (end) params.set('end', end);
    return request<DiagnosticsResponse>(
      `/api/v1/market/${instrumentId}/diagnostics?${params.toString()}`
    );
  },

  getVelocityAbsorption: (instrumentId: string, start?: string, end?: string) => {
    const params = new URLSearchParams();
    if (start) params.set('start', start);
    if (end) params.set('end', end);
    const qs = params.toString();
    return request<VelocityAbsorptionResponse>(
      `/api/v1/market/${instrumentId}/velocity-absorption${qs ? `?${qs}` : ''}`
    );
  },

  getMRScore: (instrumentId: string, window: number, start?: string, end?: string) => {
    const params = new URLSearchParams({ window: String(window) });
    if (start) params.set('start', start);
    if (end) params.set('end', end);
    return request<MRScoreResponse>(
      `/api/v1/market/${instrumentId}/mrscore?${params.toString()}`
    );
  },

  getSubstrate: (instrumentId: string, window: number, start?: string, end?: string) => {
    const params = new URLSearchParams({ window: String(window) });
    if (start) params.set('start', start);
    if (end) params.set('end', end);
    return request<SubstrateResponse>(
      `/api/v1/market/${instrumentId}/substrate?${params.toString()}`
    );
  },
};
