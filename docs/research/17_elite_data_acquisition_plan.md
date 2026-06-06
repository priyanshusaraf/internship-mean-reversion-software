# Elite Data Acquisition Plan

**Document class:** Team-E (Elite Data Acquisition Lab) acquisition pre-registration for the AMR programme (DRAFT — pending red-team).
**Status:** REVISED & APPROVED for promotion → doc 17 (red-team revisions applied 2026-06-03; PARTIALLY OVERTAKEN BY EVENTS).

> **▸ RED-TEAM REVISIONS + EVENT UPDATE APPLIED (binding).**
> 1. **PARTIALLY OVERTAKEN:** deep real leg data has since arrived (`~/Downloads/mean-reversion-data`; audited in `data/mr_cohort_manifest.md`) — **46 TRUSTED legs, 7 constructible causal spreads**. This plan is no longer the immediate blocker; it stands as the path to *further* depth/coverage and as the standing sourcing protocol.
> 2. **Corrections:** gold–silver is **standard cointegration, not "fractional"**; individual-contract futures depth is **~17yr (from ~Dec-2008), not 18**; the Khandani–Lo figure is the daily magnitude (see doc 15). GLD/GDX cointegration-fail, WTI–Brent ~2010 break, and Databento $125 credits were red-team-verified TRUE.

**Date:** 2026-06-03.
**Mode:** Research Mode. Pure sourcing/prioritisation; no data acquired, no statistic computed, no signal. This document is a *shopping list with a justification per line*, gated to be executed only on explicit authorization.

> **▸ CONTEXT (frozen).** ADANIENT is a trend-heavy placeholder; the deployment domain (commodity
> calendar · intercommodity · cointegrated equity pairs · FI relative value · ETF RV) is expected
> materially more mean-reverting. State T is DEAD (zombie prohibition). This plan does not reopen it.
> See `CONTINUATION_STATE.md` §0; `docs/research/12_institutional_review_post_state_t.md`.

---

## 0. The decisive lesson this plan is built around (Arm-0)

Every deployment-domain "spread" on disk (`cl_brn_spread_60`, `coffee_cocoa_spread_1d`,
`ng12_spread`, `rb23_spread`, `hdfc_icici_spread_1d`, …) is a **precomputed single `close` series
with the legs discarded** (confirmed first-hand: float-noise closes like `3.1700000000000514`,
counterfactual OHLC, negative values with no leg to recover the hedge ratio). Therefore:

- The hedge ratio's **causality is unverifiable** from the file. If any used a full-sample β, the
  series is **stationary by hindsight construction** and indistinguishable from a legitimate one.
- High/Low on any `A−βB` series are **counterfactual** (the bar's true intrabar extreme is not
  `A_high − β·B_high`), so spread OHLC is untrusted for anything but `close`.

**THE #1 ACQUISITION CRITERION IS THEREFORE NOT "GET SPREADS." IT IS "GET RAW LEGS."** We must be
able to source each leg as an independent, raw, contract-level series and **build the spread
ourselves, causally** (rolling/Kalman β estimated only on information available at `t`). A pre-made
spread series — however reputable the vendor — re-imports the exact Arm-0 contamination and is
**rejected by default**. Synchronized legs (same exchange/session) are strongly preferred so the
reconstructed spread is clean rather than stitched across misaligned sessions.

**Corollary that kills the "free is good enough" temptation.** The free continuous-front-month feeds
(Yahoo `CL=F`, Stooq `cl.f`) provide a *single chained front-month series* and **cannot return
individual contract months** [yfinance #2399; Stooq]. They can rebuild **neither** a calendar spread
(needs M1 *and* M2 as separate legs) **nor** a verifiable roll. They are useful only as a free
cross-check oracle, **not** as a primary acquisition. Free constant-maturity Treasury yields (FRED
DGS2/DGS10) are **pre-interpolated** — they are not raw instruments and their curve spread is not
leg-reconstructable RV.

---

## 1. Prioritisation criteria (ranked, frozen for this plan)

1. **Causal reconstructibility (gate).** Raw legs sourceable as separate series; roll/contract specs
   knowable (CME product pages). If legs are not sourceable → instrument is rejected regardless of MR
   strength. *This is a hard gate, not a weight.*
2. **Deployment relevance / economic MR anchor.** A *structural* reason the spread reverts (cost-of-
   carry, processing/refining margin, cointegration, near-substitutes) — not a curve-fit.
3. **History depth.** ≥ **3×** the largest trailing window. The repo's committed floors:
   **< 504 daily bars = UNUSABLE for any single-instrument MR verdict; ≥ 750 daily-equivalent bars =
   TRUSTED** for multi-window VR up to W=250 (doc 12 §7). Target deep (10–18 yr) legs.
4. **Low contamination risk.** Aligned sessions, documented roll, positive-or-handled prices
   (return-space/log math breaks on negative spreads → level-difference math required and flagged).
5. **Ease / cost of sourcing.** Free public exchange data → Nasdaq Data Link → Stooq/FRED (oracles) →
   FirstRateData / Databento credits → paid vendor.
6. **Strength of MR evidence (literature).** Calendar (storage arbitrage), crack/crush (margin
   equilibrium), gold–silver (fractional cointegration), on/off-the-run (liquidity premium).

**What "elite ≠ largest" means here.** We deliberately acquire a **small, deep, leg-complete,
economically-anchored core** that unblocks the most AMR work per instrument, rather than a wide
shallow zoo. Five Tier-1 acquisitions is the target.

---

## 2. What each acquisition unblocks (the EV ledger)

| Blocked AMR work (from doc 12) | What it needs from this plan |
|---|---|
| **Arm A — habitat discovery** (highest research EV; currently blocked) | ≥1 *verified, leg-built, ≥750-bar* reverter to run multi-window surrogate-relative VR on |
| **Kalman μ\* S1/S2 cross-instrument panel** (doc 06 §15; could not run — only ADANIENT qualified) | ≥3 independent leg-built reverters of adequate depth → a real panel (not pseudo-replicate twins) |
| **Substrate OU-gate calibration** (doc 10; VR<0.75 gate **must NOT be tuned on ADANIENT**) | a *genuine* real reverter to adjudicate the OU gate on the correct regime |
| **MRScore cross-instrument fix** (doc 09 §7; self-rank inverts → only distributional cross-instrument form survives) | a multi-instrument trusted cohort to compute distributional (not self-ranked) discrimination |
| **Arm D — etiology** (north-star; data-gated) | (future) signed order flow / OI / COT on a flow-driven leg — *spec only, not Tier-1* |

A Tier-1 hit is defined as an instrument that, once leg-built, **simultaneously** feeds Arm A, the
Kalman panel, the OU-gate adjudication, and the MRScore distributional fix. The whole Tier-1 list
below is chosen so that, collectively, those four are unblocked at lowest contamination risk.

---

## 3. TIER 1 — acquire FIRST (the 5 that unblock the most AMR work)

> Selection logic: deepest history · cleanest single-exchange sessions · strongest *structural*
> (not statistical-only) MR anchor · legs trivially separable. All are **US-listed CME-complex
> futures** → one roll convention family, one session family, one sourcing path, COMEX/NYMEX/CBOT
> aligned settlement. This maximises reconstructibility and minimises session-misalignment
> contamination — the synthetic-spread rule's core requirement.

### T1-A — WTI crude **calendar** spread (CL M1–M2 / M1–M3 / M1–M12)
- **Exact instruments + legs.** NYMEX WTI `CL` individual contract months, e.g. `CLF26` (Jan-26),
  `CLG26` (Feb-26), … built into front-vs-deferred calendars. **Legs = two raw CL contract months.**
- **Why (economic MR anchor + history).** The single cleanest cost-of-carry reverter in commodities:
  the calendar spread is pinned by storage cost + convenience yield (contango/backwardation
  oscillates around carry). Both legs are the **same contract, same exchange, same session** → the
  reconstructed spread is *maximally* clean (no cross-asset session skew; the synthetic-spread rule
  is satisfied by construction). 18 yr of CL contract data exists [FirstRateData].
- **Sourcing difficulty/cost.** **LOW.** Databento GLBX.MDP3 returns *every* contract month with
  parent symbology; **$125 free sign-up credits** cover a daily-bar pull of the full CL stack
  [Databento pricing]. Alternatives: Barchart Premier (`CLF26` expired-contract symbology, full
  history) [Barchart help]; FirstRateData individual contracts (2-wk free sample to validate schema
  before buying) [FirstRateData].
- **Expected value.** **Very high.** A same-exchange calendar is the lowest-contamination real
  reverter obtainable → the ideal first instrument to adjudicate the **VR<0.75 OU-gate** off
  ADANIENT (doc 10 reopen trigger) and to seed Arm A. Roll fully documented on the CME CL product
  page (termination = 3rd business day prior to the 25th calendar day of the month preceding
  delivery) [CME].
- **Causal-reconstructibility risk.** **LOW.** Legs are literally separate contracts; β for a
  calendar is ≈1 (same underlying), so even a naive difference is economically valid and a causal
  rolling β is trivial. Main care: build the **continuous calendar** with an explicit, causal roll
  rule (roll N days before expiry); do not inherit a vendor's adjusted continuous.

### T1-B — **3-2-1 crack** spread legs (CL · RB · HO)
- **Exact instruments + legs.** NYMEX `CL` (WTI), `RB` (RBOB gasoline), `HO` (ULSD/heating oil),
  same-month contract triples. Classic refiner margin: **3 CL : 2 RB : 1 HO** (per-bbl unit-matched).
  **Legs = three raw NYMEX energy contracts.**
- **Why.** Refinery gross margin → strong economic reversion: a high crack incentivises more refining
  → product supply up → crack pulled back to equilibrium. Crack-spread option literature explicitly
  rests on **leg cointegration ⇒ the spread must be mean-reverting** [ScienceDirect crack-option
  valuation; Haigh–Holt JAE 2002]. All three legs trade on **NYMEX, same session** → clean synchronous
  bars.
- **Sourcing difficulty/cost.** **LOW.** Same path as T1-A; CL/RB/HO all in GLBX.MDP3 and on
  FirstRateData (18 yr energy depth) [Databento; FirstRateData].
- **Expected value.** **High.** A 3-leg structure exercises the causal-β machinery harder than a
  2-leg pair (the unit-conversion 3:2:1 is a *known* structural ratio, so we can test causal-β
  recovery against a ground-truth ratio — a built-in validation Arm A can use).
- **Causal-reconstructibility risk.** **LOW–MED.** Legs clean; the only subtlety is the unit
  convention (CL in $/bbl; RB, HO in $/gal → ×42 to bbl-equivalent). Documented on CME pages;
  must be applied explicitly, not silently.

### T1-C — **Soybean crush** spread legs (ZS · ZM · ZL)
- **Exact instruments + legs.** CBOT `ZS` (soybeans, ¢/bu), `ZM` (meal, $/short-ton), `ZL` (oil,
  ¢/lb). Board-crush ratio **10 ZS : 11 ZM : 9 ZL**; GPM = 0.022·ZM + 0.11·ZL − ZS [CME Soybean
  Crush Reference Guide]. **Legs = three raw CBOT contracts.**
- **Why.** Processing-margin equilibrium: strong crush → processors bid beans up / sell product →
  margin reverts. The most-studied agricultural cointegration spread (Bayesian cointegration case
  studies use the crush explicitly) [Oxford JRSS-C 2020]. **All legs CBOT, same session** → clean.
- **Sourcing difficulty/cost.** **LOW.** ZS/ZM/ZL on Databento GLBX (CBOT included) and FirstRateData
  (ZS continuous from 2008; ZM/ZL comparable) [Databento; FirstRateData].
- **Expected value.** **High.** Adds an **independent economic family** (ags, not energy) → the
  Kalman panel gets genuine cross-habitat breadth instead of 3 energy spreads that co-move. Another
  known-ratio leg structure → second ground-truth β check.
- **Causal-reconstructibility risk.** **LOW–MED.** Legs clean and synchronous; unit conversions
  (bu/ton/lb) are fixed and documented. ZL/ZM occasionally illiquid in far months → prefer
  front-cluster contracts for clean bars.

### T1-D — **Gold–Silver** spread legs (GC · SI)
- **Exact instruments + legs.** COMEX `GC` (gold) and `SI` (silver) contract months. **Legs = two
  raw COMEX metals contracts**; spread via causal hedge ratio (or the classic GC/SI ratio).
- **Why.** Near-substitute precious metals with a **fractionally-cointegrated** long-run parity;
  recent work confirms GC–SI cointegration holds on **live COMEX futures 2015–2025** and trades as a
  mean-reverting pair [SSRN 5710242; fractional-cointegration parity studies]. **Same exchange
  (COMEX), same session.**
- **Sourcing difficulty/cost.** **LOW.** GC/SI in GLBX.MDP3; GC has 18 yr on FirstRateData
  [Databento; FirstRateData].
- **Expected value.** **High.** A *cross-asset relative-value* habitat distinct from calendar/crack/
  crush (different reversion etiology: substitution/portfolio, not carry/margin) → widens the panel's
  regime coverage. Positive-priced legs → return/log-VR math works directly (no negative-spread
  handling needed), making it the cleanest input for the return-space VR characterisation Arm A runs.
- **Causal-reconstructibility risk.** **LOW.** Two clean liquid legs; causal rolling/Kalman β is
  standard. Caveat to pre-register: the GC–SI hedge ratio drifts (regime-dependent) → β must be
  **causal time-varying**, never full-sample (this is itself a good Kalman-vs-static β test).

### T1-E — Natural-gas **calendar** spread (NG M1–M2, and a seasonal e.g. Mar–Apr "widow-maker")
- **Exact instruments + legs.** NYMEX `NG` Henry Hub contract months (e.g. `NGH26`/`NGJ26` =
  Mar/Apr — the canonical seasonal storage spread). **Legs = two raw NG contract months.**
- **Why.** Seasonal storage economics give NG calendars a *structural* (weather/injection-withdrawal)
  reversion anchor distinct from CL's smooth carry — a second, differently-shaped carry reverter.
  Same-contract, same-session legs → clean. Deep NG history (18 yr) [FirstRateData].
- **Sourcing difficulty/cost.** **LOW.** Same path as T1-A (GLBX/FirstRateData/Barchart).
- **Expected value.** **Med–High.** Diversifies the *shape* of carry reversion (seasonal vs smooth)
  and adds a higher-vol reverter to stress the substrate engine's vol-context descriptor. Ranked 5th
  only because its seasonality adds a confound (annual cycle ≠ pure OU) that Arm A must model.
- **Causal-reconstructibility risk.** **LOW** mechanically (separate contracts); **MED** analytically
  (seasonal mean → the OU "μ\*" is itself seasonal; do not mistake seasonal drift for a trend or a
  broken reverter — pre-register the seasonal handling).

**Tier-1 rationale in one line.** Five same-family (CME-complex), deep-history, single-session,
leg-trivially-separable, *structurally*-anchored reverters spanning **four distinct reversion
etiologies** (carry · refining margin · processing margin · substitution) → unblock Arm A, the
Kalman cross-instrument panel, the off-ADANIENT OU-gate adjudication, and the MRScore distributional
fix, at the lowest contamination risk available, for ≈$0–$200.

---

## 4. TIER 2 — acquire SECOND (broaden habitats; slightly higher friction)

### T2-A — **WTI–Brent** location spread (CL · BZ, both CME-listed)
- **Legs.** NYMEX `CL` + CME/ICE `BZ` (Brent) contract months. Both available on CME GLBX (CME lists
  Brent `BZ`) → can keep one exchange/session.
- **Why / caveat.** Textbook cointegrated location/quality spread — **but** literature documents a
  **structural break ~2010** (post-shale WTI–Brent decoupling) [Wiley JFM 2021, Geyer-Klingeberg].
  → cointegration is *regime-dependent*; pre-register a post-2011 sample and treat pre-break data as a
  different regime. Med contamination risk from the break, not from sourcing.
- **Sourcing.** LOW–MED (GLBX/FirstRateData). **EV: Med–High** (adds a genuine cross-grade RV habitat;
  caveat keeps it out of Tier-1).

### T2-B — **Treasury-futures calendar / inter-tenor** (ZT · ZF · ZN · ZB contract months)
- **Legs.** CBOT `ZN` (10y), `ZF` (5y), `ZT` (2y), `ZB` (bond) contract months. Inter-tenor (e.g.
  NOB = ZN vs ZB) or **calendar** (front vs next ZN) → the tractable, *leg-sourceable* FI relative-
  value substrate (this is the **right** FI RV input, not FRED constant-maturity yields).
- **Why.** Curve RV with an economic anchor; all legs CBOT, same session, deep history. This is how
  to get FI RV **with real legs** while the true on/off-the-run reverter stays data-gated (Tier 3).
- **Sourcing.** LOW–MED (GLBX/FirstRateData). **EV: Med–High** (adds the FI asset class with clean
  legs; ranked T2 because curve-RV reversion is weaker/slower than commodity carry and DV01-weighting
  the legs adds modelling overhead).

### T2-C — **Heating-oil vs gasoline** & **gas-oil substitution** (HO · RB), **corn–wheat** (ZC · ZW)
- **Legs.** Same-exchange product pairs (NYMEX HO/RB; CBOT ZC/ZW). Substitution/relative-demand MR.
  Clean sessions, deep history. **EV: Med.** Cheap add-ons once the Tier-1 energy/ag legs are already
  in hand (RB, HO arrive with the crack; ZC arrives near the crush) → near-zero marginal sourcing.

### T2-D — **Cointegrated equity pair, leg-built** (candidate, not GLD/GDX)
- **Legs.** Two raw US equity/ETF price series (free: Stooq US / yfinance daily — these *do* return
  raw single-name legs, unlike their futures-continuous limitation). Build the spread causally.
- **Caveat (load-bearing).** **Do NOT use GLD/GDX** as the canonical pair — it **fails cointegration**
  (ADF ≈ −1.64, below even the 10% level; Johansen confirms none) and trends for long stretches
  [QuantStart; Chan]. Pick a pair with a *structural* link and a current cointegration test (e.g.
  dual-listed / share-class / sector near-substitutes), and **re-test cointegration on a causal
  rolling window** before trusting it (McLean–Pontiff edge-decay applies). **EV: Med** (equities are
  free and leg-clean, but idiosyncratic-risk break-downs make the MR anchor weaker than a commodity
  structural spread → not Tier-1).

---

## 5. TIER 3 — defer / data-gated (spec the unlock, do not acquire now)

### T3-A — **On-the-run / off-the-run Treasury** spread (the canonical FI RV reverter)
- **Why it's the textbook reverter.** Liquidity premium between newly-issued (on-the-run) and
  seasoned (off-the-run) issues; well-documented, economically anchored, mean-reverting
  [Krishnamurthy 2002; Pasquariello–Vega; Goldreich–Hanke–Nath 2005].
- **Why DEFER.** The legs are **CUSIP-level individual-bond prices**, not freely/cheaply available;
  reconstructing the spread needs matched on/off pairs + repo specialness — heavy data, not in the
  free/credits tier. **Highest-pedigree FI reverter but worst sourcing.** Unlock = a bond-level price
  source (e.g. CRSP/TRACE-derived) → then promote. Until then, T2-B (Treasury futures) is the FI
  stand-in.

### T3-B — **Etiology / order-flow data** (Arm D north-star; doc 12 §4 Arm D)
- **Spec the unlock only.** Signed order flow (OFI) **or** open-interest/COT positioning **or**
  options skew on a flow-driven leg already in Tier-1/2 (e.g. CFTC COT for CL/NG/ZS is *free* and
  weekly → a bounded, legal volume/positioning→reversal observational probe à la
  Campbell–Grossman–Wang). **Not an acquisition target now** (daily bars alias the ~1-day flow flip;
  v0 scope). Listed so the future unlock is pre-identified.

### T3-C — **Coffee–cocoa / soft-softs cross-spreads** (the on-disk contaminated set)
- The existing `coffee_cocoa_spread` is contaminated *and* short (673 bars) *and* cross-exchange
  (ICE softs, misaligned sessions, different currencies) with **no clean economic cointegration
  anchor** (coffee and cocoa are not substitutes/complements). **Do not re-acquire as a spread.** If
  ever wanted, source the raw KC/CC legs — but EV is low; deprioritised below everything above.

---

## 6. Master ranked table

| Tier | Instrument (spread) | Legs (raw, separately sourced) | Exchange / session | MR anchor (literature) | History | Sourcing (cost) | Causal-reconstruct. risk | EV |
|---|---|---|---|---|---|---|---|---|
| **1** | **WTI calendar** (M1–M2 … M1–M12) | `CL` month A, `CL` month B | NYMEX, single | Cost-of-carry / storage arbitrage | ~18 yr | Databento $125 credits / FirstRateData / Barchart Premier — **LOW** | **LOW** (same contract; β≈1) | **Very high** |
| **1** | **3-2-1 crack** | `CL`, `RB`, `HO` (3:2:1) | NYMEX, single | Refinery margin; leg cointegration ⇒ MR [crack-option lit; Haigh 2002] | ~18 yr | as above — **LOW** | **LOW–MED** (gal→bbl ×42) | **High** |
| **1** | **Soybean crush** | `ZS`, `ZM`, `ZL` (10:11:9) | CBOT, single | Processing margin; cointegration [JRSS-C 2020] | ~18 yr (ZS ’08+) | as above — **LOW** | **LOW–MED** (bu/ton/lb units) | **High** |
| **1** | **Gold–Silver** | `GC`, `SI` | COMEX, single | Fractional cointegration, substitution [SSRN 5710242] | ~18 yr (GC) | as above — **LOW** | **LOW** (causal β drifts) | **High** |
| **1** | **NatGas calendar** (Mar–Apr etc.) | `NG` month A, `NG` month B | NYMEX, single | Seasonal storage economics | ~18 yr | as above — **LOW** | **LOW** mech / **MED** (seasonal μ\*) | **Med–High** |
| **2** | **WTI–Brent** | `CL`, `BZ` | CME (GLBX) | Cointegration w/ **2010 break** [Wiley 2021] | deep | **LOW–MED** | **MED** (regime break) | **Med–High** |
| **2** | **Treasury futures curve** (NOB / calendar) | `ZT`,`ZF`,`ZN`,`ZB` | CBOT, single | Curve RV (FI RV w/ real legs) | deep | **LOW–MED** | **MED** (DV01 weighting) | **Med–High** |
| **2** | HO–RB · ZC–ZW (substitution) | `HO`,`RB` / `ZC`,`ZW` | NYMEX / CBOT | Substitution / relative demand | deep | **LOW** (arrive w/ Tier-1) | **LOW–MED** | **Med** |
| **2** | Equity pair (leg-built, **not GLD/GDX**) | 2 raw equity/ETF series | NYSE/Nasdaq | Cointegration (must re-test causally) | deep, free | Stooq/yfinance — **FREE** | **MED** (idio break-down) | **Med** |
| **3** | On-/off-the-run Treasury | matched CUSIP bond prices | OTC | Liquidity premium [Krishnamurthy 2002] | deep | **HIGH** (CUSIP-level, gated) | n/a (gated) | High *(future)* |
| **3** | Order-flow / COT (etiology) | OFI / OI / COT on a Tier-1 leg | — | Inventory→reversal [CGW; Nagel] | — | COT free; OFI paid | n/a (gated) | Highest *(future)* |
| **3** | Coffee–cocoa (on-disk, contaminated) | `KC`, `CC` (if ever) | ICE, **cross-session** | none (not substitutes) | short on disk | — | high (no anchor) | **Low — drop** |

---

## 7. Acquisition protocol (so the buy itself doesn't re-contaminate)

For **every** Tier-1/2 instrument, on acquisition (gated; execute only when authorized):
1. **Acquire legs, never the pre-made spread.** Pull each contract month as its own raw OHLCV(+OI/
   volume where present) series. Reject any vendor "spread" product.
2. **Prefer same-exchange/session legs** (all Tier-1 satisfy this) so the reconstructed spread bars
   are synchronous — the synthetic-spread rule (High/Low counterfactual) bites least when sessions
   align.
3. **Validate schema on the free sample first** (FirstRateData 2-wk sample / Databento small query)
   before spending credits/$ — check monotone dates, dtypes, no O=H=L=C degenerate runs, no all-NaN.
4. **Record contract specs + roll rule** from the CME product page into a per-instrument manifest
   (termination date, unit, tick, delivery) so the causal roll is documented, not inferred.
5. **Build the spread causally downstream** (Arm-A scope, not here): rolling/Kalman β on
   information ≤ `t`; explicit causal roll N days pre-expiry; **never** a full-sample β (that is the
   Arm-0 contamination we are escaping). High/Low of the synthetic spread flagged untrusted; use
   `close` (or level-difference) only; log/return-VR only where legs/levels are positive.
6. **Feed Arm 0's manifest, then Arm A.** Each new leg-built instrument enters the
   `cohort_manifest` with disposition **TRUSTED** only if ≥750 usable bars and causal β confirmed;
   otherwise PROVISIONAL/UNUSABLE per doc 12 §7 rules.

---

## 8. Single highest-EV acquisition & main risk (for the red-team)

- **Single highest-EV acquisition: the WTI crude calendar spread (CL M1–M2 / M1–M3), legs sourced
  as raw CL contract months.** It is the lowest-contamination real reverter obtainable (same
  contract, same exchange, same session → β≈1, clean synchronous bars), has ~18 yr of depth (far
  above the 750-bar floor), a *structural* carry anchor, and is essentially **free** via Databento
  sign-up credits. It alone can adjudicate the VR<0.75 OU-gate off ADANIENT and seed Arm A.
- **Main sourcing risk:** the cheap/free tier (Yahoo, Stooq, FRED) returns **continuous front-month
  or pre-interpolated** series — **not** the per-contract legs the programme needs — so naively
  "free" data silently re-imports Arm-0 contamination. The mitigation (and the only modest cost) is
  to source **per-contract legs** from Databento credits / FirstRateData / Barchart Premier and build
  every spread causally ourselves. Secondary risk: roll-rule / unit-conversion errors during
  reconstruction (gal→bbl, bu/ton/lb, seasonal μ\* in NG) — mitigated by recording CME specs in the
  manifest before any spread is built.

---

## 9. Sources

- Databento — pricing, $125 sign-up credits, GLBX.MDP3 (all CME/CBOT/NYMEX/COMEX contract months, parent symbology): https://databento.com/pricing · https://databento.com/datasets/GLBX.MDP3 · https://databento.com/futures/commodity
- FirstRateData — 18 yr individual + roll-adjusted continuous futures, 2-wk free samples (CL/NG/GC/ZC/ZS): https://firstratedata.com/i/futures/CL · https://firstratedata.com/i/futures/NG · https://firstratedata.com/i/futures/GC · https://firstratedata.com/i/futures/ZS
- Barchart — historical download; expired-contract symbology (`CLF26`), free tier = 2 yr, Premier = full history: https://help.barchart.com/support/solutions/articles/242748-how-can-i-download-historical-data- · https://www.barchart.com/my/price-history/download
- Stooq — free CSV (continuous front-month futures `cl.f`; raw equity legs), no API: https://stooq.com/db/h/ · https://stooq.com/q/d/?s=cl.f
- yfinance — no full futures chain / continuous front-month only (#2399): https://github.com/ranaroussi/yfinance/discussions/2399
- FRED — Treasury constant-maturity (pre-interpolated; DGS2/DGS10, T10Y2Y): https://fred.stlouisfed.org/series/DGS2 · https://fred.stlouisfed.org/series/T10Y2Y
- CME — official contract specs / roll (CL, NG, Corn, Brent, Soybean complex): https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.contractSpecs.html · https://www.cmegroup.com/markets/agriculture/grains/corn.contractSpecs.html · https://www.cmegroup.com/markets/agriculture/oilseeds/soybean.html
- Soybean crush ratio (10-11-9, GPM formula): https://www.sfu.ca/~poitras/CME_soybean-crush-reference-guide.pdf · CME Soybean Crush wiki: https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457090502/Soybean+Crush
- Crack spread cointegration ⇒ MR: https://www.sciencedirect.com/science/article/abs/pii/S0140988315001917 · Haigh–Holt (time-varying volatility spillovers, crack hedging) JAE 2002: https://onlinelibrary.wiley.com/doi/10.1002/jae.628
- Soybean crush cointegration (Bayesian case study): https://academic.oup.com/jrsssc/article/69/2/483/7058535
- Gold–silver cointegration / mean-reversion (COMEX 2015–2025): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5710242
- WTI–Brent cointegration & 2010 structural break: https://onlinelibrary.wiley.com/doi/full/10.1002/fut.22184 · HMM stat-arb in crude futures: https://arxiv.org/pdf/2309.00875
- GLD/GDX NOT cointegrated (do-not-use): https://www.quantstart.com/articles/an-introduction-to-stooq-pricing-data/ (and Chan, http://epchan.blogspot.com/2011/06/when-cointegration-of-pair-breaks-down.html)
- On-/off-the-run liquidity premium (FI RV reverter, data-gated): https://webuser.bus.umich.edu/ppasquar/onofftherun.pdf · https://faculty.haas.berkeley.edu/hender/on-off.pdf
