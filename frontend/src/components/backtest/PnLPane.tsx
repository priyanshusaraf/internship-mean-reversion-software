'use client';

// ── Quadrant 3 — P&L panel ────────────────────────────────────────────────────────────────────
//
// Reuses the EXACT metric cards / equity curve / trade log from PnLShared.tsx (same primitives the
// Workbench P&L Cockpit uses — no duplicated rendering). Every number comes straight from the
// BacktestResult in useBacktestStore. The slippage note is rendered UNCONDITIONALLY (QA check c).
// The Run action is owned by the page (so Space and the button share one path) and passed in.

import { useBacktestStore } from '@/lib/store';
import { C, mono } from '@/components/observatory/ui';
import {
  RED, fmt1, fmt2, pct1,
  MetricCard, EquityChart, TradeLog,
} from './PnLShared';
import type { BacktestResult } from '@/lib/types';

const SLIPPAGE_NOTE = 'slippage=0 · placeholder rule · not deployable';

interface Props {
  onRun: () => void;
  canRun: boolean;          // instrument selected AND window ≥ 60 bars
}

export function PnLPane({ onRun, canRun }: Props) {
  const { status, result, error } = useBacktestStore();
  const loading = status === 'loading';
  const r: BacktestResult | null = result;

  const m = (render: (res: BacktestResult) => { value: string; color?: string }) =>
    r ? render(r) : { value: '—', color: '#2d3a4a' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', background: C.bg, minHeight: 0 }}>

      {/* ── metric cards — 3×2 grid (~35%) ── */}
      <div style={{ flex: '0 0 35%', minHeight: 0, display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gridTemplateRows: 'repeat(2,1fr)', borderBottom: `1px solid ${C.borderSoft}` }}>
        <MetricCard label="Win rate" loading={loading} {...m(res => ({ value: pct1(res.win_rate) }))} />
        <MetricCard label="Total P&L" loading={loading} {...m(res => ({ value: fmt2(res.total_net_pnl), color: res.total_net_pnl < 0 ? RED : '#c9d1d9' }))} />
        <MetricCard label="Sharpe" loading={loading} {...m(res => ({ value: fmt2(res.sharpe_ratio) }))} />
        <MetricCard label="Max DD" loading={loading} {...m(res => ({ value: fmt2(res.max_drawdown), color: RED }))} />
        <MetricCard label="Avg hold" loading={loading} {...m(res => ({ value: `${fmt1(res.avg_bars_held)} bars` }))} />
        <MetricCard label="Trades" loading={loading} {...m(res => ({ value: String(res.n_trades) }))} />
      </div>

      {/* ── play button + slippage note ── */}
      <div style={{ flexShrink: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4, padding: '8px 0 6px', borderBottom: `1px solid ${C.borderSoft}` }}>
        <button
          data-testid="run-backtest"
          onClick={onRun}
          disabled={!canRun || loading}
          style={{
            ...mono, fontSize: 12, fontWeight: 600,
            color: !canRun || loading ? C.textDim : '#070b10',
            background: !canRun || loading ? '#161d27' : C.accent,
            border: 'none', borderRadius: 4, padding: '6px 20px',
            cursor: !canRun || loading ? 'default' : 'pointer',
            display: 'flex', alignItems: 'center', gap: 8,
          }}
        >
          {loading && <span style={{ width: 10, height: 10, border: '1.5px solid #3d4d5e', borderTopColor: '#8b99a8', borderRadius: '50%', display: 'inline-block', animation: 'cockpit-spin 0.7s linear infinite' }} />}
          {loading ? 'Running…' : '▶ Run Backtest'}
        </button>
        {/* RIGOR (QA check c): slippage note ALWAYS visible, no interaction required */}
        <span style={{ ...mono, fontSize: 9, color: C.warn }}>{SLIPPAGE_NOTE}</span>
        {status === 'error' && error && (
          <span style={{ ...mono, fontSize: 10, color: RED }}>✕ {error}</span>
        )}
      </div>

      {/* ── equity curve (~40%) ── */}
      <div style={{ flex: '0 0 40%', minHeight: 0, display: 'flex', flexDirection: 'column' }}>
        <div style={{ flexShrink: 0, padding: '4px 10px', background: C.bgPanel, borderBottom: `1px solid ${C.borderSoft}` }}>
          <span style={{ ...mono, fontSize: 9, color: C.textDim, letterSpacing: '0.08em' }}>equity curve · cumulative net P&L</span>
        </div>
        {r ? (
          <EquityChart data={r.equity_curve} />
        ) : (
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            {loading
              ? <span style={{ width: 20, height: 20, border: `2px solid ${C.border}`, borderTopColor: C.accent, borderRadius: '50%', display: 'inline-block', animation: 'cockpit-spin 0.7s linear infinite' }} />
              : <span style={{ ...mono, fontSize: 11, color: C.textDim }}>Select a window and press ▶ to run</span>}
          </div>
        )}
      </div>

      {/* ── compact trade log (~25%) — smaller font, scroll within (max ~8 rows) ── */}
      <div style={{ flex: '0 0 25%', minHeight: 0, display: 'flex', flexDirection: 'column', borderTop: `1px solid ${C.borderSoft}` }}>
        <div style={{ flexShrink: 0, padding: '4px 10px', background: C.bgPanel, borderBottom: `1px solid ${C.borderSoft}` }}>
          <span style={{ ...mono, fontSize: 9, color: C.textDim, letterSpacing: '0.08em' }}>trade log{r ? ` · ${r.n_trades}` : ''}</span>
        </div>
        {r && r.trades.length
          ? <TradeLog trades={r.trades} fontSize={8.5} />
          : <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', ...mono, fontSize: 10, color: C.textDim }}>{r ? 'no trades in window' : '—'}</div>}
      </div>
    </div>
  );
}
