# Doc 33a — EIA Conditional Entry: Execution Preparation

**Document class:** Pre-execution checklist and implementation specification.
**Date:** 2026-06-04. **Status:** BLOCKING — must be resolved before any code is written.
**Governs:** `scripts/run_eia_conditional_test.py` (not yet written).
**Pre-registration:** doc 33 (frozen). **No parameter changes permitted from this document.**
**Source of truth for implementation ambiguities supersedes doc 33 where explicitly noted.**

> This document converts doc 33 from a research plan into an unambiguous build spec.
> Every section below identifies an implementation decision that must be made correctly
> the first time — there is no second run that can "fix" a causal contamination post-hoc.

---

## 1. Data Acquisition Requirements

### 1.1 What to acquire

Two EIA weekly series, matched date-for-date:

```
Series A:  Working gas in underground storage, Lower 48 states (Bcf)
           — actual weekly figure (first-release preferred; see §1.3)

Series B:  EIA-published 5-year average, same week and same release
           — the figure EIA computes and publishes in the same weekly report
```

Both series must share the same date index so that storage_anomaly can be computed per release.

### 1.2 Primary source options (in order of preference)

**Option 1 — EIA Open Data API v2 (recommended)**

Endpoint: `https://api.eia.gov/v2/natural-gas/stor/wkly/data/`
API key: free registration at eia.gov/opendata.

The v2 API returns data in JSON with a `period` field representing the **week-ending date** (Friday
of the data week — NOT the Thursday publication date). Both current-level and 5-year average are
available as separate series identified by `process` facets.

Relevant process codes (verify against current EIA API documentation):
- `SAR` — Working gas in storage, weekly (actual level, Bcf)
- `SNR` — 5-year average (if available; alternatively may be labelled differently)

Date range to request: 2001-01-01 through 2026-04-30 (wider than ng12 range to allow buffer).

**Option 2 — EIA weekly storage report archive (fallback)**

URL: `https://www.eia.gov/naturalgas/storage/dashboard/`

EIA publishes a weekly Excel file. The historical archive extends back to 2001. This source
is more likely to represent first-release figures (the live report, not revised data).

**Option 3 — Bloomberg / Refinitiv (if accessible)**

Bloomberg ticker: `NGSNGAS Index` — captures first-release figures time-stamped at publication.
This is the cleanest source for timestamp integrity but requires a Bloomberg subscription.

### 1.3 First-release vs revised data: practical position

**EIA data is revised.** The initial Thursday release is based on a survey of storage operators;
some operators report late, causing small revisions in subsequent weeks. Annual revisions can also
adjust historical figures.

**Practical impact:** For storage anomaly as % of 5-year average, revisions are typically
< 0.3% of the absolute storage level (< 10 Bcf on ~3,400 Bcf). This produces anomaly changes
of < 0.3 percentage points. For a threshold of 10%, this is negligible — a revision is unlikely
to flip a trade from permitted to suppressed or vice versa.

**Documentation rule:** If using revised data (the default from the EIA API), document this
explicitly in the results file as:
> "EIA data sourced from API (revised figures). Revisions estimated <0.3% impact on anomaly;
> negligible effect on threshold decisions. First-release data would require manual archive
> reconstruction."

**If first-release data is available** (Bloomberg or manual archive): prefer it and note
"first-release" in the data provenance record.

### 1.4 Validation checks before any test code runs

```
CHECK-1:  Row count
          Expect: ≥ 52 rows per calendar year (EIA publishes every Thursday)
          Fail condition: < 40 rows in any year → investigate gap

CHECK-2:  Date continuity
          Expect: week_ending_date increments by exactly 7 days in each step
          Fail condition: any step ≠ 7 days → flag as possible holiday delay or data gap

CHECK-3:  Date range coverage
          Expect: earliest record ≤ 2006-07-28; latest record ≥ 2026-04-10
          Fail condition: any end is outside this range → data is truncated

CHECK-4:  5-year average availability
          Expect: 5yr_avg is non-NaN for every row in [2006-07-28, 2026-04-15]
          Fail condition: any NaN in the ng12 date range → handle per §2.4

CHECK-5:  Spot-check 3 dates against EIA archived releases
          Select: 2010-01-07, 2018-03-15, 2022-11-03 (arbitrary, pre-committed)
          Verify: storage_actual and 5yr_avg match the published EIA report for those dates
          Fail condition: any value differs by > 15 Bcf → data source integrity concern

CHECK-6:  No future-dated records
          Expect: latest week_ending_date ≤ 2026-04-19 (Friday before ng12 last bar)
          Fail condition: records exist after ng12 end date → trim or flag

CHECK-7:  Storage anomaly range sanity
          Compute storage_anomaly for all rows; print min, max, mean, p5, p95
          Expect: range approximately −30% to +30% (extreme glut/deficit)
          Flag if: any anomaly > 60% or < −60% → likely data error, investigate
```

---

## 2. Preprocessing Rules

### 2.1 Date transformation: week-ending to publication date

**THE MOST CRITICAL TRANSFORMATION IN THE ENTIRE PIPELINE.**

EIA API data is indexed by `period` = **week_ending_date** (the Friday the data covers).
The storage report is **published the following Thursday**, 6 calendar days later.

```
publication_date = week_ending_date + 6 days
```

Example:
```
week_ending_date  2020-03-06 (Fri) → publication_date  2020-03-12 (Thu)
week_ending_date  2020-03-13 (Fri) → publication_date  2020-03-19 (Thu)
```

**This transformation is mandatory.** If the week_ending_date is used directly as the join key,
storage data will be assigned to price bars **6 days before the data was actually published.**
That is systematic causal leakage affecting every single bar in the dataset.

### 2.2 Holiday exception handling

EIA shifts release dates on US holidays. The most common case:

**Thanksgiving (fourth Thursday of November):** EIA releases Wednesday instead of Thursday.
In this case `publication_date = week_ending_date + 5 days` (not +6).

Other holidays (Christmas, New Year, July 4th) typically shift by ±1 day.

**Practical handling:**

Option A (recommended if using EIA API): The API may return data with the actual publication
date as a separate field. Check the API response for a `releaseDate` or equivalent field. If
present, use it directly instead of computing week_ending + 6 days.

Option B (manual): Maintain a list of known holiday-shifted releases. For 2006–2026,
the major shifts are Thanksgiving weeks (approximately 20 occurrences). A list is available
from EIA's published release calendar. The impact is: holiday-shifted bars use a release
that is 1 day earlier than computed by the formula — the effect is at most 1 trading day
of assignment error in 20 weeks out of ~1,050 total releases. Very low impact on results,
but must be documented.

**Minimum viable handling:** Apply the week_ending + 6 formula uniformly; note in the
results document that holiday weeks have a possible 1-day assignment error (document how
many Thanksgiving weeks fall in the test period). This is acceptable given the small
impact, as long as it is disclosed.

### 2.3 Anomaly computation

```python
storage_anomaly_pct = (storage_actual_bcf - storage_5yr_avg_bcf) / storage_5yr_avg_bcf * 100.0
```

- Units: percentage deviation from 5-year seasonal average
- Sign: positive = above average (excess supply); negative = below average (deficit)
- Entry gate fires when this value is < 10.0 (doc 33 §3.3)

### 2.4 Missing value handling (EIA gaps)

EIA occasionally does not publish (government shutdowns, natural disasters). If a week is
missing, the storage_anomaly for that week is NaN.

**Pre-committed NaN handling rule (conservative, causal):**
- Missing EIA data → treat as `eia_allowed = False` (suppress trading for that period)
- Do NOT forward-fill from prior week (that would extend an outdated reading indefinitely)
- Report the count and date range of any NaN periods in the results document

This means any gap in EIA data acts as a trading suspension — the most conservative possible
interpretation. The alternative (forward-fill) would allow trading based on stale data of
unknown age, which violates causal discipline.

### 2.5 Output format of preprocessed EIA table

After all preprocessing, produce a DataFrame with exactly this structure:

```
columns:  [pub_date_utc, week_ending_date, storage_actual_bcf,
           storage_5yr_avg_bcf, storage_anomaly_pct, eia_allowed]

pub_date_utc:       datetime64[us, UTC]  — publication date at UTC midnight
                    = week_ending_date + 6 days, localized UTC
week_ending_date:   datetime64[us]       — original EIA period date (kept for audit)
storage_actual_bcf: float64
storage_5yr_avg_bcf: float64
storage_anomaly_pct: float64             = (actual - avg) / avg * 100
eia_allowed:         bool                = storage_anomaly_pct < 10.0
                                           False when NaN anomaly
```

Sort by `pub_date_utc` ascending before any join.

---

## 3. Join Logic with NG Bars

### 3.1 The ng12 index after load_leg()

`load_leg()` converts all dates to **UTC-aware** (`datetime64[us, UTC]`) at midnight UTC.

```python
ng = spread_from_series("NG", load_leg("data/raw/ng12_spread.csv"), date_min="2006-07-28")
# ng.index: dtype=datetime64[us, UTC], tz=UTC
```

**The EIA pub_date_utc must be localized to UTC before joining.** A tz-naive EIA date joined
against a tz-aware ng12 index will raise `TypeError: Cannot compare tz-naive and tz-aware
datetime-like objects` — a hard failure, not a silent contamination.

### 3.2 The exact join algorithm

```python
# eia_df: preprocessed EIA table (§2.5), sorted by pub_date_utc
# ng.index: UTC-aware datetime index, length 4969

ng_dates = pd.DataFrame({"bar_date": ng.index})

eia_join = eia_df[["pub_date_utc", "storage_anomaly_pct", "eia_allowed"]].copy()

joined = pd.merge_asof(
    ng_dates.sort_values("bar_date"),
    eia_join.sort_values("pub_date_utc"),
    left_on="bar_date",
    right_on="pub_date_utc",
    direction="backward",
    allow_exact_matches=False,    # ← CRITICAL: strict < semantics (doc 33 §2.6)
)
```

**Result:** `joined` has one row per ng12 bar, with `eia_allowed` representing the most
recent EIA release published STRICTLY BEFORE that bar's date.

### 3.3 Causal alignment proof — worked example

Using real dates from the ng12 series:

```
EIA release schedule (publication dates after +6 day transform):
  pub_date = 2020-03-05 Thu UTC midnight (covers week ending 2020-02-28)
  pub_date = 2020-03-12 Thu UTC midnight (covers week ending 2020-03-06)
  pub_date = 2020-03-19 Thu UTC midnight (covers week ending 2020-03-13)

ng12 bars in this window:
  bar 2020-03-09 Mon → merge_asof backward strict: last pub < 2020-03-09 = 2020-03-05 ✓
  bar 2020-03-10 Tue → last pub < 2020-03-10 = 2020-03-05 ✓
  bar 2020-03-11 Wed → last pub < 2020-03-11 = 2020-03-05 ✓
  bar 2020-03-12 Thu → last pub < 2020-03-12 = 2020-03-05 ✓  (strict: 2020-03-12 is NOT < 2020-03-12)
  bar 2020-03-13 Fri → last pub < 2020-03-13 = 2020-03-12 ✓  (new EIA effective from Friday)
  bar 2020-03-16 Mon → last pub < 2020-03-16 = 2020-03-12 ✓
```

Thursday bar uses prior week's EIA. Friday bar uses current week's EIA. This is exactly
the rule in doc 33 §2.6. The `allow_exact_matches=False` parameter is what enforces this.

### 3.4 The critical parameter: allow_exact_matches=False

`pd.merge_asof` defaults to `allow_exact_matches=True`, which assigns the EIA release to the
same-day Thursday bar. This silently violates doc 33 §2.6. The error would be invisible —
no exception is raised, but Thursday bars would receive the Thursday EIA release that was
published at 10:30am ET that morning. A daily bar opening before 10:30am ET would have
lookahead contamination.

**This is the most dangerous silent failure mode in the entire implementation.** One keyword
argument (`allow_exact_matches=False`) separates a causally clean test from a contaminated one.

### 3.5 Post-join validation

After the join, verify these properties:

```
VALIDATE-A:  No NaN in joined eia_allowed before date_min
             Check: joined.loc[joined['bar_date'] >= '2006-07-28', 'eia_allowed'].isna().sum() == 0
             Fail: NaN eia_allowed → no EIA data covers that bar date → investigate gap

VALIDATE-B:  Thursday bar uses prior week (not same-week) EIA
             Check on a known Thursday, e.g., 2020-03-12:
             joined.loc[joined['bar_date'] == '2020-03-12 UTC', 'pub_date_utc']
             Expected: 2020-03-05 UTC (prior Thursday), NOT 2020-03-12 UTC
             Fail: same-day assignment → allow_exact_matches=True was used accidentally

VALIDATE-C:  Friday bar uses current week EIA
             Check: 2020-03-13 UTC → pub_date = 2020-03-12 UTC ✓
             Fail: pub_date = 2020-03-05 UTC → the +6 day shift was not applied

VALIDATE-D:  eia_allowed fraction sanity
             Compute: fraction of bars where eia_allowed == True
             Expect: approximately 75–85% (glut years ~5/20 years = ~25% excluded)
             Flag if: < 50% → threshold may be too tight for this series
             Flag if: > 95% → threshold may never exclude any bars

VALIDATE-E:  Sunday bars get correct EIA assignment
             The 2 Sunday bars (2011-11-13, 2011-11-20) should receive prior-week EIA numbers
             Verify their pub_date_utc values are from the Thursday before each Sunday
```

---

## 4. Surrogate Conditioning Implementation

### 4.1 The core requirement

Surrogates must use the **same eia_allowed boolean array** as the real instrument.
The eia_allowed mask is a real external variable; it is NOT simulated. All N surrogate paths
(RW, GARCH, OU, Splice) receive the same mask, applied position-by-position.

This ensures the p-value tests: "does real NG respond to the EIA conditioning MORE than a
zero-MR process conditioned on the same EIA history?" — which is the correct question.

### 4.2 Required change to run_fade()

The existing `run_fade(s, theta, cost, lookback, max_hold)` has no entry gating. A new function
`run_fade_conditional(s, theta, cost, allowed_mask, lookback, max_hold)` is required.

Interface spec (pre-committed):

```python
def run_fade_conditional(
    s: np.ndarray,
    theta: float,
    cost: float,
    allowed_mask: np.ndarray,   # shape (n,), dtype bool; True = entry allowed on bar t
    lookback: int = 60,
    max_hold: int = 40,
) -> list[dict]:
    """
    Identical to run_fade() but entry is gated by allowed_mask[t].
    Exit logic is UNCHANGED — exits based on z-reversion or max_hold regardless of allowed_mask.
    A position entered before the mask changes is held to completion (no mid-trade gating).
    Returns same dict structure as run_fade().
    """
```

**Key invariant:** `allowed_mask` gates ENTRY only. An existing position is never force-exited
because the EIA mask changes. This is stated in doc 33 §2.3 and must be preserved.

### 4.3 Surrogate ensemble flow with conditioning

```
1. Compute eia_allowed[0..n-1] from the joined EIA data (one array, computed once)
2. For real NG: run_fade_conditional(s_ng, theta, cost, eia_allowed)
3. For each surrogate type (rw, garch, ou, splice):
   For each of N draws:
     path = generate_surrogate(params, n, rng)
     trades = run_fade_conditional(path, theta, cost, eia_allowed)  # ← SAME mask
     record gross
4. p_rw = fraction of rw surrogate gross values ≥ real gross
```

The `eia_allowed` array is computed ONCE from the real EIA data and passed to all surrogate
runs unchanged. It must NOT be recomputed per surrogate draw.

### 4.4 OU surrogate conditioning — resolution of doc 33 internal contradiction

**Contradiction in doc 33 §4.2:**
- Body text: "Full surrogate suite: RW, GARCH(1,1), OU(φ=0.948), Splice-RW. All four with
  IDENTICAL EIA conditioning applied."
- Kill-criterion table: "p_ou = 1.000 — NOT KILLED — OU doesn't get EIA conditioning."

**Resolution (pre-committed by this document, supersedes doc 33 §4.2 kill-criterion note):**

OU surrogate **DOES** receive the same EIA conditioning as all other surrogates (consistent
with the body text). The kill-criterion note ("OU doesn't get EIA conditioning") was incorrect
and is retracted here.

**Rationale:** Giving OU conditioning makes the comparison fair. An OU process with EIA
conditioning applied would also benefit from trading only in normal-storage regimes. If real
NG still beats conditioned-OU, that is stronger evidence. If conditioned-OU beats conditioned-NG,
the structural OU finding from doc 31 (OU>NG at every threshold) persists even in the conditional
setting — which would be a meaningful finding that the EIA conditioning did not repair the regime
gap.

The p_ou result is non-binding for the verdict (as doc 33 states) regardless of which approach
is used. The resolution is about consistency of test design.

### 4.5 Robustness grid conditioning (Stage 2 appendix §4.4 of doc 33)

The robustness grid tests θ_eia ∈ {5%, 10%, 15%, 20%}. For each θ_eia, a **separate** eia_allowed
array is computed:

```python
eia_allowed_5  = storage_anomaly_pct < 5.0   # most restrictive
eia_allowed_10 = storage_anomaly_pct < 10.0  # primary (pre-committed)
eia_allowed_15 = storage_anomaly_pct < 15.0
eia_allowed_20 = storage_anomaly_pct < 20.0  # most permissive
```

For the robustness grid, surrogates use the **same threshold-specific mask** as the real NG
for that threshold. The primary verdict uses eia_allowed_10 exclusively.

**Computation note:** All four eia_allowed arrays can be computed upfront and passed to the
surrogate ensemble. The Stage 2 robustness grid requires N=500 surrogates × 4 thresholds.
Run the primary (θ_eia=10%) surrogate ensemble first, determine the primary verdict, then
run the robustness grid as a separate non-blocking appendix.

---

## 5. Stage 1 Runbook (N=200 Speed Gate)

### 5.1 Pre-conditions before Stage 1 executes

All of the following must be TRUE before running Stage 1:

```
[ ] EIA data acquired and saved to data/raw/eia_ng_storage_weekly.csv (or equivalent)
[ ] All 7 data validation checks (§1.4) pass
[ ] EIA preprocessed table produced per §2.5 spec
[ ] Join executed per §3.2; all 5 post-join validations (§3.4) pass
[ ] VALIDATE-B confirms allow_exact_matches=False is active (Thursday bar test)
[ ] run_fade_conditional() implemented per §4.2 spec
[ ] eia_allowed computed with θ_eia=10% (primary only; robustness grid deferred to Stage 2)
[ ] Unconditional baseline (run_fade() on full ng12, same parameters as doc 30) confirmed
    reproducible (produces same numbers as doc 31 — this is the regression check)
[ ] OOS conditional trade count estimated (see §5.2) and result documented
```

### 5.2 Pre-run OOS trade count estimate

Before running Stage 1, estimate the number of conditional OOS trades (post-2018):

```python
# Approximate: apply eia_allowed to OOS bars, count |z|≥1.0 bars that are also eia_allowed
# Use the unconditional trade count from doc 31 as baseline: 61 trades in OOS at θ=1.0
# From doc 23: glut years in OOS = 2020, 2025 (2 of 8 OOS years ≈ 25% excluded)
# Expected conditional OOS trades: ~61 * 0.75 ≈ 46 trades
# Kill criterion if < 30 trades: INCONCLUSIVE (not kill)
# Must compute and record before Stage 1 proceeds
```

If estimated OOS conditional trades < 30: **document before running Stage 1** that INCONCLUSIVE
is the expected outcome for the OOS criterion. This is not a reason to abort Stage 1 — it sets
expectations for interpreting the OOS result.

### 5.3 Stage 1 execution sequence

```
Step 1: Load ng12 via load_leg() + spread_from_series() — same as doc 30/31
Step 2: Load preprocessed EIA table; compute eia_allowed_10
Step 3: Join EIA to ng12 bars per §3.2; run all 5 post-join validations
Step 4: Run run_fade_conditional(s, theta=1.0, cost=0.003, eia_allowed_10)
        → conditional_trades_full
Step 5: Run run_fade(s, theta=1.0, cost=0.003)
        → unconditional_trades_full  [same as doc 31; use for comparison]
Step 6: Compute conditional stats: n, gross, net, hit, avg_hold
Step 7: Run N=200 RW surrogates with eia_allowed_10 conditioning
        → surrogate_rw_gross[200]
Step 8: Compute p_rw = pval(conditional_gross, surrogate_rw_gross)
Step 9: Compute OOS split: apply eia_allowed_10 to OOS window (2018+)
        → conditional_oos_trades; record n_oos
Step 10: Apply kill criteria (§4.1 of doc 33):
         KILL if p_rw > 0.20 → write kill result, stop
         KILL if conditional_gross ≤ unconditional_gross → write kill result, stop
         KILL if conditional_net < −0.002 → write kill result, stop
         INCONCLUSIVE if conditional_n < 30 AND oos_n < 20 → note, continue to verify
         GO if all go criteria met
Step 11: Write Stage 1 result to data/processed/eia_conditional_stage1.json
```

### 5.4 Stage 1 output format

```json
{
  "stage": 1,
  "n_surrogates": 200,
  "eia_threshold_pct": 10.0,
  "conditional": {
    "n": <int>,
    "gross": <float>,
    "net": <float>,
    "hit": <float>,
    "avg_hold": <float>
  },
  "unconditional_baseline": {
    "n": 149,
    "gross": -0.0006,
    "net": -0.0036
  },
  "p_rw_200": <float>,
  "oos_conditional_n": <int>,
  "stage1_verdict": "GO" | "KILL_PVAL" | "KILL_NO_IMPROVEMENT" | "KILL_NEGATIVE" | "INCONCLUSIVE",
  "proceed_to_stage2": <bool>
}
```

---

## 6. Hidden Implementation Risks Register

Ordered by severity. Each risk has a specific guard action.

---

### R1 — Week-ending vs publication date (SEVERITY: HIGH / SILENT FAILURE)

**What goes wrong:** EIA API data is indexed by week_ending_date (Friday). Without the +6 day
transform, every bar is assigned storage data 6 days before it was published. This is not
detectable from outputs alone — the test runs, produces p-values, and appears valid.

**Detection:** VALIDATE-C (§3.5) catches this. If Friday bar shows pub_date = week_ending_date
(rather than week_ending + 6 days), the transform was not applied.

**Guard action:** Implement the +6 transform in the preprocessing step (§2.1). Run VALIDATE-C
before any fade logic executes. Abort if VALIDATE-C fails.

---

### R2 — merge_asof allow_exact_matches (SEVERITY: HIGH / SILENT FAILURE)

**What goes wrong:** Default `allow_exact_matches=True` assigns Thursday's EIA to Thursday's bar.
The contamination is small (1 bar per week) but systematic. p-values may improve spuriously for
strategies that enter on Thursdays. Not detectable without an explicit validation check.

**Detection:** VALIDATE-B (§3.5) catches this. Verify that bar 2020-03-12 (Thu) receives
pub_date = 2020-03-05, NOT 2020-03-12.

**Guard action:** Always explicitly pass `allow_exact_matches=False` to `pd.merge_asof`.
Add a comment in the code citing doc 33 §2.6 and this risk register. Run VALIDATE-B before
any fade logic executes. Abort if VALIDATE-B fails.

---

### R3 — OU conditioning inconsistency resolved here (SEVERITY: MEDIUM / METHODOLOGY)

**What goes wrong:** Doc 33 §4.2 contradicts itself — body says all four surrogates get EIA
conditioning, kill-criterion note says OU does not. If implemented inconsistently, the OU
result is not interpretable and the test design violates its own specification.

**Resolution:** §4.4 of this document (binding): OU gets EIA conditioning, same as all others.
The kill-criterion note in doc 33 is retracted.

**Guard action:** In code, OU surrogate calls `run_fade_conditional(ou_path, ..., eia_allowed_10)`,
not `run_fade(ou_path, ...)`. Document this in the script with a comment citing doc 33a §4.4.

---

### R4 — tz-naive EIA vs tz-aware ng12 index (SEVERITY: MEDIUM / HARD FAILURE)

**What goes wrong:** `load_leg()` produces UTC-aware timestamps. EIA pub_date computed from
week_ending + 6 days will be tz-naive unless explicitly localized. The `merge_asof` call
will raise `TypeError: Cannot compare tz-naive and tz-aware datetime-like objects`.

**This is actually a DESIRABLE hard failure** — it is self-announcing and forces the fix.

**Guard action:** Explicitly apply `.dt.tz_localize('UTC')` to pub_date after the +6 day
transform, before the join.

---

### R5 — Thanksgiving and holiday-shifted releases (SEVERITY: LOW / DOCUMENTATION)

**What goes wrong:** In ~20 Thanksgiving weeks (2006–2026), EIA releases Wednesday instead of
Thursday. The +6 day formula assigns these to Wednesday + 6 = Tuesday, which is wrong. The
true publication date is Wednesday.

**Impact:** Approximately 20 of ~1,050 releases (< 2%) have a possible 1-day assignment error.
The direction of the error (assigning 1 day late) means affected Wednesday releases are
effectively treated as if published Thursday. Bars on the Wednesday after Thanksgiving would
use the release from 2 weeks prior instead of the same-week release. Impact on results: minimal.

**Guard action:** Do not attempt to enumerate all holiday exceptions. Instead, document in the
results file: "EIA release dates computed as week_ending + 6 days. Thanksgiving and holiday
weeks may have ±1 day assignment error (estimated 20 occurrences in 2006–2026). Impact on
verdict: negligible."

---

### R6 — OOS conditional trade count below kill floor (SEVERITY: MEDIUM / VERDICT RISK)

**What goes wrong:** Post-2018 OOS period contains glut years 2020 and 2025. The EIA
conditioning excludes these years' bars from entry. OOS conditional trade count may fall
below the 30-trade floor, triggering INCONCLUSIVE rather than KILLED or DEPLOYABLE_CANDIDATE.

**Pre-calculation:** Estimated OOS conditional n ≈ 46 (§5.2). This is above the 30-trade
floor, but not by a large margin. If the threshold has higher exclusion rate than estimated
(e.g., 2020 glut was more prolonged than projected), OOS n could be < 30.

**Guard action:** Compute actual OOS conditional n before proceeding to Stage 1. If n_oos < 30,
the verdict will be INCONCLUSIVE on the OOS criterion, not KILLED. This is acceptable per doc 33
§4.2. Document the OOS n in the Stage 1 output file.

---

### R7 — Sunday bars in ng12 (SEVERITY: LOW / DOCUMENTATION)

**What goes wrong:** Two Sunday bars (2011-11-13, 2011-11-20) persist in the ng12 spread after
`spread_from_series`. These bars have NaN volume. The z-score lookback window includes them as
valid price bars. For the EIA join, they receive the most recent prior-Thursday EIA release —
which is correct per the algorithm (strict <). Their presence slightly distorts the 60-bar
rolling window for adjacent bars.

**Guard action:** Do not filter them out (this would be a methodology change requiring a new
pre-registration). Document their existence in the results file. Their impact on any p-value
or expectancy calculation is negligible.

---

### R8 — Single eia_allowed computation shared across all surrogate runs (SEVERITY: LOW / CORRECTNESS)

**What goes wrong:** If `eia_allowed` is recomputed per surrogate draw (e.g., from a copy of
the data), any floating-point inconsistency could produce different masks across draws. This
would add noise to the surrogate distribution, biasing p_rw slightly.

**Guard action:** Compute `eia_allowed_10 = (storage_anomaly_pct < 10.0)` exactly once after
the EIA join. Pass this array by reference (not by copy) to all surrogate ensemble calls.

---

### R9 — Stage 2 compute time for N=500 × 4 robustness thresholds (SEVERITY: LOW / LATENCY)

**What goes wrong:** The robustness appendix (§4.4 of doc 33) runs N=500 surrogates for each of
{5%, 10%, 15%, 20%}. This is 2,000 total surrogate runs. At the doc 30/31 benchmark (N=500 in
approximately 2-3 minutes on this hardware), the full Stage 2 including robustness grid takes
approximately 8-12 minutes.

**Guard action:** Run the primary (θ_eia=10%) Stage 2 first. Determine and record the primary
verdict. Then run the robustness grid as a separate step. The robustness grid output should be
clearly labelled as "descriptive appendix" in the JSON output file.

---

### R10 — NaN propagation if EIA has coverage gaps (SEVERITY: LOW / DATA QUALITY)

**What goes wrong:** Any week where EIA data is NaN (government shutdown, delayed release)
produces NaN storage_anomaly. The join propagates this NaN to all bars in that week. Without
explicit handling, run_fade_conditional() would encounter NaN in the allowed_mask, potentially
causing silent `True` interpretation (depending on Python bool(NaN) behavior).

**Guard action:** The NaN handling rule in §2.4 is binding: NaN anomaly → eia_allowed = False.
Implement as: `eia_allowed = np.where(np.isfinite(storage_anomaly_pct), storage_anomaly_pct < 10.0, False)`.
Not `storage_anomaly_pct < 10.0` directly (which leaves NaN as NaN in boolean context).

---

## 7. Implementation Pre-flight Summary

Before writing a single line of the test script, confirm:

```
RESOLVED AMBIGUITIES (from this document):
  [x] OU surrogate conditioning: OU DOES get EIA conditioning (§4.4)
  [x] Causal join semantics: allow_exact_matches=False is mandatory (§3.2)
  [x] Date transform: week_ending + 6 days = publication_date (§2.1)
  [x] NaN handling: NaN anomaly → eia_allowed=False, no forward-fill (§2.4)
  [x] Mid-trade gating: exits are NOT conditioned on EIA updates (§4.2)
  [x] Robustness grid: runs after primary Stage 2 verdict is determined (§4.5)

REQUIRED INPUTS:
  [ ] data/raw/eia_ng_storage_weekly.csv  (or equivalent; see §1.1–1.3)
  [ ] All 7 CHECK validations (§1.4) passing
  [ ] All 5 VALIDATE verifications (§3.5) passing
  [ ] Estimated OOS conditional n > 30 (§5.2) or INCONCLUSIVE expectation noted

BLOCKING RISKS CLEARED:
  R1 (week-ending transform) — handled in preprocessing
  R2 (allow_exact_matches) — handled in join with VALIDATE-B gate
  R3 (OU conditioning) — resolved by this document
  R4 (timezone) — hard failure on wrong implementation; forced fix
  R5–R10 — documented, non-blocking, handled by code comments + result-file disclosures
```

Once all checkboxes above are ticked, execution of Stage 1 is authorized.

---

*Markers: BINDING IMPLEMENTATION SPECIFICATION · Resolves doc 33 §4.2 OU conditioning
contradiction · Flags R1 and R2 as silent-failure risks requiring explicit validation gates ·
No parameter changes from doc 33 pre-registration.*
