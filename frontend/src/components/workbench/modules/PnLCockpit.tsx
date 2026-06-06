'use client';

// ── P&L Cockpit — diagnostic module for the FROZEN placeholder backtest engine ──────────────────
//
// CONSTITUTIONAL POSTURE (CLAUDE.md §10, §11.2):
//   This is an EXECUTION/MEASUREMENT readout, NOT a strategy surface. Every number rendered here
//   comes DIRECTLY from the BacktestResult returned by POST /api/v2/backtest/run. No statistic is
//   computed in JS — the only transformations are display formatting (toFixed, fraction→percent,
//   sign→colour). The slippage_note ("slippage=0, placeholder rule, not deployable") is rendered
//   UNCONDITIONALLY in the header bar so the user can never mistake this for a deployable result.
//
// Charting: lightweight-charts (frozen stack §8) — NOT Recharts. Equity = line + zero price-line;
// trade scatter = two marker-only line series (wins green / losses red) sharing the bars-held axis.

import { useEffect, useRef } from 'react';
import {
  createChart, ColorType, CrosshairMode, LineStyle,
  type IChartApi, type ISeriesApi, type Time, type MouseEventParams,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import { useWorkstationStore, useBacktestStore } from '@/lib/store';
import type { ModuleProps } from '../types';
import type { BacktestResult, BacktestTrade, EquityPoint } from '@/lib/types';

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

const GREEN = '#3fb950';
const RED = '#f85149';
const SLIPPAGE_FALLBACK = 'slippage=0, placeholder rule, not deployable';

// ── display-only formatters (NO statistics computed here) ───────────────────────────────────────
const fmt2 = (n: number) => (Number.isFinite(n) ? n.toFixed(2) : '—');
const fmt1 = (n: number) => (Number.isFinite(n) ? n.toFixed(1) : '—');
const pct1 = (frac: number) => (Number.isFinite(frac) ? (frac * 100).toFixed(1) + '%' : '—');
const shortReason = (r: string) => (r === 'Z_CROSS' ? 'Z✓' : r === 'TIME_STOP' ? '⏱' : r);

// ════════════════════════════════════════════════════════════════════════════════════════════════
// Equity curve — single line, colour by final value, dashed zero reference line.
// ════════════════════════════════════════════════════════════════════════════════════════════════
function EquityChart({ data }: { data: EquityPoint[] }) {
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

// ════════════════════════════════════════════════════════════════════════════════════════════════
// Trade-duration scatter — x: entry date · y: bars_held · colour: net_pnl sign (two series).
// Hover tooltip: trade_id · direction · net_pnl · exit_reason.
// ════════════════════════════════════════════════════════════════════════════════════════════════
function TradeScatter({ trades }: { trades: BacktestTrade[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const tipRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const winRef = useRef<ISeriesApi<'Line'> | null>(null);
  const lossRef = useRef<ISeriesApi<'Line'> | null>(null);
  // date → trade lookup (entry dates are unique: one position at a time in the engine)
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
    // each series needs ascending-unique times; trades are already entry-ordered
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

// ════════════════════════════════════════════════════════════════════════════════════════════════
// Metric card
// ════════════════════════════════════════════════════════════════════════════════════════════════
function MetricCard({ label, value, color, loading }: { label: string; value: string; color?: string; loading?: boolean }) {
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

// ════════════════════════════════════════════════════════════════════════════════════════════════
// Trade log table — sticky header, alternating rows, native scroll.
// ════════════════════════════════════════════════════════════════════════════════════════════════
const COLS: { key: string; label: string; w: number }[] = [
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

function TradeLog({ trades }: { trades: BacktestTrade[] }) {
  const cell: React.CSSProperties = { ...mono, fontSize: 9.5, padding: '3px 6px', textAlign: 'right', whiteSpace: 'nowrap' };
  const head: React.CSSProperties = { ...cell, color: '#2d3a4a', letterSpacing: '0.05em', textTransform: 'uppercase', fontSize: 8.5 };
  return (
    <div style={{ flex: 1, minHeight: 0, overflow: 'auto', background: '#070b10' }}>
      <table style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead style={{ position: 'sticky', top: 0, zIndex: 1, background: '#090d13' }}>
          <tr style={{ borderBottom: '1px solid #161d27' }}>
            {COLS.map(c => <th key={c.key} style={{ ...head, width: c.w }}>{c.label}</th>)}
          </tr>
        </thead>
        <tbody>
          {/* trades arrive entry-ordered ascending from the engine (trade_id == entry order) */}
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

// ════════════════════════════════════════════════════════════════════════════════════════════════
// Main module
// ════════════════════════════════════════════════════════════════════════════════════════════════
export function PnLCockpit(_props: ModuleProps) {
  // instrument target comes from the Workstation selection (NOT the prop) — gates the Run button.
  const selectedInstrumentId = useWorkstationStore(s => s.selectedInstrumentId);
  const { start, end, status, result, error, lastRunAt, setStart, setEnd, runStart, runSuccess, runError } = useBacktestStore();

  const loading = status === 'loading';
  const r: BacktestResult | null = result;

  const onRun = async () => {
    if (!selectedInstrumentId) return;
    if (!start || !end) { runError('Set a start and end date'); return; }
    runStart();
    try {
      const res = await api.runBacktest({ instrument_id: selectedInstrumentId, start, end });
      runSuccess(res, new Date().toISOString());
    } catch (e) {
      runError(e instanceof Error ? e.message : 'Backtest failed');
    }
  };

  const strategyLabel = r?.strategy_id ?? 'MR_PLACEHOLDER_V1';
  const modeLabel = r?.verification_watermark ? 'VERIFICATION' : 'RESEARCH';
  const modeColor = r?.verification_watermark ? '#d2993c' : GREEN;
  const slippageNote = r?.slippage_note ?? SLIPPAGE_FALLBACK;
  const lastRunStr = lastRunAt ? new Date(lastRunAt).toLocaleTimeString() : null;

  const dateInput: React.CSSProperties = {
    ...mono, fontSize: 10, width: 92, background: '#0a0f16', color: '#8b99a8',
    border: '1px solid #1c2733', borderRadius: 3, padding: '3px 6px', outline: 'none',
  };
  const pill = (text: string, color: string): React.CSSProperties => ({
    ...mono, fontSize: 9, color, border: `1px solid ${color}55`, background: `${color}14`,
    borderRadius: 999, padding: '2px 8px', letterSpacing: '0.08em',
  });

  // metric values: '—' when no result; skeleton handled by MetricCard via `loading`
  const m = (render: (res: BacktestResult) => { value: string; color?: string }) =>
    r ? render(r) : { value: '—', color: '#2d3a4a' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', background: '#070b10' }}>

      {/* ── ZONE 1 — strategy header bar ─────────────────────────────────────────────────────── */}
      <div style={{
        flexShrink: 0, minHeight: 60, display: 'flex', alignItems: 'center', gap: 14,
        padding: '0 14px', background: '#090d13', borderBottom: '1px solid #0e1520',
      }}>
        <span style={{ ...mono, fontSize: 12, color: '#c9d1d9', letterSpacing: '0.04em' }}>{strategyLabel}</span>
        <span style={pill(modeLabel, modeColor)}>{modeLabel}</span>
        <span style={{ ...mono, fontSize: 9, color: '#3d4d5e' }}>
          {r ? `${r.start} → ${r.end}` : '— → —'}
        </span>

        {/* RIGOR: slippage note — unconditionally visible, no toggle, no hover */}
        <span style={{ ...mono, fontSize: 9, color: '#d2993c', marginLeft: 6 }}>⚠ {slippageNote}</span>

        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 8 }}>
          <input type="text" placeholder="start (ISO)" value={start} onChange={e => setStart(e.target.value.trim())} style={dateInput} />
          <span style={{ ...mono, fontSize: 10, color: '#2d3a4a' }}>→</span>
          <input type="text" placeholder="end (ISO)" value={end} onChange={e => setEnd(e.target.value.trim())} style={dateInput} />

          {lastRunStr && <span style={{ ...mono, fontSize: 9, color: '#2d3a4a' }}>Last run: {lastRunStr}</span>}

          {selectedInstrumentId ? (
            <button onClick={onRun} disabled={loading} style={{
              ...mono, fontSize: 10, color: loading ? '#3d4d5e' : '#070b10',
              background: loading ? '#161d27' : '#58a6ff', border: 'none', borderRadius: 3,
              padding: '5px 12px', cursor: loading ? 'default' : 'pointer', fontWeight: 600,
              display: 'flex', alignItems: 'center', gap: 6,
            }}>
              {loading && <span style={{
                width: 9, height: 9, border: '1.5px solid #3d4d5e', borderTopColor: '#8b99a8',
                borderRadius: '50%', display: 'inline-block', animation: 'pnl-spin 0.7s linear infinite',
              }} />}
              {loading ? 'Running' : 'Run Backtest'}
            </button>
          ) : (
            <>
              <button disabled style={{
                ...mono, fontSize: 10, color: '#3d4d5e', background: '#161d27', border: 'none',
                borderRadius: 3, padding: '5px 12px', cursor: 'default',
              }}>Run Backtest</button>
              <span style={{ ...mono, fontSize: 9, color: '#2d3a4a' }}>Load an instrument first</span>
            </>
          )}
        </div>
      </div>

      {/* error banner — below the header bar */}
      {status === 'error' && error && (
        <div style={{
          flexShrink: 0, padding: '6px 14px', background: '#2d0f0f', borderBottom: '1px solid #5a1a1a',
          ...mono, fontSize: 10, color: RED,
        }}>✕ {error}</div>
      )}

      {/* ── ZONE 2 — metrics row ─────────────────────────────────────────────────────────────── */}
      <div style={{ flexShrink: 0, height: 100, display: 'flex', borderBottom: '1px solid #0e1520' }}>
        <MetricCard label="Win rate" loading={loading} {...m(res => ({ value: pct1(res.win_rate) }))} />
        <MetricCard label="Total P&L" loading={loading} {...m(res => ({ value: fmt2(res.total_net_pnl), color: res.total_net_pnl < 0 ? RED : '#c9d1d9' }))} />
        <MetricCard label="Sharpe" loading={loading} {...m(res => ({ value: fmt2(res.sharpe_ratio) }))} />
        <MetricCard label="Max drawdown" loading={loading} {...m(res => ({ value: fmt2(res.max_drawdown), color: RED }))} />
        <MetricCard label="Avg hold" loading={loading} {...m(res => ({ value: `${fmt1(res.avg_bars_held)} bars` }))} />
        <MetricCard label="Trades" loading={loading} {...m(res => ({ value: String(res.n_trades) }))} />
      </div>

      {/* ── ZONE 3 — charts + trade log ──────────────────────────────────────────────────────── */}
      <div style={{ flex: 1, minHeight: 0, display: 'flex' }}>
        {r ? (
          <>
            {/* LEFT 60% — two stacked charts */}
            <div style={{ flex: '0 0 60%', minWidth: 0, display: 'flex', flexDirection: 'column', borderRight: '1px solid #0e1520' }}>
              <div style={{ flex: '0 0 55%', minHeight: 0, display: 'flex', flexDirection: 'column' }}>
                <div style={{ flexShrink: 0, padding: '5px 12px', background: '#090d13', borderBottom: '1px solid #0e1520' }}>
                  <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.08em' }}>Equity curve (cumulative net P&L)</span>
                </div>
                <EquityChart data={r.equity_curve} />
              </div>
              <div style={{ flex: '0 0 45%', minHeight: 0, display: 'flex', flexDirection: 'column', borderTop: '1px solid #0e1520' }}>
                <div style={{ flexShrink: 0, padding: '5px 12px', background: '#06090e', borderBottom: '1px solid #0a0f16' }}>
                  <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.08em' }}>Trade duration vs entry date</span>
                </div>
                <TradeScatter trades={r.trades} />
              </div>
            </div>

            {/* RIGHT 40% — trade log */}
            <div style={{ flex: '0 0 40%', minWidth: 0, display: 'flex', flexDirection: 'column' }}>
              <div style={{ flexShrink: 0, padding: '5px 12px', background: '#090d13', borderBottom: '1px solid #0e1520' }}>
                <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.08em' }}>Trade log · {r.n_trades}</span>
              </div>
              <TradeLog trades={r.trades} />
            </div>
          </>
        ) : (
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            {loading ? (
              <span style={{
                width: 22, height: 22, border: '2px solid #161d27', borderTopColor: '#58a6ff',
                borderRadius: '50%', display: 'inline-block', animation: 'pnl-spin 0.7s linear infinite',
              }} />
            ) : (
              <span style={{ ...mono, fontSize: 11, color: '#2d3a4a' }}>
                {selectedInstrumentId ? 'Run a backtest to see results' : 'Load an instrument first'}
              </span>
            )}
          </div>
        )}
      </div>

      <style>{`@keyframes pnl-spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
