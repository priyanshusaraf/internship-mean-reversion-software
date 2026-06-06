# AMR Session Summary — 2026-06-04b
## Strategic Inflection, Controlled-β Gate Analysis, and 7-Day Execution Plan

**Session type:** Research Mode — strategic adjudication, programme redesign pressure-test, and execution planning.
**One-line arc:** Entered session with a confirmed-but-uneconomic NG edge and a methodology question (controlled-β). Exited with a trader-first constitutional redesign (doc 32), a pre-registered EIA conditional entry test (doc 33), a rigorous controlled-β first-principles analysis, a pressure-tested 7-day execution plan, and explicit answers to five hard strategic questions.

---

## Starting State (inherited from session 2026-06-04a)

| Item | Status |
|---|---|
| NG calendar MR | CONFIRMED — p=0.005, VR=0.448, but PERSISTENT-BUT-UNECONOMIC (naive book break-even before cost) |
| NG selectivity | KILLED A_FALSE_RESCUE (doc 31, p_rw=0.551 primary, jackknife >500% at high-θ) |
| Rolling-OLS-β on levels | INADMISSIBLE (doc 19, β-update-noise 82–97% of Var(ΔS)) |
| β=1 definitional spreads | ADMISSIBLE (doc 20/21, zero β-DOF) |
| Controlled-β (pairs/cross-asset) | PRE-REGISTERED but NOT EXECUTED (doc 30) |
| Portfolio route | GATED — cohort breadth = 1 instrument (NG only); insufficient for netting |
| State T / Transition timing | ARCHIVED — zombie prohibition binding |
| Programme identity | "Pure research → deployment eventually"; needed redesign |

---

## What Happened in This Session

### Part 1 — Controlled-β Gate Analysis (first-principles, pre-execution)

Produced a comprehensive adversarial analysis of whether non-definitional spreads can be constructed admissibly. Five-part document:

**Part 1 — Mechanism derivation.** The rolling-OLS-β failure is algebraically clean:
```
ΔS_t = (ΔA_t − β_{t−1}·ΔB_t)  −  (β_{t−1} − β_{t−2})·B_{t−1}
                                      └── β-update-noise × price level ──┘
```
The second term accounts for 82–97% of Var(ΔS) on trending legs. A legal β must suppress this term below τ=10% of Var(ΔS) — the mechanistic gate (f_βupdate < τ) in doc 30 §2.4.

**Part 2 — Candidate families evaluated** (survival probability estimates):

| Family | Prob | Key risk |
|---|---|---|
| F1 Kalman β (frozen q_β) | 55–65% | q_β too large → v1 artifact |
| F2 Ridge β | 40–50% | Three-knob DOF surface |
| F3 Long-window OLS (W≥250) | 40–55% | M-gate unknown; symptom-only confirmed in doc 19 |
| F4 Sparse rebalance β | 45–55% | Rebalance spike contaminates VR(q=2) |
| F5 Frozen β (pre-sample) | 70–80% | β instability over long OOS |
| F6 Economic anchor β | 75–85% | Only valid for pairs with known anchor |

**Part 3 — Red team.** Three structural kill arguments: (a) the trilemma — any β that tracks drift has large Δβ on trending B; (b) the positive-control is β=1 only (no confirmed baseline for estimated-β anywhere in the programme); (c) surrogate logic is asymmetric — β estimation on incointegrated surrogates may behave differently than on real pairs.

**Part 4 — Implementation plan.** ~200–270 new lines, full apparatus reused. Primary test pair: Gold-Silver (textbook cointegrated pair, published MR literature, doc-19 diagnostic shows W=500 gives VR(20)=0.60). HDFC-ICICI as negative reference.

**Part 5 — Recommendation.** Controlled-β is worth executing — it is the gate on the entire pairs/cross-asset deployment domain, the pre-registration is done, and the implementation is small. But it is NOT the first move given the trader-first redesign.

---

### Part 2 — Strategic Inflection: Five Hard Questions

**Q1 — Strategic direction.** Answer: **C with explicit sequencing (not symmetric).**

- NOT A alone (Cycle-2 first): too slow; methodology validation without deployment path
- NOT B alone (portfolio now): portfolio requires ≥2 instruments; NG alone cannot net
- C with 70/30 weighting toward deployment-targeted tracks:
  - Weeks 1–3 parallel: EIA conditional entry (NG) + BRN M1-M2 calendar
  - Weeks 2–5: Crack spread controlled-β positive control
  - Weeks 4–10 (gated on BRN): portfolio construction + Cycle-2 controlled-β

**Q2 — Top 5 epistemic risks (ranked by danger × likelihood):**

1. **Vendor back-adjustment contaminating NG** (DANGER: HIGH, LIKELIHOOD: MEDIUM-HIGH) — splice-RW null indistinguishable from real NG (p=0.84); regime-conditionality is the only positive evidence it is not artifact. Mitigation: leg rebuild.
2. **EIA conditioning is State-T with economics attached** (DANGER: HIGH, LIKELIHOOD: MEDIUM) — post-hoc regime identification; threshold selected after seeing heterogeneity. Mitigation: pre-commit threshold before running, vol-controlled check, cross-habitat replication.
3. **False diversification — NG + BRN left-tail correlation** (DANGER: HIGH, LIKELIHOOD: MEDIUM) — normal-market R²~0.15-0.25 masks stress-period R²~0.5-0.7 (2020 COVID, 2022 energy crisis). Mitigation: measure conditional correlation on drawdown periods, not full-sample.
4. **Cost modelling overoptimism** (DANGER: MEDIUM-HIGH, LIKELIHOOD: HIGH) — 0.003 round-trip may be 2-3× understated during high-|z| entries (elevated bid-ask at spread extremes). Mitigation: use 0.005 and 0.008 cost grid; require profitability at 0.005 before calling deployable.
5. **Weak-edge aggregation illusion** (DANGER: MEDIUM, LIKELIHOOD: MEDIUM-HIGH) — realised book P&L path may have unacceptable max drawdown even if expectancy arithmetic is positive. Mitigation: simulate full P&L path, not just expectancy.

**Q3 — Trader-quant balance framework:**

| Domain | Intuition owns | Quant owns |
|---|---|---|
| Generation | Which ideas to test | Whether they survive |
| Mechanism | What drives the edge | Whether it is detectable |
| Causal variables | Which variable to acquire | Whether it adds signal |
| Risk | Sizing, stops, drawdown | Nothing |
| Verdict | Cannot override | Hard kills (§2.2/§2.4 thresholds) |

Key guard: economic mechanism strength is not a substitute for empirical confirmation. Physical arbitrage bounds are a prior, not a confirmed edge.

**Q4 — 30-day roadmap:** Covered in detail in the session; distilled in Part 3 below.

**Q5 — Actual trader product (evidence-based, not imagined):**

A commodity calendar spread book, 3–5 instruments, conditioned on inventory regimes, trading storage arbitrage mean reversion at 2–6 week holding periods. Energy (NG, BRN) first; agricultural (ZC) as diversification; metals if Cycle-2 confirms controlled-β. Structurally: always-on when inventory below seasonal norm, explicitly off in glut regimes. Not a regime-timing engine. Simple, explainable, institutionally defensible.

---

### Part 3 — Pressure-Test: Six Harder Questions

**Q1 — Are we prematurely collapsing into "commodity storage MR"?**

Partially yes, and acknowledged. Evidence that commodities are merely the first habitat (not final destination):
- Kalman-β crack spread confirmation would prove the mechanism transfers to cross-product refinery economics
- ZC agricultural confirmation with USDA variable would prove the structure generalises beyond energy
- FI on/off-the-run specialness is structurally identical (carry bounded by repo specialness)

Current probability: 70% that commodity calendars are a large sub-class, not the entire domain.

**Q2 — Hardest kill arguments against EIA direction:**

Five genuine kill arguments produced:
1. **Explanatory ≠ predictive** — regime label was discovered post-hoc (looking at heterogeneity, then proposing EIA). Cannot undo this without treating the upcoming test as genuinely pre-registered.
2. **Vol-regime confounding** — storage drawdowns = high vol = larger dollar gross even if VR unchanged. The conditional edge might be vol-selection, not improved reversion. Test: does EIA conditioning improve VR, or only gross?
3. **EIA data revision risk** — preliminary estimates revised weekly; 5-year seasonal average retroactively available. Genuine causal implementation requires vintage data as released at time t.
4. **Small-sample conditional regime** — ~14 non-glut years × ~8-10 trades/year = ~112-140 conditional trades. Marginally powered.
5. **Lagging causal variable** — EIA release is Thursday; applies to the previous week's inventory. By following Monday, the market may have already corrected. Futures curve shape is a more real-time storage proxy.

A genuinely hard-to-fool implementation requires: (a) pre-committed threshold, (b) vintage EIA data, (c) vol-controlled check (VR improvement, not just gross), (d) regime-conditioned surrogate (not unconditional surrogates applied to conditional real data), (e) cross-habitat replication on BRN, (f) falsification check on a non-storage instrument (Gold calendar — should NOT respond to EIA).

**Q3 — NG rebuild sequencing.** User was right. **Rebuild first, EIA filter second.** 

Revised logic: if rebuild kills (vendor artifact confirmed), EIA filter result is retroactively uninterpretable. The 2-3 day cost of doing rebuild first prevents wasting 2-3 weeks on a conditional test built on an invalid foundation. Rebuild and EIA data acquisition run in parallel in week 1; comparison diagnostic runs before the conditional test begins.

**Q4 — Portfolio skepticism.** NG + BRN is an energy calendar book, not a diversified portfolio.

Trader-quality definition of sleeve independence: maximum simultaneous drawdown ≤ 1.3× single-sleeve max drawdown. Full-sample R² is insufficient. BRN and NG calendar spreads have stress-period correlation ~0.5-0.7 (2020, 2022). True diversification requires a structurally different asset class (ZC agricultural, GC-SI metals), not a second energy instrument.

**Q5 — Ruthless prioritization (3 things, 4 weeks):**

1. **NG rebuild + EIA conditional entry** (combined, weeks 1-2) — resolves foundation AND deployment unlock simultaneously; highest single EV action.
2. **BRN M1-M2 calendar** (weeks 1-2, parallel) — cohort breadth gate; portfolio direction opens or closes.
3. **Crack spread controlled-β positive control** (weeks 2-3) — apparatus gate for all future non-definitional pairs.

NOT doing: Cycle-2 full execution, portfolio construction math, residual ecology, regime classification, ZC data acquisition, any UI work.

**Q6 — Exact 7-day execution plan:** Documented in detail below.

---

## Exact 7-Day Execution Plan

### Day 1
- Acquire EIA weekly storage data (FRED NGASWNUS or EIA API NG.NW2_EPG0_SA_R48_BCF.W), 2006–2025
- Acquire BRN2! 1D raw leg (verify vs BRN1! format/dates)
- Check data manifest for NG1!/NG2! daily continuations
- **Pre-register doc 33 EIA test before touching data:** freeze primary statistic (net expectancy at storage_surplus_pct < 0.10, θ=1.0), N=200 speed gate, surrogate types, cost=0.003, OOS split ≤2017 train / ≥2018 test

### Day 2
- Build NG self-constructed spread from raw legs (apply ADR_003 roll masking, _valid_increment_mask)
- Clean EIA data: align weekly release to daily spread dates (causal shift: Thursday release → applicable from following Monday), compute rolling 5-year causal seasonal average, compute storage_surplus_pct
- Verify EIA variable identifies the 5 documented glut years (2009, 2012, 2017, 2020, 2025)

### Day 3
- Begin BRN M1-M2 spread construction (same methodology as self-built BRN in doc 21)
- Write EIA conditional test script (conditional mask: storage_surplus_pct.shift(1) < threshold)
- Write vol-controlled check: verify EIA conditioning improves VR, not just gross

### Day 4 — First hard kill gates
- **Kill gate A:** Compare self-built NG VR(20) vs vendor VR(20). If self-built > 0.65 (materially worse): halt EIA filter, report artifact finding, re-evaluate NG programme.
- **Kill gate B:** BRN N=200 speed gate. If p_rw > 0.20: BRN calendar direction killed.
- Run EIA conditional test on vendor spread, N=200. Primary statistic: net expectancy.

### Day 5
- EIA speed gate verdict. If p_rw > 0.20: kill conditional entry; pivot to rebuild-only track.
- If pass: upgrade to N=500 EIA test; run on self-built NG spread for comparison.
- BRN: if speed gate passed, upgrade to N=500.

### Day 6-7
- Full N=500 results on whichever tracks passed speed gates.
- Comparison: vendor vs self-built NG VR — is the conditional edge driven by the same mechanism on both?
- First verdict document (doc 34 or equivalent): EIA filter go/kill; BRN go/kill.
- If both pass: begin portfolio P&L path simulation (NG + BRN daily trade simulation, max drawdown analysis).
- If one or both kills: write kill memo immediately; reprioritize remaining 3 weeks.

---

## What Needs to Happen for Things to Proceed

### Immediate blockers (must resolve before any code runs)

1. **Data availability check:** Do NG1!/NG2! daily continuations exist in the data directory? The self-build requires both raw legs with roll schedule metadata. If not available, data acquisition is the first blocker.

2. **BRN2! 1D acquisition:** BRN1! daily (9526 bars) is confirmed present. BRN2! (second-month continuous) must be acquired from the same source. Without it, BRN calendar test cannot run.

3. **EIA vintage data:** The standard EIA API provides current data. Vintage data (EIA releases as they were issued at time t) requires EIA's API with revision-tracking or FRED's point-in-time data. This matters for strict causality. Acceptable short-cut if vintage unavailable: use current EIA data but acknowledge the limitation and test at time t-1 week alignment to mitigate.

4. **Pre-registration freeze before any data touch:** Doc 33 (EIA conditional entry) must be fully frozen — exact threshold, exact primary statistic, exact N, exact OOS split — before any EIA-conditioned VR is computed. This step requires no data, only a 30-minute specification writing task.

### Decision gates that determine whether each direction continues

| Test | Pass condition | Fail condition | Action on fail |
|---|---|---|---|
| NG self-build comparison | Self-built VR(20) within 10% of vendor VR(0.448) | Self-built > 0.65 (materially worse) | Halt EIA filter; treat NG MR as foundation-uncertain; publish artifact finding |
| EIA conditional N=200 speed gate | p_rw ≤ 0.15 at primary threshold | p_rw > 0.20 | Kill conditional entry direction; NG stays PERSISTENT-BUT-UNECONOMIC |
| EIA vol-controlled check | VR improves under conditioning, not just gross | Gross improves but VR does not | Flag as vol-selection artifact; downgrade to CONDITIONAL SURVIVAL (mechanism unclear) |
| BRN N=200 speed gate | p_rw ≤ 0.15 | p_rw > 0.20 | Kill BRN calendar; move to ZC as next breadth candidate; portfolio direction delayed |
| Crack spread N=200 speed gate | p_rw ≤ 0.15 | p_rw > 0.20 | Kalman-β apparatus needs recalibration; Cycle-2 controlled-β deferred until apparatus fixed |

### Downstream unlocks (contingent on above gates)

| Unlock | Requires |
|---|---|
| NG deployable candidate | EIA conditional passes N=500 + net > 0 at 0.005 cost + self-build consistent |
| Portfolio framing | BRN confirms (≥2 independent instruments) |
| Cycle-2 controlled-β execution | Crack spread positive control confirms apparatus |
| ZC agricultural calendar | BRN kills OR bandwidth frees after BRN closes |
| Dynamic hedge ratio pairs (B2) | Cycle-2 controlled-β confirms Kalman-β admissibility |

### What has already been done (does NOT need repeating)

- Doc 30 (Cycle-2 controlled-β pre-registration) — frozen, complete, awaiting execution authorization
- Doc 32 (trader-first constitutional update) — governing doctrine; active
- Doc 33 (EIA conditional entry pre-registration) — frozen, complete, awaiting data
- Doc 33 (calendar carry/seasonal sleeve pre-registration) — frozen, separate hypothesis line
- β-update-noise decomposition analysis — proven analytically and empirically (doc 19); does not need re-derivation
- Candidate β family evaluation — completed in this session (F1-F6 with survival probabilities)
- Red-team analysis of EIA direction — completed; 5 kill arguments documented; hard-to-fool implementation specified

### Sacred invariants that must not be violated in upcoming work

- Pre-register before touching data. No exceptions.
- Surrogate-relative reads only. Raw VR without surrogate comparison is not admissible evidence.
- Vol-controlled check on EIA conditioning (the new requirement from this session's adversarial analysis).
- Regime-conditioned surrogates for the full N=500 EIA test (surrogates must be conditioned on the same EIA regime windows as the real data — standard unconditional surrogates are inadequate).
- No threshold selection after seeing results. The two pre-committed thresholds (0.00% and 10% above seasonal average) are fixed; no third threshold added based on results.
- Temporal firewall: EIA storage_surplus_pct must use shift(1) alignment (last available reading before each bar). No contemporaneous EIA reading.

---

## Documents Produced / Updated This Session

| Doc | Title | Status |
|---|---|---|
| 30 | Cycle-2 controlled-β admissibility pre-registration | Pre-existing; context reviewed |
| 31 | NG selectivity results (A_FALSE_RESCUE) | Pre-existing; starting state |
| 32 | Programme redesign: trader-first constitutional update | Pre-existing; governing doctrine confirmed |
| 33 | EIA conditional entry pre-registration | Pre-existing; ready to execute |
| — | Controlled-β Gate analysis (Parts 1–5) | Produced in this session; not yet written as a standalone doc |
| — | Strategic inflection: 5 hard questions + answers | Produced in this session; should become doc 34 or appended to doc 32 |
| — | Pressure-test: 6 harder questions + answers | Produced in this session; key findings integrated above |

**Recommended: write a consolidated doc 34** capturing the controlled-β first-principles analysis and the strategic pressure-test findings as a permanent institutional record. The analysis in this session contains load-bearing conclusions (EIA kill arguments, rebuild sequencing reversal, false-diversification definition) that should survive in the research archive.

---

*Session arc: programme entered with one confirmed-but-undeployable instrument and a methodology question. Programme exits with: a trader-first constitution (doc 32), a pre-registered conditional test (doc 33), a complete controlled-β adversarial analysis, a reversed rebuild-sequencing decision, five documented epistemic risks, a trader-quality definition of sleeve independence, a ruthless 3-priority 4-week plan, and a concrete 7-day execution sequence. The binding bottleneck is now data acquisition (EIA, BRN2!, NG raw legs) and pre-registration freeze before Day 2.*
