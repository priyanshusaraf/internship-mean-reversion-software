# MRScore (#... v0 block) — Observatory Diagnostic: Build Record & Discrimination Finding

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **MRScore v1 BUILT** as a faithful observatory diagnostic (doc 01 §3, eq. 13–34). The
**engine is correct** (verified: causal-firewall bit-identical, formulas faithful, Monte-Carlo matches
design). The **cross-instrument discrimination claim is WEAKENED** — reliable only *in expectation*,
NOT on a single instrument/window. Authorized under a narrow §10 freeze-break (observability ≠
productionization). **Not wired to any signal/gate** — structurally terminal.
**Date:** 2026-06-02.
**Scope:** the v0 "MRScore" interpretation as an *observe/falsify* instrument. Causal-only; EMA μ*
only; per-bar series + workbench panel (MRS). No validity gate, no RFI, no thresholding.

> **▸ CONTEXT (placeholder framing — frozen).** All empirical reads here are **architecture-level** or
> **ADANIENT-substrate-conditioned** (the synthetics are scale-matched to a 600-bar ADANIENT window).
> ADANIENT is a placeholder, trend-heavy; the deployment domain is expected materially more
> mean-reverting. No market truth is inferred. See `CONTINUATION_STATE.md` §0.

---

## 1. Prior thesis

MRScore (doc 01 §3) is a scalar "Mean Reversion Favorability" = `0.20·B1 + 0.60·B2 + 0.20·B3`, each
block a rank-aggregate of features (B1 reliability: ADF/KPSS, MSI, VSI; B2 strength: DRC, HitRate, VR;
B3 tradability: HL-proximity, vol-compression, tx-cost). Doc 01 §3.1 frames it as **"a detection
instrument, not a prediction instrument."** Working expectation entering the build: MRScore would be
**higher on genuine mean-reverters than on nulls** (the implicit discrimination claim behind any
favorability score).

## 2. Implementation (faithful; `backend/app/services/analytics_mrscore.py`)

- Master eq. 13 and all block/feature formulas implemented to spec (eq. 14–34). Weights frozen
  20/60/20 — economic priors, never fit (§3.2). 252-bar percentile rank, current bar excluded.
- **Temporal honesty (guarded by tests):** causal z standardizes by *shifted* trailing μ,σ (the
  existing `analytics.compute_zscore` includes the current bar — a leak, NOT reused); DRC/HitRate trim
  the last `h` bars; Newey-West HAC (Andrews lag) on DRC; bit-identical future-injection firewall test
  is the standing acceptance bar (passes).
- **Scope decisions (researcher-frozen this build):** causal-only (full-information mode **deferred** —
  no genuine future-using μ* exists; `compute_full_ema` is a warmup variant, not future-using, so a
  "dual mode" on it would be a §6.2 violation dressed as compliance); **EMA μ* only** (Kalman is
  reversion-fidelity-unresolved); **c-free TCF** fallback `max(0,1−VP/100)` (doc 01:714) — no unfrozen
  `c` knob.
- **DOC INCONSISTENCY resolved (MEASUREMENT class).** eq. 28 is typed `…/ln 2` (zeros at HL=5, 20) but
  the same paragraph states zeros at HL=2.5 and 40 (a factor-of-4 band, with economic reasoning). The
  `/ln 2` coefficient is a typo; implemented the prose-stated band `/ln 4`. Flagged, not silently kept.
- **DAG discipline (STRUCTURAL):** MRScore takes μ* as an input series; the module imports from
  `analytics` and is never imported back into the μ*/Kalman paths. Output terminates at display →
  **does not trip the μ* reversion-fidelity reopen trigger** (CONTINUATION_STATE §1; descriptive use).

## 3. New intel — evidence gathered

### FINDING 1 — Intra-instrument rank erases cross-instrument discrimination (**STRUCTURAL**)
eq. 14 ranks each feature within the *instrument's own* trailing 252 bars. A uniformly-reverting OU
has a consistently very-negative DRC → any single bar is "unremarkable vs its own history" → mid rank;
a RW's DRC *wanders*, throwing high-ranking excursions. Net: the **self-ranked B2/MRScore does not
separate reverters from nulls, and inverts.** On the on-disk 600-bar synthetics (mean over scored bars):

| instrument | truth | raw DRC | raw hit | raw vr_agg | **self-ranked B2** | **MRScore** |
|---|---|---|---|---|---|---|
| ANCHOR_OU | OU reverter | −2.30 | 0.565 | 0.579 | 58.2 | 55.6 |
| BLIND_1 | OU reverter | −1.25 | 0.653 | 0.669 | 58.9 | 53.8 |
| NULL_RW | pure RW | −1.40 | 0.564 | 0.638 | **70.1** | **62.5** |
| NULL_DRIFT | drift RW | −2.20 | 0.598 | 0.602 | 50.8 | 47.9 |
| BLIND_4 | pure RW | **−2.79** | 0.678 | 0.401 | 30.4 | 41.6 |

The pure random walk NULL_RW earns the **highest** MRScore. Consequence: MRScore as specified is a
**within-instrument, relative-to-recent-history** favorability score — NOT a cross-instrument
reverter-detector. Cross-instrument classification would need a *shared* rank reference (the deferred
cross-instrument panel, CONTINUATION_STATE §1).

### FINDING 2 — Even raw DRC is unreliable on a single 600-bar real-scale path (**MEASUREMENT**)
The raw Block-2 features were the fallback discriminator (artifact-resistant: DRC uses forward
*returns*, white on a RW). But on single real-scale realizations the discriminator degrades:
BLIND_4 (**pure RW**) drew DRC −2.79 — more "significant reversion" than both genuine OU blinds.

Monte Carlo (n=600, 30 seeds, EMA-20 residual) characterizes it:
- OU(lam=−0.1): mean DRC **−3.15** (sd 0.90, range [−4.53, −1.33])
- RW: mean DRC **−0.58** (sd 1.00, range [−2.59, +1.27])
- 0% of RW paths beat the *median* OU → **discriminates in expectation**;
- **~10% of pure-RW paths draw DRC < −2.0** → a single null can look "significantly mean-reverting."

BLIND_4 is exactly such a tail draw; the genuine OU blinds happened to draw weak DRC → on n=1 they
overlapped. The estimator is not wrong (expectation-level separation is clean and matches the OU/RW
design); single-path inference is the problem.

## 4. Methodology quality
Synthetic ground-truth (OU vs RW), Monte-Carlo over seeds, plus the frozen blind packet (n=1 per type,
ADANIENT-scale). Engine correctness independently pinned by unit tests + the bit-identical causal
firewall. **Limits:** single substrate (ADANIENT scale); n=1 per blind type; no surrogate-null bands
on the raw features yet (§13-style arms remain deferred).

## 5. Confidence update
- **Engine faithfulness / temporal integrity:** **HIGH** (formulas to spec; firewall bit-identical;
  MC reproduces the OU/RW design separation).
- **Discrimination — in expectation (multi-path):** **MEDIUM-HIGH** (clean OU vs RW separation).
- **Discrimination — single instrument/window:** **LOW** (self-ranked score fails/inverts; raw DRC
  ~10% false-positive on nulls). This is the operative confidence for any real, single-instrument use.

## 6. Surviving uncertainty · explicit non-conclusions
- **NOT** concluded: "MRScore detects mean reversion." It does so only *in expectation*; single-window
  reads are unreliable and the self-ranked score is within-instrument relative.
- **NOT** a market claim. The one real segment (BLIND_5 = ADANIENT) is ground-truth-unknown by design.
- **NOT** a signal. No threshold, no gate, no sizing — structurally terminal (freeze-break condition).
- Full-information mode and a Kalman-μ* variant remain **deferred**.

## 7. Next high-information question
Does a **cross-instrument / surrogate-null reference** (rank features against a shared pool or against
per-instrument surrogate-null DRC bands) restore *single-window* discrimination — turning MRScore from
an expectation-level instrument into a usable one-instrument read? This is the natural bridge to the
deferred cross-instrument panel (CONTINUATION_STATE §1). Until then, MRScore is an **observational /
descriptive** instrument; its raw Block-2 features should be read **with sampling caveats**, never as a
single-number verdict.

---

## 8. Adversarial review (2026-06-02) — findings, dispositions, disclosed divergences

Three independent adversarial agents reviewed v1 (empirical runtime / research-alignment / static
code). **Temporal integrity proven sound** (high confidence): full-column future-injection (all 17
output columns, not just `mrscore`) + one-bar endpoint-replay (135,850 cell comparisons) → zero
leakage; bar-`t` exclusion demonstrated directly. **One-way DAG structurally confirmed** (`analytics.py`
has zero mrscore refs; μ* is always an input). **No hidden signal / threshold / verdict / State-T
coupling; observatory-only honored.** All weights and all ten rank directions verified exact.

**Fixed this cycle:**
- **C1 (was the worst issue) — silent failure on non-positive/spread prices.** `np.log(price)` in
  Block 2/3 (eq. 25, 29) is undefined on negative series; the frozen deployment domain (spreads ·
  pairs · cross-asset RV, CLAUDE.md §1.1) and the on-disk `NG12` go negative → engine returned an
  all-NaN score (`n_scored=0`) with no error. Now the endpoint emits an explicit `data_warning`
  ("structural incompatibility, NOT an unfavorable reading") and the panel renders it (red banner +
  no-score notice). **Spread-domain scoring (level-diffs vs returns) is deferred research** — not
  silently approximated.
- **M1 — percentile-rank tie depression.** Strict `<` ranked saturated/capped features (MeanStab=1,
  TCF=1) at 0 (= worst), inverting meaning on flat/degenerate series. Now mid-rank
  (`mean(<) + 0.5·mean(==)`) → constant feature ranks ~50.
- **M4 — warmup honesty.** The panel now distinguishes "warming up (scored 0/N — needs ~280 bars)"
  and "incompatible instrument" from a genuine reading, instead of a silent all-`—` blank.

**Disclosed interpretation divergences (M2/M3 — defensible, recorded here per CLAUDE.md §5 rather
than silently presented as faithful):**
- **M2 — MSI/VSI use residual-σ** (std of ε = P−μ*), where doc 01's glossary defines σ_t as the
  return/level σ. Residual-σ is the z-score denominator and is self-consistent with the rest of AMR;
  it makes drift "in deviation-σ" (matching the doc's "0.5σ" language). Flagged as a choice, not a
  silent claim of fidelity. Block-1 is 20% of MRScore; MSI/VSI together 70% of B1.
- **M3 — ADF lag follows doc 01's literal `⌊(w/100)^¼⌋`**, which collapses to **0 at w<100** (so the
  default 60-bar ADF is an unaugmented DF test). The canonical Schwert (1989) rule carries a leading
  constant (≈12) that doc 01's printed formula omits — same class as the eq. 28 `/ln 2` typo.
  Empirically the lag-0 test still discriminates (OU p≈0.003 vs RW p≈0.90); ADF/KPSS jointly are 30%
  of B1 ≈ 6% of MRScore, and the doc itself down-weights them to "supporting certification only."
  Implemented faithfully to the printed formula; the Schwert-constant question is surfaced for the
  researcher, not silently "corrected."

**Discrimination finding — STRENGTHENED with blind-packet evidence (supersedes §3 FINDING 2's
framing).** On the frozen blind packet, the pure-random-walk `BLIND_4` showed a *significant* DRC in
**97.7%** of its windows vs the genuine-OU `BLIND_1` at only **14.6%** — a single random walk
out-"reverts" the one true reverter. Multi-seed control: RW false-positive rate at the −2.86
threshold is **3.5%** (200 seeds); OU beats RW 10/10 across est_window∈{150,252,300}. Conclusion
unchanged and reinforced: **discrimination is an expectation-level property; single-instrument /
single-window reads are unreliable** — the score is observational, not a classifier.

**Open items deliberately NOT actioned (logged):** crosshair re-render cost and long-series endpoint
latency (G1 ≈ 11s/call) — performance, not correctness; `vc` divide-by-zero is currently safe only
via the rank's finite-filter (guard could be made explicit); discrimination unit test is single-seed
best-case (a multi-seed / "single-instrument-unreliable" test would remove false confidence).
