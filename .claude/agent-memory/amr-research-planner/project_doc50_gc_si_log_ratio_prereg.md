---
name: doc50-gc-si-log-ratio-prereg
description: Doc 50 (2026-06-10): GC-SI log-ratio IS VR pre-registration — corrective construction after doc-49 level-β CONSTRUCTION-INADMISSIBLE; α=0.0167 from 3-look Bonferroni; OOS NON-PROMOTABLE (peeked); underpowered branch universal
metadata:
  type: project
---

GC-SI log-ratio IS VR pre-registration frozen 2026-06-10.

**Why:** Doc-49 four-lens audit found level-β F5 on GC-SI CONSTRUCTION-INADMISSIBLE (64.6% of Var(spread) was deterministic linear trend from gold-silver ratio drift 39.9→83.1). The admissible object is X_t = ln(GC2!) − ln(SI2!), β=1 definitional in log space.

**Key decisions:**

- Object: X_t = ln(GC2!_close) − ln(SI2!_close). β=1 definitional. f_βupdate=0 identically.
- Trim: 1998-07-07 (frozen from doc-49 SI2! flat-bar derivation). No presample consumed for β.
- IS/OOS: 70/30 row-count chronological. IS ≈ 4,911 bars. OOS NON-PROMOTABLE (peeked).
- α = 0.0167 (0.05/3, Bonferroni): L1=doc49 level screen; L2=2026-06-10 diagnostic peek (VR(20)=0.947 IS / 0.797 OOS observed during defect diagnosis); L3=this test. L2 cannot be reclassified as informational — it is a direct favorable look at this test's statistic.
- INCONCLUSIVE zone: p ∈ [0.0167, 0.05) = INCONCLUSIVE-LEANING-FAIL (not a pass, not a clean negative).
- Seed: 20260612.
- Power α = 0.0167 (matches gate, stricter than doc-49's 0.025).
- Underpowered branch universal (doc-49 lesson): ANY failure with power<0.30 → INCONCLUSIVE-UNDERPOWERED. "VR>1 means nothing to detect" is NOT a valid override.
- Expected power ex ante: ~0.20–0.35 at n≈4,911, VR=0.90, α=0.0167. INCONCLUSIVE is a legitimate leaf.

**Verdict tree leaves:** PASS → GC-SI log-ratio = second-sleeve CANDIDATE → economics prereg next. FAIL power≥0.30 → SCREENED-NEGATIVE (honest negative). FAIL power<0.30 → INCONCLUSIVE-UNDERPOWERED (data-depth options: extend history / accept single-sleeve / PL-PA new data source). MEASUREMENT-INADMISSIBLE (flat-bar >5% IS window, no trim DOF). OOS-SIGN-REVERSAL veto (VR_oos>1, p_oos<0.05).

**OOS status:** Peeked (VR=0.797 seen). Reported secondary, informational. NON-PROMOTABLE as confirmation in this doc. OOS confirmation only via subsequent economics prereg (trade-rule statistics, different statistic family).

**§11.8:** LE-GF remains sole anchor. This run does not exercise §11.8 — the admissible construction was never given to the apparatus in doc-49.

**How to apply:** When writing the runner or results doc, cite α=0.0167 and the 3-look accounting. Do not accept p ∈ [0.0167, 0.05) as a pass. Enforce the underpowered-branch universal rule.

Related: [[doc49-second-sleeve-prereg]] [[crack-beta-gate]] [[arm-a-verdict]]
