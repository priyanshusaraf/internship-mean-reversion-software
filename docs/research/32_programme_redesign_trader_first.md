# Doc 32 — AMR Programme Redesign: Trader-First Constitutional Update

**Document class:** Permanent institutional redesign memo. Supersedes the priority ordering and research pipeline
architecture of §1–§4 and §12–§15 of CLAUDE.md where they conflict with this document. Does NOT relax
falsification standards, temporal integrity, surrogate-relative requirements, or frozen invariants (§6, §8).
**Date:** 2026-06-04. **Status:** ACTIVE — governing doctrine.

> **Core thesis:** The AMR programme is not shifting from rigour to intuition. It is shifting from
> *universal-truth-seeking* to *deployment-targeted evidence accumulation*. The difference is directional,
> not methodological. Every tool in the falsification stack remains intact. What changes is which questions
> those tools are pointed at, and in which order.

---

## 1. Objective Redesign

### Prior objective (retiring)

> "Discover and understand mean reversion in structurally trendy markets through rigorous research-grade
> falsification, building towards eventual trading."

This framing produced: 31 documents, 14 killed hypotheses, 3 conditional survivals, and exactly 0 deployed
edges. The academic completeness constraint was always deferring the deployment question to the next phase.

### New objective hierarchy

**Tier 1 — Trader Reality** *(the only tier that ultimately matters)*

Deploy at least one cost-clearing mean reversion book in a liquid commodity spread market, generating
positive net expectancy after all-in costs (bid-ask, roll, margin, back-office overhead) in a 12-week
forward hold-out window. A "book" means: positive Σwᵢ·E[gᵢ−cᵢ] across instruments, not dependent on any
single crisis event, not reliant on regime-timing.

**This tier defines success. If we never reach it, the programme failed regardless of how many hypotheses
we correctly falsified.**

**Tier 2 — Quant Falsification** *(serves Tier 1, not an end in itself)*

Prevent self-deception via causal integrity, surrogate-relative testing, pre-registration, and OOS
validation. Falsification is the immune system of Tier 1: it kills ideas that would waste deployment capital.
It is not the objective. A result that survives Tier 2 but has no Tier 1 path is a finding, not a success.

**This tier has veto power. It does not have promotion power.**

**Tier 3 — Research Elegance** *(earns its keep or gets cut)*

Understanding the mechanism behind a confirmed edge. Useful when: (a) it suggests a better construction;
(b) it identifies which instruments should share the edge; (c) it enables a causal entry variable.
Not useful when: it is beautiful but does not improve a Tier 1 path. Mechanism research is authorized
when a specific Tier 1 question is identified that it would answer. Not otherwise.

### What this changes operationally

| Prior posture | New posture |
|---|---|
| Hypothesis → falsify → maybe deploy | Deployment path → work backwards to what must be true |
| Research completeness before action | Minimum sufficient evidence for each step forward |
| Any confirmed truth is valuable | Only truths with a deployment path are prioritized |
| Black swans are research targets | Black swans are risk management problems |
| 500-surrogate precision for all tests | 200-surrogate speed gate, 500-surrogate final verdict only |
| Positive control as §11.8 formality | Positive control as actual confidence in the apparatus |

---

## 2. New Research Constitution

### 2.1 — Before any research starts (binding pre-conditions)

Every new idea must pass ALL four before a single line of code is written:

**P1 — Trade sentence.** Write the trade in one sentence: "Buy [instrument A], sell [instrument B], when
[causal condition], exit when [exit rule], expected hold [N], expected gross [X]." If you cannot write this
sentence, the idea is not ready for research. Intuition must be articulable.

**P2 — Cost arithmetic.** Before any empirical work: estimate expected gross per trade and expected cost
per trade with realistic assumptions. If theoretical gross/cost < 1.5× under optimistic assumptions, the
prior is VERY LOW — proceed only if the economic mechanism is unusually strong (physically anchored
arbitrage) or the instrument is unusually liquid (low costs). Document this estimate. It becomes the
prior for the test.

**P3 — Deployment path.** Name: (a) the specific instrument(s), (b) the contract structure (calendar spread,
pairs, etc.), (c) the execution venue (screen/voice/futures pit), (d) the minimum viable position size for
the edge to matter, (e) any data or infrastructure currently missing. If the deployment path requires
something not acquirable in 4 weeks, move to DEFERRED with a named acquisition trigger.

**P4 — Causal label.** Identify the entry and exit rule with zero forward-looking information. If the rule
requires regime identification, name the causal variable (inventory, COT, EIA report, etc.) — NOT a price
pattern. Rules that require "knowing we are in a mean-reverting regime" without a named causal variable
are State-T-adjacent and inherit the §4 zombie prohibition.

### 2.2 — Fast-kill criteria (binding, not advisory)

An idea is KILLED immediately if any of these trigger before the primary test:

| Trigger | Kill rule |
|---|---|
| Theoretical gross/cost < 1.0× after realistic cost modelling | Kill before any code |
| N=200 surrogate gate: p_rw > 0.20 | Kill; do not upgrade to N=500 |
| Episode-jackknife drop > 300% | Kill unless regime-conditionality proven causal |
| p_ou > 0.80 AND no causal variable to exploit the conditionality | Kill (instrument's own MR beats you) |
| OOS sign reversal on ≥ 50% of OOS period | Kill |
| Replication fails on first cross-habitat attempt | Move to CONDITIONAL SURVIVAL with named expiry, NOT kill; acquire 2nd instrument |

**These are thresholds, not suggestions.** The asymmetry is deliberate: false kills are survivable (we
miss a real edge); false survivals waste capital and time on sub-cost books.

### 2.3 — When intuition is admissible

**Always admissible:**
- Hypothesis generation and framing ("storage MR should exist in energy calendars")
- Instrument selection based on economic structure ("crack spreads have physical arbitrage bounds")
- Sizing and risk management decisions with causal backing
- Deciding which causal variable to acquire ("EIA storage report is the right inventory signal")

**Admissible with explicit flag:**
- Rejecting a kill verdict based on regime explanation — allowed ONLY if the regime explanation is
  causal (non-price) and the test on the conditional strategy is pre-registered before re-running
- Narrowing the instrument universe based on market knowledge — allowed but must be documented as
  a pre-registered restriction, not post-hoc filtering

**Never admissible:**
- Declaring statistical significance ("this feels like it works")
- Bypassing the surrogate-relative requirement ("the mechanism is so clear we don't need surrogates")
- Treating one good OOS period as evidence ("it worked in 2022-2024")
- Selecting the threshold/parameter after seeing results

### 2.4 — When quant vetoes intuition

Quant veto is AUTOMATIC and non-negotiable when:

1. p_rw ≥ 0.05 at the pre-committed primary threshold (no statistical significance = no edge claim)
2. Jackknife collapse > 300% (one-trade concentration = not a strategy, it's a lottery ticket)
3. Full-sample negative + OOS positive but OOS n < 50 trades (small-sample OOS is not override)
4. Surrogate null (RW/GARCH/OU) beats the real instrument at p > 0.50 (the null is a better description)
5. The causal regime label is defined by the FOLLOWING period's data (any forward-looking regime variable)

Intuition may SUGGEST the mechanism; the quant apparatus DECIDES whether evidence exists. These roles
are not interchangeable.

### 2.5 — Sufficient evidence for deployment (binding)

A strategy moves to Deployment Candidate when ALL of these are simultaneously true:

| Criterion | Threshold |
|---|---|
| Primary surrogate gate | p_rw < 0.05, N ≥ 500, pre-registered primary statistic |
| Episode-jackknife | Gross drop < 50% after removing largest single trade |
| Net expectancy after all-in cost | Net > 0 at full cost grid, primary cost assumption |
| OOS hold-out | Sign-consistent with full-sample, n ≥ 40 trades |
| Cross-habitat replication | ≥ 2 independent instruments confirm at p_rw < 0.10 each |
| No causal variable required for basic edge | OR causal variable is identified, acquirable, and pre-tested |

The OOS hold-out is not time-split only — it includes instrument-OOS (tested on instruments not in
the discovery set).

---

## 3. Research Prioritization Redesign

Rated on: Trader EV (potential net expectancy × capacity) · Deployment speed (weeks to first evidence) ·
Economic grounding (physical/structural anchor) · Research risk (contamination, artifact, zombie) ·
Recommendation.

### TIER A — Execute immediately

**A1. EIA storage regime filter for NG (NEW — unlocks NG deployment)**

- **Trader EV:** HIGH. NG is confirmed mean-reverting (p=0.005, VR=0.448) but sub-cost unconditionally.
  The mechanism is known: MR switches off in storage glut years. EIA weekly natural gas storage data
  is public, causal (released Thursday 10:30am ET), and directly indexes the glut/non-glut distinction.
  A simple conditional entry — "enter only when storage surplus < X% of 5-year seasonal average" —
  is a physically-grounded causal variable, NOT a price morphology, NOT State-T.
- **Deployment speed:** 2–3 weeks (data acquisition + pre-registered conditional test)
- **Economic grounding:** STRONG — theory of storage (Working 1949); inventory directly determines
  the restoring force in commodity calendar spreads
- **Research risk:** LOW contamination (EIA is causal, released on a fixed schedule, no forward-reading).
  Non-trivial risk: the conditional entry might still fail if glut/non-glut is too few years for power.
- **Expected value:** Converts PERSISTENT-BUT-UNECONOMIC to potentially deployable. Highest single-instrument
  expected value action in the entire programme.
- **Kill criterion:** Conditional entry fails p_rw < 0.10 at N=200 with two different causal variables
  (EIA storage deviation + EIA inventory trend). Then the conditional path is closed and NG remains a
  "confirmed but undeployable" finding.
- **Recommendation: PURSUE — highest priority**

**A2. BRN M1-M2 daily calendar construction + VR test (unlocks cohort breadth)**

- **Trader EV:** HIGH. If Brent confirms MR, we have two instruments for portfolio framing. Brent has
  storage economics similar to NG but different regime structure (no documented glut years from the
  data so far).
- **Deployment speed:** 1–2 weeks (BRN2! 1D acquisition + spread construction from raw legs + VR test)
- **Economic grounding:** STRONG — same storage arbitrage theory as NG; Brent is more liquid, tighter
  bid-ask, better capacity
- **Research risk:** Medium — vendor precomputed spread not available; must build from raw legs (avoids
  back-adjustment artifact). BRN1! daily already exists (9526 bars).
- **Kill criterion:** VR(20) not significantly < 1 surrogate-relative (p_rw > 0.10 at N=200)
- **Recommendation: PURSUE — highest priority**

**A3. Crack spread controlled-β positive control (RB-HO or CL-HO) (§11.8 gate + apparatus validation)**

- **Trader EV:** HIGH structural value. Validates the controlled-β construction pathway. If confirmed,
  enables pairs trading with a physically-anchored hedge ratio. Crack spreads (gasoline vs crude vs
  heating oil) have documented seasonal MR driven by refinery margins — a textbook physically-anchored
  edge.
- **Deployment speed:** 2–3 weeks (data check + Kalman-β construction + VR test)
- **Economic grounding:** STRONGEST in the programme — refinery economics create hard mean-reversion
  bounds via physical arbitrage; seasonal crack patterns are widely documented
- **Research risk:** Medium — controlled-β apparatus not yet validated; requires Kalman or ridge β
  (NOT rolling OLS). The risk is the apparatus, not the instrument.
- **Why this is §11.8-mandatory:** the apparatus that could not confirm the crack spread CANNOT be
  trusted to have found (or not found) MR elsewhere. Apparatus recalibration before admitting new
  controlled-β instruments.
- **Recommendation: PURSUE — execute in parallel with A1/A2**

---

### TIER B — Pursue after Tier A has evidence

**B1. Portfolio/book construction (gated on A2 confirming cohort breadth)**

- **Trader EV:** VERY HIGH if ≥ 2 instruments confirm. Diversification cannot rescue sub-cost sleeves
  (expectancy arithmetic, doc 25), but a book of independently cost-clearing edges has higher Sharpe and
  lower drawdown than any single instrument.
- **Gate:** ≥ 2 instruments independently clear the cost floor at p_rw < 0.05. If only NG ever confirms,
  this arm stays dormant.
- **Recommendation: DEFER — explicitly gated on A2 result**

**B2. Dynamic (Kalman/ridge) hedge ratio for pairs (gated on A3 positive control)**

- **Trader EV:** HIGH. Real pairs trading desks use regularized β, not fixed β. If the apparatus
  validates via crack spread (A3), this becomes the methodology for all cross-commodity pairs.
- **Gate:** A3 positive control confirms the Kalman-β apparatus is credible. Then apply to new pairs
  (energy spreads, agricultural spreads, metals calendar structures).
- **Research risk:** Medium-high — regularized β has DOF if not disciplined. Must pass same surrogate
  tests as β=1 construction.
- **Recommendation: DEFER — execute immediately after A3 confirms**

**B3. ZC M1-M2 daily calendar (corn — extends β=1 cohort to agricultural)**

- **Trader EV:** Medium-High. Corn calendar has storage economics. Less liquid than NG/BRN, higher
  bid-ask.
- **Gate:** BRN1! already acquired; ZC2! 1D still needed.
- **Recommendation: DEFER — second data acquisition after BRN2!**

---

### TIER C — Low priority under new objective

**C1. Etiology-conditioned reversion (signed order flow)**

- **Trader EV:** VERY HIGH in theory — the best-grounded mechanism in the programme. Inventory/flow
  positions predict reversion; information positions continue. This is the fundamental distinction
  between noise and informed trading.
- **Deployment speed:** SLOW — requires signed order-flow or OI/COT data, currently blocked.
- **Research risk:** Low contamination (causal variable is non-price). High acquisition cost.
- **Recommendation: DEFER — highest long-run EV, but data-gated. Reopen trigger: acquire CME COT
  disaggregated positioning data for NG or BRN. If EIA filter (A1) works, this becomes the next
  sophistication upgrade.**

**C2. Residual ecology (observational morphology)**

- **Trader EV:** LOW direct. Understanding what residuals look like around realized reversions has
  no direct deployment path under the new objective.
- **Deployment speed:** N/A — observational only by §11.5 construction
- **Recommendation: ARCHIVE under new objective. Not killed — the §11.5 doctrine is sound — but
  deprioritized to "run only if there is excess capacity after Tier A/B work is complete."**

**C3. Regime classification (vol/trend filter)**

- **Trader EV:** Medium. A crude vol filter ("don't trade when 20-day realised vol > Xσ above
  historical average") is easy to implement and might reduce exposure to crisis-period contamination.
- **Research risk:** HIGH — conditional models reliably lose OOS (Goyal-Welch; doc 14 §3.2). The
  cruder the better; HMM/ML forms are traps.
- **Recommendation: DEFER until core instruments confirm. If NG conditional entry (A1) works via EIA
  storage, a vol filter could be layered as a second filter — but only tested unconditionally first.**

**C4. Equilibrium-stability / VR(q) ecology (observational)**

- **Trader EV:** LOW — observational, no-trade-environment input only
- **Recommendation: DEFER — gated behind positive control and Arm A v2 instrument confirmation**

---

### TIER D — Maintain current status (no change needed)

**D1. Kalman μ*** — terminal/descriptive, instrumentation only. No priority change.

**D2. Construction ontology (`beta_mode` taxonomy)** — partially frozen. Resolves naturally via A3.

---

### ARCHIVE — Do not revisit without named reopen trigger

State T, Trend→MR transition, MRScore, CSU identity — zombie prohibition binding.

---

## 4. New Canonical Research Loop

Seven stages with explicit stop/go criteria. Designed for maximum trader learning per week.

```
Stage 0 — ECONOMIC GROUNDING          (1 day)
Stage 1 — SPEED GATE                  (2–3 days)
Stage 2 — COST FLOOR TEST             (1–2 days)
Stage 3 — ROBUSTNESS FAST-PATH        (3–5 days)
Stage 4 — CROSS-HABITAT REPLICATION   (1–2 weeks)
Stage 5 — DEPLOYMENT ARCHITECTURE     (1 week)
Stage 6 — FORWARD HOLD-OUT            (4–12 weeks)
```

Total minimum: 4–5 weeks from economic intuition to deployment candidate. Total with data acquisition:
6–10 weeks. This is the target cycle time. Anything slower indicates process drift.

---

### Stage 0 — Economic Grounding (1 day hard cap)

**Do:**
- Write the trade sentence (P1 in §2.1)
- Run the cost arithmetic (P2)
- Identify the deployment path (P3)
- Identify the causal label (P4)
- Write the prior probability and the minimum gross/cost ratio needed to be interesting

**Stop criteria:**
- Gross/cost ratio < 1.2× under optimistic assumptions → KILL before writing code
- No causal entry label (requires regime-reading) without a named non-price variable → DEFER until
  data acquired
- Deployment path requires instruments not acquirable in 4 weeks → DEFER with named acquisition trigger

**Go criteria:**
- All four pre-conditions (P1-P4) satisfied
- Prior probability ≥ LOW (physically-anchored mechanism) OR data exists to test quickly

**Output:** One-page brief: mechanism, trade sentence, prior, gross/cost estimate, deployment path,
proposed primary statistic, proposed N and test type.

---

### Stage 1 — Speed Gate (2–3 days, N=200 surrogates)

**Do:**
- Minimal causal implementation (β=1 or pre-committed fixed β; no parameter tuning)
- N=200 surrogate-relative test (RW + OU minimum; GARCH if vol clustering suspected)
- Compute gross expectancy, p_rw, and a single jackknife check (drop 3 largest trades)

**Why N=200 not N=500:** Speed. A p-value of 0.12 at N=200 will not pass 0.05 at N=500. A p-value
of 0.04 at N=200 is already interesting. N=500 is for the final verdict, not speed-gating.

**Stop criteria:**
- p_rw > 0.20 → KILL (cannot be significant at any reasonable N)
- Jackknife drops > 500% → KILL unless a crisis-period explanation exists AND is pre-registered for
  conditional testing
- Gross < cost × 1.2 AND no clear path to cost reduction → KILL

**Go criteria:**
- p_rw ≤ 0.15 (borderline interesting)
- Jackknife drop ≤ 200% (not single-trade concentrated)
- Gross/cost ≥ 1.2× at primary cost assumption

**Output:** One-page speed-gate result with go/kill verdict.

---

### Stage 2 — Cost Floor Test (1–2 days)

**Do:**
- Run full cost grid (0.5×, 1.0×, 1.5×, 2.0× primary cost assumption)
- Break-even analysis: what cost does the strategy tolerate?
- Market impact modelling: estimate realistic execution cost at intended position size
- Capacity estimate: maximum daily notional before market impact erodes edge

**Stop criteria:**
- Net < 0 at primary cost assumption AND break-even cost < realistic execution cost → KILL
- Capacity estimate < meaningful position size for the intended book → KILL (the edge is microscopic)

**Go criteria:**
- Net > 0 at primary cost OR break-even cost > realistic execution cost with plausible headroom
- Capacity > minimum viable book size

**Output:** Cost waterfall table, break-even cost, capacity estimate.

---

### Stage 3 — Robustness Fast-Path (3–5 days)

**Do:**
- Upgrade to N=500 surrogates (RW, GARCH, OU)
- Full episode-jackknife
- OOS split (≥20% of sample held out, most recent data)
- Regime-conditionality check: does the edge flip in identifiable periods? (Look for it — do not hide it)
- Cost sensitivity: test across full cost grid
- Pre-register primary statistic and all parameters BEFORE seeing these results (if not done in Stage 0)

**Stop criteria:**
- p_rw ≥ 0.05 at N=500 → KILL
- Jackknife drop > 200% AND no causal regime variable to exploit the conditionality → KILL
- OOS sign reversal → KILL
- Edge concentrated in a single year or single crisis period → move to CONDITIONAL SURVIVAL with
  explicit condition named (e.g., "works only when EIA storage surplus < X%")

**Go criteria:**
- p_rw < 0.05 at N=500
- Jackknife drop < 100% (comfortable stability)
- OOS directionally consistent, net positive
- No pathological concentration in one event

**Output:** Full Stage 3 results table, verdict (CONDITIONAL SURVIVAL or CONFIRMED for this instrument),
next instrument for cross-habitat test.

---

### Stage 4 — Cross-Habitat Replication (1–2 weeks per instrument)

**Do:**
- Run identical pre-registered apparatus on ≥ 2 independent instruments
- Pre-register instrument list and q grid BEFORE running (no argmax on instruments)
- For each instrument: same surrogate types, same primary statistic, same cost assumption
- Report all instruments run, not just the ones that confirm

**Stop criteria:**
- 0/N instruments confirm at p_rw < 0.10 → KILL the hypothesis class (not just the instrument)
- 1/N confirms and N ≥ 3 → CONDITIONAL SURVIVAL, single-instrument finding, name expiry trigger
- Confirmation rate < 25% → LOW CONFIDENCE, defer further instrument acquisition

**Go criteria:**
- ≥ 2/N confirm at p_rw < 0.10 each, independently
- Cross-habitat pattern consistent with the named mechanism (storage MR confirmed in BOTH energy
  and agricultural is stronger evidence than two energy instruments)

**Output:** Cross-habitat replication table. Verdict: CONFIRMED-IN-CLASS, CONDITIONAL, or KILLED.

---

### Stage 5 — Deployment Architecture (1 week)

Only reached by strategies that survive Stage 4.

**Do:**
- Position sizing: Kelly fraction, max position per instrument, max book-level concentration
- Drawdown analysis: simulate realistic drawdown scenarios (regime flip, liquidity event, vol spike)
- Correlation structure: how correlated are the confirmed instruments in stress periods?
- Execution plan: entry/exit mechanics, roll schedule, re-entry after drawdown
- Risk limits: maximum daily loss, stop-loss per instrument, book-level stop

**Output:** Deployment brief. This is the document that goes to a PM.

---

### Stage 6 — Forward Hold-Out (4–12 weeks, ongoing)

Paper trade or minimum-viable live sizing. Record every trade. Compare to the pre-registered model.

**Stop criteria:**
- Forward hold-out net < 0 over ≥ 40 trades → suspend (not kill; forward test can have bad luck runs)
- Two consecutive 40-trade windows negative → KILL unconditionally
- One trade exceeds 5× expected gross → investigate mechanism immediately

**Deployment gate:** CONFIRMED in forward hold-out after ≥ 80 trades at consistent net positive.

---

## 5. Immediate Next 3 Highest-EV Moves

Ordered by expected trader learning per week under the new objective.

---

### Move 1 — EIA storage conditional entry on NG (highest immediate EV)

**What:** Acquire EIA weekly natural gas storage report data (public, released Thursday 10:30am ET,
reported in Bcf; 5-year seasonal average published by EIA). Construct a causal conditioning variable:
`storage_surplus_pct = (storage_actual − storage_5yr_seasonal_avg) / storage_5yr_seasonal_avg`.
Pre-register a conditional entry rule: "trade the NG calendar only when `storage_surplus_pct < θ_inventory`
(below-average storage = storage drawdown regime, physical restoring force strongest)."

**Why this is the highest-EV move:** We already know NG MR exists (VR=0.448, p=0.005) and the mechanism
(storage arbitrage). We know it switches off in glut years. The EIA data IS the causal inventory variable
that determines whether the restoring force is active. This is NOT regime-timing from price patterns
(State-T resurrection); this is using the fundamental economic variable that drives the MR. The cost of
this test is low (EIA data is free/cheap); the upside is converting the programme's only confirmed MR
finding from "interesting" to "deployable."

**Pre-registration requirements:**
- θ_inventory threshold set before running (pre-commit to ≤ 2 choices: e.g., 0% and 10% above seasonal)
- Same θ∈{1.0, 1.5} z-entry thresholds as doc 30 (no new threshold exploration)
- Primary statistic: net expectancy at (storage_surplus_pct < 10%, θ=1.0)
- N=200 speed gate first; N=500 only if speed gate passes

**Kill criterion:** Conditional entry at best storage threshold still fails p_rw < 0.10 at N=200.
Archive the conditional-entry path; NG remains PERSISTENT-BUT-UNECONOMIC.

**Expected time to first result: 2–3 weeks.** If this works, NG goes from academic to live.

---

### Move 2 — BRN M1-M2 daily calendar construction (cohort breadth gate)

**What:** Acquire `ICEEUR_DLY_BRN2!` at 1D frequency (ICE Brent second-month continuous futures daily).
BRN1! daily already exists (9526 bars, from data manifest). Construct BRN M1-M2 calendar spread from
raw legs (NOT a vendor precomputed spread — avoids back-adjustment artifact that exists in ng12_spread.csv).
Run full Arm A v2 apparatus: deseasonalize (causal trailing seasonal), VR(q) grid, N=500 surrogate test
(RW+GARCH+OU+MA(1)), same pre-registered protocol as doc 20/21.

**Why this is the second-highest EV move:** Portfolio framing (the only path to a meaningful book size)
requires ≥ 2 independently confirming instruments. NG alone is "cohort of one." Brent is the most
natural extension: same commodity class (energy), same storage economics, higher liquidity, better
capacity. The marginal cost of this test, given the existing apparatus, is small. If it confirms, the
portfolio direction becomes empirically posable for the first time.

**Kill criterion:** VR(20) p_rw > 0.10 at N=200 speed gate. Kill Brent calendar direction; move to ZC
as next candidate.

**Expected time to first result: 1–2 weeks** (primarily gated on BRN2! data acquisition).

---

### Move 3 — Crack spread controlled-β positive control (§11.8 gate + apparatus readiness)

**What:** Select the HO2!/RB2! calendar crack spread (heating oil vs gasoline, same RBOB barrel → less
basis contamination than crude-product). Construct using Kalman-filtered hedge ratio (NOT rolling OLS —
which is inadmissible, doc 19). Run through the full Arm A v2 apparatus. This is the §11.8-mandated
real-data positive control for the controlled-β construction pathway.

**Why this is the third move (not first):** The §11.8 gate must be cleared before admitting any new
controlled-β instruments. But it is a gate, not a deployment target — the apparatus validation is a means
to unlocking B2 (dynamic hedge ratio pairs trading). Without it, every future controlled-β result is
potentially meaningless (we cannot distinguish "real edge not found" from "apparatus too blunt").

**Why crack spread specifically:** Refinery margin MR is the most physically grounded, widely documented
commodity spread edge in the literature. If the apparatus cannot detect it, the problem is the apparatus.
If it does detect it, we have unlocked the controlled-β pathway for every commodity pairs trade.

**Kill criterion:** If the crack spread FAILS to confirm at p_rw < 0.10 at N=200, the problem is
the Kalman-β apparatus itself — recalibrate before admitting any other controlled-β pair.

**Expected time to first result: 2–3 weeks.**

---

### Priority ordering and parallelism

Moves 1 and 2 are independent and can be run **in parallel** (EIA data acquisition ≠ BRN2! data
acquisition). Move 3 can run concurrently with both once data is available. All three can be in
progress simultaneously.

**Expected total wall-clock time to first major verdict: 2–3 weeks.**

---

## 6. Sacred Cows Killed Under New Objective

These ideas survive the old constitution but fail the new Tier 1 priority test:

**Residual ecology (observational arm)** — under the old objective, "understand what residuals look like
around reversions" was a legitimate research goal. Under the new objective: there is no deployment path
from observational morphology without a causal variable, and we explicitly killed the causal-variable
path (State-T, transition prediction). This arm is deprioritized to "excess capacity only."

**Kalman μ* development** — beautiful instrument; low direct EV. Survives as a diagnostic but does not
earn primary research time under the new objective.

**Comprehensive regime taxonomy** — the programme has spent significant effort classifying regime types.
Under the new objective: regimes matter only as risk-management inputs ("when NOT to trade") — not as a
classification system. A single crude filter (e.g., EIA storage surplus) is worth more than an elegant
taxonomy.

**Full theoretical mechanism resolution before deployment** — the old constitution implicitly required
understanding WHY before asking WHETHER. The new constitution allows: "we don't know exactly why NG
MR is stronger in low-storage regimes, but the EIA signal is causal and the effect is there — that is
sufficient to trade." The mechanism matters for instrument discovery; it does not gate deployment.

---

## 7. What Does NOT Change

Falsification standards are unchanged. The following remain binding without exception:

```
temporal/causal integrity — still sacred
pre-registration — still required
surrogate-relative reads — still mandatory
anti-overfit culture — still enforced
statistical significance over narrative — still the rule
frozen invariants (§6) — unchanged
technology stack (§8) — unchanged
zombie prohibition — unchanged
p-hacking at scale — still the cardinal sin
"stopping is a success" — still true (but now costs time, not just momentum)
```

The change is directional, not methodological. We point the same tools at questions a trader would pay
for answers to.

---

## 8. Programme State Under New Constitution

| Finding | Status under new objective |
|---|---|
| NG calendar MR (VR=0.448, p=0.005) | CONFIRMED — needs EIA conditional entry to deploy |
| NG PERSISTENT-BUT-UNECONOMIC | ACTIVE — convertible via A1 (EIA storage filter) |
| NG selectivity KILLED A_FALSE_RESCUE | CLOSED — do not reopen on NG unconditional |
| Brent calendar MR | UNTESTED — Move 2 |
| Crack spread MR (controlled-β) | UNTESTED — Move 3 |
| Portfolio/book framing | GATED — unlocks after Move 2 confirms Brent |
| State T / Transition timing | ARCHIVED — zombie prohibition binding |
| EIA conditional entry for NG | NEW — first test after this doc |
| Dynamic hedge ratio (pairs) | DEFERRED — unlocks after Move 3 |

---

*Markers: SUPERSEDES §12-§15 priority ordering · LAYERS ON §1-§11 rigor requirements ·
INTRODUCES explicit cost-arithmetic pre-conditions and fast-kill thresholds · KILLS residual
ecology priority and Kalman μ* development priority · ELEVATES EIA storage conditional entry
as first new hypothesis pre-registration under this doctrine.*
