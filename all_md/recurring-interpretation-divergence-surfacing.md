---
name: recurring-interpretation-divergence-surfacing
description: Audit pattern — when code defensibly reinterprets a frozen spec, CLAUDE.md §6 requires it be SURFACED, not silently presented as faithful
metadata:
  type: feedback
---

When auditing AMR code against research docs: a defensible interpretation choice that departs from the frozen spec/glossary must be explicitly surfaced (in the build-record doc and CONTINUATION_STATE), even when the choice is likely correct. Silent reinterpretation presented as "formulas to spec" is the recurring drift class to flag.

**Why:** CLAUDE.md §6 (frozen invariants) requires surface+justify before departing from a frozen item. The HL `/ln4` case did this correctly (code comment + doc 09 + CONTINUATION_STATE). The MSI/VSI residual-σ-vs-return-σ case did NOT — it was the single worst drift in the MRScore audit precisely because it was defensible but unflagged.

**How to apply:** During fidelity audits, separate "is the math defensible?" from "was the divergence disclosed?" Both must pass. A defensible-but-undisclosed divergence is a MEDIUM finding (provenance/honesty gap), not a pass. Distinguish from the HL case: HL was disclosed → LOW/clears. Check doc 09 §2 and CONTINUATION_STATE §3 for disclosure when judging.
