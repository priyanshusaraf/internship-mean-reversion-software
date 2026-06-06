# Doc 37 — Crack-Spread Controlled-β: Synthetic Calibration Gate Results

**Document class:** Permanent AMR research record (institutional memory).
**Date:** 2026-06-05. **Mode:** Controlled Implementation — synthetic only (NO real data touched).
**Pre-registration:** `crack_beta_execution_prereg.md` (frozen 2026-06-05).
**Extends:** doc 30 (Cycle-2 specification). **Data:** `data/processed/crack_beta_synthetic_gate.json`.
**Status:** GATE PASSED FOR F6+F5 — cleared for real-data execution next session.

---

## Prior Belief

Per doc 30 §4 hierarchy: F1 (Kalman) > F2 (Ridge) > F3 (long-window OLS) was the prior expectation.
Updated by user instruction to F6 > F5 > F1 > F3 > F2 (prefer frozen-β families).
Prior probability of ≥1 family passing all synthetic controls: MEDIUM (~50%).

---

## Synthetic Controls Used

| Control | Generating process | Expected result |
|---|---|---|
| P (positive control) | A=β*×B+OU, B=trending RW, φ=0.95, n=5000 | Family CONFIRMS (VR<0.80, p_rw<0.05) |
| Z1 (martingale) | A=1.0×B+RW, B=trending | VR(20) ∈ [0.80, 1.20], f_βupdate < 0.10 |
| Z2 (stress null) | A=1.0×B+RW, B=STRONGLY trending (drift×10) | VR(20) ∈ [0.80, 1.20], f_βupdate < 0.10 |
| Z3 (independent) | A, B = independent RWs | No false cointegration |

All: n=5000, N_draws=200, seed=20260604.

---

## Gate Results (Full Matrix)

### F6 — Economic Anchor (β = 1.0, frozen) — **ADMISSIBLE** ✓

| Control | VR(20) | p_rw | f_βupdate | In band? | Result |
|---|---|---|---|---|---|
| P positive control | 0.6423 | 0.005 | 0.000 | — | ✓ CONFIRMS (VR<0.80) |
| Z1 martingale | 1.0564 | 0.861 | 0.000 | ✓ YES | ✓ NULLS |
| Z2 stress null | 0.9701 | 0.473 | 0.000 | ✓ YES | ✓ NULLS |
| Z3 independent | 1.1590 | 0.781 | 0.000 | ✓ YES | ✓ NULLS |

P=PASS, N=PASS, M=PASS → **ADMISSIBLE.** Zero f_βupdate throughout (definitionally so).

### F5 — Pre-sample OLS (β estimated on first 25%, then frozen) — **ADMISSIBLE** ✓

| Control | VR(20) | p_rw | f_βupdate | In band? | Result |
|---|---|---|---|---|---|
| P positive control | 0.6101 | 0.005 | 0.000 | — | ✓ CONFIRMS |
| Z1 martingale | 1.0202 | 0.517 | 0.000 | ✓ YES | ✓ NULLS |
| Z2 stress null | 0.9272 | 0.259 | 0.000 | ✓ YES | ✓ NULLS |
| Z3 independent | 0.9118 | 0.169 | 0.000 | ✓ YES | ✓ NULLS |

P=PASS, N=PASS, M=PASS → **ADMISSIBLE.** Once β is frozen post-pre-sample, no update noise.
Z3 VR=0.912 approaches the lower band (0.80) — monitor on real data but within the frozen band.

### F1 — Kalman β (q_beta=0.0001) — **INADMISSIBLE** ✗

| Control | VR(20) | p_rw | f_βupdate | In band? | Result |
|---|---|---|---|---|---|
| P positive control | 0.0578 | 0.005 | 0.459 | — | False confirm (over-fit) |
| Z1 martingale | **0.1427** | **0.005** | 0.386 | **✗ NO** | **FALSE POSITIVE** |
| Z2 stress null | **0.0501** | **0.005** | 0.487 | **✗ NO** | **CATASTROPHIC** |
| Z3 independent | 0.3367 | 0.005 | 0.149 | **✗ NO** | False positive |

**N=FAIL, M=FAIL** → INADMISSIBLE. Even with q_beta=0.0001, the Kalman β over-absorbs OU dynamics
into the β estimate AND generates f_βupdate=0.39-0.49. The Z2 stress null (VR=0.050!) is
catastrophically false — the Kalman tracks the OU as β variation, creating extreme apparent MR
even on non-MR synthetic data. This confirms the doc-19 mechanism fires with any updating β.

### F3 — Long-window OLS (W=500) — **INADMISSIBLE** ✗

| Control | VR(20) | p_rw | f_βupdate | In band? | Result |
|---|---|---|---|---|---|
| P positive control | **2.6458** | 1.000 | 0.156 | — | **FAILS TO CONFIRM** |
| Z1 martingale | **7.6018** | 1.000 | 0.485 | **✗ NO** | Extreme super-diffusion |
| Z2 stress null | **11.3635** | 1.000 | 0.635 | **✗ NO** | Catastrophic super-diffusion |
| Z3 independent | **3.7916** | 1.000 | 0.181 | **✗ NO** | Extreme super-diffusion |

**P=FAIL, N=FAIL, M=FAIL** → INADMISSIBLE. Long-window OLS WORSENS the artifact, not reduces it.
With strongly trending B (cumulative level), even slow β updates produce large f_βupdate because
B_{t-1} is enormous. W=500 is WORSE than W=60 on trending legs. The prior assumption "long window
= less artifact" is FALSIFIED by the synthetic gate.

### F2 — Ridge β (λ=10, W=126, target=1.0) — **INADMISSIBLE** ✗

| Control | VR(20) | p_rw | f_βupdate | In band? | Result |
|---|---|---|---|---|---|
| P positive control | 0.6443 | 0.005 | 0.001 | — | ✓ Confirms (barely) |
| Z1 martingale | 1.0272 | 0.677 | 0.001 | ✓ YES | ✓ NULLS |
| Z2 stress null | **11.6772** | 1.000 | **0.745** | **✗ NO** | **CATASTROPHIC** |
| Z3 independent | 1.0894 | 0.458 | 0.000 | ✓ YES | ✓ NULLS |

**N=FAIL (Z2), M=FAIL (Z2)** → INADMISSIBLE. Ridge works on Z1 (moderate trending B) but
CATASTROPHICALLY fails on Z2 (strongly trending B). The f_βupdate=0.745 on Z2 is actually
worse than F3, confirming that the shorter window × strong trend creates β-update × large B
that dominates the spread variance. Ridge shrinkage toward 1.0 does not save it from Z2.

---

## Key Findings (Non-Obvious, Durable)

**Finding 1 — ONLY FROZEN β IS ADMISSIBLE:**
Any β that updates during the test period fails the Z2 stress null when B is strongly trending.
The doc-19 mechanism: (β_{t-1}-β_{t-2})×B_{t-1} is large even with tiny β changes when B
accumulates to a large level over time. The ONLY safe strategy is to freeze β before the test.

**Finding 2 — LONG WINDOW WORSENS, NOT HELPS:**
Prior assumption: large W → slow β update → less artifact. FALSIFIED. On trending legs,
large W means large B_{t-1} when the β changes — so the product is larger, not smaller.
W=500 on the stress null gives VR=11.36 vs W=60 in doc-19 giving VR≈6. WORSE.

**Finding 3 — KALMAN OVERABSORBS OU:**
Kalman with q_beta=0.0001 produces VR=0.058 on the positive control (genuine OU = 0.642 for F6).
The Kalman "explains" the OU deviation as β variation, removing it from the spread and producing
extreme false sub-diffusion. The f_βupdate=0.46 confirms this is absorption, not artifact.
This makes Kalman inadmissible by BOTH N (false confirms on Z1/Z2/Z3) and M (f_βupdate >> τ).

**Finding 4 — PRE-SAMPLE OLS IS THE SCIENTIFIC CONTRIBUTION OF CYCLE 2:**
F5 cleanly separates the legitimate use of β estimation (learn the relationship pre-sample, apply
post-sample with zero update noise) from the illegitimate use (update β during the test period).
This is the admissible non-trivial family. If F5 confirms on HO2!-CL2! real data, it opens a
new class of spread construction: estimated-once, applied-frozen spreads across asset pairs
where the cointegrating relationship is stable enough to be learned pre-sample.

---

## Gate Verdict

```
GATE VERDICT: CLEARED_FOR_REAL_DATA
ADMISSIBLE FAMILIES: F6 (economic anchor, β=1.0), F5 (pre-sample OLS, β frozen post-25%)
INADMISSIBLE FAMILIES: F1 (Kalman), F3 (long-window OLS), F2 (Ridge)
```

**F6 is the baseline (equivalent to β=1 definitional). The scientific question is whether F5 confirms on real HO2!-CL2! data.**

**Permanent demotion NOT triggered:** F6 confirms the positive control, proving the apparatus can see genuine OU. The inadmissible families fail N/M, not P — this is the "estimator problem, not apparatus problem" condition from doc 30 §2.6. Demotion requires ALL families to fail P AND N simultaneously — that condition is NOT met.

---

## Next Action

**Execute F5 and F6 on real HO2!-CL2! data (next session):**
- Load both legs (confirmed available: HO2! 7,006 bars 1998-2026; CL2! 9,230 bars 1989-2026)
- Normalize: A_barrel = HO2! × 42, B_barrel = CL2!
- F6: β=1.0; F5: OLS on first 25% of data (pre-2003 approximately), then frozen
- Run evaluate_v2 equivalent with construction-controlled corroboration check
- Report f_βupdate on real data as a sanity check (should be 0.000 for both F5 and F6)

**Do NOT test F1, F3, or F2 on real data** (inadmissible by synthetic gate; zombie prohibition applies).

---

*Append-only. Synthetic gate results locked. No real HO2!/CL2! data was read at any point in this session.*
