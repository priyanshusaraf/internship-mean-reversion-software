# Pre-Registration: RB-CL Alternative Split (Test A) + LE-GF Ex-COVID OOS (Test B)

**Document class:** Frozen AMR pre-registration — two registry-named reopen triggers.
**Written:** 2026-06-10. **Status:** FROZEN (Revision 1) — no redesign after this line.
**Motivation:** Unblocks the two-sleeve book (doc 45 INSUFFICIENT). Both tests are named explicitly
in HYPOTHESIS_REGISTRY.md (last updated 2026-06-06). Neither test is exploratory — both triggers
were pre-named at registration before this document was written.
**Results doc:** `48_rb_cl_alt_split_le_gf_subperiod_results.md` (written after all execution).
**Gate position:** `controlled-β admissibility → per-instrument positive expectancy → portfolio construction`
(strategic dependency graph; this is the cohort-breadth gate).

---

## REVISION 1 (2026-06-10) — Provenance Block

**Original freeze:** 2026-06-10 (same date, earlier draft).

**Adversarial audit returned INADMISSIBLE on both tests.** Four defects identified and adjudicated:

| # | Defect class | Location | Defect | Mitigation applied |
|---|---|---|---|---|
| 1 | CONSTRUCTION | §A.4, Part IV | CL1! leg substitution — RB-CL object (docs 39/40/44/45) is RB2!−CL2! throughout; CL1! was a false substitution | Leg corrected to CL2! everywhere; "consistent with docs 39-40" claim removed |
| 2 | METHODOLOGY | §A.3 | Vacuous excision premise — structural justification for alternative split rested on excision-window-placement; doc 40 line 29 records CL2! back-adj offset as negligible (zero negative barrel values), so no excision is warranted at all | Excision dropped from Test A primary; §A.3 rewritten on power-ground alone; excised-IS retained as optional descriptive robustness arm only |
| 3 | METHODOLOGY | §A.5 | Alpha undercount — three looks exist (doc-40 full-period p=0.015; doc-45 IS-only p=0.313 with its excised variant counted as one look's robustness arm; this look); Bonferroni requires α=0.05/3≈0.0167, not 0.05/2=0.025 | α corrected to 0.0167; INCONCLUSIVE band updated to [0.0167, 0.05); kill threshold updated |
| 4 | METHODOLOGY | §B.3 | PnL-derived window — COVID excision end-date 2021-12-31 was wider than programme-standard width; the COVID attribution itself arose from inspecting OOS PnL (docs 45/46); mandatory placebo control added | Window corrected to 2020-01-01→2021-06-30 (programme-standard, externally datable); selection-on-regime risk caveat added; placebo control (§B.6) made mandatory and binding |

**Change list (no silent rewrite):** (1) CL1!→CL2! in §A.4, §A.3 footnote, data-files block, Part IV; (2) §A.3 rewritten — power ground only, excision justification removed as primary; (3) §A.5 α 0.025→0.0167, pass/inconclusive/kill thresholds updated; (4) §A.10 kill threshold updated; (5) §A.11/§A.12 pass threshold updated; (6) §B.2 window end 2021-12-31→2021-06-30; (7) §B.3 window end + justification corrected + provenance caveat added; (8) §B.6 placebo-control section added (mandatory, pre-committed, dual-criterion pass); (9) §B.9 survive criteria updated to dual criterion; (10) §B.10 outcome table updated; (11) Part IV frozen params corrected throughout; (12) Combination gate §C.1 references corrected to 0.0167/dual-criterion.

**Registry provenance (Test A):** HYPOTHESIS_REGISTRY.md (2026-06-06) pre-named an illustrative split ("e.g. 1998-2023") on power grounds but did not freeze exact leg identity, exact IS_END date, or the excision; this prereg (Revision 1) is the freeze. The illustrative framing in the registry did not constitute a pre-commitment to CL1! or to the excision window.

---

## REVISION 2 (2026-06-10) — Delta-Audit Execution Mandates (binding, pre-data)

Delta audit verdict: **ADMISSIBLE-WITH-CAVEAT (both tests)**. The following reporting mandates are
binding on execution and on the results doc; failure to include any of them voids the verdict.

1. **Test A power evidence (blocking for a CONFIRMED verdict):** compute the power figure by
   simulation at the frozen IS length (true VR=0.898, N=500 surrogates, identical extraction), and
   report IS VR **with vs without the 2020-01-01→2021-06-30 bars** — the excised-IS robustness arm
   is hereby **MANDATORY** (elevated from optional), so a power gain driven by volatile-COVID-bar
   re-inclusion is visible. A CONFIRMED verdict whose significance vanishes in the excised-IS arm
   must be reported as CONFIRMED-WITH-COVID-DEPENDENCE-FLAG.
2. **Test B placebo symmetry:** apply the ≥30-trade filter symmetrically; report the placebo
   Sharpe distribution **both filtered and unfiltered**, plus the COVID-window excision trade
   count, so asymmetric culling is auditable.
3. **Test B effective-N:** report placebo specificity against **non-overlapping** 18-month windows
   as well as the monthly-step distribution; state effective N (~7). The 90th-percentile rank is a
   rank statistic over overlapping windows, not independent draws — caveat must appear in results.
4. **Verdict citation restriction:** the Test A verdict may cite ONLY p_rw(N=500, q=20, raw
   spread, frozen split). Any secondary read (other q, deseasonalized, robustness arm) appearing
   as supporting evidence in the verdict voids the alpha-spending guarantee.

---

> **Adversarial constraint acknowledged explicitly.** Test A is a SECOND look at RB-CL after the
> first split failed (doc 45 Gate A: IS VR p=0.313) and a THIRD look at the full-period result
> (doc 40: p=0.015). This is structurally Trap-7-adjacent (split shopping). The design must and
> does: (a) justify the alternative split on structural grounds fixed before any data touch;
> (b) pre-commit exact split dates with no tuning; (c) spend alpha via Bonferroni across all
> three looks (α=0.05/3≈0.0167); (d) name the kill: if this third look also fails, RB-CL moves
> DEFERRED→ARCHIVED permanently — no fourth look, ever.

---

## Part I — Test A: RB-CL IS Sub-Diffusion on Alternative Split

### §A.1 Gate Position

**Current status:** RB-CL = DEFERRED-OOS-SIGNAL (registry). Reopen trigger (pre-named
2026-06-06): "IS VR confirmed on alternative split (e.g. 1998-2023 IS, 2023-2026 OOS)."

**What this unlocks if it passes:** RB-CL IS VR confirmed → pre-register + run portfolio
combination test again (doc 45 reopen trigger, registry). Without this, the two-sleeve book
cannot be re-attempted because independence is already confirmed (ρ=0.013) but only one sleeve
(LE-GF) has confirmed IS VR.

### §A.2 Hypothesis

RB-CL (RBOB 2nd-month continuous vs WTI 2nd-month continuous, F6 β=1.0 after barrel
normalization) exhibits statistically significant sub-diffusion (VR(20) < RW null 5th percentile)
in the IS period defined by the alternative split (1998-08-03 to 2022-12-31), on the raw spread,
relative to surrogate nulls run through identical construction.

### §A.3 Structural Justification for Alternative Split

The original 70/30 chronological split was constructed in doc 44. Doc 45 Gate A yielded
p_rw=0.313 — IS sub-diffusion not confirmed.

The sole structural ground for the alternative split is **power.** This is the only ground; no
excision argument applies (see below).

**Power ground (pre-committed).** Doc 45 power analysis: ~30–40% power to detect true VR=0.898
in ~4,904 IS bars at α=0.05 (naive). Extended IS (1998-08-03 to 2022-12-31) yields approximately
6,100 bars, raising power to ~45–55% — a structural improvement, not optimization. This ground
is fixed before execution; the IS_END date below is frozen.

**No excision argument (REVISION 1 correction).** The prior draft (Revision 0) also cited the
CL2! back-adj contamination window (2020-03-01 to 2021-06-30) as a structural ground, arguing
that IS must extend past 2021-06-30 to make excision non-vacuous. That argument is removed.
Doc 40 line 29 records the CL2! back-adj offset for this period as negligible (zero negative
barrel values); no spread-level contamination is present. An excision window with negligible
real contamination is not a valid construction argument. Excision is therefore dropped from
the Test A primary.

**Optional descriptive robustness arm (no gate).** The runner MAY report IS VR(20) computed on
the spread with the 2020-03-01 to 2021-06-30 window removed, labeled clearly as
"excised-IS robustness arm — informational, not gating." This arm does NOT change the verdict
in any direction.

**Registry provenance.** The registry (2026-06-06) pre-named an illustrative IS range
("e.g. 1998-2023") on power grounds. It did not freeze exact IS_END date, leg identity, or
any excision window. This prereg (Revision 1) is the first and only freeze.

### §A.4 Construction

**Pair:** NYMEX_DL_RB2! (RBOB Gasoline 2nd-month) vs **NYMEX_DL_CL2!** (WTI Crude Oil
2nd-month). CL2! is the correct leg — the RB-CL object in docs 39, 40, 44, and 45 is
RB2!−CL2! throughout. CL1! is NOT used and was an error in the prior draft.

**β-mode:** F6 economic-anchor, β = 1.0 (FROZEN, barrel-equivalent normalization).

```
RB_barrel_t = RB2!_close_t × 42.0    [42 gallons/barrel — physical constant, not estimated]
CL_barrel_t = CL2!_close_t            [USD/barrel natively]
S_t = RB_barrel_t − 1.0 × CL_barrel_t    [crack margin at parity]
```

β is FIXED at 1.0 with zero updates. f_βupdate = 0.000 by construction (F6 is definitionally
admissible; no β-update-noise check needed beyond stating this). No Kalman, no rolling OLS,
no re-estimation of any kind.

**β-update-noise check (F6):** f_βupdate = Var((β_{t-1}−β_{t-2})·B_{t-1}) / Var(ΔS) = 0/Var(ΔS)
= 0.000. F6 is unconditionally admissible on the β-update-noise gate. No halt condition triggers.

**Data files (FROZEN):**
```
data/raw/more-mean-reversion-data/NYMEX_DL_RB2!, 1D.csv
data/raw/more-mean-reversion-data/NYMEX_DL_CL2!, 1D.csv
```

**Date range (FROZEN):**
```
DATE_MIN   = 1998-08-03    [first date both legs available — consistent with docs 39-40]
DATE_MAX   = 2026-06-03    [manifest-locked]
```

**IS / OOS split (FROZEN — alternative split):**
```
IS_END        = 2022-12-31    [last IS bar: the last trading day on or before 2022-12-31]
OOS_START     = 2023-01-01    [first OOS bar: first trading day on or after 2023-01-01]
```

Rationale: IS≈6,100 bars raises power from ~30–40% (doc-45 original IS) to ~45–55%.
OOS = 2023-01-01 to 2026-06-03 ≈ 3.5 years ≈ 850 trading days.

**No primary excision window.** The IS period is used in full (no bars removed). The optional
robustness arm (2020-03-01 to 2021-06-30 removed) is informational only — see §A.3.

**Roll-mask (FROZEN, per ADR_003):** jump threshold k=8.0 applied to RB2! and CL2! separately.
Window = 60 bars. Any bar where |close_t − close_{t-1}| > k × rolling_std(60) is masked (the
bar and 2 surrounding bars excluded). Roll-mask is applied before spread construction.

**Deseasonalization:** NONE applied for the primary VR gate. Raw spread is the gate. Deseasonalized
spread results reported as secondary (informational) only, consistent with gate0_le_gf_is_verify_prereg.md.

### §A.5 Primary Statistic

VR(20) = Var(20-bar spread returns) / (20 × Var(1-bar spread returns)), IS-only, one-sided lower
test (sub-diffusion: VR < 1).

p_rw = fraction of RW surrogate VR(20) values ≤ observed VR(20). PASS if p_rw < 0.0167.

**Alpha-spending rule (FROZEN — no wriggle, REVISION 1 corrected):** Three pre-named looks at
the same series:
1. Doc 40 full-period (already executed, p=0.015 — counts as one look);
2. Doc 45 IS-only (already executed, p=0.313 — FAILED; the excised-IS variant from that doc is
   counted as one robustness arm of look 2, not an independent look);
3. This test.

Bonferroni correction for three looks: α_per_test = 0.05 / 3 ≈ **0.0167**. This is the binding
threshold. The family-wise Type-I error rate across all three looks remains ≤ 0.05 if this
threshold is respected.

The doc-45 excised-IS variant is explicitly counted as look 2's robustness arm (not a separate
look) because it used the same IS period with a minor excision; it did not constitute an
independent sample or an independent pre-registration. This classification is stated here before
execution; it cannot be revised post-hoc.

If this test yields p_rw ∈ [0.0167, 0.05), it is NOT a pass — it is INCONCLUSIVE-LEANING-FAIL
(weakly directional, does not survive the spending rule). Report the actual p_rw; do not claim
"borderline pass." The kill still triggers: DEFERRED→ARCHIVED.

### §A.6 Null Families

All four null families below are conditioned on the full IS period (no excision in primary)
and run through **identical construction** (same barrel normalization, same roll-mask, same IS
date range). Surrogates are not pre-filtered; the identical pipeline applies to both real and
synthetic.

| Null | Construction | Conditioning | Role |
|---|---|---|---|
| **RW** | First-difference of IS spread resampled at matched (μ, σ); cumulative sum | IS mean + std of 1-bar spread changes | **Gating primary null** |
| **GARCH(1,1)** | GARCH(1,1) fit on IS first-differences; resimulated | Parameters fit on IS spread changes; resimulated path is a new GARCH trajectory | Mandatory for calendar/commodity tests |
| **MA(1)-noise** | MA(1) fit on IS first-differences; resimulated | MA(1) θ-hat from IS changes | Mandatory for calendar/commodity tests |
| **OU** | OU process fit on IS spread via MLE (κ, μ, σ_ou); resimulated | IS spread MLE; VR of OU at matched lag is the favorable null | Non-gating reference (consistent with prior prereg protocol) |

p_garch, p_ma1, p_ou reported in full; only p_rw is gating. Surrogates run through the
same VR(q) grid and the same IS window. No surrogate receives lookahead.

**N (FROZEN):**
```
N_SPEED = 200    [speed gate — kill at p_rw > 0.20 before full run]
N_FULL  = 500    [full test]
SEED_A  = 20260610
```

### §A.7 VR Grid and Multiplicity

VR is computed at q ∈ {2, 5, 10, 20, 40}. Primary statistic is VR(20) only (frozen, consistent
with entire programme since doc 21). All q results reported — never argmax. Secondary q values
are informational; they do not change the verdict.

No θ grid in Test A — this is a VR test, not an economic fade test. Fade economics are
reported secondarily (θ=1.0, cost=$0.20/bbl, consistent with sleeve_verification_prereg.md)
but do not gate the verdict.

### §A.8 OOS Hold-Out

OOS period: 2023-01-01 to 2026-06-03. OOS is held out entirely — NOT touched during Test A.

OOS statistics (VR(20), n_trades, mean_net at θ=1.0 and cost=$0.20/bbl) are reported as
secondary characterization after the IS gate is evaluated. OOS VR p_rw < 0.05 is a supporting
criterion only; OOS sign reversal (n_trades ≥ 30) is a kill criterion (see §A.10).

Minimum n_trades for OOS verdict to be binding: 30 trades. If OOS produces < 30 trades, OOS
outcome is INCONCLUSIVE (not a pass, not a kill on its own).

### §A.9 Cost Grid (FROZEN)

Primary cost: **$0.20/bbl** (defended realistic from sleeve_verification_prereg.md).
Cost grid reported at: $0.05, $0.10, $0.15, $0.20, $0.30, $0.40, $0.50, $0.80, $1.00/bbl.
Net expectancy = gross mean trade − cost. Report at each grid point; report breakeven cost
(where net = 0). Report at the standard programme thresholds 0.003 and 0.008 as fractional
equivalents (gross − cost for reference, though unit is $/bbl not fraction for this spread).

### §A.10 Kill Criteria (Ordered — Each Binding)

1. **Speed gate:** p_rw(N=200) > 0.20 → kill immediately. Do not run N=500.
2. **Jackknife drop:** jackknife VR(20) estimate drops > 300% vs full-sample IS VR(20) → kill (instability; result driven by a small subset of IS).
3. **f_βupdate ≥ 10%:** not applicable for F6 (f=0.000); stated for completeness per programme protocol.
4. **Third-look failure (permanent):** p_rw(N=500) ≥ 0.0167 → RB-CL moves DEFERRED→ARCHIVED. No fourth look, no alternative construction attempt, no θ-tuning rescue. This kill is permanent and unconditional. The INCONCLUSIVE band [0.0167, 0.05) also triggers this permanent kill — it is not a stay.
5. **OOS sign reversal:** if n_OOS_trades ≥ 30 AND OOS net mean trade < 0 at cost=$0.20/bbl → note as kill-signal for subsequent combination pre-registration (does not retroactively kill IS result but blocks portfolio combination).

### §A.11 Survive Criteria

Test A is a PASS iff ALL of the following hold:
- p_rw(N=500) < 0.0167 (primary gate; Bonferroni 3-look spending rule)
- p_garch < 0.10 (supporting — must not be a pure volatility-clustering artifact)
- IS mean_net > 0 at cost=$0.20/bbl (positive economic expectancy — sanity check)
- No speed-gate kill at N=200
- No jackknife instability kill

A PASS on Test A does NOT immediately re-open portfolio combination. It re-opens the
COMBINATION PRE-REGISTRATION gate (run a new doc-45-equivalent with this split as the IS).
The combination test must be newly pre-registered before execution.

A PASS on Test A that is accompanied by OOS sign reversal (if n_OOS_trades ≥ 30) is recorded
as PASS-WITH-OOS-CAUTION and blocks combination test until OOS characterization is explained.

### §A.12 Decision Tree — All Four Outcomes

| Outcome | p_rw result | Registry transition | Next action |
|---|---|---|---|
| **CONFIRMED** | p_rw < 0.0167 at N=500; supporting criteria met | DEFERRED-OOS-SIGNAL → IS-VR-CONFIRMED (conditional) | Pre-register + run combination test (doc 49 analogue) |
| **CONFIRMED-WITH-OOS-CAUTION** | p_rw < 0.0167; IS positive; OOS sign reversal (n≥30) | IS-VR-CONFIRMED with OOS caution flag | Combination pre-reg must explicitly address OOS caution before proceeding |
| **INCONCLUSIVE-SPENDING-RULE** | p_rw ∈ [0.0167, 0.05) | DEFERRED → ARCHIVED (permanent — the kill stands) | No fourth split. No further IS re-split. Combination blocked permanently. |
| **ARCHIVED** | p_rw ≥ 0.05 at N=500 OR speed-gate kill OR jackknife kill | DEFERRED → ARCHIVED (permanent) | No further RB-CL IS VR testing. Portfolio combination blocked permanently on RB-CL. Report §11.2: apparatus validated; RB-CL IS sub-diffusion not supported across three pre-named looks. |

---

## Part II — Test B: LE-GF Ex-COVID OOS Economics

### §B.1 Gate Position

**Current status:** LE-GF = §11.8 IS-ONLY CONFIRMED (registry, doc 46). IS Sharpe=0.939
(confirmed). OOS Sharpe=0.233 (doc 44/46), attributed to COVID-era livestock market disruption
(JBS plant closures 2020-04, feeder-to-live basis dislocation 2020–2021).
Reopen trigger (pre-named 2026-06-06): "sub-period OOS ex-COVID (2020-2021); if ex-COVID OOS
Sharpe > 0.50, re-evaluate standalone."

**What this unlocks if it passes:** LE-GF re-evaluated as potential standalone sleeve (not merely
IS-only confirmed). Combined with Test A CONFIRMED, opens the portfolio combination gate.

### §B.2 Hypothesis

LE-GF (CME Live Cattle 2nd-month vs CME Feeder Cattle 2nd-month, F5 β=0.565 frozen pre-sample)
delivers OOS Sharpe > 0.50 in the OOS sub-period excluding the COVID-era livestock disruption
window (2020-01-01 to 2021-06-30), AND the ex-COVID Sharpe lift is specific to the COVID window
(not generic to removing any 18-month block), at θ=1.0 and cost=$0.20¢/lb, using the IS/OOS
split from gate0_le_gf_is_verify_prereg.md (DATE_MIN=1995-01-01, OOS_SPLIT=0.70).

### §B.3 Construction

**Pair:** CME_DL_LE2! (Live Cattle 2nd-month) vs CME_DL_GF2! (Feeder Cattle 2nd-month).

**β-mode:** F5 (pre-sample OLS, first 25% of full merged LE2!-GF2! dataset, frozen; no
re-estimation thereafter). β = 0.565 (frozen from doc 44/sleeve_verification_prereg.md).
f_βupdate = 0.000 during IS and OOS (F5 frozen-β; no updates after pre-sample). Admissible
unconditionally under the β-update-noise gate.

**Data files (FROZEN):**
```
data/raw/more-mean-reversion-data/CME_DL_LE2!, 1D.csv
data/raw/more-mean-reversion-data/CME_DL_GF2!, 1D.csv
```

**IS / OOS split (FROZEN — inherited from gate0_le_gf_is_verify_prereg.md):**
```
DATE_MIN_LEGF = 1995-01-01
DATE_MAX      = 2026-06-03
OOS_SPLIT     = 0.70    [first 70% = IS; last 30% = OOS]
PRE_FRAC      = 0.25    [first 25% for β pre-sample; not part of IS for VR testing]
```

OOS period = last 30% of merged dataset after date alignment (approximately 2014-08 onward,
exact start date computed from dataset length at execution).

**Ex-COVID exclusion window (FROZEN, REVISION 1 corrected):**
```
EXCISE_COVID_START = 2020-01-01
EXCISE_COVID_END   = 2021-06-30    [inclusive — programme-standard 18-month width]
```

**Justification for window definition (pre-committed, revised):** COVID demand shock for Live
and Feeder Cattle is externally datable: onset March–April 2020 (JBS USA and Tyson plant
closures, USDA Emergency Order); feeder-to-live basis disruption and reduced feedlot capacity
persisted through the JBS cyberattack (May–June 2021) and associated supply-chain
disintermediation. EXCISE_COVID_END = 2021-06-30 aligns with the JBS cyberattack resolution
and matches the programme-standard 18-month excision width used in doc 45.

**REVISION 1 correction from prior draft:** The prior draft used EXCISE_COVID_END = 2021-12-31
(24-month window). That wider end-date was not independently justified before data inspection —
the COVID attribution itself arose from inspecting OOS PnL patterns in docs 45/46. The wider
window therefore carried selection-on-regime residual risk. The window is corrected here to the
programme-standard 18-month width (through 2021-06-30) aligned to the externally datable
JBS cyberattack endpoint.

**Selection-on-regime caveat (honest, pre-committed).** The COVID window was identified by
observing OOS PnL underperformance in docs 45/46 and attributing it to the COVID disruption.
This carries residual selection risk: the excision that lifts OOS Sharpe most was partly
motivated by observed results. The mandatory placebo control in §B.6 is the direct mitigation:
the Sharpe lift must be *specific* to this window, not generic to removing any 18 months. This
caveat is stated before execution and cannot be removed post-hoc.

**Roll-mask:** k=8.0, W=60, consistent with ADR_003 and all prior programme protocol.

**Deseasonalization:** NONE for primary statistic. Consistent with Gate 0 gate0_le_gf_is_verify_prereg.md.

### §B.4 Primary Statistic

**Dual-criterion pass (REVISION 1 — both criteria must hold):**

Criterion 1 — OOS Sharpe threshold:
```
Sharpe_ex_covid = (mean_net_trade_ex_covid / std_net_trade_ex_covid) × sqrt(trades_per_year_ex_covid)
```
Where net_trade = gross_trade − cost = realized fade gross PnL per entry/exit cycle − $0.20¢/lb.
θ = 1.0 (entry threshold: |z| ≥ 1.0; exit at z = 0). LB = 60 (lookback for z-score mean/std).
MH = 40 (max holding bars). All frozen from gate0_le_gf_is_verify_prereg.md.

Criterion 1 pass: Sharpe_ex_covid > **0.50** (registry pre-named exactly this threshold).

Criterion 2 — COVID-window specificity (placebo control):
The Sharpe lift must be specific to the COVID window, not generic. Criterion 2 pass: the
COVID-window excision Sharpe ≥ 90th percentile of the placebo-excision Sharpe distribution
(see §B.6 for full definition).

**Test B passes iff BOTH Criterion 1 AND Criterion 2 are satisfied.**

### §B.5 Null Families for Test B

Test B is an economic (Sharpe) test on a realized OOS sub-period. The VR IS gate already passed
(doc 46 p_rw=0.024). This test asks: is the OOS underperformance explained by COVID mechanism?

**Surrogate test:** Run the same fade strategy on N=500 matched-OU surrogates on the OOS
sub-period (ex-COVID bars only), seeded at SEED_B. Report the fraction of OU surrogates with
ex-COVID OOS Sharpe > observed. This provides a reference distribution for whether the Sharpe
observed ex-COVID is genuine or chance.

**RW null:** Also report fraction of RW surrogates (same OOS ex-COVID window, matched σ) with
Sharpe > observed.

p_ou_excovidOOS and p_rw_excovidOOS are informational (OU null = favorable; non-gating per
prior protocol). Primary gate is the pre-committed dual criterion.

**Null for mechanism claim:** Report full-OOS Sharpe (0.233 from doc 44) and ex-COVID OOS
Sharpe side-by-side. The delta (Sharpe_ex_covid − Sharpe_full_oos) is the mechanism test
— a large positive delta supports the COVID-disruption explanation. No formal threshold
on the delta; it is reported for adversarial review.

**N (FROZEN):**
```
N_SURR_B  = 500
SEED_B    = 20260610
```

### §B.6 Placebo Control (MANDATORY — pre-committed, binding)

**Purpose:** The COVID window was identified partly by observing OOS PnL. The placebo control
tests whether the Sharpe lift is specific to the COVID window or generic to removing any 18-month
block in the OOS period.

**Construction (FROZEN before execution):**
1. Define the full OOS period (approximately 2014-08 onward through 2026-06-03).
2. Enumerate every contiguous 18-month window within the OOS period, stepping by 1 calendar month.
   Each placebo window spans exactly 18 months (EXCISE_PLACEBO_START to EXCISE_PLACEBO_START + 18m).
3. For each placebo window, compute OOS Sharpe under excision of that window (same fade strategy,
   same θ=1.0, same cost, same min-trades filter applied).
4. Collect the full distribution of placebo-excision Sharpe values (one per window).
5. Compute the 90th percentile of this distribution.

**Dual-criterion pass rule (both required):**
- Criterion 1: Sharpe_ex_covid > 0.50.
- Criterion 2: Sharpe_ex_covid ≥ 90th percentile of the placebo-excision Sharpe distribution
  (the COVID-window excision must be in the top decile of all 18-month excisions).

**Fail on Criterion 2:** LE-GF ex-COVID lift is generic (removing any 18-month block produces
similar improvement); the COVID-mechanism claim is not supported. Registry stays as §11.8
IS-ONLY CONFIRMED; standalone re-evaluation NOT supported.

**Fail on Criterion 1 only:** As before — OOS weakness structural.

**This is NOT an archive trigger for Test B.** Either failure on Test B leaves LE-GF at
§11.8 IS-ONLY CONFIRMED (IS result unchanged); it simply does not re-open standalone or
combination. The registry designation is preserved.

**Minimum-trades filter for placebo windows:** apply the same n_OOS_ex_window ≥ 30 filter
within each placebo excision. If a placebo window removes enough OOS bars to yield < 30
trades in the remaining OOS, exclude that placebo window from the distribution (do not count
it as a zero-Sharpe entry; simply drop it). Report how many windows were excluded.

**Report:** Full placebo-excision Sharpe distribution (histogram or percentile table),
90th percentile value, COVID-window excision Sharpe rank within the distribution, and pass/fail
on Criterion 2.

### §B.7 Multiplicity (Test B)

Test B primary statistic (Criterion 1) has no multiplicity problem — single pre-named sub-period,
single pre-named threshold. The placebo control (Criterion 2) is a pre-committed specificity check,
not a search; the 90th-percentile threshold is frozen here before execution.

Full-OOS metrics (inclusive of COVID) are also reported for transparency and adversarial audit.

### §B.8 Cost Grid (FROZEN, consistent with programme)

Primary cost: **$0.20¢/lb** (frozen from sleeve_verification_prereg.md).
Cost grid: 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50¢/lb — all reported.
Net positive at cost=0.005 (programme standard): reported as a fractional check alongside the
$/unit primary.

### §B.9 Kill Criteria (Test B)

1. **n_OOS_ex_covid < 30 trades:** verdict is INCONCLUSIVE regardless of Sharpe or placebo
   result (insufficient trades for binding verdict). Note explicitly; do not claim a pass.
2. **Sharpe_ex_covid ≤ 0.50 (Criterion 1 fail):** FAIL — COVID explanation is insufficient;
   LE-GF OOS weakness is structural, not COVID-specific. Registry: §11.8 IS-ONLY CONFIRMED
   remains but standalone re-evaluation is NOT supported. Combination gate blocked.
3. **Criterion 2 fail (placebo specificity fail):** FAIL — Sharpe lift is generic, not
   COVID-specific. Same consequence as above: standalone and combination gate remain blocked.
4. **Sharpe_ex_covid ∈ (0.50, 0.60) with Criterion 2 passing:** MARGINAL PASS — satisfies
   both criteria; noted as weak positive; re-evaluation authorized but combination
   pre-registration must flag the marginal OOS base.
5. **Mean_net_ex_covid < 0 at cost=$0.20¢/lb:** FAILED economic test regardless of Sharpe
   (negative net expectancy; not deployable under any Sharpe framing).

### §B.10 Survive Criteria

Test B is a PASS iff:
- n_OOS_ex_covid ≥ 30 trades
- Sharpe_ex_covid > 0.50 (Criterion 1)
- COVID-window excision Sharpe ≥ 90th percentile of placebo-excision distribution (Criterion 2)
- mean_net_ex_covid > 0 at cost=$0.20¢/lb

A PASS re-opens LE-GF for "standalone re-evaluation" per the registry trigger. It does NOT
automatically declare LE-GF a CONFIRMED-STANDALONE-SLEEVE — that designation requires a
new pre-registration addressing the ex-COVID characterization and the mechanism question.

### §B.11 Decision Tree — All Outcomes

| Outcome | Result | Registry transition | Next action |
|---|---|---|---|
| **COVID-MECHANISM-CONFIRMED** | Criterion 1 AND 2 pass; n≥30; net>0 | §11.8 IS-ONLY CONFIRMED → CONDITIONAL-OOS-VIABLE (ex-COVID) | New standalone pre-registration; if Test A also CONFIRMED, open combination pre-registration |
| **MARGINAL-COVID-CONFIRMED** | Both criteria pass; Sharpe_ex_covid ∈ (0.50, 0.60); n≥30; net>0 | Remains §11.8 IS-ONLY CONFIRMED; weak OOS viability noted | Combination pre-registration may proceed with explicit OOS-marginal flag |
| **SPECIFICITY-FAIL** | Criterion 1 passes but Criterion 2 fails (lift is generic) | Remains §11.8 IS-ONLY CONFIRMED; COVID mechanism not confirmed as specific | Combination gate blocked. Standalone economics not supported. |
| **OOS-STRUCTURAL-WEAKNESS** | Criterion 1 fails (Sharpe_ex_covid ≤ 0.50) | Remains §11.8 IS-ONLY CONFIRMED; OOS weakness structural | Combination gate blocked. LE-GF IS anchor only. |
| **INCONCLUSIVE** | n_OOS_ex_covid < 30 trades | No registry change; verdict deferred | Report n; note data-limitation. Do not claim pass or fail. |

---

## Part III — Cross-Test Combination Gate

### §C.1 Requirement for Portfolio Combination Re-Open

The combination pre-registration (doc 45 analogue) may be opened ONLY IF:
- Test A = CONFIRMED (p_rw < **0.0167**, IS VR gate passed)
- Test B = COVID-MECHANISM-CONFIRMED or MARGINAL-COVID-CONFIRMED (Sharpe_ex_covid > 0.50
  AND Criterion 2 placebo specificity passes)
- Independence remains confirmed (ρ=0.013, from doc 45 Gate B — already locked, no re-test needed)

Test A CONFIRMED + Test B FAIL (either criterion) → combination gate BLOCKED. LE-GF IS anchor
holds but the book has only one sleeve with bilateral (IS+OOS) economics.

Test A ARCHIVED + Test B pass → combination gate BLOCKED (only one sleeve).

Test A CONFIRMED + Test B INCONCLUSIVE → combination gate BLOCKED pending additional OOS
accumulation (more bars needed).

Either test reaching ARCHIVED/FAIL + the other FAIL → programme is at single-sleeve LE-GF
IS-anchor status only. Tier-1 two-sleeve book is DEFERRED until a new instrument with IS VR
confirmation is identified.

### §C.2 New Combination Pre-Registration (if unlocked)

A new portfolio combination document (doc 49 equivalent) must be written and frozen BEFORE
any combination execution. It must:
- Use the alternative split IS/OOS dates from Test A (IS_END=2022-12-31)
- Align LE-GF split to match Test A's OOS start (2023-01-01) for portfolio comparability
- Apply the ex-COVID characterization as a robustness sub-report
- Re-run Gates A through D from portfolio_combination_prereg.md with new numbers
- Explicitly address the alpha-spending history (Test A was the third RB-CL look across three
  pre-named contexts: doc 40 full-period, doc 45 IS-only, this test)

---

## Part IV — Frozen Parameters (Complete Registry)

```python
# ─── TEST A: RB-CL ALTERNATIVE SPLIT ───────────────────────────────────────
SEED_A             = 20260610
DATE_MIN_RBCL      = "1998-08-03"
DATE_MAX           = "2026-06-03"
IS_END_ALT         = "2022-12-31"    # IS cutoff — alternative split (power ground only; §A.3)
OOS_START_ALT      = "2023-01-01"    # OOS start
# NO primary excision window — CL2! back-adj offset is negligible per doc 40 line 29
# OPTIONAL robustness arm only (informational, not gating):
EXCISE_ROBUSTNESS_START  = "2020-03-01"    # not applied to primary; robustness arm only
EXCISE_ROBUSTNESS_END    = "2021-06-30"    # not applied to primary; robustness arm only
CL_LEG             = "CL2!"          # FROZEN — CL2! (2nd-month WTI); NOT CL1!
BETA_RBCL          = 1.0             # F6 economic anchor; FROZEN; zero updates
NORM_RB_FACTOR     = 42.0            # gallons-per-barrel (physical constant)
JUMP_K             = 8.0
JUMP_W             = 60
N_SPEED_A          = 200
N_FULL_A           = 500
VR_Q_PRIMARY       = 20
VR_Q_GRID          = [2, 5, 10, 20, 40]
PASS_P_RW_A        = 0.0167          # Bonferroni 3-look spending rule: 0.05/3; NOT 0.025
INCONCLUSIVE_BAND_A = (0.0167, 0.05) # still triggers ARCHIVED — not a stay
JACKKNIFE_KILL     = 3.00            # 300% drop → kill
THETA_A            = 1.0             # fade entry z-score (secondary economic report only)
COST_RBCL          = 0.20            # $/bbl defended cost
COST_GRID_RBCL     = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.80, 1.00]  # $/bbl

# ─── TEST B: LE-GF EX-COVID OOS ─────────────────────────────────────────────
SEED_B             = 20260610
DATE_MIN_LEGF      = "1995-01-01"
DATE_MAX           = "2026-06-03"
OOS_SPLIT_LEGF     = 0.70
PRE_FRAC_LEGF      = 0.25            # pre-sample for F5 β; β frozen at 0.565 from doc 44
BETA_LEGF          = 0.565           # F5 frozen — no re-estimation
EXCISE_COVID_START = "2020-01-01"    # ex-COVID OOS window start (externally datable: COVID onset)
EXCISE_COVID_END   = "2021-06-30"    # ex-COVID OOS window end — programme-standard 18m width;
                                     # JBS cyberattack resolution endpoint; NOT 2021-12-31
JUMP_K             = 8.0
JUMP_W             = 60
LB                 = 60
MH                 = 40
THETA_B            = 1.0
COST_LEGF          = 0.20            # ¢/lb defended cost
COST_GRID_LEGF     = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]   # ¢/lb
N_SURR_B           = 500
PASS_SHARPE_B      = 0.50            # registry-named threshold; not tunable (Criterion 1)
MIN_TRADES_OOS_B   = 30              # below this → INCONCLUSIVE, not FAIL

# Placebo control (§B.6) — mandatory
PLACEBO_WINDOW_LEN_MONTHS = 18       # match EXCISE_COVID window length exactly
PLACEBO_STEP_MONTHS       = 1        # monthly step through OOS period
PLACEBO_SPECIFICITY_PCT   = 90       # Criterion 2: COVID excision must be ≥ 90th pctile
PLACEBO_MIN_TRADES        = 30       # placebo windows yielding < 30 remaining OOS trades
                                     # are excluded from the distribution (not counted as 0)
```

---

## Part V — Non-Goals

This pre-registration does NOT authorize:

- Any θ grid search on IS or OOS for either test (θ=1.0 is frozen)
- Any β re-estimation or family switching for either instrument
- Any change to roll-mask parameters
- Any new pair testing or instrument addition
- Portfolio construction execution (requires separate pre-registration)
- Deseasonalized VR as a gating criterion for Test A (informational only)
- EIA conditioning or regime conditioning of any kind
- Extending the ex-COVID window beyond 2021-06-30 or shrinking it post-hoc
- A fourth IS look for RB-CL if Test A is archived
- Dynamic sizing models, execution infrastructure, deployment code
- Using CL1! for the RB-CL spread construction (CL2! is the only admissible leg)

---

## Part VI — Sequential Execution Protocol

1. Run Test A at N=200 speed gate. If p_rw > 0.20, kill and proceed directly to Test B.
2. If speed gate survives, run Test A at N=500. Record verdict per §A.10/§A.12.
3. Run Test B (independent of Test A outcome — Test B result is needed regardless).
4. Run placebo control (§B.6) as part of Test B execution. Record Criterion 2 verdict.
5. Evaluate combination gate per §C.1 (corrected thresholds: p<0.0167; dual criterion).
6. Write doc 48 with all results. Update HYPOTHESIS_REGISTRY.md and PROJECT_STATE.md.
7. If combination gate opens: write combination pre-registration (doc 49) BEFORE any execution.
8. Hard stop after doc 48 is written and registry updated.

Tests A and B may be run in parallel (they use different instruments and different splits).
Results should be recorded independently before combining into the combination-gate evaluation.

---

*Pre-registration frozen (Revision 1): 2026-06-10. No parameters, thresholds, split dates,
excision windows, or placebo control rules may be changed after this line. Results doc:
48_rb_cl_alt_split_le_gf_subperiod_results.md*
