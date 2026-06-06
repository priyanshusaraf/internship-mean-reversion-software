# Kalman μ\* — Equilibrium Research Update

**Document class:** Permanent AMR research record (living institutional log — appended, not rewritten)
**Status:** Active. Supersedes the verdict of `05_kalman_v1_results_memo.md`. Sections 1–11 record the synthetic→authorization arc; sections 12–13 record the real-market reassessment and the decisive question; section 14 records the Step 2A structural-falsification instrumentation; section 15 records the Step 2A.5 final cheap empirical gate and the **provisional (weak, non-blocking)** freeze of μ\* uncertainty, with a binding revisit-trigger before any upstream use depends on μ\* reversion fidelity.
**Date opened:** 2026-06-01
**Scope:** EMA baseline → diagnostics workbench → validation sprint → initial Kalman rejection → replication audit → confirmatory test → authorization of Step 1 → **Step 1 execution + methodological reassessment (§12) → new decisive question (§13) → Step 2A: S2 (false-centering) instrumentation + first reads (§14) → Step 2A.5: final cheap empirical gate, regime-stratified single real underlying → freeze S2/μ\* uncertainty as non-blocking (§15).**

> This document records a change in understanding, not a change in code. It exists so that a future researcher (human or model) can reconstruct *how the conclusion moved* without re-reading conversation logs. It uses a **claim → evidence → implication** structure throughout. Where an earlier finding was overturned, both the original claim and its falsification are preserved.

> **Revision history.**
> - **Rev 1 (2026-06-01):** §1–§11 written. Verdict: synthetic centering advantage confirmed; Step 1 authorized.
> - **Rev 2 (2026-06-01):** §12–§13 added. Step 1 executed; a methodological critique demoted *centering* from a frozen conclusion to an insufficient diagnostic and reframed the decisive question around causal reversion fidelity. **No Rev 1 text was deleted** — affected claims in §8/§9 carry inline `▸ REVISED (Rev 2 → §12)` markers pointing here. Read §1–§11 as the state of belief *as of Rev 1*; read §12–§13 for the current state.
> - **Rev 3 (2026-06-01):** §14 added. Step 2A executed: the minimum-viable instrumentation for the **S2 (false-centering / signal-absorption)** arm of the §13 question — the velocity-contribution decomposition δ and an out-of-sample walk-forward predictive-decay test on the velocity-ON (ε^K) vs velocity-OFF (ε^R) residual systems. First manual reads on ADANIENT (real) and NIFTY_SYN (synthetic) recorded. **No conclusion frozen** — this Rev adds an instrument and an observation, not a finding. The §13 surrogate-null and naive-detrend (S1) arms are **still not built**; §14 states explicitly what Step 2A does and does not answer. No prior text was deleted.
> - **Rev 4 (2026-06-01):** §15 added. Step 2A.5 (final cheap empirical gate) executed. The intended 4–6 real-instrument panel **could not be run** — only ADANIENT qualifies on disk and no data-fetch capability is installed — so the existing frozen instrumentation was run across **pre-declared intra-instrument regime windows** of ADANIENT (sideways / moderate-trend / parabolic-trend / full). Result: Δβ tiny and **sign-incoherent across regimes** (the absorption-prone sideways regime is anti-absorption-signed), R²ₒₒₛ ≈ 0 for both estimators in every regime. **Classification B (unresolved, non-blocking); catastrophic false-centering (C) excluded.** Decision (researcher, Rev 4): **PROVISIONAL / weak freeze** — move up the stack now, but the freeze is explicitly flagged low-confidence with a **binding revisit-trigger**: it must be re-opened (cross-instrument panel first) before any upstream component depends on μ\* *reversion fidelity*; descriptive/centering uses do not trigger. Confidence delta: §14's tentative benign read STRENGTHENED (now covers the worry regime) but capped LOW-MEDIUM by the single underlying. No prior text deleted.

---

## 1. Executive Abstract

**What changed.** The Kalman μ\* estimator was initially rejected for v1 on kill-criterion KC4 ("velocity absorbs alpha") with KC1 secondary ("no artifact reduction"). An independent replication audit falsified both grounds: the absorption metric (G-ABSORB) was shown to be contaminated and trend-invariant, and the KC1 gate was shown to be internally unsatisfiable by *any* estimator including EMA. A single pre-registered confirmatory experiment — Kalman against a **matched-effective-span** EMA on OU-in-trend, 360 paired conditions per operating point — then isolated the one axis on which the two estimators genuinely differ: **trend-adjusted residual centering**. EMA residuals inside a trend carry a deterministic lag bias of magnitude `slope × span / 2`; this bias grows without bound as the trend steepens and renders the EMA residual operationally unusable for reversion signalling (residual sign-agreement with the true deviation ≈ 0.49, a coin flip). Kalman's velocity state eliminates the bias (sign-agreement ≈ 0.85) while preserving the deviation signal (corr(ε, deviation) ≈ 0.92, variance ratio ≈ 1.0). The effect is large, mechanistically exact, and robust (Wilcoxon p < 1e-30 across all seeds, slopes, OU strengths, and SNRs).

**Why it matters.** The AMR thesis is *mean reversion inside structurally trendy markets*. An equilibrium estimator whose residual is dominated by trend-lag artifact cannot serve that thesis, regardless of how well-behaved its residual's persistence or half-life look. The confirmatory test reframes the selection criterion from **residual shape** (persistence, ACF, half-life — on which the estimators are statistically indistinguishable) to **residual usability** (centering, sign-agreement — on which Kalman is categorically superior). On the usability axis, Kalman earns authorization to proceed to controlled real-market integration (Step 1). The prior KC4/KC1 rejection rationale is formally struck from the record.

---

## 2. Initial Equilibrium Framing

**Claim (original).** EMA μ\* is adequate baseline instrumentation for locating equilibrium, not a final equilibrium model.

**Role assigned.** EMA was chosen as the v0 μ\* estimator on three grounds: (i) it is the minimal causal smoother — one parameter (`span`), no fitting, no lookahead; (ii) it is analytically transparent, so its failure modes are derivable rather than empirical; (iii) it establishes a fixed reference against which any more complex estimator must demonstrate marginal value. EMA was never framed as the equilibrium; it was framed as the instrument that makes equilibrium *observable* cheaply.

**Known limitation, now a frozen finding.** EMA residuals are **mechanically contaminated by the smoothing structure itself.** Three components of that contamination are now established:

- **Deterministic trend-lag bias.** Inside a linear trend of slope `m`, the EMA lags the price by a fixed offset, so the residual `ε = P − EMA` has a non-zero mean `≈ m · span / 2`. This is not noise; it is a structural offset that scales with both trend slope and smoothing span. (Confirmed analytically and numerically — see §7.)
- **ACF inheritance.** The EMA residual's autocorrelation structure is partly imposed by the smoother's geometric weighting, not solely by the underlying process. EMA-residual ACF(1) sits at ≈0.88–0.94 across admissible spans even on a pure random walk, so residual persistence is *not* a clean read of process persistence.
- **Non-neutral residual.** Because of the above, the EMA residual is not a zero-mean, process-faithful deviation. It is the deviation plus a smoother-induced offset plus smoother-induced autocorrelation.

**Implication.** These limitations were the original motivation to test a competing estimator. The trend-lag bias in particular is the precise failure that the velocity-aware Kalman was hypothesized to remove — a hypothesis only confirmed much later, and for different reasons than originally argued.

**Frozen:** EMA residual contamination (trend-lag bias, ACF inheritance, non-neutral mean) is a permanent finding. EMA remains valid as fast baseline instrumentation; it is not a trend-robust equilibrium estimator.

---

## 3. Diagnostics Workbench & Validation Layer

**Claim.** Plausible ≠ trustworthy. An equilibrium estimate that *looks* reasonable on a chart can be silently contaminated (lookahead, warmup artifact, mislabeled mode). Observability had to precede any estimator comparison.

**Why observability became necessary.** Before comparing estimators, the system needed a way to *see* residual processes, validate temporal integrity, and verify that synthetic ground truth was being recovered. Without this layer, a comparison between EMA and Kalman would have compared two black boxes. The workbench is a **quantitative observatory**, not a trading dashboard — its purpose is inspection and falsification, not monitoring or execution.

**Workbench architecture (modules).**

- **Estimator inspector** — renders μ\* against price; exposes the estimator parameters and the resulting equilibrium track for visual drift diagnosis.
- **Residual observatory** — renders ε = P − μ\* as a time series with its distribution and autocorrelation; the primary surface for judging residual quality.
- **Assumption validator** — runs the synthetic ground-truth battery (OU half-life recovery, random-walk sanity, stationarity/ADF significance) and reports pass/fail against pre-registered tolerances.
- **Replay boundary** — enforces and visualizes the causal cutoff: at bar *t*, only `prices[0..t]` are visible. Makes temporal leakage detectable by construction.
- **Event log** — records what was computed, with which parameters, in which mode (full-information vs causal), so that any displayed figure is traceable to its provenance.

**Validation sprint — what was checked and corrected.**

- **OU validation.** On synthetic OU with known λ, the half-life estimator recovers the true half-life within tolerance. This anchors every downstream residual-quality claim to a known answer.
- **Random-walk sanity.** On a pure random walk (no mean reversion), the residual must *not* manufacture reversion. This is the null guard.
- **Replay integrity.** Verified that values at early bars are bit-identical whether the series ends at bar *t* or extends past it — no future bar perturbs a past estimate.
- **Causal firewall.** A future spike injected at a late bar leaves all prior μ\* values unchanged. Causality is structural, not incidental.
- **Half-life correction.** The half-life estimator was corrected to include an intercept term and to gate on ADF stationarity significance, removing a bias present in the naive AR(1) fit.
- **EMA interpretation correction.** An earlier warmup-initialization choice caused EMA to be transiently mislabeled as a "full-information" track near the series start. Corrected by initializing at the steady-state condition, eliminating the warmup artifact.

**Frozen:** the observatory and validation battery are the standing acceptance framework. Any new estimator is admitted only after passing the same synthetic ground-truth tests under the same causal firewall. "Plausible on a chart" is never sufficient.

---

## 4. Initial Kalman Thesis

**Claim (hypothesis).** A Kalman filter may produce a cleaner equilibrium estimate than EMA in trendy markets with embedded mean reversion, because it can model the trend explicitly rather than lagging it.

**State choice.** The frozen specification used a **2-state local-linear-trend** model:

```
x_t = [μ_t, v_t]      F = [[1, 1], [0, 1]]      H = [1, 0]
Q = diag(q_μ, q_v),  q_μ = κ · q_v,  κ = 0.05 (frozen)
```

where μ is the latent equilibrium level and v is its velocity (drift). The single dimensionless knob is `SNR = q_v / R_p`, with R_p normalized once from the robust scale of price changes `(1.4826 · MAD(ΔP))²` — a unit normalization, not a fit. The **research residual is the one-step-ahead innovation** `P_t − μ_{t|t−1}` (pre-update), chosen specifically to avoid the circularity of a filtered (post-update) residual.

**Why 2-state, not 1-state.** A 1-state local-level Kalman is, at steady state, **algebraically an EMA** — its steady-state gain equals the EMA α. A level-only Kalman therefore cannot, even in principle, out-perform EMA on a trend; it would reproduce EMA's lag bias exactly. The *only* feature that distinguishes the model class from EMA is the **velocity state v**. Consequently the entire case for Kalman rests on velocity being simultaneously (a) active enough not to collapse to an EMA, and (b) disciplined enough not to absorb the very deviation the system wants to measure. This tension is the axis on which the estimator was later judged.

**Frozen:** the level-only Kalman is rejected a priori as equivalent to EMA. Any Kalman μ\* must carry the velocity state. The 2-state specification (κ = 0.05, single SNR knob, innovation residual, MAD-normalized R) is the frozen model; the investigation that follows did not unfreeze it.

---

## 5. Failed Rejection Phase

This section is preserved in full because the rejection it documents was later overturned. Recording the failure path is part of the epistemic record.

**Claim (original rejection).** Kalman is rejected for v1: **KC4 (alpha absorption) primary**, **KC1 (no artifact reduction) secondary**. No admissible SNR band exists.

**The argument as originally made.**

- **G-ABSORB.** Absorption was measured as `|corr(velocity, deviation)|`, with a pre-registered pass threshold of < 0.20. Across a 28-point SNR sweep (`logspace(-9, 0, 28)`), the minimum observed absorption was **0.208** — failing the threshold at *every* SNR. The interpretation: the velocity state tracks the mean-reverting deviation, degrading the signal the filter was meant to isolate.
- **Disjoint-region finding.** The three core gates — H2 (OU half-life ±25%), G-IDENT (impulse cosine < 0.99, i.e. "not an EMA"), and G-ABSORB — were found to occupy **disjoint SNR regions**. H2 passes only for slow filters (effective span ≳ 54). G-IDENT fails at the very slow end (velocity so suppressed the filter degenerates to EMA). G-ABSORB fails everywhere. No SNR satisfied all three simultaneously.
- **KC1.** At the slow SNRs that recover OU, the random-walk innovation ACF(1) was ≈0.95–0.98 — worse than EMA-20's ≈0.88 — read as "the filter manufactures more artifact than EMA, not less."
- **Mechanism asserted.** A mean-reverting excursion "looks locally like a slope change," so the velocity tracks it regardless of SNR; the feature justifying Kalman (velocity) was claimed to be the feature disqualifying it (absorption) — a property of the model class, not the tuning.

**Why this conclusion was later challenged.** Several process failures attended this phase and motivated independent replication:

- **Environment corruption.** A numpy warning flood (~11MB to stderr) was initially mistaken for output redaction / environment corruption, degrading confidence in the raw tool channel during the run.
- **Memo contamination.** An earlier draft of `05` reported an *admissible band* and a KC1-only verdict — figures produced while the tool-output channel was intermittently truncating results. Those numbers were **fabricated by truncation** and were retracted (recorded in §8 of `05`).
- **Under-swept SNR grid.** The first sweep used `logspace(-4, 0, 17)`, too coarse and too fast-biased to characterize the slow regime where H2 lives. It was later extended to `logspace(-9, 0, 28)`.
- **Contradictory test failure.** A pytest assertion failed (`OU half-life err 75.1% ≥ 25%`) against a memo claim of clean recovery — an internal contradiction that exposed the contaminated figures.

**Implication.** The *destination* (a rejection) might still be correct, but the *map* (KC4 absorption, KC1 artifact, disjoint regions) was built on a contaminated channel and an unaudited metric. That is sufficient grounds to distrust the rejection and replicate it independently. This is the transition into §6.

---

## 6. Replication Audit & Falsification

**Claim.** The rejection must be re-earned by an independent reviewer who is not permitted to assume Kalman either failed or succeeded. The destination may be right; the map is suspect.

**Audit design.** Four controlled experiments (in `scripts/audit_kalman.py`): an absorption null test, slope sensitivity, kappa sensitivity, and a disjointness reconstruction. Each was designed to test whether a *specific* leg of the rejection survives scrutiny.

**Finding 1 — KC4 is falsified.** The claim "velocity absorbs alpha" predicts the deviation signal should be degraded in the residual. It is not. Across the H2-admissible band, the residual retains the deviation:

- `corr(ε_kalman, true_deviation) ≈ 0.9`
- `var_ratio = var(ε) / var(deviation) ≈ 1.0`

The signal is preserved, not absorbed. The premise of KC4 is false.

**Finding 2 — G-ABSORB is a contaminated metric.** The absorption statistic `|corr(velocity, deviation)|` is **trend-invariant**, which is disqualifying for a metric whose entire purpose is to detect trend-related contamination:

| slope | trendHL/devStd | absorb | varRatio |
|------:|---------------:|-------:|---------:|
| 0.00 | 0.000 | 0.288 | 0.997 |
| 0.10 | 0.302 | 0.288 | 0.997 |
| 0.25 | 0.755 | 0.288 | 0.997 |
| 1.00 | 3.021 | 0.288 | 0.997 |
| 2.00 | 6.043 | 0.288 | 0.997 |

(SNR = 1e-8; from `scripts/audit_kalman.py`, exp2.) The metric reads **identically (0.288)** at zero slope and at slope 2.0. A statistic that does not move when the trend goes from absent to dominant is not measuring trend contamination — it is measuring a mechanical floor of the velocity/deviation correlation that exists even with no trend at all.

**Finding 3 — the threshold is fragile and underived.** The pass threshold (0.20) was not derived from first principles, and the reported minimum (0.208) is a knife-edge failure against an arbitrary line. Combined with Finding 2, the 0.208 vs 0.20 result carries no structural weight: it is a hair's-breadth miss against an underived threshold on a metric that does not respond to the phenomenon it claims to gate.

**Finding 4 — kappa-invariance confirms the metric is inert.** Sweeping κ over {0, 0.01, 0.05, 0.20, 0.50, 1.00} at SNR = 1e-8 leaves both absorption (0.288) and OU half-life error (0.155) **completely unchanged** (exp3). The absorption metric does not respond to the one structural knob that controls the velocity process noise. This is consistent with it measuring a floor, not a behavior.

**Finding 5 — KC1 (H1/H2 contradiction) is invalid.** The KC1 / H1 gate demanded the random-walk innovation ACF be < 0.20. But EMA itself produces RW residual ACF(1) ≈ 0.88–0.98 at the *same* spans where H2 (OU recovery) passes. The gate is therefore **unsatisfiable by any estimator**, EMA included — it is not a discriminating criterion, it is an impossible one. Penalizing Kalman for failing a gate that EMA also fails (and that no causal smoother can pass) is invalid.

**Implication — what became invalid.**

- KC4 ("velocity absorbs alpha"): **falsified** — signal is preserved (corr ≈ 0.9, var_ratio ≈ 1.0).
- G-ABSORB metric: **invalidated** — trend-invariant, κ-invariant, underived threshold, knife-edge result.
- KC1 / H1 gate: **invalidated** — internally unsatisfiable by any estimator including EMA.

With both stated grounds for rejection removed, the rejection of `05` no longer stands. But falsifying the rejection is not the same as confirming the estimator. The audit established only that *the case against Kalman was wrong*, not that *the case for Kalman is right*. That required a single decisive confirmatory test (§7).

**Frozen:** G-ABSORB (as `|corr(velocity, deviation)|` with a 0.20 threshold) is retired as a selection gate. It does not measure trend contamination. Any future absorption gate must be demonstrably trend-responsive before use.

---

## 7. Confirmatory Experiment

This is the decisive section. It answers the only remaining question with one fair, controlled, pre-registered experiment.

### 7.1 The fairness problem

**Claim.** A naive Kalman-vs-EMA comparison is confounded by responsiveness. If the two estimators have different effective speeds, any residual difference could be a speed artifact rather than a structural difference. The comparison must hold responsiveness fixed so the estimators differ **only** by the velocity state.

**Solution — matched effective span.** For a given Kalman SNR, compute the steady-state level gain from the Riccati recursion:

```
α = K∞[0]              (steady-state Kalman gain on the level)
EMA span = 2/α − 1     (the EMA with identical one-step responsiveness)
```

Both estimators then have **identical one-step responsiveness** by construction. Any residual difference is attributable to the velocity state alone — not to one estimator being faster than the other. This is the crux that makes the test fair.

### 7.2 Experimental design

- **Environment:** `ou_in_trend` — a mean-reverting OU deviation superimposed on a linear trend. This is the AMR thesis substrate: reversion *inside* a trend.
- **Pairing:** fully paired. The same random seed drives both estimators, so paired deltas (Kalman − EMA) are tested directly.
- **Grid:** 30 seeds × 4 slopes (0.05, 0.10, 0.25, 0.50) × 3 OU strengths (λ = −0.05, −0.10, −0.20; true half-lives ≈ 13.5, 6.93, 3.11) = **360 paired conditions per operating point.**
- **Operating points:** the 4 H2-admissible SNRs (1e-9, 1e-8, 1e-7, 3.16e-7), giving matched EMA spans of 251, 141, 80, 60. Outside the H2 band Kalman does not recover OU, so a residual-quality comparison there is moot.
- **Residual:** Kalman = one-step innovation; EMA = `P − EMA`.
- **Metrics:** half-life error, ACF(1), ACF(5), `|mean(ε)|` (centering), corr(ε, deviation), var_ratio.
- **Significance:** Wilcoxon signed-rank on the paired deltas. (Statistics, not optimization — the frozen spec forbids fitting, not significance testing.)
- **Reproduce:** `backend/scripts/confirm_kalman.py` → `/tmp/confirm.txt`.

### 7.3 Core result

At SNR = 1e-8 (matched span 141; representative — all 4 operating points agree in direction):

| metric | Kalman med | EMA med | median Δ | Wilcoxon p | verdict |
|---|---:|---:|---:|---:|---|
| **abs_mean** (centering) | **0.095** | **12.19** | **−11.76** | 9.4e-61 | **Kalman, categorical** |
| hl_err | 0.099 | 0.130 | −0.024 | 4.8e-12 | Kalman, marginal |
| acf1 | 0.890 | 0.888 | +0.004 | 7.1e-06 | tie (trivial) |
| acf5 | 0.538 | 0.534 | +0.015 | 2.2e-06 | tie (trivial) |
| corr_dev | 0.925 | 0.935 | −0.020 | 1.0e-12 | EMA, trivial |
| var_ratio | 0.978 | 0.925 | +0.056 | 9.2e-15 | tie (both ≈ 1) |

**Reading the result.** On **persistence and shape** — ACF(1), ACF(5), half-life, corr(ε, deviation), var_ratio — the two estimators are statistically indistinguishable (all differences in the third decimal or smaller; corr_dev trivially favors EMA). The KC3-redundancy hypothesis was **correct about persistence**: at matched span, Kalman and EMA produce residuals with the same autocorrelation structure. On **centering** — `|mean(ε)|` — the estimators differ by **two orders of magnitude** (0.095 vs 12.19), the single largest and most significant effect in the entire study.

### 7.4 The deterministic EMA lag-bias mechanism

The centering difference is not empirical luck; it is the textbook EMA trend-lag bias, confirmed to three significant figures (SNR = 1e-8, span = 141):

| slope | EMA \|mean ε\| | theory (slope·span/2) | Kalman \|mean ε\| |
|------:|---------------:|----------------------:|------------------:|
| 0.05 | 3.42 | 3.53 | 0.085 |
| 0.25 | 17.24 | 17.63 | 0.086 |
| 1.00 | 69.05 | 70.50 | 0.086 |

**EMA residual mean = `slope × span / 2`**, matching theory exactly, and **growing without bound as the trend steepens.** Kalman's residual mean stays flat at ≈ 0.085 *regardless of slope* — the velocity state absorbs the trend's first moment into the equilibrium track, leaving the innovation centered on zero. This is the precise contamination identified as a frozen EMA limitation in §2, and the velocity state removes it by construction.

**Why this is foundational.** Inside a trend, the EMA residual is dominated by an additive offset that has *nothing to do with the deviation*. At slope 0.25, the offset (17.2) is ≈ 7× the deviation's own standard deviation (≈ 2.3). The EMA residual is mostly trend-lag artifact with the deviation buried inside it. The variance-ratio metric missed this entirely because it is computed on *demeaned* variance — it confirms the signal is present but is blind to the offset that makes the signal unusable.

### 7.5 Sign-agreement (operational meaning)

The operational consequence of centering: the fraction of bars where the residual's sign matches the *true* deviation's sign (slope = 0.25):

- **Kalman: 0.854**
- **EMA: 0.492** — worse than a coin flip.

**Why 0.49 vs 0.85 matters.** A reversion signal is read off the residual's sign and its zero-crossings: "price is above equilibrium → expect reversion down," and vice versa. EMA's constant trend-lag offset pushes the residual entirely to one side of zero, so its sign no longer tracks the deviation — at 0.49, the EMA residual sign is **uninformative** about whether the market is actually above or below its mean-reverting equilibrium. Kalman's centered residual recovers the deviation's sign 85% of the time. For an estimator whose purpose is to find reversion inside a trend, this is the difference between a usable signal and noise.

**Robustness.** The centering advantage holds across all 30 seeds, all 4 slopes, all 3 OU strengths, and all 4 SNRs. Every Wilcoxon p on abs_mean is < 1e-30 (the slowest operating point, span 251, gives Kalman 0.18 vs EMA 20.7, p = 9.4e-61). The effect grows monotonically with slope, as the mechanism predicts. This is not a noise artifact and not a single-condition fluke.

---

## 8. Updated Equilibrium Understanding

> **▸ REVISED (Rev 2 → §12).** This section elevated *centering* (and its operational proxy, sign-agreement) to the primary selection criterion and called it "central to AMR." That elevation was justified **only on synthetic OU-in-trend, where centering and reversion are entangled by construction.** §12 demotes centering to an *important but insufficient and confounded* diagnostic: it is necessary, not sufficient, for mean reversion, and the Kalman advantage on it may be structurally guaranteed (the detrending confound S1) rather than evidence of better equilibrium discovery. The Rev 1 text below is preserved as the state of belief at authorization; do not cite it as a current frozen conclusion.

**Claim.** The selection criterion for an equilibrium estimator must be **residual usability**, not **residual shape**.

**The conceptual shift.** Before the confirmatory test, estimator quality was judged primarily on residual *persistence* — does ε have clean, interpretable autocorrelation and a recoverable half-life? On that axis, EMA and a matched Kalman are equivalent, which is why KC3-redundancy looked plausible. The test shows that persistence is the *wrong* primary axis: it does not discriminate, and more importantly it does not determine tradeability. The axis that determines whether a residual can carry a reversion signal is *centering* — whether ε is a faithful, zero-centered read of the deviation, or whether it is the deviation buried under a trend-induced offset.

**Residual usability vs residual persistence.**

- **Persistence** (ACF, half-life): describes the *shape* of the residual process. Both estimators are equivalent here. Necessary but not sufficient.
- **Usability** (centering, sign-agreement): describes whether the residual can be *acted on* as a deviation signal. Only Kalman delivers it inside a trend.

**New interpretation of equilibrium (now central to AMR).** `▸ REVISED (Rev 2 → §12): "central to AMR" overstated; centering is a diagnostic, not the objective.`

> An equilibrium estimate must remain **centered inside trends** — the residual must read the deviation faithfully without inheriting the trend's first moment, and without absorbing the deviation itself.

EMA satisfies neither half of this inside a trend: it inherits the trend's first moment (the lag bias) while leaving the deviation present but offset. The 2-state Kalman satisfies both: velocity absorbs the trend's first moment into μ\*, the innovation stays centered, and the deviation is preserved (corr ≈ 0.92, var_ratio ≈ 1.0). This is the operational definition of a trend-robust equilibrium, and it is the property the AMR thesis requires.

---

## 9. Frozen Conclusions

> **▸ REVISED (Rev 2 → §12).** Every CONFIRMED item below is **synthetic-only** (OU-in-trend with known ground truth). They remain true *of that synthetic regime*. Two carry caveats added in Rev 2: (i) "Signal is preserved, not absorbed" was established with `corr(ε, true_deviation)` — a test that **requires ground truth and therefore cannot be evaluated on real markets**, so the no-absorption (false-centering) question is *re-opened*, not closed, for real data (S2); (ii) "Centering drives operational usability" is **demoted** — centering is necessary but insufficient for reversion, and the Kalman edge on it may be structurally guaranteed (S1). See §12.

### CONFIRMED (synthetic regime, as of Rev 1)

- **EMA residuals carry a deterministic trend-lag bias** of magnitude `slope × span / 2`, verified to three significant figures and growing without bound with slope. (§2, §7.4) — *mechanism, holds analytically.*
- **The 2-state Kalman eliminates this bias** — innovation mean ≈ 0.085 independent of slope. (§7.4) — *holds on synthetic linear trends; attenuates on real curved/accelerating trends, §12.*
- **Signal is preserved, not absorbed** — corr(ε_kalman, deviation) ≈ 0.92, var_ratio ≈ 1.0. (§6, §7.3) `▸ REVISED: ground-truth test; re-opened for real markets (S2).`
- **Kalman and EMA are equivalent on persistence/shape** — ACF and half-life statistically indistinguishable at matched span. (§7.3)
- **Centering drives operational usability** — residual sign-agreement with the true deviation: Kalman ≈ 0.85 vs EMA ≈ 0.49 at slope 0.25. (§7.5) `▸ REVISED: demoted to insufficient diagnostic (S1); usability ≠ reversion fidelity.`
- **Level-only Kalman ≡ EMA** at steady state; only the velocity state can differentiate the model class. (§4)

### FALSIFIED

- **KC4 — "velocity structurally absorbs alpha."** False. Signal is preserved (corr ≈ 0.9). (§6)
- **G-ABSORB as a contamination gate.** Invalid: trend-invariant, κ-invariant, underived threshold, knife-edge 0.208-vs-0.20 result. (§6)
- **KC1 / H1 random-walk ACF gate.** Invalid: unsatisfiable by any causal estimator including EMA. (§6)
- **KC3-redundancy as a kill.** False as a kill: Kalman and EMA *are* redundant on persistence, but redundancy on persistence is not redundancy overall — they diverge categorically on centering. (§7.3)
- **The `05` rejection verdict (REJECTED, KC4 primary / KC1 secondary).** Superseded. (§5, §6)

### UNRESOLVED

- **Real-market robustness.** All evidence to date is on synthetic OU-in-trend with known ground truth. Behavior on real instruments — with fat tails, microstructure noise, non-stationary volatility — is untested.
- **Violent regime transitions.** The velocity state's response to abrupt structural breaks and regime switches (where a true slope change and a deviation are genuinely confounded) is not characterized.
- **False centering.** It must be ruled out that the velocity state can produce a *spuriously* centered residual during a genuine slope change — i.e. that centering is achieved by correctly modelling the trend, not by quietly fitting the deviation as drift during transitions.
- **Replacement absorption metric.** G-ABSORB is retired; a trend-responsive successor (candidate: the centering / sign-agreement statistic itself) has not been formally specified or gated.

---

## 10. Research Implications for AMR

**μ\*.** EMA remains valid fast baseline instrumentation. The 2-state Kalman is now the candidate **trend-robust equilibrium** estimator, justified specifically by centering inside trends. The two are complementary, not competing: EMA for cheap responsiveness reads, Kalman where trend-robust centering matters.

**ε (residual).** The residual definition for reversion work shifts toward the Kalman innovation inside trended regimes, because the EMA residual's trend-lag offset makes its sign uninformative. Any reversion logic built on EMA residuals must be re-examined for slope-dependent bias.

**MR diagnostics.** Mean-reversion diagnostics that depend on residual *sign* or *zero-crossings* (not just persistence) must use a centered residual. On EMA residuals inside a trend, sign-based diagnostics are at coin-flip reliability and should be treated as invalid until centered.

**State T.** State T (transition dynamics) is the regime where trend and deviation are most confounded and where the "false centering" risk is highest. The velocity state's behavior during transitions is exactly what State T research must characterize — the confirmatory test validates centering in *stationary* trend regimes only, not across transitions.

**Trend-aware reversion.** The core AMR thesis — reversion inside trends — now has a concrete estimator-level requirement: the equilibrium track must absorb the trend's first moment so the residual stays centered. This is the operational definition the rest of the program builds on.

---

## 11. Next Authorized Research Step

**Step 1 — Controlled Real-Market Integration.**

**Why we move forward.** The KC3-redundancy hypothesis is falsified, both `05` rejection grounds are invalidated, and a single pre-registered 360-condition experiment shows a large, mechanistically exact, robust (p < 1e-30) advantage on the one axis the AMR thesis is about — trend-adjusted centering — with no signal degradation. This clears the pre-registered bar for authorization ("clear, repeatable, material improvement in residual quality OR trend centering without signal degradation"). Kalman earns Step 1.

**What Step 1 is.** Controlled integration of `compute_kalman_mu_star` against real instruments behind the existing causal firewall and observatory, validating the single confirmed advantage (centering / sign-agreement) on real data rather than synthetic ground truth. Scope discipline from the frozen spec holds: **no model features are added.** The win comes from the minimal 2-state filter exactly as specified (κ = 0.05, single SNR knob, innovation residual, MAD-normalized R). Adding adaptive Q/R, MLE, or fancier variants is out of scope.

**Remaining skepticism (no overclaiming).** The confirmed advantage is established only on synthetic OU-in-trend. Step 1 must:

- Test centering and sign-agreement on **real instruments** (fat tails, microstructure, non-stationary vol) before any production claim.
- Characterize the velocity state across **regime transitions / structural breaks** (State T territory), where trend and deviation are genuinely confounded.
- Explicitly test for **false centering** — confirm the residual is centered because the trend is modelled correctly, not because the deviation is being fitted as drift.
- Specify a **trend-responsive replacement** for the retired G-ABSORB gate before re-introducing any absorption criterion.

The advantage is real and authorized. It is not yet proven outside the synthetic regime. Step 1 exists to close that gap, not to assume it closed.

> **▸ UPDATE (Rev 2).** Step 1 was executed (additive integration: Kalman wired beside EMA in `/diagnostics`, `EstimatorCompare` workbench module, structured real-market pass). Its findings and the methodological critique that followed are recorded in §12. The Rev 1 framing above — "validate the centering advantage on real data" — was itself found to rest on a confounded objective; §12 reframes the task.

---

## 12. Methodological Reassessment of Real-Market Evidence

*(Rev 2. This section records the execution of Step 1, the critique of its evidence, and the resulting demotion of centering. It deliberately separates four things that §1–§11 sometimes ran together: the **observed result**, its **interpretation**, the **methodology quality** that produced it, and the **confidence level** that survives.)*

### 12.1 What Step 1 produced

Additive integration only (no model change; frozen filter unchanged; EMA remains production μ\*). One structured real-market pass on ADANIENT (2012–2022, daily), Kalman vs EMA at matched effective span ≈ 141, residuals bucketed by regime. Reproduce: `backend/scripts/eval_kalman_real.py` → `/tmp/eval_real.txt`.

### 12.2 The four-layer separation (do not collapse these)

| Layer | Strong-trend centering | False-centering probe | Sideways behavior |
|---|---|---|---|
| **Observed result** | `\|mean ε\|` EMA 238.7 vs Kalman 151.3 (≈1.6×); Kalman 3.5× higher zero-cross rate, shorter sign runs. | Median Kalman/EMA ε-peak ratio at largest displacements ≈ 1.17 (incl. 2020 COVID crash); one local exception (2019-05-20, ratio 0.35). | Kalman *more* centered than EMA (`\|mean ε\|` 43.2 vs 5.6), not equal. |
| **Interpretation (Rev 1 reflex)** | "Centering advantage persists in reality." | "Feared signal-absorption failure mode did not appear → cautious optimism." | "Anomaly: collapse-to-EMA prediction failed." |
| **Methodology quality** | **Low.** Confounded (S1) and contaminated (C1–C4, C6). | **Medium.** Direction is informative but the probe metric (ε-peak magnitude) is crude and ground-truth-free. | **Low–medium.** Two interpretations (A benign / B pathological) are observationally equivalent under this metric. |
| **Confidence that survives** | **Low.** The 1.6× is **currently unproven** — plausibly an artifact of S1 + price-scale. | **Medium-low.** Best read: *no systematic* false centering on this instrument; not "false centering ruled out." | **Unresolved.** Cannot distinguish A from B without a ground-truth-free reversion test. |

The Rev 1 narrative collapsed "observed" into "confirmed." It is not. A directionally-consistent, uncalibrated, single-instrument result is an *observation*, not a finding.

### 12.3 Confound analysis

**S1 — The Detrending Confound (structural).**
*Claim:* "Kalman is more centered than EMA" may reflect **extra structural capability**, not better equilibrium discovery.
*Evidence/mechanism:* The Kalman carries an integrated **velocity** state; EMA structurally cannot. Centering = removal of the residual's first moment = exactly what an integrated drift term does by construction. The matched-effective-span control equalized **level responsiveness** (steady-state gain on μ) but **not detrending capability** — the one axis on which the estimators are structurally unequal and the exact axis centering rewards. So the comparison is rigged in Kalman's favor *a priori*: we are observing "the estimator with a drift term removes drift better," which is a tautology about model structure, not a discovery about markets.
*Implication:* A centering win over matched-span EMA is **expected regardless of whether Kalman discovers anything real about equilibrium.** The correct control is not matched-span EMA but a *naive detrender of matched memory* (trailing-OLS / Holt). If Kalman's edge vanishes against that, the edge was "we added a trend term" (KC3-redundancy reborn against the right baseline).

**S2 — False Centering / Signal Absorption (structural, re-opened).**
*Claim:* The velocity state *can* mechanically explain genuine reversion as drift, producing a residual that looks clean because it destroyed signal.
*Evidence:* doc 06 Rev 1 "falsified" this (the old KC4) using `corr(ε, true_deviation)` — a test that **requires ground truth that real markets do not provide.** Therefore S2 is **unfalsified on real data.** The sideways anomaly (12.2) is exactly the shape S2 would take: Kalman "more centered" could be A (EMA lags real low-frequency drift, Kalman corrects it → benign) or B (velocity absorbed reversion → pathological). The current metric set cannot separate them.
*Implication:* The single most important open question is S2, and it needs a *ground-truth-free* discriminator (designed in §13 / the MVF plan).

### 12.4 Methodology Contamination Audit (C1–C6)

This taxonomy — **measurement vs methodology vs structural** — is hereby adopted as standing AMR research language. The fix differs by class: measurement → renormalize; methodology → redesign the test; **structural → cannot be fixed by either, must be controlled with the right baseline or it invalidates the comparison.**

| ID | Contamination | Class | Consequence |
|---|---|---|---|
| **C1** | Lookahead in evaluation: regime buckets used **full-sample** slope/vol quantiles. | Methodology | The innovation is causal; the *test around it* is not. Any statistic so conditioned is contaminated. |
| **C2** | Endogenous conditioning: buckets defined by rolling slope — the very quantity that drives the centering gap. | Methodology | We measured the effect inside windows selected *because* they contain the confounder. Circular. |
| **C3** | Scale contamination: `\|mean ε\|` in absolute price units; ADANIENT ran ~50→~3000. | Measurement | The 238-vs-151 gap is dominated by the high-nominal-price parabolic episode; reflects *when* the trend occurred, not estimator quality. Fix: vol-/returns-normalized residuals. |
| **C4** | Tiny effective sample: 499 autocorrelated bars ≈ a few independent trend episodes, one stock, one market. | Methodology | No CIs, no significance (unlike the synthetic Wilcoxon). Anecdote, not result. |
| **C5** | Smoother-induced reversion: a random walk through any smoother yields residual ACF ≈ 0.88 — true for **both** EMA and Kalman ε. | Measurement/structural | ACF/half-life of ε are mechanically inflated; comparing them compares two contaminated quantities. The obvious "measure reversion via ACF" is a trap. |
| **C6** | Serial dependence in the test statistic: sign-runs / `\|mean\|` over contiguous bars. | Measurement | Effective N ≪ nominal; reported numbers have no error bars. |

### 12.5 Net reassessment

- **Demote centering** from a frozen conclusion to an *important-but-insufficient, confounded diagnostic.* It remains useful for visual inspection and as a necessary condition; it is no longer a decision criterion.
- The **mechanism** (EMA lag bias `slope·span/2`) stays confirmed — it is analytic. What is *not* established is that removing it constitutes better **reversion discovery** rather than generic detrending (S1) achieved without signal loss (S2).
- The Step 1 "1.6×" is **unproven**, not weakly-true: it survives neither the detrending control (S1) nor the contamination audit (C1–C4, C6).
- Confidence summary: *mechanism* high; *real-market centering advantage* low; *no-false-centering* medium-low (no systematic appearance, not ruled out); *reversion superiority* — **untested.**

---

## 13. Next Decisive Research Question

**The question is no longer:**

> Does Kalman center residuals better than EMA?

That question is answered (yes, by construction — S1) and demoted (insufficient — §12).

**The active frontier is:**

> Does Kalman ε produce **more causally honest mean reversion** than EMA ε — measured **out-of-sample / walk-forward**, **after subtracting smoother-induced reversion artifacts** (a null), **controlling for the detrending confound** (a naive-detrend baseline, S1), and **without having achieved it by absorbing genuine reversion into the velocity state** (a ground-truth-free δ-discriminator, S2)?

A residual earns "mean-reverting" only if its current level **predicts its own future decay toward zero, out-of-sample, beyond what the same filter manufactures on surrogate data with no real reversion.** Centering, prettiness, raw ACF, and half-life are demoted from the evidence base: insufficient (centering) or smoother-contaminated (ACF/half-life, C5).

This question governs whether Kalman μ\* survives to a further phase. The **minimum-viable falsification plan** answering it is the companion deliverable to this Rev (see project planning record / Part II of the Rev 2 planning note); it is deliberately scoped to ~80% of the information for ~20% of the methodology, and is **not yet executed**. Until it returns a verdict, Kalman remains a research-only comparison estimator and EMA remains production μ\*.

> **▸ UPDATE (Rev 3 → §14).** The **S2 arm only** of this question — *did the velocity state absorb genuine reversion?* — now has minimum-viable instrumentation (the δ-decomposition + walk-forward decay test) and a first pair of manual reads. The surrogate-null and naive-detrend (S1) arms remain unbuilt. §14 records what was built, the first reads, and — emphatically — what is **not** yet concluded.

---

## 14. Step 2A — Structural Falsification Instrumentation (S2 arm) + First Reads

*(Rev 3. This section records the build and first manual use of the minimum-viable instrumentation for the false-centering / signal-absorption arm of §13. It is written to the mandated separation: prior thesis, new instrument, evidence, methodology quality, confidence movement, surviving uncertainty, explicit non-conclusions, next question. The first reads are **observations, not findings** — Surface 3 of the workbench module deliberately renders raw numbers with no verdict engine, and this section honors that.)*

### 14.1 Prior thesis (entering Step 2A)

From §12: the no-false-centering (S2) question was **re-opened for real data** because the only test that had "falsified" it — `corr(ε, true_deviation)` — requires ground truth real markets do not provide. The structural worry (S2, **STRUCTURAL**): the Kalman velocity state `v` may produce a better-centered residual not by discovering equilibrium but by *absorbing genuine mean-reversion into drift* — false centering. The sideways-regime anomaly (§12.2) has exactly this shape and the §12 metric set could not separate the benign reading (A: EMA lags real low-frequency drift; Kalman corrects it) from the pathological one (B: velocity ate the reversion).

### 14.2 New instrument (what was built — additive only)

The decisive realization, confirmed before coding: **there are only two residual systems, bridged by one series.** The "restored" residual is *algebraically identical* to the matched-span EMA one-step prediction residual — it is not a third estimator.

- **δ (velocity contribution).** `δ_t = μ^K_{t|t−1} − μ^{EMA,pred}_t`. The Kalman one-step prediction is recovered from the **frozen** filter output by subtraction — `μ^K_{t|t−1} = close_t − ε^K_t` — with **no filter recomputation** and no new parameter. `μ^{EMA,pred}` is a matched-span EMA prediction; the span comes from the frozen steady-state level gain via the Riccati identity `span = 2/K∞ − 1` (≈ 141 for the frozen constants), i.e. the §7.1 fairness control, not a fit.
- **The restoration identity.** `ε^R = ε^K + δ = close − μ^{EMA,pred}`. ε^K is velocity-**ON** (the integrated-drift estimator); ε^R is velocity-**OFF** (the same level responsiveness, no velocity state). δ is exactly the reversion-or-drift that the velocity state injects. This is the structural lever: comparing the predictive behavior of ε^K vs ε^R isolates *what the velocity state did*.
- **Walk-forward predictive-decay test (METHODOLOGY, deliberately minimal).** For each residual system and horizon `h ∈ {1, 5}`: a single chronological 50/50 split, OLS `Δε_{t→t+h} = α + β·ε_t` fit on the **first** half, then out-of-sample **R²** evaluated on the held-out **second** half (not clamped; may be negative). β < 0 ⇒ deviations predict their own snapback. This is the §13 "predicts its own future decay, out-of-sample" criterion in its cheapest honest form — **not** an in-sample descriptive regression. β is scale-free (immune to C3).

Surfaces: ABS workbench module — Surface 1 (decay table, both systems × both horizons: β, R²ₒₒₛ, n); Surface 2 (δ-vs-price plot — is the velocity contribution structured or noise?); Surface 3 (**raw Δβ = β_restored − β_kalman**, direction, magnitude, cross-horizon consistency — **no verdict text**). Causal firewall test included: a future spike cannot alter δ or ε^K at earlier bars (verified to 1e-9).

### 14.3 Evidence gathered (first manual reads — raw)

| Instrument | Δβ(h=1) | Δβ(h=5) | direction | β magnitudes | R²ₒₒₛ (both systems) |
|---|---|---|---|---|---|
| ADANIENT (real, strong-trend) | −0.00026 | −0.00190 | both < 0 (restored↓) | ~0.01–0.07 | near-zero / negative |
| NIFTY_SYN (synthetic) | −0.0179 | −0.0842 | both < 0 (restored↓) | larger | small / negative |

Reading of the raw numbers (no verdict): Δβ < 0 means the velocity-**OFF** residual predicts snapback *slightly more strongly* than the velocity-ON residual — direction consistent across both horizons on both instruments. On **ADANIENT the separation is tiny** (Δβ ~1e-4 to 2e-3 against β magnitudes ~1e-2) and **R²ₒₒₛ is near-zero/negative for both systems** — neither residual predicts its own decay out-of-sample on this instrument. NIFTY_SYN shows a larger separation but is synthetic and cannot adjudicate real behavior.

### 14.4 Methodology quality

**Strengths.** (i) Out-of-sample, walk-forward — addresses the in-sample-fit contamination that §12 flagged. (ii) δ recovered algebraically from frozen output — **zero** estimator mutation, no new tunable. (iii) Matched-span control equalizes level responsiveness, so the comparison isolates the velocity state specifically (partial S1 control on the *responsiveness* axis). (iv) β scale-free → immune to C3 (price-scale contamination, which sank the Step 1 "1.6×"). (v) Causal firewall unit-tested.

**Limitations (do not overlook).** (i) **Single chronological split, n small** — one OOS window; **C4 (tiny effective sample)** is live, and with R²ₒₒₛ near zero the β separation sits inside plausible noise. (ii) **No surrogate null yet** — Δβ is not yet compared against what the *same filter manufactures on data with no real reversion* (C5, smoother-induced reversion, unaddressed). (iii) **No naive-detrend baseline yet** — the S1 detrending confound is only partially controlled (responsiveness matched, but not "is this just generic detrending?"). (iv) **n=2 instruments, one of them synthetic** — not a panel. (v) No confidence interval / significance on Δβ — by design (Surface 3 is raw).

### 14.5 Confidence update

- **S2 (false-centering) — movement: marginal, direction not yet decisive.** Prior (Rev 2): re-opened, untestable on real data without ground truth. Now: a **ground-truth-free** test for it *exists and runs*. The first real read (ADANIENT) is **consistent with the benign reading (Hypothesis A): the velocity state removed little useful reversion** — but at **LOW** confidence, because R²ₒₒₛ ≈ 0 means the test had little power to detect absorption on this instrument either way. We have an instrument that *could* see absorption; we have not yet *exercised* it on a regime where reversion is strong and real.
- **Methodology capacity — STRENGTHENED to MEDIUM.** We can now ask the S2 question on real markets at all, which §12 said we could not. That is the genuine Rev 3 gain.
- **Reversion superiority (the full §13 question) — unchanged: untested.** Step 2A is the S2 arm only.

### 14.6 Surviving uncertainty (UNRESOLVED)

- Whether ADANIENT's near-zero Δβ is **benign drift removal (A)** or **low test power masking absorption (B)** — R²ₒₒₛ ≈ 0 cannot distinguish these.
- Whether the direction (restored↓, consistent on both instruments) is signal or an artifact of the single split / smoother (no surrogate null to subtract).
- Everything the S1 (naive-detrend) and surrogate-null arms would resolve — still open.
- Real-market behavior in a **strong, genuine reversion regime** — ADANIENT is strong-*trend*; the instrument most likely to expose absorption (range-bound / mean-reverting real series) is not yet in the panel.

### 14.7 Explicit non-conclusions (what Rev 3 does NOT license)

- ❌ "False centering is ruled out / Hypothesis A confirmed." It is not — LOW power on one instrument.
- ❌ "The velocity state is harmless." Untested in the regime that would stress it.
- ❌ "Kalman ε mean-reverts better / worse than EMA ε." The decay R²ₒₒₛ is ~0 for **both** systems here — neither demonstrated reversion; this is not yet a comparison either side wins.
- ❌ Any cross-instrument generalization from n=2 (one synthetic).
- ❌ Promoting Δβ direction to a "finding." Per Surface-3 discipline: *research language gets frozen only after repeated observation across a real panel.*

### 14.8 Next highest-information step

**Run the existing ABS instrumentation across a real multi-instrument panel — manual reads first, no verdict engine.** The blocker is **data, not code**: the panel needs real instruments spanning trend / pullback / sideways / volatile regimes with length ≥ 3× matched-span (≈ 423 bars); currently only ADANIENT qualifies (NIFTY_SYN synthetic, NIFTY50 too short). Priority within the panel: a genuinely **range-bound real series**, the one case that can actually exercise the absorption test. Only after the panel shows a *repeated* pattern does the §13 plan justify spending the remaining ~complexity on the surrogate-null and naive-detrend (S1) arms. Sequence is deliberate: cheap real reads → decide whether the expensive nulls are warranted.

> **▸ UPDATE (Rev 4 → §15).** This step was attempted and **could not be run as specified**: no real multi-instrument panel exists on disk (only ADANIENT qualifies; no market-data fetch capability installed). §15 records the **substitute** that *was* run — the existing ABS instrumentation across pre-declared **intra-instrument regime windows** of ADANIENT — its raw results, and the resulting decision to **freeze the S2 uncertainty as non-blocking**. The cross-instrument panel remains the genuinely-open follow-up if μ\* is ever re-opened.

---

## 15. Step 2A.5 — Final Cheap Empirical Gate (regime-stratified, single real underlying)

*(Rev 4. The "final cheap empirical pass" before freezing μ\* uncertainty and moving up the stack. Mandated separation preserved. The verdict here is a **freeze decision**, not a positive finding about Kalman.)*

### 15.1 Prior thesis (entering the gate)

From §14: the S2 (false-centering / signal-absorption) arm had instrumentation and one full-series read on ADANIENT — tiny Δβ, R²ₒₒₛ ≈ 0, read as *consistent with benign* at **LOW** confidence (low test power). The open worry: a genuinely **range-bound** real regime — not yet tested — was the case most able to expose absorption (velocity eating reversion as drift).

### 15.2 New intel — what changed, and a hard constraint

**The gate could not be run as designed.** A data inventory established that the store holds exactly **one** real instrument with sufficient history (ADANIENT, 2463 bars ≥ 3× matched-span ≈ 423); NIFTY50 (246 bars) is too short, NIFTY_SYN is synthetic, and **no market-data fetch library is installed** (no yfinance / pandas-datareader / etc.) and no other OHLCV files exist on disk. A 4–6 ticker real panel was therefore impossible without methodology/dependency expansion — forbidden by the gate's own scope.

**Substitute actually run (scope-respecting):** the **existing** `compute_velocity_absorption` (frozen function, no new code, no new methodology) on **pre-declared, non-overlapping calendar windows** of ADANIENT, each ≥ 3× matched-span, chosen *before* seeing any Δβ and all reported (no cherry-pick):

- **W1 sideways / round-trip** 2013–2016 (price ~42 → ~42) — the absorption-prone regime (priority case from §14.8).
- **W2 trend-moderate** 2017–2019 (~42 → ~208).
- **W3 trend-parabolic** 2020–2022 (~208 → ~3278).
- **FULL** 2012–2022 (reference; the §14 read).

**MEASUREMENT limitation (decisive for confidence):** these are regime windows of a **single underlying**, not independent tickers. The materiality rule's clause "repeated across real **instruments**" is therefore only **partially** testable — repeats are across-regime and correlated. This structurally caps the verdict at A or B and forbids a confident C.

### 15.3 Evidence gathered (raw — `Δβ = β_restored − β_kalman`; Δβ<0 = absorption-concern direction)

| Window (regime) | Δβ(h=1) | Δβ(h=5) | sign across h | Δβ vs \|β\| | R²ₒₒₛ (K, R) |
|---|---|---|---|---|---|
| W1 sideways | **+0.00084** | **+0.00432** | + / + (anti-absorption) | ~4–5% | ≈0 / neg |
| W2 trend-mod | **−0.00231** | **−0.01054** | − / − | ~10–12% | +0.01…+0.05 |
| W3 trend-para | **+0.00835** | **+0.03488** | + / + (anti-absorption) | ~30% (h=5) | small + |
| FULL ref | −0.00026 | −0.00190 | − / − (trivial) | ~3% | ≈0 |

Reproduce: existing endpoint `GET /ADANIENT/velocity-absorption?start=&end=` per window, or the frozen `analytics.compute_velocity_absorption` on date-sliced closes. No artifact committed (inline pass).

### 15.4 Methodology quality

**Strengths.** Existing frozen instrumentation; OOS walk-forward; scale-free β (C3-immune); pre-declared windows reported in full; the absorption-prone regime explicitly included. **Limitations.** Single underlying (no cross-instrument independence — the central one); single chronological split per window (C4 live); R²ₒₒₛ ≈ 0 ⇒ low power throughout; no surrogate null, no naive-detrend (S1) — unchanged, by scope.

### 15.5 Confidence update

- **Catastrophic false-centering (the C case) — EXCLUDED, confidence LOW-MEDIUM.** Required signature is *large, repeated, negative* Δβ. Observed: Δβ **sign flips across regimes** (W1 +, W2 −, W3 +, FULL −); the absorption-prone sideways regime carries the **anti-absorption** sign; the only negative Δβ of any size sits in a *trend* window (benign drift-removal context) at ~10% of \|β\|. No repeated negative pattern exists.
- **New robust observation — MEDIUM:** R²ₒₒₛ ≈ 0 for **both** residual systems in **every** regime → on real ADANIENT neither estimator's residual predicts its own decay out-of-sample. *There is little OOS-useful reversion for the velocity state to absorb in the first place* — which makes catastrophic absorption nearly moot here and reinforces the §13 demotion of in-sample ACF/half-life as smoother-contaminated.
- **S2 net:** §14's tentative benign read is **STRENGTHENED** to a non-blocking freeze — now covering the worry regime — though still on one underlying.

### 15.6 Surviving uncertainty (UNRESOLVED)

- The **fine structure** — why Δβ sign is regime-dependent (benign in sideways/parabolic, mildly concern-signed in moderate-trend) — is unresolved and below the noise floor (R²ₒₒₛ ≈ 0). Not pursued: would require the forbidden nulls.
- **Cross-instrument replication** never happened — the central evidentiary gap. Any generalization beyond ADANIENT is unlicensed.
- Whether Kalman ε reverts *better than* EMA ε out-of-sample — still untested and, on this evidence, neither does so meaningfully on real data.

### 15.7 Explicit non-conclusions

- ❌ "False centering is ruled out" → no; only the **catastrophic** case is excluded, on one underlying, at low power.
- ❌ "Kalman ε mean-reverts on real markets" → R²ₒₒₛ ≈ 0; not demonstrated for either estimator.
- ❌ "Benign confirmed (A)" → sign incoherence + ~0 power forbid the clean-benign claim; this is **B (unresolved, non-blocking)**.
- ❌ Any cross-ticker generalization.

### 15.8 Decision — PROVISIONAL FREEZE (weak, non-blocking)

**Classification: B — mixed/unresolved, non-blocking; C excluded.** Per the gate's decision objective, both A and B → **freeze the S2 / μ\* uncertainty and move upward in the stack.** The catastrophic case that would force "stop and revisit μ\*" did not appear, and the residual carries little OOS-predictable reversion for either estimator.

**The freeze is explicitly PROVISIONAL (researcher decision, Rev 4).** It rests on **one real underlying** at low statistical power; it is *not* a validated cross-instrument result. We proceed up the stack now, but the freeze is flagged **weak / low-confidence** so it is revisited early rather than treated as settled.

**Revisit trigger (binding).** Before any upstream component is allowed to **depend on μ\* reversion fidelity** — i.e. treat the Kalman/EMA residual as a *trustworthy mean-reverting signal* for State-T detection, equilibrium-conditioned logic, or anything downstream that would be wrong if the residual does not actually revert — this freeze must be **re-opened** and the **genuine cross-instrument panel** (§14.8) run first, ahead of the surrogate-null / naive-detrend (S1) arms. Uses that only need μ\* as a *descriptive centering line* (visual inspection, replay, diagnostics) do **not** trigger re-opening. Kalman remains a research-only comparison estimator; EMA remains production μ\*.

> **▸ CONTEXT (placeholder framing — added post-audit, no finding changed).** The "one real
> underlying" above is **ADANIENT, a placeholder visual substrate** (chosen for live moving data /
> observability / debugging), **not** a representative of the intended deployment domain
> (commodities · pairs · cross-asset relative value · spread structures — materially more
> mean-reverting). ADANIENT is **trend-heavy**; the deployment regime is expected to be the
> opposite. The §15 real reads are therefore **trend-regime conditioned and deployment-regime
> untested by default.** This does not change the verdict, the **B** classification, or the
> **provisional / weak / non-blocking** framing — it only clarifies that the binding cross-instrument
> panel must specifically include the **mean-reverting deployment regime**; ADANIENT evidence is
> local to its regime and is not global evidence. See `CONTINUATION_STATE.md` §0.

---

## Appendix — Reproduction & Record Corrections

**Reproduce.**

- Calibration sweep: `backend/scripts/calibrate_kalman.py` → `/tmp/cal_table.txt`
- Replication audit (4 experiments): `backend/scripts/audit_kalman.py` → `/tmp/audit_exp{2,3,4}.txt`
- Confirmatory test (360 conditions × 4 SNRs): `backend/scripts/confirm_kalman.py` → `/tmp/confirm.txt`
- Estimator: `backend/app/services/analytics.py::compute_kalman_mu_star` (SNR knob, κ = 0.05, MAD-normalized R)
- Generators: `backend/app/services/synthetic.py` (8 ground-truth processes incl. `ou_in_trend`)
- **Step 1 (Rev 2):** real-market pass `backend/scripts/eval_kalman_real.py` → `/tmp/eval_real.txt`; integration in `backend/app/routers/market.py` (`/diagnostics` carries both estimators) and `frontend/src/components/workbench/modules/EstimatorCompare.tsx` (CMP module).
- **Step 2A (Rev 3):** δ-decomposition + walk-forward decay in `backend/app/services/analytics.py` (`kalman_steady_state_gain`, `_walk_forward_decay`, `compute_velocity_absorption` — μ^K_pred recovered by subtraction, no filter recompute); read-only endpoint `GET /{instrument_id}/velocity-absorption` in `backend/app/routers/market.py`; models `ReversionStat` / `VelocityAbsorptionRow` / `VelocityAbsorptionResponse` in `backend/app/models/market.py`; workbench `frontend/src/components/workbench/modules/VelocityAbsorption.tsx` (ABS module, Surface 3 raw-only, no verdict engine); locks in `backend/tests/test_velocity_absorption.py` (restoration identity, matched-span derivation, causal firewall, OOS finiteness — 4 pass; full suite 57 pass).

**Record corrections (status).** Items carrying the overturned KC4/KC1 rationale:

- `backend/app/services/analytics.py` — header comment corrected during Step 1 (Rev 2): now records the overturned verdict, the centering advantage, and the §12 demotion. **Done.**
- `docs/research/05_kalman_v1_results_memo.md` — **Done (Rev 4 audit).** A SUPERSEDED banner now heads the file: the REJECTED verdict is marked overturned (points here, §6/§8/§15), the memo is retained unaltered as the Rev-0 historical record, and the frozen Kalman equations it pins are noted as still correct.
- `backend/tests/test_kalman_validation.py` — **Docstring annotated (Rev 4 audit); assertion-reframe still Pending, blocked on §13.** A STATUS NOTE at the top records that the REJECTION verdict was overturned and that the green assertions are a *measurement* lock on synthetic data, not a current verdict. Assertions are deliberately **unchanged** — per §12 they must NOT be reframed to lock in *centering* (demoted), and the §13 causal-reversion criterion has no verdict yet (the cross-instrument MVF never ran; the §15 freeze is provisional). Step 2A's `test_velocity_absorption.py` locks only the *instrumentation* (identity, firewall, finiteness), not a pass/fail reversion gate.

This document is the authoritative record. §1–§11 = Rev 1 (synthetic arc); §12–§13 = Rev 2 (real-market reassessment + open frontier); §14 = Rev 3 (Step 2A S2-arm instrumentation + first reads); §15 = Rev 4 (Step 2A.5 final cheap gate → freeze S2/μ\* uncertainty as non-blocking).
