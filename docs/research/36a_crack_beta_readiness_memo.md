# Crack-Spread Controlled-β Positive Control — Readiness Memo

**Date:** 2026-06-05. **Scope:** Assess readiness to execute the Cycle-2 controlled-β keystone test.
**This memo is INFORMATIONAL ONLY — do NOT execute until the execution prereg is written and frozen.**
**Governing spec:** doc 30 (`30_cycle2_controlled_beta_prereg.md`).

---

## 1. What Exists vs What Is Missing

### EXISTS (doc 30 — admissible specification)
- Full admissibility protocol: P (power) ∧ N (no-manufacture) ∧ M (mechanistic f_βupdate gate) ∧ C (causal)
- β-family candidates: F1 (Kalman/shrunk) > F2 (Ridge/shrinkage) > F3 (long-window OLS)
- Banned constructions: full-sample hindsight β, short-window rolling-OLS-on-levels, argmax-on-test-pair β
- Synthetic calibration suite: positive control (OU pair), Z1 (true martingale), Z2 (doc-19 stress null), Z3 (independent legs)
- Implementation surface: ~200-270 additive lines in `analytics_arm_a_v2_beta.py`
- Strategic positioning: correctly identified as the KEYSTONE (construction gate on all non-definitional spreads)

### MISSING — Execution prereg is NOT complete (doc 30 §6 explicitly says "no code, no data touched")

| Missing item | Impact | Where it must be committed |
|---|---|---|
| **Pre-committed real textbook pair** | Cannot execute without it; pair selection post-data is laundered lookahead | Execution prereg §1 |
| **Frozen hyperparameters** per family | F1: `q_beta` (Kalman process noise); F2: `λ` (ridge), `target` (prior); F3: `W` (frozen large window) | Execution prereg §2 |
| **Frozen τ (f_βupdate bound)** | Doc 30 says "e.g. τ=0.10" — not frozen; the bound that defines admissibility | Execution prereg §3 |
| **Frozen no-manufacture band** | "VR within a frozen band around 1" — quantitative band not specified | Execution prereg §4 |
| **Real pair literature anchor** | §11.8 positive control requires a "known, literature-documented, economically-anchored real edge" | Execution prereg §1 |

**Status: doc 30 is an admissible SPECIFICATION. It is NOT an executable pre-registration.**

---

## 2. Data Availability

| Leg | Bars | Date range | Status |
|---|---|---|---|
| `NYMEX_DL_CL1!, 1D.csv` | 9,844 | 1987-04-07 → 2026-06-03 | **Available** |
| `NYMEX_DL_CL2!, 1D.csv` | 9,230 | 1989-09-14 → 2026-06-03 | **Available** |
| `NYMEX_DL_HO2!, 1D.csv` | 7,728 | 1995-08-29 → 2026-06-03 | **Available** |
| `NYMEX_DL_RB2!, 1D.csv` | 7,006 | 1998-07-19 → 2026-06-03 | **Available** |

**Data is not a blocker.** All crack-spread legs are present with 27–39 years of daily history.

**Unix timestamp format:** All legs use Unix epoch timestamps (same as BRN). The `load_leg_unix()` wrapper from `run_brn_calendar_test.py` handles this — no new loader needed.

---

## 3. Candidate Pairs and Literature Anchors

**For the §11.8 positive control, the pair must have a published MR result.** Candidate pairs:

| Pair | Economic basis | Literature anchor | β-estimation required | Notes |
|---|---|---|---|---|
| **HO2! vs CL2!** (heating oil / crude) | Refinery margin (crack spread); storage arbitrage across refinery processing | Pindyck & Rotemberg (1990), Routledge et al. (2000) — crude/product cointegration documented | Yes: HO in $/gallon, CL in $/barrel (1 barrel = 42 gallons); refinery yield β ≈ 0.6–0.8 in return terms | RECOMMENDED: well-documented cointegration, economic mechanism clear |
| **RB2! vs CL2!** (gasoline / crude) | Gasoline crack spread; same refinery margin logic | Similar literature; Girma & Paulson (1998), Borenstein et al. (1997) | Yes: same unit conversion; β ≈ 0.6–0.9 | Alternative; less studied than HO-CL in storage MR literature |
| WTI (CL1!) vs Brent (BRN1!) | Geographic arbitrage, transport cost | Volkov & Yuhn (2016), Reboredo (2011) — documented cointegration | Yes: price-level cointegration, β near 1 but variable | Available but unit-identical (both $/barrel); less β-estimation challenge; weaker Cycle-2 test |

**Recommendation:** HO2! vs CL2! (heating oil vs crude oil, second-month to avoid front-month roll noise). Economic mechanism is clear, literature support is strong, and the unit-conversion β ≈ 42 provides a genuine estimation challenge (not definitional).

---

## 4. β-Construction Hazards (Flagged Explicitly — This Is the Highest-Artifact-Risk Test)

### H1 — Unit conversion creates near-definitional β

HO prices are in USD/gallon; CL in USD/barrel. The conversion factor 1 barrel = 42 gallons is a physical constant — not a market-estimated relationship. The β=42 (or 1/42) is DEFINITIONAL in the unit sense, but the CRACK MARGIN (the economic signal) varies around this. If the β estimate collapses to 42 (or the reciprocal), the construction reduces to a definitional spread — Cycle-2 is not testing estimation, it's replicating the β=1 logic in different units.

**Mitigation:** Normalize both legs to the same units ($/barrel) before β estimation. The estimated β should be close to 1.0 in normalized units. The deviation of β from 1.0 is the genuine estimation challenge.

### H2 — f_βupdate > τ is likely at short windows

The doc-19 stress test showed rolling-OLS W=60 had f_βupdate ≈ 0.82–0.97. For HO-CL, the refinery margin β changes slowly (seasonal, OPEC policy). Kalman β with tiny process noise and long-window OLS (W≥500) are the most likely admissible families. Ridge β shrunk toward 1.0 (normalized units) is also promising. Short-window families WILL fail Z2 — they are banned a priori (L-BAN-2).

**Mitigation:** Pre-commit LARGE frozen W for F3 (e.g., W=500 or W=1000). F1 (Kalman): pre-commit TINY q_beta (e.g., 0.0001 process noise variance). F2 (Ridge): pre-commit λ large enough to bind (e.g., λ=10.0 in normalized-units scale).

### H3 — Seasonal β variation

Crack spreads (especially heating oil) have strong seasonal patterns in the β relationship — the refinery margin widens in winter (heating demand) and narrows in summer. A static β=1 equivalent will misfit in seasonal peaks, generating spurious spread dynamics.

**Mitigation:** Causal trailing deseasonalization of both legs before β estimation OR pre-commit β estimation on deseasonalized legs. This must be in the execution prereg — not a post-hoc decision.

### H4 — Back-adjustment × β-estimation interaction

Both HO and CL are back-adjusted continuous contracts. The BRN experience (doc 36) confirmed back-adj can create persistent level offsets. For estimated-β spreads, back-adj offsets in BOTH legs interact with the β estimate — if the legs have different cumulative back-adj histories, the β estimate absorbs the cross-offset, creating spurious "stable β" reads.

**Mitigation:** The raw vs back-adj sensitivity check must be in the execution prereg. The mechanistic f_βupdate gate (§2.4) is the primary defense — it will detect if β movements are dominated by adjustment artifacts rather than fundamental changes.

### H5 — Surrogate mismatch: OU-pair vs crack-spread dynamics

The Cycle-2 synthetic positive control uses a "textbook cointegrated pair" (OU deviation). Real crack spreads have non-Gaussian, GARCH-type volatility AND seasonal β variation. The synthetic OU control may overestimate power on a real crack spread.

**Mitigation:** The MA(1)-noise surrogate (from the v2 apparatus) is the primary defense. The GARCH surrogate handles volatility clustering. Pre-commit that the real-pair verdict requires the full RW∧GARCH∧MA(1) gate (not just OU consistency).

---

## 5. Current Doctrine Assessment

**Does doc 30 remain admissible under current doctrine (§11 + BRN results)?**

- f_βupdate < τ gate: **ADMISSIBLE** — τ=0.10 is mentioned as the reference; not yet frozen, but the principle is correct and the gate is the right mechanistic instrument.
- β-family hierarchy: **ADMISSIBLE** — F1 > F2 > F3 ordering (highest suspicion on F3 = long-window OLS because closest to banned rolling-OLS). BRN results add no new information that changes this.
- No-manufacture band: **NEEDS SPECIFICATION** — "VR within a band around 1" is not a number. Must be frozen.
- Synthetic-first rule: **ADMISSIBLE** — synthetic calibration gate must pass before any real-pair read. This is correct.
- **BRN drift alert:** The BRN MERELY-TRUE result (HL=107 bars, back-adj artifact) reinforces the importance of the back-adj sensitivity check and the mechanistic f_βupdate gate. These were already in doc 30; no doctrine update needed.

**No doc 30 redraft required.** The specification is sound. The execution prereg is the missing piece.

---

## 6. Next Action (BEFORE EXECUTION)

**One blocking deliverable:** write the execution prereg extending doc 30 with:
1. Pre-committed pair: HO2! vs CL2! (normalized to $/barrel) with the Routledge et al. (2000) / Pindyck & Rotemberg (1990) literature anchor.
2. Frozen hyperparameters: F1 q_beta=0.0001; F2 λ=10.0 target=1.0; F3 W=500.
3. Frozen τ=0.10 (f_βupdate bound — the doc-19 mechanistic gate).
4. Frozen no-manufacture band: VR ∈ [0.85, 1.15] on Z1/Z2/Z3 (VR within this band = "not manufacturing").
5. Pre-registered real pair dates and deseasonalization decision (before or after β estimation).

This prereg is the gate. Only after it is written and frozen does implementation begin (§3 B1–B5).

**Do NOT execute until execution prereg is frozen.**

---

*Strategic context: the crack-β keystone is the highest-leverage test in the programme. A CONFIRM opens the deployment domain to pairs/cross-asset RV (the stated deployment target). A permanent demotion (all families fail the trilemma) collapses deployment to definitional calendars only — a strategic narrowing that requires honest acknowledgment. Either outcome re-prices the entire programme.*
