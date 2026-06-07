'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import {
  createChart, ColorType, CrosshairMode,
  type IChartApi, type ISeriesApi, type Time,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import type { ModuleProps } from '../types';
import type { DiagnosticsResponse, DiagnosticsRow } from '@/lib/types';

// Research comparison module (Step 1 — controlled real-market integration).
// Question under test: does the SYNTHETIC trend-centering advantage of Kalman μ* survive real
// markets? EMA innovation carries a deterministic lag bias (slope·span/2) inside a trend; the
// Kalman velocity state should null it. This module makes that falsifiable on real data.
//
// NOT a redesign: reuses the existing /diagnostics endpoint (which now carries both estimators)
// and the shared replay window. EMA stays the production μ*; Kalman is shown alongside only.

const EMA_COLOR = 'rgba(88,166,255,0.85)';    // dim blue  — production EMA
const KAL_COLOR = 'rgba(255,180,60,0.9)';     // amber     — Kalman research estimator
const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};
function fmt(n: number | null | undefined, d = 3) {
  return n == null || !Number.isFinite(n) ? '—' : n.toFixed(d);
}

// ── Centering metrics — computed client-side, no backend bloat (Step 2 stayed minimal) ──
interface Centering {
  emaAbsMean: number; kalAbsMean: number;
  emaStd: number; kalStd: number;
  emaFracPos: number; kalFracPos: number;      // balance: 0.5 = perfectly centered
  emaCrossRate: number; kalCrossRate: number;  // zero-crossings / n: low = sign-persistent (biased)
  emaMaxRun: number; kalMaxRun: number;        // longest single-sign run (bars): sign persistence
  kalmanEffSpan: number | null;                // 2/gain_∞ − 1, for fair-comparison guidance
}

function signRuns(vals: number[]): { crossRate: number; maxRun: number } {
  if (vals.length < 2) return { crossRate: 0, maxRun: vals.length };
  let crosses = 0, run = 1, maxRun = 1;
  for (let i = 1; i < vals.length; i++) {
    const a = vals[i - 1] >= 0, b = vals[i] >= 0;
    if (a === b) { run++; if (run > maxRun) maxRun = run; }
    else { crosses++; run = 1; }
  }
  return { crossRate: crosses / (vals.length - 1), maxRun };
}

function computeCentering(rows: DiagnosticsRow[]): Centering {
  const ema = rows.map(r => r.epsilon);
  const kal = rows.map(r => r.epsilon_kalman);
  const mean = (a: number[]) => a.reduce((s, x) => s + x, 0) / (a.length || 1);
  const std = (a: number[]) => {
    const m = mean(a);
    return Math.sqrt(a.reduce((s, x) => s + (x - m) ** 2, 0) / (a.length || 1));
  };
  const fracPos = (a: number[]) => a.filter(x => x > 0).length / (a.length || 1);
  const er = signRuns(ema), kr = signRuns(kal);
  const lastGain = rows.length ? rows[rows.length - 1].kalman_gain : 0;
  const effSpan = lastGain > 0 && lastGain < 1 ? 2 / lastGain - 1 : null;
  return {
    emaAbsMean: Math.abs(mean(ema)), kalAbsMean: Math.abs(mean(kal)),
    emaStd: std(ema), kalStd: std(kal),
    emaFracPos: fracPos(ema), kalFracPos: fracPos(kal),
    emaCrossRate: er.crossRate, kalCrossRate: kr.crossRate,
    emaMaxRun: er.maxRun, kalMaxRun: kr.maxRun,
    kalmanEffSpan: effSpan,
  };
}

function rollingMean(vals: number[], win: number): number[] {
  const out = new Array(vals.length).fill(0);
  let acc = 0;
  for (let i = 0; i < vals.length; i++) {
    acc += vals[i];
    if (i >= win) acc -= vals[i - win];
    out[i] = acc / Math.min(i + 1, win);
  }
  return out;
}

export function EstimatorCompare({ instrumentId, dateRange, window: win }: ModuleProps) {
  const overlayRef = useRef<HTMLDivElement>(null);
  const residRef = useRef<HTMLDivElement>(null);
  const overlayChart = useRef<IChartApi | null>(null);
  const residChart = useRef<IChartApi | null>(null);
  const priceS = useRef<ISeriesApi<'Line'> | null>(null);
  const emaMuS = useRef<ISeriesApi<'Line'> | null>(null);
  const kalMuS = useRef<ISeriesApi<'Line'> | null>(null);
  const emaEpsS = useRef<ISeriesApi<'Line'> | null>(null);
  const kalEpsS = useRef<ISeriesApi<'Line'> | null>(null);
  const emaRollS = useRef<ISeriesApi<'Line'> | null>(null);
  const kalRollS = useRef<ISeriesApi<'Line'> | null>(null);

  const [data, setData] = useState<DiagnosticsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // ── Chart setup ──
  useEffect(() => {
    if (!overlayRef.current || !residRef.current) return;
    const base = {
      layout: { background: { type: ColorType.Solid, color: '#070b10' }, textColor: '#3d4d5e', fontSize: 10 },
      grid: { vertLines: { color: '#0e1520' }, horzLines: { color: '#0e1520' } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: '#161d27' },
      timeScale: { borderColor: '#161d27' },
    };
    const oc = createChart(overlayRef.current, { ...base, width: overlayRef.current.clientWidth, height: overlayRef.current.clientHeight });
    const rc = createChart(residRef.current, { ...base, width: residRef.current.clientWidth, height: residRef.current.clientHeight });
    priceS.current = oc.addLineSeries({ color: 'rgba(140,160,180,0.35)', lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 'price' });
    emaMuS.current = oc.addLineSeries({ color: EMA_COLOR, lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 'μ* EMA' });
    kalMuS.current = oc.addLineSeries({ color: KAL_COLOR, lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 'μ* Kalman' });
    emaEpsS.current = rc.addLineSeries({ color: EMA_COLOR, lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 'ε EMA' });
    kalEpsS.current = rc.addLineSeries({ color: KAL_COLOR, lineWidth: 1, lastValueVisible: false, priceLineVisible: false, title: 'ε Kalman' });
    emaRollS.current = rc.addLineSeries({ color: 'rgba(88,166,255,0.35)', lineWidth: 2, lineStyle: 2, lastValueVisible: false, priceLineVisible: false });
    kalRollS.current = rc.addLineSeries({ color: 'rgba(255,180,60,0.4)', lineWidth: 2, lineStyle: 2, lastValueVisible: false, priceLineVisible: false });
    overlayChart.current = oc; residChart.current = rc;

    // Synchronized replay: keep both time scales locked together.
    const syncFrom = (src: IChartApi, dst: IChartApi) => src.timeScale().subscribeVisibleLogicalRangeChange((r) => {
      if (r) dst.timeScale().setVisibleLogicalRange(r);
    });
    syncFrom(oc, rc); syncFrom(rc, oc);

    const ro = new ResizeObserver(() => {
      if (overlayRef.current) oc.applyOptions({ width: overlayRef.current.clientWidth, height: overlayRef.current.clientHeight });
      if (residRef.current) rc.applyOptions({ width: residRef.current.clientWidth, height: residRef.current.clientHeight });
    });
    ro.observe(overlayRef.current); ro.observe(residRef.current);
    return () => { ro.disconnect(); oc.remove(); rc.remove(); overlayChart.current = null; residChart.current = null; };
  }, []);

  // ── Data ──
  useEffect(() => {
    setError(null);
    if (!instrumentId) return;
    let cancelled = false;
    setLoading(true);
    api.getDiagnostics(instrumentId, win, dateRange.start ?? undefined, dateRange.end ?? undefined)
      .then((resp) => {
        if (cancelled) return;
        setData(resp);
        const t = (d: string) => d as Time;
        const rows = resp.rows;
        priceS.current?.setData(rows.map(r => ({ time: t(r.date), value: r.close })));
        emaMuS.current?.setData(rows.map(r => ({ time: t(r.date), value: r.mu_star })));
        kalMuS.current?.setData(rows.map(r => ({ time: t(r.date), value: r.mu_star_kalman })));
        emaEpsS.current?.setData(rows.map(r => ({ time: t(r.date), value: r.epsilon })));
        kalEpsS.current?.setData(rows.map(r => ({ time: t(r.date), value: r.epsilon_kalman })));
        const emaRoll = rollingMean(rows.map(r => r.epsilon), win);
        const kalRoll = rollingMean(rows.map(r => r.epsilon_kalman), win);
        emaRollS.current?.setData(rows.map((r, i) => ({ time: t(r.date), value: emaRoll[i] })));
        kalRollS.current?.setData(rows.map((r, i) => ({ time: t(r.date), value: kalRoll[i] })));
        overlayChart.current?.timeScale().fitContent();
        residChart.current?.timeScale().fitContent();
      })
      .catch((e: unknown) => { if (!cancelled) setError(e instanceof Error ? e.message : 'Fetch failed'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [instrumentId, dateRange.start, dateRange.end, win]); // eslint-disable-line react-hooks/exhaustive-deps

  const c = useMemo(() => (data && data.rows.length ? computeCentering(data.rows) : null), [data]);

  // Centering verdict (descriptive, not a pass/fail gate — this is falsification, not scoring).
  const verdict = useMemo(() => {
    if (!c) return null;
    const ratio = c.emaAbsMean / (c.kalAbsMean || 1e-9);
    const spanMismatch = c.kalmanEffSpan != null && Math.abs(c.kalmanEffSpan - win) / win > 0.5;
    if (ratio > 3) return { tone: '#3fb950', text: `Kalman ε is ${ratio.toFixed(1)}× more centered than EMA ε — consistent with trend-bias removal.` };
    if (ratio < 1) return { tone: '#f85149', text: `EMA ε is more centered than Kalman here — synthetic advantage NOT reproduced in this window.` };
    return { tone: '#d8a657', text: `Centering comparable (${ratio.toFixed(2)}×)${spanMismatch ? ' — likely a sideways window or span mismatch.' : '.'}` };
  }, [c, win]);

  const row = (label: string, ema: string, kal: string, kalBetter?: boolean) => (
    <div key={label} style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr 1fr', gap: 4, padding: '2px 0', borderBottom: '1px solid #0a0f16' }}>
      <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)' }}>{label}</span>
      <span style={{ ...mono, fontSize: 10, color: '#6f7d8c', textAlign: 'right' }}>{ema}</span>
      <span style={{ ...mono, fontSize: 10, color: kalBetter ? '#3fb950' : '#d8a657', textAlign: 'right' }}>{kal}</span>
    </div>
  );

  return (
    <div style={{ display: 'flex', height: '100%', background: '#070b10' }}>
      {/* Left: stacked overlay + residual charts */}
      <div style={{ flex: '0 0 64%', minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 16, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', letterSpacing: '0.14em', textTransform: 'uppercase' }}>Estimator Compare — μ* overlay</span>
          <span style={{ ...mono, fontSize: 9, color: EMA_COLOR }}>EMA-{win}</span>
          <span style={{ ...mono, fontSize: 9, color: KAL_COLOR }}>Kalman (frozen)</span>
          {loading && <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>loading</span>}
          {error && <span style={{ ...mono, fontSize: 9, color: '#f85149' }}>{error}</span>}
        </div>
        <div ref={overlayRef} style={{ flex: 1, minHeight: 0 }} />
        <div style={{ height: 22, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 12, gap: 12, background: '#06090e', borderTop: '1px solid #0e1520', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase' }}>Residual ε (dashed = rolling mean, window {win}) — flat-on-zero = centered</span>
        </div>
        <div ref={residRef} style={{ flex: 1, minHeight: 0 }} />
      </div>

      {/* Right: centering panel — the thesis test */}
      <div style={{ flex: '0 0 36%', minWidth: 0, borderLeft: '1px solid #0e1520', display: 'flex', flexDirection: 'column', background: '#070b10' }}>
        <div style={{ height: 26, flexShrink: 0, display: 'flex', alignItems: 'center', paddingLeft: 10, gap: 8, background: '#090d13', borderBottom: '1px solid #0e1520' }}>
          <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>Centering Panel</span>
        </div>

        <div style={{ flex: 1, minHeight: 0, overflowY: 'auto', padding: '8px 10px' }}>
          {c ? (
            <>
              <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr 1fr', gap: 4, padding: '2px 0', borderBottom: '1px solid #161d27', marginBottom: 2 }}>
                <span style={{ ...mono, fontSize: 8, color: '#1e2833', textTransform: 'uppercase' }}>metric</span>
                <span style={{ ...mono, fontSize: 8, color: EMA_COLOR, textAlign: 'right' }}>EMA</span>
                <span style={{ ...mono, fontSize: 8, color: KAL_COLOR, textAlign: 'right' }}>Kalman</span>
              </div>
              {row('|mean ε|', fmt(c.emaAbsMean, 3), fmt(c.kalAbsMean, 3), c.kalAbsMean < c.emaAbsMean)}
              {row('std ε', fmt(c.emaStd, 3), fmt(c.kalStd, 3))}
              {row('|mean|/std', fmt(c.emaAbsMean / (c.emaStd || 1), 3), fmt(c.kalAbsMean / (c.kalStd || 1), 3), (c.kalAbsMean / (c.kalStd || 1)) < (c.emaAbsMean / (c.emaStd || 1)))}
              {row('frac ε>0', fmt(c.emaFracPos, 3), fmt(c.kalFracPos, 3), Math.abs(c.kalFracPos - 0.5) < Math.abs(c.emaFracPos - 0.5))}
              {row('0-cross rate', fmt(c.emaCrossRate, 3), fmt(c.kalCrossRate, 3), c.kalCrossRate > c.emaCrossRate)}
              {row('max sign run', String(c.emaMaxRun), String(c.kalMaxRun), c.kalMaxRun < c.emaMaxRun)}

              {verdict && (
                <div style={{ marginTop: 10, padding: '8px 8px', background: '#06090e', border: `1px solid ${verdict.tone}33`, borderRadius: 3 }}>
                  <div style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 4 }}>Reading</div>
                  <div style={{ ...mono, fontSize: 9, color: verdict.tone, lineHeight: 1.5 }}>{verdict.text}</div>
                </div>
              )}

              <div style={{ marginTop: 10, padding: '6px 8px', background: '#06090e', border: '1px solid #0e1520', borderRadius: 3 }}>
                <div style={{ ...mono, fontSize: 8, color: 'var(--amr-text-dim)', lineHeight: 1.6 }}>
                  Kalman effective span ≈ <span style={{ color: '#8b99a8' }}>{c.kalmanEffSpan != null ? c.kalmanEffSpan.toFixed(0) : '—'}</span> bars.
                  {' '}For a fair centering comparison set the EMA window near this — otherwise responsiveness, not the velocity state, drives the difference.
                </div>
              </div>

              <div style={{ marginTop: 8, padding: '6px 8px' }}>
                <div style={{ ...mono, fontSize: 8, color: '#1e2833', lineHeight: 1.6 }}>
                  Thesis test (doc 06): inside a trend, EMA ε inherits a deterministic offset slope·span/2 — long single-sign runs, |mean ε| ≫ 0. A centered Kalman ε crosses zero often and stays near zero. <span style={{ color: '#6f4a4a' }}>Failure mode to watch: a violent regime change where velocity FALSELY centers ε by absorbing a real displacement.</span>
                </div>
              </div>
            </>
          ) : (
            <span style={{ ...mono, fontSize: 9, color: '#1e2833' }}>—</span>
          )}
        </div>
      </div>
    </div>
  );
}
