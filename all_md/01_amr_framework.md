Adaptive Mean Reversion Framework

Adaptive Mean Reversion Framework
Research Architecture, Model Specification, and Validation Design

Working Paper · Instruments: Equity Indices, Commodities, FX  ·  Timeframe Hierarchy: Weekly / Daily /
4H

Abstract
This paper specifies the Adaptive Mean Reversion (AMR) Framework, a quantitative detection
and trading architecture targeting equity indices (NIFTY, S&P 500), commodity futures (crude
oil,  gold),  and  major  FX  pairs  across  a  weekly/daily/4H  timeframe  hierarchy.  The  framework
pursues  a  single  central  objective:  determine  whether  a  given  market  exhibits  statistically
meaningful,  reliable,  and  actionable  mean  reversion,  and  if  so,  estimate  the  regime-aware
equilibrium mean around which price organises its behaviour. The core instrument is the Mean
Reversion Favorability Score (MRScore), a three-block composite that explicitly prioritises direct
empirical evidence of mean-reverting behaviour over abstract stationarity diagnostics. Block 1
(Mean  Reliability,  20%)  certifies  that  the  estimated  equilibrium  mean  is  trustworthy.  Block  2
(Mean Reversion Strength, 60%) directly measures whether price deviations snap back toward
equilibrium. Block 3 (Tradability, 20%) assesses whether detected mean reversion is practically
exploitable.  The  framework  is  grounded  in  Ornstein-Uhlenbeck  theory,  estimated  via  rolling
historical windows to prevent lookahead bias, and validated through purged cross-validation.
Every design choice is derived from first principles with explicit economic justification.

§  Section

Content

1  Research Roadmap  Objectives, phases, volatility filter

OU process, Variance Ratio, z-score

Status

Complete

Complete

2  Mathematical
Foundations

3  MRScore — Full
Specification

4  Optimal Mean
Estimation

5  Downstream
Objectives

6  Validation

Architecture

Three-block architecture and master equation

Complete

Regime-aware multi-scale mean hierarchy

Complete

Structure classification, signals, exit rules

Scoped

Purged CV, falsification criteria

Framework

7  Variable Glossary

All symbols defined

Complete

Adaptive Mean Reversion Framework

1  Broader Objective and Research Roadmap

1.1  The Two-Level Research Programme
This research programme operates at two levels of abstraction. The first is diagnostic: given a
market  and  timeframe,  determine  whether  exploitable  mean  reversion  exists.  The  second  is
prescriptive: given that mean reversion is confirmed, derive and operationalise the optimal trading
strategy.  Neither  level  is  meaningful  without  the  other  —  a  diagnostic  finding  with  no  trading
consequence  is  academic  noise;  a  trading  strategy  without  rigorous  diagnostic  foundations  is
speculation.

Definition  1.1    (Primary  Objective  1  —  Detection).    For  a  price  series  {Pt}  observed  on
instrument i at timeframe τ, determine whether a statistically significant, persistent, and tradable
mean-reversion tendency exists. If so, identify the reference mean µ*(i, τ) around which reversion
occurs.

Definition 1.2  (Primary Objective 2  — Strategy).  Conditional on mean reversion detection,
derive  the  optimal  entry  signal  set,  position  sizing  function,  and  exit  rule  that  maximises  risk-
adjusted return net of transaction costs over the identified reversion horizon.

1.2  The Full Research Roadmap
The programme decomposes into five sequential phases. Each is a necessary prerequisite for
the next.

Phase  Objective

Key Deliverable

Mean Estimation

Regime-aware µ*(i, τ) with stability
certification

Status

Active

MR Detection

MRScore three-block score

Specified

Structure
Classification

GBM / OU / nonlinear-OU classification

Scoped

Signal Generation

Entry/exit indicators calibrated to structure

Scoped

Strategy Optimisation  Position sizing, stops, holding period

Scoped

1

2

3

4

5

1.3  Why Mean Estimation is the Foundation
Every downstream component depends on a credible µ*(i, τ). The MRScore (Phase 2) computes
z-scores relative to it. Structure classification (Phase 3) fits process parameters around it. Trading
signals (Phase 4) define entries and exits as multiples of deviation from it. Position sizing (Phase
5)  scales  risk  as  a  function  of  deviation  magnitude.  A  poorly  estimated  mean  corrupts  every
component simultaneously.

The mean instability problem.  Standard rolling arithmetic means and EMAs are not conditioned on
whether the underlying price process is actually mean-reverting at the chosen window. In a trending
market, these estimators track the trend, producing a mean that is always below (in a bull market) or
above (in a bear market) current price. Trading against this estimated mean is not mean reversion —

Adaptive Mean Reversion Framework

it is fading momentum. Mean estimation must be conditioned on regime before any other component
has meaning.

1.4  Phase 3: Market Structure Classification
Once  mean  reversion  is  confirmed,  the  market  is  classified  into  a  structural  model.  This
classification determines which trading signals are appropriate.

Model

GBM

Process

MR Behaviour

Trading Implication

dP = µP dt + σP dW

None (null model)

Use trend-following

Linear OU

dX = κ(µ−X)dt + σdW

Symmetric, linear

z-score entries; symmetric sizing

Nonlinear
OU

dX = f(X−µ)dt + σdW

Asymmetric /
threshold

Asymmetric entry thresholds

OU + Jumps  OU + Poisson J

MR interspersed with
jumps

Wider stops; volatility filter on
entries

The practical question for Phase 3 is whether knowing the structural model materially changes
trading decisions. For position sizing and stop placement, the answer is yes — nonlinear reversion
implies  asymmetric  deviation  thresholds.  For  entry  signals,  the  difference  is  smaller.  The
recommendation is to implement linear OU as the default and add nonlinear extensions only after
demonstrating  that  AR(1)  residuals  are  systematically  nonlinear  via  RESET  test  or  threshold
autoregression.

1.5  Volatility Regime Integration
A central concern is the behaviour of mean reversion strategies during volatility expansion. The
core hypothesis: when volatility exceeds a threshold, mean reversion trades should only be taken
in the direction of the prevailing trend, and position sizing should be reduced.

Let VPₜ denote the current volatility percentile and TrendᵰFᴴ the trend direction on the next-higher
timeframe (+1 for uptrend, −1 for downtrend). The directional filter is:

Trade direction = ±1   if VPₜ < θᵜᵒᵌ  (MR freely, both directions)        (1a)

Trade direction = TrendᵰFᴴ  if θᵜᵒᵌ ≤ VPₜ < θᵉˣᵗ  (unidirectional only)        (1b)

Suspend MR  if VPₜ ≥ θᵉˣᵗ        (1c)

Recommended defaults: θᵜᵒᵌ = 70th percentile and θᵉˣᵗ = 90th percentile. Hidden Markov Models
can formally detect persistent regime changes; when such a shift is detected, the MR framework
is suspended entirely. The volatility filter in (1) serves as a lightweight, non-parametric substitute
until HMM integration is implemented.

Adaptive Mean Reversion Framework

2  Mathematical Foundations

2.1  Stationarity
Definition 2.1  (Weak Stationarity).  A process {Xt} is weakly stationary if:

E[Xₜ] = µ   ∀ t        (2)

Var(Xₜ) = σ²   ∀ t        (3)

Cov(Xₜ, Xₜ₊ₖ) = γ(k)  depends only on lag k, not on t        (4)

A price series is globally nonstationary — it trends. However, over short enough windows, markets
may  exhibit  local  stationarity:  the  series  oscillates  around  a  slowly  drifting  mean.  The  central
challenge is distinguishing genuine local stationarity, where mean reversion is real and tradable,
from a trending process whose rolling mean merely tracks the trend.

2.2  The Ornstein-Uhlenbeck Process
The canonical continuous-time model of mean reversion is the Ornstein-Uhlenbeck process:

dXₜ = κ(µ − Xₜ) dt + σ dWₜ        (5)

where  κ  >  0  is  the  mean  reversion  speed,  µ  is  the  long-run  equilibrium,  σ  >  0  is  the  diffusion
coefficient, and dWₜ is a standard Wiener increment. The linear restoring force κ(µ − Xₜ) pulls the
process  back  toward  µ  with  force  proportional  to  the  distance:  larger  deviations  are  corrected
more aggressively than small ones.

The stationary distribution of equation (5) is:

X∞ ~ N(µ,  σ² / 2κ)        (6)

Definition 2.2  (Half-Life of Mean Reversion).   The expected time for a deviation (X0 − µ) to
decay to half its initial magnitude is:

HL = ln 2 / κ        (7)

Why OU and not GBM?  GBM (dP = µP dt + σP dW) has no restoring force — deviations grow
without bound in expectation. OU's linear restoring force is the formal mathematical definition of
mean reversion. All parameter estimation, signal generation, and stop-loss derivation in this
framework are calibrated against the OU benchmark.

2.3  Discrete-Time Approximation
Applying the Euler-Maruyama scheme to equation (5) with step Δt = 1:

Xₜ = μ(1 − e⁻ᵏ) + e⁻ᵏ · Xₜ₋₁ + εₜ,   εₜ ~ N(0,  σ²(1 − e⁻²ᵏ) / 2κ)        (8)

This shows the OU process is exactly an AR(1) in discrete time, with 0 < β < 1 required for mean
reversion (β = 1 is a unit root; β > 1 is explosive). The continuous-time parameters are recovered
from OLS estimates:

Why AR(1) and not higher-order AR or ARMA? For detecting the restoring force κ, the first-lag coefficient carries
the signal. Higher-order lags add noise without improving the κ estimate. ARMA's moving-average component

κ̂ = − ln β̂,   HL̂ = ln 2 / κ̂        (9)

Adaptive Mean Reversion Framework

conflates  mean  reversion  with  microstructure  effects.  AR(1)  is  the  simplest  model  consistent  with  OU,  and
simplicity is prioritised unless evidence of inadequacy is clear.

2.4  The Z-Score
Definition 2.3  (Z-Score).  The normalised deviation of price from its estimated mean at time t:

zₜ = (Pₜ − µ*ₜ) / σₜ        (10)

where µ*ₜ is the optimal mean estimate (developed in Section 4) and σₜ is the rolling standard
deviation of  log  returns over  window  w.  The z-score  is  the  primary  input  to  every  downstream
component: the Direct Reversion Coefficient, Hit Rate, and all entry and exit rules. Its quality is
entirely determined by the quality of µ*ₜ — a biased mean produces systematically one-sided z-
scores that mislead every downstream component.

2.5  The Variance Ratio and its Relationship to the OU Process
The Variance Ratio test provides a direct non-parametric test of mean reversion. For horizon q:

VR(q) = Var(Xₜ − Xₜ₋ᵤ) / (q · Var(Xₜ − Xₜ₋₁))        (11)

Under a random walk, VR(q) = 1 for all q. The theoretical VR under an OU process with AR(1)
coefficient β = e⁻ᵏ is:

VRᴿᵁ(q) = (2/q) · [1 − (1 − βᵤ) / (q(1 − β))]        (12)

Equation (12) shows that VR is not a heuristic — it is a direct function of κ. As κ → 0 (weak mean
reversion), VR → 1. As κ → ∞ (strong mean reversion), VR → 0. This provides a consistency
check:  κ̂  from  AR(1)  regression  and  the  κ  implied  by  the  observed  VR  should  agree.  Large
discrepancies suggest model misspecification or structural breaks within the estimation window.

Adaptive Mean Reversion Framework

3  Mean Reversion Favorability Score — Full Specification

3.1  Architecture and Master Equation
The  MRScore  is  a  scalar  summary  of  how  favourable  current  market  conditions  are  for  mean
reversion  strategies.  It  is  a  detection  instrument,  not  a  prediction  instrument  —  it  estimates
whether mean reversion strategies are likely to work, not what the market will do.

The  architecture  separates  the  model  into  three  logically  distinct  blocks,  each  answering  a
different question:

Block

Core Question

Block 1 — Mean
Reliability

Is the estimated equilibrium mean trustworthy
enough to anchor analysis?

Block 2 — Mean
Reversion Strength

Does price actually snap back toward the mean after
deviating?

Block 3 — Tradability

Even if mean reversion exists, can it be profitably
traded?

Weight

w₁ = 0.20

w₂ = 0.60

w₃ = 0.20

MRScoreₜ = 0.20 · B₁ₜ + 0.60 · B₂ₜ + 0.20 · B₃ₜ        (13)

3.2  Justification for the 20/60/20 Weighting
The  weight  structure  reflects  a  deliberate  hierarchy  of  economic  importance.  Block  2  receives
dominant  weight  (60%)  because  it  directly  and  empirically  answers  the  central  question:  does
price actually revert? A high Block 2 score means the market has demonstrated mean-reverting
behaviour  in  historical  data  —  this  is  the  core  edge  being  traded.  No  amount  of  structural
certification or tradability optimisation is valuable if this evidence is absent.

Block 1 receives 20% because the reliability of the equilibrium mean is a necessary precondition:
if  the  mean  is  drifting  or  unstable,  z-scores  are  meaningless  and  Block  2  evidence  is
contaminated.  However,  mean  reliability  is  logically  prior  to  —  and  less  important  than  —  the
empirical reversion evidence itself. A stable mean that price never reverts to is useless; unstable
mean estimates can sometimes still yield actionable reversion signals at shorter horizons.

Block 3 receives 20% because tradability conditions — half-life proximity, volatility regime, and
transaction cost coverage — determine whether a genuine structural edge is actually extractable
given  current  market  conditions.  Tradability  should  not  suppress  a  strong  structural  signal;  it
should modulate timing and sizing.

Anti-overfitting constraint.  These weights are principled economic priors, not parameters to be
optimised in-sample. Fitting block weights to maximise historical Sharpe ratio defeats the entire
purpose of the architecture. The weights reflect the researcher's prior on economic importance, and
their validity is tested only through out-of-sample performance comparison against naive baselines.

3.3  Rank Aggregation
Each raw feature fᵢ,ₜ is converted to a percentile rank before entering its block score:

Adaptive Mean Reversion Framework

Rᵢ,ₜ = rank( fᵢ,ₜᵃᵈʲ within {fᵢ,ₜ₋ᴺ, ..., fᵢ,ₜ₋₁} ) / W × 100        (14)

where fᵢ,ₜᵃᵈʲ is the directionally adjusted feature (so R = 100 always means most mean reversion-
favourable), and W = 252 trading days. Rank aggregation is used rather than a weighted linear
combination  of  raw  values  because  raw  feature  values  operate  on  incompatible  scales  —  t-
statistics,  unitless  ratios,  and  probabilities  cannot  be  directly  compared.  Rank  aggregation
enforces  equal  scale,  is  robust  to  outliers,  and  introduces  zero  free  weight  parameters  at  the
feature level.

   Block 1 — Mean Reliability  (Weight: 20%)

Block 1 answers the question: is the estimated equilibrium mean µ* reliable enough to anchor
mean reversion analysis? A trustworthy mean is one that has been approximately stable over the
recent  past,  that  the  underlying  process  shows  evidence  of  organising  around,  and  whose
associated volatility has not shifted sharply enough to invalidate z-score construction.

The  three  features  in  Block  1  work  together  as  a  reliability  certification  system  rather  than  as
independent predictive signals. The mean stability feature dominates because operational mean
stability  is  the  most  direct  measure  of  whether  µ*  is  a trustworthy  reference.  Stationarity  tests
provide supporting statistical evidence. Variance stability ensures that the σₜ denominator of the
z-score is consistent with the estimation window.

Feature

Purpose

Internal Weight

B1.1  ADF/KPSS
Stationarity

Certification that the series is not a pure unit
root or random walk

30%

B1.2  Mean Stability Index  Direct test that the rolling mean has not drifted

50%

in volatility-adjusted terms

B1.3  Variance Stability
Index

Test that the z-score denominator σₜ has not
shifted regime

20%

B1.1  ADF and KPSS Stationarity Certification
The  Augmented  Dickey-Fuller  test  (Said  &  Dickey  1984)  tests  H₀:  unit  root  exists  against  H₁:
stationary. The test regression over rolling window w is:

ΔXₜ = α + β₁Xₜ₋₁ + ΣⱼγⱼΔXₜ₋ⱼ + εₜ        (15)

with  test  statistic  τᴬᴰᴼ  =  β̂₁  /  SE(β̂₁)  and  p-value  pᴬᴰᴼ  from  the  MacKinnon  (1996)  response
surface. Lag order p follows the Schwert (1989) rule: p = ⌊(w/100)¹/⁴⌋.

The KPSS test (Kwiatkowski et al. 1992) reverses the null hypothesis: H₀: stationary, H₁: unit root.
The null is σ²ᵤ = 0. The KPSS test statistic is:

η = (1/T²) Σ Sₜ² / ś²(ℓ),   Sₜ = Σⱼᵌₜ ầⱼ        (16)

where ầⱼ are OLS residuals and ś²(ℓ) is the Newey-West long-run variance with lag truncation ℓ =
⌊4(T/100)¹/⁴⌋.

Combining ADF and KPSS produces a four-outcome diagnostic grid:

Adaptive Mean Reversion Framework

ADF Result

KPSS Result

Conclusion

Rejects H₀ (unit root)

Fails to reject H₀
(stationary)

Strong stationarity — both tests agree

Rejects H₀

Rejects H₀

Fractional integration or structural break

Fails to reject H₀

Fails to reject H₀

Insufficient power to distinguish

Fails to reject H₀

Rejects H₀

Strong non-stationarity — both tests agree

ADF  has  known  finite-sample  size  distortion.  Near-unit-root  processes  frequently  appear  stationary  at  short
windows.  At  w  =  60,  test  power  against  slowly  trending  alternatives  can  fall  below  50%.  ADF  and  KPSS  are
therefore treated as supporting certification conditions within Block 1, not as primary predictive signals.

B1.2  Mean Stability Index  (Dominant Feature in Block 1)
Even if stationarity tests pass, the trading mean must be operationally stable. The Mean Stability
Index measures how much the rolling mean has drifted in volatility-adjusted terms over the recent
past. A mean that drifts is a mean that price is not organising around — and z-scores computed
from it will be systematically biased.

MeanDriftₜ = |µₜ − µₜ₋ₖ| / σₜ,   clipped at 3.0        (17)

MeanStabₜ = 1 / (1 + MeanDriftₜ)        (18)

Parameters: w = 60 (mean window), k = 20 (lag for drift comparison). Normalising by σₜ makes
the measure scale-invariant across instruments. The reciprocal transformation maps [0, ∞) → (0,
1], with zero drift scoring 1 and large drift scoring near 0.

Why δ₁ = 0.5σ is the stability threshold. A mean that drifts 0.5σ over 20 days is moving at 0.025σ per day. Over
a typical mean reversion trade of 5–10 days, this introduces a mean estimation error of 0.125–0.25σ — within
acceptable bounds for z-score construction. Drift exceeding 0.5σ in 20 days is more consistent with a trending
regime than a stable equilibrium.

B1.3  Variance Stability Index
A sudden volatility regime shift invalidates σₜ in the z-score denominator. The Variance Stability
Index detects such shifts:

VarStabₜ = 1 − |(σₜ / σₜ₋ₖ) − 1|,   clipped at 0        (19)

Parameters: w = 20, k = 20. A value of 1 means volatility is identical to k periods ago; a value of
0  means  it  has  doubled  or  halved.  The  purpose  is  narrow:  ensure  that  the  σₜ  used  in  z-score
construction  is  representative  of  the  current  regime  and  was  not  estimated  under  a  materially
different volatility environment.

Block 1 Score
Combining the three features with their internal weights:

B₁ₜ = 0.30 · (Rᴬᴰᴼ + Rᴺᴸᴺᴸ) / 2 + 0.50 · Rᴹᴸᴬₛ + 0.20 · Rᵛᴸᵃ        (20)

All R-values are percentile ranks on the 252-day lookback window, scaled to [0, 100], directionally
adjusted so that R = 100 is always most mean reversion-favourable.

Adaptive Mean Reversion Framework

   Block 2 — Mean Reversion Strength  (Weight: 60%)

Block 2 is the heart of the framework. It directly addresses the central economic hypothesis: does
price  actually  snap  back  toward  equilibrium  after  deviating?  A  high  Block  2  score  means  the
market  has  demonstrated,  in  historical  data,  that  deviations  from  the  estimated  mean  are
predictably  followed  by  reversals  —  the  defining  characteristic  of  a  tradable  mean-reverting
process.

Block 2 is weighted at 60% because it is the only block that directly and empirically answers the
detection question. Mean reliability (Block 1) and tradability (Block 3) are necessary conditions,
but neither tells you whether the reversion actually occurs. Only Block 2 does.

Feature

Economic Purpose

Internal Weight

B2.1  Direct Reversion
Coefficient (DRC)

B2.2  Mean Reversion Hit Rate

Tests whether z-score deviations
empirically predict future snapback
returns

Measures consistency: how often do
large deviations actually revert?

50%

30%

B2.3  Multi-Scale Variance Ratio  Structural process-level test of mean

20%

reversion across multiple horizons

B2.1  Direct Reversion Coefficient — The Primary Signal
The Direct Reversion Coefficient is the most economically direct test in the framework, and the
strongest single signal. It asks the question that matters most: conditional on the current z-score
deviation, do future returns predict a move back toward the mean?

The DRC is estimated by regressing forward returns at horizon h on the current z-score:

rₜ₊ℎ = α + β · zₜ + εₜ,   h ∈ {1, 3, 5}        (21)

For  a mean-reverting  market,  β <  0:  when price  is  above  the mean (z  >  0), future returns are
expected to be negative (price falls back); when price is below the mean (z < 0), future returns
are  expected  to  be  positive  (price  rises  back).  The  coefficient  β  is  the  empirical  analog  of  the
restoring force κ in the OU process.

The DRC t-statistic uses Newey-West HAC standard errors:

tβ(h) = β̂(h) / SEᴺᴺᴬᴹ(β̂(h))        (22)

with Newey-West lag ℓᴺᴺ = ⌊1.3 · h²/³⌋ (Andrews 1991 plug-in rule). Aggregating across horizons:

DRCₜ = minℎ∈{1,3,5} tβ(h)        (23)

Rank direction: rank on −DRCₜ (most negative aggregate t-statistic receives rank 100). Minimum
window: w = 120 days.

Why β < 0 is the mean reversion signal.  The regression in equation (21) is the discrete-time
equivalent of asking whether the OU restoring force is present. In the continuous-time OU process, κ
> 0 means deviations are corrected. In the discrete-time AR(1) equivalent, β ∈ (0, 1) is mean-
reverting. In the predictive regression (21), β < 0 is the empirical manifestation of the same force:
deviations above the mean predict negative future returns. A strongly negative β with a large Newey-

Adaptive Mean Reversion Framework

West t-statistic is the most direct available evidence that the market is mean-reverting around the
estimated equilibrium.

Why Newey-West standard errors are mandatory.  When h > 1, the regression residuals are
serially correlated by construction — overlapping return windows share observations. OLS standard
errors will be too small, producing inflated t-statistics that overstate the statistical evidence. HAC
correction via the Newey-West estimator is not optional; it is required for valid inference.

Lookahead bias prevention.  The z-score zₜ uses µ*ₜ and σₜ, both of which must be computed on
data strictly before time t (using Pₜ₋₁ through Pₜ₋ᵤ). Including Pₜ in the mean or variance estimate
introduces contemporaneous bias that makes the backtest meaningless. This constraint applies
identically in live trading, where the current bar is not yet closed when signals are computed.

B2.2  Mean Reversion Hit Rate
The Hit Rate measures the empirical frequency with which large z-score deviations are followed
by a price move  back toward  the mean.  Where the  DRC  measures  the  average magnitude  of
reversion, the Hit Rate measures its consistency.

HitRateₜ = #{s ∈ Wₜ : |zₜ| > θ and sign(Pₜ₊ℎ − Pₜ) = −sign(zₜ)} / #{s ∈ Wₜ : |zₜ| > θ}        (24)

where Wₜ is the rolling estimation window, θ = 1.0 (fixed), and h = 5. The feature is excluded from
the block score if the event count falls below 20.

Why θ = 1.0 is fixed rather than optimised. Searching over θ to maximise hit rate is direct overfitting. The 1-sigma
threshold has theoretical grounding: under Gaussian returns it corresponds to the 84th percentile of the deviation
distribution. Fixing θ = 1.0 consistently across all instruments is a principled constraint that trades some potential
precision for complete resistance to data-snooping bias.

B2.3  Multi-Scale Variance Ratio
Computing VR at four horizons q ∈ {2, 5, 10, 20}:

VR(q)ₜ = Var̂(Xₜ − Xₜ₋ᵤ) / (q · Var̂(Xₜ − Xₜ₋₁))        (25)

Aggregated by taking the minimum across horizons:

VRᵃᵍᵍₜ = minᵤ∈{2,5,10,20} VR(q)ₜ        (26)

Under  a  random  walk,  VR(q)  =  1  for  all  q.  Mean  reversion  produces  VR  <  1.  Trend-following
produces  VR  >  1.  Taking  the  minimum  identifies  the  most  mean-reverting  horizon,  which  also
informs holding period calibration in Phase 4. Rank direction: rank on (1 − VRᵃᵍᵍₜ).

The Variance Ratio serves as a structural process-level sanity check rather than a primary signal. Because it is
derived  mathematically  from  the  same  AR(1)  coefficient  β  that  underpins  the  OU  process,  the  VR  and  DRC
estimates  of  the  reversion  parameter  κ  should  agree.  Large  discrepancies  between  them  signal  model
misspecification or structural instability within the estimation window.

Block 2 Score

B₂ₜ = 0.50 · Rᴰᴼᴶ + 0.30 · Rᴴᴼ + 0.20 · Rᵛᴼ        (27)

   Block 3 — Tradability  (Weight: 20%)

Adaptive Mean Reversion Framework

Block 3 answers a different question from Blocks 1 and 2. Blocks 1 and 2 establish that mean
reversion exists and is reliable. Block 3 asks whether it is currently easy to extract. A market may
exhibit strong structural mean reversion yet be temporarily difficult to trade due to an adverse half-
life, a volatility compression pattern, or a spread level that prevents breakeven.

Importantly, Block 3 should not suppress a strong signal from Block 2. A tradability score of 0
does  not  mean  the  structural  edge  has  disappeared  —  it  means  current  conditions  are
unfavourable for extraction. This distinction informs risk management: lower Block 3 scores call
for reduced position sizing and patience, not trade abandonment.

B3.1  OU Half-Life Proximity Score
For daily strategies, there is an optimal half-life range: too short (< 2–3 days) and the reversion is
dominated by microstructure noise that is not tradable; too long (> 40 days) and transaction costs
erode the edge before reversion completes. The half-life proximity score rewards the sweet spot:

HL scoreₜ = max(0,  1 − |ln HLₜ − ln HLᵒᵖᵗ| / ln 2),   HLᵒᵖᵗ = 10 days        (28)

Score peaks at 1.0 when HL = 10 days. It reaches 0 at HL ≤ 2.5 or HL ≥ 40 days. Set to 0 when
κ̂ ≤ 0. Log-space is used because half-life spans orders of magnitude: in linear space, HL = 20
and HL = 0.5 are penalised identically despite the former being far more tradable.

B3.2  Volatility Compression Score
Mean reversion strategies perform best when volatility is falling from a moderate base — not when
it is expanding from an extreme. The Volatility Compression Score captures this:

VCₜ = −(RVₜ − RVₜ₋ₖ) / RVₜ₋ₖ,   RVₜ = √(252/wₜ · Σ r²ₜ₋ᵢ)        (29)

VCscoreₜ = VCₜ · (1 − VPₜ / 100)        (30)

Parameters: wₜ = 20, k = 5. A positive VCscore means volatility is falling from a moderate base
—  the  ideal  mean  reversion  environment.  The  weighting  term  (1  −  VPₜ/100)  penalises
compression  from  extreme  volatility  levels,  since  extreme  vol  regimes  are  structurally
unfavourable for mean reversion trading regardless of the trend direction.

B3.3  Transaction Cost Filter
The Transaction Cost Filter estimates whether the current expected edge from a trade exceeds
the all-in transaction cost:

ExpEdgeₜ = |zₜ| · σₜ · |β̂ᴰᴼᴶ|        (31)

AdjEdgeₜ = ExpEdgeₜ − TotalCostₜ        (32)

zᵚᵢᵏ,ₜ = TotalCostₜ / (σₜ · |β̂ᴰᴼᴶ|)        (33)

zᵚᵢᵏ,ₜ  is  the  breakeven  z-score  —  entries  with  |zₜ|  <  zᵚᵢᵏ,ₜ  cannot  cover  transaction  costs  in
expectation. When spread data is unavailable, proxy TotalCostₜ ≈ c · RVₜ with c ∈ [0.1, 0.3] and
use TCFscoreₜ = max(0, 1 − VPₜ / 100).

Block 3 Score

B₃ₜ = (1/3) · (Rᴴᴸ + Rᵛᴶ + Rᴻᴶᴼ)        (34)

Adaptive Mean Reversion Framework

Complete Variable Glossary

Index and Timeframe Variables

Symbol

Definition

t

i

τ

Pₜ

rₜ

r(q)ₜ

w

W

Wᴴ

Wᴹ

Wₜ

wₜ

k

h

p

q

N

Time index. Current observation t; past observations t−1, t−2, …

Instrument index (e.g. NIFTY, Crude Oil, EUR/USD)

Timeframe (τᴴ = weekly, τᴹ = daily, τᴸ = 4H)

Log price at time t

Log return: rₜ = ln Pₜ − ln Pₜ₋₁

q-period log return: r(q)ₜ = ln Pₜ − ln Pₜ₋ᵤ

Short rolling window length (default: 60 days)

Percentile rank lookback window (252 trading days)

Higher-timeframe trend classification window (52 weekly bars)

Medium-timeframe mean estimation window (60 daily bars)

Short detrending window for trending markets (20 daily bars)

Short volatility estimation window (20 days)

Lag displacement for stability tests (20 days)

Forward horizon for predictive regressions (h ∈ {1, 3, 5} days)

AR lag order (AIC selection; Schwert default: ⌊(w/100)¹/⁴⌋)

Variance Ratio horizon (q ∈ {2, 5, 10, 20})

Event count for Hit Rate (minimum 20 qualifying events required)

Mean and Volatility Estimates

Symbol

Definition

µ*ₜ

µₜ

µₜ₋ₖ

r̅

σₜ

σₜ₋ₖ

σₜₜ

RVₜ

Optimal mean estimate — the central object of Section 4

Rolling arithmetic mean of prices over window w

Rolling mean lagged k periods (used in MeanDrift)

Sample mean of returns over window w

Rolling standard deviation of log returns over w

Rolling standard deviation lagged k periods (used in VarStab)

OU stationary standard deviation: σₜₜ = σ/√(2κ)

Realised volatility over wₜ: √(252/wₜ · Σr²ₜ₋ᵢ)

Adaptive Mean Reversion Framework

VPₜ

zₜ

zᵉᵌᵗᴿᵧ

zₜᵗᵒᵖ

zᵚᵢᵏ

Volatility percentile: rank of RVₜ in 252-day history × 100

Z-score: (Pₜ − µ*ₜ) / σₜ

Entry z-score threshold from breakeven condition

Stop-loss z-score increment: kₜᵗᵒᵖ · σₜₜ

Breakeven z-score: minimum deviation that covers transaction costs

OU Process Parameters

Symbol

Definition

κ

κ̂

βᵁᵁ

αᵁᵁ

HL

OU mean reversion speed (continuous time). κ > 0 required for mean reversion.

Estimated κ: −ln β̂ᵁᵁ from discrete AR(1)

AR(1) coefficient: must satisfy βᵁᵁ ∈ (0, 1) for mean reversion

AR(1) intercept: αᵁᵁ = µ(1 − e⁻ᵏ)

Half-life: ln 2 / κ

HLᵒᵖᵗ

Optimal half-life for daily strategies: 10 trading days

HLscoreₜ

Proximity score (equation 28). Peaks at HL = HLᵒᵖᵗ.

dWₜ

Standard Wiener process increment: N(0, dt)

MRScore Features, Blocks, and Parameters

Symbol

Definition

pᴬᴰᴼ

pᴺᴸᴺᴸ

ADF test p-value. Lower → stronger rejection of unit root.

KPSS test p-value. Higher → fail to reject stationarity.

MeanDriftₜ

|µₜ − µₜ₋ₖ| / σₜ. Drift of rolling mean in volatility units.

MeanStabₜ

1 / (1 + MeanDriftₜ) ∈ (0, 1]. Mean stability index.

VarStabₜ

1 − |σₜ/σₜ₋ₖ − 1|. Variance stability index, clipped at 0.

VR(q)ₜ

VRᵃᵍᵍₜ

β̂ᴰᴼᴶ

tβ(h)

DRCₜ

Variance Ratio at horizon q. Random walk → 1; MR → <1; trend → >1.

min_q VR(q)ₜ. Most mean-reverting horizon.

OLS slope in DRC regression (equation 21). Negative → mean reversion.

Newey-West t-statistic on β̂ at horizon h.

min_h tβ(h). Aggregate Direct Reversion Coefficient.

HitRateₜ

Empirical P(reversion within h = 5 days | |zₜ| > 1.0).

θ

Hit Rate threshold. Fixed at 1.0σ.

Adaptive Mean Reversion Framework

VCₜ

VCscoreₜ

AdjEdgeₜ

B₁ₜ

B₂ₜ

B₃ₜ

Volatility compression: −(RVₜ − RVₜ₋ₖ) / RVₜ₋ₖ. Positive = vol falling.

VCₜ · (1 − VPₜ/100). Compression weighted by volatility level.

Expected gross edge minus transaction cost (equation 32).

Block 1 score (equation 20). Mean Reliability.

Block 2 score (equation 27). Mean Reversion Strength.

Block 3 score (equation 34). Tradability.

MRScoreₜ

Master score (equation 13). ∈ [0, 100].

Rᵢ,ₜ

Percentile rank of feature i at time t, 252-day window, scaled to [0, 100].

Trend and Stability Parameters

Symbol

Definition

tᵇ

R²

ε̂ₜ

δ₁

θᵜᵒᵌ

θᵉˣᵗ

t-statistic on OLS slope in trend regression (equation 36)

Coefficient of determination in trend regression. Threshold: R² ≥ 0.30

Detrended residual: Pₜ − µ*(T)ₜ (equation 44)

Mean drift threshold for S1: MeanDrift < δ₁ = 0.5

Volatility percentile threshold for normal MR trading: 70th percentile

Volatility percentile for full MR suspension: 90th percentile

TrendᵰFᴴ

Trend direction on higher timeframe: +1 (uptrend) or −1 (downtrend)

Tᵚᵃˣ

kₜᵗᵒᵖ

ℓᴺᴺ

Maximum holding period: 2 · HL̂ ₜ days

Stop-loss multiplier: 1.5 standard deviations of OU stationary distribution

Newey-West lag: ⌊1.3 · h²/³⌋ (Andrews 1991)

S1–S5

Mean certification conditions (equations 40–47)

Key parameter defaults — all in one place.  w = 60 (feature windows) · W = 252 (rank lookback) ·
Wᴴ = 52 (weekly trend) · Wᴹ = 60 (non-trending mean) · Wₜ = 20 (detrend window) · wₜ = 20 (realised
vol) · k = 20 (stability lag) · q ∈ {2, 5, 10, 20} (VR horizons) · h ∈ {1, 3, 5} (DRC horizons) · θ = 1.0
(Hit Rate) · HLᵒᵖᵗ = 10 days · θᵜᵒᵌ = 70th percentile · θᵉˣᵗ = 90th percentile · δ₁ = 0.5 · R² ≥ 0.30
(trend) · kₜᵗᵒᵖ = 1.5 · Tᵚᵃˣ = 2 · HL̂


