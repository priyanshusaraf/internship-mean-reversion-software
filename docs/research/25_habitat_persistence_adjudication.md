# 25 — Forward Habitat-State Persistence: Adjudication & Pre-Registration

## Status

```text
DATE:        2026-06-04
MODE:        RESEARCH MODE (CLAUDE.md §3 Mode 1) — adjudication + pre-registration only
DELIVERABLE: VERDICT + leakage-free causal protocol, frozen BEFORE any data is touched
NOT THIS:    empirical run (NOT yet authorized) · code · signal · detector
GOVERNS:     CLAUDE.md §6 (temporal), §11.1 (rolling guard), §11.7 (OOS unit), §11.8 (positive control), §4 (zombie)
SUPERSEDES:  nothing — extends the Arm-A line (docs 18–23); prior MR-Habitat-v2 forward kill is PARTITIONED here
```

This document is pre-registration-grade. The grid, cohort, success and kill criteria in §9 are frozen
on publication. Nothing below may be re-optimized after the data is touched. Any deviation requires a
new dated doc and a §4 reopen justification.

---

## 1. The Exact Question

Does the claim

> "recent MR habitat in [t−k, t]  →  elevated probability of MR habitat in [t+1+g, t+h]"

represent **(1) a circular tautology / mechanical artifact**, or **(2) valid regime persistence** (a
falsifiable property of the data-generating regime, analogous to volatility-clustering / GARCH
persistence / Hamilton p_HH)?

**Load-bearing distinction (frozen).** We test **persistence of HABITAT** — a latent second-moment
regime-state property (is the environment sub-diffusive?) — **NOT** the sign, magnitude, or timing of
the next price move. Forecasting the next price move conditional on a deviation is State T (doc 11,
FALSIFIED-IN-FORM) and is **dead**. This object emits **no tense about price**.

---

## 2. Verdict

```text
VERDICT: EMPIRICALLY-DECIDABLE
         (admissible as posed → reopened as a surrogate-relative, embargoed, economically-gated test;
          NOT a priori valid, NOT a definitional tautology, NOT invalid-as-posed)
```

**Four-lens vote (unanimous):**

| Lens | Vote |
|---|---|
| Quant-econometrician (regime-persistence estimation) | EMPIRICALLY_DECIDABLE |
| Trader / PM (1–12-week book) | EMPIRICALLY_DECIDABLE |
| Statistical adversary (default-to-tautology) | EMPIRICALLY_DECIDABLE |
| Time-series specialist (leakage / estimator memory / surrogate) | EMPIRICALLY_DECIDABLE |

**Decisive reasoning (two repo-anchored facts, not vibes):**

1. **Why it is NOT a priori valid.** Doc 19 proved on synthetic ground truth (HIGH confidence) that a
   slow rolling statistic manufactures the very property it measures (rolling-β-on-levels:
   82–97% β-update-noise, ACF≈0.81, true-VR<1 inflated to VR=6.23). A habitat classifier — VR(q), κ̂,
   ACF, ADF — is exactly such a slow, finite-sample, window-memory-laden statistic. A
   **constant-parameter, no-regime** world WILL print positive δ = P(H_test|H_class) − P(H_test|¬H_class)
   from **(b)** estimator autocorrelation / shared-bar leakage and **(c)** unconditional-stationarity-as-
   common-state, with **zero** regime switching. The raw δ is therefore uninterpretable.

2. **Why it is NOT a definitional tautology.** H_class and H_test are measured on **NON-OVERLAPPING**
   bars by a **single causal classifier** — two independent measurements of a latent regime state,
   asking whether they correlate. That is structurally identical to volatility-clustering / GARCH
   persistence (α+β) and Hamilton p_HH, all falsifiable and non-circular **because** they are read
   against a nested constant-parameter null and concern a regime / second-moment **state**, not the
   realized first-moment path. The estimand — P(environment sub-diffusive in [t+1+g, t+h] | environment
   sub-diffusive in [t−k, t]) — is the **latent-regime transition probability**, not a conditional
   return forecast.

**Therefore tautology-vs-persistence is undecidable by armchair logic and decidable ONLY by the
surrogate.** A matched constant-parameter null run **bit-identically** through classify→embargo→test
cancels (b)+(c) by construction; real-minus-surrogate isolates (a) true regime persistence. Doc 23
supplies the confirming asymmetry: genuine storage MR selectively switched **OFF** in glut years — an
artifact has no reason to respect the fundamental calendar. That regime-conditionality signature is the
independent corroborant of (a) vs (b)/(c).

The protocol is the decider. It is admissible **only** in the form specified in §6, after the six
mandatory fixes (§7) are carried. Absent that form it reverts to the prior kill's backward-only
description.

---

## 3. Disposition of the Prior Adversary Kill — PARTITION

The prior MR-Habitat-v2 redesign adversary KILLED "conditional prior of FUTURE MR" as a State-T
tautology and forced the object backward-only. **Disposition: PARTITION (uphold half, overturn half).**
All four lenses concur.

```text
UPHELD  (stays dead): forward PRICE-REVERSAL prediction — sign / magnitude / timing of the next move
        conditional on a deviation, |z|≥θ pre-window anchoring, "reverse-now / favorable-now."
        This IS State T (doc 11, FALSIFIED-IN-FORM). Nothing here resurrects it.

OVERTURNED (reopened): forward HABITAT-STATE persistence — the transition probability of a latent
        second-moment regime, emitting NO tense about price. A distinct, falsifiable estimand. The
        prior kill OVER-REACHED by ruling it "State-T tautology with a coarser timestamp."
```

**The precise line.** The admissible object emits a **current habitat-STATE label** for capital
allocation / universe tilt — "tilt limited capital toward instruments currently MEASURING as MR-friendly"
(the standard stat-arb universe-rebalance premise). The forbidden object emits a **price-direction /
timing read** — "this instrument will revert now." The label carries **no sign**; the moment any output
conditions a trade on direction or emits a tense about the next price move, it is State-T resurrection
(§4 zombie prohibition).

**What the prior kill got RIGHT (preserved as binding danger).** The naive forward-conditional read
**is** mechanically contaminated — the doc-19 β-noise mechanism generalized to the habitat label itself.
The kill correctly identified the **MECHANISM** (slow-statistic autocorrelation manufacturing
persistence) but **mis-classified its problem class**: it called STRUCTURAL (definitional circularity)
what is actually MEASUREMENT/leakage (defeatable by surrogate + embargo), sitting beside a genuinely
falsifiable regime-state object. Correct partition; corrected class.

---

## 4. Three-Source Decomposition

Apparent persistence (δ > 0) can arise from three sources that the design must separate:

```text
(a) TRUE regime persistence    — the interesting, falsifiable claim (latent-state transition prob)
(b) MECHANICAL estimator       — slow-statistic finite-sample autocorrelation + shared-bar / kernel
    autocorrelation              leakage; manufactures δ>0 in a CONSTANT-parameter world (doc 19)
(c) STRUCTURAL artifact        — unconditional stationarity makes "habitat" the trivial common state;
                                  every window samples it; vol-clustering local-variance regimes persist
```

**How the design separates them:**

- **(b)+(c) cancel by construction** when a matched constant-parameter null (which contains b and c by
  definition, having NO regime switching) is run **bit-identically** through the same
  classifier→embargo→test→statistic pipeline. The surrogate's δ-distribution IS the (b)+(c) floor.
- **(a) is isolated** as δ_excess = δ_real − δ_surrogate, read only as excess over the surrogate band.
- **Independent corroborant of (a):** economic regime-conditionality (doc 23) — does habitat switch
  **off** for an identifiable fundamental reason (glut years)? **Uniform** persistence across all regimes
  is a RED FLAG for (b)/(c), not a green flag; an artifact has no reason to respect the fundamental
  calendar.
- **The embargo-sensitivity sweep δ_excess(g) is the single most diagnostic output:** if δ_excess
  decays into the surrogate band as g grows past estimator memory L, the persistence was (b) → KILL; if
  it survives at g ≫ L, it is (a).

---

## 5. Mandatory Fixes from Adversarial Stress-Test (all carried)

The stress-test produced six mandatory fixes; all are incorporated into §6. Summary of disposition:

| # | Fix | Disposition |
|---|---|---|
| F1 | **Embargo re-derivation.** L = empirically-measured decay length of the CLASSIFIER-STATISTIC autocorrelation (lag at which corr(H_class,H_test) returns to its surrogate floor on the matched null), **NOT** kernel width q_max. The near-unit-root half-life of the level governs this and is potentially ≫ q_max and unidentifiable in-sample, so g on L=q_max can be an order of magnitude too short. | **CARRIED** — §6.2 |
| F2 | **Conditional-floor surrogate calibration.** Match the surrogate to the real series' **unconditional LABEL/VR-estimate autocorrelation** (the quantity δ is built from), not only marginal ACF(1)/half-life/sq-increment-ACF. δ_excess must clear the **WORST-CASE (most-persistent)** surrogate member, never the cross-member mean. HARD gate: GARCH sq-increment ACF ≥ real sq-increment ACF (reject under-clustering fits). | **CARRIED** — §6.4 |
| F3 | **Disjoint θ/q-rule freeze.** Freeze θ and the full H=1 conjunction rule on a **CALIBRATION epoch/cohort contributing ZERO observations** to the δ_excess test set; audit the label as a fixed deterministic bit-identical function across real and every surrogate path (no per-cell/per-q re-optimization). Closes the θ-as-argmax leak. | **CARRIED** — §6.1, §6.5 |
| F4 | **Splice null at true seam scale + periodic null.** Build the splice/back-adjustment null from each instrument's **actual** contract-roll cadence and realized seam jumps (rebuild from raw legs where feasible); **add a roll-cadence-phased PERIODIC null** to the family (absorbs the doc-23 (3,5,3,5) regularity). δ_excess must clear the splice anchor at **matched scale** — retire the hand-set −0.80 threshold. | **CARRIED** — §6.4 |
| F5 | **Direction-free economic gate.** Replace any z-entry/deviation-anchored trade proxy with a pure **universe-tilt capital-allocation aggregate** (habitat-tilted vs equal-weight book, fixed rebalance clock, **sign-symmetric**, no deviation entry). Interface guard forbids any downstream consumer mapping the label or δ_excess(h) to entry timing/direction/holding-horizon. | **CARRIED** — §6.6, §6.8 |
| F6 | **Matched-scale real positive control (§11.8).** Before any δ_excess≤0 is a credible kill, require the apparatus to CONFIRM a known literature-anchored **DAILY** regime-persistent reverter at the relevant scale (Brent hourly is off-scale, doc 23) AND simultaneously print δ_excess≈0 on pure RW / single-regime OU. An un-power-validated kill is INCONCLUSIVE → recalibrate apparatus, not market. | **CARRIED** — §6.7 |

No fix is waived. F1 and F2 are decisive: unfixed, each alone would let mechanical estimator-
autocorrelation persistence be reported as genuine.

---

## 6. Leakage-Free Causal Protocol (frozen)

### 6.1 Classifier on [t−k, t]

Single causal **binary** habitat label H ∈ {0,1}, computed on [t−k, t] using **only** information
available at t, applied **identically and independently** in the test window.

```text
H = 1  iff  a pre-registered CONJUNCTION of κ̂-free SECOND-MOMENT diagnostics holds:
  (i)   level-difference VR(q) = Var(S_t − S_{t−q}) / (q · Var(ΔS)) < 1  on a frozen q-grid
        q ∈ {2, 5, 10, 20}   (doc 18a/19 ratified estimator — NOT rolling-β-on-levels, which is
        doc-19 INADMISSIBLE because it manufactures the property), AND
  (ii)  return ACF bounded/negative within a frozen band, AND
  (iii) stationarity (ADF AND KPSS) on a FROZEN reference.
```

**Non-negotiable cuts:**

- **(a) habitat is a DIFFUSIVITY / second-moment property** — it is **never** defined using the realized
  first-moment reversion of the same path later tested. (That is the literal MR-defines-MR circularity.)
- **(b) NO smoother / Kalman / rolling-β state enters the label** (κ̂-free, smoother-free). Slow recursive
  state is the doc-19 artifact engine.

**Discrimination requirement (statistical-adversary win).** A stationary null is **always** "in habitat,"
so a label that merely detects VR<1 / stationarity saturates under the null (P(H)≈1), δ degenerates,
zero discriminating power. Therefore **H=1 means "more sub-diffusive than the matched constant-parameter
null at threshold θ," NOT "stationary."** The label must demonstrably separate real from matched-stationary-
surrogate at classification time.

**θ / q-rule freeze (F3).** θ and the **full** H=1 conjunction rule (how the four q's + ACF + ADF/KPSS
combine — a fixed deterministic Boolean) are frozen on a **disjoint calibration cohort/epoch** (§9.3)
that contributes **zero** observations to the δ_excess test set. **No** per-cell or per-q re-optimization.
The label is audited bit-identical across real and every surrogate path.

### 6.2 Embargo g (justified vs estimator memory) — F1

Embargo g inserted between classification-window end (t) and test-window start (t+1+g), pre-registered
**per classifier** and justified against **measured** estimator memory L — never by convention.

```text
L is NOT q_max.  L = the empirically-measured decay length of the CLASSIFIER-STATISTIC autocorrelation:
    L = the lag at which corr(H_class, H_test)  [equivalently corr of the underlying VR/κ̂ estimate series]
        returns to its surrogate floor, measured ON THE MATCHED CONSTANT-PARAMETER NULL.
```

**Why kernel width is insufficient (the decisive F1 point).** VR(q) and local ACF are estimated on k
bars of a near-unit-root process; the **sampling distribution** of those estimates is serially correlated
at lags **far exceeding** q_max, because adjacent k-windows share the same realized low-frequency OU
excursions (doc 14 §2.1–2.3: half-life CI unbounded-above; flat likelihood). The decay length of THAT
autocorrelation is governed by the OU half-life of the level — tens to hundreds of bars, unidentifiable
in-sample. So g = ceil(q_max) can be an order of magnitude too short. **L is measured empirically on the
surrogate, not assumed.**

```text
Rule:  g ≥ ceil(L) × safety multiple (≥ 1.5),  with L the measured classifier-statistic decay length.
       L_floor = max( q_max=20 , max-ACF-lag , 99% IRF decay of any residual component )  — a LOWER bound only.
       Carry-over guard: ZERO carry-over of class-window estimates / normalization constants / filter
       state across the embargo. β / μ* (if used anywhere downstream) re-estimated independently in the
       test window. No shared rolling parameter spans the boundary.
```

**Embargo-sensitivity sweep δ_excess(g)** is the single most diagnostic output and a falsification probe:
if δ_excess decays into the surrogate band as g grows past L → mechanical (confound b) → **KILL**; if it
survives at g ≫ L → regime-genuine.

### 6.3 Test window [t+1+g, t+h]

Re-run the **same** causal classifier on the **disjoint** bars [t+1+g, t+h] to obtain H_test,
independently. Zero shared bars with [t−k, t]; zero shared rolling-parameter / normalization state; no
carried filter state across the embargo. h is varied on the pre-registered grid (§9) to produce the
horizon-resolved decay curve.

### 6.4 Persistence statistic & surrogate protocol

**Primary statistic.**

```text
δ = P(H_test = 1 | H_class = 1) − P(H_test = 1 | H_class = 0)
    — the off-diagonal-vs-diagonal contrast of the empirical 2×2 habitat transition matrix
    (equivalently the dominant-eigenvalue persistence read of that matrix).
```

**Read STRICTLY as real-minus-surrogate:**

```text
δ_excess = δ_real − δ_surrogate
```

with **serial-dependence-robust** CI (block bootstrap / Newey-West, block length ≥ L — naive binomial
SEs are anti-conservative because adjacent t-anchored observations are dependent). Horizon-resolved:
δ_excess(h) reported as a function of h (the regime-label half-life / decay curve), per the trader's need
for the half-life, not a point.

**Surrogate families (each run BIT-IDENTICALLY through the same classifier, same [t−k,t] window, same
embargo g, same [t+1+g,t+h] re-measurement, same θ and label rule — construction artifact cancels only
if extraction is identical, doc 14 binding guard):**

```text
{ OU (single FIXED κ,θ,σ — NO regime switching),
  RW,
  GARCH(1,1) — NO regime switching,
  SPLICE / back-adjustment null  — MANDATORY for futures legs,
  PERIODIC roll-cadence-phased null }                                      (F4)
```

**Calibration audit — CONDITIONAL FLOOR (F2, decisive).** δ is a **conditional** 2×2 transition
contrast — a property of the **joint** law of two windowed estimates, not of the marginal ACF. Two DGPs
can share ACF(1) and unconditional half-life yet differ in the transition off-diagonal. Therefore the
calibration target must include the **conditional-floor generator directly**:

```text
HARD calibration gates (reject any surrogate fit that fails):
  (1) surrogate reproduces the real series' UNCONDITIONAL LABEL/VR-ESTIMATE AUTOCORRELATION
      (the quantity δ is built from) — the "transition-floor match," not just marginal ACF(1)/half-life;
  (2) GARCH sq-increment ACF ≥ real sq-increment ACF  (doc 19 measured real ~0.44; reject UNDER-clustering
      fits — an under-persistent GARCH understates the (c) floor and hands a false positive);
  (3) splice null built from each instrument's ACTUAL roll cadence & realized seam jumps (rebuild from
      raw m1/m2 legs where feasible); δ_excess must clear the splice anchor at MATCHED scale — the
      hand-set −0.80 threshold (doc 23) is RETIRED;
  (4) periodic null phased to the vendor roll calendar to absorb the doc-23 (3,5,3,5) regularity.
```

**Worst-case reading (F2).** δ_excess must clear the **WORST-CASE (most-persistent) surrogate member**,
**never** the cross-member mean. B ≥ 500 paths per cell; frozen seed. The raw δ_real is **uninterpretable**
and never leaves the report without its matched-null subtracted.

### 6.5 Multiplicity control & pre-registered grid

```text
Pre-register the FULL (k, h, g, θ, q-grid) grid AND the instrument cohort BEFORE any run; freeze seed.
Report the ENTIRE search-surface distribution of δ_excess — NEVER the argmax cell (§11.7; argmax-only
= grounds for rejection).
Multiplicity: ONE pre-registered FWER/FDR rule over grid × instruments. Build a MAX-STATISTIC null by
running the IDENTICAL grid on EACH surrogate path, so the per-cell surrogate band PLUS the family-wise
correction jointly absorb the inflation. The H=1 conjunction is a fixed deterministic function with NO
per-cell/per-q re-optimization (F3) — confirm the max-statistic null spans the SAME label rule on every
surrogate path. Report full search, the argmax, AND the corrected verdict.
```

### 6.6 Cross-habitat OOS replication — the unit of evidence

```text
δ_excess must survive on ≥ 2–3 INDEPENDENT instruments AND disjoint epochs that did NOT inform the
pre-registration. A single-instrument / single-epoch positive is INCONCLUSIVE / DEFERRED — NEVER
confirmation (§11.7). Local survivability = persistence across MULTIPLE DISJOINT windows (doc 23: pooled
across 19 disjoint years with a 14/19 binomial, not one favorable window). The cherry-picked favorable
(k,h,g,θ) cell is the cardinal sin of this ontology (§11.1).
```

### 6.7 §11.8 positive-control gate — F6

```text
Before any δ_excess ≤ 0 is a credible kill, the apparatus must SIMULTANEOUSLY:
  (A) CONFIRM habitat persistence (δ_excess > band) on a known, literature-anchored, DAILY,
      economically-anchored regime-persistent reverter at the RELEVANT SCALE (Brent hourly is
      off-scale — doc 23 — and does not satisfy this); AND
  (B) print δ_excess ≈ 0 (within band) on a pure RW and on a single-regime constant-parameter OU
      (the zero-controls); AND
  (C) RECOVER known persistence above band on a synthetic Markov regime-switching series with a
      known MR↔non-MR switch (calibrated power).
A kill from an apparatus failing (A)/(B)/(C) is INCONCLUSIVE → recalibrate apparatus, not market
(doc 19 instrument-defect precedent).
```

### 6.8 State-T firewall

```text
The object emits ONLY a current habitat-STATE label  P(habitat-state | habitat-state)  for
capital-allocation / universe-tilt. It NEVER emits a price direction, magnitude, reversion timing,
|z| pre-window, or "reverse-now / favorable-now" read.

Banned vocabulary enforced:  T-score · hazard · ignition · imminent · favorable-now.

Direction-free guarantees (F5):
  - the label emits NO SIGN; any capital-tilt consumer is SIGN-SYMMETRIC (allocates capacity to the
    instrument's MR-strategy as a whole, never a directional position);
  - δ_excess(h) is a latent-regime-state half-life descriptor — an INTERFACE GUARD forbids any
    downstream object consuming it as a holding / entry / reversion horizon (the rename
    "regime half-life → expected reversion window" is the banned read with a coarser timestamp);
  - the economic gate (§6.6 below / §8) is a PURE universe-tilt aggregate — NO z-entry, NO deviation
    anchoring, NO per-trade timing proxy (the doc-23 z-entry proxy is the primary firewall-creep vector
    and is excluded).

Firewall acceptance test: future-injection bit-identity — detonate a future bar; every classification-
window label and every embargo boundary must be bit-identical (the doc-19 causal gate). Any classifier
output that conditions a trade on direction, or any read tense about the next price move, is State-T
resurrection (doc 11, §4 zombie prohibition) and requires a NEW independent pre-registration passing the
§4 zombie-reopen test.
```

---

## 7. Falsification / Kill Trigger (frozen)

Forward habitat persistence is declared **ABSENT** and the object **reverts to backward-only description**
if **ANY** of:

```text
(1) δ_excess CI overlaps zero / does not exceed the upper (worst-case) surrogate band after FWER
    correction across the pre-registered grid and the named cross-habitat cohort  (H0 not rejected);
(2) the embargo-sensitivity sweep shows δ_excess DECAYS into the surrogate band as g grows past
    estimator memory L  (confound-b proven — mechanical);
(3) δ_excess fails cross-habitat OOS replication (appears in one instrument/epoch only)  → INCONCLUSIVE,
    never confirmation;
(4) TRADER ECONOMIC GATE: δ_excess is statistically positive but the net-of-cost capital-allocation lift
    (after turnover, transaction cost, borrow, capacity, sizing, drawdown) of a SIGN-SYMMETRIC universe
    tilt toward currently-MR instruments fails to beat equal-weight by the book's minimum threshold, OR
    the regime half-life h is too short for a 1–12-week book  → real-but-tiny / short-lived edge is a
    NON-FINDING and killed;
(5) INSTRUMENT-DEFECT branch (doc-19 precedent): if the §11.8 controls (§6.7) fail — constant-parameter
    OU/RW positive control itself prints non-zero δ_excess (apparatus manufactures persistence) OR the
    regime-switching control fails to recover known persistence OR the matched-scale real reverter fails
    to confirm — verdict is INCONCLUSIVE and the APPARATUS is recalibrated, NOT the market declared null.
```

H0 (frozen): δ_excess ≤ 0 across the pre-registered grid and ≥ N_min independent instruments — no regime
persistence beyond the mechanical floor a constant-parameter world manufactures. H1: δ_excess > 0,
exceeding the upper worst-case surrogate band on M-of-N disjoint windows, binomially significant (doc 23
14/19 template). The falsifiable statement is a property of the **DGP regime** (latent-state transition),
explicitly **NOT** of returns.

---

## 8. Economic Gate (direction-free) — F5 detail

```text
Construction: build TWO books on a FIXED rebalance clock (e.g. weekly/biweekly, pre-registered):
  - EQUAL-WEIGHT book over the instrument universe;
  - HABITAT-TILTED book — capacity tilted toward instruments whose CURRENT causal habitat label H=1,
    SIGN-SYMMETRIC (allocates to the instrument's MR strategy as a whole; emits no directional position
    and no entry timing).
Metric: net-of-cost portfolio-AGGREGATE lift (after turnover/tcost/borrow/capacity/sizing/drawdown) of
        the tilted book over equal-weight. NO z-entry, NO deviation anchoring, NO per-trade proxy.
Pass: lift ≥ book minimum threshold AND regime half-life adequate for a 1–12-week horizon.
The deployable object is a BOOK, not an instrument (§11.2). A statistically real but uneconomic edge is
a NON-FINDING.
```

---

## 9. Pre-Registration Block (FROZEN before any data is touched)

### 9.1 Frozen (k, h, g, θ, q) grid

```text
k  (classification window, bars):     {60, 120, 250}
h  (test window length, bars):        {20, 40, 60, 120}        — horizon-resolved decay curve
g  (embargo, bars):                   {ceil(L), 2·ceil(L), 4·ceil(L), 8·ceil(L)}  where L is MEASURED
                                      per-classifier on the matched null (F1); the sweep over g IS the
                                      decay-probe falsification (§7 clause 2). L_floor = max(20, max-ACF-
                                      lag, 99% IRF decay) is a LOWER bound; the binding g uses measured L.
θ  (habitat sub-diffusivity threshold): frozen on the DISJOINT calibration cohort (§9.3) as the cut that
                                      separates real from matched-stationary-surrogate at classification
                                      time; SINGLE frozen value, no per-cell re-optimization.
q-grid (VR aggregation horizons):     {2, 5, 10, 20}  (frozen)
H=1 conjunction rule:                 fixed deterministic Boolean over {VR(q)<1 ∀q in band} ∧ {ACF in band}
                                      ∧ {ADF ∧ KPSS pass}, frozen on calibration cohort; bit-identical on
                                      every surrogate path.
Surrogates per cell B:                ≥ 500;  frozen seed.
Surrogate families:                   {OU(fixed), RW, GARCH(1,1) no-switch, SPLICE(true-seam), PERIODIC(roll-cadence)}
δ_excess read:                        vs WORST-CASE (most-persistent) surrogate member.
```

### 9.2 Instruments / epochs cohort

```text
Test cohort (δ_excess test set — NO observation informs θ or the label rule):
  - the Arm-A TRUSTED legs / reconstructible spreads (46 legs, §11.7) spanning ≥ 2–3 INDEPENDENT
    instruments and disjoint epochs;
  - includes the NG calendar (doc 21/23 CONDITIONAL-SURVIVAL anchor) AND ≥ 2 instruments from a
    DIFFERENT habitat family (cross-asset / different roll structure) for genuine cross-habitat OOS.
Replication unit (§11.7): "survives across independent habitats," NOT "appears in one." Single-instrument
  positive = INCONCLUSIVE.
```

### 9.3 Disjoint calibration cohort (F3)

```text
A separate epoch/cohort, contributing ZERO observations to the δ_excess test set, on which θ and the
H=1 conjunction rule are frozen. Specified and locked BEFORE the test data is touched. Any leakage of
the test epoch into θ-selection voids the run.
```

### 9.4 Success & kill criteria (frozen)

```text
SUCCESS (CONDITIONAL SURVIVAL → freeze as a named, conditioned object):
  δ_excess > upper worst-case surrogate band, FWER-corrected, on M-of-N disjoint windows AND on
  ≥ 2 independent instruments/epochs, with δ_excess(g) PERSISTING at g ≫ L (no decay), AND the
  direction-free economic gate clearing the book threshold at a 1–12-week-adequate half-life.
  → Conditional survival names its condition (which instruments/regimes) and a pre-registered kill
    trigger for OOS failure (§11.3).

KILL (revert to backward-only description): any of §7 clauses (1)–(4).

INCONCLUSIVE (recalibrate apparatus, not market): §7 clause (5) — any §11.8 control failure.
```

---

## 10. Surviving Uncertainty · Explicit Non-Conclusions · Next Action

**Confidence (trustworthiness of the design, not of any result):** MEDIUM-HIGH that the protocol is
leakage-free **after** F1–F6; the decisive residual risks are F1 (measured-L embargo) and F2 (conditional-
floor surrogate) executing correctly in code.

**Surviving uncertainty:**

```text
- Whether the empirically-measured classifier-statistic memory L (F1) is finite/identifiable enough on
  near-unit-root real legs to set a g that is both leakage-safe AND leaves usable sample — a too-long L
  may starve the test (a real risk, not a flaw).
- Whether any surrogate member can fully reproduce the CONDITIONAL δ-floor (F2); the worst-case read is
  the guard, but an unmodeled higher-order dependence could still understate it.
- Whether a matched-scale (daily) literature-anchored real positive control (F6) exists in the cohort;
  if not, a kill is not yet credible and the verdict on a null is INCONCLUSIVE.
- Splice/(3,5,3,5)-periodic null adequacy remains the doc-23 inherited open item until built at true
  seam scale.
```

**Explicit non-conclusions:**

```text
- This document does NOT conclude that forward habitat persistence EXISTS. It rules it DECIDABLE and
  frozen the test.
- It does NOT authorize any empirical run, any code, any detector, any signal, any tilt deployment.
- It does NOT relax the State-T firewall: forward price-reversal prediction remains DEAD.
- A single-instrument positive, should one appear, is explicitly NOT confirmation.
```

**Next highest-information empirical action (the actual run, pending authorization):**

```text
STEP 0 (instrument check, BLOCKING for the kill-credibility branch): identify whether a matched-scale
        DAILY literature-anchored regime-persistent reverter exists in the cohort (F6). If not, surface
        it as a blocker before any negative verdict.
STEP 1: on the DISJOINT calibration cohort, freeze θ + the H=1 conjunction rule (F3); confirm the label
        SEPARATES real from matched-stationary-surrogate at classification (discrimination requirement).
STEP 2: measure L (classifier-statistic autocorrelation decay) per classifier on the matched null (F1);
        set the g-grid from measured L.
STEP 3: run the §11.8 controls (§6.7): zero-controls (RW, single-regime OU → δ_excess≈0) and the
        regime-switching power control (→ recover δ_excess>band). If they fail → INCONCLUSIVE, fix
        apparatus, stop.
STEP 4: only then, run the frozen grid on the test cohort, surrogate-relative (worst-case member),
        FWER-corrected, reporting the FULL search surface; produce δ_excess(g) decay sweep and
        δ_excess(h) horizon curve; apply the direction-free economic gate.
STEP 5: cross-habitat OOS adjudication (≥ 2–3 independent instruments/epochs) → FREEZE /
        CONDITIONAL-SURVIVAL / KILL / INCONCLUSIVE per §9.4. Record in HYPOTHESIS_REGISTRY.md.
```

---

*End of doc 25. Pre-registration frozen 2026-06-04. Empirical run not yet authorized.*
