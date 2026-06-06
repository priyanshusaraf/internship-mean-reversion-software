# MR Cohort — Provenance & Quality Manifest (deep leg cohort)

**Generated:** 2026-06-03 · **Source:** `~/Downloads/mean-reversion-data` · **Pre-reg:** doc 12 §7 (Arm 0 extension)
**Scope:** foundation hygiene ONLY (schema/dates/provenance/depth/price-integrity). No reversion/VR/OU statistic. Conservative defaults.
**Floors:** TRUSTED ≥ 750 daily bars · UNUSABLE < 504. These are LEGS; spread trust depends on construction (canonical spread protocol).

**Dispositions (all timeframes):** TRUSTED 46 · PROVISIONAL 16 · UNUSABLE 0

## Constructible causal spreads (legs available at daily depth)
| spread | method | min daily bars | constructible | note |
|---|---|--:|:--:|---|
| USD/INR calendar | calendar β=1 | 3344 | ✓ | cleanest causal spread at depth (same contract, adjacent months) |
| HDFC–ICICI pair | pair, rolling β | 5543 | ✓ | canonical MR habitat; deep real cash legs; lagged rolling β |
| Gold–Silver | intercommodity, β | 8786 | ✓ | metals substitution; both 2nd-month continuous |
| Gold–Copper | intercommodity, β | 8786 | ✓ | macro vs industrial metal |
| Platinum–Palladium | intercommodity, β | 10261 | ✓ | PGM substitution; platinum is TVC composite (trim) |
| WTI–Brent | intercommodity, β | 2638 | ✓ | KNOWN ~2010 structural break; mixed sources/sessions |
| TCS–INFY (IT pair) | pair, rolling β | 5370 | ✓ | Indian IT cointegration candidate; cross-venue BSE/NSE |

## Daily legs by disposition
- **`CBOT_DL_ZC1!`** [futures_continuous] — TRUSTED · 14189 bars · 1970-01-05..2026-06-03
  - flags: TradingView continuous (1!/2!) — verify roll/back-adjustment before differencing; calendar legality requires 1!&2! aligned & same roll
- **`COMEX_DL_SI2!`** [futures_continuous] — TRUSTED · 11186 bars · 1981-12-17..2026-06-03
  - flags: TradingView continuous (1!/2!) — verify roll/back-adjustment before differencing; calendar legality requires 1!&2! aligned & same roll
- **`NYMEX_DL_PA1!`** [futures_continuous] — TRUSTED · 10261 bars · 1985-08-26..2026-06-03
  - flags: TradingView continuous (1!/2!) — verify roll/back-adjustment before differencing; calendar legality requires 1!&2! aligned & same roll
- **`ICEEUR_DLY_BRN1!`** [futures_continuous] — TRUSTED · 9526 bars · 1989-03-01..2026-06-03
  - flags: TradingView continuous (1!/2!) — verify roll/back-adjustment before differencing; calendar legality requires 1!&2! aligned & same roll
- **`COMEX_DL_HG1!`** [futures_continuous] — TRUSTED · 9517 bars · 1988-07-29..2026-06-03
  - flags: TradingView continuous (1!/2!) — verify roll/back-adjustment before differencing; calendar legality requires 1!&2! aligned & same roll
- **`COMEX_DL_GC2!`** [futures_continuous] — TRUSTED · 8786 bars · 1991-06-26..2026-06-03
  - flags: TradingView continuous (1!/2!) — verify roll/back-adjustment before differencing; calendar legality requires 1!&2! aligned & same roll
- **`NSE_DLY_WIPRO`** [cash_equity] — TRUSTED · 7468 bars · 1996-05-02..2026-06-03
- **`BATS_MSFT`** [cash_equity] — TRUSTED · 7114 bars · 1998-02-20..2026-06-02
- **`BSE_DLY_ICICIBANK`** [cash_equity] — TRUSTED · 6866 bars · 1998-08-25..2026-06-03
- **`CAPITALCOM_COCOA`** [broker_cfd_spot] — TRUSTED · 6709 bars · 1998-08-27..2026-06-03
- **`NSE_DLY_INFY`** [cash_equity] — TRUSTED · 6530 bars · 2000-01-24..2026-06-03
- **`OANDA_USDJPY`** [fx] — TRUSTED · 6254 bars · 2002-05-06..2026-06-03
- **`BSE_DLY_HDFCBANK`** [cash_equity] — TRUSTED · 5543 bars · 2003-10-29..2026-06-03
- **`BSE_DLY_TCS`** [cash_equity] — TRUSTED · 5370 bars · 2004-08-31..2026-06-03
- **`FOREXCOM_USDCHF`** [fx] — TRUSTED · 5307 bars · 2006-01-03..2026-06-03
- **`BATS_NVDA`** [cash_equity] — TRUSTED · 5084 bars · 2006-03-17..2026-06-02
- **`FX_IDC_INRUSD`** [fx] — TRUSTED · 4956 bars · 2007-06-04..2026-06-03
- **`CME_MINI_DL_MIR2!`** [futures_continuous] — TRUSTED · 3361 bars · 2013-01-28..2026-06-03
  - flags: TradingView continuous (1!/2!) — verify roll/back-adjustment before differencing; calendar legality requires 1!&2! aligned & same roll
- **`CME_MINI_DL_MIR1!`** [futures_continuous] — TRUSTED · 3344 bars · 2013-01-28..2026-06-03
  - flags: TradingView continuous (1!/2!) — verify roll/back-adjustment before differencing; calendar legality requires 1!&2! aligned & same roll
- **`CFI_WTI`** [broker_cfd_spot] — TRUSTED · 2638 bars · 2014-02-26..2026-06-03
- **`FOREXCOM_COFFEE`** [broker_cfd_spot] — TRUSTED · 1785 bars · 2019-04-04..2026-06-03
- **`BATS_PLTR`** [cash_equity] — TRUSTED · 1424 bars · 2020-09-30..2026-06-02
- **`TVC_SILVER`** [composite_index] — PROVISIONAL · 14805 bars · 1802-01-04..2026-06-03 (daily-era 1998-10-16, 7001b)
  - flags: TVC composite — spliced/synthetic; early history is low-frequency proxy (flat O=H=L=C bars=6700); usable only from daily-era start 1998-10-16 (~7001 genuine-daily bars)
- **`TVC_DXY`** [composite_index] — PROVISIONAL · 14042 bars · 1967-01-31..2026-06-03 (daily-era 1971-01-04, 13994b)
  - flags: TVC composite — spliced/synthetic; early history is low-frequency proxy (flat O=H=L=C bars=3760); usable only from daily-era start 1971-01-04 (~13994 genuine-daily bars)
- **`TVC_PLATINUM`** [composite_index] — PROVISIONAL · 10576 bars · 1984-06-26..2026-06-03 (daily-era None, 10576b)
  - flags: TVC composite — spliced/synthetic; early history is low-frequency proxy (flat O=H=L=C bars=3709); usable only from daily-era start None (~10576 genuine-daily bars)
- **`TVC_US10Y`** [composite_index] — PROVISIONAL · 8216 bars · 1989-03-17..2026-06-03 (daily-era 1990-01-10, 8062b)
  - flags: TVC composite — spliced/synthetic; early history is low-frequency proxy (flat O=H=L=C bars=4977); usable only from daily-era start 1990-01-10 (~8062 genuine-daily bars)
- **`OANDA_EURUSD`** [fx] — PROVISIONAL · 6254 bars · 2002-05-06..2026-06-03
  - flags: duplicate export ((n)) — dedupe

## Intraday availability (60m/15m) — bars per instrument
- `BATS_MSFT`: 15m=20054
- `CAPITALCOM_COCOA`: 15m=20131, 60m=18977
- `CBOT_DL_ZC1!`: 15m=20639, 60m=18842
- `CFI_WTI`: 15m=21802, 60m=19082
- `COMEX_DL_GC2!`: 15m=20160, 60m=23189
- `COMEX_DL_HG1!`: 15m=21798, 60m=20200
- `COMEX_DL_SI2!`: 15m=21696, 60m=22890
- `FOREXCOM_COFFEE`: 15m=20520, 60m=7416
- `FOREXCOM_COTTON`: 60m=23791
- `FOREXCOM_USDCHF`: 15m=20785, 60m=21258
- `ICEEUR_DLY_BRN1!`: 15m=21195, 60m=22978
- `ICEEUR_DLY_BRN2!`: 15m=21063, 60m=22955
- `NYMEX_DL_PA1!`: 15m=20746, 60m=23064
- `OANDA_EURUSD`: 15m=20786, 60m=21276
- `OANDA_USDJPY`: 15m=20785, 60m=21276
- `TVC_DXY`: 15m=21680, 60m=21109
- `TVC_PLATINUM`: 15m=21662, 60m=25774
- `TVC_SILVER`: 15m=21847
- `TVC_US10Y`: 15m=20892, 60m=24208

## Provenance flags (binding for construction)
- **TVC composites** (SILVER/DXY/PLATINUM/US10Y): spliced; early history is annual/low-freq proxy (flat OHLC). Use ONLY from the detected daily-era start; never treat pre-daily-era bars as observations.
- **TradingView 1!/2! continuous**: verify roll & back-adjustment; build calendars only from aligned 1!&2! with identical roll; difference Open/Close (synchronized), never naive High/Low (§6).
- **WTI–Brent** has a documented ~2010 structural break — any cointegration must be post-2011 or break-aware.
- **Cross-venue legs** (BSE cash vs NSE cash; broker CFD vs ICE): session/holiday/timezone mismatch → inner-join on synchronized timestamps only.
- **Dedupe** the `(n)` files before use (BRN1! 15/60, EURUSD 15/60/1D).
