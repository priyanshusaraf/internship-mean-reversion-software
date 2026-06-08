# Session Log — Observatory v2: Contract Freeze + Phase-1 Slice

**Date:** 2026-06-06
**Scope:** First build task of the AMR Observatory & Backtesting interface — STEP 1 (freeze the
API/data contract) + STEP 2 (thin vertical slice). The backtester is a separate, later instruction.
**Governing specs:** `MASTER_DIRECTIVE_STRATEGY_BACKTEST_INTERFACE.md`,
`DIRECTIVE_OBSERVATORY_COCKPIT_FRONTEND.md`, `docs/build/api_contract.md` (frozen).

---

## 0. What was asked

Deliver, in order:
1. **STEP 1** — freeze the API + data contract (`docs/build/api_contract.md`) as the spine that lets
   backend / backtester / frontend work in parallel without diverging. Reviewed and frozen before Step 2.
2. **STEP 2** — build a thin vertical slice (one thread end-to-end): upload a CSV → column-map →
   data-quality report → price chart with a draggable as-of (hide-forward) cursor → Kalman μ* + z
   overlay (causal) → select a window → surrogate-relative habitat score with its null cloud +
   raw-vs-deseason toggle.

Hard constraints carried through the whole task:
- **No statistic reimplemented in JS** — every number comes from the existing frozen Python engines.
- **Causal firewall** — causal computations use only data ≤ the as-of cursor; forward data is
  evaluation-only.
- **Habitat is surrogate-relative** — always shown with its surrogate (null) distribution, never bare.
- **Regime timing is NOT solved** (T2.5 = NO_CONTENT) — no automatic regime-gated signals; build the
  hook, leave it empty. (Not exercised this task.)

---

## 1. Context discovered (existing system)

- **Backend:** FastAPI + DuckDB store + `loader.load_ohlcv` (auto-detects ISO/dayfirst dates,
  resamples intraday→daily, rejects true dupes). Existing router `/api/v1/market/*` already serves
  OHLCV, EMA, and **Kalman μ\*** (via `/diagnostics`, firewalled to data ≤ `end`).
- **Kalman engine** `analytics.compute_kalman_mu_star` — causal 2-state filter; returns
  `mu_star_kalman, epsilon_kalman, kalman_velocity, kalman_gain, kalman_state_var`. Reused as-is.
  Frozen constants `KALMAN_SNR=1e-8, KAPPA=0.05, WARMUP=60`.
- **Habitat engine** `scripts/calibrate_habitat_score.py::habitat_score(x, seed)` — returns only the
  scalar 0–100; the RW + MA(1) null arrays are computed internally then **discarded**. The directive
  needs the surrogate cloud, so this needed a thin distribution-returning wrapper.
- **Frontend:** Next.js 15.5 / React 19 / TypeScript / Tailwind 4 / **lightweight-charts 4.2** /
  zustand / lucide. Existing `/workbench` route + `src/lib/api.ts`. No Plotly.

---

## 2. STEP 1 — the frozen contract

**File:** `docs/build/api_contract.md` · **Commit:** `e837954`

### Decisions (D1–D4)
- **D1** — `dataset` reuses the existing instrument store; `dataset_id == instrument_id`. No parallel
  persistence.
- **D2** — new clean `/api/v2/*` surface; legacy `/api/v1/market/*` workbench untouched. Both call the
  same engines.
- **D3** — habitat surrogate cloud requires a thin wrapper (`habitat_score_full`) returning the null
  arrays the engine already computes — same math, frozen constants unchanged.
- **D4** — single `as_of` causal-cursor convention; `as_of` is never a no-op.

### Adversarial review → mitigations folded in
The first draft was returned **INADMISSIBLE-TO-FREEZE** by `amr-adversarial` (two firewall holes + a
non-functional anti-p-hacking mechanism). All 7 findings were written into the contract before freeze:

| # | Issue | Severity | Fix |
|---|---|---|---|
| 1 | z's σ undefined → forward-vol leak into interior-bar z | CRITICAL | **M1**: σ = causal **expanding** std over `epsilon_kalman[t'≤t]`; fixed basis; future-injection bit-identity test |
| 2 | optional `as_of` silently disables the firewall | CRITICAL | **M2**: `as_of` null ≡ last bar; cap always applied |
| 6 | Verification mode decorative (409 vs nothing) | CRITICAL | **M4**: real pre-reg pin store; verdict path requires a pin |
| 3 | habitat wrapper could drift from frozen score | HIGH | **M3**: one null-generating path; bit-identical score + badge reproduced |
| 5 | frontend could re-percentile `null_min_vr[]` | HIGH | **M5**: backend owns every scalar; array render-only |
| 7 | no rolling-β / construction gate | HIGH | **M6**: `construction.beta_mode`; `rolling-INADMISSIBLE` → 422 |
| 4 | exploratory results promotable to verdicts | MED | `exploratory_watermark` in provenance |

### Endpoints frozen
- `POST /api/v2/datasets` (multipart CSV + column mapping → dataset + quality)
- `GET /api/v2/datasets` · `GET /api/v2/datasets/{id}` · `GET /api/v2/datasets/{id}/series` (as_of +
  forward_bars) · `GET /api/v2/datasets/{id}/quality`
- `POST /api/v2/analysis/equilibrium` (causal μ*, velocity, innovation, causal-expanding z)
- `POST /api/v2/analysis/habitat` (score + **mandatory** surrogate distribution + calibration badge +
  raw-vs-deseason)

(`.gitignore` was also patched: `docs/build/` was being caught by a generic `build/` ignore rule;
un-ignored so the contract is tracked.)

---

## 3. STEP 2 — the vertical slice

**Commit:** `6e1c6ad` · **Sign-off:** `amr-rigor-qa` → **SIGN-OFF GRANTED**

Execution was sequential (backend first as the dependency and live surface, then frontend against the
running backend) so the integration proven by the slice is real, not mocked.

### Backend (`backend-api` agent) — additive, legacy untouched
| File | Purpose |
|---|---|
| `backend/app/services/analytics_habitat.py` | `habitat_score_full(x, seed)` — single null-generating path (M3); VR + RW + MA(1) math copied verbatim, constants unchanged |
| `backend/app/services/observatory_quality.py` | `quality_report(df)` — rows/range/freq/gaps/dupes/non-positive(+excision)/seams; `load_ohlcv_mapped()` optional column-map override |
| `backend/app/models/observatory.py` | Pydantic shapes per contract; non-finite floats → null |
| `backend/app/routers/observatory.py` | `/api/v2` router — all endpoints; as_of resolver (M2); causal z (M1); construction 422 (M6); provenance + watermark |
| `backend/tests/test_observatory_v2.py` | 14 tests (firewall bit-identity, single-path, surrogate-mandatory, construction 422, upload/quality) |
| `scripts/calibrate_habitat_score.py` (mod) | `habitat_score()` now delegates to `habitat_score_full` — one null path |
| `backend/app/main.py` (mod) | registers the v2 router alongside the legacy one |

Sidecar `v2_dataset_meta` table holds column_map / date_format / construction / timezone (store schema
untouched; keyed by dataset_id).

### Frontend (`frontend-architect` agent, integration owner) — additive, `/workbench` + `api.ts` untouched
| File | Purpose |
|---|---|
| `frontend/src/lib/observatory.ts` | typed v2 client; `binForHistogram` (display-only, derives no scalar) |
| `frontend/src/components/observatory/IngestPanel.tsx` | upload → header preview → column-map (auto-detect + override) → POST /datasets |
| `frontend/src/components/observatory/QualityPanel.tsx` | quality report; non-positive flagged + excision, "not auto-dropped" |
| `frontend/src/components/observatory/PriceChart.tsx` | lightweight-charts price + draggable as-of cursor + greyed forward bars + μ* overlay + z sub-pane |
| `frontend/src/components/observatory/HabitatPanel.tsx` | score never bare — always with surrogate cloud; calibration badge; raw↔deseason toggle + contamination flag; provenance |
| `frontend/src/components/observatory/ui.tsx` | shared dark-idiom primitives |
| `frontend/src/app/observatory/page.tsx` | new `/observatory` route |
| `frontend/src/components/AppNav.tsx` (mod) | Observatory nav link |

---

## 4. Rigor sign-off (amr-rigor-qa, code-level audit)

All six applicable checklist items verified **enforced in code** (file:line evidence), not just shown:

- **Firewall (M1/M2):** `_resolve_as_of` null→last bar; series sliced ≤ as_of before any engine; no path
  where forward rows reach an engine; z = `expanding(min_periods=2).std` over innovations. Bit-identity
  tests pass.
- **Surrogate-relative:** `surrogate_distribution` is a non-optional model field; the score never
  renders without its cloud.
- **No-JS-math:** every displayed scalar is backend-verbatim; binning produces bars only.
- **M3 single path:** `habitat_score` delegates; calibration badge reproduced **bit-exactly** OU 71.3 /
  RW 49.2 / trend 17.2.
- **M6:** rolling-INADMISSIBLE → 422 on both analysis endpoints.
- **Provenance:** dataset/hash/as_of/params/mode/exploratory_watermark/computed_at on every result.
- **Isolation:** legacy `/api/v1/market/*` and `api.ts` byte-clean; full suite 160 passed, 1 failed
  (pre-existing unrelated `test_loader.py::test_duplicate_timestamps_rejected`).

**Verdict:** SIGN-OFF GRANTED. Three MEDIUM items logged as Phase-2 hardening, not slice defects:
untested deseason-path firewall; RW+MA(1)-only null cloud (per frozen contract, vs GARCH/OU);
M6 currently guards a door no production code opens yet (no spread endpoint this slice).

---

## 5. Proof artifacts (`docs/build/slice_proof/`)

- `01_quality_ou.png` — OU dataset quality report (300 daily rows, range, non-positive CLEAN, gaps).
- `02_chart_mu_z_cursor.png` — price + μ* + as-of cursor @ 2023-08-18; **135 forward bars greyed**,
  "future — evaluation only, NOT available to the model"; z sub-pane with bands; provenance line.
- `03_habitat_cloud.png` — habitat **score 100.0 WITH its surrogate cloud** (n=2000, real-VR left of
  the null cloud, p10/p90 markers), VR(q) curve, calibration badge, raw 65.8 vs deseason 100.0
  "verdict stable", full provenance.
- `04_nonpositive_excision.png` — CL April-2020 case: 6 non-positive prices flagged, suggested excision
  2020-04-15 → 2020-04-22, "flagged — not auto-dropped".
- `ou_meanrev.csv`, `cl_negative.csv` — reproducible test fixtures.

---

## 6. What works / what does NOT

- **Works:** MR habitat characterization (surrogate-relative), Kalman equilibrium (μ*, velocity,
  innovation), the causal firewall + hide-forward cursor, raw-vs-deseason contamination read,
  data-quality gating (incl. the negative-price case).
- **NOT solved (unchanged):** regime *timing* / transition detection (T2.5 NO_CONTENT). No automatic
  regime-gated signal generation shipped — the hook stays empty. Habitat = characterization, not timing.

---

## 7. Deferred to later instructions (contract-reserved, not defects)

Phase 2: backtester (event-driven, walk-forward, cost-aware) · strategy/signal layer · P&L/metrics
widgets · Research/Verification modes + the pre-reg pin store · trend-death redesign panel.
Phase 3: manual-regime workflow · LE-GF paper-trade cockpit · portfolio view.
Phase 4: the compilation document.
Hardening: deseason-path firewall test · GARCH/OU null families.

---

## 8. Commits this session

```
6e1c6ad  Observatory v2 Phase-1 vertical slice (ingestion→firewall→equilibrium→habitat)
e837954  Freeze Observatory v2 API & data contract (docs/build/api_contract.md)
b72844b  Add 4 build agents: frontend-architect, backend-api, backtest-engine, amr-rigor-qa
```

Left intentionally uncommitted: `.claude/settings.local.json` (local), `CLAUDE.md` (user/linter edit),
`backend/data/amr.duckdb` (restored — test-upload pollution).

---

## 9. How to run it yourself

**Backend** (from `backend/`):
```
.venv/bin/uvicorn app.main:app --port 8000
```
**Frontend** (from `frontend/`):
```
npm run dev          # serves http://localhost:3000
```
Then open **http://localhost:3000/observatory**. Upload a CSV (e.g.
`docs/build/slice_proof/ou_meanrev.csv` for a clean OU series, or `cl_negative.csv` to see the
non-positive-price flag), map the columns, drag the as-of cursor, select a window, read the habitat
score with its surrogate cloud.
