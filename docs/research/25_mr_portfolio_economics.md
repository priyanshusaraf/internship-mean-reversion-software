# Research Initiative — MR Portfolio Economics: Can Portfolio Construction Make Weak MR Deployable?

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **COMPLETE — research verdict (Research Mode; no implementation authorized).** Produced by an 8-agent
trader-first workflow (5 required lenses: PM · quant stat-arb · execution/cost · statistical adversary · risk
manager → 2 adversarial kill-passes → PM-lead synthesis), plus a **decisive empirical diagnostic run by the
research lead.** **Question:** can habitat gating · selectivity · diversification · cross-instrument netting ·
turnover reduction · conditional participation convert statistically-real-but-weak MR into cost-clearing alpha?
**Date:** 2026-06-04. **Builds on:** doc 23 (NG: true MR, uneconomic naive book) · doc 24 (timing is not the
bottleneck).

> **VERDICT: `ROUTE_GATED_ON_VALIDATION_AND_COHORT` — there is NO deployable MR route on the current cohort.**
> Two facts decide it: **(1)** the doc-23 failure is a **~7.5× EXPECTANCY gap** (gross +0.0004 vs cost 0.003),
> and expectation is linear/correlation-free, so **4 of 6 levers are variance-movers that cannot rescue a
> sub-cost edge**; **(2)** the only available expectancy lever (selectivity) is, on **exploratory
> (non-pre-registered) evidence, CURRENTLY UNSUPPORTED / LOW-PRIOR** (§2 — a soft prior update, NOT a binding
> verdict; it must clear a pre-registered surrogate test it has not yet faced), and the only cost lever
> (netting) has **nothing to operate on** because the admissible daily β=1 MR cohort is **NG alone.** The route
> is **gated on cohort expansion (Cycle-2 controlled-β), not portfolio cleverness** — and this top-line verdict is
> **robust to the selectivity status** (the cohort gate binds either way; §7). *truth ≠ usefulness*, reaffirmed.

---

## 1. The spine — expectancy vs variance (arithmetic, not opinion)
`E[Σ wᵢ(gᵢ − cᵢ)] = Σ wᵢ·E[gᵢ − cᵢ]` — **correlation-free.** A diversified book of negative-expectancy sleeves is
negative-expectancy. Classifying the six user levers:

| Lever | Class | Can it rescue a sub-cost edge? |
|---|---|---|
| **Selectivity** | EXPECTANCY (↑gross/trade) | Yes in principle — **but it's the State-T selection artifact here (§2)** |
| **Cross-instrument netting** | COST (↓cost/trade via shared legs) | Yes in principle — **but structurally absent on this cohort (§3)** |
| Turnover reduction | COST (↓cost frequency) | Largely the *same* lever as selectivity here (raising θ already collapses 10→4 trades/yr); RT cost is per-trade-invariant to hold length |
| Diversification | VARIANCE/Sharpe | **No** — only makes an already-positive book holdable; moot at n≈1 |
| Conditional participation | VARIANCE (+ trap) | **No** — and the doc-23 "avoid gluts" filter is *ex-post*; an ex-ante version is forbidden State-T-adjacent timing (doc 24) |
| Habitat gating | VARIANCE / cross-instrument selectivity | **No** per-trade expectancy effect; nothing to gate at n≈1 |

**Only selectivity and netting can move the ledger. Both fail on the current cohort.**

## 2. Selectivity: currently unsupported / low-prior (exploratory grounding, NOT a binding verdict)
> **EPISTEMIC STATUS (REVISED — corrects the first draft's overstatement).** The evidence below is **exploratory
> grounding → a SOFT PRIOR UPDATE**, not a frozen verdict: the surrogate protocol was **not pre-registered before
> execution** (RW-only, one seed, one threshold, no frozen train/OOS split, no episode-jackknife). It **lowers the
> prior** that NG tail selectivity clears costs; it does **not** kill it. **Do not conflate** *selection-on-deviation
> (a failure mode the strategy must survive)* with *economically pre-registered tail selectivity (a legitimate
> strategy class)* — tail selectivity is admissible IF frozen ex ante AND it survives surrogate-relative null + OOS +
> episode-jackknife + cost-clearing. The binding test (§5) has not been run; status = **CURRENTLY UNSUPPORTED, LOW
> PRIOR**, not "dead."

The in-sample selectivity gradient looked like a rescue — raising the entry threshold flips NG net-positive:
`|z|≥1.0` gross +0.0004 (net −0.0026) → `|z|≥1.5` +0.0201 (+0.0171, 6.7× cost) → `|z|≥2.5` +0.0508 (16.9×).
**But this is the exact "condition on a big |z|, observe reversion" operation that killed State T** (doc 11
Phase 5; doc 16 §6 binding rule: no raw |z|-conditioned statistic — must be real-minus-matched-surrogate). The
research lead ran the **selection-on-deviation null**:

> NG real, fade `|z|≥2`: gross **+0.0365**/trade (n=110). **Matched RW null** (zero MR, identical selective
> proxy, 300 paths): mean +0.0001, **p95 = +0.047, p99 = +0.058**. NG sits at ~the 89th percentile → **p ≈ 0.11
> — NOT distinguishable from a random walk faded at the same threshold.** **Concentration: 63% of NG's entire
> selective gross comes from 3 of 110 trades** (crisis-episode reversions). OOS halves both positive but weak
> against a p95-of-0.047 null + 3-trade concentration.

**A pure random walk faded at `|z|≥2` produces the same apparent "edge"** because `|z|` regresses to the mean of a
bounded standardized variable by construction. The selectivity gradient is **inadmissible as presented** (unfrozen
post-hoc argmax sweep — doc 22 §5 froze a *single* `|z|≥1`; §11.1 cardinal sin, §11.7 argmax) and **does not beat
its own null.** This is the **risk** tail selectivity must be proven (pre-registered) to survive — not proof it is dead.
Prior that a properly-formalized version survives: **LOW** (soft, exploratory). The pre-registered test (§5) is what
converts this from a low prior into a binding verdict either way.

## 3. The cohort is n≈1 — the binding constraint
The admissible **clean-construction daily β=1 MR universe is essentially NG ALONE**: RB calendar is a martingale
at q≤20 (doc 23, not MR); Brent calendar is hourly-only (off-scale apparatus control, not a daily sleeve); USD/INR
is stale-quote UNUSABLE; and **every** pair/intercommodity spread that could diversify or net (HDFC-ICICI,
Gold-Silver, Gold-Copper, Pt-Pd, TCS-INFY, WTI-Brent) requires **rolling-OLS-β, which doc 19 proved manufactures
VR** (82–97% β-update-noise, HIGH). Controlled/regularized β is UNTESTED (Cycle 2). Consequence: **the two
genuinely portfolio-level levers (diversification, netting) have nothing to operate on** — `corr(ΔNG,ΔRB)≈−0.015`
is moot because RB carries no edge; the real metals-netting structure (shared GC2! leg) is locked behind untested
controlled-β; and even a full 2× netting cut moves NG only 7.5×→3.75× below cost (insufficient). **You cannot
diversify or net a portfolio of one. The portfolio-rescue question is not empirically posable today.**

## 4. The minimum economically plausible route (strictly-ordered gates)
Neither half alone is fundable; **the binding gate is the cohort.** Expectancy first; variance machinery only
after *multiple* positive-expectancy sleeves exist.
- **GATE 1 — Expectancy (NG, cohort-of-one):** selectivity survives a pre-registered **surrogate-relative + OOS +
  episode-jackknife** test (§5). Admissible only if `Δnet(θ)=net_NG(θ)−E[net_surr(θ)] > 0` **and** `net_NG(θ) >
  cost`, θ frozen on a train split, OOS on a disjoint holdout, surviving removal of the single largest shock year,
  full θ-grid reported. *(The §2 exploratory check is a LOW prior on passing — not a foregone conclusion; this test
  is genuinely worth running, see §7.)* Even on a full pass → one ~4–8-trade/yr, capacity-trivial, undiversified
  sleeve = **unfundable standalone.**
- **GATE 0/2 — Cohort breadth (the binding gate):** Cycle-2 **controlled-β** (shrinkage/Kalman-fixed, OOS-frozen,
  NOT rolling-OLS) must first pass an §11.8 positive control on a textbook cointegrated pair **and** print VR≈1 on
  a known martingale (doc-19 zero-control), then admit **≥3–5 instruments each independently clearing its own
  crossing cost** under its own Gate-1 surrogate test.
- **GATE 3 — Book (variance machinery earns its keep only here):** assemble surviving positive-expectancy sleeves;
  net the metals cluster (accepting that **netting CANCELS that leg's diversification** — cost-saving and
  variance-reduction cannot both be banked); diversify across uncorrelated habitat families; evaluate the **book
  net-of-cost Sharpe / return-on-margin OOS** after costs/capacity/borrow/drawdown, with **exogenous-only** risk
  overlays (half-life-scaled time/MAE stop, cross-asset stress stand-aside, roll blackout — none keyed to
  reversion forecasts, doc 24). **KILL:** if <2 sleeves independently clear cost → no deployable book on this
  cohort (a valid terminal outcome).

## 5. Pre-registerable next test (highest-information; the project's own rule mandates it)
**NG selectivity surrogate falsification** — the test doc 16 §6 already requires but the engine never ran on the
trade proxy (surrogate ensemble is wired to VR(q) only). Freeze before data: full θ-grid {1.0,1.5,2.0,2.5,3.0}
reported in every cell (never argmax); causal z (≤ t−1); cost grid {0.0015 native, 0.003 conservative, 0.0045
crisis}; surrogate ensemble N≥500 of **RW + OU(φ matched to NG's 12.9-bar half-life) + GARCH(1,1) + a splice
surrogate at ng12's true seam cadence** (also closes the back-adjustment channel doc 23 left open), all through
**bit-identical** causal-z + fade logic. Primary statistic `Δnet(θ)` standardized by the surrogate-ensemble SD,
crisis-robust block-bootstrap CI; **PASS only if** `Δnet(θ)` exceeds the multiplicity-deflated band **and**
`net_NG(θ)>cost`, θ frozen on a train split, clearing cost OOS on a disjoint holdout, surviving episode-jackknife.
**Expected outcome (honest prior, reinforced by §2): Δnet shrinks under the surrogate → "no deployable route on
the current cohort, gated on Cycle-2" — a finding, not a failure.** *Build this first; build no portfolio/book
machinery until it passes AND the cohort expands (else = cohort-of-one-dressed-as-a-portfolio + a §11.7
multiple-comparison DOF blowout).*

## 6. Confidence · non-conclusions · next move
**Confidence:** HIGH that 4/6 levers cannot rescue a sub-cost edge (arithmetic); HIGH that the cohort is n≈1 and
diversification/netting are not posable now; **LOW-to-MEDIUM (soft, exploratory)** prior that NG tail selectivity
clears a pre-registered surrogate+OOS test — **CURRENTLY UNSUPPORTED, not demonstrated-dead** (the binding test is
unrun). **Non-conclusions:** no claim MR is *never* deployable — only not on *this* cohort via *these* levers; **no
claim tail selectivity is dead** (only currently unsupported, low prior); no claim Cycle-2 controlled-β will fail
(untested); no authorization to build portfolio machinery. **The binding bottleneck has moved from *timing* (doc 24) to
*admissible-cohort breadth*** — the route to deployable MR runs through **Cycle-2 controlled-β** (a larger clean
MR universe with netting-friendly shared legs), not through portfolio construction on NG alone. **Recommended next
build:** the Gate-1 NG selectivity surrogate harness (cheap, mandated, settles the only standalone lever), then
spec Cycle-2 controlled-β.

## 7. Does the verdict change under the selectivity downgrade? + strategic dependency graph
**(a) Materiality of the downgrade.** Downgrading selectivity from "dead" → "currently unsupported / low prior"
does **NOT** change the top-line verdict (`ROUTE_GATED…COHORT`), because **the binding constraint was never the
selectivity status — it is the cohort.** Both branches gate identically: selectivity dead ⇒ no route (dead lever +
cohort of one); selectivity *validated* ⇒ still no fundable **book** (one ~4–8-trade/yr sleeve, n≈1, nothing to
diversify/net) ⇒ still gated on cohort breadth. What the downgrade **does** change: (1) it **re-justifies running
the Gate-1 pre-registered selectivity test** — no longer a foregone "dead," it is a cheap, decision-relevant,
genuinely-uncertain (low-prior) test whose surprise-pass would confirm NG as a real standalone *building block*
(still book-gated); (2) it relabels the lever honestly (legitimate strategy class, currently unsupported), not a
killed object. **Verdict robust; Gate-1 status elevated from "settled-negative" to "open, low-prior, worth testing."**

**(b) Strategic dependency graph — what must be true before each is ECONOMICALLY meaningful:**
```
APPARATUS TRUST (§11.8 positive control, per-object)        [partial: doc 21 CONDITIONAL; back-adj channel open]
        │
        ▼
CONTROLLED-β ADMISSIBILITY  (Cycle 2 — the KEYSTONE)         [UNTESTED]
   pass §11.8 on a textbook cointegrated pair + VR≈1 on a doc-19 martingale zero-control
        │
        ├───────────────────────────────┐
        ▼                                ▼
COHORT BREADTH (≥3–5 clean MR sleeves)   PER-INSTRUMENT EXPECTANCY (per sleeve, ≥1 lever works)
   needs controlled-β to escape n≈1        base-MR-clears-cost? OR pre-registered tail-selectivity? OR netting?
        │                                  [NG base sub-cost; selectivity low-prior-untested; → currently 0 proven]
        └───────────────┬──────────────────┘
                        ▼
            PORTFOLIO CONSTRUCTION (meaningful only with ≥2 positive-expectancy sleeves)
              diversification + netting now earn their keep (variance/cost on positive-mean streams)
                        │
        ┌───────────────┴───────────────┐
        ▼                                ▼
   BOOK-LEVEL COST/CAPACITY TEST     HABITAT PERSISTENCE (economically meaningful)
   (OOS, after costs/borrow/dd)        = a book-selectivity input; ECONOMIC value is DOWNSTREAM of a
        │                              cost-clearing book existing. Absent that → "true but inert"
        ▼                              (research-prioritization value only). Must also be non-circular
   DEPLOYABLE MR                       + material + non-State-T (the habitat-* adjudications).
```
**Reading of the graph:** **Controlled-β admissibility (Cycle 2) is the keystone** — cohort breadth, portfolio
construction, and deployable MR are ALL downstream of it; while the cohort is n≈1 none of them is economically
posable. **Per-instrument expectancy is a parallel, possibly-fatal prerequisite** (currently *zero* proven
cost-clearing sleeves — NG base is sub-cost, selectivity is low-prior-untested). **Habitat persistence is
economically meaningful only DOWNSTREAM of a cost-clearing book** (it selects/weights instruments *for* a book);
with no book it is *true-but-economically-inert* and retains only research-prioritization value — which **confirms
and extends the user's reprioritization** (portfolio economics ahead of habitat persistence): habitat persistence
should not be elevated to an economic deliverable until ≥1 cost-clearing sleeve exists. **Critical path to
deployable MR:** apparatus-trust → **controlled-β (Cycle 2)** → cohort breadth + per-instrument expectancy →
portfolio construction → book cost test → deployable. The single highest-leverage next object is therefore
**Cycle-2 controlled-β admissibility**; the Gate-1 selectivity test is a cheap parallel that settles the lone
standalone lever.

---
*Markers: WEAKENED/REVISED (selectivity = "currently unsupported / low prior, soft exploratory" — NOT
"demonstrated artifact"; distinguished from pre-registered tail selectivity, which stays a legitimate untested
class) · ROBUST (top-line verdict ROUTE_GATED…COHORT unchanged — cohort, not selectivity, is binding) ·
ESTABLISHED (expectancy-vs-variance: only selectivity & netting move the ledger) · KEYSTONE (Cycle-2 controlled-β
gates all downstream economic objects) · CONTINGENT (habitat persistence economically meaningful only downstream
of a cost-clearing book). truth ≠ usefulness, reaffirmed. No history erased.*
