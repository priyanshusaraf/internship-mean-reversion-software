# Strategy 05 — MR book on the new commodities data (final, honest)

**Date:** 2026-06-09. Data: `/Users/priyanshusaraf/Downloads/commodities-data/daily` (23 outright M1 legs).
Test harness: `strategy-tests/mr_book.py`. Deployable: `scripts/spread_mr_strategy.pine`.

## Method (the distilled MR strategy)
Cross-commodity log-ratio spreads `ln A − β·ln B`; β from TRAIN OLS frozen for TEST (causal);
Engle-Granger cointegration + half-life gate; discrete z-MR (enter |z|≥2, exit |z|≤0.5, z-disaster 4,
time-stop 60); vol-targeted equal-risk BOOK across active spreads. True walk-forward OOS.

## Result — MR does NOT clear the bar
- **All-pairs book (253): Sharpe −0.62.** "Top" spreads were economic nonsense (PL-ZL, BRN-ZC) =
  spurious cointegration from screening 253 pairs.
- **Curated economic pairs (26): Sharpe −0.44.** Even Brent-WTI (BRN-WBS), the most-cointegrated
  spread in commodities, LOSES.
- **Gross of cost (cost=0): OOS Sharpe 0.01** — the edge is ~zero before costs. In-sample is *negative*,
  meaning 2σ stretches slightly CONTINUE (momentum), not revert. Consistent with trend-heavy markets.
- **Positive in BOTH IS and OOS: only SI-HG, CC-SB, WBS-RB** (3/26). And CC-SB / CC-KC have
  return-correlation ≈ 0 → **spurious** (cocoa isn't linked to sugar/coffee).

## What honestly survives (weak, real)
| pair | legA/legB/β | Sharpe | note |
|---|---|---|---|
| SI-HG | SI1!/HG1!/0.62 | 0.29 | silver vs copper; ret-corr 0.40 — real |
| WBS-RB | WBS1!/RB1!/1.28 | 0.17 | WTI vs gasoline (crack); ret-corr 0.31 — real |
| HG-PL | HG1!/PL1!/0.83 | regime | copper vs platinum; +50 OOS but −30 IS — unreliable |

## Verdict
**Mean-reversion yields ~2 economically-defensible spreads at Sharpe ~0.2–0.3 — NOT a smooth,
consistent, multi-instrument book.** The goal (smooth equity, ≥5 instruments) is not achievable with MR
on this data; the edge is too thin and too few pairs survive. This is the third independent rigorous
confirmation (old data MR, trend books, new data MR) that simple technical edges don't survive here.

## Deliverable
`scripts/spread_mr_strategy.pine` — CORRECT, bug-free, sizing-capped spread-MR tool. Deploy ONLY on
SI/HG and WBS/RB (small size). It is a real but modest edge, honestly labeled. The path to the actual
goal remains a diversified cross-asset (bonds/FX/equity-index) trend book — a data problem, not a tuning one.

> Status: MR **REJECTED as a book**; 2 weak survivor pairs shipped honestly. Goal unmet by MR on this data.
