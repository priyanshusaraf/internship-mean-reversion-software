# ZC (Corn) M1–M2 Daily Calendar — FROZEN Pre-Registration

**Document class:** Permanent AMR pre-registration (institutional memory — frozen before any result).
**Date:** 2026-06-05. **Mode:** Trader-discovery (§11.2). **Status:** FROZEN — no redesign after this line.
**Supersedes:** nothing. **Extends:** brn_calendar_prereg.md (identical apparatus, new habitat).
**Inherits binding:** doc 33 (ZC old-crop/new-crop confirmatory cell), doc 23 (NG rolling frame), doc 25
(cost-aware ledger), CLAUDE.md §11 (rolling safeguards, crisis isolation, full-search reporting).

> **Objective (the only one):** determine whether the β=1 ZC1!−ZC2! daily corn calendar is a
> **cost-clearing, deployable sleeve** with structural diversification from energy — or merely-true
> (statistically real, sub-cost) — or dead (no MR signal). One verdict, no argmax, no post-hoc tuning.

> **Structural diversification claim (pre-committed prior):** ZC is agricultural (CBOT corn futures),
> NOT energy. Mechanistic driver: grain storage + seasonality of harvest/usage, NOT OPEC policy.
> If ZC and NG/BRN both confirm cost-clearing MR, they are genuinely independent sleeves (different
> supply shocks, different storage mechanism) — this is the minimum condition for portfolio breadth.
> This claim is a PRIOR, not a conclusion; it depends on ZC confirming on its own merits.

> **Zombie clearance (§4):** ZC is pre-registered in doc 33 §1 as a confirmatory instrument (old-crop
> cell). This pre-registration operationalizes that cell with the full Tier-1/Tier-2 gate apparatus,
> consistent with the BRN prereg framework. No new hypothesis — an already-listed confirmatory cell
> executed under the frozen programme.

---

## 0. Data Coverage — Pre-Registration Scoping Audit

> *Scoping only — no statistical result.*

| Leg | Bars | First bar | Last bar | Source |
|---|---|---|---|---|
| `CBOT_DL_ZC1!, 1D.csv` | 8,796 | 1991-05-28 | 2026-06-04 | `data/raw/more-mean-reversion-data/` |
| `CBOT_DL_ZC2!, 1D.csv` | 8,805 | 1991-01-31 | 2026-06-04 | `data/raw/more-mean-reversion-data/` |

**Overlap start:** 1991-05-28 (ZC1! determines the binding start).
**Usable bars (estimated, inner join):** ~8,790 bars — ~35 years of daily data, well above minimum.

**Pre-registration date range (FROZEN):**
```
DATE_MIN = 1991-05-28
DATE_MAX = 2026-06-04
```

No data examined for price levels, spread distribution, or VR at any point prior to this freeze.
Scoping was limited to row count and timestamp range only.

---

## 1. Hypothesis (FROZEN — one line)

> The β=1 definitional ZC1!−ZC2! daily corn calendar spread is a **cost-clearing, tradeable MR sleeve**
> at the institutional cost floor (K = 0.005) with a half-life in the tradeable band [5, 60] bars —
> **or it is merely-true / a non-finding.**

**Merely-true definition (FROZEN):** VR confirms sub-diffusion at p_rw ≤ 0.05 (N=500), but pooled
gross expectancy (ex-crisis, rolling-local) does not clear K = 0.005. Statistically real MR that is
sub-cost is a non-finding for portfolio purposes per doc 25 ledger.

**Dead calendar definition (FROZEN):** p_rw > 0.20 at N=200 (speed-gate kill) or VR(20) ≥ 1.0 globally.

---

## 2. Construction (FROZEN)

```
SPREAD:        S_t = close(ZC1!)_t − close(ZC2!)_t           [β=1, definitional; same commodity, adjacent months]
LEG SOURCE:    daily settlement bars only (Unix-timestamp TradingView format; no intraday resampling)
JOIN:          UTC date index, inner join (both legs present required)
DESEASONALIZE: causal trailing month-of-year mean (identical to NG and BRN; causal at all t)
ROLL MASK:     ADR_003 increment_jump_mask, frozen k = 8.0 (via spread_from_series jump_k=8.0)
VR TYPE:       level-difference VR (frozen Arm A v2 apparatus)
PRIMITIVES:    analytics_arm_a.py / analytics_arm_a_v2.py — reused AS-IS; do NOT modify
LEG LOADER:    Unix-timestamp loader (same as BRN execution script); do not use date-format load_leg
```

**Corn-specific construction note:** ZC prices are in USD per bushel (cents/bushel in some formats).
The spread = ZC1! - ZC2! is in the same units as the legs. Confirm units are consistent on construction.
Typical spread range: −0.30 to +0.30 $/bushel for non-crisis periods.

**Construction integrity (FROZEN):**
- β=1 definitional; no hedge-ratio estimation; zero β-update-noise contribution.
- Do not apply HP-filtering, Kalman smoothing, or detrending to the spread before VR.
- Do not modify roll-masking k without a new pre-registration.

---

## 3. Gate Architecture (FROZEN — Tier-1 and Tier-2 run in the same pass)

### Gate Tier-2 (QUANT) — surrogate-relative VR(q)

**Primary surrogate (HEADLINE):** RW (random walk, iid Gaussian residuals).
**Secondary surrogates (HEADLINE):** GARCH(1,1); MA(1)-noise.
**Reference (non-gating):** OU process calibrated from data half-life.

**Q grid (FROZEN):** {5, 10, 20, 40, 60}. **Primary statistic:** VR(20) (~1 calendar month).

**Speed gate — N=200:**
- Kill immediately if p_rw(VR(20)) > 0.20 at N=200 OR VR(20) ≥ 1.0.

**Full test — N=500 (only if speed gate passes):**
- Significance threshold: p_rw(VR(20)) ≤ 0.05 for QUANT gate PASS.
- p_rw ∈ (0.05, 0.20]: QUANT gate BORDERLINE — report with caution flag.

**SEED (FROZEN):** 20260604.

**OOS split (FROZEN):** First 70% of overlapping bars (by date) = training; final 30% = OOS.
Flag if VR(20)_OOS > VR(20)_train + 0.15 (sign flip / regime nonstationarity indicator).

### Gate Tier-1 (TRADER) — causal z-entry book simulation, pooled rolling-local

**Frame:** doc-23 rolling-local pooled mean-z book sim (same mechanics as BRN prereg).

**Cost grid (FROZEN):** {0.003, 0.005, 0.008}. **Primary cost threshold:** K = 0.005.

**Netting grid (FROZEN):** {η_upper = min(M,3), η_realistic = 1.5, η_conservative = 1.0}.

**Half-life tradeable band (FROZEN):** 5–60 bars (1 week to 3 months of trading days).

**Pooled rolling-local frame (FROZEN):**
- Yearly windows: full date range (earliest full year with ≥ 100 bars through 2025).
- Per-window: compute VR(20) z-score relative to in-window RW band (N=200).
- Pooled statistic: mean-z across non-crisis windows (primary verdict).
- Crisis years excluded from primary verdict; reported separately.

**TRADER gate PASS criteria (FROZEN):**
1. Pooled gross expectancy (ex-crisis) ≥ 0.005.
2. Half-life inside tradeable band [5, 60] bars.
3. Episode jackknife (drop 3 largest gross trades) retains ≥ 50% of gross expectancy.

**TRADER gate FAIL → MERELY-TRUE (if QUANT passes):**
- Gross confirmed but < 0.005, OR half-life outside [5, 60], OR jackknife collapse.

---

## 4. Seasonal Conditioning — ZC Pre-Registered Directional Split (doc 33, §1)

**FROZEN (doc 33):** ZC has exactly one binary directional split:
```
OLD-CROP:  March – August  (confirmatory cell — pre-registered directional hypothesis)
NEW-CROP:  September – February  (descriptive only — non-confirmatory)
```

**Pre-registered directional hypothesis (OLD-CROP):** old-crop carry is THICKER; storage tightens
into harvest. The spread MR signal, if it exists, should be stronger in the old-crop window.

**Binding rules (FROZEN):**
- The verdict reads ONLY the unconditional cell for the QUANT/TRADER gate (whole-sample).
- The old-crop seasonal conditioning is an ABLATION CHECK (secondary): run it, report it,
  but it does NOT change the primary verdict. If unconditional is MERELY_TRUE, conditional
  old-crop cannot rescue it to SLEEVE_CANDIDATE (that would require a new pre-registration).
- Old-crop cell is PRE-REGISTERED as a directional check per doc 33 — but for DEPLOYMENT VERDICT
  purposes, the UNCONDITIONAL cell governs (consistent with the BRN prereg design).
- New-crop numbers are DESCRIPTIVE, NEVER headlined.

---

## 5. Black-Swan Isolation (FROZEN)

Three designated crisis years for ZC (agricultural market disruptions):
- **2020 (COVID-19):** supply chain disruption, ethanol demand collapse, major corn basis dislocation.
- **2022 (Ukraine war / food security shock):** Ukraine is a major corn exporter; the war created
  extreme dislocations in grain calendar spreads globally.
- **2012 (US drought):** severe US drought drove corn spreads to historically extreme levels
  (not in the BRN crisis list — this is ZC-specific and pre-registered here).

**Binding rule:**
- Run full sample including all crisis years → report as "full sample."
- Run excluding 2020, 2022, and 2012 → report as "ex-crisis."
- **Verdict rests on the EX-CRISIS pooled read.** Full sample is context.
- No other years may be selectively excluded post-hoc.

---

## 6. Harvest-Period Diagnostic (PRE-REGISTERED, descriptive only — non-binding)

After computing the unconditional VR and book sim:
- Split the sample into harvest-transition months (August–October, when new-crop pricing begins to
  dominate) and the remainder.
- Report VR(20) and pooled gross for each sub-period descriptively.
- This is NOT a pre-registered conditional strategy. Purpose: understand mechanism.

---

## 7. Verdict Decision Tree (FROZEN — identical structure to BRN prereg)

```
Speed gate (N=200):
  p_rw(VR20) > 0.20 OR VR(20) >= 1.0  →  DEAD_CALENDAR — kill, record, note for programme.

N=500 full test:
  VR(20) < 1.0 AND p_rw <= 0.05:
    QUANT gate PASS → run TRADER gate:
      Half-life outside [5, 60]     →  MERELY_TRUE (not deployable horizon)
      Pooled gross < 0.005 (ex-crisis)  →  MERELY_TRUE (sub-cost)
      Jackknife collapse > 50%      →  CONCENTRATION → MERELY_TRUE
      All three pass                →  SLEEVE_CANDIDATE — advance to portfolio test
  VR(20) < 1.0 AND p_rw in (0.05, 0.20]:  BORDERLINE → MERELY_TRUE regardless of TRADER gate

VERDICT: exactly one of {DEAD_CALENDAR, MERELY_TRUE, SLEEVE_CANDIDATE}
```

---

## 8. Anti-Lookahead Firewall (FROZEN)

Prohibited after this line:
1. Changing DATE_MIN, DATE_MAX, q grid, cost grid, k, seed, half-life band, or crisis-year list.
2. Adding/removing surrogate types after seeing VR values.
3. Selecting a different q as "primary" based on which gives the best p-value.
4. Excluding years not on the pre-registered crisis list {2020, 2022, 2012}.
5. Modifying analytics_arm_a / analytics_arm_a_v2 primitives.
6. Reporting only the ex-crisis number if full-sample is inconvenient.
7. Using the old-crop seasonal result to rescue an unconditional MERELY_TRUE to SLEEVE_CANDIDATE.

Violation of any → result is INADMISSIBLE under §6.1 temporal integrity invariant.

---

## 9. Reporting Requirements (FROZEN)

```
§9.1  Full VR(q) profile: q ∈ {5,10,20,40,60} — real vs RW/GARCH/MA(1)/OU surrogates
§9.2  p_rw(VR20) at N=200 and N=500 — both reported
§9.3  OOS VR(20) vs training VR(20); sign flip flag
§9.4  Measured global half-life (AR1 fit on deseasonalized spread)
§9.5  Book sim: pooled gross, full-sample AND ex-crisis (2020/2022/2012), cost grid {0.003,0.005,0.008}
§9.6  Netting grid: upper / realistic / conservative
§9.7  Episode jackknife: pooled gross with 3 largest trades removed
§9.8  Crisis-year sensitivity: 2020, 2022, 2012 windows reported individually
§9.9  Seasonal split: old-crop vs new-crop VR(20) and gross (descriptive, non-binding)
§9.10 Harvest-period diagnostic (descriptive)
§9.11 Verdict: exactly one of {DEAD_CALENDAR, MERELY_TRUE, SLEEVE_CANDIDATE}
§9.12 Strategic implication: what the verdict means for the calendar programme and cohort breadth
```

---

## 10. Strategic Context (Pre-Committed — Not a Result)

**Prior (pre-committed, before any data read):** MEDIUM 30–45% probability of SLEEVE_CANDIDATE.
Calibrated from: (a) NG PERSISTENT-BUT-UNECONOMIC — storage MR hypothesis real but uneconomic;
(b) BRN MERELY_TRUE (2026-06-05) — confirms storage MR real but uneconomic (half-life too long);
(c) ZC has STRONGER seasonal anchor than BRN and NO OPEC-equivalent policy risk; (d) corn storage
mechanism closer to NG (fixed elevator capacity) than BRN (elastic floating storage); (e) typical
corn spread std ~$0.10-0.30/bushel, lower absolute magnitude → cost threshold may be relatively
harder to clear; (f) doc 33 identified ZC as Tier-1 instrument.

**Higher prior than BRN because:** (a) no OPEC-equivalent; (b) stronger harvest-season anchor;
(c) fixed storage capacity creates true "storage-full" regime analogous to NG injection-season.

**Strategic significance:**
- `SLEEVE_CANDIDATE` → cohort breadth achieved with a non-energy instrument; portfolio framing
  (doc 25) becomes tractable; advance to book aggregation test.
- `MERELY_TRUE` → confirms storage MR as real-but-uneconomic across grain calendars; closes the
  daily-calendar direction entirely; focus shifts to crack-spread controlled-β (the keystone).
- `DEAD_CALENDAR` → ZC closed; calendar thesis further weakened; crack-β becomes the programme.

---

*Pre-registration frozen: 2026-06-05. No results exist at time of freeze. Execute only via
frozen analytics_arm_a / analytics_arm_a_v2 primitives without modification. Use the Unix-
timestamp leg loader (same as BRN execution script). Do not run until this prereg is reviewed.*
