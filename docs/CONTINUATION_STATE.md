# AMR — Deterministic Continuation State

**Purpose.** Minimum sufficient project state for a fresh context window (post-`/clear`). Not a
summary — a handoff ledger. Read this + the files in §6 and you have lost nothing important.
Authoritative detail lives in the linked docs; this file is the index, not a second copy.

**As of:** 2026-06-02 · **Last cycle:** Kalman μ\* equilibrium research → Step 2A/2A.5 → provisional freeze; CLAUDE.md rewritten as operating constitution; **v0 stack resumed → REP (historical replay) built & survives; LAG (#12 lag-illusion) built → adjudicated → KILLED (C, medium) → de-registered & archived (doc 07); #11 (synthetic null testing) built → blind-adjudicated (F1–F5) → SURVIVES PROVISIONALLY (B) → closed & archived (doc 08). Equilibrium Observatory v0 formally CLOSED. **MRScore v1 built** as an observatory diagnostic (authorized narrow §10 freeze-break: observability ≠ productionization; structurally terminal) — engine faithful/correct, but discrimination reliable only *in expectation*, NOT single-window (doc 09). **Substrate Observatory v1 built** (same narrow freeze-break; the pre-State-T substrate layer — "what kind of market?"; planner+alignment-advisor adjudicated YES-with-guardrails) — engine correct/causal-firewall-proven; **key finding: substrate character is SCALE-DEPENDENT** — ADANIENT (macro trend-heavy) reads RW-Null at all causal windows 60–500 bars; v1 is high-specificity/low-sensitivity for OU (doc 10).** Project was in State T PLANNING only; **UPDATE 2026-06-03: State T existence is now CLOSED — FALSIFIED-IN-FORM / KILLED** (doc 11 Phase 5, 2026-06-02): high-|z| windows show directional continuation across 12 instruments / 5+ habitats (incl. the decisive HDFC–ICICI pair spread). Post-kill institutional review + ranked surviving arms in **doc 12**; immediate next action = **Arm 0 data provenance audit** (doc 12 §7). State-T DETECTION/timing remains FROZEN (the existence kill does not unlock it). · **CYCLE 2026-06-03b — DATA UNBLOCK + PHASE PIVOT:** deep real leg cohort arrived (`~/Downloads/mean-reversion-data`; audited → `data/mr_cohort_manifest.md`: **46 TRUSTED legs, 7 constructible causal spreads**) — the prior "0 trustworthy deployment-domain instruments" bottleneck is **resolved**. Waiting-period research package promoted (**docs 13–17**: spread protocol · temporal ontology · MR literature · morphology map · data acquisition; red-team in `waiting_period/red_team_critique.md`). **`ADR_003` roll-law filled** (TradingView `1!/2!` = NON-back-adjusted raw-stitched → roll-handling mandatory; `SI2!`/`GC2!` roll artifacts caught). **Arm A pre-registered (doc 18)** — VR(q) real-minus-surrogate habitat test on the 7 spreads, decisive = HDFC–ICICI + Gold–Silver, kill criteria frozen; **STOPPED before any VR(q) computed — execution is the next authorization.** Bottleneck flipped: data → running Arm A.

---

## 0. Frozen contextual invariant — ADANIENT is a PLACEHOLDER (read first)

**ADANIENT is a placeholder visual substrate, not deployment evidence.** It was loaded only for
live moving data — observability, debugging, runtime intuition. It is **economically out-of-scope**.

- **Deployment domain** = commodities · pairs · cross-asset relative value · spread structures ·
  mean-reverting environments.
- **Observed regime ≠ deployment regime.** ADANIENT is **trend-heavy** (single equity, ~100× ramp);
  deployment targets are expected to be **materially more mean-reverting** — the opposite regime.
- **Therefore, by default:** every **real-market** conclusion in this project (μ\* reversion fidelity,
  velocity-absorption reads, the **#12 LAG kill**, the #11 null scale-match) is **local to ADANIENT's
  trend regime and deployment-regime UNTESTED unless explicitly replicated** on a mean-reverting real
  instrument.

**Scope of this invariant (precise — do not over- or under-read):**
- It does **not** invalidate prior work and does **not** change any confidence class, verdict, or
  methodology. It changes **confidence *framing*** only: ADANIENT evidence is **not global evidence**.
- The **machinery is structurally instrument-agnostic** (engine, Kalman scale-normalization,
  synthetic validation harness, REP/RES/CMP as tools) — this invariant concerns **empirical
  conclusions and intuition**, not architecture.
- **Researcher intuition** built on ADANIENT (how much EMA lags, how often residuals revert, what
  equilibrium "looks like") is a **trend-regime prior**, not a neutral one — re-baseline on a
  reverting instrument (e.g. `ANCHOR_OU`) before trusting feel on deployment data.

**Reopen/correction trigger:** when a genuinely mean-reverting **real** instrument becomes available,
the real-market conclusions above are the ones to replicate first (see doc 06 §15 trigger, doc 07 §7
trigger). Source: post-#11 dataset-coupling audit (2026-06-01).

## 1. What is frozen

| Item | Why frozen | Confidence | Reopen trigger |
|---|---|---|---|
| **Temporal firewall / causal replay boundary** | Core research-validity invariant | HIGH | Never casually; freeze-break must be justified (CLAUDE.md §6) |
| **Kalman μ\* equations** (`x=[μ,v]`, `F=[[1,1],[0,1]]`, `Q=diag(κ·q_v,q_v)`, `κ=0.05`, SNR=1e-8, innovation residual `P_t−μ_{t|t−1}`, warmup 60) | Validated; mechanism analytic | HIGH | Evidence the equations are wrong (not the *verdict* — that already moved) |
| **Innovation residual definition** (pre-update one-step) | Verified (analytics.py) | HIGH | Same as above |
| **Technology stack** (CLAUDE.md §8) | Project decision | HIGH | Freeze-break w/ justification |
| **S2 / μ\* reversion-fidelity question** (06 §15, Rev 4) | Step 2A.5 cheap gate → class **B**, non-blocking; catastrophic false-centering (**C**) excluded | **LOW-MEDIUM** (single real underlying, R²ₒₒₛ≈0) | **PROVISIONAL** — re-open (run cross-instrument panel first) **before any upstream component depends on μ\* reversion fidelity**; descriptive/centering uses do not trigger |
| **EMA = production μ\*; Kalman = research-only comparison estimator** | Outcome of the above | MEDIUM-HIGH | A future cross-instrument result favoring Kalman |

## 2. What remains unresolved

- **Cross-instrument validation of μ\* reversion fidelity** — *non-blocking, deferred.* The Step 2A.5 panel could not run (only ADANIENT qualifies on disk; no data-fetch lib). This is the owed first step if μ\* is re-opened. Blocks nothing currently.
- **Δβ fine structure** (regime-dependent sign, R²ₒₒₛ≈0) — *non-blocking.* Below noise floor; would need the §13 surrogate-null + naive-detrend (S1) arms, deliberately not built.
- **§13 surrogate-null & naive-detrend arms** — *deferred.* Only justified if a cross-instrument panel first shows a repeated pattern.
- **`test_kalman_validation.py` assertion reframe** — *deferred, blocked on §13 verdict.* Docstring annotated; assertions intentionally unchanged (measurement lock, green).

## 3. Current implementation state (meaningful systems only)

**Backend (FastAPI, frozen endpoints under `/api/v1/market`):** `POST /load` · `GET /instruments` · `GET /{id}/ohlcv` · `GET /{id}/estimator` (EMA) · `GET /{id}/research` · `GET /{id}/diagnostics` (carries **both** EMA + Kalman fields) · `GET /{id}/velocity-absorption` (Step 2A ABS; read-only) · `GET /{id}/mrscore` (observatory diagnostic, read-only; per-bar, causal-only, EMA μ* descriptive — **structurally terminal**, not a signal; doc 09) · `GET /{id}/substrate` (substrate-character observatory, read-only; per-bar, causal-only; resemblance to 4 archetypes — **structurally terminal**, character-not-timing, not a signal; doc 10).

**Analytics (`backend/app/services/analytics.py`):** `compute_kalman_mu_star` (frozen) · `kalman_steady_state_gain` (Riccati, deterministic) · `_walk_forward_decay` (OOS 50/50 split) · `compute_velocity_absorption` (δ-decomposition; μ^K_pred recovered by subtraction, no filter recompute). Synthetic generators in `synthetic.py` (incl. `ou_in_trend`).

**MRScore analytics (`backend/app/services/analytics_mrscore.py`, NEW — one-way DAG, imports `analytics`, never imported back):** faithful eq. 13–34 — `causal_zscore` (shifted), `rolling_percentile_rank`, `realized_vol`/`vol_percentile`, Block-2 (`drc_window` w/ Newey-West HAC + h-trim, `hit_rate_window`, `variance_ratios`), Block-1 (`mean_stability`, `variance_stability`, `adf_kpss_pvalues`), Block-3 (`hl_proximity_value`/`halflife_proximity`, `vol_compression`, `tcf_score` c-free), `compute_mrscore`. Tests: `tests/test_mrscore.py` (32, green incl. bit-identical firewall). **MRScore HL band uses `/ln 4` (prose-consistent; eq. 28 `/ln 2` is a doc typo — doc 09 §2).**

**Substrate analytics (`backend/app/services/analytics_substrate.py`, NEW — self-contained on raw OHLCV; imports nothing from μ*/Kalman/MRScore, never imported back; re-derives its own vol helper to keep the two observatories independent):** 3 causal descriptors — `directional_efficiency` (trend↔chop axis, |net|/path ∈[0,1], survives sign changes), `variance_ratio_mean` (OU↔RW axis, log-price VR over q∈{2,5,10}), `realized_vol_percentile` (context only, never a character driver) — plus `character_scores` (pure, pointwise, frozen, monotone, hand-set-threshold map → 4 resemblance scores `ou_like/trend_like/rw_null/ambiguous` + `dominant`/`confidence`; **no fitting/HMM/DL**) and per-bar `substrate_descriptors`/`compute_substrate`. **Hurst removed** (window/method-sensitive — the "easy to hallucinate" estimator). **Causal-only** (full-info = one-line window swap, deferred). C1 non-positive/spread `data_warning` (VR log-undefined) mirrors MRScore. Models: `SubstrateRow/Stats/Response`. Tests: `tests/test_substrate.py` (25, green incl. bit-identical firewall + 3 habitat-discrimination). **Map-design correction caught mid-build (MEASUREMENT, doc 10 §2): first map let VR≈1 misread deterministic trends as RW — rebuilt DE-primary (drift adds to mean not variance, so VR cannot carry the trend axis).**

**Frontend (Next.js 15) workbench modules (active):** EST · RES · **REP** (Replay, v0 #10; causal scrub, local cursor over prefetched diagnostics — no backend, leans on prefix-invariance) · **CMP** (EstimatorCompare, Step 1) · **ABS** (VelocityAbsorption, Step 2A; Surface 3 raw-only, no verdict engine) · **MRS** (MRScore, `modules/MRScore.tsx`; MRScore(t)+B2 vs price, B1/B2/B3 contribution + feature-rank decomposition + RAW DRC/hit/vr discriminators, crosshair as-of-t readout, prominent regime-warning gate, NO verdict language) · **SUB** (SubstrateCharacter, `modules/SubstrateCharacter.tsx`; **descriptors-first** — DE/VR sparklines + descriptor cards primary, resemblance scores subordinate behind a toggle; causal-only; prominent character-not-timing gate, NO verdict language; doc 10) · ASM · DIF · LOG. Registry: `frontend/src/components/workbench/registry.ts`. Shared smoother util: `frontend/src/lib/smoothers.ts` (`centeredMA`, used by REP). **LAG (#12) de-registered — KILLED**, see below.

**REP design (frozen for v0):** `frontend/src/components/workbench/modules/Replay.tsx`. Fetches `/diagnostics` once for the active window; a **local row-index cursor** reveals prefix `[0..t]` and re-fits the chart so it renders exactly as it would have at bar t (price + causal EMA μ\* always; causal Kalman μ\* toggle, default off). Interaction = scrub/step/jump only (no autoplay, by design). **Hindsight track** = a **client-side centered moving average** (half-width ⌊span/2⌋) over the *full* fetched prices — genuinely uses future bars, default OFF, dashed amber, explicit "not knowable at t" warning strip + `μ* lag` readout. No whole-window stats during scrub (single as-of-t readout only). Kalman shown descriptively → does **not** trip the μ\* reopen trigger.

**LAG (#12) — CLOSED, verdict C-KILLED (MEDIUM), see `docs/research/07_lag_illusion.md`.** Instrument worked (frozen identity `ε_c = ε_h + L`, exact); the *research layer* did not earn a permanent place. Decisive kill **K2 (REP redundancy):** *material lag = obvious in REP; non-obvious lag = immaterial* (`corr(|ε_c|,|slope|·price)=0.897`; `corr(|slope%|,s)=0.18`). **K3:** the load-bearing **Mode B** (lag-manufactured false reversions) is **rare** on ADANIENT (2 of 20 largest episodes; large reversions predominantly *honest*) — EMA μ\* less dangerous than feared. K1/K5 did not fire (lag common+material) but those cases are Mode A (REP-visible). K4 weakened (localization bandwidth-sensitive; qualitative story survives). **Disposition:** de-registered from workbench nav; `LagIllusion.tsx` retained **inert** (not deleted); `smoothers.ts` retained (REP uses it). **Reopen trigger (frozen):** only if a genuinely **range-bound real instrument** becomes available — then re-run the *exact* K1–K5 adjudication; no redesign/no new methodology otherwise. **#12 does NOT block upward movement in the stack.**

**#11 (synthetic null testing) — CLOSED, verdict B — SURVIVES PROVISIONALLY, see `docs/research/08_synthetic_null_testing.md`.** Load-bearing question: *can a researcher distinguish genuine reversion from mechanical pseudo-reversion using only REP/RES/CMP?* Guardrail (frozen): "ε reverts on a RW" is expected mechanics, **not** a kill — the test is DISCRIMINATION. Frozen modification: **no variance-ratio / metric discriminator** — REP-first, visual, blind. **Zero new endpoints, zero new frontend** — nulls are ordinary instruments through `/diagnostics`. Built & retained: `synthetic.drift_random_walk` (N2; `random_walk`=N1, `ou`=A0 reused) + `backend/scripts/generate_nulls.py` + `tests/test_synthetic_nulls.py` (3 metric-free construction tests, green). **Materialized in live DB:** labeled `NULL_RW`/`NULL_DRIFT`/`ANCHOR_OU` + blind `BLIND_1..5` (sealed `blind_key.json`). Scale-matched to a **scale-stationary 600-bar window** (idx 650–1250, 2015-06→2017-11, max/min≈2.6×) — full-history constant-σ arithmetic RWs go negative/tiny vs the real 100× ramp (scale/sign confound); frozen arithmetic form preserved (n never frozen); disclosed positivity filter (orthogonal to reversion). **Blind result:** isolated the single genuine reverter (BLIND_1=A0/OU) and called **zero nulls reverting**; the seduction case (BLIND_3, round-trip RW) was flagged *uncertain*, **not** seduced into "reverting." **F1–F5:** F1 SUPPORTED (discriminator = *equilibrium stability*, NOT residual reversion), F2 SUPPORTED (no fooling basin; but round-trip near-basin mechanism is real), F3 SUPPORTED-conditional (REP/CMP correct; **RES autocorr/half-life mislead on a RW** — doc 06 C5, do not trust blindly), F4 SUPPORTED-weakened (replay did not seduce, but exerted measurable pull), F5 SUPPORTED-conditional. **Why B (not A, not C):** discriminated cleanly with no false positives → not C; but conditional on discipline + real seduction surface + RES-stats vulnerability + n=1 packet → not A. **Frozen institutional warnings:** (a) don't trust RES persistence metrics blindly (smoother-manufactured); (b) ask *"did the equilibrium stay put?"*, not *"did price come back?"*. **Not a μ\* reopen** (descriptive/null use; EMA stays production μ\*). **All findings architecture-level or ADANIENT-substrate-conditioned — never global market claims.** Reopen only on cross-substrate ambiguity / deployment-domain contradiction / F1 weakening (doc 08 §9). **#11 does NOT block upward movement.**

**Finding surfaced during REP (IMPLEMENTATION/MEASUREMENT class — not a μ\* reopen):** there is currently **no genuine future-using ("full-information") μ\* track** in the system. `analytics.compute_full_ema` is `ewm(adjust=True)` — a warmup-normalization variant that uses *no* future data and converges to causal EMA after ~3×span; its docstring ("the causal estimator is 'behind' hindsight") and the `/diagnostics` "look-ahead gap" framing are **misleading**. This is a latent gap against the frozen Dual-Information invariant (CLAUDE.md §6.2, which requires every major computation to support a real Full-Information mode). REP's hindsight surface is the *only* genuine full-information μ\* view that now exists, and it is client-side. **Open decision (not actioned):** whether to (a) correct the misleading `compute_full_ema` docstring/`/diagnostics` wording, and/or (b) add a real backend full-information μ\* (e.g. RTS smoother) to satisfy §6.2. Flagged, not resolved.

**Tests:** full backend suite green (**120**); `test_velocity_absorption.py` (4: identity, matched-span, causal firewall, OOS finiteness); `test_kalman_validation.py` (measurement locks, annotated); `test_mrscore.py` (32); `test_substrate.py` (25).

**Data on disk:** ADANIENT (2463 bars, real, only one ≥3×matched-span≈423) · NIFTY_SYN (500, synthetic) · NIFTY50 (246, too short). No market-data fetch capability installed.

## 4. What must NOT be revisited (settled — do not re-litigate)

- **The KC4/KC1 "REJECTED" verdict (05 memo)** — overturned (confounded synthetic reading); 05 carries a SUPERSEDED banner. Do not resurrect the rejection *or* re-run that debate.
- **"Centering" as a decision criterion** — DEMOTED to a necessary-but-insufficient, confounded diagnostic (06 §12). Do not re-promote it.
- **Three-residual confusion** — there are only **two** residual systems (ε^K velocity-ON, ε^R velocity-OFF) bridged by δ; ε^R ≡ matched-span EMA prediction residual. Do not invent a third series.
- **Verdict engine on ABS Surface 3** — intentionally absent; raw numbers only. Do not add interpretation language.
- **Frozen ADRs:** `001_local_first` · `002_temporal_integrity` · `003_roll_adjustment`.
- **Deferred complexity (v0):** State T, execution, signal engine, regime classifiers, HMMs, ML, real-time infra — out of scope until explicitly authorized.

## 5. Observatory status & next layer

**Equilibrium Observatory v0 is effectively COMPLETE.** Frozen observatory status:
```
REP (#10)            survives
LAG (#12)            KILLED (C, medium) — doc 07
Synthetic Null (#11) survives provisionally (B) — doc 08
μ* (Kalman line)     provisional / non-blocking — doc 06
```
The observatory **stayed lean** and survived adversarial testing **conditionally** (see doc 08 §5:
discipline required, seduction surface exists, RES-stats vulnerability, n=1 packet). None of these
block upward movement.

**Diagnostic observatories built since (separate layers, both narrow §10 freeze-break, both structurally terminal):**
```
MRScore v1 (MRS)            BUILT — engine HIGH; discrimination in-expectation only, NOT single-window — doc 09
Substrate Observatory (SUB) BUILT — engine HIGH; CHARACTER not timing — doc 10
```
**Substrate Observatory v1 status (doc 10):** the pre-State-T substrate layer ("what kind of market?"),
adjudicated this session by research-planner (TAXONOMY-NEXT=YES) + alignment-advisor
(CONSISTENT-WITH-GUARDRAILS). Engine faithfulness/causal firewall **HIGH**. **Finding 1 (STRUCTURAL,
MEDIUM-HIGH):** substrate character is **scale-dependent** — ADANIENT (macro trend-heavy) reads
**RW-Null at every causal trailing window 60–500 bars** (drift adds to mean not variance → diffuses
like RW at sub-multi-year scales) → reinforces §0 (ADANIENT local≠global). **Finding 2 (MEASUREMENT,
MEDIUM):** v1 is **high-specificity/low-sensitivity for OU** — the frozen map yields OU>RW only when
VR<0.75; mild-but-genuine reverters (ANCHOR_OU, VR~0.85) read RW-Null. Deliberate conservatism (the
MRScore anti-hallucination lesson); **NOT retuned**. **Reopen triggers:** (1) does a multi-window
("scale-axis") substrate read beat any single W? (2) is VR<0.75 the right OU gate for the deployment
domain — needs a **mean-reverting REAL instrument**; must **NOT** be tuned on ADANIENT. Terminal:
feeds nothing into μ*/MRScore/gates → no μ* reopen. Does NOT block upward movement.

**▸ UPDATE 2026-06-03 — the marker below is OVERTAKEN BY EVIDENCE.** State T existence was tested
(doc 11 Phases 3–5) and **KILLED (FALSIFIED-IN-FORM)**: high-|z| windows show directional *continuation*,
not stabilization, across 12 instruments / 5+ habitats incl. the canonical MR pair spread. The project did
NOT advance into State-T model logic; it redirected **down to the foundation** — see doc 12 (post-kill
review). Surviving arms, ranking, and the authorized next action (Arm 0 — provenance audit) live in
`docs/research/12_institutional_review_post_state_t.md`. State-T detection/timing remains FROZEN.

**▸ TRANSITION MARKER (SUPERSEDED — preserved for provenance).** The project is transitioning from
**observatory / epistemics** toward **model logic — specifically State T**. The **substrate layer
beneath State T is now built** (SUB, doc 10) — the adjudicated prerequisite (State T is
substrate-conditional; you cannot characterize "transition from X" without characterizing X). This
remains a **planning marker only**: State T research/planning may continue; **State T implementation
remains deferred** (CLAUDE.md §4 phase discipline, §10 v0 scope). No execution, no signal engine, no
regime classifiers, no detection/timing. Remaining untouched v0 item that does *not* depend on Kalman
and stays inside the observatory line: interval selection (#9) (CLAUDE.md §10).

**Researcher chooses the specific target** (avoid roadmap drift — do not auto-pick). **Hard
boundary:** State T *implementation* / signals / execution remain deferred. Do **not** wire anything
to Kalman μ\* *reversion fidelity* without first tripping the §1 reopen trigger (cross-instrument
panel). EMA μ\* is the stable foundation downstream work builds on.

## 6. Mandatory reading path after `/clear`

**Must-read (start here, in order):**
1. `CLAUDE.md` — the operating constitution (identity, modes, invariants, workflow). Governs all behavior.
2. `docs/research/18_arm_a_habitat_preregistration.md` — **← CURRENT FRONTIER.** Frozen pre-registration of the Arm-A VR(q) real-minus-surrogate habitat test on 7 causally-constructed spreads (decisive: HDFC–ICICI, Gold–Silver). Pair with `docs/research/13_canonical_spread_protocol.md` + `ADR_003` (construction law) and `data/mr_cohort_manifest.md` (the audited legs). **Next action = execute it** (construct → surrogate → VR(q) → §5 decision rule). Waiting-period package = docs 13–17.
2b. `docs/research/12_institutional_review_post_state_t.md` — post-State-T-kill institutional review (what survives/fails, ranked arms, roadmap). Arm 0 (provenance audit) is DONE → `data/cohort_manifest.md` (old cohort) + `data/mr_cohort_manifest.md` (deep cohort).
3. `docs/research/11_state_t_existence.md` — **the State-T kill record** (Phases 3–5; FALSIFIED-IN-FORM 2026-06-02). Read before any impulse to revisit State T (zombie prohibition).
4. `docs/research/06_kalman_equilibrium_research_update.md` — **active living record** of the Kalman μ\* line; read §12–§15 + revision history for current state.
5. This file — current state index.

**Optional reference (read when the task touches them):**
- `docs/research/02_mu_star_equilibrium.md` — equilibrium foundations.
- `docs/architecture/software_architecture_v1.md` — system shape.
- `docs/decisions/ADR_00{1,2,3}` — frozen decisions (local-first, temporal integrity, roll adjustment).
- `docs/research/01_amr_framework.md`, `03_state_t_report.md`, `04_state_t_conditional_relevance.md` — framework + (deferred) State T.
- `docs/research/07_lag_illusion.md` — **#12 LAG kill record** (read before any impulse to rebuild a lag-illusion layer; it was tested and killed — REP suffices on available evidence).
- `docs/research/08_synthetic_null_testing.md` — **#11 synthetic-null verdict (B — survives provisionally)** (read before trusting any reversion read: the discriminator is *equilibrium stability*, not residual reversion; do not trust RES persistence stats blindly).
- `docs/research/09_mrscore_observatory.md` — **MRScore v1 build record + discrimination finding.** Engine faithful/correct (HIGH); **discrimination reliable only in expectation, NOT on a single instrument/window** (self-ranked score inverts; raw DRC ~10% false-positive on nulls). Read before reading any single MRScore value as evidence: it is observational/descriptive, within-instrument relative, NOT a signal. Single-substrate (ADANIENT-scale), n=1 blinds.
- `docs/research/10_substrate_observatory.md` — **Substrate Observatory v1 build record + scale-dependence finding.** The pre-State-T substrate layer ("what kind of market?"). Engine/causal-firewall HIGH. **Substrate character is SCALE-DEPENDENT** — ADANIENT reads RW-Null at all causal windows 60–500 bars (macro trend invisible at trailing-window scale; reinforces §0 local≠global). v1 is **high-specificity/low-sensitivity for OU** (OU>RW only at VR<0.75; conservatism intended, not retuned). Read before reading any single substrate read as a regime claim: it is window-resemblance (character, not timing), NOT a signal/detection. Reopen on a mean-reverting real instrument (VR<0.75 OU-gate adjudication) or a multi-window read.

**Archival only (do not read unless auditing history):**
- `docs/research/05_kalman_v1_results_memo.md` — superseded Rev-0 verdict (banner explains).

*Optimize continuity over volume: items 1–3 are sufficient to resume productively.*
