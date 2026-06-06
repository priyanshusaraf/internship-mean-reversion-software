# BRN M1–M2 Daily Calendar — FROZEN Pre-Registration

**Document class:** Permanent AMR pre-registration (institutional memory — frozen before any result).
**Date:** 2026-06-05. **Mode:** Trader-discovery (§11.2). **Status:** FROZEN — no redesign after this line.
**Supersedes:** nothing. **Extends:** doc 33 (BRN unconditional cell, §1), doc 35 (BRN execution prep),
doc 22 (pooled mean-z rolling frame). **Inherits binding:** doc 14 (rolling artifact guards), doc 23
(z-entry trade proxy, pooled rolling-local), doc 25 (cost-aware ledger), CLAUDE.md §11 (Tier-1/2 gates,
crisis-year isolation, full-search reporting).

> **Objective (the only one):** determine whether the β=1 BRN1!−BRN2! daily calendar is a
> **cost-clearing, deployable second sleeve** — or merely-true (statistically real but sub-cost) —
> or a dead calendar (no MR signal). One verdict, no argmax, no post-hoc tuning.

> **Zombie clearance (§4).** BRN unconditional cell was listed in doc 33 as confirmatory (§1,
> UNCONDITIONAL ONLY). This pre-registration executes that cell with the full Tier-1 + Tier-2
> gate apparatus. It does NOT add new cells, seasonal splits, or conditioning beyond what is
> frozen here. No State-T connections; no predictive claims; observational + book-sim only.

---

## 0. Data Coverage — Pre-Registration Scoping Audit

> *Scoping only — no statistical result. Performed before freezing parameters.*

| Leg | Bars | First bar | Last bar | Source |
|---|---|---|---|---|
| `ICEEUR_DLY_BRN1!, 1D.csv` | 7,341 | 1997-10-22 | 2026-06-04 | `data/raw/more-mean-reversion-data/` |
| `ICEEUR_DLY_BRN2!, 1D.csv` | 8,872 | 1991-10-03 | 2026-06-04 | `data/raw/more-mean-reversion-data/` |

**Overlap start:** 1997-10-22 (BRN1! determines the binding start).
**Usable daily bars (inner join, estimated):** ~7,340 — comfortably above the 2,000-bar minimum for
reliable VR(q) at q=60 and N=500 surrogate runs.

**Pre-registration date range (FROZEN):**
```
DATE_MIN = 1997-10-22
DATE_MAX = 2026-06-04
```

No data was examined for price levels, spread distribution, or VR at any point prior to this freeze.
Scoping was limited to row count and timestamp range only.

---

## 1. Hypothesis (FROZEN — one line)

> The β=1 definitional BRN1!−BRN2! daily calendar spread is a **cost-clearing, tradeable MR sleeve**
> at the institutional cost floor (K = 0.005 in spread-return units) with a half-life in the tradeable
> band — **or it is merely-true / a non-finding**.

**Merely-true definition (FROZEN):** VR confirms sub-diffusion at p_rw ≤ 0.05 (N=500), but pooled
gross expectancy per trade does not clear K = 0.005 after the rolling-local book sim. Statistically
real MR that a trader cannot monetize is a non-finding for portfolio purposes (doc 25 ledger).

**Dead calendar definition (FROZEN):** p_rw > 0.20 at N=200 (speed-gate kill) or VR(20) ≥ 1.0 globally.

---

## 2. Construction (FROZEN)

```
SPREAD:        S_t = close(BRN1!)_t − close(BRN2!)_t           [β=1, definitional; no hedge-ratio estimation]
LEG SOURCE:    daily settlement bars only — no intraday resampling
JOIN:          UTC date index, inner join (both legs present required)
DESEASONALIZE: causal trailing month-of-year mean (same as NG positive control, doc 20/21)
ROLL MASK:     ADR_003 roll_transition_mask, frozen k = 8.0 (causal MAD-based jump filter)
VR TYPE:       level-difference VR (same as the frozen Arm A v2 apparatus)
PRIMITIVES:    analytics_arm_a.py / analytics_arm_a_v2.py — reused AS-IS; do NOT modify
```

**Units note:** BRN spreads are priced in USD/bbl. Costs are expressed in the same spread-return units
as doc 23 (fractional daily returns of the spread). Cost grid {0.003, 0.005, 0.008} references these
fractional units, consistent across the AMR programme.

**Construction integrity (FROZEN):**
- Do not substitute the 60m BRN2! leg (4 years only, resampled intraday ≠ daily settlement).
- Do not modify roll-masking k without a new pre-registration.
- Do not apply any detrending, HP-filtering, or Kalman smoothing to the spread before VR.

---

## 3. Gate Architecture (FROZEN — Tier-1 and Tier-2 run in the same pass)

Two co-primary gates. **Both must pass for SLEEVE verdict.** Either alone failing produces
MERELY-TRUE or DEAD CALENDAR.

### Gate Tier-2 (QUANT) — surrogate-relative VR(q)

**Primary surrogate (HEADLINE):** RW (random walk, iid Gaussian residuals).
**Secondary surrogates (HEADLINE, non-gating reference):** GARCH(1,1); MA(1)-noise.
**Reference (non-gating, for interpretability):** OU process calibrated from the data half-life.

**Q grid (FROZEN):** {5, 10, 20, 40, 60}. **Primary statistic:** VR(20) — ≈1 calendar month.

**Speed gate — N=200:**
- Kill immediately if: p_rw(VR(20)) > 0.20 at N=200.
- Rationale: p_rw > 0.20 at N=200 cannot reach p_rw ≤ 0.05 at N=500 with any reliable margin.
  Stop work; do not escalate to N=500.

**Full test — N=500 (only if speed gate passes):**
- Significance threshold: p_rw(VR(20)) ≤ 0.05 required for QUANT gate PASS.
- p_rw ∈ (0.05, 0.20]: QUANT gate BORDERLINE — report with caution flag; TRADER gate may still kill.
- VR profile must be reported across full q grid {5,10,20,40,60} — the full search, not the argmax.

**SEED (FROZEN):** 20260604. Same across all surrogate runs in this pre-registration.

**OOS split (FROZEN):** First 70% of overlapping bars (by date) = training; final 30% = OOS.
VR(20)_OOS reported alongside full-period; verdict primarily on full-period unless OOS shows
sign flip (VR(20)_OOS > VR(20)_train + 0.15 → artifact flag).

**Non-gating reads (FROZEN — descriptive, never headlines):**
- GARCH and MA(1)-noise: reported for mechanism interpretation only; they do not set the kill criterion.
- OU reference: confirms whether MR is stronger or weaker than a matched OU process; reported; non-gating.

### Gate Tier-1 (TRADER) — causal z-entry book simulation, pooled rolling-local

**Frame:** doc-23 rolling-local pooled mean-z book sim. Same causal z-entry trade proxy mechanics.

**Cost grid (FROZEN):** {0.003, 0.005, 0.008} (spread-return units, round-trip per trade).
**Primary cost threshold (FROZEN):** K = 0.005. Success requires pooled gross expectancy to clear 0.005.

**Netting grid (FROZEN):** {η_upper = min(M,3), η_realistic = 1.5, η_conservative = 1.0}.
Netting reduces cost only (`K/η`); never applied to gross (§33 binding rule).

**Half-life tradeable band (FROZEN):** 5–60 bars (1 week to 3 months of trading days).
- Half-life < 5 bars: reverts within 1 week; 1D bars likely miss it; MERELY-TRUE / efficiency flag.
- Half-life > 60 bars: too slow for a 1–12 week book; MERELY-TRUE / deployment-band miss.
- Half-life 5–60 bars required for TRADER gate PASS.

**Pooled rolling-local frame (FROZEN):**
- Yearly windows: 2000–2025 (as available given DATE_MIN = 1997-10-22; first full year 1998).
- Per-window: compute pooled mean-z (doc-22 instrument). Report every window; no argmax.
- Pooled statistic: mean-z across all non-crisis windows first; then including crisis windows.
- The pooled read is the verdict (see §4 crisis-year isolation).

**TRADER gate PASS criteria (FROZEN):**
1. Pooled gross expectancy (pooled cross-year, excluding crisis years) ≥ 0.005 (primary cost floor).
2. Half-life inside tradeable band [5, 60] bars.
3. Episode jackknife (drop 3 largest gross trades) retains ≥ 50% of gross expectancy. If jackknife
   collapses > 50% → CONCENTRATION FLAG; verdict caps at MERELY-TRUE regardless of pooled gross.

**TRADER gate FAIL → MERELY-TRUE (if QUANT passes):**
- Gross confirmed real but < 0.005, OR half-life outside [5, 60], OR jackknife collapse.

---

## 4. Black-Swan Isolation (FROZEN)

Two designated crisis years:
- **2020 (COVID-19 supply shock):** BRN spread behavior around the April 2020 negative-price event
  and the storage-glut induced contango spike is anomalous. A single event of this type must not
  decide the verdict.
- **2022 (Russia-Ukraine energy shock):** Extreme backwardation in energy calendars, driven by
  geopolitical supply shock. Not a structural MR regime.

**Binding rule:**
- Run the full book sim INCLUDING crisis years → report as "full sample."
- Run again EXCLUDING 2020 and 2022 → report as "ex-crisis."
- **Verdict rests on the EX-CRISIS pooled read.** Full sample is context only.
- If the full-sample result and ex-crisis result are qualitatively identical (both pass or both fail),
  note the agreement. If they diverge: ex-crisis governs; full-sample divergence is documented as
  "crisis-year sensitivity" in the final report.

**No other years may be selectively excluded.** Identifying additional "anomalous" years post-hoc
to rescue a borderline result is prohibited.

---

## 5. OPEC-Period Diagnostic (PRE-REGISTERED, descriptive only — non-binding)

After computing the unconditional VR and book sim:

- Split the sample into OPEC-action weeks (±4 weeks around known OPEC/OPEC+ major production
  decisions) and non-OPEC weeks.
- Report VR(20) and pooled gross for each sub-period descriptively.
- This diagnostic does NOT constitute a pre-registration for any OPEC-conditioned strategy.
- Purpose: distinguish "global MR is weak because OPEC trending overwhelms storage MR" from
  "global MR exists and OPEC periods are a subset of the regime."
- If VR(20) > 1.0 in OPEC periods but < 1.0 in non-OPEC periods → flag as OPEC-contamination
  in the report; does NOT affect the unconditional verdict.

---

## 6. Verdict Decision Tree (FROZEN)

```
Speed gate (N=200):
  p_rw(VR20) > 0.20  →  DEAD CALENDAR — kill, record, pivot to ZC.

N=500 full test:
  VR(20) ≥ 1.0       →  DEAD CALENDAR — no MR signal; kill.

  VR(20) < 1.0 AND p_rw ≤ 0.05:
    QUANT gate PASS →  run TRADER gate:
      Half-life outside [5, 60]  →  MERELY-TRUE (efficiency miss or too slow)
      Pooled gross < 0.005 (ex-crisis)  →  MERELY-TRUE
      Jackknife collapse > 50%   →  CONCENTRATION → MERELY-TRUE
      Pooled gross ≥ 0.005 (ex-crisis) AND half-life ∈ [5,60] AND jackknife stable:
        →  SLEEVE CANDIDATE — advance to portfolio/book test

  VR(20) < 1.0 AND 0.05 < p_rw ≤ 0.20:
    QUANT gate BORDERLINE →  MERELY-TRUE regardless of TRADER gate
    (statistically marginal MR is not a deployable basis)
```

**No intermediate outcomes.** The verdict is exactly one of:
- `DEAD CALENDAR` — no MR evidence; this direction is closed.
- `MERELY-TRUE` — statistically real but sub-cost or undeployable; confirms storage MR hypothesis
  at an intellectual level; does NOT unlock portfolio framing (doc 25 ledger arithmetic).
- `SLEEVE CANDIDATE` — clears both gates; advance to portfolio/book aggregation test.

---

## 7. What May Not Happen (Anti-Lookahead Firewall, FROZEN)

The following are unconditionally prohibited after this line:

1. Changing any frozen parameter (DATE_MIN, DATE_MAX, q grid, cost grid, k, seed, half-life band,
   crisis-year list) based on what the data shows.
2. Adding or removing surrogate types after seeing VR values.
3. Selecting a different q as the "primary statistic" based on which q gives the best p-value.
4. Excluding years not on the crisis-year list.
5. Modifying analytics_arm_a / analytics_arm_a_v2 primitives for this test.
6. Running the OPEC diagnostic as a confirmatory cell retroactively.
7. Reporting only the ex-crisis number if the full-sample number is inconvenient.

Violation of any of these converts the result to INADMISSIBLE under the temporal-integrity
invariant (CLAUDE.md §6.1).

---

## 8. Reporting Requirements (FROZEN)

Every execution of this pre-registration must report ALL of the following — no selective reporting:

```
§8.1  Full VR(q) profile: q ∈ {5,10,20,40,60} — real series vs RW/GARCH/MA(1)/OU surrogates
§8.2  p_rw(VR20) at N=200 (speed gate) and N=500 (full) — both reported regardless of outcome
§8.3  OOS VR(20) vs training VR(20)
§8.4  Measured half-life (from AR(1) fit on deseasonalized spread)
§8.5  Book sim: pooled gross per trade, full-sample AND ex-crisis, across cost grid {0.003,0.005,0.008}
§8.6  Netting grid: upper / realistic / conservative for the primary cost threshold K=0.005
§8.7  Episode jackknife: pooled gross with 3 largest trades removed
§8.8  Crisis-year sensitivity: 2020 and 2022 windows reported individually alongside pooled ex-crisis
§8.9  OPEC diagnostic: VR(20) and pooled gross for OPEC-action vs non-OPEC sub-periods (descriptive)
§8.10 Verdict: exactly one of {DEAD CALENDAR, MERELY-TRUE, SLEEVE CANDIDATE}
§8.11 Strategic implication: what the verdict means for the doc-33 calendar programme
       and for whether cohort breadth (doc 25) is addressable
```

---

## 9. Strategic Context (Pre-Committed — Not a Result)

**Prior (pre-committed, before any data read):** LOW-MEDIUM 15–25% probability of SLEEVE CANDIDATE
outcome. Calibrated from: (a) NG confirmed PERSISTENT-BUT-UNECONOMIC (real MR, sub-cost); (b) BRN
has a genuine storage restoring force (elastic floating storage) but higher market efficiency; (c) OPEC
structural trend risk introduces persistent non-MR regimes with no NG analogue; (d) doc 35 honest prior.

**Strategic significance of each outcome:**
- `SLEEVE CANDIDATE` → portfolio framing (doc 25) becomes tractable; advance to book aggregation.
- `MERELY-TRUE` → second instrument confirming storage MR hypothesis is real across habitats;
  closes the BRN direction for deployment; focus shifts to ZC calendar or crack spread.
- `DEAD CALENDAR` → OPEC trending / market efficiency dominates; closes BRN direction entirely;
  accelerates pivot to ZC and crack spread positive control; note for the hypothesis registry.

**This pre-registration is closed for BRN M1–M2 in its unconditional form.** Any conditional
BRN analysis (OPEC-filtered, regime-gated) requires a new independent pre-registration passing
the §4 zombie-reopen test if the parent hypothesis was killed.

---

*Pre-registration frozen: 2026-06-05. No results exist at time of freeze. Execute only via
frozen analytics_arm_a / analytics_arm_a_v2 primitives without modification.*
