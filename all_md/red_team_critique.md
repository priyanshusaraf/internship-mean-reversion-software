# Red Team Critique — Waiting-Period Package

**Status:** DRAFT.
**Date:** 2026-06-03.
**Team:** F (Red Team) — adversarial pre-promotion review of the five waiting-period deliverables.
**Posture:** Each deliverable is assumed wrong until it survives attack. Mission: find hidden hindsight,
leakage, overfit, theory creep, fake adaptivity, impossible implementation, hidden assumptions, and
unverified/false factual claims, before any of these becomes permanent AMR law.

**Method.** All five docs read in full. Load-bearing factual claims fact-checked against primary sources
(NBER/RFS/JFE PDFs text-extracted locally where the fetch model choked on the binary). Internal anchors
cross-checked against the on-disk `data/cohort_manifest.md`, `docs/research/12_*`, and the (empty)
`docs/decisions/ADR_003_roll_adjustment.md`.

**Verification key:** ✅ CONFIRMED (primary source) · ⚠️ PLAUSIBLE-BUT-UNVERIFIED / MISLABELED · ❌ FALSE-as-stated.

---

## 0. Headline verdicts (one line each)

| Deliverable | Verdict | Single deciding condition |
|---|---|---|
| **A — Canonical Spread Protocol** | **APPROVE-WITH-REVISIONS** | Stop deferring the roll law to an empty ADR_003; demote RA-1/RA-2 and the Kalman "residual-manufacturing" claim to explicitly UNDEMONSTRATED. |
| **B — Temporal Ontology** | **APPROVE-WITH-REVISIONS** | Kill the implied "VR(q) curve is trap-free"; it is consistent-but-biased in small samples (overlapping-window bias, Lo-MacKinlay z* heteroskedasticity sensitivity). |
| **C — Institutional MR Lit Review** | **APPROVE-WITH-REVISIONS** | Fix the Khandani-Lo **−62.5σ frequency misattribution** (it is a daily-strategy event magnitude normalized by a 60-min sigma, NOT a "60-minute contrarian return"). |
| **D — Post-State-T Morphology** | **APPROVE-WITH-REVISIONS** | The horizon-VR sign-flip is **not** a clean extrapolation/null discriminator; the selection-on-deviation null *can* manufacture a flip. Downgrade it from "cleanest separator" to "candidate, surrogate-gated." |
| **E — Elite Data Acquisition** | **APPROVE-WITH-REVISIONS** | Correct the inflated "18 yr individual-contract" depth (per-contract legs start ~Dec-2008 ≈ 17yr; FirstRateData advertises 15yr) and the gold-silver "fractional cointegration" mislabel; re-confirm Databento credits cover a *full-stack per-contract* pull. |

**No deliverable is APPROVE-AS-LAW as written.** None is REJECT outright — the skeletons are sound and the
causal instincts are correct. But every one carries at least one load-bearing overclaim that would harden
into false law if promoted unedited.

---

## A — Canonical Spread Construction Protocol (Team A)

### Kill shots (ranked)
1. **The roll law is built on a void.** §5 (RA-1/RA-2/RA-3) repeatedly defers final authority to
   `docs/decisions/ADR_003_roll_adjustment.md` — which is a **literal 0-byte file** (confirmed:
   `ADR_001`, `ADR_002`, `ADR_003` are all 0 bytes). The protocol forbids additive (Panama) back-adjustment
   and ratio adjustment *as spread legs*, mandates "build from actual individual contracts," then says
   "ADR_003 governs if it specifies a different method." **A frozen law cannot subordinate itself to an empty
   file.** As written, the single most consequential roll rule is simultaneously (a) asserted with FROZEN-RULE
   force and (b) self-marked LOW-confidence and overridable by a document that does not exist. This is a
   STRUCTURAL hole, not a wording nit: promote this and you have frozen a rule with a dangling pointer.
   **Fix:** either write ADR_003 first, or demote RA-1/RA-2 to PROVISIONAL and stop citing a nonexistent
   authority as binding.
2. **The Kalman-β "residual-manufacturing" claim is transferred, not demonstrated — and the doc admits it.**
   HR-4 forbids a Kalman hedge ratio on the grounds that "β-chasing is residual-manufacturing," explicitly
   carrying over the doc-07 lag-illusion verdict "verbatim" to the hedge-ratio level. The doc's own §8 concedes
   this "has **not** been empirically demonstrated at the β level in this repo (only at the μ\* level)." So a
   **FROZEN-RULE deferral rests on an analogical, undemonstrated mechanism.** The *deferral* is defensible on
   conservative grounds (don't add complexity nothing has earned); the *stated mechanism* ("it manufactures
   reversion") is a hypothesis dressed as a finding. Promote the deferral, not the mechanism-as-fact.
3. **"Naïve High/Low must be forbidden" is over-generalized.** §6/OHLC-3 is correct for a **synthetic
   multi-leg** spread `A−βB` (legs' intrabar extrema occur at different timestamps → counterfactual). But the
   doc states the rule with near-universal force, and the cohort manifest applies "HIGH/LOW UNTRUSTED" to
   *every* spread including **β=1 calendar spreads on the same underlying**. For a true **exchange-listed**
   calendar/crack spread that trades as its *own* instrument with its *own* order book (CME lists native
   calendar and crack spread products), the High/Low are **real, observed, synchronized** prints — not
   counterfactual. The protocol conflates "synthetic spread I computed from two leg series" with "spread as a
   traded instrument." **The forbid-H/L rule is correct for constructed spreads and FALSE for natively-traded
   exchange spreads.** It should say so.

### Hidden hindsight / leakage
- The causal firewall (C-1…C-6) is genuinely strong and is the best part of the doc — trailing-window β, lag
  the β (C-3), no future normalization (C-6), inner-join default (AL-1). No leakage found *inside* the rules.
- **One residual surface the doc names but under-polices:** AL-2 forward-fill "high fill fraction ⇒
  CONTAMINATED" has **no numeric threshold** (admitted in §8). Until a cutoff is pre-registered, "high" is a
  free post-hoc DOF — a small but real selection knob. Correctly flagged; must be closed before law.

### Theory creep / zombie risk
- **Clean.** This is a construction law; it emits no scores/detectors/timing. The zombie prohibition header is
  honored. No State-T leakage.

### Unverified / false claims
- ✅ Arm-0 anchor (§0): "0 deployment-domain whitelisted; all 8 spreads CONTAMINATED" — **CONFIRMED** against
  `data/cohort_manifest.md` (TRUSTED whitelist = `aapl_60, adanient, dell_60`; CONTAMINATED = the 8 spreads).
- ✅ Invalid-bar counts (§6.1): `g1_gold` 630, `ng12` 169, `rb23` 35 — **CONFIRMED EXACT** in the manifest.
- ✅ WTI CLK20 settled **−\$37.63 on 2020-04-20** — **CONFIRMED** (widely documented; correct contract/date).
- ✅ Engle-Granger 1987 *Econometrica* 55(2):251-276; Johansen 1991 *Econometrica* 59(6):1551-1580 — citations
  correct.
- ⚠️ The continuous-futures roll comparison table (§5) is sourced to a stack of practitioner blogs
  (QuantStart/QuantPedia/arbitragelab/QuantInsti). The *mechanics* (Panama additive → drift bias + possible
  negative history; ratio → preserves % returns but rescales levels) are textbook-correct, but the "VIX 14.8%
  phantom jump vs 0.3% real" example is a single uncited practitioner anecdote presented as illustrative fact.
  Low stakes; label as illustrative.

### Verdict: **APPROVE-WITH-REVISIONS.**
**Deciding condition:** the roll section may not be promoted while ADR_003 is empty. Either write ADR_003 or
demote RA-1/RA-2 to PROVISIONAL and remove the "ADR_003 governs" subordination. Secondarily, scope the H/L
forbiddance to *constructed* spreads (exempt natively-traded exchange spreads), and relabel the Kalman
residual-manufacturing mechanism as UNDEMONSTRATED-AT-β-LEVEL.

---

## B — Temporal Ontology of Mean Reversion (Team B)

### Kill shots (ranked)
1. **"VR(q) is the one trap-free reading" is overstated — VR is consistent but NOT unbiased in small samples.**
   The memo leans hard on the variance-ratio curve as the *escape hatch* from the smoother trap ("the only
   trap-free reading of reversion character is return-space VR"). The estimator literature says otherwise:
   Lo-MacKinlay (1988) VR with **overlapping** long-horizon returns is **consistent but biased in finite
   samples**, with documented size distortion that worsens as q grows relative to T, and the test's validity
   under heteroskedasticity rests on the z* statistic whose own finite-sample size is unreliable (Kim 2006
   wild-bootstrap and the "exact VR test with overlapping data" literature exist *precisely because* the
   asymptotic VR test misbehaves in small samples). On AMR's regime — short spreads, W≤250, q up to 20 —
   **this bias is live, not academic.** The memo's §4 caveat ("multiplies researcher DOF") catches the
   *selection* trap but not the *estimator-bias* trap. **A "trap-free" statistic that is biased exactly in the
   small-sample regime AMR operates in is not trap-free.** This is the single most important revision.
2. **Self-contradiction on horizon collapse vs the recommended discriminator.** §4/§7 (correctly) forbid
   `min()`-collapsing the VR(q) curve and insist on reporting the whole profile. But §0/§7 then recommend
   reading "equilibrium stability" as *the* discriminator — which is itself a scalar verdict ("did μ\* stay
   put?"). The memo never reconciles "never collapse the curve to a decision scalar" with "do collapse μ\*
   behavior to a stay-put/moved scalar." Not fatal, but the asymmetry is unjustified and invites the same
   selection critique one level over.
3. **The whole memo risks being a 40KB restatement of "use a fixed grid, don't tune."** Its actionable output
   (S-A: fixed pre-registered q-grid; no online half-life; no regime-κ) is correct but already implied by the
   frozen lookahead constitution + doc 04. As *law* it adds little beyond what doc 04 froze; its value is the
   external-literature corroboration, not new constraint. Risk: promoting it as a numbered doc creates the
   *appearance* of new findings where there is mostly synthesis. (Scope/altitude critique, not correctness.)

### Hidden hindsight / leakage
- The memo is *about* hindsight and is rigorous on it. §5 and §8's DANGER list (D1 full-sample-tuned window;
  D2 lag-illusion; D3 regime-κ noise-tracking; D4 hindsight horizon-selection; D5 anchored-window
  over-training) are the correct trap taxonomy. No leakage *committed*; this is the doc that names the traps.
- **One subtle self-snare:** §5.1 endorses Kalman/particle/adaptive-bandwidth filters as "legitimately causal"
  *if hyperparameters are pre-frozen*. True — but "adaptive bandwidth" with a frozen rule is a thin line from
  "bandwidth that adapts to data," and the memo's own D1 says the leak hides in the *selection step* that
  "leaves no trace in the per-bar computation." The memo should state that **a recursive filter with a
  data-adaptive (not pre-frozen) bandwidth is D1, not §5.1** — currently a reader could mis-file it.

### Theory creep / zombie risk
- **Clean, and actively anti-zombie.** Explicitly: no detector/score/hazard/timing; κ "may inform intuition,
  may not gate in v0." S-B and S-C are REJECTED/DEFERRED with reopen triggers. Good kill-discipline.

### Unverified / false claims
- ✅ Yu (2012) *J. Econometrics* 169(1):114-122, MLE bias of κ, worst near unit root — **CONFIRMED** (real
  paper, correctly characterized; κ̂ upward-biased / overstates reversion speed is the correct reading).
- ✅ Lo-MacKinlay (1988) *RFS* 1(1):41-66, VR<1 reversion / >1 momentum, heteroskedastic-robust z* —
  **CONFIRMED**.
- ✅ Goyal-Welch (2008) *RFS* 21(4) conditioning penalty; Murray-Papell (2002) infinite half-life upper CI;
  Stock (1991) wide near-unit-root CIs; Avellaneda-Lee (2010) κ>252/30=8.4 gate — all consistent with the
  primary literature.
- ⚠️ Repo-internal anchor: the κ̂ simulation table (φ=0.98→SD(κ̂)=0.083; φ=0.95→SD(κ̂)=0.093) is attributed to
  "doc 04 §1.5.3." Not independently re-simulated here; the *direction* (SD(κ̂) > κ near unit root) is
  textbook-correct, so the claim is plausible, but it is a repo-internal number the red team did not recompute.
- ⚠️ Self-flagged unverified items (Wang-Phillips-Yu exact venue; Phillips 2014 page range) are honestly
  marked — good practice, no action.

### Verdict: **APPROVE-WITH-REVISIONS.**
**Deciding condition:** the memo must stop implying VR(q) is *unconditionally* trap-free. Add the
finite-sample / overlapping-window / heteroskedasticity-z* bias caveat and require the matched-surrogate
subtraction (which it already endorses for selection) to *also* neutralize estimator bias — i.e. real-minus-
surrogate VR, never raw VR, because the surrogate carries the same finite-sample bias.

---

## C — Institutional MR Literature Review (Team C)

### Kill shots (ranked)
1. **The Khandani-Lo "−62.5σ" headline is FREQUENCY-MISATTRIBUTED.** Team C writes: *"the 60-minute contrarian
   return hit **−62.5σ on Aug 8, 2007** (table: Aug 6 −5.3σ, Aug 7 −15.4σ, Aug 8 −62.5σ, Aug 9 −26.1σ at
   60-min)."* The primary source (NBER w14465, p.38) **does** contain `8/8/2007 … -62.49` in a column headed
   "**60 Minutes**" — BUT that table's columns ("5 Minutes / 10 / 15 / 30 / 60 Minutes") are the **intraday
   sampling interval used to compute the volatility (sigma) denominator**, and each row is a **daily date**.
   The "July Sigma" normalizer row (3.53 at the 60-min column) confirms it. So −62.49 is the **standardized
   cumulative *daily* return of the Lehmann/Lo-MacKinlay contrarian strategy on 8/8**, normalized by a sigma
   estimated from 60-minute data — **NOT** "the 60-minute contrarian *return*." Team C's numbers match the
   column exactly (✅ magnitudes real), but the **description converts a daily-strategy event magnitude into a
   60-minute-frequency strategy return** (❌ as-stated). This is a MEASUREMENT-class error that would mislead
   any future reader about what the −62.5σ object *is*. The directional point (catastrophic contrarian loss as
   market-makers withdrew) survives; the framing does not.
2. **DLY skew result is correct but the "FI RV is not one habitat" caveat undersells one specific number.**
   ✅ The core figures are **CONFIRMED EXACT** from the primary PDF: equally-weighted FI-arb **Sharpe = 0.597**,
   **t = 2.78**, **gain/loss = 1.643**, "most positively skewed," vol-arb and MBS-premium negatively skewed.
   Excellent fidelity. Minor: the doc says LTCM "lost >$1.3B in volatility arbitrage alone" — this is sourced
   via DLY-citing-Lowenstein, i.e. secondary; flag as secondary-sourced, not primary.
3. **Practitioner-magnitude firewall is good but inconsistently applied.** §3 correctly brands trading-education
   profitability claims "unverified marketing." But §1.1 still passes through "calendar-spread arbitrage
   profits 'decreasing gradually'" and capacity claims as practitioner consensus without the same sk
   discipline. The doc's own rule ("use exchange/peer-reviewed for magnitudes; books for method, not numbers")
   is the right standard — apply it uniformly.

### Hidden hindsight / leakage
- N/A as a leakage surface — this is an external-literature synthesis making **no claim on AMR's own data**
  (stated up front). The risk here is **factual fidelity**, not temporal contamination, and on that axis it is
  the most-verified of the five (four primary PDFs text-extracted). The −62.5σ misattribution is the one real
  blemish.

### Theory creep / zombie risk
- **Clean and disciplined.** Every "AMR instrument" suggestion is explicitly framed as *characterization*, not
  a detector ("MR character is VIX-conditional, NOT a timing signal"; "co-divergence … explicitly not a
  detector/score"). The §2.5 etiology point and the §4.4 "etiology-unidentified ⇒ low-confidence default" are
  exactly aligned with the constitution. No State-T resurrection.

### Unverified / false claims (summary)
- ✅ **DLY 2007**: Sharpe 0.597, t 2.78, gain/loss 1.643, positive skew, vol-arb/MBS-premium negative skew —
  **CONFIRMED EXACT** (primary, *RFS* 20(3):769 author copy, text-extracted).
- ✅ **Nagel 2012**: +**0.22 pp/day** per VIX-pp, **adj. R² = 0.07** on daily — **CONFIRMED EXACT** (primary,
  NBER w17653, text-extracted). Strong.
- ✅ **McLean-Pontiff**: 2016 JF = 97 anomalies, **26% OOS / 58% post-pub** (publication effect ≈32pp); 2013 WP
  ≈82 chars; decay greater for cheaper-to-arbitrage names — **CONFIRMED** (numbers match exactly).
- ❌ **Khandani-Lo −62.5σ "60-minute contrarian return"** — **MAGNITUDE REAL, FREQUENCY-LABEL FALSE** (see kill
  shot 1). The value belongs to the **daily** contrarian strategy, normalized by 60-min sigma.
- ✅ Szymanowska et al. 2014 *JF* 69(1) term premia ≈1-3%/yr via calendars; Shleifer-Vishny 1997; Xiong 2001;
  Brunnermeier-Pedersen 2009; Working 1949 — citations consistent with primaries/credible secondaries.

### Verdict: **APPROVE-WITH-REVISIONS.**
**Deciding condition:** fix the Khandani-Lo −62.5σ frequency misattribution (re-label as the standardized
*daily* contrarian event magnitude, sigma estimated at 60-min sampling). This is the **load-bearing episode in
the binding context** — getting its description wrong propagates a measurement misconception. Everything else
is minor.

---

## D — Post-State-T Morphology: Mechanism Map (Team D)

### Kill shots (ranked)
1. **The horizon-VR sign-flip is NOT a clean extrapolation-vs-null discriminator — the selection null can
   produce a flip too.** This is the doc's headline claim (§6, §8, §9: "the cleanest price-only separator… a
   short-continuation → long-reversal sign flip the selection null structurally cannot make," ranked #1). Attack:
   **selection-on-deviation conditions on a large terminal |z|.** Conditioning on an extreme endpoint
   mechanically induces **negative** serial dependence on the *far* side of the peak (regression-to-the-mean /
   Lo-MacKinlay (1990) conditioning), while the directional run-up supplies **positive** short-lag dependence.
   A statistic that is positive at short q (run-up) and negative at long q (post-peak mean-reversion of the
   selected extreme) is **exactly a sign flip** — and it is produced by *selection alone*, with no
   extrapolation, no positive feedback, no economics. The doc asserts the null is "monotone"; that is **not
   generally true for an endpoint-anchored, |z|-conditioned VR curve.** The flip's *existence* therefore does
   not separate §6 from §1; only a **real-minus-matched-surrogate** flip (surrogate under identical |z|
   anchoring) could — which is the doc's own §1(d) anti-hook, but §9 forgets it when crowning §6 "cleanest."
   **The #1-ranked mechanism's #1 evidence is contaminated by the very null the doc says it beats.** This must
   be downgraded.
2. **"Mechanism map, not theory" is doing a lot of load-bearing disclaiming over a menu that re-imports flow
   objects.** §2 (inventory), §4 (forced positioning), §5 (liquidity vacuum) are exactly the microstructure
   etiology the repo has repeatedly DEFERRED-pending-data. The doc flags every one as "data-gated," which is
   honest — but a "menu" of six mechanisms, ranked, with falsification hooks, is one promotion away from
   becoming a research program that quietly resurrects per-deviation etiology classification. **Zombie-adjacent
   risk:** none of these is State-T, but §2/§4/§5's "post-peak reversal conditioned on flow/depth" is, in
   spirit, a *per-episode favorability* object. It is currently caged correctly (corpus-level, time-symmetric,
   surrogate-relative); the cage must stay explicit on promotion.
3. **§3 (information momentum) leans on the equilibrium-stability discriminator to do work it may not be able to
   do causally.** The proposed split — "classify each |z|-peak by whether μ\* structurally shifts over the
   *forward* window" — is described as "runnable now… already the licensed discriminator." But a **forward**
   μ\*-break test is forward-looking by construction; doing it *causally* (only data ≤ t) at the peak is a
   different, weaker test than the full-information break the prose implies. The doc should state which
   information mode (causal vs full-info §6.2) each hook runs in — it currently blurs them.

### Hidden hindsight / leakage
- **§7 (GARCH) is the strongest part** and is correctly named "mandatory hygiene": devolatilize returns and
  use a GARCH(1,1)-matched surrogate before crediting any mean mechanism. This is the right defense and is
  *more* rigorous than the rest of the doc. Keep it; it should gate everything.
- **The latent leak is in §6d/§8/§9** as above: presenting a selection-producible sign-flip as null-exceeding
  is precisely "hindsight-as-discriminator" if the surrogate subtraction is skipped. The doc *names* the
  surrogate requirement in §1 then *forgets* it in its ranking conclusion.

### Theory creep / zombie risk
- **Mostly clean, with the structural caveat above.** Explicit: "No State-T resurrection… a mechanism that
  reduces to the killed morphology is rejected on sight"; "NO detector/score/timing/per-bar object." The
  guardrails are stated well. The risk is not a committed zombie but **promotion drift**: a ranked mechanism
  menu naturally pulls toward "pick the winning mechanism," which is one step from per-episode labeling.

### Unverified / false claims
- ✅ Hendershott-Menkveld (2014) *JFE* price pressures, **0.92-day half-life**, 0.49% avg pressure — consistent
  with the published paper.
- ✅ The behavioral/micro stack (Hong-Stein 1999; DHS 1998; George-Hwang 2004 "no reversal at 52-week-high
  extremes"; De Bondt-Thaler 1985; Barberis-Greenwood-Jin-Shleifer 2018; Coval-Stafford 2007;
  Kirilenko-Kyle-Samadi-Tuzun 2017; Lobato-Savin 1998 ACF-invalid-under-GARCH; Beveridge-Nelson 1981;
  Fama-French 1988) — citations are accurate and correctly characterized. Literature scholarship is solid.
- ⚠️ The **analytical** claim "horizon-VR sign flip distinguishes extrapolation from the null" (§6c/§9) is
  **not a citation but a derivation**, and it is **wrong as stated** (kill shot 1): the selection null is not
  monotone under endpoint anchoring. This is the one substantive technical error.

### Verdict: **APPROVE-WITH-REVISIONS.**
**Deciding condition:** downgrade the horizon-VR sign-flip from "cleanest separator the null cannot make" to
"candidate separator, valid only as real-minus-matched-surrogate under identical |z| anchoring," and state the
information-mode (causal vs full-info) of every hook. With those two edits the map is a legitimate
observatory-prep menu; without them it ships a false discriminator as its headline.

---

## E — Elite Data Acquisition Plan (Team E)

### Kill shots (ranked)
1. **"18 yr of individual-contract history" is inflated and conflates continuous-series depth with
   per-contract-leg depth.** The plan's entire thesis is "GET RAW LEGS, not pre-made spreads" (correct, and the
   best idea in the package). But it then claims "~18 yr" of *individual contract* data for CL/RB/HO/GC/ZS via
   FirstRateData (T1-A…E, master table). Verified: FirstRateData's CL page advertises **15 years**, and
   **individual contracts start at `CLZ08` (Dec 2008)** — i.e. per-contract legs are ~**17 yr** at most, and
   the deepest *continuous* (not per-contract) series start 2007/2008. The "18 yr" figure (a) overstates by
   1-3 yr and (b) **silently swaps the quantity that matters** (per-contract leg depth) for the easier number
   (continuous-series depth). For the calendar/crack/crush spreads the plan targets, you need *both legs as
   separate contracts simultaneously* over the window — the binding depth is the per-contract one, which is
   shorter. **The plan's headline feasibility claim rests on the wrong depth number.** Not fatal (17yr ≫ the
   750-bar floor), but a law-grade doc must not cite leg depth it has not confirmed.
2. **"Gold-silver fractional cointegration 2015-2025 [SSRN 5710242]" is MISLABELED.** Verified: SSRN 5710242
   exists and *does* use COMEX futures 2015-2025 and confirms cointegration (p=0.0235) with a Kalman dynamic
   hedge — BUT it is titled **"Gold Silver Pair Trading — Mean Reversion Strategy Using Machine Learning"
   (Mittal & Mittal)** and reports **standard** (Engle-Granger/Johansen) cointegration, **not "fractional
   cointegration."** "Fractional cointegration" is a *different* literature (Caporale-Gil-Alana and the older
   "Parities and Spread Trading in Gold and Silver" fractional analysis, different periods). Team E has fused
   two distinct strands and attached the fractional label to the wrong paper. ⚠️ The economic point (GC-SI
   cointegrates, β drifts → causal time-varying β) survives; the citation label is wrong.
3. **"Free is good enough is a trap" is correct, but the Databento $125 claim needs a feasibility re-check at
   the stated scope.** Verified: Databento **does** give **$125 sign-up credits** and GLBX.MDP3 **does** carry
   every CME/NYMEX/COMEX/CBOT contract month. BUT the credit FAQ says credits apply to historical data **or the
   first month of a subscription** — and a **full per-contract-stack pull** (every monthly CL/RB/HO/GC/ZS/NG
   contract over ~17 yr, even at daily bars) is a *much* larger query than the "$2.17 example." The plan asserts
   "$125 credits cover a daily-bar pull of the full CL stack" without a metered cost estimate. **Likely true for
   one product's daily bars; unverified for the full Tier-1 set.** The mitigation the plan already names
   (validate schema on free samples first; use `metadata.get_cost` before pulling) is correct — but the
   "≈$0-$200 for all five" bottom line is an *estimate presented as a budget*. Re-meter before authorizing.

### Hidden hindsight / leakage
- **This is the most leakage-aware of the five and its core instinct is exactly right:** a pre-made spread
  re-imports the Arm-0 full-sample-β contamination, so source legs and build causally (rolling/Kalman β ≤ t,
  causal roll N days pre-expiry, inner-join, level-diff, Open/Close only). §7 acquisition protocol is sound.
- **One forward-looking snag:** §3 repeatedly promises causal β "rolling/Kalman" — but Team A's protocol just
  **DEFERRED Kalman-β (HR-4)** and prefers β=1 / rolling for calendars. Team E should align: for the Tier-1
  calendars β≈1 (no estimation), and "Kalman β" should not be floated as a default when the sister deliverable
  forbids it for v0. Minor cross-doc inconsistency, but it matters if both become law.

### Theory creep / zombie risk
- **Clean.** Pure sourcing/prioritization; no statistic, no detector. T3-B (order-flow/COT) is correctly
  spec-only and deferred. No State-T.

### Unverified / false claims (summary)
- ✅ **Databento $125 sign-up credits**, GLBX.MDP3 = all CME-complex contract months — **CONFIRMED** (credits
  also usable toward first subscription month; full-stack cost unmetered — see kill shot 3).
- ✅ **GLD/GDX fails cointegration, ADF ≈ −1.64** (below 10% level), Johansen confirms none — **CONFIRMED**
  (matches QuantStart/Chan; the do-not-use warning is correct and well-placed).
- ✅ **WTI-Brent ~2010 structural break** (post-shale decoupling) — **CONFIRMED** (Dec-2010 break; decoupling
  July-2010→Aug-2011 in the persistence literature). ⚠️ The specific attribution "Geyer-Klingeberg, Wiley JFM
  2021/fut.22184" could not be confirmed as that author/paper — the *break* is real, the *byline* is unverified.
- ⚠️ **"18 yr individual-contract" depth** (CL/RB/HO/GC/ZS) — **INFLATED**; per-contract legs ~Dec-2008 (≈17yr);
  FirstRateData advertises 15yr. Conflates continuous vs per-contract depth.
- ⚠️ **Gold-silver "fractional cointegration" [SSRN 5710242]** — paper exists & cointegration confirmed, but it
  is **standard** cointegration in an ML pair-trading paper, **not** "fractional"; label is wrong.
- ⚠️ Soybean crush ratio "10 ZS : 11 ZM : 9 ZL", GPM = 0.022·ZM + 0.11·ZL − ZS — matches the CME Soybean Crush
  reference; unit conventions (gal→bbl ×42; bu/ton/lb) are correct in spirit (not re-derived here).

### Verdict: **APPROVE-WITH-REVISIONS.**
**Deciding condition:** correct the per-contract-leg depth claim (≈17yr, legs from ~Dec-2008, not "18yr
individual"), re-label the gold-silver citation as standard (not fractional) cointegration, and re-meter the
Databento full-Tier-1 pull cost with `metadata.get_cost` before the "$0-$200" budget is trusted. The
acquisition *strategy* (legs-not-spreads, same-exchange, causal build) is correct and should proceed; only the
specific factual claims need tightening.

---

## Cross-cutting traps (common to several deliverables)

1. **"Surrogate-relative" is invoked as a ritual but skipped at the moment of conclusion.** B and D both
   correctly state that the *only* honest reading is **real-minus-matched-surrogate** (to net out both
   selection AND finite-sample/GARCH estimator bias) — then both quietly headline a **raw** statistic as the
   discriminator (B: "VR is the trap-free reading"; D: "the sign-flip the null cannot make"). The surrogate is
   the firewall; using the raw statistic as evidence is the leak. **Every VR/morphology verdict in this package
   must be real-minus-surrogate, never raw — and the surrogate must carry the same finite-sample bias.** This
   is the single most important cross-cutting fix.
2. **Pointer-to-a-void / internal-anchor risk.** A defers binding authority to an **empty ADR_003**. Several
   docs lean on doc-04/06/07/08/11/12 internal numbers as settled (κ̂ SD, ACF≈0.88, the State-T kill). The
   *external* literature is well-verified; the *internal* anchors are taken on faith. The cohort manifest and
   doc 12 checked out where tested — but the package treats repo-internal findings as immutable law, which is
   fine *only if* those docs are themselves frozen-and-correct. Flag: a law built on a 0-byte ADR is not law.
3. **Inflated/mislabeled specifics riding on correct directional claims.** C (−62.5σ frequency), E (18yr legs;
   fractional-cointegration label; Geyer-Klingeberg byline). In each case the *direction* is right and the
   *specific* is wrong. For a document that will be cited as ground truth, a right-direction/wrong-number claim
   is more dangerous than a hedge, because it launders precision it did not earn.
4. **Same-exchange "synchronized" optimism.** E leans on "same exchange/session ⇒ synchronized legs ⇒ clean
   spread." Mostly true within CME Globex, but settlement-time vs continuous-trading timestamp conventions,
   contract-specific pit/electronic session differences, and roll-seam alignment still require the C-5/AL
   machinery from A. The two docs are compatible but E slightly understates the residual alignment work A
   mandates.
5. **Half-life / κ used as a sizing or universe gate while admitted unidentifiable.** B proves κ̂ is
   biased+high-variance+skewed+∞-CI, yet C (via Avellaneda-Lee κ>8.4 gate, Chan half-life sizing) and E (NG
   "seasonal μ\*") still route decisions through κ/half-life. B itself flags this tension; the package as a
   whole should state once, loudly: **κ/half-life informs intuition, never gates, in v0** — and make sure C/E
   don't imply otherwise.

---

## The one deliverable most likely to cause damage if trusted as-is

**Team D (Post-State-T Morphology).** Reasoning: A/B/C/E make *construction/sourcing/synthesis* claims whose
errors are bounded and local (an empty ADR, an inflated year-count, a mislabeled frequency). D makes an
**analytical discrimination claim** — "the horizon-VR sign flip separates real extrapolation from the
selection null" — that is **technically wrong in a way that points the entire downstream Arm-A/Arm-B program at
a contaminated discriminator.** It is also the doc explicitly nominated (§9) as "the natural successor probe to
fold into Arm A," so a false "cleanest separator" here would propagate directly into the next authorized
experiment. The selection-on-deviation null **can** manufacture a short-positive/long-negative VR flip via
endpoint conditioning (regression-to-the-mean on the selected extreme); presenting that flip as null-exceeding
without surrogate subtraction is the exact "smoother-manufactured-but-looks-real" pathology the constitution
exists to stop — one level up, in the morphology layer. **D is the most seductive because it is the most
sophisticated and the most action-adjacent, and its headline is the one with a real technical hole.**

(Runner-up for damage: **A**, solely because of the empty-ADR_003 pointer — a frozen roll law that subordinates
itself to a nonexistent file is an institutional hazard even though the rules themselves are mostly right.)

---

## Promotion gate — per deliverable (DRAFT → permanent numbered research doc)

| # | Deliverable | Promote now? | What must change first |
|---|---|:--:|---|
| **A** | Canonical Spread Protocol | **NO — not yet** | Write ADR_003 (or demote RA-1/RA-2 to PROVISIONAL and delete the "ADR_003 governs" subordination); scope the H/L-forbid rule to *constructed* spreads (exempt natively-traded exchange spreads); relabel the Kalman residual-manufacturing mechanism as UNDEMONSTRATED-at-β. Then promotable — the causal firewall (C-1…C-6, OHLC-1…5) is genuinely strong. |
| **B** | Temporal Ontology | **NO — light edit** | Remove the implication that raw VR(q) is unconditionally trap-free; add the finite-sample/overlapping/heteroskedasticity-z* caveat; require real-minus-surrogate VR. Then promotable (its conclusions are conservative and correct). |
| **C** | Institutional MR Lit Review | **NO — fix one fact** | Correct the Khandani-Lo −62.5σ frequency misattribution (daily strategy, 60-min sigma denominator). Apply the practitioner-magnitude firewall uniformly. Then promotable — it is the most factually-verified doc in the set. |
| **D** | Post-State-T Morphology | **NO — substantive edit** | Downgrade the horizon-VR sign-flip to a surrogate-gated candidate (the selection null is NOT monotone under endpoint anchoring); state causal-vs-full-info mode per hook; keep §7 GARCH hygiene as the gate on all mechanisms. Then promotable as an observatory-prep menu (explicitly not a hypothesis). |
| **E** | Elite Data Acquisition | **NO — fix specifics** | Correct per-contract-leg depth (~17yr, legs from ~Dec-2008, not "18yr individual"); relabel gold-silver as standard (not fractional) cointegration; re-meter the Databento full-Tier-1 cost; align β guidance with A's HR-4 (β≈1 for calendars, no Kalman default in v0). Then promotable — the legs-not-spreads strategy is correct. |

**Net:** zero of five may be promoted to permanent numbered law *today*; all five are *close* and become
promotable after the bounded, specific edits above. The package as a whole is **research-grade and
constitution-aligned in posture** — its failure mode is not roadmap drift or zombie resurrection (those are
well-guarded) but **overclaimed specifics and one false analytical discriminator (D)** that must be caught
before they harden.

---

## Confirmed-FALSE claims (for the record)

1. **Team C — Khandani-Lo "60-minute contrarian return hit −62.5σ":** ❌ FALSE-as-stated. The −62.49 value is
   the standardized **daily** Lehmann/Lo-MacKinlay contrarian-strategy magnitude on 8/8/2007, with the sigma
   denominator estimated at 60-minute sampling (NBER w14465 p.38, "July Sigma" row = 3.53 at 60-min). Magnitude
   real; "60-minute return" frequency label wrong.
2. **Team D — "horizon-VR sign flip is a flip the selection null structurally cannot make":** ❌ FALSE as a
   general analytical claim. Endpoint (|z|≥θ) conditioning induces regression-to-the-mean on the selected
   extreme → a short-positive/long-negative VR profile is producible by selection alone. Only a
   real-minus-matched-surrogate flip would discriminate.
3. **Team E — gold-silver "fractional cointegration 2015-2025 [SSRN 5710242]":** ❌ mislabel. SSRN 5710242 is a
   *standard*-cointegration ML pair-trading paper (Mittal & Mittal), not a fractional-cointegration study.
4. **Team E — "18 yr individual-contract" futures depth:** ❌ inflated/conflated. Per-contract legs ≈17yr (from
   ~Dec-2008); FirstRateData advertises 15yr; the figure swaps continuous-series depth for per-contract depth.

*(Team A's empty-ADR_003 dependency is a STRUCTURAL defect, not a false factual claim — recorded as a kill shot,
not in this list.)*
