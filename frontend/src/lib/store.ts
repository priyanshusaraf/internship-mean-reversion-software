import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { InstrumentMeta, BacktestResult, HabitatResult } from './types';

// ── Workstation store ──────────────────────────────────────────────────────────

interface DateRange {
  start: string | null;
  end: string | null;
}

// Views that participate in global instrument sync. The Workstation is the canonical picker and is
// always live; these three can each be PINNED to hold their own instrument independent of the global.
export type SyncView = 'backtest' | 'workbench' | 'observatory';

interface WorkstationState {
  instruments: InstrumentMeta[];
  selectedInstrumentId: string | null;
  dateRange: DateRange;

  // per-view pins: a present entry means that view is locked to that instrument and IGNORES the
  // global selection. effective(view) = pinned[view] ?? selectedInstrumentId.
  pinned: Partial<Record<SyncView, string>>;

  estimatorEnabled: boolean;
  estimatorWindow: number;
  estimatorMode: 'causal' | 'full_info';

  activeWorkbenchModule: string;

  setInstruments: (instruments: InstrumentMeta[]) => void;
  selectInstrument: (id: string) => void;
  pinView: (view: SyncView, id: string) => void;
  unpinView: (view: SyncView) => void;
  setDateRange: (range: DateRange) => void;
  toggleEstimator: () => void;
  setEstimatorWindow: (n: number) => void;
  setEstimatorMode: (mode: 'causal' | 'full_info') => void;
  setActiveWorkbenchModule: (id: string) => void;
}

export const useWorkstationStore = create<WorkstationState>()(
  persist(
    (set) => ({
      instruments: [],
      selectedInstrumentId: null,
      dateRange: { start: null, end: null },
      pinned: {},
      estimatorEnabled: false,
      estimatorWindow: 20,
      estimatorMode: 'causal',
      activeWorkbenchModule: 'estimator-inspector',

      setInstruments: (instruments) => set({ instruments }),
      selectInstrument: (id) => set({ selectedInstrumentId: id, dateRange: { start: null, end: null } }),
      pinView: (view, id) => set((s) => ({ pinned: { ...s.pinned, [view]: id } })),
      unpinView: (view) => set((s) => { const p = { ...s.pinned }; delete p[view]; return { pinned: p }; }),
      setDateRange: (range) => set({ dateRange: range }),
      toggleEstimator: () => set((s) => ({ estimatorEnabled: !s.estimatorEnabled })),
      setEstimatorWindow: (n) => set({ estimatorWindow: n }),
      setEstimatorMode: (mode) => set({ estimatorMode: mode }),
      setActiveWorkbenchModule: (id) => set({ activeWorkbenchModule: id }),
    }),
    {
      // Persist ONLY the selected instrument id — not the server-owned `instruments` list
      // (refetched on load) nor transient estimator/module UI state. A stale id that no longer
      // exists simply 404s on the next API call; the user reselects.
      name: 'amr-workstation-v1',
      partialize: (s) => ({ selectedInstrumentId: s.selectedInstrumentId, pinned: s.pinned }),
    }
  )
);

// ── UI settings store (persisted to localStorage) ─────────────────────────────

export interface UISettings {
  fontScale: number;     // 0.75–2.0; multiplies base font sizes
  leftWidth: number;     // InstrumentPanel width px
  rightWidth: number;    // EstimatorPanel width px
  chartSplit: number;    // % of vertical space for the chart (30–80)
  lineWidth: number;     // chart overlay line width px
  textColor: string;     // primary text hex; '' = use brightened globals.css default
}

const UI_DEFAULTS: UISettings = {
  fontScale: 1.0,
  leftWidth: 220,
  rightWidth: 176,
  chartSplit: 60,
  lineWidth: 1.5,
  textColor: '',
};

// Default text presets surfaced in Settings. The `value` is the primary text hex;
// '' means "let globals.css :root defaults apply" (the brightened Normal baseline).
export const TEXT_COLOR_PRESETS: { label: string; value: string }[] = [
  { label: 'Dim',    value: '#6b7a8c' },
  { label: 'Normal', value: '' },
  { label: 'Bright', value: '#c2d0de' },
];

// Derive the three text CSS vars from a single chosen primary hex. bright lightens toward
// near-white, dim darkens toward the panel background — keeps the picker to one decision
// while preserving the brightness hierarchy the UI relies on.
export function deriveTextVars(primary: string): { text: string; bright: string; dim: string } {
  return {
    text: primary,
    bright: mixHex(primary, '#e6edf3', 0.4),
    dim: mixHex(primary, '#0a0f16', 0.45),
  };
}

function mixHex(a: string, b: string, t: number): string {
  const pa = parseHex(a);
  const pb = parseHex(b);
  if (!pa || !pb) return a;
  const m = (x: number, y: number) => Math.round(x + (y - x) * t);
  const h = (n: number) => n.toString(16).padStart(2, '0');
  return `#${h(m(pa[0], pb[0]))}${h(m(pa[1], pb[1]))}${h(m(pa[2], pb[2]))}`;
}

function parseHex(hex: string): [number, number, number] | null {
  const m = /^#?([0-9a-f]{6})$/i.exec(hex.trim());
  if (!m) return null;
  const n = parseInt(m[1], 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}

interface UIStore extends UISettings {
  setUI: (s: Partial<UISettings>) => void;
  resetUI: () => void;
}

export const useUIStore = create<UIStore>()(
  persist(
    (set) => ({
      ...UI_DEFAULTS,
      setUI: (s) => set(s),
      resetUI: () => set(UI_DEFAULTS),
    }),
    { name: 'amr-ui-v1' }
  )
);

// ── Backtest store (P&L Cockpit) ──────────────────────────────────────────────
// Isolated slice: only the start/end date window is user-editable (the strategy is FROZEN).
// instrument_id is NOT held here — it is read from useWorkstationStore.selectedInstrumentId at
// run time so the cockpit always targets the instrument loaded on the Workstation.

type BacktestStatus = 'idle' | 'loading' | 'error';
type HabitatStatus = 'idle' | 'loading' | 'error';

interface BacktestState {
  start: string;                 // ISO date (config window lower bound)
  end: string;                   // ISO date (config window upper bound — hard firewall)
  status: BacktestStatus;
  result: BacktestResult | null;
  error: string | null;
  lastRunAt: string | null;      // ISO timestamp of the last successful fetch

  // ── habitat slice (Trade Cockpit Q4) — scored on scrubber RELEASE, never during drag ──
  habitatResult: HabitatResult | null;
  habitatStatus: HabitatStatus;
  habitatError: string | null;

  setStart: (d: string) => void;
  setEnd: (d: string) => void;
  runStart: () => void;          // status → loading, clears prior error
  runSuccess: (result: BacktestResult, at: string) => void;
  runError: (message: string) => void;

  setHabitatResult: (r: HabitatResult) => void;
  setHabitatStatus: (s: HabitatStatus) => void;
  setHabitatError: (e: string | null) => void;
}

export const useBacktestStore = create<BacktestState>((set) => ({
  start: '',
  end: '',
  status: 'idle',
  result: null,
  error: null,
  lastRunAt: null,

  habitatResult: null,
  habitatStatus: 'idle',
  habitatError: null,

  setStart: (d) => set({ start: d }),
  setEnd: (d) => set({ end: d }),
  runStart: () => set({ status: 'loading', error: null }),
  runSuccess: (result, at) => set({ status: 'idle', result, error: null, lastRunAt: at }),
  runError: (message) => set({ status: 'error', error: message, result: null }),

  setHabitatResult: (r) => set({ habitatResult: r, habitatStatus: 'idle', habitatError: null }),
  setHabitatStatus: (s) => set({ habitatStatus: s, ...(s === 'loading' ? { habitatError: null } : {}) }),
  setHabitatError: (e) => set({ habitatError: e, habitatStatus: e ? 'error' : 'idle' }),
}));
