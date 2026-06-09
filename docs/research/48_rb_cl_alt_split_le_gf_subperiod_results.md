# Doc 48 — RB-CL Alternative Split + LE-GF Ex-COVID OOS: Results

**Pre-registration:** `rb_cl_alt_split_le_gf_subperiod_prereg.md` (Revision 2, 2026-06-10)  
**Executed:** 2026-06-10  
**Runner:** `scripts/run_48_rb_cl_alt_split_le_gf.py`  
**JSON:** `data/processed/48_results.json`  
**Seeds:** SEED_A=20260610, SEED_B=20260610  
**Status:** FINAL — all Revision-2 mandates satisfied

---

## Revision-2 Mandate Compliance Checklist

All four binding mandates are satisfied:

| Mandate | Requirement | Satisfied |
|---|---|---|
| 1 | Power simulation at frozen IS length (true VR=0.898, N=500) | YES — 1.000 empirical power |
| 1 | Excised-IS robustness arm MANDATORY; COVID-dependence flag if applicable | YES — VR=0.8726, p=0.0279; no COVID flag (consistent) |
| 2 | Placebo Sharpe distribution filtered AND unfiltered | YES — filtered=unfiltered (0 excluded, all 67 windows ≥30 trades) |
| 2 | COVID-window excision trade count reported | YES — n_covid_bars_oos=377, n_ex_covid_trades=47 |
| 3 | Non-overlapping window specificity (effective N) stated | YES — effective N≈4; caveat included |
| 4 | Test A verdict cites ONLY p_rw(N=500, q=20, raw spread, frozen split) | YES — verdict based solely on p_rw=0.0798 |

---

## Part I — Test A: RB-CL Alternative Split

### Construction

| Parameter | Value |
|---|---|
| Pair | RB2!×42 ($/bbl) − CL2! ($/bbl) |
| β mode | F6 (β=1.0, definitional, zero updates) |
| f_βupdate | 0.000000 |
| Date range | 1998-08-03 → 2026-06-03 |
| IS range | 1998-08-03 → 2022-12-29 (last trading day ≤ 2022-12-31) |
| OOS range | 2023-01-02 → 2026-06-03 |
| Total merged bars | 6,993 |
| IS bars | 6,134 |
| IS valid (non-NaN) | 6,131 |
| OOS bars | 859 |
| OOS valid | 857 |
| Roll-masked bars | 5 (0.07%) |
| Flat bar % | 0% (constructed spread) |
| Negative CL barrel values | 232 (back-adj offset; roll-masked; increments unaffected) |
| Negative RB barrel values | 0 |

f_βupdate = 0.000000 < τ=0.10: PASS. F6 definitionally admissible.

### Primary Statistic: VR(20), IS raw spread

**Speed gate (N=200):** VR(20)=0.9008, p_rw=0.0945. Pass (≤0.20) — proceed to N=500.

**Full test (N=500):**

| Null family | VR(20) | p (N=500) | Role | Surrogate dist [p5, p50, p95] |
|---|---|---|---|---|
| **RW** | 0.9008 | **0.0798** | **PRIMARY GATE** | [0.8893, 0.9938, 1.0946] |
| GARCH(1,1) | 0.9008 | 0.2096 | Supporting | [0.8073, 0.9856, 1.1724] |
| MA(1)-noise | 0.9008 | 0.1158 | Supporting | [0.8775, 0.9725, 1.0802] |
| OU | 0.9008 | 0.0719 | Non-gating reference | [0.8924, 0.9890, 1.1167] |

**Full q grid (IS, RW, N=500) — informational, no argmax:**

| q | VR(q) | p_rw |
|---|---|---|
| 2 | 0.9887 | 0.1876 |
| 5 | 0.9547 | 0.0399 |
| 10 | 0.9000 | 0.0080 |
| **20** | **0.9008** | **0.0798** |
| 40 | 0.9533 | 0.3493 |

Primary statistic is VR(20) only. Secondary q values are informational; they do not change the verdict per §A.7 and Revision-2 Mandate 4.

### Revision-2 Mandatory: Excised-IS Robustness Arm

Excision: 2020-03-01 → 2021-06-30 (338 bars removed from IS).

| Metric | Full IS | Excised IS |
|---|---|---|
| n bars | 6,134 | 5,796 |
| VR(20) | 0.9008 | 0.8726 |
| p_rw (N=500) | 0.0798 | 0.0279 |
| Surr dist [p5, p50, p95] | [0.8893, 0.9938, 1.0946] | [0.8882, 0.9943, 1.1023] |

**COVID-dependence flag:** NOT triggered. Full-IS p=0.0798 (fails α=0.0167); excised-IS p=0.0279 (also fails α=0.0167). The signal does not depend on COVID-volatile bars — the spread is sub-diffusive both with and without the excision window, but neither meets the Bonferroni threshold.

Note: the excised-IS arm shows stronger signal (p=0.0279) than the full IS. The COVID-volatile bars slightly dilute the IS sub-diffusion rather than driving it. This makes a COVID-manufacture interpretation implausible, but it does not rescue the verdict — neither value crosses α=0.0167.

### Revision-2 Mandatory: Power Simulation

**True VR target:** 0.898  
**Calibration:** AR(1) with φ=−0.056561 (binary search); theoretical VR=0.8980  
**IS valid bars:** 6,131  
**N power paths:** 500  
**α:** 0.0167  

**Empirical power: 500/500 = 1.000**

Interpretation: an apparatus with 6,131 IS bars and true VR=0.898 has essentially 100% power to detect at α=0.0167. The failure to confirm (p=0.0798) therefore reflects genuine absence of sufficient sub-diffusion signal at this level, not a power limitation. The alternative split (IS≈6,100) was correctly motivated on power grounds, and it did raise power — but the spread does not actually beat the α=0.0167 threshold even with this sample size.

### Jackknife Concentration Check

| Metric | Value |
|---|---|
| Full-IS VR(20) | 0.9008 |
| JK min | 0.8558 |
| JK median | 0.8951 |
| JK max | 0.9820 |
| Max drop (vs full) | 5.0% |
| Threshold | 300% |
| Verdict | PASS |

No concentration instability. Sub-diffusion is broadly distributed across IS episodes.

### IS Economics (Secondary, Informational)

θ=1.0, LB=60, MH=40.

| Cost ($/bbl) | Net/trade ($/bbl) |
|---|---|
| 0.05 | −0.2826 |
| 0.10 | −0.3326 |
| 0.15 | −0.3826 |
| 0.20 | −0.4326 |
| 0.30 | −0.5326 |
| 0.40 | −0.6326 |
| 0.50 | −0.7326 |
| 0.80 | −1.0326 |
| 1.00 | −1.2326 |

IS: n_trades=195, mean_gross=−0.2326 $/bbl, mean_net(0.20)=−0.4326 $/bbl, Sharpe=−0.344.

IS economics are negative across the entire cost grid. Note: VR sub-diffusion in the IS spread does not translate to positive IS fade economics at θ=1.0 — the spread mean-reverts weakly but not enough to produce positive gross expectancy at this entry threshold.

### OOS Secondary Characterisation

OOS (2023-01-02 → 2026-06-03): n_bars=859, n_valid=857.

| Metric | Value |
|---|---|
| VR(20) | 0.8434 |
| p_rw (N=500) | 0.2555 |
| n_trades | 31 |
| mean_net (0.20) | +0.4300 $/bbl |
| Sharpe | 0.330 |

OOS: n_trades=31 ≥ 30. OOS mean_net=+0.4300 > 0 at primary cost → no OOS sign reversal kill. However, OOS VR p_rw=0.2555 (non-significant). The OOS economics are incidentally positive but do not rescue the IS result — the verdict is determined solely by p_rw(N=500, q=20, IS).

### Kill Gates

| Gate | Result |
|---|---|
| 1. f_βupdate ≥ 10% | PASS (F6, f=0.000) |
| 2. Speed gate p_rw(N=200) > 0.20 | PASS (p=0.0945) |
| 3. Jackknife drop > 300% | PASS (5.0% max drop) |
| 4. Third-look failure p_rw(N=500) ≥ 0.0167 | **KILL — ARCHIVED (permanent)** |
| 5. OOS sign reversal (n≥30) | N/A — IS gate killed first; OOS was PASS regardless |

### Test A Verdict

**ARCHIVED (permanent)**

p_rw(N=500) = 0.0798. This exceeds both the Bonferroni spending threshold α=0.0167 and the INCONCLUSIVE band boundary 0.05. The kill is unconditional — per §A.10 kill criterion 4 and §A.12:

> "p_rw ≥ 0.05 at N=500 → RB-CL moves DEFERRED → ARCHIVED. No fourth look, no alternative construction attempt, no θ-tuning rescue. This kill is permanent and unconditional."

**Registry transition: DEFERRED-OOS-SIGNAL → ARCHIVED (permanent).**

No fourth split. No further RB-CL IS VR testing. Portfolio combination blocked permanently on RB-CL.

**Apparatus note (§A.12 / §11.8):** The apparatus has been validated — it has near-unity power at 6,131 bars for true VR=0.898, and the positive control (LE-GF, doc 46) confirms. RB-CL IS sub-diffusion is not supported across three pre-named looks (doc 40 full-period p=0.015; doc 45 IS-only p=0.313; this look p=0.0798). Three looks with different splits have all failed at the Bonferroni-corrected threshold. The apparatus is not the cause.

---

## Part II — Test B: LE-GF Ex-COVID OOS Economics

### Construction

| Parameter | Value |
|---|---|
| Pair | CME_DL_LE2! vs CME_DL_GF2! |
| β mode | F5 (pre-sample OLS, first 25% = 1,472 bars, frozen thereafter) |
| β computed | 0.56500 |
| β frozen (pre-registered) | 0.565 |
| \|β_computed − β_frozen\| | 0.0000 (exact match) |
| f_βupdate | 0.000000 |
| Date range | 2002-08-14 → 2026-06-03 |
| n total | 5,890 |
| IS (70%) | 4,123 bars (2002-08-14 → 2019-05-23) |
| OOS (30%) | 1,767 bars (2019-05-24 → 2026-06-03) |
| Roll-masked | 1 bar |

β verification: computed β=0.56500 matches pre-registered β=0.565 exactly.

### Full OOS Baseline (from doc 44/45)

| Metric | Value |
|---|---|
| n_trades | 60 |
| Sharpe | 0.342 |
| mean_net (0.20¢/lb) | +0.2965 ¢/lb |

Full OOS Sharpe=0.342 (consistent with doc 44 reference of 0.233 — note: the dates here extend to 2026-06-03, adding ~1 year of OOS, which shifts the Sharpe upward from the doc-44/45 computation).

### Ex-COVID OOS Primary Result

Excision: 2020-01-01 → 2021-06-30 (377 COVID bars removed from OOS).

| Metric | Value |
|---|---|
| n_covid_bars_oos | 377 |
| n_oos_excised_bars | 1,390 |
| n_ex_covid_trades | 47 |
| Sharpe_ex_covid | **0.3508** |
| mean_net_ex_covid (0.20¢/lb) | +0.2782 ¢/lb |
| Sharpe delta (ex-COVID − full OOS) | +0.009 |
| Criterion 1 (Sharpe > 0.50) | **FAIL** |

n_ex_covid_trades=47 ≥ 30: passes minimum-trades gate (verdict is not INCONCLUSIVE).  
mean_net_ex_covid=+0.2782 > 0: positive net expectancy at primary cost.  
Sharpe_ex_covid=0.3508 ≤ 0.50: **Criterion 1 fails.**

**Key diagnostic: Sharpe delta = +0.009.** The COVID excision produces essentially no improvement in Sharpe (0.342 → 0.351). The OOS underperformance attributed to COVID in docs 45/46 is not substantiated by this window definition. The 18-month ex-COVID window (through 2021-06-30) does not explain the gap between IS Sharpe=0.939 and OOS Sharpe.

### Ex-COVID OOS Cost Grid

| Cost (¢/lb) | Net/trade (¢/lb) |
|---|---|
| 0.05 | +0.4282 |
| 0.10 | +0.3782 |
| 0.15 | +0.3282 |
| 0.20 | +0.2782 |
| 0.25 | +0.2282 |
| 0.30 | +0.1782 |
| 0.40 | +0.0782 |
| 0.50 | −0.0219 |

Breakeven cost ≈ 0.48¢/lb.

### Surrogate Reference (Informational)

| Null | p (ex-COVID OOS) |
|---|---|
| RW | 0.0299 |
| OU | 0.0719 |

Both informational only — primary gate is the dual-criterion Sharpe test.

### Placebo Control (Criterion 2, Mandatory)

Placebo windows: all contiguous 18-month excisions within OOS period, monthly step.

| Metric | Value |
|---|---|
| Total windows enumerated | 67 |
| Included (≥30 trades remaining) | 67 |
| Excluded (<30 trades) | 0 |
| Effective N (non-overlapping) | ≈4 |

**Placebo Sharpe distribution (filtered, n=67):**

| Pctile | Sharpe |
|---|---|
| min (0th) | −0.2218 |
| p25 | 0.1331 |
| p50 | 0.3089 |
| p75 | 0.5414 |
| **p90** | **0.6574** |
| max (100th) | 0.9620 |

**COVID-excision Sharpe=0.3508. Rank=36/67 = 53.7th percentile.**

Criterion 2 (≥ p90=0.6574): **FAIL** (0.3508 < 0.6574).

**Effective-N caveat (Revision-2 Mandate 3):** The 90th-percentile rank is computed over 67 overlapping monthly-step windows; effective independent draws ≈4. The COVID-excision Sharpe lands at the 53.7th percentile of the overlapping distribution — solidly in the middle of the distribution, far below the 90th percentile in both the overlapping and the non-overlapping sense. The specificity claim fails unambiguously regardless of the overlapping-window caveat.

**Interpretation:** Removing the COVID window does not specifically lift OOS Sharpe. The ex-COVID Sharpe (0.351) is nearly identical to the median placebo Sharpe (0.309). Removing any typical 18-month block from the OOS produces similar or better results than removing the designated COVID window. The COVID-mechanism hypothesis (that COVID disruption specifically caused OOS underperformance) is not supported.

### Test B Kill Gates

| Gate | Result |
|---|---|
| n_OOS_ex_covid ≥ 30 trades | PASS (n=47) |
| Criterion 1 (Sharpe_ex_covid > 0.50) | **FAIL (Sharpe=0.3508)** |
| Criterion 2 (placebo specificity ≥ p90) | **FAIL (pctile=53.7%)** |
| mean_net_ex_covid > 0 | PASS (+0.2782 ¢/lb) |

### Test B Verdict

**OOS-STRUCTURAL-WEAKNESS**

Criterion 1 fails: Sharpe_ex_covid=0.3508 ≤ 0.50. Criterion 2 also fails independently (COVID excision is the 53.7th percentile of all 18-month excisions — not specific to the COVID window).

Per §B.9 kill criterion 2:
> "COVID explanation is insufficient; LE-GF OOS weakness is structural, not COVID-specific."

**Registry:** LE-GF remains at §11.8 IS-ONLY CONFIRMED. The IS result (doc 46 p_rw=0.024) is unchanged and unaffected. OOS standalone re-evaluation is NOT supported. Combination gate blocked.

---

## Part III — Combination Gate (§C.1)

| Test | Verdict |
|---|---|
| Test A | ARCHIVED (permanent) |
| Test B | OOS-STRUCTURAL-WEAKNESS |

**Combination gate: BLOCKED.**

Both tests failed. Per §C.1:
> "Either test reaching ARCHIVED/FAIL + the other FAIL → programme is at single-sleeve LE-GF IS-anchor status only. Tier-1 two-sleeve book is DEFERRED until a new instrument with IS VR confirmation is identified."

Independence ρ=0.013 (doc 45 Gate B) remains confirmed but is irrelevant — the gate requires both sleeves to have confirmed IS VR and bilateral economics.

---

## Summary Table — All Primary Numbers

| Statistic | Value | Threshold | Result |
|---|---|---|---|
| **TEST A** | | | |
| f_βupdate (F6) | 0.000000 | <0.10 | PASS |
| VR(20) IS raw | 0.9008 | — | — |
| p_rw N=200 speed gate | 0.0945 | <0.20 | PASS |
| p_rw N=500 PRIMARY | **0.0798** | <0.0167 | **FAIL → ARCHIVED** |
| p_garch N=500 | 0.2096 | — | informational |
| p_ma1 N=500 | 0.1158 | — | informational |
| p_ou N=500 | 0.0719 | — | informational |
| Jackknife drop | 5.0% | <300% | PASS |
| VR(20) excised-IS | 0.8726 | — | informational |
| p_rw excised-IS | 0.0279 | — | informational (no COVID flag) |
| Empirical power (VR=0.898) | **1.000** | — | power adequate |
| OOS p_rw N=500 | 0.2555 | — | informational |
| OOS n_trades | 31 | ≥30 | sign-reversal gate applicable |
| OOS mean_net | +0.4300 | >0 | no sign reversal |
| **TEST B** | | | |
| f_βupdate (F5) | 0.000000 | <0.10 | PASS |
| β computed | 0.56500 | =0.565 | exact match |
| Full OOS Sharpe | 0.342 | — | reference |
| n_ex_covid_trades | 47 | ≥30 | trade gate PASS |
| Sharpe_ex_covid | **0.3508** | >0.50 | **FAIL Criterion 1** |
| mean_net_ex_covid | +0.2782¢/lb | >0 | PASS |
| Sharpe delta | +0.009 | — | negligible lift |
| Placebo p90 (filtered) | 0.6574 | — | — |
| COVID-excision pctile | **53.7%** | ≥90% | **FAIL Criterion 2** |
| Effective N (non-overlapping) | ≈4 | — | caveat noted |

---

## Registry Transitions

| Instrument | Prior status | New status | Trigger |
|---|---|---|---|
| RB-CL | DEFERRED-OOS-SIGNAL | **ARCHIVED (PERMANENT)** | Third look p=0.0798 ≥ 0.0167; §A.10 kill criterion 4 |
| LE-GF | §11.8 IS-ONLY CONFIRMED | **§11.8 IS-ONLY CONFIRMED (unchanged)** | Test B does not archive; OOS weakness structural |

**RB-CL archive is unconditional and permanent.** No fourth split, no alternative construction, no θ-tuning rescue. The apparatus is validated (power=1.000; LE-GF positive control confirmed in doc 46). RB-CL IS sub-diffusion is not supported.

**LE-GF IS anchor is preserved.** The IS VR result from doc 46 (p_rw=0.024) stands. Test B failure does not weaken the IS finding. LE-GF is IS-anchored but OOS-unconfirmed.

---

## Non-Conclusions (Explicit)

1. The OOS incidental positivity for RB-CL (Sharpe=0.330, mean_net=+0.43) is NOT a result — OOS was held out entirely and is informational; the IS gate governs.
2. VR(10) for RB-CL IS yielding p=0.0080 (significant) is NOT a result — q=20 is the pre-committed primary; reporting VR(10) as supporting evidence would void the alpha-spending guarantee (Revision-2 Mandate 4). Full grid is reported for completeness only.
3. The excised-IS arm showing p=0.0279 is NOT a rescue — it is informational. The primary IS period is used in full.
4. LE-GF ex-COVID Sharpe=0.351 being positive net does NOT constitute OOS confirmation.
5. The placebo distribution showing wide variation does NOT excuse the COVID excision ranking at p53.7.

---

## Next Action

Per §C.2 and §11.8: programme is at single-sleeve LE-GF IS-anchor status only.

The combination pre-registration (doc 49) **cannot be opened** — it requires both Test A CONFIRMED and Test B COVID-MECHANISM-CONFIRMED.

The standing §11.8 mandate remains: the apparatus can detect a known real reverter (LE-GF confirmed; NG confirmed conditionally). The next high-information action is identifying a second instrument with IS VR confirmation to reconstruct the two-sleeve book. Candidates per the hypothesis registry should be evaluated under a new pre-registration.

*Results frozen 2026-06-10. No parameters, thresholds, or verdicts may be revised post-execution.*
