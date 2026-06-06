import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { InstrumentMeta } from './types';

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
