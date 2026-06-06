'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import type { ModuleProps } from '../types';
import type { DiagnosticsRow, DiagnosticsStats } from '@/lib/types';

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};
function fmt(n: number, d = 3) { return n.toFixed(d); }

// ── Sparkline strip ───────────────────────────────────────────────────────────
// Renders a time-series of values as a thin strip with a threshold line.
// Regions where value exceeds threshold are shaded.
function TestStrip({
  label, description, values, threshold, invertPass,
}: {
  label: string;
  description: string;
  values: number[];
  threshold: number;
  invertPass: boolean; // true = "fail when value > threshold"
}) {
  if (!values.length) return null;

  const W = 800, H = 48;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = (max - min) || 1;
  const n = values.length;

  const toY = (v: number) => H - 4 - ((v - min) / range) * (H - 8);
  const threshY = toY(threshold);

  const pts = values.map((v, i) => `${(i / (n - 1)) * W},${toY(v)}`).join(' ');

  // Shade failing regions
  const failRects: { x: number; w: number }[] = [];
  let start: number | null = null;
  values.forEach((v, i) => {
    const fails = invertPass ? v > threshold : v < threshold;
    if (fails && start === null) start = i;
    if (!fails && start !== null) {
      failRects.push({ x: (start / n) * W, w: ((i - start) / n) * W });
      start = null;
    }
  });
  if (start !== null) failRects.push({ x: (start / n) * W, w: ((n - start) / n) * W });

  const lastVal = values[values.length - 1];
  const isFailing = invertPass ? lastVal > threshold : lastVal < threshold;

  return (
    <div style={{ borderBottom: '1px solid #0e1520', background: '#06090e' }}>
      <div style={{ height: 18, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 12, borderBottom: '1px solid #0a0f16' }}>
        <span style={{ ...mono, fontSize: 9, fontWeight: 600, color: isFailing ? '#f85149' : '#3fb950', letterSpacing: '0.08em', width: 36 }}>
          {isFailing ? 'FAIL' : 'PASS'}
        </span>
        <span style={{ ...mono, fontSize: 9, color: '#3d4d5e', letterSpacing: '0.08em' }}>{label}</span>
        <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>{description}</span>
        <span style={{ ...mono, fontSize: 9, color: '#3d4d5e', marginLeft: 'auto', marginRight: 12 }}>
          current: {fmt(lastVal)}  threshold: {fmt(threshold)}
        </span>
      </div>
      <svg width="100%" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" style={{ display: 'block', height: H }}>
        {failRects.map((r, i) => (
          <rect key={i} x={r.x} y={0} width={r.w} height={H} fill="rgba(248,81,73,0.06)" />
        ))}
        <line x1={0} y1={threshY} x2={W} y2={threshY} stroke="rgba(248,81,73,0.3)" strokeDasharray="4,3" />
        <polyline points={pts} fill="none" stroke="rgba(88,166,255,0.5)" strokeWidth="1" />
      </svg>
    </div>
  );
}

export function AssumptionValidator({ instrumentId, dateRange, window: win }: ModuleProps) {
  const [rows, setRows] = useState<DiagnosticsRow[]>([]);
  const [stats, setStats] = useState<DiagnosticsStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setError(null);
    if (!instrumentId) return;
    let cancelled = false;
    setLoading(true);

    api.getDiagnostics(instrumentId, win, dateRange.start ?? undefined, dateRange.end ?? undefined)
      .then((resp) => {
        if (cancelled) return;
        setRows(resp.rows);
        setStats(resp.stats);
      })
      .catch((e: unknown) => { if (!cancelled) setError(e instanceof Error ? e.message : 'Fetch failed'); })
      .finally(() => { if (!cancelled) setLoading(false); });

    return () => { cancelled = true; };
  }, [instrumentId, dateRange.start, dateRange.end, win]); // eslint-disable-line react-hooks/exhaustive-deps

  // Derive rolling ε zscore as proxy for stationarity — large |z| = non-stationary behavior
  // (Full rolling ADF/KPSS would require a backend endpoint — deferred. This is the causal proxy.)
  const epsilonZscores = rows.map(r => r.epsilon_zscore ?? 0);
  const rollStds = rows.map(r => r.epsilon_rolling_std);
  const innovations = rows.map(r => r.innovation ?? 0);
  // ACF-1 rolling proxy: use absolute zscore to detect volatility expansion
  const absEps = rows.map(r => Math.abs(r.epsilon));

  const interpret = (s: DiagnosticsStats) => {
    const issues: string[] = [];
    if (Math.abs(s.acf_lag1) > 0.3) issues.push(`ACF(1)=${fmt(s.acf_lag1)} — residuals are autocorrelated (not white noise)`);
    if (s.halflife_bars == null) issues.push('Half-life undefined — residual may not be mean-reverting');
    else if (s.halflife_bars > 60) issues.push(`Half-life=${fmt(s.halflife_bars, 0)} bars — reversion is slow`);
    if (Math.abs(s.epsilon_skew) > 1) issues.push(`Skew=${fmt(s.epsilon_skew, 2)} — distribution is asymmetric`);
    if (s.epsilon_kurt > 3) issues.push(`Kurtosis=${fmt(s.epsilon_kurt, 2)} — fat tails present`);
    if (issues.length === 0) issues.push('No major assumption violations detected for this window.');
    return issues;
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', background: '#070b10' }}>
      {/* Header */}
      <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 16, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
        <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.14em', textTransform: 'uppercase' }}>Assumption Validator</span>
        {loading && <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>loading</span>}
        {error && <span style={{ ...mono, fontSize: 9, color: '#f85149' }}>{error}</span>}
        <span style={{ ...mono, fontSize: 9, color: '#1e2833', marginLeft: 'auto', marginRight: 12 }}>
          PASS (green) · FAIL (red) — last bar status
        </span>
      </div>

      {/* Interpretation panel */}
      {stats && (
        <div style={{ flexShrink: 0, padding: '8px 12px', borderBottom: '1px solid #0e1520', display: 'flex', flexWrap: 'wrap', gap: 6 }}>
          {interpret(stats).map((msg, i) => (
            <span key={i} style={{
              ...mono, fontSize: 9,
              color: msg.startsWith('No major') ? '#3fb950' : '#f85149',
              background: msg.startsWith('No major') ? 'rgba(63,185,80,0.04)' : 'rgba(248,81,73,0.04)',
              border: `1px solid ${msg.startsWith('No major') ? 'rgba(63,185,80,0.15)' : 'rgba(248,81,73,0.15)'}`,
              padding: '2px 6px', borderRadius: 2,
            }}>{msg}</span>
          ))}
        </div>
      )}

      {/* Test strips */}
      <div style={{ flex: 1, minHeight: 0, overflowY: 'auto' }}>
        {rows.length > 0 ? (
          <>
            <TestStrip
              label="|ε z-score| > 2σ"
              description="Local residual z-score — bars exceeding 2σ of rolling window. ~5% expected for any normal ε."
              values={epsilonZscores.map(Math.abs)}
              threshold={2.0}
              invertPass={true}
            />
            <TestStrip
              label="Rolling σ(ε)"
              description="Standard deviation of residuals — expanding σ = model uncertainty growing"
              values={rollStds}
              threshold={(stats?.epsilon_std ?? 1) * 1.5}
              invertPass={true}
            />
            <TestStrip
              label="|ε| (abs residual)"
              description="Absolute residual magnitude — sustained |ε| > 2σ = non-mean-reverting regime"
              values={absEps}
              threshold={(stats?.epsilon_std ?? 1) * 2}
              invertPass={true}
            />
            <TestStrip
              label="Innovation |close[t] − μ*[t-1]|"
              description="One-step prediction error — large sustained innovation = estimator lagging badly"
              values={innovations.map(Math.abs)}
              threshold={(stats?.epsilon_std ?? 1) * 2}
              invertPass={true}
            />
          </>
        ) : (
          <div style={{ padding: 24 }}>
            <span style={{ ...mono, fontSize: 10, color: '#1e2833' }}>
              {instrumentId ? 'Loading...' : 'Select an instrument'}
            </span>
          </div>
        )}
      </div>

      {/* Footer note */}
      <div style={{ flexShrink: 0, padding: '6px 12px', borderTop: '1px solid #0e1520', background: '#06090e' }}>
        <span style={{ ...mono, fontSize: 8, color: '#1e2833' }}>
          Note: Full rolling ADF/KPSS tests deferred — these strips use causal ε-based proxies. Strip 1 and Strip 3 measure related quantities (local vs global z-score normalization). Neither measures autocorrelation directly. Red = threshold exceeded; ~5% of bars expected to fail Strip 1 under normality.
        </span>
      </div>
    </div>
  );
}
