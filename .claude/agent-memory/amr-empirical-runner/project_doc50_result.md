---
name: project_doc50_result
description: doc 50 (2026-06-10): GC-SI log-ratio IS VR — INCONCLUSIVE-UNDERPOWERED (speed gate kill; power=0.228 < 0.30); disjoint sub-window VR=1.16 (super-diffusive, p=0.928); OOS VR=0.773 (informational); cohort unchanged
metadata:
  type: project
---

GC-SI log-ratio doc-50 result: **INCONCLUSIVE-UNDERPOWERED**

**Why:** Speed gate kill (p_rw(N=200)=0.4677 > 0.20). IS VR(20)=0.9851 — essentially flat, nearly RW. Power simulation (corrected AR(1)-increments, n_IS=4,893, α=0.0167) yielded 0.228 at ref VR=0.90, below the 0.30 universal underpowered threshold. Universal underpowered branch applies — cannot distinguish trending from moderately-mean-reverting.

**Key numbers:**
- n_aligned=7,016; IS rows=4,911 (1998-07-07→2018-01-21); OOS rows=2,105 (2018-01-22→2026-06-03)
- IS VR(20)=0.9851, p_rw(N=200)=0.4677
- Power@ref_vr=0.90: 114/500=0.228 (UNDERPOWERED); power@obs_vr=0.985: 0.020
- Flat bars IS: GC2!=0.509%, SI2!=0.570% (both PASS)
- ADR_003: SI2! 2026-01-29 caught (robust_Z=22.93); GC2! 1999-09-26 caught (robust_Z=10.09)
- Combined masked: 25 bars (0.36%)
- Disjoint sub-window (1998-07-07→2005-06-30, Revision-1 Mandate 2): VR=1.160, p_rw=0.928 — super-diffusive, NO sub-diffusion in unpeeked slice
- OOS (NON-PROMOTABLE): VR=0.773, p_rw=0.018 (informational only; peeked)

**Registry transition:** GC-SI log-ratio → INCONCLUSIVE-UNDERPOWERED (data constraint; ~4,900 IS bars, α=0.0167 too strict for this n)

**How to apply:** Cohort exhausted at current data depth. Programme remains single-sleeve (LE-GF IS-ONLY CONFIRMED). Options surfaced: (a) acquire pre-1998 GC2!/SI2! history; (b) accept single-sleeve LE-GF; (c) PL-PA remains DEFERRED-MEASUREMENT-INADMISSIBLE. Combination gate still BLOCKED.

[[project_doc49_cohort_result]] [[project_single_sleeve_status]]
