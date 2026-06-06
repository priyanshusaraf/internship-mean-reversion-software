# Arm A v2 — Cycle 1b: Rolling-Local Trader-Persistence of the NG Calendar MR — Results & Verdict

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **COMPLETE.** Executes doc 22 (frozen) exactly. Trader-first deployability read, four-lens
adjudicated (pre-freeze design review + post-execution adversarial+trader verification).
**Date:** 2026-06-04. **Provenance:** engine `analytics_arm_a_v2.py`; runner `scripts/run_arm_a_v2_rolling.py`;
results `data/processed/arm_a_v2_rolling_results.json`. Confidence = trustworthiness-of-evidence.

> **Verdict:** **PERSISTENT-BUT-UNECONOMIC (naive book); back-adjustment NOT cleanly excluded.** NG calendar
> storage MR is a **statistically robust, regime-spanning, recency-surviving** property (pooled mean-z = −0.627,
> t=−4.37, **p≈0.0002**), **structured in a genuinely MR-favoring way** (it switches off in storage-glut years,
> not shocks). But it is **"merely true," not a deployable simple book**: a naive causal z-entry strategy is
> break-even *before* costs and net-negative after. **Confidence MEDIUM.** §11.8: this **neither strengthens nor
> downgrades** the doc-21 edge claim; it modestly **strengthens the apparatus** (the clean-construction Brent
> calendar is a genuine positive control).

---

## 1. The question & instrument (doc 22)
*Is NG calendar storage MR persistent enough across regimes to matter to a 1–12-week trader, or a regime-averaged
read?* The per-window **binary** flag was falsified pre-freeze (synthetic: underpowered on real MR, fires *higher*
on bounce, blind to back-adjustment), so the frozen instrument is the **pooled mean-z** (per-window standardized
VR(20) distance below its own RW surrogate band) + a **construction-controlled corroborator** (self-built Brent
calendar) + **splice-RW diagnostic** + **half-life/amplitude/causal-trade-proxy** for deployability.

## 2. Results
| Read | mean-z | n | note |
|---|--:|--:|---|
| **NG yearly (A, PRIMARY)** | **−0.627** | 19 | t=−4.37, **p≈0.0002** vs RW center; below RW band (−0.32); 14/19 below RW-median (Binom one-sided p=0.032) |
| NG 2-yr blocks (B, granularity) | −1.239 | 10 | 9/10 — same data, not independent |
| NG pre-2020 | −0.714 | 13 | |
| **NG post-2020 (Q6)** | **−0.438** | 6 | below −0.32 → **recency holds**, attenuated |
| Brent calendar (self-built, no vendor back-adj) | −3.54 | 8 | hourly/off-scale — apparatus positive control, NOT level evidence for NG |
| splice-RW frac0.25 / frac0.5 (back-adj reference) | −0.657 / −1.053 | — | **NG (−0.627) ≈ frac0.25 anchor** |
| genuine moderate-MR anchor (OU φ=0.95) / RW null | −0.33 / +0.02 | — | RW band [−0.32,+0.41] |

- **Global half-life 12.9 bars** (~2.6 wks; in the frozen tradeable band 3–40). 
- **Trade proxy (frozen causal z-entry, cost 0.003):** 200 trades, **avg net −0.0026**, **avg gross +0.0004**,
  hit 0.53. Calm net −0.006 (141 trades) · shock net +0.007 (63 trades).
- **Off-years** (z≈0, not below RW-median): **2009, 2012, 2017, 2020, 2025** — mean VR(20)=**1.016** vs on-years
  0.626; mean half-life **26.5** vs on-years 15.4 bars.

## 3. The six trader questions (answered)
1. **Stable across regimes?** **YES.** Pooled mean-z −0.627 (p≈0.0002), 14/19 years below RW-median, present
   pre- *and* post-2020. Sub-diffusion is a robust, regime-spanning property — not one favorable window.
2. **When does it fail?** In **5 of 19 years** — 2009, 2012, 2017, 2020, 2025 — where VR(20)→≈1.0 and half-life
   lengthens to ~27 bars (reversion goes slow/absent).
3. **Failures clustered around shocks?** **NO — the opposite.** Shock-period pooled-z (−0.707) is *slightly more*
   reverting than calm (−0.569), and the meagre trade edge concentrates in shocks (+0.007 vs calm −0.006). The
   off-years are **storage-glut / low-scarcity** regimes (plausibly post-GFC 2009, warm-winter 2012, oversupply
   2017, COVID 2020, recent glut 2025), not acute shocks. **This regime-conditionality is the single strongest
   evidence the persistence is genuine storage MR, not a uniform vendor splice** (a back-adjustment artifact would
   not selectively switch off in glut years). *Caveat:* off-year spacing (3,5,3,5 yrs) is oddly regular — should
   be checked against the vendor contract-roll cadence.
4. **Would a trader stay out?** **YES, unconditionally** — the edge is uneconomic (Q5). The ex-post "avoid gluts"
   pattern is **not** a deployable ex-ante filter (that needs a separately-validated causal regime classifier —
   State-T-adjacent, **out of scope**, §10).
5. **Deployable or merely true?** **MERELY TRUE.** Persistent, regime-structured, tradeable half-life,
   apparatus-corroborated — but per-trade reversion capture (**+0.0004 gross**) is **break-even before costs** and
   net-negative after a conservative 0.003 round-trip (robust to halving the cost; *not* a strawman-rule
   artifact). The one untested door (§11.2): a **portfolio/book** aggregating many sub-cost per-trade spread edges
   with leg-netting — a different, unevaluated claim.
6. **Survives post-2020?** **YES, attenuated.** post-2020 mean-z −0.438 (< −0.32); 2021–2024 below RW-median;
   the post-2020 misses are 2020 (COVID) and 2025 (glut) — consistent with the glut-conditionality.

## 4. Adversarial verification (preserved, §5)
Both lenses HOLD_WITH_CAVEATS, MEDIUM. **(a) "Uneconomic" is robust** (trader): gross is break-even before any
cost; clearing 0.003 needs ~7.5× gross improvement that forbidden rule-optimization can't credibly supply on this
instrument; only portfolio aggregation could rescue it (untested). **(b) "Persistent vs RW" is strong** (t=−4.37).
**(c) "Not back-adjustment" is NOT cleanly excluded** (STRUCTURAL, MEASUREMENT): NG −0.627 is statistically
indistinguishable from the quarter-strength splice anchor (−0.657, p=0.84) and the escape from
BACK-ADJUSTMENT-SUSPECT rests on the hand-set −0.80 threshold; Brent (−3.54, hourly) proves the *apparatus*
detects genuine sub-diffusion but is **off-scale** for NG's daily magnitude. The **regime-conditionality (Q3) is
the main positive evidence** the NG persistence is real. **(d) §11.8 call correct:** strengthen "apparatus can
confirm a real reverter" (Brent positive control); do **not** strengthen "NG edge is real-and-clean"; do **not**
downgrade (regime-conditionality is MR-favoring). Net **neither strengthen nor downgrade the edge.**

## 5. Confidence · non-conclusions · next questions
**Confidence: MEDIUM.** HIGH that NG calendar sub-diffusion is *persistent vs a random walk*; MEDIUM that it is
*genuine storage MR vs partial vendor back-adjustment* (regime-conditionality favors genuine; the splice channel
is not closed); HIGH that the *naive single-instrument book is uneconomic*.
**Explicit non-conclusions:** (a) NOT "deployable" — merely true at the single-instrument naive level. (b) NOT a
clean exclusion of vendor back-adjustment. (c) NO ex-ante regime/timing rule (out of scope, State-T-adjacent).
(d) NOT cross-habitat replicated at matched scale (Brent is hourly/off-scale; §11.7 daily replication still owed).
(e) NO statement on a portfolio book (untested — the genuine open door).
**Next high-information questions (ranked):**
1. **Close the back-adjustment channel:** run the splice diagnostic on the **actual ng12 seam dates** (detect
   monthly-roll jumps in the series) and/or **rebuild NG from raw m1/m2 legs** (data-gated) — and justify/lower
   the −0.80 suspect threshold on a matched-scale instrument. *Until then "genuine MR" stays MEDIUM.*
2. **Portfolio/book test (§11.2):** does aggregating sub-cost per-trade calendar edges across instruments, with
   leg-netting, clear costs? This is the only path from "merely true" to "deployable."
3. **Cross-habitat daily replication (§11.7):** a second *daily* β=1 calendar built from raw legs.
4. **Cycle 2 (doc 22 §7):** controlled-β positive control on a textbook cointegrated pair — the deployment-domain
   construction still untested.

---
*Markers: CONFIRMED (persistence vs RW, HIGH) · STRENGTHENED (regime-conditionality as genuine-MR evidence;
apparatus via Brent) · UNRESOLVED (vendor back-adjustment vs storage MR) · KILLED-FOR-DEPLOYMENT (naive
single-instrument book — uneconomic) · CARRIED-FORWARD (portfolio test; daily cross-habitat; Cycle 2). The
binary-flag instrument was falsified pre-freeze and replaced by pooled mean-z; the "deployable-with-stand-aside"
verdict tier was removed pre-freeze (ex-post ≠ ex-ante). No history erased.*
