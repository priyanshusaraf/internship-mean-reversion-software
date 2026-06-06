| State | T:    | Mean-Reversion |               |     | Ignition |     |
| ----- | ----- | -------------- | ------------- | --- | -------- | --- |
|       | Final | Synthesis,     | Formalization |     | & Freeze |     |
The Regime-Transition Layer of an Adaptive Mean-Reversion Framework
When does tradeable residual mean reversion ignite inside a trend?
|     | Layer    | 2 — Regime-Shift | Detection           |         |               |              |
| --- | -------- | ---------------- | ------------------- | ------- | ------------- | ------------ |
|     | Residual | ε = P −µ∗        | (with µ∗ and        | MRScore | frozen)       |              |
|     |          | Frozen           | — theory converged; | only    | the empirical | gate remains |
Status
|          |      | Institutional | research report |     |     |     |
| -------- | ---- | ------------- | --------------- | --- | --- | --- |
| Document | type |               |                 |     |     |     |
|          | Date | 31 May        | 2026            |     |     |     |
Audience: finance professionals first, quants second. Every technical object is paired with its economic intuition,
itsformula,itslimitations,anditstradingrelevance. Mathematicssupportsthenarrative;itdoesnotdominateit.

| State T — | Mean-Reversion |     | Ignition |     |     |     | Final Synthesis | & Freeze |
| --------- | -------------- | --- | -------- | --- | --- | --- | --------------- | -------- |
Abstract
This report compiles and finalizes the definition, mechanics, and structure of T, the
State
hypothesized regime in which a market transitions from trend domination into tradeable
residualmeanreversionbeforethatreversionbecomesobviousandcrowded. Workingstrictly
on the residual ε = P −µ∗ (with the equilibrium estimator µ∗ and the MRScore filter
held frozen), we converge on a single institutional-grade definition, fix the ontology, map
the transition mechanically, separate necessary from sufficient conditions,
A → T → B
and reduce a sprawling idea space to three orthogonal mechanisms. We then specify a
circularity-proofquantitativetarget,acheaptwo-weekfalsificationgate,andthedecisivetests
thatwouldproveorkillthethesis. Thehonestverdictisdeliberatelysplitfourways: StateT
is a real mechanism (high confidence), a plausible-but-unproven edge (moderate-to-low), and
its tradeable-early form at daily frequency is the single open question — bottlenecked not by
theory but by two measurable facts: the daily base rate and the width of the mechanism-
recognition gap. Both are testable in roughly two weeks. The instruction this document
| issues | is simple: |        |             |               |               |          |         |     |
| ------ | ---------- | ------ | ----------- | ------------- | ------------- | -------- | ------- | --- |
|        |            | freeze | the theory, | run the gate, | build nothing | until it | passes. |     |
Contents
| 1 Introduction |     | and Scope |     |     |     |     |     | 3   |
| -------------- | --- | --------- | --- | --- | --- | --- | --- | --- |
1.1 The one problem this layer solves . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
1.2 The residual, and what is frozen . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
1.3 The three-state vocabulary: A, T, B . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
1.4 Two claims, never to be tested as one. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
| 2 Executive | Verdict    |      |         |               |     |     |     | 4   |
| ----------- | ---------- | ---- | ------- | ------------- | --- | --- | --- | --- |
| 3 The Final | Definition | of   | State   | T             |     |     |     | 5   |
| 4 Ontology  | of T:      | What | Kind of | Object Is It? |     |     |     | 5   |
4.1 Primary commitment: a window, not a point . . . . . . . . . . . . . . . . . . . . . . . . . 5
4.2 Generating mechanism: a threshold bifurcation, not gradual drift . . . . . . . . . . . . . . 6
4.3 Observable identity: critical speeding up . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
4.4 Temporal descriptor: a hazard schedule . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
4.5 Economic carrier: an order-flow imbalance flip. . . . . . . . . . . . . . . . . . . . . . . . . 6
| 5 The A→T | →B  | Mechanics |     |     |     |     |     | 6   |
| --------- | --- | --------- | --- | --- | --- | --- | --- | --- |
5.1 State A — trend domination (shallow / absent basin) . . . . . . . . . . . . . . . . . . . . 6
5.2 The A→T transition: causal order (this ordering is the thesis) . . . . . . . . . . . . . . . 7
5.3 State T — ignition (formed-but-unrecognized basin) . . . . . . . . . . . . . . . . . . . . . 7
5.4 State B — crowded / obvious reversion (deep, known basin) . . . . . . . . . . . . . . . . . 7
5.5 Mechanical summary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
| 6 Necessary | and | Sufficient | Conditions |     |     |     |     | 8   |
| ----------- | --- | ---------- | ---------- | --- | --- | --- | --- | --- |
6.1 Necessary conditions (causal — without each, no edge) . . . . . . . . . . . . . . . . . . . . 8
6.2 The sufficient condition (what makes T and tradeable) . . . . . . . . . . . . . . . . . 9
early
6.3 Honest classification (demote weak ideas instead of hiding them) . . . . . . . . . . . . . . 9
| 7 The Three | Mechanisms |     |     |     |     |     |     | 9   |
| ----------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
7.1 Mechanism 1 — Basin formation / critical speeding up of . . . . . . . . . . . . . . . . . 9
ε
7.2 Mechanism 2 — Order-flow / inventory imbalance flip at extremes . . . . . . . . . . . . . 10
7.3 Mechanism 3 — Crowding / recognition lag . . . . . . . . . . . . . . . . . . . . . . . . . . 10
7.4 Why everything else was rejected . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
| 8 The Mechanism-Recognition |     |     |     | Gap: the Alpha | Question |     |     | 11  |
| --------------------------- | --- | --- | --- | -------------- | -------- | --- | --- | --- |
8.1 Strongest argument FOR a positive gap . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
8.2 Strongest argument AGAINST . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
8.3 Final verdict . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
1

| State T         | — Mean-Reversion |        | Ignition      |     |     |     | Final Synthesis | & Freeze |
| --------------- | ---------------- | ------ | ------------- | --- | --- | --- | --------------- | -------- |
| 9 Illusion      | Risks,           | Ranked |               |     |     |     |                 | 12       |
| 10 Quantitative |                  | Target | Formalization |     |     |     |                 | 13       |
10.1 Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
10.2 The five candidate formulations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
10.3 The recommended target: C3 primary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
10.4 Secondary and benchmark . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
| 11 The | Existence | Gate: | Experimental | Design |     |     |     | 14  |
| ------ | --------- | ----- | ------------ | ------ | --- | --- | --- | --- |
11.1 Data and scope (deliberately narrow). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
11.2 The three questions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
11.3 Kill criteria (pre-registered, numeric, non-negotiable) . . . . . . . . . . . . . . . . . . . . . 15
11.4 Daily-viability decision rule . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
| 12 Decisive | Tests: | What      | Would | Prove or | Kill T |     |     | 15  |
| ----------- | ------ | --------- | ----- | -------- | ------ | --- | --- | --- |
| 13 The      | Frozen | Blueprint |       |          |        |     |     | 16  |
13.1 Frozen (decided — do not reopen without strong new evidence) . . . . . . . . . . . . . . . 16
13.2 Deferred (revisit only if the gate passes and a specific need appears) . . . . . . . . . . . . 16
13.3 Removed (rejected — do not resurrect). . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
13.4 The one open question, and the only authorized next work . . . . . . . . . . . . . . . . . . 17
| A Notation         | and        | Key       | Formulae | (frozen | for this | phase) |     | 17  |
| ------------------ | ---------- | --------- | -------- | ------- | -------- | ------ | --- | --- |
| B Pre-Registration |            | Checklist | (fill    | before  | touching | data)  |     | 17  |
| Selected           | References |           |          |         |          |        |     | 17  |
2

| State T        | — Mean-Reversion |         |     | Ignition  |       |        |     |     |     | Final Synthesis | & Freeze |
| -------------- | ---------------- | ------- | --- | --------- | ----- | ------ | --- | --- | --- | --------------- | -------- |
| 1 Introduction |                  |         |     | and Scope |       |        |     |     |     |                 |          |
| 1.1 The        | one              | problem |     | this      | layer | solves |     |     |     |                 |          |
A trending market and a mean-reverting market demand opposite trades. The dangerous ground
is the seam between them — the moment a market that still trendy begins, underneath
looks
the surface, to revert. Our entire programme is built to trade that seam. We are not claiming
markets are permanently mean reverting; we are asking a narrower, sharper question:
The regime-transition problem. On the residual ε = P −µˆ∗, when does tradeable
|     |     |     |     |     |     |     |     | t   | t   | t   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
mean reversion — and can we detect that ignition it becomes obvious and
|            |           |       | ignite   |               |     |              |         |     | before |     |     |
| ---------- | --------- | ----- | -------- | ------------- | --- | ------------ | ------- | --- | ------ | --- | --- |
| crowded,   |           | while | alpha    | still exists? |     |              |         |     |        |     |     |
| 1.2 The    | residual, |       | and      | what          | is  | frozen       |         |     |        |     |     |
| Everything | in        | this  | document | lives         | on  | the residual |         |     |        |     |     |
|            |           |       |          |               |     | ε =          | P −µˆ∗, |     |        |     | (1) |
|            |           |       |          |               |     | t            | t       | t   |        |     |     |
the gap between price and our estimated equilibrium. Two upstream layers are frozen and are
revisited here: (i) the equilibrium estimator µ∗, and (ii) the MRScore / DRC framework
not
that decides whether a market has historically been mean-reversion-favourable. We critique
neither. We take ε as given and ask only about its transition dynamics.
Thisscopingisnotcosmetic. Becauseeveryquantitywecomputeisafunctionofε,andεdepends
on µ∗, a biased would bias every feature every label simultaneously. We therefore treat
|     |     | µ∗  |     |     |     | and |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
“model-free” as a claim about only, never about the equilibrium estimate —
|     |     |     |     | reversion |     | dynamics |     |     |     |     |     |
| --- | --- | --- | --- | --------- | --- | -------- | --- | --- | --- | --- | --- |
and we build an explicit µ∗-robustness test into the falsification gate (Section 12).
| 1.3 The      | three-state |           |             | vocabulary:  |     | A, T,      | B    |               |            |              |         |
| ------------ | ----------- | --------- | ----------- | ------------ | --- | ---------- | ---- | ------------- | ---------- | ------------ | ------- |
| We partition |             | the world |             | the residual |     | can be in  | into | three states. |            |              |         |
| •            |             |           |             |              |     | Deviations | from | persist       | or extend; | the residual | behaves |
| State        | A           | — trend   | domination. |              |     |            |      | µ∗            |            |              |         |
like a random walk; fading loses money. There is no basin to fall into.
• State T — ignition. A restoring force has formed and a costed fade has positive expectancy,
|     |           |     |         | crowded. |     | This is the | narrow, | valuable | window. |     |     |
| --- | --------- | --- | ------- | -------- | --- | ----------- | ------- | -------- | ------- | --- | --- |
| but | the trade | is  | not yet |          |     |             |         |          |         |     |     |
• State B — crowded reversion. The reversion is obvious and consensus; everyone fades
every deviation; competition compresses the edge to zero. The basin is still there; the alpha
is gone.
| 1.4 Two | claims, |     | never | to  | be tested | as  | one |     |     |     |     |
| ------- | ------- | --- | ----- | --- | --------- | --- | --- | --- | --- | --- | --- |
The programme bundles two logically distinct claims. Conflating them is the central failure
| mode this | document |     | guards | against. |     |     |     |     |     |     |     |
| --------- | -------- | --- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- |
Claim E (Existence). Inside trend-dominated markets there exist episodes of genuinely
| tradeable |     | residual | reversion. |     |     |     |     |     |     |     |     |
| --------- | --- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
Claim P (Predictability / Earliness). The onset of those episodes (State T) is
| detectable |     | before | the | reversion | becomes | crowded |     | (State B). |     |     |     |
| ---------- | --- | ------ | --- | --------- | ------- | ------- | --- | ---------- | --- | --- | --- |
3

| State T — | Mean-Reversion |     | Ignition |     |     |     | Final | Synthesis & Freeze |
| --------- | -------------- | --- | -------- | --- | --- | --- | ----- | ------------------ |
Claim E is plausible and partly supported by the literature. Claim P is the hard, fragile,
alpha-bearing claim, and it is where almost all of the falsification effort must go. A project
of this kind “proves” E, feels validated, and then quietly assumes P. We refuse that move and
| require P   | to clear | a far   | higher bar. |     |     |     |     |     |
| ----------- | -------- | ------- | ----------- | --- | --- | --- | --- | --- |
| 2 Executive |          | Verdict |             |     |     |     |     |     |
We answer the existence question four ways, deliberately, because the four have very different
confidence levels and are substitutes. Treating a high score on the first as evidence for the
not
| fourth is | precisely | the | self-deception | to avoid. |     |     |     |       |
| --------- | --------- | --- | -------------- | --------- | --- | --- | --- | ----- |
| Question  |           |     |                | Verdict   |     |     |     | Conf. |
Theoretical existence. Can Yes. This is a local bifurcation; the High
a residual pass from near-unit- economics that produce it (trend-fuel (∼85%)
roottoatradeablemean-reverting exhaustion, dealer inventory rebal-
| basin? |     |     |     | ancing,      | auction acceptance) |     | are mi-  |     |
| ------ | --- | --- | --- | ------------ | ------------------- | --- | -------- | --- |
|        |     |     |     | crostructure | orthodoxy,          | not | exotica. |     |
Empirical plausibility (Claim Probable. Safari–Schmidhuber’s Mod.-high
Does tradeable residual rever- finding that “trends revert before (∼60%)
E).
sion actually occur inside trendy becoming statistically significant” is
| markets? |     |     |     | sub-significant | residual      | reversion         | in- |     |
| -------- | --- | --- | --- | --------------- | ------------- | ----------------- | --- | --- |
|          |     |     |     | side a trend.   | But           | “sub-significant” |     |     |
|          |     |     |     | implies         | the effect is | small.            |     |     |
Daily-frequency viability. Doubtful. Daily sits squarely in the Low-mod.
Does it survive at daily resolution, trend-dominated band, and the clean- (∼35%)
| net of | costs? |     |     | est reversion | carrier   | we have | (inven-   |     |
| ------ | ------ | --- | --- | ------------- | --------- | ------- | --------- | --- |
|        |        |     |     | tory price    | pressure) | has an  | empirical |     |
|        |        |     |     | half-life     | of ∼1 day | — much  | of the    |     |
|        |        |     |     | reversion     | completes |         | the daily |     |
inside
bar.
Alpha viability (Claim P). Is Unproven, fragile. The lead ex- Low
the mechanism detectable before ists in private order flow (the dealer (∼25–35%)
thecrowd,withagapwideenough knows their book); whether any sur-
| to trade? |     |     |     | vives in              | public daily | data  | is exactly |     |
| --------- | --- | --- | --- | --------------------- | ------------ | ----- | ---------- | --- |
|           |     |     |     | what efficient-market |              | logic | competes   |     |
|           |     |     |     | toward                | zero.        |       |            |     |
Thehonestcompoundread. Theseconditionsareconjunctive: atradeabledailystrategy
needs existence and daily-survival and a positive public earliness gap, simultaneously.
The all-in probability is therefore the product, not the maximum — realistically ∼20–30%.
That is not a reason to stop; it is a reason to spend two weeks testing rather than months
building. A 25% shot resolved by a cheap experiment is a good research bet. A 25% shot
| you build | a   | full stack | on top of | is a bad one. |     |     |     |     |
| --------- | --- | ---------- | --------- | ------------- | --- | --- | --- | --- |
4

| State T | — Mean-Reversion |            | Ignition |     |     |       |     |     |     | Final Synthesis | & Freeze |
| ------- | ---------------- | ---------- | -------- | --- | --- | ----- | --- | --- | --- | --------------- | -------- |
| 3 The   | Final            | Definition |          |     | of  | State | T   |     |     |                 |          |
There is one definition. It is frozen. No competing formulations are retained.
State T is the bounded interval during which the residual ε = P −µ∗ develops a tradeable
mean-reverting basin of attraction whose existence is not yet reflected in positioning.
It begins when the marginal order-flow balance at deviation extremes flips from
continuation-dominant to reversion-dominant — the economic cause being exhaustion of
marginal trend demand and/or completion of a directional risk transfer that forces liquidity
| providers |     | to rebalance | one-sided |     | inventory. |     |     |     |     |     |     |
| --------- | --- | ------------ | --------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
It is by the residual’s signature — recovery rate rising from
|     | identified |     |     |     | critical-speeding-up |     |     |     |     |     |     |
| --- | ---------- | --- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- |
≈ 0, lag-1 autocorrelation of ε falling, deviation variance contracting — conditional on (a)
a deviation large enough to clear round-trip costs, |z| outside the no-arbitrage band, and
(b) timescale separation 1 (an equilibrium stable enough, over the holding horizon, to
S >
| revert | to). |     |     |     |     |     |     |     |     |     |     |
| ------ | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
It only while market recognition — open interest / positioning — remains light,
persists
and it ends, becoming State B, when reversion grows crowded and expected fade return
| compresses |     | below | its risk-and-cost |     |     | hurdle. |     |     |     |     |     |
| ---------- | --- | ----- | ----------------- | --- | --- | ------- | --- | --- | --- | --- | --- |
Why this definition, and not the alternatives. It is the only formulation that is simultane-
ously (i) a precise with a theory-fixed, non-fitted signature; (ii) computable
|     |     | physical |     | identity |     |     |     |     |     |     |     |
| --- | --- | -------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
from data up to time with no smoothed or look-ahead inputs; (iii) economically rather
|     |     |     | t   |     |     |     |     |     |     | causal |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- |
than correlational; (iv) falsifiable on a specific predicted lead–lag; and (v) anchored by the one
non-monotone clause — recognition — that separates the profitable window from the crowded
one. Each rejected alternative (a threshold-crossing point, a hidden-Markov latent state, a pure
hazard process, an order-flow regime alone, a timescale-divergence event, gradual drift) fails at
| least one | of  | these tests, | as  | detailed | in  | Sections | 4 and | 7.  |     |     |     |
| --------- | --- | ------------ | --- | -------- | --- | -------- | ----- | --- | --- | --- | --- |
Every clause maps to a measurable: the signature → recovery rate / AR(1) / variance of ε; the
deviation |z|; the equilibrium-stability precondition S; the boundary open interest /
|     | →   |     |     |     |     |     |     | →   |     | →   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
positioning. Nothing in the definition is mystical, and nothing in it can be satisfied by hindsight.
| 4 Ontology |     | of  | T:  | What | Kind |     | of Object | Is  | It? |     |     |
| ---------- | --- | --- | --- | ---- | ---- | --- | --------- | --- | --- | --- | --- |
Ruling. StateTisalatenttransitionwindow —aprocessoffinite,variable,andsometimes-
zero duration — generated by a threshold bifurcation, observed as critical speeding up,
|            |     | a hazard |     | schedule, | and |         | an  | order-flow | imbalance | flip. |     |
| ---------- | --- | -------- | --- | --------- | --- | ------- | --- | ---------- | --------- | ----- | --- |
| completing |     | on       |     |           |     | carried | by  |            |           |       |     |
These are not five competing ontologies. They are one object described at five levels. The ruling
| fixes the   | hierarchy | and         | rejects | the | literal   | alternatives. |     |         |     |     |     |
| ----------- | --------- | ----------- | ------- | --- | --------- | ------------- | --- | ------- | --- | --- | --- |
| 4.1 Primary |           | commitment: |         |     | a window, |               | not | a point |     |     |     |
Basin formation is a deepening: the restoring force rises through a range over multiple bars. A
point or instantaneous-break model (Bai–Perron, or a hidden-Markov model’s zero-width regime
jump) discards the very interior dynamics — the speeding-up — that make T detectable and
| tradeable. | Reject | the | point. |     |     |     |     |     |     |     |     |
| ---------- | ------ | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
5

| State T | — Mean-Reversion |     | Ignition |     |     |     |     |     |     | Final | Synthesis | & Freeze |
| ------- | ---------------- | --- | -------- | --- | --- | --- | --- | --- | --- | ----- | --------- | -------- |
4.2 Generating mechanism: a threshold bifurcation, not gradual drift
Threshold-cointegration and smooth-transition models establish that reversion is band-activated:
inside the cost band the residual is random walk; outside it, it reverts. There is a genuine
≈
qualitative switch, not a linear ramp. The well forms; it does not fade in. Reject smooth
drift.
| 4.3 Observable |     |     | identity: | critical |     | speeding | up  |     |     |     |     |     |
| -------------- | --- | --- | --------- | -------- | --- | -------- | --- | --- | --- | --- | --- | --- |
This is the deepest and most useful identity, and it is not loose. The early-warning literature
shows that a system approaching a tipping point exhibits down: recovery from
|     |     |     |     |     |     |     |     | critical | slowing |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------- | --- | --- | --- |
perturbations slows, lag-1 autocorrelation → 1, variance rises. The mirror phenomenon — when
a basin of attraction is compressed or steepened — is critical speeding up: recovery accelerates,
autocorrelation falls, variance contracts. State A is the shallow-basin / near-critical state (ε
| near unit-root, |     | AR(1) | 1). |       |     |                   |     |          |          |     |     | This is the |
| --------------- | --- | ----- | --- | ----- | --- | ----------------- | --- | -------- | -------- | --- | --- | ----------- |
|                 |     |       | ≈   | State | T   | is the residual’s |     | critical | speeding |     | up. |             |
measurable face of the bifurcation, and its signs are locked by theory — a small overfitting
surface.
| 4.4 Temporal |     | descriptor: |     | a   | hazard | schedule |     |     |     |     |     |     |
| ------------ | --- | ----------- | --- | --- | ------ | -------- | --- | --- | --- | --- | --- | --- |
“When does the well finish forming?” is a time-varying hazard conditional on precursors. This is
the right language because T has a (minutes to weeks), can be
|     |     |     |     |     | duration | distribution |     |     |     |     |     | censored |
| --- | --- | --- | --- | --- | -------- | ------------ | --- | --- | --- | --- | --- | -------- |
(the trend resumes; the well never completes), and is covariate-driven. The hazard view also
makes “early” precise: act while the hazard is rising and recognition is still low.
| 4.5 Economic |     | carrier: |     | an order-flow |     | imbalance |     | flip |     |     |     |     |
| ------------ | --- | -------- | --- | ------------- | --- | --------- | --- | ---- | --- | --- | --- | --- |
The bifurcation is not magic; it is carried by a flip in marginal flow at the extremes (continuation
orders thinning, contrarian / absorbing orders dominating). This is the cause beneath the
| statistical | signature. |     |     |     |     |     |     |     |     |     |     |     |
| ----------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Explicitly rejected as the literal ontology: (1) the point / instantaneous break —
wrong because T has interior dynamics; (2) the HMM discrete-state jump — useful as
a probability scaffold for A and B, but it models the passage as a zero-width
|     |     |     |     |     |     |     |     | A   | → B |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
event, which is exactly what T is not, so it cannot represent T’s interior; (3) the
metastable
equilibrium as a standalone steady state — T is a transition, not a third resting attractor,
so “metastable” survives only as an adjective for the window’s instability.
The window is narrow by nature and idealizable as a point only in the limit of instant recognition
— which is precisely the limit in which it becomes untradeable. The ontology and the alpha
| thesis are | the | same | statement | viewed    |     | from two angles. |     |     |     |     |     |     |
| ---------- | --- | ---- | --------- | --------- | --- | ---------------- | --- | --- | --- | --- | --- | --- |
| 5 The      | A   | → T  | → B       | Mechanics |     |                  |     |     |     |     |     |     |
The entire alpha claim lives in the lead–lag ordering of what changes. This section is the
| mechanistic | map. |     |       |            |     |          |     |        |        |     |     |     |
| ----------- | ---- | --- | ----- | ---------- | --- | -------- | --- | ------ | ------ | --- | --- | --- |
| 5.1 State   | A    | —   | trend | domination |     | (shallow | /   | absent | basin) |     |     |     |
• Force: residual restoring force ≈ 0 or negative; deviations from µ∗ persist or extend.
• Flow: at any deviation, marginal continuation demand ≥ marginal contrarian supply.
Trend-aligned market orders keep arriving at the extremes; faders are absorbed or run over.
6

| State T | — Mean-Reversion |     | Ignition |     |     |     | Final Synthesis | & Freeze |
| ------- | ---------------- | --- | -------- | --- | --- | --- | --------------- | -------- |
• near unit-root; AR(1) of 1; basin around shallow or absent.
| Signature: |     | ε   |     | ε ≈ |     | µ∗  |     |     |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
• Why fades fail here: there is no well to fall into. A fade bets on a restoring force that
| does | not yet | exist. |     |     |     |     |     |     |
| ---- | ------- | ------ | --- | --- | --- | --- | --- | --- |
5.2 The A → T transition: causal order (this ordering is the thesis)
1. LEADS (earliest, hardest to see): the marginal trend force decays. Not the
trend — its increment. Aggressive trend-direction market orders thin; the rate of new
continuation demand falls. This is the trend-exhaustion mismatch: continuation weakens
faster than pullback weakens. The level can still be visibly trending while the marginal fuel
is gone. Economically, this is where someone — the exhausting trend-follower, the dealer
| who       | absorbed | the           | flow — experiences | the | change before | the crowd. |              |               |
| --------- | -------- | ------------- | ------------------ | --- | ------------- | ---------- | ------------ | ------------- |
|           |          |               |                    |     |               |            | If earliness | is possible   |
| anywhere, |          | it originates | here.              |     |               |            |              |               |
| 2.        |          |               |                    |     |               |            |              | The restoring |
THEN: reversion switches on at the edges first (band activation).
force appears outside the cost band before it appears near µ∗. The rim of the basin forms
before its floor; absorption at the extremes begins; deviations get rejected rather than
extended.
3. THEN: the basin deepens — critical speeding up becomes measurable. κ rises
from ≈ 0; AR(1) of ε falls; variance of ε around µ∗ contracts. A consequence of steps 1–2, so
it lags them slightly — but it is the first thing cleanly observable in price alone.
4. LAGS (last): recognition / crowding. Open interest builds, positioning concentrates,
| the | reversion | becomes | consensus. | The well | is now deep | known. |     |     |
| --- | --------- | ------- | ---------- | -------- | ----------- | ------ | --- | --- |
and
The single load-bearing sentence. The mechanism (steps 1–3) leads; recognition (step
4) lags; State T is the gap between them. Earliness equals the width of that gap.
If the gap is zero, T exists instantaneously and is untradeable. The whole alpha thesis
| reduces   | to one | question:  |                          |               |             |             |          |               |
| --------- | ------ | ---------- | ------------------------ | ------------- | ----------- | ----------- | -------- | ------------- |
|           |        |            | is that                  | gap positive, | stable, and | wide enough | to trade | net of costs? |
| 5.3 State | T      | — ignition | (formed-but-unrecognized |               |             | basin)      |          |               |
• Force: positive and strong enough that a costed fade has positive expectancy.
• marginal balance at the extremes has flipped — contrarian / absorbing supply now
Flow:
dominates continuation demand — but total participation is still light (low OI build, light
positioning).
• critical speeding up underway (κ ↑, AR(1) ↓, variance↓); balance forming around
Signature:
| µ∗; | |z| still | elevated | (a deviation | to fade exists); | crowding | low. |     |     |
| --- | --------- | -------- | ------------ | ---------------- | -------- | ---- | --- | --- |
5.4 State B — crowded / obvious reversion (deep, known basin)
| • Force: | high | and stable; | the well | is deep and | established. |     |     |     |
| -------- | ---- | ----------- | -------- | ----------- | ------------ | --- | --- | --- |
• marginal mean-reversion supply now dominates numerous; the trade is consen-
| Flow: |     |     |     |     | and | is  |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- |
sus.
• OI / positioning high; range long-established; spreads tight around the reversion
Signature:
trade.
7

State T — Mean-Reversion Ignition Final Synthesis & Freeze
• What ends the edge: competition. As in the documented decay of pairs trading, once
everyone fades every deviation, deviations are arbitraged away faster and smaller; expected
fade return falls below the risk-and-cost hurdle. The well is still there; the edge is gone.
5.5 Mechanical summary
Restoring Marginal flow AR(1) Crowd- Fade exp.
force at extremes of ε ing (net cost)
A ≈ 0 / neg. continuation buyers ≈ 1 low negative
T rising, positive contrarian (just flipped) falling low positive
B high, stable reversion crowd (many) low/stable high ≈ 0
Every column except crowding is monotone A → T → B. Crowding is the only
non-monotone separator of T from B. Any detector built solely on reversion-strength
variables fires loudest in State B — when the alpha is already gone. This single fact is
why the recognition axis is non-negotiable (Section 7, Mechanism 3).
6 Necessary and Sufficient Conditions
6.1 Necessary conditions (causal — without each, no edge)
N1 — Equilibrium exists over the horizon (S > 1).
µ∗ must be stable relative to the reversion being traded; the trend’s coherence time must
exceed the residual’s half-life. If µ∗ drifts as fast as ε reverts, there is nothing fixed to
revert to. This is the precondition for the word “residual” to mean anything. S > 1 is a
condition, not a mechanism — see Section 7 for why it is demoted from the mechanism
shortlist.
N2 — A net restoring force exists.
At deviations, marginal flow points back toward µ∗ (contrarian supply > continuation
demand at the extremes). This is the economic heart — the basin’s existence. Without it
there is only autocorrelation, not reversion.
N3 — The force beats round-trip costs.
Expected reversion in price exceeds spread + slippage + (futures) roll. This is the line
between statistical reversion (ε shrinks) and tradeable reversion (a fade makes money). It
is why sub-significant reversion may be real yet untradeable.
N4 — A fadeable deviation exists.
A |z| outside the cost band must be present. No deviation, no trade — even with a strong
force.
N5 — Bounded reversion time.
Reversion must complete within a horizon compatible with capital, risk limits, and µ∗’s
own stability. Infinite-horizon reversion is untradeable.
Causal chain: N1 enables N2; then N2 + N4 + N3 + N5 = profitable residual mean reversion.
Each is a link; break any one and the chain breaks.
8

| State T — | Mean-Reversion |     | Ignition |     |     |     |     |     |     | Final | Synthesis | &   | Freeze |
| --------- | -------------- | --- | -------- | --- | --- | --- | --- | --- | --- | ----- | --------- | --- | ------ |
6.2 The sufficient condition (what makes T early and tradeable)
S*
— N1–N5 hold and the mechanism-recognition gap is positive and cost-
clearing. Necessary conditions establish that reversion is tradeable; they do not establish
that it is early. The sufficient condition for State T specifically (as opposed to jumping
straight to a crowded State B) is that the basin (N1–N5) forms while positioning is still
light — the gap of Sections 5 and 8 is open and wider than costs. This is the only place
| “earliness” | enters, | and | it is | the whole | alpha. |     |     |     |     |     |     |     |     |
| ----------- | ------- | --- | ----- | --------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
6.3 Honest classification (demote weak ideas instead of hiding them)
• Causal requirements: N1–N5 and S*. These belong in any detector of T.
• (set the of the edge, not its existence): low crowding intensity, volatility
| Modulators |     |     | size |     |     |     |     |     |     |     |     |     |     |
| ---------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
compression, clean balance formation, sharp nonlinear activation, multi-timescale confirma-
tion.
• symptoms(movewith Tbutdonotcauseit): volatilitycompression, value-area
Coincident
| contraction, | falling | realized |     | range. | Do  | not promote |     | these | to causes. |     |     |     |     |
| ------------ | ------- | -------- | --- | ------ | --- | ----------- | --- | ----- | ---------- | --- | --- | --- | --- |
• (rejected as drivers): raw volatility level, dDRC/dt and other
| Non-causal                       | correlates |            |     |                   |     |     |            |         |     |     |     |     |     |
| -------------------------------- | ---------- | ---------- | --- | ----------------- | --- | --- | ---------- | ------- | --- | --- | --- | --- | --- |
| derivatives-of-noisy-statistics, |            |            |     | historical-analog |     |     | similarity | scores. |     |     |     |     |     |
| 7 The                            | Three      | Mechanisms |     |                   |     |     |            |         |     |     |     |     |     |
No feature zoo. Three mechanisms, each on a (orthogonality is
|     |     |     |     |     |     | different | raw | information |     | source |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | ----------- | --- | ------ | --- | --- | --- |
a property of inputs, not of labels), each mapping to a clause of the Section 3 definition, each
| surviving | adversarial | critique. |     |     |     |     |     |     |     |     |     |     |     |
| --------- | ----------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
7.1 Mechanism 1 — Basin formation / critical speeding up of ε
Source: price–time dynamics of the residual. Maps to the definition’s identity clause.
Intuition: “becomingmoremean-reverting”is therestoringforceturningup,andthechange leads
the level. Quantitatively, model the residual locally as a mean-reverting (Ornstein–Uhlenbeck /
AR(1)) process,
|     | dε = | −κε | dt+σdW |     | ⇐⇒  |     | ε = | ϕ ε | +η , | κ = −lnϕ | ,   |     | (2) |
| --- | ---- | --- | ------ | --- | --- | --- | --- | --- | ---- | -------- | --- | --- | --- |
|     | t    | t   |        | t   |     |     | t+1 | t t | t    | t        | t   |     |     |
with half-life HL = ln2/κ . The State-T signature is the joint, sign-locked movement
|     | t   |     | t   |              |     |     |      |         |     |      |     |     |     |
| --- | --- | --- | --- | ------------ | --- | --- | ---- | ------- | --- | ---- | --- | --- | --- |
|     |     | ∆κ  | >   | 0, ∆AR(1)(ε) |     |     | < 0, | ∆Var(ε) |     | < 0. |     |     | (3) |
|     |     |     | t   |              |     | t   |      |         | t   |      |     |     |     |
We track a filtered, bias-corrected speed state (a Kalman / local AR(1) estimate carrying its
posterior variance) and its short-horizon change ∆κ . This mechanism absorbs the old “nonlinear
t
activation” idea as the shape of the same basin — reversion switching on at the rim first — via
| the cheap   | split-slope   | proxy |       |          |           |     |     |     |     |     |     |     |     |
| ----------- | ------------- | ----- | ----- | -------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
|             |               |       |       | = κˆ(|z| | c)−κˆ(|z| |     | c), |     | 1,  |     |     |     | (4) |
|             |               |       | a     | t        | >         |     | <   |     | c ≈ |     |     |     |     |
| rather than | as a separate |       | axis. |          |           |     |     |     |     |     |     |     |     |
is worst-estimated near the unit root: the finite-sample bias is severe and
| Failure | mode. κ |     |     |     |     |     |     |     |     |     |     |     |     |
| ------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
downward exactly where the decision boundary sits, and the estimator variance is largest there.
9

| State T | — Mean-Reversion |     |     | Ignition |     |     |     |     | Final | Synthesis | &   | Freeze |
| ------- | ---------------- | --- | --- | -------- | --- | --- | --- | --- | ----- | --------- | --- | ------ |
If the filter’s posterior variance swamps the signal, this axis is uninformative.
|     |     |     |     |     |     |     |     |     |     | Mitigation: |     | never |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ----- |
trade a point estimate; use the ratio S t (below) where errors partially cancel, and uncertainty-
weight.
7.2 Mechanism 2 — Order-flow / inventory imbalance flip at extremes
Source: order flow / absorption (and its best available proxy). Maps to the definition’s cause
clause.
This is the microstructure carrier of the bifurcation — the flip from continuation-dominant to
reversion-dominant marginal flow at deviations. Two of the strongest economic theories unify
here:
• Trend-fuel exhaustion — the rate of new continuation demand falls while contrarian
supply at the extremes holds or rises, so the marginal balance flips at the rim.
• Inventory / risk-transfer completion — a large directional transfer completes, and
the liquidity providers who warehoused the opposite side must rebalance one-sided books,
| mechanically |     | pushing |     | price back | toward | value. |     |     |     |     |     |     |
| ------------ | --- | ------- | --- | ---------- | ------ | ------ | --- | --- | --- | --- | --- | --- |
This is not hypothetical. Intermediary-level data show inventory shocks generate price pressure
that predictably reverses: empirically, a $100,000 inventory shock moves price by about 0.28%
on average, with a 0.92 days. That number is double-edged — it confirms the
|     |     |     | half-life | of  | ≈   |     |     |     |     |     |     |     |
| --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
mechanism is real, and it warns that much of the reversion completes within a single daily bar
| (see the | daily-aliasing |     | risk, | Section | 9). |     |     |     |     |     |     |     |
| -------- | -------------- | --- | ----- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
Why it could precede T: the lead is structural and informational — the dealer knows their
own inventory, and marginal fuel dies, before the level turns. Failure mode: we cannot see
dealer inventory directly; OI / volume is a noisy daily proxy; and the ∼1-day half-life threatens
daily viability.
| 7.3 Mechanism |     |     | 3 — | Crowding | /   | recognition | lag |     |     |     |     |     |
| ------------- | --- | --- | --- | -------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
Source: open interest / positioning. Maps to the definition’s boundary clause. The crown jewel —
| and the | only | non-monotone |     | axis. |     |     |     |     |     |     |     |     |
| ------- | ---- | ------------ | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
A normalized measure of how recognized the trade already is: OI build-up against a contracting
| range; | for index | futures, |     | option-positioning |     | skew. | It is |       |        |       |           |     |
| ------ | --------- | -------- | --- | ------------------ | --- | ----- | ----- | ----- | ------ | ----- | --------- | --- |
|        |           |          |     |                    |     |       | low   | in A, | rising | in T, | saturated |     |
B. The futures-reversal literature is explicit: contrarian edge concentrates in
| in  |     |     |     |     |     |     |     |     |     | high-volume, |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- |
low-open-interest states — “reversion firing, not yet crowded” — which is the operational
| fingerprint | of  | T-vs-B. | Schematically, |     |     |     |     |     |     |     |     |     |
| ----------- | --- | ------- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∆OI
|     |     | =   |       | t            |     | T : low&rising, |     | B : | saturated. |     |     | (5) |
| --- | --- | --- | ----- | ------------ | --- | --------------- | --- | --- | ---------- | --- | --- | --- |
|     |     | C   |       |              | ,   | C               |     |     | C          |     |     |     |
|     |     | t   | range | / volatility |     | t               |     |     | t          |     |     |     |
t
Why it is indispensable: without a non-monotone axis, “before everyone else” is not a
measurable statement (Section 5). Every other variable is loudest when the alpha is gone.
OI / positioning quality and timeliness at daily frequency; the OI→crowding
| Failure | mode: |     |     |     |     |     |     |     |     |     |     |     |
| ------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
mapping may be too noisy. If this axis carries no information, Claim P is declared dead — not
papered over.
| 7.4 Why | everything |     |     | else | was rejected |     |     |     |     |     |     |     |
| ------- | ---------- | --- | --- | ---- | ------------ | --- | --- | --- | --- | --- | --- | --- |
• Timescale separation S — demoted to necessary condition N1. It states whether an
t
equilibrium exists to revert to, not what the transition. It is a precondition, not a
ignites
10

| State T | — Mean-Reversion |     | Ignition |     |     |     |     |     |     | Final Synthesis | &   | Freeze |
| ------- | ---------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------ |
mechanism, and it shares with Mechanism 1 by construction; kept only as the ratio
κ
|     |     |     |     | τ     | −1/lnρ |     |       |        |     |        |     |     |
| --- | --- | --- | --- | ----- | ------ | --- | ----- | ------ | --- | ------ | --- | --- |
|     |     |     | S = | µ,t = |        | µ,t | , AMR | regime | ⇐⇒  | S > 1, |     | (6) |
|     |     |     | t   |       |        |     |       |        |     | t      |     |     |
|     |     |     |     | HL    | ln2/κ  |     |       |        |     |        |     |     |
|     |     |     |     | t     |        | t   |       |        |     |        |     |     |
where ρ is the AR(1) persistence of µ∗-increments — the ratio form being where κ-errors
µ,t
| partially | cancel. |     |     |     |     |     |     |     |     |     |     |     |
| --------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
• Auction / balance acceptance — demoted to a coincident symptom. It is the observable
tapeexpression ofMechanisms1–2(exhaustion→rotationaroundvalue), notanindependent
cause, and likely collinear with the exhaustion signal. Retain only if it earns marginal
| information |     | after | orthogonalization. |     |     |     |     |     |     |     |     |     |
| ----------- | --- | ----- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
• Volatility-state transition — rejected as a cause; it is a symptom of balance forming and
| is largely |     | already | inside | and | .   |     |     |     |     |     |     |     |
| ---------- | --- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|            |     |         |        | z   | σ   |     |     |     |     |     |     |     |
eq
• Participation / liquidity-lag, reflexivity breakdown — rejected as too vague or circular
| to measure |     | cleanly | at daily | frequency. |     |     |     |     |     |     |     |     |
| ---------- | --- | ------- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
• Historical-analog similarity, dDRC/dt, per-bar SETAR/ESTAR—rejectedassample-
| starved | or  | derivative-of-noise |     |     | at daily | frequency. |     |     |     |     |     |     |
| ------- | --- | ------------------- | --- | --- | -------- | ---------- | --- | --- | --- | --- | --- | --- |
Three mechanisms, three sources (price–residual dynamics, order flow, positioning), three
| roles | (identity,            | cause, | boundary). |     | This | is  | the complete |     | frozen set. |          |     |     |
| ----- | --------------------- | ------ | ---------- | --- | ---- | --- | ------------ | --- | ----------- | -------- | --- | --- |
| 8 The | Mechanism-Recognition |        |            |     |      |     | Gap:         | the | Alpha       | Question |     |     |
This is the most important section. Everything else can be right and the thesis still dies here.
The question: can the restoring mechanism emerge before the crowd recognizes it, by a margin
| wide enough   |     | to trade? |     |     |     |          |     |     |     |     |     |     |
| ------------- | --- | --------- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
| 8.1 Strongest |     | argument  |     | FOR | a   | positive | gap |     |     |     |     |     |
The lead is informational, not lucky. Three independent reasons:
|     | structural |     | and |     |     |     |     |     |     |     |     |     |
| --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1. Inventory asymmetry of information. The market-maker who warehoused the trend’s
opposite side knows their own book before any public series reveals reversion. Their rebalanc-
ing the contrarian flow, and it begins from private information; the documented inventory
is
| price             | pressure | confirms |               | the channel |       | is real. |            |     |          |           |            |     |
| ----------------- | -------- | -------- | ------------- | ----------- | ----- | -------- | ---------- | --- | -------- | --------- | ---------- | --- |
| 2.                |          |          |               |             | Trend |          | exhaustion | is  | a change | in the    | of demand. |     |
| Marginal-vs-level |          |          | invisibility. |             |       |          |            |     |          | increment |            |     |
It is invisible in the price (still trending) and shows only in flow / acceleration — so
level
it necessarily precedes obvious reversion in the level. The lead is built into the order of
observability.
3. Recognition has a time constant. Crowding requires many participants to independently
notice, allocate capital, and act. Capital reallocation is not instantaneous; positioning
| concentrates  |     | over     | days-to-weeks, |         | not | ticks. |     |     |     |     |     |     |
| ------------- | --- | -------- | -------------- | ------- | --- | ------ | --- | --- | --- | --- | --- | --- |
| 8.2 Strongest |     | argument |                | AGAINST |     |        |     |     |     |     |     |     |
Anything visible in public price / OI is, by construction, available to everyone at
The genuine informational lead belongs to those who see order flow — which we do
| once. |     |     |     |     |     |     |     |     | private |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- |
not. In a near-efficient market the basin becomes measurable from public data at approximately
11

| State T | — Mean-Reversion | Ignition |     |     |     |     | Final Synthesis | & Freeze |
| ------- | ---------------- | -------- | --- | --- | --- | --- | --------------- | -------- |
the moment it gets priced; the public-data gap is competed toward zero. Worse, the one
mechanism with a documented lead (inventory) has a ∼1-day half-life, so by the time a daily
| bar prints, | the lead      | may already | be spent.    |     |     |              |            |           |
| ----------- | ------------- | ----------- | ------------ | --- | --- | ------------ | ---------- | --------- |
| 8.3 Final   | verdict       |             |              |     |     |              |            |           |
| The         | gap plausibly | exists      | in principle | and | is  |              |            | — but its |
|             |               |             |              |     | not | structurally | impossible |           |
publicly observable, daily-frequency width is the binding unknown, and the prior should
be that it is small, possibly sub-cost, and possibly aliased below the daily bar. The FOR
argument defeats the strong claim “early is impossible.” The AGAINST argument defeats
the strong claim “early is easy.” What survives is the modest, correct position: a thin,
capacity-limited, possibly-positive public gap whose existence is an empirical question, not a
one. Theory cannot adjudicate. The lead–lag test (P2, Section 12) adjudicates.
theoretical
| 9 Illusion | Risks, | Ranked |     |     |     |     |     |     |
| ---------- | ------ | ------ | --- | --- | --- | --- | --- | --- |
An aggressive attempt to show T is an artifact, ranked by how lethal and how insidious each
risk is.
µ∗-construction
| Rank 1 | —   |     | illusion | (most | dangerous). |     |     |     |
| ------ | --- | --- | -------- | ----- | ----------- | --- | --- | --- |
With µ∗ frozen and necessarily lagging, apparent “reversion” can be µ∗ mechanically catching
up to price rather than price returning to a contemporaneous equilibrium. The critical-
speeding-up signature can be by the filter’s tracking dynamics — it would
manufactured
pass every signature test while being pure artifact. Ranked first because it is invisible to the
signature itself; only a µ∗-perturbation test exposes it, and it is specific to this frozen-µ∗
setup.
Test: P3.
| Rank 2 | — Recognition |     | coincidence | (no | earliness | gap). |     |     |
| ------ | ------------- | --- | ----------- | --- | --------- | ----- | --- | --- |
The basin becomes measurable exactly when it gets priced; T collapses instantly into B; the
edge is real-but-uncapturable. This is the Section 8 objection and the direct attack on Claim
P. Ranked second only because it does not make the reversion fake — it makes the earliness
| fake.  | Test: P2.         |     |           |     |     |     |     |     |
| ------ | ----------------- | --- | --------- | --- | --- | --- | --- | --- |
| Rank 3 | — Daily-frequency |     | aliasing. |     |     |     |     |     |
The bifurcation forms and completes within a day (the inventory half-life is ∼1 day), so daily
sampling averages it away. T is real intraday, invisible daily. Promoted from a tail risk to a
live risk by the half-life finding. Test: base-rate / clustering at daily; intraday fallback if they
fail.
| Rank 4 | — Random | timing | / overfit. |     |     |     |     |     |
| ------ | -------- | ------ | ---------- | --- | --- | --- | --- | --- |
Profitable fades are realized noise; “early” is survivorship over the bets that happened to
work. The most controllable risk: defeated by clustering tests (is the event series non-IID?)
| and | a locked out-of-sample |     | hold-out. | Test: | P4. |     |     |     |
| --- | ---------------------- | --- | --------- | ----- | --- | --- | --- | --- |
The ordering drives the gate sequencing: Ranks 1–2 are the high-value, theory-proof failure
channels and must be tested first and cheaply, before any build. Ranks 3–4 are handled by
| frequency       | and hold-out | discipline. |               |     |     |     |     |     |
| --------------- | ------------ | ----------- | ------------- | --- | --- | --- | --- | --- |
| 10 Quantitative |              | Target      | Formalization |     |     |     |     |     |
12

State T — Mean-Reversion Ignition Final Synthesis & Freeze
The target is the ground truth every later test is validated against. If it is circular or leaky, every
downstream result is fiction. The hard constraints: (R1) use only information up to decision
time plus forward realized prices (no look-ahead in features); (R2) the target must not be defined
using κ, half-life, or MRScore — the very things we predict; (R3) operate on ε = P −µ∗; (R4) be
economically realistic (costs, slippage, roll, bounded horizon); (R5) separate statistical reversion
(ε shrinks) from tradeable reversion (a costed fade makes money).
10.1 Notation
The residual is ε = P −µˆ∗. Volatility is the model-free realized vol σRV (rolling realized vol of
t t t t
returns — deliberately not σ , which contains κ). The standardized deviation is
eq
ε
z = t . (7)
t σRV
t
An “entry” is considered only when |z | ≥ z (e.g. 1.0–1.5): we label fade opportunities, not
t entry
all bars.
10.2 The five candidate formulations
# Formulation Circular? Stat vs. trade Verdict
C1 Next-bar partial reversion, clean statistical only Reject
sign(∆ε) over 1 bar
C2 Fixed-horizon net P&L of clean tradeable Primary
fading ε to µ∗ over H bars
C3 Triple-barrier on ε, raw-σRV clean tradeable Primary (preferred)
barriers, fixed H
C4 Triple-barrier, σ barriers, leaks (κ) tradeable Secondary (realism only)
eq
half-life-scaled H
C5 OU-optimal analytic net re- leaks (κ) tradeable Benchmark only
turn (Bertram / Leung–Li)
10.3 The recommended target: C3 primary
For each candidate entry at time t with |z | ≥ z , set three barriers and take the first touch
t entry
within a fixed horizon H bars:
• Profit barrier (partial reversion): price moves toward µ∗ by g·σRV with g ≈ 0.5 (partial,
t
not full reversion — full reversion is rarely realized and overstates edge).
• Stop barrier: the residual expands by s·σRV (e.g. s ≈ 1.0) — the genuine risk of fading
t
inside a trend.
• Time barrier: fixed H ∈ {5,10,20} bars, pre-registered, not tuned per series.
The label is the continuous signed net return of the fade at first touch, in σRV units (comparable
across instruments), net of spread + slippage + (futures) roll:
(realized fade P&L at first touch)−costs
y = . (8)
t σRV
t
13

| State T | — Mean-Reversion | Ignition |     |     |     | Final Synthesis |     | & Freeze |
| ------- | ---------------- | -------- | --- | --- | --- | --------------- | --- | -------- |
Crucially, barriers and horizon are in model-free units: does not contain and is
|     | both |     |     |     | σRV |     | κ   | H   |
| --- | ---- | --- | --- | --- | --- | --- | --- | --- |
a fixed constant, so the label cannot validate the model against itself. Convert to a binary
y t
{tradeable fade = 1} only at the decision stage, at a pre-registered net-return hurdle.
| 10.4 | Secondary | and benchmark |     |     |     |     |     |     |
| ---- | --------- | ------------- | --- | --- | --- | --- | --- | --- |
C4 (barriers in σ , horizon scaled to half-life) is the “how it would actually be traded” version
eq
— used to confirm C3’s events are not artifacts of an unrealistic fixed horizon. Require
only
| C3 and | C4 to   | agree. | C5 (closed-form | OU optimum) |          |          | for   | from |
| ------ | ------- | ------ | --------------- | ----------- | -------- | -------- | ----- | ---- |
|        | broadly |        |                 |             | sets the | defaults | g,s,H |      |
theory, then they are frozen and sensitivity-tested rather than optimized; it also gives an analytic
yardstick — realized C3 returns wildly above the OU-optimal expectation signal a labelling bug
or look-ahead.
| 11 The | Existence | Gate: | Experimental |     | Design |     |     |     |
| ------ | --------- | ----- | ------------ | --- | ------ | --- | --- | --- |
falsify, cheaply, any feature engineering. The design is deliberately minimal
| Purpose: |     | before |     |     |     |     |     |     |
| -------- | --- | ------ | --- | --- | --- | --- | --- | --- |
and hostile to its own thesis. It answers three questions in order, and any one failing stops the
build.
| 11.1 | Data and | scope (deliberately |     | narrow) |     |     |     |     |
| ---- | -------- | ------------------- | --- | ------- | --- | --- | --- | --- |
• Instruments: one liquid index future (NIFTY) and one liquid commodity future (different
microstructure / carry — a genuine out-of-sample-in-spirit check). Resist adding more;
| breadth | is how | false discoveries | enter. |     |     |     |     |     |
| ------- | ------ | ----------------- | ------ | --- | --- | --- | --- | --- |
• Frequency: daily bars first (the contested band); intraday held in reserve.
• as long a clean history as µ∗ supports; reserve the most recent 20–30% as a
| Sample:  |           |           |      |     |     |     |     | locked |
| -------- | --------- | --------- | ---- | --- | --- | --- | --- | ------ |
| hold-out | untouched | until the | end. |     |     |     |     |        |
• real spread + slippage + roll, set conservatively. Under-costing is the easiest way to
Costs:
| manufacture | a fake    | edge.     |     |     |     |     |     |     |
| ----------- | --------- | --------- | --- | --- | --- | --- | --- | --- |
| 11.2        | The three | questions |     |     |     |     |     |     |
1. Are tradeable-fade events non-trivial in number? (Base rate — tests Claim E.)
Report the base rate of tradeable fades among |z| ≥ z candidates, by instrument and
entry
| year, | and conditional | on trend | strength. |     |     |     |     |     |
| ----- | --------------- | -------- | --------- | --- | --- | --- | --- | --- |
2. Do tradeable events cluster in time? (Non-IID — necessary for predictability.)
Ljung–Box / runs test on the binary event series; dispersion index (variance/mean of events-
per-window) versus 1; empirical inter-event-time distribution versus exponential. If events
are temporally indistinguishable from random, there is no regime to detect.
3. Is there any precursor structure? (Predictability probe.) For each of the ≤ 5
pre-registered axes, compute simple summary statistic as of decision time and test
one
forward association with the C3 label under: purged + embargoed cross-validation; sample-
uniqueness weighting; a block-bootstrap null (the comparison is against block-shuffled data
that preserves autocorrelation but destroys the precursor→event link); and multiple-testing
control (Bonferroni / Benjamini–Hochberg over the pre-registered axes). Run the crowding
axis C as a separate, explicit test of Claim P: does it separate early (sustained-edge) from
t
| crowded | (immediate-decay) |     | fades? |     |     |     |     |     |
| ------- | ----------------- | --- | ------ | --- | --- | --- | --- | --- |
14

| State | T — Mean-Reversion |     | Ignition         |     |          |                 |     | Final Synthesis | & Freeze |
| ----- | ------------------ | --- | ---------------- | --- | -------- | --------------- | --- | --------------- | -------- |
| 11.3  | Kill criteria      |     | (pre-registered, |     | numeric, | non-negotiable) |     |                 |          |
| K1    | (base rate)        |     |                  |     |          |                 |     |                 |          |
Tradeable-fadebaseratebelow∼5%consistentlyonbothinstruments⇒phenomenon
|     | too thin | at daily |     | drop to intraday |     | or stop. |     |     |     |
| --- | -------- | -------- | --- | ---------------- | --- | -------- | --- | --- | --- |
⇒
K2 (clustering)
EventseriesstatisticallyindistinguishablefromIIDonbothinstruments⇒noregime
|     | to detect      | ⇒   | stop or | go intraday. |     |     |     |     |     |
| --- | -------------- | --- | ------- | ------------ | --- | --- | --- | --- | --- |
| K3  | (no precursor) |     |         |              |     |     |     |     |     |
No axis beats the block-bootstrap null after correction, on purged CV, on both
|     | instruments |     | Claim | P rejected. |     |     |     |     |     |
| --- | ----------- | --- | ----- | ----------- | --- | --- | --- | --- | --- |
⇒
| K4  | (no earliness) |     |     |     |     |     |     |     |     |
| --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
fails to separate early from crowded the claim is dead; at best a lagging
|     | C   |     |     |     |     | ⇒ alpha |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- |
t
|     | MR filter, | not       | an ignition | detector. |     |     |     |     |     |
| --- | ---------- | --------- | ----------- | --------- | --- | --- | --- | --- | --- |
| K5  | (hold-out  | collapse) |             |           |     |     |     |     |     |
Any surviving signal vanishes on the locked recent hold-out ⇒ overfit ⇒ stop.
| 11.4 | Daily-viability |     | decision | rule |     |     |     |     |     |
| ---- | --------------- | --- | -------- | ---- | --- | --- | --- | --- | --- |
• Daily survives if K1–K3 pass on daily for both instruments with economically meaningful
base rate and at least one robust precursor axis proceed to Stage 3 at daily frequency.
⇒
• Drop to intraday if K1 or K2 fails on daily but the reversion regime is plausibly reachable
at higher frequency re-run the identical protocol on intraday bars building anything.
|     |     |     | ⇒   |     |     |     |     | before |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- |
• Stop if the phenomenon fails at both frequencies, or exists (Claim E) but is never early (K4)
— in which case the honest pivot is to a non-early residual-MR filter, explicitly abandoning
| the | alpha-from-earliness |        | thesis. |      |       |          |      |     |     |
| --- | -------------------- | ------ | ------- | ---- | ----- | -------- | ---- | --- | --- |
| 12  | Decisive             | Tests: |         | What | Would | Prove or | Kill | T   |     |
The definition is engineered to be falsifiable. It stands or falls on four tests. Run the two that
| target | the un-killable-by-theory |     |         | risks           | (P2, P3) | first. |     |     |     |
| ------ | ------------------------- | --- | ------- | --------------- | -------- | ------ | --- | --- | --- |
| Would  | PROVE                     |     | T (all  | four required): |          |        |     |     |     |
| P1     | — Signature,              |     | correct | signs.          |          |        |     |     |     |
Around historical tradeable-fade clusters, ε shows critical speeding up (κ ↑, AR(1) ↓,
variance↓) with theory-predicted signs, beyond a block-bootstrap null.
| P2  | — Mechanism |     | leads | recognition. |     |     |     |     |     |
| --- | ----------- | --- | ----- | ------------ | --- | --- | --- | --- | --- |
The signature and/or order-flow flip OI / positioning build-up by a positive,
precede
stable margin. This single number — the gap width — is the empirical heart of the
programme.
| P3  | — µ∗-robustness. |     |     |     |     |     |     |     |     |
| --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
P1 and P2 survive small perturbations of µ∗; reversion is toward a contemporaneous
|     | equilibrium, |     | not µ∗ | catch-up.     |     |              |     |     |     |
| --- | ------------ | --- | ------ | ------------- | --- | ------------ | --- | --- | --- |
| P4  | — Clustering |     | and    | out-of-sample |     | persistence. |     |     |     |
Tradeable events are non-IID and the signature/lead survives on a locked hold-out
|     | and a | second | instrument. |     |     |     |     |     |     |
| --- | ----- | ------ | ----------- | --- | --- | --- | --- | --- | --- |
15

| State T — | Mean-Reversion |        | Ignition |           |     |        |                 |     | Final Synthesis  | & Freeze |
| --------- | -------------- | ------ | -------- | --------- | --- | ------ | --------------- | --- | ---------------- | -------- |
|           |                |        |          | signature |     | absent | or wrong-signed |     | (identity wrong; | stop);   |
| Would     | KILL           | T (any | one):    |           |     |        |                 |     |                  |          |
gap ≤ 0 (T exists but never early; pivot or stop); signature vanishes under µ∗ perturbation
(construction artifact; stop); events IID or effect dies out-of-sample (random timing /
| overfit; | stop). |     |     |     |     |     |     |     |     |     |
| -------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
P2 and P3 are the decisive, cheap, theory-proof tests. Run them — and
| Design | discipline. |     |     |     |     |     |     |     |     |     |
| ------ | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
the descriptive gates K1 (base rate) and K2 (clustering) — before committing to any feature or
model program. These specific tests are the whole gate; no feature creep.
| 13 The | Frozen |     | Blueprint |     |     |     |     |     |     |     |
| ------ | ------ | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
13.1 Frozen (decided — do not reopen without strong new evidence)
| • The |     | (Section |     | 3): one definition, |     | no  | alternatives. |     |     |     |
| ----- | --- | -------- | --- | ------------------- | --- | --- | ------------- | --- | --- | --- |
definition
• The ontology (Section 4): latent transition window — bifurcation → critical speeding up →
| hazard | schedule | →   | order-flow | flip. |     |     |     |     |     |     |
| ------ | -------- | --- | ---------- | ----- | --- | --- | --- | --- | --- | --- |
• The A → T → B mechanics (Section 5), including “crowding is the only non-monotone
separator.”
| •         |     |            |     |       |                |     |           | S*  | (Section 6). |     |
| --------- | --- | ---------- | --- | ----- | -------------- | --- | --------- | --- | ------------ | --- |
| Necessary |     | conditions |     | N1–N5 | and sufficient |     | condition |     |              |     |
• The three-mechanism set (Section 7): basin formation (identity), order-flow / inventory
| flip (cause), |     | crowding | lag | (boundary). |     |     |     |     |     |     |
| ------------- | --- | -------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
• The target spec: C3 model-free triple-barrier primary; C4 quarantined realism check; κ
| never | enters | the primary |     | target. |     |     |     |     |     |     |
| ----- | ------ | ----------- | --- | ------- | --- | --- | --- | --- | --- | --- |
• The kill criteria and prove/kill tests: K1, K2, P1–P4 with pre-registered thresholds.
13.2 Deferred (revisit only if the gate passes and a specific need appears)
• Auction/balanceaxis(admittedonlyifitearnsmarginalinformationafterorthogonalization).
• Vol-of-vol collapse (candidate 6th axis, on demonstrated marginal information only).
• Historical-analog layer (sample-starved), DMA / adaptive weighting (event-starved), full
| SETAR/ESTAR |     | per | bar | (infeasible), | multi-timeframe |     | confirmation. |     |     |     |
| ----------- | --- | --- | --- | ------------- | --------------- | --- | ------------- | --- | --- | --- |
• All signal construction, sizing, and exit optimization (Layer 5 — premature by design).
| 13.3 Removed   |                      | (rejected       |     | — do        | not | resurrect) |              |     |     |     |
| -------------- | -------------------- | --------------- | --- | ----------- | --- | ---------- | ------------ | --- | --- | --- |
| • T-as-a-point |                      | / instantaneous |     | structural  |     | break.     |              |     |     |     |
| • HMM          | smoothed-probability |                 |     | definitions |     | (embed     | look-ahead). |     |     |     |
• Timescale separation as a mechanism (it is necessary condition N1).
• dDRC/dt and derivatives-of-noisy-statistics; raw vol level; historical-analog similarity as an
axis.
• Any symmetric (sign-blind) architecture — condition on sign(ε) relative to trend.
16

State T — Mean-Reversion Ignition Final Synthesis & Freeze
13.4 The one open question, and the only authorized next work
Open question. Whether the publicly observable, daily-frequency mechanism-recognition
gap is positive, stable, and cost-clearing. This is not a theory question; it is resolved by
P2 (lead–lag) and P3 (µ∗-robustness), gated by K1 (base rate) and K2 (clustering), on
NIFTY-daily + one liquid commodity-daily, with the intraday fallback pre-specified.
Next action. (1) Lock the target spec (C3 primary, C4 secondary, defaults from the OU
optimum) as a frozen pre-registration — 1–2 days. (2) Run the gate — ∼1–2 weeks. (3)
Decide by the kill criteria, not by hope. This layer is now frozen; do not re-theorize State
T. Run the gate, then move forward.
A Notation and Key Formulae (frozen for this phase)
Quantity Definition
Residual ε = P −µˆ∗
t t t
Model-free standardization z = ε /σRV, σRV = rolling realized vol of returns
t t t
OU / AR(1) link ε = ϕ ε +η , κ = −lnϕ
t+1 t t t t t
Half-life HL = ln2/κ
t t
√
Stationary OU std (not in primary tar- σ = σ/ 2κ
eq
get)
Trend coherence time τ = −1/lnρ , ρ = AR(1) of ∆µˆ∗
µ,t µ,t µ,t t
Timescale separation (spine) S = τ /HL ; AMR regime ⇐⇒ S > 1
t µ,t t t
Nonlinear activation proxy a = κˆ(|z| > c)−κˆ(|z| < c), c ≈ 1
t
Critical-speeding-up signature ∆κ > 0, ∆AR(1)(ε) < 0, ∆Var(ε) < 0
Crowding axis (non-monotone) C = ∆OI /(range/vol)
t t t
Fade label (C3) y = [fade P&L at first touch−costs]/σRV
t t
B Pre-Registration Checklist (fill before touching data)
Instruments; sample split and locked hold-out dates; z ; g, s, H grid; cost model (spread,
entry
slippage, roll); σRV window; the ≤ 5 axes and the single summary statistic per axis; the
binarization hurdle; CV scheme (purge + embargo lengths); bootstrap scheme (block length);
multiple-testing method; and the numeric values of K1–K5. No statistic is computed until this
page is filled and frozen.
Selected References
1. Scheffer et al. (2009), Early-warning signals for critical transitions, Nature 461:53–59.
2. Critical speeding up as an early warning signal of regime switching, arXiv:1901.08084.
3. Balke & Fomby (1997), Threshold Cointegration, International Economic Review 38:627–645.
17

| State T — | Mean-Reversion | Ignition |     |     |     |     | Final Synthesis | & Freeze |
| --------- | -------------- | -------- | --- | --- | --- | --- | --------------- | -------- |
4. Kapetanios, Shin & Snell (2003), Testing for a Unit Root in the Nonlinear STAR Framework, J.
| Econometrics | 112:359–379.  |                  |        |               |              |         |         |             |
| ------------ | ------------- | ---------------- | ------ | ------------- | ------------ | ------- | ------- | ----------- |
| 5. Safari    | & Schmidhuber | (2025),          |        |               |              |         |         |             |
|              |               |                  | Trends | and Reversion | in Financial | Markets | on Time | Scales from |
| Minutes      | to Decades,   | arXiv:2501.16772 |        | (Physica A).  |              |         |         |             |
6. Hendershott & Menkveld (2014), Pressures, Journal of Financial Economics.
Price
| 7. Hamilton, | Regime-Switching |     | Models. |     |     |     |     |     |
| ------------ | ---------------- | --- | ------- | --- | --- | --- | --- | --- |
8. Bertram (2010), Analytic Solutions for Optimal Statistical Arbitrage Trading, Physica A 389:2234–
2243.
9. Leung & Li (2015), Optimal Mean Reversion Trading with Transaction Costs and Stop-Loss Exit,
arXiv:1411.5062.
| 10. Avellaneda | & Lee (2010), |             |     |                  |             | Market. |     |     |
| -------------- | ------------- | ----------- | --- | ---------------- | ----------- | ------- | --- | --- |
|                |               | Statistical |     | Arbitrage in the | US Equities |         |     |     |
11. Gatev,Goetzmann&Rouwenhorst(2006),Pairs Trading: Performance of a Relative-Value Arbitrage
Rule.
12. Yu (2012), Bias in the estimation of the mean-reversion parameter, J. Econometrics 169:114–122.
13. López de Prado (2018), Advances in Financial Machine Learning (triple-barrier, purged CV, meta-
labelling).
|     |     | End | of report | — State T frozen. | Next: run | the gate. |     |     |
| --- | --- | --- | --------- | ----------------- | --------- | --------- | --- | --- |
18
