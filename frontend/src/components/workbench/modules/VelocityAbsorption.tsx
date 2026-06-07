'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import {
  createChart, ColorType, CrosshairMode,
  type IChartApi, type ISeriesApi, type Time,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import type { ModuleProps } from '../types';
import type { VelocityAbsorptionResponse, ReversionStat } from '@/lib/types';

// Step 2A — false-centering falsification (read-only instrumentation).
// Single question: did the Kalman velocity state remove economically useful reversion signal?
//   ε^K  (velocity-ON)  = Kalman innovation
//   ε^R  (velocity-OFF) = ε^K + δ ≡ matched-span EMA prediction residual
// Restoration test: does adding δ back (→ ε^R) materially improve predictive decay (β more
// negative) vs ε^K? If yes → velocity removed reversion. If ε^K ≈ ε^R → benign trend removal.
//
// Surface 3 shows RAW Δβ / direction / magnitude / consistency only — NO verdict language.
// Interpretation is manual at this stage; research language is frozen only after observation.
//
// Uses the matched-span EMA internally (backend), so this module is INDEPENDENT of the CMP
// display window. Respects the replay date range only.

const KAL_COLOR = 'rgba(255,180,60,0.9)';     // velocity-ON
const RES_COLOR = 'rgba(88,166,255,0.85)';    // velocity-OFF (restored ≡ matched EMA)
const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};
function fmt(n: number | null | undefined, d = 5) {
  return n == null || !Number.isFinite(n) ? '—' : (n >= 0 ? '+' : '') + n.toFixed(d);
}
function byH(stats: ReversionStat[]): Record<number, ReversionStat> {
  const m: Record<number, ReversionStat> = {};
  stats.forEach(s => { m[s.horizon] = s; });
  return m;
}

export function VelocityAbsorption({ instrumentId, dateRange }: ModuleProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chart = useRef<IChartApi | null>(null);
  const priceS = useRef<ISeriesApi<'Line'> | null>(null);
  const deltaS = useRef<ISeriesApi<'Line'> | null>(null);
  const zeroS = useRef<ISeriesApi<'Line'> | null>(null);

  const [data, setData] = useState<VelocityAbsorptionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;
    const c = createChart(chartRef.current, {
      layout: { background: { type: ColorType.Solid, color: '#070b10' }, textColor: '#3d4d5e', fontSize: 10 },
      grid: { vertLines: { color: '#0e1520' }, horzLines: { color: '#0e1520' } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: '#161d27' },
      leftPriceScale: { borderColor: '#161d27', visible: true },
      timeScale: { borderColor: '#161d27' },
      width: chartRef.current.clientWidth, height: chartRef.current.clientHeight,
    });
    priceS.current = c.addLineSeries({ color: 'rgba(140,160,180,0.4)', lineWidth: 1, priceScaleId: 'right', lastValueVisible: false, priceLineVisible: false, title: 'price' });
    zeroS.current = c.addLineSeries({ color: 'rgba(255,255,255,0.12)', lineWidth: 1, lineStyle: 2, priceScaleId: 'left', lastValueVisible: false, priceLineVisible: false });
    deltaS.current = c.addLineSeries({ color: 'rgba(216,166,87,0.9)', lineWidth: 1, priceScaleId: 'left', lastValueVisible: false, priceLineVisible: false, title: 'δ' });
    chart.current = c;
    const ro = new ResizeObserver(() => chartRef.current && c.applyOptions({ width: chartRef.current.clientWidth, height: chartRef.current.clientHeight }));
    ro.observe(chartRef.current);
    return () => { ro.disconnect(); c.remove(); chart.current = null; };
  }, []);

  useEffect(() => {
    setError(null);
    if (!instrumentId) return;
    let cancelled = false;
    setLoading(true);
    api.getVelocityAbsorption(instrumentId, dateRange.start ?? undefined, dateRange.end ?? undefined)
      .then((resp) => {
        if (cancelled) return;
        setData(resp);
        const t = (d: string) => d as Time;
        priceS.current?.setData(resp.rows.map(r => ({ time: t(r.date), value: r.price })));
        const dpts = resp.rows.filter(r => r.delta != null).map(r => ({ time: t(r.date), value: r.delta as number }));
        deltaS.current?.setData(dpts);
        zeroS.current?.setData(resp.rows.map(r => ({ time: t(r.date), value: 0 })));
        chart.current?.timeScale().fitContent();
      })
      .catch((e: unknown) => { if (!cancelled) setError(e instanceof Error ? e.message : 'Fetch failed'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [instrumentId, dateRange.start, dateRange.end]);

  const k = useMemo(() => (data ? byH(data.reversion_kalman) : null), [data]);
  const r = useMemo(() => (data ? byH(data.reversion_restored) : null), [data]);

  // Surface 3 — RAW structural comparison only. Δβ = β_restored − β_kalman. No verdict.
  const dbeta = useMemo(() => {
    if (!data || !k || !r) return null;
    return data.horizons.map(h => {
      const bk = k[h]?.beta, br = r[h]?.beta;
      const d = (bk != null && br != null) ? br - bk : null;
      return { h, d };
    });
  }, [data, k, r]);
  const consistentDir = useMemo(() => {
    if (!dbeta) return null;
    const signs = dbeta.map(x => (x.d == null ? null : Math.sign(x.d))).filter(s => s !== null) as number[];
    if (signs.length < 2) return null;
    return signs.every(s => s === signs[0]);
  }, [dbeta]);

  const cell = (s: ReversionStat | undefined, color: string) => (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 4 }}>
      <span style={{ ...mono, fontSize: 10, color, textAlign: 'right' }}>{fmt(s?.beta)}</span>
      <span style={{ ...mono, fontSize: 10, color: '#6f7d8c', textAlign: 'right' }}>{fmt(s?.r2, 4)}</span>
      <span style={{ ...mono, fontSize: 10, color: 'var(--amr-text-dim)', textAlign: 'right' }}>{s?.n ?? '—'}</span>
    </div>
  );

  return (
    <div style={{ display: 'flex', height: '100%', background: '#070b10' }}>
      {/* Left: δ vs price (Surface 2) */}
      <div style={{ flex: '0 0 58%', minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 14, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', letterSpacing: '0.14em', textTransform: 'uppercase' }}>Velocity Contribution δ vs Price</span>
          <span style={{ ...mono, fontSize: 9, color: 'rgba(216,166,87,0.9)' }}>δ (left)</span>
          <span style={{ ...mono, fontSize: 9, color: 'rgba(140,160,180,0.6)' }}>price (right)</span>
          {loading && <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>loading</span>}
          {error && <span style={{ ...mono, fontSize: 9, color: '#f85149' }}>{error}</span>}
        </div>
        <div ref={chartRef} style={{ flex: 1, minHeight: 0 }} />
        <div style={{ flexShrink: 0, padding: '4px 12px', background: '#06090e', borderTop: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 8, color: '#1e2833', lineHeight: 1.5 }}>
            δ = μ_Kalman(pred) − EMA_match(pred): the equilibrium movement the velocity state adds over a matched-responsiveness EMA. Qualitative read: trend-following drift removal vs absorption of reversion swings.
          </span>
        </div>
      </div>

      {/* Right: decay table (Surface 1) + raw Δβ (Surface 3) */}
      <div style={{ flex: '0 0 42%', minWidth: 0, borderLeft: '1px solid #0e1520', display: 'flex', flexDirection: 'column', background: '#070b10', overflowY: 'auto' }}>
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 10, gap: 8, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>Predictive Decay (walk-forward, OOS)</span>
        </div>

        {/* Surface 1 */}
        <div style={{ padding: '8px 10px', borderBottom: '1px solid #161d27' }}>
          {data && k && r ? (
            <>
              <div style={{ ...mono, fontSize: 8, color: '#1e2833', marginBottom: 4 }}>
                β = train-half slope (β&lt;0 ⇒ snapback) · R² = out-of-sample · n = test pairs
              </div>
              {data.horizons.map(h => (
                <div key={h} style={{ marginBottom: 8 }}>
                  <div style={{ ...mono, fontSize: 9, color: '#6f7d8c', marginBottom: 2 }}>horizon h = {h}</div>
                  <div style={{ display: 'grid', gridTemplateColumns: '0.9fr 1fr 1fr 1fr', gap: 4, paddingBottom: 2, borderBottom: '1px solid #0a0f16' }}>
                    <span style={{ ...mono, fontSize: 8, color: '#1e2833' }} />
                    <span style={{ ...mono, fontSize: 8, color: '#1e2833', textAlign: 'right' }}>β</span>
                    <span style={{ ...mono, fontSize: 8, color: '#1e2833', textAlign: 'right' }}>R²ₒₒₛ</span>
                    <span style={{ ...mono, fontSize: 8, color: '#1e2833', textAlign: 'right' }}>n</span>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '0.9fr 3fr', gap: 4, padding: '2px 0' }}>
                    <span style={{ ...mono, fontSize: 9, color: KAL_COLOR }}>Kalman</span>
                    {cell(k[h], KAL_COLOR)}
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '0.9fr 3fr', gap: 4, padding: '2px 0' }}>
                    <span style={{ ...mono, fontSize: 9, color: RES_COLOR }}>Restored</span>
                    {cell(r[h], RES_COLOR)}
                  </div>
                </div>
              ))}
            </>
          ) : (
            <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>—</span>
          )}
        </div>

        {/* Surface 3 — raw Δβ, no verdict */}
        <div style={{ padding: '8px 10px', borderBottom: '1px solid #161d27' }}>
          <div style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 6 }}>Δβ = β(Restored) − β(Kalman)</div>
          {dbeta ? (
            <>
              {dbeta.map(({ h, d }) => (
                <div key={h} style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr 1fr', gap: 4, padding: '2px 0', borderBottom: '1px solid #0a0f16' }}>
                  <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)' }}>h = {h}</span>
                  <span style={{ ...mono, fontSize: 10, color: '#8b99a8', textAlign: 'right' }}>{fmt(d)}</span>
                  <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', textAlign: 'right' }}>{d == null ? '—' : d < 0 ? 'restored↓' : d > 0 ? 'kalman↓' : 'flat'}</span>
                </div>
              ))}
              <div style={{ marginTop: 6, display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ ...mono, fontSize: 8, color: '#1e2833' }}>direction consistent across horizons</span>
                <span style={{ ...mono, fontSize: 9, color: '#6f7d8c' }}>{consistentDir == null ? '—' : consistentDir ? 'yes' : 'no'}</span>
              </div>
              <div style={{ ...mono, fontSize: 8, color: '#1e2833', lineHeight: 1.5, marginTop: 6 }}>
                Δβ &lt; 0 ⇒ restored (velocity-OFF) shows stronger snapback than Kalman. Raw magnitudes only — interpretation is manual at this step (no verdict engine).
              </div>
            </>
          ) : (
            <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>—</span>
          )}
        </div>

        {/* Meta */}
        <div style={{ padding: '8px 10px' }}>
          {data && (
            <div style={{ ...mono, fontSize: 8, color: '#1e2833', lineHeight: 1.7 }}>
              matched EMA span = <span style={{ color: '#6f7d8c' }}>{data.matched_span}</span> (K∞ = {data.steady_state_gain.toFixed(4)}) · burn = {data.burn} · n = {data.n}
              <br />Matched-responsiveness EMA isolates the velocity contribution from a speed gap. Window-independent.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
