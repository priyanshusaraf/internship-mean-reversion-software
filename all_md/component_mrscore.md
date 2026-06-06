---
name: component-mrscore
description: MRScore v1 implementation status, file map, and the audited research-to-code mappings (doc 01 §3 eq.13-34)
metadata:
  type: project
---

MRScore v1 is BUILT, audited faithful + freeze-compliant (Yes-with-conditions). Observatory diagnostic, structurally terminal (no gate/RFI/signal consumes it). Authorized under narrow §10 freeze-break (observability != productionization).

**File map:**
- Engine: `backend/app/services/analytics_mrscore.py` — eq.13-34 faithful. One-way DAG: imported ONLY by `market.py`; `analytics.py` has zero mrscore refs (verified grep both directions). Takes μ* as input, never feeds back.
- Endpoint: `backend/app/routers/market.py` GET `/{id}/mrscore` (line ~317) + `_MRSCORE_REGIME_WARNING` (line ~31).
- Models: `backend/app/models/market.py` MRScoreRow/Stats/Response.
- UI: `frontend/src/components/workbench/modules/MRScore.tsx` (registry id `mrscore`, shortLabel MRS). No verdict/threshold language. Regime warning rendered as prominent amber strip.
- Tests: `backend/tests/test_mrscore.py` (32 tests, incl. bit-identical causal firewall).
- Build record: `docs/research/09_mrscore_observatory.md`.

**Audited-correct (do not re-verify unless code changes):** master 20/60/20; B1 .30/.50/.20; B2 .50/.30/.20; B3 1/3 each; ALL 10 rank directions correct (no inversions); eq.14 prior-W exclude-current; VP_t include-current (defensible — glossary defines VP as incl-today); Newey-West HAC + h-trim; causal-z shifted μ,σ; c-free TCF; EMA-only no Kalman; dual-mode honestly DEFERRED not faked (mode="causal").

**Two known interpretation divergences from doc 01:**
1. HL band uses `/ln4` not eq.28's `/ln2` — LEGITIMATE: eq.28 formula contradicts its own prose ("0 at 2.5/40" needs ln4). Surfaced + justified per §6 in code comment + doc 09 §2 + CONTINUATION_STATE §3. COMPLIANT. (Nit: doc 01 itself not annotated with erratum marker.)
2. **MSI/VSI use residual-σ (close−EMA) not glossary's return-σ (σ_t)** — defensible (self-consistent with residual z-score) BUT NOT surfaced anywhere as a divergence. The single worst drift found. Documentation-only fix: flag in doc 09 §2. See [[recurring-interpretation-divergence-surfacing]].

Audit verdict 2026-06-02: zero CRITICAL/HIGH. All findings MEDIUM/LOW, documentation-honesty only.
