'use client';

import { useWorkstationStore } from '@/lib/store';

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

function Chip({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
      <span style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase' }}>{label}</span>
      <span style={{ ...mono, fontSize: 10, color: 'var(--amr-text)' }}>{value}</span>
    </div>
  );
}

const SEP = <div style={{ width: 1, height: 10, background: '#161d27', flexShrink: 0 }} />;

export function ContextBar() {
  const { selectedInstrumentId, dateRange, estimatorWindow, estimatorMode, instruments } = useWorkstationStore();
  const inst = instruments.find(i => i.instrument_id === selectedInstrumentId);

  return (
    <div style={{
      height: 30, flexShrink: 0,
      display: 'flex', alignItems: 'center',
      paddingLeft: 12, paddingRight: 12, gap: 12,
      background: '#090d13',
      borderBottom: '1px solid #161d27',
    }}>
      <Chip label="instrument" value={inst?.display_name ?? '—'} />
      {SEP}
      <Chip label="estimator" value={`EMA-${estimatorWindow}`} />
      {SEP}
      <Chip label="mode" value={estimatorMode === 'causal' ? 'causal' : 'full-info'} />
      {SEP}
      <Chip label="from" value={dateRange.start ?? inst?.start_date ?? '—'} />
      <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>→</span>
      <Chip label="to" value={dateRange.end ?? inst?.end_date ?? '—'} />

      {inst && (
        <>
          {SEP}
          <Chip label="bars" value={inst.row_count.toLocaleString()} />
        </>
      )}

      {!selectedInstrumentId && (
        <span style={{ ...mono, fontSize: 9, color: '#1e2833', marginLeft: 8 }}>
          Select an instrument on the Workstation to begin
        </span>
      )}
    </div>
  );
}
