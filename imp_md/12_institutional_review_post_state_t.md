# Post State-T Institutional Research Review & Arm-0 Pre-Registration

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **REVIEW — institutional state assessment after the State-T existence kill (doc 11, 2026-06-02).**
Reconstructs what survives / fails / is unresolved, adjudicates the four candidate directions, ranks the
surviving research arms, and **pre-registers Arm 0 (the data provenance & quality audit)** as the authorized
next action. No new empirical claim is made here; this is Research-Mode synthesis + an audit pre-registration.
**Date:** 2026-06-03.
**Mode:** Research Mode (review). Arm 0 §7 is a Controlled-Implementation pre-registration; execution is a
separate authorization.
**Scope:** the whole programme as of the State-T kill. Synthesises docs 01–11 + a direct on-disk data audit +
an external literature pass + an adversarial (red-team) pass. Produces no scores, no signals, no detection.

> **▸ CONTEXT (placeholder framing — frozen).** ADANIENT is a trend-heavy **placeholder**; the deployment
> domain (commodities · pairs · cross-asset RV · spreads) is expected materially more mean-reverting. Every
> real-market conclusion here is **regime-local, not global** (CLAUDE.md §1.1; `CONTINUATION_STATE.md` §0).

---

## 0. Provenance of this review

Synthesised 2026-06-03 from: a direct read of the decisive falsification record (doc 11) and the two state
docs (SESSION_BRIEF, CONTINUATION_STATE); four institutional sub-reviews (two repository-historian digests of
docs 01/03/04 and 06/09/10; a literature-team evidence brief; a red-team adversarial pass); and a first-hand
audit of `data/raw/`. Where a claim rests on a sub-review it is attributed; where it is a Chief-Scientist
judgment that diverges from a sub-review, that is stated.

---

## 1. State assessment — where the programme stands

**The structural diagnosis.** The programme pursued *when* tradeable reversion ignites (State T) **before** it
established *where* reversion robustly exists, on *trustworthy data*. The State-T kill, read with the data
audit (§4 Arm 0), exposes that inverted ordering as the central problem. The corrective is **downward to the
foundation, not forward to the "true object."**

**The kill is real, clean, and STRUCTURAL** (doc 11 Phase 5). State-T-as-pre-window-stabilization
(innov_var↓ / acf1↓ / dir_eff↓ in high-|z| causal pre-windows) is **FALSIFIED-IN-FORM** across
**12 instruments / 5+ habitats / 2–3 resolutions / 2 comparison methods / 3 θ**, with `dir_eff` **positive in
all 12** — directional *continuation*, the opposite signature — **including the pre-registered DECISIVE
instrument** (HDFC–ICICI pair spread, the canonical MR habitat). The positive control fired correctly
(dir_eff≈−0.9 on a true stabiliser under identical anchoring) so the method is demonstrably not blind; a null
adversary reproduced the *entire* result with **selection-on-deviation** (anchoring on |z|≥θ samples
extreme-endpoint = directionally-efficient paths) + ordinary momentum, requiring **zero** State T. Confidence
the tested formulation reflects a real phenomenon in any tested habitat: **~5–10%**.

**Independently corroborated by the literature.** Continuation around large deviations is the *expected* result
at the tested horizons — George–Hwang (2004, 52-week-high momentum: reversals do *not* occur at extremes);
Jegadeesh–Titman (1993, intermediate underreaction). Conditioning a sample on extreme |z| is the Lo–MacKinlay
(1990) cross-autocovariance selection trap. **The negative result is textbook, not anomalous.**

## 2. Survives / fails / unresolved

**DEAD — do not resurrect (zombie prohibition, CLAUDE.md §4):**
- State-T as pre-window stabilisation morphology (STRUCTURAL kill, doc 11 Phase 5).
- **CSU (κ↑ / AR(1)↓ / Var↓) as the *identity* of reversion** — demolished *analytically* in doc 04 §1.5
  independent of the empirical kill: `Var(ε)=σ²/(1−ϕ²)` makes AR(1)↓ and Var↓ "one fact stated twice"; the
  one independent leg is a *volatility* signal; Δκ sits below the estimation noise floor at the unit root
  (SD(κ̂)≈0.08–0.09 vs κ≈0.02–0.05). (STRUCTURAL + MEASUREMENT.)
- "Centering drives usability" as a μ* decision criterion (DEMOTED, confounded — doc 06 §12).
- Self-ranked MRScore as a reverter-detector — it **inverts** (a pure random walk scored highest, 62.5 vs
  ANCHOR_OU 55.6; doc 09 §3, STRUCTURAL).
- The post-|z|-peak "aftermath" window **as a rescue of State T** — its one-shot license is **SPENT**
  (alignment ruling, doc 11 Phase 5).

**UNTESTED — alive in principle, NOT dead:**
- The broad post-deviation-dynamics idea (~40–50%, doc 11 Phase 5) — only one morphology was probed.
- **Etiology-conditioned reversion** (inventory/flow → reverts; information repricing → continues) — doc 04's
  "single most consequential omission," never stratified. *Best-grounded principle in the programme* per the
  literature (Hendershott–Menkveld inventory ~0.92-day half-life; Nagel reversal-as-liquidity-provision;
  Campbell–Grossman–Wang volume→reversal) — **but real-time causal etiology identification is unsolved and the
  required data is absent** (§4 Arm D).
- Whether the deployment-domain instruments are *genuinely* mean-reverting — their MR character was **never
  separately verified** (doc 11 explicit non-conclusion); their large-deviation episodes looked like the trend
  control.

**FROZEN-but-alive — binding constraints untouched by the kill:**
- Temporal firewall; Kalman μ* equations/constants; v0 scope; the validation discipline (purged CV, surrogate
  nulls, pre-registered kill criteria, "stopping is a success").
- **State-T detection / hazard / transition-timing remains FROZEN.** The existence kill does NOT unlock it.
- **The μ* reversion-fidelity reopen trigger** (doc 06 §15.8, verbatim): nothing may depend on Kalman/EMA
  residual *reversion fidelity* until a genuine cross-instrument panel — *including a verified mean-reverting
  instrument* — is run first. Descriptive/centering use does not trigger it.

**The load-bearing epistemic rule governing all reversion work** (doc 08 §7; doc 06 C5): residual reversion and
residual ACF/half-life are **smoother-manufactured** (a pure RW's EMA residual shows ACF≈0.88, half-life≈6).
The validated discriminator is **equilibrium stability — "did μ* stay put?"**, not "did price come back?".
Return-space variance-ratio is the one core statistic that escapes the trap.

## 3. Verdicts on the four candidate ideas

| Idea | Verdict | Reason |
|---|---|---|
| **Adaptive MRScore** | **REJECT** the adaptive / time-varying / per-bar-"NOW" form | Re-imports two falsified priors: the self-ranked score that inverts (doc 09), and the conditioning penalty (Goyal–Welch 2008; doc 04 lesson 3: unconditional beats conditional OOS). A per-bar "favorable NOW" score is also the frozen per-bar/timing object (doc 11 §1). |
| | *salvageable remnant* | Cross-instrument / surrogate-null-relative **distributional** discrimination (doc 09 §7 fix) survives — but it is no longer "MRScore," it **is habitat discovery** → folded into Arm A. |
| **Multi-horizon time handling** | **SPLIT** | As *characterisation* — report VR/DRC as a **curve over horizon** instead of `min()`-collapsing — **YES** (Lo–MacKinlay VR is inherently multi-horizon; character is horizon-dependent, doc 10). As *adaptive weighting* — **NO** (conditioning penalty). |
| **Morphology discovery** | **PURSUE — only surrogate-relative & pre-registered** | Theory-free trawling on |z|-anchored windows rediscovers selection-on-deviation as a "finding" (red-team). Constrained to "what exceeds a matched OU/RW/GARCH surrogate under identical anchoring," it is genuinely falsifiable. |
| **Habitat discovery** | **PURSUE — highest EV — gated on Arm 0 first** | The one return-space (non-smoother-trap), observatory-legal, machinery-exists direction; logical prerequisite for everything else. Blocked by leg-stripped spreads of unknown provenance (§4 Arm 0). |

## 4. Surviving research arms (PART-6 format)

### ARM 0 — Data provenance & quality audit *(precondition; pre-registered in §7)*
- **Problem.** Every cross-instrument conclusion rests on instruments whose trustworthiness is unverified. The
  on-disk "spreads" are **precomputed single `close` columns — the legs are gone** (verified §4.1); if any used
  a full-sample hedge ratio it is **stationary by hindsight construction** and cannot be told from the file.
- **First-principles thesis.** You cannot characterise "which markets mean-revert" on instruments that may be
  stationary by lookahead. Provenance is upstream of every statistic.
- **Supporting literature.** McLean–Pontiff (2016): published edges decay 26–58% (provenance/survivorship
  dominate). Do–Faff (2010/2012): non-converging pairs rose post-2002.
- **Adversarial critique / failure modes.** The audit may conclude *most of the cohort is unusable* — itself a
  critical finding, not a failure. Mis-inferring spread provenance from value range; treating descending dates
  as corruption when intentional. Mitigation: where provenance is unrecoverable, default **CONTAMINATED**, not
  trusted.
- **Cheap falsification plan (3–5 days).** §7. Output a **trusted-cohort whitelist** + per-instrument manifest.
- **Expected value.** Gates Arms A/B/C against silent contamination. Highest value-per-day in the programme.
- **Recommendation: PURSUE IMMEDIATELY.**

### ARM A — Habitat discovery (unconditional, surrogate-relative, multi-horizon VR characterisation)
- **Problem.** Which on-disk instruments are genuinely mean-reverting, at which horizons, *distinguishably from
  a matched null* — the deployment premise everything depends on.
- **First-principles thesis.** Spread/term-structure MR is economically anchored (cointegration; Szymanowska
  et al. 2014 term premia); "is this OU-like?" is answerable in *return space* where the smoother trap does not
  bite.
- **Supporting literature.** Lo–MacKinlay (1988) VR (inherently multi-horizon; VR<1 = MR); pairs/commodity-
  spread MR real-but-decayed (GGR 2006; Avellaneda–Lee 2010; Do–Faff). Report VR as a *curve over q* with
  heteroskedastic-robust stats; avoid point Hurst (fragile).
- **Adversarial critique.** Scale-dependence multiplies researcher DOF (VR(short)≠VR(long)); short samples
  (HDFC–ICICI = 503 daily bars) give κ/VR CIs straddling the gate; negative-price spreads break return-VR
  variants; selection-on-deviation re-enters *iff* habitat is stratified by high-|z| anchors → characterise
  **unconditionally**.
- **Failure modes.** Tuning the VR<0.75 OU-gate on ADANIENT (forbidden — wrong regime, doc 10); calling
  503-bar noise a "ranking."
- **Cheap falsification plan (2–3 wks).** Extend the existing Substrate engine to multi-window VR curves;
  compare each *trusted* instrument to its **own matched OU/RW/GARCH surrogate** under identical extraction;
  pre-register expected-OU instruments. **Kill condition:** if no instrument separates from its matched null at
  any horizon → the deployment-domain MR premise is in serious trouble (decision-changing negative result).
- **Expected value.** Establishes (or refutes) the foundation; finally adjudicates the VR<0.75 gate on a
  *verified* reverter; absorbs the only salvageable piece of "adaptive MRScore."
- **Recommendation: PURSUE after Arm 0.** Highest research EV.

### ARM B — Morphology discovery (surrogate-relative, separately pre-registered)
- **Problem.** Beyond "they continue," is there *any* real structure in large-deviation morphology that a
  matched null does not already produce?
- **First-principles thesis.** The kill answered "do they stabilise?" (no). The unanswered, higher-information
  question is "is real == surrogate?" Yes → favorability premise is in deep trouble; No → the deviation is the
  seed of a *new* pre-registered hypothesis (the only legitimate State-T successor).
- **Supporting literature.** Continuation-at-extremes predicted (George–Hwang; Jegadeesh–Titman); overreaction-
  reversal appears only at high volume / long horizon (Campbell–Grossman–Wang; De Bondt–Thaler) — concrete
  surrogate-vs-real contrasts.
- **Adversarial critique (decisive).** "Observe without theory" is unfalsifiable and is the zombie vector;
  |z|-anchored full-info windows are selection-on-deviation by construction; "understanding only" is a label,
  not a firewall against back-channelling hindsight into causal design.
- **Cheap falsification plan.** **Pre-register a surrogate morphology taxonomy first** (what classes do
  OU/RW/GARCH produce under identical |z| anchoring); count only real morphology that *exceeds surrogate
  frequency*. Quarantined, full-information, no back-propagation into causal features.
- **Expected value.** Either kills the favorability premise cleanly or yields the only legitimate State-T
  successor hypothesis.
- **Recommendation: PURSUE after Arm A** identifies OU-like instruments. Without the surrogate pre-registration
  it collapses to storytelling → then REJECT.

### ARM C — Kalman cross-instrument panel *(reframed; conditional — DEFER)*
- **Problem.** Does Kalman μ* track equilibrium better than EMA across instruments — *only relevant if*
  something downstream will consume residual reversion fidelity.
- **Adversarial critique (decisive).** "Does Kalman ε revert better than EMA ε?" is the **wrong, smoother-
  contaminated question** — a faster-adapting μ* *mechanically* manufactures a more-reverting, lower-variance ε
  (the lag illusion, doc 07; doc 04 §1.5.4), and the frozen P3 perturbation test cannot catch a systematic
  bias. The right discriminator is **equilibrium stability**, with frozen constants (per-instrument refit = a
  §6.3 freeze-break).
- **Recommendation: DEFER.** The freeze is non-blocking and *nothing currently depends on it* (MRScore /
  Substrate are terminal/descriptive). Reopen only when a concrete downstream consumer is proposed — do not
  solve a problem nothing has.

### ARM D — Order-flow / etiology *(north star; data-gated — DEFER + spec the unlock)*
- **Problem.** Condition reversion-vs-continuation on deviation *cause* (inventory/flow → reverts; information
  → continues).
- **Assessment.** *Most promising principle, most impossible execution.* Literature grounds the principle
  strongly; red-team + data audit agree it is **unbuildable now** — OHLC-only, most spreads volume-less, no
  tick/OFI/OI/COT/options; daily/60m bars alias the ~1-day-to-seconds flip; inferring etiology from price is
  outcome-conditioning (circular); violates v0 scope.
- **Recommendation: DEFER and specify the unlock** — signed order flow OR OI/positioning on a flow-driven
  instrument. Highest-value *future* arm. *(A bounded volume→reversal observational probe à la
  Campbell–Grossman–Wang is possible on the few volume-bearing instruments — note only, not an arm.)*

## 5. Ranking

| Rank | Arm | Sci. merit | EV | Tractability | Falsifiability | Impl. cost | Net |
|---|---|---|---|---|---|---|---|
| 1 | **Arm 0 — Provenance audit** | — (enabling) | Very high | Very high | n/a | Very low | **Do now** |
| 2 | **Arm A — Habitat discovery** | High | High | High | High | Low–Med | **Primary** |
| 3 | **Arm B — Morphology (surrogate-relative)** | High | Med–High | Med | High *(iff pre-registered)* | Low | **After A** |
| 4 | **Arm C — Kalman panel (reframed)** | Med | Low *(no consumer)* | Med | Med | Med | **Defer** |
| 5 | **Arm D — Order-flow / etiology** | Highest | Highest *(ultimately)* | **Zero now** | High | **Blocked** | **Defer + spec data** |

## 6. Recommended 30–60 day roadmap

- **Phase 0 (Days 1–5) — Foundation hygiene.** Continuity corrections (§8, done); run **Arm 0**; emit the
  trusted-cohort whitelist. *Gate: which instruments are trustworthy?*
- **Phase 1 (Days 5–25) — Arm A.** Multi-window surrogate-relative VR characterisation across the trusted
  cohort; pre-register expectations; adjudicate the VR<0.75 OU-gate on a *verified* reverter (never ADANIENT).
  *Gate: does any real instrument distinguish from its matched null? If no → stop and escalate to data
  acquisition.*
- **Phase 2 (Days 25–50) — Arm B.** Only on Phase-1-confirmed OU-like instruments: pre-register a surrogate
  morphology taxonomy, then characterise real-vs-surrogate large-deviation morphology (full-info, quarantined).
- **Phase 3 (Days 50–60) — Decision gate.** Either (a) verified habitat + surrogate-exceeding morphology →
  draft a **new, independently pre-registered causal hypothesis** (the legitimate State-T successor, alignment-
  reviewed); or (b) no verified habitat / real==surrogate → **honest stop**, and the binding constraint becomes
  **data acquisition** (a real mean-reverting instrument *with legs* + flow data), which also unblocks Arm D.

## 7. ARM 0 — executable pre-registered plan (the authorized next action)

**Objective (frozen).** Produce a **trusted-cohort whitelist** — the subset of on-disk instruments whose
cross-instrument statistics may be believed — by auditing provenance, sample adequacy, and hygiene **before**
any reversion/habitat statistic is computed.

**Non-goals.** No reversion statistics, no scoring, no habitat verdict (Arm A). No new market-data acquisition.
No signal/timing. (This audit must not itself become a covert habitat read.)

**Pre-committed disposition rules (fixed before running, so the whitelist is not post-hoc):**
- **TRUSTED** — (raw single-asset OR spread with *confirmed causal/rolling* hedge ratio) AND `usable_bars ≥ 3×`
  the largest downstream trailing window (commit: ≥ **750** daily-equivalent bars for multi-window VR up to
  W=250) AND monotone date ordering AND documented price-sign/units.
- **PROVISIONAL** — raw single-asset, adequate bars, with a *fixable* hygiene flag (e.g. reversed dates).
  Usable after the fix is applied and re-checked.
- **CONTAMINATED** — spread/derived series with **full-sample or unverifiable** hedge ratio → OU-character is
  lookahead-suspect → **excluded from any OU/habitat verdict** (may still feed null-relative *continuation*
  checks that assume no stationarity).
- **UNUSABLE** — `usable_bars` below the power floor (commit: < **504** daily bars for any single-instrument MR
  verdict), unrecoverable date/format corruption, or degenerate columns (all-NaN, O=H=L=C runs).

**Method (executable; Bash/Python, no new deps):**
1. **Schema audit** — per file: header, dtypes, row count, OHLCV+volume presence, null/zero counts.
2. **Date hygiene** — detect ascending/descending ordering and format; **fix reversed ordering** (`g1_gold`,
   `ng12_spread`, `rb23_spread` flagged); compute true span, infer resolution, flag gaps.
3. **Provenance** — per spread: are legs present anywhere on disk / in any metadata? Infer construction from
   value range/sign. If hedge-ratio causality is **not verifiable → CONTAMINATED** (conservative default).
4. **Sample adequacy** — `usable_bars` vs the committed floors; flag the **15m/1d twins** (HDFC–ICICI,
   EURUSD) as pseudo-replicates (sample-uniqueness violation — never double-count in a "panel").
5. **Price-sign / units** — flag instruments requiring **level-difference (not log/return)** math; confirm
   every Arm-A statistic is log-free (negative-price-safe).
6. **Emit** `data/cohort_manifest.{md,json}` — per-instrument `{disposition, reason, usable_bars, resolution,
   neg_price, provenance}` + the whitelist of instruments Arm A may compute OU-verdicts on, and an explicit
   call on whether **any** instrument qualifies as a candidate verified reverter (or the honest finding that
   none do).

**Success criteria (committed).** A reproducible manifest with a disposition + reason per instrument; the
explicit Arm-A OU-verdict whitelist; explicit identification of the candidate mean-reverting instrument(s) or
the honest "none qualify."

**Failure modes of the audit itself.** Treating bar-volume presence as quality; assuming descending dates are
corruption; mis-inferring provenance from range. Mitigation: record inferences *as* inferences; unrecoverable
provenance defaults to CONTAMINATED.

**What it gates.** Arm A (habitat) and any future Arm C/D cross-instrument work. Estimated cost **3–5 days**.

## 8. Continuity corrections applied (2026-06-03)

Two state docs were stale on the State-T kill and were corrected (no history erased; corrections marked):
- **SESSION_BRIEF.md** §1.3 + "Where We Are / What's Next" / "honest single next action" — they still framed
  State-T existence as the *unanalysed active frontier* and prescribed running the existence probe; doc 11
  (Jun 2) already carried the **FALSIFIED-IN-FORM / KILLED** verdict. Corrected to point at doc 11 + this doc;
  next action repointed to Arm 0.
- **CONTINUATION_STATE.md** "As of" header + §5 transition marker — predated the kill ("State T PLANNING
  only"). Corrected to record the kill, its reopen triggers, and Arm 0 as the next action.

**Next high-information question:** does any *trusted* on-disk instrument separate from its matched null in
return-space VR at any horizon (Arm A) — i.e. does a verified mean-reverting habitat exist on the data we have?
