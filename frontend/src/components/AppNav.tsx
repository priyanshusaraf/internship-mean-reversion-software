'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';
import { useUIStore, useWorkstationStore } from '@/lib/store';
import { api } from '@/lib/api';
import { SettingsModal } from './SettingsModal';

const mono: React.CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

export function AppNav() {
  const pathname = usePathname();
  const [settingsOpen, setSettingsOpen] = useState(false);
  const { fontScale } = useUIStore();

  // Apply font scale as a CSS variable on the root so scaled components can use it
  useEffect(() => {
    document.documentElement.style.setProperty('--amr-scale', String(fontScale));
  }, [fontScale]);

  // App-wide instrument list fetch. The Workstation panel also fetches, but Workbench/Observatory
  // do not — so a reload that lands directly on those pages (now possible because
  // selectedInstrumentId is persisted) would leave the instruments[] empty and the restored
  // instrument's display name unresolved (chip shows "—"). Fetching once here keeps the persisted
  // selection coherent on every page. Only fills when empty so it never clobbers a fresh list.
  useEffect(() => {
    if (useWorkstationStore.getState().instruments.length === 0) {
      api.listInstruments().then(useWorkstationStore.getState().setInstruments).catch(() => {});
    }
  }, []);


  return (
    <>
      <nav
        style={{
          height: 30,
          flexShrink: 0,
          background: '#060a0f',
          borderBottom: '1px solid #0e1520',
          display: 'flex',
          alignItems: 'center',
          paddingLeft: 12,
          paddingRight: 8,
          gap: 2,
        }}
      >
        <span style={{ ...mono, fontSize: 9, color: '#1e2833', letterSpacing: '0.16em', textTransform: 'uppercase', marginRight: 10 }}>
          AMR
        </span>

        {[
          { href: '/', label: 'Workstation' },
          { href: '/workbench', label: 'Workbench' },
          { href: '/observatory', label: 'Observatory' },
          { href: '/backtest', label: 'Backtest' },
        ].map(({ href, label }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              style={{
                ...mono,
                fontSize: 10,
                fontWeight: active ? 600 : 400,
                color: active ? '#58a6ff' : '#2d3a4a',
                textDecoration: 'none',
                padding: '2px 8px',
                borderRadius: 3,
                background: active ? 'rgba(56,139,253,0.07)' : 'transparent',
                border: `1px solid ${active ? 'rgba(56,139,253,0.2)' : 'transparent'}`,
                letterSpacing: '0.04em',
                transition: 'all 0.12s',
              }}
            >
              {label}
            </Link>
          );
        })}

        {/* Spacer */}
        <div style={{ flex: 1 }} />

        {/* Settings gear */}
        <button
          onClick={() => setSettingsOpen(true)}
          title="Settings"
          style={{
            background: 'none', border: '1px solid transparent', borderRadius: 3,
            cursor: 'pointer', padding: '2px 6px',
            color: '#2d3a4a', fontSize: 11, lineHeight: 1,
            transition: 'all 0.12s',
          }}
          onMouseEnter={e => {
            const b = e.currentTarget as HTMLButtonElement;
            b.style.color = '#58a6ff';
            b.style.borderColor = 'rgba(56,139,253,0.25)';
            b.style.background = 'rgba(56,139,253,0.06)';
          }}
          onMouseLeave={e => {
            const b = e.currentTarget as HTMLButtonElement;
            b.style.color = '#2d3a4a';
            b.style.borderColor = 'transparent';
            b.style.background = 'none';
          }}
        >
          ⚙
        </button>
      </nav>

      {settingsOpen && <SettingsModal onClose={() => setSettingsOpen(false)} />}
    </>
  );
}
