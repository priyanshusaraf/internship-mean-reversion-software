'use client';

import { useRef } from 'react';
import { InstrumentPanel } from '@/components/workspace/InstrumentPanel';
import { ChartWorkspace } from '@/components/workspace/ChartWorkspace';
import { IntervalBar } from '@/components/workspace/IntervalBar';
import { EstimatorPanel } from '@/components/workspace/EstimatorPanel';
import { ResearchSurface } from '@/components/workspace/ResearchSurface';
import { useUIStore } from '@/lib/store';

function DragHandle({ onDelta }: { onDelta: (dx: number) => void }) {
  const dragging = useRef(false);
  const lastX = useRef(0);

  function onMouseDown(e: React.MouseEvent) {
    e.preventDefault();
    dragging.current = true;
    lastX.current = e.clientX;

    function onMove(ev: MouseEvent) {
      if (!dragging.current) return;
      onDelta(ev.clientX - lastX.current);
      lastX.current = ev.clientX;
    }
    function onUp() {
      dragging.current = false;
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    }
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onUp);
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
  }

  return (
    <div
      onMouseDown={onMouseDown}
      style={{ width: 5, flexShrink: 0, cursor: 'col-resize', background: 'transparent', transition: 'background 0.12s', zIndex: 10 }}
      onMouseEnter={e => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(56,139,253,0.35)'; }}
      onMouseLeave={e => { (e.currentTarget as HTMLDivElement).style.background = 'transparent'; }}
    />
  );
}

export default function WorkstationPage() {
  const { leftWidth, rightWidth, chartSplit, setUI } = useUIStore();

  return (
    <div
      style={{
        display: 'flex',
        flex: 1,
        minHeight: 0,
        overflow: 'hidden',
        background: '#070b10',
        color: '#c9d1d9',
      }}
    >
      <InstrumentPanel />

      {/* Left drag handle */}
      <DragHandle onDelta={dx => setUI({ leftWidth: Math.max(160, Math.min(380, leftWidth + dx)) })} />

      <div style={{ display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0 }}>
        <IntervalBar />

        <div style={{ display: 'flex', flex: 1, minHeight: 0 }}>
          <div style={{ display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0, minHeight: 0 }}>
            <div style={{ flex: `0 0 ${chartSplit}%`, minHeight: 0, display: 'flex', flexDirection: 'column' }}>
              <ChartWorkspace />
            </div>
            <div style={{ flex: `0 0 ${100 - chartSplit}%`, minHeight: 0, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <ResearchSurface />
            </div>
          </div>

          {/* Right drag handle */}
          <DragHandle onDelta={dx => setUI({ rightWidth: Math.max(120, Math.min(300, rightWidth - dx)) })} />

          <EstimatorPanel />
        </div>
      </div>
    </div>
  );
}
