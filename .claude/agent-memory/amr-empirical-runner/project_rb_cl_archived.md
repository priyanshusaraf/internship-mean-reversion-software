---
name: project_rb_cl_archived
description: RB-CL crack spread permanently archived after third look (doc 48, 2026-06-10) — p=0.0798, power=1.000, no further testing ever
metadata:
  type: project
---

RB-CL (RB2!×42 − CL2!, F6 β=1.0) is PERMANENTLY ARCHIVED as of 2026-06-10 (doc 48).

**Third look result:** IS 1998-08-03→2022-12-29 (6,134 bars), N=500 surrogates: p_rw=0.0798. Bonferroni α=0.0167 (3 looks: doc-40 full p=0.015; doc-45 IS-only p=0.313; doc-48 alt split p=0.0798). None of the three looks survive.

**Why:** Empirical power simulation at IS length = 1.000 (AR(1) calibrated to true VR=0.898, 500 paths, N=200 test). The failure is genuine absence of IS sub-diffusion, not a power limitation. The alternative split from 1998 raised power from ~35% (doc-45) to ~100% — and still failed.

**How to apply:** Do NOT suggest any further RB-CL IS VR testing, alternative splits, β re-estimations, θ tuning, or construction variants. The archive is unconditional. No fourth look, ever. Portfolio combination based on RB-CL is permanently blocked.

**Kill sequence:** speed gate PASS (p=0.0945), jackknife PASS (5% drop), excised-IS PASS (p=0.0279, no COVID dependence), but primary gate FAIL (p=0.0798 ≥ 0.0167 ≥ 0.05).
