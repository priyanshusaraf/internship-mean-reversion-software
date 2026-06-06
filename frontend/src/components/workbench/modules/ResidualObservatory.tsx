'use client';

import { useEffect, useRef, useState } from 'react';
import {
  createChart, ColorType, CrosshairMode,
  type IChartApi, type ISeriesApi, type Time,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import type { ModuleProps } from '../types';
import type { DiagnosticsResponse } from '@/lib/types';

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};
function fmt(n: number, d = 2) { return n.toFixed(d); }

// ── Histogram (SVG) ───────────────────────────────────────────────────────────
function Histogram({ values, mean, std }: { values: number[]; mean: number; std: number }) {
  const BINS = 24;
  const W = 280, H = 100;
  if (!values.length) return null;

  const min = Math.min(...values), max = Math.max(...values);
  const range = max - min || 1;
  const binWidth = range / BINS;
  const counts = Array(BINS).fill(0);
  values.forEach(v => {
    const b = Math.min(Math.floor((v - min) / binWidth), BINS - 1);
    counts[b]++;
  });
  const maxCount = Math.max(...counts);
  const barW = W / BINS;

  // Normal overlay
  const normalY = (x: number) => {
    const z = (x - mean) / (std || 1);
    const density = Math.exp(-0.5 * z * z) / (Math.sqrt(2 * Math.PI) * (std || 1));
    return density;
  };
  const normalScale = (maxCount / values.length) / (1 / (Math.sqrt(2 * Math.PI) * (std || 1)));
  const normalPts = Array.from({ length: 60 }, (_, i) => {
    const x = min + (i / 59) * range;
    const y = normalY(x) * normalScale * values.length;
    return `${(i / 59) * W},${H - (y / maxCount) * H * 0.9}`;
  }).join(' ');

  const zeroX = ((0 - min) / range) * W;

  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} style={{ display: 'block' }}>
      {counts.map((c, i) => {
        const barH = (c / maxCount) * H * 0.9;
        const isNeg = (min + i * binWidth + binWidth / 2) < 0;
        return (
          <rect key={i}
            x={i * barW + 0.5} y={H - barH} width={barW - 1} height={barH}
            fill={isNeg ? 'rgba(248,81,73,0.35)' : 'rgba(63,185,80,0.35)'}
          />
        );
      })}
      <polyline points={normalPts} fill="none" stroke="rgba(88,166,255,0.5)" strokeWidth="1" />
      {zeroX > 0 && zeroX < W && (
        <line x1={zeroX} y1={0} x2={zeroX} y2={H} stroke="rgba(255,255,255,0.1)" strokeDasharray="3,3" />
      )}
    </svg>
  );
}

// ── ACF bars (SVG) ────────────────────────────────────────────────────────────
function ACFBars({ stats }: { stats: DiagnosticsResponse['stats'] }) {
  const W = 280, H = 80;
  const lags = [
    { lag: 'lag1', v: stats.acf_lag1 },
    { lag: 'lag5', v: stats.acf_lag5 },
    { lag: 'lag10', v: stats.acf_lag10 },
    { lag: 'lag20', v: stats.acf_lag20 },
  ];
  const barW = W / (lags.length * 2);
  const cy = H / 2;

  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} style={{ display: 'block' }}>
      <line x1={0} y1={cy} x2={W} y2={cy} stroke="rgba(255,255,255,0.08)" />
      {/* ±0.1 reference lines */}
      <line x1={0} y1={cy - H * 0.1} x2={W} y2={cy - H * 0.1} stroke="rgba(88,166,255,0.15)" strokeDasharray="3,3" />
      <line x1={0} y1={cy + H * 0.1} x2={W} y2={cy + H * 0.1} stroke="rgba(88,166,255,0.15)" strokeDasharray="3,3" />
      {lags.map(({ lag, v }, i) => {
        const x = (i * 2 + 0.5) * barW;
        const barH = Math.abs(v) * cy * 0.9;
        const y = v >= 0 ? cy - barH : cy;
        return (
          <g key={lag}>
            <rect x={x} y={y} width={barW} height={barH}
              fill={v > 0.1 ? 'rgba(248,81,73,0.6)' : 'rgba(88,166,255,0.4)'} />
            <text x={x + barW / 2} y={H - 2} textAnchor="middle"
              style={{ fontFamily: 'ui-monospace,monospace', fontSize: 8, fill: '#3d4d5e' }}>
              {lag}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

export function ResidualObservatory({ instrumentId, dateRange, window: win }: ModuleProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const epsSeriesRef = useRef<ISeriesApi<'Line'> | null>(null);
  const rollMeanRef = useRef<ISeriesApi<'Line'> | null>(null);
  const upper1Ref = useRef<ISeriesApi<'Line'> | null>(null);
  const lower1Ref = useRef<ISeriesApi<'Line'> | null>(null);

  const [data, setData] = useState<DiagnosticsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
    epsSeriesRef.current = chart.addLineSeries({ color: 'rgba(140,180,200,0.7)', lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 'ε' });
    rollMeanRef.current = chart.addLineSeries({ color: 'rgba(255,200,60,0.3)', lineWidth: 1, lastValueVisible: false, priceLineVisible: false });
    upper1Ref.current = chart.addLineSeries({ color: 'rgba(63,185,80,0.2)', lineWidth: 1, lineStyle: 3, lastValueVisible: false, priceLineVisible: false });
    lower1Ref.current = chart.addLineSeries({ color: 'rgba(248,81,73,0.2)', lineWidth: 1, lineStyle: 3, lastValueVisible: false, priceLineVisible: false });
    chartRef.current = chart;
    const ro = new ResizeObserver(() => containerRef.current && chart.applyOptions({ width: containerRef.current.clientWidth, height: containerRef.current.clientHeight }));
    ro.observe(containerRef.current);
    return () => { ro.disconnect(); chart.remove(); chartRef.current = null; };
  }, []);

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
        epsSeriesRef.current?.setData(resp.rows.map(r => ({ time: toTime(r.date), value: r.epsilon })));
        rollMeanRef.current?.setData(resp.rows.map(r => ({ time: toTime(r.date), value: r.epsilon_rolling_mean })));
        upper1Ref.current?.setData(resp.rows.map(r => ({ time: toTime(r.date), value: r.epsilon_rolling_mean + r.epsilon_rolling_std })));
        lower1Ref.current?.setData(resp.rows.map(r => ({ time: toTime(r.date), value: r.epsilon_rolling_mean - r.epsilon_rolling_std })));
        chartRef.current?.timeScale().fitContent();
      })
      .catch((e: unknown) => { if (!cancelled) setError(e instanceof Error ? e.message : 'Fetch failed'); })
      .finally(() => { if (!cancelled) setLoading(false); });

    return () => { cancelled = true; };
  }, [instrumentId, dateRange.start, dateRange.end, win]); // eslint-disable-line react-hooks/exhaustive-deps

  const s = data?.stats;
  const epsilonValues = data?.rows.map(r => r.epsilon) ?? [];

  return (
    <div style={{ display: 'flex', height: '100%', background: '#070b10' }}>
      {/* Left: residual time series */}
      <div style={{ flex: '0 0 60%', minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 16, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.14em', textTransform: 'uppercase' }}>Residual Observatory — ε = P − μ*</span>
          {loading && <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>loading</span>}
          {error && <span style={{ ...mono, fontSize: 9, color: '#f85149' }}>{error}</span>}
        </div>
        <div ref={containerRef} style={{ flex: 1, minHeight: 0 }} />
      </div>

      {/* Right: distribution + ACF + stats */}
      <div style={{ flex: '0 0 40%', minWidth: 0, borderLeft: '1px solid #0e1520', display: 'flex', flexDirection: 'column', background: '#070b10' }}>
        {/* Distribution */}
        <div style={{ flex: '0 0 50%', minHeight: 0, borderBottom: '1px solid #0e1520', display: 'flex', flexDirection: 'column' }}>
          <div style={{ height: 20, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 10, background: '#06090e', borderBottom: '1px solid #0a0f16' }}>
            <span style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase' }}>Distribution</span>
          </div>
          <div style={{ flex: 1, minHeight: 0, padding: '8px 10px' }}>
            {s && <Histogram values={epsilonValues} mean={s.epsilon_mean} std={s.epsilon_std} />}
          </div>
        </div>

        {/* ACF */}
        <div style={{ flex: '0 0 30%', minHeight: 0, borderBottom: '1px solid #0e1520', display: 'flex', flexDirection: 'column' }}>
          <div style={{ height: 20, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 10, gap: 8, background: '#06090e', borderBottom: '1px solid #0a0f16' }}>
            <span style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase' }}>Autocorrelation of ε</span>
            <span style={{ ...mono, fontSize: 8, color: '#1e2833' }}>— red bar = ACF &gt; 0.1</span>
          </div>
          <div style={{ flex: 1, minHeight: 0, padding: '6px 10px' }}>
            {s && <ACFBars stats={s} />}
          </div>
          <div style={{ flexShrink: 0, padding: '3px 10px', borderTop: '1px solid #0a0f16', background: '#06090e' }}>
            <span style={{ ...mono, fontSize: 8, color: '#1e2833', lineHeight: 1.4 }}>
              ⚠ High ACF does not prove mean-reversion. EMA residuals inherit EMA autocorrelation — a pure random walk filtered through EMA-20 will show ACF lag1 ≈ 0.88. Use half-life and visual ε behavior together.
            </span>
          </div>
        </div>

        {/* Stats */}
        <div style={{ flex: 1, minHeight: 0, padding: '8px 10px', overflowY: 'auto' }}>
          {s ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {([
                ['n', String(s.n)],
                ['mean ε', fmt(s.epsilon_mean)],
                ['std ε', fmt(s.epsilon_std)],
                ['skew', fmt(s.epsilon_skew, 3)],
                ['kurtosis', fmt(s.epsilon_kurt, 3)],
                ['half-life', s.halflife_bars != null ? fmt(s.halflife_bars, 1) + ' bars' : 'n/m'],
              ] as [string, string][]).map(([label, value]) => (
                <div key={label} style={{ display: 'flex', justifyContent: 'space-between', padding: '2px 0', borderBottom: '1px solid #0a0f16' }}>
                  <span style={{ ...mono, fontSize: 9, color: '#2d3a4a' }}>{label}</span>
                  <span style={{ ...mono, fontSize: 10, color: '#8b99a8' }}>{value}</span>
                </div>
              ))}
            </div>
          ) : (
            <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>—</span>
          )}
        </div>
      </div>
    </div>
  );
}
