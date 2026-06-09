---
name: doc49-verdict-label-defect
description: Doc 49 GC-SI runner bypassed its own frozen INCONCLUSIVE-UNDERPOWERED branch via a hardcoded speed-gate classification; numbers reproduce but label is prereg-noncompliant
metadata:
  type: project
---

Doc 49 (second-sleeve GC-SI/PL-PA screening) terminal label dispute.

**All numbers reproduce exactly** (independently re-run 2026-06-10): GC-SI aligned 7016, IS-valid 3155, beta 39.48, IS VR(20)=1.0106, p_rw(N=200)=0.6418, power@obsVR=0.006, power@VR0.90=0.176; PL-PA flat 12.39% post-trim (pervasive 1998-2007 at 30-42%, PA1! clean 0.95%). The 4911->3155 IS loss = 1754 F5 presample (NaN by design) + 2 roll-mask = legitimate, matches prereg Part III middle-45% rule.

**The defect (METHODOLOGY/IMPLEMENTATION):** Frozen kill-tree branch-3 mandates "GC-SI fails + power<0.30 -> INCONCLUSIVE-UNDERPOWERED + mandatory §11.8 recalibration report." Power=0.176<0.30 at the reference sub-diffusion VR. But the runner's speed-gate branch (run_49 lines ~924-971) returns SPEED_GATE_KILL and never routes through the underpowered->INCONCLUSIVE logic that exists ONLY in the full-test path (lines 1135-1139). Then line 1276 hardcodes `gc_si_failed_clean = verdict in (...,"SPEED_GATE_KILL",...)`. The runner's OWN JSON contradicts the prose: apparatus_status="UNDERPOWERED", 11_8_trigger=true. The results-doc prose ("clean kill", "§11.8 recalibration NOT triggered") is post-hoc reasoning the prereg never authorized.

**Why the runner's defense fails:** "VR>1.01 means no sub-diffusion to detect" conflates point-estimate sign with discriminating power. At n=3155 with power 0.176, a genuinely sub-diffusive VR~0.90 spread would also fail to reject ~82% of the time. The test cannot distinguish "trending" from "moderately MR but underpowered." The frozen tree anticipated exactly this and pre-committed the label.

**Correct cohort leaf:** NOT the clean "COHORT-EXHAUSTED -> book infeasible". GC-SI = INCONCLUSIVE-UNDERPOWERED (§11.8 recalibration report owed before any spread-MR negative is credible per §11.8 standing gate). PL-PA = MEASUREMENT-INADMISSIBLE (correct). Cohort breadth question is unresolved-underpowered, not exhausted.

**No zombie violation:** F5 frozen beta, f_betaupdate=0 — kill-ledger entry 5 (rolling-OLS-beta) does NOT apply. Construction admissible.
