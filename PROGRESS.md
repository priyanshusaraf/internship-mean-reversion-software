# AMR Research System — Progress Summary

> **As of 2026-06-01.** Feed this file wherever you need to re-establish context.

---

## What This System Is

**Adaptive Mean Reversion (AMR) Research System** — a temporally honest, research-grade market intelligence and falsification engine. The goal is to understand mean reversion inside structurally trendy markets, not to trade or build dashboards.

Core principle: **correctness > speed, simplicity > sophistication, falsification before optimization.**

---

## Overall Status: Phase 1 Complete + Phase 2 Research Workbench Fully Built

The v0 specification is essentially complete. Both the backend and frontend are fully functional and wired end-to-end. The system is runnable today.

---

## v0 Scope Checklist (from CLAUDE.md)

| Item | Status | Notes |
|------|--------|-------|
| CSV / Parquet ingestion | ✅ Done | `loader.py` handles both; date alias resolution, volume normalization, duplicate rejection, timezone stripping |
| OHLCV loading | ✅ Done | `store.py` + DuckDB; `GET /{id}/ohlcv` with date range filtering |
| Futures roll handling | ✅ Done (ADR) | ADR_003 documents the decision; loader handles roll-adjusted files transparently |
| DuckDB integration | ✅ Done | File-backed `.duckdb`; `instruments` + `ohlcv` tables; per-request connections; test-injectable `_conn` |
| Full-information mode | ✅ Done | `compute_full_ema` (adjust=True); exposed in `/diagnostics` as `mu_star_adj` |
| Causal mode | ✅ Done | `compute_ema` (adjust=False, no lookahead by construction); temporal firewall tested |
| Equilibrium estimation (μ*) | ✅ Done | EMA-based μ* on causal path; exposed at `/estimator` and `/research` endpoints |
| Equilibrium comparison | ✅ Done | Both modes returned in single `/diagnostics` call; Δ gap series computed |
| Interval selection | ✅ Done | `IntervalBar` component: 1M/3M/6M/1Y/2Y/ALL presets + raw date inputs |
| Historical replay | ✅ Done | `end` param on all endpoints strictly limits data; `TimelineRail` in Workbench |
| Synthetic null testing | ✅ Done | `test_analytics_validation.py`: OU process, random walk, trend, ACF ground truth, replay boundary |
| Lag illusion testing | ✅ Done | Documented artifact: EMA residuals of random walk show ACF ≈ 0.88; UI warns, test documents |
| Thin UI | ✅ Done | Two pages (Workstation + Workbench), no retail dashboard aesthetics |

**Not yet built (intentionally deferred):** State T detection, execution logic, signal engine, HMMs, ML complexity, real-time infrastructure.

---

## Backend

### Stack
- FastAPI 0.115+, Python 3.13, DuckDB 1.1+, Pandas 2.2+, NumPy, Statsmodels, Pydantic v2

### File Structure

```
backend/
  app/
    main.py                  # FastAPI app, CORS, lifespan (DB init), health check
    models/
      market.py              # All Pydantic models (OHLCV, Diagnostics, Research, Estimator)
    services/
      loader.py              # load_ohlcv() — CSV/Parquet ingestion with validation
      store.py               # DuckDB layer — init, store, list, query instruments/ohlcv
      analytics.py           # All analytics functions (see below)
    routers/
      market.py              # All API endpoints
  tests/
    conftest.py
    test_health.py
    test_loader.py
    test_store.py
    test_market_router.py
    test_estimator.py
    test_analytics_validation.py   # Synthetic ground-truth validation suite
```

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/market/load` | Load CSV/Parquet into DuckDB |
| GET | `/api/v1/market/instruments` | List all loaded instruments |
| GET | `/api/v1/market/{id}/ohlcv` | OHLCV bars (date-range filtered) |
| GET | `/api/v1/market/{id}/estimator` | μ* EMA values (causal) |
| GET | `/api/v1/market/{id}/research` | close + μ* + ε with summary stats |
| GET | `/api/v1/market/{id}/diagnostics` | Full dual-mode payload (see below) |

### `/diagnostics` Payload — The Core Research Endpoint

Returns per-bar:
- `close`, `mu_star` (causal EMA), `mu_star_adj` (full-info EMA), `mu_star_diff` (Δ gap)
- `epsilon` (causal residual), `epsilon_adj`, `epsilon_rolling_mean`, `epsilon_rolling_std`, `epsilon_zscore`
- `innovation` (one-step prediction error: close[t] − μ*[t−1])

Returns stats:
- `epsilon_mean/std/skew/kurt`, `acf_lag1/5/10/20`, `halflife_bars`, `mu_star_diff_mean/max`, `n`

### Analytics Layer (`analytics.py`)

| Function | Description | Notes |
|----------|-------------|-------|
| `compute_ema(closes, span)` | Causal EMA — `adjust=False` | No future information |
| `compute_full_ema(closes, span)` | Full-info EMA — `adjust=True` | Differs from causal only during warmup |
| `compute_residual(close, mu_star)` | ε = close − μ* | |
| `compute_zscore(residual, window)` | Rolling z-score | |
| `compute_acf(series, lags)` | ACF via statsmodels FFT | Lags [1, 5, 10, 20] |
| `compute_halflife(residuals)` | OU half-life via OLS with intercept | ADF t-stat guard (< −2.86); returns None if not mean-reverting |
| `compute_innovation(close, mu_star)` | close[t] − μ*[t−1] | One-step prediction error |

**Key design decision on `compute_halflife`:** OLS includes an intercept term. Without it, EMA lag on a trending price creates a nonzero mean in ε that biases λ toward zero, making the series appear non-mean-reverting. The intercept absorbs the level offset. Also guards against false positives with an ADF-equivalent t-stat cutoff of −2.86 (5% MacKinnon 1994).

**Known documented artifact:** EMA residuals of a random walk will return a short half-life (~6 bars for EMA-20) because EMA smoothing induces AR structure in its own residuals. This is not a bug — it's documented in `test_analytics_validation.py` and warned about in the UI.

### Temporal Integrity

The `end` query parameter on all endpoints is a hard temporal firewall — it restricts both the data slice and any rolling computation to `date ≤ end`. EMA is causal by construction (pandas `ewm(adjust=False)` only uses data up to and including bar t). The spike contamination test (`test_diagnostics_no_future_data_in_metrics`) verifies this invariant: a future price spike cannot change μ* computed at an earlier date.

### Test Suite

```
test_health.py               — 1 test (health check)
test_loader.py               — 7 tests (CSV/Parquet loading, edge cases)
test_store.py                — 5 tests (DuckDB store/query)
test_market_router.py        — 8 tests (router integration)
test_estimator.py            — 5 tests (EMA unit + temporal integrity)
test_analytics_validation.py — 12 tests across:
  TestHalflifeRecovery        — OU with known λ, intercept fix, trend contamination
  TestRandomWalkSanity        — RW not classified as MR; EMA artifact documented
  TestTrendProcess            — EMA lag on trend; innovation scales with trend speed
  TestReplayBoundary          — End-date firewall integration; bar-by-bar stepping; future spike test
  TestACFGroundTruth          — AR(1) rho=0.6 recovery; white noise near-zero
```

---

## Frontend

### Stack
- Next.js 15, TypeScript, Tailwind CSS, `lightweight-charts` v4, Zustand

### Two Pages

#### 1. Workstation (`/`) — Data Loading + Chart Surface

The primary data surface. Load instruments, inspect candles, overlay μ*, select date ranges.

Layout: `InstrumentPanel` (left sidebar) | `ChartWorkspace` + `ResearchSurface` (main, 60/40 split) | `EstimatorPanel` (right sidebar)

| Component | File | Function |
|-----------|------|----------|
| `InstrumentPanel` | `workspace/InstrumentPanel.tsx` | File path + ID input; load → list instruments; click to select |
| `IntervalBar` | `workspace/IntervalBar.tsx` | Preset buttons (1M/3M/6M/1Y/2Y/ALL) + date range inputs |
| `ChartWorkspace` | `workspace/ChartWorkspace.tsx` | `lightweight-charts` candlestick; causal EMA overlay (toggled); resize-aware; OHLCV loads first, estimator additive |
| `EstimatorPanel` | `workspace/EstimatorPanel.tsx` | Toggle EMA overlay on chart; window control; placeholder rows for Rolling Mean / Kalman / VWAP (dimmed, not yet built) |
| `ResearchSurface` | `workspace/ResearchSurface.tsx` | Research data table below the chart |

#### 2. Workbench (`/workbench`) — Diagnostic Research Modules

The research surface. Five swappable diagnostic modules. All consume `/diagnostics`. No instrument re-loading needed — shares Zustand store.

Layout: `ContextBar` (top) | `ModuleNav` (left) + active module viewport (center) + `ResearchControls` (right) | `TimelineRail` (bottom)

| Module | ID | Description |
|--------|----|-------------|
| **EstimatorInspector** | `estimator-inspector` | Price + causal μ* + adjusted μ* on one chart; Δ initialization gap on sub-chart; stats sidebar (n, Δ mean/max, ε stats, ACF, half-life) |
| **ResidualObservatory** | `residual-observatory` | ε time series + rolling ±1σ bands; ε histogram with normal overlay (red/green bins, blue curve); ACF bar chart at lags 1/5/10/20; stats panel |
| **AssumptionValidator** | `assumption-validator` | Four `TestStrip` sparklines: \|ε z-score\| > 2σ, rolling σ(ε), \|ε\| > 2σ, innovation \|close[t]−μ*[t−1]\|; PASS/FAIL status per strip; interpretation panel summarizing active violations |
| **CausalDiff** | `causal-diff` | Time series of Δε = ε_causal − ε_adj and Δμ* (initialization gap); scatter plot of Δμ* vs +5-bar forward returns with Pearson r; gap statistics |
| **EventLog** | `event-log` | Auto-detected events: ε spikes (2σ/3σ), ε zero crossings, causal divergence; manual annotation input with date tagging; click row → jumps to that date in TimelineRail |

### State Management (`lib/store.ts`)

Zustand store with:
- `instruments` — loaded instrument list
- `selectedInstrumentId` — active instrument
- `dateRange` — `{start, end}` — shared across Workstation and Workbench
- `estimatorEnabled`, `estimatorWindow`, `estimatorMode` (`'causal' | 'full_info'`)
- `activeWorkbenchModule` — which module is active in `/workbench`

### API Client (`lib/api.ts`)

Typed fetch wrappers for all six endpoints. Base URL from `NEXT_PUBLIC_API_URL` env var (defaults to `http://localhost:8000`).

---

## Data

- `data/raw/nifty_synthetic.csv` — 500-bar synthetic OHLCV for smoke testing
- `data/amr.duckdb` — persistent DuckDB file (created on first server start)

---

## Running the System

```bash
# Backend
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm run dev
# → http://localhost:3000
```

Tests:
```bash
cd backend
source .venv/bin/activate
python -m pytest -v
```

---

## Architecture Decisions (ADRs)

| ADR | Decision |
|-----|---------|
| ADR_001 | Local-first — no cloud, no remote DB, one researcher on one machine |
| ADR_002 | Temporal integrity — causal EMA as μ*, `end` param as hard firewall, every computation has a `full_info` variant |
| ADR_003 | Roll adjustment — loader handles roll-adjusted files transparently; no automatic continuous contract construction |

---

## What Is Next (Not Yet Built)

These are **intentionally deferred** per the v0 spec in CLAUDE.md:

1. **Kalman μ* estimator** — In-progress at session interruption. Would add `compute_kalman_mu_star()` to `analytics.py` and expose via `/estimator?estimator=kalman`. The `EstimatorPanel` already has a "Kalman" placeholder row.
2. **Rolling Mean estimator** — Similar; `EstimatorPanel` has placeholder.
3. **State T detection** — Deferred until equilibrium behavior is well understood.
4. **Regime classifiers** — Post-State-T work.
5. **HMMs / ML complexity** — Intentionally out of v0.
6. **Real-time / execution** — Not in scope.
7. **Synthetic null / lag illusion UI panels** — Tests exist; dedicated UI panels not yet built.
8. **Futures roll constructor** — Loader handles pre-adjusted files; automatic construction deferred.

---

## Known Limitations and Technical Debt

| Item | Status |
|------|--------|
| EMA artifact: high ACF does not prove mean-reversion | Documented in tests + UI warning in ResidualObservatory |
| Half-life of EMA residuals of random walk ≈ 6 bars (artifact, not signal) | Documented in `test_ema_residual_of_rw_halflife_known_limitation` |
| DuckDB file connection is single-writer; concurrent requests serialized | Acceptable for single-researcher local use |
| No rolling ADF/KPSS in AssumptionValidator — uses ε-based proxies | Noted in component footer; deferred |
| EventLog manual annotations are ephemeral (session-only) | Acceptable for v0; persistence deferred |
| `mu_star_diff` (EMA init gap) is nonzero only in the first ~3×span bars | Expected behavior, documented in CausalDiff |
| Spread OHLC high/low use symmetric β (high_A − β×high_B) | Acknowledged approximation; close series is the research-valid series |

---

## Session Update — 2026-06-04

### Feature: Synthetic Spread Construction

**Backend** (`backend/app/routers/market.py`):
- `POST /api/v1/market/spread` — new endpoint; params: `instrument_a`, `instrument_b`, `beta` (float), optional `spread_id`
- Inner-joins both legs on date history; constructs spread OHLCV: `O/H/L/C = leg_A − β × leg_B`, `volume = 0`
- Stored as a new instrument in DuckDB; `file_path = spread://A-β*B` tag preserves provenance
- Returns `LoadResponse` (same contract as `/load`); error handling for missing instruments and no overlapping dates
- OHLC note: high/low apply β symmetrically — acknowledged approximation; `close` is the research-valid series

**Frontend** (`frontend/…/InstrumentPanel.tsx`):
- Tab switcher: **Load** | **Spread** tabs in InstrumentPanel
- Spread tab: Leg A dropdown, Leg B dropdown, β numeric input, optional name override, live formula preview (e.g. `NG12 − 1×G1`), Create Spread button
- Spread instruments tagged with ⇌ icon in list; reload button hidden (path is virtual)
- Spread instruments are full first-class citizens: selectable, chartable, pass through all analytics (MRScore, substrate, diagnostics, Kalman)

### Fixes (same session)

**Intraday resampling** (`backend/app/services/loader.py`):
- `load_ohlcv()` now auto-detects intraday data (multiple bars/day) and resamples to daily OHLCV (open=first, high=max, low=min, close=last, volume=sum) before storing
- Previously crashed with a 500 error on 60-min futures files; now handled transparently

**UI settings panel**:
- ⚙ icon in nav opens Settings panel; state persisted to localStorage
- Controls: font scale (XS–2X), left/right panel widths, chart/research split %, graph line width
- Drag handles on both sidebars for live resize

**Drag & drop + multi-file upload**:
- Drop `.csv` / `.parquet` files directly onto InstrumentPanel; filename stem used as `instrument_id`
- Path autocomplete backed by server-side glob suggestions

### API Endpoint Table (updated)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/market/load` | Load CSV/Parquet into DuckDB |
| POST | `/api/v1/market/spread` | Construct synthetic spread and store as instrument |
| GET | `/api/v1/market/instruments` | List all loaded instruments (including spreads) |
| GET | `/api/v1/market/{id}/ohlcv` | OHLCV bars (date-range filtered) |
| GET | `/api/v1/market/{id}/estimator` | μ* EMA values (causal) |
| GET | `/api/v1/market/{id}/research` | close + μ* + ε with summary stats |
| GET | `/api/v1/market/{id}/diagnostics` | Full dual-mode payload |
