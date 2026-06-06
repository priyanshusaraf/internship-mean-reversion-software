# Doc 33 — Cycle-2: Calendar Carry & Seasonal-Sleeve Discovery — FROZEN Pre-Registration

**Document class:** Permanent AMR pre-registration (institutional memory — frozen before any result).
**Date:** 2026-06-04. **Mode:** Trader-discovery. **Status:** FROZEN — execution-ready. No redesign after this line.
**Supersedes:** nothing. **Extends:** doc 30 (Cycle-2 trigger), doc 32 (trader-first objective). **Inherits binding:**
doc 15 (storage anchor), doc 23 (NG persistent-but-uneconomic), doc 31 (NG selectivity KILLED — A_FALSE_RESCUE),
doc 25 (only selectivity & netting move the ledger; selectivity now dead → **netting + carry are the live levers**).

> **Objective (the only one):** find **ONE deployable calendar sleeve** — positive net expectancy after costs —
> or **kill the calendar thesis**. Not coverage. Not ontology. Not understanding. One sleeve or a clean kill.

> **Zombie clearance (§4).** This is **not** a resurrection of the killed NG edge. Dead: NG reversion-*timing*
> capture (doc 23, uneconomic) and NG |z|-*selectivity* (doc 31, false rescue). Untested, different object:
> **carry/roll-yield** and **exogenous calendar-season-conditioned dated convergence** on storage calendars.
> Prior objections bind neither. Trigger: substrate ranking placed seasonal storage calendars at Tier 1.

---

## 0. The object and the ledger (frozen)

Per round-trip trade, in spread-return units (consistent with doc 23):

```
E_net  =  G  +  C_carry  −  K/η

G        = gross MR-timing expectancy per trade   (measured; NG whole-sample anchor +0.0004, doc 23)
C_carry  = roll-yield/term-premium accrued while held = r_carry · H̄    (NEW)
K        = round-trip cost per spread = 0.003 (frozen reference; + sensitivity readout)
η        = book netting factor ≥ 1 (cost divisor): {η_upper=min(M,3), η_realistic=1.5, η_cons=1.0}
H̄        = avg holding bars (reused realized holding from the doc-23 causal z-trade proxy)
r_carry  = causal per-bar structural drift of S (signed)   (NEW)
```

Break-even: `G + C_carry ≥ K/η`. Three estimates per cell: **upper / realistic / conservative**, exactly as the
Stage-0 prereg. **Netting reduces cost only** (`K/η`); it is never applied to gross. **G is frozen-measured, never
re-optimized** (re-tuning entry to lift G is laundered lookahead, doc 14 D1). **Margin offset does NOT enter `E_net`**
(it is a capacity/return-on-capital effect — counting it here is double-counting).

---

## 1. Instruments & frozen seasonal partitions (Red-Team-corrected)

Three β=1 **definitional** front calendars, built from **raw legs** (back-adjustment-clean), ADR_003 roll-masked.
**Exactly two binary directional splits total.** No month sweep, no shoulder-season, no three-way.

| Instrument | Split (FROZEN boundary) | Pre-registered DIRECTIONAL hypothesis | Mechanism |
|---|---|---|---|
| **NG**    | **Withdrawal = Nov–Mar** vs **Injection = Apr–Oct** (EIA storage-season convention) | withdrawal-season carry **thicker**, sign **negative** | scarcity-dated end-of-withdrawal convergence |
| **Corn**  | **Old-crop = Mar–Aug** vs **New-crop = Sep–Feb** (single harvest boundary at Sep) | **old-crop** carry **thicker** | storage tightens into harvest |
| **Brent** | **UNCONDITIONAL ONLY — no seasonal split** | (none) | crude has no clean storage-season mechanism → imposing one is fishing |

**Confirmatory cells = 3** (NG withdrawal; Corn old-crop; Brent unconditional). All other cells (off-seasons, any
per-month breakdown) are **DESCRIPTIVE, NON-CONFIRMATORY** and may never be headlined.

---

## 2. Frozen safeguards (binding — the B-grade preconditions)

1. **One-cell confirmatory logic.** The verdict reads ONLY the pre-registered directional cell per instrument
   (Brent: the unconditional cell). Off-season and per-month numbers are context only.
2. **Directional hypotheses frozen** (§1): which season is thick, and the sign. Test is **one-sided**;
   multiplicity per instrument = 1.
3. **Boundaries frozen** (§1): exact calendar months, same every year, transferable across years.
4. **No-argmax rule.** An unregistered month/season that "looks good" CANNOT be claimed without a NEW
   pre-registration (§4 zombie discipline). No promoting a descriptive cell to a finding.
5. **No ex-post refinement.** No boundary nudging, no shoulder tuning, no switching the hypothesized season
   after seeing results.
6. **Deflation note.** Report `partitions_tested` (every cell computed, incl. descriptive) and deflate any
   significance claim accordingly (Bailey–López de Prado).
7. **Jackknife-by-year gate (kill condition, not a footnote).** Leave-one-year-out the confirmatory `E_net`:
   sign must hold in **≥ ⌈0.6·N_years⌉** folds, and **max single-year leverage < 100%** of the point estimate
   (the doc-31 selectivity kill failed at >500%). Fail ⇒ artifact ⇒ that instrument is dead.
8. **Roll-cadence contamination check (precondition).** Verify the season boundary months do NOT coincide with
   the contract-roll-jump concentration (else "seasonality" = roll artifact, doc-23 cadence worry). Fail ⇒ the
   seasonal read is **void** for that instrument.

---

## 3. Contamination gates (all four mandatory; any fail ⇒ flag/void as specified)

1. **Back-adjustment:** carry on raw-leg series vs vendor continuous. Disagree ⇒ flag; force `C_carry=0` in the
   conservative column. (Carry that exists only on the vendor series is a splice artifact, not a return.)
2. **Carry separability:** `r_carry` via unconditional `mean(ΔS|season)` vs `|z|≈0`-conditional `mean(ΔS|season,|z|≤z0)`
   (`z0=0.5` frozen). Material disagreement ⇒ carry not isolable from timing ⇒ flag.
3. **Roll-cadence alignment** (§2.8): pass/fail precondition.
4. **Year stability** (§2.7): jackknife gate.

**Carry is measured on RAW `ΔS` — deseasonalization is OFF for the carry estimator** (`deseasonalize_causal` would
erase the very drift being measured). Deseasonalization remains available only for any downstream surrogate check,
not for the carry ledger.

---

## 4. Decision thresholds (frozen — evaluated on the confirmatory cell only)

Evaluate `E_net^{upper,realistic,cons}` in each confirmatory cell, after all four gates.

| Grade | Condition (confirmatory cell) | Action |
|---|---|---|
| **A — deployable sleeve** | `E_net^cons > 0` **AND** carry uncontaminated (gates 1–2 pass) **AND** jackknife + roll-cadence pass | **Sleeve found.** Spec the minimal book object. |
| **B — conditional / acquire** | `E_net^realistic > 0 ≥ E_net^cons`, gates pass | **Acquire named-month contracts** for that ONE pair (Phase 2); re-gate. |
| **C — cohort insufficient** | `E_net^upper ≤ 0` in all confirmatory cells, other constructions not excluded | **Redirect to cohort breadth** (no book engine). |
| **D — hopeless under construction** | `E_net^upper < 0` **AND** `C_carry ≤ 0`/contaminated **AND** no feasible `η/M` closes it | **Stop** this construction. |

First satisfied grade (A→D order) per instrument is its verdict. **Programme-level greenlight** = ≥1 instrument at A.
**Programme-level continue** = ≥1 at B. Else → KILL (below).

---

## 5. Kill criteria (frozen — no moving goalposts)

**KILL the calendar thesis if ALL hold across NG, Corn, Brent:**
- carry contaminated on every instrument and not cleanable (gates 1–2 fail everywhere); **and**
- no instrument clears `E_net^realistic > 0` unconditionally; **and**
- no confirmatory cell clears `E_net^realistic > 0`; **and**
- no instrument reaches grade **B**.

→ **Calendar-as-storage-MR-book killed on the class as tested.** Freeze the record; escalate the **flow-data
procurement decision** (substrate #6). Acquiring refined products "to be sure" requires a NEW pre-registration with
its own justification — it is NOT a continuation of this one.

**Continue (not kill):** ≥1 confirmatory cell at B → targeted named-month acquisition for that pair only.
**Greenlight:** ≥1 confirmatory cell at A → that is the deployable sleeve.

---

## 6. Frozen parameters (single source of truth)

```
K (round-trip cost ref) = 0.003   (+ sensitivity: report the K at which E_net flips sign)
η                       = {upper: min(M,3), realistic: 1.5, cons: 1.0}
z0 (|z|≈0 band)         = 0.5
jump-mask k             = 8.0  (engine default, increment_jump_mask)
G                       = measured per season from the doc-23 causal z-trade proxy (NOT re-optimized)
H̄                       = measured realized holding from the same proxy
seasons                 = NG{withdrawal Nov–Mar / injection Apr–Oct}; Corn{old Mar–Aug / new Sep–Feb}; Brent{none}
confirmatory cells      = NG.withdrawal, Corn.old-crop, Brent.unconditional   (partitions_tested counts ALL cells)
jackknife gate          = sign in ≥⌈0.6·N_years⌉ folds AND max single-year leverage < 100%
```

Anything not listed here is NOT a free parameter and may not be introduced post-freeze.

---

## 7. Non-conclusions / what this does NOT do

No detector, no score, no timing, no per-bar object. No controlled-β (this is β=1 definitional; controlled-β stays
doc 30's separate question). No surrogate-significance claim on the carry ledger (it is arithmetic; surrogates enter
only if a seasonal edge survives to a deployability claim). No expansion beyond the three named instruments without a
new prereg. **Next high-information question is fixed:** *does seasonal storage carry clear cost on NG or Corn?*

---

*Markers reserved for the results doc: CONFIRMED · CONDITIONAL · INSUFFICIENT · KILLED · CONTAMINATED · CARRY-DOMINATED.*
*Freeze authority: trader-first discovery mode (doc 32 Tier 1). No history to be rewritten; results append to a doc 34.*
