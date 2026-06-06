# MASTER DIRECTIVE — AMR Strategy & Backtesting Interface (Observatory v2)

**From:** Project owner / Governor (strategy chat)
**To:** Claude Code (orchestrator) + build subagents
**Status:** Frozen master build spec. Companion to
`DIRECTIVE_OBSERVATORY_COCKPIT_FRONTEND.md` (the observatory panels) — read both together;
this master prompt adds the **backtesting engine, the strategy/signal layer, the
P&L/metrics widgets, the manual-regime workflow, and the build orchestration.** Where this
conflicts with momentum toward "a fully automatic regime-gated algo," **this wins.**

---

## 0. THE LOAD-BEARING CONSTRAINT (read before anything)

**Regime *timing* detection is NOT done.** T2.5 (doc 47) returned NO_CONTENT — the
trend-death trigger has no cross-instrument content. Therefore:

- **Regime CHARACTERIZATION** ("how MR is this window?") = the **habitat score**, built and
  calibrated (OU 71 / RW 49 / trend 17). **This works — use it.**
- **Regime TIMING / TRANSITION detection** ("when does the trend die?") = **does not exist
  yet.** Do **NOT** build automatic regime-gated signal generation as a live feature.

**What the interface does instead:** the user **marks regimes manually** (hide forward data,
identify where the market turns, mark the MR zone), the **habitat score confirms** the zone
is genuinely MR, and **deterministic z-band signals** trade *within* a confirmed/marked zone.
Automated regime-gating is a **pluggable module hook** that goes live only when a detector
passes validation (future phase). Build the hook, leave it empty.

---

## 1. WHAT WE BUILD NOW vs WHAT IS GATED

**Build now (this directive):**
1. Observatory (companion doc): ingestion, causal firewall + replay, equilibrium (Kalman),
   habitat score + scanner.
2. **Backtesting engine** (event-driven, walk-forward, cost-aware) — §4.
3. **Strategy/signal layer** for MR (z-band entry/exit, half-life-derived holds) — §3.
4. **P&L / metrics widgets** (TradingView-style, rigor-wrapped) — §5.
5. **Manual-regime workflow** (hide-forward → mark zone → habitat-confirm → trade) — §6.
6. **LE-GF paper-trade cockpit** (companion doc §5), once LE-GF clears its gates.

**Gated (future, do NOT build now):**
- Automatic regime-gated signal generation across a whole series (needs a validated
  detector). Build the **interface hook** for it; leave the detector slot empty.
- Any "fully automatic algo from wherever data is selected" framing.

---

## 2. RIGOR GUARDS — the anti-overfitting wrapper (non-negotiable)

A TradingView-style tweak-and-watch-the-equity-curve interface is an overfitting machine.
These guards stop it from undoing the project's discipline:

1. **Research mode vs Verification mode.**
   - *Research:* all params free; localStorage-backed drafts; results labelled
     **"EXPLORATORY — not a verdict."**
   - *Verification:* params loaded from a **frozen pre-reg**, **locked/uneditable**, criteria
     fixed, backend-pinned with full provenance. The official result.
2. **The headline number is honest, the seductive one is secondary.** The prominently
   displayed metric is **out-of-sample, walk-forward, net-of-cost** expectancy/Sharpe. The
   in-sample equity curve is shown but visually secondary and labelled in-sample.
3. **Walk-forward by default.** Backtests split IS/OOS; report both; never present an
   in-sample-only curve as the result.
4. **Range-selection is exploratory.** A backtest on a user-hand-picked range is labelled
   selection-biased exploration; a verdict requires pre-committed criteria or OOS.
5. **Derived defaults, not hand-tuned.** Hold ≈ 2× half-life; entry θ from breakeven cost.
   Tunable only in Research mode; Verification uses the pre-committed values.
6. **Cost floor.** No "profitable" anywhere without net-of-cost. Costs editable but every
   result re-states the cost assumption used.
7. **localStorage scope:** Research drafts + UI prefs + **reset-to-base** only. Verification
   params are backend-pinned, never localStorage.
8. **No statistic re-implemented in JS** — all math from the frozen backend engines (single
   source of truth; a JS reimplementation is a contamination channel).

---

## 3. STRATEGY / SIGNAL LAYER (MR strategy, within a confirmed zone)

- **Equilibrium:** μ* from the chosen estimator (Kalman level, or causal mean/EMA for a
  spread with an economic anchor). z = (price − μ*)/σ.
- **Entry signal:** |z| > θ, θ defaulted **above breakeven cost** (computed from cost & σ).
- **Exit signal:** z → 0 (mean-touch) **or** time-stop at **≈ 2× half-life** (half-life from
  the OU fit), whichever first.
- **Stop:** regime-invalidation — μ* roam exceeds bound, CUSUM break fires, or |z| widens
  past a hard pre-committed bound without reverting.
- **Sizing:** deviation-scaled, **vol-capped** (suspend in top-decile vol), capacity-bounded.
- Signals only generate **inside a regime the user has marked MR (or a future validated
  detector has gated)** — never blindly across the whole series.
- Every parameter visible and editable (Research mode); defaults derived.

---

## 4. BACKTESTING ENGINE (the new core logic)

- **Event-driven:** bar → signal → position change → simulated fill (with slippage/cost) →
  P&L accrual → metrics. Causal only (no lookahead); forward bars never inform a decision.
- **Period-scoped:** the user selects a date range (like the habitat-score window selection)
  to backtest over; the engine runs the strategy across that range. **Exploratory** unless run
  in Verification mode on a pre-committed range/criteria.
- **Walk-forward harness:** IS/OOS split (and optionally rolling walk-forward); report both
  separately; OOS is the verdict number.
- **Cost model:** editable per-instrument (commission, slippage, spread); every output
  re-states the assumption.
- **Outputs (feed §5 widgets):** equity curve, per-trade P&L, win rate, average win/loss,
  expectancy, Sharpe, max drawdown (and drawdown vs median trade), exposure, trade count,
  hold-time distribution.
- **Reuses backend stats** (VR, half-life, μ*, habitat) — does not recompute them in JS.

---

## 5. P&L / METRICS WIDGETS (TradingView-style, rigor-wrapped)

A **separate P&L widget** as the user requested, plus the metrics panel:
- **Equity-curve graph** (cumulative P&L over time); IS vs OOS shaded distinctly.
- **Per-trade P&L** (bar/scatter), drawdown curve.
- **Win rate, expectancy net of cost, Sharpe, max drawdown, hold-time histogram** — with the
  **OOS net-of-cost figures as the headline**, in-sample secondary.
- **Editable transaction costs** with instant recompute (Research mode) and a re-stated
  assumption on every figure.
- **Reset-to-base** button restoring the base parameter set (localStorage in Research mode).
- Trade markers overlaid on the price/spread chart (entries/exits/stops).
- **Replay/play button:** step the backtest forward bar-by-bar and watch the equity curve and
  positions evolve — TradingView-replay feel — strictly causal.

---

## 6. MANUAL-REGIME WORKFLOW (the honest version of "the algo decides")

This is the core loop the owner described and it is buildable now:
1. Load a series; **hide forward data** at a chosen as-of point.
2. Inspect: is the market trending or turning? (trend overlay, slope/t-stat, residual
   structure, Kalman velocity, CUSUM flag).
3. **Mark a candidate MR zone** (a date range the user believes is mean-reverting).
4. **Habitat-confirm:** the habitat score (surrogate-relative, with its null cloud) scores the
   marked zone — is it genuinely MR or noise?
5. If confirmed, **enable signals in that zone** and backtest/paper-trade the MR strategy
   there; if not, no signals.
6. Reveal forward data to evaluate (marked evaluation-only) — and check **"did μ* stay put"**,
   not merely "did price come back."

The **automated-gate hook**: the same pipeline, but step 3 is produced by a regime detector
instead of the user — wired but **disabled** until a detector passes validation.

---

## 7. SUBAGENT ORCHESTRATION (small, crisp, one integrator)

Claude Code (orchestrator) coordinates; each subagent has a contract and a boundary. **Avoid
fragmentation** — the integration owner is single.

- **`frontend-architect`** (integration owner): Next.js app structure, component architecture,
  charting, the panels/widgets, state management, the Research/Verification mode machinery,
  localStorage handling. Owns merges/integration. (Attach a frontend/component design skill if
  available.)
- **`backend-api`**: expose the **existing frozen engines** (`analytics.py`,
  `analytics_arm_a_v2_beta.py`, calibrated habitat score, trend-death module) as endpoints;
  build the CSV ingestion service (§ companion doc) + caching. **Touches no math** — wraps
  what exists.
- **`backtest-engine`**: the event-driven backtester + walk-forward harness + cost model
  (§4). Reuses backend stats; does not recompute them.
- **`amr-rigor-qa`** (create this, or use `amr-adversarial`+`amr-trader`): audits the shipped
  UI against §2 and the companion's rigor checklist. **Sign-off required before any phase is
  called done.** Specifically verifies: firewall enforced, surrogate-relative reads, modes
  lock pre-reg params, OOS/cost-floor headline, no-JS-math, provenance present.

Hand-offs between agents carry the frozen doc + the API contract, never a verbal summary.
Single source of truth = repo + markdown memory.

---

## 8. SETTINGS / CONFIGURATION
- **One inspectable parameter registry** surfaced in the UI: Kalman SNR; trend window W;
  t-stat thresholds; flip-window k; forward horizon H; VR q-set; surrogate counts; θ;
  exit/stop/sizing; costs. Each shows its **base/default** and current value.
- **Defaults derived where possible** (hold from half-life, θ from cost).
- **Reset-to-base** restores the registry to defaults.
- **Research:** params in localStorage; **Verification:** params from a backend-pinned frozen
  pre-reg, locked.

---

## 9. PHASING
- **P1 — Observatory core** (companion doc §2,3,4.1,4.2): ingestion, firewall/replay,
  equilibrium, habitat score + scanner.
- **P2 — Backtester + strategy + P&L** (§3,4,5) + Research/Verification modes (§2). The
  rigor-wrapped TradingView-style backtest.
- **P3 — Manual-regime workflow + LE-GF cockpit** (§6 + companion §5) + portfolio view.
- **P4 — Compilation doc** (§10).
- Each phase: `amr-rigor-qa` sign-off before "done."

---

## 10. FINAL PHASE — THE COMPILATION DOCUMENT (agent-assigned)
After the interface is built, an agent compiles a single authoritative document covering:
the **MR habitat score** (definition, calibration, surrogate logic), **Kalman utilisation**
(μ*, velocity, innovation/CUSUM, stability read, the β-kill scope correction), **state shifts
/ regime work** (trend-death thesis, T2.5 NO_CONTENT, what's characterization vs timing),
the **regression/trend model**, the **strategy/backtest methodology**, and the **rigor
invariants**. This is institutional memory; it must state honestly what works (habitat score,
apparatus, LE-GF) and what does not (regime timing).

---

## 11. SCOPE BOUNDARIES (what this does NOT do)
- Does **not** ship automatic regime-gated signal generation (regime timing unvalidated —
  build the hook, leave it empty).
- Does **not** authorize research verdicts — those still run through pre-registration +
  named-agent + cross-model adjudication. The interface **shows and steers**; it does not
  adjudicate.
- Does **not** let an in-sample, hand-tuned equity curve stand as a result — OOS, walk-forward,
  net-of-cost is the headline.

---

## 12. RIGOR CHECKLIST (must all hold in shipped UI; `amr-rigor-qa` verifies)
- [ ] Regime timing NOT presented as solved; auto-gate hook present but disabled.
- [ ] Causal computations never see data > as-of cursor; forward marked evaluation-only.
- [ ] Habitat score always shows its surrogate cloud; never self-ranked.
- [ ] Raw-vs-deseason toggle + contamination flag.
- [ ] Frozen-β enforced; rolling-β flagged inadmissible.
- [ ] Research/Verification modes; Verification locks pre-reg params (no post-hoc tuning).
- [ ] OOS / walk-forward / net-of-cost is the headline; in-sample secondary & labelled.
- [ ] Hold/θ derived by default; tuning is Research-only.
- [ ] localStorage only for Research drafts + reset; Verification params backend-pinned.
- [ ] No statistic re-implemented in JS; all math from frozen backend engines.
- [ ] Full provenance on every result.