'use client';

import { useWorkstationStore } from '@/lib/store';

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

export function TimelineRail() {
  const { selectedInstrumentId, instruments, dateRange, setDateRange } = useWorkstationStore();
  const inst = instruments.find(i => i.instrument_id === selectedInstrumentId);

  const absStart = inst?.start_date ?? '';
  const absEnd = inst?.end_date ?? '';

  const rangeStart = dateRange.start ?? absStart;
  const rangeEnd = dateRange.end ?? absEnd;

  function handleStartChange(e: React.ChangeEvent<HTMLInputElement>) {
    const v = e.target.value;
    if (!v) { setDateRange({ start: null, end: rangeEnd || null }); return; }
    setDateRange({ start: v, end: rangeEnd || null });
  }

  function handleEndChange(e: React.ChangeEvent<HTMLInputElement>) {
    const v = e.target.value;
    if (!v) { setDateRange({ start: rangeStart || null, end: null }); return; }
    setDateRange({ start: rangeStart || null, end: v });
  }

  function stepEnd(direction: -1 | 1) {
    if (!absStart || !absEnd || !inst) return;
    const dates = getDatesInRange(absStart, absEnd);
    const currentEnd = rangeEnd || absEnd;
    const idx = dates.findIndex(d => d >= currentEnd);
    const nextIdx = Math.max(0, Math.min(dates.length - 1, idx + direction));
    setDateRange({ start: rangeStart || null, end: dates[nextIdx] });
  }

  function resetToAll() {
    if (!inst) return;
    setDateRange({ start: inst.start_date, end: inst.end_date });
  }

  const hasInstrument = !!selectedInstrumentId && !!inst;

  return (
    <div style={{
      height: 44, flexShrink: 0,
      background: '#060a0f',
      borderTop: '1px solid #0e1520',
      display: 'flex', alignItems: 'center',
      paddingLeft: 12, paddingRight: 12, gap: 10,
    }}>
      <span style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.12em', textTransform: 'uppercase', width: 56, flexShrink: 0 }}>
        Timeline
      </span>

      {/* Bar-by-bar step buttons */}
      <button
        onClick={() => stepEnd(-1)}
        disabled={!hasInstrument}
        title="Step backward one bar"
        style={{
          ...mono, fontSize: 12, background: 'none', border: '1px solid #161d27', borderRadius: 3,
          color: hasInstrument ? '#3d4d5e' : '#1e2833', cursor: hasInstrument ? 'pointer' : 'not-allowed',
          width: 24, height: 24, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
        }}
      >
        ‹
      </button>

      {/* Date range inputs */}
      <input
        type="date"
        value={rangeStart}
        min={absStart}
        max={rangeEnd || absEnd}
        onChange={handleStartChange}
        disabled={!hasInstrument}
        style={{
          ...mono, background: '#0d1520', border: '1px solid #1a2230', borderRadius: 3,
          padding: '3px 7px', fontSize: 10, color: hasInstrument ? '#7a8898' : '#1e2833',
          outline: 'none', flexShrink: 0,
        }}
      />
      <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>—</span>
      <input
        type="date"
        value={rangeEnd}
        min={rangeStart || absStart}
        max={absEnd}
        onChange={handleEndChange}
        disabled={!hasInstrument}
        style={{
          ...mono, background: '#0d1520', border: '1px solid #1a2230', borderRadius: 3,
          padding: '3px 7px', fontSize: 10, color: hasInstrument ? '#58a6ff' : '#1e2833',
          outline: 'none', flexShrink: 0,
        }}
      />

      <button
        onClick={() => stepEnd(1)}
        disabled={!hasInstrument}
        title="Step forward one bar"
        style={{
          ...mono, fontSize: 12, background: 'none', border: '1px solid #161d27', borderRadius: 3,
          color: hasInstrument ? '#3d4d5e' : '#1e2833', cursor: hasInstrument ? 'pointer' : 'not-allowed',
          width: 24, height: 24, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
        }}
      >
        ›
      </button>

      {/* ALL shortcut */}
      <button
        onClick={resetToAll}
        disabled={!hasInstrument}
        style={{
          ...mono, fontSize: 9, padding: '2px 7px', borderRadius: 3,
          background: 'transparent', border: '1px solid #161d27',
          color: hasInstrument ? '#2d3a4a' : '#1e2833',
          cursor: hasInstrument ? 'pointer' : 'not-allowed', letterSpacing: '0.04em',
        }}
      >
        ALL
      </button>

      {inst && (
        <span style={{ ...mono, fontSize: 9, color: '#1e2833', marginLeft: 'auto' }}>
          {inst.start_date} – {inst.end_date} · {inst.row_count.toLocaleString()} bars
        </span>
      )}

      {!hasInstrument && (
        <span style={{ ...mono, fontSize: 9, color: '#1e2833', marginLeft: 'auto' }}>
          No instrument selected
        </span>
      )}
    </div>
  );
}

// Approximate date list for bar-stepping (calendar days, not trading days)
function getDatesInRange(start: string, end: string): string[] {
  const result: string[] = [];
  const cur = new Date(start);
  const last = new Date(end);
  while (cur <= last) {
    result.push(cur.toISOString().split('T')[0]);
    cur.setDate(cur.getDate() + 1);
  }
  return result;
}
