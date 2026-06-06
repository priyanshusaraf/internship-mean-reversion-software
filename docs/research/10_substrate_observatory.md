# Substrate Observatory (v1) — Build Record & Scale-Dependence Finding

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **Substrate Observatory v1 BUILT** as a cheap, interpretable, causal character instrument —
*"what kind of market are we looking at?"* answered as **resemblance to coarse archetypes over a
trailing window**. Engine correct (causal-firewall bit-identical; synthetic habitats discriminate as
designed). Authorized under a narrow §10 freeze-break (the observational substrate layer beneath State
T; observability ≠ productionization). **Not wired to any signal/gate/μ\*/MRScore** — structurally
terminal. The decision to build this layer *before* State T was adjudicated this session by the
research-planner and alignment-advisor (both: YES, with guardrails — recorded in §1).
**Date:** 2026-06-02.
**Scope:** causal-only; 3 descriptors (directional efficiency · variance ratio · realized-vol
percentile-as-context); 4 buckets (OU-like · Trend-like · RW-Null · Ambiguous); frozen transparent
monotone score map. Per-bar series + workbench panel (SUB). No detection, no timing, no threshold.

> **▸ CONTEXT (placeholder framing — frozen).** All real reads here are on ADANIENT (placeholder,
> trend-heavy at the macro scale) and on-disk synthetics scale-matched to it. The deployment domain
> (spreads · pairs · cross-asset RV) is expected materially more mean-reverting. No market truth is
> inferred. See `CONTINUATION_STATE.md` §0.

---

## 1. Prior thesis & the build decision

MRScore v1 (doc 09) established that **local reversion evidence is noisy and easy to hallucinate in
isolation**, and that State T appears **conditional on market substrate, trend etiology, and
environmental context**. Hypothesis entering this session: the next layer should be an *observational
substrate layer* answering "what kind of market is this?" **before** State T — because State T is
*defined* as a substrate-conditional transition, and characterising "transition from X" requires first
characterising X.

**Adjudication (this session):**
- **research-planner →** TAXONOMY-NEXT = YES. Highest-ROI next layer; State T on an uncharacterised
  substrate is uninterpretable (cannot tell genuine transition from substrate baseline) and its kill
  criteria (base-rate / clustering) cannot be correctly stratified. Reframed "taxonomy" → **Substrate
  Observatory** (descriptors, not a classifier product).
- **alignment-advisor →** CONSISTENT-WITH-GUARDRAILS. The sharp line: classifying instrument
  **character** is observatory-legal (doc 04 §2.5.1); classifying episode **timing** ("a regime is
  igniting now") is State T detection (doc 04 §1.2.2/§1.3.1, FROZEN). A soft score does **not** launder
  a forbidden question. Three hard constraints adopted: **(1) character, not timing** (exhaustion /
  etiology excluded — episode-level, the deferred State-T conditioning gate, doc 04 §2.6.4);
  **(2) terminal + transparent + frozen-weight, exactly like MRScore**; **(3) a small observatory, not
  a Layer-4 framework** — no HMM, no DL, coarse fixed buckets.

## 2. Implementation (`backend/app/services/analytics_substrate.py`)

- **3 descriptors, causal, trailing window W** (default 120). DE at bar `t` and VR at `t` use only
  `[t−W+1, t]`; realized-vol percentile ranks today's vol in its trailing history. Bit-identical
  future-injection firewall is the standing acceptance bar (passes).
  - **Directional efficiency** DE = |net move|/path-length ∈ [0,1] — the **trend↔chop axis**. Survives
    sign changes (works on spreads).
  - **Variance ratio** VR = mean of VR(q), q∈{2,5,10} on log-prices — splits **OU (<1) vs RW (≈1)**.
    Mean (not min, unlike MRScore's MR-favourable min_q) for a *neutral* central read.
  - **Realized-vol percentile** — **context only**, never a character driver (would be gameable).
- **Character map** `character_scores(DE, VR)` — pure, pointwise, frozen, monotone, hand-set
  thresholds (NEVER fit): `Trend = min(1, DE + 0.30·t_vr)`, `OU = (1−DE)·m_vr`, `RW = (1−DE)·rw_vr`,
  `Ambiguous = 1 − max(...)`, where `t_vr=clip((VR−1)/1)`, `m_vr=clip((1−VR)/0.5)`,
  `rw_vr=max(0,1−|VR−1|/0.5)`. `dominant`=argmax; `confidence` from top-two margin (clear ≥0.20 ·
  weak ≥0.08 · ambiguous). Scores are **independent resemblance** in [0,1], not a partition.
  **"Frozen" here = fixed-for-v1 / will-not-be-retuned (especially not on ADANIENT), NOT
  validated-as-correct** — the thresholds (0.30, 0.75, the margin cuts) are economic/structural priors,
  unvalidated against any outcome by design (this is a descriptive instrument; see §4, §7).
- **Scope decisions (frozen this build):** **Hurst removed** (window/method-sensitive — the "easy to
  hallucinate" estimator; VR carries the same axis with a closed-form null). **Causal-only** — the
  full-information variant is a one-line window swap, deferred (no genuine future-using descriptor
  exists yet; a faked dual mode would be a §6.2 violation dressed as compliance, per the doc-09
  precedent). **Vol = context, not a driver.**
- **DESIGN CORRECTION caught during the build (MEASUREMENT).** First map used `½·DE + ½·t_vr` for
  Trend and equal-weighted RW. It misread a deterministic trend as RW because **a deterministic-drift
  trend has VR ≈ 1** (drift adds to the mean, not the variance — VR detects only *stochastic*
  persistence). VR therefore **cannot** carry the trend axis; DE must. Map rebuilt DE-primary (VR>1 is
  a momentum *bonus*, never a requirement). Flagged, not silently kept.
- **C1 guard (mirrors doc 09).** VR uses log-prices → undefined on non-positive/spread series. Endpoint
  emits an explicit `data_warning` ("structural incompatibility, NOT an unfavorable reading"); panel
  renders red banner + no-read notice. Spread-domain (raw-price VR) is deferred research.
- **One-way DAG (STRUCTURAL).** Self-contained on raw OHLCV; imports nothing from μ\*/Kalman/MRScore and
  is never imported back. Re-derives its own small vol helper rather than coupling to the MRScore
  observatory — two terminal observatories stay independent. Output terminates at display.
- **Vertical:** `compute_substrate` → `GET /api/v1/market/{id}/substrate?window&start&end` (respects the
  `end` replay boundary) → SUB workbench panel (**descriptors-first** UI: DE/VR sparklines + descriptor
  cards primary; resemblance scores subordinate behind a toggle — researcher decision, so the evidence
  is read before the archetype label). 25 tests (service + character map + habitat discrimination +
  firewall + endpoint); full backend suite 120 passed.

**Synthetic habitat validation (pinned by tests):** strong OU (lam=−0.25, VR~0.72) → OU-like dominant;
deterministic trend → Trend-like dominant; pure RW → RW-Null dominant. Bit-identical under a 6× future
spike.

## 3. New intel — evidence gathered (live, ADANIENT + on-disk anchors)

### FINDING 1 — Substrate character is strongly SCALE-DEPENDENT; macro "trend-heavy" ≠ trailing-window trend (**STRUCTURAL**)

ADANIENT is trend-heavy as a *10-year macro* object. At **every causal trailing window tested (60–500
bars)** it reads **predominantly RW-Null**, not Trend-like — DE stays low (~0.08–0.19), VR hovers near 1
(0.89–1.12). A slow multi-year equity uptrend, viewed through a months-to-2yr causal window, **diffuses
like a random walk**: the per-window net displacement is small relative to the path length.

| window | ADANIENT median DE | median VR | dominant distribution |
|---|---|---|---|
| 60  | 0.158 | 0.895 | rw_null 1208 · ambiguous 733 · ou 343 · trend 120 |
| 120 | 0.185 | 0.915 | **rw_null 1619** · ambiguous 620 · ou 77 · trend 28 |
| 250 | 0.106 | 1.058 | rw_null 1865 · ambiguous 347 · ou 2 |
| 500 | 0.076 | 1.123 | rw_null 1625 · ambiguous 338 · ou 1 |

This is **real signal, not a defect**, and it directly reinforces CLAUDE.md §1.1 (observed regime ≠
deployment regime; ADANIENT evidence is local, not global): the substrate observatory *confirms* that
ADANIENT's trendiness is not legible at the scales State T would operate on. **Implication for State T:**
"what kind of market" has no single answer — it is a function of horizon. A v2 substrate read may need a
**scale axis** (character across multiple W) rather than one window.

### FINDING 2 — v1 is high-specificity / low-sensitivity for OU: the OU↔RW crossover sits at VR < 0.75 (**MEASUREMENT**)

The genuine reverter `ANCHOR_OU` ("positive anchor, genuine reversion, seed 13") reads **predominantly
RW-Null**, not OU-like, across windows — its windowed VR is consistently **~0.82–0.94** (mildly <1),
never near 0.5. Algebra of the frozen map: for VR<1, `OU = (1−DE)·2(1−VR)` and `RW = (1−DE)·(1−2(1−VR))`,
so **OU > RW only when VR < 0.75**. A mild-but-real reverter at VR~0.85 therefore classifies RW-Null.

This is a **deliberate, defensible conservatism**, not retuned away: RW-Null is the *skeptical null*, and
defaulting mild reversion to it is exactly the MRScore lesson (don't hallucinate reversion in isolation).
The v1 OU bucket is **high-specificity, low-sensitivity** — it fires only on *strong* reversion
(VR≲0.75, e.g. the lam=−0.25 habitat), and abstains to RW-Null on weak reversion. The VR<0.75 threshold
was **NOT** loosened to make OU fire more often (that would be fitting-for-appearance / quant theater).
The trade-off is logged as a calibration question (§7), not silently optimised.

## 4. Methodology quality

Synthetic ground-truth habitats (OU / trend / RW) with discrimination + bit-identical firewall tests;
live reads on ADANIENT and the on-disk anchors across a 60–500-bar window sweep. **Limits:** single real
substrate (ADANIENT); single OU anchor live (n=1 of the genuine-reverter type at this scale); no
multi-seed sensitivity band on the bucket distribution yet; the map's thresholds are economic priors,
unvalidated against any outcome (by design — this is descriptive).

## 5. Confidence update

- **Engine faithfulness / temporal integrity:** **HIGH** (firewall bit-identical; habitats discriminate
  as designed; map is transparent and monotone).
- **Scale-dependence of character (Finding 1):** **MEDIUM-HIGH** (consistent across 4 windows on
  ADANIENT; mechanism is clear — drift adds no variance / small net-over-path at short windows).
- **OU sensitivity on realistic data (Finding 2):** **MEDIUM** — the conservatism is intended and
  understood, but whether VR<0.75 is the *right* OU gate for the mean-reverting deployment domain is
  **untested** (ADANIENT/anchors are not that domain).

## 6. Surviving uncertainty · explicit non-conclusions

- **NOT** concluded: "ADANIENT is a random walk." Concluded only: *at causal trailing windows of
  60–500 bars, its character resembles RW-Null* — a scale-local, substrate-local statement.
- **NOT** a detection or timing claim anywhere. Scores are window-resemblance, never "a regime is
  changing now" (State T, frozen).
- **NOT** a market claim about the deployment domain — ADANIENT is the opposite regime.
- **NOT** a calibrated OU detector — v1 deliberately abstains on mild reversion (Finding 2).
- Full-information mode, a scale-axis (multi-W) read, and exhaustion/etiology character remain
  **deferred** (the last two are State-T territory).

## 7. Next high-information question

Two, ordered by information value:
1. **Is character a scale, not a point?** Does a **multi-window substrate read** (DE/VR across
   W∈{60,120,250,500} surfaced together) give a more honest answer than any single W — e.g. "RW-Null at
   6mo, weak-Trend at 2yr"? Finding 1 suggests the single-window answer is under-determined.
2. **Is VR<0.75 the right OU gate for the deployment domain?** The conservatism is correct for
   ADANIENT (avoids hallucinating reversion in a trend-heavy substrate), but the mean-reverting targets
   may sit at VR~0.85 where v1 abstains. This needs a *mean-reverting real instrument* to adjudicate —
   it must **not** be tuned on ADANIENT (would overfit to the wrong regime). Reopen trigger: first
   mean-reverting real instrument loaded.

Until then, the Substrate Observatory is an **observational / descriptive** instrument: read DE and VR
directly (descriptors-first), treat RW-Null as the honest default, and treat OU-like as a
*high-confidence-only* read.
