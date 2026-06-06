# Temporal Ontology of Mean Reversion

**Document class:** AMR research memo — Team B (Temporal Ontology Lab) (DRAFT — pending red-team + approval).
**Status:** REVISED & APPROVED for promotion → doc 14 (red-team revisions applied 2026-06-03).

> **▸ RED-TEAM REVISION APPLIED (binding).** VR(q) is **not "trap-free."** It is *consistent but small-sample biased* (overlapping-window bias; Lo–MacKinlay z\* heteroskedasticity sensitivity) precisely in AMR's W≤250 / q≤20 regime. It remains the **least-bad** richer temporal object, but is admissible **only as real-minus-matched-surrogate** (each instrument vs its own OU/RW/GARCH surrogate under identical extraction), **never as a raw curve**. Wherever this memo says VR(q) is "trap-free," read "trap-resistant only under surrogate-relative use."

**Date:** 2026-06-03.
**Author hat:** quant researcher / skeptical collaborator (Research Mode — no implementation, no MRScore, no State-T resurrection).

> **What this memo is.** A reasoning document about what *time* means inside mean reversion (MR) and how it can exist *causally* inside AMR. It asks of every temporal object the lookahead-constitution question — *could this exist at `t` with only information available at `t`?* — and treats the answer "no, but it was tuned to look like yes" as the central danger. It builds on the repo's already-frozen findings (κ̂ noise floor, smoother-manufactured ACF, conditioning-is-not-free, VR-as-curve, equilibrium-stability-as-discriminator) and does **not** re-derive them. Citations give author/year/venue; where a fact could not be confirmed from the source it is marked **unverified**.

> **▸ CONTEXT (placeholder framing — frozen, CLAUDE.md §1.1).** All repo real-market numbers cited below are ADANIENT (trend-heavy placeholder). The deployment domain (commodities · pairs · cross-asset RV · spreads) is expected materially more mean-reverting. Every real-market conclusion here is **regime-local, not global**.

---

## 0. Thesis in one paragraph

Inside MR, "time" is not one number. The literature and the repo agree on a sharper statement: the *speed* of reversion (κ, equivalently the half-life `ln2/κ`) is the single most economically load-bearing temporal quantity **and** the single worst-estimated one, because the regime AMR targets (genuine but slow reversion) sits arbitrarily close to the unit root, exactly where κ̂ has its largest variance and bias. Every attempt to make AMR "adaptive in time" — pick the best window, the best horizon, the best half-life, let the decay rate drift with regime — is therefore an attempt to estimate a quantity that is near-unidentifiable in-sample, and the danger is not that it fails loudly but that it fails *silently by laundering hindsight*: a parameter chosen with future information looks adaptive, prints a clean backtest, and dies out-of-sample. The recommended causal stance is consequently conservative: **time enters AMR as a small, pre-registered, fixed horizon *set*, reported as a profile/curve (never `min()`-collapsed for decision use), with NO online half-life estimation, NO regime-conditioned decay, and NO window/horizon selection on in-sample fit** — adaptivity is admitted *only* where it is mechanically causal by construction (a filter's recursion) and *never* where a free parameter is tuned to data the decision will be evaluated on.

---

## 1. The object: what "time" is inside mean reversion

A mean-reverting price/spread is canonically the Ornstein–Uhlenbeck (OU) process (continuous time) or its AR(1) discretization:

```
dX_t = κ(θ − X_t) dt + σ dW_t          (OU; κ = reversion speed, θ = level, σ = vol)
X_t  = c + φ X_{t−1} + ε_t             (AR(1);  φ = e^{−κΔ},  κ = −ln φ / Δ)
half-life  H = ln2 / κ = ln2 / (−ln φ)
```

There are at least **four** distinct temporal objects entangled here, and conflating them is the first error:

1. **The level θ (equilibrium μ\*).** *Where* it reverts to. The repo's Kalman/EMA line (docs 05/06) is about estimating θ causally; the validated discriminator there is **equilibrium stability — "did μ\* stay put?"** (doc 08 §F1), not "did price come back."
2. **The speed κ / half-life H.** *How fast* it reverts. This memo's primary subject. It is a **nuisance parameter** in the statistical sense — not the object of interest economically (the edge is the reversion itself), but required to size, time, and even *detect* reversion — and it is the fragile one.
3. **The horizon q.** *Over what holding/measurement interval* reversion is assessed. The repo's MRScore is multi-horizon (DRC over h∈{1,3,5}, VR over q∈{2,5,10,20}) then `min()`-collapsed to frozen 20/60/20 weights (doc 09 §3.2). VR(q) is **inherently** a function of q (Lo–MacKinlay 1988).
4. **The regime clock.** *Whether κ itself moves through time* (time-varying / regime-switching decay). This is where "adaptivity" lives — and where laundered lookahead is most dangerous.

**Critical pre-registered claim, inherited not re-derived:** residual ACF and residual half-life are **smoother-manufactured** (doc 06 C5; doc 08 §7) — a pure random walk run through an EMA produces residual ACF(1)≈0.88, half-life≈6. Therefore object (2) **must not** be read off a smoother residual's ACF; the only trap-free reading of reversion *character* is **return-space variance ratio** (object 3), and the only trap-free reading of *equilibrium quality* is stability of θ (object 1). This memo treats (2) accordingly: half-life is a quantity we are forced to reason about but must never naively estimate from residual persistence.

---

## 2. OU half-life instability — why κ̂ is a fragile nuisance parameter

This is the load-bearing technical section. Three independent reasons converge on the same verdict: **the half-life is near-unidentifiable in exactly the regime AMR cares about.**

### 2.1 The repo's own measurement (the anchor)

doc 04 §1.5.3 simulated 2000 windows of 60 daily bars at the near-unit-root values that characterize slow real reversion:

| True φ | True κ | Mean φ̂ | Bias in φ̂ | SD(κ̂) |
|---:|---:|---:|---:|---:|
| 0.98 | 0.0202 | 0.892 | −0.088 | 0.083 |
| 0.95 | 0.0513 | 0.863 | −0.087 | 0.093 |

**`SD(κ̂) ≈ 0.083–0.093` is larger than κ itself (≈0.020–0.051), and the bias in φ̂ (≈−0.088) is several times κ.** The repo's verdict is verbatim: *"Detecting Δκ over a short window is statistically hopeless at daily frequency near the unit root. This is not a tuning problem; it is intrinsic."* Everything below is the external literature explaining *why* this is intrinsic, not a coding artifact — i.e., the repo's empirical finding is the textbook result.

### 2.2 Finite-sample / near-unit-root bias of κ̂ (the estimator literature)

- **Yu, J. (2012), "Bias in the estimation of the mean reversion parameter in continuous time models," *Journal of Econometrics* 169(1):114–122.** Derives the bias of the ML/LS estimator of κ in the Gaussian OU process. The central finding directly matches the repo: **the bias is most severe precisely when reversion is slow (the near-unit-root regime), which is the empirically realistic case for financial series**, and standard first-order bias approximations *break down* there. κ̂ is **upward-biased** (overstates reversion speed) — i.e., the estimator systematically tells you the series reverts faster than it does, which is the most dangerous possible direction for a strategy that bets on reversion completing within a holding horizon.
- **Bao, Ullah, Wang & Yu (2013/2015), "Bias in the Mean Reversion Estimator in Continuous-Time Gaussian and Lévy Processes," *Economics Letters* 134:16–19** (and the SKEMA/CoFiE WP 03-2013 version). Extends the bias result and adds a nonlinear correction term; confirms standard bias formulas "do not work satisfactorily when the speed of mean reversion is slow."
- **Wang, Phillips & Yu, "Exact Distribution of the Mean Reversion Estimator in the Ornstein–Uhlenbeck Process" (UC Riverside WP 201413; published vicinity *Journal of Econometrics*, **unverified** exact venue).** Shows the finite-sample distribution of κ̂ is **severely skewed and can be multi-modal**, so even the *shape* of the estimator's sampling distribution defeats symmetric ±SD reasoning — confidence statements built on asymptotic normality are simply wrong near the unit root.

**Implication.** The repo's SD(κ̂)≈0.09 is not the whole story; the distribution is skewed, so a point κ̂ plus a naive standard error understates how badly you know the half-life. The half-life `H = ln2/κ` inherits this through a **nonlinear, variance-amplifying** transform: as κ̂ → 0, `H → ∞`, so the upper tail of the half-life estimate is effectively unbounded.

### 2.3 The half-life confidence interval is uninformative (the macro/PPP literature)

The cleanest external demonstration that half-life is a fragile nuisance parameter comes from the purchasing-power-parity "persistence puzzle," where the entire empirical question *is* a half-life:

- **Murray & Papell (2002), "The purchasing power parity persistence paradigm," *Journal of International Economics* 56(1):1–19.** Computing half-life CIs that account for serial correlation, sampling uncertainty, and small-sample bias, they find **the upper confidence limit of the half-life is *infinite* for every exchange rate considered**, and conclude single-equation methods "provide virtually no information regarding the size of the half-lives."
- **Stock, J. (1991), "Confidence intervals for the largest autoregressive root in U.S. macroeconomic time series," *Journal of Monetary Economics* 28:435–459.** The foundational local-to-unity result: CIs for the dominant AR root near one (by inverting ADF t-tests) are **typically wide** on real macro data. This is the inferential root cause of 2.2–2.3: near the unit root the likelihood is flat in φ, so the data barely constrain it.
- **Phillips (2014), "On Confidence Intervals for Autoregressive Roots and Predictive Regression," *Econometrica* 82(3):1177–1195** (**page range unverified**). Sharpens the warning: Stock-type CIs are valid *local-to-unity* but become **invalid at the stationary boundary** (locational bias + width distortion) — so even the standard fix for near-unit-root inference misbehaves exactly where a "mildly mean-reverting" series lives.

**Synthesis (object 2).** The half-life is (i) **biased** (Yu 2012, repo doc 04), (ii) **high-variance** relative to its own magnitude (repo SD(κ̂)≈0.09 > κ), (iii) **skewed/multi-modal** in finite samples (Wang–Phillips–Yu), and (iv) **bounded-above only by ∞** in CI terms (Murray–Papell). It is the textbook fragile nuisance parameter. **Any AMR component that consumes a point half-life as if it were known is consuming noise dressed as a number.** This is a STRUCTURAL constraint, not a MEASUREMENT one — no estimator choice repairs a flat likelihood.

---

## 3. Regime-dependent / time-varying decay — does reversion speed change, and does modelling it pay?

Two separable questions: **(A) does κ actually move with regime?** (a fact question) and **(B) does *modelling* κ-drift earn its complexity *causally / OOS*?** (a methodology question). The repo has already answered (B) for the general case; the literature lets us answer (A) carefully and check (B) against named methods.

### 3.1 Does κ move? (supporting evidence — fact question A)

Yes, there is real economic structure to reversion-speed variation:

- **Regime-switching MR is a well-populated literature.** Pairs/stat-arb work routinely models the spread as a mean-reverting process whose parameters switch with a hidden Markov chain — e.g. Vasicek-with-regime-switching pairs models (S&P 500 evidence; *International Review of Financial Analysis*, **exact cite unverified**), and HMM stat-arb on crude-oil futures (arXiv:2309.00875, 2023). The motivation is concrete: **structural breaks make a constant-κ model bet on reversion that never completes**, producing the classic "spread blew through the band and never came back" loss.
- **Foundational regime-switching machinery.** Hamilton (1989), "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle," *Econometrica* 57:357–384. Survey: **Ang & Timmermann (2012), "Regime Changes and Financial Markets," *Annual Review of Financial Economics* 4:313–337** — which *itself* flags that regime-switching parameters carry substantial **estimation error and identification/misspecification risk** (corroborated by Guidolin–Timmermann).
- **The repo's own corroboration that "regime" matters for character:** doc 10 Finding 1 — substrate character is strongly **scale-dependent** (ADANIENT reads RW-Null at 60–500-bar causal windows despite being a macro trend). This is the same phenomenon viewed through horizon rather than calendar regime: the apparent reversion structure is not a fixed property of the series.

So (A) is **plausibly yes** — κ is not a universal constant.

### 3.2 Does modelling κ-drift pay OOS? (opposing evidence — methodology question B)

This is where the repo's frozen lesson binds hardest, and the named TVP/DMA methods must be judged against it.

- **The conditioning penalty (already frozen, doc 04 lesson 3, after Goyal & Welch 2008, *RFS* 21(4)):** unconditional forecasts beat conditional ones OOS *because conditioning adds estimated parameters and estimation noise overwhelms the signal*. **"Conditioning is not free. Any regime-conditioned weighting must beat its own unconditional baseline OOS or be rejected."** A time-varying-κ model is exactly a conditioning scheme; it inherits this penalty by default.
- **Dangl & Halling (2012), "Predictive regressions with time-varying coefficients," *Journal of Financial Economics* 106(1):157–181.** The strongest *pro-TVP* evidence: a Bayesian TVP framework on monthly S&P 500 returns shows OOS predictability and utility gains of ≈1.8–5.8%/yr, with TVP models dominating constant-coefficient ones. **But read carefully against the danger:** their gains come from a *fully Bayesian* treatment that integrates over coefficient paths and **shrinks hard** (the time-variation is heavily disciplined by priors, not free), and the object is the *return predictive coefficient*, not κ near the unit root. It is evidence that disciplined time-variation *can* pay — **not** that estimating a drifting half-life on a 60-bar window pays.
- **Koop & Korobilis (2012), "Forecasting Inflation Using Dynamic Model Averaging," *International Economic Review* 53(3):867–886.** DMA with two forgetting factors (λ, α ∈ (0,1]); observations j periods back get weight λ^j. Reports substantial gains over TVP and fixed benchmarks for inflation. **The AMR-relevant caveat:** the forgetting factors are themselves free parameters, and the repo's own methodology map (doc 04 §2.4.2) already adjudicated DMA/Bayesian forgetting as **"Defer (denser data); λ overfit-prone"** and time-varying relevance as something that *"must be done parsimoniously, or instability-tracking degenerates into noise-tracking."* DMA earns its keep on monthly macro series with decades of data and a genuine model-instability problem; it is **not** obviously transportable to a single short spread where κ is already near-unidentifiable.

**Verdict on (B):** modelling κ-drift **does not earn its complexity by default in the AMR setting.** The pro-evidence (Dangl–Halling, Koop–Korobilis) is real but lives in data-rich, heavily-shrunk regimes and concerns *predictive coefficients*, not *near-unit-root reversion speed on short windows*. Importing a forgetting-factor or Markov-κ layer into AMR **imports estimation noise** (3.1's Ang–Timmermann estimation-error warning × 2.2's κ̂ instability) and must clear the doc-04 bar: **beat its own unconditional / fixed-κ baseline OOS, under purged CV and a surrogate null, or be rejected.** Default expectation: it will not.

---

## 4. Multi-timescale MR — should AMR model a horizon *profile/curve* rather than a scalar?

**Yes — and this is the one place the literature and the repo jointly *recommend* a richer temporal object, because the curve is cheap, model-free, and trap-resistant.**

- **Lo & MacKinlay (1988), "Stock market prices do not follow random walks," *Review of Financial Studies* 1(1):41–66.** VR(q) = Var(q-period return)/(q·Var(1-period return)); =1 under random walk, **<1 ⇒ mean reversion, >1 ⇒ momentum**. Crucially VR is **defined as a function of q** — there is no single "the variance ratio." The heteroskedasticity-robust z\* statistic makes it usable under ARCH/GARCH.
- **The repo already knows character flips with horizon** (CLAUDE.md established-fact (c): "substrate character is a function of horizon — Lo–MacKinlay VR flips sign with q"; doc 10 Finding 1; doc 04 separation `S = τ/half-life` as a ratio of two near-unit-root estimates). The repo's post-State-T review (doc 12 §3) *already split the verdict*: **report VR/DRC as a curve over horizon = YES; `min()`-collapse or adaptive-weight it = NO.**
- **Why a scalar is actively misleading:** the existing MRScore `min()`-aggregation (doc 09) collapses the q-profile into one number, and doc 09 §3 showed the self-ranked collapse **inverts** (a pure RW scored highest, 62.5 vs ANCHOR_OU 55.6). The collapse destroys the very information — *at which horizons does this behave OU-like vs RW-like* — that distinguishes a reverter from a null. A spread can be VR<1 at q=5 and VR≈1 at q=20; that shape *is* the signal, and `min()` throws it away while manufacturing a false ranking.

**Recommended temporal object:** AMR should carry a **horizon profile** — `VR(q)` (and optionally a decay/DRC curve) over a small fixed q-grid — as a *displayed curve with heteroskedastic-robust CIs*, **not** a collapsed scalar feeding a decision. This is causal (each VR(q) at bar t uses only `[t−W+1, t]`, already implemented in the Substrate engine, doc 10 §2), model-free (no κ to estimate), and escapes the smoother trap (return space). It is the *cheapest honest* upgrade to AMR's temporal ontology.

**Caveat (failure mode, from doc 12 / doc 10):** a horizon curve **multiplies researcher degrees of freedom** (VR(short)≠VR(long) ⇒ "pick the q that looks reverting" is a new selection trap). It must be (i) a *pre-registered* fixed q-grid, (ii) characterized **unconditionally** (not on |z|-anchored windows — that re-enters the selection-on-deviation trap that killed State-T morphology, doc 11/doc 12), and (iii) compared to a **matched OU/RW/GARCH surrogate** under identical extraction. The curve is an *observable*, not a free knob.

---

## 5. Adaptive filtering — where adaptivity is legitimate vs laundered lookahead

The cleanest way to separate honest from dishonest adaptivity: **does the adaptive quantity have a one-sided recursive definition (computable at t from past only), or is it the argmax of an in-sample objective over a parameter the decision is scored on?**

### 5.1 Legitimately causal adaptivity (recursion-defined)

- **Kalman filter (the repo's frozen 2-state μ\*).** The filtered state `x_{t|t}` and one-step innovation `P_t − μ_{t|t−1}` are **defined by a forward recursion** — structurally causal, firewall-verifiable (doc 06: a future spike leaves prior μ\* bit-identical). The repo's frozen constants (κ=0.05, single SNR knob, MAD-normalized R) are *fixed in advance, not fit per instrument* — which is exactly what keeps the adaptivity honest. **Refitting those constants per instrument on its own history would be a §6.3 freeze-break** and would convert honest adaptivity into in-sample tuning (doc 12 Arm C explicitly forbids this).
- **Particle filters / adaptive bandwidth** are *capable* of honest causal adaptivity (sequential, past-only updating). They become laundered lookahead the moment a hyperparameter (bandwidth h, process-noise Q, resampling threshold, the forgetting λ of §3.2) is **selected on the full sample** or tuned to optimize a backtest. The recursion is causal; the *hyperparameter selection* is where future information leaks in.

### 5.2 Laundered lookahead (selection-defined) — the danger

- The Kalman/EMA "does ε revert better" question is **the wrong, smoother-contaminated question** (doc 12 Arm C; doc 07 lag illusion): a faster-adapting μ\* *mechanically* manufactures a more-reverting, lower-variance residual (the **lag illusion**, doc 07) — a self-fulfilling adaptivity. doc 07 was **KILLED** on this exact ground (Mode B false-reversion), with a binding reopen only on a genuine range-bound instrument.
- **The general principle:** adaptivity is legitimate iff the adaptive value at t is a deterministic function of `data[≤ t]` *and* every hyperparameter governing the recursion was frozen before seeing the evaluation period. Adaptivity is **laundered lookahead** iff any tuning step ranges over the data the decision is evaluated on — including the "innocent" choices: which window length, which half-life, which horizon, which forgetting factor, which regime count.

---

## 6. Stat-arb horizon literature & regime-switching of horizons (where the half-life actually bites economically)

- **Avellaneda & Lee (2010), "Statistical arbitrage in the US equities market," *Quantitative Finance* 10(7):761–782.** The most operationally explicit treatment of reversion *time* as a tradeability gate: they **only trade an eigenportfolio if its estimated reversion is fast enough — κ > 252/30 = 8.4 (reversion time < ½ period)**. This is the half-life used as a *hard filter*: too slow ⇒ untradeable. **The AMR lesson is double-edged:** (i) it confirms half-life is economically central (you cannot size or hold a position without it); (ii) it means the strategy's *universe selection* depends on κ̂ — and per §2 that estimate is biased upward (Yu 2012), so a κ>8.4 filter **systematically admits spreads that look fast enough but are not**, the precise hidden failure mode. Avellaneda–Lee partly mitigate by estimating on a fixed 60-day window with stated rules (pre-registered, not tuned) — itself a model of disciplined causal practice.
- **Leung & Li (2015), "Optimal Mean Reversion Trading with Transaction Costs and Stop-Loss Exit," *International Journal of Theoretical and Applied Finance* 18(3)** (also the 2016 Princeton monograph). Derives optimal entry/exit *as price intervals* under an OU spread with costs and stop-loss. **Relevance:** the entire optimal policy is a *function of κ, θ, σ*; the timing object is endogenous to the (badly-estimated) parameters. It is a clean statement that "when to act" in MR is parameter-driven — which is exactly why parameter fragility (§2) propagates into timing fragility, and why AMR's observatory-first posture (observe/falsify *before* timing) is the correct ordering: you cannot honestly optimize entry timing on a half-life you cannot estimate.
- **Regime-switching of horizons:** the pairs-trading-with-regime-switching literature (§3.1) is, viewed temporally, exactly "the relevant horizon switches with regime." The honest version (online filter-based parameter estimation, e.g. arXiv:2309.00875) is causal; the dishonest version fits the regime dates on the full sample and reports the in-sample fit.

---

## 7. Core question — how should time exist *causally* inside AMR? (recommended stance)

Three candidate stances, judged against the lookahead constitution and the repo's frozen findings:

| Stance | What it is | Verdict |
|---|---|---|
| **(S-A) Fixed pre-registered horizon set** | A small frozen grid of horizons/windows (e.g. VR over q∈{2,5,10,20}; μ\* span fixed), reported as a profile. No online parameter estimation. | **RECOMMENDED (primary).** Maximally causal; zero selection DOF; trap-resistant (return-space curve); already half-built (Substrate engine). |
| **(S-B) Online-estimated profile/half-life** | Estimate κ / half-life / best horizon online and let it drive decisions. | **REJECT for v0.** §2: κ̂ is biased + high-variance + skewed + ∞-CI near the unit root; §3.2: conditioning penalty. It *imports* noise and is the laundered-lookahead vector. |
| **(S-C) Regime-conditioned / adaptive decay** | Markov-κ or DMA forgetting-factor decay that drifts with regime. | **REJECT for v0; DEFER as research.** §3.2: does not beat unconditional baseline by default; Ang–Timmermann estimation error; doc 04 already filed DMA as "Defer (denser data), λ overfit-prone." Reopen only on dense data + a downstream consumer + an OOS win over fixed-κ. |

### Recommended causal stance (the answer)

**Time enters AMR as a fixed, small, pre-registered horizon *set*, surfaced as a profile/curve, with the half-life treated as an UNCERTAINTY to be displayed, never a scalar to be consumed.** Concretely:

1. **Horizon = a frozen q-grid, reported as a VR(q) curve** (+ optionally a DRC/decay curve) with heteroskedastic-robust CIs — **never `min()`-collapsed** for any decision (doc 09 inversion; doc 12 split verdict). The curve *is* the temporal object; its shape is the information.
2. **κ / half-life is reported as an interval, never a point, and never used as a hard gate in v0.** If a half-life must be shown, show it with its (wide, possibly ∞-upper) CI per §2.3, explicitly framed as "we do not know this well." It may inform *intuition*; it may not *gate* in v0.
3. **No online half-life/window/horizon *selection*.** The forbidden operation is `argmax over {window, horizon, half-life, λ, regime-count} of in-sample fit`. This is the single most important rule and the subject of §8.
4. **Adaptivity only where recursion-causal.** The Kalman recursion is fine *with its frozen constants*; particle/adaptive-bandwidth filters are fine *only* if every hyperparameter is pre-frozen. Per-instrument refit of frozen filter constants = freeze-break = forbidden without explicit authorization.
5. **The discriminator stays equilibrium stability + return-space VR, not residual reversion** (doc 08; doc 12 §2) — because residual-ACF/half-life are smoother-manufactured (C5). Time-quality is judged by "did μ\* stay put" and "does VR(q) separate from a matched null," not by "did the residual revert."
6. **If/when S-C is ever revisited:** it must (a) clear a *new* freeze-break justification, (b) have a concrete downstream consumer (doc 12 Arm C: "do not solve a problem nothing has"), (c) beat its own fixed-κ / unconditional baseline OOS under purged CV + surrogate null, and (d) run on data dense enough that κ̂ is identifiable (intraday or long panels, not single short daily spreads).

**Why this is the right ordering (observatory-first, CLAUDE.md §10):** you cannot honestly *operationalize* a temporal parameter you cannot *estimate*. The fixed-grid profile lets AMR *observe* the multi-timescale structure (the legitimate scientific goal) without *betting* on a number the data refuses to pin down. Richer time-models earn entry only after the profile is observed, a verified mean-reverting habitat exists (doc 12 Arm A is the precondition), and a concrete consumer demands it.

---

## 8. Implementation dangers — hidden hindsight disguised as adaptivity (ranked, with mechanisms)

The lookahead constitution names this the single most important danger. Concrete mechanisms by which it enters AMR's temporal layer, **ranked by likelihood × harm**:

### DANGER 1 (highest) — Full-sample-tuned "adaptive" window / horizon / half-life

**Mechanism.** Choose the lookback window W, the horizon q, or the half-life H that *maximizes in-sample reversion evidence* (best VR, best DRC, best backtest), then present the resulting per-bar value as "adaptive." Because the parameter was selected with knowledge of the whole sample, the apparent adaptivity is **future information compressed into a hyperparameter**. The series then "reverts beautifully" in-sample and dies OOS.
**Why it is near-invisible.** It produces *exactly* the chart an honest adaptive method would; the leak is in the *selection step*, which leaves no trace in the per-bar computation. Bailey & López de Prado (2014), "The Deflated Sharpe Ratio," *Journal of Portfolio Management* 40(5):94–107, and the Probability of Backtest Overfitting (Bailey, Borwein, López de Prado & Zhu, 2014/2017) formalize this: try N variations, keep the best, and the max Sharpe is inflated **even if all N are pure noise**. A swept window/horizon grid is precisely N trials.
**AMR-specific bite.** §2: because κ̂ is biased upward and high-variance, the "best-looking" window is disproportionately the one whose noise draw *overstates* reversion — selection actively seeks the most misleading window. doc 09 §3 already showed a self-ranked collapse can rank a pure RW highest; window/horizon selection is the same pathology one level up.
**Mitigation (binding).** Pre-register the grid; never select on the evaluation period; report the *whole* curve, not the argmax; deflate any performance number for the number of trials; compare to a matched surrogate null under identical extraction.

### DANGER 2 — Lag-illusion adaptivity (faster μ\* manufactures reversion)

**Mechanism.** Make μ\* "adapt faster" (raise the Kalman SNR / shrink the EMA span / add a velocity term) so the residual looks more mean-reverting. doc 07 proved this is **mechanically self-fulfilling**: a faster-adapting equilibrium drags ε toward zero (Mode B), forging apparent reversion that the honest deviation never had. doc 04 §1.5.4: a lagging μ\* "makes ε=P−μ\* revert as μ\* catches up, manufacturing AR(1)↓ and variance↓," and *"this bias is systematic, so it is not caught by the frozen P3 small-perturbation test."*
**Why it is near-invisible.** It passes the standard perturbation/firewall test (the recursion *is* causal); the contamination is structural, not temporal. The KILLED verdict on doc 07 (#12 LAG) stands on exactly this.
**Mitigation (binding).** Judge μ\* by **equilibrium stability ("did μ\* stay put")**, never by residual reversion (doc 08 §F1). Keep filter constants frozen; no per-instrument SNR/span tuning. Reopen the residual-reversion question only with a surrogate null that subtracts what the *same* filter manufactures on no-reversion data (doc 06 §13 plan).

### DANGER 3 — Regime-conditioned decay that is really noise-tracking

**Mechanism.** Let κ drift with an estimated regime (Markov-κ, DMA forgetting factor). Because SD(κ̂) > κ near the unit root (§2.1) and regime parameters carry heavy estimation error (Ang–Timmermann 2012), the "regime-varying half-life" is **mostly tracking sampling noise**, but each wiggle is rationalized as a regime change. doc 04 lesson 4: time-varying relevance *"must be done parsimoniously, or instability-tracking degenerates into noise-tracking."*
**Why it is near-invisible.** Regime stories are post-hoc-plausible (every κ̂ jump "corresponds to" some market event), and in-sample the conditioned model always fits better (more parameters). The leak hides in the *narrative*, not the math.
**Mitigation (binding).** Conditioning must beat its own *unconditional* baseline OOS or be rejected (doc 04 lesson 3 / Goyal–Welch 2008). Cap regime count low (≤3, partial pooling, doc 04 §2.4.3). Default to fixed κ. Defer DMA/forgetting to dense-data future with a named consumer.

### DANGER 4 — Hindsight horizon selection ("it reverts at *this* horizon")

**Mechanism.** Report VR(q) at the q where VR is most below 1 — i.e., let the multi-timescale *curve* (a virtue, §4) degrade into "pick the reverting horizon." This is the State-T-morphology selection-on-deviation trap (doc 11/doc 12) re-entering through the horizon axis: scanning q over full-sample data and keeping the favorable q is the same DOF inflation as scanning windows.
**Why it is near-invisible.** It looks like *richer characterization* (a virtue we recommend in §4), so it is easy to slide from "report the curve" into "headline the best point."
**Mitigation (binding).** Fixed pre-registered q-grid; report the *entire* curve with CIs; characterize **unconditionally** (not on |z|-anchored windows); never headline the argmin-VR point.

### DANGER 5 — Anchored-window over-training masking instability

**Mechanism.** Anchored (expanding) walk-forward windows accumulate so much training data in later windows that *"almost any parameters look reasonable,"* making overfitting **harder to detect** than with rolling windows (general walk-forward critique; corroborated across the WFO literature). An "adaptive" half-life validated this way can be silently overfit.
**Why it is near-invisible.** The OOS curve looks stable precisely because the late windows are over-trained; the instability is hidden by data abundance.
**Mitigation.** Prefer rolling windows for *validation*; report performance per window; deflate for trials; never read a flat anchored-OOS curve as evidence of robustness.

---

## 9. Required sections — explicit summary

**Supporting evidence (time-varying / multi-timescale MR is real):** κ genuinely varies with regime (regime-switching pairs/stat-arb literature; Hamilton 1989; Ang–Timmermann 2012); character is genuinely scale-dependent (repo doc 10; Lo–MacKinlay 1988 VR(q)); disciplined time-variation *can* pay OOS in data-rich settings (Dangl–Halling 2012; Koop–Korobilis 2012); the half-life is genuinely economically load-bearing (Avellaneda–Lee 2010 κ>8.4 gate; Leung–Li 2015 parameter-driven optimal timing).

**Opposing evidence (modelling time-variation rarely pays here):** κ̂ is biased + high-variance + skewed + ∞-CI near the unit root (Yu 2012; Wang–Phillips–Yu; Stock 1991; Murray–Papell 2002; repo doc 04 §1.5.3); conditioning is not free and unconditional beats conditional OOS (Goyal–Welch 2008; repo doc 04 lesson 3); DMA/forgetting filed as "defer, λ overfit-prone" (repo doc 04 §2.4.2); residual reversion/half-life are smoother-manufactured (repo doc 06 C5 / doc 08); the pro-TVP evidence lives in dense-data, heavily-shrunk regimes that do not transport to short spreads.

**Failure modes:** (a) flat likelihood near unit root ⇒ half-life unidentifiable (STRUCTURAL); (b) upward κ̂ bias ⇒ universe/timing filters admit too-slow spreads (MEASUREMENT→economic); (c) regime-κ degenerates to noise-tracking (METHODOLOGY); (d) horizon-curve degrades into horizon-cherry-picking (METHODOLOGY); (e) smoother-manufactured residual reversion mistaken for signal (STRUCTURAL/MEASUREMENT, C5); (f) anchored-window over-training masks overfit (METHODOLOGY).

**Implementation dangers (hidden-hindsight-as-adaptivity):** §8, ranked — D1 full-sample-tuned window/horizon/half-life (highest); D2 lag-illusion faster-μ\*; D3 regime-conditioned-decay noise-tracking; D4 hindsight horizon selection; D5 anchored-window masking. Each carries a concrete mechanism + why it is near-invisible + a binding mitigation. The unifying rule: **`argmax over {window, horizon, half-life, λ, regime-count} of in-sample fit` is forbidden; adaptivity is legitimate only when recursion-causal with pre-frozen hyperparameters.**

---

## 10. Confidence, surviving uncertainty, non-conclusions, next question

**Confidence (trustworthiness of evidence, not excitement):**
- κ̂ instability near the unit root: **HIGH** (repo simulation + Yu 2012 + Murray–Papell + Stock 1991 converge; it is textbook).
- "Conditioning/adaptive-κ does not pay OOS by default in AMR's regime": **MEDIUM-HIGH** (strong general result; the pro-TVP exceptions are real but non-transporting).
- "Horizon profile > scalar": **MEDIUM-HIGH** (Lo–MacKinlay structural + repo doc 09 inversion + doc 12 split verdict).
- Recommended causal stance (S-A): **MEDIUM-HIGH** as a *research-phase* stance; deliberately conservative.

**Surviving uncertainty (UNRESOLVED):** whether the *deployment-domain* (genuine MR spreads), at the right frequency, makes κ identifiable enough that S-C could ever pay — untestable until a verified MR habitat + denser data exist (doc 12 Arm A/D preconditions). Whether intraday frequency (where queue/inventory half-lives ~1 day are *not* aliased, doc 04 §1.6.2) changes the κ̂-identifiability calculus. Whether a horizon *curve* discriminator beats a matched surrogate null on a verified reverter (the Arm A experiment).

**Explicit non-conclusions:** This memo does **not** conclude κ never varies (it does, §3.1); does **not** kill TVP/DMA in general (they pay in dense data, §3.2); does **not** propose any detector/score/hazard/timing object (zombie prohibition); does **not** authorize building anything (Research Mode). It concludes only that *for AMR v0, on the data it has, time should enter as a fixed pre-registered profile, not an online-estimated one.*

**Next highest-information question:** On a *verified mean-reverting* instrument (the doc 12 Arm A precondition), does a **fixed-grid VR(q) curve separate from its own matched OU/RW/GARCH surrogate at any horizon, unconditionally** — i.e., is the multi-timescale temporal object *real and trap-free* on deployment-like data — before any online/adaptive temporal machinery is ever considered? Until that returns yes, S-B/S-C stay deferred.

---

## Sources

- Yu, J. (2012). "Bias in the estimation of the mean reversion parameter in continuous time models." *Journal of Econometrics* 169(1):114–122. https://www.sciencedirect.com/science/article/abs/pii/S030440761200005X
- Bao, Ullah, Wang & Yu (2015). "Bias in the estimation of mean reversion in continuous-time Lévy processes." *Economics Letters* 134:16–19. https://www.sciencedirect.com/science/article/abs/pii/S0165176515002426
- Wang, Phillips & Yu. "Exact Distribution of the Mean Reversion Estimator in the Ornstein–Uhlenbeck Process." UC Riverside WP 201413. https://economics.ucr.edu/repec/ucr/wpaper/201413.pdf
- Stock, J. (1991). "Confidence intervals for the largest autoregressive root in U.S. macroeconomic time series." *Journal of Monetary Economics* 28:435–459. https://www.nber.org/papers/t0105
- Phillips, P.C.B. (2014). "On Confidence Intervals for Autoregressive Roots and Predictive Regression." *Econometrica* 82. https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA11094
- Murray, C.J. & Papell, D.H. (2002). "The purchasing power parity persistence paradigm." *Journal of International Economics* 56(1):1–19. https://www.scirp.org/reference/referencespapers?referenceid=1874710
- Goyal, A. & Welch, I. (2008). "A Comprehensive Look at the Empirical Performance of Equity Premium Prediction." *Review of Financial Studies* 21(4):1455–1508. (repo-established)
- Dangl, T. & Halling, M. (2012). "Predictive regressions with time-varying coefficients." *Journal of Financial Economics* 106(1):157–181. https://www.sciencedirect.com/science/article/abs/pii/S0304405X12000633
- Koop, G. & Korobilis, D. (2012). "Forecasting Inflation Using Dynamic Model Averaging." *International Economic Review* 53(3):867–886. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-2354.2012.00704.x
- Lo, A.W. & MacKinlay, A.C. (1988). "Stock market prices do not follow random walks: Evidence from a simple specification test." *Review of Financial Studies* 1(1):41–66. https://academic.oup.com/rfs/article-abstract/1/1/41/1601244
- Avellaneda, M. & Lee, J. (2010). "Statistical arbitrage in the US equities market." *Quantitative Finance* 10(7):761–782. https://www.tandfonline.com/doi/abs/10.1080/14697680903124632
- Leung, T. & Li, X. (2015). "Optimal Mean Reversion Trading with Transaction Costs and Stop-Loss Exit." *International Journal of Theoretical and Applied Finance* 18(3). https://arxiv.org/abs/1411.5062
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." *Econometrica* 57:357–384.
- Ang, A. & Timmermann, A. (2012). "Regime Changes and Financial Markets." *Annual Review of Financial Economics* 4:313–337. https://www.nber.org/system/files/working_papers/w17182/w17182.pdf
- Bailey, D.H. & López de Prado, M. (2014). "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality." *Journal of Portfolio Management* 40(5):94–107. https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
- Bailey, Borwein, López de Prado & Zhu (2014/2017). "The Probability of Backtest Overfitting." *Journal of Computational Finance*. https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf
- HMM stat-arb in crude-oil futures (2023). arXiv:2309.00875. https://arxiv.org/pdf/2309.00875

*Markers available for future revisions: REVISED · WEAKENED · STRENGTHENED · FALSIFIED · UNRESOLVED · PROMOTED · DEMOTED. This is a DRAFT; no conclusion is frozen.*
