# State T — Observational Existence Programme (v1): Pre-Registration & Build Record

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **PRE-REGISTRATION (written before any real-data run).** This section fixes the empirical
claim, the comparison directions, and the falsification rules *before* results exist, so that any
later finding is confirmation/falsification — not post-hoc morphology storytelling.
**Date:** 2026-06-02.
**Mode:** Controlled Implementation Mode (authorized this session). Freeze-adjacent.

> **▸ CONTEXT (placeholder framing — frozen).** Real reads are on ADANIENT (placeholder, trend-heavy)
> and on-disk synthetics scale-matched to it. Deployment domain (spreads · pairs · cross-asset RV) is
> expected materially more mean-reverting. No market truth is inferred. See `CONTINUATION_STATE.md` §0.

---

## 0. What this is NOT

Not State T. Not a detector. Not transition timing. Not hazard logic. Not per-bar State-T
observability. Not "candidate-T" logic. **No** T-score, T-probability, candidate-transition score,
transition confidence, ignition/imminent/precursor semantics, or episode labels. Nothing here may
imply "State T is happening now." Adjudicated this session by research-planner + alignment-advisor;
verdict and guardrails are binding (see doc 04 §1.4.3/§2.6.4 for the frozen detection boundary).

## 1. The empirical claim under test

> In the **causal** μ\* Kalman innovation stream (`epsilon_kalman`, doc 06; one-step innovation,
> causal by construction), is the **distribution** of residual morphology inside high-deviation
> windows **statistically distinguishable from matched synthetic nulls** — measured as a
> corpus-level, time-symmetric verdict, never a per-bar quantity?

Existence = a statement about the *distribution*, not about any bar. The gating test for every
diagnostic (alignment-advisor): **does the output's meaning depend on *when* you read it?** If yes →
timing/hazard → frozen. If no → distributional existence → legal.

## 2. Binding architecture — two arms

**ARM 1 — CAUSAL (the ONLY verdict-bearing arm).**
- Window selection must be evaluable using data ≤ t. **No forward outcome selection, no reversion
  anchoring, no hindsight episodes.**
- Anchor rule (frozen for v1): **multi-θ symmetric partition** on the causal z-score
  (`analytics_mrscore.causal_zscore`): for θ ∈ **{1.0, 1.5, 2.0}**, partition all bars into
  high-|z| (`|z| ≥ θ`) vs the rest. This is a *symmetric descriptive partition of all history*,
  **not** a trigger that "flags an imminent reversion."
- For each anchor bar t, take the causal pre-window `[t−W+1, t]` of `epsilon_kalman` (and the close
  path), compute descriptors, and compare the high-|z| descriptor distribution to the matched-null
  distribution under *identical* extraction.

**ARM 2 — FULL-INFORMATION (understanding only; built later, quarantined).**
- Reversion-anchored (hindsight) windows allowed — explicitly labeled "understanding only — not
  evidence." Not verdict-bearing, not causal evidence, may not back-propagate into Arm 1.

## 3. Descriptors (minimal — 3, no soup)

Computed on each causal pre-window:
- **D1 innovation variance** — `std(epsilon_kalman)` over the window. (residual stabilization axis)
- **D2 continuation persistence** — innovation `ACF(1)` over the window. (continuation axis)
- **D3 directional efficiency** — `analytics_substrate.directional_efficiency(close path)` ∈ [0,1].
  (chop↔continuation of price)

No score. No label. No weighting. Raw descriptor distributions only.

## 4. PRE-REGISTERED comparison directions (written before seeing real data)

These are the *hypothesised* directions IF a real State-T-like phenomenon exists. **We do not assert
they are true.** They are fixed now so the result cannot be re-storied afterward.

Relative to the matched **null** ensemble, high-|z| windows — IF T exists — are expected to show:

| Descriptor | Pre-registered direction (high-|z| vs null) | Rationale |
|---|---|---|
| **D1 innovation variance** | **↓ lower** | residual stabilization before reversion |
| **D2 continuation persistence (ACF1)** | **↓ lower / more negative** | continuation failing, deviation losing momentum |
| **D3 directional efficiency** | **↓ lower** | price chops/hesitates rather than continuing |

Effect-size metric (descriptive, not a p-hacked verdict): standardized mean difference
(Cohen's-d-style) of each descriptor, high-|z| vs null, reported per θ. Direction agreement with the
table above is the existence signal; magnitude is secondary.

## 5. Falsification framework (how we avoid hallucinating T on noise)

Run nulls **first**, real data **second**. Nulls (via `synthetic.py`, run through the same
`compute_kalman_mu_star` + extraction):
- **RW** (`random_walk`) — easy baseline. Any contrast here that mirrors "real" means the morphology
  is just what large RW excursions look like → nothing to explain.
- **OU** (`ou`) — **the hard / sympathetic null.** OU mean-reverts *by construction* with no State T.
  **If OU reproduces the same directional shifts as real, the thesis is FALSIFIED-by-construction:**
  the pattern is generic mean-reversion mechanics, not a distinct State-T object.
- **Trend** (`trend`) — supplementary; reversions here are forced trend-fatigue.

**Falsification outcomes (stated in advance):**
1. High-|z| windows indistinguishable from nulls on all 3 descriptors → **no existence signal** (thesis weakened).
2. OU null reproduces the pre-registered shifts → **falsified by construction** (sympathetic-null match).
3. Real effects point **opposite** to the pre-registration → thesis weakened; **no post-hoc re-story.**

Circularity guard: label synthetic OU with the *identical* θ-partition; if OU shows the same pattern,
the "signal" is mechanically induced by the partition, not evidence of a state.

## 6. Hard guardrails (hard-coded)

Observational (output = distributional verdict + effect sizes, never a per-bar series; no persisted
"T" column; null-comparison is mandatory framing) · Causal (Arm-1 window selection uses only data
≤ anchor; bit-identical future-injection acceptance test) · Terminal (read-only on the residual
stream; zero imports back into μ\*/Kalman/MRScore/Substrate/signals/gates) · No latent-state model
(no HMM/ML/DL) · Banned vocab in code/docs/UI (T-score, T-probability, candidate, hazard, ignition,
imminent, precursor, transition timing, per-bar T, episode label). Permitted: distinguishable /
not-distinguishable from null · effect size · descriptive · in-expectation · existence verdict.

---

## 7. Build log & results

### Phase 2 — minimal causal arm (BUILT, GREEN)
`backend/app/services/analytics_state_t.py` + `tests/test_state_t_existence.py` (14 tests). Reuses
`compute_kalman_mu_star`, `causal_zscore`, `directional_efficiency`. The freeze-critical test
(perturb bars >t by +50 → descriptors at anchors ≤t **bit-identical**) passes. **No thesis movement**
— mechanism only; no data interrogated.

### Phase 3 — synthetic falsification battery (RUN, doc-11 §5)
Reproducible probe `backend/scripts/state_t_existence_probe.py`; standing guards
`tests/test_state_t_falsification.py` (4 tests, all pass). Pooled effect sizes (Cohen's-d, real high-|z|
vs pooled null high-|z|; N=800; 6 real seeds, 12 null seeds):

**(1) NO-FALSE-POSITIVE — PASS.** OU-real vs OU-null and RW-real vs RW-null: all |d| ≤ 0.15 across
θ∈{1.0,1.5,2.0} and all 3 descriptors. *The machinery does not manufacture State-T morphology from
ordinary mean reversion or random walk.* (Minor consistent acf1 ≈ −0.07…−0.15 — finite-sample, within ~0.)

**(2) SENSITIVITY (positive control) — PASS, after a rejected first attempt (recorded, no revisionism):**
- **REJECTED control v1** (two-regime OU: compressed σ=0.25/λ=−0.45 high-|dev| zone + near-RW quiet
  zone σ=1.0/λ=−0.04): produced **+0.20 innov_var, +0.04 acf1, +0.20 dir_eff** — *opposite* sign to
  pre-registration, stable across θ AND across forward/backward window placement. Diagnosis: its
  high-|z| windows are dominated by the trendy quiet APPROACH it must traverse to reach a large
  deviation, so they read *more* trending/variable than OU. **Methodology finding (METHODOLOGY class):**
  this was a bad *control*, not a method defect — the descriptors clearly separated it from OU
  (non-zero, consistent), i.e. they are demonstrably **not blind**; they were just measuring the
  wrong feature of a mis-built control. Forward windows did not change this (timing was not the cause).
- **ACCEPTED control v2** (clean stabilize-then-revert: σ(dev)=1/(1+0.30·|dev|) monotone compression,
  always-strong λ=−0.40): shows the pre-registered signature **decisively** — innov_var d ≈ **−1.90…−1.97**,
  acf1 d ≈ **−2.06…−2.50**, dir_eff d ≈ **−0.89…−0.95**, all negative, all θ. The construction is the
  literal embodiment of the hypothesis (principled, not reverse-engineered to a number).

**Phase-3 verdict:** the existence machinery is **validated** — silent on noise/ordinary MR
(no false positive), and loud + correctly-directed on a genuine stabilize-then-revert object
(sensitivity). A null result on real data would now be *interpretable* ("no T-like morphology"),
not merely "blind descriptors." **Confidence in the METHOD: MEDIUM-HIGH. Confidence about whether
State T EXISTS in real data: UNTESTED** — no real series has been interrogated yet (Phase 4+).

**Surviving uncertainty / non-conclusions:** (a) the pre-registered signature is one plausible
T-morphology; absence of *this* signature ≠ absence of all T-like phenomena. (b) The clean control is
an idealization; real T (if it exists) will be far noisier and may sit near the no-false-positive
floor. (c) Nothing here is evidence about ADANIENT or any market. **Next high-information question:**
does real causal residual morphology (ARM 1) sit at the OU-null floor or shift toward the
positive-control signature? — Phase 4/5.

### Phase 4 — real cohort (PRE-RUN expectations, committed before results)
**Frame (binding):** this is *"what does a real instrument look like under the validated method?"*,
NOT *"prove State T."* A null in the wrong habitat is NOT evidence against T. Each instrument vs
scale-matched OU null (lam=−0.1; nulls scale-matched to each instrument's close-diff std). `acf1` and
`dir_eff` are scale-free (trustworthy); `innov_var` is scale-sensitive (relies on match quality).
Cohort designed for CONTRAST, n=1 per habitat (characterization, not inference).

| Instrument | Habitat | Pre-registered expectation | Role |
|---|---|---|---|
| **ADANIENT** | trend-heavy equity | **A (floor) or B (trend-ward: dir_eff↑, acf1↑)** — NOT C | negative-context control; C here ⇒ suspect artifact |
| **g1** | commodity outright | ambiguous (trend+reversion mix) | exploratory |
| **ng12** | spread (deployment domain) | **C plausible here** (innov_var↓, acf1↓, dir_eff↓) if T exists | existence probe |
| **rb23** | spread (deployment domain) | **C plausible here** if T exists | existence probe |

**The only existence-relevant pattern:** C in the spreads AND (A or B) in ADANIENT — that *contrast*
would justify deeper work. C everywhere (incl. ADANIENT) ⇒ likely method artifact, not T. A/B
everywhere ⇒ no empirical reason to keep believing T exists (in these instruments/windows).

### Phase 4 — real cohort RESULTS (run 2026-06-02; `scripts/state_t_cohort_probe.py`)
Cohort: ADANIENT (trend equity, control), g1 (commodity outright), ng12 & rb23 (deployment-domain
spreads; negative/near-zero prices — Arm 1 is log-free so handles them). Two independent comparisons.
**T-signature = all three descriptors NEGATIVE.**

**A. vs scale-matched OU-null** (d = real − OU; θ=1.5 shown):

| Instrument | innov_var | acf1* | dir_eff* | read |
|---|---|---|---|---|
| ADANIENT | −0.52 | **+0.92** | **+1.60** | B (trend-ward) — as pre-registered |
| g1 | −0.18 | **+0.78** | **+1.15** | B (trend-ward) |
| ng12 (spread) | −1.21 | +0.38 | **+1.63** | mixed: var↓ but strongly directional — NOT C |
| rb23 (spread) | +0.56 | +0.27 | **+2.01** | directional — NOT C |

**B. within-instrument high-|z| vs low-|z|** (confound-controlled; θ=1.5):

| Instrument | innov_var | acf1 | dir_eff |
|---|---|---|---|
| ADANIENT | +0.30 | +0.83 | +1.00 |
| g1 | +0.30 | +0.66 | +0.87 |
| ng12 (spread) | +0.09 | +0.37 | +1.00 |
| rb23 (spread) | +0.54 | +0.01 | +0.44 |

**FINDING (FALSIFYING / confidence-DECREASING for State T as specified):** *No instrument shows the
pre-registered C signature.* `dir_eff` is **positive in every instrument under BOTH comparisons** —
real high-deviation windows are MORE directionally efficient (continuation), not chop/stabilization.
`acf1` is positive (more continuation) almost everywhere; `innov_var` is not compressed within-series.
The within-instrument control reproduces the sign of the vs-OU read, so the directional character is
**not** a real-vs-OU artifact. Crucially, the **deployment-domain spreads (ng12, rb23) look
qualitatively like the trend control** — the existence-relevant contrast (C in spreads, B in ADANIENT)
**did not appear**. (The vs-OU `dir_eff` magnitudes +1.5…+2.3 vs within-instrument +0.4…+1.0 confirm a
*partial* vs-OU inflation — flagged, not load-bearing; the sign/conclusion is robust to it.)

- **Problem class:** existence result (substantive), with a controlled METHODOLOGY confound.
- **Confidence — State T exists IN THE FORM TESTED:** DEMOTED → **LOW**. Evidence trustworthiness:
  **MEDIUM** (real data, 2 agreeing comparisons, confound-controlled; but n=4, one signature, daily bars).
- **Explicit non-conclusions:** (1) This does NOT prove State T cannot exist. The window-averaged
  descriptor over [t−W+1, t] anchored at peak |z| is **dominated by the directional run-up**; a brief
  *terminal* stabilization (bars immediately after the peak) could be swamped and would not show here.
  (2) Only ONE morphology was tested. (3) n=4 instruments, daily resolution — not generalizable; these
  particular "spreads" may themselves be repricing/trend-dominated in their large-deviation episodes
  (their MR character was not separately verified). (4) Nothing here concerns intraday or other habitats.
- **Highest-information next question:** does a SHORT, FORWARD, post-peak window (immediately after a
  causal |z| peak) show stabilization that the symmetric pre-window averages away? — **NOTE: forward
  post-peak description edges toward the frozen "what happens after the extreme" detection question;
  requires alignment-advisor review BEFORE building (do not implement unprompted).**

**Bottom line for the programme:** the first real-data read gives **no empirical reason to elevate
belief in State T** (as a stabilize-then-revert morphology) in this cohort — including the
deployment-domain spreads. The honest posture is confidence-decreasing, with a clearly-scoped
methodological caveat (window placement) as the one surviving way the negative could be a measurement
artifact rather than a true absence.

> **PROVENANCE CORRECTION (alignment audit, 2026-06-02):** "Comparison B" (within-instrument
> high-|z| vs low-|z|) was **introduced at results-time as a confound control — it was NOT
> pre-registered as a named method.** §2 only implicitly contemplated the symmetric "vs the rest"
> partition. This is disclosed rather than glossed: B is *more* adversarial than the vs-OU comparison
> (it killed the CL-BRN tease, below), so its agreement strengthens the negative; but its provenance
> is post-hoc-control, not pre-registration. Pre-registered parameters (θ∈{1,1.5,2}, W=30, lam=−0.1,
> z_window=60) are bit-identical to Phase 3 — audit confirmed **no parameter drift, no signature
> redefinition, no hidden detection.**

### Phase 4b — cohort extended to 60-min intraday (DELL, AAPL, CL-BRN); run 2026-06-02
New instruments at a NEW resolution (60-min), challenging habitat-specificity. T-signature = all 3 NEGATIVE.

**A. vs OU-null (θ=1.5):** DELL(repricing) iv−0.52 acf+0.73 de+1.31 · AAPL(mixed) iv+0.15 acf+0.75
de+1.13 · CL-BRN(crude-brent spread) iv−1.29 **acf−0.14** de+0.53.
**B. within-instrument (θ=1.5):** DELL iv+0.28 acf+0.53 de+0.75 · AAPL iv+0.33 acf+0.58 de+0.57 ·
CL-BRN iv+0.16 acf+0.60 de+0.88.

CL-BRN's vs-OU `acf1−0.14` (the only sub-zero acf1 in the cohort) **inverts to +0.60 under the
confound-controlled comparison** → it was an OU-null calibration artifact (OU deviations are oddly
persistent), not a real property. **Under Comparison B, all 7 instruments / 2 resolutions / 3 θ show
positive dir_eff AND positive acf1 — unanimous directional continuation, zero T-signatures.**

**FINDING — SERIOUSLY THREATENED (FALSIFIED-IN-FORM, pending two scoped outs):**
- Confidence — State T as the pre-registered morphology: **LOW, approaching falsified.** `dir_eff`
  points the *wrong way* in every instrument; the result is unanimous across habitat AND resolution;
  the deployment spreads look like the trend control where C was most expected. Evidence
  trustworthiness: **MEDIUM-HIGH** (7 instruments, 2 resolutions, 2 methods, no drift).
- **Two surviving outs (both pre-existing, NOT post-hoc goalposts — ranked by cost):**
  1. **Substrate mismatch (cheapest, no freeze issue):** were the high-|z| anchors actually OU-like
     *at those windows*, or Trend-like? (Doc 10: ADANIENT reads RW-Null despite being trend-heavy —
     same scale-dependence may mean ng12/rb23/CL-BRN deviations occurred in trend-dominated windows,
     i.e. the wrong sub-population.) Disambiguate by **substrate-stratifying existing anchors** via the
     built `analytics_substrate` reads — near-zero new code. **This is the highest-information next step.**
  2. **Terminal-window blindness (one-shot license, alignment-gated):** the pre-window averages the
     directional run-up; a brief *post-peak* stabilization could be swamped. A short FORWARD post-peak
     window is a legitimate **final** test — but only with its signature pre-registered first, as the
     LAST window geometry (a third geometry after another negative = goalpost retreat), and after
     alignment review (detection-adjacent).
- **Concrete KILL condition (committed):** on substrate-confirmed **OU-like** anchors, in ≥2 spreads,
  across all θ, under BOTH pre-window and (alignment-cleared) post-peak window, **no consistent
  negative-direction signal** → the current State-T formulation is killed for this domain/resolution.
  No p-value required; consistent wrong-direction sign on the right substrate is sufficient.
- **Bayesian update:** entering Phase 4 prior on "T-as-specified exists in deployment domain" was
  already LOW-MEDIUM (after daily negative). The unanimous 60-min + daily negative removes most of the
  remaining mass: posterior **LOW** and dropping. The substrate-stratification result will be decisive
  — if OU-confirmed anchors are still negative, drop below LOW (≈ "not in this domain/resolution").

### Phase 5 — broad cross-habitat validation (PRE-REGISTERED before results, 2026-06-02)
New instruments added (unchanged machinery — same θ/W/descriptors/both comparisons, NO patching):
EURUSD 1D & 60m (FX major), BANKNIFTY 1D (index), **HDFCBANK−ICICIBANK pair spread 1D & 15m** (the
canonical mean-reversion habitat; negative-price spreads — log-free Arm 1 handles them). Pre-registered
per-instrument expectations (committed before seeing numbers; T-signature = innov_var↓ acf1↓ dir_eff↓):

| Instrument | Habitat | Expectation | Decisiveness |
|---|---|---|---|
| **HDFC−ICICI 1D** | **pair spread (canonical MR)** | **C most plausible HERE** | **HIGHEST** — if C fails here, best habitat failed → thesis seriously damaged |
| **HDFC−ICICI 15m** | pair spread, intraday | C plausible (intraday may help) | HIGH (short sample ~500 bars → modest power) |
| EURUSD 1D | FX major | mixed; mild C possible in range regimes | MEDIUM |
| EURUSD 60m | FX intraday | low power (~388 bars) | LOW |
| BANKNIFTY 1D | index | B (trend-ward), like equities | control-like |

**Decision rule (committed):** the pair spread is the make-or-break instrument. **C in the pair spread
(esp. 1D) ⇒ thesis STRENGTHENS** (right habitat finally shows the signature). **Directional continuation
in the pair spread like the rest of the cohort ⇒ thesis SERIOUSLY THREATENED → kill-condition met** (the
single best habitat failed). Mixed/ambiguous ⇒ neutral, defer to substrate-stratification.

### Phase 5 RESULTS & VERDICT — **FALSIFIED-IN-FORM. Current State-T formulation KILLED.** (2026-06-02)
Within-instrument (confound-controlled, trustworthy) θ=1.5, [innov_var, acf1, dir_eff]; T-sig = all NEGATIVE:
EURUSD-1d +.42/+.47/+.58 · EURUSD-60m +.35/+.39/+.36 · BANKNIFTY +.44/+.79/+.56 ·
**HDFC-ICICI pair-spread 1d +.29/+.27/+.96 · 15m +.64/+.46/+.77** (joining the prior 7). Across **12
instruments / 5+ habitats / 2-3 resolutions / 2 comparison methods / 3 θ**, `dir_eff` is **positive in
all 12**; the entire Section-B table has **one** negative cell (rb23 acf1 @θ=2). The pre-registered
DECISIVE instrument — the HDFC-ICICI pair spread (canonical mean-reversion habitat) — showed directional
continuation like everything else. **The committed kill-condition fired.**

**Prior thesis (preserved):** State T = an extended deviation from μ\* losing momentum and reverting,
producing innov_var↓ / acf1↓ / dir_eff↓ in high-|z| causal *pre-windows*.
**Evidence:** Phase 3 validated the method is NOT blind (no false positive on OU/RW; clean positive
control fired correctly at dir_eff≈−0.9 using the SAME anchoring). Phases 4/4b/5 → unanimous OPPOSITE sign.
**Adversarial panel (this session):** planner → kill-condition met, pivot to Arm-2. alignment-advisor →
machinery clean, no drift/redefinition/selective-reporting, kill is honest (not over-skepticism); the
forward post-peak window's one-shot license is **SPENT** (refuse as rescue); substrate-stratification is
confirmatory-only. skeptic → strongest survival argument (B-ii: trailing window mechanically forbids
dir_eff↓) **DEFEATED** by the positive control (same anchoring produced dir_eff↓ on a stabilizer).
null-hypothesis → entire 12-instrument result explained with NO State T by **selection-on-deviation**
(anchoring on |z|≥θ samples extreme-endpoint = directionally-efficient paths; magnitude inflated, but the
SIGN is set by real path shape) + **ordinary momentum/repricing**; no residual requires State T.
**Methodology class of the failure:** STRUCTURAL (the phenomenon as formulated is absent), not
MEASUREMENT — because the positive control rules out the trailing-window-geometry artifact.
**Confidence — current formulation reflects a real phenomenon in any tested habitat: ~5-10% (KILLED,
FALSIFIED-IN-FORM).** Broader State-T *idea* (post-deviation dynamics): ~40-50%, **UNTESTED** here.

**Explicit non-conclusions:** (1) Only ONE morphology (pre-window stabilization) was tested; absence of
THIS ≠ absence of all T-like phenomena. (2) The *aftermath* (what happens AFTER a causal |z| peak) was
never measured — that is a DIFFERENT hypothesis, detection-adjacent (doc 04 freeze), and must reopen only
as a NEW independently pre-registered programme, not a continuation (§4 zombie prohibition; advisor ruling).
(3) Sub-bar / faster-timescale variants untested.
**Reopen triggers (§4):** a *different, independently pre-registered* morphology (e.g. post-peak aftermath,
with freeze review); OR substrate-stratification revealing the cohort never contained OU-like anchors.
**Open refinement (not a gate):** a per-instrument matched OU/GARCH surrogate would quantify how much
positive dir_eff is selection-geometry vs true continuation — but it cannot flip the sign conclusion.
**Implementation note:** dir_eff / causal-z / innov_var all use LEVEL differences (not % returns), so
negative-price spreads are handled correctly; dir_eff returns NaN on flat (O=H=L=C) windows — no degenerate
inflation. (Verified against `analytics_substrate.directional_efficiency`, `analytics_mrscore.causal_zscore`.)
**Next authorized step:** Arm-2 full-information characterization — "what DO large deviations actually do?"
— observe the real morphology rather than test for a pre-supposed one. State-T DETECTION remains FROZEN.

---

### Phase 6 — Cross-habitat broad sweep: 62 files / 20+ instruments (2026-06-04)

**Authorization:** user-authorized re-investigation with new data. Zombie-reopen test satisfied: prior
failure (wrong-sign across 12 instruments; selection-on-deviation null reproduces it) was explicit; new
evidence (62 new files across diverse instruments) was unavailable at Phase 5; prior objections remain
binding; reopen trigger = cross-habitat breadth sufficient to settle the question definitively.

**Data:** `~/Downloads/mean-reversion-data/` — 62 CSV files spanning equities (US, India), commodities
(gold, silver, copper, platinum, WTI, Brent, corn, cocoa, coffee, cotton), FX (EURUSD, USDJPY, USDCHF,
DXY, INRUSD), rates (US10Y), at 15-min / 60-min / 1D resolutions. Same extraction parameters as all
prior phases (W=30, z_window=60, θ∈{1.0,1.5,2.0}, 12 OU null seeds, MIN_BARS=200, MIN_ANCHORS=10).
Stop-loss: halt if NOISE ≥ 19 files (30%). Script: `backend/scripts/state_t_broad_sweep.py`.

**Results (62/62 processed; stop-loss never triggered — zero NOISE files):**

| Verdict | Count | % |
|---|---|---|
| REJECTS | 62 | 100% |
| CONFIRMS | 0 | 0% |
| INCONCLUSIVE | 0 | 0% |
| NOISE | 0 | 0% |

**Pattern (consistent across all 62 files):**

| Descriptor | Direction vs OU null | Effect size range (d @θ=1.0) | Assessment |
|---|---|---|---|
| `acf1` | **WRONG (+)** — universally | +0.40 to +0.70 | Strong wrong-direction; zero exceptions |
| `dir_eff` | **WRONG (+)** — universally | +0.78 to +1.16 | Very strong wrong-direction; zero exceptions |
| `innov_var` | mixed | −1.39 to +0.67 | Inconsistent; not compressed |

Not a single file across any asset class, resolution, or geography showed the pre-registered T-signature
(all 3 negative). The `acf1` and `dir_eff` effect sizes are not near zero — they are consistently and
substantially in the wrong direction.

**VERDICT — ARCHIVED. State T (pre-window stabilization morphology) is definitively dead.**

This phase removes the last residual uncertainty from Phase 5. Phase 5 killed the specific 12-instrument
cohort. Phase 6 extends that to 62 files / 20+ instruments / 3 resolutions / all major asset classes —
same result. No habitat shows a hint of the T-signature. The data breadth was sufficient to trigger the
stop-loss (≥19 NOISE) if the data was inadequate; it did not trigger, meaning the rejection is clean.

- **Confidence — State T as pre-window stabilization morphology exists:** < 5% (ARCHIVED).
- **Reopen triggers:** NONE remaining for this morphology. The §4 zombie-prohibition is now load-bearing:
  any future resurrection must pass the full zombie-reopen test with a NEW independently pre-registered
  morphology (NOT a variant of pre-window stabilization), a NEW mechanism, and NEW evidence not
  explained by selection-on-deviation.
- **Explicit non-conclusions (preserved from Phase 5):** (1) This does NOT prove no post-deviation
  structure exists — only that this specific morphology (pre-window stabilization) does not. (2) The
  aftermath / post-peak dynamics remain UNTESTED here (detection-adjacent, frozen). (3) Residual Ecology
  (observational description around realized reversions) is a DIFFERENT hypothesis, separately gated.
- **What the signal IS (selection-on-deviation, confirmed):** anchoring on |z|≥θ samples paths that
  arrived at an extreme by directional travel → those pre-windows ARE directionally efficient by
  construction. The OPPOSITE of stabilization. This is the complete mechanistic explanation; no State T
  required.
