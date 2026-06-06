'use client';

import { useWorkstationStore } from '@/lib/store';

const PRESETS = [
  { label: '1M', months: 1 },
  { label: '3M', months: 3 },
  { label: '6M', months: 6 },
  { label: '1Y', months: 12 },
  { label: '2Y', months: 24 },
  { label: 'ALL', months: null },
] as const;

function subtractMonths(dateStr: string, months: number): string {
  const [y, m, d] = dateStr.split('-').map(Number);
  let targetMonth = m - months;
  let targetYear = y;
  while (targetMonth <= 0) {
    targetMonth += 12;
    targetYear -= 1;
  }
  const lastDay = new Date(targetYear, targetMonth, 0).getDate();
  const targetDay = Math.min(d, lastDay);
  return `${targetYear}-${String(targetMonth).padStart(2, '0')}-${String(targetDay).padStart(2, '0')}`;
}

const inputStyle: React.CSSProperties = {
  background: '#0d1520',
  border: '1px solid #1a2230',
  borderRadius: 3,
  padding: '3px 7px',
  fontSize: 10,
  color: '#7a8898',
  outline: 'none',
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

export function IntervalBar() {
  const { instruments, selectedInstrumentId, dateRange, setDateRange } =
    useWorkstationStore();

  const selected = instruments.find((i) => i.instrument_id === selectedInstrumentId);

  function applyPreset(months: number | null) {
    if (!selected) return;
    if (months === null) {
      setDateRange({ start: selected.start_date, end: selected.end_date });
    } else {
      setDateRange({
        start: subtractMonths(selected.end_date, months),
        end: selected.end_date,
      });
    }
  }

  return (
    <div
      className="flex items-center shrink-0"
      style={{
        height: 36,
        paddingLeft: 12,
        paddingRight: 12,
        background: '#090d13',
        borderBottom: '1px solid #161d27',
        gap: 10,
      }}
    >
      {/* Preset buttons */}
      <div style={{ display: 'flex', gap: 2 }}>
        {PRESETS.map((p) => (
          <button
            key={p.label}
            onClick={() => applyPreset(p.months)}
            disabled={!selected}
            className="font-data"
            style={{
              padding: '2px 7px',
              fontSize: 10,
              fontWeight: 600,
              color: selected ? '#3a4a5c' : '#1e2630',
              background: 'transparent',
              border: '1px solid transparent',
              borderRadius: 3,
              cursor: selected ? 'pointer' : 'not-allowed',
              letterSpacing: '0.04em',
              transition: 'all 0.12s',
            }}
            onMouseEnter={(e) => {
              if (selected) {
                const btn = e.currentTarget;
                btn.style.color = '#8b99a8';
                btn.style.borderColor = '#1e2630';
                btn.style.background = 'rgba(255,255,255,0.02)';
              }
            }}
            onMouseLeave={(e) => {
              const btn = e.currentTarget;
              btn.style.color = selected ? '#3a4a5c' : '#1e2630';
              btn.style.borderColor = 'transparent';
              btn.style.background = 'transparent';
            }}
          >
            {p.label}
          </button>
        ))}
      </div>

      {/* Divider */}
      <div style={{ width: 1, height: 14, background: '#161d27', flexShrink: 0 }} />

      {/* Spacer */}
      <div style={{ flex: 1 }} />

      {/* Date range inputs */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        <input
          type="date"
          value={dateRange.start ?? ''}
          onChange={(e) => setDateRange({ ...dateRange, start: e.target.value || null })}
          style={inputStyle}
          onFocus={(e) => { e.target.style.borderColor = '#388bfd'; e.target.style.color = '#c9d1d9'; }}
          onBlur={(e) => { e.target.style.borderColor = '#1a2230'; e.target.style.color = '#7a8898'; }}
        />
        <span style={{ color: '#1e2630', fontSize: 10, userSelect: 'none' }}>—</span>
        <input
          type="date"
          value={dateRange.end ?? ''}
          onChange={(e) => setDateRange({ ...dateRange, end: e.target.value || null })}
          style={inputStyle}
          onFocus={(e) => { e.target.style.borderColor = '#388bfd'; e.target.style.color = '#c9d1d9'; }}
          onBlur={(e) => { e.target.style.borderColor = '#1a2230'; e.target.style.color = '#7a8898'; }}
        />
      </div>
    </div>
  );
}
