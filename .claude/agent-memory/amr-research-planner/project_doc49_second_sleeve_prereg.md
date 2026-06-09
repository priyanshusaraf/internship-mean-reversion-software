---
name: doc49-second-sleeve-prereg
description: Doc 49 (2026-06-10) + REVISION 1 (2026-06-10 adversarial audit): GC-SI (F5, α=0.025) then PL-PA (PL2!/PA1!, F5, α=0.025); 6 new binding gates added; PA1! on-disk verified; PL1! unmanifested; flat-bar gate + ADR_003 assertion + kill-tree leaf separation now binding
metadata:
  type: project
---

Doc 49 frozen 2026-06-10. Revision 1 applied same day (adversarial audit MEASUREMENT + METHODOLOGY corrections).

**Authorization:** HYPOTHESIS_REGISTRY row "Second-sleeve IS VR screening cohort (GC-SI → PL-PA)", proposed doc 48 trader-lens.

**Why:** Doc 48 archived RB-CL permanently (3-look alpha budget exhausted) and found LE-GF OOS-STRUCTURAL-WEAKNESS (COVID attribution FALSIFIED). Combination gate BLOCKED. Need second instrument with IS VR confirmation.

**Construction per pair (frozen, confirmed after Revision 1):**
- GC-SI: `COMEX_DL_GC2!, 1D.csv` vs `COMEX_DL_SI2!, 1D.csv` — F5 presample-OLS (β frozen, 25% presample); β≠1 because gold:silver price ratio ≈80×; level spread; no deseason
- PL-PA: `NYMEX_DL_PL2!, 1D.csv` vs `NYMEX_DL_PA1!, 1D.csv` — F5 presample-OLS; same logic; tested only if GC-SI fails. PL1! is on-disk but NOT manifest-TRUSTED (unmanifested); PL2! retained. Roll-mismatch caveat ACTIVE (PL2!=2nd-continuous, PA1!=1st-continuous).

**Data status (Revision 1):** PA1! on-disk verified (10261 rows, 1985-08-26). PA2! does not exist. PL1! exists on disk but is unmanifested — flat early bars confirmed.

**Split rule:** 70/30 chronological ROW-COUNT (not calendar date). Pre-sample for β = first 25%; IS = rows 25–70%; OOS = rows 70–100%.

**α procedure:** fixed-sequence — GC-SI at α=0.025; PL-PA at α=0.025 only if GC-SI fails. FWER ≤ 0.05.

**GC-SI look-count disclosure (Revision 1, §4 zombie-reopen):** doc 18/19 look used rolling-OLS-β (INADMISSIBLE, construction kill) → VOID, zero evidential weight. Doc 49 = look #1 under admissible construction. α=0.025 unchanged.

**Primary statistic:** IS VR(20) vs RW null, N=500; speed gate N=200 p>0.20; full q grid {2,5,10,20,40}; jackknife ≤300%; 4 nulls (RW gating, GARCH, MA(1), OU reference). Seeds: GC-SI=20260610; PL-PA=20260611.

**Revised kill tree (Revision 1 additions binding):**
- 0. FileNotFoundError → BUG (halt, no verdict — never a DEFERRED-DATA)
- 0b. Flat-bar >5% in pre-sample after trimming → MEASUREMENT-INADMISSIBLE
- 1. f_βupdate ≥ 0.10 → construction-inadmissible
- 2. Aligned bars < 2000 → DEFERRED-DATA
- 3. Speed gate p>0.20 → kill
- 4. Jackknife >300% → kill
- 5. p_rw(N=500) ≥ 0.025 → not confirmed; §11.8 check if GC-SI
- 6. Pass all → IS VR CONFIRMED

**ADR_003 assertion (Revision 1, binding pre-VR):** runner must assert SI2! 2026-01-30 (+37.6%) and GC2! large event (+12.1%) are both caught by k=8.0 mask; report total masked bars per leg; halt on assertion failure.

**Flat-bar gate (Revision 1, binding):** within the 25% β pre-sample window, flat-bar % per leg >5% → trim early splice era; if still >5% after trimming → MEASUREMENT-INADMISSIBLE. Known: PL2! ≈15.6% flat overall (trimming expected); SI2! ≈5.0% borderline.

**§11.8 + power simulation:** apparatus recalibration mandatory if GC-SI fails. Power simulation must use increments-AR(1) cumulated (not level-AR(1); doc 48 four-lens fix).

**Economics gate (not in this doc):** separate prereg — OOS Sharpe>0.50, n≥30, cost 0.005.

**How to apply:** runner reads doc 49 + Revision 1 block as the sole source of truth. Revision 1 is in the same file, at the bottom. No parameter changes after freeze. Cite doc 49 Revision 1 for all GC-SI/PL-PA IS VR runner specs.
