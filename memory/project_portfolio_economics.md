---
name: project_portfolio_economics
description: "Portfolio combination (doc 45, 2026-06-06): INSUFFICIENT — Gate A fail (IS VR p=0.313, excision window in OOS); RB-CL DEFERRED-OOS-SIGNAL; LE-GF §11.8 anchor; independence ρ=0.013 clean"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2948af27-7fac-4e7b-bc98-f815d2ed82fa
---

**PORTFOLIO COMBINATION TEST COMPLETE (doc 45, 2026-06-06). Pre-registered before execution.**

**Verdict: INSUFFICIENT.** Gate A failed; RB-CL dropped from combined book; combination untestable.

**RB-CL (F6, β=1.0) — DOWNGRADED: DEFERRED-OOS-SIGNAL:**
- Gate A (excision test) FAIL: excised IS VR p=0.358 (pre-committed threshold p<0.050)
- Root cause: excision window (2020-03 to 2021-06) falls entirely in OOS (0 IS bars excised)
- IS-only raw VR (1998-2018, 4902 bars): p=0.313 — NOT significant BEFORE excision
- Full-period VR: p=0.015 — doc 44's "CLEAN" was full-period, NOT IS-only
- IS economics (DS): +$0.424/bbl, Sharpe=0.380 — positive, below threshold
- OOS economics: +$0.591/bbl, Sharpe=0.496 — OOS STRONGER than IS
- Power analysis: ~30-40% power to detect true VR=0.898 in 4902 IS bars
- NOT falsified. Named reopen trigger: IS VR on 1998-2023 IS / 2023-2026 OOS split

**LE-GF (F5, β=0.565) — MERELY-TRUE + §11.8 ANCHOR (re-anchored from RB-CL):**
- Unchanged verdict from doc 44
- IS Sharpe=0.939 (best in programme), OOS Sharpe=0.233 (COVID mechanism failure)
- Raw VR p=0.005 (full-period; expected IS-confirmed given strength of signal)
- Zero negative prices, no back-adj artifacts
- §11.8 ANCHOR: replaces RB-CL (whose IS VR p=0.313 makes it a weaker anchor)
- Capacity: $350-500k/yr. Reopen path: sub-period OOS ex-COVID Sharpe > 0.50

**Independence (informational, doc 45 Gate B):**
- Full return correlation: 0.013 (virtually uncorrelated)
- COVID 2020: sim loss 26.5% (INDEPENDENT), corr=-0.037
- Energy spike 2022: sim loss 23.6% (INDEPENDENT), corr=-0.032
- CONFIRMED INDEPENDENT. Clean result for future book construction.

**Informational combined book (Gate C, had Gate A passed):**
- Combined OOS Sharpe ≈ 0.41 (SMALL-BOOK-ONLY threshold 0.40)
- Combined capacity ≈ $2.35M/yr
- Result: would have been SMALL-BOOK-ONLY, not DEPLOYABLE-BOOK

**PRE-REG LESSON (doc 45):**
Any VR test used as a gate criterion must specify IS-only explicitly in the pre-registration. Full-period VR for characterization ≠ temporal violation. But full-period VR used as a PASS/FAIL gate criterion implicitly uses OOS data to determine whether to proceed.

**Prior durable principles (still binding):**
1. EXPECTANCY ≠ VARIANCE: diversification cannot rescue negative-expectancy sleeves
2. NG selectivity KILLED (doc 31): A_FALSE_RESCUE
3. VR sub-diffusion ≠ extractable fade alpha when back-adj contaminates levels
4. IS-only VR non-significance ≠ falsification when power is 30-40%

**Immediate next actions:**
1. LE-GF sub-period OOS ex-COVID (2020-2021)
2. RB-CL IS VR on alternative split (1998-2023 IS), pre-register first
3. HARD STOP: no portfolio construction until RB-CL IS VR confirmed

[[project_crack_beta_gate]], [[project_arm_a_verdict]], [[project_amr_framework]]
