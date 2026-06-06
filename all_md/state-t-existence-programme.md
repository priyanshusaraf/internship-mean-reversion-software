---
name: state-t-existence-programme
description: State-T observational existence programme (doc 11) — pre-reg signature, frozen probe params, audited integrity status, the two surviving artifact-outs
metadata:
  type: project
---

State-T existence programme = doc 11 (`docs/research/11_state_t_existence.md`). Observational existence ONLY, not detection (frozen boundary, doc 04 §1.4.3/§2.6.4). Output is corpus-level Cohen's-d over distributions, never per-bar.

**Pre-registered T-signature (doc 11 §4, written before data):** high-|z| windows show innov_var↓ / acf1↓ / dir_eff↓ (all three NEGATIVE). Hard-coded identically in doc 11 §4, `scripts/state_t_existence_probe.py`, `scripts/state_t_cohort_probe.py`, `app/services/analytics_state_t.py`. Verified unchanged across all negative results (2026-06-02 audit).

**Frozen probe parameters (Phase 3 == cohort, verified bit-identical 2026-06-02):** θ∈{1.0,1.5,2.0}; W=30; OU-null lam=−0.1; causal z_window=60. Both probes call the same `analytics_state_t.extract/window_descriptors/cohens_d` — no forked/flattered code path. Treat any future deviation from these as parameter drift.

**Result status (post-Phase-5, 2026-06-02):** unanimous NEGATIVE across 12 instruments / 3 resolutions (daily + 60m + 15m) / 2 comparisons. dir_eff POSITIVE everywhere (wrong direction — continuation, not stabilization); within-instrument Section B has only 1 negative cell in the whole table. The canonical HDFC-ICICI pair spread (pre-registered HIGHEST-decisiveness, "fails ⇒ kill-condition met") failed like everything else. **The committed Phase-5 kill condition is MET.** State-T-as-the-pre-registered-morphology is FALSIFIED-IN-FORM for this domain across habitat/resolution. Confidence: drop below LOW. Integrity audit found NO parameter drift, NO signature redefinition, NO selective reporting, NO hidden detection.

**Two surviving outs — RULED (2026-06-02 audit):** (1) substrate-stratification = still LEGITIMATE (pre-existing, near-zero new code, no freeze issue) — but it is a *diagnostic of the negative's cause*, NOT a path back to a positive verdict; if OU-confirmed anchors are still positive-dir_eff, that CONFIRMS the kill. (2) forward post-peak window = the ONE-SHOT license is now SPENT. The pair-spread make-or-break test already resolved negative; running post-peak after a clean canonical-habitat failure would be the renewal the prior ruling forbade. It is NO LONGER a clean pre-existing test — invoking it now to defer the kill = goalpost retreat → REFUSE.

**Why:** This is a falsification-integrity-critical line — the risk is epistemic corruption (post-hoc storytelling, goalpost moves), not freeze violation.
**How to apply:** When auditing this line: (a) Comparison B (within-instrument high-|z| vs low-|z|) is LEGITIMATE confound control — it is strictly MORE adversarial than vs-OU (it killed the CL-BRN A-tease), NOT a goalpost move. BUT doc 11 §2 only contemplates it implicitly ("high-|z| vs the rest"); the named two-comparison framing appeared at results-time, so do NOT let it be written up as "pre-declared in §2" — that overstates provenance (see [[recurring-interpretation-divergence-surfacing]]). (b) The forward post-peak window is a LEGAL final test of out #2 ONLY IF: signature pre-registered before running, it is the LAST window geometry (no third), advisor-reviewed before build, output stays distributional. A third geometry after it fails = goalpost retreat → stop it.
