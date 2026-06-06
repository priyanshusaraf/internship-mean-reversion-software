# Doc 38 — ZC M1–M2 Corn Calendar: Results & Verdict

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Date:** 2026-06-05. **Pre-registration:** `zc_calendar_prereg.md` (frozen 2026-06-05).
**Status:** CONTAMINATED_RESULT — VR signal is artifact of deseasonalization on back-adjusted prices.
**Extends:** doc 36 (BRN calendar), doc 38a (back-adj diagnostic). **Data:** `data/processed/zc_results.json`.

---

## Prior Belief (FROZEN before execution)

**Prior:** MEDIUM 30-45% probability of SLEEVE_CANDIDATE.
Rationale: non-energy mechanism, stronger seasonal anchor than BRN, fixed storage capacity.
Calibration: NG PERSISTENT-BUT-UNECONOMIC, BRN MERELY-TRUE (doc 36).

---

## Evidence Gathered

### Spread Characteristics (ANOMALY)

| Metric | Value | Comment |
|---|---|---|
| Mean | 202.540 cents/bushel | ANOMALOUS — adjacent-month calendar should be 0-50 cents; confirms back-adj level offset |
| Std | 232.921 cents/bushel | Enormous relative to expected spread range |
| Roll-masked bars | 176 of 8,698 (2.0%) | Higher than BRN (0.33%) — more roll seams flagged |
| Flat bars | 0 | — |

### VR Test (N=500 — Quant gate)

| Metric | Value | Interpretation |
|---|---|---|
| VR(20) | **0.1583** | Extremely strong apparent sub-diffusion |
| p_rw | **0.002** | Maximum resolution (N=500 floor) |
| p_garch | **0.002** | — |
| p_ma1 | **0.002** | Sub-diffusion is more than bid-ask bounce |
| **p_ou** | **0.002** | **RED FLAG: real spread beats matched OU surrogate** |

**p_ou = 0.002 is an artifact fingerprint, not exceptional MR.** A matched OU surrogate is parameterized to the spread's own HL=315 bars. Beating it at q=20 means the short-lag structure is far more stationary than a 315-bar OU process — impossible from genuine market dynamics, but consistent with causal monthly-mean subtraction imposing short-horizon stationarity on a back-adjusted level.

### OOS Split (70/30 by date; train ≈ 1991-2010, OOS ≈ 2010-2026)

| Period | VR(20) | N bars | Interpretation |
|---|---|---|---|
| Training | 0.1764 | 6,089 | Strong in training (artifact-rich period) |
| **OOS** | **0.9200** | 2,609 | **Near-pure diffusion — statistically indistinguishable from RW** |
| Sign flip | TRUE (gap=0.744, 5× the 0.15 threshold) | — | Largest OOS degradation in the programme |

The OOS confidence interval: with n≈2,600 bars, SE ≈ √(40/2600) ≈ 0.124. A 95% CI on VR=0.920 spans [0.68, 1.16] — contains 1.0. The OOS period is statistically random walk.

### Global Half-Life: 315.6 bars (~15 months). **5.3× outside tradeable band [5, 60].**

### Rolling-Local (doc-23 frame)

| Pool | mean_z | N windows | Note |
|---|---|---|---|
| Full sample | -1.4127 | 36 | Below frac0.5 splice anchor (-1.053) |
| **Ex-crisis {2020,2022,2012}** | **-1.5062** | 33 | **IN CONTAMINATED ZONE** |
| Crisis only | +0.511 | 3 | 2020/2022/2012 trending as expected |

**Ex-crisis mean_z = -1.506 is below the frac0.5 splice anchor of -1.053** from doc 23 (calibrated on NG). By the doc-23 splice calibration, this places ZC in the CONTAMINATED zone.

### Back-Adjustment Diagnostic (Track C — same session, doc 38a)

| Spread | mean_z (raw) | mean_z (deseasonalized) | Ratio | Grade |
|---|---|---|---|---|
| NG vendor | -0.581 | -1.523 | 2.6× | CLEAN (raw genuine) |
| BRN M1-M2 | +0.259 | -0.699 | N/A | TRENDING raw (no raw MR) |
| **ZC M1-M2** | **-0.315** | **-1.413** | **4.5×** | CLEAN raw (marginal); CONTAMINATED deseason |

**ZC raw (no deseasonalization): mean_z = -0.315** — barely sub-diffusive, just below the RW null band. The 4.5× amplification to -1.413 when deseasonalized means the deseasonalization step created the apparent MR signal by removing the +202 cent back-adj offset, not by exposing genuine seasonal-adjusted MR.

### Four-Lens Adjudication Verdict

**All three lenses converge: CONTAMINATED_RESULT (HIGH confidence).**

- Adversarial: deseasonalization is artifact engine, not signal extraction; p_ou fingerprints contamination; spread mean=202 cents is data validity flag
- Statistical: p_ou vs HL=315 is irreconcilable; frac0.5 comparison is directionally sound; OOS VR=0.920 CI contains 1.0
- Trader: HL=315 fatal on first gate; OOS is random walk; no diversification credit; calendar thesis should be formally closed

---

## Verdict (FROZEN)

```
VERDICT:           CONTAMINATED_RESULT
CONFIDENCE CLASS:  HIGH
PROBLEM CLASS:     MEASUREMENT + METHODOLOGY
```

**Decision path:**
- QUANT gate: PASS (p_rw=0.002, triple-surrogate confirmed, including p_ou — but p_ou=0.002 is artifact flag, not a stronger confirm)
- Half-life gate: FAIL (315.6 bars >> 60-bar tradeable band)
- Back-adj contamination: CONFIRMED (ex-crisis mean_z = -1.506 < frac0.5 anchor of -1.053; 4.5× deseason amplification of marginal raw signal)
- OOS: FAIL (VR=0.920, statistically random walk)
- Raw signal: marginal (-0.315), not establishing genuine MR prior to deseasonalization

**CONTAMINATED_RESULT vs MERELY_TRUE:** MERELY_TRUE implies a confirmed genuine MR signal that is non-deployable. Here, the signal's validity itself is in question — the VR evidence is driven by a construction artifact (deseasonalization of back-adj level offset), not by genuine storage MR dynamics. CONTAMINATED_RESULT is the correct designation.

**NOTE:** This designation does NOT require the ZC market to have no genuine MR. It means the current test, as constructed on vendor back-adjusted data with causal deseasonalization, cannot cleanly distinguish genuine from artifact. The question is unresolved, not answered negatively.

---

## Confidence Update

| | Before | After |
|---|---|---|
| ZC calendar MR genuine (raw) | MEDIUM-HIGH | LOW-MEDIUM (raw mean_z = -0.315 marginal; no regime conditioning established) |
| ZC calendar deployable (unconditional) | MEDIUM (30-45%) | VERY LOW (<5%) |
| Grain storage MR hypothesis | MEDIUM | UNRESOLVED (ZC contaminated; no clean instrument) |
| Calendar thesis (NG+BRN+ZC) | ACTIVE | **FORMALLY CLOSED for unconditional daily form** |

---

## Explicit Non-Conclusions

- This does NOT prove grain storage MR is absent in the physical market.
- This does NOT validate or invalidate NG's PERSISTENT-BUT-UNECONOMIC verdict (NG has genuine raw sub-diffusion -0.581 which is independent of ZC's contamination).
- This does NOT close the crack-spread direction.

## Next High-Information Question

Does a clean, non-back-adjusted crack spread (HO2!-CL2! with frozen pre-sample β) show genuine MR in the OOS period? This is the §11.8 standing gate — apparatus must confirm a known real edge before the calendar kills carry full apparatus-validated weight.

---

## Strategic Implication

ZC closes the calendar programme. All three instruments (NG, BRN, ZC) return non-deployable verdicts. The crack-β keystone (now cleared on synthetic gate) is the only remaining path.

**§11.8 mandate activated:** "Before any further negative/kill is credible, the apparatus must demonstrate it can CONFIRM a known, literature-documented, economically-anchored REAL edge." The three calendar kills are only fully credible after the crack-spread confirms. This is not optional.

*Append-only. Provenance: Phase 1 (scripts/run_zc_calendar_test.py), Track C back-adj diagnostic, Phase 2 four-lens workflow (2026-06-05).*
