# Doc 35 — BRN M1–M2 Calendar: Execution Preparation Memo

**Document class:** Pre-execution research memo and implementation specification.
**Date:** 2026-06-04. **Status:** BLOCKING — BRN2! 1D data acquisition required before Stage 1.
**Next action after data acquired:** pre-register, then execute Stage 1.
**Arm A v2 framework:** doc 20/21 (NG positive control) applies with adaptations noted here.

> **Summary finding:** BRN M1-M2 is a genuinely different habitat from NG and has a legitimate
> theoretical case for calendar spread MR — but the restoring-force mechanism is weaker and
> the structural-trend risk (OPEC) is materially higher. Data gap (BRN2! daily missing) is the
> immediate binding constraint. Prior before data: **LOW-MEDIUM (20–30%)** that BRN delivers
> both statistically real AND cost-clearing MR. Execution-ready once BRN2! 1D is acquired.

---

## 1. Data Integrity and Current Status

### 1.1 What exists

| File | Location | Bars | Date range | Usable for daily test? |
|---|---|---|---|---|
| `ICEEUR_DLY_BRN1!, 1D.csv` | `~/Downloads/mean-reversion-data/` | 9,526 | 1989-03-01 → 2026-06-03 | **YES** |
| `ICEEUR_DLY_BRN2!, 60.csv` | `~/Downloads/mean-reversion-data/` | 22,955 | 2022-06-03 → 2026-06-03 | **NO** — 4 years only |
| `ICEEUR_DLY_BRN2!, 15.csv` | `~/Downloads/mean-reversion-data/` | 21,063 | ~2022 → 2026 | **NO** — 4 years only |
| `cl_brn_spread_60.csv` | `data/raw/` | 19,399 | 2023-02-20 → present | WTI-Brent, not BRN M1-M2 |

### 1.2 What is missing and why it matters

**BRN2! at daily frequency is NOT AVAILABLE.** The 60m file only covers 4 years (2022-2026).
Resampling 60m → daily gives 1,032 bars — far below the minimum 2,000+ bars needed for a
reliable VR(q) surrogate-relative test (fewer bars → noisy VR estimates → unreliable p-values).

The BRN M1-M2 calendar spread cannot be constructed for the necessary depth without BRN2! 1D.

### 1.3 Spread preview from available overlap (informational only)

From resampling BRN2! 60m → daily close (last bar per date) over 2022-2026:

```
Calendar spread = BRN1! close − BRN2! close
Period:   2022-06-03 → 2026-06-03 (1,032 bars)
Mean:     +0.921 $/bbl  (BRN1 consistently trades above BRN2 = mild backwardation)
Std:      1.406 $/bbl
Min/Max:  −1.38 / +13.46 $/bbl
```

The +13.46 spike is the COVID/invasion supply shock (likely early 2022). The mean backwardation
(+0.92) is the structural state of Brent during this period. This preview is NOT sufficient for
VR analysis — too short, too recent, biases toward the post-invasion supply shock period.

### 1.4 Required data acquisition

**Step 1 (BLOCKING):** Export `ICEEUR:BRN2!` at 1D frequency from TradingView.

Target: as many years as available at daily frequency (TradingView typically provides Brent
continuous futures back to ~2000). File format: same as BRN1! 1D (TradingView CSV export).
Save to: `data/raw/ICEEUR_DLY_BRN2!, 1D.csv` (matching existing naming convention).

**Step 2:** Copy BRN1! 1D from Downloads to `data/raw/`:
`cp ~/Downloads/mean-reversion-data/ICEEUR_DLY_BRN1\!,\ 1D.csv data/raw/`

**Step 3:** Verify overlap and minimum bar count before pre-registration.

---

## 2. Contract Construction and Calendar Definition

### 2.1 What BRN M1-M2 is

```
BRN M1-M2 spread = F_BRN(T1) − F_BRN(T2)
                 = BRN1! close − BRN2! close
```

Where:
- `BRN1!` = ICE Brent crude front-month continuous futures (nearest expiry)
- `BRN2!` = ICE Brent crude second-month continuous futures
- Both legs are **definitional β=1** (same underlying commodity, adjacent months)
- Construction is identical to NG M1-M2 in method; the economic content differs entirely

### 2.2 ICE Brent roll schedule and expiry mechanics

**Expiry timing:** ICE Brent futures expire approximately the business day before the 15th of
the month preceding the delivery month. Examples:
- April delivery → expires ~13th or 14th of March
- This is EARLIER than CME NG (which expires ~3 business days before month-end)

**Roll schedule for continuous contract (TradingView):** BRN1! rolls to the next contract
at/around expiry. The roll timing for TradingView's continuous contract uses the same
back-adjustment as their other continuous futures.

**Important:** Brent uses **Exchange for Physical (EFP)** settlement, not physical delivery to
a fixed point. This creates a settlement mechanism where the Brent price at expiry is determined
by the EFP market, not by a fixed pipeline delivery price (unlike WTI at Cushing). This makes
Brent less susceptible to local delivery bottlenecks but more susceptible to complex pricing
mechanics near expiry.

**Roll transition handling:** The existing `roll_transition_mask` in analytics_arm_a.py (causal
MAD-based jump filter) handles large price discontinuities at roll seams. This is the same
mechanism used for NG. No special treatment needed for Brent specifically.

### 2.3 Price units and normalization

- BRN futures are priced in **USD per barrel**
- Typical spread level: −$5 to +$15 ($/bbl), depending on market structure
- Cost assumption for the trade proxy test (pre-committed): **$0.03/bbl round-trip**
  (bid-ask ~$0.01-0.02/bbl + exchange fees; institutional cost floor)
- This is the cost assumption to pre-register for Stage 1 (see §5)

For comparison: NG M1-M2 uses cost=0.003 $/MMBtu. These are different units — direct comparison
is not meaningful. Gross/cost ratio is the relevant metric in each instrument's own units.

### 2.4 Construction protocol

Follow the identical protocol as NG (doc 20/21 §4):

1. Load both legs via `load_leg()` (UTC-aware index, ascending sort)
2. Join on UTC date index, inner join (require BOTH legs to have valid close on each bar)
3. Compute spread: `s_close = brn1_close − brn2_close`
4. Apply `spread_from_series()` logic (NaN close dropped, flat bar flagged)
5. Causal deseasonalization via `deseasonalize_causal()` — month-of-year trailing mean
6. VR test via `evaluate_v2()` (frozen Arm A v2 apparatus)

**Construction integrity requirement:** Do NOT use the 60m resampled BRN2! as a leg. The
daily settlement price for a continuous futures contract must come from daily-bar data, not
an intraday OHLCV resampled to daily. Resampled intraday close ≠ official daily settlement
price — the discrepancy can be 0.1-0.3 $/bbl, which is material for a spread with 1-2 $/bbl
typical range.

---

## 3. NG vs BRN: Economic Differences That Matter

This section is the core of the execution prep. Most contamination risks and prior-probability
assessments flow from these structural differences.

### 3.1 Storage mechanism (the restoring-force comparison)

**NG (Henry Hub):**
- Storage asset: **underground caverns** (depleted reservoirs, salt caverns, aquifers)
- Capacity: FIXED at any point in time — cannot be expanded quickly
- Seasonal pattern: strong injection season (April–October), withdrawal season (November–March)
- When full: cash-and-carry arbitrage is BLOCKED. Producers must sell at spot regardless of
  the calendar spread. The restoring force physically disappears.
- When at normal levels: arbitrage fires reliably. Multiple operators execute it continuously.

**BRN (ICE North Sea):**
- Storage assets: **above-ground tanks** + **floating storage** (tankers used as storage)
- Capacity: ELASTIC — you can always rent more tankers at a price; above-ground tanks can
  be expanded (slowly) or floating storage added (quickly)
- Seasonal pattern: WEAKER than NG. Crude demand is more continuous; no sharp seasonal peak
- In "glut" conditions: floating storage prevents the complete collapse of the restoring
  force. Even in extreme contango, there is ALWAYS a physical restoring mechanism available
  (if the contango exceeds storage + financing costs). The mechanism never fully turns off.

**Key implication:** The BRN restoring force is MORE RELIABLE than NG's (doesn't switch off)
but produces SMALLER DEVIATIONS before firing (the arb is always available, so prices can't
deviate as far). This is the fundamental trade-off: NG has occasional large, exploitable
dislocations (when storage is tight); BRN has smaller but more consistent MR.

**For the VR test:** BRN's more continuous restoring force may produce a stronger global VR
signal but smaller gross per trade. For the economic test: smaller deviations → harder to
clear a cost floor that BRN's lower bid-ask only partially compensates.

### 3.2 OPEC production policy (the structural trend risk — unique to BRN)

**This has NO analogue in NG and is the single most important asymmetry.**

OPEC+ production decisions create DIRECTIONAL, PERSISTENT structural moves in Brent calendar
spreads:

- **Production cuts (e.g., 2016, 2022-2023):** Front-month rises faster than deferred →
  spread widens into backwardation. This is a TREND, not a deviation. The spread can stay
  in extreme backwardation for months as the production cut plays out.
- **Production increases (e.g., 2020 COVID crash, 2014-2016 price war):** Front-month falls
  faster than deferred → spread collapses into deep contango. Again a TREND.

A z-score system fading these moves would be systematically WRONG during OPEC policy regimes:
it would sell backwardation expecting reversion, but backwardation could continue widening for
weeks or months. The "deviation" it fades is not a deviation from equilibrium — it IS the new
equilibrium under the policy regime.

**Quantitative risk:** OPEC holds scheduled meetings approximately every 2 months. Major
production decisions typically move Brent front-month calendars by $1-4/bbl within days.
On a spread with typical std ≈ $1-2/bbl, this is a 1-3σ move that looks like a high-confidence
fade signal but is actually a regime change.

**The OPEC effect on VR:** If OPEC-driven structural moves dominate, BRN M1-M2 could show
VR > 1 (trending) in OPEC-dominated periods — overwhelming the underlying cash-and-carry MR
in the aggregate. This is the primary mechanism by which BRN could fail the VR test despite
having a genuine restoring force.

**No analogous risk in NG:** NG storage injections/withdrawals are demand-driven, not policy-
driven. There is no single entity that can impose a structural directional regime on NG
calendars for months at a time.

### 3.3 Convenience yield structure

**NG:** convenience yield is HIGH and VOLATILE — it spikes sharply when storage is tight
(cold snaps, heat waves) and collapses when storage is full. This creates LARGE deviations in
the calendar spread that are genuinely mean-reverting once the supply/demand shock passes.

**BRN:** convenience yield reflects OPEC supply uncertainty + refinery throughput demand.
It is LOWER on average (crude is typically in mild contango = negative convenience yield)
and LESS VOLATILE in normal conditions. Large swings occur around OPEC decisions and
geopolitical events (supply shocks from Middle East, Russia, etc.) but these are often
TREND-REINFORCING rather than mean-reverting in the short term.

### 3.4 Seasonality

**NG:** Strong, economically anchored seasonal demand pattern:
- Winter: high heating demand → spot premium → backwardation tendency
- Summer: injection season → reduced spot demand → contango tendency
- The seasonal pattern creates a natural mean-reversion anchor around the expected season

**BRN:** Weak, diffuse seasonality:
- Driving season (summer, Northern Hemisphere): marginally higher gasoline demand
- Heating oil (winter): some crude demand for distillates
- Global 24/7 consumption with diversified end-uses → no sharp seasonal anchor
- The deseasonalization step for BRN will remove less variance than for NG and may remove
  some genuine structure; use with caution (treat the seasonal adjustment as an ablation
  check, not a required pre-processing step)

### 3.5 Geopolitical sensitivity

**NG:** Primarily domestic US market (Henry Hub). Geopolitical events (Russia-Ukraine,
Middle East) have second-order effects through LNG pricing. Generally LOWER geopolitical
sensitivity for the spread itself.

**BRN:** Global benchmark for seaborne crude. DIRECTLY affected by:
- OPEC/OPEC+ production decisions (most important)
- Middle East supply disruptions (Strait of Hormuz, Yemen, Libya)
- Russian production (post-2022 sanctions)
- North Sea field maintenance and outages (direct supply to the physical delivery process)

These create large, sudden price moves that generate high z-scores but are NOT mean-reverting
(they represent genuine supply shocks). A z-score system will generate false signals around
geopolitical events.

### 3.6 Roll structure comparison

| Feature | NG (CME NYMEX) | BRN (ICE) |
|---|---|---|
| Exchange | CME, New York | ICE, London |
| Settlement | Physical delivery at Henry Hub | EFP (Exchange for Physical) at ICE |
| Expiry | ~3-4 business days before month-end | ~Business day before 15th of preceding month |
| Roll period | Short (~1 week of elevated volume) | Longer (~2 weeks before expiry) |
| Back-adj artifact risk | Moderate (monthly roll jump) | Similar (monthly roll jump) |
| Liquidity at roll | Very high | Extremely high (among most liquid futures) |

BRN rolls EARLIER than NG relative to the delivery month. This means the BRN M1-M2 spread
can exhibit complex behavior in the 2-3 weeks before the front-month expiry (basis trades,
EFP transactions, positioning adjustments). The roll_transition_mask handles the seam itself,
but pre-roll dynamics may add noise to the 20-40 bar lookback window.

### 3.7 Market efficiency comparison

**NG M1-M2:** Moderately efficient. Significant participation from producers hedging forward
production, consumers locking in winter gas prices, storage operators running cash-and-carry.
The calendar spread is actively traded but not dominated by fast algorithmic participants.

**BRN M1-M2:** MORE EFFICIENT than NG. The world's most liquid crude oil futures. Hundreds of
institutional participants monitor and trade calendar spreads. Any systematic deviation is
quickly arb'd. This means:
- MR reverts FASTER → shorter half-lives → needs tighter lookback windows
- Per-trade alpha is SMALLER → harder to clear a cost floor
- The VR test may show weaker MR signal (more efficient = closer to martingale)

---

## 4. Prior Probability (Honest Assessment Before Seeing Data)

### 4.1 Prior decomposition

**P(VR < 1 globally, p_rw < 0.05):**
Probability that BRN M1-M2 shows statistically significant mean reversion vs the RW surrogate
at q=20, N=500.

```
Supporting: floating storage provides genuine restoring force; crude calendar MR is cited in
  the storage literature (Pindyck 1994; Routledge et al. 2000); Brent liquidity ensures prices
  converge quickly to arbitrage bounds when they breach them.
Against: OPEC structural trending may dominate; market efficiency means deviations are small
  and quickly corrected (VR may be statistically near 1 even if <1); the half-life may be so
  short that 1D bars don't capture it.

PRIOR (statistical real): ~40–50%
```

**P(gross > cost, deployable after costs):**
Probability that the spread earns more per trade than the assumed $0.03/bbl round-trip cost.

```
Supporting: BRN bid-ask is tight ($0.01-0.02/bbl); if MR exists, the tight cost floor
  makes it easier to clear.
Against: the tight bid-ask exists BECAUSE the market is efficient; smaller deviations
  → smaller gross per trade; the OPEC-driven trending events produce large losses that
  dominate the net expectancy even if most trades are profitable.

PRIOR (economically deployable): ~20–35%
```

**Combined prior (both statistically real AND economically deployable):**

```
PRIOR: LOW-MEDIUM = 15–25%
```

**Calibration reference:**
- NG prior before testing: MEDIUM (~40%) → confirmed statistically (VR p=0.005) but UNECONOMIC
- NG EIA conditioning prior: MEDIUM (~40%) → KILLED (p_rw=0.502)
- BRN prior: **LOWER than NG** because of OPEC risk + market efficiency

This is an honest prior that the project's confirmed skepticism demands. BRN is not
obviously a better habitat than NG.

### 4.2 What would move the prior substantially

**UPWARD:**
- Historical data shows BRN M1-M2 was in backwardation >60% of the time (implies supply-scarcity
  premium that mean-reverts)
- VR(20) < 0.80 across multiple sub-periods (strong MR, not concentrated in one period)
- The spread shows the same regime-conditionality as NG (switches off predictably in
  OPEC-glut periods → suggests genuine storage MR, not artifact)

**DOWNWARD:**
- VR(20) ≥ 1.0 or VR(20) < 1.0 but not significantly vs OU (indicating efficiency)
- Large concentration of MR signal in 2020-2022 (COVID + Ukraine war anomalous period)
- Cost-clearing only achieved in high-z regime (single-event concentration)
- Robustness grid shows the effect is localized to one sub-period

### 4.3 Adverse scenario — what "dead calendar" looks like for BRN

"Dead" means: VR(20) approximately 1.0 globally; no statistically significant MR; the BRN
M1-M2 spread is well-described by a GARCH martingale reflecting OPEC volatility clustering.
This would confirm that BRN's market efficiency overwhelms any storage MR signal at the daily
frequency.

---

## 5. Stage 1 Design (Trader-First, N=200)

### 5.1 Pre-registration requirements

**Before any data is loaded, freeze ALL of these:**

```
INSTRUMENT:       BRN M1-M2 = BRN1! close − BRN2! close (β=1 definitional)
CONSTRUCTION:     Both legs from daily data only (no intraday resampling)
DATE_MIN:         First date where BOTH legs have valid closes and bar count ≥ 750 from start
                  (to be confirmed after data acquisition; commit before running)
DATE_MAX:         2026-06-03 (or latest available)
DESEASONALIZE:    Causal trailing month-of-year mean (consistent with NG; ablation check optional)
PRIMARY STATISTIC: VR(20) — same as NG positive control (doc 21)
Q GRID:           {5, 10, 20, 40, 60} — same as NG
SURROGATES:       RW, GARCH(1,1), OU(half-life to be measured from data), MA(1)
N_STAGE1:         200
SIGNIFICANCE:     p_rw < 0.10 at q=20, N=200 (speed gate — same as doc 20 Stage 1 threshold)
SEED:             20260604 (same as all tests)
OOS_SPLIT:        70% train / 30% OOS by date
COST:             $0.03/bbl round-trip (pre-committed primary; grid: {0.01, 0.03, 0.05})
```

**Primary statistic rationale:** VR(20) is the pre-committed primary (same as NG). The choice
of q=20 corresponds to approximately 1 calendar month of trading days — a sensible window for
crude oil calendar spread dynamics where monthly supply/demand cycles create the primary
restoring force.

**Cost assumption rationale (pre-committed to $0.03/bbl):**
- ICE Brent M1-M2 spread bid-ask: typically $0.01-0.02/bbl
- Exchange fees + clearing: approximately $0.005-0.01/bbl per round-trip
- Total round-trip cost for an institutional trader: $0.02-0.05/bbl
- Pre-committing $0.03/bbl as the primary is the midpoint of the realistic institutional range

### 5.2 Fast-kill criteria (Stage 1)

Trigger any one → **KILL immediately:**

| Criterion | Kill threshold | Reasoning |
|---|---|---|
| VR(20) p_rw at N=200 | > 0.15 | Speed gate: clearly not significant at N=500; stop |
| VR(20) real | ≥ 1.0 (trending, not mean-reverting) | No MR signal at all |
| OU reference: real beats OU | p_ou < 0.05 (OU beats real) | Market more efficient than expected half-life |
| OOS VR(20) sign flip | VR(20)_OOS > VR(20)_train by > 0.15 | MR is training-period artifact |
| Concentration in post-2020 | VR(20) < 0.90 only in 2020-2026 sub-period | COVID/Ukraine anomaly, not structural |

**Go criteria (Stage 1 → Stage 2):**

| Criterion | Go threshold |
|---|---|
| VR(20) p_rw at N=200 | ≤ 0.10 |
| VR(20) real | < 0.90 (clear sub-diffusion, not borderline) |
| VR profile shape | Monotonically declining from q=5 to q=60 (pattern consistent with genuine MR) |
| Full-period vs OOS consistency | VR(20)_OOS within 0.15 of VR(20)_full |

### 5.3 Additional BRN-specific diagnostic (pre-registered)

**OPEC-period conditioning check (diagnostic only, non-binding for Stage 1 verdict):**

After computing the unconditional VR test, split the sample into:
- OPEC-action periods: weeks surrounding major OPEC+ production decisions
  (at least ±4 weeks around known decisions; use publicly available OPEC meeting calendar)
- Non-OPEC periods: remaining bars

Report VR(20) for each sub-period descriptively. If VR(20) > 1.0 in OPEC periods but < 1.0
in non-OPEC periods, document as a structural diagnostic. This does NOT constitute pre-registry
for a conditional OPEC-filtered strategy (which would require a new pre-registration).

Purpose: distinguish "global MR is weak because OPEC trending overwhelms genuine storage MR"
from "global MR exists and is similar in OPEC and non-OPEC periods."

### 5.4 Half-life expectation for OU calibration

For NG: documented half-life = 12.9 bars (doc 21); AR(1) φ = 0.947.
For BRN: expected half-life is SHORTER than NG because:
- Floating storage fires the restoring force faster (less capacity constraint friction)
- Market efficiency is higher
- Expected half-life: 5-10 bars (1-2 weeks trading days)

This is a PRE-COMMITTED PRIOR expectation. Actual half-life is measured from the data before
freezing φ. If the measured half-life is > 25 bars, that signals weak MR (barely statistically
distinguishable from RW) and the prior drops further.

### 5.5 What the VR profile should look like for a genuine BRN MR habitat

**Expected VR profile (if genuine):**
```
q:   5    10    20    40    60
VR:  0.85  0.82  0.78  0.82  0.88  (monotonically declining then recovering)
```

The recovery at high q reflects return to martingale behavior as the MR reverts within the
lookback window. The minimum near q=15-30 is the characteristic "MR bowl."

**Red flag — efficiency-driven VR profile:**
```
q:   5    10    20    40    60
VR:  0.97  0.98  1.00  1.01  1.01  (flat near 1, no bowl, possibly trending at high q)
```
This indicates efficient market: deviations exist but are corrected within 1-2 bars — not
visible at daily resolution.

**Red flag — OPEC trending VR profile:**
```
q:   5    10    20    40    60
VR:  0.99  1.01  1.05  1.08  1.10  (VR > 1 at all lags, increasing — momentum not MR)
```
This indicates structural trending dominates.

---

## 6. Hidden Contamination Vectors (BRN-Specific)

### C1 — Floating storage vs underground: artifact risk

**Risk:** Floating storage is financially, not physically, settled. Large contango periods
attract floating storage, which creates mechanical mean-reversion as the contango contracts
once the storage trade unwinds. This LOOKS like MR but is actually a leveraged carry trade
unwinding. The VR test cannot distinguish this from genuine storage MR.

**Implication:** If BRN VR < 1, we cannot cleanly attribute it to "fundamental storage MR"
vs "floating-storage carry unwinding." This weakens the interpretability of a positive result.
Document as a residual confound.

**Guardrail:** Surrogate-relative test (vs RW and OU) is the defense. If the MR is stronger
than what a matched OU process produces, it is at least statistically genuine. The mechanism
question remains open even if the statistical test passes.

### C2 — OPEC-event selection-on-deviation

**Risk:** OPEC decisions create large spread moves that generate high z-scores. A fade strategy
enters after these moves. If OPEC decisions are followed by a short-term reversal (e.g., an
announcement is initially over-priced by the market and partially gives back), the z-score
fade would appear profitable. But this is NOT storage MR — it is fade-the-news event trading
with a high Sharpe for a small number of trades.

**Guardrail:** Episode-jackknife (drop the 3 largest gross trades) in Stage 2. If the VR and
gross expectancy are driven by a small number of OPEC-reversal trades, the jackknife will show
catastrophic collapse. This is the same mechanism that killed the doc 31 θ=2.5 result.

### C3 — EFP settlement mechanism at expiry

**Risk:** Near expiry, BRN prices reflect the EFP market (the physical-financial settlement
mechanism), which can diverge from the pure futures-calendar spread by $0.10-0.50/bbl in the
final days before expiry. The roll_transition_mask handles the roll seam itself but may not
capture the 3-5 day pre-expiry EFP distortion window.

**Guardrail:** Same as NG: the roll_transition_mask (MAD-based causal jump filter) flags large
pre-roll price jumps. Ablation check on masked vs unmasked VR (as in doc 20) validates that
the headline result is robust to the EFP window.

### C4 — North Sea field outages

**Risk:** Maintenance of North Sea fields (Forties, Oseberg, Ekofisk, Buzzard) causes
temporary spikes in Brent backwardation. These typically last 2-4 weeks and DO mean-revert
as the maintenance ends and production resumes. This is a genuine physical MR signal.

**Important:** This is actually FAVORABLE for the hypothesis (genuine supply-shock MR).
The risk is that if the VR test picks this up, it may not be generalizable — North Sea
outages are a UK North Sea-specific phenomenon, and the effect may not replicate on other
crude calendars. Document the mechanism if the VR confirms.

### C5 — WTI-Brent differential contamination

**Risk:** The WTI-Brent differential has undergone structural regime changes (2010-2015 US
shale boom, 2019 onward). This affects LEVELS of Brent pricing but should NOT affect the
M1-M2 SPREAD (which differences out the common level). Verify that the spread is stationary
in mean (not trending) before running VR — if the spread trends, deseasonalization is
insufficient and the spread is not a proper calendar object.

**Guardrail:** Run an ADF test on the spread level in the pre-registration step. If non-
stationary (trend), the spread is not admissible as a β=1 calendar without further
investigation.

### C6 — Data alignment: settlement vs last-trade prices

**Risk:** BRN1! and BRN2! from TradingView use the ICE daily settlement price, not the
last-trade price. The settlement prices for adjacent months are computed simultaneously by
ICE at the end of the trading session. This means BRN1! and BRN2! daily settlements are
sampled at exactly the same time → no bid-ask timing contamination in the spread.

**This is actually favorable:** unlike some pairs where legs trade at different hours, the
Brent M1-M2 spread construction from ICE settlement prices is clean in terms of timestamp
alignment.

---

## 7. Spread Construction Audit Protocol

Before pre-registering Stage 1, run these checks on the combined BRN1!/BRN2! spread:

```
AUDIT-1:  Bar count
          Both legs must have ≥ 2,000 overlapping daily bars
          Fail: insufficient for reliable VR(q) at q=60

AUDIT-2:  Date alignment
          After inner join, gaps should be ≤ 5 consecutive bars
          Fail: systematic gaps indicate leg mismatch (different roll conventions)

AUDIT-3:  Spread level stationarity
          ADF test on the raw spread: p-value < 0.05 (stationary in level)
          Fail: spread is trending → not a valid β=1 calendar spread; investigate

AUDIT-4:  Spread value sanity
          Spread should fluctuate around a stable seasonal mean (±$5 typical range)
          Red flag: sustained moves > $10 lasting > 3 months → OPEC structural regime

AUDIT-5:  Roll seam detection
          Apply roll_transition_mask to spread increments; identify seam dates
          Compare to known ICE Brent expiry calendar
          Fail: mask identifies >15% of bars as roll artifacts (data quality issue)

AUDIT-6:  Daylight saving / timezone consistency
          Both legs must have UTC-aware identical timestamps on every overlapping bar
          Fail: any timestamp mismatch → construction artifact in spread

AUDIT-7:  Price magnitude comparison
          BRN1! close and BRN2! close should trade within 5% of each other in normal periods
          Fail: spreads regularly > $20 → possible data sourcing issue (different benchmarks)
```

---

## 8. BRN vs NG: Decision Criteria for "Genuinely Better Habitat"

Before executing, define what "BRN is a genuinely better habitat" means. Three possible outcomes:

**OUTCOME A — BRN is better:** 
- VR(20) < 0.85 (BRN) vs 0.448 (NG at q=20 — note: VR(20)_NG was very strong)
- Actually, NG VR(20) = 0.448 is EXTREMELY strong for a real instrument
- BRN would need VR(20) < 0.70 to be "comparable" considering market efficiency
- AND gross > $0.03/bbl (cost floor)
- This is the ONLY outcome that opens the portfolio framing for a multi-instrument book

**OUTCOME B — BRN is real but uneconomic (same as NG):**
- VR(20) < 0.90, p_rw < 0.05 (statistically real MR)
- But gross < $0.03/bbl (sub-cost)
- This adds a second PERSISTENT-BUT-UNECONOMIC instrument; does NOT unlock portfolio framing
  per the expectancy arithmetic (doc 25: diversification of sub-cost sleeves = still sub-cost)
- Strategic value: confirms the storage MR hypothesis is real across instruments, narrows the
  search for when and where it is economically exploitable

**OUTCOME C — BRN is a dead calendar:**
- VR(20) ≥ 0.95 or p_rw > 0.15 at N=200
- No evidence of MR; OPEC trending or market efficiency overwhelms the storage signal
- Kill immediately; pivot to ZC (corn calendar) as the next cohort candidate

---

## 9. Immediate Next Steps (Before Stage 1)

Ordered by dependency:

```
Step 1 (BLOCKING):  Acquire BRN2! 1D from TradingView
                    Export ICEEUR:BRN2! at 1D frequency
                    Copy to data/raw/ with consistent naming

Step 2:             Copy BRN1! 1D to data/raw/ from Downloads

Step 3:             Run AUDIT-1 through AUDIT-7 (§7 above)
                    Confirm minimum bar count, alignment, stationarity

Step 4:             Pre-register all Stage 1 parameters (this doc §5.1 as template)
                    Freeze date_min based on actual data overlap

Step 5:             Execute Stage 1 (N=200, VR test, fast-kill criteria)

Step 6:             If Stage 1 passes: assess readiness for Stage 2 and cost-floor test
                    If Stage 1 kills: pivot to ZC calendar or crack spread controlled-β
```

---

*Summary: BRN is a theoretically legitimate MR candidate (storage theory applies; floating
storage provides genuine restoring force; historical crude calendar trading confirms the
mechanism). But the OPEC structural-trend risk and higher market efficiency give it a
genuinely lower prior than NG had before NG's own testing (LOW-MEDIUM, 15-25%). The test is
cheap and the data gap is the only immediate blocker. Worth running after BRN2! 1D is acquired;
the result will either unlock portfolio breadth (OUTCOME A) or cleanly close this direction
(OUTCOME C) within 2 weeks of data acquisition.*
