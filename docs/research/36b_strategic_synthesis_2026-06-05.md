# Strategic Synthesis — Weekly Research Council Frame

**Date:** 2026-06-05. **Mode:** Posterior review + priority assessment.
**Covers:** BRN calendar verdict (doc 36) + ZC/crack-β staging + programme dependency graph.
**Governing frame:** §11 (trader-constrained, rolling-local), §12 (execution doctrine), §13 (workflow G cadence).

---

## 1. What Was Decided This Session

| Action | Outcome | Confidence |
|---|---|---|
| BRN M1-M2 calendar test executed (doc 36) | MERELY-TRUE | HIGH |
| BRN four-lens adjudication (Phase 2) | Convergent: STRUCTURAL+MEASUREMENT+METHODOLOGY | HIGH |
| ZC prereg frozen (zc_calendar_prereg.md) | FROZEN — ready to execute | — |
| Crack-β readiness memo (doc 36a) | Spec admissible; execution prereg MISSING | — |

---

## 2. Programme Dependency Graph — Current State

```
APPARATUS (doc 21 - positive control)
    │ CONDITIONAL SURVIVAL — passes power + selectivity + calibration
    ↓
CONSTRUCTION ADMISSIBILITY
    │ β=1 DEFINITIONAL: ADMISSIBLE (doc 20/21) — calendars, same-unit spreads
    │ β=ESTIMATED (controlled): UNTESTED — doc 30 spec; execution prereg MISSING (KEYSTONE)
    │ rolling-OLS-β: INADMISSIBLE (doc 19) — zombie-prohibited
    ↓
CALENDAR INSTRUMENTS (β=1 definitional)
    │ NG: PERSISTENT-BUT-UNECONOMIC (doc 23) — real MR, sub-cost, not deployable alone
    │ BRN: MERELY-TRUE (doc 36) — real MR, HL=107 bars, OOS degradation, energy tail-correlated
    │ ZC: PREREG FROZEN — execute next; first non-energy candidate
    │ (Doc 33 carry/seasonal layer: ungated but NG1!/NG2! still pending)
    ↓
COHORT BREADTH (doc 25)
    │ Currently: 0 cost-clearing sleeves (NG+BRN both merely-true)
    │ Gate: ≥2 INDEPENDENT cost-clearing sleeves needed for book netting
    │ Independence: NG+BRN fail (energy tail correlation confirmed)
    │ ZC MIGHT provide first non-energy sleeve (diversification candidate)
    │ controlled-β pairs WOULD provide breadth if admissible (gated on keystone)
    ↓
PORTFOLIO / BOOK (doc 25)
    │ GATED — no admissible cohort yet
    │ Unlocks: ZC confirms cost-clearing + ≥1 more independent sleeve
    ↓
DEPLOYMENT
    STATUS: NOT REACHABLE on current evidence
```

---

## 3. Posterior Update

### Prior (before BRN)
- P(deployable book reachable) estimated LOW-MEDIUM (20-30%) based on NG MERELY-TRUE and the programme's structural strength (real MR confirmed, apparatus validated).

### Evidence from BRN (doc 36)
- **STRENGTHENS:** Storage MR hypothesis confirmed cross-instrument (NG + BRN both real). Apparatus confirms power. The "merely-true" pattern is consistent and interpretable.
- **WEAKENS:** Energy calendars are co-correlated sleeves (independence requirement fails). The unconditional form is now demonstrably not the deployment path. OOS degradation in BRN (post-2012 financialization) suggests the calendar MR was partly regime-specific in the pre-shale era.
- **NET:** Storage MR hypothesis credibility HIGHER; deployment probability via energy calendars LOWER. The signal is real; the access route is different from what was originally assumed.

### Posterior (after BRN)
- P(deployable book reachable via energy calendars alone) = **VERY LOW** (<5%). NG and BRN together are not an independent pair.
- P(deployable book reachable if ZC confirms AND is independent of energy) = **LOW-MEDIUM** (15-25%). ZC + NG/BRN with low crisis correlation would give a 2-sleeve basis, but still requires cost-clearing.
- P(programme reaches deployment via controlled-β pairs if ZC also fails) = **MEDIUM** (30-45%). The crack-β keystone is designed precisely for this scenario — if definitional calendars cannot field a cost-clearing book, estimated-β pairs (with proper construction) are the remaining route.
- P(deployment completely unreachable — all routes fail) = **LOW-MEDIUM** (15-20%). The apparatus is validated; real MR exists across instruments; the cost problem is structural, not instrument-specific. Controlled-β may solve it.

### Overall assessment
P(deployable cost-clearing book is reachable via some path within the programme) = **MEDIUM** (~45-55%). The programme's signal detection is working; the economic threshold is the unsolved problem. BRN does not change this materially — it confirms the known pattern.

---

## 4. Energy Calendar Thesis — What BRN Tells Us

**The energy calendar thesis in unconditional form is closed.** Two independent instruments (NG, BRN) have now returned consistent MERELY-TRUE verdicts:

| Instrument | VR(20) | p_rw | Global HL | Ex-crisis gross | Verdict |
|---|---|---|---|---|---|
| NG (doc 23) | ~0.45 | 0.005 | 12.9 bars | +0.0004 $/MMBtu | PERSISTENT-BUT-UNECONOMIC (sub-cost) |
| BRN (doc 36) | 0.282 | 0.002 | 106.8 bars | +0.129 $/bbl | MERELY-TRUE (HL outside band; energy-correlated) |

**Pattern:** Both instruments show strong sub-diffusion vs martingale nulls. Neither is deployable. The failure modes differ (NG: gross doesn't clear costs; BRN: HL too long, OOS degradation, energy correlation), but the deployment verdict is the same.

**What this means for the programme:**
- The unconditional energy calendar IS NOT the deployment vehicle. Confirmed.
- The EIA conditional path (doc 33/34) was tested and KILLED for NG. BRN conditional form is not yet tested (would require a new prereg on post-2012 data only, at $0.03/bbl cost).
- The energy calendar MR signal is real and may be harvestable with better conditioning or book construction (higher frequency, different entry logic, position sizing). But those are new pre-registrations.

**ZC now carries the diversification thesis.** If ZC fails, the energy-only calendar programme effectively closes, and the controlled-β keystone (crack spread) becomes the last internally-funded route to portfolio breadth.

---

## 5. Ranked Next Actions for Following Session

**Priority 1 (IMMEDIATE, HIGH leverage):** Execute ZC calendar prereg
- Script: adapt `run_brn_calendar_test.py` for ZC paths
- Data: confirmed ready (8,796/8,805 bars, 1991–2026)
- Verdict: ZC SLEEVE_CANDIDATE → programme pivot to portfolio test; ZC MERELY_TRUE → calendar thesis closed; ZC DEAD_CALENDAR → focus shifts entirely to crack-β
- Why now: fastest path to closing or confirming the calendar thesis. No new infrastructure.

**Priority 2 (THIS SESSION or next, HIGH strategic leverage):** Write crack-β execution prereg
- Extends doc 30 with: HO2!-CL2! as pair, frozen hyperparameters (F1: q_beta=0.0001, F2: λ=10 target=1.0, F3: W=500), τ=0.10, no-manufacture band [0.85, 1.15]
- Do NOT execute until frozen
- Why now: this is the keystone — the sooner it's frozen, the sooner implementation can begin

**Priority 3 (AFTER ZC verdict):** Implement §3 B1–B5 (crack-β analytics module)
- ~200-270 lines additive, reusing frozen apparatus
- Only after execution prereg is frozen

**Priority 4 (LOW, gated):** NG back-adjustment closure
- Reopens the "back-adj not cleanly excluded" caveat on the NG MERELY-TRUE verdict
- Does NOT change deployment status (sub-cost regardless of back-adj)
- Low priority until ZC/crack-β results are in

---

## 6. What If ZC Also Returns MERELY-TRUE?

If ZC fails the economic gate (which is plausible — similar sub-cost dynamics), the programme reaches a clear crossroads:

```
ALL THREE CALENDARS: NG + BRN + ZC = MERELY-TRUE
    ↓
Calendar thesis: CLOSED in unconditional definitional form
    ↓
Doc 25 cohort is empty (0 cost-clearing sleeves)
    ↓
Deployment route narrows to:
  (A) Controlled-β pairs (crack spread, doc 30) — the keystone test
  (B) Conditional calendar forms (new pre-registrations with different conditioning variables)
  (C) EIA surprise / flow-based variable for NG (doc 34 non-conclusion: untested)
```

**Honest verdict if this happens:** the programme should explicitly state that β=1 definitional calendars are a **REAL-BUT-UNECONOMIC** asset class in unconditional form, and pivot to (A) as the primary route. This is not a failure — it is a clear empirical finding that re-prices the deployment thesis.

---

## 7. Continuation State for Next Session

### What is decided (FROZEN)
- BRN M1-M2 unconditional: MERELY-TRUE (HIGH confidence). Energy tail-correlated with NG. Not a portfolio sleeve.
- NG + BRN energy calendar unconditional form: CLOSED as deployment vehicle.
- ZC prereg: FROZEN and ready to execute (zc_calendar_prereg.md).
- Crack-β: doc 30 specification admissible; execution prereg MISSING (next deliverable).

### What is frozen-and-ready-to-run
1. **ZC calendar test:** Run `run_brn_calendar_test.py` adapted for ZC paths. Data: `CBOT_DL_ZC1!, 1D.csv` + `CBOT_DL_ZC2!, 1D.csv`. Follow the prereg exactly.
2. **Crack-β implementation:** After execution prereg is written.

### Single next action
**Execute ZC calendar test.** Adapt `run_brn_calendar_test.py` for ZC paths. This is 20 minutes of work and produces the most information per unit effort currently available.

---

*This document constitutes the weekly-council strategic synthesis for the session of 2026-06-05.*
*Append-only record. Prior beliefs preserved. No revisionist history.*
