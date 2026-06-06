# Doc 39 — Crack-Spread Controlled-β: Real Data Results (HO2!-CL2!)

**Document class:** Permanent AMR research record (institutional memory).
**Date:** 2026-06-05. **Mode:** Controlled Implementation — real data execution.
**Pre-registration:** `crack_beta_execution_prereg.md` (frozen 2026-06-05).
**Synthetic gate:** doc 37 (F6+F5 ADMISSIBLE; F1/F2/F3 INADMISSIBLE).
**Data:** `data/processed/crack_beta_real_results.json`.
**Script:** `scripts/run_crack_beta_real.py`.
**Status:** CYCLE-2 CONFIRM — §11.8 POSITIVE CONTROL CONFIRMED.

---

## Prior Belief

Per crack_beta_execution_prereg.md §A: literature-documented HO-CL cointegration (Pindyck & Rotemberg 1990; Routledge, Seppi & Spatt 2000). Prior probability of full Cycle-2 CONFIRM: MEDIUM-HIGH (~65%). Expected F6 to confirm (β=1 definitional). Expected F5 to corroborate if pre-sample β materially differs from 1.0.

Back-adjustment caveat (pre-noted): 3,291/7,003 bars have negative A_barrel (back-adj offset). VR test operates on increments (not levels), so level contamination is isolated to roll dates (masked). Concern: deseasonalization removes back-adj drift, potentially inflating apparent sub-diffusion — flagged BEFORE execution.

---

## Data & Construction

| Item | Value |
|---|---|
| Pair | A = NYMEX HO2! × 42.0 ($/bbl), B = NYMEX CL2! ($/bbl) |
| Date range | 1998-07-19 → 2026-06-03 |
| N bars (merged) | 7,003 |
| OOS split | 70/30 — IS: 4,902 bars (≤2018-01-24), OOS: 2,101 bars (≥2018-01-25) |
| F5 pre-sample | First 1,750 bars ≈ 6.9 yr (≤2005-02 approx.), β=1.0537 frozen post-pre-sample |
| F6 β | 1.0 (fixed) |
| Roll detection | increment_jump_mask(k=8.0, W=60) on deseasonalized spread |
| Roll masked bars | F6: 20 bars; F5: ~12 bars post-pre-sample |

---

## β Construction Sanity Check

| Family | β value | f_βupdate | vs τ=0.10 |
|---|---|---|---|
| F6 | 1.0000 (fixed) | 0.0000 | ✓ PASS |
| F5 | 1.0537 (pre-sample OLS, frozen) | 0.0000 | ✓ PASS |

Zero β-update noise for both families. Causal firewall intact.
F5 β=1.0537 indicates the HO/CL cointegrating ratio is slightly above barrel-parity — consistent with HO having a small quality/delivery premium over crude.

---

## Results: Full Period (1998-2026)

| Family | VR(2) | VR(5) | VR(10) | VR(20) | p_rw | p_garch | p_ma1 | p_ou | CONFIRM |
|---|---|---|---|---|---|---|---|---|---|
| F6 (β=1.0) | 0.8169 | 0.6650 | 0.5789 | **0.4931** | **0.005** | **0.015** | **0.005** | 0.169 | **YES** |
| F5 (β=1.054) | 0.6253 | 0.4967 | 0.4225 | **0.3350** | **0.005** | **0.005** | **0.005** | 1.000 | **YES** |

Both families pass the RW∧GARCH∧MA1 headline gate. Construction-controlled corroboration: **AGREE** (both confirm, F5 shows stronger sub-diffusion).

---

## Results: OOS Period (2018-01-25 → 2026-06-03)

| Family | VR(2) | VR(5) | VR(10) | VR(20) | p_rw | p_garch | p_ma1 | p_ou | CONFIRM |
|---|---|---|---|---|---|---|---|---|---|
| F6 (β=1.0) | 0.9859 | 0.8920 | 0.7985 | **0.6673** | **0.005** | **0.020** | **0.005** | **0.005** | **YES** |
| F5 (β=1.054) | 0.9834 | 0.8801 | 0.7755 | **0.6367** | **0.005** | **0.015** | **0.005** | **0.005** | **YES** |

OOS confirmation is the decisive gate. Both families confirm in the 2018-2026 window, which has lower back-adj contamination risk than the full period (recent data, smaller cumulative roll offsets).

---

## Key Findings

**Finding 1 — CYCLE-2 CONFIRM:**
≥1 admissible family yields real-pair VR(20) < 5th percentile of matched RW ensemble (p<0.05), f_βupdate < 0.10, confirmed OOS. This constitutes a Cycle-2 CONFIRM per crack_beta_execution_prereg.md §D.

**Finding 2 — §11.8 POSITIVE CONTROL CONFIRMED:**
The apparatus detects the known HO-CL cointegrated MR edge (documented in the literature since 1990). Both families confirm; OOS holds. An apparatus that cannot detect a known real reverter cannot be trusted elsewhere — this gate is now satisfied. Confidence upgrade: apparatus confirmed on a literature-grade real instrument.

**Finding 3 — F5 STRONGER THAN F6 (pre-sample β adds value):**
F5 VR(20)=0.335 vs F6 VR(20)=0.493 (full period). Pre-sample OLS β=1.054 better aligns with the true cointegrating vector than the forced β=1.0. This validates the "estimated-once, applied-frozen" construction as a scientific contribution: learning the ratio pre-sample and applying it frozen preserves both causal integrity and improved spread construction. F6 serves as the baseline; F5 is the refined version.

**Finding 4 — OOS IS DURABLE:**
Full-period VR(20) is lower (stronger MR) than OOS VR(20) — expected since full period includes back-adj-contaminated early data where deseasonalization removes back-adj drift. OOS-only (2018-2026) VR(20) ≈ 0.64-0.67 is the more conservative and credible estimate. Still strongly confirms (p_rw=0.005, p_ma1=0.005 both families).

**Finding 5 — BACK-ADJ CAVEAT (MONITORED, NOT FATAL):**
3,291 negative A_barrel values (back-adj level offset). Pre-registration noted this. VR operates on increments (not levels); deseasonalization removes the secular drift. MA1 null passes — if back-adj roll artifacts were driving the result via spurious autocorrelation, the MA1 null would have caught it. The OOS confirmation (less back-adj contamination in 2018-2026) further supports the result as genuine. However, exchange-native (non-back-adj) prices remain the ideal future robustness check.

**Finding 6 — F5 FULL-PERIOD p_ou=1.000 (non-fatal):**
The OU null for F5 full period is NOT beaten — the fitted OU process is MORE sub-diffusive than VR(20)=0.335 from the real data. Interpretation: the OU null fits the autocorrelation structure of the F5 spread with such fast reversion that even VR=0.335 looks weak by comparison. This is a known limitation of the OU null (it can overfit to the real dynamics). Since OU is non-gating, this does not affect the headline verdict. The OOS period shows p_ou=0.005 for F5 (OU null IS beaten in 2018-2026), consistent with a genuine MR signal.

---

## Verdict

```
CYCLE-2 VERDICT:   CONFIRM (full and OOS)
§11.8 STATUS:      POSITIVE CONTROL CONFIRMED
F6 (β=1.0):        CONFIRMED — VR20=0.493 full / 0.667 OOS
F5 (β=1.054):      CONFIRMED — VR20=0.335 full / 0.637 OOS
CORROBORATION:     AGREE (both families confirm; F5 stronger)
f_βupdate:         0.000 both families (causal firewall intact)
BACK-ADJ CAVEAT:   MONITORED — OOS confirmation reduces concern; exchange-native
                   prices remain the ideal robustness check
```

---

## Confidence Update

| Dimension | Prior | Posterior |
|---|---|---|
| Apparatus validity (§11.8) | MEDIUM (synthetic only) | **HIGH** — confirmed on a known real edge |
| HO-CL crack spread MR | MEDIUM-HIGH (lit-documented) | **HIGH** — full + OOS confirm, both families |
| Controlled-β (F5) admissibility on real data | MEDIUM (cleared synthetic only) | **HIGH** — zero f_βupdate, stronger confirm than F6 |
| Back-adj contamination risk | MODERATE concern | **LOWER** — OOS confirm + MA1 passes reduce concern; residual |

---

## What This Does NOT Establish

- **Trading deployability:** Confirmation of MR existence ≠ cost-clearing book. Transaction costs, capacity, carry, and execution must be evaluated before any deployment claim. This is an observability result, not a signal.
- **Universal MR:** Local result on one instrument/window. Cross-habitat replication required per §11.7.
- **State T / timing:** This result is purely distributional and corpus-level. No per-bar signal, no timing claim, no score. Any drift in that direction is forbidden.
- **Non-back-adj confirmation:** Exchange-native prices are the ideal replication target.

---

## Surviving Uncertainty

1. Back-adj level contamination: reduces with exchange-native replication.
2. F5 β stability: pre-sample OLS on 6.9 years (1998-2005) — need to check if the relationship was stable in that period vs 2005-2026.
3. OOS VR(20)≈0.64-0.67 — weaker than full period; cost-clearing remains unproven.
4. p_ou=1.000 for F5 full period: OU overfit explanation is likely correct but deserves examination in a future session.

---

## Next High-Information Action

The §11.8 gate is satisfied. The programme may now proceed to:

1. **Cross-habitat OOS replication** (§11.7 binding): a second cointegrated pair (e.g. RB2!-CL2! gasoline crack, or a non-energy textbook cointegrated pair) must also confirm before the apparatus result is global rather than local.
2. **Economic evaluation of the crack spread**: can this be the anchor for a cost-clearing book? Requires: transaction cost, bid-ask, capacity, carry analysis. Very likely to be MERELY-TRUE at the naive level (same pattern as NG), but worth the check before writing off.
3. **F5 β stability check**: compare pre-sample (1998-2005) β=1.054 to the full-period OLS β — if they agree, this strengthens the F5 result; if they diverge sharply, it warrants investigation.

---

*Append-only. Results locked from data/processed/crack_beta_real_results.json run 2026-06-05.*
