'use client';

import { useWorkstationStore } from '@/lib/store';

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

export function ResearchControls() {
  const { estimatorWindow, estimatorMode, setEstimatorWindow, setEstimatorMode } = useWorkstationStore();

  return (
    <aside style={{
      width: 180, flexShrink: 0,
      background: '#090d13',
      borderLeft: '1px solid #161d27',
      display: 'flex', flexDirection: 'column',
      overflowY: 'auto',
    }}>
      {/* Header */}
      <div style={{ height: 26, display: 'flex', alignItems: 'center', paddingLeft: 10, borderBottom: '1px solid #161d27' }}>
        <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', letterSpacing: '0.14em', textTransform: 'uppercase' }}>Controls</span>
      </div>

      <div style={{ padding: '10px 10px', display: 'flex', flexDirection: 'column', gap: 12 }}>
        {/* Estimator mode */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <span style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase' }}>Mode</span>
          <div style={{ display: 'flex', gap: 4 }}>
            {(['causal', 'full_info'] as const).map(mode => (
              <button
                key={mode}
                onClick={() => setEstimatorMode(mode)}
                style={{
                  ...mono, fontSize: 9, flex: 1, padding: '4px 0', borderRadius: 3,
                  background: estimatorMode === mode ? 'rgba(56,139,253,0.1)' : 'transparent',
                  border: `1px solid ${estimatorMode === mode ? 'rgba(56,139,253,0.3)' : '#161d27'}`,
                  color: estimatorMode === mode ? '#58a6ff' : '#2d3a4a',
                  cursor: 'pointer',
                }}
              >
                {mode === 'causal' ? 'causal' : 'full-info'}
              </button>
            ))}
          </div>
          <span style={{ ...mono, fontSize: 8, color: '#1e2833', lineHeight: 1.4 }}>
            {estimatorMode === 'causal'
              ? 'Only data ≤ t used. Temporally valid.'
              : 'adjust=True weighting. Differs from causal only during warmup (~3× span bars).'}
          </span>
        </div>

        {/* Window */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <span style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase' }}>EMA Window</span>
          <input
            type="number"
            min={5} max={200} step={1}
            value={estimatorWindow}
            onChange={e => setEstimatorWindow(Math.max(5, Math.min(200, parseInt(e.target.value) || 20)))}
            style={{
              ...mono, background: '#0d1520', border: '1px solid #1a2230', borderRadius: 3,
              padding: '4px 8px', fontSize: 11, color: '#c9d1d9', outline: 'none', width: '100%',
            }}
          />
          <span style={{ ...mono, fontSize: 8, color: '#1e2833' }}>bars (5–200)</span>
        </div>

        {/* Divider */}
        <div style={{ height: 1, background: '#161d27' }} />

        {/* Interpretation hints */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <span style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.1em', textTransform: 'uppercase' }}>Reading guide</span>
          {[
            ['ACF(1) > 0.3', 'ε has memory — but EMA artifact can inflate ACF even on RW'],
            ['Δμ* ≈ 0', 'EMA variants have converged — expected after ~3× span bars'],
            ['Δμ* large', 'short series or warmup period — not a modeling failure'],
            ['Half-life', 'bars to 50% reversion (OLS with intercept — reliable)'],
            ['Skew ≠ 0', 'asymmetric residuals'],
            ['Kurt > 3', 'fat tails — z-score understates risk'],
          ].map(([label, desc]) => (
            <div key={label} style={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <span style={{ ...mono, fontSize: 8, color: 'var(--amr-text)' }}>{label}</span>
              <span style={{ ...mono, fontSize: 8, color: '#1e2833', lineHeight: 1.3 }}>{desc}</span>
            </div>
          ))}
        </div>
      </div>
    </aside>
  );
}
