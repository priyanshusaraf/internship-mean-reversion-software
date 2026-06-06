# AMR Research System — Complete Session Brief

> Written 2026-06-03. A self-contained three-layer reference: research arc, empirical verdicts,
> and full code anatomy. Anyone reading this cold should be able to reconstruct where we are,
> what was proven, what failed, and exactly how the system is built.

---

## LAYER 1 — The Research Arc

### 1.1 What this system is trying to do

The **Adaptive Mean Reversion (AMR) Research System** is a falsification engine for a single
economic hypothesis:

> *Mean reversion exists and is tradeable inside structurally trendy markets — and it can be
> detected before it becomes obvious to everyone else.*

That is it. Not a trading bot. Not a backtester. Not a dashboard. A disciplined research tool for
determining whether a specific edge actually exists and can be measured without fooling yourself.

The thesis decomposes into a research programme with five sequential phases:

```
Phase 1: Mean Estimation     → what is μ* (the equilibrium around which reversion happens)?
Phase 2: MR Detection        → does price actually revert to μ*?
Phase 3: Structure Class     → which process (OU / nonlinear-OU / OU+jumps) drives reversion?
Phase 4: Signal Generation   → how do you trade it?
Phase 5: Strategy Optim.     → position sizing, stops, holding period?
```

**Phases 1 and 2 are the active frontier.** Nothing else is in scope. Phases 3–5 are deliberately
deferred until the first two are resolved without contamination.

The test instrument (ADANIENT, the NSE large-cap equity) is a **placeholder** — chosen purely
because real price data was available. It is trend-heavy. The intended deployment domain
(commodities, pairs, spread structures, cross-asset relative value) is expected to be
mean-reverting — the opposite regime. All real-data findings in this project are therefore
**regime-local and provisionally scoped** to ADANIENT's trend regime, not global evidence.

---

### 1.2 Phase 1 completed: the μ* problem and its resolution

Before any reversion signal can be built, you need a credible equilibrium estimate μ*. The naive
approach (rolling mean, EMA) has a known, fatal flaw:

> Inside a trending market, EMA **lags** the price by `slope × span / 2`. This offset is not
> noise — it is a deterministic structural artifact that grows without bound as the trend steepens.
> At EMA-20 span inside a slope-0.25 trend, the residual `ε = P − EMA` has a mean of ≈17 price
> units — roughly 7× the actual deviation's standard deviation. The residual is dominated by the
> lag artifact, not by the deviation. Its sign matches the true deviation sign only 49% of the
> time — worse than a coin flip.

This is the core motivation for testing a 2-state Kalman filter as the equilibrium estimator. The
Kalman carries a **velocity state** alongside a level state, which absorbs the trend's first moment
into the equilibrium track and keeps the innovation centered near zero regardless of slope.

The research conducted for this project:

1. **Formalized the μ* problem** in `docs/research/02_mu_star_equilibrium.md` — the Anchored
   Kalman paper (V2.5), which specifies the full model, its failure modes, and the validation
   architecture.

2. **Built the EMA baseline** — a fully causal EMA with dual-mode (causal / full-information),
   temporal firewall, and a 12-test synthetic ground-truth validation battery.

3. **Failed to reject Kalman** — an initial rejection on `KC4 (alpha absorption)` and
   `KC1 (no artifact reduction)` was later found to be based on a contaminated metric
   (`G-ABSORB` was trend-invariant and κ-invariant — it never actually measured trend contamination)
   and an unsatisfiable gate (the H1 random-walk ACF < 0.20 threshold could not be met by any
   causal smoother, EMA included). Full audit in `docs/research/06_...` §5–§6.

4. **Confirmed the centering advantage** — a pre-registered confirmatory experiment over 360
   paired conditions (30 seeds × 4 slopes × 3 OU strengths) at matched effective span found:
   - `|mean(ε)|`: Kalman ≈ 0.095 vs EMA ≈ 12.19 — two orders of magnitude difference
   - Sign-agreement with true deviation: Kalman ≈ 0.85 vs EMA ≈ 0.49
   - Persistence/shape (ACF, half-life, var_ratio): statistically indistinguishable
   - Wilcoxon p < 1e-30 across all seeds, slopes, OU strengths, SNRs

5. **Demoted centering from a frozen conclusion (Rev 2)** — after integrating Kalman into the
   real-market workbench (Step 1), a methodological critique identified two structural confounds:
   - **S1 (detrending confound):** the matched-span fairness control equalizes level responsiveness
     but not detrending capability. Kalman's centering advantage might just be "the estimator with
     a drift term removes drift" — a tautology, not a market discovery.
   - **S2 (false centering):** the velocity state might absorb genuine reversion into drift, producing
     a spuriously centered residual by eating the signal.

6. **Ran the final cheap empirical gate (Step 2A.5, Rev 4)** — the walk-forward decay test
   (`Δβ = β_restored − β_kalman`) across four pre-declared regime windows of ADANIENT:
   - Δβ sign is incoherent across regimes (W1 sideways: +0.00084, W2 moderate-trend: −0.00231,
     W3 parabolic: +0.00835) — the absorption-prone sideways regime carries the anti-absorption sign
   - R²ₒₒₛ ≈ 0 for both estimators in every regime — neither residual predicts its own decay OOS
   - **Classification: B (unresolved, non-blocking). Catastrophic false centering excluded.**

7. **Current μ* status:** EMA is production μ*. Kalman is a research-only comparison estimator.
   The freeze is explicitly **provisional** (one real underlying, low power). The revisit trigger
   binds before any upstream component depends on μ* reversion fidelity.

---

### 1.3 Phase 2 frontier: MRScore, Substrate, State T

Once μ* was instrumented, the project moved to Phase 2 observatories — all observatory-only,
never wired to signals or gates.

#### MRScore Observatory (doc 09)
A faithful implementation of the three-block MR favorability score from `docs/research/01_amr_framework.md`:

```
MRScore = 0.20 · B1 (Mean Reliability) + 0.60 · B2 (MR Strength) + 0.20 · B3 (Tradability)
```

**Key finding (STRUCTURAL):** the self-ranked percentile architecture (eq. 14, rank within own
252-bar history) erases cross-instrument discrimination. A pure random walk earned the *highest*
MRScore in our blind test. MRScore is a **within-instrument relative favorability read**, not a
cross-instrument reverter-detector. Raw Block-2 features (DRC, HitRate) are the actual
discriminators — but even those are unreliable on a single 600-bar path (~10% false-positive rate
for pure RW drawing DRC < −2.0).

#### Substrate Observatory (doc 10)
Answers "what kind of market is this over the trailing window?" using three causal descriptors:
- **Directional Efficiency (DE)** — |net move| / path length ∈ [0,1]. Trend vs chop axis.
- **Variance Ratio (VR)** — mean of VR(q) at q∈{2,5,10}. OU (<1) vs RW (≈1) vs trend (>1) axis.
- **Realized-vol percentile** — context only, never a character driver.

Output: resemblance scores for four buckets: `{ou_like, trend_like, rw_null, ambiguous}`. 
The engine is correct; ADANIENT reads trend-like as expected (it is trend-heavy).

**Key finding:** discriminates synthetic habitats (OU vs trend vs RW) reliably, but scale-dependence
of the VR is a known limitation. Full-info mode deferred.

#### State T Existence Programme (doc 11)
The most recent work. Asks:

> Is the distribution of residual morphology inside high-deviation windows (|z| ≥ θ for θ∈{1.0, 1.5, 2.0})
> statistically distinguishable from matched synthetic nulls?

**ARM 1 (causal, verdict-bearing):** symmetric partition — no reversion anchoring, no hindsight.
Three descriptors per causal pre-window: innovation variance, ACF(1), directional efficiency.
The comparison is distributional (effect size), never a per-bar quantity.

**UPDATE 2026-06-03 (corrects the two sentences below):** the real-data reads ARE analyzed and
the thesis is **FALSIFIED-IN-FORM / KILLED** (doc 11 Phase 5, 2026-06-02) — across 12 instruments /
5+ habitats, high-|z| windows show directional *continuation* (dir_eff > 0 in all 12), the opposite
of the pre-registered stabilization signature, including the decisive HDFC–ICICI pair spread. The
post-kill institutional review, ranked surviving arms, and next action are in
`docs/research/12_institutional_review_post_state_t.md`.

~~The code is built. The real-data reads have not yet been analyzed to a conclusion. This is
the active work frontier.~~ *(superseded — see UPDATE above)*

---

### 1.4 What is explicitly NOT built (intentional deferrals)

The following are frozen out of scope until the observatory layer returns a verdict:

```
State T detection / classification         — "does T appear to exist?" only, not "is T happening now?"
MRScore productionization                  — it is a diagnostic instrument
Hazard models                             — deferred post State T existence proof
Signal engine                             — Phase 4 work
Execution logic                           — Phase 5 work
HMMs / ML complexity                      — post-observatory phase
Real-time infrastructure                  — not in scope
Regime classifiers                        — State T detection layer, deferred
```

---

## LAYER 2 — What Went Wrong and What We Proved

This layer documents every empirical finding that changed the state of belief — failures,
falsifications, confirmations, and open resolutions.

---

### 2.1 The Kalman rejection that was overturned

**What we initially concluded:**
> Kalman is rejected. KC4 (velocity absorbs alpha): absorption metric G-ABSORB
> failed its pre-registered threshold (0.208 > 0.20). KC1 (no artifact reduction):
> random-walk innovation ACF(1) ≈ 0.95–0.98, worse than EMA.

**What went wrong:**

| Failure | Class | Evidence |
|---------|-------|----------|
| G-ABSORB is trend-invariant | STRUCTURAL | `|corr(velocity, deviation)|` = 0.288 at slope 0.00 AND at slope 2.00 — identical. A metric that doesn't move when the trend goes from absent to dominant is not measuring trend contamination. |
| G-ABSORB is κ-invariant | STRUCTURAL | Sweeping κ ∈ {0, 0.01, 0.05, 0.20, 0.50, 1.00} leaves absorption at 0.288 in every case. The metric ignores the one structural knob that controls velocity process noise. |
| H1 gate is unsatisfiable | METHODOLOGY | EMA-20 itself produces RW residual ACF(1) ≈ 0.88–0.98 at spans where OU recovery passes. Penalizing Kalman for failing a gate EMA also fails is invalid. |
| Knife-edge threshold | METHODOLOGY | 0.208 vs 0.20 against an underived threshold on a metric that doesn't work is not a rejection — it's noise. |
| Environment corruption | IMPLEMENTATION | A numpy warning flood (~11MB to stderr) was initially mistaken for output redaction; contaminated figures from a truncated channel were published in the first memo. |

**What the replication audit confirmed:**
- `corr(ε_kalman, true_deviation) ≈ 0.92` — signal is preserved, not absorbed (KC4 **falsified**)
- `var_ratio = var(ε) / var(deviation) ≈ 1.0` — no signal degradation
- The KC1 gate was internally unsatisfiable by any causal estimator — **invalidated as discriminating criterion**

**Final verdict:** Both stated rejection grounds were wrong. The rejection of Kalman does not stand.

---

### 2.2 What the confirmatory experiment proved

The decisive result (360 conditions, Wilcoxon p < 1e-30):

| Metric | Kalman | EMA | What it means |
|--------|--------|-----|---------------|
| `\|mean ε\|` (centering) | 0.095 | 12.19 | EMA residual mean = `slope × span / 2` — textbook EMA lag bias, confirmed to 3 sig figs |
| Sign-agreement with true deviation | 0.854 | 0.492 | EMA residual sign is a coin flip inside a trend. Kalman recovers the true deviation sign 85% of the time. |
| ACF(1), ACF(5) | ≈0.89 | ≈0.89 | Statistically indistinguishable — persistence is identical at matched span |
| half-life error | 0.099 | 0.130 | Marginally better for Kalman; not the decisive axis |

**The mechanism is analytic, not empirical luck:**

At span=141, slope=0.25: EMA `|mean ε|` = 17.24, theory predicts `slope × span / 2` = 17.63. ✓  
At span=141, slope=1.00: EMA `|mean ε|` = 69.05, theory predicts 70.50. ✓  
Kalman `|mean ε|` ≈ 0.086 at all slopes — the velocity state absorbs the trend's first moment regardless of slope magnitude.

---

### 2.3 The methodological demotion of centering (Rev 2)

After integrating Kalman into the real-market workbench and running it on ADANIENT:

**Observed:** Kalman `|mean ε|` = 151.3 vs EMA `|mean ε|` = 238.7 (1.6× improvement). Kalman
had 3.5× higher zero-crossing rate and shorter sign runs.

**Why this didn't survive methodological scrutiny:**

| Contamination ID | Class | Description |
|-----------------|-------|-------------|
| C1 | METHODOLOGY | Regime buckets used full-sample slope/vol quantiles — the evaluation was not causal even though the innovation was |
| C2 | METHODOLOGY | Endogenous conditioning: buckets defined by rolling slope — the exact confounder driving the centering gap |
| C3 | MEASUREMENT | `\|mean ε\|` in absolute price units — ADANIENT went from ~50 to ~3000, so the gap reflects when the trend occurred, not estimator quality |
| C4 | METHODOLOGY | 499 autocorrelated bars ≈ a few independent trend episodes on one stock in one market |
| S1 | STRUCTURAL | Matched-span controls level responsiveness but NOT detrending capability — Kalman wins centering by construction ("estimator with a drift term removes drift"), not by market discovery |
| S2 | STRUCTURAL | The velocity state could produce a spuriously centered residual by absorbing genuine reversion into drift — this was unfalsified on real data because the old KC4 test required ground truth |

**Consequence:** The "1.6×" is **unproven**, not weakly true. "Centering drives usability" is
demoted from frozen conclusion to insufficient confounded diagnostic.

---

### 2.4 The EMA lag bias — a frozen finding

This is analytic, not empirical, and is permanently established:

**EMA residual inside a linear trend of slope m and span s:**
```
mean(ε) = P − EMA ≈ m × s / 2   (grows without bound)
```

At slope 0.25, span 141 (EMA-141): the mean residual is ≈ 17.2 price units. The deviation's own
standard deviation is ≈ 2.3. **The residual is 7× dominated by the lag artifact.** Its sign matches
the true deviation only 49% of the time. This is the core reason an EMA-based reversion signal
inside a trend is unreliable.

This finding **freezes the limitation** of EMA as an equilibrium estimator. EMA is valid as fast
baseline instrumentation; it is not a trend-robust equilibrium estimator. This was previously
documented as a known limitation in the theory papers; the research here confirmed it numerically
and derived the mechanism precisely.

---

### 2.5 The MRScore self-ranking bug (structural)

**Expected:** MRScore should discriminate reverting instruments from null processes.

**What actually happened:**
- NULL_RW (pure random walk) earned the **highest** MRScore in a blind test
- ANCHOR_OU (genuine reverter) scored 55.6; NULL_RW scored 62.5

**Why:** Eq. 14 ranks each feature within the instrument's own trailing 252-bar window. A
consistently reverting OU process will have a consistently negative DRC — which means at any
given bar, its DRC is "unremarkable vs its own history" → mid percentile rank. A random walk's DRC
*wanders*, occasionally throwing high-ranking excursions. The self-ranked score rewards variance in
the feature, not the feature itself.

**The fix (not implemented in v1, documented):** cross-instrument ranking or surrogate-null-relative
raw features. MRScore's raw Block-2 values (DRC, HitRate, VR) are the actual discriminators
and discriminate in expectation. Single-path inference is unreliable (~10% false-positive on
pure RW paths drawing DRC < −2.0).

---

### 2.6 The final empirical gate result (Step 2A.5)

**The question:** in a genuine range-bound (sideways) regime where the velocity state is most
at risk of absorbing reversion, does Δβ = β_restored − β_kalman show a consistent negative sign
(absorption direction)?

**The result:**

| Window | Regime | Δβ(h=1) | Δβ(h=5) | Sign |
|--------|--------|---------|---------|------|
| W1 | Sideways / round-trip | +0.00084 | +0.00432 | anti-absorption |
| W2 | Moderate trend | −0.00231 | −0.01054 | absorption-direction |
| W3 | Parabolic trend | +0.00835 | +0.03488 | anti-absorption |
| FULL | Reference | −0.00026 | −0.00190 | trivial |

The worry regime (sideways, W1) is **anti-absorption-signed**. The only negative Δβ sits in a
trend regime where benign drift removal is the expected interpretation. Catastrophic false-centering
requires a large, consistent negative pattern — that pattern **does not exist** in this data.

Additional key observation: **R²ₒₒₛ ≈ 0 for both systems in every regime**. Neither EMA nor Kalman
residuals predict their own decay out-of-sample on real ADANIENT. There is nothing useful for the
velocity state to absorb in the first place. This is consistent with the §13 demotion of in-sample
ACF/half-life as smoother-contaminated artifacts.

**Verdict:** Classification B (mixed/unresolved, non-blocking). Catastrophic false-centering
excluded at LOW-MEDIUM confidence. Freeze the S2 uncertainty and move up the stack — but this
freeze is **provisional** and must be re-opened if any upstream component depends on μ* reversion
fidelity (e.g. State T detection conditioned on Kalman residual).

---

### 2.7 The half-life estimator bug and fix

**Problem:** the naive AR(1) half-life estimator (no intercept) was producing false positives.
EMA residuals of a random walk returned a half-life of ≈6 bars, implying mean reversion.

**Mechanism:** EMA smoothing imposes geometric weighting on the residual, inducing AR structure
by construction. This inflates |ACF(1)| to ≈0.88–0.94 on pure random walk residuals. Without an
intercept, the trend-lag mean in ε biases λ toward zero (apparent fast reversion) rather than
reflecting the process's actual mean-reversion speed.

**Fix:**
1. OLS with intercept: `Δy = λ·y[t-1] + μ + ε`. The intercept absorbs the level offset.
2. ADF significance gate: only report mean-reversion if t-stat < −2.86 (5% MacKinnon 1994).
   This blocks finite-sample bias from calling random walks mean-reverting.

The known artifact is documented in tests and warned about in the UI: *"EMA residuals of a random
walk show ACF ≈ 0.88 and half-life ≈ 6 bars — this is a smoother artifact, not evidence of
mean reversion."*

---

### 2.8 What is genuinely unresolved

These questions remain open and are NOT answered:

- Whether Kalman ε mean-reverts *better* than EMA ε out-of-sample, on real data, after controlling
  for the detrending confound (S1) and smoother-induced reversion (the surrogate-null arm)
- Whether State T exists as a distinguishable distributional phenomenon (ARM 1 test is built;
  real-data reads not yet analyzed)
- Whether MRScore is useful with a cross-instrument / surrogate-null reference (single-window
  discrimination is currently unreliable)
- Real-market behavior of any component in a genuinely mean-reverting deployment domain
  (pairs, spreads, cross-asset) — zero evidence exists from such an instrument

---

## LAYER 3 — Complete Code Structure

### 3.1 Technology Stack

**Backend (frozen)**
```
FastAPI 0.115+       HTTP API layer
Python 3.13          Runtime
DuckDB 1.1+          In-process columnar DB — single .duckdb file
Pandas 2.2+          Time-series manipulation
NumPy                Kalman filter, halflife OLS, all numerics
Statsmodels          ACF (FFT), Newey-West HAC on DRC
SciPy                (available, not yet used directly in routing)
Pydantic v2          Request/response models
pytest               Unit + integration tests
```

**Frontend (frozen)**
```
Next.js 15           App router, SSR
TypeScript           Strict mode throughout
Tailwind CSS         Styling
lightweight-charts v4  Candlestick + overlay chart (TradingView-compatible)
Zustand              Global state management
React Query          (available, API calls currently use typed fetch wrappers directly)
```

**Architecture decisions**
- Local-first, single researcher, one machine. No cloud, no microservices, no Redis, no Celery.
- DuckDB is file-backed (`data/amr.duckdb`). Single-writer — concurrent requests serialize.
  Acceptable for local research use.
- Per-request DB connections (opened/closed in `get_db()`); tests inject an in-memory connection
  via `store._conn` override.

---

### 3.2 Folder Structure

```
internship-final-reports/
├── CLAUDE.md                          # Project constitution — operating modes, frozen invariants
├── PROGRESS.md                        # v0 checklist + running status
├── SESSION_BRIEF.md                   # This file
│
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app, CORS, lifespan (DB init), health check
│   │   ├── models/
│   │   │   └── market.py              # All Pydantic request/response models
│   │   ├── routers/
│   │   │   └── market.py              # All API route handlers
│   │   └── services/
│   │       ├── analytics.py           # Core analytics: EMA, Kalman, residuals, halflife, ACF
│   │       ├── analytics_mrscore.py   # MRScore v1 engine (Block 1/2/3, causal z, DRC)
│   │       ├── analytics_state_t.py   # State T existence programme — causal window descriptors
│   │       ├── analytics_substrate.py # Substrate Observatory: DE, VR, character map
│   │       ├── loader.py              # CSV/Parquet ingestion with validation
│   │       ├── store.py               # DuckDB layer: init, store, list, query
│   │       └── synthetic.py           # 8 synthetic ground-truth processes (OU, RW, trend, etc.)
│   │
│   ├── tests/
│   │   ├── conftest.py                # In-memory DuckDB fixture; test app client
│   │   ├── test_health.py             # 1 test
│   │   ├── test_loader.py             # 7 tests: CSV/Parquet, edge cases, validation
│   │   ├── test_store.py              # 5 tests: DuckDB store/query
│   │   ├── test_market_router.py      # 8 tests: router integration
│   │   ├── test_estimator.py          # 5 tests: EMA unit + temporal integrity
│   │   ├── test_analytics_validation.py # 12 tests: synthetic ground-truth validation suite
│   │   ├── test_kalman_validation.py  # Kalman synthetic tests (measurement lock, not verdict)
│   │   ├── test_mrscore.py            # MRScore engine correctness + causal firewall
│   │   ├── test_substrate.py          # Substrate Observatory engine correctness
│   │   ├── test_synthetic_nulls.py    # Synthetic null battery (OU/RW/trend/drift)
│   │   ├── test_state_t_existence.py  # State T ARM 1 causal machinery tests
│   │   ├── test_state_t_falsification.py # State T ARM 1 pre-registration falsification tests
│   │   └── test_velocity_absorption.py   # δ-decomposition + walk-forward decay: identity + firewall
│   │
│   └── scripts/
│       ├── audit_kalman.py            # 4-experiment replication audit (G-ABSORB falsification)
│       ├── calibrate_kalman.py        # SNR sweep on synthetic OU → finds H2-admissible band
│       ├── confirm_kalman.py          # 360-condition pre-registered confirmatory experiment
│       ├── eval_kalman_real.py        # Step 1: real-market pass (ADANIENT, regime buckets)
│       ├── generate_habitat.py        # Substrate Observatory: generate synthetic habitat sets
│       ├── generate_nulls.py          # MRScore Observatory: generate synthetic null packet
│       ├── probe_h1.py                # H1 gate probe (KC1 falsification)
│       ├── state_t_cohort_probe.py    # State T: cohort-level descriptor probes
│       └── state_t_existence_probe.py # State T: existence programme real-data probe runner
│
├── frontend/
│   └── src/
│       ├── app/
│       │   ├── page.tsx               # Workstation (/ route)
│       │   └── workbench/
│       │       └── page.tsx           # Workbench (/workbench route)
│       ├── components/
│       │   ├── AppNav.tsx             # Top navigation between pages
│       │   ├── workspace/             # Workstation components
│       │   │   ├── ChartWorkspace.tsx # lightweight-charts candlestick + EMA overlay
│       │   │   ├── EstimatorPanel.tsx # Toggle + window control for μ* overlay
│       │   │   ├── InstrumentPanel.tsx # File load + instrument selector
│       │   │   ├── IntervalBar.tsx    # Preset date range buttons + raw date inputs
│       │   │   └── ResearchSurface.tsx # Research data table below chart
│       │   └── workbench/             # Workbench components
│       │       ├── ContextBar.tsx     # Shows active instrument + date range
│       │       ├── ModuleNav.tsx      # Left-side module switcher
│       │       ├── ResearchControls.tsx # Right-side controls per module
│       │       ├── TimelineRail.tsx   # Bottom timeline for replay
│       │       ├── registry.ts        # Module manifest (id → component)
│       │       ├── types.ts           # Workbench TypeScript types
│       │       └── modules/
│       │           ├── EstimatorInspector.tsx # Price + causal + adj μ* + stats
│       │           ├── ResidualObservatory.tsx # ε time series + histogram + ACF bars
│       │           ├── AssumptionValidator.tsx # 4 TestStrip PASS/FAIL sparklines
│       │           ├── CausalDiff.tsx  # Δε and Δμ* time series + scatter vs forward returns
│       │           ├── EventLog.tsx    # Auto-detected events + manual annotations
│       │           ├── EstimatorCompare.tsx # Kalman vs EMA comparison (Step 1 workbench)
│       │           ├── VelocityAbsorption.tsx # δ-decomposition + walk-forward decay (ABS)
│       │           ├── LagIllusion.tsx # EMA lag artifact visualization
│       │           ├── MRScore.tsx     # MRScore panel (MRS module)
│       │           ├── Replay.tsx      # Historical replay module
│       │           ├── SubstrateCharacter.tsx # Substrate Observatory panel (SUB module)
│       │           └── (... more)
│       └── lib/
│           ├── api.ts                 # Typed fetch wrappers for all endpoints
│           ├── store.ts               # Zustand store (instruments, dateRange, estimator state)
│           ├── types.ts               # Shared TypeScript types
│           └── smoothers.ts           # Client-side EMA/smoothing utilities
│
├── data/
│   ├── raw/
│   │   └── nifty_synthetic.csv        # 500-bar synthetic OHLCV for smoke testing
│   └── amr.duckdb                     # Persistent DuckDB (created on first server start)
│
└── docs/
    └── research/
        ├── 01_amr_framework.md        # Full AMR specification (OU model, MRScore, blocks)
        ├── 02_mu_star_equilibrium.md  # Anchored Kalman paper V2.5
        ├── 03_state_t_report.md       # State T: definition, mechanics, A→T→B model
        ├── 04_state_t_conditional_relevance.md  # State T: conditions, deferred scope
        ├── 05_kalman_v1_results_memo.md # SUPERSEDED — the overturned KC4/KC1 rejection (preserved)
        ├── 06_kalman_equilibrium_research_update.md # Active living record (supersedes 05)
        ├── 07_lag_illusion.md         # EMA lag bias documentation
        ├── 08_synthetic_null_testing.md # Synthetic null battery documentation
        ├── 09_mrscore_observatory.md  # MRScore build record + self-ranking finding
        ├── 10_substrate_observatory.md # Substrate Observatory build record
        ├── 11_state_t_existence.md    # State T existence pre-registration
        ├── implementation_plan.md     # Build notes
        └── software_architecture_v1.md # Architecture decisions (ADRs)
```

---

### 3.3 Backend — Key Code Deep-Dives

#### `analytics.py` — the core computation layer

The most important file in the system. All analytics flow through here.

**Causal vs full-information EMA:**
```python
def compute_ema(closes: pd.Series, span: int) -> pd.Series:
    # adjust=False: EMA at bar t uses only prices[0..t]
    # equivalent to: α = 2/(span+1), μ_t = α·P_t + (1-α)·μ_{t-1}
    return closes.ewm(span=span, adjust=False).mean()

def compute_full_ema(closes: pd.Series, span: int) -> pd.Series:
    # adjust=True: each bar is re-weighted using all observations
    # Differs from causal only during warmup (first ~3×span bars)
    # After warmup, both converge — the "full-info" label is somewhat misleading
    return closes.ewm(span=span, adjust=True).mean()
```

**Half-life estimator (with the intercept fix):**
```python
def compute_halflife(residuals: pd.Series) -> float | None:
    # OU test: Δy = λ·y[t-1] + μ + ε  (intercept REQUIRED — absorbs EMA lag mean)
    # λ < 0 → mean-reverting; half-life = -ln(2)/λ
    # Guards:
    #   - minimum 10 bars
    #   - ADF t-stat < -2.86 (5% MacKinnon 1994) to reject unit root null
    #   - returns None if not mean-reverting or not statistically significant
    ...
    X = np.column_stack([y_lagged, np.ones(n)])  # [y_lagged | 1]
    coeffs, _, _, _ = np.linalg.lstsq(X, delta_y, rcond=None)
    lam = float(coeffs[0])
    ...
    t_stat = lam / np.sqrt(var_lam)
    if t_stat > -2.86:
        return None  # not significant — treat as non-mean-reverting
    return float(-np.log(2) / lam)
```

**Kalman filter (2-state local-linear-trend, frozen spec):**
```python
# State:      x_t = [μ_t, v_t]ᵀ   (level, velocity)
# Transition: F = [[1,1],[0,1]], Q = diag(q_μ, q_v), q_μ = κ·q_v
# Observation: P_t = μ_t + noise,  H = [1, 0],  R = R_p
# Research residual = INNOVATION (pre-update): P_t − μ_{t|t−1}
#   NOT the filtered residual — that would be circular

KALMAN_SNR   = 1e-8    # FROZEN: SNR = q_v / R_p
KALMAN_KAPPA = 0.05    # FROZEN: controls q_μ release vs I(2) ringing

for t in range(n):
    x_pred = F @ x
    P_pred = F @ P @ F.T + Q
    y = prices[t] - x_pred[0]          # innovation (research residual)
    S = P_pred[0, 0] + R_p
    K = (P_pred @ H) / S
    x = x_pred + K * y                 # posterior update
    P = (I2 - np.outer(K, H)) @ P_pred
```

**Velocity absorption instrumentation (Step 2A):**
The δ-decomposition recovers the matched-span EMA prediction from the frozen Kalman output
algebraically — no filter recomputation:

```python
# δ_t = μ^K_{t|t−1} − μ^{EMA,pred}_t
# Key identity: μ^K_{t|t−1} = close_t − ε^K_t  (recovered by subtraction)
# Restoration: ε^R = ε^K + δ = close − μ^{EMA,pred}  (velocity-OFF counterfactual)
# Walk-forward decay: chronological 50/50 split,
#   OLS Δε_{t→t+h} = α + β·ε_t on first half, R²ₒₒₛ on second half
#   β < 0 ⇒ residual predicts its own decay OOS
```

#### `analytics_mrscore.py` — MRScore observatory

```python
# MRScore_t = 0.20·B1 + 0.60·B2 + 0.20·B3  (eq. 13)
# B1 (mean reliability): ADF/KPSS, Mean Stability Index, Variance Stability Index
# B2 (MR strength): DRC (Newey-West HAC), HitRate, Multi-Scale Variance Ratio
# B3 (tradability): HL-proximity score, Volatility Compression, TCF

def causal_zscore(residual: pd.Series, window: int = 60) -> pd.Series:
    # Uses shifted trailing μ,σ — NOT the contemporaneous bar
    # Prevents the current bar from contaminating the standardizer
    mu = residual.rolling(window=window, min_periods=2).mean().shift(1)
    sd = residual.rolling(window=window, min_periods=2).std().shift(1)
    return (residual - mu) / sd
```

#### `store.py` — DuckDB layer

Two tables: `instruments` (metadata) and `ohlcv` (OHLCV bars). Per-request connections.
Tests inject an in-memory DuckDB via `store._conn = duckdb.connect(":memory:")`.

```python
def init_db(path: str = "data/amr.duckdb"):
    conn = duckdb.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS instruments (
            instrument_id TEXT PRIMARY KEY,
            display_name  TEXT,
            file_path     TEXT,
            loaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ohlcv (
            instrument_id TEXT,
            date DATE, open REAL, high REAL, low REAL, close REAL, volume REAL,
            PRIMARY KEY (instrument_id, date)
        )""")
    conn.close()
```

#### `loader.py` — CSV/Parquet ingestion

Handles column alias resolution (accepts many common date/OHLCV column naming conventions),
volume normalization, timezone stripping, duplicate rejection, and forwards-only date validation.
Returns a clean DataFrame with a DatetimeIndex ready for `store.store_instrument`.

---

### 3.4 API Endpoints

All endpoints are in `backend/app/routers/market.py` under `/api/v1/market/`.

| Method | Path | What it returns |
|--------|------|-----------------|
| GET | `/health` | `{"status": "ok"}` |
| POST | `/api/v1/market/load` | Load CSV/Parquet → DuckDB. Returns row count, date range, columns. |
| GET | `/api/v1/market/instruments` | List all loaded instruments (id, display_name, file_path, dates). |
| GET | `/api/v1/market/{id}/ohlcv` | OHLCV bars with optional `start`/`end` date filtering. |
| GET | `/api/v1/market/{id}/estimator` | Causal EMA μ* values only. `span` query param. |
| GET | `/api/v1/market/{id}/research` | `close + μ* + ε` with summary stats (mean, std, skew, kurt, ACF). |
| GET | `/api/v1/market/{id}/diagnostics` | **The core research endpoint.** Full dual-mode payload (see below). |
| GET | `/api/v1/market/{id}/velocity-absorption` | δ-decomposition + walk-forward decay table. |
| GET | `/api/v1/market/{id}/mrscore` | MRScore per-bar series + block scores + stats. |
| GET | `/api/v1/market/{id}/substrate` | Substrate character per-bar series (DE, VR, bucket). |
| GET | `/api/v1/market/{id}/state-t-existence` | State T ARM 1: descriptor distributions across θ thresholds. |

**The `/diagnostics` payload per bar:**
```
close, mu_star (causal EMA), mu_star_adj (full-info EMA), mu_star_diff (Δ initialization gap)
epsilon (causal residual), epsilon_adj, epsilon_rolling_mean, epsilon_rolling_std, epsilon_zscore
innovation (close[t] − μ*[t−1])
mu_star_kalman, epsilon_kalman, kalman_velocity, kalman_gain, kalman_state_var
```

**Temporal integrity:** the `end` query parameter is a hard firewall on every endpoint — it
restricts both the data slice and every rolling computation to `date ≤ end`. Spike contamination
test verifies this invariant (a future price spike cannot change μ* at any earlier date).

---

### 3.5 Frontend — Pages and Components

**Two pages:**

#### Workstation (`/`) — Data Load + Chart Surface

Primary market inspection surface. Layout: InstrumentPanel (left) | ChartWorkspace + ResearchSurface (center, 60/40 vertical split) | EstimatorPanel (right).

| Component | File | What it does |
|-----------|------|--------------|
| `InstrumentPanel` | `workspace/InstrumentPanel.tsx` | File path + ID input; POSTs to `/load`; lists instruments; click to select |
| `IntervalBar` | `workspace/IntervalBar.tsx` | Preset buttons (1M/3M/6M/1Y/2Y/ALL) and raw date inputs; writes to Zustand `dateRange` |
| `ChartWorkspace` | `workspace/ChartWorkspace.tsx` | `lightweight-charts` candlestick chart. Fetches OHLCV on instrument select. Adds EMA overlay series from `/estimator` when estimator toggle is on. Resize-aware. |
| `EstimatorPanel` | `workspace/EstimatorPanel.tsx` | Toggle EMA overlay on/off; window size control; dimmed placeholders for Kalman + Rolling Mean + VWAP (not yet wired) |
| `ResearchSurface` | `workspace/ResearchSurface.tsx` | Tabular view of research data below the chart |

#### Workbench (`/workbench`) — Research Modules

Research + falsification surface. Consumes `/diagnostics`. No instrument re-loading needed — shares Zustand store. Layout: ContextBar (top) | ModuleNav (left) + active module (center) + ResearchControls (right) | TimelineRail (bottom).

| Module | ID in store | What it shows |
|--------|-------------|---------------|
| **EstimatorInspector** | `estimator-inspector` | Price + causal μ* + adjusted μ* overlaid; Δ initialization gap sub-chart; stats sidebar (n, ACF at 1/5/10/20, half-life, ε stats, Δμ* mean/max) |
| **ResidualObservatory** | `residual-observatory` | ε time series + ±1σ rolling bands; ε histogram with normal overlay (bins colored red/green, blue Gaussian curve); ACF bar chart; stats panel |
| **AssumptionValidator** | `assumption-validator` | Four TestStrip sparklines: `\|ε z-score\| > 2σ`, rolling `σ(ε)`, `\|ε\| > 2σ`, innovation `\|close[t]-μ*[t-1]\|`. Each strip shows PASS/FAIL. Interpretation panel summarizes active violations. |
| **CausalDiff** | `causal-diff` | Time series of Δε and Δμ* (EMA initialization gap); scatter: Δμ* vs +5-bar forward returns with Pearson r; gap statistics |
| **EventLog** | `event-log` | Auto-detected events: ε spikes (2σ/3σ), zero crossings, causal divergence spikes. Manual annotation input with date tagging. Click row → jumps to that date in TimelineRail. |
| **EstimatorCompare** | `estimator-compare` | Kalman vs EMA side-by-side on price chart + residual sub-chart (Step 1 workbench) |
| **VelocityAbsorption** | `velocity-absorption` | ABS module — 3 surfaces: decay table (β, R²ₒₒₛ per system per horizon), δ-vs-price plot, raw Δβ (no verdict engine — deliberate) |
| **MRScore** | `mrscore` | MRScore per-bar series + block decomposition + observatory warning banner |
| **SubstrateCharacter** | `substrate` | DE + VR per-bar + dominant character bucket bar chart |

---

### 3.6 State Management (`lib/store.ts`)

Zustand store shared across both pages:

```typescript
interface WorkstationState {
  instruments: InstrumentMeta[];
  selectedInstrumentId: string | null;
  dateRange: { start: string | null; end: string | null };
  estimatorEnabled: boolean;
  estimatorWindow: number;               // EMA span
  estimatorMode: 'causal' | 'full_info';
  activeWorkbenchModule: string;
}
```

`dateRange.end` is the temporal firewall — every API call passes it to every endpoint.

---

### 3.7 Test Architecture (57 tests passing)

```
test_health.py               — 1  health check
test_loader.py               — 7  CSV/Parquet loading, edge cases, invalid files
test_store.py                — 5  DuckDB init, store, list, query, duplicate handling
test_market_router.py        — 8  router integration: all endpoints, 404, 422
test_estimator.py            — 5  EMA unit, temporal integrity (future spike)
test_analytics_validation.py — 12 synthetic ground truth:
    TestHalflifeRecovery      — OU with known λ; intercept fix; trend contamination
    TestRandomWalkSanity      — RW not classified as MR; EMA artifact documented
    TestTrendProcess          — EMA lag on trend; innovation scales with trend speed
    TestReplayBoundary        — end-date firewall; bar-by-bar stepping; future spike
    TestACFGroundTruth        — AR(1) rho=0.6 recovery; white noise near-zero
test_kalman_validation.py    — Synthetic measurement locks (not a verdict — see doc 06 §12)
test_mrscore.py              — MRScore correctness + causal firewall (bit-identical injection)
test_substrate.py            — Substrate Observatory engine + firewall + habitat discrimination
test_synthetic_nulls.py      — Synthetic null battery (OU/RW/trend/drift)
test_state_t_existence.py    — State T ARM 1: causal partitioning + descriptor extraction
test_state_t_falsification.py — State T pre-registration falsification gates
test_velocity_absorption.py  — δ-decomposition identity + matched-span derivation + causal firewall
```

---

### 3.8 Running the System

```bash
# Backend
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm run dev
# http://localhost:3000

# Tests
cd backend && source .venv/bin/activate && python -m pytest -v

# Key research scripts
python scripts/confirm_kalman.py   # → /tmp/confirm.txt (360-condition experiment)
python scripts/audit_kalman.py     # → /tmp/audit_exp*.txt (G-ABSORB falsification)
python scripts/calibrate_kalman.py # → /tmp/cal_table.txt (SNR sweep)
```

---

## Where We Are and What's Next

**Completed and stable:**
- Full v0 scope (all 13 items from CLAUDE.md §10)
- EMA μ* with dual-mode and temporal firewall
- Kalman μ* with 360-condition confirmatory experiment and Step 2A instrumentation
- Diagnostics workbench (all 5 original modules + EstimatorCompare + VelocityAbsorption)
- MRScore observatory v1 (all blocks, causal firewall, adversarial review)
- Substrate Observatory v1 (DE, VR, character map)
- State T existence programme v1 (pre-registration, ARM 1 code, causal partitioning)

**Active frontier — UPDATED 2026-06-03:**
- State T existence programme: **CLOSED — FALSIFIED-IN-FORM / KILLED** (doc 11 Phase 5, 2026-06-02).
  Across 12 instruments / 5+ habitats, high-|z| windows show directional continuation, not stabilization.
- Post-kill institutional review + ranked surviving arms: `docs/research/12_institutional_review_post_state_t.md`
- Immediate next action: **Arm 0 — data provenance & quality audit** (doc 12 §7). **[DONE 2026-06-03]**
- **CYCLE 2026-06-03b:** Arm 0 complete (old cohort → 0 trustworthy; deep cohort arrived → `data/mr_cohort_manifest.md`: 46 TRUSTED legs, 7 constructible causal spreads). Waiting-period package promoted (docs 13–17); `ADR_003` roll-law filled; **Arm A pre-registered (doc 18)**.
- **CYCLE 2026-06-03c — ARM A EXECUTED → INCONCLUSIVE (construction-defective).** Built engine (`backend/app/services/analytics_arm_a.py`, 9 causal/ground-truth tests green), froze execution params (`doc 18a`), ran all 7 spreads from raw legs. Full record: **`docs/research/19_arm_a_habitat_results.md`**. Verdict: **0/7 admissible confirms; the decisive question was never validly tested.** The frozen W=60 rolling-OLS-β-on-levels **manufactures super-diffusion** via a β-update-noise term (82–97% of ΔS variance; proven on synthetic ground truth) → the "both DECISIVE fail → premise damaged" kill fired on *contaminated* evidence and is **invalid (decisive pairs UNRESOLVED, not negative)**. USD/INR "confirm" = stale-quote artifact (76% flat → UNUSABLE); WTI–Brent beats RW but **fails the vol-clustering GARCH null** (p=0.094) → sub-diffusion is largely vol clustering. Premise **neither confirmed nor validly damaged.** Load-bearing finding (methodological): **a causal time-varying hedge ratio manufactures VR structure — doc-13 HR-4 / doc-07 lag illusion now DEMONSTRATED at the β level.** **Current next action: re-pre-register Arm A's CONSTRUCTION** (rolling-cointegration β on a long window with the β-update term controlled, or leg/log-spread VR) — a NEW pre-registration, then re-run the decisive instruments. Bottleneck moved from data → construction.
- **CYCLE 2026-06-03d — PROGRAMME DOCTRINE v2 adopted (`CLAUDE.md §11`).** Governance revamp (not a reset): rolling-local ontology (WHEN not WHETHER MR exists); trader lens as a *prioritization* constraint (deployable object = a cost-aware BOOK, not an instrument); pipeline gains **empirical probation** + **conditional survival** before freeze/kill; **Hypothesis Registry** (`docs/research/HYPOTHESIS_REGISTRY.md`); **Residual Ecology** observational arm (fenced from killed State T); mandatory multi-lens (research+statistical+trader+adversarial) subagent decomposition for major empirical conclusions; data-phase transition (bottleneck is now prioritization/evidence-generation, not data); and a new standing gate — a **real-data positive control** before any further kill is credible. Rigor core (§1–§10) preserved beneath §11.

**Not yet built (frozen deferrals):**
- Cross-instrument panel (binds the Kalman μ* revisit trigger)
- Surrogate-null bands for MRScore raw DRC (the §13-style arm)
- Full-information MRScore mode (genuine future-using μ* required — deferred)
- State T detection (not before existence is confirmed)
- Anything in Phase 3–5 (structure classification, signal generation, execution)

**The honest single next action (UPDATED 2026-06-03c — Arm A executed; verdict INCONCLUSIVE / construction-defective):**
> **Re-pre-register Arm A's spread CONSTRUCTION**, then re-run the decisive instruments. The frozen W=60
> rolling-OLS-β-on-levels was *proven* to manufacture super-diffusion (β-update-noise = 82–97% of ΔS variance;
> `docs/research/19_arm_a_habitat_results.md` §2/§5), so it is inadmissible for VR habitat tests on trending legs.
> Candidates to adjudicate-then-freeze *before* results: (a) causal rolling-cointegration (Engle–Granger) β on a
> long window with the β-update term explicitly controlled; (b) VR on the positive legs (NP-2) / a causal
> log-spread for strictly-positive pairs; (c) acquire synchronized sub-bar leg data. Do **NOT** silently re-run
> with a longer window and call it the verdict (freeze discipline — that is the post-hoc adaptation forbidden by
> doc 18 §7 / CLAUDE.md §6); it must be a NEW pre-registration. The engine, surrogate machinery, and decision rule
> (doc 18a, ratified) are reusable as-is.
>
> *(Superseded action: "EXECUTE Arm A (doc 18)" — DONE 2026-06-03c, doc 19. Earlier-superseded: Arm 0 audit (done,
> `data/mr_cohort_manifest.md`); State-T existence probe (done; killed, doc 11).)*
