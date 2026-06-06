'use client';

/**
 * Observatory v2 — vertical slice (contract §10).
 *   ingest + column-map + quality → price chart + draggable as-of cursor → causal μ* + z
 *   → window-selected, surrogate-relative habitat score with its cloud + raw/deseason toggle.
 *
 * Thin client: every number comes from /api/v2. No statistic computed in JS (M5).
 * Additive & isolated: NEW route; does not touch /workbench or src/lib/api.ts.
 */
import { useState } from 'react';
import {
  type IngestResponse,
  type EquilibriumResponse,
} from '@/lib/observatory';
import { C, mono, Badge } from '@/components/observatory/ui';
import { Panel } from '@/components/observatory/ui';
import { IngestPanel } from '@/components/observatory/IngestPanel';
import { QualityPanel } from '@/components/observatory/QualityPanel';
import { PriceChart } from '@/components/observatory/PriceChart';
import { HabitatPanel } from '@/components/observatory/HabitatPanel';

export default function ObservatoryPage() {
  const [ingest, setIngest] = useState<IngestResponse | null>(null);
  const [asOf, setAsOf] = useState<string | null>(null);
  const [equilibrium, setEquilibrium] = useState<EquilibriumResponse | null>(null);
  const [windowSel, setWindowSel] = useState<{ start: string | null; end: string | null }>({ start: null, end: null });

  const datasetId = ingest?.dataset.dataset_id ?? '';

  return (
    <div style={{ display: 'flex', flex: 1, minHeight: 0, background: C.bg, padding: 10, gap: 10 }}>
      {/* left column — ingest + quality */}
      <div style={{ width: 340, display: 'flex', flexDirection: 'column', gap: 10, minHeight: 0, overflow: 'auto' }}>
        <Panel title="1 · ingest + column map">
          <IngestPanel
            onIngested={(r) => {
              setIngest(r);
              setAsOf(null);
              setEquilibrium(null);
              setWindowSel({ start: null, end: null });
            }}
          />
        </Panel>
        {ingest && (
          <Panel
            title="quality report"
            right={
              <Badge tone={ingest.quality.non_positive_prices.count > 0 ? 'danger' : 'good'}>
                {ingest.quality.non_positive_prices.count > 0 ? 'flags' : 'clean'}
              </Badge>
            }
          >
            <QualityPanel q={ingest.quality} datasetId={datasetId} />
          </Panel>
        )}
      </div>

      {/* center — price chart + as-of cursor + μ* + z */}
      <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
        {datasetId ? (
          <Panel title={`2–3 · price · μ* · z — ${ingest?.dataset.name}`} style={{ flex: 1 }}>
            <PriceChart
              datasetId={datasetId}
              asOf={asOf}
              onAsOfChange={setAsOf}
              onEquilibrium={setEquilibrium}
              windowSel={windowSel}
              onWindowSel={setWindowSel}
            />
          </Panel>
        ) : (
          <Empty />
        )}
      </div>

      {/* right — habitat */}
      <div style={{ width: 420, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
        <Panel title="4 · MR habitat — surrogate-relative" style={{ flex: 1 }}>
          {datasetId ? (
            <HabitatPanel datasetId={datasetId} asOf={asOf} window={windowSel} />
          ) : (
            <span style={{ ...mono, fontSize: 11, color: C.textDim }}>ingest a dataset to score a window.</span>
          )}
        </Panel>
        {equilibrium?.provenance.exploratory_watermark && (
          <div style={{ ...mono, fontSize: 10, color: C.warn, marginTop: 6 }}>
            ⚠ non-frozen Kalman params — results are EXPLORATORY, not a verdict.
          </div>
        )}
      </div>
    </div>
  );
}

function Empty() {
  return (
    <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', border: `1px solid ${C.border}`, borderRadius: 5 }}>
      <span style={{ ...mono, fontSize: 12, color: C.textDim }}>upload a CSV to open the observatory →</span>
    </div>
  );
}
