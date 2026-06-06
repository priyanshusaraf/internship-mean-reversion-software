export const meta = {
  name: 'habitat-persistence-adjudication',
  description: 'Adjudicate: is "recent MR habitat -> elevated future MR habitat" a circular tautology or valid regime persistence? 4 lenses -> verdict + leakage-free pre-registered protocol',
  whenToUse: 'Resolve the core MR Habitat v2 disagreement: admissibility of conditional habitat persistence vs philosophical invalidity',
  phases: [
    { title: 'Lenses', detail: '4 required lenses adjudicate independently: econometrician, trader/PM, statistical adversary, time-series specialist' },
    { title: 'Adjudicate', detail: 'Synthesizer reconciles to ONE verdict + drafts the leakage-free causal protocol' },
    { title: 'StressTest', detail: 'Dedicated adversary attacks the DRAFTED protocol for residual leakage / mechanical persistence / State-T drift' },
    { title: 'Finalize', detail: 'Write the pre-registration-grade adjudication artifact; return verdict + protocol' },
  ],
}

// ---------------------------------------------------------------------------
const DOCTRINE = `
AMR DOCTRINE — BINDING (CLAUDE.md). This is RESEARCH MODE: the deliverable is a VERDICT + a PRE-REGISTERED PROTOCOL, NOT code, NOT the empirical run.
- Temporal integrity is sacred (§6.1): at time t only info available at t. Full-Information vs Causal both supportable (§6.2).
- Rolling/local estimation is the #1 artifact surface (§11.1): window+rebalance pre-registered; surrogate-relative (matched OU/RW/GARCH through IDENTICAL extraction so construction artifact cancels); multiplicity-controlled; local survivability = persistence across MULTIPLE disjoint windows, never one favorable window.
- Surrogate-relative reads mandatory; significance over narrative; no arbitrary weights; no black-box ML.
- ZOMBIE PROHIBITION (§4): State T (predict/classify/time reversion) is DEAD (doc 11). Nothing here may resurrect it. Banned vocab: T-score, hazard, ignition, imminent, favorable-now.
- Cross-habitat OOS replication is the unit of evidence (§11.7); report the full search, never the argmax.
`

const THE_QUESTION = `
THE EXACT DISAGREEMENT TO ADJUDICATE:
Does the claim  "recent MR habitat (in [t-k, t])  ->  elevated probability of MR habitat in [t+1, t+h]"  represent:
  (1) a CIRCULAR TAUTOLOGY (defining MR-with-MR; or mechanically induced by estimator autocorrelation / overlapping windows / slow-moving statistics), OR
  (2) VALID REGIME PERSISTENCE (a genuine, falsifiable property of the data-generating regime, analogous to volatility clustering / GARCH persistence)?

LOAD-BEARING DISTINCTION — we are NOT predicting price reversal. We are testing PERSISTENCE OF HABITAT (a regime-state property), not the sign/timing of the next price move. Habitat persistence is about whether the *mean-reversion-friendliness of the environment* persists, not about forecasting returns.

USER-SPECIFIED CAUSAL SKELETON (the starting protocol to harden, not weaken):
- At time t, classify habitat using ONLY [t-k, t].
- Then test [t+1, t+h] for persistence.
- NO overlap between classification and test windows. NO hindsight. NO State-T resurrection.

PRIOR CONTEXT (what is being challenged): the previous MR-Habitat-v2 redesign adversary KILLED the forward framing, ruling "conditional prior of FUTURE MR" a State-T tautology and forcing the object backward-only. The user is now challenging that kill: is forward HABITAT-STATE persistence (distinct from forward PRICE-REVERSAL prediction) actually admissible? Adjudicate honestly — uphold, overturn, or partition the prior kill.

CORE ANALYTICAL TENSION the lenses must resolve precisely:
- Apparent persistence can arise from THREE sources that must be separated: (a) TRUE regime persistence (the interesting claim), (b) MECHANICAL estimator autocorrelation — slow statistics / finite-sample window memory / shared-bar leakage manufacturing persistence even in a CONSTANT-parameter world, (c) a structural artifact (e.g. unconditional stationarity making "habitat" the common state). The test is admissible ONLY if it can separate (a) from (b)/(c). The decisive instrument is the SURROGATE: does a matched constant-parameter null (OU / RW / GARCH with NO regime switching) run through the IDENTICAL classify-then-test windowing also show the same "persistence"? If yes, it is mechanical (tautology side). If real data persistence exceeds the surrogate band, it is genuine regime persistence (valid side).
`

const PROTOCOL_REQUIREMENTS = `
THE PROTOCOL MUST BE LEAKAGE-FREE AND STRICTLY CAUSAL. At minimum specify, with justification:
- habitat classifier on [t-k,t]: which causal diagnostics (e.g. VR<1, kappa-hat>0, bounded ACF, stationarity on frozen reference) and the BINARY/categorical habitat label rule — defined with ZERO forward information.
- the embargo/buffer g between t and t+1 so estimator overlap and microstructure bleed cannot create mechanical correlation; justify g vs estimator memory length.
- test window [t+1+g, t+h]: how habitat is re-measured there with the SAME causal classifier, independently.
- the persistence statistic: e.g. P(habitat_{test} | habitat_{class}) - P(habitat_{test} | not habitat_{class}), or transition-matrix persistence, or conditional effect-size; stated as a falsifiable H0 (no persistence beyond null) vs H1.
- the SURROGATE protocol: matched OU/RW/GARCH (+ a splice/back-adjustment surrogate) run bit-identically through classify-test-embargo so the construction artifact cancels; persistence read ONLY as real-minus-surrogate.
- multiplicity control over the (k, h, g, theta) grid and across instruments; pre-registration of the grid; report full search not argmax.
- cross-habitat OOS replication requirement (multiple independent instruments / disjoint epochs) as the unit of evidence.
- the explicit firewall keeping this HABITAT-STATE persistence and forbidding any slide into price-direction/timing (State T).
- the falsification + kill trigger: what result declares persistence ABSENT.
`

// ---------------------------------------------------------------------------
const LENS_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['lens', 'verdict', 'reasoning', 'killer_confound', 'admissibility_conditions', 'protocol_demands', 'analogy_check', 'one_line'],
  properties: {
    lens: { type: 'string' },
    verdict: { type: 'string', enum: ['CIRCULAR_TAUTOLOGY', 'VALID_PERSISTENCE', 'EMPIRICALLY_DECIDABLE', 'INVALID_AS_POSED'], description: 'this lens\'s call on the core question' },
    reasoning: { type: 'string', description: 'why — the decisive argument, not a survey' },
    killer_confound: { type: 'string', description: 'the single most dangerous mechanism that could manufacture FALSE persistence (or the one that proves it is genuine)' },
    admissibility_conditions: { type: 'array', items: { type: 'string' }, description: 'exact conditions under which the claim becomes admissible (empty if it cannot be saved)' },
    protocol_demands: { type: 'array', items: { type: 'string' }, description: 'non-negotiable protocol elements this lens requires to trust a result' },
    analogy_check: { type: 'string', description: 'is this genuinely like volatility clustering / GARCH persistence (admissible) or like circular MR-defines-MR? adjudicate the analogy' },
    one_line: { type: 'string', description: 'one-sentence bottom line' },
  },
}

const DRAFT_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['verdict', 'verdict_reasoning', 'prior_kill_disposition', 'classifier', 'embargo', 'persistence_statistic', 'surrogate_protocol', 'multiplicity_and_oos', 'state_t_firewall', 'falsification_trigger', 'open_attack_surface'],
  properties: {
    verdict: { type: 'string', enum: ['CIRCULAR_TAUTOLOGY', 'VALID_PERSISTENCE', 'EMPIRICALLY_DECIDABLE', 'INVALID_AS_POSED'] },
    verdict_reasoning: { type: 'string' },
    prior_kill_disposition: { type: 'string', description: 'UPHOLD / OVERTURN / PARTITION the prior adversary kill of the forward framing — with reasoning' },
    classifier: { type: 'string', description: 'the causal habitat classifier on [t-k,t]' },
    embargo: { type: 'string', description: 'buffer g + justification vs estimator memory' },
    persistence_statistic: { type: 'string', description: 'the falsifiable H0/H1 persistence statistic' },
    surrogate_protocol: { type: 'string', description: 'matched-null families + identical-extraction protocol; real-minus-surrogate read' },
    multiplicity_and_oos: { type: 'string', description: 'grid pre-registration, multiplicity control, cross-habitat OOS replication unit' },
    state_t_firewall: { type: 'string', description: 'how habitat-state persistence is kept distinct from price-direction/timing' },
    falsification_trigger: { type: 'string', description: 'what result declares persistence ABSENT / kills the claim' },
    open_attack_surface: { type: 'array', items: { type: 'string' }, description: 'residual weaknesses the stress-test should attack' },
  },
}

const STRESS_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['residual_leakage', 'mechanical_persistence_paths', 'state_t_drift', 'surrogate_gaps', 'survives', 'mandatory_fixes'],
  properties: {
    residual_leakage: { type: 'array', items: { type: 'string' }, description: 'any path by which future info / overlap / embargo-failure still contaminates the drafted protocol' },
    mechanical_persistence_paths: { type: 'array', items: { type: 'string' }, description: 'ways the protocol could still report persistence that is pure estimator autocorrelation' },
    state_t_drift: { type: 'array', items: { type: 'string' }, description: 'any slide toward price-direction/timing prediction' },
    surrogate_gaps: { type: 'array', items: { type: 'string' }, description: 'null families that fail to cancel the real construction artifact' },
    survives: { type: 'string', description: 'does the protocol survive as leakage-free? what must change for it to be admissible?' },
    mandatory_fixes: { type: 'array', items: { type: 'string' }, description: 'fixes the final artifact MUST incorporate' },
  },
}

// ---------------------------------------------------------------------------
phase('Lenses')

const LENSES = [
  { key: 'quant-econometrician', brief: 'Quant econometrician. Treat this as a regime-persistence estimation problem. Is conditional habitat persistence identifiable and non-tautological under the non-overlapping causal design? Relate precisely to Markov regime-switching persistence and GARCH/vol-clustering — where those are admissible and why, and whether this inherits that admissibility or collapses to circularity. Be rigorous about what "habitat" must be defined as to avoid defining-MR-with-MR.' },
  { key: 'trader-pm', brief: 'Institutional trader / PM (1-12 week book). Strip the philosophy: do you actually believe regimes persist enough to act on, and is "habitat persists" decision-useful WITHOUT being a price signal? What persistence horizon h and hit-rate edge would change book construction (e.g. capital allocation toward currently-mean-reverting instruments) vs be economically meaningless? Kill it if persistence, even if real, is too short or too weak to matter after costs.' },
  { key: 'statistical-adversary', brief: 'Statistical adversary. Your job: PROVE it is a tautology / mechanical artifact. Attack with: estimator autocorrelation from slow statistics, finite-sample window memory, shared-bar leakage, unconditional-stationarity making "habitat" the trivial common state, selection over (k,h,theta), survivorship, and the splice/back-adjustment confound. State the exact surrogate that, if persistence survives it, would force you to concede it is GENUINE. Default to tautology unless the surrogate-relative design defeats you.' },
  { key: 'timeseries-specialist', brief: 'Time-series specialist. Nail the leakage mechanics: how long is estimator memory for each candidate classifier, hence the minimum embargo g; how non-overlap must be enforced; whether the persistence statistic is contaminated by overlapping rolling estimates; how to construct matched nulls (constant-parameter OU/RW/GARCH) through bit-identical extraction; and what a clean transition-matrix / conditional-probability persistence estimator looks like with correct standard errors under serial dependence.' },
]

const lensResults = (await parallel(LENSES.map(L => () =>
  agent(
    `${DOCTRINE}\n\n${THE_QUESTION}\n\n${PROTOCOL_REQUIREMENTS}\n\n` +
    `YOU ARE THE ${L.key.toUpperCase()} LENS: ${L.brief}\n\n` +
    `Adjudicate the core question from your lens, decisively. Converge to ONE verdict (not an essay). Be concrete about the killer confound and the exact conditions/protocol elements that make the claim admissible or expose it as circular.`,
    { label: `lens:${L.key}`, phase: 'Lenses', schema: LENS_SCHEMA })
))).filter(Boolean)

const lensBrief = lensResults.map(l =>
  `## LENS: ${l.lens}\nVERDICT: ${l.verdict}\nREASONING: ${l.reasoning}\nKILLER CONFOUND: ${l.killer_confound}\n` +
  `ANALOGY: ${l.analogy_check}\nADMISSIBILITY CONDITIONS: ${l.admissibility_conditions.join(' | ')}\n` +
  `PROTOCOL DEMANDS: ${l.protocol_demands.join(' | ')}\nBOTTOM LINE: ${l.one_line}`
).join('\n\n')

log(`Lenses: ${lensResults.map(l => `${l.lens.split(/[ /]/)[0]}=${l.verdict}`).join(', ')}`)

// ---------------------------------------------------------------------------
phase('Adjudicate')

const draft = await agent(
  `${DOCTRINE}\n\n${THE_QUESTION}\n\n${PROTOCOL_REQUIREMENTS}\n\n` +
  `FOUR LENSES ADJUDICATED:\n${lensBrief}\n\n` +
  `YOU ARE THE ADJUDICATOR (research lead). Reconcile the four lenses into ONE verdict on the core question and DRAFT the leakage-free causal protocol. Where lenses disagree, adjudicate explicitly and say who wins and why. Explicitly dispose of the PRIOR adversary kill (uphold / overturn / partition). Your verdict must be defensible and falsifiable — if the honest answer is "EMPIRICALLY_DECIDABLE", say so and make the protocol the decider. List the open attack surface for the stress-test to hit.`,
  { label: 'adjudicate:draft', phase: 'Adjudicate', schema: DRAFT_SCHEMA })

const draftBrief =
  `VERDICT: ${draft.verdict}\nREASONING: ${draft.verdict_reasoning}\nPRIOR-KILL DISPOSITION: ${draft.prior_kill_disposition}\n` +
  `CLASSIFIER: ${draft.classifier}\nEMBARGO: ${draft.embargo}\nPERSISTENCE STAT: ${draft.persistence_statistic}\n` +
  `SURROGATE: ${draft.surrogate_protocol}\nMULTIPLICITY/OOS: ${draft.multiplicity_and_oos}\n` +
  `STATE-T FIREWALL: ${draft.state_t_firewall}\nFALSIFICATION: ${draft.falsification_trigger}\n` +
  `OPEN ATTACK SURFACE: ${draft.open_attack_surface.join(' | ')}`

log(`Draft verdict: ${draft.verdict} | prior-kill: ${draft.prior_kill_disposition.slice(0, 80)}`)

// ---------------------------------------------------------------------------
phase('StressTest')

const stress = await agent(
  `${DOCTRINE}\n\n${THE_QUESTION}\n\n` +
  `The adjudicator drafted this verdict + protocol:\n${draftBrief}\n\n` +
  `YOU ARE THE DEDICATED ADVERSARIAL STRESS-TEST. Attack the DRAFTED PROTOCOL ONLY (not the abstract question). Try to find: (a) residual leakage — any future info / window overlap / insufficient embargo that survives; (b) mechanical-persistence paths — where the protocol could still report estimator-autocorrelation persistence as if genuine, even after the surrogate; (c) State-T drift — any slide toward price direction/timing; (d) surrogate gaps — null families that do NOT cancel the real construction artifact (incl. splice/back-adjustment). Then state whether it survives as leakage-free and the mandatory fixes the final artifact must carry.`,
  { label: 'stress:redteam', phase: 'StressTest', schema: STRESS_SCHEMA })

log(`Stress-test: ${stress.survives.slice(0, 120)}`)

// ---------------------------------------------------------------------------
phase('Finalize')

const stressBrief =
  `RESIDUAL LEAKAGE: ${stress.residual_leakage.join(' | ')}\nMECHANICAL PATHS: ${stress.mechanical_persistence_paths.join(' | ')}\n` +
  `STATE-T DRIFT: ${stress.state_t_drift.join(' | ')}\nSURROGATE GAPS: ${stress.surrogate_gaps.join(' | ')}\n` +
  `SURVIVES: ${stress.survives}\nMANDATORY FIXES: ${stress.mandatory_fixes.join(' | ')}`

const ARTIFACT = 'docs/research/25_habitat_persistence_adjudication.md'

const finalSummary = await agent(
  `${DOCTRINE}\n\n${THE_QUESTION}\n\n${PROTOCOL_REQUIREMENTS}\n\n` +
  `FOUR LENSES:\n${lensBrief}\n\nADJUDICATOR DRAFT:\n${draftBrief}\n\nADVERSARIAL STRESS-TEST:\n${stressBrief}\n\n` +
  `YOU ARE THE FINALIZER (research lead). Produce the definitive adjudication, incorporating EVERY mandatory fix from the stress-test (or showing precisely why a fix is unnecessary). WRITE it to ${ARTIFACT} using the Write tool — pre-registration-grade, dense, high-signal (CLAUDE.md §5/§14), no narrative inflation.\n\n` +
  `The doc MUST contain, as explicit sections:\n` +
  `- Status header (date 2026-06-04, RESEARCH-MODE adjudication + pre-registration; empirical run NOT yet authorized).\n` +
  `- VERDICT (one of: circular tautology / valid persistence / empirically-decidable / invalid-as-posed) with the decisive reasoning, and the FOUR-LENS vote.\n` +
  `- Disposition of the PRIOR adversary kill (uphold / overturn / PARTITION — and the precise line between admissible forward HABITAT-STATE persistence and forbidden forward PRICE-REVERSAL prediction / State T).\n` +
  `- The three-source decomposition (true regime persistence vs mechanical estimator autocorrelation vs structural artifact) and how the design separates them.\n` +
  `- The LEAKAGE-FREE CAUSAL PROTOCOL, fully specified: classifier on [t-k,t]; embargo g (justified vs estimator memory); test window [t+1+g, t+h]; persistence statistic as falsifiable H0/H1; surrogate protocol (matched OU/RW/GARCH + splice/back-adjustment, bit-identical extraction, real-minus-surrogate read); multiplicity control + pre-registered (k,h,g,theta) grid; cross-habitat OOS replication as the unit of evidence; the State-T firewall; the falsification/kill trigger.\n` +
  `- Pre-registration block: the frozen grid, instruments/epochs cohort, success & kill criteria, fixed BEFORE any data is touched.\n` +
  `- Surviving uncertainty, explicit non-conclusions, and the next highest-information empirical action (the actual run).\n\n` +
  `After writing, RETURN a tight summary: the verdict + four-lens vote, the prior-kill disposition in one sentence, the single decisive surrogate test, the top 3 leakage guards, and the exact pre-registered next empirical step.`,
  { label: 'finalize:artifact', phase: 'Finalize' })

return {
  artifact: ARTIFACT,
  verdict: draft.verdict,
  lens_votes: lensResults.map(l => ({ lens: l.lens, verdict: l.verdict })),
  prior_kill_disposition: draft.prior_kill_disposition,
  stress_survives: stress.survives,
  summary: finalSummary,
}
