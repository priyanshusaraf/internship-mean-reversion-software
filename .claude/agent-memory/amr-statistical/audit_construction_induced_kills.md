---
name: audit-construction-induced-kills
description: Frozen level-β spreads on ratio-drifting pairs manufacture VR≈1 — the kill is construction-induced, not market evidence. Check before crediting any spread VR kill.
metadata:
  type: project
---

When auditing spread VR results, a kill (VR≈1 / super-diffusive) is **construction-induced, not market evidence** when:
the spread is a FROZEN LEVEL-β object (S=Leg1−β·Leg2, β fixed from a presample) AND the underlying
price ratio drifts across the test window. A static level-β cannot track a drifting ratio, so the
residual inherits the ratio's secular trend as super-diffusion. The level-spread VR is then a near-
guaranteed ≈1, independent of whether the pair mean-reverts.

**Diagnostic (doc 49 GC-SI, verified 2026-06-10):** trend share of level-spread variance = 0.646
(65% of Var(spread) is a deterministic linear trend). VR(20) level = 1.007 (super-diffusive). Same
window, log-ratio framing: VR(20) = 0.947 (sub-diffusive). OOS: level VR 0.642 vs log VR 0.797.
Construction choice flips the verdict sign → the level-spread choice doomed the sub-diffusion test ex ante.

**Why:** doc 42/19 family of failures — wrong spread construction manufactures the statistic. For
ratio-cointegrated pairs (gold-silver is the textbook case) the admissible object is log-spread /
log-ratio, NOT a frozen level-β. The prereg listed log-spread as "informational only, cannot override
the kill" — that ordering is itself the defect: it pre-committed to the inadmissible construction.

**How to apply:** for any frozen-level-β spread kill, compute (a) ratio drift across the window,
(b) trend share of level-spread variance, (c) log-spread VR for the SAME window. If trend share is
large and log VR < 1 while level VR ≈ 1, label the kill CONSTRUCTION-INDUCED (METHODOLOGY defect),
NOT a market finding. β=1 definitional same-unit calendars are exempt; estimated-β cross-level spreads
are the risk surface. Distinct from the §11.8 apparatus question — a construction-induced kill is not
an apparatus power failure, it is a wrong-object error.
