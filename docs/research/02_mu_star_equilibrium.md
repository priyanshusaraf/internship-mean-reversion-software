Table of Contents
Equilibrium Price Estimation in Adaptive Mean Reversion Frame-
works 3
The Anchored Kalman Approach: Architecture, Validation, and Confi-
dence Quantification . . . . . . . . . . . . . . . . . . . . . . . . . 3
Research Paper V2.5 . . . . . . . . . . . . . . . . . . . . . . . . . 3
Abstract . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
Notation and Symbol Glossary . . . . . . . . . . . . . . . . . . . . . . 4
Section 1 — The Problem of Equilibrium Price Estimation . . . . . . . 7
1.1 Why Equilibrium Matters . . . . . . . . . . . . . . . . . . . . 7
1.2 Definition of Latent Equilibrium . . . . . . . . . . . . . . . . . 8
1.3 Four Subproblems . . . . . . . . . . . . . . . . . . . . . . . . 8
1.4 Hidden Assumptions . . . . . . . . . . . . . . . . . . . . . . . 9
1.5 Three Structural Difficulties . . . . . . . . . . . . . . . . . . . 9
Section 2 — Mathematical Foundations . . . . . . . . . . . . . . . . . 10
2.1 Stationarity Prerequisites . . . . . . . . . . . . . . . . . . . . 10
2.2 The Ornstein-Uhlenbeck Process . . . . . . . . . . . . . . . . 11
2.3 Discrete-Time Approximation and the Near-Unit-Root Problem 11
2.4 State-Space Formulation . . . . . . . . . . . . . . . . . . . . . 12
2.5 Unobserved Component Model and Misspecification Implica-
tions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
2.6 The Kalman Filter Recursions . . . . . . . . . . . . . . . . . . 13
Section 3 — Why Existing Methods Fail . . . . . . . . . . . . . . . . . 14
3.1 Rolling Mean . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
3.2 Exponential Moving Average . . . . . . . . . . . . . . . . . . 15
3.3 OU-Implied Equilibrium . . . . . . . . . . . . . . . . . . . . . 15
Section 4 — The Anchored Kalman Estimator . . . . . . . . . . . . . . 15
4.1 Motivation and Design Objectives . . . . . . . . . . . . . . . . 15
4.2 Full Model Specification . . . . . . . . . . . . . . . . . . . . . 16
4.3 The Long-Run Anchor and Its Economic Justification . . . . . 16
4.4 The Anti-Drift Guarantee . . . . . . . . . . . . . . . . . . . . . 17
4.5 Kalman Recursions (Operational) . . . . . . . . . . . . . . . . 18
4.6 Steady-State Properties . . . . . . . . . . . . . . . . . . . . . 19
4.7 Parameter Calibration and the Constrained Estimator . . . . . 19
4.8 Volume Availability and the PSEUDO_ANCHORED_KALMAN
Flag . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
Section 5 — Candidate Equilibrium Methods . . . . . . . . . . . . . . 20
5.1 The Anchored Kalman as Primary (Tier 1) . . . . . . . . . . . 20
5.2 VWAP as Anchor Validator (Tier 1 Support) . . . . . . . . . . 21
5.3 Point of Control as Tier 2 Component . . . . . . . . . . . . . . 21
5.4 OU-Implied Equilibrium as Diagnostic Only . . . . . . . . . . 21
5.5 EMA as Fallback, S/R Eliminated . . . . . . . . . . . . . . . . 21
Section 6 — The Controlled Adaptation Problem . . . . . . . . . . . . 22
6.1 Formal Statement . . . . . . . . . . . . . . . . . . . . . . . . 22
6.2 The
𝑄/𝐷2
Ratio as the Primary Adaptation Diagnostic . . . . 22
6.3 Adaptive 𝑄 Variants (Deferred) . . . . . . . . . . . . . . . . . 22
6.4 The Inflection-Point Problem . . . . . . . . . . . . . . . . . . 23
1

6.5 CUSUM Break Detection and the Post-Break Protocol . . . . . 23
Section 7 — The Mean Clustering Hypothesis . . . . . . . . . . . . . . 24
7.1 The Ensemble Argument (Compressed) . . . . . . . . . . . . . 24
7.2 The Independence Violation Problem . . . . . . . . . . . . . . 24
7.3 Where Genuine Orthogonality Exists . . . . . . . . . . . . . . 25
7.4 Revised Role: Qualitative Heuristic . . . . . . . . . . . . . . . 25
Section 8 — The Equilibrium Validity Problem . . . . . . . . . . . . . . 25
8.1 When Equilibrium Does Not Exist . . . . . . . . . . . . . . . . 25
8.2 Conditions for Validity . . . . . . . . . . . . . . . . . . . . . . 25
8.3 The Phase-Specific Validity Gate . . . . . . . . . . . . . . . . 26
Section 9 — Independent Regime Engine . . . . . . . . . . . . . . . . 27
9.1 Purpose and Independence Requirement . . . . . . . . . . . . 27
9.2 RFI_lite Specification . . . . . . . . . . . . . . . . . . . . . . 27
9.3 Gating Rules and Threshold Protection . . . . . . . . . . . . . 27
9.4 DAG Structure . . . . . . . . . . . . . . . . . . . . . . . . . . 28
9.5 Kill Criterion . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
Section 10 — Four-Layer Architecture and Integration . . . . . . . . . 29
10.1 Architecture Overview . . . . . . . . . . . . . . . . . . . . . 29
10.2 What This Architecture Does Not Do . . . . . . . . . . . . . 29
10.3 AMR Framework Integration . . . . . . . . . . . . . . . . . . 30
𝜇
10.4 The Confidence Score 𝐶 . . . . . . . . . . . . . . . . . . . 30
𝑡
Section 11 — Failure Mode Analysis . . . . . . . . . . . . . . . . . . . 33
11.1 Near-Unit-Root Parameter Instability . . . . . . . . . . . . . 33
11.2 CUSUM Cascade . . . . . . . . . . . . . . . . . . . . . . . . 34
11.3 Anchor Drift During Sustained Trends . . . . . . . . . . . . . 34
11.4 Model Misspecification (Non-Gaussian Innovations) . . . . . 35
11.5 Volume Data Degradation . . . . . . . . . . . . . . . . . . . 35
11.6 Regime Conditioning Circularity . . . . . . . . . . . . . . . . 35
11.7 Multi-Timeframe Consistency . . . . . . . . . . . . . . . . . 35
Section 12 — Validation Architecture . . . . . . . . . . . . . . . . . . 36
12.0 Data Validation Protocol . . . . . . . . . . . . . . . . . . . . 36
12.1 Out-of-Sample Design . . . . . . . . . . . . . . . . . . . . . . 36
12.2 Experiment Programme . . . . . . . . . . . . . . . . . . . . 36
12.3 Simulation Studies . . . . . . . . . . . . . . . . . . . . . . . 38
12.4 Kill Criteria . . . . . . . . . . . . . . . . . . . . . . . . . . . 38
Section 13 — Research Roadmap . . . . . . . . . . . . . . . . . . . . . 39
13.1 Phase 1 — Baseline Validation (Current) . . . . . . . . . . . 39
13.2 Phase 2 — Regime Integration . . . . . . . . . . . . . . . . . 39
13.3 Phase 3 — Confidence Integration and Signal Readiness . . . 40
13.4 Deferred Components . . . . . . . . . . . . . . . . . . . . . 40
13.5 What Constitutes Premature Optimisation . . . . . . . . . . 40
Section 14 — Conclusion . . . . . . . . . . . . . . . . . . . . . . . . . 41
Appendix A — Mathematical Derivations . . . . . . . . . . . . . . . . 42
A.1 Proof of the Anti-Drift Theorem (Theorem 4.2) . . . . . . . . . 42
A.2 Derivation of the Steady-State Kalman Gain . . . . . . . . . . 42
A.3 Prediction Error Decomposition Likelihood . . . . . . . . . . . 42
Appendix B — Deferred Research Directions . . . . . . . . . . . . . . 43
B.1 Adaptive 𝑄 Variants . . . . . . . . . . . . . . . . . . . . . . . 43
2

B.2 Robustness Extensions Under Non-Gaussianity . . . . . . . . 43
B.3 Multi-Timeframe Hierarchy . . . . . . . . . . . . . . . . . . . 44
B.4 Confidence Score Tier 2 Introduction Protocol . . . . . . . . . 44
Equilibrium Price Estimation in Adaptive Mean Rever-
sion Frameworks
The Anchored Kalman Approach: Architecture, Validation, and
Confidence Quantification
Research Paper V2.5
This document constitutes the working research paper for the
𝜇∗
equilibrium
estimation component of the Adaptive Mean Reversion (AMR) framework. It
is scoped exclusively to equilibrium estimation — it does not constitute a trad-
ing strategy, a signal generation specification, or a position-sizing guide. Its
purpose is to establish a theoretically coherent, empirically testable, and im-
plementationally viable method for estimating the latent price level to which a
market temporarily reverts.
Abstract
The estimation of a latent equilibrium price
𝜇∗
is the foundational problem in
any mean reversion trading framework. Errors in equilibrium estimation prop-
agate multiplicatively through regime detection, signal construction, and posi-
tion sizing — a poorly identified
𝜇∗
does not merely degrade individual trades
but systematically biases the entire downstream inference structure. Despite
this centrality, equilibrium estimation has received comparatively little rigor-
ous treatment in applied quantitative finance, where practitioners typically
default to rolling means or exponentially weighted moving averages without
formal justification.
This paper presents V2.5 of the Anchored Kalman Equilibrium Estimator, a
frameworkthattreats𝜇∗
asalatentstatetrackedbyaKalmanfilterwhoselong-
run mean is anchored to an economically grounded reference — the volume-
weighted average price (VWAP) over an institutionally relevant horizon. Three
architectural advances distinguish V2 from earlier practice: an independent
regime engine (RFI) that gates the use of
𝜇∗
without introducing feedback
3

into its estimation; a CUSUM-based structural break detector that replaces
the fragile three-bar rule of prior implementations; and a compressed three-
phase validation roadmap with explicit kill criteria that bounds the research
programme.
V2.5 introduces two further refinements. First, a revised post-break recovery
protocol in Section 6.5 eliminates cascade failure in the CUSUM detector — a
fragilityinV2inwhichgenuinestructuralbreakscouldtriggeroscillatoryfalse-
positivesequencesthatprolongedfiltersuspensionwellbeyondtheactualtran-
𝜇
sition. Second, a redesigned confidence score 𝐶 in Section 10.4 quantifies
𝑡
real-timeestimationreliabilityusingKalman-internaldiagnosticsonly, without
circularity or reference to downstream trading performance. The confidence
score is deployable from Phase 1 of the validation programme, enabling data
collection on its predictive value before any operational use is committed.
The framework is structured as a directed acyclic graph (DAG): RFI feeds into
the validity gate 𝑉 , which gates signal use; neither RFI nor 𝑉 feeds back into
|     |     | 𝑡   |     |     | 𝑡   |     |
| --- | --- | --- | --- | --- | --- | --- |
the Kalman filter’s execution. This architecture resolves the circularity prob-
lem that afflicts simpler mean reversion frameworks. All claims remain work-
ing hypotheses pending empirical validation under the programme described
| in Section | 12. |                 |     |     |     |     |
| ---------- | --- | --------------- | --- | --- | --- | --- |
| Notation   | and | Symbol Glossary |     |     |     |     |
The following symbols are used consistently throughout. The scope constraint
𝜇∗
— that this document addresses estimation only — applies to every formula.
| No signal, | position, | or PnL quantity | appears     | here.       |               |     |
| ---------- | --------- | --------------- | ----------- | ----------- | ------------- | --- |
| Symbol     |           |                 | Definition  |             |               |     |
| 𝜇∗         |           |                 |             |             |               | 𝑡.  |
|            |           |                 | True latent | equilibrium | price at time |     |
𝑡
Unobserved.
| 𝜇̂  |     |     | Filtered | estimate | of 𝜇∗ given information |     |
| --- | --- | --- | -------- | -------- | ----------------------- | --- |
| 𝑡|𝑡 |     |     |          |          | 𝑡                       |     |
𝑡.
|     |     |     | through | The primary | output. |     |
| --- | --- | --- | ------- | ----------- | ------- | --- |
𝜇̂ 𝜇∗
|       |     |     | One-step-ahead | prediction    | of .        |      |
| ----- | --- | --- | -------------- | ------------- | ----------- | ---- |
| 𝑡|𝑡−1 |     |     |                |               | 𝑡           |      |
| 𝜇     |     |     | Long-run       | anchor level. | Equals VWAP | over |
anchor,𝑡
|     |     |     | the anchor | window       | when volume data | is  |
| --- | --- | --- | ---------- | ------------ | ---------------- | --- |
|     |     |     | available; | arithmetic   | mean otherwise   |     |
|     |     |     | (flagged   | separately). |                  |     |
4

| Symbol |     | Definition  |                 |          |                |     |      |        |
| ------ | --- | ----------- | --------------- | -------- | -------------- | --- | ---- | ------ |
| 𝑃      |     | Posterior   | error           | variance |                | of  | 𝜇̂ . | Kalman |
| 𝑡|𝑡    |     |             |                 |          |                |     | 𝑡|𝑡  |        |
|        |     | uncertainty | measure.        |          |                |     |      |        |
| 𝑃      |     | Prior       | error variance. |          | One-step-ahead |     |      |        |
𝑡|𝑡−1
|     |     | prediction | variance. |     |     |     |     |     |
| --- | --- | ---------- | --------- | --- | --- | --- | --- | --- |
𝑃
|     |     | Steady-state |     | posterior |     | variance: |     |     |
| --- | --- | ------------ | --- | --------- | --- | --------- | --- | --- |
∞
𝑄/max(1−𝜌2,0.01).
| 𝜌   |     | Mean | reversion | speed |     | parameter. |     |     |
| --- | --- | ---- | --------- | ----- | --- | ---------- | --- | --- |
𝜌 ∈ (0,1).
|     |     |     | Controls |     | pull-speed |     | toward |     |
| --- | --- | --- | -------- | --- | ---------- | --- | ------ | --- |
𝜇
.
anchor
| 𝜌   |     | Cross-instrument |     |     | prior | for 𝜌 | used | in the |
| --- | --- | ---------------- | --- | --- | ----- | ----- | ---- | ------ |
0
|     |     | constrained | estimator.  |     |                | An empirically |            |          |
| --- | --- | ----------- | ----------- | --- | -------------- | -------------- | ---------- | -------- |
|     |     | motivated   | starting    |     | value          | drawn          |            | from the |
|     |     | observed    | range       | of  | near-unit-root |                |            | mean     |
|     |     | reversion   | persistence |     | at             | daily          | frequency. |          |
|     |     | See Section | 4.7.        |     |                |                |            |          |
𝑄
|     |     | State | transition | variance. |     | Controls |     | how |
| --- | --- | ----- | ---------- | --------- | --- | -------- | --- | --- |
𝜇∗
|     |     | fast | is permitted |     | to  | move. |     |     |
| --- | --- | ---- | ------------ | --- | --- | ----- | --- | --- |
𝑡
𝐷2
|     |     | Observation    |        | noise     | variance    |     | (denoted | 𝑅 in |
| --- | --- | -------------- | ------ | --------- | ----------- | --- | -------- | ---- |
|     |     | standard       | Kalman | notation; |             |     | 𝐷2 used  | here |
|     |     | to distinguish |        | from      | correlation |     |          |      |
coefficients).
| 𝜁   |     | Normalised | innovation: |     |       | 𝜈 /√𝑆   |     | where |
| --- | --- | ---------- | ----------- | --- | ----- | ------- | --- | ----- |
| 𝑡   |     |            |             |     |       | 𝑡       | 𝑡   |       |
|     |     | 𝑆 = 𝑃      | +𝐷2         | .   | Under | correct |     |       |
𝑡 𝑡|𝑡−1
|     |     | specification: |     | 𝜁 ∼ | iid𝑁(0,1). |     |     |     |
| --- | --- | -------------- | --- | --- | ---------- | --- | --- | --- |
𝑡
| 𝐾   |     | Kalman | gain | at time | 𝑡.  |     |     |     |
| --- | --- | ------ | ---- | ------- | --- | --- | --- | --- |
𝑡
| 𝜂   |     |             |            |          |     | 𝜂 ∼      | 𝑁(0,𝑄). |     |
| --- | --- | ----------- | ---------- | -------- | --- | -------- | ------- | --- |
| 𝑡   |     | State       | transition | noise.   |     | 𝑡        |         |     |
| 𝜀   |     |             |            |          | 𝜀 ∼ | 𝑁(0,𝐷2). |         |     |
|     |     | Observation |            | noise.   |     |          |         |     |
| 𝑡   |     |             |            |          | 𝑡   |          |         |     |
| RFI |     | Independent |            | upstream |     | regime   | gate.   |     |
𝑡
|     |     | Scalar   | ∈ [0,100]. | Constructed |     |           | from |        |
| --- | --- | -------- | ---------- | ----------- | --- | --------- | ---- | ------ |
|     |     | variance | ratio      | and         | ADF | statistic |      | on raw |
𝜇∗
|     |     | price   | and volume |       | only.  | No   | -derived |        |
| --- | --- | ------- | ---------- | ----- | ------ | ---- | -------- | ------ |
|     |     | inputs. | RFI        | gates | signal | use, | not      | Kalman |
𝑡
execution.
| MRScore | 𝑡   | Mean | reversion | favourability |     |     | score | from |
| ------- | --- | ---- | --------- | ------------- | --- | --- | ----- | ---- |
𝑉
|     |     | the AMR | framework. |     | Appears |     | in  | and |
| --- | --- | ------- | ---------- | --- | ------- | --- | --- | --- |
𝑡
|     |     | as experimental |     | stratification. |     |         | Full |        |
| --- | --- | --------------- | --- | --------------- | --- | ------- | ---- | ------ |
|     |     | specification   |     | in the          | AMR | working |      | paper. |
5

| Symbol | Definition  |     |          |       |        |     |     |
| ------ | ----------- | --- | -------- | ----- | ------ | --- | --- |
| 𝑉      | Equilibrium |     | validity | gate. | Binary |     |     |
𝑡
𝑉 = 1
|     | indicator. |     |     | permits | downstream |     | use |
| --- | ---------- | --- | --- | ------- | ---------- | --- | --- |
𝑡
|     | of 𝜇̂ . | Two | phase-specific |     | forms | defined |     |
| --- | ------- | --- | -------------- | --- | ----- | ------- | --- |
𝑡|𝑡
|            | in Section | 8.3.   |           |     |        |     |      |
| ---------- | ---------- | ------ | --------- | --- | ------ | --- | ---- |
|            |            |        |           |     |        | =   | 1    |
| break_flag | One-bar    | binary | detection |     | event. |     | only |
𝑡
|     | on the     | bar where |      | CUSUM | first | exceeds |     |
| --- | ---------- | --------- | ---- | ----- | ----- | ------- | --- |
|     | threshold. | Not       | used | in    | 𝑉 .   |         |     |
𝑡
| suspended | Persistent |     | suspension |     | indicator |     |     |
| --------- | ---------- | --- | ---------- | --- | --------- | --- | --- |
𝑡
|     | ∈ {0,1}. |        |     |       |            |     | = 1 |
| --- | -------- | ------ | --- | ----- | ---------- | --- | --- |
|     |          | Active |     | after | break_flag |     |     |
𝑡
|     | until recovery |      | conditions |     |            | in Section |     |
| --- | -------------- | ---- | ---------- | --- | ---------- | ---------- | --- |
|     | 6.5 are        | met. | Replaces   |     | break_flag |            | in  |
𝑡
𝑉
all 𝑡 formulas.
+
| CUSUM | Upper | CUSUM | statistic |     | for | positive |     |
| ----- | ----- | ----- | --------- | --- | --- | -------- | --- |
𝑡
|     | innovation | sequences. |     |     |     |     |     |
| --- | ---------- | ---------- | --- | --- | --- | --- | --- |
−
| CUSUM | Lower | CUSUM | statistic |     | for | negative |     |
| ----- | ----- | ----- | --------- | --- | --- | -------- | --- |
𝑡
|     | innovation | sequences. |     |     |     |     |     |
| --- | ---------- | ---------- | --- | --- | --- | --- | --- |
ℎ
|     | CUSUM | decision |     | threshold. |     | Default |     |
| --- | ----- | -------- | --- | ---------- | --- | ------- | --- |
𝑐
|     | starting      | value | 5.0.     | Temporarily |     | elevated |     |
| --- | ------------- | ----- | -------- | ----------- | --- | -------- | --- |
|     | under cascade |       | damping. |             |     |          |     |
𝑘
| 𝑐      | CUSUM       | reference  |         | value    | (slack |        |      |
| ------ | ----------- | ---------- | ------- | -------- | ------ | ------ | ---- |
|        | parameter). |            | Default | starting |        | value  | 0.5. |
| 𝐶local | Local       | confidence |         | score    | ∈      | [0,1]. |      |
𝑡
|     | Kalman-internal. |        |     | Real-time   |     | estimate |     |
| --- | ---------------- | ------ | --- | ----------- | --- | -------- | --- |
|     | quality          | based  | on  | uncertainty |     | and      |     |
|     | CUSUM            | state. |     |             |     |          |     |
𝐶global
|     | Global | confidence |     | score | ∈   | [0,1]. |     |
| --- | ------ | ---------- | --- | ----- | --- | ------ | --- |
𝑡
|     | Rolling    | window |           | coherence |            | of the     |     |
| --- | ---------- | ------ | --------- | --------- | ---------- | ---------- | --- |
|     | estimator, |        | based     | on        | innovation |            |     |
|     | whiteness  | and    | parameter |           |            | stability. |     |
𝜇
| 𝐶   | Combined |     | confidence |     | score: |     |     |
| --- | -------- | --- | ---------- | --- | ------ | --- | --- |
𝑡
|     | 𝐶local ×𝐶global |                | ∈   | [0,1]. | Logged | from  |        |
| --- | --------------- | -------------- | --- | ------ | ------ | ----- | ------ |
|     | 𝑡               | 𝑡              |     |        |        |       |        |
|     | Phase           | 1. Operational |     |        | only   | after | Tier 2 |
validation.
| DRC | Direct      | Reversion    |          | Coefficient. |         | Primary    |        |
| --- | ----------- | ------------ | -------- | ------------ | ------- | ---------- | ------ |
|     | validation  | metric       |          | from         | the AMR |            |        |
|     | framework.  |              | Measures |              | whether | deviations |        |
|     | from 𝜇̂     | historically |          | revert.      | Defined |            | in the |
|     | AMR working |              | paper.   |              |         |            |        |
6

| Symbol |     |     | Definition      |     |          |               |       |            |       |
| ------ | --- | --- | --------------- | --- | -------- | ------------- | ----- | ---------- | ----- |
| VWAP   |     |     | Volume-weighted |     |          | average       |       | price over | a     |
|        |     |     | specified       |     | window.  |               |       |            |       |
| POC    |     |     | Point           | of  | Control. | Price         | level | with       |       |
|        |     |     | maximum         |     | volume   | concentration |       | over       | a     |
|        |     |     | specified       |     | window.  | Tier          | 2     | component  | only. |
𝜏
|     |     |     | Timeframe        |     | index    | in          | the multi-timeframe |             |     |
| --- | --- | --- | ---------------- | --- | -------- | ----------- | ------------------- | ----------- | --- |
|     |     |     | hierarchy.       |     | Deferred |             | until               | after Phase | 1–2 |
|     |     |     | single-timeframe |     |          | validation. |                     |             |     |
| OOS |     |     | Out-of-sample.   |     |          |             |                     |             |     |
𝜇∗
Scope constraint: All formulas in this paper are estimation formulas.
Quantities from the AMR framework (MRScore, DRC, z-scores, signal thresh-
𝑉
olds) appear only where necessary to define 𝑡 or describe the validation
|     |     |     |     |     |     |     | 𝐶   | 𝜇   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
structure. They are never inputs to the Kalman filter or to .
𝑡
| Section | 1 — The     | Problem | of Equilibrium |     |     | Price | Estimation |     |     |
| ------- | ----------- | ------- | -------------- | --- | --- | ----- | ---------- | --- | --- |
| 1.1 Why | Equilibrium | Matters |                |     |     |       |            |     |     |
A mean reversion trading strategy rests on a single premise: that the current
pricewilltendtoreturntowardsomeequilibriumlevel. Everyoperationalcom-
ponent of such a strategy — regime detection, entry timing, exit targeting, po-
sitionsizing—dependsonhavingareliableestimateofwherethatequilibrium
lies. The equilibrium price 𝜇∗ is not a peripheral input; it is the load-bearing
| structure | of the entire | framework. |     |     |     |     |     |     |     |
| --------- | ------------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
This dependency is multiplicative in character. Suppose the true equilibrium
𝜇∗
is $100 and the current price is $105. A framework using a rolling mean es-
timate of $103 identifies a 2-unit deviation and generates a trade accordingly.
Aframeworkusingabetterestimateof$100identifiesa5-unitdeviation—not
just a different scale but a different trading conclusion. When this misidentifi-
cation occurs systematically across many instruments and periods, the perfor-
|     |     |     |     |     | 𝜇̂ = | 𝜇∗+𝛿 |     | 𝛿   |     |
| --- | --- | --- | --- | --- | ---- | ---- | --- | --- | --- |
mance degradation compounds. Formally: if where is the estima-
𝜇∗)
tion error, then the measured deviation 𝑧 = 𝑃 − 𝜇̂ = (𝑃 − − 𝛿 . Every
|     |     |     |     | 𝑡   | 𝑡   | 𝑡   | 𝑡   | 𝑡   | 𝑡   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
signal threshold, every position scale, and every exit level is contaminated by
𝛿
| 𝑡 . The | error does | not cancel; | it accumulates. |     |     |     |     |     |     |
| ------- | ---------- | ----------- | --------------- | --- | --- | --- | --- | --- | --- |
Thismotivatesthetreatmentofequilibriumestimationasafirst-classresearch
7

| problem |            | rather | than a    | preprocessing |     | step. |     |     |     |
| ------- | ---------- | ------ | --------- | ------------- | --- | ----- | --- | --- | --- |
| 1.2     | Definition |        | of Latent | Equilibrium   |     |       |     |     |     |
𝜇∗
Definition 1.1 (Latent Equilibrium): The equilibrium price is the unob-
𝑡
served scalar price level toward which the observed price 𝑃 exhibits statisti-
𝑡
cally detectable mean reversion during periods of confirmed mean reversion
regime. It is not assumed to be constant, nor to be observable directly. It is a
| latent | state      | whose | dynamics |          | are characterised |           | in Section   | 2.  |     |
| ------ | ---------- | ----- | -------- | -------- | ----------------- | --------- | ------------ | --- | --- |
| Three  | properties |       | are      | required | of any            | candidate | equilibrium: |     |     |
𝜇∗
1. Economic coherence: should correspond to a price level that has
𝑡
an interpretable relationship to market activity — not a purely statistical
|     | artefact | of  | the estimation |     | window. |     |     |     |     |
| --- | -------- | --- | -------------- | --- | ------- | --- | --- | --- | --- |
−𝜇∗)shouldbestationary,oratminimum
|     | 2. Stationarityofdeviations: |         |     |           | (𝑃     |      |           |          |     |
| --- | ---------------------------- | ------- | --- | --------- | ------ | ---- | --------- | -------- | --- |
|     |                              |         |     |           |        | 𝑡 𝑡  |           |          |     |
|     | exhibit                      | bounded |     | variance, | during | mean | reversion | regimes. |     |
𝜇∗
3. Estimability: should be recoverable with quantifiable uncertainty
𝑡
from observed price and volume data, without requiring future informa-
tion.
| 1.3 | Four | Subproblems |     |     |     |     |     |     |     |
| --- | ---- | ----------- | --- | --- | --- | --- | --- | --- | --- |
Theproblemofestimating𝜇∗ decomposesintofourdistinctsubproblems, each
𝑡
| of  | which | requires | independent |     | treatment: |     |     |     |     |
| --- | ----- | -------- | ----------- | --- | ---------- | --- | --- | --- | --- |
Givenanassumeddynamicmodelfor𝜇∗
| Subproblem |     |     | 1 — State | estimation: |     |     |     |     | ,   |
| ---------- | --- | --- | --------- | ----------- | --- | --- | --- | --- | --- |
𝑡
|     |     |     |     |     |     | 𝜇̂  |     | 𝑃   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
what is the optimal real-time estimate 𝑡|𝑡 and its associated uncertainty 𝑡|𝑡 ?
Subproblem 2 — Parameter calibration: The dynamic model contains pa-
rameters {𝜌,𝑄,𝐷2} that must be estimated from data. How should they be
𝜇̂
estimated, and how sensitive is 𝑡|𝑡 to parameter misspecification?
𝜇∗
Subproblem 3 — Break detection: may exhibit occasional structural
𝑡
shifts that violate the assumed dynamics. How should these be detected, and
| what | is the | correct | protocol |     | upon detection? |     |     |     |     |
| ---- | ------ | ------- | -------- | --- | --------------- | --- | --- | --- | --- |
Subproblem 4 — Regime conditioning: During periods when the market is
𝜇̂
not mean reverting, 𝑡|𝑡 may be formally well-defined but economically unin-
formative. How should the validity of the equilibrium estimate be conditioned
| on  | regime | state? |     |     |     |     |     |     |     |
| --- | ------ | ------ | --- | --- | --- | --- | --- | --- | --- |
The Anchored Kalman framework addresses all four. Subproblems 1 and 2
are addressed in Sections 2 and 4. Subproblem 3 is addressed in Section 6.
8

Subproblem 4 is addressed in Sections 8 and 9.
1.4 Hidden Assumptions
The framework rests on several working assumptions that require honest ex-
amination.
Assumption 1.1 (Existence): A latent equilibrium
𝜇∗
exists during mean re-
𝑡
version regimes. This is definitional given the regime conditioning in Section
8, but the existence of a tradable equilibrium — one estimable with sufficient
accuracy and lead time — is an empirical question addressed in Experiment 1.
Assumption 1.2 (Temporal Stability): The dynamics of
𝜇∗
are sufficiently
𝑡
stable within a 60-day estimation window that MLE-estimated parameters pro-
vide a useful approximation. This assumption breaks during structural breaks;
Section 6 addresses the consequences.
Assumption 1.3 (Cross-Timeframe Equilibrium Identity): If the frame-
work is eventually extended to multiple timeframes, the equilibrium estimated
at the daily timeframe and the equilibrium estimated at the weekly timeframe
shouldexhibitacoherentrelationship. Thisassumptionremainsanunresolved
open hypothesis. V2 addresses Assumption 1.4 directly via the latent-state
Kalman framing. Assumptions 1.2 and 1.3 remain open working hypotheses;
themulti-timeframehierarchyisdeferredpendingsingle-timeframevalidation
(Section 13).
Assumption 1.4 (Direct Estimability):
𝜇∗
isestimableasalatentstatefrom
𝑡
observed prices and volumes using a linear state-space model. V2 addresses
this assumption directly via the Kalman framing — the latent state is tracked
with explicit uncertainty quantification.
Assumption 1.5 (Gaussian Noise): State and observation noise are Gaus-
sian. This assumption is standard and computationally convenient. It is vio-
lated during structural breaks and in markets with significant microstructure
effects. Robustness under non-Gaussianity is a deferred research direction
(Appendix B.2).
1.5 Three Structural Difficulties
Beyond these assumptions, three structural difficulties make equilibrium esti-
mation genuinely hard.
Difficulty 1 — Regime dependence:
𝜇∗
is only interpretable as an equilib-
𝑡
riumwhenthemarketisactuallymeanreverting. Duringtrendingregimes,the
9

“equilibrium” estimated by any method is a moving statistical artefact, not an
economically meaningful level. The V2 DAG architecture resolves this during
the research and validation phase by establishing an independent regime en-
gine (RFI) that operates without any
𝜇∗
-derived inputs. In a production Phase
3+ environment, the question of whether MRScore-informed 𝑄 adjustment is
permissible would reintroduce a partial feedback, which is why the research
architecture explicitly forbids it during Phases 1–2.
Difficulty2—Observationalconfounding: Theobservedprice𝑃 issimulta-
𝑡
neouslythesignalbeingestimated(throughitsmeanreversionproperties)and
the noise source contaminating the estimate (through trend and microstruc-
ture components). No method cleanly separates these.
Difficulty 3 — Latency of equilibrium shifts: When
𝜇∗
shifts, there is an
𝑡
irreduciblelagproportionalto1/𝐾 (thesteady-stateKalmangainreciprocal),
∞
during which the filter tracks the old equilibrium level. This lag is not a defect
of the Kalman filter — it is a consequence of the optimal tradeoff between
noisefilteringandresponsivenesstogenuineshifts. Theconfidenceframework
𝜇
(Section 10.4) addresses this by degrading 𝐶 when CUSUM statistics build,
𝑡
providing advance warning of an impending shift before the binary flag fires.
Section 2 — Mathematical Foundations
2.1 Stationarity Prerequisites
Let 𝑃 denote the log price at time 𝑡. The framework requires that the devia-
𝑡
tion process 𝑑 = 𝑃 − 𝜇∗ is stationary (or at minimum mean-reverting with
𝑡 𝑡 𝑡
bounded variance) during mean reversion regimes. Formally, we require that
the autocorrelation function of 𝑑 decays at a geometric rate:
𝑡
Corr(𝑑 ,𝑑 ) ≤ 𝜙ℎ for some 𝜙 ∈ (0,1)
𝑡 𝑡+ℎ
Standard unit root tests (ADF, KPSS) provide evidence for or against this prop-
erty at the instrument level and form part of the RFI computation (Section 9).
The Ljung-Box test on Kalman normalised innovations provides a within-filter
check on whether the assumed dynamics are consistent with observed data.
10

| 2.2 The | Ornstein-Uhlenbeck |     |     | Process |     |     |     |     |     |
| ------- | ------------------ | --- | --- | ------- | --- | --- | --- | --- | --- |
The continuous-time theoretical framework is the Ornstein-Uhlenbeck (OU)
process:
𝜅(𝜇∗
|     |     |     |     | 𝑑𝑃 = | −𝑃  | )𝑑𝑡+𝜎𝑑𝑊 |     |     |     |
| --- | --- | --- | --- | ---- | --- | ------- | --- | --- | --- |
|     |     |     |     | 𝑡    |     | 𝑡       |     | 𝑡   |     |
0isthemeanreversionspeed,𝜇∗
| where𝜅 | >   |     |     |     |     |     | isthelong-runmean(heretreated |     |     |
| ------ | --- | --- | --- | --- | --- | --- | ----------------------------- | --- | --- |
as fixed for the continuous-time characterisation), and 𝑊 is a standard Brow-
𝑡
𝑃
nian motion. The OU process has the important property that 𝑡 is stationary
with:
𝜎2
|     |     |     |     | 𝔼[𝑃 ] = | 𝜇∗, | Var(𝑃 | ) = |     |     |
| --- | --- | --- | --- | ------- | --- | ----- | --- | --- | --- |
|     |     |     |     | 𝑡       |     |       | 𝑡   |     |     |
2𝜅
The half-life of the process — the expected time for a deviation to reduce by
half — is:
ln2
|     |     |     |     |     | ℎ   | =   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1/2 𝜅
Thisquantityprovidesintuitionforthemeanreversionspeedinpracticalterms:
𝜅 ≈ 0.069
| a half-life | of  | 10 trading |     | days corresponds |     | to  |     | per | day. |
| ----------- | --- | ---------- | --- | ---------------- | --- | --- | --- | --- | ---- |
2.3 Discrete-Time Approximation and the Near-Unit-Root Problem
| The Euler-Maruyama |         |     | discretisation             |          | of  | the OU | process | gives:    |     |
| ------------------ | ------- | --- | -------------------------- | -------- | --- | ------ | ------- | --------- | --- |
|                    |         | 𝑃   | = 𝜌𝑃                       | +(1−𝜌)𝜇∗ |     | +𝜀     | , 𝜀     | ∼ 𝑁(0,𝜎2) |     |
|                    |         |     | 𝑡                          | 𝑡−1      |     |        | 𝑡       | 𝑡         | 𝜀   |
| where𝜌             | = 𝑒−𝜅Δ𝑡 |     | ∈ (0,1)andΔ𝑡isthetimestep. |          |     |        |         |           |     |
InthisAR(1)representation,
| 𝜌   |     |     |     |     |     |     | 𝜌 → | 1,  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
is the mean reversion parameter. When the process approaches a
| random | walk. |     |     |     |     |     |     |     |     |
| ------ | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
Thenear-unit-rootproblemiscriticaltounderstand. ForliquidequitiesandFX
pairs at daily frequency, instruments that exhibit mean reversion over multi-
week horizons typically have 𝜌 in the range [0.95,0.99]. At 𝜌 = 0.99, the
| equilibrium-implied |     |     | estimate | of 𝜇∗ | is: |     |     |     |     |
| ------------------- | --- | --- | -------- | ----- | --- | --- | --- | --- | --- |
𝛼̂
𝜇∗̂
=
|     |     |     |     |     | 𝑂𝑈  | 1−𝜌̂ |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
11

|     | 𝛼̂  | 𝜌̂are |     |     |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
where and OLS estimates from the AR(1) regression. The asymptotic
| variance | of  | this estimate |     | is approximately: |     |     |     |     |     |
| -------- | --- | ------------- | --- | ----------------- | --- | --- | --- | --- | --- |
𝜎2
|     |     |     |     | Var(𝜇∗̂ |     | ) ≈     | 𝜀   |     |     |
| --- | --- | --- | --- | ------- | --- | ------- | --- | --- | --- |
|     |     |     |     |         | 𝑂𝑈  | 𝑛(1−𝜌)2 |     |     |     |
At𝜌 = 0.99and𝑛 = 60,thisvarianceis10,000timeslargerthantheinnovation
| variance𝜎2 |     | TheOU-impliedestimateof𝜇∗ |     |     |     |     |                                    |     |     |
| ---------- | --- | ------------------------- | --- | --- | --- | --- | ---------------------------------- | --- | --- |
|            | 𝜀   | .                         |     |     |     |     | iseffectivelyuninformativeinfinite |     |     |
samples for near-unit-root processes. This instability is the primary reason
OU-implied equilibrium is excluded from the confidence framework (Section
𝜇
10.4) — including it would degrade 𝐶 precisely when the Kalman filter is
𝑡
| most valuable   |     | relative    | to  | simpler | alternatives. |     |     |     |     |
| --------------- | --- | ----------- | --- | ------- | ------------- | --- | --- | --- | --- |
| 2.4 State-Space |     | Formulation |     |         |               |     |     |     |     |
The Anchored Kalman framework is specified as a linear Gaussian state-space
𝜇∗
model. The state variable is 𝑡 , modelled as a latent mean-reverting process.
𝑃
| The observation |     | is  | .   |     |     |     |     |     |     |
| --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝑡
| State       | equation | (transition |     | model):      |      |          |           |            |       |
| ----------- | -------- | ----------- | --- | ------------ | ---- | -------- | --------- | ---------- | ----- |
|             |          | 𝜇∗ = 𝜌𝜇∗    |     | +(1−𝜌)𝜇      |      |          | +𝜂 ,      | 𝜂 ∼ 𝑁(0,𝑄) | (4.1) |
|             |          | 𝑡           | 𝑡−1 |              |      | anchor,𝑡 | 𝑡         | 𝑡          |       |
| Observation |          | equation    |     | (measurement |      | model):  |           |            |       |
|             |          |             | 𝑃   | = 𝜇∗         | +𝜀 , | 𝜀        | ∼ 𝑁(0,𝐷2) |            | (4.2) |
|             |          |             |     | 𝑡 𝑡          | 𝑡    | 𝑡        |           |            |       |
𝜇∗
The state equation says that 𝑡 follows a mean-reverting process with pull-
| speed𝜌towardtheanchorlevel𝜇 |     |     |     |     |     | Thenoise𝑄allows𝜇∗ |     |     |     |
| --------------------------- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- |
. todeviatefrom
anchor,𝑡 𝑡
this mean-reverting path, accommodating gradual shifts in equilibrium. The
observation equation says that the observed price 𝑃 is the latent equilibrium
𝑡
𝐷2
| plus observation |     | noise |     | .   |     |     |     |     |     |
| ---------------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
{𝜌,𝑄,𝐷2}.
Three parameters require estimation: This is discussed in Section
| 4.7 and | the | constrained |     | estimator | arm | in Section |     | 4.8. |     |
| ------- | --- | ----------- | --- | --------- | --- | ---------- | --- | ---- | --- |
2.5 Unobserved Component Model and Misspecification Implications
Thestate-spacemodelbelongstotheclassofunobservedcomponent(UC)mod-
els. A key result is that the optimal linear filter for such a model — the Kalman
12

filter — is equivalent in its steady-state behaviour to an ARMA(1,1) filter ap-
| plied | to  | 𝑃 : |     |     |     |     |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝑡
𝜇̂
Proposition 2.1: The Kalman-filtered equilibrium estimate satisfies, at
𝑡|𝑡
steady state:
|     |     |     |     | 𝜇̂  | = (1−𝐾 |     | )𝜇̂ | +𝐾      | 𝑃   |     |
| --- | --- | --- | --- | --- | ------ | --- | --- | ------- | --- | --- |
|     |     |     |     |     | 𝑡|𝑡    |     | ∞   | 𝑡−1|𝑡−1 | ∞ 𝑡 |     |
where 𝐾 is the steady-state Kalman gain. This has the structure of an expo-
∞
nentially weighted moving average with smoothing parameter 𝐾 .
∞
A misspecification note: the AR(1) observation model is mildly misspecified
if the true price process has an MA component, as is common due to bid-ask
bounce and microstructure effects. The true UC model has an ARMA(1,1) re-
duced form. OLS applied to the AR(1) representation is consistent but the
𝜇̂
omitted MA component adds variance to — it does not introduce bias.
𝑡|𝑡
| 2.6 | The | Kalman | Filter |     | Recursions |     |     |     |     |     |
| --- | --- | ------ | ------ | --- | ---------- | --- | --- | --- | --- | --- |
Given the state-space formulation, the Kalman filter computes the optimal lin-
𝜇∗
| ear | unbiased | estimator |     |     | of  | given | all observations |     | through 𝑡. |     |
| --- | -------- | --------- | --- | --- | --- | ----- | ---------------- | --- | ---------- | --- |
𝑡
| Prediction |     | step | (prior): |       |       |         |     |         |          |     |
| ---------- | --- | ---- | -------- | ----- | ----- | ------- | --- | ------- | -------- | --- |
|            |     |      |          | 𝜇̂    | =     | 𝜌𝜇̂     |     | +(1−𝜌)𝜇 |          |     |
|            |     |      |          | 𝑡|𝑡−1 |       | 𝑡−1|𝑡−1 |     |         | anchor,𝑡 |     |
|            |     |      |          |       | 𝑃     | =       | 𝜌2𝑃 | +𝑄      |          |     |
|            |     |      |          |       | 𝑡|𝑡−1 |         |     | 𝑡−1|𝑡−1 |          |     |
Innovation:
|        |     |                   |     |       |     |      |       | +𝐷2, |          | /√𝑆     |
| ------ | --- | ----------------- | --- | ----- | --- | ---- | ----- | ---- | -------- | ------- |
|        |     | 𝜈 =               | 𝑃   | −𝜇̂   | ,   | 𝑆    | = 𝑃   |      | 𝜁 = 𝜈    |         |
|        |     | 𝑡                 | 𝑡   | 𝑡|𝑡−1 |     | 𝑡    | 𝑡|𝑡−1 |      | 𝑡 𝑡      | 𝑡       |
| Update |     | step (posterior): |     |       |     |      |       |      |          |         |
|        | 𝐾   | = 𝑃               | /𝑆  | ,     | 𝜇̂  | = 𝜇̂ | +𝐾    | 𝜈 ,  | 𝑃 = (1−𝐾 | )𝑃      |
|        |     | 𝑡 𝑡|𝑡−1           |     | 𝑡     | 𝑡|𝑡 |      | 𝑡|𝑡−1 | 𝑡 𝑡  | 𝑡|𝑡      | 𝑡 𝑡|𝑡−1 |
The normalised innovation 𝜁 is the key diagnostic quantity. Under correct
𝑡
| model | specification |     |     | and | stationarity: |     | 𝜁   | ∼ iid𝑁(0,1). |     |     |
| ----- | ------------- | --- | --- | --- | ------------- | --- | --- | ------------ | --- | --- |
𝑡
Steady-state: The recursion for 𝑃 converges to a fixed point 𝑃 satisfying:
|     |     |     |     |     |     |     | 𝑡|𝑡 |     |     | ∞   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
13

|     |     | 𝑄−(1−𝜌2)𝐷2 |     | +√[𝑄−(1−𝜌2)𝐷2]2 |     | +4𝑄𝐷2 |        |
| --- | --- | ---------- | --- | --------------- | --- | ----- | ------ |
|     | 𝑃   | =          |     |                 |     |       | (4.15) |
∞
2
{𝜌,𝑄,𝐷2}
| Parameter |     | calibration | context: | Parameters |     | are estimated | by  |
| --------- | --- | ----------- | -------- | ---------- | --- | ------------- | --- |
MLE against the prediction error decomposition likelihood on a rolling 60-day
window. If Simulation Study 1 finds that the unconstrained MLE produces
𝜎(𝜌)̂ > 0.05 in simulation, the constrained estimator — with 𝜌 fixed at a cross-
|     |     | 𝜌   | {𝑄,𝐷2} |     |     |     |     |
| --- | --- | --- | ------ | --- | --- | --- | --- |
instrument prior 0 and estimated freely — becomes the default. The
| constrained |     | estimator | is specified | in Section | 4.7. |     |     |
| ----------- | --- | --------- | ------------ | ---------- | ---- | --- | --- |
| Section     | 3   | — Why     | Existing     | Methods    | Fail |     |     |
Before specifying the Anchored Kalman estimator, it is useful to characterise
precisely why the two most common alternatives — rolling means and expo-
nentiallyweightedmovingaverages—areinadequateforthisapplication, and
why the OU-implied estimate fails empirically despite its theoretical appeal.
| 3.1 Rolling       |     | Mean      |              |             |                                |     |     |
| ----------------- | --- | --------- | ------------ | ----------- | ------------------------------ | --- | --- |
| Therollingmean𝜇𝑅̂ |     |           | 𝑀            | 𝑤−1         |                                |     |     |
|                   |     |           | = (1/𝑤)∑     | 𝑃           | isthemostwidelyusedequilibrium |     |     |
|                   |     |           | 𝑡            | 𝑖=0         | 𝑡−𝑖                            |     |     |
| estimate          | in  | practice. | It has three | fundamental | deficiencies.                  |     |     |
Trend contamination: During the window preceding a mean reversion sig-
nal, the price has typically moved away from equilibrium. The rolling mean,
which averages all prices in the window, is contaminated by exactly the trend-
ing period that preceded the reversion candidate. The estimated equilibrium
is pulled toward the trended price, systematically understating the deviation.
No uncertainty quantification: The rolling mean provides a point estimate
with no associated uncertainty. The framework cannot distinguish between a
reliable equilibrium estimate and an unreliable one. All equilibrium estimates
| receive | equal | operational | weight | regardless | of filter | state. |     |
| ------- | ----- | ----------- | ------ | ---------- | --------- | ------ | --- |
Endpoint sensitivity: The rolling mean is maximally sensitive to the oldest
observation in the window, which drops off discontinuously after 𝑤 bars. This
createsartificialdiscontinuitiesintheequilibriumestimatethatarepurelyarte-
| facts of | the | window | boundary. |     |     |     |     |
| -------- | --- | ------ | --------- | --- | --- | --- | --- |
14

| 3.2       | Exponential |     | Moving   |     | Average |     |     |     |     |     |
| --------- | ----------- | --- | -------- | --- | ------- | --- | --- | --- | --- | --- |
| TheEMA𝜇𝐸̂ |             | 𝑀𝐴  | = (1−𝜆)𝑃 |     | +𝜆𝜇𝐸̂   | 𝑀𝐴  |     |     |     |     |
improvesontherollingmeanbyeliminat-
|     |     | 𝑡   |     |     | 𝑡   | 𝑡−1 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ing the endpoint discontinuity. It remains deficient on two critical dimensions.
𝜆
Arbitrary parameterisation: The smoothing parameter is typically chosen
onadhocgrounds. Thereisnoprincipledderivationofthecorrect𝜆foragiven
instrument and regime. In contrast, the Kalman filter derives the optimal gain
| 𝐾   | from | the structural |     | parameters |     | {𝜌,𝑄,𝐷2} |     | estimated | by MLE. |     |
| --- | ---- | -------------- | --- | ---------- | --- | -------- | --- | --------- | ------- | --- |
𝑡
No uncertainty quantification: Like the rolling mean, the EMA provides
no uncertainty estimate. It is, as established in Proposition 2.1, the Kalman
filter at steady state — but without the Kalman filter’s machinery for tracking
uncertaintyduringnon-steady-stateperiods,orfordegradingconfidencewhen
| model |            | assumptions |             | are violated. |     |     |     |     |     |     |
| ----- | ---------- | ----------- | ----------- | ------------- | --- | --- | --- | --- | --- | --- |
| 3.3   | OU-Implied |             | Equilibrium |               |     |     |     |     |     |     |
𝜇∗
The theoretically motivated alternative is to estimate from the AR(1) fixed
point as described in Section 2.3. Despite its theoretical connection to the
mean reversion model, this estimator is empirically unreliable for the reason
|     |     |     |     |     |     |     |     | 𝜌 = 0.99, |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- |
established there: near-unit-root instability. At the estimation vari-
|             |     | 𝜇∗̂      |     |       |               |     | 10,000×𝜎2 |     |           |              |
| ----------- | --- | -------- | --- | ----- | ------------- | --- | --------- | --- | --------- | ------------ |
| ance        | of  | at       | 𝑛 = | 60 is | approximately |     |           | —   | rendering | the estimate |
|             |     | 𝑂𝑈       |     |       |               |     |           | 𝜀   |           |              |
| practically |     | useless. |     |       |               |     |           |     |           |              |
TheOU-impliedestimatedoeshavearoleintheframework, butnotasanequi-
OU-implied𝜇∗
librium estimator: it serves as a diagnostic. When the is reason-
ably stable across rolling windows, it provides weak corroborating evidence
| that    | the        | Anchored | Kalman |          | estimate | is in      | a credible | range. |     |     |
| ------- | ---------- | -------- | ------ | -------- | -------- | ---------- | ---------- | ------ | --- | --- |
| Section |            | 4 —      | The    | Anchored |          | Kalman     | Estimator  |        |     |     |
| 4.1     | Motivation |          | and    | Design   |          | Objectives |            |        |     |     |
TheAnchoredKalmanestimatorisdesignedtosatisfyfourrequirementssimul-
taneously:
|     | 1. Optimality |     | under | the | assumed | state-space |     | model. |     |     |
| --- | ------------- | --- | ----- | --- | ------- | ----------- | --- | ------ | --- | --- |
2. Uncertainty quantification — tracking the posterior variance 𝑃 .
𝑡|𝑡
3. Anti-drift — preventing the estimate from drifting arbitrarily far from an
|     | economically |     | grounded |     | anchor. |     |     |     |     |     |
| --- | ------------ | --- | -------- | --- | ------- | --- | --- | --- | --- | --- |
15

4. Break detection compatibility — maintaining filter warmth during sus-
| pension | periods. |     |     |     |     |     |     |     |     |
| ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
No existing simple estimator satisfies all four. The rolling mean and EMA sat-
isfy none.
| 4.2 Full Model | Specification |             |     |                |     |     |     |     |     |
| -------------- | ------------- | ----------- | --- | -------------- | --- | --- | --- | --- | --- |
| The complete   | model         | is restated |     | for reference: |     |     |     |     |     |
State equation:
|             |           | 𝜇∗  | = 𝜌𝜇∗ | +(1−𝜌)𝜇 |       |          |     | +𝜂  | (4.1) |
| ----------- | --------- | --- | ----- | ------- | ----- | -------- | --- | --- | ----- |
|             |           | 𝑡   |       | 𝑡−1     |       | anchor,𝑡 |     | 𝑡   |       |
| Observation | equation: |     |       |         |       |          |     |     |       |
|             |           |     |       | 𝑃 =     | 𝜇∗ +𝜀 |          |     |     | (4.2) |
|             |           |     |       | 𝑡       | 𝑡     | 𝑡        |     |     |       |
Noise assumptions:
|     | 𝜂   | ∼ 𝑁(0,𝑄), |     | 𝜀 ∼ 𝑁(0,𝐷2), |     |     | Cov(𝜂 | ,𝜀 ) = 0 | (4.3) |
| --- | --- | --------- | --- | ------------ | --- | --- | ----- | -------- | ----- |
|     | 𝑡   |           |     | 𝑡            |     |     |       | 𝑡 𝑡      |       |
Anchor:
|     |     | 𝜇        |     | = VWAP(𝑃 |         |     | , 𝑉     | )   | (4.4) |
| --- | --- | -------- | --- | -------- | ------- | --- | ------- | --- | ----- |
|     |     | anchor,𝑡 |     |          | 𝑡−𝑤+1∶𝑡 |     | 𝑡−𝑤+1∶𝑡 |     |       |
where VWAP is the volume-weighted average price over the anchor window of
| 𝑤,  | 𝑉   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
length and denotes trading volume. When exchange-reported volume is
unavailable, 𝜇 falls back to the arithmetic mean over the anchor window.
anchor
This fallback must be flagged at the instrument level; see the data validation
| protocol in | Section | 12.0. |     |     |     |     |     |     |     |
| ----------- | ------- | ----- | --- | --- | --- | --- | --- | --- | --- |
{𝜌,𝑄,𝐷2}.
| Parameters       | to estimate: |        | 𝜃   | =       |          |     |               |     |     |
| ---------------- | ------------ | ------ | --- | ------- | -------- | --- | ------------- | --- | --- |
| 4.3 The Long-Run |              | Anchor |     | and Its | Economic |     | Justification |     |     |
The anchor 𝜇 is the defining feature that distinguishes this from a stan-
anchor,𝑡
dard Kalman filter. VWAP is not merely a technical indicator — it is the re-
alised volume-weighted transaction price over the anchor window. Institu-
tionaltradersroutinelyuseVWAPasabenchmark; ordersthatsignificantlyde-
16

viate from VWAP attract arbitrage and reversion flows from benchmark-aware
participants.
𝑤
The anchor window length is set to correspond to a recognised institutional
planning horizon — one that reflects the cadence at which institutional partic-
ipants evaluate performance and adjust positioning. Starting values for 𝑤 by
| timeframe | are: |            |              |      |           |                |      |
| --------- | ---- | ---------- | ------------ | ---- | --------- | -------------- | ---- |
| Timeframe |      | Anchor     | Window       |      | Starting  | Rationale      |      |
| Daily     | bars | 65 trading | days         | (~13 | One       | fiscal quarter | —    |
|           |      | weeks)     |              |      | standard  | institutional  |      |
|           |      |            |              |      | benchmark | period         |      |
| Weekly    | bars | 52 weeks   |              |      | One       | benchmark      | year |
| 4-hour    | bars | ~30 bars   | (~1 calendar |      | Standard  | option         |      |
|           |      | month)     |              |      | expiry    | cycle          |      |
Theseanchorwindowsrepresentstartingassumptionsgroundedinobservable
institutional behaviour, not universally optimal values. The appropriate win-
dow length for a given instrument and regime is assessed in Experiment 1a.
| 4.4 The | Anti-Drift Guarantee |     |     |     |     |     |     |
| ------- | -------------------- | --- | --- | --- | --- | --- | --- |
Underconstant𝜇
| Theorem | 4.2 (Anti-Drift): |     |     |     | , thestationarydistribution |     |     |
| ------- | ----------------- | --- | --- | --- | --------------------------- | --- | --- |
anchor
|                  |     | 𝜇∗       |          |       |          | 𝑄/(1−𝜌2). |     |
| ---------------- | --- | -------- | -------- | ----- | -------- | --------- | --- |
| of the deviation | 𝑑 = | −𝜇       | has mean | 0 and | variance |           |     |
|                  | 𝑡   | 𝑡 anchor |          |       |          |           |     |
|                  |     |          | 𝑑 =      | 𝜌𝑑    | + 𝜂      |           |     |
Proof sketch: From equation (4.1), . This is an AR(1) process
|     |     |     | 𝑡   | 𝑡−1 | 𝑡   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
with |𝜌| < 1, hence stationary. The stationary variance follows directly. □
Remark4.3(MovingAnchorQualification): Theorem4.2characterisesthe
| stationarydistributionof(𝜇 |     | −𝜇  | )underaconstantanchor. |     |     | When𝜇 |          |
| -------------------------- | --- | --- | ---------------------- | --- | --- | ----- | -------- |
|                            |     | 𝑡   | anchor                 |     |     |       | anchor,𝑡 |
drifts continuously — as during sustained trends spanning the anchor window
— the bound applies to the deviation from the current anchor level, not from
𝜇̂
a fixed reference. The anti-drift mechanism remains operative: is always
𝑡|𝑡
𝜇
pulled toward . However, if the anchor itself is trending, the long-run
anchor,𝑡
expected deviation from any fixed price level may exceed the stated bound.
Anchor stability can be monitored via the ratio |𝜇 − 𝜇 |/𝜎 . A
|     |     |     |     |     | anchor,𝑡 | anchor,𝑡−20 | 𝑡   |
| --- | --- | --- | --- | --- | -------- | ----------- | --- |
materially elevated ratio — indicative of anchor drift on the order of one stan-
dard deviation per 20 bars — warrants cautious interpretation of the anti-drift
| guarantee. | This monitoring | is  | a diagnostic, | not | a hard gate. |     |     |
| ---------- | --------------- | --- | ------------- | --- | ------------ | --- | --- |
17

| 4.5 Kalman | Recursions |     |     | (Operational) |     |     |     |     |     |     |     |
| ---------- | ---------- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
𝑡,
The per-bar execution order is fixed and non-negotiable. On each bar the
| following | steps | are performed |     |     | in sequence: |     |     |     |     |     |     |
| --------- | ----- | ------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- |
𝑃
| Step | 1 — Prediction |     | (prior | state, | before | observing |     | ):  |     |     |     |
| ---- | -------------- | --- | ------ | ------ | ------ | --------- | --- | --- | --- | --- | --- |
𝑡
|     |     |     | 𝜇̂    | = 𝜌𝜇̂ |         | +(1−𝜌)𝜇 |     |          |     |     |       |
| --- | --- | --- | ----- | ----- | ------- | ------- | --- | -------- | --- | --- | ----- |
|     |     |     | 𝑡|𝑡−1 |       | 𝑡−1|𝑡−1 |         |     | anchor,𝑡 |     |     | (4.6) |
𝜌2𝑃
|      |             |     |             | 𝑃     | =          |         | +𝑄  |              |     |     | (4.7) |
| ---- | ----------- | --- | ----------- | ----- | ---------- | ------- | --- | ------------ | --- | --- | ----- |
|      |             |     |             | 𝑡|𝑡−1 |            | 𝑡−1|𝑡−1 |     |              |     |     |       |
| Step | 2 — Observe |     | 𝑃 . Compute |       | innovation |         | and | diagnostics: |     |     |       |
𝑡
|     |     |     |     |     | 𝜈 = 𝑃   | −𝜇̂   |     |     |     |     | (4.8) |
| --- | --- | --- | --- | --- | ------- | ----- | --- | --- | --- | --- | ----- |
|     |     |     |     |     | 𝑡 𝑡     | 𝑡|𝑡−1 |     |     |     |     |       |
|     |     |     |     | 𝑆   | = 𝑃     | +𝐷2   |     |     |     |     | (4.9) |
|     |     |     |     |     | 𝑡 𝑡|𝑡−1 |       |     |     |     |     |       |
|     |     |     |     |     | 𝜁 = 𝜈   | /√𝑆   |     |     |     |     |       |
(4.10)
|      |            |            |     |         | 𝑡     | 𝑡   | 𝑡   |     |     |     |     |
| ---- | ---------- | ---------- | --- | ------- | ----- | --- | --- | --- | --- | --- | --- |
| Step | 3 — Update | (posterior |     | state): |       |     |     |     |     |     |     |
|      |            |            |     |         | 𝐾 = 𝑃 |     | /𝑆  |     |     |     |     |
(4.11)
|     |     |     |     |     | 𝑡      | 𝑡|𝑡−1 | 𝑡   |     |     |     |        |
| --- | --- | --- | --- | --- | ------ | ----- | --- | --- | --- | --- | ------ |
|     |     |     |     | 𝜇̂  | = 𝜇̂   | +𝐾    | 𝜈   |     |     |     | (4.12) |
|     |     |     |     | 𝑡|𝑡 | 𝑡|𝑡−1  |       | 𝑡   | 𝑡   |     |     |        |
|     |     |     |     | 𝑃   | = (1−𝐾 | )𝑃    |     |     |     |     |        |
(4.13)
|     |     |     |     | 𝑡|𝑡 |     | 𝑡   | 𝑡|𝑡−1 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
𝜁
Step 4 — CUSUM update (applied to the innovation from Step 2):
𝑡
|        |       | +   |     |       | −   |           |     |              |     |          |     |
| ------ | ----- | --- | --- | ----- | --- | --------- | --- | ------------ | --- | -------- | --- |
| Update | CUSUM |     | and | CUSUM | per | equations |     | (6.1)–(6.2). |     | Evaluate |     |
|        |       | 𝑡   |     |       | 𝑡   |           |     |              |     |          |     |
= 1,
| break_flag | .   | Update | suspended |     | accordingly. |     |     | If break_flag |     |     | set |
| ---------- | --- | ------ | --------- | --- | ------------ | --- | --- | ------------- | --- | --- | --- |
|            | 𝑡   |        |           |     | 𝑡            |     |     |               | 𝑡   |     |     |
suspended = 1 and record the break bar for the 20-bar deferral clock.
𝑡
| CUSUM | counters | reset | to  | zero | on flag. |     |     |     |     |     |     |
| ----- | -------- | ----- | --- | ---- | -------- | --- | --- | --- | --- | --- | --- |
MLE re-estimation executes asynchronously — it does not block the per-bar
filter execution. When the 20-bar deferral period has elapsed and recovery
conditions (Section 6.5) are met, the re-estimation result is loaded at the next
18

natural re-estimation interval. The filter continues running with held parame-
| ters until | then. |          |     |     |     |     |     |     |     |     |     |
| ---------- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|            |       | (𝑡 = 0): |     |     |     |     |     |     |     |     |     |
Initialisation
|     | 𝜇̂  | = 𝜇          |     | ,   | 𝑃   | = 𝑃 | = 𝑄/max(1−𝜌2, |     | 0.01) |     |       |
| --- | --- | ------------ | --- | --- | --- | --- | ------------- | --- | ----- | --- | ----- |
|     |     | 0|0 anchor,0 |     |     | 0|0 | 0   |               |     |       |     | (4.5) |
𝜌2,0.01)
The 𝑃 floor at max(1 − prevents numerical conditioning issues that
0
arise when 𝜌 is estimated near 1, while remaining effectively non-informative.
|     |     |     |     | ≈   | 1/𝐾 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Filter outputs during the first ∞ bars should be treated as burn-in and
|               |     | 𝐶 𝜇 < | 1   |      |     |     |     |     |     |     |     |
| ------------- | --- | ----- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
| are reflected |     | in    | via | conf | .   |     |     |     |     |     |     |
|               |     | 𝑡     |     |      | 𝑈,𝑡 |     |     |     |     |     |     |
Implementation constraint: The Kalman filter executes unconditionally on
𝑉
every bar, regardless of the validity gate 𝑡 . The filter must remain warm dur-
|     |     | 𝑃   | 𝜁   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ing suspension — , , and CUSUM statistics computed during suspension
|     |     | 𝑡|𝑡 | 𝑡   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
are required inputs to the recovery assessment and to the confidence score.
| 4.6 Steady-State |     | Properties |     |     |     |     |     |     |     |     |     |
| ---------------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The Riccati recursion (4.7) converges to the unique positive fixed point 𝑃
∞
satisfying equation (4.15). The steady-state gain 𝐾 = 𝑃 /(𝑃 + 𝐷2) con-
|     |     |     |     |     |     |     |     | ∞   | ∞ ∞ |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝑄/𝐷2
trols the filter’s long-run responsiveness. The ratio is the fundamental
𝑄/𝐷2
tradeoff parameter: a large ratio implies the equilibrium moves quickly
𝑄/𝐷2
relative to noise (high 𝐾 , responsive); a small implies a stable equilib-
∞
| rium relative |     | to noise | (low | 𝐾 , | smooth). |     |     |     |     |     |     |
| ------------- | --- | -------- | ---- | --- | -------- | --- | --- | --- | --- | --- | --- |
∞
| 4.7 Parameter |     | Calibration |     | and | the | Constrained |     | Estimator |     |     |     |
| ------------- | --- | ----------- | --- | --- | --- | ----------- | --- | --------- | --- | --- | --- |
{𝜌,𝑄,𝐷2}
| Parameters | 𝜃     | =              |     | are | estimated |     | by  | maximum | likelihood | using | the |
| ---------- | ----- | -------------- | --- | --- | --------- | --- | --- | ------- | ---------- | ----- | --- |
| prediction | error | decomposition: |     |     |           |     |     |         |            |       |     |
𝑇
|     |     |      |     | 𝑇       |     | 1   |       |       |     |     |     |
| --- | --- | ---- | --- | ------- | --- | --- | ----- | ----- | --- | --- | --- |
|     |     | ℓ(𝜃) | = − | ln(2𝜋)− |     |     | ∑[ln𝑆 | +𝜈2/𝑆 | ]   |     |     |
(4.16)
|     |     |     |     | 2   |     | 2   |     | 𝑡   | 𝑡 𝑡 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝑡=1
Estimationusesarollingwindowofthelast60tradingdays,withre-estimation
| every 5 trading |     | days.      |     |     |     |     |                   |     |     |         |     |
| --------------- | --- | ---------- | --- | --- | --- | --- | ----------------- | --- | --- | ------- | --- |
|                 |     |            |     | 𝑛   | =   | 60, |                   |     |     |         |     |
| Constrained     |     | estimator: |     | At  |     |     | the unconstrained |     | MLE | surface | for |
{𝜌,𝑄,𝐷2}
is poorly conditioned for near-unit-root processes: the likelihood
is relatively flat with respect to 𝜌, and the cross-partial derivatives between
𝜌 and 𝑄 are large. Simulation Study 1 assesses whether this identification
19

|     |     |     |     |     |     |     |     |     | (𝜎(𝜌)̂ | > 0.05 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | ------ | --- |
problem is severe enough to require constraint. If it is at target
𝜌 values), the constrained estimator is adopted as the production default: 𝜌
is fixed at a cross-instrument prior 𝜌 , and {𝑄,𝐷2} are estimated by MLE on
0
| the | rolling | window. |     |     |     |     |     |     |     |     |     |
| --- | ------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The prior 𝜌 is drawn from the empirically observed range of mean reversion
0
persistence in near-unit-root daily equity and FX processes. Mean reversion
half-lives in this asset class typically fall in the 10–30 trading day range, corre-
sponding to 𝜌 ∈ [0.95,0.99] at daily frequency. A central value of 𝜌 = 0.97 is
0
used as the starting assumption, corresponding to a half-life of approximately
23 trading days. This is not presented as a universal constant. It is an empiri-
cally motivated starting value within a defensible range — one that Simulation
Study 1 will assess against instrument-specific data, and that may be revised
instrument-by-instrument if evidence warrants. The constrained estimator’s
|     |     |     |     | 𝜌   | ∈ (0,1); |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
logic is valid for any fixed 0 the specific value affects pull-speed
toward the anchor but leaves the anti-drift property and the architectural in-
| dependence      |                           |        | intact.               |                |                            |           |        |             |             |     |             |
| --------------- | ------------------------- | ------ | --------------------- | -------------- | -------------------------- | --------- | ------ | ----------- | ----------- | --- | ----------- |
|                 |                           |        | 𝑃 = 𝑄/max(1−𝜌2,0.01), |                |                            |           |        |             |             |     |             |
| Initialisation: |                           |        | 0                     |                |                            |           | as     | specified   | in equation |     | (4.5).      |
| 4.8             | Volume                    |        | Availability          | and            | the PSEUDO_ANCHORED_KALMAN |           |        |             |             |     | Flag        |
| Two             | instrument                |        | types are             | distinguished: |                            |           |        |             |             |     |             |
|                 | • ANCHORED_KALMAN:        |        |                       |                | Exchange                   |           | volume | available   |             | and | validated.  |
|                 | VWAP                      | anchor | used.                 | Primary        | DRC                        | advantage |        | claim       | applies.    |     |             |
|                 | • PSEUDO_ANCHORED_KALMAN: |        |                       |                |                            |           | Volume | unavailable |             | or  | unreliable. |
Arithmetic mean anchor used. Results reported separately and excluded
|     | from | the | primary | DRC advantage |     | claim. |     |     |     |     |     |
| --- | ---- | --- | ------- | ------------- | --- | ------ | --- | --- | --- | --- | --- |
Silent degradation from VWAP to arithmetic mean is not acceptable — it invali-
dates the primary theoretical justification without flagging the contamination.
| Section |     | 5 —      | Candidate | Equilibrium |            |     | Methods |     |     |     |     |
| ------- | --- | -------- | --------- | ----------- | ---------- | --- | ------- | --- | --- | --- | --- |
| 5.1     | The | Anchored | Kalman    |             | as Primary |     | (Tier   | 1)  |     |     |     |
𝜇∗
The Anchored Kalman (AK) occupies Tier 1 unconditionally. When 𝑡 shifts,
1/𝐾
the Kalman filter’s response is delayed by approximately bars. This lag
∞
𝑄/𝐷2
is irreducible at the given ratio. This latency is the primary reason a
confidence score that degrades before a CUSUM flag fires is valuable — the
20

|         | factorin𝐶 |     | 𝜇                                      |     |     |     |     |           |
| ------- | --------- | --- | -------------------------------------- | --- | --- | --- | --- | --------- |
| conf    |           |     | beginsdecliningasCUSUMstatisticsbuild, |     |     |     |     | providing |
| CUSUM,𝑡 |           |     | 𝑡                                      |     |     |     |     |           |
a soft warning signal in the bars preceding a formal break detection.
| 5.2 VWAP | as  | Anchor | Validator | (Tier | 1 Support) |     |     |     |
| -------- | --- | ------ | --------- | ----- | ---------- | --- | --- | --- |
In addition to its role as the anchor for the Kalman filter, VWAP serves in-
dependently as a cross-reference equilibrium level. The economic justifica-
tion is distinct from its role as a statistical average: VWAP represents the
aggregate transacted price — the weighted average at which market partic-
ipants have actually exchanged the instrument. Persistent deviations of cur-
rent price from VWAP attract mean reversion flows from VWAP-benchmarked
| institutional | traders.   |     |         |             |     |     |     |     |
| ------------- | ---------- | --- | ------- | ----------- | --- | --- | --- | --- |
| 5.3 Point     | of Control |     | as Tier | 2 Component |     |     |     |     |
The Point of Control (POC) is the price level with maximum volume concentra-
tion over a specified look-back window, derived from the volume profile. The
POC is designated as a Tier 2 component: it is not included in the primary con-
fidence framework during Phases 1–2. The claim that Kalman-POC agreement
predicts subsequent DRC quality must be empirically validated before it can
| be operationalised. |     |             | Experiment | 5 provides    | this | validation. |     |     |
| ------------------- | --- | ----------- | ---------- | ------------- | ---- | ----------- | --- | --- |
| 5.4 OU-Implied      |     | Equilibrium |            | as Diagnostic |      | Only        |     |     |
𝜇∗̂
The OU-implied equilibrium is disqualified as a primary estimator due
𝑂𝑈
to near-unit-root instability (Section 2.3). Its retained role is as a qualitative
𝜇∗̂
diagnostic only. No quantitative weight is assigned to in any formula.
𝑂𝑈
| 5.5 EMA | as Fallback, |     | S/R | Eliminated |     |     |     |     |
| ------- | ------------ | --- | --- | ---------- | --- | --- | --- | --- |
EMA is the steady-state Kalman filter with suboptimal smoothing parameter
andnouncertaintyquantification. ItisretainedonlyifKalmaninfrastructureis
unavailable. Support/resistancemidpointsaresubjective,introducesignificant
lookahead risk in identification, and their economic content is subsumed by
| POC. They | are      | eliminated | from | the framework. |                   |     |            |        |
| --------- | -------- | ---------- | ---- | -------------- | ----------------- | --- | ---------- | ------ |
| Estimator | summary: |            |      |                |                   |     |            |        |
| Estimator |          |            | Tier | Status         |                   |     | Confidence | role   |
| Anchored  | Kalman   |            | 1    | Primary        |                   |     | Core       | input  |
| VWAP      |          |            | 1    | Anchor         | / cross-reference |     | None       | direct |
21

| Estimator     |     |           | Tier       |     | Status         |     |        |          |      | Confidence |             | role |
| ------------- | --- | --------- | ---------- | --- | -------------- | --- | ------ | -------- | ---- | ---------- | ----------- | ---- |
| POC           |     |           | 2          |     | Deferred       |     | (after | Exp.     | 5)   | Tier       | 2 only      |      |
| OU-implied    |     |           | –          |     | Diagnostic     |     | only   |          |      | None       |             |      |
| EMA           |     |           | Fallback   |     | Infrastructure |     |        | fallback | only | None       | (collapses) |      |
| S/R midpoints |     |           | –          |     | Eliminated     |     |        |          |      | –          |             |      |
| Section       | 6   | — The     | Controlled |     | Adaptation     |     |        | Problem  |      |            |             |      |
| 6.1 Formal    |     | Statement |            |     |                |     |        |          |      |            |             |      |
The adaptation problem is the tension at the heart of any online estimator:
the filter must be responsive enough to track genuine equilibrium shifts, yet
stable enough to resist noise-driven drift and false signals. In the context of
theAnchoredKalmanestimator, thistensionisparametric—itiscontrolledby
| the ratio | 𝑄/𝐷2 | .   |     |     |     |     |     |     |     |     |     |     |
| --------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝐷2
Definition 6.1 (Speed-Stability Tradeoff): For a given , increasing 𝑄
increases 𝐾 , making 𝜇̂ more responsive to recent prices. Decreasing 𝑄
|           |     | ∞          |     | 𝑡|𝑡 |              |     |     |     |     |     |     |     |
| --------- | --- | ---------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
|           | 𝐾   |            |     | 𝜇̂  |              |     |     |     |     |     |     |     |
| decreases |     | ∞ , making |     | 𝑡|𝑡 | more stable. |     |     |     |     |     |     |     |
𝑄/𝐷2
| 6.2 The |     | Ratio |     | as the | Primary |     | Adaptation |     | Diagnostic |     |     |     |
| ------- | --- | ----- | --- | ------ | ------- | --- | ---------- | --- | ---------- | --- | --- | --- |
Thenormalisedinnovation𝜁 providesthekeydiagnosticforwhetherthe𝑄/𝐷2
𝑡
𝜁 ∼ iid𝑁(0,1).
ratio is appropriately set. Under correct model specification:
𝑡
| Systematic |     | deviations |     | signal | misspecification: |        |     |          |       |     |          |     |
| ---------- | --- | ---------- | --- | ------ | ----------------- | ------ | --- | -------- | ----- | --- | -------- | --- |
| 𝔼[𝜁        | ] ≠ | 0:         |     |        |                   |        |     |          |       |     |          |     |
| •          |     | systematic |     | bias   | — the             | filter | is  | tracking | wrong | on  | average. |     |
𝑡
Var(𝜁2)
| •   |     | > 1 | consistently: |     | 𝑄 is | too | small | (filter | under-reacts). |     |     |     |
| --- | --- | --- | ------------- | --- | ---- | --- | ----- | ------- | -------------- | --- | --- | --- |
𝑡
Var(𝜁2)
| •   |     | < 1 | consistently: |     | 𝑄 is | too | large | (filter | over-reacts). |     |     |     |
| --- | --- | --- | ------------- | --- | ---- | --- | ----- | ------- | ------------- | --- | --- | --- |
𝑡
| Corr(𝜁       |     | ,𝜁    | ) > 0:   |            |             |     |       |                  |     |     |     |     |
| ------------ | --- | ----- | -------- | ---------- | ----------- | --- | ----- | ---------------- | --- | --- | --- | --- |
| •            |     | 𝑡 𝑡−1 |          | the        | observation |     | model | is misspecified. |     |     |     |     |
| 6.3 Adaptive |     | 𝑄     | Variants | (Deferred) |             |     |       |                  |     |     |     |     |
Three adaptive 𝑄 variants have been designed: exponentially weighted
| 𝑄   |     |     |     |     |     | 𝑄   |     |     |     |     |     | 𝑄   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(EWMA-based), regime-switching (two-state), and BOCD-triggered
(Bayesian Online Changepoint Detection). All three are deferred until the
base model (fixed MLE-estimated 𝑄) has been validated in Phase 1. All three
| variants | are | specified |     | in Appendix |     | B.1. |     |     |     |     |     |     |
| -------- | --- | --------- | --- | ----------- | --- | ---- | --- | --- | --- | --- | --- | --- |
22

| 6.4 The | Inflection-Point |     | Problem |     |     |     |     |     |     |
| ------- | ---------------- | --- | ------- | --- | --- | --- | --- | --- | --- |
When the market transitions between regimes, the Kalman filter’s response to
𝜇∗
a shift in is delayed by approximately 1/𝐾 bars. This delay is unavoidable
|     | 𝑡   |     |     |     |     | ∞   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
at fixed 𝐾 . Two mechanisms address this: the validity gate 𝑉 gates down-
∞ 𝑡
𝜇̂
stream use of 𝑡|𝑡 ; and the confidence score conf CUSUM,𝑡 degrades smoothly
as CUSUM statistics build, providing advance warning before the formal flag
fires.
| 6.5 CUSUM |     | Break Detection |     | and | the | Post-Break |     | Protocol |     |
| --------- | --- | --------------- | --- | --- | --- | ---------- | --- | -------- | --- |
Specification: The CUSUM detector applies the Page-Hinkley scheme to the
normalised innovation sequence {𝜁 }, where 𝜁 is the innovation from Step 2
|        |         |           |          |        | 𝑡     |     | 𝑡    |      |       |
| ------ | ------- | --------- | -------- | ------ | ----- | --- | ---- | ---- | ----- |
| of the | per-bar | execution | (Section | 4.5):  |       |     |      |      |       |
|        |         |           | +        |        |       |     | +    |      |       |
|        |         | CUSUM     | =        | max(0, | CUSUM |     | +𝜁   | −𝑘 ) | (6.1) |
|        |         |           | 𝑡        |        |       |     | 𝑡−1  | 𝑡 𝑐  |       |
|        |         |           | − =      | max(0, |       |     | − −𝜁 | −𝑘 ) |       |
|        |         | CUSUM     |          |        | CUSUM |     |      |      | (6.2) |
|        |         |           | 𝑡        |        |       |     | 𝑡−1  | 𝑡 𝑐  |       |
Defaultstartingparameters: 𝑘 = 0.5,ℎ = 5.0. Theseareempiricallymoti-
|     |     |     |     | 𝑐   |     | 𝑐   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
vatedstartingvalues,consistentwithstandardCUSUMpracticefornormalised
sequences. Experiment 7 provides instrument-specific calibration; these val-
ues should be treated as reasonable defaults pending that calibration, not as
| theoretically |       | exact parameters. |     |           |     |         |     |        |     |
| ------------- | ----- | ----------------- | --- | --------- | --- | ------- | --- | ------ | --- |
|               |       |                   | = 1 | max(CUSUM |     | +,CUSUM |     | −) > ℎ |     |
| Break         | flag: | break_flag        |     | if        |     | 𝑡       |     | 𝑡 𝑐 .  |     |
𝑡
Post-break protocol (V2.5 — replaces the V2 30-bar sub-window re-
estimation):
On flag: CUSUM counters reset to zero. suspended is set to 1. The Kalman
𝑡
filtercontinuesexecutingunconditionally(Step1throughStep4ofSection4.5
proceeds normally on every bar). MLE re-estimation is deferred until at least
20post-breakbarshaveelapsed,ensuringtheestimationwindowcontainspre-
dominantly post-break data. During the deferral period, parameters from the
lastpre-breakestimationareheld. Re-estimationexecutesasynchronouslyand
| does not | interrupt | per-bar | filter | execution. |     |     |     |     |     |
| -------- | --------- | ------- | ------ | ---------- | --- | --- | --- | --- | --- |
Cascade damping: If a second break_flag fires within 20 bars of the first, the
𝑡
CUSUM threshold is temporarily elevated — to a starting value of ℎ = 7.0,
𝑐
subject to empirical review in Experiment 7 — for the subsequent 20 bars. No
new re-estimation is triggered. This mechanism reduces the risk of oscillatory
23

false-flaggingduringgenuineregimetransitions,whenthemarketmayexhibit
several large consecutive innovations before settling under the new dynamics.
Recovery: suspended returnsto0whenallthreeofthefollowingindependent
𝑡
| conditions |     | are | met simultaneously: |     |     |     |     |     |     |     |
| ---------- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- |
1. At least 20 post-break bars have elapsed since the break flag.
2. Re-estimation has completed (MLE on the new post-break window has
converged).
|     |              |     | +,CUSUM |     | −)  |     |           |              |              |      |
| --- | ------------ | --- | ------- | --- | --- | --- | --------- | ------------ | ------------ | ---- |
|     | 3. max(CUSUM |     |         |     | <   | 0.5 | × ℎ       | . The factor | 0.5 requires | that |
|     |              |     | 𝑡       |     | 𝑡   |     | 𝑐,current |              |              |      |
CUSUM has returned to roughly half the detection threshold — indicat-
ing that the innovation sequence has genuinely stabilised — rather than
merely resetting to zero on a counter reset. This threshold is a starting
|     | value; | Experiment |     | 7   | may suggest |     | adjustment. |     |     |     |
| --- | ------ | ---------- | --- | --- | ----------- | --- | ----------- | --- | --- | --- |
False-positive rate: Under the asymptotic null (𝜁 ∼ 𝑁(0,1), correctly spec-
𝑡
ified model), the expected number of bars between false CUSUM flags with
| 𝑘   | = 0.5, | ℎ = | 5.0 |     |     |     |     |     |     |     |
| --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝑐 𝑐 is approximately 100. This approximation holds when inno-
vations are Gaussian and the model is correctly specified. In finite samples —
particularly during the first 60 bars of estimation — 𝜁 may have heavier tails
𝑡
due to parameter uncertainty, modestly increasing the false-positive rate. Ex-
periment 7 provides empirical calibration across the target instruments and
| estimation |      | conditions. |     |          |              |     |            |     |     |     |
| ---------- | ---- | ----------- | --- | -------- | ------------ | --- | ---------- | --- | --- | --- |
| Section    |      | 7 —         | The | Mean     | Clustering   |     | Hypothesis |     |     |     |
| 7.1        | The  | Ensemble    |     | Argument | (Compressed) |     |            |     |     |     |
|            | ( 1) | ( 2)        |     |          |              |     |            |     |     |     |
If 𝜇 ̂ and 𝜇 ̂ are unbiased estimates of 𝜇∗ with variances 𝜎2 and 𝜎2 and
|     | 𝑡   | 𝑡   |     |     |     |     |     | 𝑡   | 1   | 2   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝛾
correlation 12 , then the optimal weighted average has variance less than
| min(𝜎2,𝜎2)    |     |              | 𝛾   | <         | 𝜎 /𝜎            |         |          |           |          |         |
| ------------- | --- | ------------ | --- | --------- | --------------- | ------- | -------- | --------- | -------- | ------- |
|               |     | when         |     |           |                 | . The   | variance | reduction | requires | genuine |
|               | 1   | 2            |     | 12        | 1 2             |         |          |           |          |         |
| orthogonality |     | between      |     | the       | two estimators. |         |          |           |          |         |
| 7.2           | The | Independence |     | Violation |                 | Problem |          |           |          |         |
Most “candidate equilibrium” combinations violate independence. The rolling
mean, EMA, and Kalman estimator all use the same price series as their pri-
mary input. Their estimates are highly correlated in any time period where
mean reversion is well-behaved — precisely when combination would be most
appealing. TheARMA(1,1)equivalenceofProposition2.1impliesthattheEMA
andtheKalmanfilterarestructurallyidenticalatsteadystate. Averagingthem
24

| yields    | no independent |         |     | information.  |     |     |        |     |     |
| --------- | -------------- | ------- | --- | ------------- | --- | --- | ------ | --- | --- |
| 7.3 Where |                | Genuine |     | Orthogonality |     |     | Exists |     |     |
Theonecasewheregenuinenear-orthogonalitybetweenequilibriumestimates
exists is the Kalman filter (Tier 1) and the POC. The Kalman filter is derived
from the time sequence of prices, with no direct reference to volume distri-
bution. The POC is derived from the volume distribution across price levels,
with no direct reference to temporal ordering. These are structurally different
information sources. This orthogonality is the theoretical motivation for the
𝜇
Tier 2 conf factor in 𝐶 (Section 10.4); its empirical usefulness is tested
|               | POC,𝑡 |       |             |     | 𝑡   |           |     |     |     |
| ------------- | ----- | ----- | ----------- | --- | --- | --------- | --- | --- | --- |
| in Experiment |       | 5.    |             |     |     |           |     |     |     |
| 7.4 Revised   |       | Role: | Qualitative |     |     | Heuristic |     |     |     |
The Mean Clustering Hypothesis is retained in the framework as a qualitative
prior for including POC in Tier 2 of the confidence framework, not as a formal
statisticalargumentforensemblecombination. Operationalinclusionrequires
| empirical | validation |             | through     |      | Experiment |          | 5.  |         |     |
| --------- | ---------- | ----------- | ----------- | ---- | ---------- | -------- | --- | ------- | --- |
| Section   | 8          | — The       | Equilibrium |      |            | Validity |     | Problem |     |
| 8.1 When  |            | Equilibrium |             | Does | Not        | Exist    |     |         |     |
Theproblemofestimating𝜇∗
𝑡 presupposesthatameaningfulequilibriumexists
𝑡.
at time This presupposition can fail in at least three ways: trending regime
(no reversion to any level); post-structural-break transition (pre-break param-
eters unreliable); low MR-favourability (insufficient magnitude and speed of
𝑉
reversion to trade profitably). The validity gate 𝑡 addresses all three.
| 8.2 Conditions |     |     | for Validity |     |     |     |     |     |     |
| -------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- |
Four conditions define the validity of the equilibrium estimate at time 𝑡:
| Condition |     | 1 (Mean | reversion |     | favourability): |     |     | MRScore | ≥ 𝜃 . |
| --------- | --- | ------- | --------- | --- | --------------- | --- | --- | ------- | ----- |
|           |     |         |           |     |                 |     |     |         | 𝑡 𝑀𝑅  |
= 0.
| Condition |     | 2 (Suspension |     | state): |     | suspended |     |     |     |
| --------- | --- | ------------- | --- | ------- | --- | --------- | --- | --- | --- |
𝑡
Condition 3 (Innovation whiteness): The Ljung-Box test on normalised inno-
| vations | {𝜁  | } does |     | not reject |     | white | noise at | 𝑝 > 0.05. |     |
| ------- | --- | ------ | --- | ---------- | --- | ----- | -------- | --------- | --- |
𝑡−𝑤∶𝑡
Condition 4 (Regime gate): RFI ≥ 35. This condition is phase-specific —
𝑡
| active | only | from | Phase | 2 onward. |     |     |     |     |     |
| ------ | ---- | ---- | ----- | --------- | --- | --- | --- | --- | --- |
25

The Jarque-Bera normality test is monitored for diagnostic purposes but is not
| a hard  | gate condition. |          |      |     |     |     |     |
| ------- | --------------- | -------- | ---- | --- | --- | --- | --- |
| 8.3 The | Phase-Specific  | Validity | Gate |     |     |     |     |
The validity indicator 𝑉 operates in two phase-specific forms. The per-bar
𝑡
computation of 𝑉 occurs as Layer 3, after the Kalman filter (Layer 1) and con-
𝑡
fidencescore(Layer2)havealreadybeencomputedforbar𝑡.
SeeSection10.1
| for the | full layer     | ordering. |               |             |       |     |          |
| ------- | -------------- | --------- | ------------- | ----------- | ----- | --- | -------- |
| Phase   | 1 (Experiments | 1–3):     |               |             |       |     |          |
| 𝑉𝑃1     | = 1[MRScore    | ≥ 𝜃       | ]×1[suspended | = 0]×1[LB(𝜁 |       | , 𝑝 | > 0.05)] |
| 𝑡       |                | 𝑡 𝑀𝑅      |               | 𝑡           | 𝑡−𝑤∶𝑡 |     |          |
(8.1)
isloggedforeverybarbutdoesnotenter𝑉𝑃1
| RFI |     |     |     | . ThisisolatestheAnchored |     |     |     |
| --- | --- | --- | --- | ------------------------- | --- | --- | --- |
| 𝑡   |     |     |     | 𝑡                         |     |     |     |
Kalman’s DRC improvement from regime conditioning, providing clean exper-
| imental | attribution. |     |     |     |     |     |     |
| ------- | ------------ | --- | --- | --- | --- | --- | --- |
| Phase   | 2 onward:    |     |     |     |     |     |     |
𝑉𝑃2 = 1[RFI ≥ 35]×1[MRScore ≥ 𝜃 ]×1[suspended = 0]×1[LB(𝜁 , 𝑝 > 0.05)]
| 𝑡   | 𝑡   |     | 𝑡 𝑀𝑅 |     | 𝑡   |     | 𝑡−𝑤∶𝑡 |
| --- | --- | --- | ---- | --- | --- | --- | ----- |
(8.2)
In both phases: suspended (the persistent suspension indicator from Section
𝑡
6.5, evaluated in Step 4 of Section 4.5) replaces break_flag . break_flag is
|     |     |     |     |     | 𝑡   |     | 𝑡   |
| --- | --- | --- | --- | --- | --- | --- | --- |
a one-bar detection event — it equals 1 only on the specific bar where the
CUSUM threshold is crossed. Using break_flag directly would produce an
𝑡
effectivesuspensionperiodofexactlyonebar,whichisoperationallyequivalent
to no suspension. suspended persists until all recovery conditions in Section
𝑡
| 6.5 are | satisfied. |     |     |     |     |     |     |
| ------- | ---------- | --- | --- | --- | --- | --- | --- |
Implementation sequencing constraint: The Kalman filter must be
|     |     |     | 𝑉   |     |     | 𝑉   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
initialised and executing before 𝑡 can be evaluated, since 𝑡 references
|     |     |     | (𝜁  |     |     |     | 𝑉   |
| --- | --- | --- | --- | --- | --- | --- | --- |
Kalman-derived quantities , suspended ). The filter is never gated by .
|     |     |     | 𝑡   | 𝑡   |     |     | 𝑡   |
| --- | --- | --- | --- | --- | --- | --- | --- |
This constraint is non-negotiable and must be hardcoded in any implementa-
tion.
26

| Section     | 9 — | Independent  |     | Regime |             | Engine |     |     |     |
| ----------- | --- | ------------ | --- | ------ | ----------- | ------ | --- | --- | --- |
| 9.1 Purpose | and | Independence |     |        | Requirement |        |     |     |     |
TheRFI(RegimeFavourabilityIndex)isanindependentupstreamregimegate.
𝜇∗
Its defining architectural property is independence from — it must not use
any 𝜇̂ -derived quantity as an input. This is required to preserve clean ex-
𝑡|𝑡
perimental attribution in Experiment 1 and to maintain the DAG’s acyclicity
| through      | the research  |             | phase. |      |     |             |     |     |     |
| ------------ | ------------- | ----------- | ------ | ---- | --- | ----------- | --- | --- | --- |
| 9.2 RFI_lite | Specification |             |        |      |     |             |     |     |     |
| The RFI_lite | is            | constructed |        | from | two | components: |     |     |     |
Variance Ratio (VR): Measures whether short-horizon price variance is lower
than long-horizon variance, which is the signature of mean reversion:
|     |     |     |     | Var(𝑃 |     | )/𝑞 |     |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
𝑡−𝑞∶𝑡
|     |     |     | VR  | =   |     | , 𝑞 | < 𝑠 |     | (9.1) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
𝑡
|     |     |     |     | Var(𝑃 |     | )/𝑠 |     |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
𝑡−𝑠∶𝑡
|            |             |     |      |            |     |                   |     | 𝑞 = 5, 𝑠 = | 20. |
| ---------- | ----------- | --- | ---- | ---------- | --- | ----------------- | --- | ---------- | --- |
| A VR below | 1 indicates |     | mean | reversion. |     | Starting windows: |     |            |     |
ADF statistic (ADF): The augmented Dickey-Fuller test statistic. A more neg-
ative ADF statistic indicates stronger mean reversion evidence.
RFI_lite:
|     |     | RFI | = 50×(1−VR |     |     | )+50×(1−𝑝 |       | )   | (9.2) |
| --- | --- | --- | ---------- | --- | --- | --------- | ----- | --- | ----- |
|     |     |     | 𝑡          |     |     | 𝑡         | ADF,𝑡 |     |       |
where 𝑝 is the ADF p-value. Both components are scaled to contribute
ADF
| equally | to the | 0–100 | range. |     |     |     |     |     |     |
| ------- | ------ | ----- | ------ | --- | --- | --- | --- | --- | --- |
Acknowledged limitation: The two inputs — variance ratio and ADF p-value
— are correlated when the price series is strongly stationary or strongly non-
stationary. Equal weighting is accepted despite this correlation because no
principled alternative weighting is derivable without an optimisation target,
andanyoptimisationagainstdownstreamoutputswouldintroducedatasnoop-
ing. Experiment 4 tests the RFI’s predictive value empirically.
| 9.3 Gating  | Rules  | and  | Threshold |     | Protection |     |     |     |     |
| ----------- | ------ | ---- | --------- | --- | ---------- | --- | --- | --- | --- |
| Three-class | output | from | RFI       | :   |            |     |     |     |     |
𝑡
27

< 35: 𝜇∗
• RFI Trending or nonstationary regime. use suspended in Phase
𝑡
2+.
• 35 ≤ RFI < 55: Ambiguousregime. Reducedconfidence,cautioussignal
𝑡
use.
≥ 55:
• RFI Confirmed mean reversion regime. Full validity gating ap-
𝑡
plies.
The thresholds (35, 55) are starting values with no claim to optimality. No
optimisation of these thresholds against in-sample MRScore correlation is per-
mitted. If threshold adjustment is required after Experiment 4, it must be per-
formed on an out-of-sample window not used in the Experiment 4 Spearman
| correlation | calculation. |     |     |     |     |     |
| ----------- | ------------ | --- | --- | --- | --- | --- |
| 9.4 DAG     | Structure    |     |     |     |     |     |
The complete dependency graph among the framework’s primary components
| is shown | in Figure | 1.  |     |     |     |     |
| -------- | --------- | --- | --- | --- | --- | --- |
Raw price, volume
| Kalman |       | filter   |     |     | RFI  | engine |
| ------ | ----- | -------- | --- | --- | ---- | ------ |
| (𝜇̂ ,  | 𝑃 , 𝜁 | , CUSUM) |     |     | (VR, | → )    |
|        |       |          |     |     | ADF  | RFI    |
| 𝑡|𝑡    | 𝑡|𝑡   | 𝑡        |     |     |      | 𝑡      |
𝑉
Validity gate 𝑡
| Confidence |     | score |     |     |     |     |
| ---------- | --- | ----- | --- | --- | --- | --- |
(𝐶𝜇)
𝑡
Downstream sig-
nal generation
(out of scope
for this paper)
Figure1. DAGdependencystructureoftheframework’sprimarycomponents.
| Two properties |     | of this | DAG are essential: |     |     |     |
| -------------- | --- | ------- | ------------------ | --- | --- | --- |
1. No feedback from 𝑉 or RFI into the Kalman filter. The filter exe-
|       |     |            | 𝑡           | 𝑡     |     |     |
| ----- | --- | ---------- | ----------- | ----- | --- | --- |
| cutes | on  | raw prices | and volumes | only. |     |     |
𝜇̂
2. No -derived inputs to RFI . The regime engine is structurally inde-
|     | 𝑡|𝑡 |     |     | 𝑡   |     |     |
| --- | --- | --- | --- | --- | --- | --- |
pendent.
28

| 9.5 Kill | Criterion |     |     |     |     |     |     |     |     |     |
| -------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
IfExperiment4findsthatRFI hasnostatisticallysignificantSpearmancorrela-
𝑡
tion with forward DRC (𝑝 > 0.10 after correction for multiple testing), the RFI
engineinitscurrentspecificationfailsitskillcriterion. The𝑉𝑃2 gatewouldbe
𝑡
reconsidered, and an alternative regime conditioning mechanism would need
| to be developed   |     |     | before     | Phase | 2 experiments |     | proceed. |             |     |     |
| ----------------- | --- | --- | ---------- | ----- | ------------- | --- | -------- | ----------- | --- | --- |
| Section           | 10  | —   | Four-Layer |       | Architecture  |     | and      | Integration |     |     |
| 10.1 Architecture |     |     | Overview   |       |               |     |          |             |     |     |
The framework consists of four functional layers that operate in a strict depen-
𝑡,
dency order. On each bar the layers execute sequentially as follows:
Layer 1 — Filter Execution (Steps 1–4 of Section 4.5): The Kalman fil-
|     |     |     |     |     |     | {𝜇̂ | , 𝑃 , 𝜁 | }.  |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- |
ter runs unconditionally, producing 𝑡|𝑡 𝑡|𝑡 𝑡 The CUSUM statistics
|            | +,CUSUM |            | −}  |            |         |            |                |        |           |     |
| ---------- | ------- | ---------- | --- | ---------- | ------- | ---------- | -------------- | ------ | --------- | --- |
| {CUSUM     |         |            |     | are        | updated | from       | 𝜁 . break_flag | and    | suspended | are |
|            | 𝑡       |            | 𝑡   |            |         |            | 𝑡              | 𝑡      |           | 𝑡   |
| evaluated. |         | This layer |     | is ungated |         | and always | executes       | first. |           |     |
𝐶 𝜇
Layer 2 — Confidence Quantification (Section 10.4): is computed from
𝑡
Layer1outputs—specifically𝑃 ,𝑃 ,theCUSUMstatistics,therollingLjung-
|     |     |     |     |     | 𝑡|𝑡 | ∞   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
̂
Box𝑝-valueon{𝜁 },and𝑄 . Thislayerisalsoungatedandalwaysexecutes
|         |           |     | 𝑡−𝑤∶𝑡  |             | 𝑡   |     |     |     |     |     |
| ------- | --------- | --- | ------ | ----------- | --- | --- | --- | --- | --- | --- |
| second, | including |     | during | suspension. |     |     |     |     |     |     |
𝑉
Layer 3 — Validity Gating(Section8.3): iscomputedfromLayer1outputs
𝑡
(𝜁 , suspended )andexternalregimesignals(MRScore , RFI ). 𝑉 = 1permits
| 𝑡     |          | 𝑡   |      |          |     |        |     | 𝑡 𝑡 | 𝑡   |     |
| ----- | -------- | --- | ---- | -------- | --- | ------ | --- | --- | --- | --- |
| Layer | 4 access | to  | 𝜇̂ . | Executes |     | third. |     |     |     |     |
𝑡|𝑡
Layer 4 — Downstream Use: Signal generation and (eventually) position
sizing. Accessto𝜇̂ isconditionalon𝑉 = 1. Thislayerisoutofscopeforthis
|     |     |     | 𝑡|𝑡 |     |     |     | 𝑡   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
paper.
The layer ordering is non-negotiable. Layer 2 must execute after Layer 1 (con-
fidence depends on filter outputs) and before Layer 3 (the Ljung-Box input to
𝑉
| is shared |     | with | conf         | , ensuring |      | consistent | state). |     |     |     |
| --------- | --- | ---- | ------------ | ---------- | ---- | ---------- | ------- | --- | --- | --- |
| 𝑡         |     |      |              | LB,𝑡       |      |            |         |     |     |     |
| 10.2 What |     | This | Architecture |            | Does | Not        | Do      |     |     |     |
𝜇∗
• The Kalman filter does not compute signals. It estimates 𝑡 .
𝐶 𝜇
• does not modify signal entry or exit in Phases 1–2. It is logged only.
𝑡
• 𝑉 does not gate filter execution. It gates downstream signal use only.
𝑡
| • RFI | does | not | affect | Kalman |     | parameters. | It affects | 𝑉 only. |     |     |
| ----- | ---- | --- | ------ | ------ | --- | ----------- | ---------- | ------- | --- | --- |
|       | 𝑡    |     |        |        |     |             |            | 𝑡       |     |     |
29

𝑉
• MRScore does not affect Kalman parameters. It appears in only.
𝑡
| •    | 𝜇̂ does | not       | appear | as          | an input | to  | RFI | or MRScore. |     |     |     |
| ---- | ------- | --------- | ------ | ----------- | -------- | --- | --- | ----------- | --- | --- | --- |
|      | 𝑡|𝑡     |           |        |             |          |     |     | 𝑡           |     |     |     |
| 10.3 | AMR     | Framework |        | Integration |          |     |     |             |     |     |     |
𝜇∗
The estimation framework integrates into the broader AMR framework as a
drop-inreplacementforsimplerequilibriumestimators. Theinterfaceisclean:
𝜇
|     |     |     |     |     | 𝜇̂  | 𝑉   |     |     | 𝐶   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
the AMR framework receives 𝑡|𝑡 , 𝑡 , and optionally 𝑡 at each timestep.
KalmanStab: A binary stability flag indicating that the Kalman filter has
passed its initialisation burn-in period and is operating at or near steady state:
|     | KalmanStab |     |     | = 1[𝑃 | < 1.1×𝑃 |     | ]×1[suspended |     |     | = 0] | (10.1) |
| --- | ---------- | --- | --- | ----- | ------- | --- | ------------- | --- | --- | ---- | ------ |
|     |            |     | 𝑡   | 𝑡|𝑡   |         |     | ∞             |     |     | 𝑡    |        |
𝜇
| 10.4 | The | Confidence |     | Score | 𝐶   |     |     |     |     |     |     |
| ---- | --- | ---------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
𝑡
|     |     |     |     | 𝜇   |     |     |     |     |     |     | 𝜇∗  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The confidence score 𝐶 ∈ [0,1] quantifies the real-time reliability of the
𝑡
estimate using Kalman-internal diagnostics only. No MRScore, DRC, z-score,
| ordownstreamAMRcomponentappearsin𝐶 |     |     |     |     |     |     |     | 𝜇   |     |     |     |
| ---------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
. NoPOCinputisusedinPhases
𝑡
|     | 𝐶 𝜇 |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1–2. is computed in Layer 2 of the per-bar sequence, after the filter has
𝑡
| updated | and | before | the | validity | gate | is  | evaluated. |     |     |     |     |
| ------- | --- | ------ | --- | -------- | ---- | --- | ---------- | --- | --- | --- | --- |
𝐶local
Local Confidence:
𝑡
Local confidence measures the current filter state through two factors:
𝑄/max(1−𝜌2,
|     |     |     |     | 𝑃   | =   |     |     | 0.01) |     |     | (10.2) |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | ------ |
∞
𝑃
𝑡|𝑡
|     |     |     |      | =   | exp(−max(0, |     |     |     | −1)) |     |        |
| --- | --- | --- | ---- | --- | ----------- | --- | --- | --- | ---- | --- | ------ |
|     |     |     | conf | 𝑈,𝑡 |             |     |     |     |      |     | (10.3) |
𝑃
∞
|     |      |         |     |        |     |           |     | +,  |       | −)  |        |
| --- | ---- | ------- | --- | ------ | --- | --------- | --- | --- | ----- | --- | ------ |
|     |      |         |     |        |     | max(CUSUM |     |     | CUSUM |     |        |
|     |      |         | =   | max(0, | 1−  |           |     | 𝑡   |       | 𝑡 ) |        |
|     | conf |         |     |        |     |           |     |     |       |     | (10.4) |
|     |      | CUSUM,𝑡 |     |        |     |           |     | ℎ   |       |     |        |
𝑐
|     |     |     |     | 𝐶local | = conf |     | ×conf |         |     |     | (10.5) |
| --- | --- | --- | --- | ------ | ------ | --- | ----- | ------- | --- | --- | ------ |
|     |     |     |     | 𝑡      |        | 𝑈,𝑡 |       | CUSUM,𝑡 |     |     |        |
conf measuresposterioruncertaintyrelativetosteady-state. Atsteadystate
𝑈,𝑡
| (𝑃  | = 𝑃 |         |     | = 1.  |        |     |        |      | <   | 1,         |        |
| --- | --- | ------- | --- | ----- | ------ | --- | ------ | ---- | --- | ---------- | ------ |
|     |     | ): conf |     | Above | steady |     | state: | conf |     | recovering | toward |
| 𝑡|𝑡 | ∞   |         | 𝑈,𝑡 |       |        |     |        |      | 𝑈,𝑡 |            |        |
1asthefilterconverges. Thisfactorisnaturallylessthan1duringburn-inand
| after | structural | breaks. |     |     |     |     |     |     |     |     |     |
| ----- | ---------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
30

conf provides a smooth pre-break degradation signal. As the CUSUM
CUSUM,𝑡
statistic builds toward the threshold ℎ , confidence declines continuously.
𝑐
| At CUSUM | = 0: | conf    | =   | 1.  | At  | CUSUM | =   | ℎ (flag | threshold): |     |
| -------- | ---- | ------- | --- | --- | --- | ----- | --- | ------- | ----------- | --- |
|          |      | CUSUM,𝑡 |     |     |     |       |     | 𝑐       |             |     |
= 0.
| conf    | After | a flag, | the | CUSUM | resets |     | to zero, | causing | conf |         |
| ------- | ----- | ------- | --- | ----- | ------ | --- | -------- | ------- | ---- | ------- |
| CUSUM,𝑡 |       |         |     |       |        |     |          |         |      | CUSUM,𝑡 |
|         |       |         |     |       | 𝑃      |     |          | 𝑃       |      |         |
to return to 1 — but conf degrades as rises above during the recov-
|     |     | 𝑈,𝑡 |     |     | 𝑡|𝑡 |     |     | ∞   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ery period. The two local factors are thus complementary in their temporal
behaviour.
𝐶global
| Global Confidence: |     |     |     |     |     |     |     |     |     |     |
| ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝑡
Global confidence measures the rolling coherence of the estimator:
𝑝
LB,𝑡
|     |     |      |      | = min(1, |     |     | )   |     |     |        |
| --- | --- | ---- | ---- | -------- | --- | --- | --- | --- | --- | ------ |
|     |     | conf | LB,𝑡 |          |     |     |     |     |     | (10.6) |
0.20
𝑄 ̂
|     |     | conf | =   | exp(−∣ |     | 𝑡   | −1∣) |     |     | (10.7) |
| --- | --- | ---- | --- | ------ | --- | --- | ---- | --- | --- | ------ |
param,𝑡
|     |     |     |     |     |     | 𝑄 ̂ |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝑡−5
𝐶global
|     |     |     | = conf |      | ×conf |         |     |     |     | (10.8) |
| --- | --- | --- | ------ | ---- | ----- | ------- | --- | --- | --- | ------ |
|     |     | 𝑡   |        | LB,𝑡 |       | param,𝑡 |     |     |     |        |
conf usestheLjung-Box𝑝-valuecomputedovertherollingwindow{𝜁 },
| LB,𝑡 |     |     |     |     |     |     |     |     |     | 𝑡−𝑤∶𝑡 |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
|      |     | 𝑉𝑃1 |     | 𝑉𝑃2 |     |     |     |     |     |       |
the same window used in 𝑡 and 𝑡 (no duplicate computation). The nor-
malisationat𝑝 = 0.20—sothatconf = 1onlywheninnovationsareclearly
LB,𝑡
white by conventional standards — is a starting value calibrated for the in-
tended sensitivity. When 𝑝 = 0.05: conf = 0.25. When 𝑝 < 0.01: conf
|            |     |     |     |     | LB,𝑡 |     |     |     |     | LB,𝑡 |
| ---------- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | ---- |
| approaches | 0.  |     |     |     |      |     |     |     |     |      |
A note on rolling-window robustness: Ljung-Box statistics computed on short
rolling windows (20 bars is the default here) exhibit non-trivial sampling vari-
ability. The resulting conf LB,𝑡 series may be noisier in practice than the other
three confidence factors. This concern motivates the deliberate choice to log
𝜇
𝐶 fromPhase1withoutoperationaluse: theempiricalstabilityandpredictive
𝑡
usefulness of all four factors — including conf — will be assessed through
LB,𝑡
Experiment 6 stratification before any downstream application is committed.
If empirical review finds conf to be excessively noisy relative to its predic-
LB,𝑡
𝜇
tive contribution, reconsideration of its role in 𝐶 is a candidate for future
𝑡
research. The confidence architecture is unchanged; the acknowledgement is
one of intellectual honesty about rolling-window test behaviour.
̂
conf monitors parameter stability by comparing 𝑄 against its value five
| param,𝑡 |     |     |     |     |     |     |     | 𝑡   |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
bars prior — a lag chosen as a practical starting value that balances detection
31

̂
speed against noise. Abrupt jumps in 𝑄 signal that the estimation window is
= 1.
straddling a regime boundary. At zero jump: conf param,𝑡 At 50% jump:
|         | ≈ 0.61. |                 | ≈ 0.37. |     |     |
| ------- | ------- | --------------- | ------- | --- | --- |
| conf    | At      | 100% jump: conf |         |     |     |
| param,𝑡 |         |                 | param,𝑡 |     |     |
Combined:
𝜇
|     |     | 𝐶 = 𝐶local | ×𝐶global |     | (10.9) |
| --- | --- | ---------- | -------- | --- | ------ |
|     |     | 𝑡 𝑡        | 𝑡        |     |        |
𝜇
𝐶 ∈ [0,1]. High values indicate the filter is at steady state, CUSUM is low,
𝑡
innovations are white, and parameters are stable. Low values indicate at least
| one failure | mode is active. |     |     |     |     |
| ----------- | --------------- | --- | --- | --- | --- |
Why multiplicative aggregation? Any single failure mode should be able to
substantially reduce confidence regardless of the state of the others. An addi-
tive or weighted-average design would allow a healthy conf to compensate
LB
for a dangerously building conf . That is wrong: a filter approaching a
CUSUM
structuralbreakdeserveslowconfidenceevenifitsinnovationautocorrelation
is currently acceptable. Multiplicative aggregation implements this logic with-
outrequiringweights,andweightswouldrequireanoptimisationtarget—any
target derived from downstream performance reintroduces circularity.
Why these four factors? Each monitors a genuinely distinct failure mode:
conf monitors filter uncertainty above steady-state; conf monitors pre-
| 𝑈   |     |     |     | CUSUM |     |
| --- | --- | --- | --- | ----- | --- |
break transition risk; conf monitors innovation autocorrelation (model mis-
LB
𝑄 ̂
specification); conf monitors instability (regime mixing in the estima-
param
tion window). The rejected factor conf monitors the same failure mode
bias,𝑡
as CUSUM (persistent one-directional innovations) and is not independent.
Addingitwouldinflatesensitivitytothatonefailuremodeasymmetricallywith-
| out monitoring | any new   | failure mode. |     |     |     |
| -------------- | --------- | ------------- | --- | --- | --- |
| Confidence     | behaviour | by regime:    |     |     |     |
𝜇
| Regime | conf | conf  | conf | conf  | 𝐶       |
| ------ | ---- | ----- | ---- | ----- | ------- |
|        | 𝑈    |       |      |       | 𝑡       |
|        |      | CUSUM | LB   | param |         |
|        | ≈ 1  | ≈ 1   | ≈ 1  | ≈ 1   |         |
| Stable |      |       |      |       | High    |
| mean   |      |       |      |       | (> 0.8) |
reversion
|      | ≈ 1 |           |           | ≈ 1 |          |
| ---- | --- | --------- | --------- | --- | -------- |
| Slow |     | declining | declining |     | Moderate |
trend
developing
32

𝐶 𝜇
| Regime |     | conf |     | conf |       |     | conf      |     | conf   |     |
| ------ | --- | ---- | --- | ---- | ----- | --- | --------- | --- | ------ | --- |
|        |     |      | 𝑈   |      | CUSUM |     | LB        |     | param  | 𝑡   |
| Pre-   |     | ≈ 1  |     | →    | 0     |     | declining |     | stable | Low |
break
transition
| Break | /   | recovering |     | reset | →   | 1   | uncertain |     | jumps | Low |
| ----- | --- | ---------- | --- | ----- | --- | --- | --------- | --- | ----- | --- |
suspen-
sion
period
| Post- |     | recovering |     | ≈ 1 |     |     | recovering |     | recovering | Rising |
| ----- | --- | ---------- | --- | --- | --- | --- | ---------- | --- | ---------- | ------ |
break
recovery
Tier 2 Extension (Phase 3 only, after Experiment 5 validation):
If Experiment 5 confirms that Kalman-POC agreement predicts subsequent
| DRC quality, |     | a POC | factor | is  | added: |     |          |     |     |         |
| ------------ | --- | ----- | ------ | --- | ------ | --- | -------- | --- | --- | ------- |
|              |     |       |        |     |        |     | |𝜇̂ −POC |     | |   |         |
|              |     |       |        |     |        |     | 𝑡|𝑡      |     | 𝑊,𝑡 |         |
|              |     |       | conf   | =   | max(0, |     | 1−       |     | )   | (10.10) |
|              |     |       | POC,𝑡  |     |        |     |          | 2𝜎  |     |         |
𝑡
𝜇
|     |     | 𝐶   | = 𝐶local | ×𝐶global |     | ×conf |       |       |         |         |
| --- | --- | --- | -------- | -------- | --- | ----- | ----- | ----- | ------- | ------- |
|     |     | 𝑡   |          | 𝑡        | 𝑡   |       | POC,𝑡 | (Tier | 2 only) | (10.11) |
|     |     |     |          |          |     |       | 𝐶 𝜇   |       |         |         |
Operational deployment: Phases 1–2: is computed and logged on every
𝑡
bar using equation (10.9). It does not modify signal generation or position
𝜇
sizing. Phase 3 (Tier 2, if validated): 𝐶 modulates position sizing on the
𝑡
| conservative |     | linear    | schedule |      | specified |          | in Appendix | B.4. |     |     |
| ------------ | --- | --------- | -------- | ---- | --------- | -------- | ----------- | ---- | --- | --- |
| Section      | 11  | — Failure |          | Mode |           | Analysis |             |      |     |     |
A framework that acknowledges its failure modes honestly is more useful than
one that claims broad applicability. Seven failure modes are identified and
| connected           | to  | their | corresponding |           |     | mitigation  | mechanisms. |     |     |     |
| ------------------- | --- | ----- | ------------- | --------- | --- | ----------- | ----------- | --- | --- | --- |
| 11.1 Near-Unit-Root |     |       |               | Parameter |     | Instability |             |     |     |     |
Description: When 𝜌 is near 1, the MLE surface for the full parameter set
| {𝜌,𝑄,𝐷2} |     |     |     |     |     | 𝜌,  |     |     |     |     |
| -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
is flat with respect to producing high-variance parameter esti-
| mates | and unstable |     | equilibrium |     |     | estimates. |     |     |     |     |
| ----- | ------------ | --- | ----------- | --- | --- | ---------- | --- | --- | --- | --- |
33

Trigger: Instruments with slow mean reversion (half-life > 30 bars at daily
frequency), or any instrument when estimated from 𝑛 < 60 observations.
Mitigation: The constrained estimator (𝜌 fixed at the cross-instrument prior
𝜌 ) eliminates this failure mode at the cost of imposing a starting assumption
0
on the mean reversion speed. The cost is bounded: if the true 𝜌 is near 𝜌 , the
0
performance penalty is negligible. Simulation Study 1 quantifies this tradeoff
across the relevant 𝜌 range.
11.2 CUSUM Cascade
Description: A genuine structural break triggers a CUSUM flag. MLE re-
̂
estimation on a window straddling the break produces inflated 𝑄. Inflated
̂
𝑄 leads to large normalised innovations on the next pass. Large normalised
innovations re-trigger CUSUM. The filter enters an oscillatory false-flagging
sequence that may prolong suspension significantly beyond the genuine tran-
sition duration.
Trigger: Genuine structural breaks during which market dynamics shift
abruptly.
Mitigation: Thethree-conditionrecoveryprotocolwithcascadedamping(Sec-
tion 6.5). The 20-bar deferral of re-estimation avoids mixed-regime estimation.
Thetemporaryelevationofℎ —toastartingvalueof7.0—afterasecondflag
𝑐
within 20 bars of the first reduces cascade risk without permanently desensi-
tising the detector. Experiment 7 monitors cascade frequency to validate this
mechanism.
11.3 Anchor Drift During Sustained Trends
Description: During sustained price trends spanning the entire anchor win-
dow, 𝜇 drifts continuously. The anti-drift theorem (Theorem 4.2) guar-
anchor,𝑡
anteesthat𝜇̂ tracks𝜇 withboundeddeviation—butif𝜇 isitself
𝑡|𝑡 anchor,𝑡 anchor,𝑡
trending, the “equilibrium” estimate is trending.
Trigger: Sustained trends lasting more than 𝑤 bars.
Mitigation: The validity gate 𝑉 conditions signal use on MRScore ≥ 𝜃 .
𝑡 𝑡 𝑀𝑅
Anchor stability monitoring (Section 4.4, Remark 4.3) is a logged diagnostic,
not a hard gate.
34

| 11.4 Model | Misspecification |     |     | (Non-Gaussian |     | Innovations) |
| ---------- | ---------------- | --- | --- | ------------- | --- | ------------ |
Description: The Kalman filter’s MMSE optimality relies on Gaussian noise.
When price processes exhibit heavy tails, skewness, or microstructure jumps,
the normalised innovations 𝜁 are non-Gaussian. This does not bias the esti-
𝑡
mate — the Kalman filter remains BLUE under non-Gaussianity — but it inval-
idates the specific distributional properties used by the CUSUM detector and
| the Ljung-Box |     | test thresholds. |     |     |     |     |
| ------------- | --- | ---------------- | --- | --- | --- | --- |
Mitigation: Jarque-Bera is monitored for this condition. The false-positive
rate qualifier in Section 6.5 acknowledges finite-sample tail inflation. Robust
Kalman extensions are specified in Appendix B.2 for activation if empirical ev-
idence warrants.
| 11.5 Volume |     | Data Degradation |     |     |     |     |
| ----------- | --- | ---------------- | --- | --- | --- | --- |
Description: When volumedataismissing, unreported, orofpoorquality, the
anchor degrades silently to an arithmetic mean. The DRC advantage claimed
| for the Anchored |     | Kalman              | is based | on  | VWAP anchoring. |                        |
| ---------------- | --- | ------------------- | -------- | --- | --------------- | ---------------------- |
| Mitigation:      |     | The ANCHORED_KALMAN |          |     | /               | PSEUDO_ANCHORED_KALMAN |
flag system. Data validation protocol (Section 12.0) must be completed before
| experiments | begin. |              |     |             |     |     |
| ----------- | ------ | ------------ | --- | ----------- | --- | --- |
| 11.6 Regime |        | Conditioning |     | Circularity |     |     |
𝜇∗
Description: The primary circularity between RFI and is resolved via the
𝜇
DAG architecture. A secondary, limited interaction remains: 𝐶 uses CUSUM
𝑡
𝜇
statistics (Kalman-derived), and 𝐶 can eventually inform position sizing in
𝑡
Phase 3. This feedback is one-directional and operates only in Phase 3 after
| explicit             | validation; | it does | not         | affect the | research | phase. |
| -------------------- | ----------- | ------- | ----------- | ---------- | -------- | ------ |
| 11.7 Multi-Timeframe |             |         | Consistency |            |          |        |
Description: If the framework is extended to multiple timeframes, there is no
|     |     |     | 𝜇d̂ aily |     | 𝜇ŵ eekly |     |
| --- | --- | --- | -------- | --- | --------- | --- |
theoretical guarantee that and are consistent with each other.
|     |     |     | 𝑡|𝑡 |     | 𝑡|𝑡 |     |
| --- | --- | --- | --- | --- | --- | --- |
Mitigation: Single-timeframevalidationiscompletedfirst(Phases1–2). Multi-
| timeframe | extension | is explicitly |     | deferred | (Section | 13.1). |
| --------- | --------- | ------------- | --- | -------- | -------- | ------ |
35

Section 12 — Validation Architecture
12.0 Data Validation Protocol
Beforeanyexperimentbegins,thefollowingmustbeconfirmedforeachtarget
instrument:
1. Volume data source and type: Exchange-reported, broker-reported, or
unavailable.
2. Anchor type assignment: VWAP if exchange volume is available and
validated; arithmetic mean otherwise.
3. Instrumentclassificationflag: ANCHORED_KALMANorPSEUDO_ANCHORED_KALMAN.
Results from PSEUDO_ANCHORED_KALMAN instruments must be reported
separately and excluded from the primary DRC advantage claim.
12.1 Out-of-Sample Design
The framework uses purged cross-validation with a minimal embargo period.
For each instrument:
• 60% training / 40% OOS split: All parameter estimation uses only the
training period. OOS evaluation uses rolling forward execution with pa-
rameters re-estimated on expanding windows that do not include OOS
data.
• Embargo period: 20 trading days between training and OOS windows,
preventinglook-aheadcontamination through the60-day MLE estimation
window.
• Multiple non-overlapping OOS windows: Where instrument history
permits (minimum 5 years of daily data), three non-overlapping OOS eval-
uation periods provide robustness evidence.
12.2 Experiment Programme
Experiment 1 — Anchored Kalman vs. Rolling Mean (Primary Valida-
tion)
Research question: Does the Anchored Kalman estimator produce a more neg-
ative OOS DRC than the rolling mean baseline at ℎ = 5 bars?
Three arms: (a) Rolling mean (60-day window) — baseline; (b) Anchored
Kalman with unconstrained MLE
{𝜌,𝑄,𝐷2};
(c) Anchored Kalman with
constrained MLE {𝑄,𝐷2}, 𝜌 fixed at prior 𝜌 . If Simulation Study 1 finds that
0
unconstrained 𝜌 identification is unreliable at 𝑛 = 60, arm (c) becomes the
36

primary comparison. Arms (b) and (c) are compared against each other as a
secondary outcome, providing evidence on the cost of the constraint.
Primary outcome: the comparison is directional — we assess whether the
Kalman estimate provides a consistently better-identified equilibrium. The kill
criterion specifies when to stop, not when improvement is insufficient.
Concurrent experiments: Experiment 1a (Anchor Sensitivity — compare 65-
day, 130-day, 260-day windows); Experiment 1b (Re-estimation Frequency —
| compare    | 5-day, | 10-day, | 20-day      |     | intervals). |               |           |     |     |     |     |
| ---------- | ------ | ------- | ----------- | --- | ----------- | ------------- | --------- | --- | --- | --- | --- |
| Experiment |        | 2 —     | Constrained |     | vs.         | Unconstrained | Estimator |     |     |     |     |
|            |        |         |             |     | 𝜌 =         | 𝜌             |           |     |     |     |     |
Research question: Does fixing 0 improve OOS DRC stability relative to
|               |     |     | 𝑛   | = 60? |           |             |     | 𝜎(DRC) |        |     |         |
| ------------- | --- | --- | --- | ----- | --------- | ----------- | --- | ------ | ------ | --- | ------- |
| unconstrained |     | MLE | at  |       | Stability | is measured | as  |        | across |     | rolling |
OOS windows — a lower value indicates more consistent estimation.
| Experiment |     | 3 — | CUSUM | Sensitivity |     | Analysis |     |     |     |     |     |
| ---------- | --- | --- | ----- | ----------- | --- | -------- | --- | --- | --- | --- | --- |
Gridsearchover𝑘 ∈ {0.3,0.5,0.7},ℎ ∈ {4.0,5.0,6.0}onOOSwindows. The
|     |     |     | 𝑐   |     |     | 𝑐   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
purpose is confirmation that the default starting parameters are not obviously
| wrong,     | not | optimisation |                | toward | a better | configuration. |     |     |     |     |     |
| ---------- | --- | ------------ | -------------- | ------ | -------- | -------------- | --- | --- | --- | --- | --- |
| Experiment |     | 4 —          | RFI Predictive |        | Validity |                |     |     |     |     |     |
Research question: Does RFI have statistically significant Spearman correla-
𝑡
tion with forward OOS DRC? Kill criterion: 𝑝 > 0.10 after Bonferroni correc-
| tion across |           | all instruments. |                   |            |     |                |      |         |     |         |      |
| ----------- | --------- | ---------------- | ----------------- | ---------- | --- | -------------- | ---- | ------- | --- | ------- | ---- |
| Experiment  |           | 5 —              | POC Corroboration |            |     | Validity (Tier |      | 2 Gate) |     |         |      |
|             |           |                  |                   |            |     |                | (|𝜇̂ | −       |     | | < 1𝜎) |      |
| Research    | question: |                  | Does              | Kalman-POC |     | agreement      |      | POC     |     |         | pre- |
|             |           |                  |                   |            |     |                | 𝑡|𝑡  |         | 𝑊,𝑡 |         |      |
dict higher subsequent DRC? Consequence: if Mann-Whitney 𝑝 < 0.10 on a
dedicated holdout window, conf is added per equations (10.10)–(10.11). If
POC,𝑡
| not, POC | is  | eliminated | from | the | framework. |     |     |     |     |     |     |
| -------- | --- | ---------- | ---- | --- | ---------- | --- | --- | --- | --- | --- | --- |
𝜇
Experiment 6 — Confidence Score Stratification (Tier 2 Gate for 𝐶 )
𝑡
|          |           |     | high-𝐶 |     | 𝜇       | (𝐶 𝜇 > 0.7) |      |            |     |          |     |
| -------- | --------- | --- | ------ | --- | ------- | ----------- | ---- | ---------- | --- | -------- | --- |
| Research | question: |     | Do     |     | periods |             | show | materially |     | stronger |     |
|          |           |     |        |     | 𝑡       | 𝑡           |      |            |     |          |     |
|          |           | 𝜇   |        |     | 𝜇       |             | 𝜇    |            |     |          |     |
DRC than low-𝐶 periods (𝐶 < 0.3)? Uses logged 𝐶 values from Phases 1–
|     |     | 𝑡   |     |     | 𝑡   |     | 𝑡   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2. The holdout window must not have been used in any Phase 1–2 experiment.
This experiment also provides the primary assessment of whether conf con-
LB,𝑡
| tributes   | predictive |     | value | as a           | standalone | factor.     |     |     |     |     |     |
| ---------- | ---------- | --- | ----- | -------------- | ---------- | ----------- | --- | --- | --- | --- | --- |
| Experiment |            | 7 — | CUSUM | False-Positive |            | Calibration |     |     |     |     |     |
Research question: What is the empirical false-positive rate of the CUSUM de-
tectoronthetargetinstrumentsunderstable-regimeconditions? Thisprovides
37

𝑘 = 0.5,
the empirical basis for assessing whether the default parameters
𝑐
| ℎ = 5.0 | are appropriate. |     |     |     |     |     |
| ------- | ---------------- | --- | --- | --- | --- | --- |
𝑐
Extendedmetrics: thefrequencywithwhichasecondCUSUMflagfireswithin
20 bars of the first (cascade frequency); and the mean suspension duration. A
cascade frequency materially above 20% of break events — treated as a start-
ing benchmark for review, not a formally derived threshold — warrants review
| of the cascade  | damping | protocol.          |     |     |          |        |
| --------------- | ------- | ------------------ | --- | --- | -------- | ------ |
| 12.3 Simulation | Studies |                    |     |     |          |        |
|                 |         | 𝜌                  |     | 𝑛   | = 60:    |        |
| Simulation      | Study   | 1 — Identification |     | at  | Generate | 10,000 |
𝜌
realisations at each of five target values spanning the prior range
|     |     |     |     |     | ̂   | ̂2/𝐷2) |
| --- | --- | --- | --- | --- | --- | ------ |
{0.92,0.94,0.96,0.98,0.99}. Measure 𝜎(𝜌)̂ , 𝜎(𝑄 /𝑄), 𝜎(𝐷 under
unconstrained MLE. If 𝜎(𝜌)̂ > 0.05 at any target 𝜌, the constrained esti-
mator becomes the production default and the paper’s primary estimator
specification is updated accordingly before Phase 2 proceeds.
Simulation Study 2 — CUSUM Performance Under Breaks: Generate re-
alisations with known break locations. Measure CUSUM detection lag and
false-positive rate across break magnitudes. Validate the 20-bar deferral rule:
̂
confirm that re-estimation on the deferred window produces lower 𝑄 inflation
| than immediate | re-estimation. |     |     |     |     |     |
| -------------- | -------------- | --- | --- | --- | --- | --- |
𝜇
Simulation Study 3 — Confidence Score Calibration: Verify that 𝐶 is
𝑡
𝜇
empiricallycalibrated—thatperiodswith𝐶 ∈ [𝑐,𝑐+0.1]showproportionally
𝑡
| higherDRCadvantagethanperiodswith𝐶 |     |     |     | 𝜇 ∈ [𝑐−0.1,𝑐]. |     |     |
| ---------------------------------- | --- | --- | --- | -------------- | --- | --- |
Thisisacalibration
𝑡
| check, not | an in-sample | optimisation.  |              |     |               |          |
| ---------- | ------------ | -------------- | ------------ | --- | ------------- | -------- |
| 12.4 Kill  | Criteria     |                |              |     |               |          |
| Experiment |              | Kill Criterion |              |     | Consequence   |          |
| Experiment | 1            | Kalman         | DRC not more |     | Full review   | of model |
|            |              | negative       | than rolling |     | specification | required |
≥ 2/3
|     |     | mean   | DRC across |     | before Phase | 2   |
| --- | --- | ------ | ---------- | --- | ------------ | --- |
|     |     | of OOS | windows    |     |              |     |
Experiment 4 RFI shows no significant RFI specification fails;
𝑡
|     |     | Spearman | correlation |     | alternative | regime |
| --- | --- | -------- | ----------- | --- | ----------- | ------ |
(𝑝 > 0.10
|     |     |     | after correction) |     | conditioning | required |
| --- | --- | --- | ----------------- | --- | ------------ | -------- |
38

| Experiment |     | Kill Criterion |     | Consequence |     |
| ---------- | --- | -------------- | --- | ----------- | --- |
Simulation Study 1 𝜎(𝜌)̂ > 0.05 at target 𝜌 Constrained estimator
|     |     | values |     | becomes | production |
| --- | --- | ------ | --- | ------- | ---------- |
default
| Experiment | 7   | Cascade    | frequency | Cascade     | damping  |
| ---------- | --- | ---------- | --------- | ----------- | -------- |
|            |     | materially | above 20% | of protocol | reviewed |
break events
Kill criteria are not retroactively interpreted. They are stated in advance.
| Section    | 13 — Research | Roadmap    |           |     |     |
| ---------- | ------------- | ---------- | --------- | --- | --- |
| 13.1 Phase | 1 — Baseline  | Validation | (Current) |     |     |
Objective: Establish whether the Anchored Kalman estimator produces a
demonstrably better-identified equilibrium than the rolling mean baseline, as
| measured | by OOS DRC. |     |     |     |     |
| -------- | ----------- | --- | --- | --- | --- |
Scope: All Phase 1 experiments operate on a single timeframe — daily bars
on NIFTY 50 as the primary instrument, with 2–3 secondary instruments for
robustness. Multi-timeframe extension (weekly, 4H) is Tier 2 work, activated
only after Phase 1 and Phase 2 single-timeframe validation is complete. The
𝜏 and 𝜏 timeframes should not be implemented during Phases 1–2.
| 𝐻            | 𝐿      |              |                |              |     |
| ------------ | ------ | ------------ | -------------- | ------------ | --- |
| Experiments: | 1, 1a, | 1b, 2, 3, 7, | and Simulation | Studies 1–3. |     |
Phase 1 outputs logged for future use (not used operationally): RFI values on
𝑡
𝜇
every bar (Experiment 4 preparation); 𝐶 values on every bar (Experiment 6
𝑡
preparation); POC values on every bar for ANCHORED_KALMAN instruments
| (Experiment | 5 preparation). |             |     |     |     |
| ----------- | --------------- | ----------- | --- | --- | --- |
| 13.2 Phase  | 2 — Regime      | Integration |     |     |     |
Objective: Validate the independent regime engine (RFI) and introduce the
𝑉𝑃2
gate.
𝑡
| Prerequisite: | Phase | 1 kill criteria | not triggered. |     |     |
| ------------- | ----- | --------------- | -------------- | --- | --- |
Experiments: 4, 5 (POC validation, if ANCHORED_KALMAN instruments
𝑉𝑃2
available). 𝑡 gate introduced at the start of Phase 2 once Experiment 4
| confirms | RFI predictive | content. |     |     |     |
| -------- | -------------- | -------- | --- | --- | --- |
39

13.3 Phase 3 — Confidence Integration and Signal Readiness
Objective: Validate the confidence score’s predictive value and, if validated,
integrate it into the downstream signal framework.
Prerequisite: Phase 2 kill criteria not triggered. Sufficient Phase 1–2 logged
𝜇
𝐶 data available.
𝑡
Experiments: 6 (confidence stratification), and the Tier 2 integration of
conf if Experiment 5 was successful.
POC
13.4 Deferred Components
Component Tier Activation Condition
Adaptive 𝑄 (EWMA, 2 After Phase 1 base model validation
regime-switching,
BOCD)
Multi-timeframe 2 After Phase 2 single-timeframe
extension (𝜏 , 𝜏 ) validation
𝐻 𝐿
Bayesian Online 2 After Phase 1 CUSUM validation
Change Point
Detection
𝜇
conf in 𝐶 2 After Experiment 5
POC 𝑡
𝜇
𝐶 position sizing 2 After Experiment 6
𝑡
modulation
MRScore-informed 3 After Phase 2, with explicit feedback
𝑄 adjustment structure review
13.5 What Constitutes Premature Optimisation
The following actions are explicitly prohibited before their designated phase:
• Tuning CUSUM parameters (𝑘 , ℎ ) against in-sample DRC before Exper-
𝑐 𝑐
iment 7 provides the false-positive baseline.
• Selecting anchor window length based on in-sample DRC performance
before Experiment 1a.
• Implementingadaptive𝑄beforebasemodelDRCadvantageisconfirmed.
• AdjustingRFIthresholds(35,55)basedonin-sampleMRScorecorrelation
after Experiment 4 — thresholds must be adjusted only on OOS data not
used in Experiment 4.
𝜇
• Implementingthefullfour-factor𝐶 position-sizingintegrationbeforethe
𝑡
Tier 2 validation holdout has been evaluated.
40

𝜇
• Using logged 𝐶 values to filter Phase 1–2 results retroactively.
𝑡
Section 14 — Conclusion
TheAnchoredKalmanEquilibriumEstimatorpresentedinthispaperisawork-
ing hypothesis, not a validated framework. Its central claim — that treating
the latent equilibrium as a Kalman-tracked state anchored to VWAP produces
amoreaccuratelyidentifiedequilibriumthanrollingmeanorEMAalternatives
—hasstrongtheoreticalsupportbutremainsempiricallyunconfirmedpending
the Experiment 1 results.
What has been established is an internally consistent architecture. The state-
space formulation is theoretically well-grounded. The anti-drift guarantee
(Theorem 4.2) is proven under stated assumptions. The DAG independence
structure prevents the circularity that would otherwise invalidate the experi-
mental programme. The CUSUM detector provides real-time break detection
with a known asymptotic false-positive rate. The confidence framework
monitors four genuinely distinct failure modes without introducing circular
dependencies or requiring optimisation against trading performance.
V2 introduced three architectural advances over earlier practice: an indepen-
dent regime engine that gates signal use without contaminating estimation;
a CUSUM-based break detector that replaced the fragile three-bar rule; and
a compressed validation roadmap with explicit kill criteria. V2.5 introduces
two further refinements: a revised post-break recovery protocol in Section 6.5
that prevents CUSUM cascade failure through 20-bar re-estimation deferral
and temporary threshold elevation; and a redesigned confidence score in Sec-
tion 10.4 that is Phase 1 deployable, internally consistent, and operationally
grounded.
The most important constraint to preserve is the kill criterion structure. A
research programme without explicit stopping rules is a research programme
thatcannotfail,whichisaresearchprogrammethatcannotbetrusted. Thekill
criteria in Section 12.4 define the conditions under which the central hypoth-
esis is rejected and the programme restructures. They are stated in advance
and will be applied mechanically.
41

Appendix A — Mathematical Derivations
A.1 Proof of the Anti-Drift Theorem (Theorem 4.2)
Theorem: Underconstant𝜇 ,theprocess𝑑 = 𝜇∗−𝜇 hasastationary
anchor 𝑡 𝑡 anchor
distribution with mean 0 and variance
𝑄/(1−𝜌2).
Proof: From the state equation (4.1):
𝑑 = 𝜇∗ −𝜇 = 𝜌(𝜇∗ −𝜇 )+𝜂 = 𝜌𝑑 +𝜂
𝑡 𝑡 anchor 𝑡−1 anchor 𝑡 𝑡−1 𝑡
This is a standard AR(1) process with |𝜌| < 1. By standard results: 𝔼[𝑑 ] = 0
𝑡
and Var(𝑑 ) = 𝑄/(1 − 𝜌2). The process is covariance-stationary and its mean
𝑡
is zero, confirming that 𝜇∗ does not drift from 𝜇 in expectation. □
𝑡 anchor
Derivation under time-varying anchor: When 𝜇 drifts, define 𝑑 =
anchor,𝑡 𝑡
𝜇∗ −𝜇 as before. Then:
𝑡 anchor,𝑡
𝑑 = 𝜌𝑑 +(𝜌 −1)(𝜇 −𝜇 )+𝜂
𝑡 𝑡−1 anchor,𝑡 anchor,𝑡−1 𝑡
The additional term (𝜌−1)(𝜇 −𝜇 ) is negative when the anchor
anchor,𝑡 anchor,𝑡−1
rises(since𝜌 < 1),partiallyoffsettinganchordrift—butthestationaritybound
𝑄/(1−𝜌2)
no longer holds exactly.
A.2 Derivation of the Steady-State Kalman Gain
Thesteady-stateposteriorvariance𝑃 satisfiesthealgebraicRiccatiequation:
∞
𝑃2
𝑃 = 𝜌2(𝑃 − ∞ )+𝑄
∞ ∞ 𝑃 +𝐷2
∞
Let 𝐾 = 𝑃 /(𝑃 + 𝐷2) be the steady-state gain. Then 𝑃 (1 − 𝜌2𝐾) = 𝑄,
∞ ∞ ∞
giving 𝑃 = 𝑄/(1 − 𝜌2𝐾 ). Substituting back and solving the quadratic in
∞ ∞
𝑃 yieldsequation(4.15). Thesteady-stategainisthen𝐾 = 𝑃 /(𝑃 +𝐷2).
∞ ∞ ∞ ∞
□
A.3 Prediction Error Decomposition Likelihood
The log-likelihood for the state-space model is computed via the prediction
error decomposition:
42

|     |           |     |     | 𝑇   |         | 1     | 𝑇   |      | 𝜈 (𝜃)2 |     |
| --- | --------- | --- | --- | --- | ------- | ----- | --- | ---- | ------ | --- |
|     | ℓ(𝜌,𝑄,𝐷2) |     | =   | −   | ln(2𝜋)− | ∑[ln𝑆 |     | (𝜃)+ | 𝑡      | ]   |
|     |           |     |     | 2   |         | 2     |     | 𝑡    | 𝑆      | (𝜃) |
𝑡
𝑡=1
where 𝜈 (𝜃) and 𝑆 (𝜃) are the innovation mean and variance from the Kalman
|     | 𝑡   | 𝑡   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
{𝜌,𝑄,𝐷2}.
recursions, parameterised by 𝜃 = This likelihood is exact under
| the Gaussian | noise | assumptions. |     |          |     |            |     |     |     |     |
| ------------ | ----- | ------------ | --- | -------- | --- | ---------- | --- | --- | --- | --- |
| Appendix     | B     | — Deferred   |     | Research |     | Directions |     |     |     |     |
| B.1 Adaptive |       | 𝑄 Variants   |     |          |     |            |     |     |     |     |
Three adaptive 𝑄 mechanisms are specified for Phase 2+ evaluation.
| Variant1—EWMA𝑄: |     |     | 𝑄   | = (1−𝜆)𝜈2+𝜆𝑄 |     |     |                                  |     |     |     |
| --------------- | --- | --- | --- | ------------ | --- | --- | -------------------------------- | --- | --- | --- |
|                 |     |     |     | 𝑡            |     | 𝑡   | 𝑡−1 . Simpleexponentialsmoothing |     |     |     |
applied to squared innovations. Activation condition: Phase 1 confirms DRC
advantage; Experiment 2 shows 𝑄 instability as the primary failure mode.
|         |                      |     |     |     | 𝑄:  |            |     | (high-𝑄 | low-𝑄), |              |
| ------- | -------------------- | --- | --- | --- | --- | ---------- | --- | ------- | ------- | ------------ |
| Variant | 2 — Regime-Switching |     |     |     |     | Two states |     |         | /       | with transi- |
tion probabilities estimated from the 𝜁 sequence. Activation condition: Phase
𝑡
2 complete; Experiment 3 shows systematic 𝑄 mismatch across identified
regimes.
Variant 3 — BOCD-Triggered 𝑄 Reset: Bayesian Online Change Point De-
tection provides a posterior probability of a change point at each bar. When
𝑄
the posterior exceeds a threshold, is elevated for a specified number of bars.
Activation condition: Phase 1 CUSUM results reviewed; if cascade frequency
is persistent, BOCD provides a probabilistic alternative to hard thresholding.
𝑄)
All three are deferred. The base model (fixed MLE-estimated must be vali-
𝑄
| dated          | before adding |            | adaptation. |       |     |                 |     |     |     |     |
| -------------- | ------------- | ---------- | ----------- | ----- | --- | --------------- | --- | --- | --- | --- |
| B.2 Robustness |               | Extensions |             | Under |     | Non-Gaussianity |     |     |     |     |
Robust Kalman filtering: Replace the Gaussian innovation distribution with
a Student-𝑡 distribution, producing an M-estimator variant that down-weights
large innovations. Activation condition: Experiment 7 shows systematic JB
| rejection | and high | false-positive |     |     | CUSUM | rates. |     |     |     |     |
| --------- | -------- | -------------- | --- | --- | ----- | ------ | --- | --- | --- | --- |
Jump-Augmented OU Process: Add a compound Poisson jump term to equa-
tion (4.1), modelling rare large moves separately. Requires particle filtering
43

rather than Kalman filtering. Activation requires compelling empirical evi-
| dence | that            | the | jump component |           | adds | DRC | predictive | value. |     |     |     |     |     |
| ----- | --------------- | --- | -------------- | --------- | ---- | --- | ---------- | ------ | --- | --- | --- | --- | --- |
| B.3   | Multi-Timeframe |     |                | Hierarchy |      |     |            |        |     |     |     |     |     |
Themulti-timeframeextensiondefinesahierarchyoftimeframes{𝜏 (weekly), 𝜏 (daily), 𝜏 (4H)},
|     |     |     |     |     |     |     |     |     |     | 𝐻   |     | 𝑀   | 𝐿   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
with the hypothesis that 𝜇∗ provides a long-run anchor constraint on 𝜇∗ .
|     |     |     |     | 𝜏   |     |     |     |     |     |     | 𝜏   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     | 𝐻   |     |     |     |     |     |     |     | 𝑀   |     |
This extension is deferred until Phase 2 single-timeframe validation is com-
plete.
| B.4 | Confidence |     | Score | Tier | 2 Introduction |     | Protocol |     |     |     |     |     |     |
| --- | ---------- | --- | ----- | ---- | -------------- | --- | -------- | --- | --- | --- | --- | --- | --- |
𝐶 𝜇
The operational introduction of as a position-sizing input (Phase 3) follows
𝑡
this protocol:
𝜇
|     |               |     |               |     |         |       | high-𝐶  |     |         | (> 0.7)   |      |     |     |
| --- | ------------- | --- | ------------- | --- | ------- | ----- | ------- | --- | ------- | --------- | ---- | --- | --- |
|     | 1. Experiment |     | 6 validation: |     | Confirm |       | that    | 𝑡   | periods |           | show |     |     |
|     |               |     |               |     |         | low-𝐶 | 𝜇       | (<  | 0.3)    |           |      |     |     |
|     | significantly |     | stronger      | DRC | than    |       | periods |     | on      | a holdout | win- |     |     |
𝑡
downotusedinanyPhase1–2experiment. Significancethreshold: Mann-
|     | Whitney                        | 𝑝   | < 0.10. |     |     |               |     |      |               |     |     |     |     |
| --- | ------------------------------ | --- | ------- | --- | --- | ------------- | --- | ---- | ------------- | --- | --- | --- | --- |
|     |                                |     |         |     |     | Positionsize= |     |      | size×max(0.5, |     | 𝐶 𝜇 | ).  |     |
|     | 2. Conservativelinearschedule: |     |         |     |     |               |     | base |               |     |     |     |     |
𝑡
𝜇
This schedule halves the base position at 𝐶 = 0 and applies full base
𝑡
𝜇
size at 𝐶 = 1. The 0.5 floor prevents complete elimination of positions
𝑡
based on confidence alone — complete elimination requires the regime
|     |     | (𝑉 = | 0). |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
gate
𝑡
3. Holdout evaluation: The position-sizing integration is evaluated on a
|     | separate |     | holdout window |     | before | any | production | deployment. |     |     |     |     |     |
| --- | -------- | --- | -------------- | --- | ------ | --- | ---------- | ----------- | --- | --- | --- | --- | --- |
4. Tier 2 confidence formula: If conf is validated in Experiment 5, the
POC
Tier 2 formula applies equation (10.11). Otherwise, equation (10.9) re-
|     | mains | in  | force. |     |     |     |     |     |     |     |     |     |     |
| --- | ----- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝜇
𝐶
5. Reporting: The effect of 𝑡 -based position sizing is reported separately
from the base model results. The two contributions — estimator quality
|     | and | confidence-based |     | sizing | —   | are | not conflated. |     |     |     |     |     |     |
| --- | --- | ---------------- | --- | ------ | --- | --- | -------------- | --- | --- | --- | --- | --- | --- |
V2.5 — Equilibrium Estimation Framework. Research status: pre-empirical.
All claims are working hypotheses pending Experiment 1 results.
44
