'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { useWorkstationStore } from '@/lib/store';
import type { ModuleProps } from '../types';
import type { DiagnosticsRow } from '@/lib/types';

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};
function fmt(n: number, d = 2) { return n.toFixed(d); }

interface Event {
  date: string;
  type: string;
  description: string;
  value: string;
  isCausal: boolean;
  severity: 'info' | 'warning' | 'critical';
  source: 'auto' | 'manual';
}

function deriveEvents(rows: DiagnosticsRow[], epsilonStd: number): Event[] {
  const events: Event[] = [];
  const threshold2 = epsilonStd * 2;
  const threshold3 = epsilonStd * 3;

  let aboveZero = false;
  let aboveZeroStart = '';

  for (let i = 1; i < rows.length; i++) {
    const r = rows[i];
    const prev = rows[i - 1];

    // ε spike
    const absEps = Math.abs(r.epsilon);
    if (absEps > threshold3) {
      events.push({ date: r.date, type: 'ε_spike_3σ', description: `|ε| exceeded 3σ`, value: fmt(r.epsilon), isCausal: true, severity: 'critical', source: 'auto' });
    } else if (absEps > threshold2) {
      events.push({ date: r.date, type: 'ε_spike_2σ', description: `|ε| exceeded 2σ`, value: fmt(r.epsilon), isCausal: true, severity: 'warning', source: 'auto' });
    }

    // ε zero crossing
    if (prev.epsilon > 0 && r.epsilon <= 0) {
      if (aboveZero && aboveZeroStart) {
        events.push({ date: r.date, type: 'ε_reversal', description: `ε crossed zero (positive → negative) from ${aboveZeroStart}`, value: fmt(r.epsilon), isCausal: true, severity: 'info', source: 'auto' });
      }
      aboveZero = false;
    } else if (prev.epsilon <= 0 && r.epsilon > 0) {
      aboveZero = true;
      aboveZeroStart = r.date;
      events.push({ date: r.date, type: 'ε_reversal', description: `ε crossed zero (negative → positive)`, value: fmt(r.epsilon), isCausal: true, severity: 'info', source: 'auto' });
    }

    // Look-ahead gap spike
    const gapThresh = Math.abs(r.mu_star_diff);
    if (gapThresh > epsilonStd * 0.5) {
      events.push({ date: r.date, type: 'causal_divergence', description: `Δμ* gap spiked (causal model lagging)`, value: fmt(r.mu_star_diff), isCausal: false, severity: 'warning', source: 'auto' });
    }
  }

  // Deduplicate consecutive same-type events (keep only first + last of each run)
  const deduped: Event[] = [];
  let prev: Event | null = null;
  for (const e of events) {
    if (!prev || prev.type !== e.type || prev.date !== e.date) {
      deduped.push(e);
    }
    prev = e;
  }

  return deduped.sort((a, b) => b.date.localeCompare(a.date));
}

const severityColor = { info: '#3d4d5e', warning: '#d99a3c', critical: '#f85149' };
const severityBg = { info: 'transparent', warning: 'rgba(210,153,60,0.04)', critical: 'rgba(248,81,73,0.04)' };

export function EventLog({ instrumentId, dateRange, window: win }: ModuleProps) {
  const { setDateRange } = useWorkstationStore();
  const [autoEvents, setAutoEvents] = useState<Event[]>([]);
  const [manualEvents, setManualEvents] = useState<Event[]>([]);
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setError(null);
    setAutoEvents([]);
    if (!instrumentId) return;
    let cancelled = false;
    setLoading(true);

    api.getDiagnostics(instrumentId, win, dateRange.start ?? undefined, dateRange.end ?? undefined)
      .then((resp) => {
        if (cancelled) return;
        setAutoEvents(deriveEvents(resp.rows, resp.stats.epsilon_std));
      })
      .catch((e: unknown) => { if (!cancelled) setError(e instanceof Error ? e.message : 'Fetch failed'); })
      .finally(() => { if (!cancelled) setLoading(false); });

    return () => { cancelled = true; };
  }, [instrumentId, dateRange.start, dateRange.end, win]); // eslint-disable-line react-hooks/exhaustive-deps

  function addNote() {
    if (!note.trim()) return;
    const today = dateRange.end ?? new Date().toISOString().split('T')[0];
    setManualEvents(prev => [{
      date: today, type: 'observation', description: note.trim(),
      value: '', isCausal: true, severity: 'info', source: 'manual',
    }, ...prev]);
    setNote('');
  }

  function jumpToDate(date: string) {
    setDateRange({ start: dateRange.start, end: date });
  }

  const allEvents = [...manualEvents, ...autoEvents].sort((a, b) => b.date.localeCompare(a.date));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', background: '#070b10' }}>
      {/* Header */}
      <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 16, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
        <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.14em', textTransform: 'uppercase' }}>Research Event Log</span>
        {loading && <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>loading</span>}
        {error && <span style={{ ...mono, fontSize: 9, color: '#f85149' }}>{error}</span>}
        <span style={{ ...mono, fontSize: 9, color: '#1e2833', marginLeft: 'auto', marginRight: 12 }}>
          {allEvents.length} events
        </span>
      </div>

      {/* Manual annotation input */}
      <div style={{ flexShrink: 0, padding: '8px 12px', borderBottom: '1px solid #0e1520', display: 'flex', gap: 8 }}>
        <input
          style={{
            ...mono, flex: 1, background: '#0d1520', border: '1px solid #1a2230', borderRadius: 3,
            padding: '4px 8px', fontSize: 10, color: '#c9d1d9', outline: 'none',
          }}
          placeholder={`Add observation for ${dateRange.end ?? 'current date'}...`}
          value={note}
          onChange={e => setNote(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && addNote()}
          onFocus={e => { e.target.style.borderColor = '#388bfd'; }}
          onBlur={e => { e.target.style.borderColor = '#1a2230'; }}
        />
        <button
          onClick={addNote}
          disabled={!note.trim()}
          style={{
            ...mono, fontSize: 10, padding: '4px 10px', borderRadius: 3,
            background: note.trim() ? 'rgba(56,139,253,0.09)' : 'transparent',
            border: `1px solid ${note.trim() ? 'rgba(56,139,253,0.3)' : '#161d27'}`,
            color: note.trim() ? '#58a6ff' : '#2d3a4a',
            cursor: note.trim() ? 'pointer' : 'not-allowed',
          }}
        >
          Log
        </button>
      </div>

      {/* Column headers */}
      <div style={{ flexShrink: 0, display: 'flex', paddingLeft: 12, paddingRight: 12, height: 22, alignItems: 'center', borderBottom: '1px solid #0e1520', background: '#06090e' }}>
        {[['date', 80], ['type', 140], ['description', undefined], ['value', 70], ['causal', 50]].map(([label, w]) => (
          <div key={label as string} style={{ ...mono, fontSize: 8, color: '#2d3a4a', letterSpacing: '0.1em', textTransform: 'uppercase', width: w as number | undefined, flex: w ? undefined : 1 }}>
            {label}
          </div>
        ))}
      </div>

      {/* Event rows */}
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {allEvents.length === 0 && (
          <div style={{ padding: '16px 12px' }}>
            <span style={{ ...mono, fontSize: 10, color: '#1e2833' }}>
              {instrumentId ? 'No events detected for this window.' : 'Select an instrument.'}
            </span>
          </div>
        )}
        {allEvents.map((ev, i) => (
          <div
            key={i}
            onClick={() => jumpToDate(ev.date)}
            title="Click to jump to this date"
            style={{
              display: 'flex', alignItems: 'flex-start',
              paddingLeft: 12, paddingRight: 12, paddingTop: 5, paddingBottom: 5,
              borderBottom: '1px solid #0a0f16',
              background: severityBg[ev.severity],
              cursor: 'pointer',
              transition: 'background 0.1s',
            }}
            onMouseEnter={e => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(255,255,255,0.02)'; }}
            onMouseLeave={e => { (e.currentTarget as HTMLDivElement).style.background = severityBg[ev.severity]; }}
          >
            <div style={{ ...mono, fontSize: 9, color: '#3d4d5e', width: 80, flexShrink: 0 }}>{ev.date}</div>
            <div style={{ ...mono, fontSize: 9, color: severityColor[ev.severity], width: 140, flexShrink: 0, letterSpacing: '0.04em' }}>
              {ev.source === 'manual' ? '● ' : ''}{ev.type}
            </div>
            <div style={{ ...mono, fontSize: 9, color: '#8b99a8', flex: 1, lineHeight: 1.4 }}>{ev.description}</div>
            <div style={{ ...mono, fontSize: 9, color: '#3d4d5e', width: 70, flexShrink: 0, textAlign: 'right' }}>{ev.value}</div>
            <div style={{ ...mono, fontSize: 8, color: ev.isCausal ? '#3d4d5e' : '#d99a3c', width: 50, flexShrink: 0, textAlign: 'right' }}>
              {ev.isCausal ? 'causal' : 'full-info'}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
