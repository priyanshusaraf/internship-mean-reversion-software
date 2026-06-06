# 27 — Forward Habitat-State Persistence: Binary-Only Eligibility + Materiality Refinement

## Status

```text
DATE:        2026-06-04
MODE:        RESEARCH MODE (CLAUDE.md §3 Mode 1) — freeze-REFINEMENT layer, adjudication only
DELIVERABLE: BINARY-ONLY v1 OUTPUT CONTRACT + FROZEN MATERIALITY HURDLE + updated success/failure condition
SUPERSEDES:  the GRADED-WEIGHTING channel in doc 26 for v1 (capital scaling / sleeve weighting / conviction
             tilt is DEFERRED, not killed — reopen only after binary gating independently proves OOS value)
NOT THIS:    empirical run · STEP 0 · code · signal · detector · data touched · freeze/authorization of the run
GOVERNS:     CLAUDE.md §11.2 (trader lens = prioritization, never rigor relaxation), §11.3 (probation /
             conditional survival / "stopping is a success"), §11.7 (cross-habitat OOS unit + p-hacking guard),
             §4 (zombie prohibition: State-T DEAD), §6 (firewall), §5/§14 (artifact provenance)
RELATION:    Sits ON TOP of docs 25 (statistical decidability) + 26 (economic USEFUL_IF). It does NOT
             relitigate the settled object; it TIGHTENS the deployment contract under two new restrictions
             and re-expresses doc 26's success condition for a binary gate measured incremental-vs-baseline.
LENSES:      Trader/PM (lead, decisive on materiality) · Useless-Prosecutor (downgrade bar) ·
             Firewall-Architect (type-lock, binding) · Quant-Econometrician (power, honest expectations)
```

This document is pre-registration-grade on its contract and hurdle. The output contract (§4) and the
materiality hurdle (§5) and the success/failure inequality (§6) are frozen on fold-in to the combined
pre-registration. **Nothing below authorizes empirical work.** This is the freeze-refinement layer that will
*fold into* the combined pre-reg; it does not itself freeze or start STEP 0.

---

## 1. What is settled (do NOT relitigate)

- **Object (doc 25):** forward HABITAT-STATE persistence — sign-free latent second-moment regime transition
  probability, measured surrogate-relative (`δ_excess = δ_real − δ_surrogate` vs worst-case matched null).
  **EMPIRICALLY_DECIDABLE.** Pre-reg gated, not run.
- **Economics (doc 26):** **ECONOMICALLY_USEFUL_IF** (3 USEFUL_IF / 1 UNDEPLOYABLE). Only admissible economic
  decision = book-level MR-universe **MEMBERSHIP + capital WEIGHT** (never entry timing/direction). Strongest
  falsifier = **no INCREMENTAL value over a cheap 1-line vol/half-life/VR baseline.** Two-stage gate:
  statistical (25) → economic (26).

This pass changes ONE thing in the doc-26 economic decision: it **removes the WEIGHT channel for v1** and
collapses the admissible decision to **MEMBERSHIP only**, then attaches a **hard materiality hurdle.**

---

## 2. The two restrictions (precise statement + rationale)

### RESTRICTION 1 — BINARY ELIGIBILITY ONLY (v1)

```text
The object may emit ONLY {eligible / ineligible} per instrument per period.
FORBIDDEN in v1: confidence · probability · continuous score · capital scaling · sleeve weighting ·
                 graded conviction · any float derived from / monotone in the latent regime magnitude.
```

**Rationale.** Graded conviction is exactly the channel through which State-T resurrects: "MR confidence →
larger allocation → larger size when reversion looks likely" is a per-instrument continuous conviction object
indistinguishable in arithmetic from a (banned) favorable-now scalar. Removing the float removes the channel.
Weighting is **staged, not killed**: reconsidered ONLY AFTER binary gating *independently* proves value OOS.

### RESTRICTION 2 — EXPLICIT MATERIALITY HURDLE

```text
δ_excess > 0 with CI excluding 0 is NOT sufficient. Require a PRE-REGISTERED PRACTICAL hurdle: a
PM-material improvement in ≥1 of {net-of-cost Sharpe, turnover/cost, max-drawdown, capacity}, SIZED so a
real PM changes behavior. A statistically significant but immaterial gain is a NON-FINDING.
```

**Rationale (§11.2).** The deployable object is a BOOK after costs. Significance is necessary, not
sufficient. The hurdle converts "statistically real" into "a PM would re-tool the universe rule he actually
uses." Below the hurdle, the correct call is **kill/inert, not retune** (§11.7 forbids softening the bar to
manufacture a pass).

---

## 3. Adjudication of the four-lens disagreement

The four lenses **agree on verdict TYPE** and **agree on direction of realistic prior**; they disagree only
on (a) the materiality STRUCTURE and (b) the numeric prior. Adjudicated:

**(A) Inert-by-type vs inert-by-prior — RESOLVED.** Unanimous: binary universe gating is a *legitimate,
familiar, deployable* PM primitive (watchlist / eligible-set / "is this pair in the MR book this month").
Doc 26's admissible decision was already book-level MEMBERSHIP; binary is the **natural output type, not a
crippling amputation.** The only economic channel lost is conviction-scaled sizing — and an MR book sizes by
residual-vol / risk-parity / capacity, **not** by conviction, so that loss is low marginal value here.
Therefore the object is **NOT inert-by-construction**; `LIKELY_TRUE_BUT_INERT` (which asserts the object can
never move a decision) is the **wrong type label.** Where the prosecutor pushed downgrade, it explicitly
declined the reflexive move and converged: inert-by-low-prior ≠ inert-by-type.

**(B) Materiality structure — ADJUDICATED to a hybrid (trader lens decisive).** Lenses split:
trader/firewall favored *conjunction-floors + disjunction-win*; prosecutor/econometrician favored *pure
disjunction with per-axis no-harm*. These are the same object stated two ways. **Frozen structure (§5):**
DISJUNCTION on the *benefit* axis (a PM funds a universe filter if ANY single material axis clears) AND
CONJUNCTION on the *no-harm / viability guards* (capacity, turnover-cap, incrementality must ALL hold). This
is the trader lens's "conjunction floors + disjunction win" and the prosecutor's "disjunction with no-harm
clause" reconciled — they are identical. Pure-AND across all benefit axes is rejected (no real filter clears
it); pure-OR with no guards is rejected (lets a Sharpe win ride a drawdown blowup or a capacity collapse).

**(C) Numeric prior — ADJUDICATED to LOW-to-MODEST (~25–40%, point ~30%).** Trader said ~30–40%; prosecutor
~20–30%; firewall LOW/LOW-MEDIUM; econometrician ~25–35%. **The spread is driven entirely by the
incremental-vs-cheap-baseline gate, which all four name as the assassin.** Adjudicated central estimate:
**~30%, LOW-MODEST.** The cheap 1-line vol/half-life/VR filter captures most second-moment habitat structure
for free; the increment must live in the thin DISCORDANT-CELL subset where habitat disagrees with the cheap
filter. The most-likely-to-fire disjunct is **drawdown/tail** (excluding high-second-moment cells plausibly
cuts drawdown even when it does not lift Sharpe) — residual hope concentrates there.

**(D) Zombie risk — UNANIMOUS, with ONE binding seal.** Binary-only upgrades the firewall from POLICY
("don't wire the score") to STRUCTURAL ("no score exists to wire"). All four flag the SAME residual leak:
**eligibility-streak / time-in-eligibility / flip-count** is an ordinal monotone-in-conviction that
reconstructs the forbidden graded confidence. The firewall architect's type-lock is binding: emit **only the
current-period enum, consumer-stateless**; **forbid export of any streak/age/history-derived continuous
statistic.** With that seal, zombie risk is **LOW** (down from LOW-MEDIUM under continuous scoring).

---

## 4. BINARY-ONLY v1 OUTPUT CONTRACT (the type-lock — FROZEN on fold-in)

```text
TYPE:        Enum{ELIGIBLE, INELIGIBLE}  per (instrument, period).  No third state. No float anywhere.
CADENCE:     period = rebalance cadence, pre-registered, COARSE: ≥ weekly (default bi-weekly / 4-weekly to
             match the 1–12-week book and the regime-persistence horizon). NO intra-period re-evaluation.
HYSTERESIS:  two FIXED, PRE-REGISTERED, GLOBAL thresholds on the latent regime statistic:
                 enter eligibility at θ_in ; exit at θ_out ; with θ_in stricter than θ_out (asymmetric band)
                 + a minimum DWELL of D periods before any flip is honored.
             Purpose is SOLELY flip-flop turnover control — NEVER forward-return optimization. The band is
             justified by turnover, frozen, and not re-tuned per-instrument or per-period.
CONSUMER:    STATELESS. The system holds hysteresis/dwell state INTERNALLY for turnover control but EXPOSES
             only the current-period enum. No downstream function may read history off the emission.

FORBIDDEN FIELDS (type-lock — none of these may exist in the contract or be derivable from it):
    probability · confidence · continuous score · weight · sleeve allocation · graded conviction ·
    eligibility-streak length · time-since-flip · trailing eligibility-fraction · flip count ·
    any float monotone in the latent regime magnitude · any per-bar / sub-period scalar.

DECISION USE: the ONLY admissible composition is SET MEMBERSHIP — include the instrument in an
              equal-weight (or external risk-parity/capacity-sized) eligible-set book, or exclude it.
              The enum may NOT be multiplied against, thresholded with, ranked by, or regressed on any
              per-bar deviation / z / entry trigger.
```

**Proof the zombie path is severed at the type level.** State-T = a per-bar, graded, forward "MR-likely-soon
/ favorable-now" object that scales entry size. To build it you need a continuous channel to multiply against
a per-bar deviation/z. A Boolean **cannot scale a position** — it can only include/exclude it from an
externally-sized set. With (i) no float emitted, (ii) coarse period cadence so the flag cannot proxy a
per-bar signal, (iii) hysteresis making flips slow and set-membership-like, and (iv) the consumer-stateless
ban on deriving any continuous statistic from the eligibility time series, **the arithmetic for State-T does
not exist in the contract.** The type-lock is the load-bearing firewall and it holds. Necessary-and-
sufficient: the field type-lock alone is necessary-not-sufficient (streak leak); **with the streak/history
export ban it is sufficient.**

---

## 5. FROZEN MATERIALITY HURDLE (pre-registered — FROZEN on fold-in)

**STRUCTURE: DISJUNCTION on benefit, CONJUNCTION on guards.**

```text
DEPLOY  iff  [ (A) OR (B) OR (C) ]   AND   [ (CAP) AND (TURN-CAP) AND (INC) ]
```

All benefit thresholds are measured **INCREMENTAL vs the cheap-baseline eligible-set** (ARM B, §6), NOT vs
flat, and **replicated across ≥2 independent OOS habitats** under FWER control, **net of realistic costs**
(transaction + borrow + slippage).

### Benefit axes (DISJUNCTION — ≥1 must clear)

```text
(A) NET-OF-COST SHARPE        ΔSR ≥ +0.15 absolute (annualized), object-eligible-set book minus
                              cheap-baseline-eligible-set book. (Sanity: also ≥ +0.25 vs flat.)
    PM decision: "re-underwrite the sleeve / switch the universe screen." Below ~+0.10 = estimation noise,
    ignored. PRIMARY disjunct.

(B) TURNOVER / COST           ≥ 20% reduction in annualized book turnover (or ≥20% reduction in total
                              transaction+borrow cost drag, bps) at net Sharpe no worse than −0.05.
    PM decision: "fund the filter — same return for materially less cost/capacity strain." This is the
    no-trade-environment-identification value (§11.2), the object's most defensible disjunct. <10% = noise.

(C) MAX-DRAWDOWN / TAIL       ≥ 20% RELATIVE reduction in book max-drawdown (e.g. 25% → ≤20%) OR ≥15%
                              reduction in worst-month adverse excursion, at net Sharpe no worse than −0.05.
    PM decision: "deploy — cleaner tail by excluding regime-broken instruments." Most a-priori-plausible
    disjunct (regime filter excludes high-second-moment cells). <10% relative = noise.
```

### Viability guards (CONJUNCTION — ALL must hold)

```text
(CAP)      CAPACITY FLOOR. Eligible set retains ≥ 60% of flat-universe deployable notional AND ≥ 8
           instruments on average per period. A gate "better" only by shrinking to 2–3 names is a capacity
           FAILURE, not an edge — rejected even if (A)/(B)/(C) fire.
(TURN-CAP) TURNOVER CEILING. Eligibility flips (hysteresis-controlled) must not raise gross book turnover
           by > +10% over the cheap-baseline book. Rotation churn is the primary self-destruction path.
(INC)      INCREMENTAL GUARD (the binding falsifier, doc 26). Every benefit above is measured
           ORTHOGONALIZED vs the cheap 1-line vol/half-life/VR baseline-eligible-set. The object must beat
           the CHEAP BASELINE, not merely beat flat. Beating flat is necessary-not-sufficient.
```

### NON-FINDING band (stated explicitly)

```text
NON-FINDING  if  (none of A/B/C clears its floor vs the cheap baseline)  OR  (any guard breaches),
even when δ_excess > 0 is statistically real and the object beats FLAT.
Concretely: ΔSR vs cheap-baseline in (−∞, +0.15) with turnover-cut <20% and relative-MDD-cut <20% = a
true-but-immaterial habitat gate = NON-FINDING = doctrinally SUCCESSFUL stop (§11.3). Do NOT retune.
```

**Why disjunction-on-benefit + conjunction-on-guards.** A PM re-tools universe construction if it helps on
ANY ONE axis he is paid on (return, cost, or tail) — hence disjunction. But a one-axis win that strangles
capacity, churns the book, or merely re-derives the free filter is a Pyrrhic / illusory pass — hence the
three conjunctive guards. The guards are what make the bar honest rather than cherry-picked (§11.7).

---

## 6. UPDATED SUCCESS / FAILURE CONDITION (binary gating, incremental-vs-baseline)

Three books, equal-weight (or identical external risk-parity sizing) WITHIN each eligible set:

```text
ARM C (FLAT)            equal-weight over ALL candidate instruments. (necessary baseline; too-easy to beat)
ARM B (CHEAP BASELINE)  equal-weight within a cheap 1-line BINARY eligible-set: rank/threshold on
                        trailing residual-vol / half-life / variance-ratio; take eligible band. THE
                        COMPETITOR. (a junior codes it in an afternoon — the object must earn its complexity)
ARM A (OBJECT)          equal-weight within the habitat δ_excess BINARY eligible-set.
                        INCREMENT identified on DISCORDANT CELLS: instrument-periods where ARM A and ARM B
                        eligibility DISAGREE. Concordant cells carry ZERO incremental information.
```

**VALUE PRESENT iff BOTH hold:**

```text
(S-STAT)  the incremental (ARM A − ARM B) book metric has CI EXCLUDING 0, with:
              • serial-dependence-robust inference (two-way cluster by instrument×period, OR stationary
                block bootstrap with block length ≈ regime-persistence / rebalance horizon — NEVER iid SEs);
              • FWER control across the full search (≥2 habitats × the A/B/C axes) via Romano–Wolf
                step-down (NOT naive Bonferroni — axis stats are correlated);
              • REPLICATION across ≥2 INDEPENDENT OOS habitats (unit of evidence = "survives across
                independent habitats," not "appears in one");
              • the FULL search reported, NO argmax cherry-pick (§11.7).
AND
(S-MAT)   the §5 hurdle clears:  [ (A) OR (B) OR (C) ]  AND  [ (CAP) AND (TURN-CAP) AND (INC) ].
```

**Exact inequalities (incremental, ARM A − ARM B, ≥2 OOS habitats, net of cost):**

```text
(A)  ΔSR ≥ +0.15           with CI lower bound > 0
(B)  Δturnover ≤ −20%      at  ΔSR ≥ −0.05
(C)  ΔMDD_rel ≤ −20%  OR  Δworst-month-excursion ≤ −15%   at  ΔSR ≥ −0.05
(CAP)      capacity(A) ≥ 0.60 × capacity(flat)  AND  mean |eligible set| ≥ 8
(TURN-CAP) turnover(A) ≤ 1.10 × turnover(B)
(INC)      all of A/B/C evaluated as (ARM A − ARM B), never (ARM A − flat)
```

**VALUE ABSENT / NON-FINDING** if either (S-STAT) or (S-MAT) fails. A NON-FINDING is a doctrinally
successful stop (§11.3); the response is kill/inert, **not** hurdle-softening or habitat-splitting to
manufacture an argmax (§11.7 p-hacking guard).

---

## 7. POWER + FALSE-NEGATIVE note under binary coarsening

- **Coarsening tax is real but bounded.** Dichotomizing the latent regime statistic costs roughly a
  median-split's efficiency (~π/2 Gaussian-latent penalty → effective N ≈ 60–65% of a continuous-score
  design FOR THE GATING DECISION). **But the test statistic is the BOOK aggregate** (portfolio
  Sharpe/MDD/turnover), computed at FULL continuous resolution on the period-level book P&L — within-
  instrument gradation discarded by the enum does NOT coarsen the book-level statistic. Power is set by
  (#habitats ≥2) and (length of book series, multi-year multi-instrument — adequate).
- **The binding constraint is the DISCORDANT-CELL incremental test, not the binary label.** The increment is
  identified only from instrument-periods where ARM A and ARM B disagree. If the two flags agree 80–90% of
  the time (likely — both read second-moment structure), the effective sample is the 10–20% discordant
  subset, which is thin per habitat. Estimator: panel regression of book-period (or per-instrument-period)
  net P&L on a baseline-eligible dummy + habitat-eligible dummy; the incremental coefficient = discordant-
  cells contrast. Inference: block bootstrap / two-way cluster + Romano–Wolf FWER.
- **Honest power read:** a MATERIAL edge (true incremental ΔSR ~+0.25–0.30) is detectable at conventional
  power across 2 habitats with a few hundred period-obs each. A MARGINAL edge (+0.10–0.15) will likely
  **false-negative.**
- **Why the expected NON-FINDING is acceptable (§11.3).** The hurdle is deliberately sized so only PM-
  material edges survive. A false-negative on a SUB-material edge is the CORRECT economic decision — a PM
  would not deploy it anyway. The only real risk is a false-negative on a *material* edge, and that is
  dominated NOT by binary coarsening but by the (INC) orthogonalization gate: if the object's eligible set
  is near-collinear with the cheap baseline's, (INC) fails — but that is **the falsifier working, not low
  power.** Power is "adequate for material edges, intentionally blind to immaterial ones" — design working,
  not failing.

---

## 8. REVISED ZOMBIE-STATE-T RISK under binary-only

```text
LEVEL: LOW   (down from LOW-MEDIUM under doc-26 continuous/period-level scoring)
```

**Why it drops.** The firewall moves from POLICY to STRUCTURAL. With no continuous field emitted there is no
scalar to multiply against a per-bar deviation/z, so "MR-confidence → bigger size → imminent reversion"
cannot be assembled — its arithmetic does not exist. Banned vocab (T-score · hazard · ignition · imminent ·
favorable-now) has no surface to attach to.

**Residual leaks (all non-structural, sealed by pre-registration):**

```text
(1) ELIGIBILITY-STREAK / TIME-IN-ELIGIBILITY / FLIP-COUNT  — an ordinal monotone-in-conviction that
    reconstructs graded confidence. SEAL: emit only the current-period enum, consumer-stateless; forbid
    export of any streak/age/history-derived continuous statistic for sizing or timing. (BINDING — without
    this seal binary-only is NOT airtight.)
(2) THRESHOLD-CHOICE  — moving θ_in/θ_out per-period in a state-T-like way. SEAL: thresholds FROZEN /
    pre-registered; re-tuning is a freeze-break requiring OOS re-validation.
(3) HYSTERESIS-AS-TIMING  — tuning enter/exit asymmetry to encode directional timing. SEAL: band fixed,
    pre-registered, justified solely by turnover control, never by forward-return optimization.
(4) CADENCE-TOO-FINE  — sub-weekly recompute lets the boolean track short-horizon vol and proxy a timing
    signal. SEAL: cadence ≥ weekly, no intra-period re-evaluation.
```

With seals (1)–(4) the zombie path is fully severed. The output-type lock is the load-bearing firewall.

---

## 9. THE VERDICT

```text
VERDICT:  ECONOMICALLY_USEFUL_IF
```

**Verdict TYPE (decidable conditional) — ROBUST.** Under BOTH restrictions the object remains a genuine
decidable conditional, NOT inert-by-construction: binary universe gating is a real, familiar, implementable
PM decision (equal-weight-within-eligible-set is a fully deployable book); the materiality hurdle is concrete
and pre-registerable; the firewall is structural; the test is runnable incremental-vs-cheap-baseline across
≥2 OOS habitats. It is therefore **NOT** `LIKELY_TRUE_BUT_INERT` — that label asserts the object can never
move a decision, which is false here. The verdict type is **ECONOMICALLY_USEFUL_IF**.

**Realistic PRIOR (likely outcome) — LOW-MODEST, ~30% (range 20–40%).** Dominated by the incremental-vs-
cheap-baseline gate. The free vol/half-life/VR filter captures most second-moment structure; binary
coarsening hands that baseline its best footing (both reduce to a yes/no membership label, discarding the
graded advantage that justified weighting in doc 26); and a +0.15 ΔSR / −20% turnover / −20% relative-MDD
increment OVER that baseline, OOS, FWER-controlled, across ≥2 habitats is a demanding bar a coarse latent-
regime label will **more often miss than clear.** **Most probable outcome = a clean NON-FINDING** (habitat
gate true-but-not-incrementally-material over the cheap baseline) — which doctrine explicitly counts as a
**successful** result, not an apparatus failure. Worth ONE pre-registered OOS shot (cheap, on existing
machinery, §12.1); if it fails the hurdle, the correct call is **kill/inert, not retune.**

**Four-lens vote:**

```text
Trader/PM (LEAD)        ECONOMICALLY_USEFUL_IF   prior ~30–40%   (binary is native to a watchlist book; not inert)
Useless-Prosecutor      ECONOMICALLY_USEFUL_IF   prior ~20–30%   (declined reflexive downgrade; inert-by-prior ≠ inert-by-type)
Firewall-Architect      ECONOMICALLY_USEFUL_IF   prior LOW–LOW-MEDIUM (type-lock airtight after streak seal)
Quant-Econometrician    ECONOMICALLY_USEFUL_IF   prior ~25–35%   (decidable, well-posed; tail/drawdown the live disjunct)
----------------------------------------------------------------------------------------------------------
ADJUDICATED:            ECONOMICALLY_USEFUL_IF   |  TYPE = decidable conditional (robust)
                                                 |  REALISTIC PRIOR = LOW-MODEST ~30%, modal outcome NON-FINDING
```

Unanimous on type; unanimous on direction of prior. **No downgrade to LIKELY_TRUE_BUT_INERT** — the object
is not inert-by-construction. But the honest expectation is set low and a clean NON-FINDING is pre-accepted.

---

## 10. What this changes for the COMBINED PRE-REGISTRATION (deltas to fold before STEP 0)

```text
Δ1  E-BLOCK OUTPUT TYPE (replaces doc 26 weighting channel):
    REMOVE  the continuous period-level habitat score / weight / sleeve-allocation output for v1.
    ADD     the §4 binary type-lock: Enum{ELIGIBLE, INELIGIBLE} per (instrument, period); coarse cadence
            ≥ weekly; pre-registered fixed asymmetric hysteresis (θ_in, θ_out, dwell D); consumer-stateless;
            forbidden-fields list incl. streak/age/flip-count. Weighting → DEFERRED (reopen only after binary
            proves OOS value).

Δ2  SUCCESS CONDITION (replaces doc 26 §10 economic inequality):
    REPLACE  "δ_excess > 0 survives nulls/FWER/≥2 habitats" (necessary)  WITH the TWO-PART condition §6:
             VALUE PRESENT iff (S-STAT) AND (S-MAT). Add ARM B (cheap 1-line binary universe filter) and
             ARM C (flat); identify the increment on DISCORDANT CELLS (ARM A − ARM B), never ARM A − flat.

Δ3  MATERIALITY HURDLE (new, frozen, §5):
    ADD     [ (A) ΔSR≥+0.15  OR  (B) Δturnover≤−20%  OR  (C) ΔMDD_rel≤−20%/Δexcursion≤−15% ]
            AND  [ (CAP) ≥60% notional & ≥8 names  AND  (TURN-CAP) ≤+10% turnover  AND  (INC) vs cheap baseline ].
            State the NON-FINDING band explicitly; pre-commit "kill/inert, not retune" on failure.

Δ4  INFERENCE SPEC (tighten, §6/§7):
    ADD     discordant-cell panel estimator; serial-dependence-robust SEs (two-way cluster OR stationary
            block bootstrap, block ≈ regime-persistence horizon); Romano–Wolf FWER across habitats × axes;
            full-search reporting, no argmax. Forbid iid SEs.

Δ5  FIREWALL SEALS (new, §8):
    ADD     pre-registered seals (1)–(4): streak/history export ban; frozen thresholds; turnover-only
            hysteresis; cadence ≥ weekly. Threshold/cadence/hysteresis re-tuning = freeze-break.

Δ6  ECONOMIC GATE ORDER (unchanged, restated):
    statistical (doc 25 STEP 0)  →  binary-gated economic materiality (this doc §6)  →  verdict.
    Real-data positive-control gate (§11.8) remains a STANDING precondition on the apparatus.
```

---

## 11. Surviving uncertainty · explicit non-conclusions · next action

**Surviving uncertainty.**
- The actual concordance rate between ARM A and ARM B is unknown until run; it sets discordant-cell sample
  size and thus realized power. High concordance → both thin sample AND likely (INC) failure.
- Whether the drawdown disjunct (C) is the one that fires is a hypothesis, not a result.
- Cross-habitat independence is assumed; if the ≥2 habitats share a common second-moment driver, the
  replication is weaker than it looks (note for the combined pre-reg's habitat-selection block).

**Explicit non-conclusions.**
- This does NOT conclude the object passes; the modal expectation is a NON-FINDING.
- This does NOT authorize STEP 0, code, or any data touch.
- This does NOT kill the weighting channel — it DEFERS it (reopen trigger: binary gating proves OOS value).
- This does NOT relitigate docs 25/26; it tightens the deployment contract only.

**Next action (on authorization only).** Fold Δ1–Δ6 into the COMBINED pre-registration (docs 25 + 26 + 27),
freeze it, then — and only then — run STEP 0 behind the §11.8 real-data positive-control gate.
```
```
