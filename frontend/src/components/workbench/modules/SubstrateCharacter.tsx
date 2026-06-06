'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import {
  createChart, ColorType, CrosshairMode,
  type IChartApi, type ISeriesApi, type Time,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import type { ModuleProps } from '../types';
import type { SubstrateResponse, SubstrateRow } from '@/lib/types';

// Substrate Observatory — "what kind of market are we looking at?" (docs/research/10).
// OBSERVATORY DIAGNOSTIC: instrument CHARACTER over a trailing window, observe/falsify, NOT a signal.
// CHARACTER, NOT TIMING — never "a regime is igniting" (that is State T detection, frozen).
// UI posture (this session's decision): DESCRIPTORS-FIRST. The raw descriptors (DE, VR, VP) are the
// primary read; the resemblance scores are computed but kept subordinate behind a toggle, so the
// human reads the evidence before the archetype label and cannot mistake a soft score for detection.
// Causal-only (full-information deferred — no genuine future-using descriptor yet).

// v1 trailing window for descriptors (its own constant — NOT the global EMA span, which means
// something different). The dateRange.end replay boundary still firewalls the data (replay-compatible).
const SUBSTRATE_WINDOW = 120;

const C_DE = 'rgba(120,200,140,0.95)';      // directional efficiency
const C_VR = 'rgba(216,166,87,0.9)';        // variance ratio
const C_PRICE = 'rgba(140,160,180,0.4)';
const C_REF = 'rgba(255,255,255,0.10)';     // VR=1 / RW reference

const BUCKET_META: Record<string, { label: string; color: string; hint: string }> = {
  trend_like: { label: 'Trend-like', color: '#d8a657', hint: 'straight path (high DE)' },
  ou_like: { label: 'OU-like', color: '#5a8fb8', hint: 'choppy & sub-diffusive (VR<1)' },
  rw_null: { label: 'RW-Null', color: '#6f7d8c', hint: 'choppy & diffuses like a random walk' },
  ambiguous: { label: 'Ambiguous', color: '#8f7ab8', hint: 'no archetype dominates' },
};

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

function fmt(n: number | null | undefined, d = 2) {
  return n == null || !Number.isFinite(n) ? '—' : n.toFixed(d);
}

// horizontal [0,1] resemblance bar
function ScoreBar({ label, value, color, hint }: { label: string; value: number | null; color: string; hint?: string }) {
  const pct = value == null || !Number.isFinite(value) ? 0 : Math.max(0, Math.min(1, value)) * 100;
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '72px 1fr 36px', gap: 6, alignItems: 'center', padding: '1px 0' }}>
      <span style={{ ...mono, fontSize: 9, color: '#8b99a8' }} title={hint}>{label}</span>
      <div style={{ height: 6, background: '#0e1520', borderRadius: 1, overflow: 'hidden' }}>
        <div style={{ width: `${pct}%`, height: '100%', background: value == null ? '#1e2833' : color }} />
      </div>
      <span style={{ ...mono, fontSize: 9, color: '#8b99a8', textAlign: 'right' }}>{fmt(value, 2)}</span>
    </div>
  );
}

export function SubstrateCharacter({ instrumentId, dateRange }: ModuleProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chart = useRef<IChartApi | null>(null);
  const deS = useRef<ISeriesApi<'Line'> | null>(null);
  const vrS = useRef<ISeriesApi<'Line'> | null>(null);
  const refS = useRef<ISeriesApi<'Line'> | null>(null);
  const priceS = useRef<ISeriesApi<'Line'> | null>(null);

  const [data, setData] = useState<SubstrateResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hoverDate, setHoverDate] = useState<string | null>(null);
  const [showScores, setShowScores] = useState(false);  // descriptors-first: scores collapsed by default

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
    refS.current = c.addLineSeries({ color: C_REF, lineWidth: 1, lineStyle: 2, priceScaleId: 'left', lastValueVisible: false, priceLineVisible: false });
    vrS.current = c.addLineSeries({ color: C_VR, lineWidth: 1, priceScaleId: 'left', lastValueVisible: false, priceLineVisible: false, title: 'VR' });
    deS.current = c.addLineSeries({ color: C_DE, lineWidth: 2, priceScaleId: 'left', lastValueVisible: false, priceLineVisible: false, title: 'DE' });
    chart.current = c;

    const onMove = (param: { time?: Time }) => setHoverDate(param.time ? String(param.time) : null);
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
    api.getSubstrate(instrumentId, SUBSTRATE_WINDOW, dateRange.start ?? undefined, dateRange.end ?? undefined)
      .then((resp) => {
        if (cancelled) return;
        setData(resp);
        const t = (d: string) => d as Time;
        priceS.current?.setData(resp.rows.map(r => ({ time: t(r.date), value: r.close })));
        deS.current?.setData(resp.rows.filter(r => r.de != null).map(r => ({ time: t(r.date), value: r.de as number })));
        vrS.current?.setData(resp.rows.filter(r => r.vr != null).map(r => ({ time: t(r.date), value: r.vr as number })));
        refS.current?.setData(resp.rows.map(r => ({ time: t(r.date), value: 1.0 })));  // VR=1 / RW reference
        chart.current?.timeScale().fitContent();
      })
      .catch((e: unknown) => { if (!cancelled) setError(e instanceof Error ? e.message : 'Fetch failed'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [instrumentId, dateRange.start, dateRange.end]);

  // Selected row: hovered bar, else the last scored bar.
  const row: SubstrateRow | null = useMemo(() => {
    if (!data) return null;
    if (hoverDate) {
      const h = data.rows.find(r => r.date === hoverDate);
      if (h) return h;
    }
    const scored = data.rows.filter(r => r.de != null);
    return scored.length ? scored[scored.length - 1] : (data.rows[data.rows.length - 1] ?? null);
  }, [data, hoverDate]);

  const dom = row?.dominant ? BUCKET_META[row.dominant] : null;

  return (
    <div style={{ display: 'flex', height: '100%', background: '#070b10' }}>
      {/* Left: descriptor sparklines (the PRIMARY read) over price */}
      <div style={{ flex: '0 0 58%', minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 14, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.14em', textTransform: 'uppercase' }}>Descriptors (left) vs Price (right)</span>
          <span style={{ ...mono, fontSize: 9, color: C_DE }}>DE</span>
          <span style={{ ...mono, fontSize: 9, color: C_VR }}>VR</span>
          <span style={{ ...mono, fontSize: 9, color: '#2d3a4a' }}>— VR=1 (RW)</span>
          {loading && <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>loading</span>}
          {error && <span style={{ ...mono, fontSize: 9, color: '#f85149' }}>{error}</span>}
        </div>
        <div ref={chartRef} style={{ flex: 1, minHeight: 0 }} />
        {data?.data_warning && (
          <div style={{ flexShrink: 0, padding: '5px 12px', background: '#1a0d0d', borderTop: '1px solid #5a1f1f' }}>
            <span style={{ ...mono, fontSize: 8, color: '#f0857a', lineHeight: 1.5 }}>⛔ {data.data_warning}</span>
          </div>
        )}
        <div style={{ flexShrink: 0, padding: '5px 12px', background: '#13100a', borderTop: '1px solid #3a2f12' }}>
          <span style={{ ...mono, fontSize: 8, color: '#b8893a', lineHeight: 1.5 }}>
            ⚠ {data?.regime_warning ?? 'Observatory diagnostic — character, not timing. Not a signal.'}
          </span>
        </div>
      </div>

      {/* Right: as-of-bar read — descriptors first, resemblance scores subordinate */}
      <div style={{ flex: '0 0 42%', minWidth: 0, borderLeft: '1px solid #0e1520', display: 'flex', flexDirection: 'column', background: '#070b10', overflowY: 'auto' }}>
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 10px', background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: '#2d3a4a', letterSpacing: '0.12em', textTransform: 'uppercase' }}>Character (as-of bar)</span>
          <span style={{ ...mono, fontSize: 9, color: '#6f7d8c' }}>{row?.date ?? '—'}{hoverDate ? '' : ' (latest)'}</span>
        </div>

        {/* Warmup / incompatibility — never a silent blank */}
        {data && data.stats.n_scored === 0 && (
          <div style={{ padding: '10px', borderBottom: '1px solid #161d27' }}>
            <span style={{ ...mono, fontSize: 10, color: data.data_warning ? '#f0857a' : '#b8893a', lineHeight: 1.6 }}>
              {data.data_warning
                ? 'No read: instrument is structurally incompatible (see banner). Not an unfavorable reading.'
                : `No characterized bars yet — warming up. Needs the full trailing window (${SUBSTRATE_WINDOW} bars) before the cursor. Scored ${data.stats.n_scored}/${data.stats.n}; widen the range or step the cursor later.`}
            </span>
          </div>
        )}

        {/* PRIMARY: descriptor cards */}
        <div style={{ padding: '10px', borderBottom: '1px solid #161d27' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 4 }}>
            {[
              { k: 'DE', v: fmt(row?.de, 2), hint: '|net|/path · 1=straight, ~0=chop' },
              { k: 'VR', v: fmt(row?.vr, 2), hint: '<1 MR · ≈1 RW · >1 momentum' },
              { k: 'VolPct', v: row?.vp == null ? '—' : `${fmt(row?.vp, 0)}`, hint: 'vol rank (context only)' },
            ].map(c => (
              <div key={c.k} style={{ background: '#090d13', border: '1px solid #161d27', borderRadius: 2, padding: '6px 7px' }}>
                <div style={{ ...mono, fontSize: 8, color: '#2d3a4a' }}>{c.k}</div>
                <div style={{ ...mono, fontSize: 18, color: '#8b99a8' }}>{c.v}</div>
                <div style={{ ...mono, fontSize: 7, color: '#1e2833', lineHeight: 1.3 }}>{c.hint}</div>
              </div>
            ))}
          </div>
          <div style={{ ...mono, fontSize: 8, color: '#1e2833', marginTop: 6, lineHeight: 1.5 }}>
            directional efficiency carries the trend↔chop axis; the variance ratio splits OU vs RW within
            the chop. Vol percentile is context, never a character driver (doc 10 §map).
          </div>
        </div>

        {/* SUBORDINATE: resemblance scores behind a toggle (descriptors-first) */}
        <div style={{ padding: '8px 10px' }}>
          <button
            onClick={() => setShowScores(s => !s)}
            style={{ ...mono, fontSize: 9, color: '#6f7d8c', background: 'transparent', border: 'none', cursor: 'pointer', padding: 0, display: 'flex', alignItems: 'center', gap: 6 }}
          >
            <span style={{ color: '#2d3a4a' }}>{showScores ? '▾' : '▸'}</span>
            Resemblance
            {dom && (
              <span style={{ color: dom.color }}>
                {dom.label}<span style={{ color: '#2d3a4a' }}> · {row?.confidence ?? '—'}</span>
              </span>
            )}
          </button>

          {showScores && (
            <div style={{ marginTop: 8 }}>
              <div style={{ ...mono, fontSize: 8, color: '#1e2833', marginBottom: 5, lineHeight: 1.5 }}>
                resemblance over the window, not a probability and not an event — independent scores in [0,1].
              </div>
              <ScoreBar label="Trend-like" value={row?.trend_like ?? null} color={BUCKET_META.trend_like.color} hint={BUCKET_META.trend_like.hint} />
              <ScoreBar label="OU-like" value={row?.ou_like ?? null} color={BUCKET_META.ou_like.color} hint={BUCKET_META.ou_like.hint} />
              <ScoreBar label="RW-Null" value={row?.rw_null ?? null} color={BUCKET_META.rw_null.color} hint={BUCKET_META.rw_null.hint} />
              <ScoreBar label="Ambiguous" value={row?.ambiguous ?? null} color={BUCKET_META.ambiguous.color} hint={BUCKET_META.ambiguous.hint} />
            </div>
          )}

          {data && (
            <div style={{ ...mono, fontSize: 8, color: '#1e2833', lineHeight: 1.7, marginTop: 10 }}>
              mode = <span style={{ color: '#6f7d8c' }}>{data.mode}</span> (full-information deferred)
              <br />window = {data.window} bars (trailing) · characterized {data.stats.n_scored}/{data.stats.n}
              <br />map frozen & transparent — monotone in (DE, VR), never fit (doc 10)
              <br />exhaustion / etiology excluded — episode timing belongs to State T
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
