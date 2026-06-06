# Arm A — Deployment-Domain Habitat Test: Pre-Registration

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **PRE-REGISTRATION (written before any VR(q) is computed).** Fixes the claim, the cohort, the
construction, the surrogate design, and the kill criteria *before results exist*, so any later finding is
confirmation/falsification — not post-hoc storytelling. **No statistic has been computed.**
**Date:** 2026-06-03.
**Mode:** Controlled-Implementation pre-registration. **Execution is a separate authorization.**
**Scope:** the first power-adequate, provenance-audited, causally-constructed test of whether a deployment-domain
mean-reverting habitat exists. Builds on: doc 12 (Arm A), doc 13 + ADR_003 (construction law), doc 14 (VR(q) as the
admissible richer object), doc 16 (morphology — surrogate-relative), red-team critique (`waiting_period/`),
`data/mr_cohort_manifest.md` (the audited legs).

> **▸ CONTEXT.** Unlike all prior real-market work (ADANIENT, trend-heavy placeholder), this test runs on
> **genuine deployment-domain structures** (commodity intercommodity/calendar spreads, a cointegrated equity pair)
> built from audited legs. Findings here are still **instrument-specific, not global**; a null in one habitat is not
> evidence against MR everywhere.

---

## 0. What this is NOT
Not State T. Not detection, not timing, not a per-bar score, not a signal. No T-score / hazard / "MR-favorable-NOW".
The output is a **distributional, corpus-level verdict per instrument** (does its meaning depend on *when* you read
it? if yes → frozen). State-T detection remains FROZEN; the zombie prohibition binds. **This test does not touch
μ\*** — it reads the spread's *own* return-space variance ratio, not a μ\*/Kalman residual, so it does **not** trip
the doc-06 §15.8 μ\* reversion-fidelity reopen trigger.

## 1. The empirical claim under test
> For a causally-constructed, roll-handled deployment-domain spread `S_t`, is its **return-space multi-horizon
> variance-ratio curve VR(q)** distinguishable from its **own matched surrogate null** in the mean-reverting
> direction (VR < 1 and VR < surrogate) — measured as a corpus-level effect, never a per-bar quantity?

A genuine MR habitat ⇒ `VR(q) < 1` (sub-diffusive) and **below its matched-surrogate band** at one or more
pre-registered horizons. This is the logically-prior question the programme skipped: *where does MR robustly exist*,
before any *when*-it-ignites work.

## 2. Cohort & construction (frozen)
From `data/mr_cohort_manifest.md` (46 TRUSTED legs). Construction strictly per **doc 13 + ADR_003**: legs
roll-handled (R-1; roll-transition bars neutralized), **inner-join on synchronized timestamps**, **β estimated on
data ≤ t−1 and applied at t** (no contemporaneous β), **level differences** (negative-safe), **Open/Close only**.

| # | Spread | Construction | Daily bars | Role |
|---|---|---|---|---|
| 1 | **HDFC–ICICI** (BSE cash) | rolling lagged β (causal OLS, trailing W) | 5,543 | **DECISIVE** — canonical cointegrated MR pair |
| 2 | **Gold–Silver** (`GC2!`/`SI2!`) | rolling lagged β; roll-handled | 8,786 | **DECISIVE** — substitution cointegration |
| 3 | **USD/INR calendar** (`MIR1!`−`MIR2!`) | **β=1**; roll-handled | 3,344 | cleanest construction (reference) |
| 4 | Gold–Copper (`GC2!`/`HG1!`) | rolling lagged β | 8,786 | cohort |
| 5 | Platinum–Palladium (`TVC_PLATINUM`†/`PA1!`) | rolling lagged β | 10,261 | cohort (†trim composite to daily era) |
| 6 | WTI–Brent (`CFI_WTI`/`BRN1!`) | rolling lagged β; **post-2011 only** (2010 break) | 2,638 | cohort |
| 7 | TCS–INFY (BSE/NSE) | rolling lagged β; inner-join | 5,370 | cohort (cross-venue) |

Single-name deep legs (corn, cocoa, copper, …) are available for a separate single-instrument read; **not** part of
this spread-habitat verdict.

## 3. Descriptors (minimal; surrogate-relative)
- **Primary: VR(q) curve** over the **frozen grid q ∈ {2, 5, 10, 20}** (doc 14 — kept as a *curve*, **never
  `min()`-collapsed**), on the spread's level-difference returns. Heteroskedastic-robust (Lo–MacKinlay z\*).
- **Reported as REAL − MATCHED-SURROGATE, never raw** (red-team binding; doc 14/16). Raw VR is inadmissible.
- **Banned as evidence:** residual ACF, half-life, "did price come back" (smoother-manufactured; doc 06 C5 / doc 08).
  VR is chosen precisely because it lives in return space and escapes that trap.
- Secondary (context only): directional efficiency of the spread path. No score, no weighting, no label.

## 4. Pre-registered expectations (committed before results)
IF a genuine MR habitat exists in a spread, relative to its matched surrogate: **VR(q) lower (more sub-diffusive),
most clearly at intermediate q**. We do **not** assert this is true. Decisive instruments fixed now: **HDFC–ICICI and
Gold–Silver**. The MIR calendar is the cleanest-construction reference (if even a β=1 calendar shows nothing, that
bounds the instrument set, not the method).

## 5. Surrogate design & falsification framework (frozen)
- **Matched surrogate per instrument:** OU, RW, and GARCH(1,1) families, parameters estimated **causally** (trailing /
  pre-sample, never full-sample-tuned to mimic the real), **N = 200 draws each**, identical length, identical
  roll-handling, identical VR(q) extraction. The verdict compares real VR(q) to the **surrogate VR(q) ensemble**.
- **Decision rule (committed):** "MR habitat **confirmed** for instrument X" iff real VR(q) lies **below the 5th
  percentile** of X's matched-surrogate VR ensemble at **≥1 frozen horizon**, **robust** across (a) all three surrogate
  families and (b) roll-clean subsamples. Anything weaker = **not confirmed**.
- **KILL / strong-negative (committed):** if **no** spread in the cohort separates from its matched surrogate at any
  horizon → the **deployment-domain MR premise is seriously damaged** (a real, decision-changing negative, parallel to
  the State-T kill). If **both DECISIVE instruments** (HDFC–ICICI, Gold–Silver) fail to separate, the thesis is
  seriously damaged **even if** a cohort instrument squeaks through.
- **No re-story:** real effects pointing the wrong way (VR > surrogate) ⇒ weakened, **no post-hoc reinterpretation**.
  q-grid, horizons, surrogate families, N, and the 5th-percentile threshold are **frozen here**.

## 6. Hard guardrails (binding)
Causal (β and surrogate params use only data ≤ t−1; bit-identical future-injection acceptance test) · Distributional
(corpus verdict + effect sizes; no per-bar series, no "T" column, no timing) · Roll-handled (ADR_003; un-roll-handled
results inadmissible) · Surrogate-relative (raw VR inadmissible) · μ\*-independent (no Kalman/EMA residual; does not
trip §15.8) · No tuning (no parameter chosen to make separation appear) · No latent-state model (no HMM/ML).
**Banned vocab in code/docs/UI:** T-score, hazard, ignition, imminent, signal, entry, favorable-now.

## 7. Pre-run status — STOP
The cohort, construction, descriptors, surrogate design, and kill criteria are now frozen. **No VR(q), no surrogate,
no spread has been computed.** Execution (construct the 7 spreads per doc 13/ADR_003 → build matched surrogates →
compute VR(q) real-minus-surrogate → apply the §5 decision rule → write results with the four-layer separation) is a
**separate authorization**. Next high-information question: *do the decisive instruments (HDFC–ICICI, Gold–Silver)
separate from their matched surrogates in the MR direction?*
