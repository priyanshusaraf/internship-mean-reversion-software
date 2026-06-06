# 26 — Forward Habitat-State Persistence: Economic Adjudication (Trader-First)

## Status

```text
DATE:        2026-06-04
MODE:        RESEARCH MODE (CLAUDE.md §3 Mode 1) — economic adjudication only
DELIVERABLE: TRADER-USEFULNESS VERDICT + economic pre-registration that GATES doc 25 STEP 0
NOT THIS:    empirical run (NOT authorized) · STEP 0 · code · signal · detector · any data touched
GOVERNS:     CLAUDE.md §11.2 (trader lens = prioritization, never rigor relaxation), §11.7 (cross-habitat
             OOS unit), §11.8 (real-data positive control), §4 (zombie prohibition), §5/§14 (artifact)
RELATION:    Sits ON TOP of doc 25. Doc 25 settled STATISTICAL admissibility/decidability. Doc 26 asks the
             ORTHOGONAL economic question and adds an economic pre-registration BEFORE doc 25's STEP 0.
LENSES:      Trader/PM (lead) · Useless-Prosecutor · Quant-Econometrician · Firewall-Architect (4-lens survival)
```

This document is pre-registration-grade on its economic claim. The success/failure inequality in §10 is
frozen on publication. Nothing below authorizes empirical work.

---

## 1. The Economic Question (assume the statistics already won)

Doc 25 ruled forward habitat-state persistence **EMPIRICALLY-DECIDABLE**: a sign-free latent second-moment
regime transition probability, `P(habitat in [t+1+g, t+h] | habitat in [t−k, t])`, read surrogate-relative
as `δ_excess = δ_real − δ_surrogate` against a worst-case most-persistent matched null. It emits no tense
about price, no deviation/z anchoring, no entry timing.

**For this pass, ASSUME `δ_excess > 0` survives every null, cross-habitat, FWER-corrected.** The question is
no longer *is it real* but *would an institutional trader running a 1–12-week mean-reversion BOOK care*.

**Why statistical persistence is insufficient (the load-bearing wedge).** `δ_excess > 0` is a statement about
**second-moment / variance dynamics** — the environment is more persistently sub-diffusive than a matched
null. It is **NOT** a statement about **net-of-cost realized MR profitability**. Three independent gaps sit
between the two:

```text
GAP 1 (descriptor ≠ payoff):   a habitat can be persistently sub-diffusive AND persistently unprofitable
                               after costs. Variance clustering is necessary-not-sufficient for reversion P&L.
GAP 2 (statistically real ≠     surviving the surrogate proves residual latent persistence beyond the
       economically real):     smoother artifact; it does NOT prove that residual moves a tradeable payoff
                               or is non-redundant with a 1-line vol/half-life/VR filter.
GAP 3 (significant ≠ material): a significant δ_excess can be a tiny absolute conditional lift on a high
                               base rate, carrying near-zero marginal allocation information.
```

§11.2 binds: the deployable object is a **BOOK after costs**, not an instrument; a statistically-persistent-
but-uneconomic object is a **NON-FINDING**. Therefore statistical survival (doc 25) is a *necessary gate*,
not a sufficient one. Doc 26 sets the *sufficient* economic gate.

---

## 2. (1) The Exact Economic Decision Habitat Persistence Changes

Adjudicated unanimously across all four lenses (no disagreement on the *decision class*; disagreement is
only on whether the decision carries value — §7).

**Decision class — exactly ONE is admissible:** book-level **UNIVERSE MEMBERSHIP and CAPITAL WEIGHT** on the
MR-strategy sleeve. Nothing else.

```text
UNIT:       per-instrument, per-period: (a) a binary MR-universe membership flag ∈ {0,1}
            ("spread X is in the MR-deployable book this period"), and
            (b) a coarse capital/attention weight w_i ∈ [0,1] on that sleeve (e.g. 3-tier full/half/excluded).
HORIZON:    the persistence horizon h. MUST fall in 1–12 weeks to match the book's holding period,
            AND MUST exceed (classification lag + reallocation horizon) — see §4(a).
REBALANCE:  fixed, pre-registered, SLOW clock (weekly–monthly). NEVER per-bar, NEVER event-triggered.
            Deliberately slow so the object is a regime descriptor, not a trigger.
REPLACES:   the PM's current trailing-vol-clustering / half-life / VR eyeballing of the MR watchlist.
            It formalizes and forward-tilts that SAME membership call.
DOES NOT:   change WHEN the sleeve enters/exits within a selected instrument, NOR direction, NOR per-trade
            size. It is a GATE/THROTTLE upstream of an unchanged, already-validated entry engine.
```

**Critical economic caveat (prosecutor, credited).** This decision is only distinct from *doing nothing* if
(i) the eligible set actually **rotates** period-to-period — a static one-time universe pick needs no
persistence object — AND (ii) the rotation is driven by information **not already captured** by ranking on a
trailing realized-vol regime / half-life / VR at the same rebalance. The decision is real only in the narrow
band where habitat flips **slowly enough to trade but fast enough to matter and cheap enough to capture
better than the 1-line baseline**.

---

## 3. (2) MR-Attempt-Selection Value: Descriptor vs Realized-Profitability Persistence

**Can selection-only value exist without touching timing?** Adjudicated: **YES in principle, but only through
a single conditional bridge, and that bridge is the whole ballgame.**

```text
PERSISTS (what the object measures):   the ENVIRONMENT DESCRIPTOR — a sign-free second-moment/VR regime.
                                       Has NO standalone P&L.
CARRIES P&L (what a trader is paid for): REALIZED MR PROFITABILITY = f(regime present)
                                         × f(entry timing, deviation magnitude, reversion actually captured).
                                         The second factor IS State T — off-limits (§4).
```

The object delivers **only the first factor**. The bridge that converts a descriptor into selection value is
a **stable, positive, allocation-conditioning link**:

> "An MR engine — held FIXED, entry rule unchanged — applied in a persistently-MR-favorable second-moment
> environment delivers higher **period-aggregate net** P&L than the same engine in a non-favorable
> environment, averaged over the period, with NO change to the entry rule."

This is admissible because the entry engine is held constant and the prior only gates *membership/weight*; it
is an **allocation-conditioning claim, not a timing claim**. It is real **if and only if** the descriptor's
persistence empirically forecasts the sleeve's **period-aggregate net Sharpe/return** — not individual-trade
timing.

**The bound on the value (prosecutor + econometrician, decisive).** Selection value is bounded above by the
fraction of cross-instrument MR-P&L dispersion explained by *"regime-present"* versus *"well-timed-entry-
within-regime."* If most MR P&L dispersion comes from entry/deviation capture (likely — the existing engine
already conditions on regime crudely), the descriptor adds near-zero. **Selection-only value is therefore
POSSIBLE but presumptively SMALL, and must be PROVEN incremental, never assumed from the descriptor surviving
its null.** If the descriptor→realized-profitability link is absent, flat, or sign-unstable, selection value
collapses to zero even with `δ_excess > 0` (GAP 1, GAP 3).

---

## 4. (3) Practical-Uselessness Falsifiers (survives the null, still useless)

The full enumerated set on which all four lenses converge. Each fires under a precise condition; any one
firing on OOS cross-habitat data makes the object a NON-FINDING despite `δ_excess > 0`.

```text
(a) NO ACTIONABLE WINDOW  — persistence horizon too short for the slow book to act inside.
    FIRES:  h ≤ classification_lag L + reallocation/turnover horizon T_realloc.
    WHY:    habitat is itself a smoothed estimator needing ~L bars to confirm; if the regime persists only
            ~L bars beyond detection, you reallocate just as it flips. With a 1–12wk book, sub-week measured
            h is the DOMINANT killer.

(b) TRIVIAL LIFT / HIGH BASE RATE  — the descriptor is 'on' almost always.
    FIRES:  conditional lift  P(habitat_{t+h} | habitat_t) − P(habitat_{t+h})  is small in ABSOLUTE terms,
            OR cross-sectional dispersion of the prior < the weight-action resolution (flag rarely flips).
    THRESHOLD: relative lift < ~10–15% (materiality floor) OR absolute eligibility shift < ~5–10pp.
    WHY:    the deployment domain is mean-reverting BY CONSTRUCTION (CLAUDE.md §1.1), so the base rate is
            high by design. If everything is 'in habitat', the prior is a near-constant and selects nothing.
            SECOND most likely killer.

(c) NO INCREMENTAL VALUE vs CHEAP BASELINE  — the single most probable falsifier; the mandatory gate.
    FIRES:  book-level net-of-cost Sharpe/return with the habitat-persistence prior is within OOS noise of
            the SAME book selected by a 1-line trailing realized-vol / OU half-life / variance-ratio filter
            at the same rebalance.
    CONDITION: Δ(net book Sharpe)_{habitat − cheap-baseline} CI includes 0, OOS, cross-habitat.
    WHY:    persistence-of-a-second-moment-regime is exactly what a trailing vol/half-life/VR filter already
            proxies. The surrogate cancels the MECHANICAL autocorrelation but does NOT prove the residual
            beats the cheap DIRECT measure. This is the prosecution's strongest blade and the §1 simplicity
            tiebreak: complex loses to the 1-liner on ties.

(d) TURNOVER COST DOMINANCE  — rotation eats the edge.
    FIRES:  rebalance frequency × avg weight change × round-trip cost (txn + borrow + adverse-excursion-on-
            rotation) > gross selection edge per period.  Worse under estimator chatter near the threshold.
    CONDITION: net edge after rotation cost ≤ 0.
    VISE:   falsifiers (a) and (d) form a vise — slow habitat = no rotation value; fast habitat = turnover
            death. The object lives only in the narrow middle, defended by a hysteresis band.

(e) CAPACITY / BORROW BINDING  — the better set is uninvestable at book size.
    FIRES:  the instruments the prior up-weights are capacity- or borrow-constrained (thin commodity spreads,
            hard-to-borrow RV legs; high-vol regimes often coincide with thin/expensive-to-short spreads).
    CONDITION: realizable size at acceptable cost < required allocation, OR borrow cost > selection edge.

(f) DESCRIPTOR-NOT-PAYOFF  — habitat persists but the descriptor→payoff map is flat/sign-unstable (GAP 1).
    FIRES:  corr(habitat-state, forward cost-aware realized-MR-return) ≈ 0 (or sign-unstable) OOS even though
            habitat autocorrelation is high.
    WHY:    makes a fully significant δ_excess economically VOID. The econometrician weights this highest; it
            is the economic content of GAP 1.
```

---

## 5. (4) Hidden State-T Drift and the HARD FIREWALL (proof-shaped, not a promise)

**Zombie risk is HIGH in likelihood of *attempted* drift, but STRUCTURALLY BLOCKABLE to LOW** under an
output-TYPE firewall. Firewall-Architect and prosecutor concur this is structural, not behavioral.

**The exact drift path (every arrow is a real temptation):**

```text
(1) object emits a per-instrument, per-period persistence PROBABILITY p ∈ [0,1]
(2) p is relabeled "MR habitat CONFIDENCE"                          [semantic creep]
(3) confidence is refreshed "to stay current" → per-bar p_t appears  [clock creep: period → bar]
(4) per-bar p_t crosses a threshold and acquires TENSE:
    "habitat strengthening → MR likely soon"  (banned: favorable-now / imminent / ignition)  [tense smuggled]
(5) p_t is COMPOSED with a deviation/z: "high p_t AND |z| ≥ θ → enter"   [composition with entry trigger]
(6) p_t becomes a per-bar entry-confidence weight on trade size      [full State-T resurrection — DEAD, doc 11]
```

**The firewall — an OUTPUT-TYPE constraint, enforced structurally (type/interface level), making each arrow
TYPE-IMPOSSIBLE rather than merely discouraged:**

```text
F1  TYPE LOCK.        The object may emit ONLY two types: a binary universe-membership flag and a sleeve
                      capital weight w ∈ [0,1]. It is type-FORBIDDEN from emitting any per-bar scalar.
                      ⇒ Blocks (1)→(2)→(3): there is no per-bar probability object to relabel or refresh.
F2  CLOCK LOCK.       It updates ONLY on the fixed pre-registered rebalance clock, never on a bar/deviation
                      event.  ⇒ Blocks (3)→(4): no per-bar p_t can exist to cross a threshold.
F3  TENSE-FREE / SIGN-FREE.  Outputs name a CURRENT-PERIOD eligibility/weight; carry NO tense, NO 'soon',
                      NO sign, NO deviation/z anchoring.  ⇒ Blocks (4): the banned-vocab gate (T-score,
                      hazard, ignition, imminent, favorable-now) is the linguistic tripwire at the artifact
                      level; type carries no field that could hold tense.
F4  COMPOSITION BAN.  Any function whose inputs are (habitat_weight, deviation/z/half-life-from-mean/entry-
                      trigger) is banned at the type-checker level. The entry engine consumes ONLY the
                      membership flag as a hard ON/OFF GATE, never the underlying probability.
                      ⇒ Blocks (5),(6): there is no code path from the persistence output into the per-bar
                      entry function; the product that would form a State-T score cannot be typed.
F5  THROTTLE-NOT-SIZE. The weight throttles GROSS SLEEVE ALLOCATION, never individual-trade size.
                      ⇒ Reinforces (6) block.
```

**Proof shape.** Drift requires, in sequence, (i) a per-bar scalar to exist, (ii) on a bar clock, (iii)
carrying tense, (iv) composed with a deviation. F1 makes (i) untypeable; F2 makes (ii) unreachable; F3 makes
(iii) unrepresentable; F4 makes (iv) un-composable. Each arrow is independently severed at the type level, so
the path 3→6 is not merely discouraged but **structurally impossible**. **If the firewall is only documentary,
treat zombie risk as HIGH.** The moment the output is per-bar, or is AND-ed with a `|z|` condition, it HAS
BECOME State T and must be killed on sight.

---

## 6. (5) Latent-Assumption Challenge: Stable Economic STATE vs Slow Noisy ESTIMATOR

**The decisive attack (econometrician lead, all lenses concur).** "Habitat" as specified is a latent
second-moment regime probability estimated from realized-vol/VR inputs over a memory window — i.e.
**structurally a SMOOTHER**. Three claims must be separated:

```text
(i)   the smoother autocorrelates                         — TRIVIALLY true (any windowed estimator is
                                                            mechanically autocorrelated by construction).
(ii)  the surrogate cancels the mechanical part           — PLAUSIBLE; matched OU/RW/GARCH run through the
                                                            IDENTICAL smoother under identical conditioning
                                                            removes the construction artifact. This is the
                                                            doc-25 admissibility win (CLAUDE.md §11.1 guard).
(iii) the SURVIVING residual is a STABLE ECONOMIC state    — UNPROVEN, and the ONLY thing that matters.
      that moves the MR PAYOFF
```

`δ_excess > 0` establishes the real series has MORE second-moment persistence than the matched null — a
statement about **variance dynamics**. GARCH-style persistence is real, non-tautological, and **routinely
orthogonal to net-of-cost tradeable edge**. So even granting (i)–(ii), the residual is most parsimoniously a
**vol-clustering descriptor** until proven to move payoff. The trader prior (PM lens): a 2-tier trailing
realized-vol / half-life filter captures **80–90%** of any deployable membership signal at near-zero modeling
cost; habitat persistence's marginal contribution is the open question — possibly real, plausibly within noise.

**Therefore the MANDATORY incremental-value test (pre-registrable; the verdict hinges entirely on it):**

```text
Build two selection filters at IDENTICAL horizon h and IDENTICAL slow rebalance:
  FILTER-B (cheap baseline): a 1-parameter direct measure — trailing realized-vol regime OR VR threshold
                             OR OU half-life.
  FILTER-A (treatment):      the habitat-persistence prior, ORTHOGONALIZED against FILTER-B (residual-only,
                             so it cannot win by re-proxying the cheap measure).
Run a FIXED, timing-agnostic, cost-aware MR book through each. Compute book-level net-of-cost return/Sharpe
OOS, cross-habitat.
HABITAT EARNS ITS COMPLEXITY ONLY IF  Δ(net performance)_{A−B} > ~2 SE, OOS, replicated across ≥2 independent
habitats. If A ≈ B (Δ/SE ≤ ~1) → habitat is a more expensive vol filter and is DEMOTED to NON-FINDING.
```

The estimator-vs-state distinction is thus **empirically decidable** and MUST gate any economic claim. A
tie-with-baseline is an explicit NON-FINDING, not a soft pass (§1 simple > complex breaks the tie against the
machinery).

---

## 7. Reconciliation of the Four Lenses (where they disagree, who wins)

```text
LENS                    VERDICT                       ROLE
Trader/PM (lead)        ECONOMICALLY_USEFUL_IF        decisive on usefulness
Useless-Prosecutor      UNDEPLOYABLE                  sets the floor the object must clear
Quant-Econometrician    ECONOMICALLY_USEFUL_IF        sets the incremental-value bar
Firewall-Architect      ECONOMICALLY_USEFUL_IF (+firewall)  sets the binding anti-zombie constraints
```

**Vote: 3 × ECONOMICALLY_USEFUL_IF, 1 × UNDEPLOYABLE.** The disagreement is **not** about the decision class,
the falsifiers, the firewall, or the mandatory incremental test — on all of those the four lenses are
**unanimous**. The disagreement is purely a **prior on the test outcome**: the prosecutor bets the
incremental-vs-cheap-baseline test will fail; the other three withhold that bet and route to the test.

**Adjudication (who wins and why).** The prosecutor's `UNDEPLOYABLE` is a **prediction about an unrun test**,
not a structural impossibility. Per §11.2/§12.1 ("when in doubt, run the test") and §11.3 (empirical probation
before existential verdict), a prediction that the test fails is **not** grounds to refuse the test when the
test is cheap, pre-registerable, and decisive. The prosecutor's substance is **fully absorbed** — it IS the
content of falsifier (c) and the §6 incremental test, which the consensus adopts as a HARD GATE. So the
prosecutor does not lose its argument; it loses only its attempt to pre-empt the verdict. **Consensus verdict:
`ECONOMICALLY_USEFUL_IF`, where the IF is exactly the prosecutor's bar.** The trader lens is decisive on
usefulness and rules the object a *legitimate slow universe/sizing prior with zero standalone P&L*; the
prosecutor and econometrician set the bar (incremental-vs-cheap-baseline, net-of-cost, cross-habitat OOS); the
firewall architect's F1–F5 are adopted as binding deployment preconditions.

---

## 8. TRADER USEFULNESS VERDICT

```text
VERDICT: ECONOMICALLY_USEFUL_IF — true-but-inert by default; deployable ONLY if it clears the bar below.
FOUR-LENS VOTE: 3 ECONOMICALLY_USEFUL_IF / 1 UNDEPLOYABLE (the dissent = a prior the test will fail; absorbed
                as the mandatory incremental gate, not a structural objection).
```

Habitat persistence is a **legitimate slow UNIVERSE-and-SIZING prior** on the MR book with **zero standalone
P&L**. It is economically useful **if and only if** it beats a cheap realized-vol / half-life / VR selection
filter **incrementally, net-of-cost, replicated across ≥2 independent habitats OOS**, with a measured
actionable window and material conditional lift. Absent that proof it is **true-but-inert** — an expensive
re-derivation of vol-clustering and a NON-FINDING regardless of `δ_excess > 0`. It must be **type-locked to
period-level universe/weight** (F1–F5) to keep it out of dead State-T timing.

---

## 9. ZOMBIE-STATE-T RISK ASSESSMENT

```text
RISK LEVEL:   HIGH attempted-drift likelihood; reducible to LOW only under structural firewall F1–F5.
              If firewall is documentary-only → HIGH (treat as live zombie).
DRIFT PATH:   per-period probability → "confidence" → per-bar refresh → tense ("MR likely soon") →
              composed with |z| entry trigger → per-bar entry-confidence size  (= State T, DEAD doc 11).
ONE-LINE FIREWALL:  the object emits ONLY a slow, per-period {membership flag, sleeve weight}, type-forbidden
              from any per-bar scalar and structurally un-composable with any deviation/z/entry trigger —
              consumed solely by the universe/sizing layer, with no code path into the per-bar entry function.
```

---

## 10. MINIMAL DEPLOYABILITY CRITERION (smallest sufficient set)

All must hold; failure of any one ⇒ NON-FINDING:

```text
D1  WINDOW:        h_net = h − classification_lag − reallocation_horizon > 0, with h ∈ 1–12 weeks
                   (pre-registered) — a provable actionable window for the slow book.            [kills (a)]
D2  MATERIAL LIFT: conditional lift  P(habitat_{t+h}|habitat_t) − P(habitat_{t+h})  clears a pre-set
                   materiality floor (≥ ~10–15% relative, or ≥ ~10pp absolute eligibility shift), so the
                   flag actually discriminates in a domain that is mean-reverting by construction. [kills (b)]
D3  INCREMENTAL:   net-of-cost book-level improvement of the habitat-persistence prior over the cheap
                   1-line vol/half-life/VR baseline is significant on the ORTHOGONALIZED component, OOS,
                   REPLICATED across ≥2 independent habitats (argmax-over-windows reporting disqualifying).
                                                                                          [kills (c),(f),smoother]
D4  TURNOVER:      net edge survives rotation cost (txn + borrow + adverse excursion) at the realized
                   habitat-flip frequency, with a hysteresis band to suppress threshold chatter.  [kills (d)]
D5  CAPACITY:      up-weighted eligible instruments have enough capacity/borrow to absorb book-size capital
                   at acceptable cost.                                                              [kills (e)]
D6  TYPE LOCK:     output type-locked to period-level {membership, weight}; firewall F1–F5 enforced
                   structurally BEFORE any deployment.                                          [kills zombie]
```

---

## 11. EXACT ECONOMIC SUCCESS / FAILURE CONDITION (pre-registerable)

Selection-only · net-of-cost · cross-habitat OOS · incremental-vs-cheap-baseline. **Frozen on publication.**

```text
SETUP. Fix ONE entry/exit MR engine E (UNCHANGED across all arms — this guarantees selection-only, no timing
       change). Build a BOOK over a pre-registered cohort of habitats. All P&L net of transaction cost,
       borrow, capacity-capped impact, with realized rotation cost charged on EVERY membership flip.

  ARM B (cheap baseline):  E with universe-membership/weight set by a 1-line trailing realized-vol regime
                           OR OU half-life OR variance-ratio filter, at the fixed slow rebalance.
  ARM A (treatment):       E with universe-membership/weight set by the habitat-persistence prior
                           ORTHOGONALIZED against ARM B's baseline (residual-only; cannot win by re-proxying
                           the cheap measure). Same horizon h, same rebalance clock, F1–F5 enforced.
  ARM C (control):         E with flat/uniform allocation (sanity floor).

DEFINE  Δ = net-of-cost book risk-adjusted return/Sharpe(ARM A) − (ARM B), computed OUT-OF-SAMPLE on
        instruments/regimes DISJOINT from any used to specify the prior.

ECONOMIC VALUE PRESENT  iff  ALL of:
   • Δ > 0 AND its bootstrap CI excludes 0 after FWER/multiplicity correction across ALL pre-registered
     windows/cohorts (report the FULL search surface, NOT the argmax);
   • directionally consistent and REPLICATED across ≥2 pre-registered INDEPENDENT habitats (cross-habitat OOS
     is the unit of evidence, §11.7);
   • Δ exceeds the rotation/turnover cost it induces (D4) AND the up-weighted set is executable within
     capacity/borrow (D5);
   • ARM A's advantage over ARM C is NOT fully explained by ARM B (the orthogonalized component is non-null).

ECONOMIC VALUE ABSENT  iff  ANY of:
   • Δ CI includes 0 (Δ/SE ≤ ~1)  — TIE-WITH-BASELINE IS AN EXPLICIT NON-FINDING, not a soft pass;
   • Δ fails to replicate across habitats, or reverses sign OOS;
   • turnover / borrow / capacity cost consumes Δ;
   • the orthogonalized component is null (all lift was the cheap baseline).

CONTAMINATION VOID: no metric in this test may reference entry timing, deviation, or sign. If it does, the
       test is State-T-contaminated and VOID.

PRE-REGISTERED KILL TRIGGER: incremental edge insignificant or non-replicating across habitats OOS
       ⇒ habitat persistence is a NON-FINDING for the book regardless of δ_excess > 0.
```

---

## 12. How This Gates Doc 25's STEP 0

Doc 25 froze a STATISTICAL protocol (STEP 0 instrument check → STEP 5 cross-habitat verdict) that decides
whether `δ_excess > 0`. **Doc 26 changes whether — and in what form — running that protocol is worth the
effort, by adding an ECONOMIC pre-registration ABOVE it.**

```text
WHAT CHANGES.  The doc-25 statistical run is now JUSTIFIED ONLY as an INPUT to the economic test of §11, never
               as a terminal deliverable. A standalone δ_excess > 0 is, by this adjudication, economically
               inert until §11 is run. Per §11.2 (deployable object = book after costs; persistent-but-
               uneconomic = NON-FINDING), proving δ_excess > 0 WITHOUT a committed path to §11 produces a
               NON-FINDING and is low-value effort (§12.1: avoid theory loops with no posterior consequence).

ECONOMIC PRE-REGISTRATION TO ADD BEFORE STEP 0 (frozen with this doc):
  E0  CHEAP-BASELINE FREEZE.  Specify the exact 1-line baseline (which of realized-vol regime / OU half-life /
      VR; its single parameter; its rebalance) BEFORE the data is touched. The baseline is the bar; it must be
      named first so habitat cannot be tuned to beat a moving target.
  E1  FIXED ENGINE FREEZE.    Specify the fixed timing-agnostic cost-aware MR engine E and its cost model
      (txn, borrow, capacity caps, rotation charge) BEFORE STEP 0.
  E2  HORIZON/REBALANCE GRID. Pre-register h-grid (∈ 1–12wk) and the slow rebalance clock; commit that the
      ECONOMIC horizon used in §11 EQUALS the statistical h whose δ_excess(h) curve doc-25 STEP 4 produces.
  E3  HABITAT/COHORT SPLIT.   Pre-register the ≥2 independent OOS habitats and the disjoint calibration cohort,
      SHARED between the doc-25 statistical run and the doc-26 economic run (same disjointness discipline).
  E4  ORTHOGONALIZATION RULE. Freeze how the habitat prior is orthogonalized against E0 (residual-only) so it
      cannot win by re-proxying the cheap measure.
  E5  TYPE-LOCK / FIREWALL.   Commit F1–F5 as the output contract of any habitat object STEP 0 produces, so the
      statistical artifact cannot later be re-typed into a per-bar State-T score.

GATING RULE.  STEP 0 (and the doc-25 STEP 1–5 statistical run) remains authorized to proceed ONLY once E0–E5
              are frozen. The §11.8 real-data positive control (doc-25 STEP 0/F6 + STEP 3) is REINFORCED, not
              replaced: an apparatus that cannot CONFIRM a known real reverter cannot be trusted to have NOT
              found economic value — and now must also confirm that known reverter delivers ECONOMIC (net-of-
              cost) lift over the cheap baseline, else the economic apparatus is too blunt and is recalibrated,
              not the market (§11.8).
```

Net: doc 26 **does not block** the doc-25 run; it **re-prices** it — the run is worth doing **iff** it is the
first stage of the §11 economic test, with E0–E5 frozen beforehand. A purely statistical run with no economic
follow-through is now classified low-value.

---

## 13. Surviving Uncertainty · Explicit Non-Conclusions · Next Action

**Surviving uncertainty:**

```text
- The sign/magnitude of the descriptor→realized-profitability link (GAP 1 / falsifier (f)) is UNKNOWN and is
  the single largest determinant of economic value. Untested.
- Whether the measured persistence horizon h lands in the actionable band (D1) on near-unit-root real legs is
  unknown until doc-25 STEP 2 measures L.
- Whether the cheap baseline captures 80–90% (PM prior) or less of the deployable signal is the open empirical
  question §11 exists to answer.
- Capacity/borrow on the eligible commodity-spread / cross-asset RV set (D5) is data-gated and unmeasured.
```

**Explicit non-conclusions:**

```text
- This document does NOT conclude habitat persistence HAS economic value. It rules the value DECIDABLE and
  freezes the economic test + the bar (cheap baseline) it must clear.
- It does NOT authorize any empirical run, STEP 0, code, detector, signal, or deployment.
- It does NOT relax the State-T firewall: forward price-reversal / timing / entry-confidence remains DEAD.
- A single-habitat economic positive, should one appear, is explicitly NOT confirmation.
- 'Beats the surrogate' (δ_excess > 0) and 'beats flat/ARM-C' are NECESSARY but NOT SUFFICIENT; only beating
  the cheap baseline (ARM B) net-of-cost OOS cross-habitat is decisive.
```

**Next highest-information action:**

```text
Freeze the economic pre-registration E0–E5 (§12) — specifically NAME the cheap baseline (E0) and the fixed
cost-aware engine E (E1) — as the precondition that unlocks doc-25 STEP 0. Record the verdict
ECONOMICALLY_USEFUL_IF (+ its bar) and the firewall F1–F5 in HYPOTHESIS_REGISTRY.md. Do NOT run anything until
E0–E5 are frozen.
```

---

*End of doc 26. Economic adjudication frozen 2026-06-04. No empirical execution authorized. Gates doc 25 STEP 0
behind economic pre-registration E0–E5.*
