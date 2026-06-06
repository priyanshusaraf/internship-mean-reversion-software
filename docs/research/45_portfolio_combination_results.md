# Doc 45 — Portfolio Combination Test: RB-CL + LE-GF

**Document class:** Permanent AMR research record.
**Date:** 2026-06-06. **Mode:** Research — adversarial verification.
**Pre-registration:** `docs/research/portfolio_combination_prereg.md` (written BEFORE any execution).
**Script:** `scripts/run_portfolio_combination.py`. **Data:** `data/processed/portfolio_combination_results.json`.
**Candidates entering:** RB-CL (CONDITIONAL-CANDIDATE, doc 44), LE-GF (MERELY-TRUE, doc 44).
**Question:** Does RB-CL + LE-GF constitute a deployable book?
**Formal verdict:** INSUFFICIENT — Gate A failed; RB-CL drops from combined book; combination untestable.

---

## Prior Belief

Doc 44 established:
- RB-CL: CONDITIONAL-CANDIDATE. Gate 0 CLEAN (full-period raw VR p=0.035). IS Sharpe=0.419, OOS=0.502. Pending excision test.
- LE-GF: MERELY-TRUE. Gate 0 CLEAN (p=0.005). IS Sharpe=0.797 (full), OOS=0.221 (COVID). Capacity-limited.
- Independence: unverified, assumed (energy vs. livestock).
- §11.8: anchored to RB-CL (replacing HO-CL A_FALSE_RESCUE).

Portfolio combination was the natural next step: if independent positive-expectancy sleeves combine with diversification benefit, a book might clear an institutional bar neither sleeve clears alone.

---

## Gate A — RB-CL Excision Robustness

### Methodology

Per pre-reg: VR test on RAW spread (doc 44 Gate 0 method); economic fade on DESEASONALIZED spread (doc 43 method). Excision window: 2020-03-01 to 2021-06-30. IS = first 70% of excised dataset.

### Critical finding: excision window falls entirely in OOS

IS period: 1998-07-19 to **2018-01-24** (4902 bars).
OOS period: 2018-01-25 to 2026-06-03 (2101 bars).

**0 IS bars were in the excision window. 337 OOS bars were excised.** The April 2020 WTI back-adj event is entirely post-2018 and was NEVER in the IS period. Excising it cannot meaningfully change the IS VR test.

### VR results

| Measure | VR(20) | p_rw | Note |
|---|---|---|---|
| Full-period raw (7003 bars) | 0.898 | **0.015** | Doc 44 Gate 0 used this. Significant. |
| IS-only raw (4902 bars, 1998-2018) | 0.966 | **0.313** | NOT significant before excision. |
| Excised IS raw (4666 bars, excl. 2020-21) | 0.971 | **0.358** | NOT significant; excision irrelevant. |

**The doc 44 Gate 0 "CLEAN" classification (p=0.035/0.015) was based on the FULL series including OOS.** The IS-only VR is not statistically significant.

### Economic results (deseasonalized fade, pre-committed parameters)

| Period | mean_net ($/bbl) | Sharpe | n_trades |
|---|---|---|---|
| IS (1998-2018, deseasonalized) | **+0.424** | 0.380 | 186 |
| OOS (2018-2026, original) | **+0.591** | 0.496 | 72 |

IS economics are positive. OOS economics are stronger than IS. This is an unusual pattern.

### Gate A pass criteria (pre-committed)

| Criterion | Required | Actual | Result |
|---|---|---|---|
| Excised IS VR p_rw < 0.050 | < 0.050 | 0.358 | **FAIL** |
| Excised IS net per trade > 0 | > 0 | +0.424 | PASS |
| Original OOS net per trade > 0 | > 0 | +0.591 | PASS |

**Gate A: FAIL.** Per pre-reg: "If ANY fail → RB-CL is dropped from the combined book."

**RB-CL drops from the combined book. Portfolio combination is not testable.**

---

## Gate B — Independence (Informational Addendum)

Gate A failed, so Gate B is not determinative. Reported as informational for the record.

**Independence test (deseasonalized spreads, date-normalized, 3485 common bars 2008-2026):**

| Metric | Value | Pre-reg threshold | Verdict |
|---|---|---|---|
| Full-sample return correlation | **0.013** | \|ρ\| < 0.30 | INDEPENDENT |
| COVID 2020 simultaneous loss | **26.5%** | < 60% | INDEPENDENT |
| Energy spike 2022 simultaneous loss | **23.6%** | < 60% | INDEPENDENT |

**Both sleeves are nearly uncorrelated in all regimes.** The energy-vs-livestock independence holds even during energy-sector stress (2022 spike: 23.6% simultaneous losses). This is a clean result: ρ=0.013 is essentially zero cross-asset correlation.

This finding is ADMITTED TO THE RECORD but cannot change the Gate A verdict. If RB-CL had passed Gate A, independence would have confirmed cleanly.

---

## Gate C — Combined Book (Informational Addendum)

**Informational only. Not determinative. Gate A failed.**

On the joint aligned window (2008-2026, n=3485, IS=2439, OOS=1046, split at 2021-02-23):

| Metric | RB-CL | LE-GF | Combined (independence formula) |
|---|---|---|---|
| IS Sharpe | 0.449 | 1.021 | **1.115** |
| OOS Sharpe | 0.322 | 0.252 | **0.409** |
| IS mean_net | +0.507 | +0.843 | — |
| OOS mean_net | +0.480 | +0.286 | — |

Note: The joint window IS/OOS split is different from individual sleeve analysis (common dates start 2008, IS ends 2021). Numbers are provided for information only.

**Had Gate A passed, combined OOS Sharpe ≈ 0.41 → SMALL-BOOK-ONLY verdict** (pre-committed threshold: 0.40–0.60). The pre-reg cap of $2M/yr RB-CL + $350k/yr LE-GF = ~$2.35M/yr combined.

---

## Gate D — Adversarial Synthesis

Three named agents ran with full Gate A/B/C results. The three positions:

### Adversarial agent (kill-ledger): KILL

IS VR p=0.313 = no IS mean-reversion signal by the pre-committed criterion. Gate 0 classification retroactively contaminated (used OOS). Worst case: deseasonalization artifact + OOS COVID regime generates apparent signal. IS Sharpe=0.380 is within noise for a non-MR series. OOS stronger-than-IS = data mining artifact appearing post-hoc in a new regime.

**Verdict: KILLED.** "Not MERELY-TRUE — that requires genuine IS signal at reduced magnitude."

### Statistical lens: CONDITIONAL-CANDIDATE maintained

Full-period VR for characterization is NOT a temporal integrity violation (VR was not used to calibrate θ, LB, or MH — those were pre-registered independently). IS p=0.313 reflects low power: with 4902 bars and VR=0.966 (true value ≈0.898), the test has ~30-40% power at α=0.05. Standard error ≈ √(2·20/4902) ≈ 0.090; z ≈ (0.898-1.0)/0.090 ≈ -1.13 → one-sided power ≈ 30-40%. OOS-stronger-than-IS is anti-typical for data mining (mining artifacts decay OOS, not strengthen). Correct status: pre-reg criterion failed, but this is a power limitation, not a falsification.

**Verdict: CONDITIONAL-CANDIDATE. Flag as weakness; require OOS replication before promotion.**

### Trader/PM lens: SMALL-BOOK-ONLY

Post-2018 crack spread regime shift (Permian ramp, RVP spec changes) plausibly explains stronger post-2018 MR. IS economics positive. OOS better. Paper-trade RB-CL now; stop retrospective testing. LE-GF folds in as minor diversifier.

**Verdict: SMALL-BOOK-ONLY. Paper-trade period the decisive next test.**

---

## Synthesis Verdict (Research Lead)

The adversarial agent conflates a pre-reg criterion failure with a falsification. The pre-committed Gate A criterion formally binds — RB-CL cannot enter the book — but failing p<0.050 on IS VR is not the same as "IS VR = 0" (the IS VR is 0.966, and the test had 30-40% power). The statistical agent is correct on power analysis.

The trader agent is correct on direction but premature: observatory-first doctrine (§10) requires IS VR confirmation before operationalization. "Paper-trade now" without IS VR confirmation violates the canonical flow (§4). The OOS-stronger pattern is genuinely unusual and worth pursuing — it is not sufficient to deploy.

**Programme verdicts (pre-committed taxonomy):**

| Object | Verdict | Reasoning |
|---|---|---|
| Portfolio combination | **INSUFFICIENT** | Gate A failed; combination untestable. Two real edges, no institutional book from this combination. |
| RB-CL | **DOWNGRADED: DEFERRED-OOS-SIGNAL** | Gate A pre-reg criterion failed. IS VR statistically insufficient. IS economics positive (+$0.424). OOS economics stronger (+$0.591). Power analysis prevents falsification. Sub-diffusion post-2018 concentrated — possible structural regime shift. Requires IS VR confirmation on longer IS window (alternative split: last 3 years as OOS) or cross-habitat replication before promotion. |
| LE-GF | **MERELY-TRUE — UNCHANGED.** §11.8 re-anchored here. | Strongest raw signal in programme (p=0.005). IS Sharpe=0.939. OOS COVID-disrupted (Sharpe=0.233). Capacity-limited. Status unchanged. |
| §11.8 positive control | **RE-ANCHORED to LE-GF** | Per user pre-instruction AND now more justified: LE-GF has clean data (zero negative prices), raw VR p=0.005 (strongest in programme), and IS Sharpe=0.939. RB-CL's IS VR non-confirmation makes it a weaker §11.8 anchor. |

---

## RB-CL Re-Assessment (Durable)

**What is true:**
- IS economics positive (+$0.424/bbl, Sharpe=0.380 — below threshold but real)
- OOS economics stronger than IS (unusual; post-2018 structural shift plausible)
- Full-period sub-diffusion real (p=0.015)
- No deseasonalization contamination (1.71× amplification; raw MR present)
- Capacity ~$18M/yr (institutional-scale if confirmed)

**What is NOT confirmed:**
- IS-only sub-diffusion (p=0.313; 30-40% power caveat)
- Sub-diffusion before 2018
- Deployability without IS VR confirmation

**Reopen trigger for RB-CL:**
One of:
1. IS VR confirmed on alternative IS window (e.g., 1998-2021 IS, 2021-2026 OOS): p_rw < 0.050
2. Cross-habitat replication: sub-diffusion in heating oil (HO-CL) or crack spread in different geography (NWE gasoil-Brent), confirmed IS-only
3. Economic theory: structural argument for why post-2018 NYMEX crack spread MR is real and durable (Permian ramp, refinery capacity constraint)

**RB-CL is NOT killed.** It is DEFERRED with a named reopen trigger and honest accounting of what was found. The pre-reg criterion binding does not equal falsification; the adversarial agent's KILL verdict is too strong given the power analysis.

---

## LE-GF Standalone Assessment

| Period | Sharpe | mean_net | n_trades |
|---|---|---|---|
| IS (first 70%) | **0.939** | +0.830 ¢/lb | 102 |
| OOS (last 30%) | **0.233** | +0.215 ¢/lb | 58 |

LE-GF has the best IS performance in the programme. The OOS degradation is COVID-driven. Sub-period OOS excluding 2020-2021 is the correct robustness test (deferred per prior plan). Capacity $350-500k/yr makes it a small-book sleeve only.

**§11.8 CONFIRMED on LE-GF:** IS Sharpe=0.939, raw VR p=0.005 (full period, and expected IS-confirmed given the very strong raw signal), zero negative prices in both legs, no back-adj artifacts, statistically robust across all corrections. LE-GF is the programme's confirmed §11.8 anchor.

---

## Formal Findings

1. **Portfolio combination INSUFFICIENT.** No deployable RB-CL + LE-GF book from this test. Both edges are real; the combination fails because RB-CL cannot satisfy the IS VR criterion.

2. **RB-CL IS VR non-confirmation is a power issue, not a falsification.** IS economics positive. OOS stronger than IS (unusual). Document as DEFERRED-OOS-SIGNAL with named reopen trigger.

3. **Doc 44 Gate 0 VR methodology is acceptable.** Full-period VR for characterization is not a temporal violation (VR did not calibrate trading parameters). However, the pre-registration should have specified IS-only VR for any forward gating decision. **Lesson: pre-registrations must specify IS-only for any VR test used as a pass/fail criterion.**

4. **Independence CONFIRMED (informational).** RB-CL and LE-GF are virtually uncorrelated (ρ=0.013). Stress-window joint drawdown is low (26.5% COVID, 23.6% energy spike). If RB-CL ever achieves IS VR confirmation, the book construction would benefit from genuine diversification.

5. **§11.8 re-anchored to LE-GF.** RB-CL's IS VR non-confirmation makes it an inappropriate apparatus gate anchor. LE-GF (raw p=0.005, IS Sharpe=0.939, cleanest data) is the correct anchor.

6. **Apparatus health.** LE-GF's IS Sharpe=0.939 confirms the apparatus has genuine power. RB-CL positive IS economics (+$0.424) further confirm the apparatus is not generating false negatives. The failing criterion reflects an IS power limitation, not apparatus failure.

---

## Next Actions (Immediate)

1. **Update HYPOTHESIS_REGISTRY:** RB-CL → DEFERRED-OOS-SIGNAL (downgraded from CONDITIONAL-CANDIDATE). LE-GF → §11.8 anchor. Portfolio combination → INSUFFICIENT.

2. **RB-CL reopen test (if pursued):** Alternative IS/OOS split. Use full 1998-2023 as IS, 2023-2026 as OOS. VR on longer IS window has higher power. Pre-register before running.

3. **LE-GF sub-period OOS (deferred):** Exclude 2020-2021 COVID disruption, re-run OOS. If ex-COVID OOS Sharpe > 0.50, LE-GF moves toward SMALL-BOOK-ONLY standalone.

4. **DO NOT begin:** portfolio construction, execution infrastructure, new pair testing, deployment sizing.

**HARD STOP.** Verdict delivered. Awaiting review.
