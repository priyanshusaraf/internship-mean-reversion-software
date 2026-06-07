'use client';

import { PanelGroup, Panel as RPanel } from 'react-resizable-panels';
import { ResizeHandle } from '@/components/layout/ResizeHandle';
import { InstrumentPanel } from '@/components/workspace/InstrumentPanel';
import { ChartWorkspace } from '@/components/workspace/ChartWorkspace';
import { IntervalBar } from '@/components/workspace/IntervalBar';
import { EstimatorPanel } from '@/components/workspace/EstimatorPanel';
import { ResearchSurface } from '@/components/workspace/ResearchSurface';

export default function WorkstationPage() {
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
      <PanelGroup direction="horizontal" autoSaveId="amr-workstation-cols" style={{ flex: 1, minHeight: 0 }}>
        {/* Instruments rail */}
        <RPanel defaultSize={16} minSize={10} maxSize={32}>
          <InstrumentPanel />
        </RPanel>

        <ResizeHandle dir="horizontal" />

        {/* Center + estimator (IntervalBar spans the top of both) */}
        <RPanel defaultSize={84} minSize={50}>
          <div style={{ display: 'flex', flexDirection: 'column', height: '100%', minWidth: 0 }}>
            <IntervalBar />
            <PanelGroup direction="horizontal" autoSaveId="amr-workstation-main" style={{ flex: 1, minHeight: 0 }}>
              {/* Chart over research surface */}
              <RPanel defaultSize={82} minSize={40}>
                <PanelGroup direction="vertical" autoSaveId="amr-workstation-center">
                  <RPanel defaultSize={60} minSize={20}>
                    <div style={{ height: '100%', minHeight: 0, display: 'flex', flexDirection: 'column' }}>
                      <ChartWorkspace />
                    </div>
                  </RPanel>
                  <ResizeHandle dir="vertical" />
                  <RPanel defaultSize={40} minSize={15}>
                    <div style={{ height: '100%', minHeight: 0, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                      <ResearchSurface />
                    </div>
                  </RPanel>
                </PanelGroup>
              </RPanel>

              <ResizeHandle dir="horizontal" />

              {/* Estimators rail */}
              <RPanel defaultSize={18} minSize={10} maxSize={36}>
                <EstimatorPanel />
              </RPanel>
            </PanelGroup>
          </div>
        </RPanel>
      </PanelGroup>
    </div>
  );
}
