'use client';

// ── Quadrant 1 — Price chart (candlesticks + Kalman μ* + scrubber-window overlay) ─────────────────
//
// Candles for the FULL stored range. Kalman μ* overlay from GET /diagnostics (mu_star_kalman/bar).
// The scrubber window is made VISIBLE: a muted vertical line at START, an accent line at END, a
// low-opacity highlight band between them, and DIMMED candles after END (per-bar colour override —
// not a mask). Vertical lines/band/dim update only when start/end change (i.e. on scrubber RELEASE).
// No toolbar, no zoom controls.

import { useEffect, useRef, useState } from 'react';
import {
  createChart, ColorType, CrosshairMode,
  type IChartApi, type ISeriesApi, type Time, type CandlestickData, type LineData,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import { C, mono } from '@/components/observatory/ui';
import type { OHLCVBar } from '@/lib/types';

const UP = '#3fb950', DOWN = '#f85149';
const UP_DIM = 'rgba(63,185,80,0.22)', DOWN_DIM = 'rgba(248,81,73,0.22)';
const MU_WINDOW = 20; // EMA/Kalman diagnostics window (μ* overlay only — display)

interface Props {
  instrumentId: string | null;
  bars: OHLCVBar[];
  loading: boolean;       // OHLC fetch in flight (owned by the page)
  start: string | null;   // committed scrubber window (drives lines/highlight/dim)
  end: string | null;
}

export function PricePane({ instrumentId, bars, loading, start, end }: Props) {
  const hostRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candleRef = useRef<ISeriesApi<'Candlestick'> | null>(null);
  const muRef = useRef<ISeriesApi<'Line'> | null>(null);

  // overlay primitives (true vertical lines + highlight band, positioned via timeToCoordinate)
  const startLineRef = useRef<HTMLDivElement>(null);
  const endLineRef = useRef<HTMLDivElement>(null);
  const bandRef = useRef<HTMLDivElement>(null);
  const winRef = useRef<{ start: string | null; end: string | null }>({ start: null, end: null });
  winRef.current = { start, end };

  const [muLoading, setMuLoading] = useState(false);

  // ── init chart once ──
  useEffect(() => {
    if (!hostRef.current) return;
    const chart = createChart(hostRef.current, {
      layout: { background: { type: ColorType.Solid, color: C.bg }, textColor: '#3d4d5e', fontSize: 9 },
      grid: { vertLines: { color: C.borderSoft }, horzLines: { color: C.borderSoft } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: C.border },
      timeScale: { borderColor: C.border },
      handleScroll: false, handleScale: false,   // chart is driven by the scrubber, not interactive
      width: hostRef.current.clientWidth, height: hostRef.current.clientHeight,
    });
    candleRef.current = chart.addCandlestickSeries({
      upColor: UP, downColor: DOWN, wickUpColor: UP, wickDownColor: DOWN, borderVisible: false,
      priceLineVisible: false, lastValueVisible: false,
    });
    muRef.current = chart.addLineSeries({ color: C.accent, lineWidth: 1, priceLineVisible: false, lastValueVisible: false, crosshairMarkerVisible: false });
    chartRef.current = chart;

    const draw = () => drawOverlay();
    chart.timeScale().subscribeVisibleTimeRangeChange(draw);

    const ro = new ResizeObserver(() => {
      if (hostRef.current) chart.applyOptions({ width: hostRef.current.clientWidth, height: hostRef.current.clientHeight });
      draw();
    });
    ro.observe(hostRef.current);
    return () => { ro.disconnect(); chart.remove(); chartRef.current = null; candleRef.current = null; muRef.current = null; };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // ── candle data + per-bar dim after END ──
  useEffect(() => {
    if (!candleRef.current) return;
    const endT = end;
    const data: CandlestickData[] = bars
      .filter(b => Number.isFinite(b.close))
      .map(b => {
        const isUp = b.close >= b.open;
        const dim = endT != null && b.time > endT;
        const col = dim ? (isUp ? UP_DIM : DOWN_DIM) : (isUp ? UP : DOWN);
        return {
          time: b.time as Time, open: b.open, high: b.high, low: b.low, close: b.close,
          color: col, wickColor: col, borderColor: col,
        };
      });
    candleRef.current.setData(data);
    if (data.length) chartRef.current?.timeScale().fitContent();
    drawOverlay();
  }, [bars, end]);

  // ── Kalman μ* overlay (display-only; no JS math) ──
  useEffect(() => {
    if (!instrumentId) { muRef.current?.setData([]); return; }
    let cancelled = false;
    setMuLoading(true);
    api.getDiagnostics(instrumentId, MU_WINDOW)
      .then(r => {
        if (cancelled || !muRef.current) return;
        const line: LineData[] = r.rows
          .filter(row => row.mu_star_kalman != null && Number.isFinite(row.mu_star_kalman))
          .map(row => ({ time: row.date as Time, value: row.mu_star_kalman }));
        muRef.current.setData(line);
        drawOverlay();
      })
      .catch(() => { if (!cancelled) muRef.current?.setData([]); })
      .finally(() => { if (!cancelled) setMuLoading(false); });
    return () => { cancelled = true; };
  }, [instrumentId]);

  // redraw overlay when the committed window changes (scrubber release)
  useEffect(() => { drawOverlay(); }, [start, end]); // eslint-disable-line react-hooks/exhaustive-deps

  function drawOverlay() {
    const chart = chartRef.current;
    const host = hostRef.current;
    if (!chart || !host) return;
    const ts = chart.timeScale();
    const { start: s, end: e } = winRef.current;
    const w = host.clientWidth;
    const xs = s ? ts.timeToCoordinate(s as Time) : null;
    const xe = e ? ts.timeToCoordinate(e as Time) : null;

    const place = (el: HTMLDivElement | null, x: number | null) => {
      if (!el) return;
      if (x == null) { el.style.display = 'none'; return; }
      el.style.display = 'block';
      el.style.left = `${x}px`;
    };
    place(startLineRef.current, xs);
    place(endLineRef.current, xe);

    const band = bandRef.current;
    if (band) {
      if (xs != null && xe != null) {
        const lo = Math.max(0, Math.min(xs, xe));
        const hi = Math.min(w, Math.max(xs, xe));
        band.style.display = 'block';
        band.style.left = `${lo}px`;
        band.style.width = `${Math.max(0, hi - lo)}px`;
      } else {
        band.style.display = 'none';
      }
    }
  }

  // NOTE: the chart host is ALWAYS rendered (never early-returned) so the one-shot init effect can
  // create the chart on mount. When no instrument is selected we overlay the empty-state message
  // instead of unmounting the host (which would leave the []-deps init effect with no element).
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', background: C.bg }}>
      <div ref={hostRef} style={{ position: 'absolute', inset: 0 }} />

      {!instrumentId && <div style={empty}>Select an instrument to begin</div>}

      {/* overlay layer — vertical lines + highlight band (pointer-events off so chart stays clean) */}
      <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', overflow: 'hidden' }}>
        <div ref={bandRef} style={{ position: 'absolute', top: 0, bottom: 0, display: 'none', background: 'rgba(56,139,253,0.06)' }} />
        <div ref={startLineRef} style={{ position: 'absolute', top: 0, bottom: 0, width: 0, display: 'none', borderLeft: `1px solid ${C.text}` }} />
        <div ref={endLineRef} style={{ position: 'absolute', top: 0, bottom: 0, width: 0, display: 'none', borderLeft: `1px solid ${C.accent}` }} />
      </div>

      {/* header chips */}
      <div style={{ position: 'absolute', top: 6, left: 8, display: 'flex', gap: 8, alignItems: 'center', pointerEvents: 'none' }}>
        <span style={{ ...mono, fontSize: 9, color: C.textDim, letterSpacing: '0.08em' }}>price · candles · μ* (Kalman)</span>
        {(loading || muLoading) && <span style={spinner} />}
      </div>
      {start && end && (
        <div style={{ position: 'absolute', top: 6, right: 12, ...mono, fontSize: 9, color: C.textDim, pointerEvents: 'none' }}>
          <span style={{ color: C.text }}>▏start {start}</span> · <span style={{ color: C.accent }}>end {end} ▕</span> · after-end dimmed
        </div>
      )}
    </div>
  );
}

const empty: React.CSSProperties = {
  ...mono, position: 'absolute', inset: 0, zIndex: 3, display: 'flex',
  alignItems: 'center', justifyContent: 'center', background: C.bg, fontSize: 11, color: C.textDim,
};

const spinner: React.CSSProperties = {
  width: 10, height: 10, border: `1.5px solid ${C.border}`, borderTopColor: C.accent,
  borderRadius: '50%', display: 'inline-block', animation: 'cockpit-spin 0.7s linear infinite',
};
