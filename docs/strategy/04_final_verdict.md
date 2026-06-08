# Strategy 04 — Final verdict: no robust smooth book on THIS data (MR and trend both)

**Date:** 2026-06-09. Terminal outcome of the trading-strategy workstream: **rigorous falsification.**

## What was tested (all causal, all out-of-sample checked)
| Approach | Method | OOS result |
|---|---|---|
| MR z-score / RSI (single-instrument) | TV deploy + Python | consistent NEGATIVE; 2/13 positive ≈ noise |
| MR cointegration pairs | **walk-forward** Engle-Granger, β frozen, true OOS | full book totR −30 (Sharpe −0.14); persistent pairs flat (Sharpe 0.06) |
| Trend Donchian (per-trade R) | pooled R | looked +133R / rdd 2.0 — **artifact** (per-trade weighting flatters trend) |
| Trend TSMOM | **vol-targeted daily book** | Sharpe −0.04 (flat) |
| Trend Donchian-state | **vol-targeted daily book** | Sharpe −0.22 (smoothly negative) |
| Regime-switch hybrid (trend+MR) | daily | worse than trend alone; MR leg = −339k (+ blow-up). Trend leg +78R only |

## Verdict
On this dataset — **TradingView back-adjusted continuous commodity futures + 2 indices, daily,
~1990–2026** — **no standard systematic technical strategy (mean-reversion OR trend-following, in any
form tested) produces a robust, smooth, profitable book out-of-sample.** Properly vol-targeted daily
portfolios are flat-to-negative. This independently reproduces the entire AMR programme's conclusion.

## Why (honest diagnosis — these are confounds, not excuses)
1. **Universe too narrow / commodity-concentrated.** Real trend (CTA/TSMOM) smoothness comes from
   diversifying across *bonds, rates, FX, equity indices, crypto* — low-correlated sleeves. 20+
   commodities + 1 index is the *weakest* TSMOM sleeve and highly cross-correlated → no diversification.
2. **Back-adjusted continuous contracts** distort both momentum and reversion signals at roll seams.
3. **OOS period (≈2012–2020) was the documented "trend drought"** for CTAs AND a chop regime for
   commodities — the worst possible hold-out for trend.
4. **Costs** modeled generously (1–2bp); real costs are worse.

NOTE: individual instruments ARE positive standalone (SPX Sharpe 0.46, CL/HG 0.33) — it is the
*smooth diversified book* that this narrow universe cannot produce.

## What would actually hit the goal (smooth, consistent, ≥5 instruments)
1. **Broader cross-asset data** (HIGHEST leverage): add Treasury/Bund futures, FX majors, more equity
   indices (ES/NQ/RTY/DAX/Nikkei), maybe crypto. A diversified vol-targeted trend book across ~30–50
   low-correlation markets is the textbook smooth Sharpe≈0.8–1.2 strategy. The engine is built
   (`scripts/tsmom_portfolio.py`); it needs the data.
2. **Cleaner data** — properly-rolled or dated contracts, not TV back-adjusted continuous.
3. Accept a **modest single-instrument edge** (e.g. SPX trend) rather than a smooth multi-asset book.

## Artifacts
`scripts/walkforward_statarb.py` (MR walk-forward) · `scripts/trend_test.py` (Donchian R) ·
`scripts/hybrid_bt.py` (regime-switch) · `scripts/tsmom_portfolio.py` (vol-targeted books).

> Status: technical MR and trend **REJECTED as smooth deployable books on this data**. Path forward is
> a broader/cleaner cross-asset universe — a data problem, not a strategy-tuning problem. Stopping here
> is the honest result; more tuning on this data = curve-fitting.
