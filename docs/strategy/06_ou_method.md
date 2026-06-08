# Strategy 06 — OU-gated spread MR: the verified method, honestly tested

**Date:** 2026-06-09. Source: `/deep-research` (105 agents, 23 sources, 22/25 claims verified) →
implementation `strategy-tests/ou_spread_mr.py` → deployable `scripts/ou_spread_mr.pine`.

## What the research actually says (replaces "stack indicators and hope")
Professionals don't combine ADX+ATR+Supertrend+Ichimoku+RSI. The verified pipeline is:
1. **Model the spread as Ornstein-Uhlenbeck / AR(1)**, signal = dimensionless z-score (Avellaneda-Lee).
2. **Mean-reversion SPEED is a tradability GATE** — estimate half-life (regress ΔX on X_lag → b<0,
   HL=−ln2/b); trade only fast reverters; **stop when HL blows out** (this IS the OOS-break kill).
3. **Hedge ratio is first-class** — static OLS β drifts; Kalman/TLS preferred; **economic weights
   (crush/crack) avoid the rolling-β artifact entirely** (aligns with our own doc-14/19).
4. **Exit near the mean, not on sign-flip** — verified win-rate lever (Mitchell 2010: → ~73% win, lower
   profit vol).
5. **Dominant caveat (verified 3-0):** every OOS-tested strategy in the corpus degraded — negative
   Sharpes, exploded DD, crush +$200→−$20/trade. After-cost OOS deployability is fragile.

## What our test found (9 spreads, 2006–2026, causal, IS/OOS split)
| finding | result |
|---|---|
| Win rate | 45–58% (NOT the literature's 73%); **avgLoss > avgWin everywhere** → fat left tail → neg expectancy |
| Selectivity (↑z_entry) | **LOWERS** win rate here (52%→41%) — commodity extremes *continue*, not revert. Real structural difference from equity stat-arb / crush. |
| Exit-near-mean lever | **Confirmed** — `z_exit=0.5` beats `0.0` on win% and OOS Sharpe (the one finding that transfers). |
| The BOOK (9 spreads) | **flat-to-negative** (Sharpe −0.47 base; ~0 to +0.26 at best config). "Diversification = smoothness" was flagged UNVERIFIED by the research; here it does not hold. |
| OOS survivor | **silver-copper (SI1!/HG1!)** only: OOS win 52%, Sharpe 0.48, maxDD −25%, eqR² 0.80. Gold-silver marginal. |

This is the **fourth independent rigorous confirmation** (old-data MR, trend books, new-data MR book,
now OU-gated) that simple technical edges don't produce a smooth multi-instrument book on this data.

## Verdict
The OU method is **real and correctly built** — it is a genuine improvement over indicator-stacking
because the half-life gate + break-kill stop it trading dead spreads. But on this back-adjusted
continuous-commodity data it yields **one OOS-positive spread (silver-copper) and a flat book**, not a
smooth ≥5-instrument curve. The bottleneck is the data/universe (back-adjusted, commodity-concentrated,
extremes that trend), exactly as docs 04–05 concluded — not the strategy.

## Deliverable
`scripts/ou_spread_mr.pine` — apply to a **native TradingView spread symbol** (`SI1!/HG1!`,
`BRN1!-WBS1!`, `NG1!-NG2!`) so it runs single-instrument on the synthetic close (no request.security
chart−chart=0 trap) with fixed qty=1 → **it takes trades and shows an equity curve**. Defaults
(z_entry 2.0, z_exit 0.5, z_stop 3.0, HL∈[2,40]) are the most OOS-robust found. **Deploy on SI1!/HG1!
(real, modest, high-ish win rate); treat others as flat.** High win rate ⟺ fat left tail is the MR
identity — cannot be engineered away, only managed by the disaster stop.

> Status: method VERIFIED & SHIPPED; smooth ≥5-instrument book remains UNMET on this data (4th confirm).
> Honest single survivor = silver-copper. Path to the goal is still broader/cleaner cross-asset data.
