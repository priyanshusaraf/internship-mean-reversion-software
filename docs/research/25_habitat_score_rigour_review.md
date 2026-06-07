# 25 — Habitat-Score Apparatus Rigour Review (Candidates A · B · C + What Else Is Missing)

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **METHODOLOGY REVIEW — verdicts are recommendations, not freezes.** No code touched, no data read,
no kill-ledger entry written. Pre-registration requirements (§7) bind any item before it is implemented.
**Date:** 2026-06-07. **Mode:** Research. **Method:** four-lens decomposition (adversarial · statistical ·
trader/PM, each re-running the engines via Bash against the live source) synthesised by research lead.
**Governs:** the MR habitat-score apparatus (`analytics_habitat.py`) and the doc-20 positive-control path
(`analytics_arm_a_v2.py`).
**Provenance:** the three lenses verified every claim below against the shipped code and the κ-noise-floor /
μ\* lag-illusion dossier (docs 03 §7.1, 04 §1.5, 06 §15.8, 07). Disagreement is preserved, not averaged.

> **Headline for the governor (read first).** Two findings dominate everything else. **(1) The apparatus you
> asked me to improve is not the apparatus that ships.** The RW∧GARCH∧MA(1) triple-AND gate, q∈{2,5,10,20},
> N=200 you described is the doc-20 *positive-control* path (`evaluate_v2`). The **live** habitat scorer
> (`habitat_score_full`) is materially weaker: **RW + MA(1) only — no GARCH**, q∈{5,10,20}, N=2000, and a
> **continuous percentile** with **no frozen α and no panel-multiplicity control.** **(2) All three proposed
> additions are net-negative or redundant as proposed.** A and B both estimate the near-unit-root AR(1) root
> the State-T dossier already killed (doc 04 §1.5), on a *fitted* μ\* that manufactures reversion from a pure
> random walk; C is the killed MRScore/State-T predictive detector in regression costume. The real wins are
> elsewhere: **fix the live scorer back up to its own validated spec, add a distribution-free VR test, and
> formalise disjoint-window survivability** — none of which is A, B, or C.

---

## 0. Executive Summary

The level-difference variance ratio VR(q) is a sound headline statistic and the surrogate-relative percentile is
a defensible *descriptive* read. But the shipped scorer has drifted below its own frozen positive-control
prereg (doc 20): GARCH is absent from the live gate, the score is a continuous percentile with no rejection
rule, and multiplicity across the rolling-window panel is uncorrected (§11.1 BINDING GUARD violated by
omission). This is the baseline against which A/B/C must be judged — and it matters, because every proposed
addition would be bolted onto a scorer that is already weaker than the apparatus that was validated.

Against that baseline: **A (ADF/KPSS on ε=price−μ\*) — REJECT (HIGH).** It is a derived restatement of the same
φ that VR(q) already integrates, it has the lowest power exactly in the φ≈0.9–0.99 habitat region (and KPSS the
worst size there), and on a *fitted* μ\* it fires "stationary" on 100% of pure-random-walk seeds (lag illusion,
doc 07; would trip the doc-06 §15.8 freeze the live path is careful not to touch). **B (half-life τ=ln2/κ as a
gate) — split verdict, net ADOPT-WITH-GUARDS the *economic dimension* / REJECT the *proposed estimator*
(MEDIUM).** The trader is right that holding-horizon-vs-cost is the one missing P&L lever; the statistical and
adversarial lenses are right that a *point κ from an AR(1) on the fitted residual, used as a hard gate*, is
exactly the demoted near-unit-root κ object (doc 04 §1.5.3: Δκ below the noise floor; τ=−ln2/lnφ has dτ/dφ→∞
as φ→1). The need survives; the instrument does not — replace it with a model-free reversion-timescale +
adverse-excursion read. **C (DRC, forward-return-on-z) — REJECT for this apparatus (MEDIUM-HIGH).** It fires
β<0 on 67% of pure-RW seeds (selection-on-deviation), correlates +0.87 with min-VR by construction, and a
per-bar forward-conditional reversion expectation indexed on z_t *is* the killed State-T / MRScore-as-signal
object regardless of vocabulary. The statistical lens grants it is the only candidate with orthogonal (signed,
multi-horizon) content, but only after Stambaugh + Hodrick correction and never as a gate — which is no longer
a habitat-score addition.

The highest-value next actions are not A/B/C. They are: reconcile the live scorer to its validated spec
(restore GARCH, freeze α, correct panel multiplicity); add the **Wright (2000) rank/sign VR with the
Chow–Denning (1993) joint statistic** (distribution-free, heteroskedasticity-robust, analytic multiplicity —
fixes the baseline defect with provable size); and formalise **disjoint-window VR survivability** (the §11.1
anti-cherry-pick discipline the score currently omits). Full ranking in §6.

---

## 1. Current Apparatus — What It Does and What It Cannot Do

**What it computes.** For a window of level series `x` (a β=1 spread or price), `min_vr(x)` takes the minimum of
VR(q)=Var(x_t−x_{t−q})/(q·Var(Δx)) over q∈{5,10,20}. `habitat_score_full` builds a null cloud of `NS_NULL=2000`
surrogate min-VRs — **half RW (iid, vol-matched), half MA(1) (vol-matched to the real increment ACF(1))** —
and returns `score = 100·mean(null_min_vr ≥ real_min_vr)`. High score ⇒ the window sub-diffuses more than its
own martingale-class surrogates ⇒ candidate mean-reverting habitat. Validation on record: FPR 3.0% on 200 RW
seeds, MA(1)-noise discrimination, Brent-calendar corroboration.

**What it is good at.** VR(q) integrates the autocovariance structure across horizons and is robust relative to
a single-lag autocorrelation; the surrogate-relative construction cancels finite-sample VR bias (real and
surrogate run through *identical* extraction); the MA(1) null specifically defends against bid-ask-bounce /
non-synchronous-settle sub-diffusion masquerading as MR (doc 20 §5). This is a genuinely defensible
*observational* instrument and should not be casually redesigned.

**What it cannot do — and the divergence finding (all three lenses, independently).** The apparatus the
governor described is **not** the shipped scorer:

| | Governor's description / doc-20 `evaluate_v2` | LIVE `habitat_score_full` |
|---|---|---|
| Nulls | RW ∧ GARCH ∧ MA(1) (OU non-gating ref) | **RW + MA(1) only — NO GARCH, NO OU** |
| q-grid | {2,5,10,20} | **{5,10,20}** (q=2 dropped) |
| N | 200 | **2000** |
| Statistic | multiplicity-corrected min-VR **p-value**, 5th-pct **hard gate**, `real_min<1` required | **continuous percentile** `100·mean(null≥real)` — no α, no decision rule |

Three consequences, each a real limit of the *deployed* instrument:

1. **No size control / no multiplicity correction.** The continuous percentile emits a number per window with no
   rejection threshold and no family-wise correction across the rolling-window panel. §11.1's BINDING GUARD
   ("multiplicity controlled across windows") is satisfied by the doc-20 p-value path but **not** by the live
   percentile. A continuous color is a *ranking*, admissible as description; it is **not** a significance
   statement, and must not be read as one. *(STRUCTURAL/METHODOLOGY.)*
2. **GARCH is absent from the live gate.** Vol-clustering can manufacture VR<1 that RW and MA(1) do not absorb;
   doc 20 §5 made GARCH a *mandatory* headline gate. Its omission means the live scorer is **weaker than its own
   validated prereg.** *(METHODOLOGY.)*
3. **It scores one window.** It cannot distinguish a persistent reverter from one whose VR<1 is carried by a
   single sub-epoch (the regime-conditional NG failure mode, registry kill #3) — §11.1's "persistence across
   MULTIPLE disjoint windows, never appearance in one" is not implemented.

Crucially, the live scorer operates on the **raw level** `x`, not on ε=price−μ\*. It therefore carries **none**
of the μ\* construction-illusion surface. Candidates A and B would *introduce* that surface. This is the single
most important framing for what follows: **A and B are not free additions — they add artifact surface the
current scorer does not have, in exchange for information VR already encodes.**

---

## 2. Candidate A — ADF/KPSS on the Kalman Residual ε = price − μ\*

**Proposal.** Run a stationarity test (ADF / KPSS) on ε=price−μ\* rather than VR on raw price, on the argument
that VR on raw price can sub-diffuse spuriously when μ\* drifts, whereas ε tests "do deviations from equilibrium
revert."

**Adversarial.** Decisive kill. On a *pure random walk* (zero MR), the residual ε against a causal trailing-mean
μ\* shows a negative ADF coefficient in **100% of seeds**, while raw price is flat — subtracting *any* fitted
trailing equilibrium fabricates reversion (the doc-07 lag illusion). ADF on a trending leg with a lagging μ\*
will reject the unit root precisely *because* μ\* catches up, "confirming" a habitat on a pure trend. It adds
nothing VR does not already integrate (both are monotone in φ for an AR(1) residual), and it would trip the
doc-06 §15.8 μ\*-freeze that the live path explicitly avoids. **KILL** as proposed; independent-of-VR: **NO**.

**Statistical.** **INADMISSIBLE-AS-EVIDENCE** (STRUCTURAL: derived restatement of the VR-φ axis; compounded
METHODOLOGY). Under an AR(1) residual, ADF and VR(q) are both deterministic functions of φ̂ — A's only
orthogonal content is its lag-augmentation (higher-order AR) and KPSS's stationarity framing. Sample adequacy
is poor where it matters: ADF has **notoriously low power near the unit root** (cannot separate φ=0.95 from
φ=1 at n≈250–1000 — the entire habitat region), and its **size blows out to 30–60%** under MA(1) errors
(Schwert 1989) — and these spreads *carry* MA(1) microstructure by construction (doc 20 §5). Plain ADF is the
wrong estimator; DF-GLS (Elliott–Rothenberg–Stock 1996) is mandatory if A is admitted at all. KPSS over-rejects
stationarity under near-integration and is acutely lag-truncation-sensitive. A inherits the κ near-unit-root
bias directly (Yu 2012; SD(κ̂) ≫ κ). Salvage exists only as *DF-GLS with a reported CI (never a point reject) +
surrogate run through the identical ADF pipeline* — at which point it is a redundant, weaker echo of VR.

**Trader.** **MARGINAL.** A second stationarity stamp on an object VR already characterises. The one scenario
it changes a decision (borderline VR≈55, ADF p<0.01) is a window a 0.005-cost-floor book would skip anyway; and
ADF power is weakest at the 200–500-bar window lengths where habitats are scored. It maps to no holding period
and no P&L number. Reduces (nominally) false positives, but worst exactly where they arise.

**Verdict A — REJECT (as proposed). Confidence: HIGH.** Three-lens convergence to negative; the μ\* illusion is
empirically demonstrated (100% false-fire on pure RW), the instrument is a derived transform of VR, and it
breaks the §15.8 freeze for information VR already carries. *Evidence that would reopen:* a **β=1 definitional /
same-unit residual** (zero fitted-μ\* DOF, e.g. a calendar spread is itself "price − the other leg") tested
with **DF-GLS + CI + surrogate-through-identical-extraction** — and even then it must clear that it adds
non-redundant power over VR on the same series, which the AR(1) coupling argues it will not.

---

## 3. Candidate B — Half-Life τ = ln2/κ as a Gating Condition

**Proposal.** Compute τ = ln2/κ, κ = −ln(φ), φ the AR(1) coefficient on the Kalman residual, and gate on it:
VR=0.4 at τ=5 bars is tradeable for a 1–12-week book; VR=0.4 at τ=40 bars is not. Half-life conditions whether
detected MR is tradeable at the instrument's cost structure.

**Adversarial.** **KILL** the instrument. κ̂ has SD **1.7–4.2× its own magnitude** near the unit root (replicated
on 60-bar windows; φ=0.98 → 4.2×), with the Yu-2012 upward κ bias (~+0.10). τ=−ln2/lnφ is violently nonlinear
near φ=1 (dτ/dφ→∞), so it *amplifies* the worst-resolved estimate in the apparatus. τ=5 vs τ=40 is below the
resolution of a 200-bar window — the "tradeability gate" it claims to add is noise. κ, φ and VR are one fact
(doc 04 §1.5.1). Independent-of-VR: **NO**.

**Statistical.** **INADMISSIBLE-AS-EVIDENCE *as a gate*** (STRUCTURAL identity-transform of VR-φ + reopens the
KILLED point-κ construct, doc 03 §7.1 / doc 04 §1.5.3). τ contains **zero** information beyond φ for an AR(1)
residual, and the convex transform makes τ̂ severely upward-biased and unstable near the unit root. This is the
*textbook* instance of the noise-floor prohibition: doc 03 line 505 already mandates *"never trade a point
estimate; use a ratio where errors cancel, and uncertainty-weight."* A bare τ **gate** is precisely the
point-κ object the framework demoted. Admissible **only** as a posterior/CI on τ — never a hard gate — and even
then redundant with VR.

**Trader.** **CHANGES-DECISION — ranked #1 of the three by P&L impact.** This is the genuine disagreement. The
trader's case: τ maps directly to the four inputs of a break-even calculation — holding period, cost
amortisation, adverse-excursion *duration*, and annual trade count. A score of 80 with τ=6 bars and a score of
80 with τ=45 bars are **different books**: at 0.005 round-trip the slow reverter bleeds cost + 8 weeks of
adverse excursion per cycle and turns the expectancy negative, while the fast one amortises the same cost over a
week. VR at {5,10,20} alone does not tell the PM "this reverts in 6 days vs 30." HL is the one candidate that
connects the habitat score to the cost arithmetic. The trader explicitly flags it as a **false-positive
reducer on the margin that destroys P&L** (slow reverters that VR confirms but the book horizon cannot capture
net of costs).

**Verdict B — split; net ADOPT-WITH-GUARDS the *economic dimension*, REJECT the *proposed estimator*.
Confidence: MEDIUM** (lenses materially disagree on the instrument; they *agree* the dimension matters). The
reconciliation is not a compromise — it is that the trader and the statistician are answering different
questions. The trader is right that **reversion timescale vs cost-floor is the missing P&L lever** and the
current apparatus is blind to it. The statistical/adversarial lenses are right that **κ=−lnφ on a fitted
residual, used as a hard gate, is the killed near-unit-root object** and will gate on noise. Resolution: keep
the *need*, change the *instrument*. (a) Derive a **model-free reversion timescale** — the lag at which the VR(q)
curve troughs, or the empirical first-passage / mean-half-reversion time of realised excursions — **not** a
point κ from an AR(1). (b) Report it only with an uncertainty band, **never as a binary gate**. (c) Compute it
on the **raw level / β=1 spread**, never on price−μ\* (no §15.8 trip). (d) Pair it with the trader's own
adverse-excursion read (§5) so "tradeable" means *cost + drawdown-during-hold*, not just *fast*. This delivers
B's entire economic value while sidestepping the noise floor that kills B's estimator. *Evidence that would
upgrade to full ADOPT:* a synthetic study showing the model-free timescale separates τ=5 from τ=40 reverters at
200-bar windows with a usably narrow band where the κ point estimate cannot.

---

## 4. Candidate C — Direct Reversion Coefficient (forward-return-on-z)

**Proposal.** Regress forward returns on the current z-score, r_{t+h} = α + β·z_t + ε. β<0 ⇒ deviations predict
reversion — a forward-return-predictability confirmation orthogonal to the variance-structure read.

**Adversarial.** **KILL — the clearest zombie in the packet.** (a) On a pure random walk, DRC fires β<0 in
**67% of seeds** — selection-on-deviation: z is built from a trailing window, so extremes mechanically revert to
the window mean (registry kills #1, #6). (b) corr(min-VR, DRC-β) = **+0.87** across an OU-strength sweep — DRC
is VR re-expressed as a slope, not independent evidence. (c) A coefficient on r_{t+h} indexed on z_t **is** a
per-bar forward reversion expectation — the killed State-T / MRScore-as-signal predictive object (kills #1, #2,
#6), banned vocabulary notwithstanding. Independent-of-VR: **NO** (PARTIAL only insofar as it smuggles in a
directional/predictive claim VR does not make — which makes it *worse*, not better).

**Statistical.** **ADMISSIBLE-WITH-CAVEAT** (MEASUREMENT), and the dissenting voice — but the caveats are
load-bearing. C is the *only* candidate with genuinely orthogonal content: it is **signed** (VR<1 is unsigned —
consistent with both reversion and negative-MA bounce; β<0 with a t-stat carries direction VR discards) and
**multi-horizon** (off-AR(1), the h-step conditional mean is not recoverable from VR). But: overlapping forward
returns (h>1) induce MA(h−1) residual autocorrelation → OLS SEs wrong → **Hodrick (1992) SEs mandatory**
(Newey–West is anti-conservative in small samples here). Worse, z=(P−μ\*)/σ is persistent → **Stambaugh (1999)
predictive-regression bias**, signed *toward* β<0 (spurious reversion) for a mean-reverting regressor — and the
μ\* lag illusion biases β **more negative** on top, **same sign**: the two biases **stack** toward the false
conclusion. Salvageable only as *Stambaugh-corrected β̂ + Hodrick SE + frozen h + surrogate-through-identical-
regression* — at which point it is no longer a "simple confirmation."

**Trader.** **NO-VALUE for the habitat apparatus; flag as SIGNAL-IN-DISGUISE.** The habitat score answers
"is this window an MR *environment*?"; DRC answers "at a given z, does *entering* pay?" — a different level.
Wired as a gate it conflates environment quality with entry-point quality, and a window can have β≈0 in 200 bars
while being genuinely MR (all reversions occurred at small z). Its one virtue (does the z-chart pay) is what the
z-chart + VR already show informally; formalising it adds sampling noise and an unreported forward-horizon
hyperparameter. **REJECT for this apparatus**; admissible only as a full-sample observational diagnostic in a
*separate* research context, never wired to the score.

**Verdict C — REJECT for the habitat apparatus. Confidence: MEDIUM-HIGH.** Two of three lenses reject it for
this apparatus and the adversarial zombie concern is binding: a per-bar forward-conditional reversion
expectation indexed on z is the killed predictive detector, and the habitat score is explicitly an
*observational WHERE-to-deploy* instrument, not an entry timer. The statistical lens's "admissible with caveat"
is about C as a statistic in general, conditioned on corrections that make it not-as-proposed and not-a-gate —
which is consistent with rejecting it *here*. *Evidence that would reopen (as a NEW pre-registration, §4
zombie-reopen test, NOT as a habitat addition):* a sign/rank test on **realised** reversions, full-sample,
observational, with frozen h and matched surrogate — i.e. Residual-Ecology arm (§11.5), explicitly firewalled
from any "predict reversion / favorable-now" framing.

---

## 5. Additional Candidates Beyond A · B · C

Six were proposed across the lenses (≤2 each). Listed with proposer and preliminary verdict.

| # | Candidate (one-line) | Lens | Verdict | Why |
|---|---|---|---|---|
| 1 | **Wright (2000) rank/sign VR + Chow–Denning (1993) joint test** — distribution-free, heteroskedasticity-robust VR with analytic family-wise size across the q-grid | statistical | **INVESTIGATE (top)** | Delivers the size guarantee and panel-multiplicity correction the continuous percentile lacks, and absorbs vol-clustering **without** needing the (currently absent) GARCH surrogate. Same VR family, correctly distributed — lowest-risk addition (IMPLEMENTATION-class only). Directly fixes the §1 baseline defect. |
| 2 | **Disjoint-window VR survivability** — require min-VR<1 to persist across ≥3 *disjoint* sub-windows; report the fraction, not a single full-sample VR | adversarial | **INVESTIGATE** | §11.1 BINDING GUARD already *mandates* this ("persistence across multiple disjoint windows, never appearance in one"); the live scorer omits it. Necessary-not-sufficient: a μ\*-manufactured reversion would also persist, so it sits *behind* construction admissibility, never in front. Costs q=20 power per sub-window (needs n≳80/window). |
| 3 | **Block / stationary bootstrap null on the *real* increments** — model-free surrogate preserving short-range increment dependence | adversarial | **INVESTIGATE** | Every current null is *parametric* (RW/GARCH/MA1/OU); a block bootstrap nulls everything except the *ordering* that produces reversion, catching higher-order / non-Gaussian dependence the parametric families miss. Block length is a researcher DOF → must be pre-registered, not argmax'd. |
| 4 | **DFA / Hurst exponent** — scaling exponent across all scales jointly; H<0.5 ⇒ anti-persistence | statistical | **INVESTIGATE / DEFER** | Orthogonal to the AR(1)-φ axis (does not assume AR(1); captures fractional/long-memory MR), runs on the raw level (no μ\* surface). But small-sample upward bias + sensitivity to trend/short-range autocorrelation (MEASUREMENT); for an AR(1) it is largely redundant with VR — pays off only if long-memory MR is genuinely present. Lower priority than 1–3. |
| 5 | **Conditional max-adverse-excursion (MAE) distribution** — peak-to-trough loss on the spread *before* reversion completes, conditional on habitat | trader | **INVESTIGATE** | The primary driver of *realised* vs *theoretical* Sharpe after costs and the input to position sizing / stop calibration. The score says whether it reverts, never how much pain en route — a VR=0.35 reverter that routinely moves 3× entry-z blows stops or ties up 3× capital. Pairs with the §4 model-free timescale to make "tradeable" mean cost + drawdown-during-hold. |
| 6 | **Habitat persistence / regime duration** — expected above-threshold run length before the score decays | trader | **INVESTIGATE** | Actionability at book cadence: a habitat that flips 80→20 in 3 weeks cannot be sized before it decays. Computable as the autocorrelation / above-threshold run-length distribution of the score series. Overlaps candidate 2 (disjoint-window stability) — they should be designed together. |

No additional candidate is a resurrection of a killed object: none estimates point-κ, none uses rolling-OLS-β,
none is a per-bar predictive detector. 1–3 are stricter surrogate/discipline; 4 is an orthogonal scaling axis;
5–6 are risk/persistence characterisations a PM demands before trusting a "habitat" label.

---

## 6. Synthesis — Ranked Priority List

Ruthlessly ordered by expected value to the programme, not comprehensiveness. A, B-as-proposed, and C do **not**
appear — they are rejected or subsumed.

**Rank 1 — Reconcile the live scorer to its own validated spec.** Restore the **GARCH gate**, freeze a decision
**α** (so the score carries a rejection rule, not just a color), correct **panel multiplicity** across the
rolling-window read, and resolve the q-grid ({5,10,20} vs {2,5,10,20}). *Why highest:* the shipped instrument is
**weaker than the apparatus that was validated** (doc 20), every other improvement is grafted onto it, and this
is the cheapest fix with the largest correctness return. Flagged independently by all three lenses.

**Rank 2 — Adopt the Wright rank/sign VR + Chow–Denning joint statistic.** *Why:* distribution-free,
heteroskedasticity-robust, and **analytically multiplicity-correct across q** — it delivers Rank-1's size
guarantee with provable properties and absorbs vol-clustering without depending on the GARCH surrogate.
Lowest-risk addition in the review (same VR family, correctly distributed).

**Rank 3 — Formalise disjoint-window VR survivability (+ habitat-persistence run-length).** *Why:* §11.1 already
*requires* persistence-across-disjoint-windows and the score omits it; this is the apparatus's main defence
against the regime-conditional false positive (registry kill #3) and simultaneously answers the PM's
actionability question (candidate 6). Cheap, mandated, convergent (adversarial #2 + trader #6).

**Rank 4 — Deliver B's economic dimension via a model-free reversion-timescale + conditional MAE — NOT κ.**
*Why:* the trader's #1 P&L lever (timescale vs 0.005 cost floor and adverse-excursion duration) is real and the
apparatus is blind to it; delivering it model-free (VR-trough lag / empirical first-passage) on the raw level
captures the value while sidestepping the κ noise floor that makes B-as-proposed inadmissible. Subsumes
candidate 5.

**Rank 5 — Add a block/stationary-bootstrap null on the real increments.** *Why:* every current null is
parametric; a model-free surrogate catches higher-order/non-Gaussian dependence the RW/GARCH/MA1 families
cannot, tightening the false-confirm guard. Below 1–4 because block-length is a DOF requiring its own
pre-registration discipline.

**Rank 6 — Evaluate DFA/Hurst as an orthogonal long-memory axis.** *Why:* genuinely orthogonal to AR(1)-φ and
μ\*-free, but largely redundant with VR under AR(1) and small-sample-biased — worth a bounded synthetic
evaluation only after 1–5, and only if long-memory MR is plausibly present in the deployment spreads.

*(Not on the list, explicitly: A — derived/μ\*-illusion/REJECT; B-as-κ-gate — noise-floor zombie/REJECT;
C — predictive-detector zombie/REJECT-for-apparatus.)*

---

## 7. Pre-Registration Requirements (before any real data is touched)

**Rank 1 — live-scorer reconciliation.** Freeze: the null set (RW ∧ GARCH ∧ MA(1)), N, the q-grid, the decision
**α** and the rejection rule (multiplicity-corrected min-VR p-value < α, `real_min<1`), and the panel-level
multiplicity method (e.g. FDR across windows). Re-run the doc-20 §5a synthetic calibration on the reconciled
path (seasonal-OU CONFIRM / true-RW NULL at ~α / RW+iid-noise CAUGHT-by-MA1 / no-seam no-op) **before** any
live habitat is recolored — the live FPR/power do not transfer from `evaluate_v2` automatically. Document the
divergence and its resolution as a record update (no silent rewrite).

**Rank 2 — Wright/Chow–Denning.** Freeze: rank vs sign variant (or both reported), the q-grid, the
permutation/exact-distribution method, and that the Chow–Denning joint statistic is the headline (not per-q
cherry-pick). Calibrate size on the existing RW/GARCH synthetic suite; confirm it reproduces the FPR the
percentile achieves and tightens it under heteroskedasticity.

**Rank 3 — disjoint-window survivability + persistence.** Freeze: number and construction of disjoint
sub-windows (deterministic rule, not result-selected), the minimum n per sub-window for q=20 validity, the
survivability threshold (≥k of m windows), and the persistence statistic (run-length / score-ACF). Pre-commit
that survivability sits **behind** construction admissibility (it cannot rescue a μ\*-artifact). Report the full
per-window matrix; no argmax over windows (§11.7).

**Rank 4 — model-free timescale + MAE (B's dimension).** Freeze: the timescale definition (VR-trough lag *or*
empirical first-passage — pick one a priori, not the favorable one), that it is reported with an uncertainty
band and is **never a binary gate**, that it is computed on the raw level / β=1 spread (no μ\*; no §15.8 trip),
the MAE definition (entry-z to reversion, conditional on habitat), and the cost model (≥0.005 round-trip) used
to translate timescale+MAE into a break-even. Synthetic check: separates τ=5 from τ=40 reverters at 200 bars
with a usable band.

**Rank 5 — block-bootstrap null.** Freeze: bootstrap type (stationary vs fixed-block), the block-length rule
(deterministic, e.g. n^{1/3}, **not** argmax'd over the real series), N, and that it is reported as an
additional null beside (not replacing) the parametric families. Confirm one-sided safety (too-long blocks leak
power but do not manufacture false confirms).

**Rank 6 — DFA/Hurst.** Freeze: detrending order (≥1), box-size grid, the Ĥ CI method, and the
surrogate-through-identical-DFA matching, before any real read. Gate the whole evaluation on a synthetic
demonstration that DFA adds power over VR for a *fractional/long-memory* MR alternative an AR(1) cannot
represent — if it does not, do not adopt it.

**Cross-cutting freeze (binds A/B/C should any be reopened).** Any statistic on ε=price−μ\* requires (i) a
**causal/OOS μ\***, never a full-sample in-sample Kalman fit, and (ii) the **surrogate run through the identical
μ\* extraction** so the construction artifact cancels in the percentile — and a NEW pre-registration justifying
the doc-06 §15.8 freeze-break, which none of A/B/C currently carries. Banned-vocabulary and the §11.5
State-T/Residual-Ecology firewall apply to any C-adjacent forward-conditional read.

---

### Confidence ledger
- Baseline divergence (live ≠ validated): **HIGH** — verified in source by all three lenses.
- A REJECT: **HIGH** — three-lens convergence; μ\* illusion empirically demonstrated (100% false-fire on RW).
- B split → ADOPT-dimension / REJECT-estimator: **MEDIUM** — lenses disagree on the instrument, agree on the need.
- C REJECT-for-apparatus: **MEDIUM-HIGH** — adversarial + trader reject; statistical admits only not-as-a-gate.
- Ranked list: **MEDIUM-HIGH** for Ranks 1–3 (convergent, cheap, mandated), **MEDIUM** for 4–6.

### Surviving uncertainty / explicit non-conclusions
- Not concluded: that VR is the *best* headline (it is *adequate and validated*; Wright is a strict improvement, not a replacement of the ontology).
- Not concluded: that the model-free timescale (Rank 4) actually resolves τ=5 vs τ=40 at 200 bars — that is the synthetic gate it must pass.
- Not concluded: that DFA adds anything over VR on these spreads — explicitly gated on a synthetic power demonstration.

### Next high-information question
*Does restoring the live scorer to its validated spec (GARCH + frozen α + panel multiplicity) and adding the
Wright/Chow–Denning distribution-free VR change any existing habitat verdict on the 46-leg corpus — i.e. is the
baseline gap material, or cosmetic?*
