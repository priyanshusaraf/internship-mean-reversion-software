---
name: project_crack_beta_gate
description: "Crack-β programme (docs 37-46): RB-CL DEFERRED-OOS-SIGNAL; LE-GF MERELY-TRUE + §11.8 IS-ONLY CONFIRMED (doc 46, p_rw=0.024, 4 surrogates); spread programme CLOSED; Track 1+2 authorized"
metadata:
  type: project
---

## Programme context (docs 37-46)
- Synthetic gate (37): F5+F6 ADMISSIBLE; F1/F2/F3 INADMISSIBLE
- HO-CL (39): VR CONFIRM; A_FALSE_RESCUE economic (back-adj)
- RB-CL (40): F6 VR CONFIRM full+OOS; C_GENUINE_ECONOMIC (43)
- LE-GF (42): F5 VR CLEAN CONFIRM full+OOS; C_GENUINE_ECONOMIC (43)
- Gauntlet (44): RB-CL CONDITIONAL-CANDIDATE, LE-GF MERELY-TRUE
- Portfolio (45): Gate A FAIL → INSUFFICIENT; RB-CL DEFERRED, §11.8 → LE-GF
- **Gate 0 IS-only (46): LE-GF IS VR p_rw=0.024 → §11.8 anchor CONFIRMED IS-only; spread programme CLOSED; Track 1+2 unblocked**

## Sleeve verdicts (doc 46, current)

**LE-GF (F5, β=0.565) — MERELY-TRUE + §11.8 IS-ONLY CONFIRMED:**
- IS-only VR(20) p_rw=0.024 — PASS (pre-committed threshold p<0.050)
- All 4 surrogates pass: RW p=0.024, GARCH p=0.026, MA(1) p=0.020, OU p=0.044
- IS period: 2002-08-14 to 2019-05-23 (4123 bars, 2651 valid)
- Full-period vs IS-only: 0.766 (p=0.002) → 0.822 (p=0.024) — IS holds (unlike RB-CL)
- VR lag profile: sub-diffusive only at q≥20 (consistent with feedlot cycle ~1 month)
- Power: 58% (better than RB-CL's 30-40%)
- IS Sharpe (DS): 0.939. IS Sharpe (raw): -0.014. VR is on raw; economics on DS — different objects, coherent.
- OOS Sharpe: 0.233 (COVID/JBS disruption 2020-2021; mechanistic)
- Independent re-implementation: analytic p≈0.033; robust p≈0.04-0.06 — borderline but passes

**RB-CL (F6, β=1.0) — DEFERRED-OOS-SIGNAL (doc 45):**
- IS VR p=0.313 (FAIL). Spread programme CLOSED per directive.
- Reopen: IS VR on 1998-2023 IS split OR cross-habitat replication
- NOT killed; PARKED.

## Spread programme status
**CLOSED per 2026-06-06 directive.** No new crack/calendar pairs. No RB-CL rescue attempts.
LE-GF harvest is NOT reopening spread research — it is harvesting an already-confirmed edge.

## Key admissibility rules (frozen, unchanged)
- F5: pre-sample OLS β (first 25%), frozen post-pre-sample; f_βupdate=0.000 required
- F6: β=1.0 definitional; only when BOTH legs normalized to same physical unit
- F1/F2/F3: INADMISSIBLE on real data (zombie prohibition)
- PRE-REG LESSON (doc 45+46): any gating VR test must specify IS-only; DS claim ≠ raw VR claim — both can be true simultaneously

## What's authorized now (post doc 46)
1. **Track 1** (background): pre-register LE-GF trade rules → IS sanity → 2022-2026 sub-period check → live paper
2. **Track 2** (main effort): T2.5 minimal trend-death test — AAPL, CL outright, NIFTY/SPX, ADANIENT
3. HARD STOP on: portfolio construction, new spread pairs, deployment infrastructure

[[project_portfolio_economics]], [[project_arm_a_verdict]], [[project_amr_framework]]
