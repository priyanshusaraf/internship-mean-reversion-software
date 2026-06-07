'use client';

import { useWorkstationStore } from '@/lib/store';
import { WORKBENCH_MODULES } from './registry';

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
};

export function ModuleNav() {
  const { activeWorkbenchModule, setActiveWorkbenchModule } = useWorkstationStore();

  return (
    <nav style={{
      width: '100%', height: '100%',
      background: '#090d13',
      borderRight: '1px solid #161d27',
      display: 'flex', flexDirection: 'column',
      paddingTop: 8,
      overflowY: 'auto',
    }}>
      <div style={{ ...mono, fontSize: 8, color: '#1e2833', letterSpacing: '0.14em', textTransform: 'uppercase', paddingLeft: 10, paddingBottom: 6 }}>
        Modules
      </div>

      {WORKBENCH_MODULES.map(mod => {
        const active = activeWorkbenchModule === mod.id;
        return (
          <button
            key={mod.id}
            onClick={() => setActiveWorkbenchModule(mod.id)}
            title={mod.description}
            style={{
              textAlign: 'left',
              padding: '7px 10px',
              background: active ? 'rgba(56,139,253,0.07)' : 'transparent',
              border: 'none',
              borderLeft: `2px solid ${active ? '#388bfd' : 'transparent'}`,
              cursor: 'pointer',
              transition: 'all 0.1s',
              display: 'flex', flexDirection: 'column', gap: 1,
            }}
            onMouseEnter={e => { if (!active) (e.currentTarget as HTMLButtonElement).style.background = 'rgba(255,255,255,0.02)'; }}
            onMouseLeave={e => { if (!active) (e.currentTarget as HTMLButtonElement).style.background = 'transparent'; }}
          >
            <span style={{
              ...mono, fontSize: 10, fontWeight: active ? 600 : 400,
              color: active ? '#58a6ff' : '#3d4d5e',
              letterSpacing: '0.04em',
            }}>
              {mod.label}
            </span>
            <span style={{ ...mono, fontSize: 8, color: '#1e2833', lineHeight: 1.3 }}>
              {mod.description.split(' ').slice(0, 4).join(' ')}…
            </span>
          </button>
        );
      })}
    </nav>
  );
}
