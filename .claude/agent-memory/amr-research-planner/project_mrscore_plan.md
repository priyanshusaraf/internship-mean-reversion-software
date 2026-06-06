---
name: project-mrscore-plan
description: MRScore canonical spec, implementation phases, key temporal integrity decisions, and phase-discipline tension resolution from the 2026-06-02 planning session.
metadata:
  type: project
---

MRScore implementation planned as an observatory-mode falsifiable diagnostic (not productionized signal). Authorization from researcher required before any build (§10 deferral tension).

**Why:** "MRScore productionization" is deferred in CLAUDE.md §10. However, "MRScore as observatory diagnostic" (observe → falsify, not operationalize) may be compatible with the observatory-first rule, analogous to how State T observability is permitted while State T detection is deferred. The planning session established this distinction clearly and flagged it as the central go/no-go.

**How to apply:** Always surface the authorization question before any MRScore implementation begins. The phrase "observatory-mode falsifiable diagnostic — not a signal" is the key framing.

---

## Canonical MRScore spec (frozen from doc 01)

Master equation: MRScore_t = 0.20·B1_t + 0.60·B2_t + 0.20·B3_t

Block 1 (Mean Reliability, 0.20):
  B1_t = 0.30·(R_ADF + R_KPSS)/2 + 0.50·R_MSI + 0.20·R_VSI
  - MSI: MeanDrift_t = |μ_t − μ_{t-k}| / σ_t (clipped at 3), MeanStab_t = 1/(1+MeanDrift), w=60, k=20
  - VSI: 1 − |σ_t/σ_{t-k} − 1| (clipped at 0), w_t=20, k=20
  - ADF: lag p = ⌊(w/100)^(1/4)⌋, MacKinnon p-values
  - KPSS: lag ℓ = ⌊4(T/100)^(1/4)⌋

Block 2 (MR Strength, 0.60):
  B2_t = 0.50·R_DRC + 0.30·R_HitRate + 0.20·R_VR
  - DRC: min_{h∈{1,3,5}} t_β(h), NW lag ⌊1.3·h^(2/3)⌋, min window 120 bars, rank on −DRC
  - HitRate: θ=1.0 (FIXED), h=5, min 20 events; pairs use only s ≤ t-h
  - VR: min_{q∈{2,5,10,20}} VR(q)_t, rank on (1−VR_agg)

Block 3 (Tradability, 0.20):
  B3_t = (1/3)·(R_HL + R_VC + R_TCF)
  - HL: max(0, 1 − |ln(HL_t)−ln(10)| / ln(2)), set to 0 if κ̂ ≤ 0
  - VCscore: −(RV_t−RV_{t-k})/RV_{t-k} · (1−VP_t/100), w_t=20, k=5
  - TCF proxy (when no spread data): TCFscore = max(0, 1−VP_t/100); c=0.2 default (NOT calibrated)

Rank aggregation: percentile rank of f_{i,t} against {f_{i,t-N},...,f_{i,t-1}}, W=252, [0,100], directionally adjusted.

## Key temporal integrity findings

- DRC and HitRate: at time t, last valid regression pair is (z_{t-h}, r_t). Pairs with s>t−h involve future prices. Window must be shifted by h.
- DRC z_t predictor: μ* and σ in z_t must be from window BEFORE t (not including P_t). Two separate temporal requirements in DRC.
- Newey-West HAC on DRC is NON-OPTIONAL per doc 01. Without it, t-statistics are inflated.
- Rank aggregation: rank current f_{i,t} against PRIOR W observations only (not including t itself).
- Circularity: μ* → MRScore is one-way. MRScore must never feed back into μ* or the filter.

## Open decisions not frozen

- TotalCost proxy c ∈ [0.1, 0.3]: not frozen, researcher must pick. Default c=0.2 recommended as economic prior, never fitted.
- Which μ* for MRScore: plan assumes EMA (production μ*, per existing frozen decision). Kalman vs EMA comparison of MRScore is a separate optional research arm.
- DRC window before 120+h bars: fill NaN or partial B2? Recommendation: fill NaN.

## Implementation phase order

Phase 0: Authorization gate
Phase 1: Foundation primitives (RV_t, VP_t, rolling percentile rank)
Phase 2: B1 sub-scores (MSI, VSI, ADF/KPSS)
Phase 3: B2 sub-scores (VR, HitRate, DRC) — HIGHEST RISK for temporal integrity
Phase 4: B3 sub-scores (HL proximity, VCscore, TCF)
Phase 5: Aggregation + API endpoint + frontend panel
Phase 6: Synthetic falsification (ANCHOR_OU vs NULL_RW discrimination)

## ADANIENT regime warning for MRScore

ADANIENT is trend-heavy. MRScore on ADANIENT is expected to score LOW on B1 (non-stationary) and LOW on B2 (no mean reversion). This is correct behavior, not a bug. Primary validation must be against synthetic instruments (ANCHOR_OU: should score high; NULL_RW: should score low).

## Hint list divergences from docs

"Expectancy" (hint list B2) does not appear in the docs. B2.2 is "Hit Rate," not expectancy. "Expectancy" as AdjEdge is in B3.3 (TCF). Do not conflate.
