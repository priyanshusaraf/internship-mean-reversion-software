# Arm A — Execution Parameter Freeze (companion to doc 18)

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **PRE-EXECUTION FREEZE.** Written *after* doc 18's pre-registration and *before any VR(q), surrogate,
or spread is computed.* It fixes the three construction parameters doc 18 deliberately left open (the rolling-β
window, the surrogate-fit procedures, the negative-safe VR estimator) so that none of them can be tuned after a
result is seen. Doc 18 §5's q-grid, surrogate families, N, 5th-percentile threshold, and kill criteria are
inherited verbatim and are **not** re-opened here.
**Date:** 2026-06-03. **Mode:** Controlled-Implementation (authorized). **Nothing computed at write time.**
**Relates to:** doc 18 (pre-registration), doc 13 + ADR_003 (construction law), doc 14 (VR ontology),
`waiting_period/red_team_critique.md` (binding: real−surrogate only), `data/mr_cohort_manifest.md` (the legs).

> **Why this exists.** doc 18 froze *what* is tested and the *decision rule*. It left three knobs unspecified:
> the rolling-β lookback `W`, the exact surrogate-parameter fits, and how VR is computed on a sign-crossing
> spread (doc 13 NP-1 forbids log/return transforms there, so the frozen Substrate VR — which uses log-prices —
> cannot be reused as-is). Each knob moves the verdict. doc 14 DANGER-1 names "full-sample-tuned window/horizon"
> as the highest-likelihood leak. The only defense is to freeze them a-priori, with justification, on the record,
> before any statistic exists. That is this document.

---

## F1 — Hedge-ratio construction (per spread) + rolling-β window & cadence

**β policy per spread is inherited from doc 18 §2 / doc 13 §1.6 (habitat→β map) and is NOT re-opened:**

| # | Spread | Legs (raw, from manifest) | β policy | Role |
|---|---|---|---|---|
| 1 | **HDFC–ICICI** | `BSE_DLY_HDFCBANK`, `BSE_DLY_ICICIBANK` | **rolling-β** (HR-2) | **DECISIVE** |
| 2 | **Gold–Silver** | `COMEX_DL_GC2!`, `COMEX_DL_SI2!` | **rolling-β** (HR-2) | **DECISIVE** |
| 3 | **USD/INR calendar** | `CME_MINI_DL_MIR1!` − `CME_MINI_DL_MIR2!` | **β = 1** (HR-1, definitional) | reference (cleanest) |
| 4 | Gold–Copper | `COMEX_DL_GC2!`, `COMEX_DL_HG1!` | rolling-β | cohort |
| 5 | Platinum–Palladium | `TVC_PLATINUM`, `NYMEX_DL_PA1!` | rolling-β | cohort |
| 6 | WTI–Brent | `CFI_WTI`, `ICEEUR_DLY_BRN1!` | rolling-β | cohort |
| 7 | TCS–INFY | `BSE_DLY_TCS`, `NSE_DLY_INFY` | rolling-β | cohort (cross-venue) |

**FROZEN — the one new decision (the rolling-β knob), justified a-priori, never result-selected:**
- **Window `W = 60` daily bars.** Justification: Avellaneda–Lee (2010) use a 60-day estimation window for
  equity stat-arb (cited in doc 14 §6); it is the canonical short pairs lookback. Chosen *before* any VR.
- **Cadence: re-fit every bar** (walk-forward), OLS of leg A on leg B over the trailing window.
- **Lag: `β` estimated on data `≤ t−1`, applied at `t`** (C-3, the load-bearing rule). Bit-identical
  future-injection acceptance test required (a future bar must not change any earlier β or spread value).
- **Warm-up: first `W` bars masked (NaN), never imputed** (C-2).
- **`W = 120` is computed only as a NON-VERDICT robustness display.** The verdict is read at `W = 60`.
  Selecting whichever `W` "looks more reverting" is forbidden (doc 14 D1). If the two disagree, that is reported
  as fragility, not resolved by picking one.
- β=1 calendar (MIR) has **zero** hedge-ratio DOF and no warm-up beyond the inner-join.

## F2 — Matched surrogate fits (the three frozen families, doc 18 §5)

All surrogates: **N = 200 draws each**, **identical length** to the real roll-clean spread, **identical
roll-handling and VR extraction**, parameters estimated **causally** and **never tuned so the surrogate's VR(q)
matches the real's** (doc 18 §5; red-team bias-cancellation requirement — the surrogate must carry the *same*
finite-sample / overlapping-window VR bias as the real so that real−surrogate nets it out).

- **RW (primary null).** I.i.d. Gaussian increments, `σ = sample SD(ΔS_real)` on the roll-clean spread.
  A martingale level (VR=1 in expectation); its N=200 ensemble *is* the finite-sample null distribution of VR.
  Beating it ⇒ genuine sub-diffusive linear structure beyond i.i.d. noise.
- **GARCH(1,1).** Zero-mean GARCH(1,1) **fit by QMLE to `ΔS_real`** (`arch` 8.0.0, stack-sanctioned §8),
  then simulated as a **martingale level** (cumulated zero-mean GARCH increments — no reversion injected).
  Beating it ⇒ the sub-diffusion is not a volatility-clustering artifact.
- **OU.** AR(1) on the **level**: `S_t = c + φ·S_{t−1} + e_t`, `φ̂, σ̂_e` estimated on the real (a generic
  reverting null, **not** a full-sample MLE tuned to reproduce the real VR curve). Beating it ⇒ the real is
  *more* cleanly sub-diffusive than a plain OU fit — the stringent leg of the test. Reported per-family so the
  verdict stays legible if OU behaves as a calibration control rather than a pure null.

> **Surviving ambiguity (resolved conservatively, recorded):** doc 18 says "below 5th percentile across **all
> three** families." The RW/GARCH nulls are martingales; the OU null is itself reverting, so "beat OU too" is a
> deliberately hard bar. We do **not** relax it. We report the per-family separation transparently; a
> CONFIRMED verdict requires the conjunction doc 18 froze. If a spread beats RW+GARCH but not OU, that is
> reported as **partial / not-confirmed**, never re-storied into a pass.

## F3 — VR(q) estimator on a sign-crossing spread (negative-safe; doc 13 NP-1)

- **Level-difference variance ratio** (additive, defined through zero):
  `VR(q) = Var(S_t − S_{t−q}) / (q · Var(S_t − S_{t−1}))`, computed on the **spread level `S`** (Open/Close
  only), **never on log-prices or returns** (forbidden on a series that crosses zero — NP-1). This is the
  negative-safe analogue of Lo–MacKinlay; doc 18 §3 mandates "level-difference returns." `< 1` ⇒ sub-diffusive
  (mean-reverting), `≈ 1` ⇒ random walk, `> 1` ⇒ persistent.
- **Frozen horizon grid `q ∈ {2, 5, 10, 20}`** (doc 18 §3; extends the Substrate engine's `{2,5,10}`). Reported
  as a **curve**, never `min()`-collapsed.
- **Lo–MacKinlay heteroskedasticity-robust `z*` is reported** alongside each VR(q) for context, but the
  **verdict rests on the surrogate ensemble** (doc 18 §5), not on the asymptotic z* (which is itself
  small-sample-biased — doc 14 red-team). Overlapping q-differences, `ddof=1`.
- **Canonical observable = Close** (OHLC-2). **Open** used only for an Open/Close construction cross-check.
  **High/Low never touched** (OHLC-3: counterfactual for constructed spreads).

## Roll & data-hygiene handling (ADR_003; frozen, pre-result)

- **Continuous-futures legs only** (`GC2!`, `SI2!`, `HG1!`, `PA1!`, `BRN1!`, `MIR1!`, `MIR2!`): flag bar `t` as a
  **roll transition** if that leg's 1-bar log-return `|r_t| > 8 × (trailing-60-bar MAD of r)` — a **causal**
  robust-scale gate with the **multiplier 8 frozen** (R-6: threshold pre-registered, not fitted to the realized
  path). Flagged increments are **masked**; q-differences are formed **only over mask-free spans** (roll-clean
  segments). Every masked bar is counted and reported per leg. Equity/CFD/composite legs have no roll → no
  roll-mask. (Sanity target from ADR_003: `SI2!`/`GC2!` ~2026-01-30 jumps must be caught.)
- **WTI–Brent: post-2011 only** (legs trimmed to `date ≥ 2011-01-01`; documented 2010 structural break).
- **Platinum–Palladium:** drop degenerate proxy bars (`O=H=L=C`) from the `TVC_PLATINUM` composite leg before
  alignment (manifest flag).
- **Alignment: inner-join on UTC timestamps** (AL-1); positional/index merges forbidden (C-5). Cross-venue pairs
  (TCS–INFY BSE/NSE; WTI CFD vs Brent ICE) inner-join only.
- **Degenerate-bar robustness:** flat (`O=H=L=C`) leg bars (e.g. early illiquid HDFC) deflate increment variance
  and can manufacture apparent stillness; per-spread flat-bar fraction is reported, and "flat-bar-trimmed" is
  carried as a **frozen robustness subsample** alongside "roll-clean."

## Decision rule & kill criteria (inherited verbatim from doc 18 §5 — restated for one-page execution)

- **CONFIRMED** for spread X iff real VR(q) `< 5th percentile` of X's matched-surrogate VR ensemble at **≥1
  frozen horizon**, **robust across (a) all three families** (RW, GARCH, OU) **and (b) roll-clean subsamples**.
- **KILL / strong-negative:** no spread separates from its matched surrogate at any horizon ⇒ deployment-domain
  MR premise **seriously damaged**. If **both DECISIVE** (HDFC–ICICI, Gold–Silver) fail ⇒ seriously damaged even
  if a cohort instrument squeaks through.
- **No re-story:** real VR `>` surrogate ⇒ weakened, no post-hoc reinterpretation.

## Hard guardrails (doc 18 §6 — binding)
Causal (β & surrogate params on `≤ t−1`; future-injection bit-identity test) · Distributional (corpus verdict,
no per-bar series, no "T" column, no timing) · Roll-handled (un-handled = inadmissible) · Surrogate-relative
(raw VR inadmissible as evidence) · μ\*-independent (no Kalman/EMA residual; does not trip doc-06 §15.8) ·
No tuning to manufacture separation · No latent-state model. Banned vocab in code/docs/UI: T-score, hazard,
ignition, imminent, signal, entry, favorable-now.

---

## Decision-rule completion — ratified 2026-06-03, PRE-REAL-DATA (synthetic controls only)

doc 18 §5 left two clauses under-specified; a literal reading of each is statistically broken. Both were
resolved from first principles and validated on **synthetic ground-truth controls before any real spread was
constructed** (proper synthetic-validation practice, doc 08), then ratified by the Chief Scientist. **No real
cohort statistic existed at ratification.** The literal readings remain **computed and reported** for every
spread; the ratification fixes only the *headline* verdict.

1. **OU surrogate = stringency REFERENCE, not a veto (the verdict gate = RW + GARCH martingale nulls).**
   *Evidence:* a textbook OU (φ=0.8) separates from RW/GARCH at every horizon but **cannot** beat an OU
   surrogate fit to itself (it sits inside its own ensemble) — so "must beat all three" has **no achievable
   positive control**, and a "nothing confirmed → KILL" under it could be a self-fit-OU artifact, not evidence
   of absent MR. CONFIRMED therefore means *"distinguishable from a random walk"* (the economically meaningful
   question; doc 12 Arm A). "Also exceeds a causal OU" is recorded as a bonus, never required.
2. **Significance = multiplicity-corrected min-VR statistic, not the naive ≥1-of-4 per-horizon rule.**
   *Evidence:* measured pure-random-walk false-positive rate of the naive rule = **10.0%** (6/60) — 2× the
   *frozen* 5% (multiplicity across 4 horizons). The corrected statistic (real best-horizon VR vs the
   surrogate's **own** best-horizon null) measures **1.7%** FPR with **100%** power at φ∈{0.95,0.9,0.8}
   (half-lives 13.5/6.6/3.1 bars). This **honors** the frozen 5% (the naive rule violates it) and the surrogate
   null absorbs the same horizon search, so it is not horizon-cherry-picking (doc 14 §4 conditions satisfied).

These are **completions of doc 18's own under-specified clauses to make the frozen 5% and the kill criterion
honest**, not changes to any frozen quantity (q-grid, N, 5% threshold, families, cohort, kill rule all
unchanged). Headline `confirmed` = multiplicity-corrected separation from RW **and** GARCH, robust across
roll-clean + flat-trimmed subsamples; `confirmed_all_three` and the naive per-horizon reading are reported
alongside for full transparency.

**Freeze status:** F1, F2, F3, the roll/hygiene rules, and the ratified decision-rule completion above are
**frozen as of 2026-06-03, pre-real-data.** Any change after the first real VR(q) is a freeze-break requiring
explicit justification (CLAUDE.md §6). Engine built and gated on 9 causal-firewall + ground-truth tests
(future-injection bit-identity, negative-safe VR, roll detection, character recovery, FPR/power calibration) —
all green. Next: **execute across the 7-spread cohort.**
