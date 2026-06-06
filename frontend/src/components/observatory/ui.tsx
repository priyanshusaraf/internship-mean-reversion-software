'use client';

/** Shared visual primitives for the Observatory v2 cockpit. Matches the dark workbench idiom. */
import type { CSSProperties, ReactNode } from 'react';

export const C = {
  bg: '#070b10',
  bgPanel: '#0a0f16',
  bgRaised: '#0d1520',
  border: '#161d27',
  borderSoft: '#0e1520',
  text: '#3d4d5e',
  textBright: '#8fa3b8',
  textDim: '#2d3a4a',
  accent: '#58a6ff',
  accentBg: 'rgba(56,139,253,0.07)',
  accentBorder: 'rgba(56,139,253,0.25)',
  warn: '#d29922',
  warnBg: 'rgba(210,153,34,0.08)',
  warnBorder: 'rgba(210,153,34,0.3)',
  danger: '#f85149',
  dangerBg: 'rgba(248,81,73,0.07)',
  dangerBorder: 'rgba(248,81,73,0.3)',
  good: '#3fb950',
  goodBg: 'rgba(63,185,80,0.08)',
  future: '#1c2530',
};

export const mono: CSSProperties = {
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
  fontVariantNumeric: 'tabular-nums',
};

export function Panel({ title, children, style, right }: { title?: string; children: ReactNode; style?: CSSProperties; right?: ReactNode }) {
  return (
    <div
      style={{
        background: C.bgPanel,
        border: `1px solid ${C.border}`,
        borderRadius: 5,
        display: 'flex',
        flexDirection: 'column',
        minHeight: 0,
        ...style,
      }}
    >
      {title && (
        <div
          style={{
            ...mono,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            fontSize: 9,
            letterSpacing: '0.14em',
            textTransform: 'uppercase',
            color: C.textDim,
            padding: '6px 10px',
            borderBottom: `1px solid ${C.borderSoft}`,
          }}
        >
          <span>{title}</span>
          {right}
        </div>
      )}
      <div style={{ flex: 1, minHeight: 0, padding: 10, overflow: 'auto', display: 'flex', flexDirection: 'column' }}>{children}</div>
    </div>
  );
}

export function Stat({ label, value, color, mono: useMono = true }: { label: string; value: ReactNode; color?: string; mono?: boolean }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      <span style={{ fontSize: 9, letterSpacing: '0.08em', textTransform: 'uppercase', color: C.textDim }}>{label}</span>
      <span style={{ ...(useMono ? mono : {}), fontSize: 13, color: color ?? C.textBright }}>{value}</span>
    </div>
  );
}

export function Badge({ children, tone = 'neutral' }: { children: ReactNode; tone?: 'neutral' | 'good' | 'warn' | 'danger' | 'accent' }) {
  const map = {
    neutral: { c: C.text, bg: 'rgba(255,255,255,0.03)', b: C.border },
    good: { c: C.good, bg: C.goodBg, b: 'rgba(63,185,80,0.3)' },
    warn: { c: C.warn, bg: C.warnBg, b: C.warnBorder },
    danger: { c: C.danger, bg: C.dangerBg, b: C.dangerBorder },
    accent: { c: C.accent, bg: C.accentBg, b: C.accentBorder },
  }[tone];
  return (
    <span
      style={{
        ...mono,
        fontSize: 9,
        letterSpacing: '0.04em',
        color: map.c,
        background: map.bg,
        border: `1px solid ${map.b}`,
        borderRadius: 3,
        padding: '1px 6px',
      }}
    >
      {children}
    </span>
  );
}

export function fmt(v: number | null | undefined, digits = 3): string {
  if (v === null || v === undefined || !Number.isFinite(v)) return '—';
  return v.toFixed(digits);
}
