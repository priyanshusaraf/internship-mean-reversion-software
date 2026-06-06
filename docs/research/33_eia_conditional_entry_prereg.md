# Doc 33 — EIA Storage Conditional Entry: Pre-Registration & Research Plan

**Document class:** FROZEN pre-registration. Parameters in §§3–4 are locked before any data is loaded
or code is run. Any post-hoc parameter change requires a new doc number and explicit justification.
**Date frozen:** 2026-06-04. **Status:** PRE-REGISTERED — awaiting EIA data acquisition.
**Builds on:** doc 21/23 (NG confirmed PERSISTENT-BUT-UNECONOMIC) · doc 30/31 (unconditional selectivity
KILLED A_FALSE_RESCUE) · doc 32 (trader-first programme redesign).
**Governing doctrine:** doc 32 §2.1 (P1–P4 pre-conditions) · doc 32 §4 (Stage 1/2 fast-kill pipeline).
Confidence labels refer to trustworthiness of evidence, not strength of expectation.

> **Central question:** Does conditioning NG calendar spread entry on a CAUSAL public inventory signal
> (EIA weekly storage anomaly) convert PERSISTENT-BUT-UNECONOMIC MR into cost-clearing, deployable alpha?

---

## 1. Mechanism: Why Storage State Should Gate Calendar MR

### 1.1 Theory of storage — the active restoring force

The NG M1-M2 calendar spread (F(T1) − F(T2)) is governed by the fundamental futures relation:

```
S_t  =  F(T1)_t − F(T2)_t
      ≈  Convenience_Yield(t)  −  Cost_of_Carry(T1→T2)
```

**Convenience yield** (CY) = the value the holder of physical inventory derives from having it available
NOW — scarcity premium, production continuity insurance, the option to deliver without sourcing from
the market. CY is HIGH when storage is tight (physical scarcity is real); CY approaches ZERO when
storage is full (gas is everywhere, no scarcity).

**Cost of carry** = storage cost + financing (relatively stable within a season).

Calendar spread MR arises from the **cash-and-carry arbitrage mechanism**, executed by storage
operators, producers with hedging mandates, gas marketers, and prop desks:

- If S falls too far below fair value: buy spot (M1), sell deferred (M2), physically store the gas.
  Physical delivery guarantees convergence. The arbitrage tightens the spread.
- If S rises too far above fair value: producers holding gas sell spot into a premium, buy deferred
  to lock future sales. Same convergence mechanic, other direction.

This arbitrage runs continuously whenever storage capacity is available. Multiple actors execute it.
The result: the spread mean-reverts toward the CY−CoC equilibrium — provided the MECHANISM IS ACTIVE.

### 1.2 Why GLUT breaks the mechanism (the kill switch)

When working gas storage approaches PRACTICAL CAPACITY LIMITS:

1. **Physical arbitrage is blocked.** The cash-and-carry trade requires storage space. When tanks are
   full, the trade CANNOT be executed regardless of the price signal. The restoring force physically
   disappears.

2. **Convenience yield collapses.** There is no scarcity. CY → 0. The spread falls toward −CoC
   (full contango). This is not a deviation from equilibrium — it IS the new equilibrium under glut.
   There is no force to revert it.

3. **Forced spot selling.** Producers who cannot store gas MUST sell at spot. This persistently
   depresses F(T1) relative to F(T2), creating TREND in the spread, not MR. The spread can drift to
   deeply negative levels (extreme contango) without triggering the arbitrage that would close it.

4. **The "mean" itself becomes unstable.** The rolling-window mean (our z-score anchor) was
   calibrated in normal conditions. In glut, the spread moves to a new structural regime. Our
   z-score fires at what it sees as a large deviation — but the spread is not deviating from
   its true equilibrium; it IS at its new equilibrium under glut. We are fading a trending move.

**This is the exact mechanism observed in doc 23:** MR switches off in 5 identified glut years
(2009, 2012, 2017, 2020, 2025); VR → 1 in those windows; pooled mean-z is driven by non-glut years.

### 1.3 Why NORMAL/TIGHT storage sustains the mechanism

When working gas storage is AT OR BELOW the seasonal norm:

1. **Physical arbitrage is fully available.** Storage operators have space. The cash-and-carry trade
   is executable. Every significant spread deviation triggers hedging activity.

2. **Convenience yield is positive and meaningful.** Scarcity premium exists. Buyers will pay a
   backwardation premium to receive gas now. This provides a credible anchor at both extremes.

3. **Multiple actors compete for the arbitrage.** In tight conditions, gas marketers, storage
   operators, E&P hedgers, and prop desks all have incentives to execute convergence trades. The
   competition ensures the arbitrage fires quickly.

4. **The z-score is calibrated in the right regime.** The rolling mean reflects what is actually
   the equilibrium in this regime. Deviations are genuine deviations from fair value, not structural
   regime shifts misidentified as deviations.

**Central thesis:** EIA storage anomaly is a CAUSAL PROXY for the on/off state of the physical
arbitrage mechanism. When anomaly is HIGH (glut), arbitrage is blocked; MR is absent. When anomaly
is LOW (normal/tight), arbitrage is active; MR is present. Conditioning on this variable should
not create alpha — it should REVEAL the alpha that always existed but was obscured by averaging
over two structurally different regimes.

### 1.4 Why this might survive competition

Three structural barriers to the conditioning trade being fully arbitraged away:

1. **Physical infrastructure requirement.** The cash-and-carry arbitrage that drives MR requires
   physical storage capacity. Not all market participants have it. The edge is accessible only to
   those who can also execute the physical side.

2. **Small per-trade edge.** The NG calendar gross per trade is ~0.004–0.007 (doc 23/31). At
   institutional size, this requires substantial volume to matter — too small for the largest players
   to focus on. The edge may persist in size tiers where competition is lower.

3. **Regime conditioning is uniformly AVOIDED.** Most quantitative MR books run unconditional
   entry precisely because conditional models overfit (Goyal-Welch; doc 14 §3.2). A simple
   physically-anchored EIA filter is the exception — robust, causal, hard to overfit — that most
   conditional models fail to be.

### 1.5 Strongest anti-thesis (adversarial)

**A1 — Glut years = macro crisis correlation.** The 5 glut years (2009: post-GFC demand collapse;
2012: mild winter + shale ramp; 2017: oversupply; 2020: COVID demand destruction; 2025: demand
weakness) overlap with US recession/demand shock periods. The EIA filter might be proxying MACRO
REGIME, not storage economics. The same filter applied to an instrument with no storage link might
work equally well if macro regime explains the conditional MR.

**Defense:** The mechanism is physically specific to commodity storage arbitrage. Macro recession
suppresses convenience yield, but the MECHANISM is the blockage of physical arbitrage — not general
risk aversion. Test: check whether the filter improves VR on Brent (if both improve, more likely
macro contamination; if only commodity calendars improve, physical mechanism more credible). Also:
run the same EIA filter on a CONTROL instrument with NO storage link (e.g., gold futures calendar)
to check whether the filter is instrument-specific or regime-correlated.

**A2 — The 5-year average is non-stationary.** LNG export capacity grew significantly from
2016–2024, absorbing structural demand. What was a storage surplus in 2018 might be "normal" in
2022. The seasonal average embedded in EIA's published 5-year figure does not adjust for structural
level shifts.

**Defense:** This is a genuine concern for long-horizon use. For the test period (2006–2026), the
structural shift is gradual. Use EIA's own published 5-year average (computed in the EIA release
from data available at that time), which self-updates as the structural level shifts. This is the
best causally available estimate.

**A3 — Publication lag and pre-pricing.** Gas storage data is widely anticipated — traders build
models of expected EIA inventory weeks in advance. The Thursday 10:30am release price move may
reflect SURPRISE (actual vs forecast) not the LEVEL. By the time we act on the level, the level
is already in prices. Our conditioning variable (the level vs 5-year average) is not the
informative part of the release.

**Defense:** TRUE — and important. This cuts against the selectivity (timing) version of the
EIA filter. But it does NOT cut against the REGIME CONDITIONING use. We are not trading the
EIA release. We are using the storage level to identify which REGIME we are in (physical
arbitrage available or blocked). This regime changes slowly (over months, not days). Whether
the market knew the level on the release day is irrelevant to whether the REGIME is active.

**A4 — Back-adjustment contamination survives.** Doc 31 §6 showed p_splice = 0.988–0.998:
real NG is near the BOTTOM of the splice-RW distribution. This is consistent with genuine MR
(not back-adj artifacts). But the conditional test will be run on ng12_spread.csv, which is
vendor precomputed. Any systematic back-adjustment pattern (monthly seam jumps) could correlate
with the EIA conditioning if glut months have different roll characteristics.

**Defense:** This is a residual concern from doc 23. The EIA conditioning test result should be
interpreted as CONDITIONAL on the back-adjustment question not yet being closed. If the test
passes, it still carries the MEDIUM confidence caveat about back-adjustment source. Closing
this requires rebuilding NG from raw M1+M2 legs (blocked until M2 data acquired).

**A5 — The filter simply reduces trade count in bad years.** If glut years have mostly losing
trades, filtering them OUT improves the average mechanically — like removing the bad observations.
The improvement could be spurious: a RANDOM conditioning variable that happened to correlate with
those years would show the same improvement.

**Defense:** This is exactly what the surrogate test detects. In the N=200/500 surrogate runs,
the SAME conditioning variable is applied to RW/OU surrogates. If filtering on EIA storage
(which is a REAL external variable, not simulated) improves real NG MORE THAN it improves
matched null processes, the conditioning adds genuine information. If surrogates also improve
by filtering on EIA storage, the filter is correlated with an artifact.

---

## 2. Trader Object Definition (P1–P4 frozen)

### 2.1 Instrument

**NG M1-M2 calendar spread (ng12_spread.csv).**

Definition: F(T1) − F(T2) where T1 = nearest expiry, T2 = second nearest. Vendor precomputed,
continuous, β=1 definitional (confirmed admissible, doc 21). Same instrument as all prior tests.
4,969 bars, 2006-07-28 → 2026-04-15.

### 2.2 Entry rule (frozen)

Enter a trade at close of bar t if ALL of the following are true simultaneously:

**Condition A — price signal:**
```
|z_score(t)| ≥ 1.0
```
where `z_score(t) = (spread_close(t) − rolling_mean(t)) / rolling_std(t)` using a CAUSAL 60-bar
trailing window (same as doc 30). Direction: if z > 1.0, sell the spread (fade high); if z < -1.0,
buy the spread (fade low).

**Condition B — EIA storage regime (the new conditional gate):**
```
storage_anomaly(t) < 10.0  (%)
```
where `storage_anomaly(t) = most recent EIA-published (working_gas_actual − 5yr_seasonal_avg) /
5yr_seasonal_avg × 100`, using the EIA number effective on bar t (see §2.6 for assignment rules).

**Trade is SUPPRESSED** (no entry) when `storage_anomaly(t) ≥ 10.0`, regardless of z-score.

### 2.3 Exit rule (frozen)

Exit at the close of bar t if EITHER:

- `|z_score(t)| < 0.1` (spread has approximately reverted to the rolling mean), OR
- bars_held ≥ 40 (maximum hold; same as doc 30)

No mid-trade conditioning on subsequent EIA releases. Once entered, the trade runs to z-reversion
or max_hold regardless of EIA updates during the hold period.

**Why no mid-trade conditioning:** Updating the exit based on EIA releases while in a trade converts
this into an EIA-event strategy — a different trade with selection-on-deviation artifacts in the
holding window. We are testing regime-conditioning of ENTRY, not dynamic EIA event trading.

### 2.4 Holding logic

- One position at a time (no pyramiding)
- Entry: immediately following bar close that satisfies Conditions A and B
- Hold: bars_held counter increments each daily bar until exit condition
- Re-entry allowed: after exit, immediately evaluate next bar for new entry
- No cooldown period (same as doc 30)

### 2.5 Sizing

Equal-sized trades, 1 unit per signal. This is an expectancy test, not a dollar-returns test.
Position-sizing optimization is explicitly deferred — adding it in this pre-registration would
be a hidden parameter requiring its own surrogate test.

### 2.6 EIA data assignment rules (CAUSAL — binding)

EIA releases every Thursday at 10:30am ET. Publication covers working gas storage through the
prior Friday.

**Assignment rule (frozen):**
- The EIA number released on Thursday T is EFFECTIVE from Friday T+1 (next trading day after release)
- The EIA number remains effective until the NEXT EIA release becomes effective
- If trading day t is a Thursday: use the PRIOR week's EIA number (not the same-day release, which
  may not yet be published at bar-open; conservative and cleanly causal)
- This means there is a systematic 1–2 day lag between the data's reference week and when it
  influences trades. This is intentional — it reflects what a real trader actually had access to.

**Formally:** let `eia_date(k)` be the publication date of the k-th release. For trading bar t,
the effective EIA number is from release k* where `k* = max{k : eia_date(k) < t}` (strictly prior
to current bar's open).

**5-year seasonal average:** use EIA's published 5-year average from the SAME release. EIA
computes and publishes this figure weekly, and it is causally available at the same time as the
actual storage reading. Do NOT compute a custom 5-year average from the raw data — use the EIA's
own published figure, which self-adjusts for structural changes.

**Data source:** EIA's "Weekly Natural Gas Storage Report" — Working Gas in Underground Storage,
Lower 48 States (Bcf), and the corresponding 5-year average. Available via EIA Open Data API
(series: NG.NW2_EPG0_SWO_R48_BCF.W for actual; NG.NW2_EPG0_SWO_R48_BCF.W_5YR for the 5-year
average), or the EIA's published weekly storage report (xls archive at eia.gov/naturalgas/storage).

### 2.7 Cost assumptions

```
Primary cost:    0.003 per round-trip (same as doc 30)
Cost grid:       {0.0015, 0.003, 0.0045}
```

### 2.8 Rebalance cadence

Daily — same as the existing ng12 spread price series.

### 2.9 Realistic implementation notes (for a commodity trader)

- EIA data is available via Bloomberg (natural gas storage release), Reuters, direct EIA API, or
  direct download from eia.gov/naturalgas/storage. No proprietary data required.
- The 5-year average is published in the same EIA release — no custom computation required.
- The Thursday-before-close timing constraint is manageable; a simple database that ingests the
  EIA 10:30am release and propagates to the next-day signal would implement this exactly.
- The trade itself (NG M1-M2 spread) is a standard CME NYMEX spread order — screen tradeable,
  liquid, institutional-size available.

---

## 3. Pre-Committed Conditioning Variable

**ONE variable. No ensemble. No stacking. Pre-committed here.**

### 3.1 Selected primary object

```
storage_anomaly(t) = (working_gas_actual(t) − 5yr_seasonal_avg(t)) / 5yr_seasonal_avg(t) × 100
```

Unit: percentage deviation from the 5-year seasonal average.

### 3.2 Why anomaly, not absolute level

| Candidate | Rejection reason |
|---|---|
| Absolute level (Bcf) | Fails: seasonal variation confounds. Winter low (2,200 Bcf) ≠ summer low (2,200 Bcf) in terms of tightness. Same absolute level has different economic meaning in different seasons. |
| Storage trend (Δ week-over-week) | Fails: measures FLOW, not LEVEL. A high-storage period with injections ongoing ≠ a high-storage period with withdrawals. Trend captures momentum, not the capacity constraint. |
| Storage surplus vs year-ago | Marginal: better than absolute level (seasonal adjustment); worse than 5-yr average (single data point, noisy year-over-year). Dropped. |
| **Storage anomaly vs 5yr avg** | **Selected.** Causally adjusted for seasonality. Self-updating as structure changes. Economically motivated: the 5yr average represents the "expected normal" that storage operators and physical arbitrageurs calibrate their actions against. |

### 3.3 Pre-committed threshold

```
θ_eia = 10.0  (percent above 5-year seasonal average)
```

**Motivation (frozen, pre-data):** 10% is a round number motivated by economic logic, NOT by
fitting to known bad years:

- Working gas storage averages ~2,500–3,500 Bcf seasonally. 10% above the seasonal average ≈
  250–350 Bcf of "excess" gas above what is historically normal.
- 250–350 Bcf excess represents ~3–4 months of net withdrawals — sufficient to draw storage from
  near-capacity to normal in a normal winter season.
- Practical interpretation: when the market has 10%+ more gas than seasonal norms suggest it should,
  physical storage arbitrage is operating under capacity constraint. The restoring force is impaired.
- The threshold is deliberately NOT calibrated to exactly exclude specific years — it is the round
  economic threshold at which capacity constraint becomes meaningful. Whether it happens to exclude
  the known glut years is an empirical finding, NOT a design choice.

**Entry condition (frozen):** `storage_anomaly(t) < 10.0`

### 3.4 What this rule says in plain English

> "Trade the NG calendar spread z-score when the market has less gas than 10% above its seasonal
> norm. Do not trade when storage is materially oversupplied relative to historical norms."

### 3.5 What is explicitly NOT pre-registered

- A second conditioning variable (explicitly forbidden — would require new pre-registration)
- A dynamic threshold that adjusts θ_eia with vol or price levels
- A storage TREND condition stacked on the storage LEVEL condition
- Any parameter estimated from the data post-hoc to replace the 10% threshold
- The robustness appendix grid {5%, 10%, 15%, 20%} as a SOURCE of the primary threshold — the
  grid is pre-registered (§4.4) but STRICTLY DESCRIPTIVE; it cannot retroactively define which
  threshold governs the verdict

---

## 4. Fast-Kill Design (Stage 1 + Stage 2)

### 4.1 Stage 1 — Speed gate (N=200, target: 2–3 days after EIA data acquired)

**Primary statistic (pre-committed):** Conditional gross expectancy per trade at θ=1.0 entry and
cost=0.003 (same primary as doc 30).

**Secondary statistics (exploratory, non-binding):** trade count, hit rate, avg hold.

**Kill criteria at Stage 1 (ANY of the following):**

| Criterion | Kill threshold | Reasoning |
|---|---|---|
| p_rw at N=200 | > 0.20 | Cannot be significant at any reasonable N; stop immediately |
| Conditional gross vs unconditional gross | No improvement (conditional ≤ unconditional) | EIA conditioning adds nothing; the filter reduces trade count without improving quality |
| Conditional net expectancy | < −0.002 | The conditional strategy is meaningfully worse than not trading |
| Trade count remaining after conditioning | < 30 trades | Power is insufficient; inconclusive rather than positive; DEFER not kill (need more history) |

**Go criteria at Stage 1 (ALL of the following):**

| Criterion | Go threshold |
|---|---|
| p_rw at N=200 | ≤ 0.15 |
| Conditional gross > unconditional gross | Yes, minimum +0.001 improvement |
| Conditional net | > 0 at primary cost |
| Trade count | ≥ 50 trades |

**Surrogate construction for Stage 1:**
- N=200 RW surrogates: Gaussian iid increments, calibrated to real NG increment std
- Apply IDENTICAL conditioning: when mapping the surrogate price path to calendar time, use the REAL
  EIA anomaly series at each date. The surrogate inherits the SAME conditioning variable as the real
  instrument — this prevents the conditioning from mechanically improving the surrogate less than
  the real (which would inflate p_rw spuriously).

**Critical implementation note on surrogate conditioning:** The EIA anomaly series is a REAL
external variable, not a simulated one. Surrogates get the SAME external conditioning — they are
simulated price paths conditioned on the REAL EIA history. This is the correct test: does the
REAL NG price RESPOND to the EIA conditioning more than a simulated price path would?

### 4.2 Stage 2 — Decisive verdict (N=500, target: 3–5 additional days)

Reached ONLY if Stage 1 passes all go criteria.

**Full surrogate suite:** RW, GARCH(1,1), OU(φ=0.948), Splice-RW (cadence=21, frac=0.25).
All four with IDENTICAL EIA conditioning applied.

**Pre-committed primary test:**
- One-sided p-value: fraction of N=500 surrogate conditional gross values ≥ real conditional gross
- Significance threshold: p_rw < 0.05 at the primary statistic

**Secondary analyses (pre-registered, non-primary for verdict):**
1. Episode-jackknife: drop largest single gross trade from conditional book; recompute statistics
2. OOS split: train = on or before 2017-12-31; OOS = 2018-01-01 onwards (same split as doc 30)
3. Full cost grid: {0.0015, 0.003, 0.0045}
4. Comparison: conditional vs unconditional trade-proxy head-to-head (same period)
5. Glut-year coverage check: what fraction of calendar-year glut periods (2009, 2012, 2017, 2020,
   2025) are excluded by the 10% threshold? Report this as a mechanical finding, NOT as validation.

**Kill criteria at Stage 2:**

| Criterion | Kill threshold | Verdict |
|---|---|---|
| p_rw ≥ 0.05 at N=500 | — | KILLED — does not survive surrogate test |
| Jackknife drop > 300% | — | KILLED — single-trade concentrated, not a strategy |
| OOS sign reversal (conditional net < 0, OOS n ≥ 30) | — | KILLED — does not hold out-of-sample |
| Conditional gross ≤ unconditional gross at N=500 | — | KILLED — EIA conditioning adds nothing at full power |
| p_ou = 1.000 at conditional test | — | **NOT KILLED** — document as structural finding. OU receives the SAME EIA conditioning as real NG (corrected in doc 33a §4.4). The OU test is informational only; not a kill criterion. |

**Survival criteria at Stage 2 → CONDITIONAL SURVIVAL:**

| Criterion | Threshold |
|---|---|
| p_rw < 0.05 | Primary test passes |
| Jackknife drop | < 150% (comfortable stability) |
| OOS net | > 0 |
| Conditional > unconditional | Clear improvement in gross expectancy |

**Stage 2 verdict options:**
- `DEPLOYABLE_CANDIDATE` — all survival criteria met; proceed to Stage 5 (deployment architecture)
- `CONDITIONAL_SURVIVAL` — p_rw < 0.05 but OOS borderline or jackknife borderline; note specific
  condition and reopen trigger
- `INCONCLUSIVE` — trade count < 50 after conditioning; need more years; do not kill
- `KILLED` — any kill criterion fires

### 4.3 Comparison framework

The conditional strategy is tested against THREE baselines:

1. **Unconditional naive book** (same as doc 30, θ=1.0, max_hold=40, cost=0.003) — the "do nothing"
   baseline. If the conditional strategy doesn't beat this, the EIA conditioning has no value.
2. **RW surrogate with EIA conditioning applied** — the primary statistical null (p_rw from §4.2)
3. **RW surrogate WITHOUT EIA conditioning** — a check that the RW null doesn't improve more from
   the conditioning than the real instrument does (would indicate EIA conditioning inflates the null)

### 4.4 Threshold stability appendix (NON-BINDING, DESCRIPTIVE ONLY)

**Status:** Pre-registered robustness appendix. NEVER used for verdict. NEVER used for threshold
selection. Reported unconditionally — regardless of whether the primary (10%) passes or fails.

**Motivation:** The primary threshold (10%) is economically justified and pre-committed (§3.3).
However, a knife-edge result — where 10% barely fails but 5% or 15% clearly passes — is a different
kind of evidence than a result that is stable across all sensible economic thresholds. This appendix
allows a future reader to distinguish "the 10% threshold happened to be on the wrong side of the
significance boundary" from "the result is genuinely robust to the economically reasonable range."

**Grid (frozen, pre-committed):**

```
θ_eia ∈ {5%, 10%, 15%, 20%}
          ↑              ↑
       tightest       loosest
       (only enter in  (enter unless severely
       below-normal    oversupplied)
       storage)
```

All four thresholds are run at Stage 2 (N=500) AFTER the primary verdict is determined. The
primary verdict is written before the robustness grid is examined. The robustness grid appears in
the results document (doc 34) as a labelled appendix — not in the body of the results.

**Reporting requirements (binding):**

For each θ_eia ∈ {5%, 10%, 15%, 20%}, report:
- Trade count (n)
- Conditional gross expectancy
- Conditional net expectancy at primary cost (0.003)
- p_rw at N=500 (with EIA conditioning)
- Jackknife stability (gross drop %)
- Comparison to unconditional baseline

Report ALL four, not just the ones that look favorable.

**What the appendix can and cannot establish:**

CAN establish:
- "The result at 10% is part of a stable pattern across {5%, 10%, 15%, 20%}" — increases
  confidence that the result is not knife-edge
- "The result at 10% is isolated — only 10% passes while 5% and 15% fail" — decreases
  confidence, flags the threshold as potentially over-fitted even though it was pre-committed
- "All thresholds fail" — confirms the kill verdict is robust

CANNOT establish:
- That a different threshold should be used as the primary
- That a passing threshold outside {10%} is evidence for the hypothesis
- That a threshold with higher gross/lower p-value is the "right" threshold
- Any post-hoc selection from this grid

**Escape-hatch closure (binding):**

The following interpretations are EXPLICITLY PROHIBITED by this pre-registration:

1. "The primary (10%) failed, but 15% passed — the threshold should have been 15%."
   → **PROHIBITED.** The primary verdict is KILLED. The appendix grid does not reopen it.
   A test at θ_eia = 15% as primary requires a NEW pre-registration with a new document number
   and explicit justification for why 15% is economically motivated independently of these results.

2. "Three out of four thresholds pass — the result is confirmed even though the pre-committed
   10% narrowly fails."
   → **PROHIBITED.** Statistical significance is assessed at the pre-committed threshold only.
   Counting passes in a sensitivity grid is not a valid significance test — it is p-hacking with
   extra steps.

3. "The robustness grid shows instability at the primary threshold, but two adjacent thresholds
   pass — this suggests the true threshold is somewhere in between."
   → **PROHIBITED.** The pre-registered threshold is the threshold. Sensitivity grids inform
   CONFIDENCE, they do not inform threshold selection ex-post.

**What IS permitted:**

If the primary (10%) PASSES and the robustness grid shows the result is STABLE across all four
thresholds (all four p_rw < 0.10), this is a legitimately strengthening finding that can be
noted in the results memo as: "The conditional entry result is robust across the full economic
range of thresholds {5%–20%}, consistent with the storage arbitrage mechanism rather than
threshold overfitting."

If the primary (10%) PASSES but the robustness grid shows the result is UNSTABLE (only 10%
passes, 5% and 15% fail), this is a legitimately WEAKENING finding that must be noted: "The
result is sensitive to the exact threshold — consistent with the pre-committed threshold being
near the boundary of the effect; interpret with lower confidence."

Both of these are post-hoc CONFIDENCE CALIBRATIONS on a passing result — NOT changes to the
verdict itself.

---

## 5. Adversarial Overfit Defense

### 5.1 Taxonomy of failure modes

#### F1 — Macro conditioning laundering hindsight

**The risk:** The 5 glut years happen to overlap with macro crises. After seeing results, the
researcher could argue "it works in non-crisis years" — which is a post-hoc redescription of the
EIA filter as a crisis filter. If the same filter works on gold, equity futures, or a non-storage
commodity, the mechanism is macro, not storage.

**Guardrail in this pre-registration:**
- The threshold (10%) is pre-committed to a round economic number, NOT chosen to exclude specific
  years
- A CONTROL INSTRUMENT test is pre-registered: after Stage 2 (if the filter passes), run the
  same EIA conditioning on rb23_spread.csv (RB M2-M3 spread, a petroleum product with different
  storage dynamics). If RB improves by a similar factor, the effect is likely macro-correlated.
  This test is PRE-REGISTERED here; it cannot be added or removed post-hoc.
- If the glut-year coverage check (§4.2 item 5) shows the 10% threshold PRECISELY excludes 5/5
  known glut years, this is flagged as a calibration concern in the verdict document.

#### F2 — Seasonal leakage in the conditioning variable

**The risk:** If we compute the 5-year average ourselves from the raw EIA storage data, we might
inadvertently use full-sample statistics. If we're using the EIA's own published 5-year average
from the weekly release, it's causally clean — but only if that published figure was available
at the time of the trade.

**Guardrail:**
- Pre-committed rule (§2.6): use EIA's PUBLISHED 5-year average from the weekly release, time-
  stamped by the release date, assigned with the 1-2 day publication lag. We use the number
  as published, not a recomputed version.
- Data sourcing validation: after acquiring the data, compare 3 spot-checks against the archived
  EIA release PDFs to verify the time-stamped figures match what was actually published.

#### F3 — Threshold overfitting post-hoc

**The risk:** After running Stage 1 and seeing results near the kill threshold, the researcher
adjusts θ_eia from 10% to 8% or 12% to pass. This is p-hacking.

**Guardrail:**
- The threshold is locked in this document before any code runs.
- If 10% fails, the test returns a KILL verdict. A subsequent test with a different threshold
  requires: (a) a new pre-registration document with explicit justification for why the mechanism
  supports a different threshold, (b) multiplicity correction, (c) the new test counted as a
  separate attempt. It cannot be presented as a continuation of this pre-registration.
- The verdict document (doc 34, when written) will report what threshold was tested and what other
  thresholds were NOT tested, with an explicit statement that no alternative thresholds were
  evaluated before committing to this result.

#### F4 — Regime stacking temptation

**The risk:** After passing Stage 1, add a second condition ("AND realized vol < threshold") to
further improve results. This turns one causal variable into a discretionary regime filter — the
State-T-adjacent failure mode.

**Guardrail:**
- This pre-registration explicitly authorizes ONE conditioning variable, ONE threshold.
- Adding ANY second conditioning variable requires a NEW pre-registration. The existing Stage 1
  and 2 results cannot be used to motivate the second variable — that would be data snooping.
- The verdict document will explicitly note whether second-variable temptations were resisted.

#### F5 — EIA data revision artifacts

**The risk:** EIA revises storage figures after initial release. The initial Thursday release
(what a real trader had) can differ from the later revised figure. If we use the revised data,
we're trading with information that wasn't available.

**Guardrail:**
- The pre-registration specifies use of FIRST-RELEASE data only (see §2.6).
- Data acquisition must source time-stamped first-release figures, not the current revised series.
  EIA maintains its historical weekly release archives; the first-release number is recoverable.
- If first-release data is unavailable and only revised data is accessible, document this as a
  data-quality caveat in the results, and treat it as a source of upward bias (first-release
  numbers are nosier than revised — using revised overstates what was actually available).

#### F6 — Publication-lag misuse

**The risk:** Use the Thursday EIA number for Thursday trading, when the report comes out at
10:30am ET — AFTER the opening bar. If we condition entry on information not yet released as of
the bar's open, we have causal leakage.

**Guardrail:**
- The assignment rule in §2.6 is explicit: EIA release effective from the NEXT TRADING DAY (Friday).
  Thursday bars use the PRIOR WEEK's EIA number. This introduces a conservative 1-day lag.
- For daily bars, this means there is always a ≥1 trading day gap between the EIA release and
  when it influences entry decisions. This is the causal floor.

#### F7 — Selection bias on the conditioning sample

**The risk:** After conditioning, the remaining trades may be concentrated in specific years,
seasons, or vol regimes that are systematically favorable. The EIA filter might be perfectly
correlated with "calm, low-vol, non-crisis years" — which themselves show better mean reversion
in many instruments, not just NG.

**Guardrail:**
- The surrogate test with EIA conditioning applied to RW paths (F1 defense) partially addresses
  this: if calm years show better MR in RW paths at the SAME rate as real NG, the conditioning is
  regime-correlated, not storage-specific.
- Additionally: report the vol characteristics of the conditional sample vs the excluded glut-year
  sample. If realized vol in the conditional sample is systematically lower, flag as confound.

#### F8 — Quiet State-T resurrection via "storage as a timing signal"

**The risk:** If successful, subsequent work begins to use the EIA signal DYNAMICALLY — "exit
early when storage is building," "increase size when storage is dropping sharply." This gradually
converts the conditioning from a REGIME GATE to a TIMING SIGNAL, which is exactly State-T.

**Guardrail:**
- The pre-registration is explicit: EIA conditioning gates ENTRY ONLY. It does NOT modify exits.
  It does NOT modify sizing. It does NOT create mid-trade signals.
- Any extension to "EIA-driven dynamic exit" requires a new pre-registration with explicit
  §4 zombie-reopen justification demonstrating it is not State-T.

---

## 6. Portfolio Compatibility Tracking

This section does NOT optimize the portfolio. It identifies where this sleeve would fit IF successful,
for future book-construction context.

### 6.1 Asset class and sector

```
Sector:         Commodity / Energy
Sub-sector:     Natural gas
Instrument:     NG M1-M2 calendar spread (futures)
Factor exposure: Storage MR / convenience yield variance
```

### 6.2 Independence characteristics

**What this would be independent FROM (expected):**
- Equity risk premium (no exposure to equity beta in calendar spread; basis positions are
  commodity-specific)
- Interest rate risk (minimal — the financing component of carry is small and fixed)
- Agricultural commodity spreads (ZC, ZW, beans) — different storage economics, different
  weather regime correlations
- Metals calendars (GC, HG) — entirely different storage and convenience yield dynamics

**What this would be CORRELATED WITH (expected):**
- Brent M1-M2 calendar MR (if BRN passes Move 2 test) — both energy storage MR; likely correlated
  in storage-tight periods
- Any other NG-linked trade (UNG, natural gas producers, LNG-linked spreads)
- In stress periods (energy supply shock): potentially correlated with oil/gasoline spreads

### 6.3 Future book assignment

If successful, this sleeve belongs to a **"Energy Storage MR" cluster** alongside:
- BRN M1-M2 conditional MR (if Move 2 confirms)
- Any NG M2-M3 calendar (not yet tested)
- Crack spread MR (Move 3, different mechanism but energy sector)

**Capital overlap risk:** HIGH within the energy sector. If EIA conditional NG + BRN conditional
both live in the same book, their downside is correlated (energy supply shock, LNG disruption,
demand collapse). Treat the energy storage cluster as a SINGLE SECTOR for risk limits.

**Maximum sector allocation:** this is a deployment decision, not a research decision. But flag:
a book consisting only of energy storage sleeves is a concentrated energy basis book, not a
diversified MR book. Portfolio diversification requires an agricultural or metals MR sleeve
(ZC calendar, copper spread) to reduce energy-sector concentration.

### 6.4 Correlation with existing confirmed findings

Currently, the only confirmed edge is NG calendar MR (unconditional). The EIA conditional
version, if it passes, is a REFINEMENT of the same underlying edge — not an independent edge.
For portfolio purposes, conditional NG should be treated as NG-EXPOSURE, not as a new
diversifying risk factor. It does NOT add diversification relative to the unconditional NG book.

---

## 7. Data Acquisition Requirements

Before any code is written, the following data must be acquired:

### 7.1 Required

```
EIA Weekly Natural Gas Storage Report — Working Gas in Underground Storage, Lower 48 States
Source:     EIA Open Data API or eia.gov/naturalgas/storage weekly archive
Series:     Working gas actual (Bcf, weekly, first-release)
            EIA-published 5-year seasonal average (Bcf, same release)
Date range: 2006-07-28 → 2026-04-15 (to match ng12_spread.csv)
Format:     Date (EIA publication date = Thursday), storage_actual_bcf, storage_5yr_avg_bcf
Time-stamp: MUST be publication date (Thursday), NOT the data reference week ending date
```

### 7.2 Data quality checks (binding before running any test)

1. Verify ≥ 52 releases per year (EIA publishes weekly; gaps are anomalies)
2. Spot-check 5 historical releases against EIA's archived weekly report PDFs to confirm
   the first-release figures match
3. Verify no future leakage: ensure the data file's most recent date ≤ 2026-04-15
4. Verify the 5-year average is the EIA-published figure, not a self-computed average
5. After mapping to daily price dates (§2.6 assignment rule), check that every price bar
   in the test period has a valid corresponding EIA storage anomaly value

---

## 8. Pre-Registration Summary (all parameters frozen)

```
INSTRUMENT:         NG M1-M2 calendar spread (ng12_spread.csv)
CONDITIONING VAR:   EIA storage anomaly = (actual − 5yr_avg) / 5yr_avg × 100
THRESHOLD:          10.0% (enter only when anomaly < 10.0%)
ENTRY Z-THRESHOLD:  1.0 (primary; same as doc 30)
Z LOOKBACK:         60 bars (causal trailing window)
MAX HOLD:           40 bars (same as doc 30)
PRIMARY COST:       0.003 per round-trip
COST GRID:          {0.0015, 0.003, 0.0045}
STAGE 1 N:          200 (RW with EIA conditioning; primary θ_eia=10% only)
STAGE 2 N:          500 (RW, GARCH, OU, Splice — all with EIA conditioning; primary θ_eia=10% only)
ROBUSTNESS APPENDIX: θ_eia ∈ {5%, 10%, 15%, 20%} at N=500; STRICTLY DESCRIPTIVE; non-binding;
                    reported unconditionally; CANNOT change verdict; CANNOT select threshold post-hoc
TRAIN END:          2017-12-31 (same as doc 30)
OOS START:          2018-01-01
PRIMARY STATISTIC:  conditional gross expectancy per trade at θ=1.0, cost=0.003
PRIMARY P-VALUE:    p_rw (one-sided, gross)
SIGNIFICANCE:       p_rw < 0.05 at Stage 2 (decisive)
KILL CRITERIA:      p_rw > 0.20 at N=200 OR p_rw ≥ 0.05 at N=500 OR jackknife drop > 300%
                    OR OOS sign reversal (n ≥ 30) OR conditional ≤ unconditional
CONTROL INSTRUMENT: rb23_spread.csv with same EIA conditioning (pre-registered; run if Stage 2 passes)
SEED:               20260604
```

---

## 9. Recommendation and Confidence

**Recommendation: RUN IMMEDIATELY. HIGH expected value of information.**

**Reasoning:**

The EIA conditional entry hypothesis is the highest-EV test available in the programme for these
reasons, taken together:

1. The MECHANISM is the strongest in the programme — theory of storage (Working 1949) is physically
   grounded; the on/off switch for physical arbitrage is well-understood; the EIA storage anomaly is
   a direct proxy for that switch.

2. The TEST IS CHEAP — EIA data is free, publicly available, and requires no proprietary sourcing.
   The test can be run in 2–3 weeks from data acquisition. The code reuses the existing ng12 trade
   proxy with a one-line entry gate.

3. The UPSIDE IS LARGE — if it passes, the programme's only confirmed MR edge (NG, PERSISTENT-BUT-
   UNECONOMIC) becomes a deployment candidate. This converts 4 months of prior research into a real
   trade. There is no other single action that could accomplish this.

4. The DOWNSIDE IS CHEAP — if it fails (p_rw > 0.05 at Stage 2), the programme learns that NG's
   regime-conditionality is not exploitable via a simple EIA filter, and pivots cleanly to Brent
   calendar (Move 2) and crack spread (Move 3). No code debt, no architectural complexity.

5. The ANTI-THESIS IS KNOWN AND CONTAINED — the adversarial analysis in §1.5 and §5 identifies
   the specific failure modes. Each is addressed by a specific guardrail in the pre-registration.
   No hidden contamination vectors.

**Prior probability: MEDIUM.** The mechanism is strong (↑); the regime-conditionality evidence
from doc 23 is real (↑); but the 5-year test period in non-glut years may have too few observations
for power (↓); back-adjustment is not fully closed (↓); macro-crisis confounding is a real concern
(↓). Revised upward from LOW (prior unconditional selectivity prior) because this uses a causal
external variable rather than a price pattern.

**Confidence in the pre-registration design: HIGH.** The guardrails in §5 are specific and binding.
The fast-kill criteria are aggressive. The control instrument test is pre-registered. The threshold
is economically motivated, not data-fitted.

**Explicit non-conclusions of this pre-registration:**
- This is NOT a test of EIA surprise trading (the release day price move)
- This is NOT a test of the EIA as a regime-timing tool (dynamic exit/sizing)
- This is NOT a claim about other instruments (EIA storage is NG-specific)
- If this FAILS, it does NOT invalidate the NG MR finding (doc 21/23); it closes the
  UNCONDITIONAL ENTRY PATH and the EIA LEVEL PATH only

---

*Markers: PRE-REGISTERED (doc 33, frozen 2026-06-04) · ACTIVE — awaiting EIA data acquisition ·
Supersedes the "EIA filter" entry in doc 32 §5 Move 1 with full parameter freeze.*
