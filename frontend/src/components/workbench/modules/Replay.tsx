'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import {
  createChart, ColorType, CrosshairMode,
  type IChartApi, type ISeriesApi, type Time,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import { centeredMA } from '@/lib/smoothers';
import type { ModuleProps } from '../types';
import type { DiagnosticsResponse } from '@/lib/types';

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

function fmt(n: number | null | undefined, d = 2) {
  return n == null || !Number.isFinite(n) ? '—' : n.toFixed(d);
}

function Toggle({ on, onClick, label, color }: { on: boolean; onClick: () => void; label: string; color: string }) {
  return (
    <button
      onClick={onClick}
      style={{
        ...mono, fontSize: 9, padding: '2px 8px', borderRadius: 3, letterSpacing: '0.06em',
        background: on ? 'rgba(255,255,255,0.04)' : 'transparent',
        border: `1px solid ${on ? color : '#161d27'}`,
        color: on ? color : '#2d3a4a', cursor: 'pointer',
      }}
    >
      {label}
    </button>
  );
}

export function Replay({ instrumentId, dateRange, window: win }: ModuleProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const priceRef = useRef<ISeriesApi<'Line'> | null>(null);
  const emaRef = useRef<ISeriesApi<'Line'> | null>(null);
  const kalmanRef = useRef<ISeriesApi<'Line'> | null>(null);
  const hindsightRef = useRef<ISeriesApi<'Line'> | null>(null);

  const [data, setData] = useState<DiagnosticsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cursor, setCursor] = useState(0);
  const [showKalman, setShowKalman] = useState(false);
  const [showHindsight, setShowHindsight] = useState(false);

  // Init chart (once)
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
    priceRef.current = chart.addLineSeries({ color: 'rgba(200,210,220,0.3)', lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 'price' });
    emaRef.current = chart.addLineSeries({ color: 'rgba(88,166,255,0.9)', lineWidth: 1, lastValueVisible: true, priceLineVisible: false, title: 'μ* causal (EMA)' });
    kalmanRef.current = chart.addLineSeries({ color: 'rgba(86,211,160,0.85)', lineWidth: 1, lastValueVisible: true, priceLineVisible: false, title: 'μ* causal (Kalman)' });
    hindsightRef.current = chart.addLineSeries({ color: 'rgba(210,153,60,0.85)', lineWidth: 1, lineStyle: 2, lastValueVisible: true, priceLineVisible: false, title: 'hindsight (not knowable at t)' });
    chartRef.current = chart;
    const ro = new ResizeObserver(() => containerRef.current && chart.applyOptions({ width: containerRef.current.clientWidth, height: containerRef.current.clientHeight }));
    ro.observe(containerRef.current);
    return () => { ro.disconnect(); chart.remove(); chartRef.current = null; };
  }, []);

  // Fetch once per (instrument, window, range). Causal series computed by backend;
  // prefix invariance (frozen) means rows[0..t] == what was knowable at t.
  useEffect(() => {
    setError(null);
    if (!instrumentId) return;
    let cancelled = false;
    setLoading(true);
    api.getDiagnostics(instrumentId, win, dateRange.start ?? undefined, dateRange.end ?? undefined)
      .then((resp) => {
        if (cancelled) return;
        setData(resp);
        setCursor(resp.rows.length - 1); // default: full history revealed; scrub left to rewind
      })
      .catch((e: unknown) => { if (!cancelled) setError(e instanceof Error ? e.message : 'Fetch failed'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [instrumentId, dateRange.start, dateRange.end, win]);

  // Hindsight track — computed over the FULL fetched price series (uses future bars by design).
  const hindsight = useMemo(() => {
    if (!data) return [] as number[];
    const k = Math.max(1, Math.floor(win / 2));
    return centeredMA(data.rows.map(r => r.close), k);
  }, [data, win]);

  // Reveal prefix [0..cursor]. Mask everything after t. Re-fit so the chart renders
  // exactly as it would have appeared at bar t.
  useEffect(() => {
    if (!data) return;
    const rows = data.rows;
    const end = Math.min(cursor + 1, rows.length);
    const toTime = (d: string) => d as Time;
    priceRef.current?.setData(rows.slice(0, end).map(r => ({ time: toTime(r.date), value: r.close })));
    emaRef.current?.setData(rows.slice(0, end).map(r => ({ time: toTime(r.date), value: r.mu_star })));
    kalmanRef.current?.setData(showKalman ? rows.slice(0, end).map(r => ({ time: toTime(r.date), value: r.mu_star_kalman })) : []);
    hindsightRef.current?.setData(
      showHindsight
        ? rows.slice(0, end).map((r, i) => ({ time: toTime(r.date), value: hindsight[i] })).filter(p => Number.isFinite(p.value))
        : []
    );
    chartRef.current?.timeScale().fitContent();
  }, [data, cursor, showKalman, showHindsight, hindsight]);

  const rows = data?.rows ?? [];
  const maxIdx = Math.max(0, rows.length - 1);
  const at = rows[Math.min(cursor, maxIdx)];
  const lag = at && showHindsight && Number.isFinite(hindsight[cursor]) ? at.mu_star - hindsight[cursor] : null;

  const step = (d: -1 | 1) => setCursor(c => Math.max(0, Math.min(maxIdx, c + d)));

  return (
    <div style={{ display: 'flex', height: '100%', background: '#070b10' }}>
      {/* Chart + controls */}
      <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 12, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.14em', textTransform: 'uppercase' }}>Replay</span>
          {loading && <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>loading</span>}
          {error && <span style={{ ...mono, fontSize: 9, color: '#f85149' }}>{error}</span>}
          <div style={{ display: 'flex', gap: 6, marginLeft: 'auto', marginRight: 12, alignItems: 'center' }}>
            <Toggle on={showKalman} onClick={() => setShowKalman(v => !v)} label="KALMAN μ*" color="rgba(86,211,160,0.9)" />
            <Toggle on={showHindsight} onClick={() => setShowHindsight(v => !v)} label="HINDSIGHT" color="rgba(210,153,60,0.95)" />
          </div>
        </div>

        {/* Chart */}
        <div ref={containerRef} style={{ flex: 1, minHeight: 0 }} />

        {/* Hindsight warning strip (only when on) */}
        {showHindsight && (
          <div style={{ height: 16, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, background: '#13100a', borderTop: '1px solid #2a2110' }}>
            <span style={{ ...mono, fontSize: 8, color: 'rgba(210,153,60,0.75)', letterSpacing: '0.08em' }}>
              ⚠ HINDSIGHT (amber, dashed) is a centered smoother — it USES FUTURE BARS and was NOT knowable at t. Shown only to expose causal lag.
            </span>
          </div>
        )}

        {/* Replay transport */}
        <div style={{ height: 40, flexShrink: 0, display: 'flex', alignItems: 'center', gap: 10, paddingLeft: 12, paddingRight: 12, background: '#060a0f', borderTop: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.12em', textTransform: 'uppercase', width: 44, flexShrink: 0 }}>Replay</span>
          <button onClick={() => setCursor(0)} disabled={!rows.length} title="Jump to first bar" style={transportBtn(!!rows.length)}>⟮</button>
          <button onClick={() => step(-1)} disabled={!rows.length} title="Step back one bar" style={transportBtn(!!rows.length)}>‹</button>
          <input
            type="range" min={0} max={maxIdx} value={Math.min(cursor, maxIdx)} disabled={!rows.length}
            onChange={(e) => setCursor(Number(e.target.value))}
            style={{ flex: 1, accentColor: '#58a6ff', cursor: rows.length ? 'pointer' : 'not-allowed' }}
          />
          <button onClick={() => step(1)} disabled={!rows.length} title="Step forward one bar" style={transportBtn(!!rows.length)}>›</button>
          <button onClick={() => setCursor(maxIdx)} disabled={!rows.length} title="Jump to last bar" style={transportBtn(!!rows.length)}>⟯</button>
          <span style={{ ...mono, fontSize: 9, color: '#3d4d5e', flexShrink: 0, width: 150, textAlign: 'right' }}>
            {at ? `${at.date} · bar ${cursor + 1}/${rows.length}` : '—'}
          </span>
        </div>
      </div>

      {/* As-of-t readout (single bar at cursor — not whole-window stats) */}
      <div style={{ width: 168, flexShrink: 0, borderLeft: '1px solid #0e1520', background: '#090d13', padding: '10px 12px', display: 'flex', flexDirection: 'column', gap: 2 }}>
        <div style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 6 }}>As of t</div>
        <Row label="date" value={at?.date ?? '—'} />
        <Row label="close" value={fmt(at?.close)} />
        <Row label="μ* causal" value={fmt(at?.mu_star)} color="rgba(88,166,255,0.9)" />
        {showKalman && <Row label="μ* kalman" value={fmt(at?.mu_star_kalman)} color="rgba(86,211,160,0.9)" />}
        {showHindsight && <Row label="hindsight" value={fmt(hindsight[cursor])} color="rgba(210,153,60,0.95)" />}
        {showHindsight && <Row label="μ* lag" value={fmt(lag)} color="rgba(210,153,60,0.7)" />}
        <div style={{ ...mono, fontSize: 8, color: '#1e2833', marginTop: 10, lineHeight: 1.6 }}>
          Scrub to replay equilibrium formation under the causal firewall: at bar t only data ≤ t is shown.
          {showHindsight && ' μ* lag = causal − hindsight; large |lag| = the causal estimator trailing where price actually was.'}
        </div>
      </div>
    </div>
  );
}

function transportBtn(enabled: boolean): React.CSSProperties {
  return {
    ...mono, fontSize: 12, background: 'none', border: '1px solid #161d27', borderRadius: 3,
    color: enabled ? '#3d4d5e' : '#1e2833', cursor: enabled ? 'pointer' : 'not-allowed',
    width: 26, height: 24, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
  };
}

function Row({ label, value, color }: { label: string; value: string; color?: string }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '3px 0', borderBottom: '1px solid #0a0f16' }}>
      <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.06em' }}>{label}</span>
      <span style={{ ...mono, fontSize: 10, color: color ?? '#8b99a8' }}>{value}</span>
    </div>
  );
}
