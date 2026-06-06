'use client';

// ── Quadrant 2 — Timeline Scrubber (the control centre of the Trade Cockpit) ──────────────────────
//
// Pure HTML/CSS drag interaction (mousedown → document mousemove → document mouseup). No slider lib.
// The track maps LINEARLY to the full date range (index 0..n-1). Two draggable handles set the
// window start/end; min window = 60 bars (handles cannot cross within 60 indices).
//
// RIGOR (QA check a): the store (useBacktestStore start/end) and the habitat backend call are
// committed ONLY on handle RELEASE (mouseup) — never on a drag tick. During a drag we mutate ONLY
// local visual state. A single one-time init commit (no habitat) seeds the window on load.

import { useEffect, useRef, useState, useCallback } from 'react';
import { C, mono } from '@/components/observatory/ui';

const MIN_WINDOW = 60; // bars

interface Props {
  dates: string[];                 // full ascending date range of the loaded instrument
  disabled: boolean;
  // released=false → init/seed (set store only); released=true → set store AND fetch habitat.
  onCommit: (start: string, end: string, released: boolean) => void;
}

export function TimelineScrubber({ dates, disabled, onCommit }: Props) {
  const trackRef = useRef<HTMLDivElement>(null);
  const n = dates.length;
  const maxIdx = Math.max(0, n - 1);

  const [i0, setI0] = useState(0);
  const [i1, setI1] = useState(maxIdx);
  const dragging = useRef<'left' | 'right' | null>(null);
  // live indices ref so document listeners read current values without re-subscribing
  const idx = useRef({ i0: 0, i1: maxIdx });
  idx.current = { i0, i1 };

  const onCommitRef = useRef(onCommit);
  onCommitRef.current = onCommit;

  // (re)seed to the full range only when the instrument's date RANGE actually changes — keyed on a
  // value signature (first|last|count), NOT array identity. In dev StrictMode the page's OHLC effect
  // double-fetches, yielding a fresh `dates` array with identical values; without this guard that
  // new identity would re-fire the seed and silently wipe a window the user just dragged.
  const sig = n >= 2 ? `${dates[0]}|${dates[maxIdx]}|${n}` : '';
  const lastSig = useRef('');
  useEffect(() => {
    if (n < 2 || lastSig.current === sig) return;
    lastSig.current = sig;
    setI0(0);
    setI1(maxIdx);
    idx.current = { i0: 0, i1: maxIdx };
    onCommitRef.current(dates[0], dates[maxIdx], false);
  }, [sig, n, maxIdx, dates]);

  const idxFromClientX = useCallback((clientX: number): number => {
    const rect = trackRef.current?.getBoundingClientRect();
    if (!rect || rect.width === 0) return 0;
    const frac = (clientX - rect.left) / rect.width;
    return Math.max(0, Math.min(maxIdx, Math.round(frac * maxIdx)));
  }, [maxIdx]);

  const startDrag = useCallback((handle: 'left' | 'right') => (e: React.MouseEvent) => {
    if (disabled || n < MIN_WINDOW) return;
    e.preventDefault();
    dragging.current = handle;
    document.body.style.userSelect = 'none';

    const onMove = (ev: MouseEvent) => {
      if (!dragging.current) return;
      const raw = idxFromClientX(ev.clientX);
      if (dragging.current === 'left') {
        const next = Math.min(raw, idx.current.i1 - MIN_WINDOW);
        setI0(Math.max(0, next));
      } else {
        const next = Math.max(raw, idx.current.i0 + MIN_WINDOW);
        setI1(Math.min(maxIdx, next));
      }
    };
    const onUp = () => {
      dragging.current = null;
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
      document.body.style.userSelect = '';
      // COMMIT on release only: store window + habitat fetch (released=true).
      const { i0: a, i1: b } = idx.current;
      onCommitRef.current(dates[a], dates[b], true);
    };
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onUp);
  }, [disabled, n, maxIdx, idxFromClientX, dates]);

  if (disabled || n < 2) {
    return (
      <div style={wrap}>
        <div style={{ ...mono, fontSize: 11, color: C.textDim }}>
          {n < 2 ? 'Loading date axis…' : 'Select an instrument to enable the scrubber'}
        </div>
      </div>
    );
  }

  const leftPct = (i0 / maxIdx) * 100;
  const rightPct = (i1 / maxIdx) * 100;
  const tooShort = n < MIN_WINDOW;

  return (
    <div style={wrap}>
      <div style={{ ...mono, fontSize: 9, letterSpacing: '0.12em', textTransform: 'uppercase', color: C.textDim, marginBottom: 4 }}>
        window scrubber · {i1 - i0} bars selected {tooShort && <span style={{ color: C.danger }}>· need ≥ {MIN_WINDOW}</span>}
      </div>

      {/* track */}
      <div style={{ position: 'relative', padding: '18px 10px 0' }}>
        <div ref={trackRef} style={{ position: 'relative', height: 8, borderRadius: 4, background: '#0d1520', border: `1px solid ${C.border}` }}>
          {/* selected fill */}
          <div style={{
            position: 'absolute', top: 0, bottom: 0, left: `${leftPct}%`, width: `${rightPct - leftPct}%`,
            background: 'rgba(56,139,253,0.22)', borderRadius: 4,
          }} />
          {/* left handle */}
          <Handle pct={leftPct} color={C.text} onMouseDown={startDrag('left')} label="start" />
          {/* right handle */}
          <Handle pct={rightPct} color={C.accent} onMouseDown={startDrag('right')} label="end" />
        </div>
      </div>

      {/* date labels: full-min (left) · selected start · selected end · full-max (right) */}
      <div style={{ position: 'relative', marginTop: 10, height: 28 }}>
        <span style={{ ...labelStyle, left: 0, color: C.textDim }}>{dates[0]}</span>
        <span style={{ ...labelStyle, right: 0, textAlign: 'right', color: C.textDim }}>{dates[maxIdx]}</span>
        <span style={{ ...labelStyle, left: `${leftPct}%`, transform: 'translateX(-50%)', color: C.text }}>
          ◀ {dates[i0]}
        </span>
        <span style={{ ...labelStyle, left: `${rightPct}%`, transform: 'translateX(-50%)', color: C.accent }}>
          {dates[i1]} ▶
        </span>
      </div>
    </div>
  );
}

function Handle({ pct, color, onMouseDown, label }: { pct: number; color: string; onMouseDown: (e: React.MouseEvent) => void; label: string }) {
  return (
    <div
      role="slider"
      aria-label={label}
      aria-valuetext={label}
      onMouseDown={onMouseDown}
      title={label}
      style={{
        position: 'absolute', top: '50%', left: `${pct}%`,
        transform: 'translate(-50%, -50%)',
        width: 12, height: 22, borderRadius: 4,
        background: '#0d1520', border: `1.5px solid ${color}`,
        cursor: 'ew-resize', zIndex: 2,
        boxShadow: '0 1px 4px rgba(0,0,0,0.5)',
      }}
    />
  );
}

const wrap: React.CSSProperties = {
  display: 'flex', flexDirection: 'column', justifyContent: 'center',
  height: '100%', padding: '0 20px', background: C.bg,
};

const labelStyle: React.CSSProperties = {
  ...mono, position: 'absolute', top: 0, fontSize: 10, whiteSpace: 'nowrap',
};
