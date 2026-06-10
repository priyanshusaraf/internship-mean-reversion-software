# Doc 50 — GC-SI Log-Ratio IS VR Results

**Date executed:** 2026-06-10
**Pre-registration:** docs/research/50_gc_si_log_ratio_prereg.md (REVISION 1 binding)
**Runner:** scripts/run_50_gc_si_log_ratio.py
**Results JSON:** data/processed/50_results.json

---

## REVISION-1 MANDATE 3 — RUN-CONDITIONING STATEMENT (binding)

> α=0.0167 (Bonferroni 3-look) **partially prices multiplicity** across the
> three-look family (L1=doc-49 level-β screen; L2=2026-06-10 diagnostic peek
> at VR=0.947/0.797; L3=this test). However, α=0.0167 does **NOT** neutralize
> **conditional-existence selection**: this test was initiated BECAUSE the peek
> (L2) was favorable. That run-selection inflates the probability of a spurious
> pass in a manner Bonferroni does not fully correct. Therefore, **no claim that
> the peek contamination is fully corrected is permitted**. A PASS here registers
> as ACTIVE-IS-CONFIRMED-PEEK-CONDITIONED, not a clean confirmation. Clean
> confirmation requires either: (a) forward data post-2026-06 with a new prereg,
> or (b) the economics-stage trade statistic from a separate prereg.

---

## Verdict

**INCONCLUSIVE-UNDERPOWERED**

---

## Step 0 — Pre-Registration Restatement

- **Hypothesis:** IS log-ratio X_t = ln(GC2!) − ln(SI2!) exhibits VR(20) < 1 relative to RW null
- **Object:** β=1 definitional in log space; f_βupdate=0 identically
- **Trim start (frozen):** 1998-07-07
- **Split:** 70/30 row-count chronological
- **Primary statistic:** IS VR(20), p_rw(N=500) < 0.0167 (Bonferroni 3-look)
- **q grid:** {2, 5, 10, 20, 40}; q=20 primary, no argmax
- **Null families:** RW (gating), GARCH (supporting), MA(1) (supporting), OU (reference)
- **N:** 200 speed gate, 500 full; seed=20260612
- **α:** 0.0167 (3-look Bonferroni); PASS=p<0.0167; INCONCLUSIVE=[0.0167,0.05)
- **Power sim:** AR(1)-increments cumulated (corrected doc-48 pattern); ref VR=0.90
- **OOS:** NON-PROMOTABLE (peeked); sign-reversal veto applies
- **Jackknife:** 5-block, max-drop ≤ 300%
- **Kill criteria (ordered):** FileNotFoundError → MEASUREMENT-INADMISSIBLE → ADR_003 → f_βupdate → speed_gate → jackknife → full_test → OOS_sign_reversal

---

## Step 1 — Data Availability and Construction

| Field | Value |
|---|---|
| GC2! raw bars | 8848 |
| SI2! raw bars | 7356 |
| Aligned pre-trim | 7696 |
| Dropped by trim | 340 |
| n_aligned post-trim | 7016 |
| Actual date range | 1998-07-07 → 2026-06-03 |
| GC2! masked (log-ret, k=8) | 17 |
| SI2! masked (log-ret, k=8) | 14 |
| Combined masked | 25 |
| n_valid X_t bars | 6991 |
| IS rows / valid | 4911 / 4893 |
| OOS rows / valid | 2105 / 2098 |
| IS date range | 1998-07-07 → 2018-01-21 |
| OOS date range | 2018-01-22 → 2026-06-03 |
| β-mode | β=1.0 definitional (log space) |
| f_βupdate | 0.0 (identically zero; gate PASS) |

### ADR_003 Assertions

| Event | Caught | Date | Log-ret | Robust Z |
|---|---|---|---|---|
| SI2! 2026-01-29 | True | 2026-01-29 | -0.37195 | 22.93 |
| GC2! 1999-09-27 | True | 1999-09-26 | 0.01113 | 10.09 |
| Gate | PASS |||

### Flat-Bar Gate

| Leg | Flat-bar % in IS | Gate |
|---|---|---|
| GC2! | 0.509% | PASS |
| SI2! | 0.57% | PASS |

---

## Step 2 — Speed Gate (N=200)

- IS VR(20) = 0.985057
- p_rw(N=200) = 0.467662
- Kill threshold: p > 0.20
- Gate: KILL (p_rw=0.467662 > 0.2)

---

## Step 3 — Power Simulation (MANDATORY)

Pattern: AR(1)-increments cumulated (corrected doc-48 block); α=0.0167; n=n_IS_valid.

| Target VR | phi | Theoretical VR | Mean realized VR | Empirical power |
|---|---|---|---|---|
| 0.9 (ref) | -0.055394 | 0.9 | 0.8965 | **0.228** |
| 0.9851 (obs) | -0.007924 | 0.9851 | 0.9846 | 0.02 |

**Underpowered branch (power < 0.30): YES**

*Ex ante disclosure: With n_IS ≈ 4,911 bars, α=0.0167, ref VR=0.90, the corrected
AR(1)-increments power simulation was expected to yield ~0.20–0.35. This range was
known and disclosed in the pre-registration before execution.*

---

## REVISION-1 MANDATE 2 — Disjoint Sub-Window Check (binding)

**The 1998-07-07 → 2005-07 segment is the ONLY unpeeked slice in existence.**
Doc-49 peek covered the 2005-2018 IS slice; this segment was not seen.
A PASS whose significance is absent here carries the PEEK-CONDITIONED label with explicit warning.

| Field | Value |
|---|---|
| Segment | 1998-07-07 → 2005-06-30 |
| Rows / valid | 1745 / 1737 |
| VR(20) | 1.160184 |
| p_rw(N=500) | 0.928144 |
| Surr p5/p50/p95 | 0.7886 / 0.9863 / 1.1907 |
| Interpretation | FAIL — sub-diffusion absent in unpeeked slice |

---

## OOS Secondary Characterisation (NON-PROMOTABLE)

**OOS was peeked during doc-49 defect diagnosis (VR(20)=0.797 observed).**
OOS is NON-PROMOTABLE as a confirmation statistic within this prereg.
OOS confirmation for GC-SI can only come from the subsequent economics prereg.

| Field | Value |
|---|---|
| OOS dates | 2018-01-22 → 2026-06-03 |
| OOS rows / valid | 2105 / 2098 |
| OOS VR(20) | 0.773016 |
| OOS p_rw (lower tail) | 0.017964 |
| OOS p_upper (super-diff veto) | None |
| Surr p5/p50/p95 | 0.8191 / 0.9882 / 1.1782 |
| OOS sign-reversal kill flag | NO |

---

## Kill Gates Summary

Gates applied in pre-registered order. First triggered terminates test.

| Gate | Result |
|---|---|
| f_betaupdate | PASS (0.000 by construction) |
| flat_bar | PASS |
| adr003 | PASS |
| speed_gate_N200 | KILL (p_rw=0.467662 > 0.2) |
| power_branch | UNDERPOWERED (power=0.228) |
| jackknife | NOT REACHED |
| full_test_N500 | NOT REACHED |
| oos_sign_reversal | NOT REACHED |

---

## Registry Transition

**GC-SI log-ratio → INCONCLUSIVE-UNDERPOWERED**

- Power < 0.30 at ref VR=0.90 (observed: 0.228).
- Cannot distinguish trending from moderately-mean-reverting.
- Data-depth options: (a) pre-1998 GC2!/SI2! history; (b) accept single-sleeve LE-GF; (c) different platinum data source.

---

## Programme Status

- **LE-GF:** IS-ONLY CONFIRMED (p=0.024, doc 46); OOS-STRUCTURAL-WEAKNESS (doc 48).
- **RB-CL:** PERMANENTLY ARCHIVED (third look p=0.0798, doc 48).
- **NG selectivity:** KILLED (docs 23/31).
- **BRN calendar:** MERELY-TRUE (doc 36).
- **GC-SI log-ratio (this doc):** INCONCLUSIVE-UNDERPOWERED

---

*Pre-registration frozen 2026-06-10. No parameters revised post-execution.*
