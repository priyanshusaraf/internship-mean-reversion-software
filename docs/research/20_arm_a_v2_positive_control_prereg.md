# Arm A v2 — Cycle 1: Real-Data Positive Control (Construction Ontology) — Pre-Registration

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **PRE-REGISTRATION + EXECUTION FREEZE (single document).** Fixes claim, cohort, construction,
surrogate ensemble, seasonality/microstructure controls, calibration gate, and decision rule **before the
formal verdict run**. Supersedes the §10 / doc-18 *rolling-OLS-β* habitat approach for this cycle; inherits
doc-18a's VR ontology, surrogate scaffolding, and multiplicity-corrected min-VR statistic verbatim where not
explicitly amended.
**Date:** 2026-06-04. **Mode:** Controlled-Implementation. **Governs:** Arm A v2, Cycle 1.
**Adversarial provenance:** this design was **hardened by a mandatory pre-freeze four-lens adversarial review**
(adversarial · statistical · trader/PM · research lead), each of which *ran the engine on the real series*.
Every CRITICAL/MAJOR finding below is incorporated. See §8 for the disclosure that the review **peeked at real
VR** (this is why the NG headline is *pilot-informed confirmatory*, not a-priori-blind).

> **Headline framing.** This is the **§11.8 real-data positive control**: before any further AMR *kill* is
> credible, the apparatus must demonstrate it can **CONFIRM a known, literature- and economically-anchored real
> edge.** The chosen edge is **storage/term-structure mean reversion in a commodity calendar spread** (Working
> 1949; Szymanowska et al. 2014; doc 15 rates this the strongest economic anchor in the deployment set). The
> primary instrument is the **natural-gas front calendar (NG m1−m2)**.

---

## 0. What this is NOT
Not State T. Not detection/timing/score/signal. No per-bar object, no "T" column, no banned vocab (T-score ·
hazard · ignition · imminent · favorable-now). Does **not** touch μ\*/Kalman/EMA residual (no doc-06 §15.8
trip). Not a tradeable-edge discovery: it is an **apparatus-validation gate**. NG is not proposed for
deployment; its storage MR is *assumed known a-priori from literature* and we test whether **our** apparatus
reproduces it for the **right reason** (genuine stochastic reversion, not seasonality / microstructure noise /
masking artifact).

## 1. Why v2 exists (prior thesis → falsification → new construction)
- **Prior (doc 18/18a):** habitat read via **rolling-OLS-β-on-levels**, W=60, with a leg-level log-return roll
  mask. **FALSIFIED-AS-INVALID (doc 19, HIGH confidence):** the β-update-noise term
  `(β_{t−1}−β_{t−2})·B_{t−1}` is 82–97% of Var(ΔS) and *manufactures* super-diffusion (VR≫1). Rolling-OLS-β
  on trending levels is **INADMISSIBLE** for VR habitat tests.
- **New construction (this doc):** restrict Cycle 1 to **β=1 DEFINITIONAL spreads** (calendars / same-unit),
  which carry **zero rolling-β DOF** and therefore cannot exhibit the v1 artifact (doc 19 §3 confirmed: the same
  legs are VR<1 under β=1). This simultaneously (a) fixes the construction and (b) furnishes the §11.8 positive
  control. The controlled/regularized-β re-test of genuine pairs is **deferred to Cycle 2** (§7), to avoid the
  §11.7 construction×instrument multiple-comparison surface.

## 2. The empirical claim under test (frozen)
> For the **β=1 NG front calendar** `S_t = NG_{m1} − NG_{m2}` (vendor pre-built, dense-era trimmed), does the
> level-difference variance-ratio curve `VR(q)`, `q∈{2,5,10,20}`, lie **below the 5th percentile** of its matched
> **RW, GARCH(1,1), AND MA(1)-microstructure-noise** surrogate ensembles (multiplicity-corrected min-VR), with
> `VR<1`, **AND survive causal deseasonalization** — i.e. does the apparatus confirm a *genuine, non-trivial*
> short-horizon stochastic mean reversion on a known storage reverter?

CONFIRM ⇒ apparatus validated (§11.8 gate satisfied). A *frozen-construction* NULL on NG is a **legitimate
terminal outcome** (see §6); it is read as apparatus-suspect **only** under the §6 two-sided rule, and even then
recalibration is permitted **only via the synthetic suite**, never by tuning to ng12/rb23.

## 3. Cohort & roles (frozen — pre-committed BEFORE the verdict run; §11.7 no argmax)
| # | Instrument | Series | β | Role | Pre-registered horizon expectation |
|---|---|---|---|---|---|
| 1 | **NG front calendar** (NG m1−m2) | `data/raw/ng12_spread.csv`, dense-era ≥ **2006-07-28** (n≈4969) | **β=1 definitional** | **PRIMARY positive control** | storage MR expected to appear at **q≤20** (front-month injection/withdrawal cycle is fast) |
| 2 | RB calendar (RB m2−m3) | `data/raw/rb23_spread.csv` (n≈5170) | β=1 definitional | **near-martingale reference (NOT a positive control)** | **expected NULL at q≤20** (back-month, weak short-horizon signal; any storage MR is multi-month, q≥60) |
| 3 | WTI–Brent | `data/raw/cl_brn_spread_60.csv` (hourly, n≈19399) | β=1 difference | **context only** | known-WEAK (v1: beat RW but FAILED GARCH, p=0.094); **cannot be substituted as the control** |

**Binding (§11.7):** NG is THE primary; RB and WTI–Brent are pre-committed as reference/context **before** the
run. The **full (instrument × q × family) matrix is reported**; no instrument may be promoted to "the control"
post-hoc by argmax. A RB null at q≤20 is the **expected, correct** outcome and is **not** apparatus failure.

## 4. Construction (frozen)
- **Headline = UNMASKED** level-difference VR on the vendor calendar **Close** (β=1; OHLC-2). Vendor pre-built
  calendars have **no leg-level roll seam** to remove; the v1 leg log-return mask is undefined on a zero-crossing
  spread. **[Review CRITICAL]** The transplanted increment-MAD jump filter (k=8, W=60) was *demonstrated* to
  delete ~35% of NG q=20 spans and flip NG VR(20) **0.45→0.94** — the v1 artifact at the mask level. Masking is a
  **one-sided lever toward VR→1** (it only deletes q-spans), so it can only *manufacture a false null*, never a
  false confirm.
- **Jump filter = ABLATION ONLY**, never the headline. Reported as a sensitivity sweep over **k∈{6,8,10,∞}**
  (∞ = unmasked). Verdict robustness is *reported*, not gated on the masked runs. If ever promoted, k must be
  calibrated on **synthetic** ground truth to be a no-op on no-seam data — never transplanted.
- **Dense-era trim (frozen deterministic rule, NOT result-selected):** NG trimmed to the first bar after both
  the last >7-calendar-day gap **and** the last non-finite close → **2006-07-28** (computed: n=4969, max gap 4d,
  0 non-finite). RB needs no trim (max gap 5d, 0 non-finite). The rule is frozen; the date is its output.
- **NaN closes dropped, never imputed**; counts reported. **Open series** carried for the open/close consistency
  cross-check (§5).
- **Causal firewall preserved (§6.1):** any trailing-window computation (deseasonalization mean, optional jump
  MAD) uses **only data ≤ t−1**; no bar t inclusion, no full-sample fit.

## 5. Surrogate ensemble & controls (frozen) — verdict gate amended from doc 18a
Inherited verbatim from doc 18a: **N=200** draws/family, identical length + mask + VR extraction (bias-cancel),
causal/pre-sample fits, **q∈{2,5,10,20}**, multiplicity-corrected **min-VR p-value** (real best-horizon VR vs
surrogate's OWN best-horizon null), **5th-percentile** gate, `real_min<1`. **Seed frozen = 20260604.** Amendments:

- **GATE = RW ∧ GARCH ∧ MA(1)-noise** (all three martingale-class nulls). **[NEW, review CRITICAL]** A pure
  RW + i.i.d. level noise (zero MR) produces VR<1 that RW/GARCH **cannot absorb** (demonstrated: corrected
  p=0.005 with zero MR). A vendor m1−m2 calendar inherits **bid-ask bounce / non-synchronous settle** of both
  legs → MA(1)-in-increments → spurious VR<1. The **MA(1)-noise surrogate reproduces the real increment ACF(1)**
  (NG ≈ −0.076) and a genuine confirm **must beat it**.
- **OU (AR(1)-on-level, pre-sample)** retained as a **non-gating stringency reference only.** Footnote: the
  pre-sample AR(1) does not model seasonality and is near-unbeatable by construction; "beats OU" is **not** cited
  as independent corroboration without the deseasonalization check.
- **SEASONALITY control (mandatory freeze condition, not optional):** report **deseasonalized VR** — subtract a
  **causal trailing-years month-of-year seasonal mean** (no lookahead) from the level before VR — alongside raw.
  A CONFIRM **must survive deseasonalization** (`VR_deseason(q*) < 1` and still beats the nulls). *(Direction
  note from statistical lens: a slow annual cycle biases VR **up** at q≤20, i.e. **against** confirming; a fast
  sub-annual cycle can fake VR<1. Requiring survival of deseasonalization neutralizes both faces.)*
- **Open/Close consistency cross-check:** report `VR` on the **Open** series beside Close. Genuine MR persists
  across the sampling point; bid-ask bounce does not. A confirm should be **consistent** open-vs-close.

## 6. Decision rule & the closed escape hatch (frozen) — amends doc 18 §5 / §11.8
- **CONFIRMED (apparatus validated)** iff **NG** real min-VR `< 5th pct` of **RW, GARCH, AND MA(1)** ensembles
  (multiplicity-corrected), `real_min<1`, at a horizon `q≤20`, **AND survives deseasonalization**, **AND** the
  synthetic calibration gate (§5a below) passed. Reported with the full matrix and the k-ablation.
- **NULL is a LEGITIMATE TERMINAL outcome.** **[Review CRITICAL — escape hatch closed]** A frozen-construction
  null is read as *"this calendar lacks beatable short-horizon level MR"* — a market/horizon fact — **NOT**
  automatically "apparatus broken." The §11.8 *recalibrate-the-apparatus* reflex is **gated**: it fires **only
  if** NG (strong literature prior at q≤20) nulls under the frozen construction **while the synthetic positive
  control (a true seasonal-OU calendar) still CONFIRMS** — proving the null is apparatus-horizon-mismatch, not
  market. **Even then, recalibration is via the SYNTHETIC suite only.** No post-result change to any frozen
  parameter (k, window, q-grid, N, seed, surrogate fits) fit to ng12/rb23 — that requires a **NEW
  pre-registration** (freeze discipline, §6 constitution). This converts a one-sided "heads-I-win" hatch into a
  genuine two-sided test.
- **No re-story:** real VR > surrogate ⇒ apparatus did not confirm here; recorded as-is.

### 5a. Synthetic calibration gate (frozen, MUST pass before the real verdict is credible)
**[Review CRITICAL — the adapter + MA(1) path is NEW; doc-18a's 1.7% FPR / 100% power does NOT transfer.]**
Re-calibrate on the new code path BEFORE reading the real verdict:
1. **True seasonal-OU calendar** (OU reversion + deterministic annual cycle) → **must CONFIRM** (power).
2. **True RW calendar** → **must NULL** at ≈5% (FPR), gate intact.
3. **RW + i.i.d. level noise** (zero MR, bounce mimic) → **must be CAUGHT by the MA(1) null** (NOT spuriously
   confirmed by RW/GARCH alone). This is the decisive new control: it proves the apparatus detects *MR*, not
   *noise*.
4. **No-seam no-op:** the jump filter at frozen k must **not** shift VR on a no-seam synthetic series.

If (1)–(4) do not all pass, the apparatus is recalibrated **on synthetic** until they do, **before** any real
read is treated as a verdict.

## 7. Cycle-2 trigger (named & date-boxed — §11.3 probation-is-not-limbo)
**Cycle 2 = controlled/regularized-β positive control on a textbook cointegrated pair with a *published* MR
result**, conditional on Cycle-1 NG CONFIRM. Rationale (trader lens): the deployment domain is **pairs /
cross-asset RV** (§1.1); a calendar-only control validates β=1 definitional spreads but **says nothing** about
the controlled-β construction genuine pairs require (the thing v1 showed rolling-OLS-β cannot do). Trigger date:
**immediately upon Cycle-1 verdict** (confirm → run Cycle 2; null → recalibrate per §6 first). Candidate
construction: rolling-cointegration (Engle–Granger) β on a long window with β-update explicitly controlled, or a
shrunk/regularized (Kalman-β) hedge ratio (registry DEFERRED item). Cohort #5 from `/arm-a` (crack spread) is
**DATA-BLOCKED** (no heating-oil/gasoline price leg locally; rb23 is a *calendar*, not a crack) — recorded, not
silently dropped.

## 8. Disclosure & epistemic provenance (binding, §5 constitution)
- **PILOT PEEK (disclosed):** the pre-freeze adversarial review **computed real VR on ng12/rb23** (NG unmasked
  ≈0.45 / deseason ≈0.31; RB ≈0.97–0.99) to *validate the design* (catch the filter-flip, the RB horizon
  mismatch, the seasonality direction). The design is correct **because of** this peek. Consequence: the NG
  headline VR is **pilot-informed confirmatory, NOT a-priori-blind.** The genuine **un-peeked** apparatus-
  validation weight rests on tests the pilot did **not** run on real data: the **MA(1)-noise null**, the
  **open/close consistency** cross-check, and the **synthetic FPR/power recalibration (§5a).** These carry the
  inferential load; the raw NG VR<1 alone does not.
- **Vendor construction (unaudited — flagged):** ng12/rb23 are opaque vendor "continuous calendar" series; the
  roll convention, back-adjustment status, and contract-month definition are **unknown** to us. Back-adjustment
  can mechanically lower long-horizon variance → fabricate VR<1. NG is therefore labeled **construction-
  unaudited**; evidential weight downgraded accordingly. (Mitigant: deseasonalization survival + MA(1) + open/
  close consistency target the most likely artifact channels.)
- **Stale-quote screen PASSED (recorded):** NG flat 0.77% / zero-incr 4.67% (max run 4); RB flat 0% / zero-incr
  3.04%. Both far from the USD/INR UNUSABLE artifact (75.6% flat / 14.4% zero). Not the USD/INR trap.

## 9. Frozen invariants preserved (§6)
Temporal firewall (all trailing computations ≤ t−1; no full-sample fit) · innovation/VR definition unchanged ·
no μ\*/Kalman touch · stack (§8) unchanged (numpy/pandas/scipy/arch/statsmodels) · v0 observatory posture
(distributional corpus verdict, no per-bar/detector/score). New code is **additive & isolated**
(`analytics_arm_a_v2.py` imports frozen primitives; the v1 `analytics_arm_a.py` leg path is untouched).

## 10. Pre-run status — FROZEN
Claim, cohort/roles, construction, surrogate ensemble (RW∧GARCH∧MA(1) gate + OU reference + deseasonalization +
open/close), calibration gate, decision rule, escape-hatch closure, Cycle-2 trigger, and disclosures are
**frozen as of 2026-06-04.** Execution = (a) build `analytics_arm_a_v2.py` additive module; (b) pass §5a
synthetic calibration; (c) run the §3 cohort, full matrix + k-ablation + deseason + open/close; (d) adversarial
verdict verification; (e) write `21_arm_a_v2_results.md`. **Next high-information question:** *does NG confirm
genuine stochastic short-horizon MR — beating the MA(1)-noise null and surviving deseasonalization — so the
apparatus is validated to detect a known real edge?*
