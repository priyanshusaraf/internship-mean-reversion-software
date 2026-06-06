# T2.5 — Trend-Death Detector: Frozen Pre-Registration

**Written:** 2026-06-06. **Status:** FROZEN BEFORE EXECUTION.
**Motivation:** First test of the central outright mission thesis: trend-death precedes mean
reversion in trendy outright markets. Gate 0 (doc 46) passed; Track-2 authorized.
**Calibration:** Habitat score passed synthetic gate (OU=71.3, RW=49.2, trend=17.2).

---

## 1. Thesis Being Tested

At each bar t, using only data ≤ t: detect when a rolling trend is "dying." Does a trend-death
event fire BEFORE a subsequent mean-reverting regime more often than chance?

This is a **present-tense model-adequacy observation** — NOT a predictive MR classifier, NOT
State T, NOT the forbidden transition-prediction object (doc 24). The signal observes that the
trend regression is losing fit; it does not predict what comes next. Forward evaluation is for
scoring only, never for signal construction.

---

## 2. Stage-1 Signal — Trend-Death Detector (causal, pre-committed)

At bar t, using only data ≤ t, fit a rolling OLS linear regression of log(price) on time over
window W. Obtain slope β̂_t, its t-statistic t_β, and residuals e_s.

**Primary window (pre-committed):** W = 60 bars.
**Robustness window (pre-committed):** W = 120 bars.
Both are reported. Primary verdict = W=60.

### Primary fire condition (both required)

**Condition 1 — Slope death:**
The trend was "established" (|t_β| ≥ 2.0 sustained for all of the prior W bars, i.e. at the
beginning of the current window), AND now |t_β| has dropped below 0.5 OR β̂_t has changed sign
from the established direction.

Implementation:
```
established = |t_β[t - W]| ≥ 2.0   (i.e. W bars ago, trend was established)
dying       = |t_β[t]| < 0.5  OR  sign(β̂_t) ≠ sign(β̂_{t-W})
fire_cond1  = established AND dying
```

**Condition 2 — Residual flip:**
At least one zero-crossing of the residuals e_s in the trailing k=10 bars (price is no longer
departing one-sidedly from the trend line).
```
fire_cond2 = any sign change in e_s[t-k+1 : t+1]  (k=10)
```

**Primary fire:** fire_cond1 AND fire_cond2.

### Ablation (pre-registered; reported alongside, never cherry-picked)

**Condition 1 only (slope-death only):** fire_cond1 alone, without requiring residual flip.
This isolates the marginal value of the residual-flip confirmation.

### No tuning: the following are FROZEN and must NOT be optimized after results are seen:

```
W_primary           = 60
W_robustness        = 120
t_stat_establish    = 2.0     (standard: ~95% CI for slope)
t_stat_dying        = 0.5     (near-zero significance)
k_flip              = 10      (trailing bars for residual zero-crossing)
```

---

## 3. Evaluator — Surrogate-Relative MR Habitat Score

### 3.1 Definition (calibrated above)

On a forward price window of H=40 bars starting at t+1:
1. Compute min VR over q ∈ {5, 10, 20} (lower = more sub-diffusive).
2. Build matched nulls from the window's own increments:
   - Null 1: RW (iid, vol-matched, n_null=1000)
   - Null 2: MA(1) (moment-estimated from window increments, same vol, n_null=1000)
3. Habitat score = fraction of null min-VRs ≥ real min-VR, mapped to 0–100.
   (High = more reverting than null.)

Score is NEVER self-ranked against the instrument's own history.

### 3.2 Parameters (frozen)

```
H                   = 40    # forward window length (bars)
VR_QS               = [5, 10, 20]
NS_NULL             = 2000  # surrogates per score evaluation
```

---

## 4. Forward Scoring + Baselines

For each fire at bar t:
- Take forward window x[t+1 : t+1+H] (evaluation only; never feeds signal)
- Compute habitat score and raw min-VR on forward window

Compare the distribution of post-fire habitat scores against:

**(a) Unconditional base rate:** habitat score at ALL eligible bars (bars with ≥ W+H valid
history, excluding the IS/OOS buffer). Eligibility: bar is in sample, not within W of the
start, not within H of the end.

**(b) Permutation null:** randomly relocate the SAME NUMBER of fire-labels across eligible
bars, recompute the post-"fire" habitat score distribution; repeat N_PERM=2000 times.
This null is automatically matched to each instrument's own dynamics.

**Test statistic:** Δ = mean(habitat | fire) − mean(habitat | permuted-fire)
**H1:** Δ > 0 (fires are followed by more MR habitat than chance).
**p-value:** fraction of permutation-null Δ values ≥ observed Δ.

---

## 5. Pre-Committed Pass / Fail

### Per-instrument "hit" (BOTH required)
1. Permutation p < 0.05 (one-sided, Δ > 0)
2. Effect-size floor: post-fire mean forward min-VR at least 0.10 LOWER than the
   permutation-null mean forward min-VR. (Significant-but-trivial does not count.)

### Programme-level verdict

**CONTENT:** hits on a MAJORITY (≥3/4) of instruments with CONSISTENT SIGN (all positive Δ),
AND pooled permutation test is significant after Bonferroni correction across instruments
(p < 0.05 / n_instruments = p < 0.0125 for 4 instruments).

**NO CONTENT:** otherwise. Then the trend-death trigger as operationalized has no predictive
content. Do NOT build Stage-2 on this operationalization. Revisit (e.g. R²-crossover or
CUSUM — pre-register separately) or re-examine the thesis.

The habitat score and Kalman μ* survive as general tools regardless; only the trigger is in
question.

---

## 6. IS / OOS, Multiplicity, Data

### IS / OOS split (pre-committed)
IS: first 70% of each instrument's bars (by count, not by date, to avoid look-ahead).
OOS: last 30%.
Primary verdict = IS. OOS reported as out-of-sample confirmation.
(Doc-45 lesson: any gating statistic must be computed IS-only.)

### Multiplicity (Bonferroni)
Full grid reported, not just the best cell:
- 4 instruments × {primary, ablation} × {W=60, W=120} = 16 combinations
- Programme-level verdict applies Bonferroni: p < 0.05 / 4 = 0.0125 per instrument

### Instruments (pre-committed, owner may override BEFORE this line)

| Instrument | File | Type | History |
|---|---|---|---|
| CL (crude, outright) | NYMEX_DL_CL1!, 1D.csv | commodity outright | ~39y |
| SPX | SP_SPX, 1D (1).csv | equity index | ~33y |
| ADANIENT | data/raw/adanient.csv | equity outright | ~10y |
| AAPL | data/raw/aapl_60.csv → resampled to daily | equity outright | ~10y (2015-2025) |

Pass one is PRICE-ONLY. Volume enters later (T2.6) if T2.5 shows CONTENT.
Log-price is the input to Stage-1 (log regression of price on time).

### Causal firewall
Signal at t uses only data ≤ t (rolling window, causal OLS).
Forward windows x[t+1 : t+1+H] are for EVALUATION ONLY and never feed the signal.

---

## 7. Frozen Parameters (cannot change after this line)

```python
SEED_T25        = 20260606
W_PRIMARY       = 60
W_ROBUST        = 120
T_STAT_ESTABLISH = 2.0
T_STAT_DYING    = 0.5
K_FLIP          = 10
H_FORWARD       = 40
VR_QS           = [5, 10, 20]
NS_NULL_SCORE   = 2000
N_PERM          = 2000
OOS_SPLIT       = 0.70
MIN_BARS        = 500      # minimum bars for an instrument to be included
EFFECT_FLOOR    = 0.10     # min-VR difference for hit (effect-size floor)
P_HIT           = 0.05     # per-instrument p threshold
P_PROGRAMME     = 0.0125   # Bonferroni-corrected (0.05/4 instruments)
MAJORITY_N      = 3        # must hit at least this many instruments (of 4)
```

---

## 8. Non-Goals (frozen)

- No Stage-2 (Kalman μ*) in this test — forward scoring is raw price window habitat
- No volume, no OI, no COT data
- No threshold optimization
- No sub-period cherry-picking
- No "it almost hit" reasoning — pre-committed criteria bind
- No deployment or execution logic
- This test does NOT determine whether trend-death MR is deployable — only whether the signal has empirical content
