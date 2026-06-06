# AMR Project State — 2026-06-05

**Purpose.** A dense, specific state record for a researcher returning cold. Covers: what the
project is, how we got here, what the critical code does, what Kalman and MR Habitat research
produced, what is killed/frozen/active, and what the next moves are.

---

## 0. One-line identity

The **Adaptive Mean Reversion (AMR) Research System** is a temporally honest, falsification-first
engine for detecting and eventually trading mean reversion inside structurally trendy commodity
spread markets. The operative question is **WHEN/WHERE MR exists**, not whether it exists
universally. The deployment target is a live commodity calendar spread book (~3–5 instruments,
2–6 week holds, conditioned on inventory regimes). The current phase is **evidence accumulation
toward one deployable, cost-clearing spread**.

---

## 1. What we are trying to accomplish (current horizon)

The programme entered a constitutional inflection on 2026-06-04 (doc 32, "trader-first redesign").
The new objective hierarchy:

| Tier | Goal |
|------|------|
| **Tier 1** (the only thing that matters) | Deploy ONE cost-clearing MR book in a liquid commodity spread. Net positive after all-in costs, 12-week forward hold-out. |
| **Tier 2** (serves Tier 1) | Quant falsification. Veto power over ideas that would waste capital. NOT an end in itself. |
| **Tier 3** (earns its keep or gets cut) | Mechanism understanding. Authorized only when it answers a specific Tier 1 question. |

**The binding bottleneck** (as of 2026-06-04) is no longer data or infrastructure. It is:
admissible cohort breadth. The admissible clean-construction daily β=1 MR universe is essentially
**NG alone** right now. Portfolio construction requires ≥2 independent instruments with positive
expectancy. The sole gate that opens the portfolio domain is **Cycle-2 controlled-β cohort
expansion** (BRN M1-M2 daily + crack spread positive control).

---

## 2. Research arc — what happened and what it proved

### Phase 1: Workstation infrastructure (2026-06-01)
Built the core observatory workstation: FastAPI backend + Next.js frontend. Kalman μ* research
began. MRScore, Substrate Observatory, historical Replay module, causal firewall established.
ADANIENT loaded as placeholder substrate (trend-heavy; **not deployment evidence**).

### Phase 2: Kalman μ* arc (2026-06-01, doc 05 → 06)
*Goal:* decide whether the 2-state Kalman filter is a better equilibrium estimator than EMA for
mean reversion inside trends.

**First rejection (doc 05) — later overturned.** Kalman was initially rejected on KC4 ("velocity
absorbs alpha," measured by G-ABSORB = `|corr(velocity, deviation)|`) and KC1 ("no artifact
reduction"). These rejection grounds were later proved invalid in a replication audit:
- G-ABSORB is **trend-invariant and κ-invariant** — it reads 0.288 regardless of whether slope is
  0 or 2.0. It doesn't measure the thing it claims to gate.
- KC1's H1 threshold is unsatisfiable by any causal smoother, including EMA itself.

**Confirmatory test (doc 06 §7) — what actually matters.** A pre-registered 360-condition paired
experiment (30 seeds × 4 slopes × 3 OU strengths) on matched-effective-span EMA vs Kalman found:
- ACF, half-life, and signal preservation (corr(ε, deviation) ≈ 0.92) are **statistically
  indistinguishable** between the two estimators at matched span.
- **Residual centering** differs by two orders of magnitude: Kalman `|mean ε| ≈ 0.085` vs EMA
  `|mean ε| ≈ 12.19` at slope 0.25. EMA's lag bias = `slope × span/2`, confirmed analytically.
- Sign-agreement with true deviation: **Kalman 0.854 vs EMA 0.492** — EMA is a coin flip inside a
  trend. Kalman's velocity state removes the trend's first moment from the residual.

**Real-market reassessment (doc 06 §12) — demotion.** After integrating Kalman into real ADANIENT
data, a methodological critique found:
- The centering advantage on real data is **confounded (S1)**: the Kalman has a drift term; any
  integrated drift model removes drift tautologically. The win vs EMA is not necessarily evidence
  of better equilibrium *discovery*.
- The "no false-centering" claim from synthetic tests **cannot be evaluated on real markets**
  (requires ground truth). S2 (false-centering) was re-opened.
- The Step 1 "1.6×" real-market result survives neither the S1 control nor the contamination
  audit (C1–C6).

**Final status (doc 06 §15) — PROVISIONAL FREEZE, non-blocking.** The δ-decomposition + walk-
forward decay test (Step 2A.5) ran on pre-declared regime windows of ADANIENT. Δβ sign **flipped
across regimes** (sideways = anti-absorption, moderate trend = mild absorption-signed, parabolic
= anti-absorption). R²ₒₒₛ ≈ 0 for both estimators in every regime. Verdict: **B (unresolved,
non-blocking); catastrophic false-centering (C) excluded.** EMA remains production μ*. Kalman
remains a research-only comparison estimator. The provisional freeze stands unless an upstream
component needs to **depend on μ* reversion fidelity** — that triggers a mandatory cross-instrument
panel before proceeding.

### Phase 3: State T existence (doc 11) — KILLED
The State T hypothesis (that a pre-reversion stabilization morphology — rising κ, falling AR(1),
declining variance — precedes reversions) was tested across 12 instruments via a Phase 5 empirical
sweep. **62/62 cross-habitat comparisons reject.** High-|z| windows showed directional continuation,
not stabilization. The selection-on-deviation null reproduces every apparent "T-shape." Verdict:
**FALSIFIED-IN-FORM / KILLED.** The zombie prohibition applies: no silent resurrection without a
new independent pre-registration + the §4 zombie-reopen test. All State T detection/timing work
is **permanently frozen**.

### Phase 4: Arm A v1 habitat discovery (doc 18/18a/19, 2026-06-03) — INCONCLUSIVE
*Goal:* test whether the deployment-domain spread cohort (7 spreads built from 46 TRUSTED legs)
exhibits MR habitat using VR(q) surrogate-relative tests.

**Finding: the construction was defective.** The pre-registered W=60 rolling-OLS-β-on-levels
construction **manufactures super-diffusion**. The increment decomposes as:

```
ΔS_t = (ΔA_t − β_{t-1}·ΔB_t)  −  (β_{t-1} − β_{t-2})·B_{t-1}
                                     └─── β-update-noise × price level ───┘
```

The second term (β wobble × trending price level) accounts for **82–97% of Var(ΔS)** on trending
legs. Proven on synthetic ground truth: a true OU spread (true VR < 1) has VR fabricated to 6.23
by rolling-β W=60, and VR recovers to < 1 when β-update noise is ablated. **Rolling-OLS-β-on-
levels is INADMISSIBLE for VR tests on trending legs.** This is a permanent, frozen finding.

All 7 spreads INCONCLUSIVE (not negative): 5 were construction-invalid, 1 was a stale-quote
artifact (USD/INR, 75.6% flat bars), 1 (WTI-Brent) failed the GARCH null (vol clustering, not MR).

### Phase 5: Arm A v2 — Cycle 1 positive control (doc 20/21, 2026-06-04) — CONDITIONAL SURVIVAL
*Goal:* fix the construction and pass the §11.8 standing gate: can the apparatus confirm a known,
literature-documented, economically-anchored real edge?

**Fix: restrict to β=1 DEFINITIONAL calendar spreads** — zero rolling-β DOF → structurally immune
to the v1 β-update artifact. These are single-leg continuous calendar series (e.g. ng12, the
front NG calendar).

**New null added: MA(1)-microstructure-noise null.** A latent RW + i.i.d. observation noise produces
ΔS = ε_t + (η_t − η_{t-1}), an MA(1) with the real series' negative incr ACF(1). This is zero
mean-reverting but reproduces bid-ask bounce. Beating this null means sub-diffusion is MORE than
bounce (genuine MR). This was the decisive gate — a pure RW+bounce series is **killed by MA(1)**
but not by RW or GARCH alone, confirming the apparatus discriminates genuine MR from noise.

**NG front calendar result (CONFIRMS):**
- VR(20) = 0.448
- Beats RW: p = 0.005
- Beats GARCH: p = 0.025  
- Beats MA(1)-noise: **p = 0.005** (the decisive control)
- Survives causal deseasonalization (→ VR 0.249)
- Open/close consistent
- RB calendar correctly NULLs at q≤20 (selectivity check passes)

**Self-built Brent calendar (BRN1!−BRN2!, 60min, no vendor back-adjustment)** confirms at all
horizons — corroborates NG, weakens the vendor-artifact hypothesis for the apparatus.

**Why CONDITIONAL (not full):** ng12 is an opaque vendor "continuous calendar" series; the
back-adjustment is unaudited. NG's MA(1) confirm sits at q=10/20 where back-adjustment compression
would also live. Confidence MEDIUM-HIGH (apparatus power/selectivity) / MEDIUM (NG clean vs
vendor artifact). §11.8 gate **passed conditionally** — future kills become more credible.

### Phase 6: Arm A v2 — Cycle 1b rolling-local (doc 22/23, 2026-06-04) — PERSISTENT-BUT-UNECONOMIC
*Goal:* test whether NG calendar MR persists across time in a trader-relevant rolling-local frame.

**Key construction correction (pre-freeze):** per-window binary VR flag is underpowered at trader
window lengths (~0.55 power on real OU; fires higher on bounce than on genuine MR). Replaced with
**pooled mean-z**: per-window standardized VR(20) below its own RW band, pooled across years.

**Result:**
- NG yearly pooled mean-z = **−0.627** (t = −4.37, p ≈ 2e-4)
- 14/19 years below RW-median; survives post-2020 (mean-z = −0.438)
- Half-life ~13 bars (tradeable)
- MR **switches off in 5 storage-GLUT years** (2009, 2012, 2017, 2020, 2025; VR→1, half-life→27)
  — NOT in price shocks. This regime-conditionality is the strongest evidence for genuine storage
  MR rather than a uniform vendor splice artifact.

**But UNECONOMIC:** naive causal z-entry book is **break-even before cost** (gross +0.0004/trade
vs 0.003 round-trip). Net-negative. Half-life is tradeable; persistence is real. **Truth ≠
usefulness.**

**Caveat:** NG −0.627 ≈ the quarter-strength splice anchor −0.657 (p = 0.84). The regime-
conditionality is the main evidence it's not pure vendor artifact, but the back-adjustment is not
cleanly excluded.

### Phase 7: Predictive transition object (doc 24, 2026-06-04) — FORBIDDEN
*Goal:* adjudicate whether a "trend→MR transition probability / precursor" object is admissible.

**Verdict: §4-FORBIDDEN as State-T resurrection.** Fails the zombie-reopen test on 3 of 4 clauses.
The decisive, durable reason is an **object-class error, not a statistical one**: a transition is
*defined by the regime that FOLLOWS* the candidate instant. No causally-definable transition label
exists. Every statistical costume (Markov-switching, CUSUM-as-transition, run-length-VR, TAR/SETAR)
inherits this error. Every "causal escape" collapses into future-label / forward-read / rolling-
manufacture / selection-on-deviation. **Closed** unless signed order flow / OFI / OI-COT on a
flow-driven instrument is acquired — that is the only path that reopens a predictive transition
object.

What **survives** from this work: a strictly observational, unconditional, fixed-grid VR(q)
characterization that folds into the existing MR-Habitat object (not a new module).

### Phase 8: Portfolio economics (doc 25, 2026-06-04) — ROUTE GATED
*Goal:* can gating/selectivity/diversification/netting/turnover convert statistically-real-but-weak
NG MR into cost-clearing alpha?

**Durable principle 1 — expectancy arithmetic:** `E[Σwᵢ(gᵢ−cᵢ)] = Σwᵢ·E[gᵢ−cᵢ]`. This is
correlation-free. A diversified book of sub-cost sleeves is **still sub-cost.** Only selectivity
(↑gross) and netting (↓cost via shared legs) move the expectancy/cost ledger. All other levers
(diversification, conditional-participation, habitat-gating, turnover reduction) are variance/Sharpe
movers — they cannot rescue negative expectancy.

**Durable principle 2 — selectivity KILLED (doc 30/31):** pre-registered adversarial test (N=500,
θ∈{1.0,1.5,2.0,2.5}, RW+GARCH+OU+Splice surrogates, episode-jackknife, OOS split). Primary θ=1.0:
gross = −0.0006, p_rw = 0.551. θ=2.0: gross +0.0068 but p_rw = 0.417 (46th percentile of RW
distribution); p_ou = 1.000 everywhere (a constant-MR OU with NG's own half-life beats NG at every
threshold — the regime-conditionality kills unconditional z-entry). Jackknife collapse >500% at
θ=2.5. Verdict: **A_FALSE_RESCUE.** The only path to selective deployment requires a causal regime/
inventory classifier = State-T-adjacent = FORBIDDEN (doc 24). **Selectivity is CLOSED as a
standalone direction on NG.**

**Durable principle 3 — cohort is n≈1:** the admissible clean-construction daily β=1 MR universe
is NG alone. Cannot diversify or net a portfolio of one. The portfolio question is not empirically
posable today.

### Phase 9: EIA conditional entry (doc 33/34, 2026-06-04) — KILLED
Pre-registered: condition NG calendar z-entry on EIA storage anomaly <10% above seasonal average.
Speed gate N=200: **p_rw = 0.502** (50th percentile of RW null). Conditional gross +0.0056 ≈ RW null
median +0.0057. Selection-on-regime artifact: EIA conditioning improves gross equally in zero-MR
surrogates. Verdict: **KILL_PVAL.** Data limitation: EIA DNAV only available from 2010; effective
test = 2015–2026; glut years 2009/2012 excluded. OOS directionally positive (n=49, net +0.0048)
but non-binding.

---

## 3. Code — what governs the majority of the codebase

### `backend/app/services/analytics.py` — Core equilibrium engine
The single most important file. Contains:

**`compute_ema` / `compute_full_ema`** — causal (adjust=False) and reference EMA. Production μ*.

**`compute_kalman_mu_star`** (lines ~167–238) — the frozen 2-state Kalman filter.
```
State: x_t = [μ_t, v_t]ᵀ
F = [[1,1],[0,1]],  Q = diag(κ·q_v, q_v),  κ = 0.05 (FROZEN)
H = [1, 0],  R_p = (1.4826 · MAD(ΔP over warmup))² (one-time unit normalization, not a fit)
SNR = q_v / R_p = 1e-8 (FROZEN)
```
Returns: `mu_star_kalman` (posterior, for charting), `epsilon_kalman` (one-step-ahead
**innovation** P_t − μ_{t|t-1} — the research residual; all stats use this, never the filtered
residual which is circular), `kalman_velocity`, `kalman_gain`, `kalman_state_var`.

The innovation residual is fundamental: using the pre-update prediction error means the residual
is causally honest — the filter hasn't seen P_t yet at the moment the residual is recorded.

**`compute_velocity_absorption`** — the δ-decomposition for S2 false-centering tests (doc 06 §14).
Recovers μ^K_{t|t−1} = close_t − ε^K_t by subtraction (no filter recompute), builds the
"velocity-OFF" counterfactual (ε^R = ε^K + δ), runs OOS walk-forward β on both systems.

**`compute_halflife`** — OLS with intercept (Δy = λ·y[t-1] + μ + ε). Intercept is required to
avoid bias when residuals have nonzero mean (EMA lag). ADF t-stat guard at −2.86 (5% MacKinnon).

**`compute_acf`** / **`compute_zscore`** — diagnostics. Z-score uses rolling mean and std.

---

### `backend/app/services/analytics_arm_a.py` — Arm A v1 VR habitat engine (FROZEN, do not modify)
Implements doc 18/18a exactly. Core function:

**`load_leg`** — loads TradingView CSV, UTC-indexed, deduped.

**`roll_transition_mask`** — flags roll seams: `|log-ret_t| > 8 × trailing-60-bar MAD`. Causal
(strictly trailing). Threshold frozen (ADR_003 R-6); cannot be tuned post-result.

**`level_vr`** — level-difference variance ratio VR(q) = Var(S_t − S_{t-q}) / (q · Var(ΔS)).
Computed in level-difference space (not log/return on the spread). The key property: defined
through zero, so β=1 definitional spreads (close-to-zero mean) are measured correctly.

**`surrogate_vr_ensemble`** — fits causal RW, GARCH(1,1), and OU surrogates from the real spread's
own empirical moments, simulates N=200 each, returns VR percentile distributions. The comparison
is always **real − matched surrogate**, never raw VR.

**`Spread` dataclass** — carries `s_close`, `s_open`, `beta`, `roll_transition`, `flat_bar`,
`index`, `meta`. The `beta` array is all-ones for definitional calendars (set explicitly in v2),
preventing any β-update-noise artifact.

This file is imported by analytics_arm_a_v2.py but **must never be modified** — it is the frozen
v1 primitive layer that v2 builds on additively.

---

### `backend/app/services/analytics_arm_a_v2.py` — Arm A v2 engine (additive over v1)
Implements doc 20 exactly. Imports frozen v1 primitives, adds only what doc 20 requires.

**`spread_from_series`** — wraps a vendor pre-built calendar (single OHLC series, β=1) into a v1
`Spread`. Sets `beta=np.ones(n)` explicitly; zero rolling-β DOF → structurally immune to v1
artifact. `jump_k=∞` by default (UNMASKED headline — the jump filter can only bias VR→1, so the
headline is always unmasked and any masked version is an ablation-only check).

**`increment_jump_mask`** — ABLATION-ONLY. Causal trailing-MAD gate in increment space. Never
used in the headline verdict.

**`deseasonalize_causal`** — subtract a causal trailing month-of-year seasonal mean (data ≤ t-1
only; §6.1 firewall). Until min_prior=2 same-month bars exist, falls back to causal global mean.

**`_fit_ma1noise` / `_sim_ma1noise`** — the MA(1) microstructure-noise null. Fits θ₁ from
negative incr ACF(1) of the real spread; simulates a pure MA(1) RW+noise process with same
marginal variance. This is the decisive null that kills bounce but not genuine MR.

**`evaluate_v2`** — main verdict function. Headline gate: `rw ∧ garch ∧ ma1` (all three martingale
nulls must fail for a confirm). Inherits min-VR multiplicity correction from v1. Returns plain
dicts (not models).

---

### `backend/app/services/analytics_mrscore.py` — MRScore observatory (STRUCTURALLY TERMINAL)
Computes the per-bar MRScore as a descriptive observatory diagnostic. It is **not a signal**,
not a detector, not a timing object. It is explicitly "structurally terminal" — it emits no
per-bar predictions and is not wired upstream into any decision logic.

The score has three blocks:
- Block 1: mean stability, variance stability, ADF/KPSS (regime character)
- Block 2: DRC window (dynamic range compression; Newey-West HAC + h-trim), hit_rate, variance_ratios
- Block 3: half-life proximity, vol_compression, TCF (c-free; trend correction factor)

**Key finding from testing (doc 09):** MRScore inverts on real data — a pure RW scored highest.
The architecture is correct (32 tests green); the discrimination is reliable only in expectation,
not in any single window. This is why MRScore is archived as a score and retained only as an
observatory diagnostic. Do not attempt to build entry/exit logic on it.

---

### `backend/app/services/analytics_substrate.py` — Substrate Observatory (STRUCTURALLY TERMINAL)
Computes per-bar substrate character: `directional_efficiency` (trend↔chop axis), `variance_ratio_mean`
(OU↔RW axis), `realized_vol_percentile`. Maps these to resemblance scores for four archetypes
(ou_like, trend_like, rw_null, ambiguous).

Key design choice: DE is primary (not VR) because drift adds to mean, not variance — a VR-primary
map misreads deterministic trends as RW (caught mid-build). Hurst removed (window/method-sensitive).

**Key finding (doc 10):** substrate character is scale-dependent. ADANIENT reads RW-null at all
causal windows 60–500 bars despite being visually trend-heavy. High-specificity, low-sensitivity
for OU. Terminal observatory; no timing/prediction authorized.

---

### Scripts

**`scripts/run_arm_a_v2.py`** — runs the Arm A v2 Cycle 1 evaluation (β=1 definitional calendars,
three nulls). Produces `data/processed/arm_a_v2_results.json`.

**`scripts/run_arm_a_v2_rolling.py`** — runs the Cycle 1b rolling-local pooled mean-z test.
Produces `data/processed/arm_a_v2_rolling_results.json`.

**`scripts/run_eia_conditional_test.py`** — ran the pre-registered EIA conditional entry speed
gate. Result: KILLED (p_rw=0.502).

**`scripts/run_selectivity_test.py`** — ran the pre-registered NG tail-selectivity test. Result:
A_FALSE_RESCUE.

**`scripts/hygiene_arm_a_v2.py`** — pre-run checks (data completeness, date alignment, etc.).

---

## 4. Kalman μ* — current status in detail

**What it is:** A 2-state local-linear-trend Kalman filter where state = `[μ_t (level), v_t (velocity)]`.
The velocity state is the only thing distinguishing it from EMA — a level-only Kalman is
algebraically an EMA at steady state.

**Why the velocity matters:** Inside a linear trend of slope m, EMA's residual has a deterministic
offset `slope × span/2` that grows without bound. This offset pushes the residual sign to one side
of zero — EMA residual sign-agreement with the true deviation drops to ≈ 0.49 (coin flip). The
velocity state absorbs the trend's first moment into μ*, keeping the innovation centered
(sign-agreement ≈ 0.85, residual mean ≈ 0.085 regardless of slope).

**Frozen constants (must not be tuned):**
```python
KALMAN_KAPPA = 0.05   # q_μ = κ·q_v
KALMAN_SNR   = 1e-8   # q_v / R_p; effective span ≈ 141 bars
KALMAN_WARMUP = 60    # bars for R_p (MAD-based) normalization
```

**Current epistemic status:**
- Mechanism (EMA lag bias `slope·span/2`): **confirmed HIGH** — analytic, holds for any linear trend
- Centering advantage over matched-span EMA: **confirmed on synthetic** (p < 1e-30 across 360 conditions)
- Real-market centering: **LOW confidence** — confounded by S1 (detrending tautology) and not
  clearly confirmed/denied
- False-centering (S2): catastrophic form **excluded (B classification)** but unresolved due to
  single instrument, R²ₒₒₛ ≈ 0; cannot confirm benign at more than LOW-MEDIUM confidence
- **EMA remains production μ*. Kalman is research-only comparison estimator.**
- **Reopen trigger:** if any upstream component needs to depend on μ* reversion fidelity (not just
  centering/charting), the cross-instrument panel (Step 2A.5 substitute) must run first.

**Kalman is deprioritized for now** (doc 32 "sacred cows killed"). Kalman μ* development is
reduced to diagnostic instrumentation — no Tier 1 question currently depends on it.

---

## 5. MR Habitat research — current status in detail

**What MR Habitat tests:** whether a spread's level-difference variance ratio VR(q) is
distinguishable from its own matched surrogate in the mean-reverting direction (VR < 1 AND
VR < surrogate), using pre-registered windows and surrogate families.

**Core construction insight (durable, frozen):** the admissibility of a spread's β construction
governs whether any VR test is valid. The β taxonomy:

| β mode | Status | Why |
|--------|--------|-----|
| β = 1 (definitional — same-unit calendars) | **ADMISSIBLE** | Zero rolling-β DOF; zero β-update-noise |
| Rolling-OLS-β on levels (W=60) | **INADMISSIBLE** | Manufactures VR≫1 via β-update-noise (82–97% of Var(ΔS)) |
| Controlled/regularized β (Kalman-β, Ridge, Frozen pre-sample) | **UNTESTED** — Cycle 2 |

**What we know:**
- NG front calendar (ng12): **CONFIRMS** (VR=0.448, p=0.005 vs RW, p=0.005 vs MA(1)-noise). True MR.
- NG MR: **real and persistent** (p≈2e-4, 19 years), regime-conditional (off in storage-glut years).
- NG MR: **uneconomic** as a naive book. Gross ≈ 7.5× too small vs round-trip cost.
- Selectivity (conditional z-entry): **KILLED** on NG. p_ou = 1.000 everywhere.
- EIA inventory conditioning: **KILLED** on NG. p_rw = 0.502.
- Portfolio rescue: **not possible** with cohort n=1.
- Brent self-built calendar (BRN1!−BRN2!, 60min): confirms at all horizons — **apparatus
  corroboration**; but hourly, so not directly comparable for daily book construction.

**What is not yet known:**
- BRN M1-M2 daily calendar (need BRN2! 1D data — not yet acquired)
- Crack spread controlled-β (need HO/RB daily leg data — not yet acquired)
- Controlled-β admissibility for pairs (Gold-Silver as positive control candidate — pre-reg exists
  but execution blocked on controlled-β apparatus being proven)
- NG back-adjustment (splice on actual ng12 seam dates vs rebuild from raw m1/m2 legs)

---

## 6. What is frozen / killed / deferred (full map)

| Object | Status | Why |
|--------|--------|-----|
| State T (pre-reversion morphology) | **KILLED — FROZEN** | 62/62 cross-habitat rejects; zombie prohibition binding |
| Predictive transition object | **§4-FORBIDDEN** | Object-class error: no causal transition label exists |
| MRScore as a signal | **ARCHIVED** | Inverts on real data (RW scores highest) |
| CSU as identity of reversion | **ARCHIVED** | Analytically demolished |
| Rolling-OLS-β-on-levels for VR tests | **INADMISSIBLE** | Manufactures VR (proved synthetically) |
| EIA conditional entry for NG | **KILLED** (p_rw=0.502) | Selection-on-regime artifact |
| NG selectivity (unconditional z-entry) | **KILLED** (p_ou=1.000) | OU beats NG at every threshold; regime-conditional MR breaks unconditional selectivity |
| Centering as primary Kalman criterion | **DEMOTED** | S1 detrending confound makes it a tautology |
| Lag illusion module | **KILLED (C-medium)** | REP makes obvious lag visible; non-obvious lag immaterial |
| Portfolio construction on current cohort | **GATED** | Cohort n=1; cannot net or diversify |
| Kalman μ* as production estimator | **NOT YET** | S2 unresolved; EMA stays production |
| Residual ecology (observational) | **ACTIVE — gated, low priority** | §11.5 new arm; no zombie risk if observational-only |
| Etiology-conditioned reversion | **DEFERRED** | Best economic mechanism; data-gated (needs signed OFI) |
| Dynamic hedge ratio pairs | **DEFERRED** | Controlled-β apparatus must be proven first |

---

## 7. Next moves — ranked and gated

The strategic dependency graph (hard order; downstream gates cannot open before upstream):

```
apparatus-trust (§11.8, passed conditionally)
  → CONTROLLED-β ADMISSIBILITY (Cycle 2 = KEYSTONE)
    → cohort breadth (≥2 instruments with admissible construction)
      → per-instrument positive expectancy (gross > cost)
        → portfolio construction (netting + diversification now matter)
          → book cost test (max drawdown, cost grid 0.003/0.005/0.008)
            → DEPLOYABLE MR BOOK
```

**Immediate next 3 moves (priority-ordered):**

### Move 1 — NG rebuild + EIA direction (combined, Weeks 1–2)
**Why:** if NG's confirmed MR is a vendor back-adjustment artifact (splice noise at seam dates), the
EIA conditional test result is retroactively uninterpretable. Rebuild first. Acquire raw NG1!/NG2!
daily legs with roll schedule metadata. Build spread using `analytics_arm_a.py` roll-masking and
β=1 (same-unit calendar). Compare self-built VR(20) vs vendor VR(20). Kill gate: if self-built
VR(20) > 0.65 (materially worse than vendor 0.448), halt and report artifact finding.

### Move 2 — BRN M1-M2 daily calendar (parallel, Weeks 1–2)
**Why:** the only path to cohort breadth. Acquire BRN2! 1D raw leg. Construct daily spread same way
as self-built Brent (BRN1!−BRN2! with ADR_003 roll-masking, β=1). Run Arm A v2 apparatus (RW +
GARCH + MA(1)-noise nulls, N=200 speed gate, N=500 full). Kill gate: p_rw > 0.20 at N=200 → kill
BRN calendar direction; portfolio route delayed.

### Move 3 — Crack spread controlled-β positive control (Weeks 2–3)
**Why:** opens the entire pairs/cross-asset deployment domain. The pre-registration (doc 30) is
done. The implementation plan is ready (~200–270 new lines, reuses all existing apparatus). Primary
test pair candidates: Gold-Silver (textbook cointegrated pair, W=500 OLS gives VR(20)=0.60 in
diagnostic) or crack spread (HO2!/RB2! or similar). The β family hierarchy by survival probability:

| Family | Probability | Key risk |
|--------|-------------|----------|
| F6 Economic anchor β (fixed ratio from known parity) | 75–85% | Valid only for pairs with a known anchor |
| F5 Frozen β (pre-sample full-OLS, never re-estimated) | 70–80% | β instability over long OOS |
| F1 Kalman β (frozen q_β) | 55–65% | q_β too large → v1 artifact resurfaces |
| F3 Long-window OLS (W≥250) | 40–55% | M-gate unknown; symptom-only fix |
| F2 Ridge β | 40–50% | Three-knob DOF surface |

**The mechanistic gate for any β family:** the β-update-noise fraction `f_βupdate < τ` (τ = 10% of
Var(ΔS)) must be demonstrated on the chosen pair. If it fails, the family is inadmissible regardless
of apparent VR readings.

---

## 8. What is NOT next (explicitly parked)

- **Cycle-2 full controlled-β execution on all pairs:** blocked until Move 3 proves the apparatus
  on one pair.
- **Portfolio construction math:** blocked until ≥2 instruments independently clear the cost floor.
- **Residual ecology:** gated behind §11.8 positive control + Arm A v2. Highest zombie-risk.
- **UI work / workbench expansion:** no Tier 1 question requires new UI.
- **Kalman development:** deprioritized to diagnostic instrumentation only (doc 32).
- **ZC agricultural calendar:** do after BRN result known; structural diversification candidate but
  not first.
- **Any selectivity/conditioning on NG:** closed — do not re-open without fresh pre-registration on
  a new instrument that has inherently higher gross/cost ratio.

---

## 9. Data on disk right now

| Dataset | Status | Notes |
|---------|--------|-------|
| ADANIENT | 2,463 bars (real) | Placeholder visual substrate. Trend-heavy. NOT deployment evidence. |
| ng12 (vendor) | present | NG front calendar, daily. Back-adjustment unaudited. |
| BRN1! 1D | confirmed present (9,526 bars) | BRN front-month continuous. |
| BRN2! 1D | **NOT YET ACQUIRED** | Needed for BRN M1-M2 calendar — Move 2 blocker. |
| NG1!/NG2! raw legs | **NOT CONFIRMED** | Needed for NG rebuild — Move 1 blocker. |
| EIA storage DNAV | acquired 2010+ | Weekly; only back to 2010 (effective test window 2015–2026). Full vintage from EIA API still not acquired. |
| 46 TRUSTED commodity legs | on disk (`data/mr_cohort_manifest.md`) | The Arm A v1 cohort. Includes HO/RB/WTI etc. — crack spread raw legs may be here; confirm before acquiring externally. |
| arm_a_v2_results.json | present | Arm A v2 Cycle 1 full results. |
| arm_a_v2_rolling_results.json | present | Arm A v2 Cycle 1b rolling results. |

---

## 10. Sacred invariants that must not be violated

1. **Pre-register before touching data.** No exceptions. The pre-registration defines the exact
   primary statistic, N, OOS split, and cost assumption before any result-conditional computation.

2. **Surrogate-relative reads only.** Raw VR(q) without surrogate comparison is inadmissible
   evidence. The surrogate must be conditioned identically to the real series (same regime windows,
   same EIA conditioning, same roll masking).

3. **Temporal firewall.** At bar t, only data ≤ t-1 may be used. The causal firewall is proven via
   future-injection bit-identity acceptance tests in the engine.

4. **β-update-noise check for any new spread construction.** Every new β family must demonstrate
   `f_βupdate < τ = 10%` of Var(ΔS) before any VR test is interpreted.

5. **Zombie prohibition.** State T, predictive transition object, and MRScore-as-signal are dead.
   Any proposal to "revisit" them must explicitly pass the §4 zombie-reopen test (why it failed,
   new evidence, why prior objections no longer bind, which trigger fired).

6. **No threshold selection after seeing results.** EIA threshold is 10%, frozen before data
   touch. If a new instrument is tested, its threshold must be committed before the VR is computed.

7. **Vol-controlled check on any conditioning variable.** EIA conditioning improved gross but not
   VR on NG — a vol-selection artifact. Any new conditioning variable must be checked: does it
   improve VR, or only gross?

8. **Cost must clear at 0.005 (not just 0.003) before calling deployable.** The 0.003 round-trip
   assumption is probably 1.5–2× understated during high-|z| entries (elevated bid-ask at spread
   extremes). Require profitability at 0.005 before the deployment gate passes.

---

## 11. Test suite health (as of last audit)

| Suite | Count | Status |
|-------|-------|--------|
| Full backend suite | 120 | Green |
| `test_velocity_absorption.py` | 4 | Green (identity, matched-span, causal firewall, OOS finiteness) |
| `test_kalman_validation.py` | measurement locks | Green (annotations updated; assertions unchanged — measurement lock, not verdict lock) |
| `test_mrscore.py` | 32 | Green (incl. bit-identical firewall) |
| `test_substrate.py` | 25 | Green (incl. bit-identical firewall + 3 habitat-discrimination) |

---

## 12. Summary: where we stand in one paragraph

The apparatus is validated (§11.8 gate passed conditionally on NG). NG calendar MR is real and
persistent (p ≈ 2e-4) but uneconomic as a naive book. All levers that could rescue NG alone —
selectivity (KILLED), EIA conditioning (KILLED), portfolio construction (cohort n=1 = impossible)
— are exhausted. The binding bottleneck is cohort breadth: we need ≥2 admissible instruments with
positive expectancy before the portfolio route opens. The keystone gate is Cycle-2 controlled-β,
which opens the entire pairs/cross-asset domain. The immediate empirical programme is three
parallel tracks: NG self-rebuild (resolve back-adjustment), BRN M1-M2 daily calendar (first
breadth candidate), and crack spread controlled-β positive control (apparatus gate for all non-β=1
pairs). Data acquisition (BRN2! 1D, NG raw legs) is the current blocker for two of three tracks.
