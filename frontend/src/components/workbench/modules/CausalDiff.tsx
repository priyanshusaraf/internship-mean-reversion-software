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
function fmt(n: number, d = 3) { return n.toFixed(d); }

// ── Scatter plot (SVG) ────────────────────────────────────────────────────────
function ScatterPlot({ xVals, yVals, xLabel, yLabel }: {
  xVals: number[]; yVals: number[]; xLabel: string; yLabel: string;
}) {
  if (!xVals.length) return null;
  const W = 220, H = 140, PAD = 16;

  const xMin = Math.min(...xVals), xMax = Math.max(...xVals);
  const yMin = Math.min(...yVals), yMax = Math.max(...yVals);
  const xRange = (xMax - xMin) || 1;
  const yRange = (yMax - yMin) || 1;

  const px = (v: number) => PAD + ((v - xMin) / xRange) * (W - 2 * PAD);
  const py = (v: number) => H - PAD - ((v - yMin) / yRange) * (H - 2 * PAD);

  // Simple Pearson r
  const n = xVals.length;
  const xm = xVals.reduce((a, b) => a + b, 0) / n;
  const ym = yVals.reduce((a, b) => a + b, 0) / n;
  const cov = xVals.reduce((s, x, i) => s + (x - xm) * (yVals[i] - ym), 0) / n;
  const sx = Math.sqrt(xVals.reduce((s, x) => s + (x - xm) ** 2, 0) / n);
  const sy = Math.sqrt(yVals.reduce((s, y) => s + (y - ym) ** 2, 0) / n);
  const r = sx > 0 && sy > 0 ? cov / (sx * sy) : 0;

  // Regression line
  const slope = sx > 0 ? (cov / (sx * sx)) : 0;
  const intercept = ym - slope * xm;
  const regPts = [xMin, xMax].map(x => `${px(x)},${py(slope * x + intercept)}`).join(' ');

  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} style={{ display: 'block' }}>
      <line x1={PAD} y1={py(0)} x2={W - PAD} y2={py(0)} stroke="rgba(255,255,255,0.06)" />
      <line x1={px(0)} y1={PAD} x2={px(0)} y2={H - PAD} stroke="rgba(255,255,255,0.06)" />
      {xVals.map((x, i) => (
        <circle key={i} cx={px(x)} cy={py(yVals[i])} r={1.5} fill="rgba(88,166,255,0.25)" />
      ))}
      <polyline points={regPts} fill="none" stroke="rgba(210,153,60,0.6)" strokeWidth="1" />
      <text x={W - 4} y={H - 2} textAnchor="end" style={{ fontFamily: 'ui-monospace,monospace', fontSize: 8, fill: '#3d4d5e' }}>
        r={fmt(r)}
      </text>
      <text x={PAD} y={10} style={{ fontFamily: 'ui-monospace,monospace', fontSize: 7, fill: '#1e2833' }}>y: {yLabel}</text>
      <text x={W - PAD} y={H - 3} textAnchor="end" style={{ fontFamily: 'ui-monospace,monospace', fontSize: 7, fill: '#1e2833' }}>{xLabel}</text>
    </svg>
  );
}

export function CausalDiff({ instrumentId, dateRange, window: win }: ModuleProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const diffEpsRef = useRef<ISeriesApi<'Line'> | null>(null);
  const diffMuRef = useRef<ISeriesApi<'Line'> | null>(null);

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
    diffEpsRef.current = chart.addLineSeries({ color: 'rgba(88,166,255,0.7)', lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 'Δε' });
    diffMuRef.current = chart.addLineSeries({ color: 'rgba(210,153,60,0.5)', lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 'Δμ*' });
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
        diffEpsRef.current?.setData(resp.rows.map(r => ({ time: toTime(r.date), value: r.epsilon - r.epsilon_adj })));
        diffMuRef.current?.setData(resp.rows.map(r => ({ time: toTime(r.date), value: r.mu_star_diff })));
        chartRef.current?.timeScale().fitContent();
      })
      .catch((e: unknown) => { if (!cancelled) setError(e instanceof Error ? e.message : 'Fetch failed'); })
      .finally(() => { if (!cancelled) setLoading(false); });

    return () => { cancelled = true; };
  }, [instrumentId, dateRange.start, dateRange.end, win]); // eslint-disable-line react-hooks/exhaustive-deps

  const rows = data?.rows ?? [];
  const s = data?.stats;

  // For scatter: Δμ* vs price_change_next_5
  const scatterX = rows.slice(0, -5).map(r => r.mu_star_diff);
  const scatterY = rows.slice(5).map((r, i) => r.close - rows[i].close);

  return (
    <div style={{ display: 'flex', height: '100%', background: '#070b10' }}>
      {/* Main chart */}
      <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 16, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.14em', textTransform: 'uppercase' }}>Causal Diff</span>
          {loading && <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>loading</span>}
          {error && <span style={{ ...mono, fontSize: 9, color: '#f85149' }}>{error}</span>}
          <span style={{ ...mono, fontSize: 9, color: '#1e2833', marginLeft: 'auto', marginRight: 12 }}>
            Δε = ε_causal − ε_adj · Δμ* = μ*_adj − μ*_causal (initialization gap, decays to 0 after warmup)
          </span>
        </div>
        <div ref={containerRef} style={{ flex: 1, minHeight: 0 }} />
      </div>

      {/* Right: scatter + stats */}
      <div style={{ width: 260, flexShrink: 0, borderLeft: '1px solid #0e1520', background: '#090d13', display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '8px 12px', borderBottom: '1px solid #0e1520' }}>
          <div style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 6 }}>
            EMA init gap vs price change +5 bars
          </div>
          <ScatterPlot
            xVals={scatterX}
            yVals={scatterY}
            xLabel="Δμ*"
            yLabel="Δclose+5"
          />
          <div style={{ ...mono, fontSize: 8, color: '#1e2833', marginTop: 4, lineHeight: 1.5 }}>
            If r ≈ 0: causal EMA gap does not predict next 5-bar returns.
            If r &gt; 0.3: initialization gap correlates with forward price — investigate further.
          </div>
        </div>

        <div style={{ padding: '8px 12px', flex: 1, overflowY: 'auto' }}>
          <div style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 6 }}>
            Gap statistics
          </div>
          {s ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {([
                ['Δμ* mean', fmt(s.mu_star_diff_mean)],
                ['Δμ* max', fmt(s.mu_star_diff_max)],
                ['n', String(s.n)],
              ] as [string, string][]).map(([label, value]) => (
                <div key={label} style={{ display: 'flex', justifyContent: 'space-between', padding: '2px 0', borderBottom: '1px solid #0a0f16' }}>
                  <span style={{ ...mono, fontSize: 9, color: '#2d3a4a' }}>{label}</span>
                  <span style={{ ...mono, fontSize: 10, color: '#8b99a8' }}>{value}</span>
                </div>
              ))}
              <div style={{ ...mono, fontSize: 8, color: '#1e2833', marginTop: 8, lineHeight: 1.6 }}>
                Δμ* near zero across the full window means the two EMA variants have converged — expected after warmup (~3× span bars).
                Large Δμ* only occurs during the first ~60 bars for EMA-20. Persistent Δμ* indicates a very short series.
              </div>
            </div>
          ) : (
            <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>—</span>
          )}
        </div>
      </div>
    </div>
  );
}
