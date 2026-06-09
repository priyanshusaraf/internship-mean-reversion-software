---
name: rb-cl-le-gf-reopen-prereg
description: 2026-06-10 Revision 1 preregs (adversarial audit applied) for two registry reopen triggers: Test A (RB-CL alt split IS VR, CL2! leg, 3-look alpha) + Test B (LE-GF ex-COVID dual-criterion with mandatory placebo)
metadata:
  type: project
---

Two-test pre-registration Revision 1 frozen 2026-06-10 in docs/research/rb_cl_alt_split_le_gf_subperiod_prereg.md. Results doc will be 48_rb_cl_alt_split_le_gf_subperiod_results.md.

Adversarial audit returned INADMISSIBLE on original draft. Four defects corrected before any data touch.

**Test A — RB-CL alternative split (Revision 1):**
- Leg: CL2! (NYMEX_DL_CL2!) — NOT CL1!; RB-CL object is RB2!−CL2! throughout docs 39/40/44/45
- IS_END = 2022-12-31; OOS_START = 2023-01-01
- Justification: POWER ONLY (~6,100 IS bars vs ~4,904 original; power ~45-55% vs ~30-40%); excision argument DROPPED (doc 40 line 29: CL2! back-adj offset negligible)
- NO primary excision window; optional robustness arm (2020-03-01 to 2021-06-30) informational only, not gating
- Alpha-spending: PASS_P_RW = 0.0167 (Bonferroni: 0.05/3 for THREE pre-named looks: doc-40 full-period p=0.015, doc-45 IS-only p=0.313, this test)
- Kill: p_rw ≥ 0.0167 at N=500 → ARCHIVED permanently (INCONCLUSIVE band [0.0167, 0.05) also triggers ARCHIVED, not a stay)
- Speed gate: p_rw(N=200) > 0.20 → kill immediately

**Test B — LE-GF ex-COVID OOS (Revision 1):**
- Excision: EXCISE_COVID_START=2020-01-01, EXCISE_COVID_END=2021-06-30 (18-month programme-standard; NOT 2021-12-31; externally datable: COVID onset + JBS cyberattack resolution)
- Selection-on-regime caveat: COVID window identified partly by observing OOS PnL in docs 45/46; placebo control is the mitigation
- DUAL-CRITERION PASS (both required):
  - Criterion 1: OOS ex-COVID Sharpe > 0.50 (registry-named threshold)
  - Criterion 2: COVID-window excision Sharpe ≥ 90th percentile of all 18-month placebo-excision Sharpres (monthly step through OOS; ≥30 trades filter applied to each window)
- Fail on either criterion → registry stays §11.8 IS-ONLY CONFIRMED; NOT an archive trigger for LE-GF
- Kill if n_trades_ex_covid < 30 → INCONCLUSIVE

**Combination gate opens only if:** Test A CONFIRMED (p<0.0167) AND Test B dual-criterion pass (Sharpe>0.50 AND ≥90th pctile placebo). Independence already confirmed (ρ=0.013, doc 45). New combination pre-registration (doc 49 equiv) required before any portfolio execution.

**Why:** [[project_arm_a_verdict]] [[project_crack_beta_gate]] [[project_portfolio_economics]]
