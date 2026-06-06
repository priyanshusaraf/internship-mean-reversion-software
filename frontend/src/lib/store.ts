import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { InstrumentMeta, BacktestResult } from './types';

// ── Workstation store ──────────────────────────────────────────────────────────

interface DateRange {
  start: string | null;
  end: string | null;
}

interface WorkstationState {
  instruments: InstrumentMeta[];
  selectedInstrumentId: string | null;
  dateRange: DateRange;

  estimatorEnabled: boolean;
  estimatorWindow: number;
  estimatorMode: 'causal' | 'full_info';

  activeWorkbenchModule: string;

  setInstruments: (instruments: InstrumentMeta[]) => void;
  selectInstrument: (id: string) => void;
  setDateRange: (range: DateRange) => void;
  toggleEstimator: () => void;
  setEstimatorWindow: (n: number) => void;
  setEstimatorMode: (mode: 'causal' | 'full_info') => void;
  setActiveWorkbenchModule: (id: string) => void;
}

export const useWorkstationStore = create<WorkstationState>((set) => ({
  instruments: [],
  selectedInstrumentId: null,
  dateRange: { start: null, end: null },
  estimatorEnabled: false,
  estimatorWindow: 20,
  estimatorMode: 'causal',
  activeWorkbenchModule: 'estimator-inspector',

  setInstruments: (instruments) => set({ instruments }),
  selectInstrument: (id) => set({ selectedInstrumentId: id, dateRange: { start: null, end: null } }),
  setDateRange: (range) => set({ dateRange: range }),
  toggleEstimator: () => set((s) => ({ estimatorEnabled: !s.estimatorEnabled })),
  setEstimatorWindow: (n) => set({ estimatorWindow: n }),
  setEstimatorMode: (mode) => set({ estimatorMode: mode }),
  setActiveWorkbenchModule: (id) => set({ activeWorkbenchModule: id }),
}));

// ── UI settings store (persisted to localStorage) ─────────────────────────────

export interface UISettings {
  fontScale: number;     // 0.75–2.0; multiplies base font sizes
  leftWidth: number;     // InstrumentPanel width px
  rightWidth: number;    // EstimatorPanel width px
  chartSplit: number;    // % of vertical space for the chart (30–80)
  lineWidth: number;     // chart overlay line width px
}

const UI_DEFAULTS: UISettings = {
  fontScale: 1.0,
  leftWidth: 220,
  rightWidth: 176,
  chartSplit: 60,
  lineWidth: 1.5,
};

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

interface BacktestState {
  start: string;                 // ISO date (config window lower bound)
  end: string;                   // ISO date (config window upper bound — hard firewall)
  status: BacktestStatus;
  result: BacktestResult | null;
  error: string | null;
  lastRunAt: string | null;      // ISO timestamp of the last successful fetch

  setStart: (d: string) => void;
  setEnd: (d: string) => void;
  runStart: () => void;          // status → loading, clears prior error
  runSuccess: (result: BacktestResult, at: string) => void;
  runError: (message: string) => void;
}

export const useBacktestStore = create<BacktestState>((set) => ({
  start: '',
  end: '',
  status: 'idle',
  result: null,
  error: null,
  lastRunAt: null,

  setStart: (d) => set({ start: d }),
  setEnd: (d) => set({ end: d }),
  runStart: () => set({ status: 'loading', error: null }),
  runSuccess: (result, at) => set({ status: 'idle', result, error: null, lastRunAt: at }),
  runError: (message) => set({ status: 'error', error: message, result: null }),
}));
