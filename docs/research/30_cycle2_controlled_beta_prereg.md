# 30 — Cycle 2: Controlled-β Admissibility Initiative — Specification & Admissibility Protocol

## Status

```text
DATE:        2026-06-04
MODE:        Research Mode — SPECIFICATION + ADMISSIBILITY DESIGN ONLY. No code. No data touched. No execution.
SCOPE:       The Cycle-2 trigger named in doc 20 §7: can a CONTROLLED/REGULARIZED hedge ratio β construct an
             admissible non-definitional spread that does NOT manufacture diffusion — the gate on the entire
             pairs / cross-asset-RV deployment premise.
RIGOR BAR:   equivalent to doc 28 (positive control · martingale zero-control · causal/OOS · surrogate logic ·
             leakage traps · frozen parameter surfaces · pass/fail · permanent-demotion trigger).
PRINCIPLE:   smallest faithful experiment on the highest-leverage uncertainty. "disappointingly simple but
             causally faithful." Reuse the doc-18a/20/21 apparatus; build only the β-construction gap.
SUPERSEDES NOTHING; EXTENDS: doc 20 (Cycle 1, β=1 definitional) → Cycle 2 (estimated β). Inherits the doc-18a
             VR ontology, surrogate ensemble, multiplicity-corrected min-VR, and FPR/power calibration verbatim.
BINDING PRIORS (do NOT relitigate):
  • rolling-OLS-β-on-levels (W=60) is INADMISSIBLE — PROVEN to manufacture super-diffusion (doc 19, HIGH).
  • β=1 definitional spreads are admissible/artifact-free (zero β-DOF; doc 19 §3, doc 20).
  • the discriminator is VR(q) real-minus-surrogate + equilibrium stability, NEVER residual ACF/half-life
    (smoother-manufactured, doc 06 C5 / doc 08 / doc 14 §5).
  • full-sample / hindsight β is CONTAMINATED by construction (doc 12 Arm 0).
```

---

## 1. Exact research object

**What is adjudicated — stated precisely.** NOT "a better β." The object is:

> **Does there exist a CAUSAL, pre-frozen β-estimation construction that forms an economically-meaningful spread
> for a genuine (non-definitional) cointegrated pair WITHOUT injecting its own dynamics into the variance-ratio —
> i.e. a β that does not MANUFACTURE diffusion (in either direction) nor DESTROY genuine reversion?**

This is a **construction-validity** question, not a market question and not an optimization. We are not asking
"which β makes the spread most stationary" (that objective is itself the laundered-lookahead trap — §4 L2). We
are asking whether estimating β can be done **VR-neutrally**.

### 1.1 The mechanism this must defeat (explicit connection to the v1 failure)

doc 19 decomposed the frozen increment and proved the failure mechanism:

```text
ΔS_t = (ΔA_t − β_{t−1}·ΔB_t)  −  (β_{t−1} − β_{t−2})·B_{t−1}
                                  └───────── β-update-noise term ─────────┘
```

The second term — **β-update-noise × a large trending price level** — was **82–97% of Var(ΔS)** on the failing
spreads (ACF≈0.81), and **manufactured super-diffusion**: for synthetic `A = 3·B + OU` (true spread IS OU, true
VR<1 = [0.97,0.91,0.81,0.65]), rolling-β W60 fabricated VR = [1.81,3.68,5.46,6.23]; **ablating the β-update term
recovered the true VR<1.** The moving construction parameter injected its own persistent dynamics into the
measured object — the hedge-ratio analogue of the doc-07 lag illusion. **Any Cycle-2 β must be shown not to do
this**, and the test is mechanistic (the decomposition itself), not merely symptomatic (VR).

### 1.2 Definitions (frozen)

```text
ADMISSIBLE β-construction — a β-estimator that, on the frozen control suite, SIMULTANEOUSLY:
  (P) PRESERVES genuine reversion — recovers VR<1 and beats the matched nulls on a synthetic OU pair (power);
  (N) MANUFACTURES nothing — yields VR within the no-manufacture band (two-sided: NOT VR≪1, NOT VR≫1) on a
      synthetic MARTINGALE pair, INCLUDING the trending-B stress configuration that broke v1;
  (M) is MECHANISTICALLY clean — the β-update-variance fraction (the doc-19 term's share of Var(ΔS)) is below a
      frozen bound on the martingale/trending nulls;
  (C) is CAUSAL — β_t uses only data ≤ t−1 (future-injection bit-identity holds); hyperparameters frozen a priori.

SUCCESS (Cycle-2) — ≥1 admissible β-family exists (passes P∧N∧M∧C on synthetics) AND, applied to the pre-
  registered real textbook cointegrated pair, yields a CONFIRM (VR<1 beats RW∧GARCH∧MA(1), multiplicity-
  corrected) that is NOT attributable to a hindsight/full-sample β. → the deployment domain opens to estimated-β
  pairs; controlled-β is established admissible.

FAILURE (Cycle-2, ordinary) — no admissible family confirms on the real pair, OR the real pair nulls under every
  admissible family. A frozen-construction null on the real pair is a LEGITIMATE terminal outcome (market/horizon
  fact), NOT automatically apparatus failure (the doc-20 §6 two-sided rule applies).

PERMANENT DEMOTION (severe — see §2.6) — EVERY admissible-in-principle family FAILS the two-sided control: each
  either manufactures VR on the martingale pair (N or M fails) OR destroys OU on the positive control (P fails).
  → no VR-neutral estimated-β exists; deployment reduces to β=1 DEFINITIONAL spreads only.

DISALLOWED CONSTRUCTIONS (banned a priori — §4): full-sample/hindsight β; short-window rolling-OLS-on-levels
  (the v1 W=60 form, doc 19); any β with hyperparameters tuned on the test pair; any β judged by residual
  ACF/half-life.
```

---

## 2. Frozen admissibility protocol (doc-28-equivalent rigor)

### 2.1 The empirical claim under test (frozen, per candidate family f)

> For a pre-registered real cointegrated pair `(A,B)` with a *published* MR result, does the level-difference
> `VR(q)`, `q∈{2,5,10,20}`, of `S_t = A_t − β^f_{t−1}·B_t` (β^f causal, hyperparameters frozen) lie below the
> 5th percentile of its matched **RW ∧ GARCH(1,1) ∧ MA(1)** ensembles (multiplicity-corrected min-VR, `VR<1`),
> **AND** does the β-update-variance fraction stay below the frozen bound — i.e. does an admissible β reveal
> genuine pair MR *without manufacturing it*?

### 2.2 Positive control (power) — frozen

```text
SYNTHETIC OU PAIR:  B_t = trending RW (drift + unit-root level, the v1-dangerous configuration);
                    A_t = β*·B_t + u_t,  u_t = genuine OU deviation (true VR<1), β* known.
REQUIREMENT (P):    each candidate family, applied CAUSALLY, recovers a spread with VR<1 that beats the nulls —
                    i.e. the construction does NOT destroy the embedded OU (over-shrinkage / over-smoothing kills
                    signal = a real failure mode of regularized β). Mirrors doc 20 §5a item 1, at the β level.
```

### 2.3 Martingale zero-controls (the decisive two-sided test) — frozen

```text
Z1 — TRUE-MARTINGALE PAIR:  A_t = β*·B_t + w_t,  w_t = pure RW (true spread is a martingale, true VR≈1).
     REQUIREMENT (N):  every family yields VR within a frozen no-manufacture band around 1 — NOT VR<1 (false
     confirm) and NOT VR≫1 (false kill). This is the gate v1 rolling-OLS FAILS.
Z2 — DOC-19 STRESS NULL (mandatory):  A = c·B + RW with B STRONGLY TRENDING — the exact β-update-noise×level
     configuration that fabricated VR=[1.81…6.23]. REQUIREMENT (N+M): the family must NOT reproduce the
     super-diffusion AND its β-update-variance fraction must clear the §2.4 bound. A family that fires here is
     the v1 artifact in new clothing → inadmissible.
Z3 — INDEPENDENT-LEGS NULL:  A,B independent RWs, β*=0 (no cointegration). The estimator must not invent a
     spread structure from noise (β̂ should be ~0/unstable → flagged, not confirmed).
```

### 2.4 β-update-variance decomposition gate (M — the mechanistic root-cause instrument) — frozen

```text
For any spread, compute the doc-19 identity term and its variance share:
   f_βupdate = Var[ (β_{t−1}−β_{t−2})·B_{t−1} ]  /  Var[ ΔS_t ]      (mask-aware, causal, on valid increments)
ADMISSIBILITY:  f_βupdate < τ  (frozen bound, e.g. τ = 0.10) on Z1/Z2/Z3.
  β=1 has f_βupdate ≡ 0 (definitionally admissible — the reference floor).
  v1 rolling-OLS W60 had f_βupdate ≈ 0.82–0.97 (the failure signature).
This gate is the heart of Cycle 2: it catches the artifact AT ITS SOURCE, is ground-truth-free (an identity),
and is the single most diagnostic admissibility read. A family can pass VR-band on a weak null yet fail here —
M is a SEPARATE, binding gate, not implied by N.
```

### 2.5 Surrogate / null logic, causal/OOS, leakage, frozen surfaces

```text
SURROGATE GAUNTLET (inherited verbatim, doc 18a/20):  RW ∧ GARCH(1,1) ∧ MA(1)-microstructure-noise, N=200
  draws/family, IDENTICAL length+mask+VR extraction (bias-cancel), causal/pre-sample fits, q∈{2,5,10,20},
  multiplicity-corrected min-VR at 5th pct, real_min<1, frozen seed. OU(AR1) retained as non-gating reference.
CAUSAL/OOS:  β_t = g(data ≤ t−1) only (the existing .shift(1) firewall); future-injection bit-identity acceptance
  test REQUIRED on every real and synthetic series (a detonated future bar leaves every earlier β and spread
  value bit-identical — exists in the v1 engine). Hyperparameters (shrinkage λ, β-process-noise, window) FROZEN
  on the synthetic control suite, NEVER tuned on the real pair.
SYNTHETIC CALIBRATION GATE (must pass BEFORE any real read is a verdict, per doc 20 §5a, extended):
  (1) positive control (§2.2) CONFIRMS for the family;  (2) Z1 within no-manufacture band;  (3) Z2 stress null
  within band AND f_βupdate<τ;  (4) Z3 invents nothing;  (5) FPR ≈ 5% / power ≈ 100% reproduced on the new β
  code path (doc-18a's 1.7%/100% does NOT transfer — new path). If (1)–(5) fail, recalibrate ON SYNTHETIC only.
FROZEN PARAMETER SURFACES:  the candidate β-family SET (§4) and each family's hyperparameters · the VR q-grid ·
  N · seed · τ (β-update bound) · the no-manufacture band · the FPR/power thresholds · the real pair(s) & roles ·
  the decision rule. All fixed BEFORE the run; full (family × instrument × q × null) matrix reported; NO argmax
  over families on the real pair (§11.7) — admissibility is decided on SYNTHETIC controls, the real pair is the
  application of already-admissible families.
LEAKAGE TRAPS: see §4 L1–L5.
```

### 2.6 Pass/fail + what would PERMANENTLY DEMOTE controlled-β

```text
PER-FAMILY ADMISSIBLE  iff  P ∧ N ∧ M ∧ C  on the synthetic control suite (decided BEFORE touching the real pair).
CYCLE-2 CONFIRM  iff  ≥1 admissible family yields a real-pair CONFIRM (VR<1 beats RW∧GARCH∧MA1, multiplicity-
  corrected, f_βupdate<τ on the real pair) that survives the open/close + (where applicable) deseason checks and
  is not a hindsight-β artifact.  → controlled-β ESTABLISHED ADMISSIBLE; deployment opens to estimated-β pairs.
CYCLE-2 NULL (ordinary)  — no admissible family confirms on the real pair → the pair lacks beatable short-horizon
  level MR under admissible construction; a market/horizon fact (doc 20 §6 two-sided rule), not a demotion.

PERMANENT DEMOTION of controlled-β (the severe failure)  iff  ALL of:
  (i)  EVERY admissible-in-principle family (§4) fails the two-sided synthetic control — each either manufactures
       VR on Z1/Z2 (N or M fails) OR destroys OU on the positive control (P fails); AND
  (ii) the failure is intrinsic, not apparatus: the positive control itself CONFIRMS for at least the static β=1
       baseline (proving the gauntlet can see a true pair-OU) — so the failure is the ESTIMATOR, not the test;
  (iii) no family achieves the (P, N, M) trilemma — there is no β-estimation that is simultaneously VR-neutral on
       nulls AND VR-preserving on true OU.
  CONSEQUENCE: estimated β cannot construct admissible non-definitional spreads. The deployment domain reduces to
  β=1 DEFINITIONAL spreads only (calendars / same-unit). Genuine cross-asset PAIRS become non-constructible
  admissibly → the cohort-breadth / netting / portfolio premise (doc 25) loses its main breadth source. This is a
  STRATEGIC demotion of the pairs line, recorded in the registry; the "dynamic shrunk/regularized hedge ratio"
  item moves DEFERRED → ARCHIVED with this trigger fired.
  GUARD (apparatus-not-market, doc 19 precedent): if the positive control fails for EVERY family INCLUDING β=1
  (the gauntlet cannot confirm any synthetic OU pair), the verdict is INCONCLUSIVE — recalibrate the apparatus,
  NOT demote controlled-β.
```

**What would constitute a Cycle-2 failure severe enough to permanently demote controlled-β?** Precisely §2.6:
not one family failing, but the **trilemma being unsatisfiable** — every admissible-in-principle family forced
to choose between *manufacturing diffusion* (fails N/M) and *destroying it* (fails P), with the gauntlet proven
able to see a true pair-OU (so the failure is the estimator, not the test). That outcome says estimated β is
*intrinsically* diffusion-distorting and collapses the deployment domain to definitional spreads — an
existential demotion of the pairs/cross-asset-RV thesis, not a method tweak.

---

## 3. Smallest possible implementation surface

```text
REUSE AS-IS (the doc-18a/20/21 apparatus — do NOT rebuild):
  analytics_arm_a.py    construct_spread (HAS beta_mode hook) · Spread · causal_rolling_beta (= long-window OLS
                        family for free, just freeze a large W) · _valid_increment_mask · level_vr ·
                        roll_transition_mask · _fit/_sim {rw, ou, garch} · surrogate_vr_ensemble · evaluate_spread
  analytics_arm_a_v2.py ma1_vr_ensemble · evaluate_v2 · MARTINGALE_GATE_V2 (RW∧GARCH∧MA1) · min-VR multiplicity
  synthetic.py          ou · random_walk · drift_random_walk · vol_cluster   (building blocks for the pair gens)
  tests                 future-injection bit-identity pattern · FPR/power calibration pattern

GENUINELY NEW (small, additive — one module `analytics_arm_a_v2_beta.py` + a few synthetic gens):
  B1  ridge_beta(a, b, *, lam, target) -> β_t        causal long-window OLS shrunk toward `target` (1 / contract
                                                      ratio / long-window β); ~25–35 lines.
  B2  kalman_beta(a, b, *, q_beta) -> β_t            random-walk-β state-space, FROZEN tiny process noise q_beta;
                                                      causal one-step β_{t|t−1}; ~40–60 lines.
      (long-window causal OLS = causal_rolling_beta at a FROZEN large W — no new code, a frozen parameter.)
  B3  beta_update_variance_fraction(spread) -> float the doc-19 decomposition gate (§2.4); ~15 lines. THE new
                                                      mechanistic instrument.
  B4  synthetic_pair(beta_star, dev_kind, trend, n, seed) -> (A,B)   OU-pair / martingale-pair / independent-legs
                                                      generators for §2.2–2.3; ~30 lines (composes existing gens).
  B5  controlled_beta_admissibility_run()           orchestration: controls → per-family (P,N,M,C) → real pair;
                                                      emits the full matrix. ~80–120 lines.
NO framework. NO generalized spread engine. NO architecture. construct_spread gains two beta_mode values
("ridge","kalman") dispatching to B1/B2; everything else is the existing path. Total new ≈ 200–270 lines.
```

---

## 4. Candidate β families (constrained comparison)

**What survives IN PRINCIPLE after the v1 rolling-OLS-on-levels artifact** — the discriminating property is
*β-update discipline*: does the family hold β still enough that `f_βupdate` (the doc-19 term) is negligible,
while still tracking a genuine slow cointegration drift?

```text
SURVIVES IN PRINCIPLE (enters the frozen comparison — admissibility decided by §2 controls, NOT assumed):
  F1  Kalman / shrunk-β (random-walk-β, FROZEN tiny process noise)  — the registry "dynamic shrunk/regularized
      hedge ratio" desk workhorse. Survives BECAUSE small process noise ⇒ β moves slowly ⇒ f_βupdate small. But a
      Kalman-β with too much process noise REPRODUCES the v1 artifact — so it is admissible ONLY if it clears Z2/M.
  F2  Ridge / shrinkage-β toward a prior (1, the contract/units ratio, or a long-window β)  — shrinkage lowers β
      variance ⇒ lowers f_βupdate. Survives in principle; admissibility via the controls.
  F3  Long-window causal OLS (FROZEN large W, e.g. ≥250)  — doc 19 showed W=500 took Gold–Silver VR(20) 5.93→0.60;
      a long window starves the β-update term. Closest to the killed form ⇒ HIGHEST suspicion ⇒ admissible only on
      a clean Z2/M pass. (Free to test: existing causal_rolling_beta at frozen large W.)
  REFERENCE (non-candidate, for calibration floors): β=1 definitional (f_βupdate≡0) and full-sample β (the
      hindsight ceiling) bracket the admissible region.

BANNED IMMEDIATELY (no test — zombie prohibition / proven / leakage):
  L-BAN-1  FULL-SAMPLE / HINDSIGHT cointegration β (Engle–Granger/Johansen on the whole series) — stationary by
           construction, CONTAMINATED (doc 12 Arm 0); indistinguishable from a genuine reverter.
  L-BAN-2  SHORT-WINDOW rolling-OLS-on-levels (the v1 W=60 form) — PROVEN to manufacture VR (doc 19, HIGH);
           reopening requires a NEW mechanism, not a re-run (§4 zombie test).
  L-BAN-3  Any β whose hyperparameters (λ, q_beta, W) are TUNED ON THE TEST PAIR to maximize VR<1 / ADF / stationarity
           — argmax-on-evaluation = laundered lookahead (doc 14 DANGER-1).
  L-BAN-4  β judged by residual ACF / half-life quality — smoother-manufactured discriminator (doc 06 C5).
  L-BAN-5  β estimated in return-space then applied to levels (or any future-bar use) — causality / space mismatch.

CONSTRAINT (anti-multiplicity, §11.7): the family SET, each family's FROZEN hyperparameters, AND the real pair(s)
  are pre-committed. The full matrix is reported. Admissibility is earned on the SYNTHETIC controls; only an
  already-admissible family's real-pair read is interpreted. No promoting "the family that confirmed" post-hoc.
```

---

## 5. Strategic EV — why controlled-β is now the keystone

**The dependency chain (the user's framing, made precise):**

```text
controlled-β ADMISSIBILITY  →  cohort BREADTH  →  per-sleeve EXPECTANCY  →  PORTFOLIO object
```

**Why it outranks the alternatives — each is structurally DOWNSTREAM of construction admissibility:**

```text
vs HABITAT PERSISTENCE (doc 28): doc 28 characterizes WHICH regimes/windows a GIVEN admissible spread is
  MR-compatible. But on a NON-definitional pair, the spread does not exist until β is chosen — and if β
  manufactures diffusion (doc 19), doc 28's VR-based habitat label INHERITS the construction artifact. doc 28 is
  scientifically admissible (doc 25 chain) yet, on estimated-β pairs, its INPUTS are construction-gated: running
  it before controlled-β is settled risks measuring the β-estimator, not the market. doc 28 is therefore
  economically downstream AND input-gated. (On β=1 calendars doc 28 is already runnable — but calendars are the
  narrow slice; the breadth question is exactly the pairs question.)

vs PORTFOLIO ECONOMICS (doc 25): doc 25's own verdict — "binding bottleneck = admissible-cohort BREADTH, not
  timing"; "netting structurally absent (cohort = NG alone)." The portfolio object needs ≥2 INDEPENDENTLY
  cost-clearing sleeves to net. Cycle 1 validated ONLY β=1 definitional spreads → one calendar (NG), which is
  "persistent but uneconomic" (doc 23). Breadth — more independent admissible spreads — comes almost entirely
  from PAIRS / cross-asset RV, which require estimated β. So controlled-β is the gate on the breadth that the
  portfolio premise is starved of. Without it, doc 25 has nothing to net.

vs RESIDUAL ECOLOGY (§11.5): the lowest-priority, highest-zombie-risk observational arm, explicitly gated behind
  the positive control AND a verified habitat. It describes morphology AROUND realized reversions on admissible
  spreads — needs admissible spreads first. Strictly downstream.

WHY IT IS THE HIGHEST-LEVERAGE UNCERTAINTY (smallest-experiment / largest-fork):
  • The answer is BINARY and THESIS-LEVEL: either an admissible estimated-β exists (deployment domain OPENS to
    pairs → breadth → portfolio is testable) or it does not (deployment COLLAPSES to definitional calendars → the
    pairs / cross-asset-RV premise — the stated deployment domain, CLAUDE.md §1.1 — is largely unreachable).
  • It is the CONSTRUCTION analogue of the §11.8 positive control: Cycle 1 proved the apparatus can CONFIRM a
    known edge on a definitional spread; Cycle 2 proves whether it can ADMISSIBLY CONSTRUCT a known edge on a
    textbook pair. Until that holds, EVERY non-definitional pairs result in the programme is construction-suspect
    (doc 19 is the standing proof that this suspicion is not hypothetical).
  • The experiment is small (§3: ~200–270 additive lines, full apparatus reused) and resolves a fork that gates
    doc 25, doc 28-on-pairs, and the whole deployment thesis. That is exactly "smallest faithful experiment on the
    highest-leverage uncertainty."
```

**Sequencing recommendation (research-mode, no execution):** PAUSE doc-28 implementation before Step A (as
directed). Run Cycle 2 FIRST as a pure admissibility experiment on synthetic controls + one pre-registered
textbook pair. Its verdict re-prices everything downstream: CONFIRM → doc 28 becomes runnable on a now-admissible
pair cohort and doc 25 gains netting candidates; PERMANENT DEMOTION → the programme honestly narrows to
definitional spreads and the breadth bottleneck becomes a DATA-acquisition problem (legs with the right
structure), not a method problem.

---

## 6. What this is NOT · non-conclusions · next action

```text
NOT State T; not a detector/score/timing/signal; no per-bar object; banned vocab excluded. Does NOT touch
  μ*/Kalman/EMA residual (no doc-06 §15.8 trip — this is spread CONSTRUCTION, not equilibrium-residual fidelity).
  Not a tradeable-edge claim: an apparatus/construction-validation gate (doc 20 lineage).
NON-CONCLUSIONS: no claim that any β family IS or is NOT admissible (unrun); no claim the real pair is/ isn't MR;
  no β hyperparameter is chosen here — only the SET and the protocol are specified. β=1 remains the only
  currently-admissible construction until this runs.
NEXT ACTION (on authorization only): (1) pre-commit the real textbook cointegrated pair(s) with a published MR
  result + each family's frozen hyperparameters + τ + the no-manufacture band; (2) freeze this as the Cycle-2
  pre-registration; (3) implement §3 B1–B5; (4) pass the §2.5 synthetic calibration gate BEFORE any real read.
  No code is written and no data is touched by this specification.
```
