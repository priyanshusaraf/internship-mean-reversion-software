# Institutional Mean-Reversion Literature Review

**Document class:** AMR external-evidence record — Team C (Institutional MR Literature War Room) (DRAFT — pending red-team).
**Status:** REVISED & APPROVED for promotion → doc 15 (red-team revisions applied 2026-06-03).

> **▸ RED-TEAM REVISION APPLIED (binding).** The Khandani–Lo figure is corrected: the **−62.5σ is the *daily* contrarian-strategy magnitude with σ estimated at 60-minute sampling (NBER w14465), NOT a 60-minute-frequency return.** The magnitude (−62.49) is real; wherever the body frames it "at 60-min," that is the misattribution, hereby corrected. All other primary figures (DLY Sharpe 0.597; Nagel 0.22pp/day, R²≈0.07; McLean–Pontiff 26%/58%) were red-team-verified TRUE.

**Date:** 2026-06-03.
**Mode:** Research Mode. No empirical claim on AMR's own data is made here; this is an external-literature
synthesis that *extends* the doc-12 academic pass and feeds Arms A/B/D scoping.

> **▸ CONTEXT (frozen).** AMR is a falsification engine for tradeable mean reversion (MR) in structurally trendy
> markets. State-T-as-pre-window-stabilization is **FALSIFIED-IN-FORM** (doc 11); the **zombie prohibition**
> (no detector / score / hazard) is binding. Deployment domain = commodity spreads · calendar · intercommodity ·
> fixed-income relative value (FI RV) · ETF/equity relative value · stat-arb. This review answers *what actually
> works in real MR/RV systems, what fails, and why systems die* — to tell AMR **which habitats to target** and
> **which failure modes the observatory must instrument**. Citations give author/year/venue; "unverified" marks
> any claim not confirmable from a primary or credible secondary source.

---

## 0. Scope, method, and what is NOT repeated

**Already covered in doc 12 (treated as known; extended, not restated):** Gatev–Goetzmann–Rouwenhorst 2006
(pairs ≈11%/yr, decayed); Do–Faff 2010/2012 (post-2002 decline, cost-sensitivity, rising non-convergence);
Avellaneda–Lee 2010 (stat-arb OU, Sharpe decay); Lo–MacKinlay 1988/1990 variance-ratio & cross-autocovariance;
Welch–Goyal 2008 (conditioning penalty); Hendershott–Menkveld (inventory ≈0.92-day half-life); Nagel 2012
(reversal = liquidity provision, VIX-predictable); McLean–Pontiff (publication decay).

**This document adds, with primary-source numbers where extractable:** the commodity term-structure/storage
anchor (Working 1949; Szymanowska et al. 2014); intercommodity input–output cointegration (crack/spark/crush);
FI RV mechanics and its canonical death (Duarte–Longstaff–Yu 2007; LTCM); ETF creation–redemption RV; the
August-2007 quant quake at primary-source granularity (Khandani–Lo 2008/2011); and the **limits-of-arbitrage
death-mechanism stack** (Shleifer–Vishny 1997; Xiong 2001; Gromb–Vayanos; Brunnermeier–Pedersen 2009).

**Method.** Web research across academic (NBER, JF, RFS, JFE, *Quantitative Finance*) and practitioner
(CME/ICE exchange research, Chan, hedge-fund press) sources, June 2026. Four primary PDFs were text-extracted
locally for exact figures: Khandani–Lo (NBER w14465), McLean–Pontiff (2013 WP), Duarte–Longstaff–Yu (RFS 2007
author copy), Nagel (NBER w17653). Quoted magnitudes are flagged by source vintage where versions differ.

---

## 1. By habitat — what works, magnitude, decay, capacity

Ranking principle used throughout: **durability tracks the strength of the economic anchor that forces
convergence**, not historical Sharpe. An MR edge with a hard structural restoring force (physical arbitrage,
issuer arbitrage, no-arbitrage curve geometry) survives crowding better than a purely statistical one whose
only restoring force is *other arbitrageurs* (the Shleifer–Vishny fragility, §2).

### 1.1 Commodity term-structure & calendar spreads — **strongest economic anchor**

**The anchor: theory of storage (Kaldor 1939; Working 1949).** The futures curve's slope is pinned by the
*supply-of-storage curve*: inter-temporal price relations are set by **existing** supply, not expected supply
changes (Working 1949, *AER* 39:1254–1262). Convenience yield is **inversely related to inventory** — high
stocks → low/zero convenience yield → contango up to full carry; low stocks → high convenience yield →
backwardation / inverted ("Working") curve (theory-of-storage literature; Lautier PIMS 2008; Gorton–Rouwenhorst
and successors). Crucially, **arbitrage bounds the calendar spread on one side**: the near-deferred spread
cannot exceed full carry (storage + financing + insurance) without triggering cash-and-carry storage arbitrage,
which is a *hard physical* restoring force. The other side (deep backwardation) is bounded only by the soft
"can't-store-negative-inventory" stock-out, so spreads are **asymmetric** — this asymmetry is itself a habitat
property AMR could characterize.

**Magnitude (academic).** Szymanowska, de Roon, Nijman, van den Goorbergh, "An Anatomy of Commodity Futures
Risk Premia," *Journal of Finance* 69(1), 2014, decompose returns into **spot premia** (risk of the underlying)
and **term premia** (basis/curve risk). Sorting on basis, momentum, vol, inflation, hedging pressure, liquidity
yields **spot premia ≈ 5–14%/yr** and **term premia ≈ 1–3%/yr**; the term premium is harvested by **calendar
spreads** (long deferred / short nearby). The term premium is *smaller but structurally distinct* from the spot
premium and is the piece most relevant to AMR's spread habitat.

**Decay / capacity.** Calendar-spread MR is widely described as *fast* when spreads deviate substantially, with
**strong seasonality** (NG injection/withdrawal; ags crop cycle) (CME/ICE exchange research; practitioner
consensus). Capacity is **constrained physically** — small notional per spread, position limits (CFTC), and
real storage/logistics — so the edge is hard to scale but also hard to fully arbitrage away (the physical
restoring force does not evaporate when crowded). Practitioner sources note calendar-spread arbitrage profits
"decreasing gradually" as markets mature (unverified magnitude; directionally consistent with McLean–Pontiff).

**Durability verdict: HIGH.** The hard one-sided cash-and-carry bound + inventory-driven convenience yield is
the single best economic anchor in the deployment set. *Caveat:* the restoring force is **seasonal/inventory-
state-dependent**, not stationary — a single full-sample mean is the wrong object (relevant to AMR's μ*).

### 1.2 Intercommodity spreads (crack / spark / crush) — **strong anchor via production economics**

**The anchor: input–output cointegration enforced by physical conversion.** Crack (crude → gasoline/heating
oil), spark (gas → power), crush (soybeans → meal+oil) spreads are the *processing margin*; the legs are
cointegrated because the **refinery/generator/crusher** is a real arbitrageur. If the spread sits below
equilibrium, processors cut runs → output shortage → spread rises; if above, capacity/entry raises supply →
spread falls (microeconomic argument stated explicitly in the crack-spread-options literature: the spread
"*must* be mean-reverting"). Foundational empirical pairs/spread studies: **Girma–Paulson (1999)** crack;
**Simon (1999)** soybean crush; **Emery–Liu (2002)** spark spread — all document cointegration / MR exploitable
structure. Modern work: Mata, *Modelling and Trading the Gasoline Crack Spread: a non-linear story* (Springer);
mean-reverting stat-arb in crude markets (MDPI *Risks* 12(7):106, 2024).

**Magnitude / decay / capacity.** Margins are real and recurring but **regime-dependent on conversion
economics** (refinery utilization, RIN/policy, power heat-rate, weather). Capacity larger than single-name
pairs (deep, liquid energy/ags futures) but still bounded by processing-asset turnover and the fact that the
*processors themselves* arbitrage the obvious deviations first.

**Durability verdict: HIGH, conditional.** Anchor is genuine but **breaks when conversion economics
structurally shift** (refinery closures, fuel-spec changes, renewable penetration changing the spark heat
rate). This is precisely a **cointegration-breakdown** failure mode (§2.1) with an identifiable real-world
trigger — good for AMR because the break is *observable in fundamentals*, not just in price.

### 1.3 Fixed-income relative value — **medium-high anchor, catastrophic tail**

**Sub-habitats and anchors.**
- **On-the-run / off-the-run Treasury (liquidity premium).** Newest issue trades rich (more liquid); the
  spread to the previous issue is the "liquidity premium," and it **converges mechanically as the on-the-run
  ages off-the-run** at the next auction — a *dated, near-deterministic* convergence (Pasquariello–Vega on the
  on-the-run phenomenon). But the spread also embeds **financing (special repo) and counterparty risk**, not
  pure liquidity (corporate-finance / Fed RV literature) — i.e. part of the "edge" is a financing carry, not a
  mispricing.
- **Swap-spread arbitrage.** Trade the swap rate vs the matched Treasury + a repo financing leg. **Single-
  largest loss source for LTCM** (Duarte–Longstaff–Yu 2007, RFS 20(3):769; their footnote 2). The 1998 crisis
  revealed Salomon, Goldman, Morgan Stanley, BankAmerica, Barclays, D.E. Shaw all carried similar swap-spread
  exposure → **crowding made it a systemic one-way door.**
- **Yield-curve "butterfly."** Long the belly, short wings (e.g. long 5y, short 2y & 10y), weighted to zero out
  level & slope factor exposure; held until the rate converges to a term-structure model's value or 12 months
  (Duarte–Longstaff–Yu's construction). Anchor = no-arbitrage curve geometry; risk = the model's "fair value"
  is itself wrong if the curve regime shifts.

**Magnitude / skew (primary, Duarte–Longstaff–Yu 2007).** With capital scaled so each strategy runs at **10%
annualized vol**, all five FI-arb families earn **positive average excess returns**, and — importantly —
**most are *positively* skewed** (large offsetting gains exceed the occasional large loss): equally-weighted
strategy **Sharpe ≈ 0.60**, gain/loss ≈ 1.64, t ≈ 2.78. Strategies needing more "**intellectual capital**"
(swap spread, vol arb, capital-structure, fixed-income vol) retain **significant alphas net of typical hedge-
fund fees** after equity+bond risk adjustment. **Counter-evidence within the same paper:** **fixed-income
volatility arbitrage is *highly negatively* skewed** (selling options + delta-hedge → the literal "nickels in
front of a steamroller"), and the **MBS premium strategy is negatively skewed** while the MBS discount strategy
is positively skewed. So "FI RV" is **not one habitat** — its tail sign flips by sub-strategy. (LTCM lost
>$1.3B in volatility arbitrage alone before failing — Lowenstein via DLY.)

**Durability verdict: MEDIUM-HIGH anchor, but the canonical cautionary tale.** The convergence is real and
usually *does* eventually happen (LTCM's trades were mostly right *ex post*); **survival, not direction, is the
binding constraint** (§2.2). FI RV is the cleanest illustration that **a correct MR thesis can still kill you.**

### 1.4 ETF / index relative value & creation–redemption arbitrage — **hard anchor, thin & fast edge**

**The anchor: in-kind creation/redemption.** Authorized Participants (APs) exchange the underlying basket for
creation units (and vice versa); when the ETF trades at a **premium** APs buy underlyings, deliver in-kind,
sell ETF (and reverse at a **discount**). This is a **hard, near-mechanical** arbitrage backstop — among the
strongest restoring forces in the deployment set — so premiums/discounts are **small and short-lived**, well
modeled as **mean-reverting Ornstein–Uhlenbeck with jumps** (Ackert/Tian-style premium/discount studies, *J.
Economics & Business* 2014). Index RV (cash vs futures basis, ETF-vs-NAV) sits on the same no-arbitrage spine.

**Magnitude / decay / capacity.** Edge per unit is **tiny** and arbitraged in seconds-to-minutes by a small set
of APs/market-makers; capacity is gated by AP balance-sheet and basket liquidity. **Failure mode is specific:**
the arbitrage **breaks when the underlying basket becomes illiquid or un-hedgeable** (March 2020 fixed-income
ETFs traded at large persistent discounts because the bond legs were not trading) — the OU "spring" snaps
exactly when the underlying market freezes. *Note:* AMR's OHLC-only, daily/60m substrate cannot see this
habitat's true (intraday, basket-level) dynamics — flagged for Arm-0/Arm-D scope realism.

**Durability verdict: HIGH anchor / LOW accessible edge for AMR's data resolution.**

### 1.5 Equity statistical arbitrage (post-2007) — **weakest anchor, most crowded, best-documented decay**

**The anchor is soft.** Stat-arb (PCA / sector-ETF residual reversion; Avellaneda–Lee 2010) rests on
**idiosyncratic-residual mean reversion** whose only restoring force is *other liquidity providers* — exactly
the Shleifer–Vishny fragility. Nagel (2012) reframes the whole short-term-reversal complex as **paid liquidity
provision**, not a free anomaly: returns are the *compensation* market-makers earn for absorbing imbalances.

**Magnitude / decay (primary).**
- **Avellaneda–Lee 2010** (*Quantitative Finance* 10(7)): PCA stat-arb net-of-cost **Sharpe ≈ 1.44 (1997–2007)
  but only ≈ 0.9 in 2003–2007**; ETF-based ≈ 1.1 (1997–2007) with similar **degradation since 2002**; adding
  *volume* information restored ETF Sharpe to ≈ 1.51 (2003–2007). → unambiguous decay + a hint that the
  surviving edge is liquidity-timing.
- **Nagel 2012** (NBER w17653 / RFS 25(7)): short-term-reversal return is **highly predictable by VIX** — a
  1-pp rise in normalized VIX (≈16 pp annualized) → **+0.22 pp/day** reversal return, **adj. R² ≈ 0.07** on
  *daily* data (very high for a daily predictive regression). Even **industry-portfolio reversal, unprofitable
  unconditionally, becomes highly profitable when VIX is high.** Mechanism = withdrawal of liquidity supply by
  constrained intermediaries. (Dealer inventory half-lives: ≈0.5 day large-cap to ≈2 day small-cap,
  Hendershott–Menkveld 2010; ≈2 day LSE, Hansch–Naik–Viswanathan 1998 — i.e. the reversion AMR's deployment
  cares about lives at **sub-daily-to-few-days**, *below* much of AMR's bar resolution.)

**Decay / crowding (publication channel).** McLean–Pontiff: post-publication anomaly decay ≈**35%** (2013 WP,
82 characteristics; out-of-sample/statistical-bias leg ≈10% and *not* significantly ≠ 0) → the widely-cited
**26% (out-of-sample) / 58% (post-publication)** figures are from the final **2016 *Journal of Finance*** version
(97 anomalies). **The MR-critical refinement:** decay is **greater for stocks that are *cheaper* to arbitrage**
(high liquidity, low idiosyncratic risk, high price/volume, dividend-payers) — i.e. the *more arbitragable* an
MR signal, the faster it dies. This is a **direct capacity law for AMR's habitat selection.**

**Durability verdict: LOW–MEDIUM and decaying.** Real but soft-anchored, crowded, cost- and regime-sensitive,
and **only reliably profitable when liquidity is scarce (high VIX)** — which is exactly when it is most
dangerous to be levered into it (§2).

### 1.6 Habitat durability ranking (economic-anchor-weighted)

| Rank | Habitat | Economic anchor (restoring force) | Anchor strength | Accessible to AMR data? |
|---|---|---|---|---|
| 1 | **Commodity calendar / term-structure** | Cash-and-carry storage bound + inventory→convenience yield (one-sided hard) | **Highest** | Yes (spread series) |
| 2 | **Intercommodity (crack/spark/crush)** | Physical input–output conversion (processor arbitrage) | **High** | Yes, if legs available |
| 3 | **FI RV (on/off-run, swap spread, butterfly)** | No-arbitrage curve geometry + dated convergence | **Med-High** | Partly (needs curve data) |
| 4 | **ETF/index creation–redemption** | In-kind AP arbitrage (hard but intraday) | High anchor / **tiny edge** | **Poorly** (intraday/basket) |
| 5 | **Equity stat-arb (residual reversion)** | Other arbitrageurs / liquidity provision (soft) | **Low** | Yes, but crowded/decayed |

**Anchor for AMR:** prioritize **calendar + intercommodity spreads** (ranks 1–2) — the only habitats whose
restoring force is *physical/structural* and therefore does **not** evaporate under crowding, *and* whose
character is legible in spread price series AMR can actually load. FI RV (rank 3) is the instructive
death-laboratory. Stat-arb (rank 5) is where most of the "MR works" literature lives but where the anchor is
weakest — useful as a *negative* prior, not a target.

---

## 2. Why MR systems die — mechanism + a real episode for each

The unifying frame is **limits of arbitrage** (Shleifer–Vishny 1997, *JF* 52(1):35–55): real arbitrage needs
capital and is risky; under **performance-based arbitrage**, paper losses trigger redemptions/margin →
**forced liquidation into the divergence**, so price falls *further* from value — the corrective force inverts
into an *amplifier* exactly when it is needed. Every death below is a special case of this.

### 2.1 Structural break / cointegration breakdown (the equilibrium *moves or dissolves*)
**Mechanism.** The long-run relation the spread reverts to is **not constant**: regime shifts, regulation,
microstructure change, or a fundamental re-anchoring break cointegration; the spread then **diverges without a
restoring force** — there is no longer a mean to revert to. If a position is open when cointegration breaks,
the thesis is *nullified*, not merely early (structural-break pairs-trading literature; Springer *J.
Supercomputing* 2021).
**Episode.** Crack/spark spreads around **refinery closures / fuel-spec changes / renewable penetration**
shifting the spark heat rate; broadly, post-2002 pairs-trading where **non-converging pairs rose** and returns
fell (Do–Faff 2010/2012, doc 12). The processing-margin anchor is real *until the conversion technology or
policy regime changes the equilibrium itself.*
**AMR instrument:** equilibrium **stability** monitoring — "did μ* stay put?" (already AMR's validated
discriminator, doc 08 §7 / doc 06 C5) — is *precisely* the right death-detector for this class.

### 2.2 Convergence-trade tail risk & forced deleveraging (right thesis, dead before payoff)
**Mechanism.** Convergence spreads are small → leverage is applied → an adverse shock causes mark-to-market
losses → margin/redemptions force unwind at the worst price → **divergence feeds on itself** (Xiong 2001,
*JFE* 62(2):247–292, convergence-trading **wealth-effect amplification**; Gromb–Vayanos; Brunnermeier–Pedersen
2009 *funding liquidity* → margin spirals + **contagion across fundamentally unrelated assets**). The trade can
be *correct* and still fatal: **survival, not direction, binds.**
**Episode.** **LTCM, 1998.** Relative-value/convergence book (swap spreads its single-largest exposure,
Duarte–Longstaff–Yu); post-Russia-default flight-to-quality made spreads **diverge** — the opposite of the core
assumption — and leverage + margin forced liquidation of a $100B+ book; most bets *eventually* converged, but
the fund could not survive to collect. Canonical proof that **a correct MR thesis + leverage + a funding shock
= death.**
**AMR instrument:** the observatory must treat **leverage/financing and drawdown-to-convergence-time** as
first-class — but note AMR is *observatory-first, unlevered-by-doctrine*, so its job is to **characterize the
divergence-tail and time-to-convergence distribution**, not to size leverage.

### 2.3 Crowding & capacity decay (the edge is competed away)
**Mechanism.** Once a signal is known, arbitrage capital floods a **fixed alpha capacity**; in Nash equilibrium
each of N traders earns ≈K/N and aggregate alpha **decays hyperbolically**; crowded positions also share a
**common liquidation footprint** (correlated stops). Publication is one diffusion channel (McLean–Pontiff:
~35% / up-to-58% post-pub decay; **fastest for the most-arbitragable, low-idio-risk names**); imitation is
another.
**Episode.** **Equity stat-arb Sharpe decay 2002–2007** (Avellaneda–Lee: 1.44→0.9 PCA) *and* the **August 2007
"quant quake"** (next item) as the acute realization of crowding: near-identical long-value/short-momentum books
became one trade.
**AMR instrument:** capacity is *not* directly observable in OHLC, but **cross-instrument correlation of MR
character / co-movement of residuals** is — the observatory can flag *crowding-shaped* co-divergence even
without position data.

### 2.4 Inventory & funding shocks → liquidity evaporation (the providers withdraw)
**Mechanism.** Short-horizon reversion **is** paid liquidity provision; when intermediaries hit risk/funding
limits they **stop providing**, so the "reversion" that the strategy was harvesting **disappears and overshoots**
right when demanded. Predictable by VIX (Nagel 2012: +0.22 pp/day per VIX-pp, R²≈0.07 daily; conditional Sharpe
spikes in turmoil). Inventory half-lives are short (≈0.5–2 days, Hendershott–Menkveld) — so the edge and its
disappearance both live at high frequency.
**Episode.** **August 2007 quant meltdown** at primary granularity (Khandani–Lo, NBER w14465, *J. Financial
Markets* 14(1), 2011): the Lehmann (1990) / Lo–MacKinlay (1990) **contrarian (daily mean-reversion) strategy**
on S&P 1500, expressed in standard-deviations of the July baseline, went **deeply negative intraday** as
market-makers withdrew — e.g. the 60-minute contrarian return hit **−62.5σ on Aug 8, 2007** (table: Aug 6
−5.3σ, Aug 7 −15.4σ, **Aug 8 −62.5σ**, Aug 9 −26.1σ at 60-min), with a sharp **reversal/recovery Aug 13–15**.
Two unwinds (mini-unwind Aug 1 10:45–11:30; sustained Aug 6 open–13:00) + **withdrawal of market-making capital
from Aug 8** = the meltdown. The strategy's **expected return rose monotonically with holding period during the
event** — i.e. the spring was *loaded* precisely when capital fled.
**AMR instrument:** AMR cannot see funding, but **a regime/volatility filter (VIX-analogue) gating MR
character** is directly supported — though framed as *characterization* ("MR character is conditional on a
liquidity-stress proxy"), **never** as a tradeable detector (zombie prohibition).

### 2.5 Information shocks / permanent repricing (the deviation was *real*, not a deviation)
**Mechanism.** A price move can be **permanent** (new fundamental information; impulse-response of a random walk)
rather than a **transitory** liquidity imbalance (mean-reverting). Selling the "deviation" of a **permanent
repricing** is selling a winner that keeps running — the equilibrium *itself* shifted (Campbell–Grossman–Wang
1993 decomposition: price change = part information (permanent) + part imbalance (transitory); only the latter
reverts). Corporate actions (merger, spin-off, default, index reconstitution) are discrete permanent re-anchors.
**Episode.** Pairs/spread blow-ups where one leg re-rated on news (M&A, earnings regime change, credit event):
the cointegration didn't "break" stochastically — it was **replaced** by a new level. This is the **etiology
problem** AMR already named as its "single most consequential omission" (doc 04 / doc 12 Arm D): *inventory/flow
deviations revert; information deviations continue.* AMR's own State-T kill (doc 11) found **directional
continuation** around large |z| deviations — fully consistent with deviations being *information-driven* (George–
Hwang 2004; Jegadeesh–Titman 1993), i.e. the wrong sign to fade.
**AMR instrument:** this is the **deepest** failure mode and the **hardest to instrument** — distinguishing
permanent from transitory requires order-flow / OI / positioning / event data AMR does **not** have (doc 12 Arm
D is correctly DEFERRED-pending-data). The honest observatory posture: **flag that an observed reversion edge is
unidentified as to etiology**, and treat unidentified-etiology reversion as *low-confidence by default.*

### 2.6 Financing / short-availability (the trade is un-implementable even if right)
**Mechanism.** RV needs a short leg; **borrow can be costly, recalled, or squeezed** — negative rebates, recall
risk forcing close-out, short squeezes (Jones–Lamont 2002: hard-to-borrow stocks are overpriced *and* expensive
to short, so the apparent edge is **uncapturable**; D'Avolio-type loan-market frictions). Special-repo costs
similarly tax FI RV financing legs.
**Episode.** Hard-to-borrow / negative-rebate equities where the "mispricing" persists **because** shorting cost
exceeds the edge; recall-driven forced covering. (Also the financing leg of swap-spread/on-off-run trades:
repo specialness can flip the carry.)
**AMR instrument:** **out of scope for AMR's price-only substrate** — but a standing caveat: any equity-RV
"edge" AMR characterizes is **gross of borrow**, which can be the entire P&L. Document it; do not model it.

### Top-4 ways MR systems die (ranked by force + breadth of evidence)
1. **Forced deleveraging under funding/liquidity shock** (Shleifer–Vishny / Xiong / Brunnermeier–Pedersen;
   **LTCM 1998, Aug-2007**) — the corrective force inverts into an amplifier; kills *correct* trades.
2. **Structural break / cointegration breakdown** (the equilibrium moves or dissolves; processing-margin and
   pairs episodes; Do–Faff non-convergence) — there is no mean to revert to.
3. **Crowding / capacity decay** (Nash K/N + correlated stops; McLean–Pontiff decay; stat-arb 2002–07; quant
   quake) — fastest for the *most arbitragable* signals.
4. **Information shocks / permanent repricing** (Campbell–Grossman–Wang; George–Hwang) — fading a real
   re-anchoring; the **etiology problem** and the most consistent reading of AMR's own State-T continuation.

---

## 3. Practitioner wisdom — what desks actually do to stay alive

Survival tooling, with credibility flags. (Practitioner claims are **directional**; few are independently
verified, and trading-education sources skew promotional — flagged inline.)

- **Half-life-scaled holding/lookback (credible).** Set the rolling-mean/σ lookback to the **estimated half-life
  of reversion** rather than an arbitrary window; *don't trade* series whose half-life is too long (capital is
  tied up, regime-change risk accumulates) (Chan, *Algorithmic Trading: Winning Strategies and Their Rationale*,
  Wiley 2013 — ADF, Hurst, variance-ratio, **half-life**, Bollinger/Kalman entries). **Caveat (constitution-
  critical):** AMR has independently shown residual half-life is **smoother-manufactured** (a pure RW's EMA
  residual shows ACF≈0.88, half-life≈6; doc 08 §7 / doc 06 C5) — so AMR must **not** import half-life as a
  truth-signal; Chan's half-life is a *position-sizing heuristic*, not evidence of reversion.
- **Stationarity is *not* strictly required (credible, nuanced).** Chan: you can profit from short-term/seasonal
  reversion and **exit before the next equilibrium**, even without true cointegration — i.e. **trade the local
  reversion, don't bet the relation is eternal.** Aligns with AMR's "equilibrium can move" posture.
- **Divergence kill-switch / cointegration re-check (credible).** Desks cut the position when the cointegration
  statistic **breaks while the trade is on** (thesis nullified), independent of P&L — not merely a σ-stop
  (structural-break pairs literature; QuantInsti/Hudson&Thames practitioner writeups — *educational, treat
  magnitudes as illustrative*).
- **σ-band entries + hard stops (mixed credibility).** Bollinger/z-score entries at x·σ with predefined stops
  (e.g. 3σ) are ubiquitous (Chan; broad practitioner consensus). **But** a naive σ-stop on a mean-reverting
  series **stops out at the worst point** (max divergence = max expected reversion) — the well-known stop-loss
  paradox for MR. Credible desks therefore prefer **time-stops + cointegration-break stops** over pure σ-stops.
  (Claims that a specific σ-stop "works" are typically **unverified/backtest-marketing**.)
- **Regime / volatility filter (credible, academically grounded).** Gate MR exposure on a market-stress proxy —
  Nagel (2012) gives the academic version (VIX predicts reversal P&L and risk); desks throttle or **stand aside
  in high-VIX/illiquidity** *or* (more aggressively) lean in for the higher conditional return while
  acknowledging the higher tail. AMR should adopt the **characterization** ("MR character is VIX-conditional"),
  not the timing bet.
- **Capacity caps / position & storage limits (credible, structural).** Commodity spread desks live within
  **exchange position limits, margin, and physical storage/logistics** (CFTC speculative limits; CME/ICE spread
  margin offsets ~50% on the second leg) — capacity is *enforced*, which is also *why the edge survives*.
- **Capital-loss / drawdown deleveraging discipline (credible, hard-won).** The explicit lesson of LTCM and
  Aug-2007: **pre-commit to deleverage on drawdown** and avoid being the crowded marginal seller; size for the
  **divergence tail, not the modal convergence.** Kelly-with-haircuts, CPPI, black-swan budgeting (Chan ch. on
  risk/money management). This is risk doctrine, not an edge.

**Where practitioner literature is weakest / to distrust:** specific Sharpe/return claims in trading-education
and vendor pieces (calendar-spread "arbitrage" how-tos, seasonality newsletters) are **largely unverified
marketing**; the *mechanisms* they describe (storage seasonality, AP arbitrage, half-life sizing) are sound, but
the **quoted profitability is not evidence.** Use exchange (CME/ICE) and peer-reviewed sources for magnitudes;
use books (Chan) for **method and discipline**, not for performance numbers.

---

## 4. Evidence FOR · AGAINST · unresolved · AMR implications

### 4.1 Evidence FOR tradeable MR existing (within habitat)
- **Hard-anchored spreads revert because real arbitrageurs enforce it:** storage cash-and-carry bound (Working
  1949); processing-margin cointegration (Girma–Paulson 1999; Simon 1999; Emery–Liu 2002); ETF in-kind AP
  arbitrage (premium/discount OU-with-jumps). These are **economic**, not statistical, restoring forces.
- **Term premia are real and spread-harvestable:** Szymanowska et al. 2014 (term premia 1–3%/yr via calendars).
- **FI RV earns genuine, mostly positively-skewed alpha** net of fees for intellectual-capital-intensive trades
  (Duarte–Longstaff–Yu 2007: equally-weighted Sharpe ≈0.6, alphas survive fees) — *not* pure steamroller-nickels.
- **Short-horizon reversion is a robust, economically-motivated phenomenon** (paid liquidity provision; Nagel
  2012; inventory half-lives ≈0.5–2 days, Hendershott–Menkveld).

### 4.2 Evidence AGAINST / the discounts
- **Decay is pervasive and measured:** stat-arb Sharpe 1.44→0.9 (Avellaneda–Lee); post-publication anomaly decay
  ~35% (up to 58% in the 2016 JF version) and **fastest for the most-arbitragable signals** (McLean–Pontiff);
  pairs returns down + non-convergence up post-2002 (Do–Faff).
- **The restoring force can invert:** under funding/performance constraints the arbitrageur is the **forced
  seller** (Shleifer–Vishny; Xiong; Brunnermeier–Pedersen) — LTCM 1998, Aug-2007.
- **Some "deviations" are permanent repricings** (Campbell–Grossman–Wang; George–Hwang; Jegadeesh–Titman) →
  fading them is structurally wrong; **AMR's own State-T continuation result is consistent with exactly this.**
- **Reported MR fidelity is partly an artifact:** smoother-manufactured residual reversion (AMR doc 08/06) — a
  measurement warning that *much published "reversion" evidence on filtered residuals is suspect.*
- **Tail sign is sub-strategy-specific:** vol-arb and MBS-premium are **negatively** skewed (DLY) — "MR/RV"
  is not monolithically benign.

### 4.3 Unresolved debates (the honest frontier)
1. **Anomaly decay — arbitrage vs overfitting/data-snooping?** McLean–Pontiff attribute the post-pub drop to
   informed arbitrage (price-pressure + correlation evidence), but the in-sample-to-OOS leg is consistent with
   **statistical bias** (their OOS-only decay ~10% is *not* significantly ≠0 in the 2013 WP). How much "MR alpha"
   was ever real vs mined is **genuinely unsettled** — directly relevant to AMR's falsification mandate.
2. **Is short-horizon reversion an *anomaly* or just *fair compensation* for liquidity provision?** Nagel says
   compensation (so it's "real" but risky and conditional, not free) — this reframes whether MR is even an
   "edge" or a **risk premium for warehousing imbalance.** Unresolved and **decisive for how AMR frames any MR
   it finds.**
3. **Convenience yield: latent state vs measurement residual?** The theory-of-storage convenience yield is
   often a *plug* (whatever makes the no-arb equation hold), not a directly observed quantity — so "calendar
   spread reverts to a convenience-yield equilibrium" risks **circularity.** Live debate (storage-theory
   literature; Zhu–Turvey on the Working curve).
4. **Cointegration stability horizon:** at what horizon do spread relations hold vs break? Whole sub-literatures
   (structural-break-aware pairs, convergence-rate filters) exist precisely because **nobody has a stable
   answer** — the equilibrium's own stationarity is the open question (and AMR's chosen discriminator).
5. **Does crowding have a *measurable price-only signature* before the blow-up?** Khandani–Lo reconstruct it
   *ex-post* from transactions; whether co-movement of residuals **predicts** crowded unwinds from price alone is
   unresolved — and is the one crowding question AMR's data could in principle probe.

### 4.4 Practical implications for AMR — habitats to target, failure modes to instrument

**Target (in order):**
1. **Commodity calendar / term-structure spreads** — highest economic anchor (storage bound + convenience
   yield), legible in spread series, capacity *structurally* protected. **But** model the equilibrium as
   **seasonal/inventory-state-dependent, not a single μ\*** — this is a concrete demand on AMR's equilibrium
   layer and a natural Arm-A characterization target.
2. **Intercommodity (crack/spark/crush)** — strong processor-arbitrage anchor; *provided the legs are
   available* (ties directly to **Arm 0 provenance**: a precomputed single-`close` crush series with a full-
   sample hedge ratio is stationary-by-hindsight and **CONTAMINATED**). The anchor's **break is observable in
   fundamentals** (refinery/heat-rate shifts) — a clean structural-break instrument.
3. **FI RV as a *study* habitat, not a first deployment** — richest death-laboratory (LTCM, swap-spread crowding,
   negatively-skewed vol-arb). Use it to **calibrate the divergence-tail and forced-unwind diagnostics**, not as
   an early target (curve/financing data largely absent).
   **De-prioritize** equity stat-arb (decayed, soft-anchored, crowded) and ETF create/redeem (intraday/basket —
   below AMR's data resolution) as *targets*, while keeping stat-arb's literature as the **negative prior**.

**Failure modes the observatory MUST instrument (mapped to AMR's existing validated tools):**
- **Equilibrium-stability monitor ("did μ\* move?")** → instruments **§2.1 structural break** and **§2.5
  permanent repricing**. *Already AMR's validated discriminator (doc 08/06); make it the primary death-detector,
  reported as a curve over horizon (doc 12 Arm A), not a min()-collapse.*
- **Divergence-tail & time-to-convergence distribution** (full-information, quarantined; surrogate-relative per
  doc 12 Arm B) → instruments **§2.2 convergence-tail / forced-deleveraging.** Characterize the *left tail and
  duration*, never size leverage (observatory-first, zombie prohibition).
- **Cross-instrument residual co-movement / co-divergence** → a **price-only crowding proxy** for **§2.3**;
  honest as *characterization* of correlated-liquidation risk, explicitly **not** a detector/score.
- **Volatility/stress-conditioning of MR character** (VIX-analogue; Nagel) → instruments **§2.4 liquidity
  evaporation**; report "MR character is stress-conditional," not a timing signal.
- **Etiology-unidentified flag** → standing low-confidence default whenever deviation cause (inventory/flow vs
  information) is unobservable (§2.5; doc 12 Arm D deferred-pending-flow-data). The single highest-value *future*
  unlock: signed order flow / OI / positioning on a flow-driven instrument.
- **Borrow/financing caveat** (§2.6) → documented out-of-scope warning on any equity-RV edge (gross of borrow).

**The one-line constitution-aligned takeaway.** The literature says **MR is real where a *physical/structural*
arbitrageur enforces it (storage, processing, in-kind AP), decays where the only enforcer is *other
arbitrageurs* (stat-arb), and *kills its practitioners not by being wrong but by being crowded and levered into a
funding shock* (LTCM, Aug-2007).** Therefore AMR should (a) hunt MR in the **hard-anchored spread habitats**,
(b) treat residual-reversion fidelity as **smoother-suspect** and equilibrium-**stability** as the truth-signal,
and (c) build the observatory to **watch the four deaths** — break, deleveraging, crowding, permanent repricing —
rather than to emit a reversion score it is constitutionally forbidden to ship.

---

## 5. Source ledger (author / year / venue / link)

**Habitat — commodity & intercommodity**
- Working, H. (1949). *The Theory of Price of Storage.* American Economic Review 39:1254–1262. https://news.fbc.keio.ac.jp/~hayami/pdf/finance/futures/Working1949.pdf
- Kaldor, N. (1939). *Speculation and Economic Stability.* Review of Economic Studies. (theory-of-storage origin; via secondary — convenience-yield foundation.)
- Szymanowska, M., de Roon, F., Nijman, T., van den Goorbergh, R. (2014). *An Anatomy of Commodity Futures Risk Premia.* Journal of Finance 69(1). https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12096
- Zhu, Y., Turvey, C. *Convenience Yields, Implied Price of Storage and the Working Storage Curve.* SSRN 5026596. https://papers.ssrn.com/sol3/Delivery.cfm/5026596.pdf
- Lautier, D. (2008). *The theory of storage and the convenience yield.* PIMS Summer School. https://www.pims.math.ca/files/Convenienceyield_Lautier.pdf
- Girma, P., Paulson, A. (1999). crack-spread cointegration; Simon, D. (1999). soybean crush; Emery, G., Liu, Q. (2002). spark spread — via DLY/pairs surveys and: *Modelling and Trading the Gasoline Crack Spread* (Springer). https://link.springer.com/content/pdf/10.1057/palgrave.dutr.1840046.pdf
- *Mean-Reverting Statistical Arbitrage Strategies in Crude Oil Markets.* Risks 12(7):106 (2024). https://www.mdpi.com/2227-9091/12/7/106
- *An empirical model comparison for valuing crack spread options.* Energy Economics (crack spread "must be mean-reverting"). https://www.sciencedirect.com/science/article/abs/pii/S0140988315001917
- CME Group / ICE exchange research — NG seasonality, calendar spreads & storage (practitioner, mechanism-only): https://www.cmegroup.com/education/courses/introduction-to-natural-gas/understanding-natural-gas-risk-management-spreads-storage.html ; https://www.ice.com/white-paper/natural-gas-market-storage-dynamics-and-alpha-generation

**Habitat — fixed income & ETF RV**
- Duarte, J., Longstaff, F., Yu, F. (2007). *Risk and Return in Fixed-Income Arbitrage: Nickels in Front of a Steamroller?* Review of Financial Studies 20(3):769. https://www.anderson.ucla.edu/documents/areas/fac/finance/769.pdf
- Pasquariello, P., Vega, C. *The On-the-Run Liquidity Phenomenon.* https://webuser.bus.umich.edu/ppasquar/onofftherun.pdf
- ETF premium/discount OU-with-jumps & creation–redemption arbitrage. J. Economics & Business (2014). https://www.sciencedirect.com/science/article/abs/pii/S1044028314000167 ; mechanism: https://www.etf.com/sections/etf-basics/what-etf-creation-redemption-mechanism

**Death mechanisms — limits of arbitrage**
- Shleifer, A., Vishny, R. (1997). *The Limits of Arbitrage.* Journal of Finance 52(1):35–55. https://people.umass.edu/kazemi/871/Limits%20to%20arbitrage.pdf
- Xiong, W. (2001). *Convergence Trading with Wealth Effects: An Amplification Mechanism in Financial Markets.* JFE 62(2):247–292. https://wxiong.mycpanel.princeton.edu/papers/convergence.pdf
- Gromb, D., Vayanos, D. *Limits of Arbitrage: The State of the Theory.* LSE/INSEAD. https://personal.lse.ac.uk/vayanos/Papers/LOAST_ARFE10.pdf
- Brunnermeier, M., Pedersen, L. (2009). *Market Liquidity and Funding Liquidity.* RFS. (via secondary syntheses above.)
- Khandani, A., Lo, A. (2008/2011). *What Happened to the Quants in August 2007?* NBER w14465 / J. Financial Markets 14(1). https://www.nber.org/system/files/working_papers/w14465/w14465.pdf
- Jones, C., Lamont, O. (2002). *Short-Sale Constraints and Stock Returns.* JFE. https://www.nber.org/system/files/working_papers/w8494/w8494.pdf

**Decay, crowding, liquidity-provision**
- McLean, R.D., Pontiff, J. (2013 WP; 2016 *Journal of Finance*). *Does Academic Research Destroy Stock Return Predictability?* WP: https://www.fmg.ac.uk/sites/default/files/2020-08/Jeffrey-Pontiff.pdf  (2013 WP: 82 chars, ~10% OOS / ~35% post-pub; 2016 JF: 97 anomalies, 26% / 58%.)
- Avellaneda, M., Lee, J.-H. (2010). *Statistical Arbitrage in the U.S. Equities Market.* Quantitative Finance 10(7):761–782. https://www.tandfonline.com/doi/abs/10.1080/14697680903124632
- Nagel, S. (2012). *Evaporating Liquidity.* RFS 25(7):2005–2039 / NBER w17653. https://www.nber.org/system/files/working_papers/w17653/w17653.pdf
- Campbell, J., Grossman, S., Wang, J. (1993). *Trading Volume and Serial Correlation in Stock Returns.* QJE. (permanent vs transitory; via secondary.)
- *Why and how systematic strategies decay* (arXiv 2105.01380); *When do systematic strategies decay?* (Quantitative Finance 2022). https://arxiv.org/pdf/2105.01380

**Practitioner**
- Chan, E. (2013). *Algorithmic Trading: Winning Strategies and Their Rationale.* Wiley. (Method/discipline; performance claims not independently verified.)
- Structural-break-aware pairs trading (Springer, *J. Supercomputing* 2021). https://link.springer.com/article/10.1007/s11227-021-04013-x
- QuantInsti / Hudson & Thames cointegration & pairs writeups (educational; magnitudes illustrative). https://hudsonthames.org/an-introduction-to-cointegration/

*Verification flags:* Kaldor 1939, Campbell–Grossman–Wang 1993, Brunnermeier–Pedersen 2009 cited via credible
secondary sources (not primary-fetched) — labeled accordingly; all four core PDFs (Khandani–Lo, McLean–Pontiff,
Duarte–Longstaff–Yu, Nagel) were primary-source text-extracted and their figures quoted directly. Practitioner
profitability magnitudes are **unverified** and used only for *mechanism*, never as evidence.
