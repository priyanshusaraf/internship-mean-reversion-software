'use client';

// Compact instrument selector + pin toggle, shared by Backtest / Workbench / Observatory.
//
// Sync model (spec §5): the Workstation is the canonical picker. Each other view shows
//   effective = pinned[view] ?? selectedInstrumentId
// • dropdown when UNPINNED → selectInstrument (global): propagates to every other unpinned view.
// • dropdown when PINNED   → pinView (local only): changes just this view, global untouched.
// • pin toggle: pin captures the current effective; unpin rejoins the global sync.

import Link from 'next/link';
import { useWorkstationStore, type SyncView } from '@/lib/store';
import { C, mono } from '@/components/observatory/ui';

export function effectiveInstrument(view: SyncView): string | null {
  const { pinned, selectedInstrumentId } = useWorkstationStore.getState();
  return pinned[view] ?? selectedInstrumentId;
}

export function InstrumentSyncBar({ view }: { view: SyncView }) {
  const { instruments, selectedInstrumentId, selectInstrument, pinned, pinView, unpinView } = useWorkstationStore();
  const isPinned = pinned[view] != null;
  const effective = pinned[view] ?? selectedInstrumentId;
  const noInstruments = instruments.length === 0;

  const onSelect = (id: string) => {
    if (!id) return;
    if (isPinned) pinView(view, id);
    else selectInstrument(id);
  };
  const togglePin = () => {
    if (isPinned) unpinView(view);
    else if (effective) pinView(view, effective);
  };

  if (noInstruments) {
    return (
      <span style={{ ...mono, fontSize: 11, color: C.textDim }}>
        No instruments — <Link href="/" style={{ color: C.accent, textDecoration: 'none' }}>load on the Workstation</Link>
      </span>
    );
  }

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <div style={{ position: 'relative' }}>
        <select
          data-testid="instrument-select"
          value={effective ?? ''}
          onChange={(e) => onSelect(e.target.value)}
          style={{
            ...mono, fontSize: 12, background: C.bgRaised, color: C.textBright,
            border: `1px solid ${C.border}`, borderRadius: 3, padding: '4px 26px 4px 10px',
            outline: 'none', cursor: 'pointer', appearance: 'none', WebkitAppearance: 'none', minWidth: 150,
          }}
        >
          <option value="">— select —</option>
          {instruments.map((i) => (
            <option key={i.instrument_id} value={i.instrument_id}>{i.instrument_id}</option>
          ))}
        </select>
        <span style={{ position: 'absolute', right: 9, top: '50%', transform: 'translateY(-50%)', color: C.textDim, fontSize: 8, pointerEvents: 'none' }}>▾</span>
      </div>

      <button
        onClick={togglePin}
        disabled={!effective}
        title={isPinned ? 'Pinned — this view ignores global changes. Click to re-sync.' : 'Pin this view to hold its instrument while others sync.'}
        style={{
          ...mono, fontSize: 9, padding: '3px 8px', cursor: effective ? 'pointer' : 'default',
          background: isPinned ? C.accentBg : 'transparent',
          border: `1px solid ${isPinned ? C.accentBorder : C.border}`,
          borderRadius: 3, color: isPinned ? C.accent : C.textDim,
          display: 'flex', alignItems: 'center', gap: 4, letterSpacing: '0.04em',
        }}
      >
        {isPinned ? '📌 pinned' : '⇄ synced'}
      </button>
    </div>
  );
}
