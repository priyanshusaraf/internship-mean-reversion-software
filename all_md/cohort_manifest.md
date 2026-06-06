# Arm 0 — Cohort Provenance & Quality Manifest

**Generated:** 2026-06-03 · **Pre-registration:** `docs/research/12_institutional_review_post_state_t.md` §7
**Scope:** foundation hygiene ONLY — schema · date hygiene · provenance · sample adequacy · price integrity.
No reversion/VR/Hurst/half-life/OU/ADF/stationarity/cointegration statistic. No habitat/morphology/timing inference.
**Floors:** TRUSTED ≥ 750 usable bars · UNUSABLE < 504.
**Legs on disk for any spread:** NO → every spread's hedge-ratio causality is **unverifiable** → CONTAMINATED (conservative default, §5).
**§6 synthetic-spread rule applied:** for every spread, Open/Close are TRUSTED (synchronized) but **High/Low are UNTRUSTED** (leg extrema at different timestamps → counterfactual spread states).

**Dispositions:** TRUSTED 3 · PROVISIONAL 1 · CONTAMINATED 8 · UNUSABLE 4

| instrument | domain | depl? | res | usable | ts-integrity | OHLC H/L | neg | disp | conf | wl |
|---|---|:--:|:--:|--:|---|:--:|:--:|---|:--:|:--:|
| `aapl_60` | equity | · | 60m | 20026 | mixed_tz(normalized_UTC); large_gaps:2868 | ok | · | **TRUSTED** | HIGH | ✓ |
| `dell_60` | equity | · | 60m | 13025 | mixed_tz(normalized_UTC); large_gaps:1867 | ok | · | **TRUSTED** | HIGH | ✓ |
| `adanient` | equity | · | 1d | 2463 | ok | ok | · | **TRUSTED** | HIGH | ✓ |
| `g1_gold` | commodity_outright | Y | 1d | 11485 | reversed | ok | · | **PROVISIONAL** | MEDIUM | · |
| `cl_brn_spread_60` | spread_or_pair | Y | 60m | 19399 | mixed_tz(normalized_UTC); large_gaps:175 | UNTRUST | Y | **CONTAMINATED** | HIGH | · |
| `ng12_spread` | spread_or_pair | Y | 1d | 5348 | reversed; large_gaps:5 | UNTRUST | Y | **CONTAMINATED** | HIGH | · |
| `rb23_spread` | spread_or_pair | Y | 1d | 5170 | reversed | UNTRUST | Y | **CONTAMINATED** | HIGH | · |
| `coffee_cocoa_spread_1d` | spread_or_pair | Y | 1d | 673 | ok | UNTRUST | Y | **CONTAMINATED** | HIGH | · |
| `hdfc_icici_spread_15` | spread_or_pair | Y | 15m | 504 | large_gaps:20 | UNTRUST | Y | **CONTAMINATED** | HIGH | · |
| `hdfc_icici_spread_1d` | spread_or_pair | Y | 1d | 504 | ok | UNTRUST | Y | **CONTAMINATED** | HIGH | · |
| `coffee_cocoa_spread_15` | spread_or_pair | Y | 15m | 309 | large_gaps:9 | UNTRUST | Y | **CONTAMINATED** | HIGH | · |
| `coffee_cocoa_spread_60` | spread_or_pair | Y | 60m | 301 | large_gaps:34 | UNTRUST | Y | **CONTAMINATED** | HIGH | · |
| `nifty_synthetic` | synthetic | · | 1d | 500 | ok | ok | · | **UNUSABLE** | HIGH | · |
| `eurusd_60` | fx | · | 60m | 388 | large_gaps:3 | ok | · | **UNUSABLE** | HIGH | · |
| `eurusd_1d` | fx | · | 1d | 387 | ok | ok | · | **UNUSABLE** | HIGH | · |
| `banknifty_1d` | index | · | 1d | 386 | ok | ok | · | **UNUSABLE** | HIGH | · |

### Per-instrument detail
- **`aapl_60`** — TRUSTED (confidence HIGH)
  - reason: single-asset, monotone ascending dates, usable_bars 20026>=750, self-documenting positive-price units, OHLC structurally valid
  - usable_bars 20026 · resolution 60m · span 2015-01-02..2026-06-01 · timestamp_integrity: mixed_tz(normalized_UTC); large_gaps:2868
  - provenance: equity (self-evident) · negative_price_handling: n/a (strictly positive price series)
  - OHLC trust: all OHLC trusted (single-asset intrabar extrema are real synchronized observations)
- **`adanient`** — TRUSTED (confidence HIGH)
  - reason: single-asset, monotone ascending dates, usable_bars 2463>=750, self-documenting positive-price units, OHLC structurally valid
  - usable_bars 2463 · resolution 1d · span 2012-10-10..2022-10-07 · timestamp_integrity: ok
  - provenance: equity (self-evident) · negative_price_handling: n/a (strictly positive price series)
  - OHLC trust: all OHLC trusted (single-asset intrabar extrema are real synchronized observations)
- **`dell_60`** — TRUSTED (confidence HIGH)
  - reason: single-asset, monotone ascending dates, usable_bars 13025>=750, self-documenting positive-price units, OHLC structurally valid
  - usable_bars 13025 · resolution 60m · span 2018-12-21..2026-06-01 · timestamp_integrity: mixed_tz(normalized_UTC); large_gaps:1867
  - provenance: equity (self-evident) · negative_price_handling: n/a (strictly positive price series)
  - OHLC trust: all OHLC trusted (single-asset intrabar extrema are real synchronized observations)
- **`g1_gold`** — PROVISIONAL (confidence MEDIUM)
  - reason: fixable hygiene: reversed dates (re-sort); 1 degenerate row(s) (drop); back-adjusted CONTINUOUS futures (g1); roll/adjustment method undocumented -> historical levels construction-dependent (provenance flag).; NOT whitelisted until fixed + re-checked
  - usable_bars 11485 · resolution 1d · span 1981-04-06..2026-04-14 · timestamp_integrity: reversed
  - provenance: commodity_outright (self-evident) · negative_price_handling: n/a (strictly positive price series)
  - OHLC trust: all OHLC trusted (single-asset intrabar extrema are real synchronized observations)
  - notes: back-adjusted CONTINUOUS futures (g1); roll/adjustment method undocumented -> historical levels construction-dependent (provenance flag). | 630 structurally-invalid OHLC bar(s).
- **`cl_brn_spread_60`** — CONTAMINATED (confidence HIGH)
  - reason: leg-stripped precompute; legs absent on disk; hedge-ratio causality UNVERIFIABLE (full-sample-fit => lookahead-stationarity indistinguishable from real MR); §6: High/Low untrusted (counterfactual leg extrema)
  - usable_bars 19399 · resolution 60m · span 2023-02-20..2026-06-02 · timestamp_integrity: mixed_tz(normalized_UTC); large_gaps:175
  - provenance: spread (legs absent, hedge-ratio unverifiable) · negative_price_handling: LEVEL-DIFF required (1431 negative-close bars); log/return math forbidden
  - OHLC trust: Open/Close TRUSTED (synchronized); HIGH/LOW UNTRUSTED — leg extrema occur at different timestamps so max(A-B)!=max(A)-max(B); Volume/OI conditional (per-leg only)
  - notes: §6: spread High/Low are counterfactual (untrusted by default) — any downstream use MUST rely on Open/Close, never naive High/Low, absent synchronized intrabar reconstruction. | negative prices present -> downstream must use level differences, not log/returns.
- **`coffee_cocoa_spread_15`** — CONTAMINATED (confidence HIGH)
  - reason: leg-stripped precompute; legs absent on disk; hedge-ratio causality UNVERIFIABLE (full-sample-fit => lookahead-stationarity indistinguishable from real MR); §6: High/Low untrusted (counterfactual leg extrema); also underpowered (309<504)
  - usable_bars 309 · resolution 15m · span 2026-05-19..2026-06-02 · timestamp_integrity: large_gaps:9
  - provenance: spread (legs absent, hedge-ratio unverifiable) · negative_price_handling: LEVEL-DIFF required (309 negative-close bars); log/return math forbidden
  - OHLC trust: Open/Close TRUSTED (synchronized); HIGH/LOW UNTRUSTED — leg extrema occur at different timestamps so max(A-B)!=max(A)-max(B); Volume/OI conditional (per-leg only)
  - notes: §6: spread High/Low are counterfactual (untrusted by default) — any downstream use MUST rely on Open/Close, never naive High/Low, absent synchronized intrabar reconstruction. | negative prices present -> downstream must use level differences, not log/returns.
- **`coffee_cocoa_spread_1d`** — CONTAMINATED (confidence HIGH)
  - reason: leg-stripped precompute; legs absent on disk; hedge-ratio causality UNVERIFIABLE (full-sample-fit => lookahead-stationarity indistinguishable from real MR); §6: High/Low untrusted (counterfactual leg extrema)
  - usable_bars 673 · resolution 1d · span 2023-09-27..2026-06-02 · timestamp_integrity: ok
  - provenance: spread (legs absent, hedge-ratio unverifiable) · negative_price_handling: LEVEL-DIFF required (673 negative-close bars); log/return math forbidden
  - OHLC trust: Open/Close TRUSTED (synchronized); HIGH/LOW UNTRUSTED — leg extrema occur at different timestamps so max(A-B)!=max(A)-max(B); Volume/OI conditional (per-leg only)
  - notes: §6: spread High/Low are counterfactual (untrusted by default) — any downstream use MUST rely on Open/Close, never naive High/Low, absent synchronized intrabar reconstruction. | negative prices present -> downstream must use level differences, not log/returns.
- **`coffee_cocoa_spread_60`** — CONTAMINATED (confidence HIGH)
  - reason: leg-stripped precompute; legs absent on disk; hedge-ratio causality UNVERIFIABLE (full-sample-fit => lookahead-stationarity indistinguishable from real MR); §6: High/Low untrusted (counterfactual leg extrema); also underpowered (301<504)
  - usable_bars 301 · resolution 60m · span 2026-04-14..2026-06-02 · timestamp_integrity: large_gaps:34
  - provenance: spread (legs absent, hedge-ratio unverifiable) · negative_price_handling: LEVEL-DIFF required (301 negative-close bars); log/return math forbidden
  - OHLC trust: Open/Close TRUSTED (synchronized); HIGH/LOW UNTRUSTED — leg extrema occur at different timestamps so max(A-B)!=max(A)-max(B); Volume/OI conditional (per-leg only)
  - notes: §6: spread High/Low are counterfactual (untrusted by default) — any downstream use MUST rely on Open/Close, never naive High/Low, absent synchronized intrabar reconstruction. | negative prices present -> downstream must use level differences, not log/returns.
- **`hdfc_icici_spread_15`** — CONTAMINATED (confidence HIGH)
  - reason: leg-stripped precompute; legs absent on disk; hedge-ratio causality UNVERIFIABLE (full-sample-fit => lookahead-stationarity indistinguishable from real MR); §6: High/Low untrusted (counterfactual leg extrema)
  - usable_bars 504 · resolution 15m · span 2026-05-04..2026-06-02 · timestamp_integrity: large_gaps:20
  - provenance: spread (legs absent, hedge-ratio unverifiable) · negative_price_handling: LEVEL-DIFF required (504 negative-close bars); log/return math forbidden
  - OHLC trust: Open/Close TRUSTED (synchronized); HIGH/LOW UNTRUSTED — leg extrema occur at different timestamps so max(A-B)!=max(A)-max(B); Volume/OI conditional (per-leg only)
  - notes: §6: spread High/Low are counterfactual (untrusted by default) — any downstream use MUST rely on Open/Close, never naive High/Low, absent synchronized intrabar reconstruction. | negative prices present -> downstream must use level differences, not log/returns.
- **`hdfc_icici_spread_1d`** — CONTAMINATED (confidence HIGH)
  - reason: leg-stripped precompute; legs absent on disk; hedge-ratio causality UNVERIFIABLE (full-sample-fit => lookahead-stationarity indistinguishable from real MR); §6: High/Low untrusted (counterfactual leg extrema)
  - usable_bars 504 · resolution 1d · span 2024-05-21..2026-06-02 · timestamp_integrity: ok
  - provenance: spread (legs absent, hedge-ratio unverifiable) · negative_price_handling: LEVEL-DIFF required (504 negative-close bars); log/return math forbidden
  - OHLC trust: Open/Close TRUSTED (synchronized); HIGH/LOW UNTRUSTED — leg extrema occur at different timestamps so max(A-B)!=max(A)-max(B); Volume/OI conditional (per-leg only)
  - notes: §6: spread High/Low are counterfactual (untrusted by default) — any downstream use MUST rely on Open/Close, never naive High/Low, absent synchronized intrabar reconstruction. | negative prices present -> downstream must use level differences, not log/returns.
- **`ng12_spread`** — CONTAMINATED (confidence HIGH)
  - reason: leg-stripped precompute; legs absent on disk; hedge-ratio causality UNVERIFIABLE (full-sample-fit => lookahead-stationarity indistinguishable from real MR); §6: High/Low untrusted (counterfactual leg extrema); also reversed dates
  - usable_bars 5348 · resolution 1d · span 2001-04-27..2026-04-15 · timestamp_integrity: reversed; large_gaps:5
  - provenance: spread (legs absent, hedge-ratio unverifiable) · negative_price_handling: LEVEL-DIFF required (4328 negative-close bars); log/return math forbidden
  - OHLC trust: Open/Close TRUSTED (synchronized); HIGH/LOW UNTRUSTED — leg extrema occur at different timestamps so max(A-B)!=max(A)-max(B); Volume/OI conditional (per-leg only)
  - notes: §6: spread High/Low are counterfactual (untrusted by default) — any downstream use MUST rely on Open/Close, never naive High/Low, absent synchronized intrabar reconstruction. | negative prices present -> downstream must use level differences, not log/returns. | 169 structurally-invalid OHLC bar(s).
- **`rb23_spread`** — CONTAMINATED (confidence HIGH)
  - reason: leg-stripped precompute; legs absent on disk; hedge-ratio causality UNVERIFIABLE (full-sample-fit => lookahead-stationarity indistinguishable from real MR); §6: High/Low untrusted (counterfactual leg extrema); also reversed dates
  - usable_bars 5170 · resolution 1d · span 2005-10-03..2026-04-15 · timestamp_integrity: reversed
  - provenance: spread (legs absent, hedge-ratio unverifiable) · negative_price_handling: LEVEL-DIFF required (1998 negative-close bars); log/return math forbidden
  - OHLC trust: Open/Close TRUSTED (synchronized); HIGH/LOW UNTRUSTED — leg extrema occur at different timestamps so max(A-B)!=max(A)-max(B); Volume/OI conditional (per-leg only)
  - notes: §6: spread High/Low are counterfactual (untrusted by default) — any downstream use MUST rely on Open/Close, never naive High/Low, absent synchronized intrabar reconstruction. | negative prices present -> downstream must use level differences, not log/returns. | 35 structurally-invalid OHLC bar(s).
- **`banknifty_1d`** — UNUSABLE (confidence HIGH)
  - reason: usable_bars 386 < power floor 504
  - usable_bars 386 · resolution 1d · span 2024-11-07..2026-06-02 · timestamp_integrity: ok
  - provenance: index (self-evident) · negative_price_handling: n/a (strictly positive price series)
  - OHLC trust: all OHLC trusted (single-asset intrabar extrema are real synchronized observations)
- **`eurusd_1d`** — UNUSABLE (confidence HIGH)
  - reason: usable_bars 387 < power floor 504
  - usable_bars 387 · resolution 1d · span 2024-12-03..2026-06-02 · timestamp_integrity: ok
  - provenance: fx (self-evident) · negative_price_handling: n/a (strictly positive price series)
  - OHLC trust: all OHLC trusted (single-asset intrabar extrema are real synchronized observations)
- **`eurusd_60`** — UNUSABLE (confidence HIGH)
  - reason: usable_bars 388 < power floor 504
  - usable_bars 388 · resolution 60m · span 2026-05-11..2026-06-02 · timestamp_integrity: large_gaps:3
  - provenance: fx (self-evident) · negative_price_handling: n/a (strictly positive price series)
  - OHLC trust: all OHLC trusted (single-asset intrabar extrema are real synchronized observations)
- **`nifty_synthetic`** — UNUSABLE (confidence HIGH)
  - reason: usable_bars 500 < power floor 504
  - usable_bars 500 · resolution 1d · span 2022-01-03..2023-12-01 · timestamp_integrity: ok
  - provenance: synthetic (self-evident) · negative_price_handling: n/a (strictly positive price series)
  - OHLC trust: all OHLC trusted (single-asset intrabar extrema are real synchronized observations)

## TRUSTED whitelist
`['aapl_60', 'adanient', 'dell_60']`

## PROVISIONAL list
`['g1_gold']`

## CONTAMINATED list
`['cl_brn_spread_60', 'coffee_cocoa_spread_15', 'coffee_cocoa_spread_1d', 'coffee_cocoa_spread_60', 'hdfc_icici_spread_15', 'hdfc_icici_spread_1d', 'ng12_spread', 'rb23_spread']`

## UNUSABLE list
`['banknifty_1d', 'eurusd_1d', 'eurusd_60', 'nifty_synthetic']`

### Interpretation notes (pre-reg gaps resolved conservatively)
- **Bar-floor band [504,750):** unbucketed in the pre-reg → resolved conservatively to PROVISIONAL (NOT whitelisted): clears the power floor but lacks the independent-window margin for a TRUSTED verdict.
- **'daily-equivalent' floor on intraday series:** applied to **raw bar count** (no effective-sample conversion — that would be new methodology). Intraday autocorrelation/twins recorded as flags only.
- **CONTAMINATED ≠ UNUSABLE:** contaminated series are excluded from any Arm-A OU/habitat verdict but may still feed null-relative checks that assume no stationarity (per pre-reg).
- **Provenance classification (NOT habitat inference):** domain labels are construction facts, not reversion claims. Deployment-domain instruments on the whitelist: **0** (none).

## ANSWER — which instruments may legally participate in Arm A?
> **`['aapl_60', 'adanient', 'dell_60']`** — and ONLY these. (All are single-name equities by classification; 0 deployment-domain instruments qualify. No reversion/habitat claim is made or implied.)
