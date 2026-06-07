'use client';

import { useEffect, useRef, useState } from 'react';
import {
  createChart,
  ColorType,
  CrosshairMode,
  type IChartApi,
  type ISeriesApi,
  type CandlestickData,
  type LineData,
  type Time,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import { useWorkstationStore } from '@/lib/store';

export function ChartWorkspace() {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);
  const estimatorSeriesRef = useRef<ISeriesApi<'Line'> | null>(null);

  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { selectedInstrumentId, dateRange, estimatorEnabled, estimatorWindow } =
    useWorkstationStore();

  // Initialize chart once on mount
  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: '#070b10' },
        textColor: '#3d4d5e',
        fontSize: 10,
      },
      grid: {
        vertLines: { color: '#0e1520' },
        horzLines: { color: '#0e1520' },
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: { color: '#1e2d3d', labelBackgroundColor: '#0d1520' },
        horzLine: { color: '#1e2d3d', labelBackgroundColor: '#0d1520' },
      },
      rightPriceScale: { borderColor: '#161d27' },
      timeScale: { borderColor: '#161d27', timeVisible: true },
      width: containerRef.current.clientWidth,
      height: containerRef.current.clientHeight,
    });

    const series = chart.addCandlestickSeries({
      upColor: '#3fb950',
      downColor: '#f85149',
      borderVisible: false,
      wickUpColor: '#3fb950',
      wickDownColor: '#f85149',
    });

    const estimatorSeries = chart.addLineSeries({
      color: 'rgba(88, 166, 255, 0.5)',
      lineWidth: 1,
      crosshairMarkerVisible: false,
      lastValueVisible: false,
      priceLineVisible: false,
    });

    chartRef.current = chart;
    seriesRef.current = series;
    estimatorSeriesRef.current = estimatorSeries;

    const ro = new ResizeObserver(() => {
      if (containerRef.current) {
        chart.applyOptions({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight,
        });
      }
    });
    ro.observe(containerRef.current);

    return () => {
      ro.disconnect();
      chart.remove();
      chartRef.current = null;
      seriesRef.current = null;
      estimatorSeriesRef.current = null;
    };
  }, []);

  // Fetch and render data. OHLCV renders first; estimator is additive and never blocks candles.
  useEffect(() => {
    setError(null);
    seriesRef.current?.setData([]);
    estimatorSeriesRef.current?.setData([]);

    if (!selectedInstrumentId || !seriesRef.current) return;

    let cancelled = false;
    setLoading(true);

    const start = dateRange.start ?? undefined;
    const end = dateRange.end ?? undefined;

    (async () => {
      try {
        // Step 1: fetch and render OHLCV — this is always the primary surface
        const ohlcvResp = await api.getOHLCV(selectedInstrumentId, start, end);
        if (cancelled) return;

        const candles: CandlestickData[] = ohlcvResp.bars.map((b) => ({
          time: b.time as Time,
          open: b.open,
          high: b.high,
          low: b.low,
          close: b.close,
        }));
        seriesRef.current?.setData(candles);
        chartRef.current?.timeScale().fitContent();
        setLoading(false);

        // Step 2: fetch estimator overlay — failure here does NOT clear the chart
        if (estimatorEnabled && !cancelled) {
          try {
            const estimatorResp = await api.getEstimator(selectedInstrumentId, estimatorWindow, start, end);
            if (cancelled) return;
            const line: LineData[] = estimatorResp.bars.map((b) => ({
              time: b.time as Time,
              value: b.value,
            }));
            estimatorSeriesRef.current?.setData(line);
          } catch (estimatorErr: unknown) {
            if (!cancelled) {
              const msg = estimatorErr instanceof Error ? estimatorErr.message : 'Estimator fetch failed';
              setError(`μ*: ${msg}`);
            }
          }
        } else {
          estimatorSeriesRef.current?.setData([]);
        }
      } catch (ohlcvErr: unknown) {
        if (!cancelled) {
          setError(ohlcvErr instanceof Error ? ohlcvErr.message : 'Fetch failed');
          setLoading(false);
        }
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [selectedInstrumentId, dateRange.start, dateRange.end, estimatorEnabled, estimatorWindow]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="flex-1 flex flex-col min-h-0 relative" style={{ background: '#070b10' }}>
      {!selectedInstrumentId && (
        <div
          className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none select-none"
          style={{ gap: 8 }}
        >
          <div
            style={{
              width: 32, height: 32, borderRadius: 8,
              background: 'rgba(56,139,253,0.06)',
              border: '1px solid rgba(56,139,253,0.12)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M2 9.5L5.5 5.5L8.5 8L12 3.5" stroke="rgba(56,139,253,0.4)" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <span style={{ fontSize: 11, color: 'var(--amr-text-dim)', letterSpacing: '0.03em' }}>
            Select an instrument to begin
          </span>
        </div>
      )}
      {error && (
        <div
          className="absolute z-10 flex items-center gap-2"
          style={{
            top: 10, left: '50%', transform: 'translateX(-50%)',
            background: 'rgba(248,81,73,0.06)',
            border: '1px solid rgba(248,81,73,0.25)',
            borderRadius: 4,
            padding: '5px 10px',
          }}
        >
          <span style={{ fontSize: 10, color: '#f85149' }}>{error}</span>
          <button
            onClick={() => setError(null)}
            style={{
              background: 'none', border: 'none', cursor: 'pointer',
              color: 'rgba(248,81,73,0.5)', fontSize: 12, lineHeight: 1,
              padding: '0 2px',
            }}
          >
            ×
          </button>
        </div>
      )}
      {isLoading && (
        <div
          className="absolute z-10 select-none font-data"
          style={{ top: 10, right: 12, fontSize: 10, color: 'var(--amr-text-dim)' }}
        >
          loading
        </div>
      )}
      {selectedInstrumentId && (
        <button
          onClick={() => chartRef.current?.timeScale().fitContent()}
          title="Fit full series (reset zoom)"
          className="absolute z-10 font-data"
          style={{
            top: 8, left: 10, fontSize: 9, padding: '1px 6px', cursor: 'pointer',
            background: '#0d1520', border: '1px solid #161d27', borderRadius: 3, color: 'var(--amr-text-dim)',
          }}
        >
          ⤢ fit
        </button>
      )}
      <div ref={containerRef} className="flex-1 min-h-0" />
    </div>
  );
}
