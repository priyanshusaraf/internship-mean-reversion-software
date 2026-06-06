import type React from 'react';

export interface ModuleProps {
  instrumentId: string;
  dateRange: { start: string | null; end: string | null };
  estimator: string;
  window: number;
}

export interface WorkbenchModule {
  id: string;
  label: string;
  shortLabel: string;
  description: string;
  component: React.ComponentType<ModuleProps>;
  requiredEndpoints: string[];
}
