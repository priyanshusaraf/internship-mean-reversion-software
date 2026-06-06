# EXECUTION STATE SNAPSHOT

**As of:** 2026-06-04 · **Mode:** EXECUTION (frozen programme — no redesign). · **Governing docs:** 33 (frozen prereg), 32 (trader-first), operator playbook.

> Read this page + doc 33 and resume instantly. Nothing else required to execute.

## Objective
Find **ONE deployable calendar sleeve** (positive net expectancy after costs) **or kill the calendar thesis** — fast. Not coverage, not ontology, not understanding.

## Frozen assumptions (do not relitigate)
- **Live levers = carry + netting.** Selectivity is DEAD (doc 31, A_FALSE_RESCUE). NG reversion-timing uneconomic (doc 23).
- **Ledger:** `E_net = G + C_carry − K/η`. `G` frozen-measured (no re-tune). Netting → cost only. Margin offset ≠ `E_net`.
- **Instruments:** NG, Brent, Corn — β=1 definitional, raw-leg back-adj-clean.
- **Frozen seasonal splits:** NG withdrawal(Nov–Mar)/injection(Apr–Oct); Corn old-crop(Mar–Aug)/new-crop(Sep–Feb); **Brent unconditional only**.
- **Confirmatory cells = 3:** NG.withdrawal, Corn.old-crop, Brent.unconditional. All else NON-CONFIRMATORY.
- **Frozen params (doc 33 §6):** K=0.003, η∈{min(M,3),1.5,1}, z0=0.5, jump-k=8, jackknife sign ≥⌈0.6·N⌉ & <100% single-year leverage.

## Active track
Doc 33 execution. Trigger = `NG1!/NG2!` 1D legs arrive (BRN/ZC incoming). DAG: raw legs → β=1 spread → causal firewall → carry (raw ΔS, deseason OFF) → seasonal partition → 4 gates → Stage-0 ledger → A/B/C/D.

## Exact current bottleneck
**Raw-leg quality + NG back-adjustment separability (Gate 1 + Gate 2).** Voids everything downstream if unresolved — same channel doc 23 could not close.

## Next executable action
Acquire `NG1!/NG2!` 1D → build 3 spreads → run causal firewall (Week 1). Then Week-2 unconditional carry.

## Hard stop / checkpoint conditions
- **Week-2 checkpoint:** clean AND economically meaningful unconditional carry on ≥1 instrument (Gate1+Gate2 pass, `C_carry` non-trivial vs cost).
  - PASS → Week-3 seasonal. FAIL → **skip Week 3, go to Week-4 adjudication.**
  - EXCEPTION: carry exists but is plausibly seasonally concentrated by prereg logic → Week-3 justified for that instrument only.
- **Gate fail = void:** firewall fail → drop instrument; roll-cadence aligns boundary → seasonal read VOID; jackknife >100% leverage → dead.
- **Verdict (Week 4):** A → book v0 · B → named-month acquisition (that pair) · C → instrument dead · D → construction dead · all C/D → **KILL thesis, escalate flow-data procurement.**

## Forbidden during execution
New ontology · substrate expansion · re-tuning `G` · reading non-confirmatory cells · argmax-month headlines · boundary nudging / shoulder tuning · margin-offset in `E_net` · refined-product acquisition without a NEW prereg · any redesign unless a hard gate (firewall / roll-cadence / §6 param assert) fails.
