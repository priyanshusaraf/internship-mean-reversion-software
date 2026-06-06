# DIRECTIVE — AMR Observatory & Paper-Trade Cockpit (Frontend Build Spec)

**From:** Project owner / Governor (strategy chat)
**To:** Claude Code / builder
**Status:** Frozen build spec. This defines the interface the owner steers the project from.
It must let the owner (1) load arbitrary CSVs, (2) **see every parameter**, (3) edit and
re-run, (4) **replay with the forward data hidden**, (5) **approve a market** before it
trades, and (6) do all of this **without ever breaking the causal/temporal firewall.** The
interface's job is to make the rigor *visible and enforced*, not optional.

---

## 0. ARCHITECTURE (non-negotiable, read first)

- **Next.js frontend + existing FastAPI backend.** The frontend is a **thin client**: it
  renders and steers; it does **NOT reimplement any statistic in JavaScript.** Every number
  (VR, half-life, habitat score, Kalman μ*, surrogates, signals, P&L) is computed by the
  **existing, frozen backend engines** (`analytics.py`, `analytics_arm_a_v2_beta.py`, the
  calibrated habitat score from `calibrate_habitat_score.py`, the trend-death module from
  `run_t2_5_trend_death.py`). **Single source of truth for the math = the backend.** A JS
  re-implementation would be a divergence/contamination channel and is forbidden — the only
  legitimate second implementation remains the cross-model adversary.
- Expose the engines as API endpoints; the frontend calls them. Cache results by
  (dataset, parameter-set, as-of cursor).
- **Performance lesson (from T2.5):** do not eagerly compute per-bar surrogate scores across
  a whole series. Compute habitat scores **on demand** for the selected window or for fire
  bars only; show loading states; cache aggressively.
- Charting: a real time-series library (lightweight-charts / Plotly / d3) with crosshair,
  overlays, and a draggable time cursor.

---

## 1. GUIDING PRINCIPLES — rigor baked into the UI

Every one of these is a *visible, enforced* property of the interface, not a convention:
1. **Temporal firewall.** Any *causal* computation uses only data ≤ the as-of cursor. The UI
   visually separates the **causal view** (what the model knew at t) from the
   **evaluation/full-information view** (forward data revealed). Forward/evaluation overlays
   are always marked "future — for scoring only, not available to the model."
2. **Surrogate-relative only.** The habitat score and any reversion read **always display the
   surrogate distribution they beat** (RW / MA(1)-bounce). Never a bare number; never
   self-ranked against the instrument's own history (that was the MRScore inversion bug).
3. **Raw-vs-deseasonalized always available**, with a contamination flag: if deseasonalizing
   changes the verdict, the UI warns (this channel voided BRN — doc 38a).
4. **Frozen-β enforced** for any spread: definitional β=1 or pre-sample-OLS-then-frozen.
   Rolling/online-β construction is flagged **INADMISSIBLE** in the UI and cannot be used for
   a gating read (f_βupdate must read ~0).
5. **Research mode vs Verification mode** (see §8): in Verification mode, pre-registered
   parameters are **locked** — no post-hoc tuning (invariant 6), enforced by the UI.
6. **Provenance on everything** (see §9): every chart/number carries its dataset, parameter
   set, as-of cursor, mode, and timestamp.
7. **Cost floor**: no "deployable / profitable" claim renders without net-of-cost expectancy.

---

## 2. DATA INGESTION — CSV upload (first-class; the owner has many files)

This must be robust; the builder already hit parsing failures (e.g. dd-mm-yyyy dates, unix
timestamps, close-only vs OHLC).

- **Upload one or many CSVs.** On upload, present a **column-mapping step**: user maps which
  column is the timestamp, which is close (and open/high/low if present), specifies the
  **date format** (auto-detect unix vs ISO vs dd-mm-yyyy, with manual override) and timezone.
  Remember mappings per file-shape.
- **Data-quality report on ingest** (mandatory, shown before analysis): row count, date
  range, inferred frequency (intraday/daily), **gaps**, **duplicate timestamps**,
  **non-positive prices** (the CL April-2020 negative-bars problem — flag and offer an
  excision window), NaNs, and any back-adjustment seams if detectable. Nothing proceeds on a
  silently broken series.
- **Dataset library:** loaded series persist in the session; the user switches between them,
  loads several at once (for cross-instrument and spread construction).
- **Resampling:** allow intraday → daily (last bar of day), as the AAPL 60-min case needed.
- **Spread construction:** select two legs → build a spread with a **frozen β** (β=1
  definitional, or pre-sample-OLS-then-frozen). Show f_βupdate. Reject/flag rolling-β. This
  is how LE-GF (LE − 0.565·GF) and any future pair are assembled.

---

## 3. THE CAUSAL FIREWALL + REPLAY (the heart of the rigor + the owner's replay vision)

- **Global as-of time cursor.** A draggable cursor on the main chart. Everything causal
  recomputes for "what was knowable at this instant." This is the **hide-forward-data**
  control.
- **Dual-mode view:** toggle between Causal (data ≤ cursor only) and Full-Information
  (forward revealed). In Full-Info, forward data is visually distinct (greyed/striped) and
  labelled as evaluation-only.
- **Replay:** a **play** button advances the cursor bar-by-bar; μ*, z, signals, and the
  habitat score evolve causally as it plays. Then reveal forward data to see what happened.
- **Replay-seduction guard (critical):** the replay must surface the **"did μ* stay put?"
  stability read** (μ* roam relative to price range), not just whether price round-tripped.
  "Price came back" is the seductive non-discriminator (a random walk round-trips by chance);
  "the equilibrium held a stable home" is the validated one. Show both, but make the
  stability read primary.

---

## 4. ANALYSIS PANELS

### 4.1 Equilibrium panel (Kalman μ* + the "Kalman read")
- Price with **Kalman μ\*** (2-state level+velocity) overlaid, causal.
- **Velocity state** (the estimated trend slope) as a sub-panel.
- **Innovation sequence + CUSUM break-detector** flag (structural-break signal).
- **μ\*-stability read** ("did μ* stay put") — the validated equilibrium-quality metric.
- **EMA vs Kalman μ\* side by side** (equilibrium comparison).
- **z-score** = (price − μ*)/σ with bands.
- Editable: Kalman process-noise / SNR knob — with a visible **warning** that an
  over-responsive filter manufactures fake reversion in its own residual (pin responsiveness;
  validate by stability, not by residual reversion).

### 4.2 MR habitat score panel (the deliverable — now built & calibrated)
- **Per-window habitat score** (0–100, surrogate-relative): select a window → score, shown
  **with the surrogate cloud** (RW + MA(1)/bounce nulls) and where the real min-VR sits.
- Underlying detail: **min-VR across q ∈ {5,10,20}**, the VR curve, the null distributions.
- **Habitat scanner:** rolling-window habitat score across the whole series, colour-coded
  over time — *where are the MR habitats?* (this is the owner's core "find the zone" view).
- **Calibration badge:** show the synthetic-gate status (OU=71.3, RW=49.2, trend=17.2 — the
  score is validated as non-inverting). If recalibrated, re-display.
- **Raw vs deseasonalized toggle** with the contamination flag.

### 4.3 Trend-death signal panel (Stage 1 — and the redesign happens here)
- Rolling/forgetting-factor trend overlay; show **slope β̂, t-stat, R², residuals**.
- **Signal overlay** marking fire bars, with **selectable operationalization**: (a) t-stat
  death + residual flip [the T2.5 primary, NO_CONTENT], (b) **R²-crossover**, (c)
  **recursive-residual CUSUM (Brown–Durbin–Evans)**. This panel is where Path-A redesign is
  done **visually**.
- **Fire-rate read, always visible** (T2.5 lesson: 18–20% is uselessly permissive; the owner
  tunes toward <5% by eye here before any formal pre-reg).
- **Discriminator sub-views:** residual one-sided runs vs zero-crossings; **curvature sign**
  (concave = pre-reversion vs convex = blow-off, via a t² term); vol-normalized residual.

### 4.4 Forward-scoring / evaluation panel (rigor)
- For a fired signal: forward-window **habitat score vs (a) unconditional base rate and
  (b) permutation null**, with the permutation distribution drawn, all marked
  **evaluation-only (future data)**.
- **Pre-committed pass/fail readout** (significance + effect-size floor) so results can't be
  cherry-picked; in Verification mode the criteria are locked.

---

## 5. PAPER-TRADE COCKPIT (Phase 3 — gated on LE-GF clearing its checks)

- **Live/replayed paper trade:** spread, μ*, z, **entry/exit/stop markers**, open positions,
  **P&L (realized vs modeled)**, drawdown, Sharpe, hit rate, **expectancy net of cost**.
- **Editable strategy params:** θ (entry, above breakeven), exit (mean-touch / time-stop =
  k×half-life), stop (regime-invalidation: μ*-roam, CUSUM break, hard |z| bound), sizing
  (deviation-scaled, vol-capped), cost assumptions, capacity cap.
- **Cost-floor gate:** "profitable" never displays without net-of-cost expectancy.
- **Approve-Market workflow (the owner's gate):** a market moves **Candidate → Reviewed →
  Approved → Live-Paper**. To approve, the owner reviews the habitat score, the replay, the
  backtest, and the linked pre-reg; approval is an explicit action with an **audit trail**
  (who/when/what params). Nothing trades paper without passing this gate.
- **Blotter / trade log.** First market loaded: **LE-GF** (LE − 0.565·GF, frozen β), with its
  caveats surfaced (deseason-dependent edge; gated on deseason-integrity + 2022–2026
  sub-period Sharpe ≥ 0.4).

---

## 6. CROSS-INSTRUMENT / PORTFOLIO VIEW
- Load multiple instruments/sleeves; compare habitat scores; **return correlation matrix**
  (the independence check, ρ); **joint left-tail / co-drawdown**; combined book Sharpe /
  capacity. This is the portfolio-combination view (doc 45) made interactive.

---

## 7. PARAMETER VISIBILITY + EDITABILITY (cross-cutting)
- **Every** parameter visible and labelled: Kalman SNR; trend window W; t-stat
  establish/dying thresholds; flip-window k; forward horizon H; VR q-set; surrogate counts;
  θ; exit/stop/sizing; cost. A single inspectable parameter panel per analysis.
- **Edit → immediate recompute** in Research mode.
- **Verification mode locks** any parameter that belongs to a frozen pre-reg (§8).

---

## 8. RESEARCH MODE vs VERIFICATION MODE (the anti-p-hacking guard)
- **Research/Exploration mode:** all knobs free; this is where the owner explores (e.g. tunes
  the trend-death operationalization and fire rate). Results are labelled "exploratory — not
  a verdict."
- **Verification mode:** load a **frozen pre-reg**; its parameters are **locked and
  uneditable**; the pass/fail criteria are fixed; the run is the official adjudicated result.
  This enforces invariant 6 (no threshold selection after results) *in the tool itself*.

---

## 9. PROVENANCE / PRE-REG / EXPORT
- Every chart and number carries: **dataset + hash, parameter set, as-of cursor, mode,
  timestamp.** Reproducible and auditable.
- **Link to the frozen pre-reg doc** for any Verification run.
- **Export** a configuration or result as a markdown doc that feeds back into the repo memory
  (single source of truth).

---

## 10. PHASING (deliver usable increments; don't ship a monolith)
- **Phase 1 — Observatory core:** §2 ingestion + §3 firewall/replay + §4.1 equilibrium +
  §4.2 habitat score & scanner. (This alone visualizes the working habitat score + Kalman and
  is immediately useful.)
- **Phase 2 — Signal + evaluation:** §4.3 trend-death panel (with the three
  operationalizations) + §4.4 forward-scoring + §8 modes. (This is where the Path-A redesign
  moves out of scripts and into the screen.)
- **Phase 3 — Cockpit + portfolio:** §5 paper-trade cockpit + approve-market + §6 portfolio.
  (Triggered when LE-GF clears its gates.)

---

## 11. WHAT THIS UNBLOCKS (why now, despite T2.5 = NO_CONTENT)
This is not dashboards over a void. Phase 1 visualizes a **working, calibrated** habitat
score and the Kalman equilibrium. Phase 2 is the **environment for the trend-death redesign**
— the owner *sees* the signal firing 1-in-5 bars, *sees* which instruments have real trend→MR
cycles, and tunes toward <5% fire rate before any formal pre-reg, instead of blind script
cycles. Phase 3 trades the one real edge (LE-GF). The mission redesign happens **inside this
tool**.

---

## 12. RIGOR CHECKLIST (must all be true in the shipped UI)
- [ ] Causal computations never see data > as-of cursor; forward data is visually marked
      evaluation-only.
- [ ] Habitat score always shows its surrogate distribution; never self-ranked.
- [ ] Raw-vs-deseason toggle present with contamination flag.
- [ ] Spread β is frozen; rolling-β flagged inadmissible.
- [ ] Verification mode locks pre-registered parameters.
- [ ] Every result carries full provenance.
- [ ] No "profitable" claim without net-of-cost expectancy.
- [ ] No statistic re-implemented in JS — all math from the frozen backend engines.

---

## NOTE ON SCOPE
This is the spec for the *interface*. It does **not** authorize new research verdicts — those
still run through pre-registration + named-agent + cross-model adjudication. The cockpit
*shows* and *steers*; it does not adjudicate.