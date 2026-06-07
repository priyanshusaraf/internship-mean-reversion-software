'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import {
  createChart, ColorType, CrosshairMode,
  type IChartApi, type ISeriesApi, type Time, type LineData,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import { centeredMA } from '@/lib/smoothers';
import type { ModuleProps } from '../types';
import type { DiagnosticsResponse } from '@/lib/types';

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

const EPS = 1e-9;

/**
 * Per-bandwidth decomposition of the causal residual, frozen identity:  ε_c = ε_h + L
 *   μ*_c  = causal EMA μ*            (knowable at t)         = rows.mu_star
 *   μ*_h  = centered smoother        (retrospective reference equilibrium proxy — future-using, NOT truth)
 *   L     = μ*_h − μ*_c              (lag component)
 *   ε_c   = P − μ*_c                 (causal residual — bandwidth-independent)
 *   ε_h   = P − μ*_h                 (residual vs reference proxy)
 *   s     = |L| / (|L| + |ε_h|)      (lag-share, continuous, descriptive only — no thresholds)
 * Edge bars within k of either end lack full ±k support → MASKED (null), never inferred.
 */
interface BandSeries {
  k: number;
  ec: (LineData | null)[];   // causal residual (masked to this band's support for visual alignment)
  eh: (LineData | null)[];   // ε_h vs reference proxy
  L: (LineData | null)[];    // lag component
  s: (LineData | null)[];    // lag-share s(t) ∈ [0,1]
}

function buildBand(dates: string[], closes: number[], muc: number[], k: number): BandSeries {
  const n = closes.length;
  const muh = centeredMA(closes, k);
  const ec: (LineData | null)[] = new Array(n).fill(null);
  const eh: (LineData | null)[] = new Array(n).fill(null);
  const L: (LineData | null)[] = new Array(n).fill(null);
  const s: (LineData | null)[] = new Array(n).fill(null);
  for (let i = 0; i < n; i++) {
    if (i < k || i >= n - k) continue; // mandatory edge masking — no full ±k support
    const t = dates[i] as Time;
    const ecV = closes[i] - muc[i];
    const ehV = closes[i] - muh[i];
    const lV = muh[i] - muc[i];
    ec[i] = { time: t, value: ecV };
    eh[i] = { time: t, value: ehV };
    L[i] = { time: t, value: lV };
    const denom = Math.abs(lV) + Math.abs(ehV);
    s[i] = denom > EPS ? { time: t, value: Math.abs(lV) / denom } : null; // mask when no residual to attribute
  }
  return { k, ec, eh, L, s };
}

const clean = (arr: (LineData | null)[]) => arr.filter((p): p is LineData => p !== null);

export function LagIllusion({ instrumentId, dateRange, window: win }: ModuleProps) {
  const decompRef = useRef<HTMLDivElement>(null);
  const shareRef = useRef<HTMLDivElement>(null);
  const decompChart = useRef<IChartApi | null>(null);
  const shareChart = useRef<IChartApi | null>(null);
  const ecS = useRef<ISeriesApi<'Line'> | null>(null);
  const ehS = useRef<ISeriesApi<'Line'> | null>(null);
  const lS = useRef<ISeriesApi<'Line'> | null>(null);
  const sAS = useRef<ISeriesApi<'Line'> | null>(null);
  const sBS = useRef<ISeriesApi<'Line'> | null>(null);

  const [data, setData] = useState<DiagnosticsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [band, setBand] = useState<'a' | 'b'>('a'); // which bandwidth the decomposition panel shows

  // Decomposition chart (top)
  useEffect(() => {
    if (!decompRef.current) return;
    const chart = createChart(decompRef.current, {
      layout: { background: { type: ColorType.Solid, color: '#070b10' }, textColor: '#3d4d5e', fontSize: 10 },
      grid: { vertLines: { color: '#0e1520' }, horzLines: { color: '#0e1520' } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: '#161d27' },
      timeScale: { borderColor: '#161d27' },
      width: decompRef.current.clientWidth, height: decompRef.current.clientHeight,
    });
    ecS.current = chart.addLineSeries({ color: 'rgba(88,166,255,0.9)', lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 'ε_c causal' });
    ehS.current = chart.addLineSeries({ color: 'rgba(210,153,60,0.85)', lineWidth: 1, lineStyle: 2, lastValueVisible: false, priceLineVisible: false, title: 'ε_h vs proxy' });
    lS.current = chart.addLineSeries({ color: 'rgba(229,108,108,0.85)', lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 'L lag' });
    decompChart.current = chart;
    const ro = new ResizeObserver(() => decompRef.current && chart.applyOptions({ width: decompRef.current.clientWidth, height: decompRef.current.clientHeight }));
    ro.observe(decompRef.current);
    return () => { ro.disconnect(); chart.remove(); decompChart.current = null; };
  }, []);

  // Lag-share chart (bottom) — both bandwidths overlaid (robustness / K4 check)
  useEffect(() => {
    if (!shareRef.current) return;
    const chart = createChart(shareRef.current, {
      layout: { background: { type: ColorType.Solid, color: '#06090e' }, textColor: '#3d4d5e', fontSize: 9 },
      grid: { vertLines: { color: '#0c1118' }, horzLines: { color: '#0c1118' } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: '#161d27' },
      timeScale: { borderColor: '#161d27', visible: false },
      width: shareRef.current.clientWidth, height: shareRef.current.clientHeight,
    });
    sAS.current = chart.addLineSeries({ color: 'rgba(86,211,160,0.85)', lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 's (k_a)' });
    sBS.current = chart.addLineSeries({ color: 'rgba(170,130,255,0.7)', lineWidth: 1, lineStyle: 2, lastValueVisible: false, priceLineVisible: false, title: 's (k_b)' });
    shareChart.current = chart;
    const ro = new ResizeObserver(() => shareRef.current && chart.applyOptions({ width: shareRef.current.clientWidth, height: shareRef.current.clientHeight }));
    ro.observe(shareRef.current);
    return () => { ro.disconnect(); chart.remove(); shareChart.current = null; };
  }, []);

  // Fetch once per (instrument, window, range). Causal μ* from backend; reference proxy client-side.
  useEffect(() => {
    setError(null);
    if (!instrumentId) return;
    let cancelled = false;
    setLoading(true);
    api.getDiagnostics(instrumentId, win, dateRange.start ?? undefined, dateRange.end ?? undefined)
      .then((resp) => { if (!cancelled) setData(resp); })
      .catch((e: unknown) => { if (!cancelled) setError(e instanceof Error ? e.message : 'Fetch failed'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [instrumentId, dateRange.start, dateRange.end, win]);

  // Two FIXED, span-derived bandwidths (not tuned, not searched).
  const ka = Math.max(1, Math.floor(win / 2));
  const kb = Math.max(2, win);

  const bands = useMemo(() => {
    if (!data) return null;
    const rows = data.rows;
    const dates = rows.map(r => r.date);
    const closes = rows.map(r => r.close);
    const muc = rows.map(r => r.mu_star);
    return { a: buildBand(dates, closes, muc, ka), b: buildBand(dates, closes, muc, kb) };
  }, [data, ka, kb]);

  // Push decomposition (selected band) + both lag-share curves
  useEffect(() => {
    if (!bands) return;
    const sel = band === 'a' ? bands.a : bands.b;
    ecS.current?.setData(clean(sel.ec));
    ehS.current?.setData(clean(sel.eh));
    lS.current?.setData(clean(sel.L));
    sAS.current?.setData(clean(bands.a.s));
    sBS.current?.setData(clean(bands.b.s));
    decompChart.current?.timeScale().fitContent();
    shareChart.current?.timeScale().fitContent();
  }, [bands, band]);

  const n = data?.rows.length ?? 0;
  const selK = band === 'a' ? ka : kb;

  return (
    <div style={{ display: 'flex', height: '100%', background: '#070b10' }}>
      <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 12, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', letterSpacing: '0.14em', textTransform: 'uppercase' }}>Lag Illusion · ε_c = ε_h + L</span>
          {loading && <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>loading</span>}
          {error && <span style={{ ...mono, fontSize: 9, color: '#f85149' }}>{error}</span>}
          <div style={{ display: 'flex', gap: 6, marginLeft: 'auto', marginRight: 12, alignItems: 'center' }}>
            <span style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.08em' }}>BANDWIDTH</span>
            {(['a', 'b'] as const).map(b => (
              <button key={b} onClick={() => setBand(b)} style={{
                ...mono, fontSize: 9, padding: '2px 8px', borderRadius: 3, letterSpacing: '0.04em',
                background: band === b ? 'rgba(255,255,255,0.04)' : 'transparent',
                border: `1px solid ${band === b ? 'rgba(88,166,255,0.7)' : '#161d27'}`,
                color: band === b ? 'rgba(88,166,255,0.9)' : '#2d3a4a', cursor: 'pointer',
              }}>
                k={b === 'a' ? ka : kb}
              </button>
            ))}
          </div>
        </div>

        {/* Decomposition (70%) */}
        <div style={{ flex: '0 0 68%', minHeight: 0, display: 'flex', flexDirection: 'column' }}>
          <div ref={decompRef} style={{ flex: 1, minHeight: 0 }} />
        </div>

        {/* Lag-share strip (32%) */}
        <div style={{ flex: '0 0 32%', minHeight: 0, display: 'flex', flexDirection: 'column', borderTop: '1px solid #0e1520' }}>
          <div style={{ height: 16, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, background: '#06090e', borderBottom: '1px solid #0a0f16' }}>
            <span style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
              lag-share s = |L| / (|L| + |ε_h|) ∈ [0,1] — both bandwidths (teal k={ka}, purple k={kb}); agreement ⇒ robust to bandwidth (K4)
            </span>
          </div>
          <div ref={shareRef} style={{ flex: 1, minHeight: 0 }} />
        </div>
      </div>

      {/* Legend / honesty panel */}
      <div style={{ width: 188, flexShrink: 0, borderLeft: '1px solid #0e1520', background: '#090d13', padding: '10px 12px', display: 'flex', flexDirection: 'column', gap: 2, overflowY: 'auto' }}>
        <div style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 6 }}>Decomposition</div>
        <Legend color="rgba(88,166,255,0.9)" label="ε_c" desc="causal residual P − μ*_c" />
        <Legend color="rgba(210,153,60,0.85)" label="ε_h" desc="P − μ*_h (vs reference proxy)" />
        <Legend color="rgba(229,108,108,0.85)" label="L" desc="μ*_h − μ*_c (lag)" />
        <div style={{ ...mono, fontSize: 8, color: '#1e2833', marginTop: 10, lineHeight: 1.6 }}>
          μ*_h is a <b style={{ color: 'var(--amr-text)' }}>retrospective reference equilibrium proxy</b> (centered smoother, future-using) — <b style={{ color: 'var(--amr-text)' }}>NOT</b> true equilibrium.
        </div>
        <div style={{ ...mono, fontSize: 8, color: '#1e2833', marginTop: 10, lineHeight: 1.6 }}>
          s≈1: residual is mostly mechanical lag — reading it as reversion is mechanically induced.
          s≈0: residual tracks the reference-proxy deviation.
        </div>
        <div style={{ ...mono, fontSize: 8, color: '#1e2833', marginTop: 10, lineHeight: 1.6 }}>
          Mode B (snapback): ε_c and L collapse toward 0 together while ε_h stays put → apparent reversion is the smoother re-equilibrating, not price reverting.
        </div>
        <div style={{ ...mono, fontSize: 8, color: '#1e2833', marginTop: 10, lineHeight: 1.6 }}>
          First/last k bars masked (no ±k support). Single instrument — does not generalize.
        </div>
        <div style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', marginTop: 'auto', paddingTop: 8 }}>
          shown k={selK} · n={n}
        </div>
      </div>
    </div>
  );
}

function Legend({ color, label, desc }: { color: string; label: string; desc: string }) {
  return (
    <div style={{ display: 'flex', alignItems: 'baseline', gap: 6, padding: '2px 0', borderBottom: '1px solid #0a0f16' }}>
      <span style={{ width: 10, height: 2, background: color, flexShrink: 0, transform: 'translateY(-2px)' }} />
      <span style={{ ...mono, fontSize: 10, color: '#8b99a8', width: 22, flexShrink: 0 }}>{label}</span>
      <span style={{ ...mono, fontSize: 8, color: 'var(--amr-text-dim)' }}>{desc}</span>
    </div>
  );
}
