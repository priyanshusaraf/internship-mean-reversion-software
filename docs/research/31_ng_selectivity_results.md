# Doc 31 — NG Calendar Selectivity Test: Results & Verdict

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** COMPLETE — binding verdict (Research Mode).
**Date:** 2026-06-04. **Pre-registration:** doc 30 (frozen before execution). **Builds on:** doc 23
(PERSISTENT-BUT-UNECONOMIC) · doc 25 §2/§5 (selectivity unsupported, low prior; binding test unrun).
**Engine:** `scripts/run_selectivity_test.py` · **Results:** `data/processed/ng_selectivity_results.json`.
Confidence = trustworthiness-of-evidence.

> **Verdict: `A_FALSE_RESCUE` — SELECTIVITY DIRECTION KILLED.**
> NG calendar high-|z| entry selectivity is **statistically indistinguishable from the selection-on-deviation
> artifact** at the pre-registered primary threshold (θ=1.0, p_rw=0.551). The apparent improvement in gross
> expectancy at θ=2.0/2.5 is driven by a **single trade** (+2.923 gross) that disappears under episode-jackknife
> (gross collapses from +0.0068/+0.0086 to −0.0301/−0.0400). **The selectivity lever cannot rescue NG's
> economic gap and is therefore CLOSED as a standalone direction.**

---

## 1. Test execution

- **Instrument:** ng12_spread.csv, 4969 bars (2006-07-28 → 2026-04-15).
- **Protocol:** exactly as pre-registered (doc 30): θ∈{1.0,1.5,2.0,2.5}, lookback=60, max_hold=40, cost=0.003,
  N=500 surrogates per type (RW, GARCH, OU(φ=0.948), Splice-RW), seed=20260604, train=≤2017, OOS=≥2018.
- **Primary statistic:** gross expectancy at θ=1.0. All higher thresholds exploratory.
- **Model fits:** mu_incr=0.00002, σ_incr=0.077; GARCH α=0.005, β=0.030; OU φ=0.948 (pre-committed).

---

## 2. Full results grid

### 2.1 Per-threshold real NG statistics (full sample, cost=0.003)

| θ | n trades | gross | net | hit | avg_hold | top3_gross% |
|---|---|---|---|---|---|---|
| **1.0** (primary) | 149 | **−0.0006** | −0.0036 | 0.61 | 24.7 | 0.12 |
| 1.5 | 114 | −0.0035 | −0.0065 | 0.54 | 27.7 | 0.19 |
| 2.0 | 80 | **+0.0068** | **+0.0038** | 0.54 | 29.1 | 0.26 |
| 2.5 | 61 | **+0.0086** | **+0.0056** | 0.57 | 28.2 | 0.28 |

Note: θ=2.0 and 2.5 show **positive net returns after 0.003 cost.** See §2.3 and §2.4 for why this is
illusory — both are jackknife-unstable and p_rw ≈ 0.45, inside the RW null distribution.

### 2.2 Surrogate-relative p-values (one-sided; p < 0.05 required for significance)

| θ | p_rw | p_garch | p_ou | p_splice |
|---|---|---|---|---|
| **1.0** (primary) | **0.551** | 0.559 | **1.000** | 0.998 |
| 1.5 | **0.575** | 0.597 | **1.000** | 0.998 |
| 2.0 | **0.417** | 0.447 | **1.000** | 0.996 |
| 2.5 | **0.461** | 0.439 | **1.000** | 0.988 |

**No threshold is significant (p_rw < 0.05) at any surrogate type.**

### 2.3 RW null distribution (gross expectancy percentiles)

| θ | p5 | p25 | median | p75 | p95 | **NG real** |
|---|---|---|---|---|---|---|
| 1.0 | −0.043 | −0.018 | +0.003 | +0.018 | +0.040 | **−0.0006** |
| 1.5 | −0.057 | −0.026 | +0.001 | +0.023 | +0.051 | **−0.0035** |
| 2.0 | −0.068 | −0.029 | −0.0004 | +0.026 | **+0.062** | **+0.0068** |
| 2.5 | −0.089 | −0.034 | +0.003 | +0.034 | **+0.081** | **+0.0086** |

At θ=2.5 the RW null *median* is +0.003 and *p95* is +0.081. NG at +0.0086 sits near the **46th percentile**
of the RW distribution — slightly above the RW median. This is not an edge; it is noise.

---

## 3. Episode-jackknife — single-trade analysis

Drop the largest-|gross| single trade; recompute statistics.

| θ | full gross | jk gross | gross drop | largest trade |
|---|---|---|---|---|
| 1.0 | −0.0006 | +0.0098 | −1826% | **−1.533 gross** (single large loser) |
| 1.5 | −0.0035 | +0.0229 | −744% | **−2.987 gross** (same class) |
| 2.0 | +0.0068 | **−0.0301** | **+543%** | **+2.923 gross** (ONE winning trade) |
| 2.5 | +0.0086 | **−0.0400** | **+567%** | **+2.923 gross** (SAME single trade) |

**The entire positive gross at θ=2.0 and θ=2.5 is produced by one trade (+2.923 gross).** Removing it
flips the result from positive to deeply negative (−0.030/−0.040). Jackknife drop >500% = **catastrophically
unstable.** The pre-registered verdict rule (>50% drop → INCONCLUSIVE) would apply if primary were
significant; it is not, so the verdict remains A_FALSE_RESCUE.

**The single dominating trade** is almost certainly a crisis-period NG dislocation that reversed sharply
(consistent with the doc-23 finding that shock periods show slightly better MR, and with the +2.923 magnitude
relative to NG's typical day increments of σ=0.077).

**At θ=1.0:** the jackknife *improves* the result (−0.0006 → +0.0098) because the dominant trade is a large
loser (−1.533). At this threshold, the result is contaminated in both directions by extreme individual events.

---

## 4. OOS split (post-2018, n=61/45/32/27 trades)

| θ | full gross | OOS gross | OOS net | OOS n |
|---|---|---|---|---|
| 1.0 | −0.0006 | **+0.0046** | **+0.0016** | 61 |
| 1.5 | −0.0035 | **+0.0081** | **+0.0051** | 45 |
| 2.0 | +0.0068 | **+0.0059** | **+0.0029** | 32 |
| 2.5 | +0.0086 | **+0.0053** | **+0.0023** | 27 |

OOS directionally positive at all thresholds. **This is the only mildly favourable signal** — OOS
does not sign-reverse. However: (a) OOS n is 27–61 trades with gross ≈ 0.003–0.008, i.e. 1–2.5 standard
errors from zero at typical σ per trade; (b) the full-sample result is not significant; (c) OOS positivity
does not change the primary verdict (which is determined by full-sample p_rw); (d) the same one-trade
concentration could exist in the OOS sub-period. The OOS result is **noted as a soft observation** — it
does not reopen the selectivity direction, which requires a new pre-registration.

---

## 5. OU comparison — the decisive qualitative reading

**p_ou = 1.000 at ALL thresholds.** Every OU surrogate with φ=0.948 (matched to NG's own half-life) produces
higher gross than real NG at every threshold. Real NG's measured selectivity is **weaker than expected from a
stable AR(1) process with its own documented half-life.** This is not a failure of the test — it is a
structurally important result:

> NG has genuine MR (confirmed, VR=0.448 at q=20, p=0.005 vs RW). But the MR is **regime-conditional** — it
> switches off in the 5 glut years (2009, 2012, 2017, 2020, 2025; VR→1, half-life→27). An unconditional
> z-entry strategy that ignores this regime structure enters positions in glut years (where the "MR" is absent),
> producing large losers that overwhelm the gains from on-years. A stable OU process (which has no glut-year
> breaks) shows far better unconditional selectivity than real NG.

This explains all three phenomena simultaneously: (a) genuine MR in VR(q) test; (b) sub-cost naive book;
(c) selectivity gradient does not beat RW. The mechanism is not "NG lacks MR" — it is "the MR is conditional
on regime, and unconditional selective entry does not exploit it."

**Implication:** the only way to recover selectivity is via a CAUSAL regime classifier that identifies non-glut
years in real-time. That is precisely the State-T-adjacent timing object this programme killed (doc 24). There
is no admissible path from here to selective deployment without signed order-flow or a causal inventory
variable.

---

## 6. Splice null — back-adjustment reading

**p_splice = 0.988–0.998 at all thresholds.** Real NG sits in the *bottom* 0.2–1.2% of the splice-RW
distribution. The splice-RW (with periodic back-adjustment jumps at monthly cadence) produces **far more
apparent gross selectivity** than real NG. This means: vendor back-adjustment does not *create* NG's apparent
selectivity (which would place NG in the UPPER tail of splice). The splice null overstates the back-adjustment
effect relative to NG. The regime-conditionality interpretation (genuine storage MR) remains the more
parsimonious explanation for NG's persistence evidence.

---

## 7. Verdict: `A_FALSE_RESCUE` — SELECTIVITY DIRECTION KILLED

| Criterion | Result |
|---|---|
| p_rw < 0.05 at θ=1.0 (primary) | **FAIL** (p=0.551) |
| Net > 0 at θ=1.0 | FAIL (net=−0.0036) |
| Jackknife stable at any sig. θ | FAIL (>500% drop) |
| Surrogate-relative significance at any θ | **FAIL** (range 0.42–0.58) |
| OOS positive direction | PASS (mildly) |
| OU beaten at any θ | **FAIL** (p_ou=1.000 everywhere) |

**The selectivity lever (↑gross by raising θ) is CLOSED.** It is not merely unproven; the 500-surrogate
test with episode-jackknife demonstrates it is mechanically non-different from what a zero-MR random walk
produces. The apparent gradient (doc 25 §2 exploratory finding) is confirmed as an artifact.

**Epistemic status update (doc 25 §2 downgraded):**
- PRIOR: LOW that selectivity survives surrogate-relative test (stated in doc 25)
- POSTERIOR: **FALSIFIED as standalone direction** — NG tail selectivity does not survive the binding
  pre-registered surrogate test

**What this does NOT kill:**
- The VR-based persistence evidence (doc 21/23 — confirmed by a different apparatus)
- The genuine storage MR interpretation (regime-conditionality evidence from doc 23 §Q3)
- Future instruments with better gross/cost ratios (portfolio direction, requires new data)
- A causal inventory-based conditional entry (requires non-financial data, not tested here)

---

## 8. Strategic consequence for doc 25 routing

Doc 25 identified a **strictly-ordered gate sequence:**

```
Gate 1 → NG selectivity surrogate test (this doc: FAILED → CLOSED)
Gate 0/2 → Cycle-2 controlled-β cohort breadth (KEYSTONE — now the ONLY open gate)
Gate 3 → book-level cost test (after ≥2 positive-expectancy instruments)
```

Gate 1 has now been run and **failed.** The selectivity lever — the only single-instrument expectancy-improvement
path — is closed. This confirms doc 25's earlier topology: **the binding bottleneck is cohort breadth
(Cycle-2 controlled-β), not selectivity.** The route to deployable MR requires instruments with *inherently*
higher gross/cost ratios, not a smarter entry rule on NG.

---

## 9. Confidence / non-conclusions / next question

**Confidence:** HIGH that NG unconditional selectivity does not beat the RW surrogate (N=500, stable protocol,
consistent across cost grid); HIGH that the apparent high-θ edge is one-trade concentrated; MEDIUM that
regime-conditionality is the mechanism (most parsimonious; direct test would require causal inventory data).

**Explicit non-conclusions:** (a) NOT "NG has no MR" — the VR test is a different apparatus and remains;
(b) NOT "all calendar selectivity is an artifact" — other instruments untested; (c) NOT "conditional
selective entry is impossible" — ruled out for UNCONDITIONAL z-entry only; (d) NOT a cross-habitat statement.

**Next high-information question:** the gate is now solely on Cycle-2 controlled-β — finding a second
instrument where *gross is inherently above cost* (not dependent on entry-rule refinement). Data acquisition
(BRN2! 1D, ZC2! 1D) is the binding action.

---

*Markers: FALSIFIED (NG unconditional selectivity as standalone direction — A_FALSE_RESCUE) ·
CONFIRMED (one-trade concentration hypothesis, consistent with doc 25 §2) · STRENGTHENED (OU>NG finding:
MR is regime-conditional, not structurally absent) · NOTED (OOS positivity as soft observation, non-binding).*
