# Arm A v2 — Cycle 1b: Rolling-Local Stability of the NG Calendar MR (Trader-Persistence) — Pre-Registration

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **FROZEN (hardened by a mandatory pre-freeze three-lens review — trader/adversarial/statistical).**
Windows, the pooled statistic, decision templates, construction-control requirement, shock regimes, and the
trader decision rule are frozen **before any rolling VR on real NG is computed.** Honors the **§11.1 BINDING
GUARD** (rolling is the #1 artifact/DOF surface). Extends doc 21 (NG global confirm, CONDITIONAL SURVIVAL).
**Date:** 2026-06-04. **Mode:** Controlled-Implementation. **Lens mandate:** trader/PM lens REQUIRED (user) —
this is a *deployability* question, not a purity question.

> **The question (trader-first):** *Is NG calendar storage MR **persistent enough across regimes to matter to a
> medium-horizon (1–12 week) trader** — or is the doc-21 global confirm a regime-averaged read a trader could
> not hold?* Six sub-questions (user): (1) stable across regimes? (2) when does it fail? (3) failures clustered
> around shocks? (4) would a trader stay out? (5) deployable or merely true? (6) survives post-2020?

> **REVISION PROVENANCE (§5 honesty).** The first draft used a per-window **binary** flag (`VR(20)<RW-median`).
> The pre-freeze review **falsified that instrument on synthetic ground truth** before any real read: it is (a)
> **underpowered** (genuine OU φ=0.95 flags only ~0.55–0.68 of windows), (b) **non-specific** (pure RW+bid-ask
> bounce flags *higher*, 0.62–0.72), and (c) **blind to vendor back-adjustment** (pure RW + monthly splices flags
> ~0.90, indistinguishable from real MR). A splice-RW *gate* was also rejected — at unknown vendor splice
> magnitude it is either vacuous or toothless (frac=0.5 kills genuine-OU detection to 0.03). The design was
> therefore re-built around a **pooled continuous statistic + construction-controlled corroboration** (below).
> **No real-NG rolling VR was computed at any point in this redesign** — all calibration is synthetic.

---

## 0. Instrument (FROZEN) — pooled mean-z, not a per-window binary flag
- **Per-window read:** VR(q) curve (q∈{2,5,10,20}) on the UNMASKED β=1 calendar within each window, plus the RW
  surrogate **mean & sd** (N=200, identical extraction → surrogate-relative, §11.1). The trader-horizon read is
  **VR(20)** (≈1-month book horizon).
- **Per-window z:** `z_w = (VR(20)_w − mean(RW_surr_VR20)_w) / sd(RW_surr_VR20)_w`. (Standardized distance of
  real VR(20) below its own within-window RW band — the small-sample VR bias self-cancels because the band is
  computed in-window.)
- **PRIMARY persistence statistic (FROZEN):** **pooled mean-z = mean over windows of z_w.** Tested one-sided vs
  the RW template. Power-robust (pools weak per-window signals; the binary count is too noisy/non-specific, §rev).
- **FROZEN synthetic decision templates** (pooled mean-z over 19 yearly windows, measured pre-freeze; ANCHORS not
  pass/fail lines): **RW null = +0.02 ± 0.24, 5–95 = [−0.32, +0.41]** · genuine moderate MR (OU φ=0.95+seasonal)
  **= −0.33** · OU φ=0.97 **= −0.52** · **back-adjustment artifact (splice-RW frac=0.5) = −0.99**.
- **Decision anchors (FROZEN):**
  - **PERSISTENT** iff pooled mean-z **< −0.32** (below the RW 5–95 band) on yearly windows, **corroborated** on
    2-yr blocks **and** on the construction-controlled Brent calendar (§3).
  - **NOT-PERSISTENT** iff pooled mean-z **≥ −0.32** (inside the RW band — sub-diffusion not distinguishable from
    a martingale across regimes).
  - **BACK-ADJUSTMENT-SUSPECT** iff pooled mean-z **< −0.80** (in the splice-RW zone) **AND** the self-built
    Brent calendar does **not** show comparably extreme z — i.e. the extreme persistence is construction-specific
    to the vendor series. (Genuine moderate MR lives at ≈ −0.3 to −0.5; ≈ −1.0 is the splice signature.)
- **Sign-count (secondary, legible only):** # windows with `VR(20) < RW-median` (RW null ≈ 50%). Reported for
  legibility; **never the verdict** (underpowered/non-specific per §rev). The `VR(20)<1` arm is **dropped as
  evidence** (RW-biased to ~0.66 at n=252).
- The strict doc-20 gate is **not** used here (synthetic: ~10% power at 3-yr; uninterpretable on null).

## 1. Windows (FROZEN — deterministic calendar blocks; no peeking; verified peek-free by review)
NG dense era 2006-07-28 → 2026-04-15. **A — yearly (PRIMARY verdict): 2007…2025 (19 windows).** **B — disjoint
2-year blocks (granularity/power view of the SAME data, NOT independent corroboration): 10 blocks.** **C —
recency split: pre-2020 = 2007-2019 (13 yrs); post-2020 = 2020-2025 (EXACTLY 6 yearly windows; 2026 partial
excluded).** Disjoint; full set reported; no argmax. **A is THE verdict; B/C corroborate; if A and B disagree,
A governs and the verdict caps at NOT-PERSISTENT** (no window-scheme argmax). Surrogate N=200; borderline windows
(|z|<0.1) reported with 5-seed stability, counted "ambiguous" if they flip.

## 2. Construction-controlled corroboration (FROZEN — REQUIRED for any PERSISTENT/§11.8-strengthen verdict)
The load-bearing open channel (doc 21) is **vendor back-adjustment**, to which per-window reads are provably blind
(§rev). It is discriminated the **clean** way:
- **Run the IDENTICAL pooled-mean-z instrument on the self-built Brent calendar** (BRN1!−BRN2!, 60m, β=1, built
  from raw ICE legs under *our* roll rule — **no vendor back-adjustment**; doc 21). Window it analogously
  (calendar-half-year or fixed-bar disjoint blocks given hourly density). **PERSISTENT for NG requires Brent to
  show the same-sign persistent pooled-z** (a clean-construction energy calendar must also persist). If only the
  vendor series persists → **BACK-ADJUSTMENT-SUSPECT**, capped, cannot strengthen doc 21.
- **Splice-RW DIAGNOSTIC (reported, not a gate):** report the pooled mean-z of a splice-injected RW (frac∈{0.25,
  0.5}) as the "how strong would back-adjustment need to be" reference. NG's mean-z is read *between* the genuine-
  MR anchor (≈ −0.4) and the splice anchor (≈ −1.0): closer to −0.4 ⇒ MR-like; near −1.0 ⇒ artifact-like.

## 3. Shock regimes (FROZEN a-priori — DIAGNOSTIC ONLY, NOT a verdict input or a deployability filter)
- **S1** GFC/commodity 2008-01-01→2009-06-30 · **S2** oil/gas crash 2014-07-01→2016-02-29 · **S3** COVID/neg-WTI
  2020 · **S4** energy crisis/Ukraine 2021-09-01→2022-12-31. **Computed on the sub-year date intervals** (not
  year-granularity) to avoid boundary mislabeling.
- **DIAGNOSTIC use only:** report pooled-z in shock spans vs calm spans ("where is persistence weakest?"). **This
  is NOT a deployability gate** — see §4. Load-bearing only if the construction-controlled Brent calendar shows
  the same calm/shock gap.

## 4. Trader decision rule (FROZEN) — ex-ante honest, cost-gated; the user's crux closed
**[Review CRITICAL — the ex-post/ex-ante crux.]** An ex-post "stand aside in null/shock years" rule is **NOT
deployable** (a trader cannot know a year's regime at its start; shock dates are hindsight). Therefore:
- **This cycle decides UNCONDITIONAL persistence + deployability ONLY.** A "deploy only in calm regimes" mode is
  **explicitly OUT OF SCOPE** — it would require a *separately-validated, ex-ante, causal* regime classifier,
  which is **State-T-adjacent and DEFERRED** (§10). We do **not** certify any filtered/conditional deployment.
- **Deployability is gated on economics, not significance alone (§11.2 book-after-costs):**
  - **half-life** (per-window & global, from causal AR(1) φ: `ln0.5/lnφ`) must lie in a **tradeable band ≈ 3–40
    bars** (within the 1–12-week hold);
  - **per-cycle reversion amplitude ≫ round-trip cost** (NG calendar 2-leg, ≈ 0.002–0.004 spread units; NG tick
    $0.001); reported **calm and shock separately**;
  - a **minimal causal trade proxy** (§5) must be **net-of-cost positive** unconditionally.
- **VERDICT MAP (FROZEN):**
  - **PERSISTENT-DEPLOYABLE** iff pooled mean-z < −0.32 (yearly) **AND** corroborated (2-yr **and** Brent) **AND**
    post-2020 pooled-z < −0.32 (recency, incl. calm years 2023-25) **AND** half-life in band **AND** trade-proxy
    net-positive.
  - **PERSISTENT-BUT-UNECONOMIC (merely true)** iff persistence holds but half-life out of band OR trade-proxy
    net-negative after cost.
  - **NOT-PERSISTENT** iff pooled mean-z ≥ −0.32 OR post-2020 ≥ −0.32 (decayed).
  - **BACK-ADJUSTMENT-SUSPECT** iff §2 fires (extreme vendor-only persistence).
- **Q4 (stay out?)** is answered honestly: a trader stays out **unconditionally** if NOT-PERSISTENT/UNECONOMIC;
  the calm/shock split is a *diagnostic of where risk concentrates*, **not** a deployable timing rule.

## 5. Minimal causal trade proxy (FROZEN reportable; not a new significance gate)
Per window: causal z-score `z_t=(S_t−μ_{t-1})/σ_{t-1}` (μ,σ = trailing-**60**-bar mean/sd, ≤ t−1). **Enter** when
`|z_t|≥1` (fade), **exit** at `z=0` **or** a **20-bar** stop, **1 unit**. Report **avg net P&L per trade** (gross
reversion capture **minus** frozen round-trip cost 0.003 spread units), **trades/yr**, **hit-rate**, and the
calm-vs-shock split. Fixed rule, no optimization (entry/exit/lookback/cost all frozen here). Answers Q5 directly.

## 6. §11.8 link (FROZEN) · half-life/amplitude
- **STRENGTHENS** doc-21 conditional pass toward deployability iff **PERSISTENT-DEPLOYABLE + Brent-corroborated**.
- **DOWNGRADES** doc-21 iff **NOT-PERSISTENT** (global confirm was regime-averaged) or **BACK-ADJUSTMENT-SUSPECT**
  (the construction-artifact channel doc 21 left open is the likely explanation).
- **PERSISTENT-BUT-UNECONOMIC** leaves doc 21 as-is (apparatus validated; edge not a trader product).

## 7. Guardrails (binding) & disclosure
- **§11.1:** windows/cadence frozen here · surrogate-relative per window (identical extraction) · disjoint windows
  · full set reported · no window-scheme argmax (A governs) · local survival = pooled persistence across MANY
  windows. **No real NG rolling VR computed at freeze time** (synthetic templates only).
- **§6.1 causal:** within-window AR(1)/surrogate/trade-proxy fits use only that window's data ≤ t−1; no
  cross-window leakage; no full-sample normalization.
- **Pilot disclosure:** the *global* NG confirm was pilot-informed (doc 20 §8); the *rolling persistence* read is
  **un-peeked** and is the clean test. Inherited frozen params: UNMASKED β=1, N=200, seed=20260604, q∈{2,5,10,20},
  RW/MA(1) surrogate machinery.

## 8. Pre-run status — FROZEN
Instrument (pooled mean-z + templates), windows (A/B/C, post-2020=6), construction-control requirement (Brent),
shock diagnostic, trader decision map (ex-ante honest, cost+half-life gated), trade proxy, and §11.8 link are
**frozen 2026-06-04, pre-real-rolling-VR.** Execution = slice NG (A/B/C) → per-window VR + RW band → z_w → pooled
mean-z + trajectory → run identical on self-built Brent → splice-RW diagnostic → half-life + amplitude/cost +
trade proxy → calm/shock diagnostic → verdict per §4 → adversarial verification → `23_arm_a_v2_rolling_results.md`.
