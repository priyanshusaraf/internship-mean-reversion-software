# Doc 36 — BRN M1–M2 Daily Calendar: Results & Verdict

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Date:** 2026-06-05. **Pre-registration:** `brn_calendar_prereg.md` (frozen before execution).
**Data:** `data/processed/brn_results.json` (full null distributions, full search).
**Mode:** Trader-discovery. **Prior:** LOW-MEDIUM 15–25%.
**Status:** MERELY-TRUE — MR confirmed statistically but non-deployable for a 1-12 week book.
**Extends:** doc 35 (BRN execution prep), doc 23 (NG rolling-local), doc 25 (portfolio economics).

**Numbering note:** Doc 30 and doc 33 each have two files (numbering collision). This doc is 36 — next
clean sequential number. Collisions: 25 (two), 28 (two), 30 (two), 33 (two) — notation only; no
research-record impact. Future docs continue from 37.

---

## Prior Belief (FROZEN before execution)

**Instrument prior:** LOW-MEDIUM probability (15–25%) of SLEEVE_CANDIDATE outcome.
- BRN has a genuine storage restoring force (elastic floating storage) — mechanism supports calendar MR.
- Higher market efficiency than NG (Brent = world's most liquid crude calendar); smaller per-trade alpha.
- OPEC structural trend risk: multi-month directional regimes with no NG analog create systematic trend episodes.
- No cost-clearing calendar instrument confirmed to date (NG is PERSISTENT-BUT-UNECONOMIC, doc 23).

---

## Execution Record

**Execution:** Phase 1 script `scripts/run_brn_calendar_test.py` (written 2026-06-05; not a modification of frozen primitives).
**Data coverage (confirmed pre-freeze):** BRN1! 7,341 bars (1997-10-22 → 2026-06-04); BRN2! 8,872 bars (1991-10-03 → 2026-06-04). Inner join: 7,341 daily bars.
**Construction:** β=1 definitional (BRN1! close − BRN2! close), ADR_003 roll-mask k=8.0, causal deseasonalization.

---

## Evidence Gathered

### Spread Characteristics

| Metric | Value |
|---|---|
| Mean | −7.186 $/bbl |
| Std | 4.595 $/bbl |
| Min / Max | −15.28 / +8.95 $/bbl |
| Roll-masked bars | 24 of 7,341 (0.33%) |
| Flat bars | 0 |

**Anomaly flagged:** Spread mean = −7.186 $/bbl. An adjacent-month futures calendar spread should not carry a persistent level offset of this magnitude from fundamental storage economics alone. This flags potential back-adjustment artifact (back-adjusted legs from TradingView accumulate asymmetric cumulative offsets over 28 years of monthly rolls). [MEASUREMENT concern — adversarial Finding 1]

### VR Test (QUANT gate)

| Metric | Value |
|---|---|
| VR(5) | 0.4770 |
| VR(10) | 0.3677 |
| **VR(20) — PRIMARY** | **0.2824** |
| VR(40) | 0.2216 |
| VR(60) | 0.1947 |
| p_rw (N=200) | 0.005 — speed gate PASSES |
| p_rw (N=500) | 0.002 |
| p_garch (N=500) | 0.002 |
| p_ma1 (N=500) | 0.002 |
| **p_ou (N=500)** | **1.000** |
| RW∧GARCH∧MA(1) gate | **PASS** |

**Key: p_ou = 1.000.** The BRN spread is statistically indistinguishable from a matched OU process at the primary q=20. Sub-diffusion is confirmed vs martingale nulls but is NOT stronger than an OU surrogate. This means the dynamics are *consistent with* a well-calibrated OU process — the test cannot distinguish BRN from an OU null.

**VR profile shape:** Monotonically declining from q=5 to q=60 (no "MR bowl" recovery). This suggests very slow mean reversion or a near-unit-root process — NOT the characteristic fast-reverting calendar spread pattern.

### OOS Split (70/30 by date; ~1997–2011 train, ~2012–2026 OOS)

| Period | VR(20) | Bars |
|---|---|---|
| Training | 0.1936 | 5,138 |
| OOS | **0.6895** | 2,203 |
| Sign flip (OOS − train > 0.15) | **TRUE** (gap = 0.496) | — |

**Structural break:** The OOS period (2012–2026, the deployment-relevant window) shows VR=0.689 — substantially weaker and approaching diffusion. The gap of 0.496 is 3× the pre-registered flag threshold. This coincides with US shale growth (~2012) + BRN financialization, creating a credible permanent structural change.

### Global Half-Life

**HL = 106.8 bars** (~5 months). **Outside tradeable band [5, 60] bars.**

For a 1–12 week (5–60 bar) institutional book, reversion takes 5× longer than the book capacity. The 20-bar stop-loss forces most trades to exit before reversion completes.

### Rolling-Local Book Sim (doc-23 frame, crisis isolation)

| Pool | mean_z | N windows | N below RW median | avg gross (K=0.005) |
|---|---|---|---|---|
| Full sample | −0.699 | 29 | 21/29 | 0.1287 $/bbl |
| **Ex-crisis (2020/2022 excluded)** | **−0.907** | 27 | 21/27 | **0.1286 $/bbl** |
| Crisis only (2020, 2022) | **+2.111** | 2 | 0/2 | 0.1454 $/bbl |

**Crisis years confirmed trending:** VR(20)_2020 = 1.633, VR(20)_2022 = 1.525. These are strongly diffusive/trending — the OPEC-supply-shock mechanism flagged in doc 35 is confirmed.

**Year-by-year VR(20) trajectory (1998–2026):**
```
1998: 0.238 | 1999: 0.519 | 2000: 0.350 | 2001: 0.357 | 2002: 0.790 | 2003: 0.648
2004: 0.988 | 2005: 0.554 | 2006: 0.997 | 2007: 0.564 | 2008: 0.427 | 2009: 0.434
2010: 1.102 | 2011: 0.660 | 2012: 0.666 | 2013: 0.674 | 2014: 1.061 | 2015: 0.496
2016: 0.415 | 2017: 0.263 | 2018: 0.919 | 2019: 0.734 | [2020: 1.633] | 2021: 1.077
[2022: 1.525] | 2023: 0.842 | 2024: 0.560 | 2025: 0.490 | 2026: 0.427
```
Note: 2003 (0.988), 2004 (0.988→near-1), 2006 (0.997→near-1), 2010 (1.102), 2014 (1.061), 2021 (1.077) also show near-diffusive or trending years — the MR is NOT universal even in the ex-crisis sample.

**Economic gate calibration issue:** The book sim used cost grid {0.003, 0.005, 0.008} $/bbl. Doc 35 estimates realistic BRN institutional round-trip cost at $0.03/bbl — 6× the pre-registered primary gate (0.005). The avg gross of 0.1286 $/bbl still appears positive at $0.03/bbl cost, but the book sim was computed on the full sample (contaminated by training-period back-adj artifact); the OOS-only book sim at $0.03/bbl has not been run. The economic gate claim is therefore unverified at realistic costs in the deployment-relevant window.

### Four-Lens Adjudication (Phase 2 — mandatory, §11.6)

**Adversarial lens (opus):**
- Finding 1 (MEASUREMENT, HIGH): Back-adjustment manufactures VR in training window; spread mean −7.186 $/bbl is anomalous for an adjacent-month calendar.
- Finding 2 (STRUCTURAL, HIGH): OOS sign flip is a permanent structural break verdict, not degradation.
- Finding 3 (MEASUREMENT, HIGH): Cost calibration 6× below realistic; economic gate unvalidated.
- Finding 4 (METHODOLOGY, MED): Global HL failure not rescued by rolling-local paradox; local HL is not pre-registered and unverified.

**Statistical lens (opus):**
- p_ou=1.000 means BRN is indistinguishable from a matched OU surrogate — weak differential evidence.
- OOS VR=0.689 may still be sub-diffusive (z≈−2.9 estimated) but the global p=0.002 is not admissible as a current deployability statement.
- Rolling-local DOF correctly controlled (crisis exclusion was pre-registered); pooled mean-z is valid on its own terms.
- The floor p-value (0.002 = 1/500+correction) has reached maximum resolution; the exact value carries no additional information.

**Trader lens (sonnet):**
- HL=107 bars fatally incompatible with 1-12 week book; the 20-bar stop bleeds systematically against 107-bar mean reversion.
- OOS VR=0.689 in the deployment-relevant window (post-2012) makes the strategy questionable for a trader today.
- NG+BRN = two energy calendars; tail correlation confirmed (both VR>1 in 2020 and 2022) — NOT independent sleeves per doc 25 independence requirement.
- Economic gate unvalidated at $0.03/bbl cost and OOS-only simulation.

**Synthesis verdict:** MERELY-TRUE (HIGH confidence). Adversarial and trader findings independently sufficient to block any higher verdict. All three lenses converge.

---

## Verdict (FROZEN)

```
VERDICT:           MERELY-TRUE
CONFIDENCE CLASS:  HIGH
PROBLEM CLASS:     STRUCTURAL + MEASUREMENT + METHODOLOGY
```

**Decision path:**
- QUANT gate: **PASS** (p_rw=0.002 at N=500, RW∧GARCH∧MA(1) confirmed)
- Half-life gate: **FAIL** (106.8 bars >> 60-bar tradeable band)
- OOS integrity: **FAIL** (sign flip: 0.194 → 0.689, structural break)
- Economic gate: **UNVERIFIED** at realistic cost ($0.03/bbl) and OOS-only sim
- Crisis correlation: NG+BRN are energy co-correlated → FAIL independence requirement for book

**Bottom line:** BRN M1-M2 calendar spread has statistically real sub-diffusion in the historical aggregate — storage MR theory is consistent with the data. But it is not deployable for a 1-12 week institutional book in its current unconditional form, for four independent reasons.

---

## Confidence Update

| | Before | After |
|---|---|---|
| BRN calendar MR statistically real | LOW-MEDIUM | **MEDIUM-HIGH** (confirmed by strong VR, triple-surrogate) |
| BRN calendar deployable (unconditional) | LOW-MEDIUM 15-25% | **LOW** (multiple independent failure modes) |
| Storage MR hypothesis (cross-instrument) | MEDIUM (NG alone) | **MEDIUM-HIGH** (NG + BRN both confirm real MR) |
| Energy calendar diversification value | — | **LOW** (crisis tail correlation — NOT independent sleeves) |
| Calendar thesis alive for ZC | HIGH (structural diversification) | **UNCHANGED — ZC now carries the diversification hope** |

---

## Surviving Uncertainty

- Local (within-year, ex-crisis) short-horizon reversion may exist as a genuine sub-component; local HL is unquantified and pre-registration-unverified.
- Whether post-2012 OOS VR=0.689 is a recoverable regime shift or permanent financialization is unresolved; post-2012-only pre-registered test has not been run.
- Back-adjustment artifact magnitude for BRN is unquantified; raw unadjusted spread reconstruction has not been attempted.

## Explicit Non-Conclusions

- This does NOT prove BRN calendar MR is absent in the physical market.
- This does NOT confirm or deny the EIA-conditional energy calendar hypothesis (unconditional failure is consistent with conditional entry being the correct form).
- This does NOT support treating BRN as an independent portfolio sleeve alongside NG.

## Next High-Information Question

Does the BRN M1-M2 spread constructed from raw (unadjusted) settlement prices, tested on the post-2012 sub-sample only at $0.03/bbl realistic cost, pass the VR and HL gates? If yes, the direction reopens as a post-2012 conditional instrument. If no, BRN is definitively closed in unconditional form.

---

## Strategic Implication for the Programme

1. **Energy calendar thesis (NG + BRN unconditional):** Both confirmed merely-true. The unconditional form of energy calendar MR is consistently real-but-undeployable. This is now a robust cross-instrument finding.

2. **Diversification via BRN:** CLOSED. NG and BRN are energy co-correlated sleeves; they share crisis-year tail risk. Portfolio breadth from a NG+BRN book does not meet the independence requirement of doc 25.

3. **ZC (corn) calendar:** NOW CARRIES the non-energy diversification thesis. The structural difference (agricultural vs energy mechanism; no OPEC analog) makes ZC the first genuine portfolio-breadth candidate. ZC prereg is frozen (zc_calendar_prereg.md, 2026-06-05) — ready to execute.

4. **Crack-spread controlled-β:** The KEYSTONE remains untouched. The calendar results (NG + BRN MERELY-TRUE) make the controlled-β test MORE important, not less. If the β=1 definitional form cannot support a deployable book, the programme's deployment route requires estimated-β pairs (doc 30 architecture). The crack-β readiness memo (doc 36a, this session) identifies the next blocking item.

5. **EIA conditional entry (doc 33):** KILLED (doc 34), but the non-conclusion above keeps the conditional-entry CONCEPT alive for future pre-registration on a different conditioning variable.

---

*Append-only record — no revisionist history. Provenance: Phase 1 execution (scripts/run_brn_calendar_test.py), Phase 2 four-lens adjudication (workflow brn-four-lens-adjudication, 2026-06-05), synthesis (main session).*
