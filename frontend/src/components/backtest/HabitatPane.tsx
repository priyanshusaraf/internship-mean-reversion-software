'use client';

// ── Quadrant 4 — MR Habitat panel ────────────────────────────────────────────────────────────
//
// Surrogate-relative habitat score for the current scrubber window (scored on RELEASE, via the
// page; result lives in useBacktestStore). COLLAPSED: score + calibration badges + a pure-CSS mini
// surrogate cloud (p10/p50/p90 + real marker). EXPANDED (overlay over the bottom row): a larger CSS
// histogram of the null min-VR cloud (binForHistogram — display only, M5), the VR(q) curve, and the
// data_warning. NOTE: Plotly is NOT installed in this project; the existing Observatory habitat view
// renders the cloud with the same CSS-bar approach reused here (frozen stack §8, no new dep).

import { useState } from 'react';
import { useBacktestStore } from '@/lib/store';
import { binForHistogram, type HabitatResponse } from '@/lib/observatory';
import { C, mono, Badge } from '@/components/observatory/ui';

const fmt = (v: number | null | undefined, d = 2) =>
  v == null || !Number.isFinite(v) ? '—' : v.toFixed(d);

function scoreColor(s: number | null): string {
  if (s == null || !Number.isFinite(s)) return C.textDim;
  if (s > 60) return C.good;
  if (s >= 40) return C.warn;
  return C.danger;
}

export function HabitatPane() {
  const { habitatResult, habitatStatus, habitatError } = useBacktestStore();
  const [expanded, setExpanded] = useState(false);
  const loading = habitatStatus === 'loading';
  const r = habitatResult;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', background: C.bg, minHeight: 0 }}>
      <div style={{ flexShrink: 0, padding: '4px 10px', background: C.bgPanel, borderBottom: `1px solid ${C.borderSoft}`, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ ...mono, fontSize: 9, color: C.textDim, letterSpacing: '0.08em' }}>MR habitat · surrogate-relative</span>
        {loading && <span style={spinner} />}
      </div>

      <div style={{ flex: 1, minHeight: 0, overflow: 'auto', padding: 12 }}>
        {!r && !loading && (
          <div style={{ ...mono, fontSize: 11, color: C.textDim, display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
            {habitatStatus === 'error'
              ? <span style={{ color: C.danger }}>✕ {habitatError}</span>
              : 'Select a window to score'}
          </div>
        )}
        {loading && !r && (
          <div style={{ ...mono, fontSize: 10, color: C.textDim, display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>scoring window…</div>
        )}
        {r && <Collapsed r={r} onExpand={() => setExpanded(true)} stale={habitatStatus === 'error'} err={habitatError} />}
      </div>

      {expanded && r && <ExpandedOverlay r={r} onCollapse={() => setExpanded(false)} />}

      <style>{`@keyframes cockpit-spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}

function Collapsed({ r, onExpand, stale, err }: { r: HabitatResponse; onExpand: () => void; stale: boolean; err: string | null }) {
  const cb = r.calibration_badge;
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10, height: '100%' }}>
      {/* big score */}
      <div style={{ textAlign: 'center' }}>
        <div style={{ ...mono, fontSize: 44, lineHeight: 1, color: scoreColor(r.score) }}>
          {r.score == null ? '—' : r.score.toFixed(1)}
        </div>
        <div style={{ ...mono, fontSize: 9, color: C.textDim, marginTop: 2 }}>habitat score · 0–100</div>
      </div>

      {/* calibration badges */}
      <div style={{ display: 'flex', gap: 6, justifyContent: 'center', flexWrap: 'wrap' }}>
        <Badge tone="good">OU {fmt(cb.ou, 1)}</Badge>
        <Badge tone="neutral">RW {fmt(cb.rw, 1)}</Badge>
        <Badge tone="danger">trend {fmt(cb.trend, 1)}</Badge>
        {cb.status === 'validated_non_inverting' && <Badge tone="good">validated_non_inverting</Badge>}
      </div>

      {/* mini surrogate cloud (pure CSS) */}
      <MiniCloud r={r} />

      {r.data_warning && (
        <div style={{ ...mono, fontSize: 9, color: C.warn, background: C.warnBg, border: `1px solid ${C.warnBorder}`, borderRadius: 3, padding: '4px 6px' }}>
          ⚠ {r.data_warning}
        </div>
      )}
      {stale && err && (
        <div style={{ ...mono, fontSize: 9, color: C.danger }}>✕ last score failed: {err}</div>
      )}

      <button onClick={onExpand} style={expandBtn}>Expand ↓</button>
    </div>
  );
}

// horizontal bar: p10 / p50 / p90 ticks + real min-VR vertical line (lower = more MR)
function MiniCloud({ r }: { r: HabitatResponse }) {
  const sd = r.surrogate_distribution;
  const real = r.real_min_vr;
  const vals = [sd.p10, sd.p50, sd.p90, real].filter((v): v is number => v != null && Number.isFinite(v));
  if (vals.length < 2) return <div style={{ ...mono, fontSize: 9, color: C.textDim }}>no surrogate cloud</div>;
  let lo = Math.min(...vals), hi = Math.max(...vals);
  const pad = (hi - lo) * 0.08 || 0.01;
  lo -= pad; hi += pad;
  const span = hi - lo || 1;
  const pct = (v: number | null) => v == null || !Number.isFinite(v) ? null : ((v - lo) / span) * 100;
  const p10x = pct(sd.p10), p50x = pct(sd.p50), p90x = pct(sd.p90), realx = pct(real);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <span style={{ ...mono, fontSize: 8.5, color: C.textDim, letterSpacing: '0.06em', textTransform: 'uppercase' }}>
        surrogate cloud · null min-VR (n={sd.n}) · frac≥real {fmt(sd.frac_ge_real, 3)}
      </span>
      <div style={{ position: 'relative', height: 26, background: '#0d1520', border: `1px solid ${C.border}`, borderRadius: 3 }}>
        {/* p10–p90 band */}
        {p10x != null && p90x != null && (
          <div style={{ position: 'absolute', top: 4, bottom: 4, left: `${p10x}%`, width: `${Math.max(0, p90x - p10x)}%`, background: 'rgba(88,166,255,0.18)', borderRadius: 2 }} />
        )}
        {p10x != null && <Tick x={p10x} c={C.text} label="p10" />}
        {p50x != null && <Tick x={p50x} c={C.textBright} label="p50" />}
        {p90x != null && <Tick x={p90x} c={C.text} label="p90" />}
        {realx != null && <Tick x={Math.max(0, Math.min(100, realx))} c={C.accent} label="real" bold />}
      </div>
    </div>
  );
}

function Tick({ x, c, label, bold }: { x: number; c: string; label: string; bold?: boolean }) {
  return (
    <div style={{ position: 'absolute', top: 0, bottom: 0, left: `${x}%`, width: 0, borderLeft: `${bold ? 2 : 1}px solid ${c}` }}>
      <span style={{ position: 'absolute', top: -1, left: 2, ...mono, fontSize: 7.5, color: c, whiteSpace: 'nowrap', fontWeight: bold ? 700 : 400 }}>{label}</span>
    </div>
  );
}

// ── expanded overlay (over the bottom row) ──
function ExpandedOverlay({ r, onCollapse }: { r: HabitatResponse; onCollapse: () => void }) {
  const sd = r.surrogate_distribution;
  const bins = binForHistogram(sd.null_min_vr, 36);
  const maxCount = Math.max(...bins.map(b => b.count), 1);
  const lo = bins.length ? bins[0].x0 : 0;
  const hi = bins.length ? bins[bins.length - 1].x1 : 1;
  const span = hi - lo || 1;
  const realX = r.real_min_vr != null && Number.isFinite(r.real_min_vr) ? ((r.real_min_vr - lo) / span) * 100 : null;

  return (
    <div style={{ position: 'fixed', left: 0, right: 0, bottom: 0, height: '46vh', zIndex: 40, background: 'rgba(7,11,16,0.97)', borderTop: `1px solid ${C.accentBorder}`, boxShadow: '0 -8px 24px rgba(0,0,0,0.5)', display: 'flex', flexDirection: 'column', padding: 16, gap: 12 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ ...mono, fontSize: 12, color: C.textBright, letterSpacing: '0.06em' }}>
          MR habitat · {r.window.start} → {r.window.end} · score <span style={{ color: scoreColor(r.score) }}>{r.score == null ? '—' : r.score.toFixed(1)}</span>
        </span>
        <button onClick={onCollapse} style={expandBtn}>Collapse ↑</button>
      </div>

      {r.data_warning && (
        <div style={{ ...mono, fontSize: 10, color: C.warn, background: C.warnBg, border: `1px solid ${C.warnBorder}`, borderRadius: 3, padding: '6px 8px' }}>
          ⚠ {r.data_warning}
        </div>
      )}

      <div style={{ display: 'flex', gap: 18, flex: 1, minHeight: 0 }}>
        {/* full surrogate cloud histogram */}
        <div style={{ flex: '1 1 60%', display: 'flex', flexDirection: 'column', minWidth: 0 }}>
          <span style={{ ...mono, fontSize: 9, color: C.textDim, letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 4 }}>
            surrogate cloud · null min-VR distribution (n={sd.n})
          </span>
          <div style={{ position: 'relative', flex: 1, minHeight: 0, background: C.bg, border: `1px solid ${C.border}`, borderRadius: 4, padding: '8px 6px 18px' }}>
            <div style={{ position: 'absolute', inset: '8px 6px 18px', display: 'flex', alignItems: 'flex-end', gap: 1 }}>
              {bins.map((b, i) => (
                <div key={i} title={`[${b.x0.toFixed(2)}, ${b.x1.toFixed(2)}) · ${b.count}`}
                  style={{ flex: 1, height: `${(b.count / maxCount) * 100}%`, background: 'rgba(88,166,255,0.3)', minHeight: b.count > 0 ? 1 : 0 }} />
              ))}
            </div>
            {realX != null && (
              <div style={{ position: 'absolute', top: 8, bottom: 18, left: `${Math.max(0, Math.min(100, realX))}%`, width: 0, borderLeft: `2px solid ${C.accent}` }}>
                <span style={{ position: 'absolute', top: 0, left: 3, ...mono, fontSize: 9, color: C.accent, fontWeight: 700 }}>real {fmt(r.real_min_vr, 3)}</span>
              </div>
            )}
            <span style={{ position: 'absolute', left: 6, bottom: 3, ...mono, fontSize: 8, color: C.textDim }}>{lo.toFixed(2)}</span>
            <span style={{ position: 'absolute', right: 6, bottom: 3, ...mono, fontSize: 8, color: C.textDim }}>{hi.toFixed(2)}</span>
          </div>
        </div>

        {/* VR(q) curve */}
        <div style={{ flex: '1 1 40%', display: 'flex', flexDirection: 'column', minWidth: 0 }}>
          <span style={{ ...mono, fontSize: 9, color: C.textDim, letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 4 }}>VR(q) curve</span>
          <VRCurve points={r.vr_curve} />
        </div>
      </div>
    </div>
  );
}

function VRCurve({ points }: { points: { q: number; vr: number | null }[] }) {
  const pts = points.filter(p => p.vr != null && Number.isFinite(p.vr)) as { q: number; vr: number }[];
  if (pts.length < 2) return <div style={{ ...mono, fontSize: 10, color: C.textDim }}>insufficient VR points</div>;
  const W = 300, H = 140, padX = 28, padY = 14;
  const qs = pts.map(p => p.q), vrs = pts.map(p => p.vr);
  const qMin = Math.min(...qs), qMax = Math.max(...qs);
  const vMin = Math.min(...vrs, 1), vMax = Math.max(...vrs, 1);
  const sx = (q: number) => padX + ((q - qMin) / (qMax - qMin || 1)) * (W - 2 * padX);
  const sy = (v: number) => H - padY - ((v - vMin) / (vMax - vMin || 1)) * (H - 2 * padY);
  const path = pts.map((p, i) => `${i ? 'L' : 'M'}${sx(p.q).toFixed(1)},${sy(p.vr).toFixed(1)}`).join(' ');
  const y1 = sy(1);

  return (
    <div style={{ flex: 1, minHeight: 0, background: C.bg, border: `1px solid ${C.border}`, borderRadius: 4, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: '100%' }} preserveAspectRatio="xMidYMid meet">
        {/* VR=1 reference (random walk) */}
        <line x1={padX} y1={y1} x2={W - padX} y2={y1} stroke={C.border} strokeDasharray="3 3" />
        <text x={W - padX + 2} y={y1 + 3} fontSize="8" fill={C.textDim} fontFamily="monospace">1</text>
        <path d={path} fill="none" stroke={C.accent} strokeWidth={1.5} />
        {pts.map(p => (
          <g key={p.q}>
            <circle cx={sx(p.q)} cy={sy(p.vr)} r={2.5} fill={C.accent} />
            <text x={sx(p.q)} y={H - 3} fontSize="8" fill={C.textDim} fontFamily="monospace" textAnchor="middle">q{p.q}</text>
          </g>
        ))}
      </svg>
    </div>
  );
}

const expandBtn: React.CSSProperties = {
  ...mono, fontSize: 10, color: C.accent, background: C.accentBg,
  border: `1px solid ${C.accentBorder}`, borderRadius: 3, padding: '3px 12px', cursor: 'pointer',
  alignSelf: 'center', marginTop: 'auto',
};

const spinner: React.CSSProperties = {
  width: 10, height: 10, border: `1.5px solid ${C.border}`, borderTopColor: C.accent,
  borderRadius: '50%', display: 'inline-block', animation: 'cockpit-spin 0.7s linear infinite',
};
