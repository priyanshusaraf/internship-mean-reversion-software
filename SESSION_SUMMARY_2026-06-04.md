# AMR Session Summary — 2026-06-04

**Scope:** one working session, four linked research initiatives + one adjudication, all under AMR doctrine
(CLAUDE.md §1–§15). Mode: mostly Research; Controlled-Implementation only for the additive v2 engine. Method:
pre-registration-first, surrogate-relative, adversarially-falsified, multi-lens (workflow) orchestration.
**One-line arc:** validated the apparatus on a real edge (NG), proved that edge is *true-but-uneconomic*, killed
the predictive "transition" object as forbidden State-T resurrection, and showed portfolio construction cannot
rescue weak MR on the current cohort — **relocating the binding bottleneck from *timing* → *cohort breadth*
(Cycle-2 controlled-β).**

---

## 0. Starting state (inherited)
- **Arm A v1 (doc 19, 2026-06-03): INCONCLUSIVE.** The frozen W=60 **rolling-OLS-β-on-levels** construction
  *manufactures* super-diffusion (β-update-noise = 82–97% of Var(ΔS); proven on synthetic ground truth). Decisive
  pairs never validly tested. Two ACTIVE priorities: the §11.8 real-data positive control, and re-pre-registering
  Arm A's construction.
- **State T** already FROZEN/KILLED-IN-FORM (doc 11/12). MRScore ARCHIVED (inverted). CSU ARCHIVED.

---

## 1. Arm A v2 — Cycle 1: real-data positive control  → **CONDITIONAL SURVIVAL**
**Docs:** `20_arm_a_v2_positive_control_prereg.md` (frozen pre-reg), `21_arm_a_v2_results.md` (verdict).
**Engine:** `backend/app/services/analytics_arm_a_v2.py` (additive; imports frozen v1 primitives, leg path
untouched). **Runner:** `scripts/run_arm_a_v2.py`. **Hygiene:** `scripts/hygiene_arm_a_v2.py`.

- **Construction fix:** restrict to **β=1 DEFINITIONAL calendar spreads** → zero rolling-β DOF → structurally
  immune to the v1 artifact. Reframed as the **§11.8 standing gate**: can the apparatus CONFIRM a known
  literature-anchored real edge (storage-driven calendar MR)?
- **Pre-freeze 4-lens review** caught: jump-filter would flip the verdict (kept UNMASKED + ablation only); RB
  belongs at long horizons; **MA(1)-microstructure-noise null was missing** (added); deseasonalization mandatory.
- **Calibration gate (all pass):** seasonal-OU confirms (power); RW FPR = **3.0%** (200 seeds); **RW+bounce killed
  by MA(1)** (the decisive noise-discrimination control); jump filter no-op on no-seam data.
- **Verdict — NG front calendar CONFIRMS:** VR(20)=0.448; beats RW (p=0.005), GARCH (0.025), **MA(1)-noise
  (0.005)**; survives causal deseasonalization (→0.249); open/close consistent. **Self-built Brent calendar**
  (BRN1!−BRN2!, our construction, no vendor back-adjustment) confirms at all horizons → corroborates the
  apparatus. RB calendar correctly NULLs at q≤20 (selectivity).
- **Confidence:** MEDIUM-HIGH (apparatus power/selectivity/calibration) / MEDIUM (NG clean vs vendor artifact).
  §11.8 gate **passed conditionally** → future kills become more credible. Open caveat: vendor back-adjustment.

---

## 2. Arm A v2 — Cycle 1b: rolling-local trader-persistence  → **PERSISTENT-BUT-UNECONOMIC**
**Docs:** `22_arm_a_v2_rolling_local_prereg.md` (frozen pre-reg), `23_arm_a_v2_rolling_results.md` (verdict).
**Runner:** `scripts/run_arm_a_v2_rolling.py`. Trader-first; windows frozen before any real rolling VR.

- **Method correction (pre-freeze):** the per-window **binary** VR flag is underpowered at trader window lengths
  (synthetic: a real φ=0.95 OU confirms ~10% of 3-yr windows) AND fires *higher* on bounce → replaced by a
  power-robust **pooled mean-z** (per-window standardized VR(20) below its own RW band) + construction-controlled
  Brent corroboration + splice-RW diagnostic + half-life + causal trade proxy.
- **Persistence: YES.** NG yearly pooled mean-z = **−0.627** (t=−4.37, **p≈2e-4**), 14/19 yrs below RW-median,
  **survives post-2020** (−0.438). Regime-structured: the edge **switches off in 5 storage-GLUT years**
  (2009/2012/2017/2020/2025; VR→1, half-life→27) — *not* in shocks — which is the strongest evidence it is genuine
  storage MR, not a uniform vendor splice.
- **Deployability: NO.** A naive causal z-entry book is **break-even before cost** (gross +0.0004 vs 0.003
  round-trip) → net-negative. Half-life ~13 bars (tradeable), persistence real — but uneconomic. **truth ≠
  usefulness.**
- **Caveat (verification):** "genuine MR vs partial vendor back-adjustment" **not cleanly excluded** (NG −0.627 ≈
  the quarter-strength splice anchor −0.657, p=0.84); the regime-conditionality is the main positive evidence.
  §11.8: neither strengthens nor downgrades the edge; modestly strengthens the apparatus.

---

## 3. Research Initiative — Transition Into MR ("better than State T")  → **OBSERVATIONAL_ONLY_SURVIVES**
**Doc:** `24_transition_into_mr_initiative.md`. **Method:** 13-agent workflow (2 ground · 7 required lenses · 3
adversarial kill-passes · 1 synthesis).

- **Verdict:** a *predictive* trend→MR transition object (transition probability / per-bar score / precursor) is
  **DEAD and §4-FORBIDDEN as State-T resurrection** — fails the zombie-reopen test on **3 of 4 clauses**; all 3
  adversaries kill = SEVERE.
- **The decisive, durable reason (object-class, not statistics):** a transition is **defined by the regime that
  FOLLOWS** the candidate instant → **no causally-definable transition LABEL exists** → every statistical costume
  (Markov-switching, CUSUM-as-transition, run-length-VR, TAR/SETAR) inherits the error. Every "causal escape"
  collapses into future-label / forward-read / rolling-manufacture (doc 19) / selection-on-deviation (doc 11/16).
- **What survives:** a strictly observational, unconditional, fixed-grid VR(q) characterization (surrogate-relative,
  μ*-independent) — which **folds into the existing MR-Habitat object**, not a new module — plus a **defensive-only
  innovation-CUSUM cut-flag** (cut/widen/stop exposure, never open an MR entry).
- **Reopen trigger:** ONLY signed order flow / OFI / OI-COT on a flow-driven instrument + a NEW pre-reg with a
  leak-free causal label. Else WHEN-as-prediction is **non-modelable and closed**. The real unlock is **data, not a
  cleverer statistic.** (Independently, State T was *definitively* archived via a 62-file cross-habitat sweep —
  62/62 rejects.)

---

## 4. Research Initiative — MR Portfolio Economics  → **ROUTE_GATED_ON_VALIDATION_AND_COHORT**
**Doc:** `25_mr_portfolio_economics.md`. **Method:** 8-agent trader-first workflow (PM · quant stat-arb ·
execution/cost · statistical adversary · risk manager → 2 adversarial kill-passes → synthesis) + a research-lead
empirical diagnostic.

- **Question:** can gating/selectivity/diversification/netting/turnover/conditional-participation convert
  statistically-real-but-weak MR into cost-clearing alpha? **Answer: not on the current cohort.**
- **The spine — expectancy vs variance (arithmetic):** `E[Σwᵢ(gᵢ−cᵢ)] = Σwᵢ·E[gᵢ−cᵢ]` is correlation-free → a
  diversified book of sub-cost sleeves is *still* sub-cost. **Only selectivity (↑gross) and netting (↓cost) move
  the ledger;** the other 4 levers are variance/Sharpe movers (cannot rescue negative expectancy).
- **Both ledger-movers fail here:** selectivity is **currently unsupported / low-prior** (see §5 correction below);
  netting has **nothing to operate on** because the admissible clean-daily-β=1 MR cohort is **NG alone** (RB
  martingale@q≤20; Brent hourly; pairs need inadmissible rolling-OLS-β; controlled-β untested).
- **Minimum route (strictly-ordered gates):** Gate 1 (NG selectivity surrogate test, low prior) → **Gate 0/2:
  Cycle-2 controlled-β cohort expansion — the binding gate** → Gate 3 (book-level cost/capacity test). Variance
  machinery earns its keep only on ≥2 positive-expectancy sleeves.

---

## 5. Adjudication — selectivity epistemic correction + strategic dependency graph
**(Pure adjudication; no diagnostics. Captured in `25_…` §2/§6/§7 + corrected registry/memory.)**

- **Correction accepted:** the NG selectivity check was **not pre-registered** → it is **exploratory grounding / a
  soft prior update, NOT a binding verdict.** Selectivity status = **CURRENTLY UNSUPPORTED / LOW PRIOR**, *not*
  "dead."
- **Distinction (do not over-collapse):** *selection-on-deviation* is a **failure mode** (fading |z|≥θ harvests
  reversion from a pure RW too — NG |z|≥2 gross +0.0365 vs RW-null p95 +0.047, p≈0.11, 63% in 3 trades) that any
  tail-selective strategy must be proven to survive; *economically pre-registered tail selectivity* is a
  **legitimate strategy class** admissible iff frozen ex ante + surrogate-relative + OOS + episode-jackknife +
  cost-clearing.
- **Materiality:** the top-line verdict is **robust** to the downgrade (the cohort, not selectivity, is binding) —
  but the downgrade **re-justifies running the Gate-1 pre-registered selectivity test** (no longer foregone).
- **Strategic dependency graph (what must be true before each is *economically* meaningful):**
  `apparatus-trust → CONTROLLED-β ADMISSIBILITY (Cycle 2 = KEYSTONE) → cohort breadth + per-instrument expectancy
  → portfolio construction → book cost test → DEPLOYABLE MR.` **Habitat persistence is economically meaningful only
  DOWNSTREAM of a cost-clearing book** (else true-but-inert; research-prioritization value only) — confirming and
  extending the user's reprioritization of portfolio economics ahead of habitat persistence.

---

## 6. Cumulative state change (what we now know)
| Object | Before session | After session |
|---|---|---|
| §11.8 real-data positive control | unmet (all synthetic) | **passed conditionally** (NG, MEDIUM-HIGH apparatus) |
| Construction ontology (`beta_mode`) | rolling-OLS killed | **β=1 definitional = admissible**; controlled-β = the untested unlock |
| NG calendar MR | unknown | real + persistent (p≈2e-4) but **uneconomic** (naive book); back-adj not cleanly excluded |
| Predictive trend→MR transition | killed-in-form | **§4-FORBIDDEN resurrection** (object-class kill; reopens only with OFI data) |
| Portfolio rescue of weak MR | open | **gated on cohort breadth + selectivity validation** (no route on current cohort) |
| Binding bottleneck | timing / data | **admissible-cohort breadth (Cycle-2 controlled-β)** |

---

## 7. Artifacts produced
- **Research docs (institutional memory):** `docs/research/20`–`25` (pre-regs + verdicts for Arm A v2 Cycle 1,
  Cycle 1b; transition initiative; portfolio economics).
- **Code (additive, isolated):** `backend/app/services/analytics_arm_a_v2.py` (pre-built-series adapter,
  MA(1)-noise null, causal deseasonalization, pooled-mean-z machinery — v1 leg path untouched). Scripts:
  `hygiene_arm_a_v2.py`, `run_arm_a_v2.py`, `run_arm_a_v2_rolling.py`.
- **Data:** `data/processed/arm_a_v2_results.json`, `arm_a_v2_rolling_results.json`.
- **Registry:** `HYPOTHESIS_REGISTRY.md` updated (positive control · Arm A v2 · `beta_mode` · NG deployability ·
  transition ARCHIVED · VR(q) ecology · portfolio framing).
- **Auto-memory:** `project_arm_a_verdict`, `project_transition_verdict`, `project_portfolio_economics` (+ index).
- **Workflows run:** Arm A v2 design review, Cycle-1 verdict verify, rolling design review, rolling verdict verify,
  transition (13 agents), portfolio economics (8 agents) — plus several inline empirical computations.

---

## 8. Open questions / next moves (ranked)
1. **KEYSTONE — Cycle-2 controlled-β admissibility:** pre-register a regularized/Kalman hedge ratio + its §11.8
   positive control + a doc-19 martingale zero-control. Gates cohort breadth → portfolio → deployable MR.
2. **Cheap parallel — Gate-1 NG selectivity surrogate test (pre-registered):** RW+OU+GARCH+splice nulls, N≥500,
   θ-grid frozen train→OOS, episode-jackknife, full grid. Settles the lone standalone expectancy lever (prior LOW).
3. **Close NG back-adjustment:** splice diagnostic on actual ng12 seam dates / rebuild from raw m1/m2 legs.
4. **Deferred (correctly):** habitat persistence as an *economic* deliverable — contingent on a cost-clearing book;
   its internal adjudications (circularity / materiality / non-State-T) are research-prioritization, not a gate.
5. **Strategic unlock (data):** signed order flow / OFI — the only path that reopens a predictive transition object.

---
## 9. Governance notes (discipline applied this session)
Pre-registration **before** every verdict (docs 20/22 frozen pre-results); surrogate-relative reads throughout;
synthetic positive controls + FPR calibration; mandatory adversarial / multi-lens falsification on every major
conclusion (§12.6); the **§4 zombie firewall** enforced (transition prediction rejected as State-T resurrection);
the **soft-prior vs binding-verdict** distinction honored (selectivity downgraded; no history erased, §5 markers
used); cost-after-book treated as first-class (§11.2). No implementation beyond the additive, reversible v2 engine
was authorized or performed.
