export const meta = {
  name: 'mrscore-v2-redesign',
  description: 'Multi-lens first-principles redesign of MRScore into "MR Habitat Score" v2; converges to ONE proposal artifact',
  whenToUse: 'Full end-to-end redesign of the MRScore workbench object — habitat-compatibility, not signal generation',
  phases: [
    { title: 'Reconstruct', detail: 'Ground readers: original intention vs current implementation drift, from the actual files' },
    { title: 'Lenses', detail: '7 required lenses fan out in parallel over the grounded reconstruction + task spec' },
    { title: 'Adversary', detail: 'Dedicated red-team attack on the converging design: circularity, signal-drift, p-hacking, hindsight' },
    { title: 'Converge', detail: 'Single synthesizer reconciles all lenses + adversary into ONE proposal, writes the artifact' },
  ],
}

// ---------------------------------------------------------------------------
// Shared doctrine + task context. Embedded inline so every agent is grounded
// without re-reading the whole repo (CLAUDE.md §12.2 "reuse prior context").
// ---------------------------------------------------------------------------

const DOCTRINE = `
AMR DOCTRINE — BINDING CONSTRAINTS (CLAUDE.md). Every recommendation MUST respect these:
- This is RESEARCH MODE. The deliverable is a PROPOSAL, not code. No implementation is authorized yet.
- MR Habitat Score is NOT a signal generator. It must NOT answer "will price revert tomorrow / short now".
  It answers ONLY: "is this market / regime / window COMPATIBLE with mean reversion?" This distinction is load-bearing.
  Any drift toward predicting reversion timing/direction from the score = State-T resurrection (DEAD, doc 11) and is FORBIDDEN.
- Timing/trigger is a SEPARATE object (State T). MR Habitat Score = conditional prior on habitat, never a trigger.
- Temporal integrity is sacred (§6.1): at time t only info available at t. Full-Information vs Causal must both be supportable (§6.2).
- Rolling/local estimation is the #1 artifact surface (§11.1 BINDING GUARD): pre-register window+rebalance; surrogate-relative
  (matched OU/RW/GARCH run through identical extraction so construction artifact cancels); multiplicity-controlled; local survivability
  = persistence across MULTIPLE disjoint windows, never one favorable window. Cherry-picking the favorable window is the cardinal sin.
- Trader lens is a prioritization constraint, never a rigor relaxation (§11.2). The deployable object is a BOOK after costs, not an instrument.
- Surrogate-relative reads mandatory; significance over narrative; no arbitrary priors/weights; no pseudo-precision; no black-box ML.
- Frozen stack (§8): FastAPI/Python/Pandas/Polars/NumPy/SciPy/Statsmodels/FilterPy/ARCH/DuckDB/Parquet backend;
  Next.js 15/React/TS/Tailwind/shadcn/Zustand/React Query/lightweight-charts/Plotly frontend. Changing it is a freeze-break.
- Engineering: minimal · additive · isolated · reversible. No rewrites, no breaking prior satisfactory modules, no overengineering.
- Required v2 properties: interpretable · causal · deployable · falsifiable. Avoid "mathematically elegant nonsense".
`

const CURRENT_IMPL = `
CURRENT MRScore v1 IMPLEMENTATION (from repo map — treat as ground truth, but verify by reading if you need detail):
- Backend engine: backend/app/services/analytics_mrscore.py (~511 lines). FROZEN spec implementing doc 01 eq.13-34.
- Formula (point-in-time, causal, WITHIN-instrument rank): MRScore_t = 0.20*B1 + 0.60*B2 + 0.20*B3.
    B1 Mean Reliability (20%) = 0.30*(R_ADF+R_KPSS)/2 + 0.50*R_MSI + 0.20*R_VSI  (stationarity, mean/variance stability)
    B2 Mean Reversion Strength (60%, CORE) = 0.50*R_DRC + 0.30*R_HitRate + 0.20*R_VR
        DRC = min_h t_beta(h) from NW-HAC OLS; HitRate = P(revert | |z|>1.0); VR_agg = min_q VR(q), q in {2,5,10,20}
    B3 Tradability (20%) = (1/3)(R_HL + R_VC + R_TCF)  (half-life proximity, vol compression, transaction-cost filter)
- mu* is EMA-only in v1 (causal ewm, span=window). Kalman exists in analytics.py (KALMAN_SNR=1e-8, KALMAN_KAPPA=0.05, frozen, doc 06) but is research-only, NOT fed into MRScore. One-way DAG: MRScore reads mu* as input, never feeds back.
- z-score is causal (shifted trailing window). Rolling window default 252.
- Spreads / non-positive prices: log-based features undefined -> flagged with data_warning (a HACK, not a principled fix).
- API: GET /{instrument_id}/mrscore in backend/app/routers/market.py:449-527 -> per-bar scores + blocks + feature ranks. Models in backend/app/models/market.py (MRScoreRow/Stats/Response).
- Frontend: frontend/src/components/workbench/modules/MRScore.tsx (~243 lines), 58/42 chart+decomposition split, lightweight-charts.
- REGISTRY STATUS: docs/research/HYPOTHESIS_REGISTRY.md lists MRScore as ARCHIVED ("inverted on random walk"; superseded by Arm A habitat discovery). docs/research/09_mrscore_observatory.md frames it as DIAGNOSTIC not signal, within-instrument not cross-sectional.
- ADD-A-WINDOW PATTERN: new module component in components/workbench/modules/, register in components/workbench/registry.ts (WORKBENCH_MODULES), add api method in lib/api.ts, types in lib/types.ts, backend endpoint in routers/market.py. ModuleProps = {instrumentId, dateRange, estimator, window}.
- Reusable backend: analytics.py (compute_ema/full_ema/kalman/halflife/acf/residual/innovation/zscore), analytics_substrate.py (character map OU/Trend/RW/Ambiguous), analytics_mrscore.py primitives, store.py (DuckDB get_ohlcv with start/end filtering), loader.py, synthetic.py (null generators).
- Data: /Users/priyanshusaraf/Downloads/mean-reversion-data (commodities, FX, equities, calendar legs — abundant; do NOT complain about data scarcity).
`

const TASK_SPEC = `
REDESIGN MANDATE — MRScore v2 / "MR Habitat Score" (full first-principles redesign, NOT an incremental patch):
ONTOLOGY (load-bearing): markets sometimes exhibit mean-reverting HABITATS. If a market has RECENTLY behaved mean-revertingly,
the CONDITIONAL prior of future MR may rise — NOT certainty, conditional prior only. The score characterizes:
mean-reversion friendliness · regime compatibility · habitat stability · conditional deployability. It is NOT a trigger.

The proposal must answer all of:
1. CRITIQUE current MRScore: what object was it ORIGINALLY trying to measure; what object is it ACCIDENTALLY measuring now (signal drift); which implementation mistakes caused the drift.
2. FORMAL ONTOLOGY of MR Habitat Score (what is this object, precisely, and what it is NOT).
3. MATHEMATICAL REDESIGN: what should the object mathematically BE? Avoid arbitrary priors, arbitrary weights, the frozen .2/.6/.2 decomposition, pseudo-precision, black-box ML. Must be interpretable, causal, deployable, falsifiable.
4. WINDOW-BASED OBSERVATORY: should scoring become PERIOD-based [t0,t1] instead of point-based? For a selected period return e.g. mean/median habitat score, stability, persistence, variance, habitat confidence, percent-favorable, regime continuity, equilibration stats, OU stability, regime-fracture diagnostics. What would an institutional trader actually care about?
5. EQUILIBRIUM ANCHORING: for period [t0,t1], estimate mu*(t0-eps) with a SELECTABLE estimator (Kalman / equilibrium filter / robust mean / custom), then FREEZE equilibrium across the window and compute all diagnostics relative to it. Is this statistically coherent? Does it reduce moving-target contamination? How to implement? ATTACK HARD.
6. RESIDUAL ECOLOGY integration (CLAUDE.md §11.5 — OBSERVATIONAL, explicitly NOT State T): model trend (linear/nonlinear/local/spline/robust/regime-aware — no forced linearity), then study residual behaviour (variance spikes, noise acceleration, OU fit/weakening, kappa instability, residual persistence, ACF change, vol compression/expansion). Does residual ecology change around REALIZED MR periods? Is this coherent or CIRCULAR? Hidden failure modes? Can it be ONE CONDITION rather than a standalone predictor? Must stay surrogate-relative, understanding-mode, never wired to a signal. ATTACK HARD.
7. AUTOMATIC HABITAT DISCOVERY: can software auto-discover historical MR habitats / consolidation zones / transition points / recurring structures / durations / persistence / break conditions WITHOUT hindsight contamination, regime cherry-picking, or fake clustering? Feasibility verdict + causal-validity guard.
8. SPREAD ROBUSTNESS: negative prices break log MR logic. Principled (non-hack) alternatives: equilibrium-relative distances, z-space normalization, affine transforms, signed-space handling, non-log formulations. Need mathematically principled treatment.
9. STATISTICAL FAILURE MODES of the whole v2 design.
10. EXACT WORKBENCH REDESIGN (backend architecture + frontend observatory UX): user must select period, select estimator, inspect equilibrium, inspect habitat diagnostics, inspect residual ecology, inspect regime transitions, compare historical habitats, replay history. Reuse existing modules; minimal additive; no rewrites.
PLUS: smallest additive implementation roadmap, and the immediate next coding tasks.
`

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------

const RECON_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['source', 'original_intent', 'current_behavior', 'drift_findings', 'reusable_assets', 'quotes'],
  properties: {
    source: { type: 'string', description: 'which files/docs you actually read' },
    original_intent: { type: 'string', description: 'what the ORIGINAL system was trying to measure, per this source' },
    current_behavior: { type: 'string', description: 'what the implementation ACTUALLY does now, per this source' },
    drift_findings: {
      type: 'array', description: 'concrete drift/mistake findings with file:line where possible',
      items: { type: 'object', additionalProperties: false, required: ['finding', 'evidence', 'class'],
        properties: { finding: { type: 'string' }, evidence: { type: 'string' },
          class: { type: 'string', enum: ['STRUCTURAL', 'METHODOLOGY', 'MEASUREMENT', 'IMPLEMENTATION'] } } },
    },
    reusable_assets: { type: 'array', items: { type: 'string' }, description: 'modules/functions worth preserving or reusing for v2' },
    quotes: { type: 'array', items: { type: 'string' }, description: 'key verbatim code/spec snippets with file:line' },
  },
}

const LENS_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['lens', 'headline', 'ontology_view', 'math_recommendation', 'window_observatory', 'equilibrium_anchoring',
             'residual_ecology_verdict', 'habitat_discovery_verdict', 'spread_treatment', 'workbench_view',
             'top_risks', 'hard_constraints', 'one_recommendation'],
  properties: {
    lens: { type: 'string' },
    headline: { type: 'string', description: 'one sentence: this lens\'s single most important position' },
    ontology_view: { type: 'string', description: 'what the v2 object should/should-not be, from this lens' },
    math_recommendation: { type: 'string', description: 'concrete math object/feature construction this lens advocates; explicitly avoid arbitrary weights/.2/.6/.2/black-box' },
    window_observatory: { type: 'string', description: 'period-based vs point-based stance + which period statistics matter from this lens' },
    equilibrium_anchoring: { type: 'string', description: 'verdict on freeze-mu*(t0-eps)-across-window: coherent? failure modes? estimator choice?' },
    residual_ecology_verdict: { type: 'string', description: 'coherent vs circular? one-condition vs standalone? hidden failure modes?' },
    habitat_discovery_verdict: { type: 'string', description: 'feasible without hindsight/cherry-picking/fake-clustering? how, or why not?' },
    spread_treatment: { type: 'string', description: 'principled non-log / signed-space / equilibrium-relative treatment' },
    workbench_view: { type: 'string', description: 'backend + frontend observatory design from this lens; reuse existing modules' },
    top_risks: { type: 'array', items: { type: 'string' }, description: 'failure modes / objections this lens raises' },
    hard_constraints: { type: 'array', items: { type: 'string' }, description: 'non-negotiables this lens imposes on any final design' },
    one_recommendation: { type: 'string', description: 'this lens converges to ONE actionable recommendation (not an essay)' },
  },
}

const ADVERSARY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['fatal_flaws', 'circularity_attacks', 'signal_drift_attacks', 'phacking_attacks', 'hindsight_attacks', 'surrogate_gaps', 'kill_or_survive', 'required_guards'],
  properties: {
    fatal_flaws: { type: 'array', items: { type: 'string' }, description: 'design elements that should be KILLED before they enter v2' },
    circularity_attacks: { type: 'array', items: { type: 'string' }, description: 'where residual-ecology / habitat-discovery becomes circular (defining MR using MR)' },
    signal_drift_attacks: { type: 'array', items: { type: 'string' }, description: 'where the design accidentally becomes a reversion timing/direction signal = State-T resurrection' },
    phacking_attacks: { type: 'array', items: { type: 'string' }, description: 'rolling/WHEN-not-WHETHER multiplicity & favorable-window cherry-picking exposure' },
    hindsight_attacks: { type: 'array', items: { type: 'string' }, description: 'lookahead / hindsight-labeling of "historical MR habitats"' },
    surrogate_gaps: { type: 'array', items: { type: 'string' }, description: 'reads not made surrogate-relative; construction artifacts not cancelled' },
    kill_or_survive: { type: 'string', description: 'overall verdict: which parts survive adversarial review, which must be removed/reframed' },
    required_guards: { type: 'array', items: { type: 'string' }, description: 'mandatory guards the final proposal MUST include to be admissible' },
  },
}

// ---------------------------------------------------------------------------
// Phase 1 — Reconstruct (grounded read of intention vs drift)
// ---------------------------------------------------------------------------

phase('Reconstruct')

const RECON_TARGETS = [
  { label: 'recon:spec-intent',
    prompt: `Read docs/research/01_amr_framework.md (esp. the MRScore section, eq.13-34) and docs/research/09_mrscore_observatory.md. Reconstruct the ORIGINAL intended ontology of MRScore: what object was it meant to measure, what epistemic status was claimed (diagnostic vs signal), within-instrument vs cross-sectional. Identify any place the SPEC itself already hints at habitat-compatibility vs reversion-prediction. Report verbatim quotes with file:line.` },
  { label: 'recon:engine-drift',
    prompt: `Read backend/app/services/analytics_mrscore.py in full and backend/app/routers/market.py:449-527. Determine what the implementation ACTUALLY computes and where it DRIFTED from "habitat compatibility" toward accidental "signal" behavior (e.g. per-bar point scores, |z|>theta hit-rate conditioning, min_h DRC selection, the 0.2/0.6/0.2 weights). Flag arbitrary weights, pseudo-precision, hidden lookahead, and the spread data_warning hack. file:line evidence.` },
  { label: 'recon:registry-history',
    prompt: `Read docs/research/HYPOTHESIS_REGISTRY.md (MRScore + habitat entries) and skim docs/research/18_arm_a_habitat_preregistration.md, 19_arm_a_habitat_results.md, 20/21 (Arm A v2 positive control). Reconstruct WHY MRScore was archived ("inverted on random walk"), what habitat discovery already established, and what precedent exists for automatic habitat identification with causal validity. This is the kill-discipline / zombie-reopen context. Quotes with file:line.` },
  { label: 'recon:equilibrium',
    prompt: `Read docs/research/02_mu_star_equilibrium.md and docs/research/06_kalman_equilibrium_research_update.md, plus the estimator functions in backend/app/services/analytics.py (compute_ema, compute_full_ema, compute_kalman, compute_halflife, compute_residual, compute_zscore). Reconstruct the available equilibrium estimators, the frozen Kalman constants, and assess the feasibility of "estimate mu*(t0-eps) then FREEZE across [t0,t1]". Note temporal-integrity hazards. file:line.` },
  { label: 'recon:workbench',
    prompt: `Read frontend/src/components/workbench/registry.ts, types.ts, the ModuleProps/WorkbenchModule interfaces, frontend/src/components/workbench/modules/MRScore.tsx, frontend/lib/api.ts, frontend/lib/types.ts, and one or two sibling modules (e.g. SubstrateCharacter.tsx, Replay.tsx) for the period-selection / replay pattern. Reconstruct EXACTLY how a new workbench window is added and how period selection + replay currently work, so v2 can be minimal-additive. file:line.` },
]

const recon = (await parallel(RECON_TARGETS.map(t => () =>
  agent(`${DOCTRINE}\n\nYou are a grounding reader for an MRScore v2 redesign. ${t.prompt}\n\nReturn structured reconstruction facts.`,
    { label: t.label, phase: 'Reconstruct', agentType: 'Explore', schema: RECON_SCHEMA })
))).filter(Boolean)

const reconBrief = recon.map(r =>
  `### SOURCE: ${r.source}\nORIGINAL INTENT: ${r.original_intent}\nCURRENT BEHAVIOR: ${r.current_behavior}\n` +
  `DRIFT: ${r.drift_findings.map(d => `[${d.class}] ${d.finding} (${d.evidence})`).join(' | ')}\n` +
  `REUSABLE: ${r.reusable_assets.join(', ')}\nQUOTES: ${r.quotes.join(' || ')}`
).join('\n\n')

log(`Reconstruction complete: ${recon.length} grounded sources, ${recon.reduce((n, r) => n + r.drift_findings.length, 0)} drift findings.`)

// ---------------------------------------------------------------------------
// Phase 2 — Lenses (the 7 required perspectives, in parallel)
// ---------------------------------------------------------------------------

phase('Lenses')

const LENSES = [
  { key: 'quant-researcher', brief: 'Quant researcher / research lead. Strongest coherent hypothesis for what the v2 object SHOULD be; the cleanest interpretable+falsifiable math; resist quant theater and elegant nonsense.' },
  { key: 'trader-pm', brief: 'Institutional trader / PM running a 1-12 week book. Would a trader fund this? Is the object decision-useful as a HABITAT prior (not a trigger)? Evaluate as a BOOK after costs/capacity/risk. Which diagnostics actually move risk; what is the "no-trade environment" read. Kill economically-irrelevant elegance.' },
  { key: 'statistical-adversary', brief: 'Statistical adversary embedded as a design lens. Demand surrogate-relative construction, multiplicity control, pre-registration of windows. Expose where any feature is non-causal, artifact-induced, or only significant by search. Insist on a synthetic OU-vs-RW-vs-GARCH discrimination test the v2 object must pass.' },
  { key: 'systems-architect', brief: 'Systems architect. Preserve AMR coherence (one-way DAG, no feedback into mu*, temporal firewall). Smallest additive backend/frontend design that reuses analytics.py/analytics_mrscore.py/store.py and the existing workbench-window pattern. No rewrites, no breaking prior modules. Name exact files to add/touch.' },
  { key: 'frontend-workbench', brief: 'Frontend / workbench observatory designer. Design the period-based observatory UX: period selector [t0,t1], estimator selector, frozen-equilibrium inspector, habitat diagnostics panel, residual-ecology panel, regime-transition view, historical-habitat comparison, replay. Thin-but-powerful, research integrity over aesthetics, lightweight-charts + Plotly. Concrete panel layout.' },
  { key: 'timeseries-specialist', brief: 'Time-series specialist. Rigor on equilibrium freezing vs moving-target contamination, OU estimation (kappa/half-life) stability, ACF/variance-ratio behavior, stationarity testing on a FROZEN reference, and the residual-ecology construction. Demand principled trend models (local/spline/robust/regime-aware) and principled spread/signed-space treatment.' },
  { key: 'regime-specialist', brief: 'Regime modeling specialist. Automatic habitat discovery WITHOUT hindsight: how to segment regimes / consolidation zones / transitions causally (e.g. expanding-window or pre-registered change-point with surrogate calibration), avoiding fake clustering and cherry-picking. Define "habitat continuity / fracture" diagnostics and recurring-structure detection that survive the §11.1 rolling guard.' },
]

const lensResults = (await parallel(LENSES.map(L => () =>
  agent(
    `${DOCTRINE}\n\n${CURRENT_IMPL}\n\n${TASK_SPEC}\n\n` +
    `GROUNDED RECONSTRUCTION (original intent vs current drift, from the actual repo):\n${reconBrief}\n\n` +
    `YOU ARE THE ${L.key.toUpperCase()} LENS: ${L.brief}\n\n` +
    `Answer the full redesign mandate FROM YOUR LENS. Be concrete and opinionated. Converge to ONE recommendation, not a survey. ` +
    `Take explicit positions on: period-based vs point-based; freeze-mu*-across-window (attack it); residual ecology coherent-vs-circular and whether it should be ONE CONDITION; automatic habitat discovery feasibility under causal validity; principled spread treatment; the replacement for the 0.2/0.6/0.2 weighting. Flag where any choice risks turning the object into a reversion SIGNAL (forbidden).`,
    { label: `lens:${L.key}`, phase: 'Lenses', schema: LENS_SCHEMA })
))).filter(Boolean)

const lensBrief = lensResults.map(l =>
  `## LENS: ${l.lens}\nHEADLINE: ${l.headline}\nONTOLOGY: ${l.ontology_view}\nMATH: ${l.math_recommendation}\n` +
  `WINDOW: ${l.window_observatory}\nEQUILIBRIUM: ${l.equilibrium_anchoring}\nRESIDUAL ECOLOGY: ${l.residual_ecology_verdict}\n` +
  `HABITAT DISCOVERY: ${l.habitat_discovery_verdict}\nSPREAD: ${l.spread_treatment}\nWORKBENCH: ${l.workbench_view}\n` +
  `RISKS: ${l.top_risks.join(' | ')}\nHARD CONSTRAINTS: ${l.hard_constraints.join(' | ')}\nONE REC: ${l.one_recommendation}`
).join('\n\n')

log(`Lenses complete: ${lensResults.length}/7 perspectives converged.`)

// ---------------------------------------------------------------------------
// Phase 3 — Adversary (dedicated red-team on the union of lens proposals)
// ---------------------------------------------------------------------------

phase('Adversary')

const adversary = await agent(
  `${DOCTRINE}\n\n${TASK_SPEC}\n\n` +
  `Seven design lenses produced the following converging v2 proposal material:\n${lensBrief}\n\n` +
  `YOU ARE THE DEDICATED ADVERSARIAL RED TEAM (mandatory per CLAUDE.md §11.6). Your ONLY job is to try to KILL this v2 design before it is committed. ` +
  `Default to skepticism. Attack hardest on: (a) CIRCULARITY — residual ecology / habitat discovery defining mean reversion using mean reversion, or "recently reverted -> likely to revert" being a tautology rather than evidence; ` +
  `(b) SIGNAL DRIFT — any path by which a "habitat compatibility" score becomes a de-facto reversion timing/direction signal (State-T resurrection, DEAD per doc 11, FORBIDDEN); ` +
  `(c) P-HACKING — the WHEN-not-WHETHER × rolling-windows × multi-instrument multiplicity explosion (§11.7), favorable-window cherry-picking (§11.1 cardinal sin); ` +
  `(d) HINDSIGHT — labeling "historical MR habitats" with information not available causally; ` +
  `(e) SURROGATE GAPS — reads not made surrogate-relative so construction artifacts survive (recall doc 19: rolling-beta update-noise manufactured VR>>1). ` +
  `Be specific and reference which lens claim you are attacking. Then state which parts survive and the mandatory guards the final proposal must carry.`,
  { label: 'adversary:redteam', phase: 'Adversary', schema: ADVERSARY_SCHEMA })

log(`Adversarial pass complete. Verdict: ${adversary?.kill_or_survive?.slice(0, 160) ?? 'n/a'}`)

// ---------------------------------------------------------------------------
// Phase 4 — Converge (single synthesizer writes ONE coherent proposal artifact)
// ---------------------------------------------------------------------------

phase('Converge')

const adversaryBrief =
  `FATAL FLAWS: ${adversary.fatal_flaws.join(' | ')}\nCIRCULARITY: ${adversary.circularity_attacks.join(' | ')}\n` +
  `SIGNAL DRIFT: ${adversary.signal_drift_attacks.join(' | ')}\nP-HACKING: ${adversary.phacking_attacks.join(' | ')}\n` +
  `HINDSIGHT: ${adversary.hindsight_attacks.join(' | ')}\nSURROGATE GAPS: ${adversary.surrogate_gaps.join(' | ')}\n` +
  `VERDICT: ${adversary.kill_or_survive}\nREQUIRED GUARDS: ${adversary.required_guards.join(' | ')}`

const ARTIFACT_PATH = 'docs/research/MRSCORE_V2_PROPOSAL.md'

const synthesis = await agent(
  `${DOCTRINE}\n\n${CURRENT_IMPL}\n\n${TASK_SPEC}\n\n` +
  `GROUNDED RECONSTRUCTION:\n${reconBrief}\n\n` +
  `SEVEN-LENS MATERIAL:\n${lensBrief}\n\n` +
  `ADVERSARIAL RED-TEAM:\n${adversaryBrief}\n\n` +
  `YOU ARE THE SYNTHESIZER (research lead). Reconcile ALL of the above into ONE COHERENT PROPOSAL — not competing essays. ` +
  `Where lenses disagree, ADJUDICATE explicitly and say why one wins (or how they compose). Every surviving design element MUST clear the adversarial guards; ` +
  `if the adversary killed something, either drop it or show precisely how the guard neutralizes the attack. The proposal must keep the object a HABITAT-COMPATIBILITY characterization, never a reversion signal.\n\n` +
  `WRITE the proposal to ${ARTIFACT_PATH} (use the Write tool; this is the institutional artifact, dense and high-signal per CLAUDE.md §14 — no narrative inflation). ` +
  `It MUST contain, as explicit sections, all TEN deliverables:\n` +
  `1. Critique of current MRScore (with file:line drift evidence, classed STRUCTURAL/METHODOLOGY/MEASUREMENT/IMPLEMENTATION)\n` +
  `2. What object it ACCIDENTALLY measures now\n` +
  `3. Formal ontology of MR Habitat Score (what it IS and explicitly is NOT; conditional-prior framing; firewall vs State T)\n` +
  `4. Mathematical redesign (the concrete statistical object + feature construction; explicit replacement for arbitrary .2/.6/.2 weights; interpretable/causal/falsifiable; NO black-box ML)\n` +
  `5. Window-based observatory design (period-based [t0,t1] vs point; the exact period statistics a trader cares about)\n` +
  `6. Equilibrium anchoring redesign (freeze mu*(t0-eps) across window; selectable estimator; statistical-coherence verdict + how it reduces moving-target contamination + implementation; include the adversary's attack and the resolution)\n` +
  `7. Residual ecology integration VERDICT (coherent vs circular; ONE-CONDITION vs standalone; surrogate-relative protocol; failure modes) — keep the §11.5 firewall vs State T explicit\n` +
  `8. Automatic habitat discovery FEASIBILITY (causal, no hindsight/cherry-picking/fake-clustering; concrete method or a reasoned no)\n` +
  `9. Statistical failure modes (the full list, each with its mandatory guard)\n` +
  `10. Trader interpretation (what the trader reads off it, as a BOOK after costs) AND the EXACT workbench redesign (backend modules+endpoints to add; frontend observatory panels; explicit REUSE of existing files; minimal-additive)\n` +
  `PLUS a final section: "Smallest additive implementation roadmap" (ordered, reversible steps; exact files to add/touch) and "Immediate next coding tasks" (the first 3-5 concrete tasks). ` +
  `End with: pre-registration requirements, a real-data positive-control plan (§11.8), surviving uncertainty, explicit non-conclusions, and the next highest-information empirical question. ` +
  `Open the doc with a status header (date 2026-06-04, RESEARCH-MODE PROPOSAL, implementation NOT yet authorized) and a one-paragraph executive thesis.\n\n` +
  `After writing the file, RETURN a concise summary: the v2 object in 2-3 sentences, the top 5 design decisions, what the adversary forced you to change/drop, and the immediate next coding tasks.`,
  { label: 'synthesis:proposal', phase: 'Converge' })

return {
  artifact: ARTIFACT_PATH,
  reconstruction_sources: recon.length,
  lenses: lensResults.length,
  adversary_verdict: adversary?.kill_or_survive ?? null,
  synthesis_summary: synthesis,
}
