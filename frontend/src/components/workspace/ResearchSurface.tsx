'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { useWorkstationStore } from '@/lib/store';
import type { ResearchRow, ResearchStats } from '@/lib/types';

const COL = {
  date: { label: 'date', width: 90 },
  close: { label: 'close', width: 80 },
  mu_star: { label: 'μ*', width: 80 },
  epsilon: { label: 'ε = P − μ*', width: 90 },
} as const;

const monoStyle: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

function fmt(n: number, decimals = 2): string {
  return n.toFixed(decimals);
}

function epsilonColor(epsilon: number): string {
  if (epsilon > 0) return 'rgba(63,185,80,0.75)';
  if (epsilon < 0) return 'rgba(248,81,73,0.75)';
  return '#3d4d5e';
}

export function ResearchSurface() {
  const { selectedInstrumentId, dateRange, estimatorEnabled, estimatorWindow } =
    useWorkstationStore();

  const [rows, setRows] = useState<ResearchRow[]>([]);
  const [stats, setStats] = useState<ResearchStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setError(null);
    if (!selectedInstrumentId || !estimatorEnabled) {
      setRows([]);
      setStats(null);
      return;
    }

    let cancelled = false;
    setLoading(true);

    api
      .getResearch(
        selectedInstrumentId,
        estimatorWindow,
        dateRange.start ?? undefined,
        dateRange.end ?? undefined
      )
      .then((resp) => {
        if (cancelled) return;
        setRows([...resp.rows].reverse());
        setStats(resp.stats);
      })
      .catch((e: unknown) => {
        if (!cancelled) setError(e instanceof Error ? e.message : 'Fetch failed');
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => { cancelled = true; };
  }, [selectedInstrumentId, dateRange.start, dateRange.end, estimatorEnabled, estimatorWindow]); // eslint-disable-line react-hooks/exhaustive-deps

  const isEmpty = !selectedInstrumentId;
  const noEstimator = selectedInstrumentId && !estimatorEnabled;

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        background: '#070b10',
        borderTop: '1px solid #0e1520',
        overflow: 'hidden',
        flexShrink: 0,
      }}
    >
      {/* Header bar */}
      <div
        style={{
          height: 28,
          display: 'flex',
          alignItems: 'center',
          paddingLeft: 12,
          paddingRight: 12,
          background: '#090d13',
          borderBottom: '1px solid #0e1520',
          gap: 12,
          flexShrink: 0,
        }}
      >
        <span style={{ ...monoStyle, fontSize: 9, fontWeight: 700, color: 'var(--amr-text-dim)', letterSpacing: '0.14em', textTransform: 'uppercase' }}>
          Research
        </span>

        {stats && (
          <>
            <div style={{ width: 1, height: 10, background: '#161d27' }} />
            <span style={{ ...monoStyle, fontSize: 10, color: 'var(--amr-text)' }}>
              n={stats.n}
            </span>
            <span style={{ ...monoStyle, fontSize: 10, color: 'var(--amr-text)' }}>
              ε̄={fmt(stats.epsilon_mean)}
            </span>
            <span style={{ ...monoStyle, fontSize: 10, color: 'var(--amr-text)' }}>
              σ(ε)={fmt(stats.epsilon_std)}
            </span>
            {loading && (
              <span style={{ ...monoStyle, fontSize: 10, color: 'var(--amr-text-dim)', marginLeft: 'auto' }}>
                loading
              </span>
            )}
          </>
        )}

        {error && (
          <span style={{ ...monoStyle, fontSize: 10, color: '#f85149', marginLeft: 8 }}>
            {error}
          </span>
        )}
      </div>

      {/* Table */}
      <div style={{ flex: 1, overflowY: 'auto', overflowX: 'hidden' }}>
        {isEmpty && (
          <div style={{ padding: '16px 12px' }}>
            <span style={{ ...monoStyle, fontSize: 10, color: '#1e2833' }}>
              Select an instrument to begin
            </span>
          </div>
        )}

        {noEstimator && (
          <div style={{ padding: '16px 12px' }}>
            <span style={{ ...monoStyle, fontSize: 10, color: '#1e2833' }}>
              Enable μ* estimator to see research data
            </span>
          </div>
        )}

        {rows.length > 0 && (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#090d13', position: 'sticky', top: 0, zIndex: 1 }}>
                {Object.entries(COL).map(([key, col]) => (
                  <th
                    key={key}
                    style={{
                      ...monoStyle,
                      textAlign: 'right',
                      padding: '4px 10px',
                      fontSize: 9,
                      fontWeight: 600,
                      color: 'var(--amr-text-dim)',
                      letterSpacing: '0.08em',
                      textTransform: 'uppercase',
                      borderBottom: '1px solid #0e1520',
                      width: col.width,
                      userSelect: 'none',
                    }}
                  >
                    {col.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, i) => (
                <tr
                  key={row.date}
                  style={{
                    background: i % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.008)',
                    borderBottom: '1px solid #0a0f16',
                  }}
                >
                  <td style={{ ...monoStyle, padding: '3px 10px', fontSize: 10, color: 'var(--amr-text)', textAlign: 'right' }}>
                    {row.date}
                  </td>
                  <td style={{ ...monoStyle, padding: '3px 10px', fontSize: 10, color: '#8b99a8', textAlign: 'right' }}>
                    {fmt(row.close)}
                  </td>
                  <td style={{ ...monoStyle, padding: '3px 10px', fontSize: 10, color: 'rgba(88,166,255,0.7)', textAlign: 'right' }}>
                    {fmt(row.mu_star)}
                  </td>
                  <td style={{ ...monoStyle, padding: '3px 10px', fontSize: 10, color: epsilonColor(row.epsilon), textAlign: 'right' }}>
                    {row.epsilon > 0 ? '+' : ''}{fmt(row.epsilon)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
