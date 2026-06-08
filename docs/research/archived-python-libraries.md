# Archived — External Candidates (Libraries & Methods)

> Provenance log for external tools/methods evaluated and **deferred/archived**, with named
> reopen triggers so they do not resurface as zombies (§4, §11.4). Not active work. One entry
> per candidate. Reopen requires the trigger satisfied + freeze-break authorization where flagged.

---

## A. RS-CCC-GARCH regime-switching VRP engine (external paper, Quant Insider 2026-06-02)

- **Source:** `external_paper_rs_ccc_garch_breakdown.md` (faithful reconstruction).
- **Status:** ARCHIVED.
- **Claim / what it is:** regime-switching CCC-GARCH (Hamilton filter + EM, K=2/3 vol states) forecasting realised variance, differenced against event-cleaned implied vol to time a **short-vol VRP carry** book.
- **Why archived (not adopted):**
  - Thesis is **orthogonal** — VRP carry (implied rich-to-realised), not mean reversion. Entire implied side (event multiplier Eq.10–12, delta-hedge cost) out of scope as strategy.
  - The only intersection is the regime layer, and adopting it as a "suspend-MR vs size-down" classifier is **predictive regime classification wired to a sizing decision** = structurally the killed object class (State T, doc 11/24). §10 explicitly defers HMMs / regime classifiers.
  - **Transfer is fatal-by-default** (paper's own §8.3): K-state is a *volatility* regime fit on returns; low-vol ≠ high-MR-prob. Importing a classifier built for a different signal, unproven on our VR(q) habitat.
  - Causal discipline it preaches (filtered-not-smoothed, rolling re-est) is **already encoded** here (causal firewall, ADR-002) — corroboration, zero integration value.
- **One transferable fact (already held):** stress-state cross-asset correlation spike → diversification fails when most needed (their Fig 5). Live PM caveat for Track 1/2 book construction (cf. LE-GF independence ρ=0.013 — don't trust that off-diagonal under stress). Known stylized fact; no model import required to honor it.
- **Reopen trigger (BOTH required):** (1) a confirmed real-data MR edge exists (survives §11.8 / probation), AND (2) an independent, pre-registered test shows vol-regime labels correlate with MR favourability. Plus §4 zombie-reopen test (this is State-T-adjacent machinery).
- **Trader relevance:** none as strategy; marginal as a diversification-stress caveat already in hand.

---

## B. NumPyro / Bayesian posterior over half-life κ (NUTS / SVI)

- **Source:** external agent recommendation (2026-06-06) + temporal ontology note flagging κ as a fragile nuisance parameter with flat likelihood near the unit root.
- **Status:** DEFERRED (Phase 3+).
- **Claim:** carry the full **posterior over κ** instead of a point estimate — principled response to the flat-likelihood/near-unit-root fragility.
- **Why deferred (not adopted now):**
  - **Sequencing backwards:** carrying a posterior over κ before confirming reversion *exists* on real data is precision on an unestimated object. We are pre-confirmation on outright MR — nothing to be Bayesian about yet.
  - **Freeze-break, not just overengineering:** NumPyro/JAX is **not in the frozen stack §8** (we hold FilterPy/ARCH/statsmodels/scipy). Adoption requires explicit §8 freeze-break + authorization — cannot enter as a quiet dependency.
  - Collides with §7 (no overengineering / no premature abstraction).
- **Reopen trigger (BOTH required):** (1) an outright-MR edge has survived probation on real data (confirmed / conditional-survival), AND (2) the deploy/size/hold decision is **demonstrably sensitive to κ uncertainty** (point-κ vs posterior-κ flips a real decision). Until (2), a point estimate + documented flat-likelihood caveat is adequate and cheaper.
- **Falsification gate (prevents noise-manufacturing):** if κ uncertainty never moves a decision, the posterior never earns its keep — do not build.
- **Trader relevance:** only if κ uncertainty materially changes sizing/hold of a confirmed survivor.
