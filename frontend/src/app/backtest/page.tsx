'use client';

// ── Trade Cockpit (/backtest) — full-screen four-quadrant cockpit ─────────────────────────────────
//
//   ┌─────────────────────── instrument bar ───────────────────────┐
//   │ Q1 PricePane  (55% × 62%)   │  Q3 PnLPane      (45% × 62%)    │
//   │ Q2 Scrubber   (55% × 38%)   │  Q4 HabitatPane  (45% × 38%)    │
//
// The scrubber (Q2) is the control centre: on handle RELEASE it commits the window to
// useBacktestStore AND fetches the habitat score (Q4). It NEVER writes the store or hits the
// backend during a drag tick. Play (Q3) / Space run the FROZEN placeholder backtest.
//
// State is SHARED, not new: useWorkstationStore (instruments, selectedInstrumentId) +
// useBacktestStore (window, backtest result, habitat slice). No new store.

import { useEffect, useMemo, useState, useCallback } from 'react';
import Link from 'next/link';
import { PanelGroup, Panel as RPanel } from 'react-resizable-panels';
import { ResizeHandle } from '@/components/layout/ResizeHandle';
import { api } from '@/lib/api';
import { useWorkstationStore, useBacktestStore } from '@/lib/store';
import { C, mono } from '@/components/observatory/ui';
import { PricePane } from '@/components/backtest/PricePane';
import { TimelineScrubber } from '@/components/backtest/TimelineScrubber';
import { PnLPane } from '@/components/backtest/PnLPane';
import { HabitatPane } from '@/components/backtest/HabitatPane';
import type { OHLCVBar } from '@/lib/types';

const MIN_BARS = 60;

export default function BacktestPage() {
  const { instruments, selectedInstrumentId, selectInstrument, setInstruments } = useWorkstationStore();
  const {
    start, end, setStart, setEnd,
    runStart, runSuccess, runError, status,
    setHabitatStatus, setHabitatResult, setHabitatError,
  } = useBacktestStore();

  const [bars, setBars] = useState<OHLCVBar[]>([]);
  const [ohlcLoading, setOhlcLoading] = useState(false);

  // populate the dropdown even on direct navigation (store persists only the id, not the list)
  useEffect(() => {
    api.listInstruments().then(setInstruments).catch(() => {});
  }, [setInstruments]);

  // full-range OHLC for the selected instrument (candles + scrubber date axis)
  useEffect(() => {
    if (!selectedInstrumentId) { setBars([]); return; }
    let cancelled = false;
    setOhlcLoading(true);
    api.getOHLCV(selectedInstrumentId)
      .then(r => { if (!cancelled) setBars(r.bars); })
      .catch(() => { if (!cancelled) setBars([]); })
      .finally(() => { if (!cancelled) setOhlcLoading(false); });
    return () => { cancelled = true; };
  }, [selectedInstrumentId]);

  const dates = useMemo(() => bars.map(b => b.time), [bars]);
  const dateIdx = useMemo(() => {
    const m = new Map<string, number>();
    dates.forEach((d, i) => m.set(d, i));
    return m;
  }, [dates]);

  const windowBars = (start && end && dateIdx.has(start) && dateIdx.has(end))
    ? (dateIdx.get(end)! - dateIdx.get(start)! + 1) : 0;
  const canRun = !!selectedInstrumentId && windowBars >= MIN_BARS && status !== 'loading';

  // ── habitat score (Q4) — as_of MUST equal the window END (never a future date) ──
  const scoreHabitat = useCallback(async (s: string, e: string) => {
    if (!selectedInstrumentId) return;
    setHabitatStatus('loading');
    try {
      const res = await api.getHabitatScore({
        dataset_id: selectedInstrumentId,
        window: { start: s, end: e },
        as_of: e,                          // firewall: as_of = window end
        deseason: false,
        params: { vr_qs: [2, 5, 10, 20], ns_null: 200, seed: 42 },
      });
      setHabitatResult(res);
    } catch (err) {
      setHabitatError(err instanceof Error ? err.message : 'habitat scoring failed');
    }
  }, [selectedInstrumentId, setHabitatStatus, setHabitatResult, setHabitatError]);

  // scrubber commit: always update the store window; fetch habitat ONLY on release.
  const onCommit = useCallback((s: string, e: string, released: boolean) => {
    setStart(s);
    setEnd(e);
    if (released) void scoreHabitat(s, e);
  }, [setStart, setEnd, scoreHabitat]);

  // ── run the frozen placeholder backtest (Play button AND Space share this) ──
  const runBacktest = useCallback(async () => {
    if (!canRun || !selectedInstrumentId) return;   // QA (d): gated on instrument + ≥60 bars
    runStart();
    try {
      const res = await api.runBacktest({
        instrument_id: selectedInstrumentId,
        start, end,
        strategy_id: 'MR_PLACEHOLDER_V1',
        mode: 'research',
      });
      runSuccess(res, new Date().toISOString());
    } catch (err) {
      runError(err instanceof Error ? err.message : 'Backtest failed');
    }
  }, [canRun, selectedInstrumentId, start, end, runStart, runSuccess, runError]);

  // ── Space → run (ignored when focus is in a text input / select) ──
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.code !== 'Space' && e.key !== ' ') return;
      const t = e.target as HTMLElement | null;
      const tag = t?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || t?.isContentEditable) return;
      e.preventDefault();
      void runBacktest();   // runBacktest self-gates on canRun
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [runBacktest]);

  const noInstruments = instruments.length === 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', flex: 1, minHeight: 0, overflow: 'hidden', background: C.bg, color: '#c9d1d9' }}>

      {/* ── instrument bar ── */}
      <div style={{ height: 44, flexShrink: 0, display: 'flex', alignItems: 'center', gap: 12, padding: '0 14px', background: C.bgPanel, borderBottom: `1px solid ${C.border}` }}>
        <span style={{ ...mono, fontSize: 10, color: C.textDim, letterSpacing: '0.1em', textTransform: 'uppercase' }}>Instrument</span>
        {noInstruments ? (
          <span style={{ ...mono, fontSize: 11, color: C.textDim }}>
            No instruments loaded — <Link href="/" style={{ color: C.accent, textDecoration: 'none' }}>go to Workstation first</Link>
          </span>
        ) : (
          <div style={{ position: 'relative' }}>
            <select
              data-testid="instrument-select"
              value={selectedInstrumentId ?? ''}
              onChange={e => e.target.value && selectInstrument(e.target.value)}
              style={{
                ...mono, fontSize: 12, background: C.bgRaised, color: '#c9d1d9',
                border: `1px solid ${C.border}`, borderRadius: 3, padding: '4px 26px 4px 10px',
                outline: 'none', cursor: 'pointer', appearance: 'none', WebkitAppearance: 'none', minWidth: 160,
              }}
            >
              <option value="">— select —</option>
              {instruments.map(i => (
                <option key={i.instrument_id} value={i.instrument_id}>{i.instrument_id}</option>
              ))}
            </select>
            <span style={{ position: 'absolute', right: 9, top: '50%', transform: 'translateY(-50%)', color: C.textDim, fontSize: 8, pointerEvents: 'none' }}>▾</span>
          </div>
        )}
        {selectedInstrumentId && (
          <span style={{ ...mono, fontSize: 9, color: C.textDim }}>
            {windowBars > 0 ? `${windowBars} bars in window` : 'drag the scrubber to set a window'} · press Space to run
          </span>
        )}
      </div>

      {/* ── four quadrants — drag any divider to resize; sizes persist per group ── */}
      <PanelGroup direction="horizontal" autoSaveId="amr-backtest-cols" style={{ flex: 1, minHeight: 0 }}>
        <RPanel defaultSize={55} minSize={25}>
          <PanelGroup direction="vertical" autoSaveId="amr-backtest-left">
            <RPanel defaultSize={62} minSize={20}>
              <div style={{ height: '100%', minHeight: 0, borderRight: `1px solid ${C.border}` }}>
                <PricePane instrumentId={selectedInstrumentId} bars={bars} loading={ohlcLoading} start={start || null} end={end || null} />
              </div>
            </RPanel>
            <ResizeHandle dir="vertical" />
            <RPanel defaultSize={38} minSize={15}>
              <div style={{ height: '100%', minHeight: 0, borderRight: `1px solid ${C.border}`, borderTop: `1px solid ${C.border}` }}>
                <TimelineScrubber dates={dates} disabled={!selectedInstrumentId || ohlcLoading} onCommit={onCommit} />
              </div>
            </RPanel>
          </PanelGroup>
        </RPanel>
        <ResizeHandle dir="horizontal" />
        <RPanel defaultSize={45} minSize={25}>
          <PanelGroup direction="vertical" autoSaveId="amr-backtest-right">
            <RPanel defaultSize={62} minSize={20}>
              <div style={{ height: '100%', minHeight: 0 }}>
                <PnLPane onRun={runBacktest} canRun={canRun} />
              </div>
            </RPanel>
            <ResizeHandle dir="vertical" />
            <RPanel defaultSize={38} minSize={15}>
              <div style={{ height: '100%', minHeight: 0, borderTop: `1px solid ${C.border}` }}>
                <HabitatPane />
              </div>
            </RPanel>
          </PanelGroup>
        </RPanel>
      </PanelGroup>

      <style>{`@keyframes cockpit-spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
