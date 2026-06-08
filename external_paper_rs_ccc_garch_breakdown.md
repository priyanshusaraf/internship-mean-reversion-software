# External Paper Breakdown — RS-CCC-GARCH for Cross-Asset VRP Forecasting

> **Purpose of this file.** A precise, faithful reconstruction of what the external paper
> *"Regime-Switching CCC-GARCH for Cross-Asset Volatility Risk Premium Forecasting"*
> (Quant Insider, June 2, 2026) actually does — its objects, its math, its claims, and its
> stated limitations. Written so that it can be reviewed against the AMR project state
> **without the reviewer needing access to the original PDF.** Nothing here is an AMR
> recommendation; integration judgement is deferred to the review prompt (see §8).
>
> **Provenance.** Reconstructed from the 8-page paper (title page + §§1–9 + references).
> Equation numbers below match the paper's own numbering. Where a claim is the paper's,
> it is stated as the paper's; where it is a structural observation, it is marked as such.

---

## 0. One-paragraph summary

The paper builds a **forecasting-and-timing engine for the volatility risk premium (VRP)** —
the wedge between option-implied variance (risk-neutral, Q-measure) and expected realised
variance (physical, P-measure). The realised-variance side is forecast by a **regime-switching
Constant Conditional Correlation GARCH (RS-CCC-GARCH)** model: a multivariate GARCH whose
variance dynamics *and* cross-asset correlation matrix are governed by a discrete latent
Markov state (low-vol vs high-vol). The implied side is adjusted by a **multiplicative
calendar-event layer** that re-prices forward-starting implied vol around scheduled macro
releases (FOMC, CPI, NFP, ECB, earnings). The difference of the two is the VRP signal used to
time a short-volatility carry trade, with positions scaled down (or off) when the high-vol
regime probability is elevated.

**The paper's alpha source is VRP carry. It is not a mean-reversion strategy.**

---

## 1. The economic thesis (what edge it claims)

- **The VRP anomaly.** Option-implied volatility has historically been *rich* relative to
  subsequently realised volatility. A trade that systematically **sells implied volatility and
  delta-hedges** the resulting exposure earns a positive average return.
- **The cost of that edge.** The payoff is **sharply negatively skewed** — losses cluster in
  short, violent market-stress episodes. The strategy is "picking up pennies" with occasional
  large drawdowns.
- **The two modelling problems the paper says it is solving:**
  1. Realised variance across assets exhibits **regime behaviour** — long quiet stretches
     punctuated by short, highly-correlated cross-asset volatility bursts. Single-regime GARCH
     *understates* the speed/size of these transitions and *overstates* vol persistence in
     quiet periods.
  2. A non-trivial share of short-dated **implied** vol is attributable to *scheduled events*
     whose contribution cannot be inferred from a pure time-series model. Failing to strip this
     out makes you misclassify event-driven implied richness as exploitable premium.

So the paper's whole reason for existing is: **forecast realised vol better (regime-switching),
and clean the implied side of calendar noise (event multiplier), so the VRP signal is sharper
and the carry trade is better-timed.**

---

## 2. The model, layer by layer

### 2.1 CCC-GARCH baseline (Section 2)

- Return vector `r_t = (r_1,t, …, r_N,t)ᵀ ∈ ℝᴺ` on N underlyings (e.g. S&P 500, EuroStoxx,
  10Y UST, EUR/USD, WTI).
- `r_t = μ_t + ε_t`, `ε_t = H_t^{1/2} z_t`, `z_t ~ N(0, I_N)`.  **(Eq. 1)**
- CCC decomposition of the conditional covariance:
  `H_t = D_t R D_t`, with `D_t = diag(σ_1,t, …, σ_N,t)`.  **(Eq. 2)**
  - `R` is a **time-invariant** correlation matrix.
  - Each marginal variance is univariate GARCH(1,1):
    `σ²_i,t = ω_i + α_i ε²_{i,t−1} + β_i σ²_{i,t−1}`, with `ω_i > 0`, `α_i, β_i ≥ 0`,
    `α_i + β_i < 1`.  **(Eq. 3)**
- **Stated key limitation of CCC:** the constant-correlation assumption "fails dramatically
  during cross-asset stress episodes." This is the explicit motivation for the regime-switching
  extension.

### 2.2 Regime-switching extension (Section 3)

- Introduce a latent first-order Markov state `S_t ∈ {1, …, K}` with transition probabilities
  `p_jk = P(S_t = k | S_{t−1} = j)`, collected in transition matrix `P`.
- Regime-conditional covariance: `H_t | S_t = k = D_t^{(k)} R^{(k)} D_t^{(k)}`.  **(Eq. 4)**
  - **Both** the GARCH parameters `(ω_i^{(k)}, α_i^{(k)}, β_i^{(k)})` **and** the correlation
    matrix `R^{(k)}` are regime-specific.
- Practical choice: **K = 2** (low/high vol) or **K = 3** (low/medium/high).
- **Empirical regime stylised fact (Figure 2):** the high-vol state typically captures
  **< 20% of calendar time** but a disproportionate share of total variance. Low-vol
  dominance, interrupted by sharp transitions to near-unit high-vol probability.

#### 2.2.1 Identification — the label-switching fix (Eq. 5)

To prevent label-switching and give regimes economic meaning, impose an **ordering on the
unconditional variance of a benchmark underlying** (typically S&P 500):

```
ω_1^{(1)} / (1 − α_1^{(1)} − β_1^{(1)})  <  ω_1^{(2)} / (…)  <  …  <  ω_1^{(K)} / (…)
```

i.e. regimes are sorted low→high by unconditional variance. This replaces a free permutation
symmetry with a deterministic ordering. **(structural note: this is their identification
discipline — directly analogous to why our project pins down estimators before scoring.)**

#### 2.2.2 Likelihood (Section 3.2)

- Per-observation contribution conditional on the regime path:
  `ℓ_t(r_t | S_t = k) = −½[ N log(2π) + log det H_t^{(k)} + ε_tᵀ (H_t^{(k)})^{−1} ε_t ]`. **(Eq. 6)**
- Observed-data log-likelihood (states integrated out by the **Hamilton filter**):
  `L(θ) = Σ_t log[ Σ_k ξ_{t|t−1}^{(k)} f(r_t | S_t = k; θ) ]`.  **(Eq. 7)**
- Recursive filter update + prediction:
  `ξ_{t|t}^{(k)} = ξ_{t|t−1}^{(k)} f(r_t|S_t=k) / Σ_j ξ_{t|t−1}^{(j)} f(r_t|S_t=j)`,
  and `ξ_{t+1|t} = Pᵀ ξ_{t|t}`.  **(Eq. 8)**
- Maximisation by **EM**: E-step runs Hamilton filter (8) + Kim smoother for `ξ_{t|T}^{(k)}`;
  M-step solves weighted GARCH likelihoods regime-by-regime.

#### 2.2.3 Multi-step variance forecast (Section 3.3) — **the key output for us**

- h-step-ahead conditional variance for asset i:
  `σ̂²_{i,t+h|t} = Σ_k ξ_{t+h|t}^{(k)} E[σ²_{i,t+h} | S_{t+h}=k, F_t]`.  **(Eq. 9)**
  with predicted regime probabilities `ξ_{t+h|t} = (Pᵀ)^h ξ_{t|t}`.
- Inner expectation: regime-conditional GARCH forecasts converge geometrically to the
  regime-unconditional variance at rate `(α_i^{(k)} + β_i^{(k)})`.
- **Net output is a regime-probability-weighted MIXTURE of geometrically-decaying paths**
  (Figure 3: low-regime path, high-regime path, and the mixture in between). This is the
  forecast that distinguishes *persistent* high-vol from *spike-and-recover*.

### 2.3 Estimation algorithm (Algorithm 1 / Section 6)

EM estimation of RS-CCC-GARCH:
1. **Input:** returns `{r_t}`, number of regimes K, tolerance ε.
2. **Initialise** θ⁽⁰⁾ via single-regime CCC-GARCH + perturbed intercepts (initialisation is
   flagged as critical; perturb the variance intercepts `ω_i^{(k)}` to break symmetry).
3. **Repeat:**
   - **E-step:** Hamilton filter (8) + Kim smoother → smoothed `ξ_{t|T}^{(k)}` and pairwise
     probs `ξ_{t,t−1|T}^{(j,k)}`.
   - **M-step:**
     - Update `p_jk ← Σ_t ξ_{t,t−1|T}^{(j,k)} / Σ_t ξ_{t−1|T}^{(j)}`.
     - For each k, maximise weighted Gaussian likelihood (weights `ξ_{t|T}^{(k)}`) → GARCH params.
     - For each k, set `R^{(k)}` to weighted sample correlation of standardised residuals.
   - Enforce ordering (Eq. 5).
4. **Until** `|L(θ^{(s+1)}) − L(θ^{(s)})| < ε`.
5. **Return** θ̂ and smoothed regime probabilities.
- Standard errors: outer product of gradients, or block bootstrap if sample is small.

---

## 3. The implied side — calendar-event layer (Section 4)

- The VRP signal is *not* realised vol; it is the **difference** between an implied-vol quote
  and the model forecast of realised vol over the *same window*.
- For a forward-starting variance contract over window `[τ_1, τ_2]`, define the
  **calendar-event multiplier**:
  `m(τ_1, τ_2) = 1 + Σ_{e ∈ E[τ_1,τ_2]} λ_e · w_e(τ_1, τ_2)`.  **(Eq. 10)**
  - `E[τ_1,τ_2]` = set of scheduled events in the window.
  - `λ_e ≥ 0` = estimated incremental variance contribution of event e (annualised variance units).
  - `w_e` = weight allocating the event's variance to the window (1 if inside, 0 if outside,
    linear pro-rata for overlapping events).
- Event-adjusted forward-starting variance forecast:
  `σ̂²,adj_{[τ_1,τ_2]} = m(τ_1, τ_2) · (1/(τ_2−τ_1)) Σ_{h=⌈τ_1⌉}^{⌊τ_2⌋} σ̂²_{i,t+h|t}`. **(Eq. 11)**
- `λ_e` estimated by regressing event-window realised variance on event-type dummies,
  controlling for the conditional variance forecast (Eq. 9) — this separates the systematic
  event contribution from day-of-week / time-of-day seasonality already in the GARCH dynamics.
- **Empirical ranking (Figure 4):** FOMC, CPI, ECB releases dominate `λ_e`; holidays contribute
  negative/near-zero variance (mild downward adjustment).

---

## 4. From forecast to signal (Section 5)

- Let `IV_{i,[τ_1,τ_2]}` = option-implied annualised variance for asset i over the window.
- **The VRP signal:**
  `VRP_{i,t}([τ_1,τ_2]) = IV_{i,[τ_1,τ_2]} − σ̂²,adj_{i,[τ_1,τ_2]}`.  **(Eq. 12)**
- **Positive value ⇒ implied exceeds the event-adjusted forecast ⇒ selling the variance
  contract is, in expectation, profitable.**

This is the central object of the entire paper: a cleaned, regime-aware estimate of how rich
implied vol is relative to a properly-forecast realised vol.

---

## 5. Portfolio construction & risk management (Section 7 backtest + Figs 5–6)

Two refinements turn the per-asset signal into a tradable book:

1. **Regime-conditional scaling.** Short-vol carry Sharpe is materially lower when the high-vol
   state `ξ_{t|t}^{(K)}` is elevated. The risk rule **scales position size by `1 − ξ_{t|t}^{(K)}`**
   — taking the trade off entirely when the high-vol state dominates. (Figure 6: scaling reduces
   drawdown magnitude at regime transitions and modestly improves end-of-sample P&L.)
2. **Cross-asset aggregation.** Stack `VRP_{i,t}` across i = 1…N and form a **risk-parity-weighted
   basket**, exploiting the diversification in the off-diagonals of `R^{(k)}`. Caveat the paper
   itself raises: under the high-vol regime, correlations spike (Figure 5), so diversification
   gains shrink *precisely when most needed*.

**Figure 5 (the paper's single most consequential output for sizing):** regime-specific pairwise
correlations across SPX/SX5E/UST/EUR/WTI. Equity-equity and equity-commodity correlations rise
materially in high-vol; equity-rates correlations turn more sharply negative (flight-to-quality).

---

## 6. Backtesting discipline the paper insists on (Section 7) — **directly relevant to our guardrails**

- **Strictly causal regime probabilities.** Smoothed `ξ_{t|T}^{(k)}` **peek at future data** and
  must be replaced by **filtered `ξ_{t|t}^{(k)}`** in any signal construction.
  → *(structural note: this is exactly our ADR-002 temporal-integrity / causal-firewall concern.
  The paper independently arrives at the same rule.)*
- **Rolling re-estimation.** Re-estimate θ on an expanding/rolling window; recompute event
  coefficients `λ_e` on the same window (no full-sample leakage).
- **Transaction costs & delta-hedge slippage.** VRP returns are gross of two cost layers: the
  option bid-ask, and the cost of replicating the delta. Delta-hedge frequency is itself a
  parameter (daily re-hedging is the stated reasonable default for short-dated structures).
- **Tail-risk attribution.** Report Sharpe **and** conditional drawdown **by regime**, since most
  adverse outcomes occur in the highest-vol regime.

---

## 7. Extensions the paper flags (Section 8)

- **DCC within regimes.** Replace regime-constant `R^{(k)}` with a regime-specific Dynamic
  Conditional Correlation (Engle 2002) process — intra-regime correlation evolution.
- **Asymmetric (GJR) marginals.** Replace Eq. 3 with GJR-GARCH to capture the leverage effect:
  `σ²_{i,t} = ω_i + α_i ε²_{i,t−1} + γ_i ε²_{i,t−1} 1{ε_{i,t−1}<0} + β_i σ²_{i,t−1}`.
- **Heavy-tailed innovations.** Replace Gaussian `z_t` with multivariate Student-t / skewed-t,
  d.o.f. estimated jointly.
- **Event-clustering shrinkage.** When the event set is large, estimate `λ_e` under a hierarchical
  prior shrinking rarely-observed event coefficients toward a global mean (overfit control).

---

## 8. The honest map onto AMR — what intersects, what does not

> This section frames the review; it deliberately stops short of a verdict, which is the job of
> the review prompt.

### 8.1 What this paper is NOT (for us)
- **It is not a mean-reversion model.** Its edge is VRP carry (implied rich-to-realised), an
  orthogonal anomaly to "reversion inside trends." We are not selling variance, not pricing
  forward-starting options, not delta-hedging.
- Therefore the **entire implied side** — calendar-event multiplier (Eq. 10–11), VRP signal
  (Eq. 12), options bid-ask / delta-hedge cost analysis — is **out of scope for our thesis** as
  a *strategy*. It can only matter as *machinery*.

### 8.2 Where the machinery plausibly touches AMR (to be critically tested, not assumed)
- **(a) The regime layer we explicitly deferred.** AMR Framework §1.5 leaves a placeholder:
  "HMM can formally detect persistent regime changes … volatility-percentile filter is a
  lightweight substitute *until HMM integration is implemented*." The Hamilton-filter + EM
  machinery (Eqs. 6–8, Algorithm 1) is a production-grade candidate for that exact deferred slot.
- **(b) A regime-aware volatility input for MRScore Block 3 (Tradability).** Our current vol
  percentile has no regime awareness — it cannot distinguish *persistent* high-vol from
  *spike-and-recover*. The mixture forecast (Eq. 9) makes precisely that distinction, which is
  what should drive "suspend MR vs. size down" (our §1.5 directional filter `θ_high / θ_ext`).
- **(c) Independent corroboration of our causal discipline.** §7's "filtered, not smoothed"
  rule and rolling re-estimation are the same temporal-integrity constraints we already encode
  (ADR-002). Useful as an external reference implementation, not a new idea.

### 8.3 The load-bearing caveat (the thing the review MUST stress-test)
- The paper's K=2 state is a **VOLATILITY** regime, fit by likelihood on returns. **It is not a
  mean-reversion regime.** Low-vol ≠ high-MR-probability. Before any of (a)/(b)/(c) can be used,
  we would have to **validate that Hamilton-filter regime labels actually correlate with our
  VR(q) habitat scores / MR favourability** — otherwise we are importing a classifier built for
  a different signal and assuming it transfers. This transfer is unproven and is the single
  biggest risk in any integration.
- Secondary caveat: regime-switching parameters are known (per our own literature review,
  Ang–Timmermann 2012; Guidolin–Timmermann) to carry **substantial estimation/identification
  error**. Adding a K-state EM layer adds real estimation risk that must clear our
  "does the complexity earn its keep, causally / OOS" bar — a bar the project has already used
  to kill noisier components.

---

## 9. Suggested review questions for the API (for the downstream prompt)

1. **Thesis check.** Restate the paper's core thesis in one sentence and confirm it is VRP carry,
   not mean reversion. Is there any *direct* reading under which its edge overlaps ours?
2. **Component value.** Of the three candidate intersections in §8.2, which (if any) survive a
   cost/benefit test against the current active frontier (Arm A: VR(q) real-minus-surrogate on
   the 7 spreads)? Rank them.
3. **The transfer risk in §8.3.** Design the *minimum* test that would confirm or kill the claim
   that a vol-regime label is informative about MR favourability, before any Hamilton-filter code
   is written. What would falsify it?
4. **Sequencing.** Does any of this belong *now*, or strictly after Phase 1/2 (mean estimation +
   MR detection) are resolved? Justify against the project's freeze discipline (don't unfreeze
   State-T-adjacent machinery on the strength of an external paper).
5. **Estimation-risk gate.** If we did build the EM/Hamilton layer, what is the falsification
   criterion that prevents it becoming another noisy component that manufactures structure?
