# Doc 49 — Second-Sleeve IS VR Screening: Pre-Registration

**Document class:** Frozen pre-registration. No parameters, construction choices, splits, or
thresholds may be revised after this document is written and before execution.  
**Date frozen:** 2026-06-10  
**Authorization:** HYPOTHESIS_REGISTRY.md row "Second-sleeve IS VR screening cohort (GC-SI → PL-PA)",
status ACTIVE, proposed 2026-06-10 (doc 48 trader-lens adjudication).  
**Blocking context:** Doc 48 archived RB-CL permanently (third-look p=0.0798 ≥ 0.0167,
3-look alpha budget exhausted) and found LE-GF OOS-STRUCTURAL-WEAKNESS (COVID attribution
FALSIFIED, doc 48 Part II). Combination gate BLOCKED. Programme at single-sleeve LE-GF
IS-anchor status. Tier-1 two-sleeve book requires a second instrument with IS VR confirmation.  
**Runner:** `scripts/run_49_second_sleeve_screening.py` (to be written per this spec)  
**Output:** `data/processed/49_results.json`

---

## Gate Position (Strategic Dependency Graph)

```
apparatus-trust (§11.8 — LE-GF confirmed doc 46)
  → controlled-β admissibility (F5 presample-OLS, doc 46 established)
    → cohort breadth (THIS DOC: screen GC-SI then PL-PA for IS VR)
      → per-instrument positive expectancy (separate economics prereg, if IS screen passes)
        → portfolio construction
          → book cost test
            → deployable book
```

**This document gates:** cohort breadth — specifically whether a second instrument joins the
admissible pool alongside LE-GF.

**What it does NOT unlock directly:** per-instrument positive expectancy, portfolio construction,
book cost test. Those require a separate, subsequent pre-registration for OOS economics
(Sharpe > 0.50, n ≥ 30 at cost floor 0.005).

---

## Part I — Hypothesis

**GC-SI:** The IS raw spread of Gold (COMEX GC2!) minus β_GC-SI × Silver (COMEX SI2!) exhibits
sub-diffusive variance ratio VR(20) < 1 in the pre-committed IS window, relative to a random-walk
null, with p_rw < 0.025 (Bonferroni-adjusted; see §Multiplicity below).

**PL-PA (conditional on GC-SI failing):** The IS raw spread of Platinum (NYMEX PL2!) minus
β_PL-PA × Palladium (NYMEX PA1!) exhibits sub-diffusive VR(20) < 1 in the pre-committed IS
window, with p_rw < 0.025.

Both are one-sided (sub-diffusion only). Super-diffusive VR > 1 is not a pass under any
circumstance.

---

## Part II — Construction

### Instrument 1: Gold–Silver (GC-SI)

#### Economic prior and β-mode justification

Gold–Silver is the textbook cointegration pair in commodity finance (Escribano and Granger 1998;
Wahab, Cohn and Lashgari 1994). Both legs are priced in USD per troy oz on COMEX — same unit,
same exchange. However, F6 (β=1 definitional) is NOT admissible here. The 1:1 unit argument
holds geometrically but not economically: gold trades at approximately 80× the price of silver
(the gold-silver ratio), so a 1 oz gold vs 1 oz silver spread is structurally trending with
the ratio and has no stable equilibrium. A β=1 construction would produce a trending object
mis-labelled as a mean-reverting spread — this is the exact failure mode doc 42 documented for
cross-commodity pairs.

**β-mode: F5 — presample full-OLS, pre-sample fraction = first 25% of the merged aligned
series, frozen for the entire remaining sample. Never re-estimated.**

Construction procedure:
1. Load `COMEX_DL_GC2!, 1D.csv` and `COMEX_DL_SI2!, 1D.csv`.
2. Inner-join on timestamp. Drop any bar where either leg is NaN or zero.
3. Apply roll-mask: drop bars where |Δprice| / price > k=8.0 (same threshold as prior docs).
4. Split the aligned, masked series at the first 25% of valid bars. Call this the pre-sample.
5. Run OLS of GC2! on SI2! (no intercept suppression — include intercept) over the pre-sample.
   Freeze the slope as β_GC-SI. Never update.
6. Construct spread S_t = GC2!_t − β_GC-SI × SI2!_t for all t in the full series.
7. All VR tests operate on the RAW spread S_t (not log-transformed, not deseasonalized).

**Log-price alternative (informational only):** A log-spread log(GC2!/SI2!) is the natural
object when ratio-cointegration is hypothesized (the gold-silver ratio); however the primary
construction is the level spread with F5 OLS β as above. If the primary construction fails,
informational reporting of log-spread VR is permitted but does not change the kill verdict and
does not constitute a rescue. Log-spread is NOT the primary hypothesis and MUST NOT be used
to override a kill.

**No deseasonalization:** precious metals spreads do not have a well-documented seasonal
production cycle analogous to livestock. Deseasonalization is not applied. If applied, it
would require its own pre-registration demonstrating a causal seasonal mechanism.

#### §11.8 dual role of GC-SI

GC-SI is simultaneously:
- The candidate second-sleeve instrument (primary purpose of this doc)
- The strongest remaining §11.8 apparatus-recalibration candidate: Escribano–Granger 1998 and
  Wahab et al 1994 provide published IS evidence of gold–silver cointegration. If the apparatus
  fails to confirm IS VR in GC-SI, that is an **apparatus-recalibration signal** per §11.8
  ("recalibrate the apparatus, not the market"). It does NOT mean gold–silver has no edge. It
  means the programme must stop and investigate why a known literature-documented reverter is
  not being detected, before any further negative results can be trusted.

**Apparatus recalibration trigger (binding):** GC-SI fails IS VR at N=500 (p_rw ≥ 0.025) →
BEFORE proceeding to PL-PA, the runner must compute and report: (a) realized VR(20) value;
(b) comparison to literature-implied VR range; (c) whether the test has adequate power at the
observed VR (using the corrected increments-AR(1) power simulation — see §Power below);
(d) whether the failure is a power issue or a genuine absence claim. If power < 0.40 at the
observed VR, the result is INCONCLUSIVE-UNDERPOWERED, not a clean miss, and the §11.8
investigation must be documented before the screening can proceed.

---

### Instrument 2: Platinum–Palladium (PL-PA)

Tested ONLY if GC-SI fails its IS VR screen (p_rw ≥ 0.025 at N=500). If GC-SI passes, PL-PA
is not screened in this document; it remains DEFERRED.

#### Economic prior and β-mode justification

Platinum and palladium are both platinum-group metals (PGMs) used primarily in autocatalytic
converters. Both are priced in USD per troy oz. As with GC-SI, same-unit same-exchange does
not imply β=1: PL and PA trade at materially different price levels (PL approximately $950–1050,
PA approximately $900–1100 as of mid-2026, but historically PL was 2–3× PA), so 1:1 is not
the equilibrium construction.

**β-mode: F5 — presample full-OLS, pre-sample fraction = first 25% of merged aligned series,
frozen for the entire remaining sample. Never re-estimated.**

Construction procedure: identical to GC-SI above, substituting PL2! for GC2! and PA1! for
SI2!.

**Leg files:**
- Platinum leg: `NYMEX_DL_PL2!, 1D.csv` (second-continuous futures; consistent with PA1!
  being the first-continuous, which is the only PA leg available; both are TradingView
  continuous adjusted). NOTE: the manifest lists TVC_PLATINUM as PROVISIONAL and flags it as
  a spliced composite requiring trimming. The `NYMEX_DL_PL2!, 1D.csv` file exists in
  `data/raw/more-mean-reversion-data/` and is preferred as NYMEX futures data. If PL2! and
  PA1! have alignment issues due to different contract months, the runner must report the
  aligned bar count; if < 2000 aligned bars, PL-PA is declared INSUFFICIENT and marked
  DEFERRED-DATA.
- Palladium leg: `NYMEX_DL_PA1!, 1D.csv` (TRUSTED, 10261 bars per manifest).

No deseasonalization. Raw spread only.

---

### Common construction parameters (both pairs)

| Parameter | Value |
|---|---|
| Roll-mask threshold | k = 8.0 (frozen, same as all prior docs) |
| β estimation window | first 25% of aligned post-mask valid bars (F5) |
| β update policy | NEVER — frozen after pre-sample estimation |
| f_βupdate | 0.000 (frozen β → zero by construction) |
| f_βupdate gate | < 0.10 (10% of Var(ΔS)) — trivially satisfied; stated for protocol completeness |
| Spread construction | S_t = Leg1_t − β × Leg2_t (levels, not log, unless log variant flagged as informational) |
| VR test series | First-differences of S_t, i.e. ΔS_t |
| Deseasonalization | NO |

---

## Part III — IS/OOS Split

**Rule (binding; governs over any approximated date):** chronological 70/30 split of the
aligned, roll-masked valid bars. The first 70% of valid bars form the IS period; the remaining
30% form the OOS period. The split is defined by the row count of the aligned merged series
after masking, not by a calendar date. The calendar date of the split boundary is reported
as informational output.

**Lesson from doc 48 (binding):** the prereg's prose date approximations were wrong (stated
"≈2014-08" but actual OOS start was 2019-05-24 because LE-GF data begins 2002, so 70% of
5890 bars = 4123 IS bars). The RULE was correct and was followed. This doc states only the
rule; approximate dates are for orientation only and are marked approximate.

**GC-SI approximate dates (orientation, NOT binding):**
- Manifest: GC2! 8786 bars, 1991-06-26 to 2026-06-03; SI2! 11186 bars, 1981-12-17 to 2026-06-03
- Aligned series is bounded by GC2! start (≈1991-06-26); estimated aligned bars ≈ 8786 (GC2! is the shorter leg)
- Pre-sample (first 25% for β): ≈ 2197 bars (≈ 1991-06 to ≈ 1999-12, approximate)
- IS (first 70%): ≈ 6150 bars (≈ 1991-06 to ≈ 2015-xx, approximate)
- OOS (last 30%): ≈ 2636 bars (≈ 2015-xx to 2026-06-03, approximate)
- All "≈" above are orientation only; the 70/30 row-count rule governs

**PL-PA approximate dates (orientation, NOT binding):**
- Manifest: PA1! 10261 bars, 1985-08-26 to 2026-06-03; PL2! not separately listed in manifest daily section but present in raw data
- Aligned series bounded by the shorter or later-starting leg; estimated aligned bars ≈ 10261 (if PL2! covers the same period) or less
- Pre-sample (25%): ≈ 2565 bars (≈ 1985-08 to ≈ 1995-xx, approximate)
- IS (70%): ≈ 7183 bars (≈ 1985-08 to ≈ 2013-xx, approximate)
- OOS (30%): ≈ 3078 bars (≈ 2013-xx to 2026-06-03, approximate)
- All "≈" above are orientation only; the 70/30 row-count rule governs

**Critical:** the 25% pre-sample for β estimation is taken from the FULL aligned series (i.e.,
the first 25% of the 100%). The IS period is the next 45% (rows 25%–70%). The OOS period is
rows 70%–100%. This means the IS VR test operates on the middle 45% of the data, not the
first 70%. This is correct and intentional: it replicates the doc 46 F5 protocol exactly
(LE-GF: pre-sample = first 1472/5890 = 25%, IS = next 2651 bars, OOS = last 1767 bars).

---

## Part IV — Frozen Constants Block

```python
# ============================================================
# DOC 49 FROZEN CONSTANTS — DO NOT MODIFY AFTER PRE-REGISTRATION
# ============================================================

# --- Pair 1: Gold–Silver ---
GC_FILE  = "data/raw/more-mean-reversion-data/COMEX_DL_GC2!, 1D.csv"
SI_FILE  = "data/raw/more-mean-reversion-data/COMEX_DL_SI2!, 1D.csv"

# --- Pair 2: Platinum–Palladium (screened only if GC-SI fails) ---
PL_FILE  = "data/raw/more-mean-reversion-data/NYMEX_DL_PL2!, 1D.csv"
PA_FILE  = "data/raw/more-mean-reversion-data/NYMEX_DL_PA1!, 1D.csv"

# --- Construction ---
ROLL_MASK_K        = 8.0          # |ΔP|/P threshold; bars above this → NaN
PRESAMPLE_FRAC     = 0.25         # first 25% of aligned bars → β estimation
IS_FRAC            = 0.70         # first 70% of aligned bars → IS (includes pre-sample)
# OOS_FRAC = 0.30 implied
BETA_UPDATE_POLICY = "FROZEN"     # never re-estimated after pre-sample
F_BETA_UPDATE_HALT = 0.10         # gate; 0.000 by construction for frozen β

# --- Primary statistic ---
VR_Q_PRIMARY       = 20           # Lo-MacKinlay lag; primary gate
VR_Q_GRID          = [2, 5, 10, 20, 40]  # full grid; informational except q=20

# --- Null families ---
NULL_FAMILIES      = ["rw", "garch", "ma1", "ou"]
# rw   = PRIMARY GATE (gating)
# garch = GARCH(1,1) surrogate (supporting)
# ma1   = MA(1)-noise surrogate (supporting; mandatory for spread tests)
# ou    = OU matched surrogate (non-gating reference)

# --- Surrogate counts ---
N_SURR_SPEED  = 200               # speed gate
N_SURR_FULL   = 500               # full test

# --- Seeds (frozen) ---
SEED_GC_SI    = 20260610          # GC-SI all surrogate runs
SEED_PL_PA    = 20260611          # PL-PA all surrogate runs (different seed, different pair)

# --- α procedure (see §Multiplicity) ---
# Fixed-sequence (Bonferroni-like) procedure:
# GC-SI tested first at α=0.025 (familywise α=0.05 / 2 max instruments)
# PL-PA tested second (only if GC-SI fails) at α=0.025
# Familywise α preserved at ≤ 0.05 regardless of outcome ordering
PASS_P_RW_SPEED    = 0.20         # kill if p_rw(N=200) > 0.20 (drop instrument, move to next)
PASS_P_RW_FULL     = 0.025        # pre-committed full-test threshold (both instruments)

# --- Kill thresholds ---
JACKKNIFE_DROP_MAX = 3.00         # 300% of full-IS VR; kill if exceeded
OOS_MIN_TRADES     = 30           # OOS sign-reversal gate requires n_trades ≥ 30

# --- Cost grid (IS economics, informational only at IS screen stage) ---
COST_PRIMARY       = 0.005        # primary cost assumption (fraction of spread price)
COST_GRID          = [0.003, 0.005, 0.008]

# --- Power simulation (corrected pattern from doc 48 four-lens review) ---
POWER_SIM_N_SURR   = 500          # paths per power simulation
# AR(1) INCREMENTS cumulated — NOT levels (doc 48 bug: level-AR(1) manufactures VR≈0.047)
# Pattern: dr[0]=ε[0]; dr[t]=φ*dr[t-1]+ε[t]; path = cumsum(dr)
# Calibrate φ by binary search until theoretical VR(20) = realized_vr_is
# Verify: run the path through the VR function; confirm realized VR ≈ calibrated target ≤ 0.01 error

# ============================================================
# END FROZEN CONSTANTS
# ============================================================
```

---

## Part V — Primary Statistic

**VR(q) — Lo-MacKinlay (1988) variance ratio** at q=20, computed on ΔS_t (first differences
of the IS raw spread), surrogate-relative against four null families.

Formula: VR(q) = Var(S_t − S_{t-q}) / (q · Var(S_t − S_{t-1}))

Under RW: VR(q) = 1. Sub-diffusion (mean reversion): VR(q) < 1.

Primary gate: VR(20) against RW surrogate distribution (N=500 paths), one-sided (lower tail).
p_rw = fraction of surrogate VR(20) values ≤ observed VR(20).
Kill if p_rw ≥ PASS_P_RW_FULL = 0.025.

The full q grid {2, 5, 10, 20, 40} is computed and reported. No argmax selection. The q=20
value is the pre-committed primary; other lags are informational and do NOT change the verdict.

---

## Part VI — Null Families

All four nulls are run on every instrument that reaches N=500. Surrogates are conditioned to
match the real IS series.

### RW (PRIMARY — gating)
Surrogate: shuffle ΔS_t (bootstrap the increments). Preserves marginal increment distribution;
destroys autocorrelation structure. p_rw is the primary gate.

### GARCH(1,1) (supporting)
Surrogate: fit GARCH(1,1) to ΔS_t IS period; generate N=500 paths of length n_IS from fitted
parameters; compute VR(20) for each. GARCH captures volatility clustering without mean
reversion. p_garch = fraction of surrogate VR(20) ≤ observed.

### MA(1)-noise (supporting, mandatory for spread tests)
Surrogate: fit MA(1) to ΔS_t IS period; simulate N=500 MA(1) paths of length n_IS; compute
VR(20). MA(1) noise can appear sub-diffusive at short lags; mandatory per programme doctrine
for all calendar and spread tests to rule out MA(1) as the complete explanation.

### OU (non-gating reference)
Surrogate: fit OU process (θ, μ, σ) to S_t IS period; simulate N=500 OU paths of length n_IS;
compute VR(20). OU is mean-reverting by construction. If p_ou < p_rw, the real series reverts
faster than a matched OU process — an upgrade signal. If p_ou > p_rw, the OU surrogate already
spans the observed sub-diffusion — a useful reference. Does NOT gate the verdict.

---

## Part VII — Multiplicity Adjudication

**Procedure: fixed-sequence (hierarchical) gatekeeping.**

Rationale: GC-SI has strong economic prior (textbook cointegration, multiple published
confirmations, §11.8 anchor status). PL-PA is a secondary candidate with a valid but weaker
prior. The fixed-sequence procedure allocates full α=0.025 to the prior-favored candidate
(GC-SI) and tests PL-PA only if GC-SI fails. Familywise α (FWER) is preserved at ≤ 0.05
without Bonferroni penalty on GC-SI. This is a standard fixed-sequence (hierarchical testing)
procedure and is appropriate when the ordering is justified by pre-data economic priors — which
it is here, explicitly.

Rejected alternative (α=0.0167 per instrument, standard Bonferroni over 2 instruments): this
would penalize GC-SI unnecessarily given the strength of its economic prior. With VR effects
in the 0.80–0.90 range and IS bars ≈ 6000–7000, α=0.025 provides adequate control.

**Fixed-sequence rules:**
1. Test GC-SI at α_primary = 0.025 (PASS_P_RW_FULL).
2. If GC-SI PASSES: stop. Report GC-SI result. PL-PA not screened. No multiplicity issue.
3. If GC-SI FAILS: test PL-PA at α_primary = 0.025 (same threshold).
   Familywise α ≤ 0.025 + 0.025 = 0.05. This is conservative (the sum overstates actual
   FWER when tests are conditionally sequential, not simultaneous).
4. If both fail: declare cohort exhausted (see §Kill Tree).

**Speed gate (both instruments):** p_rw(N=200) > 0.20 → kill instrument, no full test.
Speed-gate kills do not consume alpha — they are pure efficiency filters.

---

## Part VIII — Power Simulation (Mandatory)

Power simulation is MANDATORY per doc 48 four-lens review lesson: the doc-48 original power
sim built AR(1) in LEVELS, whose realized VR(20) ≈ 0.047 (extreme sub-diffusion), manufacturing
claimed power=1.000 — caught and corrected by the statistical and adversarial lenses; corrected
power was 0.284.

**Corrected pattern (from `scripts/run_48_rb_cl_alt_split_le_gf.py` lines ~499-511):**

```python
# AR(1) increments cumulated — NOT levels
dr[0] = eps[0]
for t in range(1, n_is):
    dr[t] = phi * dr[t-1] + eps[t]
path = np.concatenate(([0.0], np.cumsum(dr)))
```

Calibration: binary search φ such that vr_ar1_theoretical(φ, q=20) ≈ VR_IS_OBSERVED. Verify
by running the simulated path through the VR function; confirm realized VR within ±0.01 of
target.

Power is reported at:
- observed IS VR (the primary power figure)
- VR = 0.90 (reference point for comparison with other instruments)

If power < 0.30 at the observed IS VR: the VR test is **UNDERPOWERED** — a non-detection result
cannot be interpreted as evidence of absence. The result is INCONCLUSIVE-UNDERPOWERED (not a
clean kill). For GC-SI, this triggers the §11.8 apparatus-recalibration investigation.

---

## Part IX — Jackknife Concentration

For every instrument reaching N=500 full test: divide the IS period into 5 equal contiguous
blocks. Drop each block in turn. Compute VR(20) on the remaining 4 blocks. Report min, median,
max, and max-drop relative to full-IS VR(20).

Kill if: max-drop > 300% of full-IS VR deviation from 1.0. (i.e., if full VR=0.85, deviation=0.15;
kill if any jackknife block produces VR > 0.85 + 3×0.15 = 1.30 OR < 0.85 − 3×0.15 = 0.40.)
In practice: jackknife VR must remain within a range that does not imply the signal is concentrated
in a single block.

---

## Part X — OOS Secondary Characterisation (Informational)

OOS VR and IS economics are reported for instruments that pass the IS VR screen. They are
informational only at this stage — OOS confirmation is NOT the criterion for this pre-registration.
OOS confirmation is the subject of a SEPARATE, SUBSEQUENT pre-registration for economics.

OOS reported:
- VR(20), p_rw (N=500, informational)
- IS economics: n_trades, mean_net at COST_GRID, Sharpe (at θ=1.0 z-entry, LB=60, MH=40,
  same defaults as doc 46/48) — informational only

The OOS sign-reversal kill applies if an instrument passes IS VR AND OOS n_trades ≥ 30:
if mean_net_OOS < 0 at COST_PRIMARY=0.005, flag as OOS-SIGN-REVERSAL (note: does NOT kill the
IS VR result, which is the primary gate here, but must be reported).

---

## Part XI — Kill Tree (ordered, binding)

Each kill criterion is evaluated in order. First triggered criterion terminates the instrument
(move to next instrument in sequence).

### Per-instrument kill criteria:

1. **f_βupdate ≥ 0.10**: construction-inadmissible. HALT instrument. (Will be 0.000 by frozen-β
   construction; stated for protocol completeness.)

2. **Aligned bar count < 2000 after masking**: INSUFFICIENT-DATA. Mark instrument DEFERRED-DATA.
   Move to next.

3. **Speed gate: p_rw(N=200) > 0.20**: kill instrument at speed gate. No full test. Move to next.

4. **Jackknife drop > 300%**: kill instrument (concentration-unstable). Move to next.

5. **Full test: p_rw(N=500) ≥ 0.025**: IS VR not confirmed. Apply §11.8 apparatus check if
   instrument is GC-SI (see above). Move to next.

6. **Passes all above**: IS VR CONFIRMED. Stop screening. Proceed to economics pre-registration.

### Cohort-level outcomes:

**GC-SI PASSES (p_rw < 0.025 at N=500):**
- Stop screening. PL-PA deferred.
- Registry: GC-SI → ACTIVE-IS-CONFIRMED.
- Next action: write separate economics pre-registration (OOS Sharpe > 0.50, n ≥ 30, at
  cost floor 0.005) before combination reopening.

**GC-SI FAILS + apparatus check finds apparatus SOUND (power ≥ 0.30 at observed VR):**
- Proceed to PL-PA screen.
- GC-SI → SCREENED-NEGATIVE (not ARCHIVED — this is a single look, not a multi-look programme).

**GC-SI FAILS + apparatus check finds UNDERPOWERED (power < 0.30):**
- Result is INCONCLUSIVE-UNDERPOWERED.
- §11.8 apparatus-recalibration investigation is REQUIRED before proceeding.
- Recalibration report must document: observed VR, power at observed VR, what a confirmatory
  apparatus would require (n, VR target), whether the data depth is the binding constraint.
- After recalibration report: if recalibration finds apparatus adequate at a different VR target
  → GC-SI is SCREENED-NEGATIVE (proceed to PL-PA). If apparatus is insufficient for any
  economically-meaningful VR range → escalate to researcher with specific data-depth recommendation.

**PL-PA PASSES (p_rw < 0.025 at N=500):**
- IS VR CONFIRMED for PL-PA.
- Registry: PL-PA → ACTIVE-IS-CONFIRMED.
- Next action: economics pre-registration for PL-PA.

**PL-PA FAILS (p_rw ≥ 0.025 at N=500):**
- Both cohort instruments screened negative.
- Declare: SPREAD-MR BOOK INFEASIBLE AT CURRENT COHORT BREADTH.
- Registry: both → SCREENED-NEGATIVE; Portfolio/book row → BLOCKED-COHORT-EXHAUSTED.
- Surface to researcher: the 46 TRUSTED legs do not yield a second liquid commodity spread
  with IS VR confirmation at the programme's standard threshold; recommend either (a) expanding
  the cohort to Indian equity pairs or FX pairs (different asset class, different economics
  pre-registration) or (b) re-evaluating whether single-sleeve LE-GF operation is the
  primary path.

---

## Part XII — §11.8 Apparatus Recalibration Statement

Per §11.8 and the doc 48 four-lens trader-lens adjudication: Gold–Silver is the strongest
remaining §11.8 anchor candidate in the programme. If the apparatus cannot confirm IS VR in
GC-SI — a pair with multiple published confirmations in the commodity finance literature — the
null hypothesis is NOT "gold-silver no longer cointegrates." The null hypothesis is "something
is wrong with the construction, the data, the test, or the statistical power."

Apparatus recalibration is not optional if GC-SI fails. It is a binding pre-condition to
any further kill claims against the spread-MR programme. A test that cannot detect a known
effect cannot credibly report absence elsewhere.

---

## Part XIII — Survive Criteria (Positive Result)

For an instrument to constitute a positive result (IS VR confirmation):

1. f_βupdate = 0.000 (frozen β — trivially satisfied)
2. Aligned bars ≥ 2000
3. Speed gate: p_rw(N=200) ≤ 0.20
4. Jackknife drop ≤ 300%
5. Full test: p_rw(N=500) < 0.025 (pre-committed Bonferroni-adjusted α)
6. VR(20) < 1.0 (sub-diffusion direction confirmed)
7. All four surrogate families reported (not gating; coherence context)

Meeting all six criteria for at least one instrument constitutes a positive result for this
pre-registration. It does NOT constitute a deployable book; it opens the economics gate.

---

## Part XIV — Temporal Firewall Statement

The IS period must be fully pre-committed before any data is touched. The 70/30 split rule
governs; no look at OOS during IS VR testing. The pre-sample β estimation window (rows 0 to
25% of the aligned series) is logically prior to the IS test window (rows 25% to 70%). No
information from the IS or OOS windows may be used in β estimation.

Deseasonalization is NOT applied; this removes the causal-seasonal-window lookahead risk
that was identified in the doc 38/38a back-adjustment diagnostic.

OOS data is accessed only after the IS verdict is finalized and recorded.

---

## Part XV — Non-Goals

This pre-registration does NOT:

- Test OOS economics, Sharpe, or trade-level expectancy (those are gated behind a separate
  economics pre-registration)
- Re-examine RB-CL (PERMANENTLY ARCHIVED, doc 48; no fourth look under any circumstance)
- Reopen LE-GF OOS weakness (OOS-STRUCTURAL-WEAKNESS diagnosis stands; a separate LE-GF
  OOS mechanism pre-registration would be required to revisit this)
- Re-examine NG selectivity (KILLED — p_ou=1.000 everywhere, doc 23/31; EIA KILLED doc 34)
- Test deseasonalization, regime conditioning, or selective entry rules
- Make portfolio-construction decisions
- Produce a deployable book or book-level cost test
- Use rolling-OLS-β (INADMISSIBLE per doc 19)
- Produce UI output or visualization infrastructure
- Test any instrument outside the named cohort (GC-SI, PL-PA) without a new pre-registration

---

## Part XVI — Next Gate

If this test passes (at least one instrument IS VR confirmed):

**Immediate next action:** write a separate pre-registration for the confirmed instrument
covering:
- OOS economics: mean_net > 0 AND Sharpe > 0.50 at COST_PRIMARY=0.005
- n_OOS_trades ≥ 30 for binding verdict
- Comparison against the LE-GF OOS result (same cost, same θ defaults)
- Independence check (ρ) between confirmed instrument and LE-GF IS residuals

If that economics pre-registration passes: the combination pre-registration (portfolio/book
row in the registry) can be reopened with two qualified sleeves.

If this test fails (both instruments screened negative): surface to researcher, escalate per
§Kill Tree above.

---

## Summary of Frozen Choices

| Decision | Choice | Justification |
|---|---|---|
| β-mode (GC-SI) | F5 presample-OLS (frozen) | Same unit ($/oz) but 80× price ratio → β=1 inadmissible; F5 is doc-46-proven workhorse |
| β-mode (PL-PA) | F5 presample-OLS (frozen) | Same logic; PL/PA prices differ historically 2–3×; β=1 inadmissible |
| Pre-sample fraction | 25% | Replicates doc 46 LE-GF F5 protocol exactly |
| IS/OOS split | 70/30 chronological (row-count rule) | Pre-committed rule, not date; lesson from doc 48 prose error |
| Primary statistic | IS VR(20), RW null, N=500 | Exact doc-46 apparatus |
| q grid | {2, 5, 10, 20, 40} reported; q=20 primary | Full grid, no argmax; q=20 pre-registered |
| α procedure | Fixed-sequence: GC-SI first at α=0.025; PL-PA second (if GC-SI fails) at α=0.025 | FWER ≤ 0.05; preserves power for prior-favored candidate; justified by published economic priors |
| Speed gate | p_rw(N=200) > 0.20 → kill | Programme standard |
| Jackknife | 5-block, max-drop ≤ 300% | Programme standard |
| Power simulation | Increments-AR(1) cumulated, realized VR verified; corrected doc-48 pattern | Mandatory; corrected pattern eliminates level-AR(1) artifact (doc 48 four-lens fix) |
| Deseasonalization | None | No documented precious metals seasonal production cycle; back-adj contamination risk |
| Cost grid | 0.003 / 0.005 / 0.008 (primary 0.005) | Programme standard; informational at IS screen stage |
| Seeds | GC-SI: 20260610; PL-PA: 20260611 | Frozen; different per pair |
| Log-price variant | Informational only; does not override kill | Methodological completeness; primary is level spread |
| Screening order | GC-SI then PL-PA | Trader-lens adjudicated on economic priors BEFORE any VR inspection |

*Pre-registration frozen 2026-06-10. No parameter, construction choice, split, or threshold
may be revised after this date and before execution.*

---

## REVISION 1 — 2026-06-10 (Adversarial Audit Corrections)

**Provenance marker:** REVISED. Corrections adjudicated by the pre-registration architect following
an adversarial audit that found MEASUREMENT + METHODOLOGY defects in the original frozen block. The
original text above is retained unmodified (no silent rewrites). All changes are additive or
clarifying; no frozen constant (α, seeds, q, splits, β-mode) is altered. Each correction is numbered
to match the audit's numbered items.

---

### R1. PA1! Data Status — On-Disk Verified

**MEASUREMENT correction.**

`NYMEX_DL_PA1!, 1D.csv` is **on-disk verified** as of 2026-06-10. The file has been copied to
`data/raw/more-mean-reversion-data/` and matches the manifest entry exactly:

```
Manifest:  NYMEX_DL_PA1! — TRUSTED · 10261 bars · 1985-08-26..2026-06-03
On-disk:   data/raw/more-mean-reversion-data/NYMEX_DL_PA1!, 1D.csv — 10261 rows confirmed
```

PA2! does NOT exist in any data source and must not be substituted. The runner must assert
this file is present and readable before any construction begins; failure to open the file is
a BUG (see R2 below), not a data verdict.

---

### R2. Kill-Tree Leaf Separation — Infrastructure Failure vs. Data Verdict

**METHODOLOGY correction.** The original kill tree (Part XI) conflated file-not-found/infrastructure
failure with genuine data-insufficiency verdicts. These are distinct leaves with distinct actions.

**Binding rule (prepended to kill tree, evaluated before all numbered criteria):**

**Kill criterion 0 (pre-condition, evaluated before criterion 1):**

```
For each leg file in the pair:
  - Attempt to open and read the file.
  - If FileNotFoundError / IOError / unreadable: → HALT immediately.
    Do NOT record a DEFERRED-DATA or SCREENED-NEGATIVE verdict.
    Surface as: BUG — infrastructure failure (file missing or unreadable): <filename>
    The pair is NOT killed. It is suspended pending bug resolution.
    No verdict is recorded in the registry until the file issue is resolved.
  - If file opens but aligned-bar count < 2000 after masking: → DEFERRED-DATA verdict.
    This is a genuine data-insufficiency verdict (original kill criterion 2; now criterion 2
    in the revised kill tree below).
```

The runner must distinguish and report these two cases with different exit codes and different
registry entries. A BUG exit must not write any VR or verdict output.

**Revised kill tree order (binding, replaces Part XI per-instrument list):**

0. **File unreadable / FileNotFoundError** → BUG (halt, surface, no verdict)
1. **f_βupdate ≥ 0.10** → construction-inadmissible. HALT instrument.
2. **Aligned bar count < 2000 after masking** → DEFERRED-DATA verdict. Move to next.
3. **Speed gate: p_rw(N=200) > 0.20** → kill at speed gate. No full test. Move to next.
4. **Jackknife drop > 300%** → kill (concentration-unstable). Move to next.
5. **Full test: p_rw(N=500) ≥ 0.025** → IS VR not confirmed. Apply §11.8 check if GC-SI.
6. **Passes all above** → IS VR CONFIRMED. Stop. Proceed to economics pre-registration.

---

### R3. GC-SI Look-Count Disclosure (§4 Zombie-Reopen Surfacing)

**METHODOLOGY correction.** Multiplicity transparency requirement: the pre-registration must
disclose the full prior-look history for GC-SI under any construction, to satisfy the §4
zombie-prohibition and permit honest α accounting.

**Disclosure (binding, added to Part VII — Multiplicity Adjudication):**

GC-SI was previously used in doc 18/19 as the pre-registered DECISIVE instrument for the
intercommodity spread programme. In that prior look (doc 18), GC-SI exhibited VR(2..20)
ranging from 1.62 to 5.93, with p=1.0 across all null families (a strong trending, super-
diffusive object). HOWEVER: that prior look used **rolling-OLS-β-on-levels**, which was
subsequently proven construction-INVALID (doc 19, kill-ledger entry). Doc 19 established that
rolling-OLS-β-on-levels mechanically manufactures VR≫1 as a construction artifact — the doc 18
number carries **zero evidential weight** for or against the actual market behavior of GC-SI.
The prior verdict was therefore UNRESOLVED (not a market claim; a construction kill).

**Why the prior objection no longer binds:** F5 frozen-presample-OLS is a structurally
different construction. It was validated as admissible in doc 46 (LE-GF F5, f_βupdate=0.000 by
construction). The doc 18/19 VR numbers were generated by an inadmissible construction and
provide no information about what F5 will produce on GC-SI.

**Look-count accounting:**

```
Doc 18/19 GC-SI (rolling-OLS-β, INADMISSIBLE construction): look #0 — VOID, construction kill.
                                                               Does not count as a statistical look.
Doc 49 GC-SI (F5 frozen-OLS, ADMISSIBLE construction):       look #1 under any admissible construction.
```

This screening is therefore look #1 for GC-SI under an admissible construction. The fixed-
sequence α=0.025 already incorporates a conservative margin; the single admissible-look history
does not require further α reduction. This disclosure is made for institutional memory
completeness per §4 zombie-reopen protocol, not because it changes the α budget.

---

### R4. PL-PA Construction — PL1! Manifested Status Check and Decision

**MEASUREMENT + METHODOLOGY correction.**

The adjudication instruction: use PL1!/PA1! IF PL1! is manifest-TRUSTED; else keep PL2!/PA1!
with explicit roll-schedule-mismatch caveat.

**Finding:** `NYMEX_DL_PL1!, 1D.csv` and `NYMEX_DL_PL2!, 1D.csv` are both present on disk in
`data/raw/more-mean-reversion-data/`. Neither appears in `data/mr_cohort_manifest.md` as a
named TRUSTED or PROVISIONAL entry. The manifest's PL-PA constructible spread row reads:
"platinum is TVC composite (trim)" — indicating `TVC_PLATINUM` (PROVISIONAL, 10576 bars,
flat-bar-contaminated early history) was the original manifest's designated platinum source.
`NYMEX_DL_PL1!` is an unmanifested file: on-disk but never formally evaluated for TRUSTED
status in the cohort manifest.

**Decision (binding):** PL1! is NOT manifest-TRUSTED. The PL leg for this pre-registration
remains **`NYMEX_DL_PL2!, 1D.csv`** (second-continuous), paired with **`NYMEX_DL_PA1!, 1D.csv`**
(first-continuous, TRUSTED per manifest).

**Roll-schedule mismatch caveat (now binding, per adjudication):** PL2! (second-continuous)
and PA1! (first-continuous) roll on different contract schedules. The runner MUST:

1. Report per-leg roll-seam count (bars dropped by k=8.0 mask) separately for PL2! and PA1!.
2. Report the number of aligned bars where both legs have valid (non-masked) observations.
3. If the roll-seam mismatch produces > 5% additional masking relative to either leg's
   single-leg mask rate, document it as a construction caveat in the output JSON
   (`"roll_seam_mismatch_flag": true`).

This caveat does NOT change the aligned-bar threshold (< 2000 → DEFERRED-DATA) or the VR test.
It is a transparency requirement that must appear in the output.

**Note on PL1!:** PL1! early data (unix 487893600 = 1985-06-17) shows flat O=H=L=C bars with
zero volume — the same early-splice artifact pattern as TVC_PLATINUM. If PL1! is formally
manifested in a future cohort audit and assigned TRUSTED status (after flat-bar trimming), a
future pre-registration may switch to PL1!/PA1! for better roll-schedule alignment. That switch
requires a new pre-registration; it cannot be applied here.

**Updated frozen constants (PL leg only — all other constants unchanged):**

```python
# PL leg: PL2! (second-continuous) — confirmed decision after PL1! manifest check
PL_FILE  = "data/raw/more-mean-reversion-data/NYMEX_DL_PL2!, 1D.csv"
# PA leg: PA1! (first-continuous, manifest TRUSTED, on-disk verified per R1)
PA_FILE  = "data/raw/more-mean-reversion-data/NYMEX_DL_PA1!, 1D.csv"
# Roll-schedule mismatch caveat: ACTIVE (see R4 above)
PL_PA_ROLL_MISMATCH_CAVEAT = True
```

---

### R5. Flat-Bar Gate (New, Both Pairs, Binding)

**MEASUREMENT correction.** The original pre-registration did not include an explicit
flat-bar gate. Given the known flat-bar contamination in early PL2! data (15.6% flat overall,
early-clustered per manifest/audit) and SI2! borderline 5.0%, a binding flat-bar gate is added.

**Definition:** a flat bar is any bar where O = H = L = C (all four OHLC values identical).

**Gate procedure (binding, both pairs, evaluated within the β pre-sample window specifically):**

1. After loading and inner-joining the pair, apply the roll-mask (k=8.0).
2. Identify the β pre-sample window: rows 0 to floor(0.25 × n_aligned_after_mask).
3. Compute flat-bar percentage per leg within that pre-sample window:
   `flat_pct_leg = count(O==H==L==C within presample) / n_presample_bars`
4. **If flat_pct_leg > 5% for either leg:**
   - Trim the early splice era: find the first row where the flat-bar density drops below 5%
     (rolling 252-bar window). Set the series start to that row. Re-apply the full pipeline
     from that new start (re-align, re-mask, re-compute pre-sample at 25% of trimmed series).
   - Report trimmed start date and number of rows dropped.
5. **After trimming, re-check: if flat_pct_leg still > 5% within the trimmed pre-sample:**
   - Declare the pair **MEASUREMENT-INADMISSIBLE** (distinct verdict from DEFERRED-DATA or
     SCREENED-NEGATIVE). Do not run VR. Record in output JSON:
     `"verdict": "MEASUREMENT-INADMISSIBLE", "reason": "flat_bar_pct_exceeds_5pct_post_trim"`.
   - This is a construction halt, not a market verdict.

**Known values to verify and report:**

```
SI2!: flat-bar % overall ≈ borderline 5.0% — runner must compute and report
PL2!: flat-bar % overall ≈ 15.6%, early-clustered — trimming step expected; runner must report
      trimmed start date and residual flat-bar % in the new pre-sample
```

**Revised kill tree position:** flat-bar gate is evaluated after file-readability (criterion 0)
but before f_βupdate (criterion 1). It is criterion 0b in the revised kill tree:

```
0.  FileNotFoundError / unreadable → BUG
0b. Flat-bar > 5% in pre-sample after trimming → MEASUREMENT-INADMISSIBLE (halt, no verdict)
1.  f_βupdate ≥ 0.10 → construction-inadmissible
2.  Aligned bars < 2000 → DEFERRED-DATA
... (remaining criteria unchanged)
```

---

### R6. ADR_003 Verification Assertion (Both Pairs, Binding)

**MEASUREMENT correctness gate.**

The runner must assert that the roll-mask (k=8.0) catches the canonical ADR_003 pseudo-return
events before any VR is computed. These are known reference events:

```
SI2! 2026-01-30: pseudo-return ≈ +37.6% (confirmed by ADR_003 audit)
GC2! canonical large event: ≈ +12.1% (ADR_003 reference)
```

**Assertion procedure (binding):**

1. For SI2! (GC-SI pair leg): locate the bar at or nearest to 2026-01-30. Compute
   |Δprice| / price for that bar. Assert that this value > k=8.0 threshold and therefore the
   bar is masked. If the bar is NOT masked, halt with assertion error: "ADR_003 SI2! 2026-01-30
   37.6% pseudo-return escaped roll-mask — construction failure."
2. For GC2! (GC-SI pair leg): locate the bar corresponding to the +12.1% ADR_003 event.
   Assert it is masked. If not masked, halt with assertion error.
3. Report total masked bars per leg (absolute count and percentage of raw loaded bars):
   ```json
   "roll_mask_stats": {
     "GC2!": {"total_raw_bars": N, "masked_bars": M, "mask_pct": P},
     "SI2!": {"total_raw_bars": N, "masked_bars": M, "mask_pct": P},
     "PL2!": {"total_raw_bars": N, "masked_bars": M, "mask_pct": P},
     "PA1!": {"total_raw_bars": N, "masked_bars": M, "mask_pct": P}
   },
   "adr003_assertions": {
     "SI2!_20260130_caught": true/false,
     "GC2!_large_event_caught": true/false
   }
   ```
4. If either ADR_003 assertion fails → halt with assertion error; do not proceed to VR.

This gate runs before the IS/OOS split and before β estimation. It is a construction integrity
check, not a statistical test.

---

### Summary of Revision 1 Changes

| Item | Change type | Effect on frozen constants |
|---|---|---|
| R1 PA1! on-disk verified | Measurement clarification | None — status confirmed |
| R2 Kill-tree leaf separation | Methodology addition | None — adds criterion 0 |
| R3 GC-SI look-count disclosure | Multiplicity transparency | None — α=0.025 unchanged |
| R4 PL leg confirmed as PL2! | Measurement decision | PL_FILE unchanged (PL2!) |
| R4 Roll-mismatch caveat | Methodology addition | Adds reporting requirement |
| R5 Flat-bar gate | Measurement gate (new) | Adds criterion 0b; trim rule |
| R6 ADR_003 verification | Measurement assertion | Adds pre-VR assertion block |

**All frozen constants from the original block (α=0.025, seeds 20260610/20260611, q=20,
ROLL_MASK_K=8.0, PRESAMPLE_FRAC=0.25, IS_FRAC=0.70, N_SURR_FULL=500, COST_PRIMARY=0.005)
remain unchanged.**

*Revision 1 frozen 2026-06-10. Original pre-registration text above remains authoritative for
all parameters not explicitly superseded here.*
