# Canonical Spread Construction Protocol

**Document class:** Permanent AMR research record (DRAFT — pending red-team + Chief-Scientist approval).
**Status:** REVISED & APPROVED for promotion → doc 13 (red-team revisions applied 2026-06-03; audit trail `waiting_period/red_team_critique.md`).

> **▸ RED-TEAM REVISIONS APPLIED (binding — supersedes any conflicting text below).**
> 1. **ADR_003 dependency RESOLVED** — the roll-adjustment law this protocol deferred to is now written (`docs/decisions/ADR_003_roll_adjustment.md`, filled 2026-06-03); the two are consistent.
> 2. **High/Low forbiddance applies to CONSTRUCTED-from-legs spreads ONLY.** A *natively-traded exchange spread* (its own order book — a listed calendar/crack contract) has real synchronized OHLC and its High/Low are TRUSTED; the counterfactual-extrema rule (§6) binds only when WE difference legs.
> 3. **The Kalman-β "residual-manufacturing" claim is CONJECTURE** (transferred from the doc-07/12 μ\* lag finding, not demonstrated at the β level). The simplicity-first deferral of dynamic β stands regardless; do not cite the manufacturing claim as established.
> 4. **Empirical roll finding (this session):** TradingView `1!`/`2!` continuous are **non-back-adjusted (raw-stitched)** — roll-date jumps confirmed (`SI2!` 37.6% & `GC2!` 12.1% single-day artifacts @ 2026-01-30; ~monthly/quarterly spacing). Every leg-differenced spread MUST apply ADR_003 roll handling; `MIR1!/MIR2!` (FX) is cleanest.

**Date:** 2026-06-03.
**Scope:** The frozen methodological law governing how AMR may *legally* (causally, contamination-free)
construct a spread / relative-value series from its legs, across the deployment habitats (commodity calendar ·
intercommodity · equity pairs · fixed-income RV · cross-asset RV). Covers: hedge-ratio ontology, frozen
causality rules, missing-timestamp leg alignment, negative-price representation, continuous-futures roll
adjustment for legs, and the formal legality of spread OHLC. Produces **no** scores, signals, detectors, or
timing logic — it governs *data construction only*, upstream of every reversion statistic.

> **▸ CONTEXT (placeholder framing — frozen).** ADANIENT is a trend-heavy **placeholder visual substrate**, not
> the deployment domain. Every real-market conclusion in the AMR programme is **regime-local, not global**
> (CLAUDE.md §1.1). This protocol is regime-independent: it is a *construction-legality* law, not a reversion
> claim, so it binds equally in any regime.

> **▸ ZOMBIE PROHIBITION (inherited).** State-T (stabilization-then-reversion) is FALSIFIED-IN-FORM (doc 11).
> Nothing here proposes a T-detector, T-score, hazard, or "favorable-NOW" timing object. This is a data law.

> **▸ Method of derivation.** Causal rules are reasoned from first principles (the lookahead constitution).
> Technical/literature points are web-sourced with author/year/venue. Load-bearing claims I could not confirm
> are marked **(unverified)**. Per-class tags: **STRUCTURAL · MEASUREMENT · DATA · AMBIGUITY**.

---

## 0. Why this document exists (the Arm-0 finding, restated as a mandate)

The data audit (doc 12 §4; `data/cohort_manifest.md`) established the **binding empirical fact** that motivates
every rule below: **every deployment-domain spread on disk is a precomputed single `close` series with the legs
discarded.** Consequently the hedge ratio's causality is **unverifiable from the file** — a full-sample β makes
the series **stationary by hindsight construction**, which is *mechanically indistinguishable* from genuine mean
reversion. Result: **0 deployment-domain instruments** survived to the Arm-A whitelist; all 8 spreads are
**CONTAMINATED by default**. (DATA + STRUCTURAL.)

The lesson is not "find a better stationarity test." It is that **provenance is upstream of every statistic**,
and a spread is only as trustworthy as the *constructive proof* that it could have existed causally at time `t`.
This document is that constructive standard. **A spread with no causal construction proof is forbidden as
evidence**, regardless of how mean-reverting it looks.

**The single governing question (apply to every derived column, every bar):**

> *Could this exact value have existed, computed only from information available at time `t`, at time `t`?*

If the answer is "no" or "cannot be shown" → the value is **CONTAMINATED** and may not feed any
habitat/reversion verdict. Contamination is the **default**, trust is **earned**.

---

## 1. Hedge-ratio ontology — which β, in which habitat, and its lookahead risk

A spread is `S_t = A_t − β · B_t` (k-leg generalization: `S_t = A_t − Σ_i β_i B_{i,t}`). The choice of β is the
single highest-leverage modelling decision and the single largest lookahead surface. The ontology runs from
**most causally safe / least assumption-laden** to **least safe / most assumption-laden**. The frozen default
posture (CLAUDE.md complexity-earning rule): **start at β=1; escalate only when a simpler causal estimator is
demonstrably insufficient AND the more complex one is causally implementable.**

### 1.1 β = 1 — raw difference (structural / definitional spread)

- **What.** `S_t = A_t − B_t`. No estimation at all.
- **Habitat (primary).** **Calendar spreads** (same underlying, different expiry — e.g. `ng12`, `rb23`): the two
  legs are the *same commodity*, so a 1:1 economic relationship is *definitional*, not estimated. Also the
  correct default for **like-for-like intercommodity** spreads quoted 1:1 by convention (crack/crush ratios are
  the structural-β case, §1.5, not this one).
- **Causal estimation rule.** None required — there is no parameter, hence **no estimation lookahead is
  possible**. This is the *only* β with **zero** hedge-ratio lookahead risk.
- **Lookahead risk.** **None** from β. (Residual risks — roll adjustment §5, OHLC §6, alignment §3 — still
  apply.) (STRUCTURAL: the safest object.)
- **FROZEN-RULE HR-1.** Where a 1:1 economic relationship is *definitional* (same underlying / convention-quoted
  spread), **β=1 is mandatory** and a fitted β is **forbidden** — fitting a parameter that theory fixes at 1
  manufactures spurious DOF and reintroduces estimation lookahead for no economic gain.

### 1.2 Rolling-β — OLS / TLS hedge ratio on a trailing window

- **What.** Re-estimate `β_t` by regression of `A` on `B` (or total-least-squares / orthogonal regression when
  both legs carry comparable measurement error) over a **trailing window `[t−W, t−1]`**, applied at `t`.
- **Habitat.** **Equity pairs** and **cross-asset RV** where the ratio genuinely drifts and there is no
  definitional 1:1. The workhorse causal estimator; the standard remedy for the full-sample-β trap.
- **Causal estimation rule.** β estimated **strictly on data ≤ t−1**, **applied at `t`** (see FROZEN-RULE C-3).
  Walk-forward / re-estimate every step (or every rebalance period §2). Literature confirms the rolling re-fit
  *is* the standard lookahead remedy versus whole-sample regression (Chan, *Algorithmic Trading*, 2013;
  QuantRocket *Intro to Pairs Trading*; arbitragelab cointegration docs).
- **Lookahead risk (the central trap).** A **full-sample OLS β** is the canonical contamination: it chooses the
  β that makes the residual *most stationary over the whole sample*, i.e. it uses the future. This is **exactly**
  the Arm-0 contamination — indistinguishable from real MR (doc 12 §4; manifest §7). **Secondary risks:**
  rolling β is *noisy* — rolling least squares "can be very noisy with hedge ratio values varying widely"
  (QuantStart, *Dynamic Hedge Ratio … Kalman Filter*), which feeds the over-fitting/rebalance-churn problem; and
  the relationship itself is **non-stationary** — cointegration can break (Chan 2011, "When cointegration of a
  pair breaks down"; ECB WP 1013), so a window that straddles a structural break estimates a β that existed in
  *neither* regime. (STRUCTURAL + MEASUREMENT.)
- **FROZEN-RULE HR-2.** Rolling-β is the **default escalation** above β=1. It is admissible **only** under the
  §2 causality rules (trailing window, warmup, lag, rebalance). A full-sample / look-everywhere β is
  **PERMANENTLY FORBIDDEN** as evidence.

### 1.3 Cointegration-β — Engle–Granger (single relationship) / Johansen (system)

- **What.** Estimate β as the **cointegrating vector** so the residual is stationary. **Engle–Granger** (1987):
  two-step — regress `A` on `B`, test the residual for a unit root (ADF/CADF); the slope is β, hedges set to
  `(1, −β)`. **Johansen** (1991): ML estimation of *all* cointegrating vectors in a Gaussian VAR, jointly
  estimating the cointegration **rank** — required when **k ≥ 3 legs** (FI butterflies, multi-leg baskets)
  because Engle–Granger only delivers one relationship and inherits first-step residual error into the second
  step. *(Engle, R.F. & Granger, C.W.J., 1987, "Co-integration and Error Correction: Representation, Estimation
  and Testing," Econometrica 55(2):251–276. Johansen, S., 1991, "Estimation and Hypothesis Testing of
  Cointegration Vectors in Gaussian Vector Autoregressive Models," Econometrica 59(6):1551–1580.)*
- **Habitat.** **FI relative value** (multi-leg, term-structure baskets → Johansen), and **equity pairs / cross-
  asset RV** where you want the *economically motivated* long-run ratio rather than a raw rolling slope.
  Spread/term-structure MR is genuinely cointegration-anchored (doc 12 Arm A; Szymanowska et al. 2014 term
  premia; Gatev–Goetzmann–Rouwenhorst 2006 pairs).
- **Causal estimation rule.** Identical to rolling-β: the cointegrating vector must be estimated on a **trailing
  window ≤ t−1** and **re-estimated** on a fixed cadence (rolling-cointegration / walk-forward). A **single
  whole-sample** cointegrating β is the **most seductive form of the lookahead trap** — it is *defined* by
  full-sample stationarity (which series is dependent even flips on full-sample ADF; Chan/QuantStart). It is
  forbidden as evidence by the same rule as full-sample OLS.
- **Lookahead risk.** (a) **Full-sample cointegrating vector = guaranteed lookahead-stationarity** — the literal
  Arm-0 failure. (b) **Estimator fragility:** cointegration tests are "sensitive to sample period, structural
  breaks, and lag selection" (QuantRocket; sesen.ai); rejection frequency of *no-cointegration* collapses under
  a break in the relationship (ECB WP 1013) — so the test's *own* validity degrades exactly when the β is least
  stable. (c) **Direction ambiguity** in Engle–Granger (regress A~B vs B~A gives different β; the "pick the most
  negative ADF" rule is itself a full-sample selection unless done causally). (STRUCTURAL + MEASUREMENT.)
- **FROZEN-RULE HR-3.** Cointegration-β is admissible **only causally** (rolling/walk-forward window ≤ t−1, fixed
  re-estimation cadence, lagged application). **Engle–Granger for k=2; Johansen for k≥3.** A whole-sample
  cointegrating β is **FORBIDDEN as evidence** (it is the Arm-0 contamination by definition). The cointegration
  *test result* (is this pair cointegrated at all?) is **descriptive only** and must never be computed on the
  same full-sample window whose stationarity it then certifies.

### 1.4 Kalman / state-space dynamic hedge ratio — does it earn its complexity?

- **What.** Treat β_t as an unobserved state evolving as a random walk; observe it through the noisy regression
  `A_t = β_t B_t + ε_t`; recover β_t by the Kalman filter. The filter is **inherently causal** — its update at
  `t` uses only the measurement at `t` and the prior through `t−1` — and it needs **no window-length parameter**
  (QuantStart; Portfolio Optimization Book §15.6; letianzj). Reported to give **more stable, less noisy** β and
  **more stationary** spreads than rolling OLS (QuantStart; Medium/H. Wang).
- **Does it earn its complexity? — Adjudication: NO BY DEFAULT; DEFERRED. (AMBIGUITY → resolved conservatively.)**
  This mirrors the programme's standing Kalman ruling exactly. Doc 12 Arm C: *"Does Kalman ε revert better than
  EMA ε?" is the **wrong, smoother-contaminated question** — a faster-adapting fit mechanically manufactures a
  more-reverting, lower-variance residual* (the lag illusion, doc 07; doc 04 §1.5.4). The **same critique
  transfers verbatim** to a Kalman *hedge ratio*: a time-varying β that is allowed to chase the spread will
  **absorb the deviation into β** and **manufacture apparent mean reversion in the residual** — the residual
  reverts because β moved, not because the spread returned. This is the §6/doc-07 mechanism applied to the hedge
  ratio: **β-chasing is residual-manufacturing.** A Kalman β is *causal* (good) but **not automatically honest**
  (its process-noise / `delta` ratio is a tunable knob that, unconstrained, silently sets how much reversion it
  fabricates).
- **Causality.** The filter **is** causal *if and only if* its parameters (observation/process noise, initial
  state) are **frozen or estimated on a trailing window ≤ t−1** — a **full-sample EM fit of the noise
  parameters reintroduces lookahead** through the back door (the parameters were chosen knowing the whole path).
- **Lookahead risk.** (a) Full-sample EM/MLE tuning of `(Q, R, δ)` = lookahead. (b) **Residual-manufacturing**
  via an over-agile β (the decisive risk — it is the doc-07 lag illusion at the hedge-ratio level, not a data
  leak but an *interpretive* contamination that the frozen perturbation test cannot catch; doc 12 Arm C).
  (STRUCTURAL.)
- **FROZEN-RULE HR-4.** A Kalman/state-space dynamic hedge ratio is **DEFERRED — not authorized for v0
  construction.** It may be revisited **only** when (i) β=1 / rolling-β / rolling-cointegration are shown
  *insufficient* on a **verified** instrument, AND (ii) its noise parameters are frozen or causally estimated
  (no full-sample EM), AND (iii) it is evaluated by **equilibrium stability** ("did the relationship stay put?"),
  **never** by residual reversion fidelity (which it manufactures). Complexity must be *earned by a demonstrated
  failure of the simpler causal estimator*, not assumed. Until then: **do not solve a problem nothing has**
  (doc 12 Arm C).

### 1.5 Economic / structural β — theory-fixed ratios

- **What.** β fixed by economics/contract spec, **not** estimated from prices: crack spread (e.g. 3:2:1
  gasoline:distillate:crude), crush spread (soybean:meal:oil), DV01-/duration-neutral FI ratios, beta-/factor-
  neutral cross-asset constructs, exchange-defined calendar/inter-commodity ratios.
- **Habitat.** **Intercommodity** (crack/crush), **FI RV** (DV01 weights), **cross-asset RV** (factor/duration
  neutrality) — anywhere a *known production/contractual/risk identity* fixes the ratio.
- **Causal estimation rule.** The ratio is **known a priori**, so there is **no estimation lookahead** — *provided*
  the inputs to a *time-varying* structural β (e.g. DV01, which depends on yields known only at `t`) are
  themselves causal (DV01 at `t` uses the yield curve at `t` — fine; never a future curve). A *constant*
  structural ratio (3:2:1) has zero lookahead.
- **Lookahead risk.** **None from a constant ratio.** For a *dynamic* structural β (DV01-neutral), risk enters
  only if its market inputs use future information — forbidden by the general causal rule. (STRUCTURAL — second
  safest after β=1.)
- **FROZEN-RULE HR-5.** Where economics/contract/risk identity fixes the ratio, **use the structural β** in
  preference to any fitted β. A fitted β is admissible *only* to *test* the structural one descriptively, never
  to replace it silently. Time-varying structural inputs must be causal (≤ t).

### 1.6 Habitat → β decision map (frozen default; escalate only on demonstrated insufficiency)

| Habitat | Default β | Escalation (only if default insufficient on a *verified* instrument) | Forbidden |
|---|---|---|---|
| **Calendar spread** (same underlying) | **β=1** (HR-1) | — (1:1 is definitional) | any fitted β |
| **Intercommodity, ratio-quoted** (crack/crush) | **structural β** (HR-5) | rolling-β to *test* drift (descriptive) | full-sample β |
| **Equity pairs** | **rolling-β** (HR-2) | rolling-cointegration EG (HR-3) | full-sample / whole-sample coint β |
| **FI RV, 2-leg** | **structural (DV01)** (HR-5) | rolling-coint EG if no clean DV01 | full-sample β; future-curve DV01 |
| **FI RV, ≥3-leg basket** | **Johansen, rolling** (HR-3) | — | Engle–Granger for k≥3; full-sample vector |
| **Cross-asset RV** | **structural / rolling-β** | rolling-coint (HR-3); Kalman only after HR-4 gate | full-sample β; full-sample EM Kalman |

---

## 2. Causality rules (FROZEN) — the construction firewall

These bind **every** estimated-β path (§1.2–1.4). They are the constructive answer to the governing question.

- **FROZEN-RULE C-1 (trailing-window estimation).** Every estimated β/cointegrating-vector/state-space parameter
  is computed on a **trailing window that ends at or before `t−1`**. No statistic in the window may use any
  observation dated `> t−1`. Full-sample, two-sided, or centered estimation windows are **FORBIDDEN** for any β
  consumed at `t`. *(Rationale: lookahead constitution; the Arm-0 contamination is precisely a full-sample
  window.)*

- **FROZEN-RULE C-2 (warmup / burn-in).** No β is emitted, and **no spread bar is admissible**, until the
  trailing window holds the **minimum estimation length** (commit: ≥ the estimator's stated minimum; for a
  rolling regression, ≥ W observations). Bars before warmup completes are **masked (NaN), never imputed or
  back-filled** — emitting an under-determined β is silent contamination. *(Consistent with the cohort floors,
  manifest; and the LAG edge-mask precedent, doc 07 §2.)*

- **FROZEN-RULE C-3 (lag the β — the load-bearing rule).** β must be **estimated on data ≤ t−1** and **applied
  at `t`**: `S_t = A_t − β_{(≤t−1)} · B_t`. **Estimating β including the bar `t` it is applied to is lookahead**
  — even one bar. *(This is the "shift(-1) / contemporaneous-fit" trap of the lookahead constitution. A
  one-step misalignment invalidates the entire construction — Quantreo, "Look-Ahead Bias: The Invisible
  Killer"; quantjourney.)* **There is no acceptable exception.**

- **FROZEN-RULE C-4 (rebalance frequency / hysteresis).** β is **re-estimated on a fixed, pre-registered
  cadence** (every bar, or every N bars), chosen *before* seeing results — never tuned to improve apparent
  reversion. Re-estimating "when the spread looks wrong" is **outcome-conditioning** (circular; doc 12 Arm D).
  Lower rebalance frequency trades responsiveness for stability and **reduces β-noise/churn** (the rolling-OLS
  noise problem, §1.2). The cadence is a *frozen construction parameter*, not a free knob.

- **FROZEN-RULE C-5 (timestamp synchronization — applies to all β, incl. β=1).** Both legs must be sampled on the
  **same timestamp grid** before differencing. `A` and `B` must be aligned by **timestamp**, never by **row
  position/index** (positional/index merges silently pair mismatched bars — the "merge/index misalignment" trap).
  Cross-venue clock drift must be reconciled to a single canonical clock (UTC) *before* alignment. *(See §3 for
  the join semantics.)*

- **FROZEN-RULE C-6 (no future normalization).** Any normalization/z-scoring/scaling of the spread (downstream of
  construction) uses **trailing** moments only (`μ, σ` on `≤ t−1`). **Full-sample mean/σ, full-sample min–max,
  and future-realized volatility are FORBIDDEN.** *(The spread's own residual-reversion is smoother-manufactured
  — doc 12 §2 "load-bearing epistemic rule"; full-sample z-scoring re-imports the same hindsight.)* This rule is
  stated here because spread construction and spread normalization are routinely fused in one precompute — which
  is how the on-disk contamination happened.

---

## 3. Missing-timestamp leg alignment — which join is causal, which leaks

Legs rarely share a perfect timestamp set (holidays, half-days, venue/timezone differences, liquidity gaps).
The alignment method is a **causality decision**, not a convenience choice.

- **Inner-join / intersection (KEEP only timestamps present in *both* legs).** **CAUSAL — MANDATED DEFAULT.**
  A spread bar exists **iff both legs were genuinely observed at that timestamp**. Uses no information the market
  did not have. Cost: drops bars (reduced sample) — *acceptable*; a smaller honest series beats a larger
  contaminated one. (STRUCTURAL — safe.)

- **Forward-fill / last-observation-carried-forward (LOCF) on the *missing* leg.** **CONDITIONALLY CAUSAL, HIGH-
  RISK — RESTRICTED.** Forward-fill uses only the *last known* value, so a **strictly past-only** forward-fill
  does not by itself peek into the future. **BUT** it is the documented source of two contaminations:
  (a) it **fabricates observations that never traded**, manufacturing artificial autocorrelation / false
  stillness in the spread (a stale leg makes the spread look more mean-reverting than reality — the same
  smoother-manufactured-reversion family, doc 12 §2); and (b) panel/calendar fills routinely **extend a series
  before its first real observation** or across a non-trading gap, which is a real leak (arbitragelab/Quantreo;
  "Temporal Coverage Bias," arXiv 2603.20237). It is **never** acceptable for the *target/triggering* leg.

- **Back-fill / interpolation / any two-sided fill.** **FORBIDDEN — LEAKS BY CONSTRUCTION.** Back-fill and
  interpolation use a **future** observation to fill the present. This is direct lookahead. (STRUCTURAL.)

- **Tolerance / as-of merge (nearest within Δ).** **CAUSAL ONLY IF BACKWARD-ASOF.** A `merge_asof` that matches
  each `A`-timestamp to the **most recent `B` at or before it** (`direction="backward"`, finite tolerance) is
  causal — it is a bounded past-only forward-fill. A **forward** or **nearest** as-of is **FORBIDDEN** (it can
  bind a future `B`). Tolerance Δ must be small relative to the bar and **pre-registered**.

- **FROZEN-RULE AL-1 (default).** **Inner-join on synchronized timestamps is the mandated default** for all
  spread construction. It is the only alignment with no fabrication and no leak.
- **FROZEN-RULE AL-2 (fills).** Forward-fill / backward-asof is admissible **only** when (i) strictly past-only,
  (ii) bounded by a small pre-registered tolerance, (iii) applied **only** to a non-triggering leg, (iv) the fill
  fraction is **recorded per series** and a high fill fraction marks the series **CONTAMINATED** (fabricated
  stillness ⇒ untrustworthy MR). **Back-fill and interpolation are FORBIDDEN, always.**
- **FROZEN-RULE AL-3 (sessions / holidays / timezone).** Legs are reconciled to a **single canonical clock (UTC)**
  and a **common trading-session calendar** *before* alignment. Cross-session/holiday mismatches are resolved by
  **dropping the unmatched timestamp (inner-join), never by filling across the gap.** Timezone/DST drift is a
  silent index-misalignment source (C-5) and must be normalized first. (DATA + MEASUREMENT.)

---

## 4. Negative prices — levels vs returns vs transforms

Spreads **legitimately go negative** (verified on disk: `cl_brn`, `ng12`, `rb23`, all coffee-cocoa,
hdfc-icici — thousands of negative-close bars each; manifest). This is not corruption — it is the nature of a
difference. The April 2020 event is the canonical proof that even a *single outright* futures price can be
negative (WTI CLK20 settled **−\$37.63** on 2020-04-20; Merton & Nagy event study, MIT Sloan; EIA), so any
representation that assumes positivity is structurally wrong for this domain.

- **What breaks under negativity.** **Log price `ln(S)` is undefined for `S ≤ 0`.** **Log returns
  `ln(S_t/S_{t−1})` and simple returns `S_t/S_{t−1} − 1` are undefined or meaningless** across a sign change
  (and explode as `S → 0`). Therefore **every return-space, log-space, ratio, or percentage statistic is
  invalid on a spread that can cross zero** — including any VR/Hurst variant computed on *spread* log-returns,
  and any geometric/CAGR aggregation. (MEASUREMENT — this silently NaNs or, worse, returns garbage.)
- **Mandated representation.** **LEVEL DIFFERENCES.** The spread is a **level series in price units**; its
  dynamics are described by **first differences `ΔS_t = S_t − S_{t−1}`** (additive, sign-safe, well-defined
  through zero), **never** by log/simple returns of the level. This matches the manifest's per-instrument
  "LEVEL-DIFF required; log/return math forbidden" flag and CLAUDE.md's negative-price handling.

- **FROZEN-RULE NP-1.** A spread that can be ≤ 0 (any leg-difference, by default) is a **level series**;
  its representation is **first differences in price units**. **Log price, log returns, simple/percentage
  returns, and any ratio transform of the *spread* are PERMANENTLY FORBIDDEN** on such a series.
- **FROZEN-RULE NP-2.** **Return-space statistics belong on the *legs* (which are positive), not on the
  spread.** Where a return-space tool is wanted (e.g. variance-ratio character on a positive outright, doc 12
  Arm A), it is computed on the **leg** or on a verified-positive instrument — never on a sign-crossing spread.
  *(This is why Arm A's whitelist is single-name positive equities — the only place return-space VR is legal.)*
- **FROZEN-RULE NP-3.** Any normalization of a level spread (§C-6) uses **additive trailing** statistics
  (rolling mean / rolling σ of `ΔS` or of `S`), **never** multiplicative/log scaling.

---

## 5. Continuous-futures roll adjustment for spread legs

A spread leg that is a **continuous (rolled) futures series** carries roll-adjustment artifacts *into the
spread*. The adjustment method is therefore a **leg-construction legality** question, governed jointly with the
repo's frozen roll-adjustment ADR (`docs/decisions/ADR_003_roll_adjustment.md`) — which this protocol treats as
the authoritative slot for the roll decision and **extends to the spread-leg case**. *(Note: ADR_003 is a
referenced frozen slot in the repo; its body is not reproduced here. The empirical roll observation on disk is
`g1_gold` — flagged in the manifest as "back-adjusted CONTINUOUS futures; roll/adjustment method undocumented →
historical levels construction-dependent," with 630 structurally-invalid OHLC bars. Treat undocumented roll as a
provenance defect, per PROVISIONAL disposition.)*

| Method | Mechanism | Artifact injected | Returns preserved? | Levels meaning |
|---|---|---|---|---|
| **Back-adjusted, additive (Panama)** | shift each older contract by a **constant** so the seam matches | **trend/drift bias**; **negative historical prices** for deep history; **destroys percentage returns** (a fixed +/−Δ changes the %); seam-jump removed only in absolute terms | **NO** | **distorted / artificial** (absolute shift) |
| **Ratio / proportional adjustment** | multiply older prices by the **ratio** new/old at each seam | preserves % returns; **historical absolute levels are scaled (not the true traded price)** | **YES** | scaled, returns-faithful |
| **Forward-adjusted** | hold history fixed, adjust **forward** contracts | **most recent prices are not the true current price** (bad for live trading) | depends | recent levels artificial |
| **Proportional (returns-stitched)** | stitch on returns, integrate | preserves % returns by construction | **YES** | reconstructed from returns |

Sources: QuantStart *Continuous Futures Contracts for Backtesting*; QuantPedia *Continuous Futures …
Methodology*; arbitragelab *Futures Rollover*; QuantInsti *Futures Continuation*; QuantVPS continuous-futures.
The consensus: **back-adjustment introduces a drift bias and can drive deep history negative and breaks
percentage returns; proportional/ratio keeps percentage moves intact; only adjusted (never raw-spliced) series
should be used, and the raw-splice seam jump (e.g. the cited VIX 14.8% phantom jump vs 0.3% real) corrupts any
backtest.**

**Interaction with the rest of this protocol (the key tension):**
- **Additive back-adjustment + spread = double trouble.** It (a) can make a leg negative — but per §4 the spread
  is already a level series, so leg negativity is tolerable *for the spread level* **iff** all spread math is
  level-difference (NP-1); and (b) injects a **drift bias** into the leg that the spread then inherits, which can
  **manufacture or mask apparent mean reversion** — a STRUCTURAL contamination of the very property AMR studies.
- **Ratio adjustment + spread = inconsistent units.** Ratio-scaled legs are **not in true price units**, so
  `A − βB` mixes two differently-scaled legs and the difference is **economically meaningless as a price spread**
  (you are differencing rescaled histories). Ratio adjustment is right for *single-leg return analysis*, wrong
  for *cross-leg level differencing*.

- **FROZEN-RULE RA-1.** For **spread legs differenced in level space (NP-1)**, the legal continuous-futures
  construction is the one that preserves **true price levels at the seam without injecting absolute drift** —
  i.e. a roll that keeps legs in **comparable, true-price units**. **Additive (Panama) back-adjustment is
  FORBIDDEN as a spread leg** (drift bias contaminates the MR property; can break level comparability). **Ratio
  adjustment is FORBIDDEN as a spread leg** (rescaled legs are not in comparable price units for differencing).
- **FROZEN-RULE RA-2.** The **preferred** spread-leg construction is to **build the spread from the actual
  individual contracts on a defined roll schedule** (roll both legs on a pre-registered, causal calendar; keep
  the seam explicit) rather than from a pre-rolled single continuous series — because only then are both legs in
  **true, synchronized price units** at every `t`. Where only a pre-rolled leg exists, it is **PROVISIONAL at
  best**, and **CONTAMINATED if the roll/adjustment method is undocumented** (the `g1_gold` case; defer to
  ADR_003).
- **FROZEN-RULE RA-3 (roll causality).** The roll **schedule** must be causal: roll on a **pre-registered rule**
  (e.g. N days before expiry, or first notice) known at `t` — **never** roll on a future-realized condition
  (e.g. "roll at the volume-crossover" computed with hindsight). The roll date is a frozen construction
  parameter. (Ties to C-4.)
- **(LOW-confidence flag.)** The precise *preferred* adjustment for a level spread (true-price splice with
  explicit seam vs a difference-adjusted variant) is asserted here from first principles + the cited
  practitioner consensus; **ADR_003 is the binding authority** and, if it specifies a different concrete method,
  **ADR_003 governs** and RA-1/RA-2 must be reconciled to it. Marked LOW until ADR_003's body is confirmed.

---

## 6. Spread OHLC legality (FORMAL) — the synthetic-bar law

This is the formal statement of the synthetic-spread constitution already applied operationally in the cohort
manifest (§6 there). It is the **most distinctive law in this document** because it is routinely violated by
every charting/precompute pipeline that emits a 4-column spread bar.

### 6.1 The structural fact (why High/Low are counterfactual)

For a synthetic spread `S = A − βB`, each leg's **High and Low occur at *different timestamps within the bar***.
The spread's true intrabar maximum is `max_τ (A_τ − βB_τ)` over the *joint* path; this is **not**
`max(A) − β·min(B)` and **not** `max(A) − β·max(B)`. In general:

```
max_τ (A_τ − βB_τ)  ≤  max(A) − β·min(B)        (naïve "spread high" OVERSTATES range)
min_τ (A_τ − βB_τ)  ≥  min(A) − β·max(B)        (naïve "spread low"  UNDERSTATES range)
```

A "spread High" formed by combining each leg's *separately-timed* extreme describes a price state **that never
existed** (the legs were never simultaneously at those extremes). This is **externally corroborated**: CQG
states that real time-of-high/low retrieval "**cannot be used with synthetic spreads**" and must be reconstructed
bar-by-bar from the underlying intrabar path (CQG, *Synthetic Spread Time of High and Low*). It is **empirically
corroborated in-repo**: leg-wise spreads showed **structurally-invalid OHLC bars** (manifest: `g1_gold` 630,
`ng12` 169, `rb23` 35 invalid bars where the OHLC ordering `L ≤ {O,C} ≤ H` is violated).

By contrast, **Open and Close are timestamp-synchronized** — both legs *are* observed at the bar's open instant
and the bar's close instant — so `S_open = A_open − βB_open` and `S_close = A_close − βB_close` are **real,
contemporaneous states**.

### 6.2 The formal rules

- **FROZEN-RULE OHLC-1 (Open).** **`S_open = A_open − β B_open` is ADMISSIBLE (TRUSTED)** — both legs observed at
  the bar-open timestamp (synchronized). β per §1–§2 (causal, lagged).
- **FROZEN-RULE OHLC-2 (Close).** **`S_close = A_close − β B_close` is ADMISSIBLE (TRUSTED)** — both legs observed
  at the bar-close timestamp (synchronized). **Close is the canonical spread observable; all spread statistics
  default to Close.**
- **FROZEN-RULE OHLC-3 (High/Low — default FORBIDDEN).** **Naïve spread High/Low formed from per-leg extrema are
  UNTRUSTED and FORBIDDEN as data.** They are counterfactual states (§6.1) that overstate/understate true range.
  **No statistic — range, true-range, intrabar vol, candle morphology, gap, wick — may consume a naïve spread
  High/Low.** Any pipeline emitting a 4-column spread bar must **mark H/L untrusted** (or drop them).
- **FROZEN-RULE OHLC-4 (Volume / OI — conditional).** Spread Volume/OI is **CONDITIONAL — per-leg only** (there is
  no single "spread volume"; min/sum/leg-specific are different objects). Admissible only with an explicit,
  documented per-leg definition; otherwise **omit**.
- **FROZEN-RULE OHLC-5 (the *only* condition under which High/Low become TRUSTED — synchronized intrabar
  reconstruction).** Spread High/Low are admissible **iff** they are reconstructed from the **joint synchronized
  intrabar leg paths**: sample both legs on a common sub-bar grid `{τ}`, form `S_τ = A_τ − β B_τ` **causally**
  (same lagged β), and take `S_high = max_τ S_τ`, `S_low = min_τ S_τ`. This requires **synchronized sub-bar leg
  data** (which the on-disk precomputes do **not** have — legs are gone, §0). Absent that data, OHLC-3 holds and
  H/L stay forbidden. The reconstruction must itself obey C-1…C-5 (no future τ, synchronized grid).

### 6.3 Practical consequence (frozen)

Every downstream spread computation **defaults to Close** (OHLC-2), may use **Open** (OHLC-1), and **must not
touch High/Low** unless OHLC-5's synchronized intrabar reconstruction has actually been performed on real
synchronized leg data. **A spread bar whose H/L came from a precompute with discarded legs is, for H/L,
permanently untrusted.** (This is exactly the manifest's standing treatment of all 8 on-disk spreads.)

---

## 7. Disposition summary (how this protocol grades a candidate spread)

A constructed spread is admissible **as evidence** only if **all** hold (else **CONTAMINATED**):

```
β provenance        : β=1 (definitional) OR structural OR causally-rolling/coint (C-1) — NEVER full-sample
β timing            : estimated ≤ t−1, applied at t (C-3), warmed-up (C-2), fixed rebalance (C-4)
alignment           : inner-join on synchronized UTC timestamps (AL-1); fills past-only+bounded+recorded (AL-2)
representation      : level differences if sign-crossing (NP-1); return-space only on positive legs (NP-2)
roll (if futures)   : true-price comparable legs (RA-1/2); causal roll schedule (RA-3); documented (else PROVISIONAL/CONTAMINATED)
OHLC                : Open/Close only (OHLC-1/2); H/L forbidden unless synchronized intrabar reconstruction (OHLC-5)
normalization       : trailing-only, additive (C-6 / NP-3)
```

**Default disposition of any spread lacking a constructive causal proof of its β: CONTAMINATED.** Trust is
earned by construction, not granted by appearance. This is the permanent generalization of the Arm-0 verdict:
**the bottleneck is provenance, not theory** — and this document is the provenance standard.

---

## 8. Surviving uncertainty · explicit non-conclusions · next question

**Confidence in the protocol:** **MEDIUM-HIGH.** The causal rules are first-principles consequences of the
(frozen) lookahead constitution and the in-repo Arm-0 evidence; the OHLC law is independently corroborated
(CQG) *and* empirically corroborated in-repo (invalid-bar counts). The literature points are author/year/venue
sourced.

**Lower-confidence items (flagged):**
- **RA-1/RA-2 concrete preferred method (LOW–MEDIUM).** Asserted from practitioner consensus + first principles;
  **ADR_003 is the binding authority** and governs if it specifies a concrete method — reconcile, do not
  override (§5 flag).
- **Kalman HR-4 (MEDIUM).** The residual-manufacturing critique is a direct, defensible transfer of the doc-07 /
  doc-12-Arm-C ruling to the hedge ratio; it has **not** been empirically demonstrated *at the β level* in this
  repo (only at the μ\* level). The *deferral* is high-confidence; the *mechanism claim* is MEDIUM pending a
  β-level demonstration.
- **Forward-fill threshold (AMBIGUITY).** "High fill fraction ⇒ CONTAMINATED" (AL-2) needs a pre-registered
  numeric cutoff before use; left unspecified here deliberately (a free post-hoc threshold is itself a DOF).

**Explicit non-conclusions.** This document makes **no** claim that any habitat *is* mean-reverting (that is
Arm A, gated on a *verified* instrument); **no** claim that any on-disk spread can be rescued (all 8 remain
CONTAMINATED); **no** signal/score/detector/timing claim of any kind. It governs construction legality only.

**Next high-information question.** *Can a legal spread be constructed at all from acquirable data?* — i.e.,
obtain a real mean-reverting instrument **with its legs intact** (the §RA-2 / doc-12-Arm-D data unlock), apply
this protocol end-to-end (causal rolling/structural β, inner-join, level-diff, Open/Close-only), and only then
ask Arm A's "does it separate from a matched null?" on a series whose causality is *proven by construction*
rather than *assumed and unverifiable*.

---

*Markers used: FROZEN-RULE · FORBIDDEN · TRUSTED · CONTAMINATED · PROVISIONAL · CAUSAL · DEFERRED. Problem
classes: STRUCTURAL · MEASUREMENT · DATA · AMBIGUITY. This is a DRAFT pending red-team + Chief-Scientist
approval; the roll section defers to the frozen `ADR_003_roll_adjustment.md` where they would conflict.*
