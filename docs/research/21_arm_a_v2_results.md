# Arm A v2 — Cycle 1: Real-Data Positive Control — Execution, Verification & Verdict

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **COMPLETE — first apparatus-validation read in the programme.** Executes doc 20 exactly.
**Date:** 2026-06-04. **Mode:** Controlled-Implementation (execution) → Research (adjudication).
**Provenance:** engine `backend/app/services/analytics_arm_a_v2.py` (additive to the frozen v1
`analytics_arm_a.py`); runner `scripts/run_arm_a_v2.py`; hygiene `scripts/hygiene_arm_a_v2.py`; results
`data/processed/arm_a_v2_results.json`. Two adversarial sub-reviews preceded the verdict: a **pre-freeze
four-lens design review** (doc 20) and a **post-execution two-lens refutation** (adversarial + statistical).
Confidence labels = trustworthiness-of-evidence.

> **Headline verdict:** **CONDITIONAL SURVIVAL — the §11.8 real-data positive control is PASSED in the
> conditional sense.** The apparatus demonstrably has **power** (confirms known reverters), **selectivity**
> (correctly nulls a non-reverter at the book horizon and finds its reversion at the right long horizon),
> **noise-discrimination** (an MA(1)-microstructure null kills a pure RW+bounce series that RW/GARCH wrongly
> confirm), and **calibration** (gate FPR = 3.0% on 200 RW seeds). The confirm is **corroborated under a
> construction we fully control** (self-built Brent calendar). **Residual open channels** (named below) keep
> this *conditional*, not unqualified. **Confidence: MEDIUM-HIGH** that the apparatus is power- and
> selectivity-validated; **MEDIUM** that NG specifically is clean storage MR vs partial vendor-construction
> artifact (mitigated, not eliminated).

---

## 1. Prior thesis → new construction (why v2)
v1 (doc 19) was **INCONCLUSIVE / construction-defective**: rolling-OLS-β-on-levels *manufactures* VR (β-update-
noise 82–97% of variance, proven). v2 (doc 20) restricts to **β=1 DEFINITIONAL calendar spreads** (zero
rolling-β DOF → structurally immune to the v1 artifact) and reframes the question as the **§11.8 standing gate**:
*can the apparatus CONFIRM a known, literature/economically-anchored real edge (storage-driven calendar MR)?*
A gate that cannot confirm a known reverter cannot make any future *kill* credible.

## 2. What was run (execution log)
- **§5a synthetic calibration gate (must-pass, NEW adapter path — doc-18a's leg-path FPR does not transfer):**
  (1) true seasonal-OU calendar → **CONFIRMS** (power). (2) true RW calendar → gate FPR = **3.0%** over **200
  seeds** (per-family rw 3.5% / garch 3.5% / ma1 4.0% / ou 2.0%) — below nominal 5%. (3) RW + i.i.d. observation
  noise (zero MR, bid-ask bounce) → RW/GARCH/OU **spuriously confirm**, **MA(1) KILLS it** → gate NULL (the
  decisive noise-discrimination control). (4) no-seam no-op: jump filter shifts VR by 0.000 on clean OU. **ALL
  PASS.**
- **Cohort (doc 20 §3), UNMASKED headline, seed 20260604, N=200, q∈{2,5,10,20}, gate = RW ∧ GARCH ∧ MA(1)
  multiplicity-corrected min-VR < 5th pct, real_min<1.**

## 3. Verdict matrix (real − matched surrogate; multiplicity-corrected min-VR p)

| Instrument | Role | n | VR(2,5,10,20) | min | p_RW | p_GARCH | p_MA1 | p_OU | GATE |
|---|---|--:|---|--:|--:|--:|--:|--:|:--:|
| **NG calendar** (ng12, daily ≥2006-07-28) | **PRIMARY** | 4969 | 0.921,0.828,0.605,**0.448** | 0.448 | **0.005** | **0.025** | **0.005** | 0.005 | **CONFIRMED** |
| **Brent calendar (self-built BRN1!−BRN2!, 60m)** | **construction-control cross-check** | 22955 | 0.911,0.800,0.708,**0.634** | 0.634 | **0.005** | **0.010** | **0.005** | 0.005 | **CONFIRMED (all q)** |
| RB calendar (rb23, daily) | near-martingale reference | 5170 | 0.996,0.993,0.983,0.979 | 0.979 | 0.537 | — | — | — | **NULL** (expected) |
| RB calendar — long-horizon (descriptive, non-verdict) | — | 5170 | q40=0.627,q60=0.485,q120=0.415 | 0.415 | **0.005** | — | — | — | (reverts at q≥60) |
| WTI–Brent (cl_brn, 60m vendor) | context | 19399 | 0.944,0.629,0.491,0.412 | 0.412 | 0.005 | — | 0.005 | — | CONFIRMED (context) |

**Robustness on NG (primary):**
- **Deseasonalization (causal trailing month-of-year mean):** GATE=True, VR→[0.953,0.697,0.439,**0.249**],
  p_rw=p_ma1=0.005 — *survives and strengthens* (caveat in §5).
- **Open/Close consistency:** close VR(20)=0.448 vs open 0.545 — both sub-diffusive, same direction (open ~12–22%
  weaker; see §5).
- **k-ablation (jump filter, NEVER headline):** VR(20) k=6→1.125, k=8→0.972, k=10→0.905, **unmasked→0.448**. The
  filter is a **one-sided VR→1 lever** that *flips the verdict* — vindicating the unmasked headline (doc 20 §4).
- **Per-horizon separation (the load-bearing structure):** vs **RW** NG separates at **all** q; vs **GARCH** and
  **MA(1)** only at **q10/q20** (not q2/q5). The binding confirm is long-horizon.

## 4. Adversarial verification (PRECEDES the verdict; preserved per §5)
The post-execution committee (adversarial + statistical) returned **HOLDS_WITH_CAVEATS, MEDIUM**, correcting an
initial "kills are now credible" overreach to a **conditional** read. Its load-bearing findings:
- **(PRIMARY, STRUCTURAL) Vendor back-adjustment / splice compression is the one artifact the battery does not
  discriminate.** NG's confirm is carried at q10/q20; additive back-adjustment at the monthly roll mechanically
  compresses long-horizon variance → VR declining in q → *indistinguishable from storage MR* under a level-
  difference statistic. ng12 is an opaque vendor "continuous calendar" (roll/back-adjustment/contract-month
  **unaudited**, doc 20 §8). **Partially mitigated post-verification** by the **self-built Brent calendar**
  (§3): a calendar built from raw ICE legs under *our* roll rule (59/22955 bars masked, no back-adjustment)
  **confirms at ALL horizons** — the *opposite* of the long-horizon-only compression signature. Two energy
  calendars now confirm, one construction-controlled. Not fully eliminated for NG-daily specifically (different
  instrument/frequency/span).
- **(METHODOLOGY) The MA(1) null is a near-no-op at q≥10** (its VR effect decays ~1/q; at NG's ACF(1)=−0.076 the
  implied MA(1) VR is ≈0.985 at q=10). It rules out **lag-1 bid-ask bounce**, not multi-lag microstructure. *(The
  self-built Brent calendar beats MA(1) at q2 too, where MA(1) has power — partial reassurance.)*
- **(METHODOLOGY) Deseasonalization-induced reversion:** the causal trailing demean is an adaptive recursive
  filter that can induce negative autocorrelation on a pure RW; surrogates were **not** passed through the
  identical operator, so the deseason *strengthening* (0.448→0.249) is **not clean evidence** (the **raw** confirm
  does not depend on it — raw is load-bearing).
- **(MEASUREMENT) Gate FPR:** the 20-seed estimate (10%) was small-sample noise; the **200-seed re-measure =
  3.0%** (below nominal 5%, conjunction tighter than any single family) — **the calibration concern is
  resolved.** GARCH at p=0.025 is the weakest gate family (would not survive a strict 3-family Bonferroni 0.0167,
  but is the correct binding value for an intersection gate, and NG sits at the surrogate floor rank 1/201).
- **(STRUCTURAL) No rolling-local stability check** (§11.1 default): the verdict is a single global statistic over
  2006–2026; a regime mixture could read sub-diffusive. **Open — see §7.**

## 5. Verdict & confidence
**CONDITIONAL SURVIVAL — §11.8 positive control PASSED (conditional).** Precisely:
1. **Power (HIGH):** the apparatus confirms a synthetic seasonal-OU calendar at the p-floor, and confirms two
   real energy calendars (NG daily; self-built Brent hourly).
2. **Selectivity (MEDIUM-HIGH):** it correctly **NULLs RB at q≤20** (a true book-horizon non-reverter, p=0.537)
   and **finds RB's reversion at q≥60** (p=0.005) — it is not a blunt always-confirm instrument.
3. **Noise-discrimination (MEDIUM-HIGH):** the MA(1) null kills a synthetic RW+bounce series that RW/GARCH
   wrongly confirm — the apparatus detects *MR*, not lag-1 microstructure (though multi-lag is not fully closed).
4. **Calibration (MEDIUM-HIGH):** gate FPR = 3.0% (200 seeds), below nominal 5%.
5. **Construction-artifact discrimination (MEDIUM):** the self-built Brent calendar corroborates under a
   construction we control; the NG-daily vendor channel is *mitigated, not eliminated.*

**Aggregate: MEDIUM-HIGH** that the apparatus is **power- and selectivity-validated** (a real advance over the
all-synthetic prior state — the §11.8 gap is materially closed). **MEDIUM** that the NG-daily confirm is *clean
storage MR* rather than *partly vendor-construction artifact.* Provenance: the verification labeled MEDIUM; two
**un-peeked** follow-ups (200-seed FPR=3%, self-built Brent confirm) resolved two of its caveats, supporting the
upgrade to MEDIUM-HIGH on the apparatus claim.

## 6. What this licenses · explicit non-conclusions
**Licensed:** future AMR *kills* are **more credible** than under the all-synthetic regime — specifically, a kill
of a genuine long-horizon reverter is now less likely to be a false kill, because the apparatus has demonstrated
power + selectivity + 3% FPR + construction-controlled corroboration. The construction-ontology fix is
established: **β=1 definitional spreads are admissible and artifact-free; rolling-OLS-β-on-levels remains
INADMISSIBLE (v1).**
**Explicit NON-conclusions:** (a) *Not* "all future kills are credible" (overclaim, corrected). The book-horizon
(q≤20) kill credibility is weaker — that is exactly where vendor compression and multi-lag microstructure live.
(b) *No* claim NG is a tradeable edge (positive control ≠ deployment; cost-after-book untested). (c) *No* cross-
habitat *daily* replication yet (§11.7 makes it mandatory for a *finding*; for a *gate* one clean confirm +
corroboration is weaker but real). (d) *Nothing* about controlled-β **pairs** — the actual deployment
construction (§1.1) — which Cycle 2 defers and which v1 proved the apparatus mishandles. (e) No detector / score /
timing / State-T object (frozen).

## 7. Surviving uncertainty · next high-information question
**Surviving uncertainty:** vendor back-adjustment on NG-daily (multi-lag microstructure at q≥10; deseason-operator
bias-cancellation; no rolling-local stability read; single daily confirmer).
**Next high-information question (binding, ranked):**
1. **Rolling-local stability of the NG confirm** (§11.1 default; cheapest): does VR<1 persist across multiple
   disjoint sub-windows, surrogate-relative, or is the global read a regime mixture? Run on existing data.
2. **Surrogate-matched deseasonalization** (close the §5 methodology caveat): pass each surrogate draw through the
   identical causal demean so the operator artifact cancels.
3. **Multi-lag microstructure null** (close the §4 methodology caveat): an MA(p)/AR-in-noise null with longer
   memory; require the long-horizon confirm to beat it.
4. **Cycle 2 — controlled-β positive control on a textbook cointegrated pair** (doc 20 §7): the deployment-domain
   construction the calendar control does not exercise. Trigger satisfied (Cycle-1 conditional confirm).
**Crack spread (`/arm-a` priority #5): DATA-BLOCKED** — no heating-oil/gasoline *price* leg locally; recorded,
not dropped (reopen on leg acquisition).

---
*Markers: CONFIRMED-CONDITIONAL (NG storage MR, apparatus power) · STRENGTHENED (self-built Brent corroboration;
3% FPR) · UNRESOLVED (NG vendor back-adjustment vs storage MR; multi-lag microstructure) · CARRIED-FORWARD
(rolling-local stability; Cycle 2 controlled-β pairs) · DATA-BLOCKED (crack spread). The "kills are now credible"
first-pass was corrected to CONDITIONAL by the adversarial committee; no history erased.*
