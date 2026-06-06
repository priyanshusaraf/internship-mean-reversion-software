# 29 — Doc 28 Implementation Plan (constrained implementation, NOT research)

## Status

```text
DATE:        2026-06-04
MODE:        Controlled Implementation Mode (§3.2) — PLAN ONLY. No code written. No data touched. No execution.
SCOPE:       The minimum faithful implementation of the FROZEN doc 28 protocol. Nothing more.
PROHIBITED:  model search · parameter tuning · threshold sweeps · architecture creativity · premature
             extensibility · any State-T resurrection. Doc 28 freezes the science; this plan freezes only HOW.
PRINCIPLE:   "disappointingly simple but causally faithful." In doubt → simplicity over flexibility.
GROUNDING:   the doc-28 §3.1 VR classifier and §3.5 surrogate ensemble ALREADY EXIST in analytics_arm_a.py
             (level_vr, surrogate_vr_ensemble, OU/RW/GARCH sims, VR_Q_GRID=(2,5,10,20)). Build only the gap.
```

---

## 0. Reuse inventory (what exists vs the genuine build gap)

```text
REUSE AS-IS (faithful to doc 28 — do NOT reimplement):
  analytics_arm_a.py    load_leg · construct_spread · Spread · _valid_increment_mask · roll_transition_mask
                        · level_vr(s, invalid_bar, qs)               → doc 28 §3.1(i) VR(q) estimator (ratified)
                        · surrogate_vr_ensemble(spread, family,…)    → doc 28 §3.5 bit-identical extraction
                        · _fit_rw/_sim_rw · _fit_ou/_sim_ou · _fit_garch/_sim_garch → §3.5 OU/RW/GARCH families
                        · VR_Q_GRID=(2,5,10,20) · N_SURROGATE · SURR_PCTILE
  analytics_arm_a_v2.py ma1_vr_ensemble (4th family, bonus) · multiplicity-corrected min-VR pattern
  analytics_mrscore.py  adf_kpss_pvalues(...)                        → §3.1(iii) stationarity (ADF ∧ KPSS)
  analytics.py          compute_acf(...)                             → §3.1(ii) ACF band · compute_halflife
  synthetic.py          ou() · random_walk()                        → §3.8(B) zero-controls
                        regime_switch()                             → §3.8(C) Markov MR↔non-MR power control
  store.py · loader.py  data access

GENUINE BUILD GAP (small, additive — one new module file):
  G1  habitat_label(s, window, θ) → {0,1}     compose level_vr ∧ ACF-band ∧ ADF∧KPSS, RELATIVE-to-null θ
  G2  transition_delta(H_class, H_test) → δ    2×2 off-diagonal contrast (§3.4)
  G3  delta_excess(real, surrogates) → float   real − WORST-CASE surrogate member (§3.4/§3.5)
  G4  measure_L(null_paths, classifier) → L    classifier-statistic autocorr decay length (§3.2 F1)
  G5  calibration_gates(real, surrogate_fit)   the 4 F2 hard gates (§3.5)
  G6  splice_null · periodic_null              the 2 missing §3.5 surrogate families (futures legs only)
  G7  step0_controls()                         §3.8 (A)/(B)/(C) orchestration + verdict
  G8  causal_bitidentity_test()                §3.6 future-injection acceptance test
DEFER ENTIRELY until Gate 1 passes (NOT part of Step 0):
  binary eligibility contract + hysteresis (§4) · three-arm books + materiality (§5/§6) — Gate 2.
```

One new file is sufficient for Step 0: **`backend/app/services/analytics_habitat.py`** (G1–G5, G7, G8) plus a small
addition to `synthetic.py` for G6 (only when the Step-0 real control is a futures leg). No new framework, no new
package, no router/endpoint yet (endpoints are a Gate-2/observatory concern, deferred).

---

## 1. Dependency graph (the implementation DAG)

```text
LAYER 0 — FOUNDATION (all EXIST; zero build):
  data:    load_leg / construct_spread / Spread / _valid_increment_mask / roll_transition_mask
  est:     level_vr                      (VR(q), §3.1 i)
  est:     compute_acf                   (ACF band, §3.1 ii)
  est:     adf_kpss_pvalues              (stationarity, §3.1 iii)
  surr:    surrogate_vr_ensemble + _sim_{rw,ou,garch}   (§3.5 families 1–3)
  synth:   ou / random_walk / regime_switch             (§3.8 controls)

LAYER 1 — PRIMITIVES (build G1, G6):
  G1 habitat_label  ── depends on ▶ level_vr, compute_acf, adf_kpss_pvalues, θ(frozen)
  G6 splice/periodic nulls ── depends on ▶ raw m1/m2 legs, roll calendar   (only if real control is a futures leg)

LAYER 2 — STATISTIC (build G2, G4):
  G2 transition_delta ── depends on ▶ G1 applied to [t−k,t] (H_class) AND [t+1+g,t+h] (H_test)
  G4 measure_L        ── depends on ▶ G1, surrogate paths (matched null)        ┐ G4 OUTPUT g-grid
                                                                                │ feeds G2's test window offset
LAYER 3 — SURROGATE-RELATIVE READ (build G3, G5):
  G5 calibration_gates ── depends on ▶ surrogate fits, real autocorr           (GATE: reject bad surrogate fit)
  G3 delta_excess      ── depends on ▶ G2 on real, G2 on EACH surrogate family, G5 passing, worst-case member

LAYER 4 — CAUSAL + CONTROL HARNESS (build G7, G8):
  G8 causal_bitidentity_test ── depends on ▶ G1 (future-injection invariance)   (GATE: leakage → HALT)
  G7 step0_controls          ── depends on ▶ G1, G2, G3, G4, synth controls, ONE real reverter

LAYER 5 — GATE 1 RUNNER (build later; NOT Step 0):
  gate1_run ── depends on ▶ ALL above + θ frozen + STEP 0 PASSED + frozen (k,h,g,θ,q) grid

LAYER 6 — GATE 2 (defer until Gate 1 passes):
  binary contract + hysteresis + three-arm books + materiality  ── depends on ▶ Gate 1 = pass
```

### Hard blockers (ordered; nothing downstream is valid until each clears)

```text
B1  θ + the H=1 Boolean rule FROZEN on the DISJOINT calibration cohort (F3) BEFORE any test evaluation.
    Procedural, not code: θ is a loaded frozen constant; the code path contains NO optimizer over θ.
B2  G8 causal bit-identity test PASSES (future-injection invariance). If it fails → leakage → HALT; no
    result, positive or negative, is interpretable.
B3  G4 measure_L completes on the matched null → the g-grid {ceil(L)…8·ceil(L)} becomes usable (§3.7).
    Until L is measured, g is undefined and G2's test-window offset cannot be set.
B4  STEP 0 (§3.8 A/B/C) PASSES. THE MASTER BLOCKER: "before any δ_excess ≤ 0 is a credible kill, the
    apparatus must confirm a known real reverter, print ≈0 on zero-controls, and recover regime-switch
    persistence." Gate 1 on the real cohort does NOT begin until B4 clears.
```

---

## 2. Minimum module list

Each module: smallest faithful surface. Target line counts are ceilings, not goals — prefer fewer.

### G1 — `habitat_label(s, invalid_bar, *, theta) -> int`  (~40–60 lines)
```text
PURPOSE:  the doc 28 §3.1 binary habitat label on one window.
INPUTS:   s (level series of the window), invalid_bar mask, theta (FROZEN scalar from calibration cohort).
OUTPUT:   int ∈ {0,1}. NOTHING ELSE leaves the function.
FROZEN:   H=1 iff  [VR(q)<1 ∀ q∈{2,5,10,20} within band]  ∧  [ACF in frozen band]  ∧  [ADF ∧ KPSS pass],
          AND the sub-diffusivity margin exceeds theta ("more sub-diffusive than the matched null", NOT
          merely "stationary"). The Boolean is a fixed deterministic function — no per-call re-optimization.
MUST NOT: return a probability/score/VR value/p-value/margin; condition on the SIGN of any first moment;
          use any smoother / Kalman / rolling-β state (κ̂-free, §3.1 cut b); read any bar outside the window.
```

### G2 — `transition_delta(H_class: np.ndarray, H_test: np.ndarray) -> float`  (~15–25 lines)
```text
PURPOSE:  §3.4 persistence statistic δ = P(H_test=1|H_class=1) − P(H_test=1|H_class=0).
INPUTS:   paired per-anchor H_class, H_test arrays (test window starts at t+1+g; zero shared bars).
OUTPUT:   float δ (off-diagonal-vs-diagonal contrast of the empirical 2×2 transition matrix).
MUST NOT: be read in isolation — raw δ is uninterpretable and never leaves the report without §3.5 subtraction.
```

### G3 — `delta_excess(delta_real, delta_surrogate_by_family) -> float`  (~15 lines)
```text
PURPOSE:  §3.4/§3.5 surrogate-relative read.
INPUTS:   δ_real, and δ for EACH surrogate family (each via the IDENTICAL pipeline).
OUTPUT:   δ_excess = δ_real − δ_surrogate(WORST-CASE = MOST-PERSISTENT member), never the cross-member mean.
FROZEN:   worst-case member; B ≥ 500 paths/cell; frozen seed.
MUST NOT: average over families; report δ_excess without the calibration gates (G5) having passed.
```

### G4 — `measure_L(null_paths, label_fn) -> int`  (~25–40 lines)
```text
PURPOSE:  §3.2 F1 — estimator memory L (NOT q_max).
INPUTS:   matched constant-parameter null paths, the habitat label fn.
OUTPUT:   L = lag at which the classifier-statistic (windowed VR/label) autocorrelation returns to its
          surrogate floor, measured ON THE NULL. L_floor = max(20, max-ACF-lag, 99% IRF decay) is a LOWER bound.
MUST NOT: substitute q_max for L; be tuned to make δ_excess survive (it FEEDS the g-grid, it is not chosen by outcome).
```

### G5 — `calibration_gates(real_series, surrogate_fit) -> dict[str,bool]`  (~30–50 lines)
```text
PURPOSE:  §3.5 F2 hard gates — reject a surrogate fit that cannot bound the conditional floor.
INPUTS:   real series, a fitted surrogate's diagnostics.
OUTPUT:   {gate1..gate4: bool}; ALL must pass for the surrogate to be admissible.
FROZEN:   (1) surrogate reproduces real UNCONDITIONAL label/VR-estimate autocorrelation (transition-floor match);
          (2) GARCH sq-increment ACF ≥ real (reject under-clustering); (3) splice null from ACTUAL roll
          cadence/seam jumps, matched scale (the −0.80 hand-set threshold is RETIRED); (4) periodic null phased
          to the vendor roll calendar.
MUST NOT: pass a surrogate on marginal ACF(1)/half-life match alone (δ is a CONDITIONAL contrast).
```

### G6 — `splice_null(...)` / `periodic_null(...)` in `synthetic.py`  (~30–50 lines each)
```text
PURPOSE:  the 2 missing §3.5 families — ONLY needed when the instrument is a futures leg with rolls.
INPUTS:   raw m1/m2 legs + actual roll cadence/seams (splice); vendor roll calendar (periodic).
OUTPUT:   surrogate price paths run through the IDENTICAL classifier/embargo/extraction.
MUST NOT: invent seam jumps — rebuild from the instrument's real roll record. If the Step-0 real control is a
          cointegrated EQUITY pair (no rolls), G6 is NOT required for Step 0 (build only if/when needed).
```

### G7 — `step0_controls() -> dict`  (~60–100 lines, orchestration)
```text
PURPOSE:  §3.8 positive-control harness; the apparatus-validation verdict.
INPUTS:   synthetic ou()/random_walk()/regime_switch(); ONE pre-committed real daily reverter; G1–G4.
OUTPUT:   {A_confirm, B_zero_rw, B_zero_ou, C_recover, verdict ∈ {PASS, HALT-ARTIFACT, HALT-BLUNT, HALT-LEAK}}.
MUST NOT: shop for a real control that passes (the instrument is pre-committed); soften any control to pass.
```

### G8 — `causal_bitidentity_test() -> bool`  (~25–40 lines, an assertion harness)
```text
PURPOSE:  §3.6 firewall acceptance — detonate a future bar; every classification label + embargo boundary
          must be BIT-IDENTICAL (the doc-19 causal gate).
OUTPUT:   bool. False → leakage → HALT (B2).
MUST NOT: be skipped for "small" changes; it gates trust in every other result.
```

**Total Step-0 build:** one module (`analytics_habitat.py`, G1–G5/G7/G8) ≈ 250–350 lines + optional G6.
Everything else is reuse. This is the whole faithful Step-0 surface.

---

## 3. Step-0 implementation spec (positive-control gate ONLY)

```text
FROZEN INPUTS:
  - synthetic zero-controls:  random_walk(seed=S), ou(lam,sigma,seed=S)   (constant-parameter, NO switching)
  - synthetic power-control:  regime_switch([... MR ↔ non-MR ...], seed=S) with KNOWN switch points
  - ONE real control:         a PRE-COMMITTED, literature-anchored, DAILY, economically-anchored regime-
                              persistent reverter at the RELEVANT SCALE (candidate: a textbook cointegrated
                              pair OR a classic calendar/crack spread with a PUBLISHED MR result). The pick is
                              FROZEN before the run — NOT selected by which one passes (that would be a search).
  - θ + H=1 rule:             FROZEN on the disjoint calibration cohort (B1) before this harness runs.
  - surrogate families:       rw, ou, garch (reuse) [+ splice, periodic ONLY if the real control is a futures leg].
  - B ≥ 500 surrogate paths/cell; frozen seed.

SURROGATE CONSTRUCTION:  reuse surrogate_vr_ensemble's bit-identical pattern — each surrogate path passes
  through the SAME window, SAME classifier, SAME embargo g, SAME test re-measurement, SAME θ. Construction
  artifact cancels ONLY under identical extraction (doc 14 binding guard).

EMBARGO IMPLEMENTATION:  g from the measured-L grid (B3). Classification window ends at t; test window starts
  at t+1+g. ZERO carry-over of estimates / normalization constants / filter state across the embargo. The
  δ_excess(g) sweep is computed and logged (it is the §7 clause-2 kill probe even within Step 0's controls).

LEAKAGE PREVENTION (all must hold, asserted in code):
  - G8 future-injection bit-identity PASSES;
  - test window shares ZERO bars and ZERO rolling state with the classification window;
  - θ is a loaded constant — the code path contains NO optimizer/loop selecting θ by outcome;
  - the label is a function of second-moment quantities only (sign-invariant — assert H unchanged under s→−s).

CALIBRATION GATES (G5):  run the 4 F2 gates on each surrogate family fit; an inadmissible surrogate fit VOIDS
  that family's contribution (and, if it removes the worst-case member, the run is INCONCLUSIVE, not a pass).

EXPECTED PASS/FAIL BEHAVIOR:
  PASS (apparatus validated → proceed to Gate 1):
     (A) δ_excess(real control) > worst-case surrogate band  (CONFIRM a known reverter);
     (B) δ_excess(RW) ≈ 0 AND δ_excess(OU constant-param) ≈ 0  (within band — no manufactured persistence);
     (C) δ_excess(regime_switch) > band, recovering the KNOWN injected persistence  (calibrated power).
  Any other pattern is a NAMED FAILURE (below), not a soft "retry".

LOGGING REQUIREMENTS (every run, append-only, with the frozen-θ hash + seed + cohort id):
  - per control: δ_real, δ per surrogate family, worst-case member id, δ_excess, the surrogate band;
  - the full δ_excess(g) sweep for each control;
  - the G5 gate booleans per family; the G8 bit-identity result;
  - the frozen (θ, H=1-rule hash, seed, B, calibration-cohort id) provenance block;
  - the verdict enum and which clause (A/B/C) drove it. NO continuous "habitat strength" is logged as an output
    field consumable downstream — diagnostics are for the report only (firewall §4).
```

### What would constitute a STEP-0 failure severe enough to HALT the entire initiative?

```text
HALT-LEAK (most severe, immediate):  G8 future-injection bit-identity FAILS. There is lookahead; every result
  is contaminated. Stop all downstream work until the leak is found and B2 re-passes.

HALT-ARTIFACT (fatal to interpretability):  a zero-control prints δ_excess > band — a pure RW or a constant-
  parameter OU shows "persistence". The measurement is an ARTIFACT ENGINE (the doc-19 disease: the apparatus
  manufactures the property). No δ_excess anywhere is interpretable; a future "kill" would be indistinguishable
  from an artifact. RECALIBRATE THE APPARATUS, NOT THE MARKET. Initiative halts until B passes clean.

HALT-BLUNT (fatal to any negative):  (A) the known real reverter FAILS to confirm AND (C) the regime-switch
  control FAILS to recover. The instrument is too blunt to detect persistence that is KNOWN to be present —
  exactly the §11.8 condition under which a kill is meaningless. A negative would be uninterpretable; halt and
  sharpen the apparatus.

NOT initiative-halting (these are ordinary outcomes, NOT Step-0 failures):
  - the eventual real-cohort δ_excess ≤ 0 (that is a legitimate Gate-1 KILL once the apparatus is validated);
  - a single surrogate family rejected by G5 (drop it; re-evaluate worst-case from the admissible set);
  - the materiality hurdle later failing (that is a Gate-2 NON-FINDING, a doctrinally successful stop).
```

---

## 4. State-T firewall audit (treat as a security audit)

Every implementation-level vector by which State T (a per-bar, graded, forward "MR-likely-soon" object that
scales entry) could re-enter, with prohibition + enforcement.

```text
V1  HIDDEN PROBABILITIES / SCORES leaking out of the classifier.
    WHY DANGEROUS: VR(q), p-values, the sub-diffusivity margin, δ are continuous internals; exposing any as a
      "habitat strength" rebuilds the graded channel State T needs.
    PROHIBITION: G1 returns ONLY int{0,1}; continuous internals never become an output field.
    ENFORCEMENT: return-type is int/bool; unit test asserts no float in any eligibility emission; diagnostics
      logged to the REPORT path only, never to a downstream-consumable field.

V2  ELIGIBILITY PERSISTENCE / STREAK leaking conviction.
    WHY DANGEROUS: "eligible 6 periods running" is a covert confidence proxy → graded allocation.
    PROHIBITION: consumer STATELESS; no streak/age/time-since-flip/flip-count/trailing-fraction derivable.
    ENFORCEMENT: the emission is a single current-period enum; unit test that the consumer interface exposes
      no history; hysteresis/dwell state held INTERNAL and never emitted (§4 contract).

V3  THRESHOLD OPTIMIZATION (θ tuned / swept to a desired outcome).
    WHY DANGEROUS: choosing θ by what makes Step 0 or Gate 1 "work" is p-hacking AND manufactures a favorable-now read.
    PROHIBITION: θ frozen ONCE on the disjoint calibration cohort (B1); SINGLE value; no per-cell re-opt.
    ENFORCEMENT: θ is a loaded constant with a logged hash; the code path contains NO optimizer/grid-search over
      θ; a test fails if θ is set from test-set data (leakage guard).

V4  ACCIDENTAL TIMING OUTPUT (δ_excess(h) consumed as a reversion / holding / entry horizon).
    WHY DANGEROUS: renaming "regime half-life" → "expected reversion window" IS State T with a coarser timestamp.
    PROHIBITION: no function maps δ_excess(h) to a trade/entry/holding horizon.
    ENFORCEMENT: interface guard — δ_excess(h) is a report-only descriptor; no downstream consumer takes h as a
      timing input; naming forbids the rename; code review checklist item.

V5  RANKING INSTRUMENTS BY "STRENGTH".
    WHY DANGEROUS: sorting the eligible set by VR/δ magnitude reintroduces graded conviction → sizing.
    PROHIBITION: the eligible set is UNORDERED; equal-weight within set only (Gate 2).
    ENFORCEMENT: book construction takes a SET (membership), never a sorted list; no sort-by-score anywhere;
      test asserts permutation-invariance of the eligible-set consumer.

V6  PARAMETER SEARCH THROUGH ENGINEERING (argmax over the (k,h,g,θ,q) grid).
    WHY DANGEROUS: reporting the best cell is the cardinal §11.1/§11.7 sin and fabricates an edge.
    PROHIBITION: report the FULL search surface; the verdict uses the FWER max-statistic null, never a best cell.
    ENFORCEMENT: the runner iterates the FROZEN grid and emits ALL cells; a guard REFUSES to emit a single
      "best" cell as a verdict; the max-statistic null spans the identical label rule on every surrogate path.

V7  FUTURE LEAKAGE / LOOKAHEAD (shared state across the embargo; contemporaneous normalization).
    WHY DANGEROUS: any future information in the label is undetectable contamination that fakes persistence.
    PROHIBITION: ZERO carry-over of estimates/normalization/filter state across the embargo; classification uses
      only [t−k,t].
    ENFORCEMENT: G8 future-injection bit-identity test (B2) as a hard gate; test windows constructed with zero
      shared bars; no rolling parameter spans the boundary.

V8  SIGN LEAKAGE (label or book conditioning on deviation direction).
    WHY DANGEROUS: a directional read is a price forecast = State T.
    PROHIBITION: the label is a function of second-moment / VR quantities only; consumers sign-symmetric.
    ENFORCEMENT: assert H(s) == H(−s) (sign-invariance unit test); the Gate-2 book allocates to an instrument's
      MR strategy as a whole, never a directional position.
```

**Standing enforcement artifacts** (cheap, build once): a `test_firewall.py` encoding V1/V2/V5/V7/V8 as
assertions; a frozen-provenance log (θ hash + seed + cohort id) on every run; a one-line code-review checklist
(V3/V4/V6) for any change in the habitat path.

---

## 5. Minimal coding roadmap (smallest execution order)

```text
STEP A — habitat_label (G1) + sign-invariance & no-float tests.
   DIFFICULTY: low (compose existing level_vr/compute_acf/adf_kpss_pvalues).
   RUNTIME:    instant.
   FAILURE PTS: ADF/KPSS on short windows (k=60) may be noisy/undefined → handle as label=0, never as lookahead;
                "more sub-diffusive than null" needs the surrogate (Step C) — until then test the deterministic
                Boolean only.
   STOP IF:    H exposes any float; H not sign-invariant. (V1/V8 breach → fix before proceeding.)

STEP B — causal_bitidentity_test (G8).  BUILD EARLY — it gates trust in everything.
   DIFFICULTY: low.   RUNTIME: instant.
   FAILURE PTS: any shared rolling/normalization state across the window boundary.
   STOP IF:    bit-identity fails → HALT-LEAK; do not build further until labels are causally clean.

STEP C — surrogate-relative read on ONE window: transition_delta (G2) + delta_excess (G3) over the
         EXISTING rw/ou/garch ensemble, worst-case member.
   DIFFICULTY: low–medium (G2/G3 tiny; wiring through surrogate_vr_ensemble's pattern is the work).
   RUNTIME:    seconds–minutes per series (B≥500 paths).
   FAILURE PTS: forgetting identical extraction (artifact survives); averaging families instead of worst-case.
   STOP IF:    extraction not bit-identical across real & surrogate (the doc-14 guard).

STEP D — measure_L (G4) + the g-grid; then the δ_excess(g) sweep.
   DIFFICULTY: medium (autocorrelation decay of a windowed estimate series).
   RUNTIME:    minutes (re-runs C across the g-grid).
   FAILURE PTS: L under-measured (g too short → mechanical persistence survives); treat L as LOWER-bounded by
                max(20, max-ACF-lag, 99% IRF decay).
   STOP IF:    L cannot be measured stably on the null → the embargo is unjustified; do not proceed to Step 0.

STEP E — calibration_gates (G5).  [+ G6 splice/periodic ONLY if the real control is a futures leg.]
   DIFFICULTY: medium.   RUNTIME: seconds.
   FAILURE PTS: passing a surrogate on marginal ACF(1) alone (δ is conditional); GARCH under-clustering.
   STOP IF:    no admissible surrogate family remains after gating → INCONCLUSIVE.

STEP F — step0_controls (G7): wire A (real reverter) / B (RW, OU) / C (regime_switch) → verdict + logging.
   DIFFICULTY: medium (orchestration; the pieces exist after A–E).
   RUNTIME:    minutes–tens of minutes (controls × B paths × g-grid).
   FAILURE PTS: see §3 named failures.
   STOP IF:    HALT-LEAK / HALT-ARTIFACT / HALT-BLUNT (initiative halts — recalibrate apparatus, not market).
   PASS →      apparatus validated; B4 clears; Gate 1 on the real cohort becomes authorizable (separate authz).

— HARD STOP HERE FOR STEP 0 —
STEP G (Gate 1 runner) and Gate 2 (binary contract, three-arm books, materiality) are DEFERRED and NOT part of
this Step-0 build. They are specified by doc 28 §3.7/§4/§5/§6 and planned only after Step 0 PASSES.
```

---

## 6. Open decision (surface before STEP 0 execution — NOT blocking this plan)

```text
The §3.8(A) real positive control instrument must be PRE-COMMITTED before Step 0 runs (picking one that passes
= a search = a State-T-adjacent p-hack, V3/V6). This plan does not choose it. Decision required from the lead:
which DAILY, literature-anchored, economically-anchored regime-persistent reverter is the frozen positive
control — a textbook cointegrated pair (no rolls → G6 not needed) or a classic calendar/crack spread (futures →
G6 splice/periodic nulls required). This choice determines whether G6 is in the Step-0 build.
```

## 7. Non-conclusions · next action

```text
NON-CONCLUSIONS: no code exists; the apparatus is unvalidated; nothing about real habitat persistence is
  claimed. This plan commits only to HOW the frozen doc-28 protocol is faithfully executed, minimally.
NEXT ACTION (on authorization): (1) lead pre-commits the §3.8(A) control instrument (§6); (2) freeze θ + the
  H=1 rule on the calibration cohort (B1); (3) implement Steps A→F in order. STEP 0 execution is a SEPARATE
  authorization from this plan.
```
