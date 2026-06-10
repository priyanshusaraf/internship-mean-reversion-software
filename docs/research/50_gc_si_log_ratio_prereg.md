# Doc 50 — GC-SI Log-Ratio IS VR Pre-Registration

**Document class:** Frozen pre-registration. No parameters, construction choices, splits, or
thresholds may be revised after this document is written and before execution.  
**Date frozen:** 2026-06-10  
**Authorization:** Researcher-delegate adjudication. Decisions are not re-litigated here;
they are implemented exactly.  
**Blocking context:** Doc 49 four-lens audit found the level-β construction on GC-SI
CONSTRUCTION-INADMISSIBLE (64.6% of Var(spread) was deterministic linear trend from gold-silver
ratio drift 39.9→83.1 over the IS window; frozen F5 level-β cannot track a 2× ratio shift).
The admissible object for a ratio-cointegrated pair is the log-ratio. Doc 49 contamination
disclosure recorded a diagnostic peek: VR(20)=0.947 (IS slice) and 0.797 (OOS slice) were
observed on the log-ratio during defect diagnosis on the doc-49 IS window. This prereg is NOT
blind to those point estimates; the α accounts for them explicitly.  
**Runner:** `scripts/run_50_gc_si_log_ratio.py` (to be written per this spec)  
**Output:** `data/processed/50_results.json`  
**Results doc:** `docs/research/50_gc_si_log_ratio_results.md`

---

## REVISION 1 (2026-06-10, pre-data) — Delta-Audit Mandates (binding)

Adversarial delta audit: **ADMISSIBLE-WITH-CAVEAT (METHODOLOGY)**. Three mandates, applied before
any data touch; a results doc omitting any of them is void:

1. **PASS leaf is peek-conditioned.** The peeked doc-49 IS slice (2005-2018, n=3,155) is a ~64%
   subset of THIS test's IS window (n≈4,911) — the IS verdict substantially re-measures peeked
   rows, and Bonferroni prices multiplicity, NOT the fact that this test exists only because the
   peek was favorable (run-selection). Therefore an IS pass at p<0.0167 registers as
   **ACTIVE-IS-CONFIRMED-PEEK-CONDITIONED**, never as clean confirmation. The same quarantine the
   prereg applies to the peeked OOS applies to the peeked majority of IS.
2. **Mandatory disjoint sub-window check:** the **1998-07-07 → 2005-07 pre-peek IS segment**
   (the only unpeeked slice in existence) is run as a pre-committed standalone VR(20) +
   surrogate-relative read, reported alongside the primary. It is the only uncontaminated VR look
   available; a PASS whose significance is absent in this disjoint segment carries the
   PEEK-CONDITIONED label with an explicit warning. (Clean confirmation otherwise requires forward
   data post-2026-06 or the economics-stage trade statistic.)
3. **Run-conditioning statement:** the results doc must state that α=0.0167 partially prices
   multiplicity but does NOT neutralize conditional-existence selection; no claim that the peek is
   "fully corrected" is permitted.

NEGATIVE / INCONCLUSIVE outcomes (the modal expectation at power ~0.2-0.35) are fully admissible
as-is — the peek only inflates the PASS leaf, not the fail leaves.

---

## Gate Position (Strategic Dependency Graph)

```
apparatus-trust (§11.8 — LE-GF confirmed doc 46)
  → controlled-β admissibility (β=1 definitional in log space — this doc, ADMISSIBLE CLASS)
    → cohort breadth (THIS DOC: GC-SI log-ratio IS VR screen)
      → per-instrument positive expectancy (separate economics prereg, if IS screen passes)
        → portfolio construction
          → book cost test
            → deployable book
```

**This document gates:** cohort breadth — whether GC-SI log-ratio qualifies as a second sleeve
candidate. It does NOT gate economics, portfolio construction, or book cost test.

**What it does NOT unlock directly:** positive expectancy (requires separate economics prereg:
OOS Sharpe > 0.50, n ≥ 30 trades, cost floor 0.005) and all downstream nodes.

---

## Part I — Hypothesis

The IS log-ratio series X_t = ln(GC2!_close) − ln(SI2!_close) exhibits sub-diffusive variance
ratio VR(20) < 1 in the pre-committed IS window, relative to a random-walk null, with
p_rw(N=500, q=20) < 0.0167.

One-sided (sub-diffusion only). Super-diffusive VR > 1 is not a pass under any circumstance.

---

## Part II — Construction

### Object definition

**Primary object:** X_t = ln(GC2!_close) − ln(SI2!_close)

This is a β=1 DEFINITIONAL construction in log space. No estimation. No presample. No
β updates possible (β is fixed at 1.0 by arithmetic definition of the ratio). The object
tracks the log gold-silver ratio directly.

**β-mode: β=1 definitional (log space). ADMISSIBLE class per programme ontology (doc 21).
f_βupdate = 0.000 by construction — zero identically, not estimated-to-be-small.**

**Rationale for log-ratio (corrective construction, not rescue read):**

The doc-49 four-lens audit proved that a fixed level-β on GC-SI is CONSTRUCTION-INADMISSIBLE
because the gold-silver ratio drifted 39.9→83.1 across the IS window, making 64.6% of
Var(spread) a deterministic linear trend. The cointegration literature's natural object for a
ratio-cointegrated pair is the log-ratio (Escribano and Granger 1998; Wahab et al 1994 use
log specifications in their cointegration tests). β=1 in log space is geometrically equivalent
to saying the pair is ratio-cointegrated — the equilibrium is the log ratio, not a
level-weighted spread. This is the correct construction for the economics, not a post-hoc
adjustment to rescue a kill.

**No deseasonalization.** No documented seasonal production cycle for precious metals spreads.
Deseasonalization not applied.

**No rolling-OLS-β.** INADMISSIBLE per doc 19. Never used.

### Data

- GC leg: `data/raw/more-mean-reversion-data/COMEX_DL_GC2!, 1D.csv` — close prices only
- SI leg: `data/raw/more-mean-reversion-data/COMEX_DL_SI2!, 1D.csv` — close prices only
- Exchange: COMEX. Continuous adjusted (TradingView DL format). Both legs priced in USD/oz.

**Trim start (frozen):** 1998-07-07. This trim was derived in doc 49 execution from the
rolling-252 flat-bar density gate applied to the SI2! early splice era. The trim date is frozen
here; it is not re-derived on each run. The runner must assert the series starts at or after
1998-07-07 (equivalently: assert that no row with timestamp < 1998-07-07 is included after
alignment). Total aligned rows post-trim: ~7,016 (doc-49 observed; runner reports actual).

**Construction steps (binding order):**

1. Load GC2! and SI2! close price series. Assert both files are present and readable
   (FileNotFoundError → BUG, halt, no verdict — same rule as doc 49 R2).
2. Inner-join on timestamp. Drop rows where either leg is NaN, zero, or negative (log is
   undefined for non-positive prices).
3. Apply trim: drop all rows with timestamp < 1998-07-07.
4. Apply ADR_003 increment-jump mask: for each leg independently, compute
   log-returns r_t = ln(P_t / P_{t-1}). Mask bar t if |r_t| exceeds the robust Z-score
   threshold: |r_t − trailing_median(r, 252)| > k × 1.4826 × trailing_MAD(r, 252), with
   k = 8.0 (frozen). Masked bars → NaN in both legs for that date.
   - Assert SI2! 2026-01-29 event is caught (robust Z-score confirmed = 15.45 in doc 49).
   - Assert GC2! 1999-09-27 event is caught (robust Z-score confirmed = 19.26 in doc 49).
   - If either assertion fails: halt with assertion error ("ADR_003 assertion failed —
     construction integrity violated").
5. Construct X_t = ln(GC2!_close_t) − ln(SI2!_close_t) for all non-masked aligned bars.
6. ΔX_t = X_t − X_{t-1} is the increment series for VR computation.

### Flat-bar gate (binding)

Compute flat-bar percentage (O=H=L=C) per leg over the IS window (rows 0 to IS split boundary,
after trim and mask). Report per leg. If either leg exceeds 5% flat bars in the IS window:
declare MEASUREMENT-INADMISSIBLE. Do not run VR. The trim start is already frozen at
1998-07-07; no further trim DOF exists. A >5% finding here is a terminal halt, not a data
decision.

### IS/OOS split (binding)

Chronological 70/30 split of the trimmed aligned series by **row count** (not calendar date).

- IS: first 70% of rows after trim and mask alignment
- OOS: last 30% of rows

With ~7,016 total rows: IS ≈ rows 0–4,911 (boundary at row 4,910); OOS ≈ rows 4,911–7,015.
Approximate IS dates (orientation, NOT binding): 1998-07-07 → ~2018-01.
Approximate OOS dates (orientation, NOT binding): ~2018-01 → 2026-06-03.

**The RULE governs; row-count split boundary is authoritative. Date approximations are for
reader orientation only.**

**No presample for β estimation.** β=1 definitional requires no estimation window. The full IS
period is available for VR testing (no 25% pre-sample consumed). This is a structural improvement
over doc-49 F5 construction: n_IS_valid ≈ 4,911 rows vs. doc-49's active IS of ~3,155 rows.

---

## Part III — β-Update-Noise Check

β = 1.000 (fixed, definitional). f_βupdate = Var((β_{t-1} − β_{t-2}) × B_{t-1}) / Var(ΔX) = 0.000
identically (numerator is zero because β never changes). Gate threshold: f_βupdate ≥ 0.10 →
inadmissible. **Trivially satisfied: 0.000 < 0.10.** Stated for protocol completeness and
audit traceability.

---

## Part IV — Alpha Accounting (Load-Bearing)

**α = 0.05 / 3 ≈ 0.0167 (Bonferroni, 3-look family).**

PASS threshold: p_rw(N=500, q=20) < 0.0167.
INCONCLUSIVE-LEANING-FAIL zone: p_rw ∈ [0.0167, 0.05).

### Look family (all three counted; no look is voided)

**L1 — Doc 49 level-β screen (GC-SI, same pair, same question class).**

The doc-49 pre-registration tested IS VR sub-diffusion on GC-SI using F5 presample-OLS β
(a different construction on the same pair, targeting the same research question). Result:
VR(20) = 1.0106, p_rw = 0.6418, SPEED_GATE_KILL. That result was subsequently found to be
CONSTRUCTION-INADMISSIBLE (not a market verdict). However, it was a realized look at a
statistic in the same pair/question family and is conservatively counted as L1.

**L2 — 2026-06-10 diagnostic peek (DIRECT LOOK at this test's statistic family).**

During doc-49 defect diagnosis, the statistical lens computed the log-ratio VR on the doc-49 IS
window: VR(20) = 0.947 and on the doc-49 OOS window: VR(20) = 0.797. These are favorable point
estimates of sub-diffusion on the exact same object this pre-registration will test. This is a
direct, realized look at this test's statistic family. Proceeding conditional on these favorable
values is selection; the stricter α prices it. This look is MANDATORY to count — it cannot be
voided or reclassified as "informational" because its content (sub-diffusive VR) is directionally
favorable to the hypothesis being tested.

**L3 — This test (doc 50).**

**Why the doc-18/19 rolling-OLS looks are VOID and not counted:**

Doc 18/19 used rolling-OLS-β-on-levels, proven CONSTRUCTION-INVALID by doc 19. Rolling-OLS-β
manufactures VR artifacts mechanically; the numerical results carry zero evidential content for
or against the actual market behavior of GC-SI under any admissible construction. Those prior
results do not constitute looks at the log-ratio or any admissible construction. VOID per doc-49
R3 precedent. Not counted in the 3-look family.

**Binding rule:** PASS = p_rw(N=500, q=20) < 0.0167. A result with p ∈ [0.0167, 0.05) is
INCONCLUSIVE-LEANING-FAIL — not a pass, but also not a clean negative at α=0.05 family level.
Report it as such; do not round down to FAIL or up to PASS.

---

## Part V — Primary Statistic

**VR(q) — Lo-MacKinlay (1988) variance ratio** at q=20, computed on ΔX_t (first differences
of X_t = ln GC2! − ln SI2! in the IS window), surrogate-relative against four null families.

Formula: VR(q) = Var(X_t − X_{t-q}) / (q · Var(X_t − X_{t-1}))

Under RW: VR(q) = 1. Sub-diffusion (mean reversion): VR(q) < 1.

Primary gate: VR(20) against RW surrogate distribution (N=500 paths), one-sided (lower tail).
p_rw = fraction of surrogate VR(20) values ≤ observed VR(20).

Full q grid {2, 5, 10, 20, 40} computed and reported. No argmax selection. q=20 is the
pre-committed primary; other lags are informational and do NOT change the verdict.

---

## Part VI — Null Families

All four nulls run on the IS ΔX_t series. Surrogates conditioned to match the real IS series.

### RW (PRIMARY — gating)

Surrogate: bootstrap (shuffle) ΔX_t. Preserves marginal increment distribution; destroys
autocorrelation. p_rw is the sole primary gate.

### GARCH(1,1) (supporting — mandatory)

Fit GARCH(1,1) to ΔX_t IS period. Generate N=500 paths of length n_IS. Compute VR(20) per path.
p_garch = fraction of surrogate VR(20) ≤ observed. Supporting, not gating. If p_garch < 0.05
while p_rw ≥ α: no contradiction (GARCH paths are mean-free but have clustering; a sub-diffusive
IS result that fails GARCH is anomalous and must be reported). If p_garch contradicts the RW
result (p_rw < 0.0167 but p_garch ≥ 0.05): this does NOT kill the result; report it as a caveat
per doc 46/48 convention. A GARCH contradiction at p<0.05 is a flag, not a second gate.

### MA(1)-noise (supporting — mandatory for spread tests)

Fit MA(1) to ΔX_t IS period. Simulate N=500 MA(1) paths of length n_IS. Compute VR(20) per path.
p_ma1 = fraction ≤ observed. MA(1) noise can appear sub-diffusive at short lags; mandatory per
programme doctrine for all spread tests. Same contradiction convention as GARCH above.

### OU (non-gating reference)

Fit OU process (κ, μ, σ) to X_t IS period. Simulate N=500 OU paths of length n_IS. Compute
VR(20) per path. p_ou = fraction ≤ observed. Does NOT gate verdict. Reference: if p_ou > p_rw,
the real series reverts faster than a matched OU process — an upgrade signal. If p_ou < p_rw,
the OU surrogate already spans the observed sub-diffusion.

---

## Part VII — Windows and Multiplicity

All five q values in the grid {2, 5, 10, 20, 40} are tested and reported in full. No argmax.
The full grid result table must appear in the output (VR(q), p_rw per q). q=20 is the sole
pre-committed primary gate. Selecting any other q ex post to claim a pass is forbidden.

One θ (entry threshold): not applicable at this stage — the IS VR test does not use trading
rules. The entry-rule parameter grid is deferred to the separate economics pre-registration.

---

## Part VIII — N and Seed

**Speed gate:** N=200 surrogates. Kill criterion: p_rw(N=200) > 0.20 → kill immediately
(INCONCLUSIVE-UNDERPOWERED or SCREENED-NEGATIVE per power check; see §Kill Criteria).

**Full test:** N=500 surrogates. Primary gate threshold α=0.0167.

**Seed:** 20260612 (frozen; used for all surrogate draws in this pre-registration — both speed
gate and full test, all null families).

---

## Part IX — Power Simulation (Mandatory)

Power simulation is MANDATORY per doc 48 four-lens review lesson. Pattern: AR(1) increments
cumulated (corrected doc-48 pattern — NOT level AR(1)).

```python
# AR(1) increments cumulated — NOT levels
dr[0] = eps[0]
for t in range(1, n_is):
    dr[t] = phi * dr[t-1] + eps[t]
path = np.concatenate(([0.0], np.cumsum(dr)))
```

Calibration: binary search φ until vr_ar1_theoretical(φ, q=20) ≈ target VR. Verify realized VR
within ±0.01 of target.

Power reported at:
- **Reference VR = 0.90**: standard reference across the programme, for cross-instrument comparison
- **Observed IS VR**: the primary power figure for this run

**α for power simulation:** 0.0167 (matching the stricter pre-committed α, not 0.025).

**n for power simulation:** n_IS_valid (actual valid IS bars after mask, approximately 4,911).

**UNDERPOWERED BRANCH IS UNIVERSAL (doc-49 lesson binding here):**

If power < 0.30 at reference VR = 0.90: the result is INCONCLUSIVE-UNDERPOWERED regardless of
whether it is the speed gate or full test that triggered. "VR > 1 implies nothing to detect" is
NOT a valid override — a test with power < 0.30 cannot distinguish trending from
moderately-mean-reverting. The underpowered branch applies to ANY failure, including speed gate
failures.

**Expected power ex ante (honest disclosure):** With n_IS ≈ 4,911 bars, α = 0.0167, and
reference VR = 0.90, the corrected AR(1)-increments power simulation is expected to yield
approximately 0.20–0.35 (the doc-49 apparatus yielded 0.176 at n=3,155 bars and α=0.025;
the larger n here partially compensates but the stricter α penalizes). An INCONCLUSIVE outcome
is a legitimate terminal leaf, not a runner failure. The runner must report this estimate
ex ante in the results doc and state it was known before execution.

---

## Part X — OOS Secondary Characterisation

**OOS is held out and reported secondary. The OOS window was peeked during doc-49 defect
diagnosis (VR(20) = 0.797 observed). OOS is therefore NON-PROMOTABLE in this pre-registration
as a confirmation statistic for GC-SI IS VR. An IS PASS here does not count as confirmed by OOS
within this doc; OOS confirmation for GC-SI can only come from the subsequent economics-stage
prereg on trade rules, a different statistic, or forward data.**

OOS is reported for reader orientation after IS verdict is finalized:
- OOS VR(20), p_rw (N=500, informational — not gating)
- OOS sign-reversal kill flag: if OOS VR(20) > 1 AND p_rw < 0.05 (super-diffusive, one-sided
  upper tail), record as OOS-SIGN-REVERSAL. This flag is a kill signal for the IS result even if
  IS passed. It does not promote OOS to a confirmation signal; it is an asymmetric veto on a
  strong adverse OOS reading.

OOS n_trades and economics are NOT reported here. Trade-rule economics are deferred to the
separate economics pre-registration.

---

## Part XI — Kill Criteria (ordered, binding)

Each criterion evaluated in order. First triggered criterion terminates the test.

**0. File unreadable / FileNotFoundError** → BUG (halt immediately, no verdict, no registry
entry). Surface as: "BUG — infrastructure failure: <filename>".

**0b. Flat-bar gate** → MEASUREMENT-INADMISSIBLE (halt, no VR, no market verdict). If either
leg exceeds 5% flat bars (O=H=L=C) in the IS window. The 1998-07-07 trim is already frozen;
no further trim DOF. Terminal halt.

**0c. ADR_003 assertion failure** → halt with assertion error. Do not proceed to VR.

**1. f_βupdate ≥ 0.10** → construction-inadmissible. Will not trigger (0.000 by construction;
stated for protocol completeness).

**2. Speed gate: p_rw(N=200) > 0.20** → evaluate power at reference VR=0.90 (AR(1)-increments
cumulated, N=500 paths, α=0.0167):
- If power < 0.30: INCONCLUSIVE-UNDERPOWERED. Not a kill. Surface data-depth report. See
  verdict tree leaf below.
- If power ≥ 0.30: SCREENED-NEGATIVE (apparatus was powered; absence is informative).

**3. Jackknife drop > 300%** → CONCENTRATION-UNSTABLE. Kill. Divide IS into 5 equal contiguous
blocks; drop each in turn; compute VR(20) on remaining 4. If max deviation from full-IS
VR relative to (1 − VR_full) exceeds 300%: kill.

**4. Full test: p_rw(N=500) ≥ 0.0167** → evaluate:
- p_rw < 0.0167: check power → if power ≥ 0.30, PASS. If power < 0.30, INCONCLUSIVE-LEANING-
  PASS (power-qualified; surface to researcher before advancing to economics prereg).
- p_rw ∈ [0.0167, 0.05): INCONCLUSIVE-LEANING-FAIL. Not a pass; not a clean negative.
- p_rw ≥ 0.05: SCREENED-NEGATIVE (if power ≥ 0.30); INCONCLUSIVE-UNDERPOWERED (if power < 0.30).

**5. OOS sign-reversal kill flag** (evaluated after IS verdict, before registry write): if
OOS VR(20) > 1 AND p_rw_oos < 0.05 → OOS-SIGN-REVERSAL. Overrides IS PASS to CANDIDATE-OOS-
SIGNAL (surface to researcher; does not advance to economics prereg without researcher decision).

---

## Part XII — Verdict Tree (all leaves)

```
FileNotFoundError → BUG (halt; no verdict; no registry)

MEASUREMENT-INADMISSIBLE (flat-bar > 5% post-trim) → halt; no market verdict;
  GC-SI log-ratio pair status: CONSTRUCTION-INADMISSIBLE (data source, not pair)

ADR_003 assertion failure → halt; BUG

Speed gate kill (p_rw_200 > 0.20):
  power < 0.30 at VR=0.90 → INCONCLUSIVE-UNDERPOWERED
    → data-depth report required: n needed for power ≥ 0.30
    → named options: (a) acquire longer GC2!/SI2! history (pre-1998 data);
      (b) accept single-sleeve LE-GF status; (c) GC-SI economics deferred
    → registry: GC-SI log-ratio → INCONCLUSIVE-UNDERPOWERED (data constraint)
  power ≥ 0.30 at VR=0.90 → SCREENED-NEGATIVE
    → registry: GC-SI log-ratio → SCREENED-NEGATIVE
    → cohort remains COHORT-UNRESOLVED (no second sleeve confirmed)
    → surface to researcher: 46 TRUSTED legs yield no IS VR confirmation for second sleeve

Full test (N=500, q=20):
  p_rw < 0.0167:
    VR(20) ≥ 1 → cannot happen at this p_rw (one-sided lower tail); flag as runner error
    VR(20) < 1 (sub-diffusive):
      OOS sign-reversal flag (VR_oos > 1, p_oos < 0.05) →
        CANDIDATE-OOS-SIGNAL (pass held pending researcher decision)
      No OOS sign-reversal:
        power ≥ 0.30 → PASS
          → GC-SI log-ratio = second-sleeve CANDIDATE
          → next = economics prereg (OOS Sharpe > 0.50, n ≥ 30, cost 0.005)
          → registry: GC-SI log-ratio → ACTIVE-IS-CONFIRMED (candidate)
          → combination gate remains blocked until economics prereg passes
        power < 0.30 → INCONCLUSIVE-LEANING-PASS (power-qualified)
          → surface to researcher before advancing

  p_rw ∈ [0.0167, 0.05) → INCONCLUSIVE-LEANING-FAIL
    → not a pass; not a clean negative
    → registry: GC-SI log-ratio → INCONCLUSIVE (alpha boundary)
    → surface to researcher (stricter α due to peek; bare-α pass would be p<0.05)

  p_rw ≥ 0.05:
    power < 0.30 → INCONCLUSIVE-UNDERPOWERED
      → same data-depth options as speed-gate branch
    power ≥ 0.30 → SCREENED-NEGATIVE
      → honest negative for log-ratio object at powered n
      → cohort then genuinely thin → surface to researcher
      → registry: GC-SI log-ratio → SCREENED-NEGATIVE
```

---

## Part XIII — Survive Criteria (Positive Result)

For the test to constitute a positive result (IS VR confirmation, PASS leaf):

1. Files readable, no BUG halt
2. Flat-bar < 5% per leg in IS window
3. ADR_003 assertions pass
4. f_βupdate = 0.000 (trivially satisfied)
5. Speed gate: p_rw(N=200) ≤ 0.20
6. Full test: p_rw(N=500, q=20) < 0.0167
7. VR(20) < 1.0 (sub-diffusion direction)
8. Jackknife drop ≤ 300%
9. No OOS sign-reversal (VR_oos ≤ 1 OR p_oos ≥ 0.05)
10. Power ≥ 0.30 at reference VR=0.90 (otherwise: INCONCLUSIVE-LEANING-PASS, not a full PASS)

Meeting all ten constitutes a positive result. It does NOT constitute a deployable book.
It opens the economics gate: a separate pre-registration for OOS Sharpe > 0.50, n ≥ 30 trades,
cost floor 0.005, using the OOS window that is NON-PROMOTABLE in this doc.

---

## Part XIV — Cost Assumption

Cost is NOT a gate for this IS VR screen. Stated for institutional completeness and to connect
to the downstream economics prereg.

- Primary: 0.005 (cost per trade as fraction of spread price)
- Also report at: 0.003 and 0.008

Cost grid application is deferred to the economics pre-registration. Any IS economics
(hypothetical mean_net, Sharpe) reported informally in the results doc must use this grid
and must be clearly labeled INFORMATIONAL — NOT a gate for this prereg.

---

## Part XV — Temporal Firewall Statement

The IS period is fully pre-committed before any data is touched. The 70/30 row-count split rule
governs; no look at OOS during IS VR testing. β = 1 definitional; no presample β estimation
window; entire IS is available for VR.

The OOS window was peeked during doc-49 defect diagnosis (VR(20) = 0.797). This does not
require exclusion of the OOS period — it requires honest disclosure (done above in Part II and
Part IV) and α adjustment (done: α = 0.0167 instead of 0.025). The IS VR test remains
temporally clean. OOS is accessed only after the IS verdict is written and recorded.

Deseasonalization is NOT applied. This removes the causal-seasonal-window lookahead risk
documented in doc 38/38a back-adjustment diagnostic.

---

## Part XVI — Non-Goals

This pre-registration does NOT:

- Test OOS economics, Sharpe, or trade-level expectancy (gated behind separate economics prereg)
- Re-examine RB-CL (PERMANENTLY ARCHIVED, doc 48; no further look)
- Reopen LE-GF OOS weakness (stands; separate mechanism prereg would be required)
- Re-examine NG selectivity (KILLED — p_ou=1.000 everywhere, docs 23/31; EIA KILLED doc 34)
- Test deseasonalization, regime conditioning, or selective entry rules
- Make portfolio-construction decisions
- Produce a deployable book or book-level cost test
- Use rolling-OLS-β (INADMISSIBLE per doc 19)
- Produce UI output or visualization infrastructure
- Re-test the level-β F5 GC-SI construction (CONSTRUCTION-INADMISSIBLE per doc 49 four-lens)
- Test PL-PA (MEASUREMENT-INADMISSIBLE per doc 49; PL2! pervasive flat bars 1998–2007; deferred)
- Override the OOS peek contamination by reclassifying L2 as "informational"
- Claim §11.8 apparatus validation from this run (LE-GF remains the sole standing §11.8 anchor)

---

## Part XVII — Next Gate

**If PASS (IS VR confirmed, p_rw < 0.0167, power ≥ 0.30):**

Write a separate economics pre-registration for GC-SI log-ratio covering:
- OOS economics: mean_net > 0 AND Sharpe > 0.50 at COST_PRIMARY = 0.005
- n_OOS_trades ≥ 30 for binding verdict (< 30 = INCONCLUSIVE, not a pass)
- Entry rule: θ (z-score threshold) and holding period pre-committed before any OOS touch
- OOS window: same 30% held-out rows from this doc — but now under trade-rule
  statistics, not VR, so the contamination from the VR(20) peek does not carry over
- Independence check (ρ) between GC-SI OOS residuals and LE-GF OOS residuals

If economics prereg passes: combination pre-registration (portfolio/book row) can be reopened
with two qualified sleeves (LE-GF + GC-SI log-ratio).

**If INCONCLUSIVE-UNDERPOWERED (any power < 0.30 branch):**

Surface data-depth report to researcher. Named options:
(a) Acquire pre-1998 GC2!/SI2! history to extend n_IS beyond ~4,900 bars.
(b) Accept single-sleeve LE-GF operation as the primary path and focus effort on LE-GF
    economics and book-level cost testing.
(c) PL-PA remains DEFERRED-MEASUREMENT-INADMISSIBLE (PL2! data); a different platinum
    data source would require a new flat-bar assessment and new pre-registration.

**If SCREENED-NEGATIVE (power ≥ 0.30, clean negative):**

Cohort is genuinely thin. Surface to researcher with same options (a)/(b)/(c) above plus:
(d) Equity pairs or FX pairs as a different asset class (different economics, different
    pre-registration required).

---

## Part XVIII — Summary of Frozen Choices

| Decision | Choice | Justification |
|---|---|---|
| Object | X_t = ln(GC2!) − ln(SI2!) | Doc-49 four-lens: level-β INADMISSIBLE (64.6% trend Var); log-ratio = admissible cointegration literature object |
| β-mode | β=1 definitional (log space) | ADMISSIBLE class; no estimation; f_βupdate=0 identically |
| Trim start | 1998-07-07 (frozen) | SI2! flat-bar gate derived in doc 49 execution; re-derived start date would be a new look |
| IS/OOS split | 70/30 row-count chronological | Programme standard (doc 49); row-count rule governs over date approximations |
| Presample for β | NONE (β=1 definitional) | No estimation needed; full IS available for VR |
| Primary statistic | IS VR(20), RW null, N=500 | Exact programme apparatus (doc 46/48/49) |
| q grid | {2, 5, 10, 20, 40}; q=20 primary | Full grid, no argmax; q=20 pre-registered |
| α | 0.0167 (0.05 / 3, Bonferroni, 3 looks) | L1=doc-49 level-β screen; L2=2026-06-10 diagnostic peek (VR=0.947/0.797); L3=this test |
| α zone | p<0.0167 = PASS; [0.0167, 0.05) = INCONCLUSIVE-LEANING-FAIL | Peek contamination makes the zone non-trivial; must be disclosed |
| Speed gate | p_rw(N=200) > 0.20 → evaluate power | Programme standard + underpowered-branch universal (doc-49 lesson) |
| Jackknife | 5-block, max-drop ≤ 300% | Programme standard |
| Power simulation | Increments-AR(1) cumulated; corrected doc-48 pattern; α=0.0167, n=n_IS_valid | Mandatory; stricter α than doc-49 (matches gate) |
| Reference VR for power | 0.90 | Programme standard cross-instrument reference |
| Underpowered branch | Universal: any failure with power<0.30 → INCONCLUSIVE-UNDERPOWERED | Doc-49 lesson: VR>1 does not override power check |
| OOS status | NON-PROMOTABLE (peeked — VR seen during doc-49 diagnosis) | Honest contamination disclosure; OOS confirmation deferred to economics prereg |
| OOS sign-reversal | VR_oos > 1 AND p_oos < 0.05 → kill flag | Asymmetric veto on strong adverse OOS |
| Seed | 20260612 | Frozen; all surrogates this doc |
| Cost grid | 0.003 / 0.005 / 0.008 (primary 0.005) | Programme standard; informational at IS screen stage |
| Deseasonalization | None | No documented precious metals seasonal; back-adj contamination risk |
| FileNotFoundError | BUG (halt; no verdict) | Doc-49 R2 precedent |
| Flat-bar gate | > 5% IS window → MEASUREMENT-INADMISSIBLE | Doc-49 R5 precedent; no trim DOF left |
| ADR_003 assertion | SI2! 2026-01-29; GC2! 1999-09-27 | Doc-49 R6 confirmed events; assertion before VR |
| Rolling-OLS-β | INADMISSIBLE — not used | Doc 19 |
| §11.8 status | LE-GF remains sole anchor; this run does not exercise §11.8 | Doc-49 four-lens correction: §11.8 requires admissible construction given to apparatus |

---

## Part XIX — Frozen Constants Block

```python
# ============================================================
# DOC 50 FROZEN CONSTANTS — DO NOT MODIFY AFTER PRE-REGISTRATION
# ============================================================

# --- Instrument: GC-SI log-ratio ---
GC_FILE  = "data/raw/more-mean-reversion-data/COMEX_DL_GC2!, 1D.csv"
SI_FILE  = "data/raw/more-mean-reversion-data/COMEX_DL_SI2!, 1D.csv"

# --- Object ---
# X_t = ln(GC2!_close_t) - ln(SI2!_close_t)
# beta = 1.0 DEFINITIONAL (log space); no estimation; no presample for beta

# --- Trim ---
TRIM_START_DATE    = "1998-07-07"   # frozen; derived in doc-49 execution from SI2! flat-bar gate

# --- Construction ---
ROLL_MASK_K        = 8.0            # robust Z-score threshold for increment-jump masking
# Robust Z-score formula: |r_t - trailing_median(r, 252)| > 8.0 * 1.4826 * trailing_MAD(r, 252)
BETA               = 1.0            # definitional; never updated
F_BETA_UPDATE      = 0.000          # identically zero; stated for protocol
F_BETA_UPDATE_HALT = 0.10           # gate; trivially satisfied

# --- ADR_003 assertions (must pass before VR proceeds) ---
ADR003_SI_DATE     = "2026-01-29"   # ±1 day tolerance for TZ/roll offset
ADR003_SI_ROBUST_Z = 15.45          # confirmed doc-49; assert caught
ADR003_GC_DATE     = "1999-09-27"   # canonical GC2! event
ADR003_GC_ROBUST_Z = 19.26          # confirmed doc-49; assert caught

# --- IS/OOS split ---
IS_FRAC            = 0.70           # first 70% of trimmed aligned rows → IS
# OOS_FRAC = 0.30 implied
# No presample fraction — beta=1 definitional, full IS available for VR

# --- Primary statistic ---
VR_Q_PRIMARY       = 20             # Lo-MacKinlay lag; primary gate
VR_Q_GRID          = [2, 5, 10, 20, 40]   # full grid; informational except q=20
NULL_FAMILIES      = ["rw", "garch", "ma1", "ou"]
# rw   = PRIMARY GATE (gating)
# garch = GARCH(1,1) surrogate (supporting; mandatory)
# ma1   = MA(1)-noise surrogate (supporting; mandatory)
# ou    = OU matched surrogate (non-gating reference)

# --- Surrogate counts ---
N_SURR_SPEED       = 200            # speed gate
N_SURR_FULL        = 500            # full test

# --- Seed ---
SEED               = 20260612       # frozen; all surrogate draws in this prereg

# --- Alpha (3-look Bonferroni) ---
ALPHA              = 0.05 / 3       # = 0.016667
ALPHA_INCONCLUSIVE_ZONE = (0.016667, 0.05)   # [alpha, 0.05) = INCONCLUSIVE-LEANING-FAIL
PASS_P_RW_SPEED    = 0.20           # speed gate kill threshold
PASS_P_RW_FULL     = 0.016667       # full test pass threshold

# --- Jackknife ---
JACKKNIFE_N_BLOCKS = 5
JACKKNIFE_DROP_MAX = 3.00           # 300% of VR deviation from 1.0; kill if exceeded

# --- Power simulation ---
POWER_REF_VR       = 0.90           # reference VR for cross-instrument power comparison
POWER_SIM_N_PATHS  = 500
POWER_ALPHA        = 0.016667       # matches gate alpha (stricter than doc-49's 0.025)
POWER_UNDERPOWERED_THRESHOLD = 0.30 # universal branch trigger

# --- Cost grid (informational at IS screen stage) ---
COST_PRIMARY       = 0.005
COST_GRID          = [0.003, 0.005, 0.008]

# --- Flat-bar gate ---
FLAT_BAR_THRESHOLD = 0.05           # 5% of IS window bars; either leg triggers MEASUREMENT-INADMISSIBLE

# --- Results ---
RESULTS_JSON       = "data/processed/50_results.json"
RESULTS_DOC        = "docs/research/50_gc_si_log_ratio_results.md"

# ============================================================
# END FROZEN CONSTANTS
# ============================================================
```

---

*Pre-registration frozen 2026-06-10. No parameter, construction choice, split, threshold, seed,
or alpha may be revised after this date and before execution.*
