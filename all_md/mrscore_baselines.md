---
name: mrscore-baselines
description: Empirically verified behavior of MRScore v1 (analytics_mrscore.py) — temporal honesty confirmed, plus the dangerous log-price spread failure and tie-rank bug
metadata:
  type: project
---

MRScore v1 (`app/services/analytics_mrscore.py`, endpoint `/api/v1/market/{id}/mrscore`) empirical review, 2026-06-02.

**Temporal honesty: CONFIRMED clean.** Future-injection (spike close[t0]×3–10) leaves all 17 output columns (incl. sub-features drc/hit_rate/vr_agg/msi/vsi/p_adf/p_kpss and every rank) bit-identical at bars < t0. Endpoint replay: stepping `end` forward one bar adds exactly one row, never alters prior rows (135k cell comparisons, 0 mismatches). causal_zscore genuinely excludes bar t (trailing std=0 → inf, proving current bar absent from denominator). DRC forward window never reads beyond its own last bar. inf from causal_zscore / vol_compression is correctly masked downstream (newey_west and rolling_percentile_rank strip non-finite) — never reaches mrscore or JSON.

**DRC baselines (n=500, lam=-0.2, sigma=0.5):** OU mean DRC ≈ -7.1 (94.5% power at -2.86). RW mean DRC ≈ -0.33, **false-positive rate 3.5%** at -2.86 over 200 seeds (NOT the claimed ~10%; better). _nw_lag(1)=1 not 0 — the "maxlag=0 at h=1" concern is moot; maxlag=0 works in statsmodels anyway.

**MOST DANGEROUS FINDING (CRITICAL): log-price assumption silently kills negative-price series.** block2_features and realized_vol call np.log(price) unconditionally. NG12 (a spread, min -2.18, 55% of bars ≤0) → DRC all-NaN → B2 all-NaN → mrscore n_scored=0, returned as clean nulls with NO error/warning. CLAUDE.md deployment domain IS spreads/pairs/cross-asset relative value — exactly the negative-capable instruments. Engine silently fails on its own target regime. Repro: any OU spread centered at 0.

**Self-ranked mrscore does NOT discriminate reverters from nulls** (confirmed): NULL_RW mrscore 62.5 > ANCHOR_OU 55.6. Raw DRC discriminates only IN EXPECTATION (many-seed): on the 5 blind packets, pure-RW BLIND_4 had DRC significant in 97.7% of windows vs true-OU BLIND_1 at 14.6% — single-instrument raw DRC is unreliable. The suite's discrimination test uses a strong-signal best case (seed 42, lam=-0.2, margin 1.0). blind_key mapping: B1=OU, B2=drift-RW, B3/B4=pure-RW, B5=real ADANIENT.

**rolling_percentile_rank tie bug (MEDIUM):** strict `<` under-counts ties → saturated features (MeanStab capped at 1.0, TCF=1.0) rank as 0 (WORST) on flat stretches, inverting meaning. Bites hard on constant/degenerate series; on realistic noisy OU it rarely triggers (5/579 bars), R_MSI stays ≈99.7. midrank convention would fix.

**Perf:** G1 (11399 bars) endpoint = 11.1s (per-bar Python loops over halflife/ADF/DRC); usable but sluggish for bar-stepping replay. hl_proximity(40)=1.1e-16 float dust — cosmetic only.

92 tests pass. See [[mrscore-baselines]].
