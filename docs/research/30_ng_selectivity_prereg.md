# Doc 30 — NG Calendar Selectivity: Pre-Registration

**Document class:** Permanent AMR pre-registration (FROZEN before any results).
**Status:** PRE-REGISTERED — do not modify after first script execution.
**Date:** 2026-06-04. **Builds on:** doc 23 (PERSISTENT-BUT-UNECONOMIC) · doc 25 §2/§5 (selectivity is
currently unsupported, low prior; binding test unrun).

> **What this freezes.** Every decision that could have been made post-hoc — thresholds, exit rule, max hold,
> cost, surrogate types, primary statistic, significance criterion, verdict rules — is committed here before
> a single result is observed. The test implementation may only read this document; it may never change it.

---

## 1. Scientific question

> *Does large-|z| NG calendar dislocation contain genuine incremental mean-reversion tradability, or is it
> statistically indistinguishable from the selection-on-deviation artifact that a zero-MR random walk
> produces when faded at extremes?*

Background: doc 23 found NG calendar storage MR is PERSISTENT (pooled mean-z = −0.627, p≈0.0002) but the
naive unconditional z-entry book is **break-even before cost** (gross +0.0004, cost 0.003). Doc 25 §2 ran an
exploratory (non-pre-registered) check at θ=2.0 and found NG gross = +0.0365 vs RW-null p95 = +0.047,
p≈0.11 — not distinguishable from the selection-on-deviation artifact. That check had N=300 surrogates, no
frozen protocol, and no jackknife. This document formalises the binding test.

**The selection-on-deviation mechanism:** a pure random walk faded whenever |z_t| > θ generates positive
gross expectancy by construction: the rolling z-score regresses toward zero simply because the rolling MEAN
drifts toward the current price as bars accumulate, regardless of any genuine mean reversion. This artifact
grows with θ. The surrogate-relative test measures whether real NG's gross at each θ exceeds what this
mechanical regression already produces.

---

## 2. Pre-registered parameters (frozen)

| Parameter | Value | Rationale |
|---|---|---|
| Instrument | `ng12_spread.csv` | NG M1-M2 vendor calendar (same as doc 23) |
| Date trim | 2006-07-28 | Frozen dense-era trim (doc 20) |
| Rolling z lookback | 60 bars | Consistent with doc 23 trade proxy; ~3-month causal window |
| **Thresholds θ** | {1.0, 1.5, 2.0, 2.5} | Full grid; ALL reported; NEVER argmax |
| **Primary statistic** | net expectancy at **θ=1.0** | Pre-committed; all higher θ are exploratory context only |
| Exit rule | z crosses 0 (via same rolling window) OR max_hold | Consistent causal reference throughout hold |
| **max_hold** | 40 bars | 2× the doc-23 global half-life of 12.9 bars (round up) |
| Primary cost | 0.003 | Conservative institutional round-trip |
| Cost grid | {0.0015, 0.003, 0.0045} | All reported; primary = 0.003 |
| Surrogate types | RW, GARCH(1,1), OU(φ=0.94771), Splice-RW | See §3 |
| N surrogates per type | 500 | Tighter than doc 25's N=300; resolves p≈0.1 to ±0.02 |
| RNG seed | 20260604 | Fixed; reproducible |
| OU φ | 0.94771 | exp(−ln2/12.9) = matched to doc-23 global half-life |
| Train period | ≤ 2017-12-31 | Approximately 11 years in-sample |
| OOS period | ≥ 2018-01-01 | ~8 years OOS (post-2018 is the fresh period) |
| Episode-jackknife | Drop largest single gross trade, recheck significance | Concentration-stability test |

> **Primary statistic is gross expectancy at θ=1.0.** This is the threshold at which the baseline doc-23
> result was measured (200 trades, gross = +0.0004). The surrogate comparison answers whether this gross
> is ABOVE or INSIDE the zero-MR null distribution. Net expectancy = gross − 0.003 determines deployability.

---

## 3. Surrogate protocol

Each surrogate type generates N=500 independent level paths of length = real NG, starting from level 0
(z-score normalization makes the starting level irrelevant). The SAME run_fade() function with IDENTICAL
parameters is applied to each surrogate path. The surrogate gross-expectancy distribution captures the
artifact that each null model would produce at each θ.

| Surrogate | Purpose | Generation |
|---|---|---|
| **RW** | Selection-on-deviation null (primary) | Gaussian iid increments matched to real NG mean + std |
| **GARCH(1,1)** | Vol-clustering selection null | GARCH with moment-matched α,β from squared-increment ACF |
| **OU(φ=0.94771)** | Genuine-MR benchmark | AR(1) with matched φ, σ calibrated to match increment std |
| **Splice-RW** | Back-adjustment artifact null | RW + periodic back-adj jumps at monthly cadence (21 bars, frac=0.25) |

**P-value definition:** p = (1 + #{surrogates with gross ≥ real_gross}) / (N + 1). One-sided. The test
question is whether real NG gross at each θ is *above* the surrogate distribution.

---

## 4. Verdict criteria (frozen)

Verdicts are determined solely by the primary statistic (θ=1.0, cost=0.003). Higher-θ and lower-cost
results are REPORTED but do not alter the primary verdict (exploratory only).

| Verdict | Trigger |
|---|---|
| **A — FALSE\_RESCUE** | p_rw(θ=1.0) ≥ 0.05; NG selectivity indistinguishable from artifact |
| **B — GENUINE\_SUBCOST** | p_rw(θ=1.0) < 0.05 AND net(θ=1.0) ≤ 0 |
| **C — GENUINE\_ECONOMIC** | p_rw(θ=1.0) < 0.05 AND net(θ=1.0) > 0, stable to jackknife and OOS |
| **D — INCONCLUSIVE** | Primary evidence unstable: jackknife collapses significance (gross drops >50%) OR OOS direction reverses |

**Verdict hierarchy note:** if higher-θ exploratory results are significant but primary is not, the verdict
is A or D (not C). The primary statistic was frozen BEFORE observing any result.

**INCONCLUSIVE upgrade:** if primary p_rw < 0.05 and net > 0 but jackknife drops gross by >50% or OOS is
sign-negative, verdict is D not C.

---

## 5. Non-conclusions pre-committed

Regardless of outcome, this test does NOT establish:
- Cross-habitat replication (NG only)
- OOS selectivity at θ > primary threshold (exploratory only)
- Any ex-ante regime filter (unconditional selectivity test only)
- Any portfolio-level claim (single instrument)
