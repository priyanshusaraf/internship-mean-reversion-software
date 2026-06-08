# Strategy 03 — MR FALSIFIED (rigorously), TREND signal found

**Date:** 2026-06-09. Status: **major epistemic update.**

## What happened
The VR-gated z-score MR strategy (doc 02) showed **consistent NEGATIVE returns on TradingView**
across ~13 instruments (2 winners, 2 catastrophic sizing blow-ups, rest losing). Root causes:
1. **Overfit "validation"** — cherry-picked pairs on one dataset with a weak 30% holdout. Not real OOS.
2. **Object mismatch** — validated log-ratio `ln A − ln B`; deployed difference `A − B` (dominated by the
   larger-scale leg; for HO1!-CL1! it's ≈ −CL, not a crack).
3. **Sizing BUG** — vol-sizing exploded on difference spreads → −$3.7M / −890% on $100k.

## The rigorous test (`scripts/walkforward_statarb.py`)
Walk-forward, Engle-Granger cointegration selected on TRAIN only, β frozen, traded on the next
UNSEEN window, concatenated true-OOS. No post-hoc pair selection. 24 instruments → 276 pairs, 70 with
enough overlap, 26.8% of windows cointegrated.

**RESULT — MR FALSIFIED on this universe:**
- Full 66-pair book OOS: **totR −30, Sharpe −0.14 (NEGATIVE).**
- Persistent cointegrated pairs (28): totR +10, **Sharpe 0.06, R² 0.05** — statistical noise.
- 30/66 pairs OOS-positive ≈ coin flip.

Verdict: **technical mean-reversion has no robust, deployable edge on these daily commodity instruments.**
Independently reproduces this repo's AMR conclusion (trend-heavy markets; MR uneconomic net of costs).

## The trend signal (`scripts/trend_test.py`)
Same instruments, simple Donchian-55/20 breakout + ATR trailing stop (Turtle-style), no optimization:
- **15/26 instruments profitable; pooled book totR +133, totR/DD ≈ 2.0, positive.**
- Strong names: CL1! (totR/DD 5.70, PF 1.63), CT1! (5.41), SB1! (3.40), ZC1! (3.33), GF1! (3.18), KE1! (3.14).
- Profile is the inverse of MR: ~37% win, small frequent losses, occasional large winners.

## Interpretation
The data has **trend** structure, not mean-reversion structure. A **diversified multi-instrument
trend-following book** (the CTA/managed-futures shape) is the evidence-backed path to the user's actual
goal (smooth equity, consistency, ≥5 instruments) — diversification across uncorrelated trend bets is
historically among the smoothest return streams. MR fights the data; trend rides it.

## Caveats (don't repeat the overfit mistake)
- The trend result is a SINGLE first-cut config, NOT yet walk-forward validated. It must get the same
  rigorous train→test→roll treatment before any deployment claim.
- Trend-following on a SINGLE instrument is choppy; smoothness comes from the DIVERSIFIED book + vol-targeting.

## Next high-information action
Decide direction (MR is dead; pivot to trend or regime-switch), then apply the walk-forward harness to
the trend strategy and build a vol-targeted diversified book.

> Status: MR **REJECTED** (rigorous OOS). Trend-following **PROMISING, unvalidated** — pending walk-forward.
