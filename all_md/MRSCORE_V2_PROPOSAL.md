# MRScore v2 — "MR Habitat Characterization" — Redesign Proposal

**STATUS:** 2026-06-04 · RESEARCH-MODE PROPOSAL · implementation **NOT yet authorized** ·
synthesizer = research lead reconciling 7 lenses + adversarial red-team · governs §1–§12 binding.

> **EXECUTIVE THESIS.** MRScore v1 was specified as a habitat-compatibility *detection instrument*
> but its within-instrument percentile-rank architecture (eq. 14) made it a *self-ranked per-bar
> favorability scalar* that **inverts** (a pure random walk out-scores a genuine OU reverter, doc 09
> FINDING 1: NULL_RW 62.5 > OU 55.6) and is one downstream `threshold` away from a reversion signal
> (State-T resurrection, doc 11 DEAD). v2 replaces it with a **period-scoped, surrogate-relative,
> strictly-backward-looking effect-size VECTOR with no comparable scalar**: for a pre-registered
> window grid it characterizes *what a past window WAS* (sub-diffusive vs matched nulls) — never what
> a future window will be. The deployable object is a BOOK after costs, so a statistically-present
> but uneconomic habitat (the NG calendar, doc 23) is labeled PRESENT-BUT-UNECONOMIC, never
> "favorable." This is the doc-23 NG methodology generalized to user-selected windows, hardened by
> the adversary's guards. It is additive (new `analytics_habitat.py` + `/habitat` endpoint + one
> `HabitatObservatory` module), leaves v1 MRScore and the frozen μ* DAG untouched, and is structurally
> incapable — by endpoint refusal, not convention — of becoming a per-bar trigger.

---

## 0. Adjudication summary (where lenses disagreed, who wins, why)

| Dispute | Lenses split | **Verdict** | Why |
|---|---|---|---|
| Is a single headline scalar admissible (min-VR / count-tier / VR-gap)? | Research/Frontend/Arch/TS proposed one; Adversary killed all | **NO scalar of any kind** | Any ordinal sorts windows → one `ORDER BY` from favorability, one rolling recompute from a trigger. Adversary FATAL-1 wins. |
| Forward "conditional prior of future MR" framing | Mandate + most lenses kept it | **STRIKE it — backward-only** | "Recently reverted → likely to revert" is State-T with a coarser timestamp (Adversary CIRCULARITY-2). Object characterizes the PAST window only. |
| Selectable μ* estimator in the verdict path | 5 lenses wanted it | **ONE pre-registered default (robust median); alternatives understanding-mode only** | Selectability × window × q × partition = multiplicity exploit (§11.7). "Report all + flag flips" is not a guard. |
| Residual ecology as a verdict-feeding condition | TS/Regime allowed as 1 condition | **QUARANTINED — understanding-mode plots only, feeds NO count** | Circular (variance/ACF governed by same κ as reversion) + rolling-artifact-prone (doc-19 lesson at κ level) + redundant with VR/half-life. |
| Off-regime "no-trade map" actionable? | Trader/Regime called it most useful | **Ex-post, NON-ACTIONABLE** | doc 23 §3 Q4 explicitly ruled the avoid-gluts pattern inadmissible as ex-ante filter (needs separate causal regime classifier = State-T-adjacent, §10 out of scope). |
| Surrogate ensemble sufficiency | All used {OU/RW/GARCH/MA1} | **ADD mandatory splice/back-adjustment null** | doc 23 §4(c): NG sub-diffusion statistically indistinguishable from a vendor splice (p=0.84); no standard surrogate contains a roll-jump. |

The **Trader two-coordinate gate** (statistical-presence, net-of-cost) is the strongest surviving
*frame* because the economic coordinate kills "merely true" habitats — but it is presented as two
**labeled coordinates with CIs**, never collapsed to a sortable number.

---

## 1. Critique of current MRScore (drift evidence, classed)

- **[STRUCTURAL] Within-instrument self-rank inverts discrimination.** eq. 14 ranks each feature
  within its own trailing 252 bars. A uniformly-reverting OU's consistently very-negative DRC ranks
  mid (unremarkable vs its own history); a RW's wandering DRC throws high-rank excursions. Result: the
  self-ranked B2/MRScore does not separate reverters from nulls and inverts. *Evidence:* doc 09 §3
  FINDING 1 (NULL_RW 62.5 > ANCHOR_OU 55.6); `analytics_mrscore.py:52-60` `rolling_percentile_rank`;
  eq. 14 `rank(f within {f_{t-N}..f_{t-1}})/W×100`. There is **no null** in a self-referential rank —
  structurally inadmissible.
- **[MEASUREMENT] Raw Block-2 features unreliable on single windows.** ~10% of pure-RW 600-bar paths
  draw DRC < −2.0, overlapping genuine OU; BLIND_4 (pure RW) showed significant DRC in 97.7% of its
  windows vs BLIND_1 (OU) at 14.6%. Discrimination is an **expectation-level** property, not a
  single-window classifier. *Evidence:* doc 09 §3 FINDING 2, §8; confidence LOW for single-instrument use.
- **[IMPLEMENTATION] Per-bar point scores invite threshold-as-signal.** The endpoint returns a per-bar
  `MRScoreRow.mrscore` series (`market.py:495-505`), making `mrscore > 60 → go` trivial — contradicting
  the "structurally terminal, not a signal" freeze-break. The data *shape* manufactured the drift.
- **[METHODOLOGY] Frozen .20/.60/.20 + .50/.30/.20 weights applied globally per-bar without regime
  context.** A score of 60 means "top 60th pct of *this instrument's* recent history," not "favorable
  reversion regime." Defensible only for cross-habitat comparison (which the self-rank precludes).
  *Evidence:* doc 01 §3.2; doc 09 §3 FINDING 1.
- **[IMPLEMENTATION] Spread incompatibility surfaced as a "data_warning" hack.** Non-positive prices →
  log undefined → `market.py:480-488` emits a warning that conflates *structural incompatibility* with
  *unfavorable reading*. MRScore v1 cannot score its own intended deployment domain (spreads/pairs/RV,
  CLAUDE.md §1.1). *Evidence:* doc 09 §2 C1.

## 2. What object MRScore v1 ACCIDENTALLY measures now

A **within-instrument, relative-to-recent-history per-bar favorability scalar** that rewards a null's
wandering-statistic excursions over a genuine reverter's stable structure. It is neither a
cross-instrument reverter detector (no shared null) nor a habitat-compatibility probe (self-rank has no
null). At the right edge it is trivially read as "favorable now" — i.e. it accidentally measures the
exact thing CLAUDE.md forbids (a timing-adjacent favorability number), via the data shape, not intent.

## 3. Formal ontology of the v2 object — "MR Habitat Characterization"

**IT IS:** for a *pre-registered* window `[t0,t1]` of a named instrument, a **strictly-backward-looking
descriptive characterization** of whether the realized process over that window was *surrogate-relative
sub-diffusive* (OU-like: VR<1, bounded ACF decay, κ̂>0 vs matched nulls) — expressed as a **vector of
effect sizes with confidence intervals**, plus their **persistence across multiple disjoint windows**
and **regime-conditional structure**. The atomic unit of evidence is *"survives across multiple disjoint
windows AND beats its matched surrogate AND clears the economic floor,"* never *"looks favorable in one
window."*

**IT IS NOT:**
- a per-bar series, or any quantity indexed to the current/most-recent bar;
- a single comparable scalar / tier / count / min that can sort windows (KILLED — §0, Adversary FATAL-1);
- a *conditional prior of FUTURE mean reversion* (STRUCK — the forward tense is State-T with a coarser
  timestamp; we explicitly **disavow** any claim that habitat-membership raises the forward reversion
  prior — that claim is never tested here);
- a within-instrument self-rank (the v1 inversion bug);
- a timing/trigger/"favorable-now"/hazard/ignition/imminent/precursor object (banned vocab, doc 11,
  enforced in code/API/UI copy).

**Firewall vs State T (doc 11 DEAD).** State T asked "does residual morphology predict reversion?" —
answered NO. v2 never reads forward, never aligns residual shape to a future bar, never emits a tense.
The horizon-widening from 1 bar to a window does **not** make a forward claim observational; therefore
the forward claim is removed entirely. v2 answers only: *"was this past regime sub-diffusive vs a matched
null, persistently, and economically?"*

## 4. Mathematical redesign

**Drop entirely:** the 0.20/0.60/0.20 and 0.50/0.30/0.20 weights, the percentile-rank (eq. 14), and any
scalar collapse. **Zero free weights, zero fitted priors, no black-box ML.**

**Core construction (per pre-registered disjoint window `w_k`).** Generate `B ≥ 500` matched surrogate
paths per family, fit **causally on data ≤ t0−ε only** (never fit to the window under test — Adversary
CIRCULARITY-3). Run the real series and *every* surrogate path through **bit-identical** extraction.
Each diagnostic `d` becomes a surrogate-relative effect size with an attached null distribution:

```
z_d(w_k) = ( stat_d^real(w_k) − median_b[ stat_d^surrogate_b(w_k) ] ) / IQR_b[ stat_d^surrogate_b(w_k) ]
p_d(w_k) = empirical CDF position of stat_d^real within the surrogate ensemble   (calibrated p-value)
```

**Diagnostic panel (small, fixed, pre-registered).** Each is reported as `(z_d, p_d, CI)`, never blended:
1. **VR-gap (headline diagnostic, NOT a headline scalar):** `min_q VR_real(q) − median_surrogate VR(q)`
   over a *frozen q-curve* (q∈{2,5,10,20}), Lo-MacKinlay heteroskedasticity-robust, on **level-difference
   returns** (μ*-independent — escapes the smoother-manufactured-reversion trap, doc 06). This is the one
   statistic doc 21/23 proved discriminating and ~3% FPR-calibrated.
2. **Surrogate-standardized OU speed:** `κ̂ = −ln β̂` from AR(1) on the frozen residual, standardized by
   the surrogate-null κ̂ distribution (raw κ̂ is biased/noisy on short windows — never reported raw).
3. **Stationarity of the frozen residual:** ADF/KPSS reject-vs-surrogate-RW (one co-occurrence condition).
4. **Half-life in absolute bars,** reported with surrogate band and the tradeable 3–40 band overlaid.

**Aggregation — AND-gate of co-occurrence, NOT a weighted sum.** A window is *surrogate-relative
sub-diffusive* only when a pre-registered majority of independent diagnostics **each** clear their own
surrogate band. The reported objects are: the **vector** `{(z_d, p_d, CI)}`, a **persistence count**
(M-of-N disjoint windows clearing the band), and the **regime-conditional on/off map**. **No min, no
count-tier, no headline number** — the API/UI refuse to emit anything a downstream `ORDER BY` or
threshold can consume. Interpretable (each number is a named effect size vs a named null), causal (all
fits ≤ window start), falsifiable (must clear a pre-registered synthetic OU-vs-RW-vs-GARCH gate before
touching real data, §11.8).

## 5. Window-based observatory (period vs point)

**Decisively period-based.** Point/per-bar scoring is the v1 implementation drift and is statistically
empty on one bar. For `[t0,t1]` partitioned into a pre-registered set of disjoint sub-windows, the
trader-relevant period statistics are:
- **Persistence:** fraction of disjoint sub-windows clearing the surrogate band, with a binomial test
  (doc 23 template: NG 14/19 years below RW-median, p=0.032) — the *only* honest "percent-favorable."
- **Pooled effect size + cluster-robust t** across windows (doc 23: mean-z −0.627, t=−4.37, p≈0.0002).
- **Regime-fracture map:** count/location of sub-windows where VR≈1 (regime-off). doc 23's glut-year
  switch-off is positive genuineness evidence — but it is **ex-post and non-actionable** (§0, §10.OFF).
- **Half-life distribution and stability** (sd of κ̂) across windows; is it in the 1–12-week tradeable band.
- **Economic coordinate** (§10): net-of-cost edge — a real-but-uneconomic habitat is a non-finding.

The deliverable is a **period habitat-card**, never a time series of scores. Point reads survive **only**
inside the existing Replay module as a causal-honesty audit ("what was knowable at bar t").

## 6. Equilibrium anchoring redesign

**Design:** estimate `μ*(t0−ε)` from data **strictly < t0** (causal firewall §6.1), then **freeze** it
across `[t0,t1]` and compute all residual diagnostics against the frozen anchor. This removes the
moving-target contamination where an adaptive μ* chases price and mechanically shrinks residuals
(manufacturing fake stationarity — the residual analogue of doc-19 rolling-β VR inflation). **Default
estimator = robust median/trimmed mean** over the pre-window (fewest knobs). Kalman-terminal and EMA are
**understanding-mode comparisons only** and may **never change a verdict label** (§0 estimator ruling).

**Statistical coherence verdict:** coherent **conditionally**, with guards. The primary VR diagnostic is
deliberately **μ*-independent** (level-diff returns) so the headline does not inherit anchor
mis-specification; μ* enters only the residual stationarity/κ co-occurrence conditions.

**Adversary attacks → resolutions:**
- *Attack (staleness / fake reversion-to-a-corpse):* a frozen anchor on a window where the true
  equilibrium drifts manufactures a one-sided residual trend read as MR pressure. **Guard — regime-fracture
  invalidation:** if `μ*(t1−ε)` drifts from `μ*(t0−ε)` beyond a pre-registered band, the frozen read is
  **VOID** for that window. Freeze only within fracture-free, regime-homogeneous segments. (Note frozen
  anchor mis-spec biases *toward rejecting* MR — the safe direction — but a null on a long window is then
  uninformative; mitigated by reporting across window lengths.)
- *Attack (estimator selectability = DOF exploit):* killed — one pre-registered default in the verdict path.
- *Attack (anchor sampling error → CIs too tight):* **bootstrap `μ*(t0−ε)`'s sampling error INTO the
  surrogate band** (mandatory, not a footnote).
- *Attack (t0/L placement is a hidden hindsight knob):* `t0` and pre-window length `L` are part of the
  **pre-registered grid**, not analyst-chosen per read.
- *Attack (frozen-anchor artifact only cancels if surrogates are frozen identically):* surrogates anchored
  to the **same** `μ*(t0−ε)` from the **same** estimator on the **same** pre-t0 sample, via **bit-identical
  extraction** — a test-pinned invariant, not a written intention.

## 7. Residual ecology — VERDICT

**QUARANTINED. Understanding-mode, full-information, surrogate-relative descriptive PLOTS only. Feeds NO
aggregate/count/verdict.** (Adversary FATAL-4 + CIRCULARITY-1 win over the "one condition" lenses.)

- **Circular as proposed:** studying residuals "around realized reversions" conditions on the outcome —
  a realized reversion *is* `e_t→0`, so "residuals revert near reversions" is true by construction. The
  proposed fix ("use a disjoint second-moment feature, variance/ACF") does **not** de-circularize: in OU,
  variance compression and ACF decay are governed by the **same κ** as reversion. No genuinely disjoint
  residual feature exists without an **exogenous event channel + causal embargo**, which no lens specified.
- **Redundant:** κ-instability, residual persistence, half-life and VR are largely the same first-passage
  information; bundling them manufactures fake N-way confirmation from one fact.
- **Rolling-artifact-prone:** rolling OU-fit / rolling-κ are themselves rolling estimators (doc-19 β-noise
  lesson at the κ level) and would manufacture "instability" from estimation noise.
- **§11.5 firewall vs State T (explicit):** any wiring toward "predict reversion from residual shape" is a
  freeze-break requiring a **new §4 zombie-reopen pre-registration**. The residual-ecology panel is
  physically separated, badged "UNDERSTANDING — NOT CAUSAL," surrogate-relative, never future-aligned, and
  its redundancy with VR/half-life is disclosed (not independent corroboration). The single admissible
  *co-occurrence* contribution is **frozen-residual stationarity vs a matched RW surrogate** (item 3 of the
  §4 panel) — and even that is a stationarity test, not "ecology."

## 8. Automatic habitat discovery — FEASIBILITY

**Feasible ONLY as confirmatory scanning over a PRE-REGISTERED, EXOGENOUS partition with mandatory
multiplicity control — NOT as data-driven clustering/change-point search.**

- **Method:** (1) partition history into disjoint windows by a **single pre-registered exogenous regime
  key per instrument**, named with an economic mechanism **before any VR is computed** (doc 23 used
  storage-year because storage *is* the NG mechanism — justification per instrument, **not** a menu the
  analyst picks from — Adversary P-HACKING-2). (2) Run the surrogate-relative VR verdict per window.
  (3) Declare sub-diffusive **by persistence** (M-of-N below band), never by where the statistic peaks.
  (4) The regime label and its **predicted** off-condition are frozen *before* per-window VR (no HARKing
  the glut explanation — Adversary HINDSIGHT-2). (5) **Report the full search**, never the argmax.
- **Forbidden:** unsupervised clustering / HMM / unconstrained change-point search defining verdict
  windows (fake-clustering, maximal DOF, hindsight-labeling — §11.7/§11.8). Causal CUSUM change-point
  annotation is permitted **only** as a badged observational overlay that **cannot** define verdict windows.
- **Multiplicity:** the **entire knob cross-product** (window grid × q × partition key × instrument) is
  pre-registered as one correction family and FDR/maxT-corrected **jointly** — not "correct across windows
  after silently fixing the favorable estimator/q/partition" (Adversary P-HACKING-1).
- **Verdict:** YES via pre-registered exogenous partition + persistence + named regime-conditionality + joint
  multiplicity correction + full-search reporting; **NO** via any retrospective self-series clustering.

## 9. Statistical failure modes (each with its mandatory guard)

| # | Failure mode | Mandatory guard |
|---|---|---|
| F1 | Scalar collapse → sortable favorability → trigger | **No comparable scalar anywhere** in API/UI; labeled effect-size vector + CIs only |
| F2 | Period object recomputed rolling at right edge → per-bar signal | Endpoint **REFUSES** windows < pre-registered floor (≥5 estimated half-lives) **and** `t1` within a right-edge embargo → returns error, not a series |
| F3 | Self-referential rank (v1 inversion) creeps back | All stats absolute & surrogate-relative; **no percentile-within-own-history** anywhere |
| F4 | Argmax cherry-picking across windows/estimators/q/partition | Full knob cross-product pre-registered + FDR/maxT jointly; report full search; one default estimator; one partition key/instrument |
| F5 | Surrogate fit to the window under test → null too wide → under-reject | Surrogates fit on **pre-t0 data only**, independent adequacy checks |
| F6 | Frozen-anchor artifact fails to cancel | Surrogates anchored identically (same μ*, estimator, pre-sample) via **bit-identical extraction**, test-pinned |
| F7 | Anchor sampling error ignored → CIs too tight → over-reject → fake habitats | **Bootstrap anchor error into the surrogate band** |
| F8 | Frozen μ* on drifting equilibrium → fake reversion | **Regime-fracture invalidation**: void window if μ*(t1−ε) drifts beyond band |
| F9 | Back-adjustment/splice artifact read as MR | **Mandatory splice/roll-jump surrogate** in the ensemble + roll-seam admissibility gate; fail ⇒ "back-adjustment-suspect, inadmissible" |
| F10 | Residual-ecology double-counting / circularity / rolling-κ noise | Quarantined; understanding-mode plots only; feeds no count; redundancy disclosed |
| F11 | Short-window OU estimation (κ̂ biased below ~5 half-lives) | Min-window floor relative to estimated half-life; surrogate-standardized κ, never raw |
| F12 | Off-regime map used as ex-ante deploy/stand-aside filter | **Ex-post, non-actionable**; no UI affordance acts on current/latest window label (doc 23 §3 Q4) |
| F13 | "Confirmed" claimed without OOS/positive control | Only label = "candidate, single-habitat, unreplicated" until ≥1 matched-scale daily cross-habitat replication exists (doc 19 0/7; doc 23 Brent off-scale) **and** §11.8 positive control passes |
| F14 | Frozen-μ* deviation pane read as a per-bar reversion-pressure gauge | Equilibrium-relative pane is understanding-mode, **not co-located with the right edge**, no current-bar deviation readout |

## 10. Trader interpretation + EXACT workbench redesign

**What the trader reads (as a BOOK after costs):** for a selected period, an ordered two-coordinate
**labeled verdict** — `{statistically-present-AND-economically-viable | present-but-uneconomic | absent}` —
where coordinate 1 = surrogate-relative persistence/effect-size vector (did it beat matched nulls across
multiple disjoint windows) and coordinate 2 = **net-of-cost economic edge** (transaction cost, borrow,
capacity, sizing, adverse excursion; gross AND net; doc 23 trade-proxy reused verbatim). The economic
coordinate is **first-class and cannot be hidden**: the NG calendar is real but net-negative → labeled
PRESENT-BUT-UNECONOMIC, never "favorable." Neither coordinate collapses to a sortable number.

### Backend (additive, reuse-heavy)
- **NEW** `backend/app/services/analytics_habitat.py` — orchestrates existing primitives over a
  pre-registered window partition; returns the period habitat-card struct. **Reuse:**
  `analytics_arm_a_v2.py` (surrogate ensemble + min-VR + 5th-pct gate + pooled-mean-z — the FPR-calibrated
  engine; the habitat object *is* Arm A re-scoped to user windows), `analytics_mrscore.py`
  (`causal_zscore`, `drc_window`, `variance_ratios`/`variance_ratio_agg`, `newey_west_tstat`,
  `halflife_proximity` — but **DROP** `compute_mrscore`/`block2_score` self-ranked aggregator),
  `analytics.py` (`compute_halflife`, `_robust_return_scale`, Kalman/EMA for understanding-mode anchors),
  `synthetic.py` (null generators; **ADD** a splice/back-adjustment null), `store.py` `get_ohlcv`.
- **NEW endpoint** `GET /{instrument_id}/habitat?t0&t1&partition&seed` in `routers/market.py` (parallel to
  `/mrscore`, which stays untouched). Returns the **period struct only** (frozen μ* + provenance + bootstrap
  CI, per-window surrogate-relative vector with null bands, persistence array, regime-fracture/off-window
  list, half-life distribution, economic coordinate, pre-registration echo) — **never a per-bar series**.
  Enforces F2 refusals server-side.
- **NEW models** `HabitatPeriodResponse` etc. in `models/market.py`. **No** per-bar thresholdable scalar
  field; **no** banned vocab in field names.
- **Spread/signed path (principled, no log — §SPREAD consensus):** residual `e_t = S_t − μ*(t0−ε)` on the
  raw signed level; standardize by robust scale `1.4826·MAD(ΔS)` (the existing `_robust_return_scale`
  primitive); VR on **level-difference returns** `ΔS`; AR(1)-κ/half-life on level residuals. Affine,
  sign-safe, zero-crossing-safe — the proven β=1 calendar construction (doc 20/21, ADR_003). The v1
  `data_warning` log hack is **retired** (there is no log step to break). Positivity-requiring features are
  declared structurally inapplicable for spreads, not warned-as-unfavorable.

### Frontend (additive, 4-step add-a-module pattern)
- **NEW** `frontend/src/components/workbench/modules/HabitatObservatory.tsx`; register in `registry.ts`;
  add `api.getHabitat` in `lib/api.ts` (reuse `request<T>`); types in `lib/types.ts`. **Extend** `ModuleProps`
  with **optional** fields (`estimator`, frozen `period`/partition key) — backward-compatible, existing
  modules unaffected. Add window-partition control to `ResearchControls`; refactor `TimelineRail` to
  **bar-space** selection (fixes the calendar-day drift).
- **3-zone, period-first layout** (reuse `SubstrateCharacter` descriptors-first + `MRScore` right-panel
  patterns): TOP lightweight-charts pane (price / equilibrium-relative `d_t` with frozen μ* line + drift-shadow
  overlay + sub-window dividers; **no per-bar score overlay; not anchored to the right edge**);
  BOTTOM-LEFT Plotly small-multiples of the surrogate-relative effect-size vector **with visible 5th–95th
  null bands** (raw stats never shown without the band); BOTTOM-RIGHT period-stats strip (persistence %,
  binomial CI, regime-continuity, half-life band, frozen-μ* provenance stamp + economic coordinate).
- Residual-ecology and the full-search ledger are **separate, badged understanding-mode sub-views**
  (full-search ledger = all scanned windows, never an argmax leaderboard). **Replay** stays as the causal
  audit. v1 **MRScore stays registered, marked ARCHIVED/superseded** in its description.
- **One-way DAG preserved:** the module reads μ* and close, writes nothing back to μ*/RFI/sizing/State-T;
  frozen Kalman constants and frozen stack §8 untouched.

---

## 11. Smallest additive implementation roadmap (ordered, reversible)

1. **Pre-registration doc** (`docs/research/24_habitat_observatory_prereg.md`): window grid, partition key
   per instrument + named mechanism, q-curve, surrogate families (incl. splice null), B, seed, alpha,
   min-window floor, right-edge embargo, regime-fracture band, multiplicity family. *Reversible: doc only.*
2. **Synthetic discrimination gate (§11.8 power test)**: confirm the apparatus separates OU/RW/GARCH at the
   pre-registered alpha on synthetic ground truth **before** any real read. Reuse `synthetic.py` + Arm-A-v2.
   *Gate — if it cannot reject RW, recalibrate the apparatus, not the market.*
3. **`analytics_habitat.py`** orchestration over existing primitives; add splice/back-adjustment null to
   `synthetic.py`; bit-identical frozen-extraction + future-injection acceptance tests; anchor bootstrap;
   regime-fracture invalidation. *Additive new file + one new synthetic generator.*
4. **`/habitat` endpoint + Pydantic models**, with server-side F2 refusals and full-search/provenance echo.
   *Parallel to `/mrscore`, no edits to existing endpoints.*
5. **Frontend module** via 4-step pattern; extend `ModuleProps` (optional fields); refactor `TimelineRail`
   to bar-space; period-first 3-zone UI; mark MRScore superseded. *Additive; existing modules intact.*
6. **Real-data positive control** (§11.8): run on the NG calendar / a textbook cointegrated pair; must
   reproduce a known literature-anchored MR edge before any kill elsewhere is credible.

## 12. Immediate next coding tasks (first 3–5)

1. Write `docs/research/24_habitat_observatory_prereg.md` (window grid, per-instrument partition keys +
   named mechanisms, q-curve, surrogate families incl. splice null, B/seed/alpha, min-window floor,
   right-edge embargo, fracture band, joint multiplicity family). **Blocking** for everything downstream.
2. Add a **splice/back-adjustment surrogate generator** to `synthetic.py` (doc 23 splice-RW anchors
   frac∈{0.25,0.5}) + unit tests; this closes the F9 surrogate gap that the standard ensemble cannot.
3. Implement the **synthetic OU-vs-RW-vs-GARCH discrimination gate** as a standalone test harness reusing
   `analytics_arm_a_v2.py`; pin it as a CI acceptance bar (apparatus power before real data).
4. Scaffold `analytics_habitat.py` with `compute_habitat_period(close, partition, t0, t1, ...)` returning the
   period struct from existing primitives (no new estimators), with the bit-identical frozen-extraction +
   anchor-bootstrap + regime-fracture-invalidation + F2-refusal logic and a future-injection firewall test.
5. Add `GET /{instrument_id}/habitat` + `HabitatPeriodResponse` model (period-only, no per-bar field, no
   banned vocab), wired to `compute_habitat_period`, with the right-edge-embargo / min-window refusals.

---

## Pre-registration requirements (binding before any real read)

Window grid + per-instrument exogenous partition key (named mechanism, frozen before VR) + predicted
off-condition · q-curve · surrogate families (OU/RW/GARCH/MA1 **+ splice/back-adjustment null**) · B≥500 ·
seed · alpha · min-window floor (≥5 estimated half-lives) · right-edge embargo · regime-fracture band ·
default μ* estimator (robust median) · the **full knob cross-product** as one FDR/maxT correction family ·
commitment to **report the full search, never the argmax**.

## Real-data positive control plan (§11.8)

Before any negative/kill elsewhere is credible, the apparatus must **CONFIRM a known, literature-anchored,
economically-grounded real edge** at matched daily scale: the NG storage calendar (doc 21/23 conditional
survival) and/or a textbook cointegrated pair with a published MR result. An apparatus that cannot detect a
known real reverter cannot be trusted to have *not* found one elsewhere — recalibrate the apparatus, not
the market, on failure.

## Surviving uncertainty
- **Back-adjustment is not cleanly excluded** for the existence-proof case (doc 23 §4(c): NG mean-z −0.627
  statistically indistinguishable from a quarter-strength splice, p=0.84). The splice surrogate (task 2) is
  the test, not a guarantee; continuous-futures readings remain MEDIUM until it passes.
- **Zero admissible cross-habitat replications exist** (doc 19 0/7; doc 23 Brent off-scale/hourly). The
  central validity claim (persistence across *independent* habitats) is currently un-evidenced — hence the
  hard "candidate, single-habitat, unreplicated" label cap.
- Frozen-anchor mis-spec on long windows makes nulls uninformative (false-negative risk), partially
  mitigated by reporting across window lengths but not eliminated.

## Explicit non-conclusions
- v2 does **not** claim habitat-membership raises the **forward** reversion prior (that claim is removed,
  never tested here). · v2 does **not** provide a deploy/stand-aside timing filter (the off-regime map is
  ex-post, non-actionable). · v2 does **not** resurrect State T, MRScore-as-classifier, or any per-bar score.
  · A surrogate-relative-significant habitat is **not** deployable until it clears the economic coordinate
  AND a matched-scale cross-habitat OOS replication.

## Next highest-information empirical question
**Does the apparatus CONFIRM a known real edge at matched daily scale once a splice/back-adjustment
surrogate is in the ensemble — i.e. is the NG-storage sub-diffusion distinguishable from a vendor splice,
and does ≥1 independent cointegrated pair replicate it out-of-sample?** Until that is answered, every
"habitat" is a candidate, and no kill elsewhere is credible (§11.8).
