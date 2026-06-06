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

import { api } from '@/lib/api';
import { useWorkstationStore, useBacktestStore } from '@/lib/store';
import type { ModuleProps } from '../types';
import type { BacktestResult } from '@/lib/types';
// Shared render primitives — extracted to PnLShared.tsx so the Trade Cockpit (/backtest) and this
// Workbench module render identical cards / equity curve / trade log with NO duplicated logic.
import {
  mono, GREEN, RED, SLIPPAGE_FALLBACK, fmt2, fmt1, pct1,
  MetricCard, EquityChart, TradeScatter, TradeLog,
} from '@/components/backtest/PnLShared';

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
