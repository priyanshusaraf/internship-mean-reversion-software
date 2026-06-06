# Sleeve Verification Pre-Registration
# "Candidate → Confirmed" Gauntlet: RB-CL and LE-GF

**Pre-registered:** 2026-06-06 — FROZEN BEFORE ANY GATE-0 EXECUTION.
**Purpose:** Convert C_GENUINE_ECONOMIC candidates (docs 40, 42, 43) into formally confirmed sleeves
or kill them. Criteria below are binding and unmodifiable after this write.
**Execution doc:** 44_sleeve_verification_results.md (written after all gates complete).

---

## Background

RB-CL (doc 40 + 43: F6, β=1.0, p_rw=0.006, C_GENUINE_ECONOMIC) and LE-GF (doc 42 + 43: F5, β=0.565,
p_rw=0.002, C_GENUINE_ECONOMIC) were declared candidates during an un-pre-registered search spanning
docs 39-43. Before these candidates earn the designation "confirmed sleeve," the following concerns
must be resolved:

1. **Deseasonalization contamination** (doc 38a): deseason on back-adj spreads with large persistent
   level offsets manufactures MR. Must confirm raw VR signal exists independently.
2. **Multiplicity**: full search space was never enumerated or corrected. p=0.006 and p=0.002 may not
   survive correction.
3. **§11.8 anchor**: HO-CL (the stated positive control) is A_FALSE_RESCUE. The apparatus positive
   control needs re-anchoring.
4. **Book metrics missing**: no Sharpe, no max drawdown, no capacity, no breakeven curve. Per-trade
   net ≠ book economics.
5. **θ-gradient not surrogate-tested**: LE-GF's escalating gradient with θ needs surrogate validation.
6. **No adversarial review**: both verdicts came from a single research thread.

A candidate earns CONFIRMED-SLEEVE only if it passes ALL of gates 0-4.

---

## Gate 0 — Raw vs Deseason (Primary Contamination Gate)

**Test:** Re-run VR(q) framework (evaluate_v2 level) on the UNDESEASONALIZED spread for both RB-CL
and LE-GF. Also run the doc-38a splice diagnostic on each individual leg (RB, LE, GF; CL already graded).

**Pre-registered pass criteria:**

| Label | Condition | Action |
|---|---|---|
| CLEAN | raw VR(20) p_rw < 0.05 (surrogate-relative, N=200 RW null) | pass Gate 0 |
| MARGINAL-CLEAN | raw p_rw ∈ [0.05, 0.12) AND deseason amplification < 2.5× AND |raw_mean|/spread_std < 0.5 | pass with CAVEAT note |
| SUSPECT | raw p_rw ∈ [0.05, 0.12) AND (amplification ≥ 2.5× OR |raw_mean|/spread_std ≥ 0.5) | flag; adversarial weight doubles |
| CONTAMINATED | raw p_rw ≥ 0.12 AND deseason amplification ≥ 2.5× | KILLED — same signature as BRN/ZC |

**Splice diagnostic criteria (per leg):**

| Grade | Condition |
|---|---|
| CLEAN | |raw_leg_level_offset_estimate| < 0.3 × leg_std |
| SUSPECT | 0.3 ≤ offset/std < 0.7 |
| CONTAMINATED | offset/std ≥ 0.7 AND confirmed via negative-price count > 2% |

Metric: number of negative close prices in back-adj leg (physical energy/livestock prices cannot be
negative; negative values = back-adj artifact accumulation). This is the same test that identified
HO-CL contamination (3291/7003 negative values).

---

## Gate 1 — §11.8 Re-anchor

**Not a computational gate.** The positive control (§11.8) is currently documented as HO-CL
(Pindyck-Rotemberg 1990). HO-CL is now A_FALSE_RESCUE. If RB-CL passes Gate 0, it becomes
the primary §11.8 anchor (same literature, cleaner data). Update HYPOTHESIS_REGISTRY accordingly.

**Pre-registered criteria:** If RB-CL passes Gate 0, re-anchor §11.8 to RB-CL. If RB-CL fails
Gate 0, §11.8 is UNCONFIRMED and ALL downstream confidence levels must be downgraded.

---

## Gate 2 — Multiplicity Correction

**Enumeration:** List ALL pairs × β-families × θ values tested in docs 39-43.

**Pre-registered correction method:** Benjamini-Hochberg (FDR) at q=0.10, applied to all reported
p-values at θ=1.0 (primary threshold). Additionally report Bonferroni-corrected threshold for
conservative reference.

**Pre-registered pass criteria:**

- CONFIRMED: p-value survives BH(q=0.10) corrected threshold
- MARGINAL: p-value fails BH but survives Bonferroni/2 (i.e. strong raw p but borderline after
  correction) → case rests on OOS-stronger + economic anchor, report honestly
- FAILS CORRECTION: p-value fails Bonferroni threshold → demote to MERELY-TRUE pending stronger replication

RB-CL p=0.006 is expected to be borderline — report its corrected standing exactly as computed.

---

## Gate 3 — Full Book & Breakeven Metrics

**New metrics required (extend run_crack_economic_eval.py):**

1. **Annualized Sharpe** (per-trade net / per-trade net std) × √(trades/year)
2. **Max drawdown** — cumulative sum of per-trade net PnL; find peak-to-trough; express in units
   ($/bbl for energy, ¢/lb for livestock) and as multiple of median net trade
3. **Breakeven cost curve** — compute net PnL for cost ∈ {0.05, 0.10, 0.15, 0.20, 0.30, 0.40,
   0.50, 0.60, 0.80, 1.00} $/bbl (energy) or {0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50} ¢/lb
   (livestock); find the cost where OOS net = 0 (OOS breakeven)
4. **Capacity estimate** — less-liquid leg ADV lookup; cap at 5% of ADV × contract size

**Pre-registered pass criteria:**

| Metric | PASS | MARGINAL | FAIL |
|---|---|---|---|
| OOS breakeven cost | > 2.0× defended realistic cost | 1.5-2.0× | < 1.5× |
| Annualized Sharpe (full period) | > 0.8 | 0.5-0.8 | < 0.5 |
| Max drawdown (in median trades) | < 20× median net trade | 20-35× | > 35× |
| Capacity (per sleeve) | > $500k annual theoretical max | $100k-$500k | < $100k |

**Defended realistic costs (pre-registered):**
- RB-CL: $0.20/bbl (liquid NYMEX crack; 2-leg spread execution ~$0.15-0.25 all-in)
- LE-GF: $0.20/¢/lb (CME livestock; feeder cattle less liquid leg ~$0.15-0.25 all-in)

OOS breakeven target: ≥ $0.40/bbl (RB-CL), ≥ 0.40¢/lb (LE-GF) — i.e., 2× defended realistic cost.

---

## Gate 4 — θ-Gradient Surrogate Test

**Test:** Run the same fade (run_fade) on 500 matched-OU and 500 RW surrogate paths at θ ∈
{1.0, 1.5, 2.0, 2.5}. Record mean gross PnL at each θ for each surrogate type.

**Pre-registered pass criteria:**

- PASS: real gross gradient (slope across θ values) > 3× the median surrogate gradient (OU or RW)
  → the escalation is genuine, not a mechanical artifact of higher thresholds
- MARGINAL: real slope is 1.5-3× surrogate slope → note as genuine but verify
- FAIL: real slope ≤ 1.5× surrogate slope → the gradient is an artifact (same structure as NG
  selectivity, doc 31 A_FALSE_RESCUE); downgrade to flat-selectivity case

Apply to LE-GF only (most pronounced gradient); check RB-CL for completeness.

---

## Gate 5 — Named-Agent Adversarial Adjudication

**Agents spawned in parallel after Gates 0-4 computational results are known.** Each receives full
gate results as context and attempts to kill the sleeve.

| Agent | Mission | Primary attack vectors |
|---|---|---|
| Adversarial (kill-ledger) | hunt every channel that could falsify the confirm | residual back-adj in deseason, β-stability in OOS, roll-date clustering in trade entries, selection-on-deviation in θ-gradient |
| Statistical | multiplicity audit, OOS independence check, surrogate quality | p-hacking surface, dependence between surrogate types, OOS contamination, Sharpe inflation |
| Trader/PM | economic feasibility | capacity ceiling (GF ADV), realistic 2-leg execution cost, drawdown survivability, book margin requirements, crude oil tail correlation |

**Per-sleeve verdict synthesis (pre-registered):**

| Outcome | Criteria |
|---|---|
| CONFIRMED-SLEEVE | passes all Gates 0-4 AND adversarial fails to find fatal flaw |
| MERELY-TRUE | passes Gates 0-4 but adversarial identifies capacity/cost floor that neutralizes net edge |
| CONTAMINATED | fails Gate 0 or Gate 4 (regardless of other gates) |
| NON-FINDING | fails Gates 1-3 multiplicity/breakeven |

---

## Non-Negotiable Cross-Cutting Rules

- Temporal firewall intact: no future data in any gate
- Report the full search in Gate 2, no argmax
- Do not modify frozen primitives (analytics_arm_a.py, _v2.py, _v2_beta.py)
- Gates are sequential: if Gate 0 kills a sleeve, halt that sleeve's subsequent gates
- Hard stop after sleeve verdicts: do NOT begin portfolio construction or correlation analysis

---

*Pre-registered 2026-06-06. No criteria may be changed after this file is written.*
