export const meta = {
  name: 'habitat-economic-adjudication',
  description: 'Trader-first stress-test: is forward habitat-state persistence ECONOMICALLY meaningful, not merely statistically persistent? + hard anti-State-T firewall. Pure adjudication, no execution.',
  whenToUse: 'Gate before STEP 0: decide whether surviving delta_excess>0 would change any trader decision, or is true-but-inert / a hidden State-T confidence object',
  phases: [
    { title: 'Lenses', detail: 'trader/PM lead · useless-but-persistent prosecutor · econometrician (state-vs-noisy-estimator) · firewall architect' },
    { title: 'Adjudicate', detail: 'Reconcile to one economic verdict + minimal deployability criterion + exact success/failure condition + firewall; write artifact' },
  ],
}

const DOCTRINE = `
AMR DOCTRINE — BINDING (CLAUDE.md). RESEARCH MODE. PURE ADJUDICATION — NO empirical execution, NO STEP 0, NO data touched.
- §11.2 trader lens is a PRIORITIZATION constraint, never a rigor relaxation. The deployable object is a BOOK after costs (transaction cost · borrow · capacity · sizing · drawdown · adverse excursion), NOT an instrument. A statistically-persistent-but-uneconomic object is a NON-FINDING.
- §4 ZOMBIE PROHIBITION: State T (predict/classify/TIME reversion; "MR likely soon"; entry-confidence) is DEAD (doc 11). Banned vocab: T-score, hazard, ignition, imminent, favorable-now.
- Habitat ≠ signal. Habitat persistence ≠ transition/entry prediction. Persistence informs WHICH market is in scope, never WHEN to act within it.
- Significance over narrative; surrogate-relative; cross-habitat OOS is the unit of evidence; incremental value over a cheap baseline is mandatory, not optional.
`

const SETTLED = `
WHAT IS ALREADY SETTLED (doc 25, EMPIRICALLY_DECIDABLE, unanimous; do NOT relitigate):
- The object = forward HABITAT-STATE persistence: a SIGN-FREE latent second-moment regime transition probability. P(habitat in [t+1+g, t+h] | habitat in [t-k,t]), measured surrogate-relative as delta_excess = delta_real - delta_surrogate (vs worst-case most-persistent matched null). It emits NO tense about price, NO deviation/z anchoring, NO entry timing.
- Statistically it is admissible-and-decidable (structurally like GARCH vol-clustering / Hamilton p_HH persistence), NOT a definitional tautology, NOT a priori valid. The empirical run is pre-registered but GATED (not yet authorized).
- Prior State-T kill was PARTITIONED: forward PRICE-REVERSAL prediction stays dead; forward HABITAT-STATE persistence is the reopened, distinct estimand.

THIS PASS IS A DIFFERENT QUESTION — ECONOMIC, not statistical. ASSUME delta_excess>0 survives every null. Then: why should a trader care?
`

const THE_TASK = `
ADJUDICATE, trader-first:
1. ECONOMIC DECISION CHANGED: what concrete book/PM decision does habitat persistence change, IF the decision is allowed to be only universe-membership / capital-allocation / sizing / attention — and explicitly NOT entry timing or direction? Be specific about the decision's unit (instrument-in-MR-universe-this-period; capital weight), horizon, and rebalance.
2. MR ATTEMPT SELECTION: could persistence improve SELECTION of which instruments/spreads receive MR-strategy capital? Distinguish persistence of the ENVIRONMENT DESCRIPTOR from persistence of REALIZED MR PROFITABILITY — only the latter has P&L, and entry timing (which drives realized P&L) is State T, off-limits. So can selection-only value exist without touching timing?
3. PRACTICAL-USELESSNESS FALSIFIERS: enumerate the ways delta_excess>0 survives yet the object is practically useless: (a) persistence horizon h shorter than classification-lag + reallocation-cost horizon (no actionable window); (b) high unconditional base-rate of "habitat" => trivial conditional lift / low marginal information; (c) book-level net-of-cost improvement within noise of a CHEAP baseline (realized-vol / half-life / VR filter) => no incremental value; (d) turnover cost of rotating capital as habitat flips exceeds the edge; (e) capacity/borrow constraints on the eligible instruments. For each, the exact condition under which it fires.
4. HIDDEN STATE-T DRIFT: does this risk becoming a covert State-T CONFIDENCE object ("high-confidence MR habitat" -> "MR likely soon" -> entry weight)? Map the exact drift path and the structural firewall that makes it impossible (output TYPE constraint: universe/weight, never per-bar score, never composed with a deviation/z/entry trigger).
5. LATENT-ASSUMPTION CHALLENGE: attack the assumption that "habitat" is a STABLE, ECONOMICALLY MEANINGFUL STATE rather than a SLOW NOISY ESTIMATOR (a smoothed lag of vol/VR with measurement memory). If it is mostly a smoother, persistence is autocorrelation-of-a-smoother (the surrogate cancels mechanical part — but) is the residual latent state economically real, and is it captured more cheaply by a direct measure? Demand an INCREMENTAL-VALUE test vs the cheap baseline.

REQUIRED OUTPUTS (the adjudication must deliver all four, crisply):
- TRADER USEFULNESS VERDICT (one of: economically-useful-if-X / true-but-inert / undeployable; with the conditions).
- ZOMBIE-STATE-T RISK ASSESSMENT (level + the exact drift path + the firewall that blocks it).
- MINIMAL DEPLOYABILITY CRITERION (the smallest set of conditions that would make this worth deploying as a book-level allocation/selection prior).
- EXACT ECONOMIC SUCCESS/FAILURE CONDITION (a pre-registerable, net-of-cost, cross-habitat-OOS, incremental-vs-baseline, selection-only condition that declares economic value PRESENT vs ABSENT).
`

const LENS_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['lens', 'headline', 'decision_changed', 'selection_value', 'uselessness_falsifiers', 'state_t_drift', 'state_assumption_attack', 'usefulness_verdict', 'minimal_deployability', 'success_failure_condition', 'one_line'],
  properties: {
    lens: { type: 'string' },
    headline: { type: 'string' },
    decision_changed: { type: 'string', description: 'the concrete book decision habitat persistence changes (universe/weight/sizing only)' },
    selection_value: { type: 'string', description: 'can it improve MR attempt SELECTION without touching timing? environment-descriptor vs realized-profitability distinction' },
    uselessness_falsifiers: { type: 'array', items: { type: 'string' }, description: 'concrete ways persistence survives yet is practically useless, each with its firing condition' },
    state_t_drift: { type: 'string', description: 'zombie-State-T risk: the drift path + the firewall that blocks it' },
    state_assumption_attack: { type: 'string', description: 'is habitat a stable economic state or a slow noisy estimator? incremental value vs cheap baseline' },
    usefulness_verdict: { type: 'string', enum: ['ECONOMICALLY_USEFUL_IF', 'TRUE_BUT_INERT', 'UNDEPLOYABLE'], description: 'this lens\'s economic call' },
    minimal_deployability: { type: 'array', items: { type: 'string' }, description: 'smallest conditions that make it worth deploying' },
    success_failure_condition: { type: 'string', description: 'the exact net-of-cost, OOS, incremental, selection-only condition declaring value present vs absent' },
    one_line: { type: 'string' },
  },
}

phase('Lenses')

const LENSES = [
  { key: 'trader-pm', brief: 'Institutional trader / PM running a 1-12 week MR book — THE LEAD LENS. You decide capital allocation across an MR-eligible universe. Answer brutally: does knowing "this instrument\'s mean-reversion-friendly regime is likely to persist over the next h" change how you allocate, size, or build your watchlist — given you may NOT use it to time entries? State the actual decision, horizon, rebalance, and the edge magnitude that would move real risk vs be noise. If it does not change a decision you would actually make, say UNDEPLOYABLE.' },
  { key: 'useless-prosecutor', brief: 'Adversary tasked with the SPECIFIC thesis: delta_excess>0 survives every null AND the object is economically worthless. Build the strongest possible "persistent-but-useless" case: trivial base-rate lift, horizon shorter than the actionable window, no incremental value over a 1-line realized-vol/half-life filter, turnover eats the edge, capacity binds. Default to USELESS unless the trader lens produces a decision that genuinely needs THIS object and not a cheaper proxy.' },
  { key: 'econometrician', brief: 'Quant econometrician. Attack the latent assumption that "habitat" is a stable economically-meaningful STATE vs a slow noisy ESTIMATOR (smoothed lag of vol/VR). Even with the surrogate cancelling mechanical autocorrelation, is the residual latent state (i) economically real (does it change the PAYOFF to MR strategies, not just a vol descriptor) and (ii) better captured by THIS object than by a direct cheap measure? Specify the incremental-value test: habitat-persistence filter vs trivial-baseline filter, net-of-cost, OOS.' },
  { key: 'firewall-architect', brief: 'Doctrine / systems firewall architect. Prove (or disprove) that this object CANNOT accidentally become "MR likely soon" / a State-T confidence input. Specify the structural firewall as an OUTPUT-TYPE constraint (universe-membership / capital-weight at book level; NEVER a per-bar score; NEVER composed with a deviation/z-score/entry trigger; NEVER a tense-bearing "soon"). Map every drift path from habitat-persistence-probability to entry-confidence and the structural block for each. Assess zombie risk level honestly.' },
]

const lensResults = (await parallel(LENSES.map(L => () =>
  agent(
    `${DOCTRINE}\n\n${SETTLED}\n\n${THE_TASK}\n\n` +
    `YOU ARE THE ${L.key.toUpperCase()} LENS: ${L.brief}\n\n` +
    `Adjudicate decisively from your lens. Converge to ONE position, not a survey. Deliver all four required outputs (usefulness verdict · zombie risk · minimal deployability · exact success/failure condition) crisply and concretely.`,
    { label: `lens:${L.key}`, phase: 'Lenses', schema: LENS_SCHEMA })
))).filter(Boolean)

const lensBrief = lensResults.map(l =>
  `## LENS: ${l.lens}\nHEADLINE: ${l.headline}\nVERDICT: ${l.usefulness_verdict}\nDECISION CHANGED: ${l.decision_changed}\n` +
  `SELECTION VALUE: ${l.selection_value}\nUSELESSNESS FALSIFIERS: ${l.uselessness_falsifiers.join(' | ')}\n` +
  `STATE-T DRIFT: ${l.state_t_drift}\nSTATE-VS-NOISY-ESTIMATOR: ${l.state_assumption_attack}\n` +
  `MINIMAL DEPLOYABILITY: ${l.minimal_deployability.join(' | ')}\nSUCCESS/FAILURE: ${l.success_failure_condition}\nBOTTOM LINE: ${l.one_line}`
).join('\n\n')

log(`Lens verdicts: ${lensResults.map(l => `${l.lens.split(/[ /]/)[0]}=${l.usefulness_verdict}`).join(', ')}`)

phase('Adjudicate')

const ARTIFACT = 'docs/research/26_habitat_persistence_economic_adjudication.md'

const finalSummary = await agent(
  `${DOCTRINE}\n\n${SETTLED}\n\n${THE_TASK}\n\n` +
  `FOUR LENSES:\n${lensBrief}\n\n` +
  `YOU ARE THE ADJUDICATOR (research lead, trader-first). Reconcile the four lenses into ONE coherent economic adjudication — no competing essays. Where they disagree, adjudicate explicitly and say who wins and why. The trader/PM lens is decisive on usefulness; the useless-prosecutor and econometrician set the bar it must clear; the firewall architect sets the binding anti-zombie constraints.\n\n` +
  `WRITE the adjudication to ${ARTIFACT} using the Write tool — dense, pre-registration-grade, no narrative inflation (CLAUDE.md §5/§14). It MUST contain, as explicit sections:\n` +
  `- Status header (date 2026-06-04, RESEARCH-MODE economic adjudication; NO empirical execution authorized).\n` +
  `- The economic question (assume delta_excess>0 survives) and why statistical persistence is insufficient.\n` +
  `- (1) The exact economic decision habitat persistence changes — unit, horizon, rebalance — constrained to universe-membership / capital-allocation / sizing, explicitly NOT entry timing.\n` +
  `- (2) MR attempt-selection value: environment-descriptor vs realized-profitability persistence; whether selection-only value can exist without timing.\n` +
  `- (3) Practical-uselessness falsifiers (the full enumerated list, each with its firing condition) — i.e. how persistence survives yet is useless.\n` +
  `- (4) HIDDEN STATE-T DRIFT + the HARD FIREWALL: the output-type constraint and the structural block for every drift path from habitat-persistence-probability to "MR likely soon"/entry-confidence. This must be a proof-shaped argument, not a promise.\n` +
  `- (5) Latent-assumption challenge: habitat as stable economic state vs slow noisy estimator; the mandatory incremental-value-vs-cheap-baseline test.\n` +
  `- TRADER USEFULNESS VERDICT (economically-useful-if-X / true-but-inert / undeployable, with conditions and the four-lens vote).\n` +
  `- ZOMBIE-STATE-T RISK ASSESSMENT (level + drift paths + firewall).\n` +
  `- MINIMAL DEPLOYABILITY CRITERION (smallest sufficient conditions).\n` +
  `- EXACT ECONOMIC SUCCESS/FAILURE CONDITION (pre-registerable: net-of-cost, cross-habitat OOS, incremental-vs-cheap-baseline, SELECTION-ONLY; the precise inequality/threshold that declares economic value PRESENT vs ABSENT).\n` +
  `- How this gates doc 25's STEP 0 (does the economic verdict change whether/which empirical run is worth running, and what economic pre-registration must be added BEFORE STEP 0).\n` +
  `- Surviving uncertainty, explicit non-conclusions, next highest-information action.\n\n` +
  `After writing, RETURN a tight summary: the usefulness verdict + four-lens vote, the one economic decision it changes (or that it changes none), the strongest uselessness-falsifier, the zombie risk level + the one-line firewall, the minimal deployability criterion, and the exact economic success/failure condition.`,
  { label: 'adjudicate:artifact', phase: 'Adjudicate' })

return {
  artifact: ARTIFACT,
  lens_votes: lensResults.map(l => ({ lens: l.lens, verdict: l.usefulness_verdict })),
  summary: finalSummary,
}
