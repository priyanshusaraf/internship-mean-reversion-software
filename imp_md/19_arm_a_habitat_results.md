# Arm A — Habitat Discovery: Execution, Audit, Red-Team & Verdict

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **COMPLETE — first verdict-capable deployment-domain MR read in the programme.** Executes doc 18 +
doc 18a exactly; reports real−surrogate only.
**Date:** 2026-06-03. **Mode:** Controlled-Implementation (execution) → Research (adjudication).
**Provenance:** built from the 46 TRUSTED raw legs (`data/mr_cohort_manifest.md`); engine
`backend/app/services/analytics_arm_a.py` (9 causal/ground-truth tests green); runner
`scripts/run_arm_a.py`; diagnostics `scripts/diagnose_arm_a.py`; results `data/processed/arm_a_results.json`;
three independent adversarial sub-reviews (Methodology, Statistical Integrity, Red Team). Confidence labels are
trustworthiness-of-evidence, not excitement.

> **Headline verdict:** **INCONCLUSIVE — and the pre-registered test was demonstrably construction-defective.**
> The frozen rolling-β-on-levels construction *manufactures* the property it measures (proven), so the decisive
> instruments were never validly tested; the two superficial "confirms" are an artifact and a vol-clustering
> near-miss. The deployment-domain MR premise is **neither confirmed nor validly damaged.** Binding next action:
> fix the hedge-ratio construction, re-pre-register, re-run. (Full reasoning §5.)

---

## 1. Execution log (what was actually run)

- **Cohort (7 spreads), built from raw legs**, β policy / roll-handling / trims per doc 18 §2 + doc 18a. Inner-join
  on UTC timestamps; level differences (NP-1); Open/Close only; causal lagged β (C-3); ADR_003 roll-masking on
  continuous-futures legs; WTI–Brent post-2011; Pt–Pd composite flat-dropped. Seed 20260603, N=200 surrogates.
- **Statistic:** level-difference VR(q)=Var(S_t−S_{t−q})/(q·Var(ΔS)), q∈{2,5,10,20}; verdict = multiplicity-
  corrected min-VR vs RW & GARCH martingale nulls at 5th pct, robust across roll-clean + flat-trim (doc 18a, ratified).
- **Causal firewall:** every spread passed a **future-injection bit-identity acceptance test** (a detonated future
  leg bar leaves every earlier β and spread value bit-identical). `all_causal_proofs_pass = True`.
- **Engine validated** on synthetic ground truth pre-execution: future-injection causality, negative-safe VR, roll
  detection, character recovery (OU<1 / RW≈1 / momentum>1), and FPR/power calibration (corrected rule 1.7% FPR vs
  naive 10%; 100% power at φ∈{0.95,0.9,0.8}).
- **One in-flight engine defect found by audit and fixed (then re-run):** the GARCH(1,1) null silently collapsed to
  the RW null on IGARCH fits (α+β=1) via an over-aggressive guard — so "RW & GARCH" was one null tested twice.
  Fixed to admit IGARCH with variance-targeted simulation; cohort re-run. This is an implementation-faithfulness fix
  (the frozen rule said "GARCH(1,1)"); it materially changed the WTI–Brent read (§4 D1).

## 2. Methodology audit (leakage / construction / admissibility — classified)

- **Causality: CLEAN (STRUCTURAL).** All β and surrogate parameters use only data ≤ t−1; future-injection bit-identity
  holds on all 7 real spreads. No lookahead, no full-sample β, no future normalization.
- **THE decisive defect — rolling-β-on-levels manufactures super-diffusion (STRUCTURAL, verdict-invalidating).**
  Decompose the frozen increment: `ΔS_t = (ΔA_t − β_{t−1}ΔB_t) − (β_{t−1}−β_{t−2})·B_{t−1}`. The second term —
  β-update-noise × a large trending price level — is **82–97 % of Var(ΔS)** on the failing spreads (independently
  measured by two reviewers; ACF≈0.81). It injects a smooth persistent component → VR≫1. **Proven on synthetic
  ground truth:** for `A=3·B+OU` (true spread *is* OU, true VR<1), the true-β VR=[0.97,0.91,0.81,0.65] but rolling-β
  W60 fabricates VR=[1.81,3.68,5.46,6.23]; ablating the β-update term recovers the true VR<1. This is the **doc-07
  lag-illusion / doc-13 HR-4 mechanism at the hedge-ratio level** — previously "undemonstrated at the β level"
  (red-team note #3); **now DEMONSTRATED for the VR-inflation direction (HR-4 conjecture STRENGTHENED).**
- **USD/INR is a stale-quote artifact (MEASUREMENT, inadmissible).** 75.6 % flat (O=H=L=C) bars, 14.4 % exactly-zero
  increments in clustered runs. The i.i.d./OU/GARCH surrogates carry **no** zero-clustering, so real−surrogate
  measures *non-trading*, not reversion; flat-trim leaves q=20 with zero clean spans (VR=NaN). **Demote USD/INR to
  UNUSABLE** — it is not an admissible confirm despite p=0.005.
- **GARCH null adequacy (METHODOLOGY, fixed).** See §1 / §4 D1. Post-fix, real squared-increment ACF≈0.44 on the
  two clean candidates confirms genuine vol clustering was present and the null now does real work.

## 3. Habitat Discovery results (real − matched surrogate; never raw)

Multiplicity-corrected min-VR p-value vs each matched null (p<0.05 ⇒ separates in the MR direction):

| # | Spread | role | β | n | flat% | VR(2,5,10,20) | p(RW) | p(GARCH) | p(OU) | **Admissible confirm?** |
|---|---|---|---|--:|--:|---|--:|--:|--:|:--:|
| 1 | **HDFC–ICICI** | DECISIVE | roll 0.36 | 5543 | 0.1 | 1.71,3.41,5.08,6.25 | 1.0 | 1.0 | 1.0 | **No — construction-invalid** |
| 2 | **Gold–Silver** | DECISIVE | roll 27.5 | 8784 | 20.6 | 1.62,3.13,4.71,5.93 | 1.0 | 1.0 | 1.0 | **No — construction-invalid** |
| 3 | USD/INR cal | reference | β=1 | 3342 | **75.6** | 0.60,0.31,0.20,0.14 | 0.005 | 0.005 | 0.005 | **No — stale-quote artifact** |
| 4 | Gold–Copper | cohort | roll 72.6 | 8783 | 20.6 | 1.68,3.22,4.69,5.75 | 1.0 | 1.0 | 1.0 | No — construction-invalid |
| 5 | Platinum–Palladium | cohort | roll 0.50 | 6805 | 0.4 | 1.54,2.91,4.24,5.23 | 1.0 | 1.0 | 1.0 | No — construction-invalid |
| 6 | **WTI–Brent** | cohort | roll 0.94 | 2626 | 0.0 | 0.70,0.67,0.82,0.94 | **0.005** | **0.094** | 0.01 | **No — fails vol-clustering null** |
| 7 | TCS–INFY | cohort | roll 1.16 | 5369 | 0.1 | 1.71,3.31,4.97,6.21 | 1.0 | 1.0 | 1.0 | No — construction-invalid |

**Admissible robust confirmations: 0 of 7.** (The runner's `robust_confirmed=['USD/INR']` is the literal engine
flag, which does not gate on flat-bar admissibility; the §2 adjudication overrides it to UNUSABLE.)

**Construction diagnostic (non-verdict; shows the artifact):** the same pairs are sub-diffusive (VR<1) under β=1,
full-sample β, log-ratio, AND a *legal* longer causal window, but super-diffusive only under the frozen W=60 rolling-β:

| Spread | β=1 (ADF) | roll-W60 (frozen) | roll-W250 | roll-W500 | full-OLS β | log-ratio |
|---|---|---|---|---|---|---|
| HDFC–ICICI | 0.69 (ADF +0.48) | **6.25** | 3.61 | — | 0.70 | 0.63 |
| Gold–Silver | 0.80 (ADF +4.39) | **5.93** | 2.25 | **0.60** | 0.73 | 0.93 |
| WTI–Brent | **0.09** (ADF −4.29) | 0.90 | 0.14 | — | 0.09 | 0.09 |
*(VR at q=20.)* WTI–Brent is the **only** spread VR<1 under *every* construction — but β=1 is HR-1-inadmissible for
the non-definitional pairs and their β=1 differences are **non-stationary** (ADF positive), so the pairs' apparent
β=1 "MR" is co-trending illusion, not tradeable reversion, and cannot be used as evidence (no goalpost-moving).

## 4. Red-team critique (three independent adversaries — PRECEDES the verdict)

The committee was run before concluding, and it **corrected the Chief-Scientist's first-pass overreach**
("weak–moderate evidence FOR deployment MR") — preserved here per §5-provenance discipline.

- **D1 (Statistical Integrity, MAJOR, verdict-changing):** GARCH null degenerated to RW on both confirms (IGARCH);
  fixed and re-run. **Consequence: WTI–Brent now FAILS the vol-clustering null (p=0.094);** its short-horizon
  sub-diffusion is largely volatility clustering (sq-increment ACF≈0.44; GARCH min-VR p5=0.637 < real 0.674), not
  clean level mean-reversion. The lone RW-separating spread does **not** survive the full ratified gauntlet.
- **USD/INR inadmissible (MAJOR):** stale-quote artifact (§2). Drop to UNUSABLE.
- **Construction artifact (STRUCTURAL):** the DECISIVE failures are 82–97 % β-update-noise (§2) → the literal kill
  fired on contaminated evidence and is **invalid**; but β=1 is inadmissible as a rescue, so the correct state for
  the pairs is **UNRESOLVED**, not "MR confirmed."
- **Devil's advocate, honest concession:** the negative is genuinely **fragile** — a legal causal W=500 takes
  Gold–Silver to VR<1 — so the W=60 freeze was a poor a-priori choice (its own doc-18a fragility clause anticipated
  W-disagreement). But fragile ≠ confirmed; the affirmative case still does not survive.
- **Statistical hygiene:** p=0.005 is the 1/(N+1) floor; at N=2000, WTI–Brent vs RW is p≈0.001 (genuine, finite),
  USD/INR is p<0.0005 (the floor here signals a *degenerate series*, not a strong reverter). Both confirms would
  pass a cohort Bonferroni FWER, but neither is admissible for the reasons above. The min-VR estimator itself is
  implemented correctly (replicated by hand).

## 5. Final Arm A verdict

**INCONCLUSIVE.** Precisely:

1. **The decisive question was never validly tested.** The pre-registered W=60 rolling-OLS-β-on-levels construction
   *manufactures* super-diffusion via β-update-noise (82–97 % of variance; proven on synthetic ground truth). The
   "both DECISIVE fail → premise seriously damaged" kill (doc 18 §5) **fired on contaminated evidence and does not
   stand.** The HDFC–ICICI / Gold–Silver MR question is **UNRESOLVED**, not answered negatively.
2. **No admissible confirmation exists** (0/7). USD/INR is a stale-quote artifact; WTI–Brent separates from a random
   walk but **not** from a volatility-clustering martingale (its sub-diffusion is largely vol clustering). The other
   five are construction-invalid.
3. **Therefore the deployment-domain MR premise is NEITHER confirmed NOR validly damaged.** This is *not* "material
   weakening" (the decisive test was invalid — a powerless test cannot weaken a premise by failing), and *not*
   "evidence for" (nothing admissible survives the RW+GARCH gauntlet). It is a **defective-instrument INCONCLUSIVE.**
4. **The load-bearing finding is methodological, not about the market:** *a causal time-varying hedge ratio
   manufactures spurious VR structure* — the hedge-ratio analogue of the doc-07 lag illusion, now demonstrated. The
   programme's binding bottleneck moves from *data* (resolved) to **construction (the β estimator).**

**Confidence:** that the rolling-β VR-inflation is a construction artifact — **HIGH** (synthetic ground truth +
ablation + two independent decompositions + monotone window-gradient). That no admissible cohort instrument
confirms — **HIGH** (post-GARCH-fix, surrogate-relative). That deployment MR is *absent* — **explicitly NOT claimed**
(the valid test was never run).

## 6. What this establishes · non-conclusions · next question

**Establishes (frozen-eligible):**
- Level-difference VR(q) + matched-surrogate (RW/GARCH/OU) machinery, causal and ground-truth-validated, exists and
  works (`analytics_arm_a.py`).
- **STRENGTHENED:** doc-13 HR-4 / doc-07 — a causal rolling/time-varying hedge ratio *manufactures* VR structure
  (β-update-noise); demonstrated at the β level. Rolling-OLS-β-on-levels with a short window is **inadmissible** for
  VR habitat tests on trending legs (it manufactures the measured property), by the programme's own "no construction
  artifact" standard (doc 18 §6).

**Explicit non-conclusions:** No claim that the deployment domain *is* or *is not* mean-reverting. No claim WTI–Brent
is/ isn't an MR habitat (it beats RW, fails GARCH — vol-entangled, unresolved). No detector/score/timing/State-T
object of any kind (frozen). USD/INR is a data-quality casualty, not a market read.

**Next high-information question / binding next action (a NEW pre-registration, not a silent re-run — freeze
discipline):** *Re-pre-register Arm A's construction* — replace the short rolling-OLS-β with a hedge ratio that does
not manufacture VR (candidates, to be adjudicated and frozen before results): (a) a **causal rolling-cointegration
(Engle–Granger) β** re-estimated on a long window with the β-update term explicitly controlled; (b) **VR on the legs**
where positive (NP-2) / a **causal log-spread** for strictly-positive pairs; (c) acquire **legs with synchronized
sub-bar data** to escape the level-trend domination. Then re-run the decisive instruments. Until a construction that
provably does not manufacture VR exists, Arm A's decisive question stays **open**.

---

*Markers: STRENGTHENED (HR-4 β-manufacturing) · UNRESOLVED (decisive pairs) · INADMISSIBLE (USD/INR) · KILLED-AS-
INVALID (the literal both-decisive-fail kill). Epistemic provenance preserved: the first-pass "weak–moderate evidence
FOR" thesis was corrected to INCONCLUSIVE by the GARCH-fix + adversarial committee. No history erased.*
