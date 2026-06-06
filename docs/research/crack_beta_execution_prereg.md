# Crack-Spread Controlled-β — Execution Pre-Registration

**Document class:** Permanent AMR pre-registration (frozen before any result, extending doc 30).
**Date:** 2026-06-05. **Status:** FROZEN — no redesign after this line.
**Extends:** doc 30 (Cycle-2 specification); inherits all protocol invariants verbatim.
**Mode:** Controlled Implementation (§3). **NO real data touched in this session.**

> **Objective:** determine whether an admissible causal β-construction exists for the HO2!-CL2!
> crack spread that (P) preserves genuine cointegrated OU reversion AND (N+M) does NOT manufacture
> VR from the doc-19 β-update-noise mechanism. This is a CONSTRUCTION VALIDITY question, not a
> trading signal. Doc 30 §1.1 mechanism must be defeated on synthetic controls FIRST.

---

## §A. Pre-committed Pair (FROZEN)

**Pair:** A = NYMEX Heating Oil #2 continuous (HO2!), B = NYMEX WTI Crude Oil continuous (CL2!)

**Normalization (FROZEN):** Both legs normalized to USD/barrel before β estimation:
```
A_barrel_t = HO2!_close_t × 42.0    [42 gallons per barrel — physical constant, not estimated]
B_barrel_t = CL2!_close_t            [already in USD/barrel]
```
After normalization, β ≈ 1.0 in barrel-equivalent terms. The crack margin deviation from β=1.0
is the genuine estimation challenge. All β families estimate around this normalization.

**Literature anchor (§11.8 gate):** Pindyck & Rotemberg (1990) demonstrate crude/product cointegration in US energy markets. Routledge, Seppi & Spatt (2000) model the convenience yield and storage relationships creating cointegration in refinery input/output pairs. The HO-CL relationship is a textbook cointegrated pair with documented MR in the academic storage MR literature.

**Data:** `NYMEX_DL_HO2!, 1D.csv` and `NYMEX_DL_CL2!, 1D.csv` from `data/raw/more-mean-reversion-data/`.

**Date range (FROZEN):**
```
DATE_MIN = 1998-07-19   [first date both legs available; RB2! arrives here — consistent]
DATE_MAX = 2026-06-03
OOS_SPLIT = 0.70       [first 70% = synthetic calibration reference; last 30% = OOS]
```

---

## §B. β-Family Set and Frozen Hyperparameters

**Hierarchy (FROZEN, per user instruction):** F6 > F5 > F1 > F3 > F2

The hierarchy reflects decreasing β-update DOF: families with zero or near-zero β-update noise
during the test period are most admissible per the doc-19 mechanism.

| Family | Name | Construction | Frozen hyperparameters | β-update DOF |
|---|---|---|---|---|
| **F6** | Economic anchor (fixed) | β = 1.0 (barrel-equivalent normalization is the anchor; spread = A_barrel − 1.0×B_barrel = crack margin at parity) | β FIXED at 1.0; zero updates | ZERO — definitionally admissible benchmark |
| **F5** | Pre-sample OLS (frozen point estimate) | OLS β on FIRST 25% of data (pre-sample), then FROZEN for the remaining 75% | pre_sample_fraction = 0.25; β_hat frozen post-pre-sample; no updates during test | ZERO (during test period) |
| **F1** | Kalman / slow-drift β | Random-walk-β state space, very small process noise | q_beta = 0.0001 (frozen; tiny process noise variance); σ_obs estimated from pre-sample residuals | VERY LOW |
| **F3** | Long-window causal OLS | causal_rolling_beta at frozen large W; β_{t|t−1} | W = 500 (frozen; 2-year window ensures slow β updates) | LOW |
| **F2** | Ridge shrinkage-β | Shrink rolling short-window OLS toward target=1.0 with L2 penalty | λ = 10.0 (frozen); target = 1.0; W_base = 126 (6-month base window for covariance estimation) | MEDIUM |

**F6 note:** F6 is the control family. If F6 produces a Cycle-2 CONFIRM, the crack spread has genuine MR detectable at β=1 (after normalization), which would be a trivial β=1 definitional result. The scientific contribution is from F1/F3/F5 confirming WITH a β that differs from 1.0 while still passing the N+M gates.

---

## §C. Admissibility Protocol (FROZEN — from doc 30 §2, verbatim)

**Per-family admissible iff P ∧ N ∧ M ∧ C on synthetic control suite BEFORE any real data read.**

**Frozen bound:** τ = 0.10 (f_βupdate fraction of Var(ΔS) must be < 0.10 on Z1/Z2/Z3)

**Frozen no-manufacture band (FROZEN):** VR(20) ∈ [0.80, 1.20] on Z1/Z2/Z3 martingale pairs.
Any family with VR(20) < 0.80 or > 1.20 on a martingale pair is manufacturing diffusion/trending — inadmissible regardless of other tests.

**Synthetic controls (FROZEN per doc 30 §2.2-2.3):**

| Control | Generating process | Required result |
|---|---|---|
| Positive control (P) | A = β*×B + OU_dev; B = trending RW + drift; β*=1.0; φ=0.95; σ=0.02; n=5000 | Family CONFIRMS: VR(20) < 0.80 AND beats RW∧GARCH∧MA1 at p<0.05 |
| Z1 martingale | A = 1.0×B + RW_dev; B = trending RW; spread = pure RW (no MR) | VR(20) ∈ [0.80, 1.20] AND f_βupdate < 0.10 |
| Z2 doc-19 stress | A = 1.0×B + RW; B = STRONGLY trending (drift=0.01/bar); same config that broke v1 | VR(20) ∈ [0.80, 1.20] AND f_βupdate < 0.10 — this is the DECISIVE gate |
| Z3 independent | A and B are independent RWs (no cointegration); β* = 0 | Family does NOT invent a spread (VR near 1, f_βupdate < 0.10) |

**Seed (FROZEN):** 20260604. **N (FROZEN):** 200 surrogate draws per family.
**Q grid (FROZEN):** (2, 5, 10, 20). **Primary statistic:** VR(20) (consistent with frozen v1/v2 apparatus).

---

## §D. Real-Pair Protocol (only after synthetic calibration gate PASSES for a family)

Real-pair verdict for a family is admissible only if that family first passes P∧N∧M∧C on synthetics.

Real-pair: HO2! vs CL2! (normalized to $/barrel).
- Apply frozen β construction (no lookahead, β_{t|t−1} only)
- Construct spread S = A_barrel − β_{t−1} × B_barrel
- Apply causal deseasonalization (same as calendars: trailing month-of-year mean)
- Run evaluate_v2 equivalent (RW∧GARCH∧MA1 headline gate, OU non-gating reference)
- Report f_βupdate on the real pair (must also be < τ=0.10)
- Report VR(q) for q ∈ {2,5,10,20}, full-period AND OOS split (70/30 by date)

**Cycle-2 CONFIRM:** ≥1 admissible family yields real-pair VR(20) < 5th percentile of matched RW ensemble, p < 0.05, f_βupdate < 0.10, not driven by hindsight-β artifact.

**Permanent demotion trigger (doc 30 §2.6):** ALL admissible-in-principle families fail the P∧N∧M trilemma on synthetics (every family either manufactures or destroys OU) while F6 (β=1) confirms the positive control. This proves the apparatus can see genuine OU but no estimated-β can extract it — deployment collapses to definitional spreads only.

---

## §E. Anti-Lookahead Firewall (FROZEN)

1. β hyperparameters (q_beta, λ, W, pre_sample_fraction, target) are frozen at this point. No tuning on real data.
2. No-manufacture band [0.80, 1.20] and τ=0.10 are frozen. No post-hoc adjustment.
3. Family admissibility is decided on SYNTHETIC controls. Real-pair result is NOT allowed to retroactively change the admissibility decision.
4. VR q grid and N are frozen. No argmax over q or N on the real pair.
5. Do NOT examine real HO2!/CL2! data before the synthetic calibration gate runs.

*Pre-registration frozen: 2026-06-05. Synthetic gate runs this session. Real-data execution requires the synthetic gate to PASS for at least one family.*
