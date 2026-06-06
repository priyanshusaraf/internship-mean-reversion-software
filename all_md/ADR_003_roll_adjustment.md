# ADR_003 — Futures Roll Adjustment for Spread Legs

**Status:** ACCEPTED · **Date:** 2026-06-03 · **Frozen invariant** (CLAUDE.md §6; freeze-break requires justification).
**Supersedes:** the prior 0-byte placeholder. **Detailed protocol:** `docs/research/13_canonical_spread_protocol.md`.
**Relates to:** ADR_002 (temporal integrity); `data/mr_cohort_manifest.md` (the audited leg cohort).

## Context
AMR constructs spreads from futures legs. Continuous-contract *roll adjustment* injects artifacts that are
mechanically indistinguishable from — or destructive to — mean-reversion signal. Empirical finding (2026-06-03
roll diagnostic on the leg cohort): **TradingView `1!`/`2!` continuous series are non-back-adjusted (raw-stitched)**
— roll-date jumps are present and periodic (e.g. `SI2!` 37.6% and `GC2!` 12.1% single-day pseudo-returns @
2026-01-30, recurring at ~monthly/quarterly contract spacing). `MIR1!/MIR2!` (FX futures) carry only small roll
gaps and are the cleanest. A frozen rule is required so roll artifacts never enter a reversion statistic.

## Decision (frozen rules)
1. **R-1 — Default disposition: non-back-adjusted.** Treat every continuous (`1!`/`2!`) series as raw-stitched
   until proven otherwise. Detect roll jumps (large pseudo-returns at contract-cycle spacing) and **neutralize them
   before any return/VR/reversion computation** (drop the roll-transition bar, or compute statistics within
   roll-clean segments). Document every neutralized bar.
2. **R-2 — Forbidden adjustments for LEGS.** Additive (Panama) back-adjustment is **forbidden as a spread leg**
   (it injects a drift bias that contaminates MR). Ratio adjustment is **forbidden for cross-leg differencing**
   (rescales units, breaks the level spread). Adjustment used only for *display*, never as the differenced input.
3. **R-3 — Calendar spreads (`1!`−`2!`).** Both legs must share an **identical, causal roll schedule**. Difference
   **Open/Close only** (synchronized observations); **never** naive High/Low (§6 counterfactual-extrema rule).
   Flag the spread's own roll points; handle per R-1.
4. **R-4 — Per-contract preferred where available.** When individual contracts are obtainable, build the continuous
   series ourselves with an **explicit, documented, causal roll rule** (e.g. roll *k* trading days before expiry,
   `k` fixed in advance) — never a roll chosen with hindsight.
5. **R-5 — Negative/level handling.** Spreads cross zero → **level differences only**; log/return/ratio math on the
   *spread* is forbidden (return-space statistics live on the positive *legs*). (Mirrors doc 13 NP-1.)
6. **R-6 — Causality.** All roll handling uses only information available at `t` (expiry calendar is known ex-ante;
   jump-detection thresholds are pre-registered, not fitted to the realized series).

## Consequences
- Clean but conservative: roll-transition bars are lost; `MIR1!/MIR2!` is the cleanest deployable calendar, metals/
  energy legs require active roll handling, and any spread built from raw `1!/2!` legs inherits this obligation.
- Any reversion/VR result computed on un-roll-handled continuous legs is **inadmissible** (a known contamination,
  exactly the class Arm 0 exists to catch). Enforced by the Arm-A pre-registration (doc 18).
