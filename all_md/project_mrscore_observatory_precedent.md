---
name: mrscore-observatory-precedent
description: MRScore v1 is the governing structural precedent for any new observatory layer (the shape a legal scoring layer must mirror)
metadata:
  type: project
---

MRScore v1 (doc 09, `backend/app/services/analytics_mrscore.py`) is the canonical template
any new observatory/scoring layer must mirror to stay legal under §10.

The pattern that made it legal:
- Causal-firewall **bit-identical** (full-column future-injection test is the standing acceptance bar).
- Formulas **frozen to economic priors, never fit** (weights 20/60/20 fixed).
- **One-way DAG**: takes μ* as input, never imported back into μ*/Kalman/signal paths (`analytics.py` has zero refs to it).
- **Structurally terminal**: terminates at display (per-bar series + workbench panel). No threshold, no gate, no sizing, no State-T coupling.
- Authorized under a **narrow §10 freeze-break** (observability ≠ productionization), recorded in the research archive per §5.

Key empirical finding (don't re-litigate): MRScore **discriminates reverters from nulls only IN EXPECTATION** (multi-path). Single-instrument/single-window reads are unreliable — the self-ranked score inverts (pure RW scored highest), and raw DRC draws ~3.5-10% false positives on null paths. So it is observational/descriptive, NOT a classifier. Full-information mode and a Kalman-μ* variant are deferred (no genuine future-using μ* exists, so a "dual mode" on EMA warmup would be a §6.2 violation dressed as compliance — a real trap to watch for).

**Why:** Established and reviewed/remediated/frozen 2026-06-02; it is the only built v0 observatory and the cleanest available precedent.
**How to apply:** When auditing or advising on a new scoring layer (e.g. market taxonomy, see [[state-t-freeze-boundary]]), require it to replicate this exact shape — causal firewall, frozen transparent weights, one-way DAG, terminal-at-display — and flag any deviation (fit weights, gate wiring, latent-state model) as drift.
