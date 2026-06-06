# 28 — Forward Habitat-State Persistence: COMBINED PRE-REGISTRATION (freeze-ready)

## Status

```text
DATE:            2026-06-04
MODE:            RESEARCH MODE — freeze-ready pre-registration artifact.
AUTHORIZATION:   NO empirical execution authorized. NO data touched. STEP 0 is NOT run by this document.
ROLE:            Consolidates and SUPERSEDES the operative clauses of docs 25 (statistical), 26 (economic),
                 27 (binary + materiality) into ONE frozen pre-registration to authorize against.
SUPERSESSION:    The continuous habitat SCORE / WEIGHT / capacity-TILT channel of docs 25 §8 and 26 is
                 RETIRED for v1. v1 emits a BINARY eligibility enum only (doc 27). Weighting is DEFERRED —
                 reopenable ONLY after binary gating independently proves OOS value (§11.3 staged deployment).
FREEZE SEMANTICS: Every value in a "FROZEN" block becomes a §6 frozen invariant on fold-in. Changing any
                 of them after freeze is a FREEZE-BREAK requiring explicit justification + authorization
                 (CLAUDE.md §6). Pre-commitment is the point: it removes post-hoc goalpost-moving (§11.7).
```

This document is the single object an authorization decision is made against. It does not itself authorize
the run; it makes the run *authorizable* by fixing every degree of freedom in advance.

---

## 1. The object and the settled verdict chain (do NOT relitigate)

**Object.** Forward **habitat-state persistence**: a sign-free latent *second-moment* (diffusivity) regime
transition probability. For a causal habitat label `H ∈ {0,1}` measured on `[t−k, t]`, the estimand is
`P(H_test=1 | H_class=1) − P(H_test=1 | H_class=0)`, read strictly surrogate-relative as
`δ_excess = δ_real − δ_surrogate`. It is **not** a price-direction, magnitude, or reversion-timing forecast.

**Settled (prior docs — binding, not reopened here):**

| Doc | Gate | Verdict |
|-----|------|---------|
| 25 | Statistical admissibility | **EMPIRICALLY_DECIDABLE.** Not a tautology (`H_class`/`H_test` are two independent measurements of a latent state on non-overlapping bars — structurally GARCH-persistence / Hamilton `p_HH`), not a priori valid (slow estimators manufacture `δ>0` in a constant-parameter world). Prior State-T kill **PARTITIONED**: forward *price-reversal* prediction stays dead; forward *habitat-state* persistence is the reopened, distinct estimand. |
| 26 | Economic meaningfulness | **ECONOMICALLY_USEFUL_IF.** Descriptor ≠ payoff; the only admissible decision is book-level universe membership; strongest falsifier is *no incremental value over a cheap baseline*; firewall = output-type lock. |
| 27 | Binary + materiality tightening | **ECONOMICALLY_USEFUL_IF** (verdict type = decidable conditional), realistic prior ≈ **20–40%** of clearing the hurdle; modal expected outcome = a clean NON-FINDING (a doctrinally successful stop, §11.3). Zombie risk **LOW** under the binary type-lock. |

**Frozen hypothesis.**

```text
H0:  δ_excess ≤ 0 across the pre-registered grid and ≥ N_min independent instruments — no regime
     persistence beyond the mechanical floor a constant-parameter world manufactures.
H1:  δ_excess > 0, exceeding the upper WORST-CASE surrogate band on M-of-N disjoint windows, binomially
     significant (doc 23 14/19 template), AND the binary-gated economic materiality hurdle (§5) clears.
The falsifiable statement is a property of the DGP REGIME (latent-state transition), explicitly NOT of returns.
```

---

## 2. Two-gate structure (+ standing precondition)

```text
PRECONDITION (§11.8 positive-control gate, F6) — standing, must hold for ANY verdict to be credible.
GATE 1  — STATISTICAL  (doc 25): is δ_excess > worst-case surrogate band, leakage-free, cross-habitat OOS?
GATE 2  — ECONOMIC     (doc 27): does the BINARY eligibility gate clear the materiality hurdle vs a cheap baseline?
VERDICT order: PRECONDITION → GATE 1 → GATE 2. A fail at any stage is terminal for that cycle (kill/inconclusive).
```

A statistical pass that fails Gate 2 is a **NON-FINDING**, not a partial success. A Gate-1 fail under a
*failing* precondition is **INCONCLUSIVE** (recalibrate apparatus, not market) — never a market kill.

---

## 3. FROZEN STATISTICAL PROTOCOL (Gate 1 — folds doc 25 §6 + §9)

### 3.1 Classifier on `[t−k, t]`

```text
H = 1  iff a pre-registered, κ̂-free, smoother-free CONJUNCTION of SECOND-MOMENT diagnostics holds:
  (i)   level-difference VR(q) = Var(S_t − S_{t−q}) / (q·Var(ΔS)) < 1  on frozen q ∈ {2,5,10,20}
        (doc 18a/19 ratified estimator — NOT rolling-β-on-levels, which is doc-19 INADMISSIBLE), AND
  (ii)  return ACF bounded/negative within a frozen band, AND
  (iii) stationarity (ADF AND KPSS) on a FROZEN reference.
SEMANTICS: H=1 means "MORE sub-diffusive than the matched constant-parameter null at threshold θ",
           NOT "stationary" (a stationary null is always in-habitat → label would saturate, δ degenerate).
CUTS: (a) habitat is a DIFFUSIVITY/second-moment property, NEVER defined via the realized first-moment
      reversion of the same path later tested (that is the literal circularity). (b) NO smoother/Kalman/
      rolling-β state enters the label.
```

### 3.2 Embargo `g` (F1 — measured, not conventional)

```text
g inserted between class-window end (t) and test-window start (t+1+g), justified per classifier against
MEASURED estimator memory L (NOT kernel width q_max):
  L = decay length of the CLASSIFIER-STATISTIC autocorrelation, measured ON THE MATCHED NULL (the lag at
      which the windowed VR/κ̂ estimate-series autocorrelation returns to its surrogate floor).
  Rationale: adjacent k-windows share the same low-frequency OU excursions, so the estimate sampling
      distribution is serially correlated at lags ≫ q_max (doc 14 §2.1–2.3). g=ceil(q_max) can be an order
      of magnitude too short.
  Rule:  g ≥ ceil(L) × safety multiple (≥1.5).  L_floor = max(20, max-ACF-lag, 99% IRF decay) is a LOWER
      bound only; the binding g uses MEASURED L.
  Carry-over guard: ZERO carry-over of class-window estimates / normalization constants / filter state
      across the embargo; any downstream β/μ* re-estimated independently in the test window.
EMBARGO-SENSITIVITY SWEEP δ_excess(g) is the single most diagnostic output AND a kill probe:
  decays into the surrogate band as g grows past L  → mechanical (confound-b) → KILL;
  survives at g ≫ L                                 → regime-genuine.
```

### 3.3 Test window `[t+1+g, t+h]`

Re-run the **same** causal classifier on the **disjoint** bars to obtain `H_test`, independently. Zero
shared bars, zero shared rolling-parameter/normalization state, no carried filter state across the embargo.
`h` is varied on the grid (§3.7) to produce the horizon-resolved decay curve.

### 3.4 Persistence statistic

```text
δ = P(H_test=1 | H_class=1) − P(H_test=1 | H_class=0)
    (off-diagonal-vs-diagonal contrast of the empirical 2×2 habitat transition matrix).
READ STRICTLY:  δ_excess = δ_real − δ_surrogate,  with serial-dependence-robust CI (block bootstrap /
    Newey–West, block ≥ L; naive binomial SEs are anti-conservative). Horizon-resolved: δ_excess(h) is the
    regime-label half-life decay curve (the trader needs the half-life, not a point). Raw δ_real is
    UNINTERPRETABLE and never leaves the report without its matched null subtracted.
```

### 3.5 Surrogate families + calibration gates (F2, F4)

```text
Families (each run BIT-IDENTICALLY through the same classifier/window/embargo/θ/rule — artifact cancels
only under identical extraction):
  { OU(single FIXED κ,θ,σ — no switching), RW, GARCH(1,1) no-switch,
    SPLICE/back-adjustment null (MANDATORY for futures legs), PERIODIC roll-cadence-phased null }.
HARD calibration gates (reject any surrogate fit failing):
  (1) reproduces the real series' UNCONDITIONAL LABEL/VR-ESTIMATE AUTOCORRELATION (transition-floor match,
      not just marginal ACF(1)/half-life — δ is a CONDITIONAL contrast);
  (2) GARCH sq-increment ACF ≥ real (doc 19 real ~0.44; reject UNDER-clustering fits);
  (3) splice null built from each instrument's ACTUAL roll cadence & realized seam jumps (rebuild from raw
      m1/m2 legs where feasible); the hand-set −0.80 threshold (doc 23) is RETIRED;
  (4) periodic null phased to the vendor roll calendar (absorbs the doc-23 (3,5,3,5) regularity).
WORST-CASE READ: δ_excess must clear the MOST-PERSISTENT surrogate member, NEVER the cross-member mean.
                 B ≥ 500 paths per cell; frozen seed.
```

### 3.6 Multiplicity, cross-habitat OOS, firewall

```text
MULTIPLICITY: pre-register the FULL grid + cohort; report the ENTIRE search-surface distribution, NEVER the
   argmax (argmax-only = grounds for rejection, §11.7). ONE FWER/FDR rule over grid × instruments via a
   MAX-STATISTIC null (identical grid on each surrogate path). Report full search, argmax, AND corrected verdict.
CROSS-HABITAT OOS (the unit of evidence): δ_excess must survive on ≥2–3 INDEPENDENT instruments AND disjoint
   epochs that did NOT inform the pre-registration. Single-instrument/epoch positive = INCONCLUSIVE, never
   confirmation. Local survivability = persistence across MULTIPLE disjoint windows (doc 23 14/19 template).
STATE-T FIREWALL: the object emits ONLY a current habitat-STATE label for universe-tilt — never a price
   direction, magnitude, reversion timing, |z| pre-window, or "reverse-now/favorable-now". Banned vocab:
   T-score · hazard · ignition · imminent · favorable-now. δ_excess(h) is a latent-regime half-life
   descriptor; an INTERFACE GUARD forbids any downstream object consuming it as a holding/entry/reversion
   horizon. Firewall acceptance test: future-injection bit-identity (detonate a future bar; every
   classification label and embargo boundary bit-identical — the doc-19 causal gate).
```

### 3.7 FROZEN grid, cohort, calibration set

```text
k  (classification window, bars):   {60, 120, 250}
h  (test window length, bars):      {20, 40, 60, 120}                 — horizon-resolved decay curve
g  (embargo, bars):                 {ceil(L), 2·ceil(L), 4·ceil(L), 8·ceil(L)}, L MEASURED per classifier (F1)
θ  (sub-diffusivity threshold):     SINGLE value frozen on the DISJOINT calibration cohort; no per-cell re-opt
q-grid:                             {2,5,10,20} (frozen)
H=1 rule:                           fixed deterministic Boolean {VR(q)<1 ∀q in band} ∧ {ACF in band} ∧
                                    {ADF ∧ KPSS pass}; bit-identical on every surrogate path
Surrogates/cell B:                  ≥ 500; frozen seed
δ_excess read:                      vs WORST-CASE (most-persistent) surrogate member

TEST COHORT (no obs informs θ or the rule): Arm-A TRUSTED legs / reconstructible spreads (46 legs) spanning
  ≥2–3 INDEPENDENT instruments & disjoint epochs; includes the NG calendar (doc 21/23 conditional-survival
  anchor) AND ≥2 instruments from a DIFFERENT habitat family (cross-asset / different roll structure).
CALIBRATION COHORT (F3): a separate epoch/cohort contributing ZERO observations to the test set, on which
  θ and the H=1 rule are frozen BEFORE test data is touched. Any test-epoch leakage into θ-selection VOIDS the run.
```

### 3.8 §11.8 positive-control PRECONDITION (F6)

```text
Before any δ_excess ≤ 0 is a credible KILL, the apparatus must SIMULTANEOUSLY:
  (A) CONFIRM δ_excess > band on a known, literature-anchored, DAILY, economically-anchored regime-persistent
      reverter at the RELEVANT SCALE (Brent hourly is off-scale — doc 23 — and does NOT satisfy this);
  (B) print δ_excess ≈ 0 (within band) on a pure RW and on a single-regime constant-parameter OU (zero-controls);
  (C) RECOVER known persistence above band on a synthetic Markov regime-switching series (calibrated power).
A kill from an apparatus failing (A)/(B)/(C) is INCONCLUSIVE → recalibrate apparatus, not market (doc-19 precedent).
```

---

## 4. FROZEN BINARY OUTPUT CONTRACT (the type-lock — Gate 2 input)

```text
TYPE:        Enum{ELIGIBLE, INELIGIBLE} per (instrument, period). No third state. No float anywhere.
CADENCE:     period = rebalance cadence, COARSE: ≥ weekly (default bi-/4-weekly, matched to the 1–12-week
             book and the regime-persistence horizon). NO intra-period re-evaluation.
HYSTERESIS:  two FIXED, PRE-REGISTERED, GLOBAL thresholds on the latent regime statistic: enter at θ_in,
             exit at θ_out, θ_in stricter than θ_out (asymmetric band) + a minimum DWELL of D periods before
             a flip is honored. Purpose SOLELY flip-flop turnover control — NEVER forward-return optimization.
CONSUMER:    STATELESS. Hysteresis/dwell held INTERNALLY; only the current-period enum is exposed.
FORBIDDEN FIELDS (none may exist in or be derivable from the contract):
   probability · confidence · continuous score · weight · sleeve allocation · graded conviction ·
   eligibility-STREAK length · time-since-flip · trailing eligibility-fraction · flip count ·
   any float monotone in the latent regime magnitude · any per-bar / sub-period scalar.
DECISION USE: the ONLY admissible composition is SET MEMBERSHIP — include in (or exclude from) an
   equal-weight (or external risk-parity/capacity-sized) eligible-set book. The enum may NOT be multiplied
   against, thresholded with, ranked by, or regressed on any per-bar deviation / z / entry trigger.
```

**Firewall proof (type-level).** State-T needs a continuous channel to multiply against a per-bar
deviation/z to scale entry size. A Boolean cannot scale a position — only include/exclude it from an
externally-sized set. With (i) no float emitted, (ii) coarse cadence (the flag cannot proxy a per-bar
signal), (iii) hysteresis making flips slow/set-membership-like, and (iv) the **streak/history export ban**,
the arithmetic for State-T does not exist in the contract. Field type-lock alone is necessary-not-sufficient
(the streak leak); **with the streak/history ban it is sufficient.** Zombie risk: **LOW**, structural.

---

## 5. FROZEN MATERIALITY HURDLE (Gate 2)

**Structure: DISJUNCTION on benefit, CONJUNCTION on guards.** All benefit thresholds are measured
**INCREMENTAL vs the cheap-baseline eligible-set** (ARM B, §7), NOT vs flat; **replicated across ≥2
independent OOS habitats** under FWER control; **net of realistic costs** (transaction + borrow + slippage).

```text
DEPLOY  iff  [ (A) OR (B) OR (C) ]   AND   [ (CAP) AND (TURN-CAP) AND (INC) ]
```

### Benefit axes (DISJUNCTION — ≥1 must clear)

```text
(A) NET-OF-COST SHARPE   ΔSR ≥ +0.15 absolute (annualized), object-eligible-set book minus cheap-baseline-
                         eligible-set book, CI lower bound > 0. (Sanity floor: also ≥ +0.25 vs flat.)  PRIMARY.
(B) TURNOVER / COST      ≥ 20% reduction in annualized book turnover (or ≥20% reduction in total
                         transaction+borrow cost-drag, bps) at net ΔSR ≥ −0.05.  (no-trade-environment value.)
(C) MAX-DD / TAIL        ≥ 20% RELATIVE reduction in book max-drawdown OR ≥15% reduction in worst-month
                         adverse excursion, at net ΔSR ≥ −0.05.  (most a-priori-plausible disjunct.)
```

### Viability guards (CONJUNCTION — ALL must hold)

```text
(CAP)      eligible set ≥ 60% of flat-universe deployable notional AND ≥ 8 instruments avg/period.
(TURN-CAP) eligibility flips raise gross book turnover by ≤ +10% over the cheap-baseline book.
(INC)      every benefit measured ORTHOGONALIZED vs the cheap 1-line vol/half-life/VR baseline eligible-set.
           The object must beat the CHEAP BASELINE, not merely beat flat. Beating flat is necessary-not-sufficient.
```

### NON-FINDING band (explicit)

```text
NON-FINDING if (none of A/B/C clears its floor vs the cheap baseline) OR (any guard breaches), EVEN WHEN
δ_excess > 0 is statistically real and the object beats FLAT. Concretely: ΔSR vs cheap-baseline in
(−∞, +0.15) with turnover-cut <20% and relative-MDD-cut <20% = true-but-immaterial = a doctrinally
SUCCESSFUL stop (§11.3). Response is kill/inert — do NOT retune, do NOT habitat-split to manufacture an argmax.
```

---

## 5A. MATERIALITY-THRESHOLD JUSTIFICATION (added per freeze refinement, 2026-06-04)

**Headline honesty statement.** These thresholds are **conservative, heuristic PM-material hurdles. They are
not discovered truths and no theory derives them as unique optima.** Each is anchored to a defensible
practitioner consideration that brackets a *range*; the specific frozen number is a deliberately round point
inside that range. Their value comes **not from precision but from pre-commitment** — freezing a conservative
hurdle before the run is what removes the post-hoc goalpost-moving that would otherwise let any positive
`δ_excess` be retrofitted as "material" (§11.7). We freeze a round number transparently rather than fabricate
a derivation. False precision is explicitly avoided: read `+0.15` as "~+0.15, the round point in a ~+0.10–0.20
bracket," not as a measured constant.

### Why ΔSharpe ≥ +0.15 (the PRIMARY disjunct), three anchors

```text
ANCHOR 1 — DETECTABILITY / ESTIMATION-ERROR FLOOR (sets the LOWER edge).
  A Sharpe estimate has large sampling error: SE(SR) ≈ sqrt((1 + 0.5·SR²)/N_years). On the available OOS
  sample (a few years × a handful of instruments per habitat) the SE on a Sharpe DIFFERENCE is on the order
  of ~0.1–0.3 even after pooling. A hurdle materially below ~+0.10 would sit INSIDE the noise band — we would
  be asserting an edge we cannot resolve. +0.15 is the round point just above where the cross-habitat
  replication design (≥2 habitats, multi-year book series, §7 power note) has a genuine chance to separate it
  from zero. Below this floor the honest statement is "undetectable", not "small".

ANCHOR 2 — OPERATIONAL-COST / COMPLEXITY FLOOR (sets the "earns its complexity" edge).
  ARM B — the cheap one-line vol/half-life/VR filter — is something "a junior codes in an afternoon" (§7).
  The habitat object adds a standing maintenance + model-risk surface: surrogate calibration, measured-embargo
  re-estimation, periodic re-freezing, the full §3 apparatus. An INCREMENTAL Sharpe below ~+0.10 does not
  justify carrying a second, heavier classification system over the free baseline. +0.15 is roughly where the
  overlay earns the operational burden it imposes.

ANCHOR 3 — PM BEHAVIORAL THRESHOLD (the honest core; sets the UPPER edge).
  A PM re-underwrites a sleeve or switches a universe screen only when the improvement is large enough to
  (a) survive their own skepticism about backtest overfit and (b) be worth the disruption of changing
  process. In practitioner terms an incremental +0.15 annualized Sharpe on a selection OVERLAY is "noticeable
  but not transformative" — about the smallest improvement a disciplined PM acts on rather than shrugs at.
  +0.05 is shrug territory (ignored). Demanding +0.30+ would require the overlay to perform like a STANDALONE
  strategy — the wrong bar for a selection filter, and one that would near-guarantee a NON-FINDING by
  construction. +0.15 sits between "noise/shrug" and "standalone-strength".

CONVERGENCE: the three anchors bracket ~+0.10 to ~+0.20. +0.15 is the conservative round midpoint. It is a
HEURISTIC PM-material floor, frozen for pre-commitment discipline — NOT a measured or optimized constant.
```

### Why the other thresholds (same heuristic status, briefer)

```text
(B) 20% turnover/cost reduction.  HEURISTIC. Below ~10% a turnover/cost change is lost in slippage variance
    and a PM would not notice it on the cost line; ~20% is roughly where the saving becomes visible and
    fundable. The ΔSR ≥ −0.05 leash ensures the cost saving is not bought with meaningful return give-up.
(C) 20% RELATIVE max-DD reduction / 15% worst-month.  HEURISTIC. Drawdown is what breaches risk limits and
    triggers capital withdrawal/firing; a ~one-fifth cut in max-DD is the order of improvement a risk
    committee notices and re-budgets around. Relative (not absolute) so it scales across instruments.
(CAP) 60% capacity / ≥8 names.  HEURISTIC diversification + capacity floor. A gate that "wins" only by
    shrinking to 2–3 names has traded an edge for concentration/capacity risk — a Pyrrhic pass, rejected.
(TURN-CAP) +10% turnover ceiling.  HEURISTIC. The overlay must not ADD more churn-cost than its selection
    benefit; +10% is a conservative cap on self-inflicted turnover.
```

### What is principled vs heuristic (clean separation)

```text
PRINCIPLED (not heuristic), and these carry the rigor:
  - the DISJUNCTION-on-benefit / CONJUNCTION-on-guards STRUCTURE (a PM re-tools on any one axis he is paid
    on; but a one-axis win that strangles capacity / churns the book / merely re-derives the free filter is
    illusory — hence the guards);
  - INCREMENTAL-vs-cheap-baseline measurement (the binding falsifier, doc 26 — beating flat is not enough);
  - cross-habitat OOS replication, FWER, full-search reporting (the anti-p-hacking core).
HEURISTIC (transparently so), frozen as conservative PM-material floors:
  - the specific numbers +0.15 / 20% / 20% / 60% / 8 / +10%.
The rigor lives in the STRUCTURE and the INCREMENTAL/OOS discipline; the numbers are honest conservative
hurdles whose job is to be FIXED IN ADVANCE, not to be exact.
```

---

## 6. FROZEN SUCCESS / FAILURE CONDITION (binary gating, incremental-vs-baseline)

Three books, equal-weight (or identical external risk-parity sizing) WITHIN each eligible set:

```text
ARM C (FLAT)            equal-weight over ALL candidate instruments. (necessary baseline; too easy to beat)
ARM B (CHEAP BASELINE)  equal-weight within a cheap 1-line BINARY eligible-set: rank/threshold on trailing
                        residual-vol / half-life / variance-ratio. THE COMPETITOR — the object must earn its complexity.
ARM A (OBJECT)          equal-weight within the habitat δ_excess BINARY eligible-set.
                        INCREMENT identified on DISCORDANT CELLS where ARM A and ARM B eligibility DISAGREE;
                        concordant cells carry ZERO incremental information.
```

```text
VALUE PRESENT  iff BOTH:
  (S-STAT) the incremental (ARM A − ARM B) book metric has CI EXCLUDING 0, with:
             • serial-dependence-robust inference (two-way cluster instrument×period, OR stationary block
               bootstrap, block ≈ regime-persistence/rebalance horizon — NEVER iid SEs);
             • FWER control across the full search (≥2 habitats × A/B/C axes) via Romano–Wolf step-down
               (NOT naive Bonferroni — axis stats correlated);
             • REPLICATION across ≥2 INDEPENDENT OOS habitats (unit of evidence = survives across habitats);
             • FULL search reported, NO argmax cherry-pick.
  (S-MAT)  the §5 hurdle clears:  [ (A) OR (B) OR (C) ]  AND  [ (CAP) AND (TURN-CAP) AND (INC) ].

Exact inequalities (incremental, ARM A − ARM B, ≥2 OOS habitats, net of cost):
  (A)  ΔSR ≥ +0.15            with CI lower bound > 0
  (B)  Δturnover ≤ −20%       at ΔSR ≥ −0.05
  (C)  ΔMDD_rel ≤ −20%  OR  Δworst-month-excursion ≤ −15%   at ΔSR ≥ −0.05
  (CAP)      capacity(A) ≥ 0.60 × capacity(flat)  AND  mean |eligible set| ≥ 8
  (TURN-CAP) turnover(A) ≤ 1.10 × turnover(B)
  (INC)      all of A/B/C evaluated as (ARM A − ARM B), never (ARM A − flat)

VALUE ABSENT / NON-FINDING if either (S-STAT) or (S-MAT) fails. A NON-FINDING is a successful stop (§11.3);
response is kill/inert — NOT hurdle-softening or habitat-splitting to manufacture an argmax.
```

---

## 7. Power & false-negative honesty (frozen expectation)

```text
- Coarsening tax is real but bounded: dichotomizing the latent statistic costs ~a median-split (~π/2
  Gaussian-latent penalty → effective N ≈ 60–65% FOR THE GATING DECISION). But the TEST STATISTIC is the
  BOOK aggregate (portfolio Sharpe/MDD/turnover) at FULL continuous resolution on period-level P&L — the
  enum does not coarsen the book-level statistic. Power is set by (#habitats ≥2) and (book-series length).
- BINDING CONSTRAINT = the DISCORDANT-CELL incremental test. If ARM A / ARM B flags agree 80–90% of the time
  (likely — both read second-moment structure), the effective sample is the 10–20% discordant subset, thin
  per habitat. Estimator: panel regression of book-period net P&L on baseline-eligible + habitat-eligible
  dummies; incremental coefficient = discordant-cells contrast; block-bootstrap / two-way-cluster + Romano–Wolf.
- HONEST POWER READ: a MATERIAL edge (true incremental ΔSR ~+0.25–0.30) is detectable at conventional power
  across 2 habitats. A MARGINAL edge (+0.10–0.15) will likely FALSE-NEGATIVE. This is the accepted cost of
  the State-T-priority design.
- INTERPRETATION GUARD: a NON-FINDING here means "not deployable as a BINARY universe gate at a MATERIAL
  threshold" — NOT "the persistence phenomenon is absent". Gate-1 (statistical, doc 25) and Gate-2 (economic)
  verdicts are recorded SEPARATELY in the registry; do not collapse them.
```

---

## 8. Execution sequence (pre-registered; NOT authorized by this document)

```text
STEP 0  (PRECONDITION, §3.8): confirm a matched-scale DAILY literature-anchored regime-persistent reverter
        exists in the cohort and the apparatus CONFIRMS it (A); print zero-controls (B); recover the
        regime-switching control (C). Until (A)/(B)/(C) hold, NO kill is credible.
STEP 1  freeze θ + the H=1 rule on the DISJOINT calibration cohort (§3.7); verify the label separates real
        from matched-stationary surrogate at classification time.
STEP 2  measure L per classifier on the matched null; set the g-grid (§3.2/§3.7).
STEP 3  run GATE 1: δ_excess across the frozen grid × cohort, worst-case-surrogate-relative, FWER-corrected,
        with the δ_excess(g) decay probe and cross-habitat OOS replication.
STEP 4  if GATE 1 passes, run GATE 2: build ARM A/B/C books on the frozen cadence; evaluate S-STAT ∧ S-MAT
        on discordant cells.
STEP 5  posterior update → FREEZE (conditional survival, named condition + kill trigger) / NON-FINDING (kill)
        / INCONCLUSIVE (recalibrate apparatus). Update HYPOTHESIS_REGISTRY.md.
EACH STEP requires explicit authorization. No step is run by this artifact.
```

---

## 9. Freeze manifest (what becomes a §6 frozen invariant on fold-in)

```text
FROZEN: the H0/H1 statement; the §3.1 classifier & cuts; the F1 measured-embargo rule; the §3.4 statistic
        & real-minus-worst-case-surrogate read; the §3.5 surrogate families + 4 calibration gates; the
        §3.6 multiplicity/OOS/firewall rules; the §3.7 grid + cohorts; the §3.8 positive-control precondition;
        the §4 binary type-lock + streak/history ban; the §5 materiality hurdle (structure AND the frozen
        numbers); the §6 three-arm S-STAT ∧ S-MAT condition + exact inequalities; the §8 step order.
DEFERRED (remembered, not dead): continuous weighting / sleeve sizing — reopen ONLY after binary gating
        proves OOS value (§11.3); reopen trigger named in HYPOTHESIS_REGISTRY.md.
DELTAS FOLDED from docs 25/26/27 (Δ1–Δ6): Δ1 binary type-lock replaces continuous score/weight in the
        economic block; Δ2 success condition = two-part S-STAT ∧ S-MAT with ARM A/B/C, increment on
        discordant cells; Δ3 materiality hurdle (§5) added with explicit NON-FINDING band + "kill not retune";
        Δ4 discordant-cell panel estimator + serial-robust SEs + Romano–Wolf FWER + full-search reporting;
        Δ5 firewall seals (streak/history ban, frozen thresholds, turnover-only hysteresis, cadence ≥ weekly);
        Δ6 gate order PRECONDITION → GATE 1 → GATE 2 unchanged.
CHANGING ANY FROZEN ITEM AFTER FREEZE = FREEZE-BREAK (§6): surface justification + obtain authorization first.
```

---

## 10. Surviving uncertainty · explicit non-conclusions · next action

```text
SURVIVING UNCERTAINTY:
  - whether a matched-scale DAILY real positive control EXISTS in the cohort (STEP 0 is itself a real risk;
    Brent hourly does not qualify — doc 23);
  - whether the discordant-cell subset is large enough for adequate power per habitat (§7);
  - the true L (measured at runtime; the g-grid is built around it but L is not yet known).

EXPLICIT NON-CONCLUSIONS:
  - we do NOT claim habitat persistence exists (Gate 1 unrun);
  - we do NOT claim it is economically material (Gate 2 unrun);
  - we do NOT claim the +0.15 / 20% numbers are optimal — they are conservative heuristic PM floors (§5A);
  - a future NON-FINDING will NOT prove the phenomenon absent, only that it is not a deployable binary gate
    at a material threshold (§7 interpretation guard).

CONFIDENCE in the PRE-REGISTRATION DESIGN: MEDIUM-HIGH (four-lens-survived across docs 25–27; leakage,
  circularity, signal-drift, p-hacking, and economic-inertia attacks each carried into a frozen guard).
CONFIDENCE in a POSITIVE OUTCOME: LOW-MODEST (~20–40%, §27); modal expectation = clean NON-FINDING = success.

NEXT ACTION (on authorization only): freeze this document as a §6 invariant set, then authorize STEP 0
  (the real-data positive control) as the first — and independently gating — empirical step. No execution
  occurs without that explicit authorization.
```
