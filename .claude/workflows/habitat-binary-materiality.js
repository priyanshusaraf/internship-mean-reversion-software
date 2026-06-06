export const meta = {
  name: 'habitat-binary-materiality',
  description: 'Final tightening: restrict Habitat Persistence v1 to BINARY eligibility (no weighting/confidence/score) + add a pre-registered MATERIALITY hurdle. Re-adjudicate USEFUL_IF vs TRUE_BUT_INERT. No execution.',
  whenToUse: 'Last adjudication before freezing the combined pre-registration: does the object survive binary-only + materiality, or downgrade to inert?',
  phases: [
    { title: 'Lenses', detail: 'trader/PM (materiality thresholds) · useless-prosecutor (argue downgrade) · firewall architect (is binary now airtight) · econometrician (binary power + incremental test)' },
    { title: 'Adjudicate', detail: 'One verdict under both restrictions + the binary spec + the frozen materiality hurdle + updated success/failure; write refinement artifact' },
  ],
}

const DOCTRINE = `
AMR DOCTRINE — BINDING (CLAUDE.md). RESEARCH MODE. PURE ADJUDICATION + FREEZE REFINEMENT — NO empirical execution, NO STEP 0, NO data touched.
- §11.2 trader lens is a prioritization constraint, never a rigor relaxation. The deployable object is a BOOK after costs. A statistically-significant-but-immaterial gain a PM would ignore is a NON-FINDING.
- §4 ZOMBIE PROHIBITION: State T (predict/classify/TIME reversion; "MR likely soon"; entry-confidence) is DEAD (doc 11). Banned vocab: T-score, hazard, ignition, imminent, favorable-now.
- §11.3: probation-before-kill; conditional survival is a legitimate terminal outcome; a clean NON-FINDING / kill is ALSO a success ("stopping is a success").
- Habitat ≠ signal. Persistence informs WHICH market is in scope, never WHEN/how-much to act within it.
`

const SETTLED = `
SETTLED BY DOCS 25 + 26 (do NOT relitigate):
- Object = forward HABITAT-STATE persistence: sign-free latent second-moment regime transition probability, measured surrogate-relative (delta_excess vs worst-case matched null). Statistically EMPIRICALLY_DECIDABLE (doc 25). Pre-reg gated, not run.
- Doc 26 economic verdict: ECONOMICALLY_USEFUL_IF (3 USEFUL_IF / 1 UNDEPLOYABLE). The only admissible economic decision = book-level MR-universe MEMBERSHIP + capital WEIGHT (NOT entry timing/direction). Two-stage gate: statistical (25) -> economic (26). Strongest falsifier = no INCREMENTAL value over a cheap 1-line vol/half-life/VR baseline. Firewall = output-type lock (period-level only, no per-bar scalar, un-composable with any deviation/z/entry trigger).

THIS PASS — the user imposes TWO tightening restrictions and asks whether the object SURVIVES as ECONOMICALLY_USEFUL_IF or DOWNGRADES to LIKELY_TRUE_BUT_INERT:

RESTRICTION 1 — BINARY ELIGIBILITY ONLY (v1). The object may emit ONLY {eligible / ineligible} per instrument per period.
  FORBIDDEN in v1: confidence, probability output, continuous score, ANY capital scaling / sleeve weighting / graded conviction.
  Rationale: even slow weighting risks "MR confidence -> larger allocation -> hidden State-T resurrection". Weighting may be reconsidered ONLY AFTER binary gating INDEPENDENTLY proves value OOS. This is staged deployment, not permanent.

RESTRICTION 2 — EXPLICIT MATERIALITY HURDLE. Delta>0 with CI excluding 0 is NOT sufficient. Require a PRE-REGISTERED PRACTICAL hurdle: a PM-material improvement in at least one of {net-of-cost Sharpe, turnover reduction, drawdown improvement, capacity} — sized so a real PM would actually change behavior. A tiny significant gain = NON-FINDING.
`

const THE_TASK = `
ADJUDICATE under BOTH restrictions:
A. Does binary-only eligibility (no weighting) lose so much economic instrument-power that the object becomes inert, OR is binary universe gating (a familiar watchlist/eligible-set construct) still a legitimately deployable decision? Be concrete: equal-weight-within-eligible-set vs flat vs cheap-baseline-eligible-set.
B. What EXACT materiality thresholds would a PM actually require to deploy? Give concrete pre-registerable numbers/ranges for: net-of-cost Sharpe improvement floor (absolute), turnover/cost ceiling or reduction floor, max-drawdown improvement, capacity floor, and an "implementation benefit a PM would notice" framing. The hurdle must be a DISJUNCTION or CONJUNCTION — specify which and why.
C. Under binary + materiality, re-assess statistical POWER: binary labels discard information; does the OOS, cross->=2-habitat, incremental-vs-cheap-baseline test still have enough power to DETECT a material binary-gating edge, or does coarsening + a high hurdle make a false-negative likely (and is that acceptable per doctrine)?
D. Zombie-State-T risk under binary-only: is the firewall now STRUCTURALLY airtight (no continuous channel exists to compose with an entry trigger)? Confirm or find the residual leak.
E. THE VERDICT: after both restrictions, ECONOMICALLY_USEFUL_IF (survives, conditional, decidable) or LIKELY_TRUE_BUT_INERT (the coarsening + hurdle make the realistic prior failure)? Distinguish the VERDICT TYPE (is it still a decidable conditional?) from the REALISTIC PRIOR (how likely to pass). Be honest: doctrine says a clean expected NON-FINDING is acceptable.

REQUIRED OUTPUTS:
- BINARY-ONLY SPECIFICATION: the exact v1 output contract (eligible/ineligible per instrument per period; hysteresis to control flip-flop turnover; the rebalance cadence; the type-lock that forbids any continuous/score field).
- FROZEN MATERIALITY HURDLE: the pre-registered practical thresholds (with numbers), conjunction/disjunction structure, and how each maps to a PM decision.
- UPDATED SUCCESS/FAILURE CONDITION: the doc-26 condition re-expressed for binary gating + materiality (orthogonalized vs cheap binary baseline, >=2 OOS habitats, FWER, material hurdle).
- REVISED ZOMBIE RISK level under binary-only.
- THE VERDICT (USEFUL_IF vs LIKELY_TRUE_BUT_INERT) with explicit verdict-type-vs-realistic-prior separation.
`

const LENS_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['lens', 'headline', 'binary_deployability', 'materiality_thresholds', 'power_under_binary', 'zombie_under_binary', 'verdict', 'realistic_prior', 'one_line'],
  properties: {
    lens: { type: 'string' },
    headline: { type: 'string' },
    binary_deployability: { type: 'string', description: 'is binary-only universe gating still a legitimately deployable decision, or too coarse to matter?' },
    materiality_thresholds: { type: 'array', items: { type: 'string' }, description: 'concrete pre-registerable practical thresholds (Sharpe/turnover/drawdown/capacity) with numbers, and conjunction/disjunction structure' },
    power_under_binary: { type: 'string', description: 'does binary coarsening + high hurdle still permit detecting a material edge OOS, or is false-negative likely (and acceptable)?' },
    zombie_under_binary: { type: 'string', description: 'is the firewall structurally airtight under binary-only? residual leak if any' },
    verdict: { type: 'string', enum: ['ECONOMICALLY_USEFUL_IF', 'LIKELY_TRUE_BUT_INERT', 'UNDEPLOYABLE'] },
    realistic_prior: { type: 'string', description: 'separate from verdict TYPE: how likely is it to actually pass the hurdle? honest base-rate' },
    one_line: { type: 'string' },
  },
}

phase('Lenses')

const LENSES = [
  { key: 'trader-pm', brief: 'Institutional trader / PM (1-12 week MR book) — LEAD. You run an eligible-universe (watchlist) construct already; binary in/out is native to how you work. Answer: does a binary MR-eligibility flag that rotates the eligible set change your book vs a flat universe — equal-weight within eligible? Then give the EXACT materiality numbers you would demand before deploying: net-of-cost Sharpe improvement floor, turnover ceiling/reduction, max-DD improvement, capacity floor. State whether you require ALL (conjunction) or ANY (disjunction) and why. If the realistic gain is below what you would act on, say LIKELY_TRUE_BUT_INERT.' },
  { key: 'useless-prosecutor', brief: 'Adversary tasked to argue DOWNGRADE to LIKELY_TRUE_BUT_INERT. Binary discards the graded information that gave weighting its edge; a material hurdle on top means the coarse instrument must clear a high bar with less information. Prosecute: binary gating either replicates the cheap baseline binary filter (no increment) or its incremental edge is below any PM-material threshold. Default to INERT unless the trader shows a binary decision that is BOTH incremental AND material.' },
  { key: 'firewall-architect', brief: 'Doctrine / systems firewall architect. Assess whether BINARY-ONLY makes the anti-State-T firewall STRUCTURALLY airtight: with no continuous confidence/score/weight field emitted at all, is there ANY residual channel by which the object could be composed with a deviation/z/entry trigger or be read as "MR likely soon / size up"? Specify the v1 output contract type-lock (eligible/ineligible enum only, hysteresis, period cadence) and prove the zombie path is severed at the type level. Flag any residual leak (e.g. eligibility-streak length becoming a covert confidence proxy).' },
  { key: 'econometrician', brief: 'Quant econometrician. Two jobs: (1) statistical POWER under binary coarsening — binary labels discard information, so the OOS cross->=2-habitat incremental-vs-cheap-binary-baseline test has lower power; quantify the tradeoff and whether a material edge is still detectable or false-negative-likely (and whether that is acceptable per §11.3). (2) The incremental test design for binary: how to orthogonalize the habitat-eligibility flag against the cheap-baseline-eligibility flag (e.g. discordant-cells analysis: instruments eligible under habitat but NOT baseline, and vice versa) so the increment is isolated. Specify the exact estimator + serial-dependence-robust inference.' },
]

const lensResults = (await parallel(LENSES.map(L => () =>
  agent(
    `${DOCTRINE}\n\n${SETTLED}\n\n${THE_TASK}\n\n` +
    `YOU ARE THE ${L.key.toUpperCase()} LENS: ${L.brief}\n\n` +
    `Adjudicate decisively from your lens. Converge to ONE position. Deliver the required outputs crisply: binary deployability, concrete materiality thresholds, power-under-binary, zombie-under-binary, the verdict, and the realistic prior (separated from verdict type).`,
    { label: `lens:${L.key}`, phase: 'Lenses', schema: LENS_SCHEMA })
))).filter(Boolean)

const lensBrief = lensResults.map(l =>
  `## LENS: ${l.lens}\nHEADLINE: ${l.headline}\nVERDICT: ${l.verdict} (realistic prior: ${l.realistic_prior})\n` +
  `BINARY DEPLOYABILITY: ${l.binary_deployability}\nMATERIALITY THRESHOLDS: ${l.materiality_thresholds.join(' | ')}\n` +
  `POWER UNDER BINARY: ${l.power_under_binary}\nZOMBIE UNDER BINARY: ${l.zombie_under_binary}\nBOTTOM LINE: ${l.one_line}`
).join('\n\n')

log(`Lens verdicts: ${lensResults.map(l => `${l.lens.split(/[ /]/)[0]}=${l.verdict}`).join(', ')}`)

phase('Adjudicate')

const ARTIFACT = 'docs/research/27_habitat_binary_materiality_refinement.md'

const finalSummary = await agent(
  `${DOCTRINE}\n\n${SETTLED}\n\n${THE_TASK}\n\n` +
  `FOUR LENSES:\n${lensBrief}\n\n` +
  `YOU ARE THE ADJUDICATOR (research lead, trader-first). Reconcile to ONE verdict under BOTH restrictions. Where lenses disagree, adjudicate explicitly. The trader/PM lens is decisive on materiality numbers; the useless-prosecutor sets the downgrade bar; the firewall architect's type-lock is binding; the econometrician's power read sets honest expectations. Be honest about verdict TYPE vs realistic PRIOR — a clean expected NON-FINDING is doctrinally acceptable (§11.3), do not inflate.\n\n` +
  `WRITE the refinement to ${ARTIFACT} using the Write tool — dense, pre-registration-grade, no narrative inflation. It is the FREEZE-REFINEMENT layer that will fold into the combined pre-registration (it does NOT itself freeze/authorize the run). It MUST contain, as explicit sections:\n` +
  `- Status header (date 2026-06-04, RESEARCH-MODE freeze-refinement; supersedes the weighting channel in doc 26 for v1; NO execution authorized).\n` +
  `- The two restrictions stated precisely, with rationale.\n` +
  `- BINARY-ONLY v1 OUTPUT CONTRACT (the type-lock): eligible/ineligible enum per instrument per period; hysteresis rule to bound flip-flop turnover; rebalance cadence; explicit forbidden fields (no probability/score/weight/confidence/streak-as-proxy); the proof that the zombie path is severed at the type level.\n` +
  `- FROZEN MATERIALITY HURDLE: the pre-registered practical thresholds with concrete numbers (net-of-cost Sharpe floor, turnover ceiling/reduction, max-DD improvement, capacity floor), the conjunction-vs-disjunction structure and why, and the PM decision each maps to. State the NON-FINDING band explicitly.\n` +
  `- UPDATED SUCCESS/FAILURE CONDITION for binary gating: ARM B = cheap 1-line binary universe filter; ARM A = habitat-eligibility orthogonalized against B (discordant-cells); ARM C = flat. VALUE PRESENT iff the incremental binary-gated book clears BOTH statistical significance (CI excludes 0, FWER across full search, >=2 independent OOS habitats, no argmax) AND the material hurdle; VALUE ABSENT / NON-FINDING otherwise. Spell out the exact inequalities.\n` +
  `- POWER + FALSE-NEGATIVE note under binary coarsening, and why an expected NON-FINDING is acceptable.\n` +
  `- REVISED ZOMBIE-STATE-T RISK under binary-only (level + why it drops).\n` +
  `- THE VERDICT: ECONOMICALLY_USEFUL_IF vs LIKELY_TRUE_BUT_INERT, with explicit separation of verdict TYPE (decidable conditional) from realistic PRIOR (likely outcome), and the four-lens vote.\n` +
  `- What this changes for the COMBINED PRE-REGISTRATION: the exact deltas to fold into docs 25+26 before STEP 0 (binary type-lock replaces weighting in E-block; materiality hurdle added to the success condition).\n` +
  `- Surviving uncertainty, explicit non-conclusions, next action (write/freeze the combined pre-reg on authorization).\n\n` +
  `After writing, RETURN a tight summary: the verdict + verdict-type-vs-realistic-prior + four-lens vote; the binary output contract in one line; the frozen materiality numbers; the revised zombie risk; and the exact deltas to fold into the combined pre-reg.`,
  { label: 'adjudicate:artifact', phase: 'Adjudicate' })

return {
  artifact: ARTIFACT,
  lens_votes: lensResults.map(l => ({ lens: l.lens, verdict: l.verdict })),
  summary: finalSummary,
}
