# Strategy 01 — Calendar-Spread Mean-Reversion (definitive spec)

**Workstream:** SEPARATE from the AMR falsification line. Here **MR existence is GIVEN** (the spread
is assumed already mean-reverting; existence is handled upstream). Objective: trade an
already-mean-reverting **calendar spread** profitably with **smooth equity / low drawdown**.
Priority order (frozen): smooth equity > low DD > cross-instrument stability > post-cost robustness >
explainability > consistency > raw return.

**Artifact:** `scripts/calendar_spread_mean_reversion.pine` (Pine v6, runnable `strategy()`).
**Date:** 2026-06-09. Built via 4-lens fan-out (mechanics · OU-design · Pine-impl · adversarial/cost).

---

## 1. The reorientation (what a junior gets wrong)

The edge is **not in an indicator**. It is in **object + regime gate + exit**:

- **Object:** a calendar spread = `carry skeleton + seasonal skeleton + deterministic convergence
  drift + thin transitory ε`. **Only ε is harvestable.** Carry is one-sided (full-carry ceiling caps
  contango; backwardation is unbounded → asymmetric risk).
- **Exit, not entry, is the strategy** (Chan; Leung-Li). In MR a losing trade is usually *too early*,
  not *wrong* → **price stops cut recoverable entries and analytically shrink the take-profit**.
  Drawdown control comes from **regime / time exits**, not price stops.

## 2. Definitive strategy (one, not a menu)

**Seasonally-naive, slow-equilibrium OU band reverter on the native listed spread.**

| Component | Choice | Why |
|---|---|---|
| Equilibrium μ_t | **Kalman local-level** (RW+noise), **slow** (λ=Q/R≈0.01) | ML-optimal causal tracker of a drifting level; **imposes no periodic basis → cannot manufacture MR** the way explicit deseasonalization does. Slow = denies the artifact channel. |
| Deviation | causal z-score, window ends at **t−1** | no self-inclusion leak |
| OU params | trailing AR(1) → φ → **HL = −ln2/ln φ** | half-life is the master scale; windows/stops key off it |
| Entry | **\|z\| ≥ 1.25** | DERIVED: Bertram Sharpe-opt w/ cost ≈ Avellaneda-Lee empirical 1.25. 2.0 over-waits. |
| Exit | **\|z\| ≤ 0.5 partial target** | OU-optimal; last increment to mean costs disproportionate time |
| Stops | **time-stop k·HL (k=3) + equilibrium-break + roll-jump**; wide \|z\|≥4 catastrophe only | non-price stops dominate for MR (Leung-Li) |
| Regime gate | **binary** VR(q)<1 (trade/no-trade) | weighted "quality score" is a forbidden overfit object here. Rolling-Hurst rejected (unstable short-window). |
| Sizing | inverse-σ (constant risk) | smooth equity by construction |
| **Roll firewall** | mask N=8 bars after a roll-jump (\|dSpread\|>k·σ) | continuous/back-adj spreads jump at rolls → **phantom MR**; must not trade relabeling events |
| **Cost-floor veto** | no trade unless expected capture ≥ **1.5× two-leg round-trip cost** | a spread that reverts but can't clear cost is a **NON-finding** |

**Literature anchors:** Bertram 2010 (Physica A 389:2234) · Leung-Li 2015 (arXiv:1411.5062) ·
Avellaneda-Lee 2010 (s-score, ±1.25 / 0.5–0.75, 60-day window, fast-reverter κ-filter).

## 3. Pre-registered kill triggers (anti-zombie; probation is not limbo)

1. **Structural break** — rolling OOS VR(20) > 0.70 for 2 consecutive quarters → KILL (the BRN precedent).
2. **OOS-decay** — OOS net expectancy < 50% of train, or OOS Sharpe < 0 over any rolling 12mo → KILL.
3. **Cost-floor** — gross capture < 1.0× realistic round-trip cost for a quarter → strategy OFF.
4. **Half-life drift** — HL exits [10,60] bars for 2 quarters → KILL (book-incompatible).
5. **Artifact re-check** — quarterly back-adj/splice surrogate through the live pipeline; if surrogate
   produces comparable "edge" → KILL (pipeline reading construction noise).
6. **Single-instrument lottery** — must survive ≥N pre-registered disjoint windows + cross-habitat OOS,
   else at most CONDITIONAL-SURVIVAL on the named instrument.

## 4. Honest caveats (adversarial lens — do not skip)

- **This reopens a partially-killed line.** This repo's AMR research already graded energy calendars
  **non-deployable** (NG PERSISTENT-BUT-UNECONOMIC ~7.5× cost gap; BRN MERELY-TRUE, OOS-broken post-2012;
  ZC CONTAMINATED; deseasonalization amplified apparent MR 2.5–4.5× via back-adjustment offsets). Under
  the MR-given frame we proceed, but the **prior is LOW** and the burden is on raw-construction +
  cost-clearing evidence.
- **Most likely failure = economics, not statistics.** Calendar spreads are among the most arbitraged
  term-structure objects; liquidity has competed gross edge toward the cost floor. The cost-floor veto
  (§2) is the control most likely to keep this permanently in "true-but-uneconomic."
- **Data hygiene is decisive:** trade **native dated / exchange-listed spreads**, never two back-adjusted
  continuations subtracted — that compounds two roll-offset artifact streams. The slow Kalman + roll mask
  mitigate in-code, but the *data choice* is the real fix.

## 5. Next high-information action

Backtest on **raw legs** available on disk (`data/raw/more-mean-reversion-data/`): build calendar pairs
from M1!/M2! legs present — e.g. **HO1!/HO2!, RB1!/RB2!, CL1!/CL2!, BRN1!/BRN2!, ZC1!/ZC2!, KC1!/KC2!,
GC1!/GC2!, SI1!/SI2!** (all have both legs). Run the strategy, then **surrogate-relative** (OU/RW/GARCH +
a back-adj/splice surrogate) before any "it works" claim. Report the **full search, never the argmax**.

> Status: **PROBATION** — built & ready to test; deployability is a posterior, not an assumption.
