'use client';

/**
 * Observatory v2 — vertical slice (contract §10).
 *   ingest + column-map + quality → price chart + draggable as-of cursor → causal μ* + z
 *   → window-selected, surrogate-relative habitat score with its cloud + raw/deseason toggle.
 *
 * Thin client: every number comes from /api/v2. No statistic computed in JS (M5).
 * Additive & isolated: NEW route; does not touch /workbench or src/lib/api.ts.
 */
import { useState, useRef, useCallback } from 'react';
import { PanelGroup, Panel as RPanel } from 'react-resizable-panels';
import { ResizeHandle } from '@/components/layout/ResizeHandle';
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
  // true once the user has DELIBERATELY committed a window end (typed/Enter/blur). While false the
  // end auto-tracks the cursor. This distinguishes "respect a deliberate sub-window" from "follow
  // the cursor", which is the crux of Part 1. ISO 'YYYY-MM-DD' dates compare lexicographically.
  const endManualRef = useRef(false);
  const [scoreNonce, setScoreNonce] = useState(0);   // bump → HabitatPanel re-fetches (commit path)
  const [clampNote, setClampNote] = useState<string | null>(null);

  const datasetId = ingest?.dataset.dataset_id ?? '';

  // PART 1 — the as-of cursor is a HARD UPPER BOUND on the habitat window end (causal firewall).
  // start is NEVER auto-updated by the cursor. end:
  //   • no manual end yet            → tracks the cursor (forward AND back)
  //   • manual end, end > cursor     → clamp down to the cursor (firewall)
  //   • manual end, end ≤ cursor     → leave (deliberate sub-window)
  const handleAsOf = useCallback((d: string) => {
    setAsOf(d);
    setWindowSel((w) => {
      if (!endManualRef.current) return { start: w.start, end: d };
      if (w.end && w.end > d) return { start: w.start, end: d };
      return w;
    });
  }, []);

  // live (uncommitted) field edits — keep the controlled date inputs responsive; no clamp/fetch yet.
  const liveWindow = useCallback((w: { start: string | null; end: string | null }) => setWindowSel(w), []);

  // PART 2 — commit a manually edited window field (blur/Enter): clamp end ≤ as-of, then score.
  const commitWindow = useCallback(
    (field: 'start' | 'end', raw: string | null) => {
      let value = raw;
      if (field === 'end') {
        endManualRef.current = true;
        if (value && asOf && value > asOf) {
          value = asOf;
          setClampNote('window end clamped to as-of date (causal firewall)');
        } else {
          setClampNote(null);
        }
      }
      setWindowSel((w) => ({ ...w, [field]: value }));
      setScoreNonce((n) => n + 1);   // → HabitatPanel re-fetches for the committed window
    },
    [asOf],
  );

  // "≤ as-of" convenience: full causal window that RESUMES cursor-tracking of the end.
  const trackToAsOf = useCallback(
    (start: string | null) => {
      endManualRef.current = false;
      setClampNote(null);
      setWindowSel({ start, end: asOf });
    },
    [asOf],
  );

  return (
    <div style={{ display: 'flex', flex: 1, minHeight: 0, background: C.bg, padding: 10 }}>
     <PanelGroup direction="horizontal" autoSaveId="amr-observatory-cols" style={{ flex: 1, minHeight: 0 }}>
      {/* left column — ingest + quality */}
      <RPanel defaultSize={24} minSize={15} maxSize={42}>
      <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', gap: 10, minHeight: 0, overflow: 'auto', paddingRight: 6 }}>
        <Panel title="1 · ingest + column map">
          <IngestPanel
            onIngested={(r) => {
              setIngest(r);
              setAsOf(null);
              setEquilibrium(null);
              setWindowSel({ start: null, end: null });
              endManualRef.current = false;
              setClampNote(null);
              setScoreNonce(0);
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
      </RPanel>

      <ResizeHandle dir="horizontal" />

      {/* center — price chart + as-of cursor + μ* + z */}
      <RPanel defaultSize={46} minSize={28}>
      <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', minHeight: 0, padding: '0 6px' }}>
        {datasetId ? (
          <Panel title={`2–3 · price · μ* · z — ${ingest?.dataset.name}`} style={{ flex: 1 }}>
            <PriceChart
              datasetId={datasetId}
              asOf={asOf}
              onAsOfChange={handleAsOf}
              onEquilibrium={setEquilibrium}
              windowSel={windowSel}
              onWindowSel={liveWindow}
              onCommitWindow={commitWindow}
              onTrackToAsOf={trackToAsOf}
              clampNote={clampNote}
            />
          </Panel>
        ) : (
          <Empty />
        )}
      </div>
      </RPanel>

      <ResizeHandle dir="horizontal" />

      {/* right — habitat */}
      <RPanel defaultSize={30} minSize={18} maxSize={48}>
      <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', minHeight: 0, paddingLeft: 6 }}>
        <Panel title="4 · MR habitat — surrogate-relative" style={{ flex: 1 }}>
          {datasetId ? (
            <HabitatPanel datasetId={datasetId} asOf={asOf} window={windowSel} scoreNonce={scoreNonce} />
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
      </RPanel>
     </PanelGroup>
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
