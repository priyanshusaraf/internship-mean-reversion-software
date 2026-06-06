# Doc 38b — Reconciliation & Weekly Research Council Synthesis

**Date:** 2026-06-05 (extended session). **Mode:** Posterior review (§12, workflow G cadence).
**Covers:** ZC verdict (doc 38), crack-β synthetic gate (doc 37), back-adj diagnostic (doc 38a).
**Folds in:** BRN verdict (doc 36), track interdependencies, programme dependency graph.

---

## 1. Calendar Thesis — Formal Closure

**The unconditional daily storage calendar thesis is CLOSED.**

| Instrument | Raw mean_z | Verdict | Primary failure mode |
|---|---|---|---|
| NG (vendor spread, 2006+) | -0.581 | PERSISTENT-BUT-UNECONOMIC | Sub-cost (gross +0.0004 vs cost 0.003); back-adj unresolved (≈frac0.25 anchor) |
| BRN (raw legs, 1997+) | **+0.259** | MERELY-TRUE | Raw signal TRENDING — entire VR from deseason artifact; HL=107 bars |
| ZC (raw legs, 1991+) | -0.315 | **CONTAMINATED_RESULT** | Deseason amplification 4.5×; p_ou=0.002 artifact fingerprint; HL=315 bars; OOS VR=0.920 |

**Formal declaration (programme record):**
> The unconditional β=1 definitional daily storage calendar, constructed from vendor back-adjusted
> continuous futures and tested with causal deseasonalization, is **not a deployable book** on any
> of the three tested instruments (NG, BRN, ZC). The direction is CLOSED in this form.
> Reopen requires: exchange-native (non-back-adjusted) prices + OOS-only test + explicit contamination
> control + a new pre-registration passing the §4 zombie-reopen test.

**What this does NOT mean:**
- It does NOT mean storage MR is absent in physical markets.
- It does NOT mean NG's raw genuine sub-diffusion (-0.581) is invalid — NG MR is real, just undeployable in the tested form.
- It does NOT close conditional forms (EIA-conditional was separately killed; seasonal filtering is untested with clean data).

---

## 2. Back-Adjustment Finding — Programme-Wide Implication

**The causal deseasonalization step amplifies apparent MR by 2.5-4.5× across all tested instruments by removing back-adjustment level offsets, not genuine seasonal patterns.**

| Spread | Spread mean (back-adj artifact) | Deseason amplification | Implication |
|---|---|---|---|
| NG | ≈ zero | 2.6× | Genuine raw MR; amplification is real seasonal exposure removal |
| BRN | -7.186 $/bbl (large) | Sign flip: +0.259 → -0.699 | No genuine raw MR; entirely artifact-driven |
| ZC | 202.5 cents (huge) | 4.5×: -0.315 → -1.413 | Marginal genuine raw MR; heavily contaminated |

**Diagnostic rule for future instruments (FROZEN as programme standard):**
- Before running VR on any back-adjusted continuous futures spread, compute the raw spread mean.
- If |raw spread mean| > 0.5 × spread std → HIGH contamination risk; require raw-spread corroboration.
- If deseason amplification > 3× → signal is primarily construction artifact; do not report as confirmed MR.

**NG remains the only instrument with confirmed genuine raw sub-diffusion in the calendar programme.**

---

## 3. Crack-β Synthetic Gate — Key Findings

**Gate passed for F5 (pre-sample OLS) and F6 (economic anchor β=1).**

| Family | Gate | Key finding |
|---|---|---|
| F6 (β=1, frozen) | ADMISSIBLE ✓ | Zero f_βupdate; baseline reference; confirms positive control |
| F5 (pre-sample OLS, frozen) | **ADMISSIBLE ✓** | Zero f_βupdate during test; confirms OU; passes all Z controls |
| F1 (Kalman, q=0.0001) | INADMISSIBLE ✗ | Overabsorbs OU into β (VR=0.058 on positive control!); f_βupdate=0.46-0.49 |
| F3 (long-window OLS, W=500) | INADMISSIBLE ✗ | WORSENS artifact: VR=11.4 on Z2 stress null; f_βupdate=0.64 |
| F2 (Ridge, λ=10, W=126) | INADMISSIBLE ✗ | Passes Z1 but catastrophic on Z2 (VR=11.7, f_βupdate=0.75) |

**The key structural finding:** Only FROZEN β (zero update during test) is admissible. Any β that updates during the test period generates the doc-19 artifact when B is strongly trending. The prior assumption "long window = less artifact" is FALSIFIED — large W on trending legs generates MORE super-diffusion, not less.

**The scientific contribution of F5:** Pre-sample OLS — estimate β once on a pre-sample window, then freeze. This is the only non-trivial admissible β construction. If F5 confirms on real HO2!-CL2! data, it opens a new class: "estimated-once frozen-β spreads" that can be applied to any pair where the cointegrating relationship is stable enough to learn in a pre-sample.

---

## 4. §11.8 Positive Control — URGENT STATUS

**MANDATORY GATE (CLAUDE.md §11.8, standing):** "Before any further negative/kill is credible, the apparatus must demonstrate it can CONFIRM a known, literature-documented, economically-anchored REAL edge."

The three calendar kills (NG, BRN, ZC) are only apparatus-validated after the crack-spread positive control confirms. This gate has NOT been cleared on real data.

**Current status:**
- Synthetic gate: CLEARED for F5 + F6 (doc 37)
- Real-data execution: NOT YET RUN — this is the blocking next action

**If crack-β F5 confirms on HO2!-CL2!:** The apparatus has power to detect a real edge on an estimated-β pair. All three calendar kills are apparatus-validated. The deployment domain opens to frozen-β estimated-once pairs.

**If crack-β F5 fails on HO2!-CL2! (despite synthetic gate passing):**
- The pair may genuinely lack deployable MR at daily frequency — this is a legitimate market finding.
- BUT: if both F5 AND F6 fail (β=1.0 on normalized crack spread also fails), then the apparatus may be insufficiently powerful for this instrument/frequency, requiring recalibration.

---

## 5. Dependency Graph — Current State

```
APPARATUS (doc 21 - conditional survival)
    │
    ├── β=1 DEFINITIONAL (admissible)
    │       ├── NG: PERSISTENT-BUT-UNECONOMIC (raw genuine, sub-cost)
    │       ├── BRN: MERELY-TRUE (raw trending, deseason artifact)
    │       └── ZC: CONTAMINATED_RESULT (deseason artifact, HL=315)
    │               ↓
    │       CALENDAR THESIS: FORMALLY CLOSED (unconditional daily form)
    │
    └── CONTROLLED-β (Cycle 2 — synthetic gate CLEARED for F5/F6)
            ↓
    §11.8 POSITIVE CONTROL (BLOCKING — must run next)
    HO2!-CL2! F5+F6 real-data test
            ↓ (if confirms)
    DEPLOYMENT DOMAIN OPENS to estimated-once frozen-β pairs
            ↓
    COHORT BREADTH, PORTFOLIO, BOOK (doc 25)
```

---

## 6. Posterior Update

### P(deployable book reachable)

| Route | Prior (this session start) | Posterior (now) | Driver |
|---|---|---|---|
| Energy calendar unconditional | VERY LOW (<5%) | DEAD — CLOSED | NG+BRN MERELY-TRUE confirmed |
| Grain calendar unconditional | LOW-MEDIUM (~15-25%) | DEAD — CLOSED (CONTAMINATED_RESULT) | ZC contamination confirmed |
| Crack-β F5+F6 on HO2!-CL2! real data | MEDIUM-HIGH (40-60%) | MEDIUM (40-55%) | Synthetic gate cleared; real data pending |
| Conditional calendar (new prereg, clean data) | LOW-MEDIUM (~10-15%) | LOW (~5-10%) | Back-adj contamination discovered; low priority |
| Any path to deployable book | MEDIUM (~45-55%) | MEDIUM (~40-50%) | Calendar routes closed; crack-β now critical |

**The programme sits entirely on the crack-β keystone.** Calendar routes are exhausted. Conditional forms are speculative and low priority. The only active high-evidence path is F5/F6 on HO2!-CL2!.

---

## 7. Ranked Next Actions

1. **[IMMEDIATE, CRITICAL] Execute crack-β F5+F6 on HO2!-CL2! (the §11.8 positive control)**
   - Data: HO2! (7,006 bars 1998+), CL2! (9,230 bars 1989+) — both confirmed available
   - Normalize: A_barrel = HO2! × 42, B_barrel = CL2!
   - F6: β=1.0 (economic anchor); F5: OLS on first 25% of data, frozen thereafter
   - Apply the frozen pre-reg (crack_beta_execution_prereg.md) exactly
   - This is the SINGLE NEXT ACTION for the following session

2. **[AFTER CRACK-β RESULT] Portfolio/book test**
   - Only if F5 or F6 confirms on real crack spread
   - Unlock cohort breadth; test netting arithmetic

3. **[LOW PRIORITY, gated]** NG back-adjustment closure (splice diagnostic on actual ng12 seams)
   - Does not change deployment status; resolves the frac0.25 ambiguity
   - Run only after crack-β result is in

4. **[VERY LOW PRIORITY]** ZC/BRN conditional forms with exchange-native data
   - Speculative; requires new pre-registration and data sourcing
   - Only if crack-β yields permanent demotion (no remaining path)

---

## 8. Continuation State for Next Session

### What is decided (FROZEN)
- NG: PERSISTENT-BUT-UNECONOMIC (genuine raw MR, sub-cost, deseason ambiguous)
- BRN: MERELY-TRUE (raw trending, deseason artifact, HL=107, energy correlated)
- ZC: CONTAMINATED_RESULT (deseason artifact, HL=315, OOS random walk)
- CALENDAR THESIS: FORMALLY CLOSED for unconditional daily β=1 form
- Back-adj: deseasonalization amplifies apparent MR 2.5-4.5× via level-offset removal
- Crack-β synthetic gate: F5+F6 ADMISSIBLE; F1+F2+F3 INADMISSIBLE
- Long-window OLS on trending legs: FALSIFIED as "less artifact" — WORSENS the doc-19 mechanism

### Frozen and ready to run (next session)
**crack_beta_execution_prereg.md (frozen)** — execute on HO2!-CL2!:
```python
# Key parameters (from execution prereg)
A_barrel = HO2! * 42  # normalize to $/bbl
B_barrel = CL2!       # already $/bbl
DATE_MIN = "1998-07-19"  # both legs available
F6_beta = 1.0 (fixed throughout)
F5_beta = presample_ols_beta(A, B, pre_sample_fraction=0.25)  # from analytics_arm_a_v2_beta.py
tau = 0.10, no_mfg_band = (0.80, 1.20)
# Verify f_betaupdate < 0.10 on real data (should be 0.0 for both F5 and F6)
```

### Single next action
**Execute F5 and F6 on real HO2!-CL2! data using the frozen execution prereg.**

---

*Reconciliation doc frozen: 2026-06-05. Covers the full extended execution run (ZC + back-adj + crack-β synthetic gate + strategic synthesis). Append-only record.*
