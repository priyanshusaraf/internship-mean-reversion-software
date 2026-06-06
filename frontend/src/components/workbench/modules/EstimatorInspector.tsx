'use client';

import { useEffect, useRef, useState } from 'react';
import {
  createChart, ColorType, CrosshairMode,
  type IChartApi, type ISeriesApi, type LineData, type Time,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import type { ModuleProps } from '../types';
import type { DiagnosticsResponse } from '@/lib/types';

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

function fmt(n: number, d = 2) { return n.toFixed(d); }

function StatRow({ label, value, dim }: { label: string; value: string; dim?: boolean }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '3px 0', borderBottom: '1px solid #0a0f16' }}>
      <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.06em' }}>{label}</span>
      <span style={{ ...mono, fontSize: 10, color: dim ? '#3d4d5e' : '#8b99a8' }}>{value}</span>
    </div>
  );
}

export function EstimatorInspector({ instrumentId, dateRange, window: win }: ModuleProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const diffContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const diffChartRef = useRef<IChartApi | null>(null);
  const priceSeriesRef = useRef<ISeriesApi<'Line'> | null>(null);
  const causalSeriesRef = useRef<ISeriesApi<'Line'> | null>(null);
  const fullSeriesRef = useRef<ISeriesApi<'Line'> | null>(null);
  const diffSeriesRef = useRef<ISeriesApi<'Line'> | null>(null);

  const [data, setData] = useState<DiagnosticsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Init price chart
  useEffect(() => {
    if (!containerRef.current) return;
    const chart = createChart(containerRef.current, {
      layout: { background: { type: ColorType.Solid, color: '#070b10' }, textColor: '#3d4d5e', fontSize: 10 },
      grid: { vertLines: { color: '#0e1520' }, horzLines: { color: '#0e1520' } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: '#161d27' },
      timeScale: { borderColor: '#161d27' },
      width: containerRef.current.clientWidth,
      height: containerRef.current.clientHeight,
    });
    priceSeriesRef.current = chart.addLineSeries({ color: 'rgba(200,210,220,0.3)', lineWidth: 1, lastValueVisible: false, priceLineVisible: false });
    causalSeriesRef.current = chart.addLineSeries({ color: 'rgba(88,166,255,0.85)', lineWidth: 1, lastValueVisible: true, priceLineVisible: false, title: 'μ* causal' });
    fullSeriesRef.current = chart.addLineSeries({ color: 'rgba(88,166,255,0.3)', lineWidth: 1, lineStyle: 2, lastValueVisible: false, priceLineVisible: false, title: 'μ* adj' });
    chartRef.current = chart;
    const ro = new ResizeObserver(() => containerRef.current && chart.applyOptions({ width: containerRef.current.clientWidth, height: containerRef.current.clientHeight }));
    ro.observe(containerRef.current);
    return () => { ro.disconnect(); chart.remove(); chartRef.current = null; };
  }, []);

  // Init diff chart
  useEffect(() => {
    if (!diffContainerRef.current) return;
    const chart = createChart(diffContainerRef.current, {
      layout: { background: { type: ColorType.Solid, color: '#06090e' }, textColor: '#3d4d5e', fontSize: 9 },
      grid: { vertLines: { color: '#0c1118' }, horzLines: { color: '#0c1118' } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: '#161d27' },
      timeScale: { borderColor: '#161d27', visible: false },
      width: diffContainerRef.current.clientWidth,
      height: diffContainerRef.current.clientHeight,
    });
    diffSeriesRef.current = chart.addLineSeries({ color: 'rgba(210,153,60,0.7)', lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 'Δ gap' });
    diffChartRef.current = chart;
    const ro = new ResizeObserver(() => diffContainerRef.current && chart.applyOptions({ width: diffContainerRef.current.clientWidth, height: diffContainerRef.current.clientHeight }));
    ro.observe(diffContainerRef.current);
    return () => { ro.disconnect(); chart.remove(); diffChartRef.current = null; };
  }, []);

  // Fetch data
  useEffect(() => {
    setError(null);
    if (!instrumentId) return;
    let cancelled = false;
    setLoading(true);

    api.getDiagnostics(instrumentId, win, dateRange.start ?? undefined, dateRange.end ?? undefined)
      .then((resp) => {
        if (cancelled) return;
        setData(resp);
        const toTime = (d: string) => d as Time;
        priceSeriesRef.current?.setData(resp.rows.map(r => ({ time: toTime(r.date), value: r.close })));
        causalSeriesRef.current?.setData(resp.rows.map(r => ({ time: toTime(r.date), value: r.mu_star })));
        fullSeriesRef.current?.setData(resp.rows.map(r => ({ time: toTime(r.date), value: r.mu_star_adj })));
        diffSeriesRef.current?.setData(resp.rows.map(r => ({ time: toTime(r.date), value: r.mu_star_diff })));
        chartRef.current?.timeScale().fitContent();
        diffChartRef.current?.timeScale().fitContent();
      })
      .catch((e: unknown) => { if (!cancelled) setError(e instanceof Error ? e.message : 'Fetch failed'); })
      .finally(() => { if (!cancelled) setLoading(false); });

    return () => { cancelled = true; };
  }, [instrumentId, dateRange.start, dateRange.end, win]); // eslint-disable-line react-hooks/exhaustive-deps

  const s = data?.stats;

  return (
    <div style={{ display: 'flex', height: '100%', background: '#070b10' }}>
      {/* Charts area */}
      <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 16, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.14em', textTransform: 'uppercase' }}>Estimator Inspector</span>
          {loading && <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>loading</span>}
          {error && <span style={{ ...mono, fontSize: 9, color: '#f85149' }}>{error}</span>}
          <span style={{ ...mono, fontSize: 9, color: '#1e2833', marginLeft: 'auto', marginRight: 12 }}>
            price (dim) · μ* causal/adjust=False (blue) · μ* adjusted/adjust=True (dashed) · Δ init gap (amber)
          </span>
        </div>

        {/* Price + estimator chart (70%) */}
        <div style={{ flex: '0 0 70%', minHeight: 0, display: 'flex', flexDirection: 'column' }}>
          <div ref={containerRef} style={{ flex: 1, minHeight: 0 }} />
        </div>

        {/* Δ gap chart (30%) */}
        <div style={{ flex: '0 0 30%', minHeight: 0, display: 'flex', flexDirection: 'column', borderTop: '1px solid #0e1520' }}>
          <div style={{ height: 16, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, background: '#06090e', borderBottom: '1px solid #0a0f16' }}>
            <span style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.12em', textTransform: 'uppercase' }}>Δ = μ*_adj − μ*_causal (EMA initialization gap — nonzero only in warmup period)</span>
          </div>
          <div ref={diffContainerRef} style={{ flex: 1, minHeight: 0 }} />
        </div>
      </div>

      {/* Stats sidebar */}
      <div style={{ width: 160, flexShrink: 0, borderLeft: '1px solid #0e1520', background: '#090d13', padding: '10px 12px', display: 'flex', flexDirection: 'column', gap: 2, overflowY: 'auto' }}>
        <div style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 6 }}>Stats</div>
        {s ? (
          <>
            <StatRow label="n" value={String(s.n)} />
            <StatRow label="Δ mean" value={fmt(s.mu_star_diff_mean)} />
            <StatRow label="Δ max" value={fmt(s.mu_star_diff_max)} />
            <div style={{ marginTop: 8, marginBottom: 4, ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase' }}>Residual ε</div>
            <StatRow label="mean" value={fmt(s.epsilon_mean)} />
            <StatRow label="std" value={fmt(s.epsilon_std)} />
            <StatRow label="skew" value={fmt(s.epsilon_skew, 3)} />
            <StatRow label="kurt" value={fmt(s.epsilon_kurt, 3)} />
            <div style={{ marginTop: 8, marginBottom: 4, ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase' }}>Persistence</div>
            <StatRow label="ACF lag1" value={fmt(s.acf_lag1, 3)} />
            <StatRow label="ACF lag5" value={fmt(s.acf_lag5, 3)} />
            <StatRow label="half-life" value={s.halflife_bars != null ? fmt(s.halflife_bars, 1) + ' bars' : 'n/m'} />
          </>
        ) : (
          <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>—</span>
        )}
      </div>
    </div>
  );
}
