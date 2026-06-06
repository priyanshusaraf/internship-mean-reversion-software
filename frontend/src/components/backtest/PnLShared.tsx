'use client';

// ── Shared P&L render primitives ────────────────────────────────────────────────────────────────
//
// Extracted VERBATIM from PnLCockpit.tsx so the Trade Cockpit (/backtest, PnLPane) and the Workbench
// P&L Cockpit module render IDENTICAL metric cards / equity curve / trade log without duplicated
// logic. NO statistic is computed here — every number comes from a BacktestResult; the only
// transformations are display formatting (toFixed, fraction→percent, sign→colour) and binning for
// charts. Charting: lightweight-charts (frozen stack §8).

import { useEffect, useRef } from 'react';
import {
  createChart, ColorType, CrosshairMode, LineStyle,
  type IChartApi, type ISeriesApi, type Time, type MouseEventParams, type SeriesMarker,
} from 'lightweight-charts';
import type { BacktestTrade, EquityPoint } from '@/lib/types';

export const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

export const GREEN = '#3fb950';
export const RED = '#f85149';
export const SLIPPAGE_FALLBACK = 'slippage=0, placeholder rule, not deployable';

// ── display-only formatters (NO statistics computed here) ─────────────────────────────────────────
export const fmt2 = (n: number) => (Number.isFinite(n) ? n.toFixed(2) : '—');
export const fmt1 = (n: number) => (Number.isFinite(n) ? n.toFixed(1) : '—');
export const pct1 = (frac: number) => (Number.isFinite(frac) ? (frac * 100).toFixed(1) + '%' : '—');
export const shortReason = (r: string) => (r === 'Z_CROSS' ? 'Z✓' : r === 'TIME_STOP' ? '⏱' : r);

// ══════════════════════════════════════════════════════════════════════════════════════════════════
// Equity curve — single line, colour by final value, dashed zero reference line.
// ══════════════════════════════════════════════════════════════════════════════════════════════════
export function EquityChart({ data }: { data: EquityPoint[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Line'> | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, {
      layout: { background: { type: ColorType.Solid, color: '#070b10' }, textColor: '#3d4d5e', fontSize: 9 },
      grid: { vertLines: { color: '#0e1520' }, horzLines: { color: '#0e1520' } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: '#161d27' },
      timeScale: { borderColor: '#161d27' },
      width: ref.current.clientWidth,
      height: ref.current.clientHeight,
    });
    const series = chart.addLineSeries({ lineWidth: 1, lastValueVisible: true, priceLineVisible: false });
    series.createPriceLine({
      price: 0, color: '#3d4d5e', lineWidth: 1, lineStyle: LineStyle.Dashed,
      axisLabelVisible: false, title: '',
    });
    chartRef.current = chart;
    seriesRef.current = series;
    const ro = new ResizeObserver(() =>
      ref.current && chart.applyOptions({ width: ref.current.clientWidth, height: ref.current.clientHeight }));
    ro.observe(ref.current);
    return () => { ro.disconnect(); chart.remove(); chartRef.current = null; seriesRef.current = null; };
  }, []);

  useEffect(() => {
    if (!seriesRef.current) return;
    const final = data.length ? data[data.length - 1].cumulative_pnl : 0;
    seriesRef.current.applyOptions({ color: final >= 0 ? GREEN : RED });
    seriesRef.current.setData(data.map(p => ({ time: p.date as Time, value: p.cumulative_pnl })));
    chartRef.current?.timeScale().fitContent();
  }, [data]);

  return <div ref={ref} style={{ flex: 1, minHeight: 0 }} />;
}

// ══════════════════════════════════════════════════════════════════════════════════════════════════
// Enhanced equity curve — first VISUAL test of habitat regime-discrimination.
//
//   LAYER 1  habitat background band  — a single full-area div tinted by the WINDOW score.
//            The score is a SINGLE SCALAR for the whole window (HabitatResult has no per-bar
//            series), so the band is one flat colour — NOT a per-bar gradient. No interpolation,
//            no invented per-bar score. Tint thresholds are display-only colour mapping.
//   LAYER 2  equity curve line        — identical init to EquityChart (chart bg made transparent
//            so the band shows through; the relative host carries the dark base colour).
//   LAYER 3  trade entry markers      — setMarkers(), colour straight from trade.net_pnl sign.
//
// RIGOR: nothing here is a statistic. `score` is rendered verbatim from the store; marker colour
// is the sign of net_pnl from the BacktestResult. The "single-window score ≠ edge" disclaimer is
// rendered unconditionally below the chart in PnLPane (and the in-chip note here is permanent).
// ══════════════════════════════════════════════════════════════════════════════════════════════════

// display-only colour mapping for a habitat score (NO statistic — a threshold→colour lookup)
export function habitatTint(score: number | null): { band: string; text: string; tag: 'GREEN' | 'AMBER' | 'RED' | null } {
  if (score == null || !Number.isFinite(score)) return { band: 'transparent', text: '#6b7787', tag: null };
  if (score >= 60) return { band: 'rgba(63, 185, 80, 0.08)', text: GREEN, tag: 'GREEN' };
  if (score >= 40) return { band: 'rgba(186, 117, 23, 0.08)', text: '#d2993c', tag: 'AMBER' };
  return { band: 'rgba(248, 81, 73, 0.08)', text: RED, tag: 'RED' };
}

export function EnhancedEquityChart({
  data, trades, habitatScore, habitatStatus,
}: {
  data: EquityPoint[];
  trades: BacktestTrade[];
  habitatScore: number | null;
  habitatStatus: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Line'> | null>(null);

  // ── chart init — copied from EquityChart, only the background is made transparent so the
  //    habitat band (a sibling div behind the canvas) is visible through it. ──
  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, {
      layout: { background: { type: ColorType.Solid, color: 'rgba(0,0,0,0)' }, textColor: '#3d4d5e', fontSize: 9 },
      grid: { vertLines: { color: '#0e1520' }, horzLines: { color: '#0e1520' } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: '#161d27' },
      timeScale: { borderColor: '#161d27' },
      width: ref.current.clientWidth,
      height: ref.current.clientHeight,
    });
    const series = chart.addLineSeries({ lineWidth: 1, lastValueVisible: true, priceLineVisible: false });
    series.createPriceLine({
      price: 0, color: '#3d4d5e', lineWidth: 1, lineStyle: LineStyle.Dashed,
      axisLabelVisible: false, title: '',
    });
    chartRef.current = chart;
    seriesRef.current = series;
    const ro = new ResizeObserver(() =>
      ref.current && chart.applyOptions({ width: ref.current.clientWidth, height: ref.current.clientHeight }));
    ro.observe(ref.current);
    return () => { ro.disconnect(); chart.remove(); chartRef.current = null; seriesRef.current = null; };
  }, []);

  // LAYER 2 — equity line (identical logic to EquityChart)
  useEffect(() => {
    if (!seriesRef.current) return;
    const final = data.length ? data[data.length - 1].cumulative_pnl : 0;
    seriesRef.current.applyOptions({ color: final >= 0 ? GREEN : RED });
    seriesRef.current.setData(data.map(p => ({ time: p.date as Time, value: p.cumulative_pnl })));
    chartRef.current?.timeScale().fitContent();
  }, [data]);

  // LAYER 3 — trade entry markers (colour = sign of net_pnl, taken directly; sorted ascending)
  useEffect(() => {
    if (!seriesRef.current) return;
    const markers: SeriesMarker<Time>[] = [...trades]
      .sort((a, b) => (a.entry_bar < b.entry_bar ? -1 : a.entry_bar > b.entry_bar ? 1 : 0))
      .map(t => ({
        time: t.entry_bar as Time,
        position: 'inBar' as const,
        shape: 'circle' as const,
        size: 1,
        color: t.net_pnl > 0 ? GREEN : t.net_pnl < 0 ? RED : '#8b949e',
        text: '',
      }));
    seriesRef.current.setMarkers(markers);
  }, [trades]);

  const tint = habitatTint(habitatScore);
  const cornerLabel =
    habitatScore != null && Number.isFinite(habitatScore) ? `MR habitat: ${Math.round(habitatScore)}`
    : habitatStatus === 'loading' ? 'habitat: scoring…'
    : 'habitat: not scored';
  const cornerColor = habitatScore != null && Number.isFinite(habitatScore) ? tint.text : '#6b7787';

  return (
    <div style={{ position: 'relative', flex: 1, minHeight: 0, background: '#070b10' }}>
      {/* LAYER 1 — habitat background band (behind the transparent chart canvas) */}
      <div style={{
        position: 'absolute', inset: 0, zIndex: 1, pointerEvents: 'none',
        background: tint.band, transition: 'background 0.2s ease',
      }}>
        <span style={{ ...mono, position: 'absolute', top: 4, right: 8, fontSize: 9, color: cornerColor }}>
          {cornerLabel}
        </span>
      </div>
      {/* LAYER 2/3 — chart canvas (transparent bg) sits above the band */}
      <div ref={ref} style={{ position: 'absolute', inset: 0, zIndex: 2 }} />
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════════════════════════
// Trade-duration scatter — x: entry date · y: bars_held · colour: net_pnl sign (two series).
// ══════════════════════════════════════════════════════════════════════════════════════════════════
export function TradeScatter({ trades }: { trades: BacktestTrade[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const tipRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const winRef = useRef<ISeriesApi<'Line'> | null>(null);
  const lossRef = useRef<ISeriesApi<'Line'> | null>(null);
  const byDate = useRef<Map<string, BacktestTrade>>(new Map());

  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, {
      layout: { background: { type: ColorType.Solid, color: '#06090e' }, textColor: '#3d4d5e', fontSize: 9 },
      grid: { vertLines: { color: '#0c1118' }, horzLines: { color: '#0c1118' } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: '#161d27' },
      timeScale: { borderColor: '#161d27' },
      width: ref.current.clientWidth,
      height: ref.current.clientHeight,
    });
    const markerOpts = { lineVisible: false, pointMarkersVisible: true, pointMarkersRadius: 3, lastValueVisible: false, priceLineVisible: false, crosshairMarkerVisible: false } as const;
    winRef.current = chart.addLineSeries({ ...markerOpts, color: GREEN });
    lossRef.current = chart.addLineSeries({ ...markerOpts, color: RED });
    chartRef.current = chart;

    chart.subscribeCrosshairMove((param: MouseEventParams) => {
      const tip = tipRef.current;
      if (!tip) return;
      const t = param.time as string | undefined;
      const tr = t ? byDate.current.get(t) : undefined;
      if (!tr || !param.point) { tip.style.display = 'none'; return; }
      tip.style.display = 'block';
      tip.style.left = `${param.point.x + 12}px`;
      tip.style.top = `${param.point.y + 12}px`;
      tip.innerHTML =
        `<span style="color:#8b99a8">#${tr.trade_id}</span> ` +
        `<span style="color:${tr.direction === 'LONG' ? GREEN : '#d2993c'}">${tr.direction}</span><br/>` +
        `net <span style="color:${tr.net_pnl >= 0 ? GREEN : RED}">${fmt2(tr.net_pnl)}</span><br/>` +
        `<span style="color:#2d3a4a">${tr.exit_reason}</span>`;
    });

    const ro = new ResizeObserver(() =>
      ref.current && chart.applyOptions({ width: ref.current.clientWidth, height: ref.current.clientHeight }));
    ro.observe(ref.current);
    return () => { ro.disconnect(); chart.remove(); chartRef.current = null; winRef.current = null; lossRef.current = null; };
  }, []);

  useEffect(() => {
    if (!winRef.current || !lossRef.current) return;
    const map = new Map<string, BacktestTrade>();
    trades.forEach(t => map.set(t.entry_bar, t));
    byDate.current = map;
    const wins = trades.filter(t => t.net_pnl >= 0).map(t => ({ time: t.entry_bar as Time, value: t.bars_held }));
    const losses = trades.filter(t => t.net_pnl < 0).map(t => ({ time: t.entry_bar as Time, value: t.bars_held }));
    winRef.current.setData(wins);
    lossRef.current.setData(losses);
    chartRef.current?.timeScale().fitContent();
  }, [trades]);

  return (
    <div style={{ position: 'relative', flex: 1, minHeight: 0 }}>
      <div ref={ref} style={{ position: 'absolute', inset: 0 }} />
      <div ref={tipRef} style={{
        ...mono, display: 'none', position: 'absolute', zIndex: 5, pointerEvents: 'none',
        background: '#0d1420', border: '1px solid #1c2733', borderRadius: 3, padding: '4px 7px',
        fontSize: 9, lineHeight: 1.5, color: '#8b99a8', whiteSpace: 'nowrap',
      }} />
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════════════════════════
// Metric card
// ══════════════════════════════════════════════════════════════════════════════════════════════════
export function MetricCard({ label, value, color, loading }: { label: string; value: string; color?: string; loading?: boolean }) {
  return (
    <div style={{
      flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 6,
      padding: '0 14px', borderRight: '1px solid #0e1520',
    }}>
      <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.1em', textTransform: 'uppercase' }}>{label}</span>
      {loading
        ? <div style={{ height: 18, width: '60%', background: '#0e1520', borderRadius: 2 }} />
        : <span style={{ ...mono, fontSize: 19, color: color ?? '#c9d1d9' }}>{value}</span>}
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════════════════════════
// Trade log table — sticky header, alternating rows, native scroll.
// ══════════════════════════════════════════════════════════════════════════════════════════════════
export const COLS: { key: string; label: string; w: number }[] = [
  { key: 'id', label: '#', w: 38 },
  { key: 'dir', label: 'Dir', w: 32 },
  { key: 'entry', label: 'Entry', w: 78 },
  { key: 'exit', label: 'Exit', w: 78 },
  { key: 'bars', label: 'Bars', w: 40 },
  { key: 'zin', label: 'z-in', w: 44 },
  { key: 'zout', label: 'z-out', w: 44 },
  { key: 'reason', label: 'Reason', w: 50 },
  { key: 'net', label: 'Net P&L', w: 64 },
];

export function TradeLog({ trades, fontSize = 9.5 }: { trades: BacktestTrade[]; fontSize?: number }) {
  const cell: React.CSSProperties = { ...mono, fontSize, padding: '3px 6px', textAlign: 'right', whiteSpace: 'nowrap' };
  const head: React.CSSProperties = { ...cell, color: '#2d3a4a', letterSpacing: '0.05em', textTransform: 'uppercase', fontSize: fontSize - 1 };
  return (
    <div style={{ flex: 1, minHeight: 0, overflow: 'auto', background: '#070b10' }}>
      <table style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead style={{ position: 'sticky', top: 0, zIndex: 1, background: '#090d13' }}>
          <tr style={{ borderBottom: '1px solid #161d27' }}>
            {COLS.map(c => <th key={c.key} style={{ ...head, width: c.w }}>{c.label}</th>)}
          </tr>
        </thead>
        <tbody>
          {trades.map((t, i) => (
            <tr key={t.trade_id} style={{ background: i % 2 ? '#080c12' : 'transparent' }}>
              <td style={{ ...cell, color: '#3d4d5e' }}>{t.trade_id}</td>
              <td style={{ ...cell, color: t.direction === 'LONG' ? GREEN : '#d2993c' }}>{t.direction === 'LONG' ? 'L' : 'S'}</td>
              <td style={{ ...cell, color: '#8b99a8' }}>{t.entry_bar}</td>
              <td style={{ ...cell, color: '#8b99a8' }}>{t.exit_bar}</td>
              <td style={{ ...cell, color: '#8b99a8' }}>{t.bars_held}</td>
              <td style={{ ...cell, color: '#8b99a8' }}>{fmt2(t.entry_z)}</td>
              <td style={{ ...cell, color: '#8b99a8' }}>{fmt2(t.exit_z)}</td>
              <td style={{ ...cell, color: '#6b7787' }}>{shortReason(t.exit_reason)}</td>
              <td style={{ ...cell, color: t.net_pnl >= 0 ? GREEN : RED }}>{fmt2(t.net_pnl)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
