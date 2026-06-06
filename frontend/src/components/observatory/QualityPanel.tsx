'use client';

/**
 * QualityReport panel (contract §3). Every value comes from the backend's QualityReport.
 * Nothing proceeds silently: gaps, dupes, and especially non-positive prices (the CL Apr-2020
 * case) are flagged with the backend's suggested excision window.
 */
import type { QualityReport } from '@/lib/observatory';
import { C, mono, Badge, Stat, fmt } from './ui';

export function QualityPanel({ q, datasetId }: { q: QualityReport; datasetId: string }) {
  const np = q.non_positive_prices;
  const hasNonPositive = np.count > 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2,1fr)', gap: 10 }}>
        <Stat label="dataset" value={datasetId} />
        <Stat label="rows" value={q.row_count.toLocaleString()} />
        <Stat label="range" value={`${q.date_range.start ?? '—'} → ${q.date_range.end ?? '—'}`} />
        <Stat label="frequency" value={q.frequency} color={q.frequency === 'unknown' ? C.warn : C.textBright} />
        <Stat label="median Δ (days)" value={fmt(q.median_delta_days, 2)} />
        <Stat label="nan rows dropped" value={q.nan_rows_dropped} color={q.nan_rows_dropped > 0 ? C.warn : C.textBright} />
        <Stat label="gaps" value={q.n_gaps} color={q.n_gaps > 0 ? C.warn : C.textBright} />
        <Stat label="duplicate ts" value={q.duplicate_timestamps} color={q.duplicate_timestamps > 0 ? C.warn : C.textBright} />
      </div>

      {/* Non-positive prices — the CL Apr-2020 case. Flag, never silently drop. */}
      <div
        data-testid="non-positive-flag"
        style={{
          border: `1px solid ${hasNonPositive ? C.dangerBorder : C.border}`,
          background: hasNonPositive ? C.dangerBg : 'transparent',
          borderRadius: 4,
          padding: 8,
          display: 'flex',
          flexDirection: 'column',
          gap: 6,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ ...mono, fontSize: 10, color: hasNonPositive ? C.danger : C.text }}>non-positive prices</span>
          <Badge tone={hasNonPositive ? 'danger' : 'good'}>{hasNonPositive ? `${np.count} flagged` : 'none'}</Badge>
        </div>
        {hasNonPositive && (
          <>
            <div style={{ ...mono, fontSize: 10, color: C.textBright }}>
              examples:{' '}
              {np.examples.slice(0, 4).map((e, i) => (
                <span key={i} style={{ color: C.danger }}>
                  {e.time}={fmt(e.close, 2)}
                  {i < Math.min(np.examples.length, 4) - 1 ? ', ' : ''}
                </span>
              ))}
            </div>
            {np.suggested_excision && (
              <div style={{ ...mono, fontSize: 10, color: C.warn }}>
                suggested excision window:{' '}
                <span style={{ color: C.textBright }}>
                  {np.suggested_excision.from} → {np.suggested_excision.to}
                </span>{' '}
                <Badge tone="warn">flagged — not auto-dropped</Badge>
              </div>
            )}
          </>
        )}
      </div>

      {q.gaps.length > 0 && (
        <div style={{ ...mono, fontSize: 10, color: C.text }}>
          <div style={{ color: C.warn, marginBottom: 3 }}>calendar gaps</div>
          {q.gaps.slice(0, 6).map((g, i) => (
            <div key={i} style={{ color: C.textBright }}>
              {g.from} → {g.to} ({g.missing_bars} missing)
            </div>
          ))}
          {q.gaps.length > 6 && <div style={{ color: C.textDim }}>+{q.gaps.length - 6} more</div>}
        </div>
      )}

      {q.back_adjustment_seams.length > 0 && (
        <div style={{ ...mono, fontSize: 10, color: C.text }}>
          <div style={{ color: C.warn, marginBottom: 3 }}>back-adjustment seams</div>
          {q.back_adjustment_seams.slice(0, 4).map((s, i) => (
            <div key={i} style={{ color: C.textBright }}>
              {s.time} jump {fmt(s.jump, 3)}
            </div>
          ))}
        </div>
      )}

      {q.warnings.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          {q.warnings.map((w, i) => (
            <div
              key={i}
              style={{
                ...mono,
                fontSize: 10,
                color: C.warn,
                background: C.warnBg,
                border: `1px solid ${C.warnBorder}`,
                borderRadius: 3,
                padding: '4px 7px',
              }}
            >
              ⚠ {w}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
