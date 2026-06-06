# Doc 34 — EIA Storage Conditional Entry: Results & Verdict

**Document class:** Permanent AMR research record.
**Date:** 2026-06-04. **Status:** COMPLETE — binding kill verdict.
**Pre-registration:** doc 33 (frozen). **Implementation spec:** doc 33a. **Spot-check:** doc 33b.
**Script:** `scripts/run_eia_conditional_test.py`. **Output:** `data/processed/eia_conditional_stage1.json`.
**Builds on:** doc 23 (NG PERSISTENT-BUT-UNECONOMIC) · doc 31 (unconditional selectivity A_FALSE_RESCUE).

> **Verdict: `KILLED` — Stage 1 KILL_PVAL.**
> EIA storage regime conditioning does not improve NG calendar spread MR above the random-walk
> null. Conditional gross (0.0056) sits at the **50th percentile** of the RW surrogate distribution
> (p_rw = 0.502, N=200). The EIA filter adds no statistically distinguishable alpha relative to a
> zero-MR null that receives identical conditioning.

---

## 1. Data acquisition status

| Item | Status | Detail |
|---|---|---|
| EIA weekly storage levels | ACQUIRED (partial) | 2010-01-01 → 2026-05-22, 856 rows |
| Pre-2010 historical data | NOT ACQUIRED | EIA API requires key; DNAV limits download to ~16 years |
| EIA-published 5-year average | NOT ACQUIRED | Replaced by causal rolling same-week mean |
| Pre-registration date_min (2006-07-28) | **UNMET** | Documented deviation per doc 33a §5.1 CHECK-3 |
| Effective test start | 2015-01-08 | First date with ≥5 prior years of storage data |

**Effective test period:** 2015-01-08 → 2026-04-15 (2,837 bars vs 4,969 bars in full pre-registration).
**Missing data impact:** 9 years of history removed (2006-2014), including glut years 2009 and 2012.
Available glut years: 2017 (training), 2020 (OOS), 2025 (OOS) — 3 of 5 identified glut years present.

---

## 2. Pipeline validation (all VALIDATE-B checks passed)

All 5 causal spot-check assertions from doc 33b passed:

```
T02: Thursday uses prior-week EIA                           PASS ✓
T03: Friday uses current-week EIA                           PASS ✓
T05: Post-Thanksgiving Friday uses Wed holiday release      PASS ✓
T07: COVID-period Friday uses prior-day release             PASS ✓
T10: Thursday uses prior-week EIA                          PASS ✓
```

The join is causally correct. The `allow_exact_matches=False` parameter was active. No causal
contamination in the pipeline.

---

## 3. Storage anomaly characteristics (2015–2026)

```
EIA_allowed fraction:  75.3% (storage anomaly < 10%)
Suppressed fraction:   24.7% (storage anomaly ≥ 10%)
Anomaly distribution:  min=−57.0%, p5=−23.9%, median=+2.4%, p95=+33.1%, max=+52.1%
```

The 10% threshold suppressed approximately 25% of bars — broadly consistent with glut-year
coverage (2017: ~3/4 year suppressed; 2020: ~3/4 year suppressed; 2025: partial suppression).
The threshold behaves as designed.

---

## 4. Full results

### 4.1 Trade statistics

| Metric | Unconditional (baseline) | Conditional (EIA gate) |
|---|---|---|
| n trades | 86 | **65** |
| Gross expectancy | +0.0037 | **+0.0056** |
| Net expectancy (cost=0.003) | +0.0007 | **+0.0026** |
| Hit rate | — | 0.63 |
| Avg hold (bars) | — | — |

Conditional gross (+0.0056) > unconditional gross (+0.0037) by +0.0019. The conditioning
DOES improve gross expectancy on the effective test period. This meets the Stage 1 go
criterion for the "improvement" check.

### 4.2 Stage 1 surrogate results (N=200 RW, with identical EIA conditioning)

```
Conditional gross (real NG):     +0.0056
RW surrogate distribution (N=200):
  p5   = −0.0661
  p25  = −0.0278
  p50  = +0.0057     ← real NG at exactly the median
  p75  = +0.0345
  p95  = +0.0726

p_rw = 0.502
```

**Real NG sits at the 50th percentile of the zero-MR RW distribution.** The conditional gross
of +0.0056 is virtually indistinguishable from the surrogate median of +0.0057. The EIA filter
does not produce alpha beyond what a zero-MR random walk produces when subjected to identical
EIA conditioning.

### 4.3 OOS split

```
OOS period (2018-2026): n=49 trades, gross=+0.0078, net=+0.0048
```

OOS is directionally positive and mildly cost-clearing. However:
- The primary verdict is determined by p_rw (0.502), which kills the test at Stage 1
- OOS n=49 trades is adequate (above the 30-trade floor)
- OOS positivity is noted as a soft observation, non-binding (same status as doc 31 OOS)

### 4.4 Jackknife

```
Jackknife: full gross=+0.0056, after-drop gross=+0.0297, drop=427%, dropped_gross=−1.533
```

The dominant trade is a large LOSER (−1.533) — removing it improves the gross by 427%.
This parallels the doc 31 θ=1.0 finding: at the primary threshold, the result is dominated
by a large tail loss, not a large tail gain. The book is not single-trade concentrated
in the direction of apparent alpha; the large loser is suppressing the underlying mean.

---

## 5. Verdict: KILLED — KILL_PVAL

**Primary kill criterion triggered: p_rw = 0.502 > 0.20.**

```
CRITERION                              RESULT
──────────────────────────────────────────────────────────────────
p_rw ≤ 0.20 at N=200 (Stage 1 gate)   FAIL  (p_rw = 0.502)
Conditional gross > unconditional     PASS  (+0.0056 vs +0.0037)
Conditional net > −0.002              PASS  (net = +0.0026)
OOS n ≥ 30                            PASS  (n = 49)
Stage 1 proceed                       KILL — KILL_PVAL
```

The p_rw = 0.502 fails the 0.20 threshold by a wide margin. This is not a borderline kill —
real NG's conditional gross sits exactly at the median of the zero-MR null distribution.
Upgrading to N=500 would produce a p-value near 0.50, not near significance. Stage 2 was
not run, per doc 33 §4.1.

---

## 6. Mechanism interpretation

**Why did the EIA conditioning fail to improve on the RW null?**

The surrogate receives the SAME EIA conditioning as real NG. A zero-MR random walk,
when conditioned on the same "non-glut" regime, produces gross expectancy at p50 = +0.0057 —
essentially identical to real NG at +0.0056.

This means: **the EIA conditioning itself produces the apparent gross improvement** — not NG's
genuine MR during non-glut periods. When the EIA filter suppresses ~25% of bars (the glut
periods, which are mean-trending rather than mean-reverting), the average over the remaining
75% of bars improves mechanically. A random walk conditioned on the same "benign" periods
shows the same improvement, because what's being filtered is a subset of bars with more
extreme dynamics — not because the non-glut NG spread has stronger MR than a RW.

In other words: **the selection-on-regime artifact** mirrors the selection-on-deviation
artifact from doc 31. Selecting "benign" periods of any time series improves apparent
expectancy, because extreme-return periods are excluded. This benefit accrues to ALL
conditioned strategies, including zero-MR ones.

This is distinct from NG's documented MR (VR=0.448, doc 21). The MR exists globally but
is not strong enough to stand out above the selection-on-regime noise, even with the EIA
filter removing the worst periods.

---

## 7. What this kills and what it does not kill

**Killed by this result:**
- The EIA storage level conditioning as a standalone entry gate (10% threshold, pre-registered
  primary statistic, effective period 2015-2026)
- The hypothesis that regime conditioning via EIA level converts PERSISTENT-BUT-UNECONOMIC
  to DEPLOYABLE_CANDIDATE

**NOT killed by this result:**

1. **NG global MR** (VR=0.448, doc 21) — confirmed by a different apparatus. Unchanged.
2. **A more refined causal inventory variable.** The EIA storage LEVEL as a conditioning
   variable is falsified. The EIA SURPRISE (actual vs expected; week-over-week change vs
   seasonal trend) or a flow-based signal (COT positioning, LNG export data) might still work
   — but each requires a new pre-registration.
3. **BRN calendar MR.** The Brent M1-M2 calendar test is unrelated and still pending.
4. **Crack spread controlled-β apparatus.** Also unrelated and still pending.
5. **Longer-history version of this test.** If full 2006-2026 data (via EIA API key) were
   available, the test might have different power. The truncation to 2015 eliminates glut
   years 2009 and 2012, which may be the highest-signal periods for demonstrating the
   on/off switch. This result is specific to the 2015-2026 window.

---

## 8. Data limitation note and possible replication path

The 2015-2026 test window is a significant narrowing from the 2006-2026 pre-registration
design. Two of five identified glut years (2009, 2012) are excluded. The statistical power
is reduced: 65 conditional trades vs the ~149 unconditional trades in the full 2006-2026
window (doc 31).

**A higher-powered version of this test is possible with EIA API data:**
- Full history from 1993 to present
- EIA-published 5-year average (avoids rolling approximation)
- Access: free API key registration at api.eia.gov

With full data, the test would cover 2006-2026 (~149 conditional trades at θ_z=1.0), giving
somewhat more power. However, given the p_rw = 0.502 result on the available window — exactly
at the RW null median — there is no strong expectation that adding 9 more years would produce
p < 0.20. The effect, if it exists, is not concentrated in the available data.

**Decision rule for replication:** Only pursue if the user acquires the EIA API key AND can
confirm that glut years 2009 and 2012 had anomaly profiles consistent with the 10% threshold
excluding them. If those years were also near-marginal (anomaly 8-12%), the full-sample result
would be similarly mixed.

---

## 9. Strategic consequence

The EIA storage conditioning path is CLOSED for the pre-registered conditioning variable
(storage level anomaly vs 5-year average, θ_eia = 10%).

The doc-25 gate sequence now stands as:

```
Gate 1 (selectivity, doc 31):          CLOSED — A_FALSE_RESCUE
Gate 1b (EIA conditioning, doc 34):    CLOSED — KILL_PVAL
Gate 0/2 (controlled-β cohort):        SOLE OPEN GATE — BRN2! + ZC2! acquisition
```

The programme's deployable route remains solely: **cohort breadth via BRN M1-M2 and ZC M1-M2
daily calendars.** If additional instruments independently confirm VR < 1 surrogate-relative,
the portfolio framing becomes posable.

**Next highest-EV actions (reordered after this kill):**

1. **BRN M1-M2 daily calendar** (doc 32 Move 2) — BRN1! daily already exists; BRN2! 1D
   acquisition is the binding action. Highest remaining EV single test.
2. **Crack spread controlled-β positive control** (doc 32 Move 3) — validates the controlled-β
   apparatus for all future pairs work.
3. **EIA full-history replication** (optional) — only if API key acquired and user judges
   it worth running before pivoting to BRN/crack spread.

---

## 10. Confidence / non-conclusions / next question

**Confidence (trustworthiness of evidence):** MEDIUM.
- VALIDATE-B passed: join logic causally correct
- N=200 surrogates adequate for a p=0.50 kill; would not change at N=500
- Data truncation (2015-2026 vs 2006-2026) reduces confidence in finality; the result
  could differ on the full window. Current evidence does not support the hypothesis but
  does not definitively close the full-history version.

**Explicit non-conclusions:**
- NOT "NG has no MR" — VR apparatus finding is independent and stands
- NOT "EIA storage data is useless" — a different specification (surprise, flow, inventory
  change) could work and is untested
- NOT a cross-habitat statement (BRN, ZC not tested)
- NOT a full-history verdict (2006-2014 period not covered)

**Next high-information question:** Given this kill, is BRN calendar spread MR confirmable
at VR < 1 surrogate-relative (p_rw < 0.05)? That is now the programme's binding empirical
gate. Acquire BRN2! 1D.

---

*Markers: KILLED (EIA storage level conditioning, KILL_PVAL, p_rw=0.502, N=200, 2015-2026) ·
NOTED (OOS positive direction, soft, non-binding) · CONFIRMED (selection-on-regime artifact
as mechanism for apparent improvement) · DATA LIMITATION (2015-2026 only; full-history
version not run) · SOFT OPEN (longer-history version remains admissible with EIA API key).*
