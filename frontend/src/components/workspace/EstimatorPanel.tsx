'use client';

import { useWorkstationStore, useUIStore } from '@/lib/store';

export function EstimatorPanel() {
  const { estimatorEnabled, estimatorWindow, toggleEstimator, setEstimatorWindow } =
    useWorkstationStore();
  const { rightWidth, fontScale } = useUIStore();
  const sc = (base: number) => Math.round(base * fontScale);

  return (
    <aside
      className="shrink-0 flex flex-col overflow-hidden"
      style={{
        width: rightWidth,
        background: '#090d13',
        borderLeft: '1px solid #161d27',
      }}
    >
      {/* Header */}
      <div
        className="flex items-center px-3 shrink-0"
        style={{ height: 36, borderBottom: '1px solid #161d27' }}
      >
        <span
          className="font-data"
          style={{ fontSize: sc(9), fontWeight: 700, color: '#2d3a4a', letterSpacing: '0.14em', textTransform: 'uppercase' }}
        >
          Estimators
        </span>
      </div>

      {/* EMA row */}
      <div
        style={{
          padding: '10px 12px',
          borderBottom: '1px solid #161d27',
          background: estimatorEnabled ? 'rgba(56,139,253,0.03)' : 'transparent',
          transition: 'background 0.2s',
        }}
      >
        {/* Label + toggle */}
        <div className="flex items-center" style={{ marginBottom: 8, gap: 8 }}>
          {/* Color swatch */}
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: 2,
              flexShrink: 0,
              background: estimatorEnabled ? 'rgba(88,166,255,0.7)' : '#1a2230',
              boxShadow: estimatorEnabled ? '0 0 6px rgba(88,166,255,0.4)' : 'none',
              transition: 'all 0.2s',
            }}
          />

          <span
            style={{
              flex: 1,
              fontSize: sc(11),
              fontWeight: 600,
              color: estimatorEnabled ? '#c9d1d9' : '#3a4558',
              transition: 'color 0.2s',
              userSelect: 'none',
              letterSpacing: '0.01em',
            }}
          >
            μ* EMA
          </span>

          {/* Toggle */}
          <button
            onClick={toggleEstimator}
            aria-label="Toggle EMA estimator"
            style={{
              flexShrink: 0,
              width: 30,
              height: 16,
              borderRadius: 8,
              background: estimatorEnabled ? '#388bfd' : '#161d27',
              border: `1px solid ${estimatorEnabled ? '#4d9eff' : '#1e2833'}`,
              boxShadow: estimatorEnabled ? '0 0 10px rgba(56,139,253,0.4), inset 0 0 4px rgba(56,139,253,0.2)' : 'none',
              position: 'relative',
              cursor: 'pointer',
              transition: 'all 0.15s',
            }}
          >
            <span
              style={{
                position: 'absolute',
                top: 2,
                left: estimatorEnabled ? 13 : 2,
                width: 10,
                height: 10,
                borderRadius: '50%',
                background: estimatorEnabled ? 'white' : '#3a4a5c',
                boxShadow: '0 1px 3px rgba(0,0,0,0.4)',
                transition: 'left 0.15s',
              }}
            />
          </button>
        </div>

        {/* Window control */}
        <div
          className="flex items-center"
          style={{ gap: 8, opacity: estimatorEnabled ? 1 : 0.25, transition: 'opacity 0.2s' }}
        >
          <span
            className="font-data"
            style={{ fontSize: sc(10), color: '#2d3a4a', width: 44, flexShrink: 0 }}
          >
            window
          </span>
          <input
            type="number"
            min={2}
            max={500}
            value={estimatorWindow}
            disabled={!estimatorEnabled}
            onChange={(e) => {
              const v = parseInt(e.target.value, 10);
              if (v >= 2 && v <= 500) setEstimatorWindow(v);
            }}
            className="font-data"
            style={{
              flex: 1,
              background: '#0d1520',
              border: '1px solid #1a2230',
              borderRadius: 3,
              padding: '3px 8px',
              fontSize: 11,
              color: '#c9d1d9',
              textAlign: 'right',
              outline: 'none',
              cursor: estimatorEnabled ? 'text' : 'not-allowed',
            }}
            onFocus={(e) => { e.target.style.borderColor = '#388bfd'; }}
            onBlur={(e) => { e.target.style.borderColor = '#1a2230'; }}
          />
        </div>
      </div>

      {/* Future estimators — placeholder rows to hint roadmap */}
      {(['Rolling Mean', 'Kalman', 'VWAP'] as const).map((name) => (
        <div
          key={name}
          className="flex items-center px-3"
          style={{ height: 32, gap: 8, borderBottom: '1px solid #0f141a', opacity: 0.2, cursor: 'default' }}
        >
          <div style={{ width: 8, height: 8, borderRadius: 2, background: '#1a2230', flexShrink: 0 }} />
          <span style={{ fontSize: 11, color: '#3a4558' }}>{name}</span>
        </div>
      ))}

      <div style={{ flex: 1 }} />
    </aside>
  );
}
