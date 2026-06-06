# Doc 47 — T2.5: Trend-Death Detector — Minimal First Test Results

**Document class:** Permanent AMR research record.
**Date:** 2026-06-06. **Mode:** Research — adversarial verification.
**Pre-registration:** `docs/research/t2_5_trend_death_prereg.md` (written BEFORE execution).
**Scripts:** `scripts/run_t2_5_trend_death.py`, `scripts/calibrate_habitat_score.py`.
**Data:** `data/processed/t2_5_trend_death_results.json`.
**Thesis tested:** Trend-death events precede mean-reverting forward windows more than chance.
**Formal verdict: NO_CONTENT** — pre-committed criteria fail unambiguously.

---

## Prior Belief

Central Track-2 thesis: when a rolling trend regression loses statistical strength (|t_β| dying) AND
the residual flips zero-crossing, the subsequent 40-bar window will be more sub-diffusive than chance.
This was operationalized as Stage-1 trend-death detection → forward min-VR permutation test.

Confidence prior: LOW-MEDIUM. The thesis is directionally intuitive but the operationalization was
untested and the instruments are trendy outrights — not obvious MR territory.

---

## Calibration Gate (passed before real-data use)

Habitat score (surrogate-relative min-VR) calibrated on synthetic ground truth:

| Process | Mean score | Criterion | Result |
|---|---|---|---|
| OU (theta=0.25) | 71.3 | ≥ 65 | PASS |
| RW (iid) | 49.2 | 35–65 | PASS |
| Trend (AR phi=0.70) | 17.2 | ≤ 65 | PASS |

Bug fixed during calibration: deterministic-slope trend + iid noise incorrectly appears
mean-reverting under VR with sample-mean correction (mean removal cancels slope → VR ≈ 1/q).
Corrected to momentum model (AR(1) positive increments). Score is well-behaved.

---

## Dataset

| Instrument | IS bars | IS period | OOS bars | Bars total |
|---|---|---|---|---|
| CL (crude, CL1! daily) | 6890 | 1987–2018 | 2954 | 9844 |
| SPX (daily) | 5854 | 1993–2018 | 2509 | 8363 |
| ADANIENT (daily) | 1724 | 2012–2019 | 739 | 2463 |
| AAPL (resampled from 60m) | 2008 | 2015–2022 | 861 | 2869 |

---

## IS Results — Primary Signal W=60

Test statistic: Δ_vr = mean(min-VR|all) − mean(min-VR|fire). Positive = fires more MR.

| Instrument | n_fire | fire_rate | Δ_vr | p_perm | fire_mvr | unc_mvr | hab@fire | verdict |
|---|---|---|---|---|---|---|---|---|
| CL | 1287 | 18.7% | +0.002 | 0.375 | 0.321 | 0.323 | 51.8 | miss |
| SPX | 1130 | 19.3% | **+0.016** | **0.003** | 0.278 | 0.293 | 54.1 | p-only |
| ADANIENT | 330 | 19.1% | -0.009 | 0.721 | 0.386 | 0.377 | 47.3 | miss |
| AAPL | 404 | 20.1% | **-0.043** | **1.000** | 0.378 | 0.336 | 43.9 | miss |

Pre-committed hit criteria: Δ_vr ≥ 0.10 AND p < 0.05. **Zero instruments hit on both criteria.**

---

## Full Results Grid (IS) — All W, All Variants

| Instrument | W | Variant | n_fire | Δ_vr | p_perm | verdict |
|---|---|---|---|---|---|---|
| CL | 60 | primary | 1287 | +0.002 | 0.375 | miss |
| CL | 60 | ablation | 2650 | -0.006 | 0.966 | miss |
| CL | 120 | primary | 1068 | +0.001 | 0.419 | miss |
| CL | 120 | ablation | 2946 | +0.009 | 0.004 | p-only |
| SPX | 60 | primary | 1130 | +0.016 | 0.003 | p-only |
| SPX | 60 | ablation | 2032 | +0.018 | 0.000 | p-only |
| SPX | 120 | primary | 760 | +0.013 | 0.040 | p-only |
| SPX | 120 | ablation | 1843 | +0.005 | 0.145 | miss |
| ADANIENT | 60 | primary | 330 | -0.009 | 0.721 | miss |
| ADANIENT | 60 | ablation | 788 | +0.003 | 0.377 | miss |
| ADANIENT | 120 | primary | 149 | -0.104 | 1.000 | miss |
| ADANIENT | 120 | ablation | 592 | +0.000 | 0.488 | miss |
| AAPL | 60 | primary | 404 | -0.043 | 1.000 | miss |
| AAPL | 60 | ablation | 806 | -0.030 | 1.000 | miss |
| AAPL | 120 | primary | 140 | +0.003 | 0.454 | miss |
| AAPL | 120 | ablation | 482 | +0.041 | 0.000 | p-only |

No cell achieves both criteria (p<0.05 AND Δ_vr≥0.10). Reported in full per pre-reg §6.

---

## Pre-Committed Programme Verdict

| Criterion | Required | Actual | Result |
|---|---|---|---|
| Full hits (p<0.05 AND Δ≥0.10) | ≥3/4 instruments | 0/4 | FAIL |
| Sign consistent (all Δ>0) | yes | NO (ADANIENT, AAPL negative) | FAIL |
| Pooled Bonferroni (min p < 0.0125) | yes | 0.003 < 0.0125 | PASS (irrelevant — other criteria fail) |

**VERDICT: NO_CONTENT.**

Per pre-reg §5: "Do NOT build Stage-2 on this operationalization."

---

## Four-Lens Adjudication

### Adversarial (kill-ledger)
Fire rate 18-20% = signal too permissive; firing 1-in-5 bars is not selective. AAPL/ADANIENT
negative Δ: structural trending instruments → trend-death detects pauses, not MR onsets. SPX
p=0.003 with Δ=0.016 is the high-N significance trap — true but inert. Residual flip (K_flip=10)
adds noise, not orthogonal information (zero-crossings are contemporaneous with slope death, not
predictive). **Verdict: this operationalization KILLED. Thesis not dead; signal needs redesign.**

### Statistical (audit)
Methodology valid (raw min-VR, permutation test, no leakage). Effect floor 0.10 ≡ 26-36% reduction
in baseline — retrospective note: this may be too strict for a conditional selector vs a pure MR
detector. BUT SPX's Δ=0.016 is 6× below the floor — the critique doesn't rescue the result. CL
genuine null (power adequate, MDE≈0.015, Δ=0.002 << MDE). Sign inconsistency (AAPL: z=-4.3)
is systematic, not noise — heterogeneity across instrument domains. Key confound: **unconditional
min-VR already <1 across all instruments** (CL=0.323, SPX=0.293) — conditional test must beat a
baseline that already has sub-diffusion baked in. **NO_CONTENT defensible.**

### Trader/PM
Fire rate 18-20% has no selectivity value (need <5%, preferably <2%). Thesis not killed, domain
is wrong: AAPL (growth equity) shows trend continuation post-fire. CL failure: either fires
mid-trend (wrong timing) or W=60 too short for supply/demand cycles to complete. **Track 2:
empirical probation.** Minimum bar for continuation: 2+ instruments with Δ_vr>0.05, p<0.01,
fire rate <5%. Instrument selection must improve before re-testing any operationalization.

### Independent re-implementation
Fire rate plausible (K_flip=10 stretches window). SPX arithmetic confirmed (z≈2.7, p≈0.003).
AAPL arithmetic confirmed (z≈-4.3, p≈1.000). Baseline unconditional sub-diffusion is a real
confound — conditional improvement must clear a non-trivial bar. **NO_CONTENT correct.**

---

## Synthesis: What This Test Found and Didn't Find

### What failed
This specific operationalization: |t_β| threshold approach, W=60, K_flip=10, on this instrument set.

**Root causes:**
1. **Signal too permissive.** 18-20% fire rate on 4 instruments means ~1-in-5 bars fires. No selective information content can emerge from near-uniform firing.
2. **Instrument domain mismatch.** AAPL (growth equity) and ADANIENT (strong trend equity) show anti-thesis behavior — trend-death followed by trend continuation, not reversion. The signal fires correctly on these but the thesis is wrong for their regime type.
3. **Effect size too small.** Even SPX's strongest result (Δ=0.016) is 6× below the pre-committed floor. No economically meaningful conditional improvement in forward MR habitat.
4. **Residual flip adds noise.** Ablation (slope-death only) is as good or better across most cells.

### What survives

1. **Habitat score as general tool.** Calibrated (OU=71.3, RW=49.2, trend=17.2). Reusable for other tests.
2. **Stage-1 architecture (rolling OLS, slope monitoring).** Not the wrong idea — wrong thresholds and instruments.
3. **Track 2 thesis.** Not falsified — untestable in this instrument set. A universal claim was pre-committed; what failed was the universal claim, not any specific instrument's conditional story (SPX Δ=+0.016 is locally positive, just not globally significant).
4. **Baseline sub-diffusion observation.** All instruments show unconditional min-VR < 1 (CL=0.323, SPX=0.293). This is interesting on its own and consistent with prior MR habitat work.
5. **SPX local signal.** Weak (Δ=0.016, p=0.003, well below effect floor) but consistently positive across W and variants. Not actionable alone; worth noting.

### What this does NOT kill
- The thesis that trend-death precedes MR (this instrument set is not the right test for the universal claim)
- Kalman μ* as a Stage-2 estimator (never tested here)
- LE-GF Track 1 harvest (unrelated)
- Future operationalizations with: (a) fire rate target <5%, (b) instruments with documented trend→MR cycles (NOT structural growth equities), (c) conditioning variables (vol regime, R²-crossover, CUSUM)

---

## Formal Findings

1. **NO_CONTENT — pre-committed, unconditional.** The t_β-based trend-death operationalization shows no cross-instrument content on this IS. Zero of four instruments hit both criteria; two show anti-thesis effects (AAPL, ADANIENT).

2. **Signal too permissive.** 18-20% fire rate is diagnostic of an overly-broad detection condition. Any redesign must target fire rate < 5%.

3. **SPX is the lone positive.** Δ=+0.016, p=0.003, locally significant across multiple W/variant combinations. Below effect floor but directionally consistent. Documents a weak local SPX signal for future reference. Does NOT change the programme verdict.

4. **Instrument domain lesson.** Structural trending equities (AAPL, ADANIENT) show trend continuation post-fire, not MR. The outright MR thesis applies to instruments with documented supply/demand or reversion cycles — not growth equities in bull regimes. Instrument selection must precede any redesign.

5. **Calibration bug documented.** Deterministic-slope trend model incorrectly appears mean-reverting under sample-mean-corrected VR. Corrected to momentum AR(1) model. The fix and its reason are now part of permanent programme memory.

6. **Effect floor retrospective.** Δ_vr ≥ 0.10 ≡ 26-36% reduction in baseline min-VR — a strict standard for a conditional selector. SPX at Δ=0.016 is genuinely small, so this note does NOT rescue the verdict. But the next pre-reg should calibrate the floor relative to baseline and expected economic magnitude.

---

## Pre-Reg Lesson (T2.5)

Effect floor (Δ_vr ≥ 0.10) must be set relative to baseline min-VR AND to economic significance,
not as an absolute scalar. When unconditional min-VR ≈ 0.30, Δ≥0.10 requires a 33% conditional
improvement — a very high bar. Future tests: compute expected effect size under a realistic model
before pre-committing the floor.

---

## Next Actions (per pre-reg §5 non-content branch)

1. **STOP: do not build Stage-2** (Kalman μ*) for trend-death signal as currently defined.
2. **Register the NO_CONTENT result** in HYPOTHESIS_REGISTRY with named reopen triggers.
3. **Pre-register separately** before any redesign. Two approved paths:
   - Path A: R²-crossover or recursive-residual CUSUM as Stage-1 (fire rate target <5%, different instruments)
   - Path B: Better instrument selection first (document which instruments have trend→MR cycles), then re-run T2.5 architecture
4. **Track 1 (LE-GF)** continues in background per plan.
5. **DO NOT proceed to T2.6** (discriminators) without T2.5 CONTENT verdict on a redesigned test.
