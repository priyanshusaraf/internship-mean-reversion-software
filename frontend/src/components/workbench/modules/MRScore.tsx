'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import {
  createChart, ColorType, CrosshairMode,
  type IChartApi, type ISeriesApi, type Time,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import type { ModuleProps } from '../types';
import type { MRScoreResponse, MRScoreRow } from '@/lib/types';

// MRScore — Mean Reversion Favorability (doc 01 §3, eq. 13–34), OBSERVATORY DIAGNOSTIC.
// observe/falsify, NOT a signal. Causal-only (full-information deferred — no genuine future μ* yet).
// Two reads are surfaced deliberately:
//   • the self-ranked MRScore (within-instrument, relative-to-recent-history) — the spec's score;
//   • the RAW Block-2 features (DRC / hit-rate / VR) — the artifact-resistant CROSS-instrument
//     discriminators. The self-ranked score does NOT separate reverters from nulls; the raw ones do.
// No verdict/threshold language anywhere (no "entry", no MRScore>θ). Interpretation is manual.

const C_SCORE = 'rgba(120,200,140,0.95)';   // MRScore
const C_B2 = 'rgba(216,166,87,0.85)';       // B2 (the 60% driver)
const C_PRICE = 'rgba(140,160,180,0.4)';
const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

function fmt(n: number | null | undefined, d = 1) {
  return n == null || !Number.isFinite(n) ? '—' : n.toFixed(d);
}
function fmtSigned(n: number | null | undefined, d = 2) {
  return n == null || !Number.isFinite(n) ? '—' : (n >= 0 ? '+' : '') + n.toFixed(d);
}

// horizontal [0,100] rank bar
function RankBar({ label, value, color = '#6f7d8c' }: { label: string; value: number | null; color?: string }) {
  const pct = value == null || !Number.isFinite(value) ? 0 : Math.max(0, Math.min(100, value));
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '64px 1fr 34px', gap: 6, alignItems: 'center', padding: '1px 0' }}>
      <span style={{ ...mono, fontSize: 9, color: '#6f7d8c' }}>{label}</span>
      <div style={{ height: 6, background: '#0e1520', borderRadius: 1, overflow: 'hidden' }}>
        <div style={{ width: `${pct}%`, height: '100%', background: value == null ? '#1e2833' : color }} />
      </div>
      <span style={{ ...mono, fontSize: 9, color: '#8b99a8', textAlign: 'right' }}>{fmt(value, 0)}</span>
    </div>
  );
}

export function MRScore({ instrumentId, dateRange, window }: ModuleProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chart = useRef<IChartApi | null>(null);
  const scoreS = useRef<ISeriesApi<'Line'> | null>(null);
  const b2S = useRef<ISeriesApi<'Line'> | null>(null);
  const priceS = useRef<ISeriesApi<'Line'> | null>(null);
  const midS = useRef<ISeriesApi<'Line'> | null>(null);

  const [data, setData] = useState<MRScoreResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hoverDate, setHoverDate] = useState<string | null>(null);

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
    priceS.current = c.addLineSeries({ color: C_PRICE, lineWidth: 1, priceScaleId: 'right', lastValueVisible: false, priceLineVisible: false, title: 'price' });
    midS.current = c.addLineSeries({ color: 'rgba(255,255,255,0.10)', lineWidth: 1, lineStyle: 2, priceScaleId: 'left', lastValueVisible: false, priceLineVisible: false });
    b2S.current = c.addLineSeries({ color: C_B2, lineWidth: 1, priceScaleId: 'left', lastValueVisible: false, priceLineVisible: false, title: 'B2' });
    scoreS.current = c.addLineSeries({ color: C_SCORE, lineWidth: 2, priceScaleId: 'left', lastValueVisible: false, priceLineVisible: false, title: 'MRScore' });
    // left scale autoscales over the 0–100 score/B2/midline series — no manual range needed.
    chart.current = c;

    const onMove = (param: { time?: Time }) => {
      setHoverDate(param.time ? String(param.time) : null);
    };
    c.subscribeCrosshairMove(onMove);
    const ro = new ResizeObserver(() => chartRef.current && c.applyOptions({ width: chartRef.current.clientWidth, height: chartRef.current.clientHeight }));
    ro.observe(chartRef.current);
    return () => { ro.disconnect(); c.unsubscribeCrosshairMove(onMove); c.remove(); chart.current = null; };
  }, []);

  useEffect(() => {
    setError(null);
    if (!instrumentId) return;
    let cancelled = false;
    setLoading(true);
    api.getMRScore(instrumentId, window, dateRange.start ?? undefined, dateRange.end ?? undefined)
      .then((resp) => {
        if (cancelled) return;
        setData(resp);
        const t = (d: string) => d as Time;
        priceS.current?.setData(resp.rows.map(r => ({ time: t(r.date), value: r.close })));
        scoreS.current?.setData(resp.rows.filter(r => r.mrscore != null).map(r => ({ time: t(r.date), value: r.mrscore as number })));
        b2S.current?.setData(resp.rows.filter(r => r.b2 != null).map(r => ({ time: t(r.date), value: r.b2 as number })));
        midS.current?.setData(resp.rows.map(r => ({ time: t(r.date), value: 50 })));
        chart.current?.timeScale().fitContent();
      })
      .catch((e: unknown) => { if (!cancelled) setError(e instanceof Error ? e.message : 'Fetch failed'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [instrumentId, window, dateRange.start, dateRange.end]);

  // Selected row: hovered bar, else the last scored bar.
  const row: MRScoreRow | null = useMemo(() => {
    if (!data) return null;
    if (hoverDate) {
      const h = data.rows.find(r => r.date === hoverDate);
      if (h) return h;
    }
    const scored = data.rows.filter(r => r.mrscore != null);
    return scored.length ? scored[scored.length - 1] : (data.rows[data.rows.length - 1] ?? null);
  }, [data, hoverDate]);

  // Weighted block contributions to the master score (sum = MRScore).
  const contrib = useMemo(() => {
    if (!row || !data) return null;
    const w = data.weights;
    return {
      b1: row.b1 != null ? row.b1 * w.b1 : null,
      b2: row.b2 != null ? row.b2 * w.b2 : null,
      b3: row.b3 != null ? row.b3 * w.b3 : null,
    };
  }, [row, data]);

  return (
    <div style={{ display: 'flex', height: '100%', background: '#070b10' }}>
      {/* Left: MRScore(t) + B2 vs price */}
      <div style={{ flex: '0 0 58%', minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 14, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', letterSpacing: '0.14em', textTransform: 'uppercase' }}>MRScore (left, 0–100) vs Price (right)</span>
          <span style={{ ...mono, fontSize: 9, color: C_SCORE }}>MRScore</span>
          <span style={{ ...mono, fontSize: 9, color: C_B2 }}>B2</span>
          {loading && <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>loading</span>}
          {error && <span style={{ ...mono, fontSize: 9, color: '#f85149' }}>{error}</span>}
        </div>
        <div ref={chartRef} style={{ flex: 1, minHeight: 0 }} />
        {/* Structural-incompatibility banner (e.g. non-positive / spread prices) — red, distinct from the gate */}
        {data?.data_warning && (
          <div style={{ flexShrink: 0, padding: '5px 12px', background: '#1a0d0d', borderTop: '1px solid #5a1f1f' }}>
            <span style={{ ...mono, fontSize: 8, color: '#f0857a', lineHeight: 1.5 }}>⛔ {data.data_warning}</span>
          </div>
        )}
        {/* Epistemic gate — prominent, not garnish */}
        <div style={{ flexShrink: 0, padding: '5px 12px', background: '#13100a', borderTop: '1px solid #3a2f12' }}>
          <span style={{ ...mono, fontSize: 8, color: '#b8893a', lineHeight: 1.5 }}>
            ⚠ {data?.regime_warning ?? 'Observatory diagnostic — not a signal.'}
          </span>
        </div>
      </div>

      {/* Right: as-of-bar decomposition (raw, no verdict) */}
      <div style={{ flex: '0 0 42%', minWidth: 0, borderLeft: '1px solid #0e1520', display: 'flex', flexDirection: 'column', background: '#070b10', overflowY: 'auto' }}>
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 10px', background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>Decomposition</span>
          <span style={{ ...mono, fontSize: 9, color: '#6f7d8c' }}>{row?.date ?? '—'}{hoverDate ? '' : ' (latest)'}</span>
        </div>

        {/* No-score state — distinguish warmup / incompatibility from a real reading (never a silent blank) */}
        {data && data.stats.n_scored === 0 && (
          <div style={{ padding: '10px', borderBottom: '1px solid #161d27' }}>
            <span style={{ ...mono, fontSize: 10, color: data.data_warning ? '#f0857a' : '#b8893a', lineHeight: 1.6 }}>
              {data.data_warning
                ? 'No score: instrument is structurally incompatible (see banner). This is not an unfavorable reading.'
                : `No scored bars yet — warming up. MRScore needs the full estimation + rank window (~280 bars) of history before the cursor. Scored ${data.stats.n_scored}/${data.stats.n}; widen the date range or step the cursor later.`}
            </span>
          </div>
        )}

        {/* MRScore + block contributions */}
        <div style={{ padding: '10px 10px 8px', borderBottom: '1px solid #161d27' }}>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
            <span style={{ ...mono, fontSize: 26, color: C_SCORE }}>{fmt(row?.mrscore, 1)}</span>
            <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)' }}>MRScore = 0.20·B1 + 0.60·B2 + 0.20·B3</span>
          </div>
          <div style={{ marginTop: 8 }}>
            <RankBar label="B1 ·0.20" value={contrib?.b1 ?? null} color="#5a8fb8" />
            <RankBar label="B2 ·0.60" value={contrib?.b2 ?? null} color={C_B2} />
            <RankBar label="B3 ·0.20" value={contrib?.b3 ?? null} color="#8f7ab8" />
            <div style={{ ...mono, fontSize: 8, color: '#1e2833', marginTop: 3 }}>weighted contributions (sum = MRScore)</div>
          </div>
          <div style={{ display: 'flex', gap: 12, marginTop: 6 }}>
            <span style={{ ...mono, fontSize: 9, color: '#6f7d8c' }}>B1 <span style={{ color: '#8b99a8' }}>{fmt(row?.b1, 0)}</span></span>
            <span style={{ ...mono, fontSize: 9, color: '#6f7d8c' }}>B2 <span style={{ color: '#8b99a8' }}>{fmt(row?.b2, 0)}</span></span>
            <span style={{ ...mono, fontSize: 9, color: '#6f7d8c' }}>B3 <span style={{ color: '#8b99a8' }}>{fmt(row?.b3, 0)}</span></span>
          </div>
        </div>

        {/* Feature ranks by block */}
        <div style={{ padding: '8px 10px', borderBottom: '1px solid #161d27' }}>
          <div style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 4 }}>Feature ranks (0–100)</div>
          <div style={{ ...mono, fontSize: 8, color: '#5a8fb8', margin: '4px 0 1px' }}>B1 — Mean Reliability</div>
          <RankBar label="ADF" value={row?.r_adf ?? null} color="#5a8fb8" />
          <RankBar label="KPSS" value={row?.r_kpss ?? null} color="#5a8fb8" />
          <RankBar label="MSI" value={row?.r_msi ?? null} color="#5a8fb8" />
          <RankBar label="VSI" value={row?.r_vsi ?? null} color="#5a8fb8" />
          <div style={{ ...mono, fontSize: 8, color: C_B2, margin: '6px 0 1px' }}>B2 — Reversion Strength</div>
          <RankBar label="DRC" value={row?.r_drc ?? null} color={C_B2} />
          <RankBar label="HitRate" value={row?.r_hit_rate ?? null} color={C_B2} />
          <RankBar label="VR" value={row?.r_vr ?? null} color={C_B2} />
          <div style={{ ...mono, fontSize: 8, color: '#8f7ab8', margin: '6px 0 1px' }}>B3 — Tradability</div>
          <RankBar label="HL prox" value={row?.r_hl ?? null} color="#8f7ab8" />
          <RankBar label="VolComp" value={row?.r_vc ?? null} color="#8f7ab8" />
          <RankBar label="TxCost" value={row?.r_tcf ?? null} color="#8f7ab8" />
        </div>

        {/* Raw discriminators */}
        <div style={{ padding: '8px 10px' }}>
          <div style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 2 }}>Raw Block-2 (cross-instrument discriminators)</div>
          <div style={{ ...mono, fontSize: 8, color: '#1e2833', marginBottom: 5 }}>
            the self-ranked score is within-instrument relative; these raw values are what separate genuine reverters from nulls
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 4 }}>
            {[
              { k: 'DRC', v: fmtSigned(row?.drc, 2), hint: 'min_h NW-t · ≪0 = reversion' },
              { k: 'HitRate', v: fmt(row?.hit_rate, 3), hint: 'P(revert | |z|>1)' },
              { k: 'VR_agg', v: fmt(row?.vr_agg, 3), hint: '<1 = MR · ≈1 = RW' },
            ].map(c => (
              <div key={c.k} style={{ background: '#090d13', border: '1px solid #161d27', borderRadius: 2, padding: '5px 6px' }}>
                <div style={{ ...mono, fontSize: 8, color: 'var(--amr-text-dim)' }}>{c.k}</div>
                <div style={{ ...mono, fontSize: 13, color: '#8b99a8' }}>{c.v}</div>
                <div style={{ ...mono, fontSize: 7, color: '#1e2833', lineHeight: 1.3 }}>{c.hint}</div>
              </div>
            ))}
          </div>
          {data && (
            <div style={{ ...mono, fontSize: 8, color: '#1e2833', lineHeight: 1.7, marginTop: 8 }}>
              mode = <span style={{ color: '#6f7d8c' }}>{data.mode}</span> (full-information deferred — no genuine future-using μ* exists yet)
              <br />μ* = causal EMA span {data.window} · scored {data.stats.n_scored}/{data.stats.n} bars (warmup = est + rank window)
              <br />weights frozen 20/60/20 — economic priors, never fit (doc 01 §3.2)
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
