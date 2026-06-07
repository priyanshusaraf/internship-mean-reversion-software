'use client';

// ── Quadrant 1 — Price chart (candlesticks + Kalman μ* + scrubber-window overlay) ─────────────────
//
// Candles for the FULL stored range. Kalman μ* overlay from GET /diagnostics (mu_star_kalman/bar).
// The scrubber window is made VISIBLE: a muted vertical line at START, an accent line at END, a
// low-opacity highlight band between them, and the region OUTSIDE the window shaded by two
// absolutely-positioned overlay divs (pre-window left + post-window right). No toolbar, no zoom.
//
// ── FIX LOG: symmetric out-of-window dimming (left + right overlays) ──────────────────────────────
// Q1 (where/how the old dim lived): drawOverlay() drove a SINGLE overlay div (`dimRef`, anchored
//     right:0, width = totalWidth − endX). Overlay-div approach (the per-bar colour override that an
//     earlier version of this header described was already removed in a prior pass).
// Q2 (why it didn't work): there was NO pre-window (left-of-START) overlay at all — only the post-
//     window right shade existed, so candles BEFORE the start date were never dimmed.
// Q3 (the fix): add a second overlay (`leftDimRef`, anchored left:0, width = startX); keep the right
//     overlay (`rightDimRef`, width = totalWidth − endX); drive BOTH from one updateDim() with the
//     guarded formulas; call it from the three redraw paths ([start,end]+50ms settle, visible-range
//     change, ResizeObserver). Boundary lines + band were already correct and are kept.
// (Overlays live in the sibling overlay-layer, which shares the host's exact inset:0 box — same
//  coordinate space — rather than literally inside hostRef, to avoid React-vs-lightweight-charts
//  child-reconciliation conflicts. host.clientWidth is therefore the correct totalWidth.)

import { useEffect, useRef, useState } from 'react';
import {
  createChart, ColorType, CrosshairMode,
  type IChartApi, type ISeriesApi, type Time, type CandlestickData, type LineData,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import { C, mono } from '@/components/observatory/ui';
import type { OHLCVBar } from '@/lib/types';

const UP = '#3fb950', DOWN = '#f85149';
const MU_WINDOW = 20; // EMA/Kalman diagnostics window (μ* overlay only — display)

// Viewport = the chart's visible range as fractions [0,1] of the full series. View-only state,
// SEPARATE from the committed analysis window (start/end). Zoom/pan changes the viewport and the
// scrubber minimap, and NEVER triggers a habitat recompute.
export interface Viewport { from: number; to: number }

interface Props {
  instrumentId: string | null;
  bars: OHLCVBar[];
  loading: boolean;       // OHLC fetch in flight (owned by the page)
  start: string | null;   // committed scrubber window (drives lines/highlight/dim)
  end: string | null;
  viewport?: Viewport | null;                      // controlled visible range (from the scrubber minimap)
  onViewportChange?: (v: Viewport) => void;        // chart pan/zoom → report visible range up
}

export function PricePane({ instrumentId, bars, loading, start, end, viewport, onViewportChange }: Props) {
  const hostRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candleRef = useRef<ISeriesApi<'Candlestick'> | null>(null);
  const muRef = useRef<ISeriesApi<'Line'> | null>(null);

  // viewport sync plumbing
  const candleLenRef = useRef(0);          // current candle count (logical-range denominator)
  const fittedRef = useRef(false);         // has the current data been fit-to-content once?
  const applyingRef = useRef(false);       // guard: suppress reporting our own programmatic range set
  const onViewportChangeRef = useRef(onViewportChange);
  onViewportChangeRef.current = onViewportChange;

  // overlay primitives (true vertical lines + highlight band, positioned via timeToCoordinate)
  const startLineRef = useRef<HTMLDivElement>(null);
  const endLineRef = useRef<HTMLDivElement>(null);
  const bandRef = useRef<HTMLDivElement>(null);
  const leftDimRef = useRef<HTMLDivElement>(null);  // pre-window shade  (left of START)
  const rightDimRef = useRef<HTMLDivElement>(null); // post-window shade (right of END)
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
      // minBarSpacing default (0.5px) is ABOVE what a long series needs to fit in the pane
      // (e.g. 2463 bars / ~879px ≈ 0.36px/bar) — at the default, fitContent silently clamps to the
      // most-recent subset and scrolls the selected window off-screen left. Lower it so the FULL
      // series always fits and the post-window dim overlay covers only the tail.
      timeScale: { borderColor: C.border, minBarSpacing: 0.02 },
      handleScroll: true, handleScale: true,   // interactive: free zoom/pan (view-only; reported to the scrubber minimap)
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

    // Report the visible range up as [0,1] fractions whenever the user pans/zooms. Skip the echo of
    // our OWN programmatic setVisibleLogicalRange (applyingRef) so band-drag → chart → report can't loop.
    chart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
      if (!range) return;
      if (applyingRef.current) { applyingRef.current = false; return; }
      const len = candleLenRef.current;
      if (len < 2 || !onViewportChangeRef.current) return;
      onViewportChangeRef.current({ from: range.from / (len - 1), to: range.to / (len - 1) });
    });

    const ro = new ResizeObserver(() => {
      if (!hostRef.current) return;
      const w = hostRef.current.clientWidth, h = hostRef.current.clientHeight;
      chart.applyOptions({ width: w, height: h });
      // Fit-to-content only ONCE per dataset (guards the documented 0-width-host init case), then leave
      // the user's zoom/pan untouched on subsequent resizes. New data resets fittedRef (bars effect).
      if (!fittedRef.current && w > 0 && candleLenRef.current > 0) {
        chart.timeScale().fitContent();
        fittedRef.current = true;
      }
      draw();
    });
    ro.observe(hostRef.current);
    return () => { ro.disconnect(); chart.remove(); chartRef.current = null; candleRef.current = null; muRef.current = null; };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // ── candle data (uniform colours; post-window dimming is done by the div overlay) ──
  useEffect(() => {
    if (!candleRef.current) return;
    const data: CandlestickData[] = bars
      .filter(b => Number.isFinite(b.close))
      .map(b => ({ time: b.time as Time, open: b.open, high: b.high, low: b.low, close: b.close }));
    candleRef.current.setData(data);
    candleLenRef.current = data.length;
    fittedRef.current = false;             // new dataset → allow one fit-to-content
    if (data.length) { chartRef.current?.timeScale().fitContent(); fittedRef.current = true; }
    drawOverlay();
  }, [bars]);

  // Apply an externally-driven viewport (scrubber minimap drag) to the chart. Skip when the chart is
  // already there (within half a bar) — this no-ops the echo of our own reported range, breaking the loop.
  useEffect(() => {
    const chart = chartRef.current;
    const len = candleLenRef.current;
    if (!chart || !viewport || len < 2) return;
    const from = viewport.from * (len - 1);
    const to = viewport.to * (len - 1);
    const cur = chart.timeScale().getVisibleLogicalRange();
    if (cur && Math.abs(cur.from - from) < 0.5 && Math.abs(cur.to - to) < 0.5) return;
    applyingRef.current = true;
    chart.timeScale().setVisibleLogicalRange({ from, to });
  }, [viewport]);

  const fitView = () => { chartRef.current?.timeScale().fitContent(); };

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

  // redraw overlay when the committed window changes (scrubber release). The 50ms settle lets
  // lightweight-charts finish laying out the time scale so timeToCoordinate(start/end) is accurate.
  useEffect(() => {
    drawOverlay();
    const id = setTimeout(() => drawOverlay(), 50);
    return () => clearTimeout(id);
  }, [start, end]); // eslint-disable-line react-hooks/exhaustive-deps

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

    updateDim();
  }

  // Two out-of-window shades: LEFT covers [0, startX], RIGHT covers [endX, totalWidth]. The middle
  // (start→end) is left at full brightness. No window selected (start or end null) → both widths 0.
  function updateDim() {
    const chart = chartRef.current;
    const host = hostRef.current;
    const leftDim = leftDimRef.current;
    const rightDim = rightDimRef.current;
    if (!chart || !host || !leftDim || !rightDim) return;

    const { start: s, end: e } = winRef.current;
    if (!s || !e) {
      leftDim.style.width = '0px';
      rightDim.style.width = '0px';
      return;
    }
    const ts = chart.timeScale();
    const totalWidth = host.clientWidth;
    const startX = ts.timeToCoordinate(s as Time);
    const endX = ts.timeToCoordinate(e as Time);

    leftDim.style.width = startX != null && startX > 0 ? `${Math.max(0, startX)}px` : '0px';
    rightDim.style.width = endX != null && endX < totalWidth ? `${Math.max(0, totalWidth - endX)}px` : '0px';
  }

  // NOTE: the chart host is ALWAYS rendered (never early-returned) so the one-shot init effect can
  // create the chart on mount. When no instrument is selected we overlay the empty-state message
  // instead of unmounting the host (which would leave the []-deps init effect with no element).
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', background: C.bg }}>
      <div ref={hostRef} style={{ position: 'absolute', inset: 0 }} />

      {!instrumentId && <div style={empty}>Select an instrument to begin</div>}

      {/* overlay layer — out-of-window shades + vertical lines + highlight band (pointer-events off).
          Shares the host's exact inset:0 box so host.clientWidth == this layer's width. */}
      <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', overflow: 'hidden' }}>
        {/* pre-window shade: covers everything to the LEFT of the START date (width set in updateDim) */}
        <div ref={leftDimRef} style={{ position: 'absolute', top: 0, bottom: 0, left: 0, width: '0px', background: 'rgba(0,0,0,0.55)', pointerEvents: 'none', zIndex: 3, transition: 'width 0.15s ease' }} />
        {/* post-window shade: covers everything to the RIGHT of the END date (width set in updateDim) */}
        <div ref={rightDimRef} style={{ position: 'absolute', top: 0, bottom: 0, right: 0, width: '0px', background: 'rgba(0,0,0,0.55)', pointerEvents: 'none', zIndex: 3, transition: 'width 0.15s ease' }} />
        <div ref={bandRef} style={{ position: 'absolute', top: 0, bottom: 0, display: 'none', background: 'rgba(56,139,253,0.06)' }} />
        <div ref={startLineRef} style={{ position: 'absolute', top: 0, bottom: 0, width: 0, display: 'none', borderLeft: `1px solid ${C.text}` }} />
        <div ref={endLineRef} style={{ position: 'absolute', top: 0, bottom: 0, width: 0, display: 'none', borderLeft: `1px solid ${C.accent}` }} />
      </div>

      {/* header chips */}
      <div style={{ position: 'absolute', top: 6, left: 8, display: 'flex', gap: 8, alignItems: 'center' }}>
        <span style={{ ...mono, fontSize: 9, color: C.textDim, letterSpacing: '0.08em', pointerEvents: 'none' }}>price · candles · μ* (Kalman)</span>
        {instrumentId && (
          <button
            onClick={fitView}
            title="Fit full series (reset zoom)"
            style={{
              ...mono, fontSize: 9, padding: '1px 6px', cursor: 'pointer',
              background: C.bgRaised, border: `1px solid ${C.border}`, borderRadius: 3, color: C.textDim,
            }}
            onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.color = C.accent; }}
            onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.color = C.textDim; }}
          >
            ⤢ fit
          </button>
        )}
        {(loading || muLoading) && <span style={spinner} />}
      </div>
      {start && end && (
        <div style={{ position: 'absolute', top: 6, right: 12, ...mono, fontSize: 9, color: C.textDim, pointerEvents: 'none' }}>
          <span style={{ color: C.text }}>▏start {start}</span> · <span style={{ color: C.accent }}>end {end} ▕</span> · out-of-window dimmed
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
