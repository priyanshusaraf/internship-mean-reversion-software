---
name: amr-invariants
description: Non-negotiable system invariants, v0 scope boundary, frozen tech stack, dual-mode requirement — governs all planning sessions
metadata:
  type: project
---

## Core invariants (never silently violate)

1. **Temporal integrity is sacred.** At time t, only data ≤ t in causal mode. Lookahead is never silently acceptable.
2. **Dual-mode requirement.** Every major computation supports full-information mode (understanding) AND causal mode (research validity). The distinction is about computation, not operating mode.
3. **No overengineering.** One serious researcher working locally. No microservices, Redis, Celery, Docker complexity, event buses.
4. **No premature abstraction.** Simplest working implementation first.
5. **v0 scope is frozen.** See CLAUDE.md §10 for the complete list.

## State T detection boundary (hard-frozen)

- Permitted: State T observability research, falsification, manual observational diagnostics, equilibrium stability analysis.
- FORBIDDEN NOW: State T detection/classification, MRScore productionization, hazard models, signal engine, execution logic, HMMs, ML complexity, real-time infrastructure.
- Critical distinction: State T observability ≠ State T detection.

## Phase 4 status (2026-06-02)

State T existence confidence: LOW. Real-cohort unanimous negative. See [[state_t_phase4_falsification]].

## Frozen tech stack

Frontend: Next.js 15, React, TypeScript, Tailwind, shadcn/ui, Framer Motion, Zustand, React Query, lightweight-charts, Plotly.
Backend: FastAPI, Python, Pandas, Polars, NumPy, SciPy, Statsmodels, Scikit-Learn, FilterPy, ARCH, DuckDB, Parquet, pytest, hypothesis, black, ruff, mypy.

**How to apply:** Any proposal to change the stack requires explicit freeze-break justification before proceeding.
