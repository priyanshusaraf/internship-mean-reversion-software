'use client';

/**
 * Habitat panel (contract §4.2). SURROGATE-RELATIVE BY CONSTRUCTION: the score never renders
 * without its cloud. We draw:
 *   - the score (0-100, backend value)
 *   - the surrogate cloud (histogram of null_min_vr[], BINNED FOR BARS ONLY — M5) with the
 *     real_min_vr marker and where frac_ge_real sits
 *   - p10/p50/p90, frac_ge_real (all backend scalars — never recomputed in JS)
 *   - the calibration badge (OU 71.3 / RW 49.2 / trend 17.2 validated_non_inverting)
 *   - a raw ↔ deseason toggle; if raw_vs_deseason.verdict_changed → contamination flag.
 */
import { useState, useEffect } from 'react';
import {
  observatory,
  binForHistogram,
  type HabitatResponse,
} from '@/lib/observatory';
import { C, mono, Badge, Stat, fmt } from './ui';

interface Props {
  datasetId: string;
  asOf: string | null;
  window: { start: string | null; end: string | null };
  scoreNonce: number;   // bumped by the page on a window commit → re-fetch the score (Part 2)
}

export function HabitatPanel({ datasetId, asOf, window, scoreNonce }: Props) {
  const [deseason, setDeseason] = useState(false);
  const [resp, setResp] = useState<HabitatResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canRun = !!datasetId && !!window.start && !!window.end;

  async function run(ds: boolean) {
    if (!canRun || !window.start || !window.end) {
      setError('Select a habitat window (≤ as-of) on the chart first.');
      return;
    }
    // MANDATORY CAUSAL FIREWALL — fires before EVERY habitat call. The as-of cursor is the
    // temporal firewall; a window end beyond it would score on lookahead data. Clamp, never
    // silently send a future end. as_of is ALWAYS the cursor date (never the window end).
    let windowEnd = window.end;
    if (asOf && windowEnd > asOf) {
      console.warn(`habitat: window end ${windowEnd} > as-of ${asOf} — clamping to as-of (causal firewall)`);
      windowEnd = asOf;
    }
    setBusy(true);
    setError(null);
    try {
      const r = await observatory.habitat({
        dataset_id: datasetId,
        window: { start: window.start, end: windowEnd },
        as_of: asOf,
        deseason: ds,
        params: { vr_qs: [2, 5, 10, 20], ns_null: 200, seed: 42 },
      });
      setResp(r);
      setDeseason(ds);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'habitat failed');
    } finally {
      setBusy(false);
    }
  }

  // Part 2 — a committed window edit (page bumps scoreNonce) re-fetches for the new window.
  // nonce 0 = initial/no-commit → do nothing (scoring stays a deliberate action).
  useEffect(() => {
    if (scoreNonce === 0) return;
    void run(deseason);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [scoreNonce]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
        <button data-testid="run-habitat" onClick={() => run(deseason)} disabled={!canRun || busy} style={primaryBtn(canRun && !busy)}>
          {busy ? 'scoring…' : 'score window'}
        </button>
        <div style={{ display: 'flex', borderRadius: 3, overflow: 'hidden', border: `1px solid ${C.border}` }}>
          {(['raw', 'deseason'] as const).map((m) => {
            const on = (m === 'deseason') === deseason;
            return (
              <button
                key={m}
                data-testid={`toggle-${m}`}
                onClick={() => run(m === 'deseason')}
                disabled={busy || !canRun}
                style={{
                  ...mono,
                  fontSize: 10,
                  padding: '3px 10px',
                  cursor: busy ? 'default' : 'pointer',
                  border: 'none',
                  color: on ? C.accent : C.textDim,
                  background: on ? C.accentBg : 'transparent',
                }}
              >
                {m}
              </button>
            );
          })}
        </div>
        {window.start && window.end && (
          <span style={{ ...mono, fontSize: 10, color: C.textDim }}>
            {window.start} → {window.end}
          </span>
        )}
      </div>

      {error && <div style={{ ...mono, fontSize: 10, color: C.danger }}>{error}</div>}

      {resp && <HabitatResult resp={resp} />}
    </div>
  );
}

function HabitatResult({ resp }: { resp: HabitatResponse }) {
  const sd = resp.surrogate_distribution;
  const cb = resp.calibration_badge;
  const rvd = resp.raw_vs_deseason;
  const contaminated = rvd?.verdict_changed === true;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      {resp.data_warning && (
        <div style={{ ...mono, fontSize: 10, color: C.warn, background: C.warnBg, border: `1px solid ${C.warnBorder}`, borderRadius: 3, padding: '5px 8px' }}>
          ⚠ {resp.data_warning}
        </div>
      )}

      {/* score block — ALWAYS shown with the cloud below; never bare */}
      <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: 14, alignItems: 'center' }}>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span style={{ fontSize: 9, letterSpacing: '0.08em', textTransform: 'uppercase', color: C.textDim }}>habitat score</span>
          <span style={{ ...mono, fontSize: 30, color: scoreColor(resp.score), lineHeight: 1 }}>
            {resp.score === null ? '—' : resp.score.toFixed(1)}
          </span>
          <span style={{ ...mono, fontSize: 9, color: C.textDim }}>surrogate-relative · 0–100</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2,1fr)', gap: 8 }}>
          <Stat label="real min-VR" value={fmt(resp.real_min_vr, 3)} color={C.accent} />
          <Stat label="frac ≥ real" value={fmt(sd.frac_ge_real, 3)} />
          <Stat label="p10 / p50 / p90" value={`${fmt(sd.p10, 2)} / ${fmt(sd.p50, 2)} / ${fmt(sd.p90, 2)}`} />
          <Stat label="surrogates" value={sd.n} />
        </div>
      </div>

      {/* SURROGATE CLOUD — mandatory. Histogram of null_min_vr[] (bars binned for display only) */}
      <SurrogateCloud nulls={sd.null_min_vr} realMinVr={resp.real_min_vr} p10={sd.p10} p90={sd.p90} />

      {/* VR curve */}
      <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
        <span style={{ ...mono, fontSize: 9, letterSpacing: '0.08em', textTransform: 'uppercase', color: C.textDim }}>VR(q)</span>
        {resp.vr_curve.map((p) => (
          <span key={p.q} style={{ ...mono, fontSize: 11, color: C.textBright }}>
            q{p.q}=<span style={{ color: C.accent }}>{fmt(p.vr, 3)}</span>
          </span>
        ))}
      </div>

      {/* calibration badge */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
        <span style={{ ...mono, fontSize: 9, letterSpacing: '0.08em', textTransform: 'uppercase', color: C.textDim }}>calibration</span>
        <Badge tone="good">OU {cb.ou}</Badge>
        <Badge tone="neutral">RW {cb.rw}</Badge>
        <Badge tone="danger">trend {cb.trend}</Badge>
        <Badge tone={cb.status === 'validated_non_inverting' ? 'good' : 'warn'}>{cb.status}</Badge>
      </div>

      {/* contamination flag (raw vs deseason) */}
      {rvd && (
        <div
          data-testid="contamination-flag"
          style={{
            ...mono,
            fontSize: 10,
            border: `1px solid ${contaminated ? C.dangerBorder : C.border}`,
            background: contaminated ? C.dangerBg : 'transparent',
            borderRadius: 3,
            padding: '5px 8px',
            display: 'flex',
            gap: 10,
            flexWrap: 'wrap',
            alignItems: 'center',
          }}
        >
          <span style={{ color: C.textDim }}>raw {fmt(rvd.raw_score, 1)} · deseason {fmt(rvd.deseason_score, 1)}</span>
          {contaminated ? (
            <Badge tone="danger">CONTAMINATION — deseason flips the verdict (BRN lesson)</Badge>
          ) : (
            <Badge tone="good">verdict stable across deseason</Badge>
          )}
        </div>
      )}

      <Provenance prov={resp.provenance} />
    </div>
  );
}

function SurrogateCloud({
  nulls,
  realMinVr,
  p10,
  p90,
}: {
  nulls: number[];
  realMinVr: number | null;
  p10: number | null;
  p90: number | null;
}) {
  const bins = binForHistogram(nulls, 28); // BARS ONLY (M5) — no scalar derived
  if (bins.length === 0) {
    return <div style={{ ...mono, fontSize: 10, color: C.textDim }}>no surrogate cloud returned</div>;
  }
  const maxCount = Math.max(...bins.map((b) => b.count), 1);
  const lo = bins[0].x0;
  const hi = bins[bins.length - 1].x1;
  const span = hi - lo || 1;
  const W = 100; // percent coordinates
  const realX = realMinVr != null && Number.isFinite(realMinVr) ? ((realMinVr - lo) / span) * W : null;
  const p10X = p10 != null && Number.isFinite(p10) ? ((p10 - lo) / span) * W : null;
  const p90X = p90 != null && Number.isFinite(p90) ? ((p90 - lo) / span) * W : null;

  return (
    <div data-testid="surrogate-cloud" style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <span style={{ ...mono, fontSize: 9, letterSpacing: '0.08em', textTransform: 'uppercase', color: C.textDim }}>
        surrogate cloud · null min-VR distribution (n={nulls.length})
      </span>
      <div style={{ position: 'relative', height: 90, background: C.bg, border: `1px solid ${C.border}`, borderRadius: 4, padding: '6px 4px 0' }}>
        {/* bars */}
        <div style={{ position: 'absolute', inset: '6px 4px 14px', display: 'flex', alignItems: 'flex-end', gap: 1 }}>
          {bins.map((b, i) => (
            <div
              key={i}
              title={`[${b.x0.toFixed(2)}, ${b.x1.toFixed(2)}) · ${b.count}`}
              style={{ flex: 1, height: `${(b.count / maxCount) * 100}%`, background: 'rgba(88,166,255,0.28)', minHeight: b.count > 0 ? 1 : 0 }}
            />
          ))}
        </div>
        {/* p10 / p90 markers */}
        {p10X != null && <Marker x={p10X} color="#2a3548" label="p10" />}
        {p90X != null && <Marker x={p90X} color="#2a3548" label="p90" />}
        {/* real min-VR marker — where the realized statistic sits in the null cloud */}
        {realX != null && <Marker x={Math.max(0, Math.min(100, realX))} color={C.accent} label="real" bold />}
        {/* axis labels */}
        <div style={{ position: 'absolute', left: 4, bottom: 1, ...mono, fontSize: 8, color: C.textDim }}>{lo.toFixed(2)}</div>
        <div style={{ position: 'absolute', right: 4, bottom: 1, ...mono, fontSize: 8, color: C.textDim }}>{hi.toFixed(2)}</div>
      </div>
      <span style={{ ...mono, fontSize: 9, color: C.textDim }}>
        lower min-VR = more mean-reverting. real-VR left of the cloud ⇒ beats surrogates.
      </span>
    </div>
  );
}

function Marker({ x, color, label, bold }: { x: number; color: string; label: string; bold?: boolean }) {
  return (
    <div style={{ position: 'absolute', top: 6, bottom: 14, left: `${x}%`, width: 0, borderLeft: `${bold ? 2 : 1}px solid ${color}` }}>
      <span style={{ position: 'absolute', top: -2, left: 2, ...mono, fontSize: 8, color, whiteSpace: 'nowrap', fontWeight: bold ? 700 : 400 }}>{label}</span>
    </div>
  );
}

function Provenance({ prov }: { prov: HabitatResponse['provenance'] }) {
  return (
    <div style={{ ...mono, fontSize: 9, color: C.textDim, display: 'flex', gap: 10, flexWrap: 'wrap', borderTop: `1px solid ${C.borderSoft}`, paddingTop: 6 }}>
      <span>dataset {prov.dataset_id}</span>
      <span>hash {prov.dataset_hash}</span>
      <span>as-of {prov.as_of ?? '—'}</span>
      <span>mode {prov.mode}</span>
      <span>engine {prov.engine}</span>
      <span>{prov.computed_at.slice(0, 19).replace('T', ' ')}</span>
      {prov.exploratory_watermark && <Badge tone="warn">EXPLORATORY</Badge>}
    </div>
  );
}

function scoreColor(score: number | null): string {
  if (score === null) return C.textDim;
  if (score >= 70) return C.good;
  if (score >= 50) return C.accent;
  return C.warn;
}

function primaryBtn(enabled: boolean): React.CSSProperties {
  return {
    ...mono,
    fontSize: 11,
    padding: '4px 12px',
    borderRadius: 4,
    cursor: enabled ? 'pointer' : 'not-allowed',
    color: enabled ? C.accent : C.textDim,
    background: enabled ? C.accentBg : 'transparent',
    border: `1px solid ${enabled ? C.accentBorder : C.border}`,
  };
}
