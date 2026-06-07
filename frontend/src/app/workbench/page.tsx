'use client';

import { PanelGroup, Panel as RPanel } from 'react-resizable-panels';
import { ResizeHandle } from '@/components/layout/ResizeHandle';
import { useWorkstationStore } from '@/lib/store';
import { ContextBar } from '@/components/workbench/ContextBar';
import { ModuleNav } from '@/components/workbench/ModuleNav';
import { ResearchControls } from '@/components/workbench/ResearchControls';
import { TimelineRail } from '@/components/workbench/TimelineRail';
import { WORKBENCH_MODULES } from '@/components/workbench/registry';

export default function WorkbenchPage() {
  const { selectedInstrumentId, dateRange, estimatorWindow, activeWorkbenchModule } = useWorkstationStore();

  const activeModule = WORKBENCH_MODULES.find(m => m.id === activeWorkbenchModule)
    ?? WORKBENCH_MODULES[0];

  const moduleProps = {
    instrumentId: selectedInstrumentId ?? '',
    dateRange,
    estimator: 'ema',
    window: estimatorWindow,
  };

  return (
    <div style={{
      display: 'flex', flexDirection: 'column', flex: 1, minHeight: 0,
      background: '#070b10', color: '#c9d1d9', overflow: 'hidden',
    }}>
      {/* Context bar — always visible, shows current research context */}
      <ContextBar />

      {/* Main area: nav + module viewport + controls — drag dividers to resize */}
      <PanelGroup direction="horizontal" autoSaveId="amr-workbench-cols" style={{ flex: 1, minHeight: 0 }}>
        <RPanel defaultSize={12} minSize={6} maxSize={24}>
          <ModuleNav />
        </RPanel>

        <ResizeHandle dir="horizontal" />

        {/* Module viewport */}
        <RPanel defaultSize={75} minSize={40}>
          <div style={{ height: '100%', minWidth: 0, minHeight: 0, display: 'flex', flexDirection: 'column' }}>
            {selectedInstrumentId ? (
              <activeModule.component {...moduleProps} />
            ) : (
              <div style={{
                flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 8,
              }}>
                <span style={{ fontSize: 11, color: 'var(--amr-text-dim)', fontFamily: 'ui-monospace,monospace' }}>
                  No instrument selected
                </span>
                <span style={{ fontSize: 10, color: '#1e2833', fontFamily: 'ui-monospace,monospace' }}>
                  Load and select an instrument on the Workstation page first
                </span>
              </div>
            )}
          </div>
        </RPanel>

        <ResizeHandle dir="horizontal" />

        <RPanel defaultSize={13} minSize={8} maxSize={28}>
          <ResearchControls />
        </RPanel>
      </PanelGroup>

      {/* Timeline rail — the replay cursor */}
      <TimelineRail />
    </div>
  );
}
