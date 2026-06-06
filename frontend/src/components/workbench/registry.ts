import type { WorkbenchModule } from './types';
import { EstimatorInspector } from './modules/EstimatorInspector';
import { ResidualObservatory } from './modules/ResidualObservatory';
import { AssumptionValidator } from './modules/AssumptionValidator';
import { CausalDiff } from './modules/CausalDiff';
import { EventLog } from './modules/EventLog';
import { EstimatorCompare } from './modules/EstimatorCompare';
import { VelocityAbsorption } from './modules/VelocityAbsorption';
import { MRScore } from './modules/MRScore';
import { SubstrateCharacter } from './modules/SubstrateCharacter';
import { Replay } from './modules/Replay';
// NOTE: LagIllusion (#12 LAG) intentionally NOT imported/registered — research verdict C-KILLED
// (see docs/research/07_lag_illusion.md). Module file retained inert for the documented revisit
// trigger (range-bound real data). Do not re-register without re-running the K1–K5 adjudication.

export const WORKBENCH_MODULES: WorkbenchModule[] = [
  {
    id: 'estimator-inspector',
    label: 'Estimator',
    shortLabel: 'EST',
    description: 'Can we trust the estimator right now?',
    component: EstimatorInspector,
    requiredEndpoints: ['diagnostics'],
  },
  {
    id: 'residual-observatory',
    label: 'Residual',
    shortLabel: 'RES',
    description: 'Is residual behavior consistent with our thesis?',
    component: ResidualObservatory,
    requiredEndpoints: ['diagnostics'],
  },
  {
    id: 'replay',
    label: 'Replay',
    shortLabel: 'REP',
    description: 'What would the researcher have actually known at bar t?',
    component: Replay,
    requiredEndpoints: ['diagnostics'],
  },
  {
    id: 'estimator-compare',
    label: 'Compare',
    shortLabel: 'CMP',
    description: 'Does Kalman μ* stay centered inside trends where EMA drifts off?',
    component: EstimatorCompare,
    requiredEndpoints: ['diagnostics'],
  },
  {
    id: 'velocity-absorption',
    label: 'Absorption',
    shortLabel: 'ABS',
    description: 'Did the Kalman velocity state remove useful mean-reversion signal?',
    component: VelocityAbsorption,
    requiredEndpoints: ['velocity-absorption'],
  },
  {
    id: 'mrscore',
    label: 'MRScore',
    shortLabel: 'MRS',
    description: 'How favourable are conditions for mean reversion right now? (observe/falsify, not a signal)',
    component: MRScore,
    requiredEndpoints: ['mrscore'],
  },
  {
    id: 'substrate',
    label: 'Substrate',
    shortLabel: 'SUB',
    description: 'What kind of market are we looking at? (character, not timing — observe/falsify)',
    component: SubstrateCharacter,
    requiredEndpoints: ['substrate'],
  },
  {
    id: 'assumption-validator',
    label: 'Assumptions',
    shortLabel: 'ASM',
    description: 'Are our model assumptions still valid?',
    component: AssumptionValidator,
    requiredEndpoints: ['diagnostics'],
  },
  {
    id: 'causal-diff',
    label: 'Causal Diff',
    shortLabel: 'DIF',
    description: 'How much does hindsight explain?',
    component: CausalDiff,
    requiredEndpoints: ['diagnostics'],
  },
  {
    id: 'event-log',
    label: 'Event Log',
    shortLabel: 'LOG',
    description: 'What changed, and when did the model notice?',
    component: EventLog,
    requiredEndpoints: ['diagnostics'],
  },
];
