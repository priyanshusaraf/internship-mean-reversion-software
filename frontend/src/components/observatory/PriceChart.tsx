'use client';

/**
 * Price chart + draggable AS-OF cursor + Kalman μ* overlay + z sub-pane (contract §4.1, §5).
 *
 * Causal firewall (M1/M2), made VISIBLE:
 *  - bars ≤ as_of render normally (the causal view the model "knew").
 *  - forward_bars (time > as_of) render greyed and are labelled "future — evaluation only".
 *  - μ* and z come from POST /analysis/equilibrium with as_of = cursor (causal). NO JS math.
 *
 * The cursor is a draggable price-line on the time axis. Dragging it re-fetches series + re-runs
 * equilibrium causally (debounced).
 */
import { useEffect, useRef, useState, useCallback } from 'react';
import {
  createChart,
  ColorType,
  CrosshairMode,
  LineStyle,
  type IChartApi,
  type ISeriesApi,
  type LineData,
  type Time,
  type IPriceLine,
} from 'lightweight-charts';
import {
  observatory,
  type Bar,
  type EquilibriumResponse,
} from '@/lib/observatory';
import { C, mono, Badge, fmt } from './ui';

interface Props {
  datasetId: string;
  asOf: string | null;
  onAsOfChange: (d: string) => void;
  onEquilibrium: (e: EquilibriumResponse | null) => void;
  windowSel: { start: string | null; end: string | null };
  onWindowSel: (w: { start: string | null; end: string | null }) => void;
  // commit a manually edited window field (blur/Enter) → page clamps end ≤ as-of, then scores.
  onCommitWindow: (field: 'start' | 'end', value: string | null) => void;
  // "≤ as-of" convenience: full causal window that resumes cursor-tracking of the end.
  onTrackToAsOf: (start: string | null) => void;
  clampNote: string | null;
}

export function PriceChart({ datasetId, asOf, onAsOfChange, onEquilibrium, windowSel, onWindowSel, onCommitWindow, onTrackToAsOf, clampNote }: Props) {
  const priceRef = useRef<HTMLDivElement>(null);
  const zRef = useRef<HTMLDivElement>(null);
  const priceChart = useRef<IChartApi | null>(null);
  const zChart = useRef<IChartApi | null>(null);
  const closeSeries = useRef<ISeriesApi<'Line'> | null>(null);
  const fwdSeries = useRef<ISeriesApi<'Line'> | null>(null);
  const muSeries = useRef<ISeriesApi<'Line'> | null>(null);
  const zSeries = useRef<ISeriesApi<'Line'> | null>(null);
  const cursorLine = useRef<IPriceLine | null>(null);
  const winFromLine = useRef<IPriceLine | null>(null);
  const winToLine = useRef<IPriceLine | null>(null);

  const [allTimes, setAllTimes] = useState<string[]>([]);
  const [cursorIdx, setCursorIdx] = useState<number>(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fwdCount, setFwdCount] = useState(0);
  const [prov, setProv] = useState<EquilibriumResponse['provenance'] | null>(null);
  const [zBasis, setZBasis] = useState<string>('');

  // init charts (price + z subpane), synced time scales
  useEffect(() => {
    if (!priceRef.current || !zRef.current) return;
    const common = {
      layout: { background: { type: ColorType.Solid, color: C.bg }, textColor: '#3d4d5e', fontSize: 10 },
      grid: { vertLines: { color: C.borderSoft }, horzLines: { color: C.borderSoft } },
      crosshair: { mode: CrosshairMode.Normal, vertLine: { color: '#1e2d3d' }, horzLine: { color: '#1e2d3d' } },
      rightPriceScale: { borderColor: C.border },
      timeScale: { borderColor: C.border },
    };
    const pc = createChart(priceRef.current, { ...common, width: priceRef.current.clientWidth, height: priceRef.current.clientHeight });
    const zc = createChart(zRef.current, { ...common, width: zRef.current.clientWidth, height: zRef.current.clientHeight });

    closeSeries.current = pc.addLineSeries({ color: '#9fb4c9', lineWidth: 2, priceLineVisible: false, lastValueVisible: false });
    fwdSeries.current = pc.addLineSeries({ color: C.future, lineWidth: 2, priceLineVisible: false, lastValueVisible: false, crosshairMarkerVisible: false });
    muSeries.current = pc.addLineSeries({ color: C.accent, lineWidth: 1, priceLineVisible: false, lastValueVisible: false });
    zSeries.current = zc.addLineSeries({ color: '#d29922', lineWidth: 1, priceLineVisible: false, lastValueVisible: false });

    // z reference bands ±2, 0
    [{ p: 2, c: '#2a3548' }, { p: 0, c: '#3d4d5e' }, { p: -2, c: '#2a3548' }].forEach(({ p, c }) =>
      zSeries.current?.createPriceLine({ price: p, color: c, lineWidth: 1, lineStyle: LineStyle.Dashed, axisLabelVisible: true, title: String(p) }),
    );

    priceChart.current = pc;
    zChart.current = zc;

    // sync time scales between the two panes
    const sync = (src: IChartApi, dst: IChartApi) =>
      src.timeScale().subscribeVisibleLogicalRangeChange((r) => {
        if (r) dst.timeScale().setVisibleLogicalRange(r);
      });
    sync(pc, zc);
    sync(zc, pc);

    const ro = new ResizeObserver(() => {
      if (priceRef.current) pc.applyOptions({ width: priceRef.current.clientWidth, height: priceRef.current.clientHeight });
      if (zRef.current) zc.applyOptions({ width: zRef.current.clientWidth, height: zRef.current.clientHeight });
    });
    ro.observe(priceRef.current);
    ro.observe(zRef.current);

    return () => {
      ro.disconnect();
      pc.remove();
      zc.remove();
      priceChart.current = null;
      zChart.current = null;
    };
  }, []);

  // load the FULL series once (to know all timestamps & set cursor at last bar)
  useEffect(() => {
    if (!datasetId) return;
    let cancelled = false;
    (async () => {
      try {
        const full = await observatory.getSeries(datasetId, {});
        if (cancelled) return;
        const ts = full.bars.map((b) => b.time);
        setAllTimes(ts);
        const lastIdx = ts.length - 1;
        setCursorIdx(lastIdx);
        // default the as_of to ~70% through so forward bars are visible immediately
        const defIdx = Math.max(0, Math.floor(ts.length * 0.7));
        setCursorIdx(defIdx);
        onAsOfChange(ts[defIdx]);
      } catch (e) {
        setError(e instanceof Error ? e.message : 'series load failed');
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [datasetId]); // eslint-disable-line react-hooks/exhaustive-deps

  // re-fetch series (causal + forward) and equilibrium whenever as_of changes
  const refetch = useCallback(
    async (effectiveAsOf: string) => {
      if (!datasetId || !effectiveAsOf) return;
      setLoading(true);
      setError(null);
      try {
        const series = await observatory.getSeries(datasetId, { as_of: effectiveAsOf });
        const toLine = (bars: Bar[]): LineData[] =>
          bars
            .filter((b) => b.close !== null && Number.isFinite(b.close))
            .map((b) => ({ time: b.time as Time, value: b.close as number }));
        closeSeries.current?.setData(toLine(series.bars));
        fwdSeries.current?.setData(toLine(series.forward_bars));
        setFwdCount(series.forward_bars.length);
        // frame the whole series (causal + greyed forward) so the firewall boundary is visible
        priceChart.current?.timeScale().fitContent();

        // cursor price-line on the price pane (visual firewall boundary)
        const lastCausalClose = series.bars.length ? series.bars[series.bars.length - 1].close : null;
        if (cursorLine.current) closeSeries.current?.removePriceLine(cursorLine.current);
        if (lastCausalClose != null) {
          cursorLine.current =
            closeSeries.current?.createPriceLine({
              price: lastCausalClose,
              color: C.accent,
              lineWidth: 1,
              lineStyle: LineStyle.Solid,
              axisLabelVisible: true,
              title: `as-of ${effectiveAsOf}`,
            }) ?? null;
        }

        // equilibrium: causal μ* + z, as_of = cursor
        const eq = await observatory.equilibrium({ dataset_id: datasetId, as_of: effectiveAsOf });
        const muLine: LineData[] = eq.series
          .filter((r) => r.mu_star !== null && Number.isFinite(r.mu_star))
          .map((r) => ({ time: r.time as Time, value: r.mu_star as number }));
        const zLine: LineData[] = eq.series
          .filter((r) => r.z !== null && Number.isFinite(r.z))
          .map((r) => ({ time: r.time as Time, value: r.z as number }));
        muSeries.current?.setData(muLine);
        zSeries.current?.setData(zLine);
        setProv(eq.provenance);
        setZBasis(eq.z_sigma_basis);
        onEquilibrium(eq);
      } catch (e) {
        setError(e instanceof Error ? e.message : 'equilibrium failed');
        onEquilibrium(null);
      } finally {
        setLoading(false);
      }
    },
    [datasetId, onEquilibrium],
  );

  // debounce cursor drags
  useEffect(() => {
    if (!asOf) return;
    const id = setTimeout(() => void refetch(asOf), 120);
    return () => clearTimeout(id);
  }, [asOf, refetch]);

  // window-selection markers on the price pane
  useEffect(() => {
    if (winFromLine.current) closeSeries.current?.removePriceLine(winFromLine.current);
    if (winToLine.current) closeSeries.current?.removePriceLine(winToLine.current);
    winFromLine.current = null;
    winToLine.current = null;
    // markers are conceptual (time-bounds); we annotate via the panel rather than price lines
  }, [windowSel]);

  function onSlider(idx: number) {
    setCursorIdx(idx);
    const t = allTimes[idx];
    if (t) onAsOfChange(t);
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: 0, flex: 1, gap: 6 }}>
      {/* firewall banner */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
        <Badge tone="accent">causal firewall · as-of {asOf ?? '—'}</Badge>
        {fwdCount > 0 && (
          <span style={{ ...mono, fontSize: 10, color: C.future === '#1c2530' ? '#5a6b7d' : C.future }}>
            <span style={{ color: '#5a6b7d' }}>▬</span> {fwdCount} forward bars — future, evaluation only, NOT available to the model
          </span>
        )}
        {loading && <span style={{ ...mono, fontSize: 10, color: C.textDim }}>recomputing…</span>}
        {error && <span style={{ ...mono, fontSize: 10, color: C.danger }}>{error}</span>}
      </div>

      {/* price pane */}
      <div ref={priceRef} style={{ flex: 2, minHeight: 0, background: C.bg, border: `1px solid ${C.border}`, borderRadius: 4 }} />

      {/* z subpane */}
      <div style={{ display: 'flex', flexDirection: 'column', flex: 1, minHeight: 0 }}>
        <span style={{ ...mono, fontSize: 9, letterSpacing: '0.1em', textTransform: 'uppercase', color: C.textDim, marginBottom: 2 }}>
          z = (close − μ*)/σ · {zBasis || 'causal expanding innovation std'}
        </span>
        <div ref={zRef} style={{ flex: 1, minHeight: 0, background: C.bg, border: `1px solid ${C.border}`, borderRadius: 4 }} />
      </div>

      {/* as-of cursor slider (drag = hide-forward control) */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <span style={{ ...mono, fontSize: 9, letterSpacing: '0.1em', textTransform: 'uppercase', color: C.textDim, whiteSpace: 'nowrap' }}>
          as-of cursor
        </span>
        <input
          aria-label="as-of cursor"
          data-testid="as-of-cursor"
          type="range"
          min={0}
          max={Math.max(0, allTimes.length - 1)}
          value={cursorIdx}
          onChange={(e) => onSlider(Number(e.target.value))}
          style={{ flex: 1 }}
        />
        <span style={{ ...mono, fontSize: 11, color: C.accent, whiteSpace: 'nowrap' }}>{asOf ?? '—'}</span>
      </div>

      {/* window selection for habitat (≤ as_of). onChange = live (controlled value); the clamp +
          habitat fetch happen on COMMIT (blur or Enter), per Part 2. */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
        <span style={{ ...mono, fontSize: 9, letterSpacing: '0.1em', textTransform: 'uppercase', color: C.textDim }}>habitat window</span>
        <input
          type="date"
          aria-label="habitat window start"
          data-testid="window-start"
          value={windowSel.start ?? ''}
          max={asOf ?? undefined}
          onChange={(e) => onWindowSel({ ...windowSel, start: e.target.value || null })}
          onBlur={(e) => onCommitWindow('start', e.target.value || null)}
          onKeyDown={(e) => { if (e.key === 'Enter') onCommitWindow('start', (e.target as HTMLInputElement).value || null); }}
          style={dateInput}
        />
        <span style={{ color: C.textDim }}>→</span>
        <input
          type="date"
          aria-label="habitat window end"
          data-testid="window-end"
          value={windowSel.end ?? ''}
          max={asOf ?? undefined}
          onChange={(e) => onWindowSel({ ...windowSel, end: e.target.value || null })}
          onBlur={(e) => onCommitWindow('end', e.target.value || null)}
          onKeyDown={(e) => { if (e.key === 'Enter') onCommitWindow('end', (e.target as HTMLInputElement).value || null); }}
          style={dateInput}
        />
        <button
          data-testid="window-full"
          onClick={() => onTrackToAsOf(allTimes[0] ?? null)}
          style={btn}
        >
          ≤ as-of
        </button>
        {clampNote && (
          <span data-testid="clamp-note" style={{ ...mono, fontSize: 10, color: C.warn }}>⚠ {clampNote}</span>
        )}
      </div>

      {prov && (
        <div style={{ ...mono, fontSize: 9, color: C.textDim, display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          <span>engine {prov.engine}</span>
          <span>snr {fmt((prov.params as { snr?: number }).snr, 9)}</span>
          <span>κ {fmt((prov.params as { kappa?: number }).kappa, 3)}</span>
          <span>warmup {String((prov.params as { warmup?: number }).warmup)}</span>
          {prov.exploratory_watermark && <Badge tone="warn">EXPLORATORY — not a verdict</Badge>}
        </div>
      )}
    </div>
  );
}

const dateInput: React.CSSProperties = {
  ...mono,
  fontSize: 10,
  background: C.bgRaised,
  color: C.textBright,
  border: `1px solid ${C.border}`,
  borderRadius: 3,
  padding: '2px 5px',
};

const btn: React.CSSProperties = {
  ...mono,
  fontSize: 10,
  background: C.accentBg,
  color: C.accent,
  border: `1px solid ${C.accentBorder}`,
  borderRadius: 3,
  padding: '2px 8px',
  cursor: 'pointer',
};
