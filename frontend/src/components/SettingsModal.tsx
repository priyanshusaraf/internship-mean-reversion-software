'use client';

import { useUIStore, TEXT_COLOR_PRESETS } from '@/lib/store';

const FONT_STEPS = [
  { label: 'XS', value: 0.75 },
  { label: 'S',  value: 0.88 },
  { label: 'M',  value: 1.0  },
  { label: 'L',  value: 1.2  },
  { label: 'XL', value: 1.45 },
  { label: '2X', value: 1.75 },
];

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
};

export function SettingsModal({ onClose }: { onClose: () => void }) {
  const { fontScale, leftWidth, rightWidth, chartSplit, lineWidth, textColor, setUI, resetUI } = useUIStore();
  // The swatch shown in the custom picker: chosen color, or the brightened default when unset.
  const effectiveColor = textColor || '#8b9bb0';

  return (
    <>
      {/* Backdrop */}
      <div
        style={{ position: 'fixed', inset: 0, zIndex: 98, background: 'rgba(0,0,0,0.5)' }}
        onClick={onClose}
      />

      {/* Slide-out panel */}
      <div style={{
        position: 'fixed', right: 0, top: 0, bottom: 0, zIndex: 99,
        width: 300,
        background: '#090d13',
        borderLeft: '1px solid #1a2230',
        display: 'flex', flexDirection: 'column',
        boxShadow: '-8px 0 32px rgba(0,0,0,0.5)',
      }}>

        {/* Header */}
        <div style={{
          height: 44, flexShrink: 0, display: 'flex', alignItems: 'center',
          padding: '0 16px', borderBottom: '1px solid #161d27', gap: 8,
        }}>
          <span style={{ flex: 1, ...mono, fontSize: 10, fontWeight: 700, color: '#58a6ff', letterSpacing: '0.14em', textTransform: 'uppercase' }}>
            Settings
          </span>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--amr-text-dim)', fontSize: 15, lineHeight: 1, padding: '2px 4px' }}
            onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.color = '#c9d1d9'; }}
            onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.color = 'var(--amr-text-dim)'; }}
          >
            ✕
          </button>
        </div>

        {/* Body */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: 24 }}>

          {/* — Interface — */}
          <Section title="Interface">
            <Field label="Font size">
              <div style={{ display: 'flex', gap: 4 }}>
                {FONT_STEPS.map(({ label, value }) => (
                  <button
                    key={value}
                    onClick={() => setUI({ fontScale: value })}
                    style={{
                      flex: 1, padding: '5px 0',
                      ...mono, fontSize: Math.round(value * 9),
                      fontWeight: 600,
                      background: Math.abs(fontScale - value) < 0.01 ? 'rgba(56,139,253,0.15)' : '#0d1520',
                      border: `1px solid ${Math.abs(fontScale - value) < 0.01 ? 'rgba(56,139,253,0.5)' : '#1a2230'}`,
                      borderRadius: 3,
                      color: Math.abs(fontScale - value) < 0.01 ? '#58a6ff' : '#3a4a5c',
                      cursor: 'pointer', transition: 'all 0.1s',
                    }}
                  >
                    {label}
                  </button>
                ))}
              </div>
              <div style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', marginTop: 3 }}>
                Current: {Math.round(fontScale * 100)}% — affects panel text and data labels
              </div>
            </Field>
          </Section>

          {/* — Appearance — */}
          <Section title="Appearance">
            <Field label="Text color">
              <div style={{ display: 'flex', gap: 4 }}>
                {TEXT_COLOR_PRESETS.map(({ label, value }) => {
                  const sel = textColor === value;
                  return (
                    <button
                      key={label}
                      onClick={() => setUI({ textColor: value })}
                      style={{
                        flex: 1, padding: '5px 0',
                        ...mono, fontSize: 9, fontWeight: 600,
                        background: sel ? 'rgba(56,139,253,0.15)' : '#0d1520',
                        border: `1px solid ${sel ? 'rgba(56,139,253,0.5)' : '#1a2230'}`,
                        borderRadius: 3,
                        color: sel ? '#58a6ff' : '#3a4a5c',
                        cursor: 'pointer', transition: 'all 0.1s',
                      }}
                    >
                      {label}
                    </button>
                  );
                })}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 6 }}>
                <input
                  type="color"
                  value={effectiveColor}
                  onChange={e => setUI({ textColor: e.target.value })}
                  style={{
                    width: 28, height: 22, padding: 0, border: '1px solid #1a2230',
                    borderRadius: 3, background: '#0d1520', cursor: 'pointer',
                  }}
                />
                <span style={{ ...mono, fontSize: 9, color: '#4a5a6e' }}>
                  Custom — {textColor ? textColor : 'using default'}
                </span>
                {textColor && (
                  <button
                    onClick={() => setUI({ textColor: '' })}
                    style={{
                      marginLeft: 'auto', ...mono, fontSize: 9, padding: '2px 6px',
                      background: 'transparent', border: '1px solid #1a2230', borderRadius: 3,
                      color: '#4a5a6e', cursor: 'pointer',
                    }}
                  >
                    reset
                  </button>
                )}
              </div>
              <div style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)', marginTop: 3 }}>
                Sets primary text brightness across panels and data labels
              </div>
            </Field>
          </Section>

          {/* — Layout — */}
          <Section title="Layout">
            <Field label={`Instruments panel — ${leftWidth}px`}>
              <input type="range" min={160} max={380} step={4} value={leftWidth}
                onChange={e => setUI({ leftWidth: Number(e.target.value) })}
                style={{ width: '100%' }}
              />
            </Field>
            <Field label={`Estimators panel — ${rightWidth}px`}>
              <input type="range" min={120} max={300} step={4} value={rightWidth}
                onChange={e => setUI({ rightWidth: Number(e.target.value) })}
                style={{ width: '100%' }}
              />
            </Field>
            <Field label={`Chart height — ${chartSplit}% of workspace`}>
              <input type="range" min={30} max={80} step={2} value={chartSplit}
                onChange={e => setUI({ chartSplit: Number(e.target.value) })}
                style={{ width: '100%' }}
              />
            </Field>
          </Section>

          {/* — Graph — */}
          <Section title="Graph">
            <Field label={`Overlay line width — ${lineWidth}px`}>
              <input type="range" min={0.5} max={4} step={0.5} value={lineWidth}
                onChange={e => setUI({ lineWidth: Number(e.target.value) })}
                style={{ width: '100%' }}
              />
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 4 }}>
                <div style={{ flex: 1, height: lineWidth, background: 'rgba(88,166,255,0.7)', borderRadius: lineWidth }} />
                <span style={{ ...mono, fontSize: 9, color: 'var(--amr-text-dim)' }}>μ* EMA preview</span>
              </div>
            </Field>
          </Section>

        </div>

        {/* Footer */}
        <div style={{ padding: '12px 16px', borderTop: '1px solid #161d27', flexShrink: 0 }}>
          <button
            onClick={resetUI}
            style={{
              width: '100%', padding: '6px 0',
              ...mono, fontSize: 10, fontWeight: 600, letterSpacing: '0.06em',
              background: 'transparent', border: '1px solid #1a2230', borderRadius: 3,
              color: 'var(--amr-text-dim)', cursor: 'pointer', transition: 'all 0.12s',
            }}
            onMouseEnter={e => { const b = e.currentTarget as HTMLButtonElement; b.style.borderColor = '#2d3a4a'; b.style.color = '#8b99a8'; }}
            onMouseLeave={e => { const b = e.currentTarget as HTMLButtonElement; b.style.borderColor = '#1a2230'; b.style.color = 'var(--amr-text-dim)'; }}
          >
            Reset to defaults
          </button>
        </div>
      </div>
    </>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <div style={{
        fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
        fontSize: 9, fontWeight: 700, color: 'var(--amr-text-dim)',
        letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 10,
        paddingBottom: 6, borderBottom: '1px solid #0f141a',
      }}>
        {title}
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {children}
      </div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
      <span style={{ fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace', fontSize: 10, color: '#4a5a6e' }}>
        {label}
      </span>
      {children}
    </div>
  );
}
