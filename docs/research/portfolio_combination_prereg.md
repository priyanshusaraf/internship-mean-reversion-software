# Portfolio Combination Pre-Registration

**Written:** 2026-06-06 (BEFORE any execution — this is the frozen pre-commitment).
**Candidates:** RB-CL (F6, β=1.0, CONDITIONAL-CANDIDATE) + LE-GF (F5, β=0.565, MERELY-TRUE).
**Purpose:** Test whether combining two positive-expectancy sleeves produces a book that clears an
institutional bar. Hard stop after book verdict.
**Doc reference:** Builds on doc 43 (economic eval), doc 44 (sleeve verification), doc 25 (portfolio
expectancy arithmetic).

---

## 0. Expectancy Arithmetic (Binding — No Wriggle)

From doc 25: `E[Σ wᵢ(gᵢ − cᵢ)] = Σ wᵢ·E[gᵢ − cᵢ]`. Correlation-free.

**BOTH sleeves are already positive-expectancy.** RB-CL OOS net = +$0.598/bbl; LE-GF OOS net =
+$0.215¢/lb (COVID-affected). This is NOT the doc-25 scenario (sub-cost cohort). Therefore:

- Diversification CANNOT create expectancy that does not exist. It can ONLY move variance/Sharpe.
- The portfolio test is: do two positive-expectancy, possibly uncorrelated sleeves combine to produce
  a book whose risk-adjusted returns and drawdown profile clear a pre-committed institutional bar?
- No claim will be made that diversification "created" edge. Edge is already present; combination
  tests whether the book is holdable and the drawdown is survivable.

---

## 1. Gates (Pre-Committed Order — No Reordering After Execution)

```
Gate A → Gate B → Gate C → Gate D (synthesis)
```

Results from any gate do NOT change the pass/fail thresholds of subsequent gates.

---

## 2. Gate A — RB-CL Excision Robustness

**Rationale:** CL2! back-adj from April 2020 WTI event inflated ~2-3 RB-CL trades. If excising
the contamination window materially kills the edge, RB-CL is a crisis artifact and must not enter
the book.

**Protocol:**
- Excise period: 2020-03-01 to 2021-06-30 (inclusive) from IS period only.
- Re-run VR(20) and economic fade (θ=1.0, cost=$0.20/bbl) on the excised dataset.
- IS is the first 70% of the EXCISED dataset. OOS is unchanged (last 30% of full dataset).

**Pre-committed pass criteria (cannot change after execution):**

| Criterion | PASS | FAIL |
|---|---|---|
| Excised IS VR(20) p_rw | < 0.050 | ≥ 0.050 |
| Excised IS net per trade | > 0 $/bbl | ≤ 0 $/bbl |
| OOS net per trade (unchanged) | > 0 $/bbl | ≤ 0 $/bbl |

**Verdict logic:**
- ALL THREE pass → RB-CL enters book as SLEEVE-GRADE component (still low-Sharpe; excision passing
  does NOT upgrade it to CONFIRMED-STANDALONE-SLEEVE). Upgrade to CONFIRMED-SLEEVE requires the
  excised IS VR p_rw < 0.010 (original CONDITIONAL-CANDIDATE trigger).
- ANY fail → RB-CL is dropped from the combined book. Report this honestly. If dropped, the book
  is LE-GF only — report as SINGLE-SLEEVE (not a portfolio test; hard stop).

---

## 3. Gate B — Independence Test

**Rationale:** "Energy vs livestock = independent" must be shown, not assumed. Full-sample
correlation is insufficient — tail co-movement in stress windows is the decisive test.

**Protocol:**
- Spread return series: daily first-difference of RB-CL spread levels (masked for rolls and
  CL2! negative prices); daily first-difference of LE-GF spread levels (masked for rolls).
- Align on common dates. Drop NaN.
- Full-sample Pearson correlation of aligned return series.
- Stress windows (pre-committed, not data-driven):
  - COVID window: 2020-01-01 to 2020-12-31
  - Energy spike: 2022-01-01 to 2022-12-31
  - Combined stress: union of the two
- For each stress window: report mean return, max drawdown in that window for each sleeve
  independently, and simultaneous loss days (both sleeves negative on same day).

**Pre-committed independence thresholds:**

| Criterion | INDEPENDENT | CORRELATED (risk to book) |
|---|---|---|
| Full-sample Pearson ρ | |ρ| < 0.30 | |ρ| ≥ 0.30 |
| COVID simultaneous loss pct | < 60% of COVID days | ≥ 60% |
| 2022 simultaneous loss pct | < 60% | ≥ 60% |

**Note:** An INDEPENDENT verdict does not guarantee good book economics — it only means the
variance-reduction arithmetic applies. Gate C computes the actual book metrics.

A CORRELATED verdict does NOT kill the book — it means the diversification benefit is limited and
must be explicitly quantified (not assumed). The book can still be SMALL-BOOK-ONLY on capacity.

---

## 4. Gate C — Combined Book Metrics

**Book construction:**
- Sizing: inverse-volatility (σ_RB-CL, σ_LE-GF computed on IS return series). Each sleeve's weight
  is inversely proportional to its own spread return volatility.
- Capacity constraint: each sleeve capped at its pre-established capacity:
  - RB-CL: cap at $2M/yr (conservative; prevents RB-CL from dominating due to its higher liquidity)
  - LE-GF: cap at $350k/yr (realistic 1-2% GF ADV)
  - Combined capacity: ~$2.35M/yr
  - Rationale for RB-CL cap at $2M: prevents a lopsided "book" that is 98% RB-CL and 2% LE-GF
    (which would show trivially the same results as RB-CL alone). Equal-order-of-magnitude sizing
    is required to actually test diversification.
- IS split: first 70% of full data (matching sleeve verification protocol). OOS: last 30%.
- Roll masks applied. No crisis excision in the combined book (crisis years are EXAMINED in Gate B;
  excised separately only for robustness; the verdict rests on pooled OOS).

**Metrics reported (ALL pre-committed — no post-hoc dropping):**
1. Combined IS Sharpe (annualized)
2. Combined OOS Sharpe (annualized)
3. Combined IS net per year ($ absolute)
4. Combined OOS net per year ($ absolute)
5. Combined max drawdown (IS, in $ units)
6. Combined max drawdown (OOS, in $ units)
7. Diversification benefit: combined OOS Sharpe minus best single-sleeve OOS Sharpe
8. Crisis-year breakdown: 2020 and 2022 combined net (separately)
9. Combined capacity: dollar amount per year at the capped sizing

**Pre-committed verdict thresholds:**

| Metric | DEPLOYABLE-BOOK | SMALL-BOOK-ONLY | INSUFFICIENT |
|---|---|---|---|
| Combined OOS Sharpe | ≥ 0.60 | 0.40 – 0.60 | < 0.40 |
| Combined OOS net | Positive | Positive | ≤ 0 |
| Diversification benefit (OOS Sharpe delta) | > +0.08 vs best single | 0 to +0.08 | Negative (book worse) |
| Combined max drawdown (OOS) | Survivable: < 50% of annualized gross | — | > 50% |

**Combined capacity verdict:**
- Combined capacity at pre-committed sizing ≈ $2.35M/yr
- Report actual capacity in the results.
- DEPLOYABLE-BOOK requires capacity ≥ $1M/yr AND combined OOS Sharpe ≥ 0.60.
- SMALL-BOOK-ONLY: capacity $200k–$1M/yr OR Sharpe 0.40–0.60.
- INSUFFICIENT: capacity < $200k or Sharpe < 0.40 or OOS net ≤ 0.

**Robustness sub-reports (required but do not change primary verdict):**
- Report ex-COVID book metrics (excluding 2020-01 to 2021-06).
- Report ex-energy-spike (excluding 2022-01 to 2022-12-31).
- If ex-crisis metrics are materially better than full OOS → note the mechanism dependency.

---

## 5. Gate D — Adversarial Synthesis

Three named adversarial agents run AFTER Gate C results are in hand. Each receives the full Gate
A/B/C numerical results. Synthesis: one verdict from the taxonomy below.

**Attack vectors assigned (pre-committed):**

**Adversarial agent (kill-ledger):**
- Does RB-CL excision reveal an artifact? Is the excision threshold selection (2020-03 to 2021-06)
  manipulated to maximize the result?
- Is the $2M RB-CL cap chosen to make the book look good? What if RB-CL cap = $350k (matching LE-GF)?
- Hidden tail correlation: does the energy-vs-livestock independence assumption break in 2020?
- Back-adj residual in LE-GF: is the 14 ¢/lb persistent spread mean partly from back-adj (LE2! or
  GF2! may have seasonal back-adj effects not captured by the splice diagnostic)?
- Diversification benefit arithmetic: is the combined Sharpe improvement genuine or a sizing artifact?

**Statistical lens:**
- Is the cross-sleeve correlation measured on sufficient bars to be reliable?
- Is simultaneous loss pct (Gate B) statistically distinguishable from independent-by-chance?
- Is the combined OOS period long enough (number of independent observations) to support the Sharpe
  estimate? Report effective degrees of freedom.

**Trader/PM lens:**
- Can an institutional desk run both simultaneously? LE-GF (feeder cattle) and RB-CL (crack spread)
  require separate desks (energy vs livestock). This is a real operational consideration.
- At $2.35M/yr combined capacity, is this worth two-desk overhead? Minimum fundable threshold
  is typically $10-20M/yr for an institutional book.
- Does the combined drawdown path (IS+OOS) look survivable under 12-18 month horizon with quarterly
  risk reviews? Report MDD as months-of-expected-return.

---

## 6. Pre-Committed Verdict Taxonomy

| Verdict | Meaning |
|---|---|
| **DEPLOYABLE-BOOK** | Combined OOS Sharpe ≥ 0.60, OOS net positive, capacity ≥ $1M/yr, no fatal adversarial flaw |
| **SMALL-BOOK-ONLY** | Book clears but capacity or Sharpe below institutional threshold; independently verifiable edge |
| **INSUFFICIENT** | Combination does NOT clear bar — apparatus is validated, edges are real, but no institutional product exists from this combination. A legitimate Tier-1 answer. |

**The INSUFFICIENT verdict is NOT a failure of the programme.** It means: real edges confirmed,
no deployable combination exists with these two sleeves at these capacity constraints. Next step:
either find higher-capacity sleeves or accept LE-GF as a sub-institutional sleeve.

---

## 7. §11.8 Re-Anchor (Pre-Committed)

Per user instruction: re-anchor §11.8 positive control to LE-GF (strongest raw signal p=0.005,
cleanest data, zero negative prices in both legs) INSTEAD OF RB-CL (which has the CL2! April 2020
contamination, and is CONDITIONAL-CANDIDATE not confirmed).

This update does NOT change any gate verdicts. It is a housekeeping correction to the programme's
positive control anchor.

---

## 8. Frozen Parameters

```python
SEED_PORTFOLIO = 20260607
OOS_SPLIT     = 0.70           # consistent with sleeve verification
EXCISE_START  = "2020-03-01"   # RB-CL back-adj contamination window start
EXCISE_END    = "2021-06-30"   # RB-CL back-adj contamination window end
PRIMARY_THETA = 1.0            # consistent with sleeve verification
COST_RBCL     = 0.20           # $/bbl, defended cost from sleeve verification
COST_LEGF     = 0.20           # ¢/lb, defended cost from sleeve verification
CAP_RBCL_YR   = 2_000_000     # $2M/yr RB-CL cap (equal-order-of-magnitude sizing)
CAP_LEGF_YR   = 350_000       # $350k/yr LE-GF cap (1% ADV realistic)
STRESS_COVID  = ("2020-01-01", "2020-12-31")
STRESS_ENERGY = ("2022-01-01", "2022-12-31")
```

---

## 9. Hard Stop Instruction

After Gate D synthesis: write results doc (45), update HYPOTHESIS_REGISTRY + PROJECT_STATE +
continuation records. Then STOP.

Do NOT begin:
- New pair testing
- Execution infrastructure
- Deployment planning
- Dynamic sizing models
- Signal engineering

If the verdict is DEPLOYABLE-BOOK or SMALL-BOOK-ONLY: the registry says "book verdict confirmed —
next step is deployment sizing pre-registration (separate run)." If INSUFFICIENT: "apparatus
validated, real edges confirmed, no institutional book from this pair — next step is higher-capacity
sleeve search."
