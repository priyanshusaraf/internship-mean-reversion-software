# Lag Illusion Instrument (#12 LAG) — Research Verdict

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **CLOSED. Verdict: C — KILLED** (MEDIUM confidence) on available real evidence. The
instrument was implemented and works; the *research layer* did not earn a permanent place. This is
recorded as **high-value negative evidence**, not failed work.
**Date opened / closed:** 2026-06-01.
**Scope:** the v0 "lag-illusion testing" item (CLAUDE.md §10 #12) — built as the LAG workbench
module on the frozen residual-decomposition identity, adjudicated against pre-registered kill
criteria K1–K5 on ADANIENT, then de-registered from the workbench and closed.

> Uses **claim → evidence → implication**. The kill is frozen; this record preserves *why we
> believed the concern, why we tested it, why it failed, and what survived* — not a clean
> narrative. No retroactive editing of the adjudication.

> **▸ CONTEXT (placeholder framing — added post-audit; verdict unchanged).** The "available real
> evidence" is **ADANIENT only — a placeholder visual substrate, not the deployment domain**
> (commodities · pairs · cross-asset relative value · spreads — expected to be materially more
> mean-reverting). ADANIENT is **trend-heavy**, i.e. the regime *least* able to exhibit the
> load-bearing failure mode (Mode B, lag-manufactured false reversion). Therefore: **killed on
> trend-regime evidence; the deployment (mean-reverting) regime remains untested.** This is **not**
> a claim the kill was wrong, and **not** a claim the layer probably survives later — it is the
> precise external-validity boundary: the **C — KILLED (MEDIUM)** verdict stands *within its
> observed regime*, and its generality is pending deployment-domain evidence via the §7 trigger
> (unchanged). See `CONTINUATION_STATE.md` §0.

---

## 1. Prior Thesis — the fear that motivated #12

**Claim (working hypothesis, entering #12).** Causal EMA μ\* lags price inside trends by a
deterministic offset (`≈ slope·span/2`, frozen analytically in doc 06 §2/§7.4). The *feared*
consequence was epistemic, not merely geometric: that this lag could make the **causal residual
`ε_c = P − μ*_c` mechanically misleading** — i.e., manufacture *apparent* mean reversion where no
genuine reversion occurred — and thereby corrupt the very signal the AMR thesis hunts for
(reversion inside trends).

**The question was explicitly NOT** "does lag exist?" (frozen, closed). It was: **"Is lag
materially misleading in a way that REP did not already reveal?"** The burden of proof was
**survival**, not usefulness-by-default.

**Mode A vs Mode B (frozen conceptual distinction).**
- **Mode A — stale trend residual.** Persistent one-sided `ε_c` from steady-trend lag. Usually
  *visually obvious in REP* (price ramps, μ\* trails). Low informational value.
- **Mode B — mechanical snapback (the load-bearing target).** Lag component `L` *collapses*,
  dragging `ε_c` toward zero so it *looks* like a reversion event, even though the honest deviation
  `ε_h` did not revert. This is the dangerous, non-obvious failure mode — it forges the AMR signal.

---

## 2. Why the layer was built — objective & instrumentation

**Objective.** Characterize whether, when, and how often `ε_c` exhibits reversion-shaped dynamics
driven by `L` re-equilibrating (Mode B) rather than by `ε_h` returning to zero — on real data,
with explicit sensitivity to the hindsight reference, to answer *"would EMA μ\* have lied to me
here?"* (not "should I trade this?").

**Frozen identity (exact, verified `max|ε_c−(ε_h+L)| = 0.000`).**
```
μ*_c = causal EMA μ*                              (knowable at t)
μ*_h = centered-MA retrospective reference equilibrium proxy   (future-using, NOT ground truth)
L    = μ*_h − μ*_c           (lag component)
ε_c  = P − μ*_c              (causal residual — what gets interpreted)
ε_h  = P − μ*_h              (residual vs reference proxy)
s    = |L| / (|L| + |ε_h|) ∈ [0,1]   (lag-share — descriptive only; no threshold, no score)
```

**Instrumentation (implemented, then de-registered).** `frontend/src/components/workbench/modules/
LagIllusion.tsx` (LAG) — a retrospective decomposition surface: a bandwidth-switchable
decomposition panel (`ε_c`, `ε_h`, `L`) plus a lag-share strip (`s` for both bandwidths). Reuses
`/diagnostics` (`mu_star` = causal EMA) and the shared `centeredMA` (`frontend/src/lib/smoothers.ts`)
— **zero backend.** Two **fixed** span-derived bandwidths `k_a=⌊span/2⌋`, `k_b=span` (robustness,
not tuned). First/last `k` bars **edge-masked** (no ±k support; retrospective-only). No
ACF/half-life/persistence (smoother-manufactured, doc 06 C5). No rarity scalar, no thresholds, no
safe/warning/danger language. Surfaced as v0 #10's sibling; built per a frozen spec then validated
adversarially.

---

## 3. K1–K5 Adjudication (ADANIENT, 2463 bars 2012–2022, span=20, k=10/20)

Read-only inspection reproducing the LAG arithmetic on real closes (throwaway `/tmp` script, not
committed; not a new instrument). Each criterion is a **kill** — "supported" = it argues for
killing.

| Criterion | Verdict | Evidence |
|---|---|---|
| **K1 — rarity** | **FAILED** (does not kill) | Lag-share common, not rare: `s>0.5` on 64%/51% of bars (k=10/20), `s>0.7` on 37%/26%, median `s≈0.60/0.51`. The residual is *typically* more-than-half lag. |
| **K2 — REP redundancy** | **SUPPORTED — DECISIVE** | Material lag is the *obvious* kind: `corr(|ε_c|, |slope|·price)=0.897` — big residuals sit in trends REP already shows. Lag-*share* barely tracks visible trend (`corr(|slope%|, s)=0.18`); the non-obvious high-`s` bars (~56%) are the **small-residual** bars. **Material lag = obvious in REP; non-obvious lag = immaterial.** |
| **K3 — false-reversion (Mode B)** | **SUPPORTED — mechanism failed to survive** | Of the 20 largest apparent-reversion episodes: **Mode B = 2, honest = 12, ambiguous = 6.** Big excursions decay because price genuinely returns toward the proxy (Δε_h dominates), not because lag collapses. The dangerous mechanism is **rare (~10%)**. |
| **K4 — bandwidth robustness** | **WEAKENED** | Qualitative story survives both bandwidths; per-bar localization does not: `corr(s₁₀,s₂₀)=0.54`, high-`s` Jaccard `=0.46`. *Which* bars are "mostly lag" shifts with `k`. Conclusions robust; danger-localization fragile. |
| **K5 — materiality** | **FAILED** (does not kill) | When lag dominates it *is* material: `|L|/price` median 3.6%, p90 10% (vs typical daily move 1.5%); ~77% of the median `|ε_c|` is lag. But per K2/K3 those material cases are Mode A. |

---

## 4. Why the kill happened

**#12 failed to earn a standalone place.** The decomposition is exact and lag is common and
material — yet:

1. **K2 (decisive).** The *material* lag is **Mode A** — persistent trend lag already visible in
   REP + the hindsight overlay. LAG's genuinely non-redundant signal is concentrated in
   **immaterial** small-residual bars. *Material lag = obvious in REP; non-obvious lag =
   immaterial.*
2. **K3.** The **Mode B** mechanism that alone would have justified a dedicated instrument is
   **rare** on the only real instrument; large apparent reversions are **predominantly honest**.

K1 and K5 did not fire (lag is common and material), but "common + material + obvious + Mode-A" is
not a discovery — it is REP restated. This is the *"interesting, but mostly obvious in REP"*
outcome. **KILLED**, no rescue.

---

## 5. What survived (negative-result value — NOT "nothing learned")

- **Mode B is rarer than feared** on ADANIENT (~10% of large episodes). `STRENGTHENED` confidence
  that EMA μ\* at production span is *less* epistemically dangerous than the working hypothesis
  assumed.
- **Large causal-EMA residual reversions are mostly honest** — price genuinely returns toward the
  reference proxy, rather than lag re-equilibrating. The feared "fake reversion" corruption did not
  materialize in the trend regime.
- **REP is sufficient** for the lag-danger question on available evidence: the observatory did not
  need a second surface to see when μ\* trails.
- **Reusable residual: `frontend/src/lib/smoothers.ts`** (`centeredMA`) remains in use by REP.

---

## 6. Surviving uncertainty (caveats — NOT grounds to keep #12 active)

```
single instrument           (ADANIENT only — doc 06 §15 data gap)
trend-heavy instrument       (the regime least likely to exhibit Mode B)
range-bound real series      (the Mode-B-prone regime) — UNAVAILABLE on disk
production span (20)          (lag scales with span; not swept, by scope discipline)
K4 localization fragility     (qualitative verdict robust; per-bar identification is not)
```

Confidence in the kill: **MEDIUM** — multi-pronged and clear, but single-instrument and unable to
observe the one regime most able to revive the concern.

---

## 7. Reopen trigger (frozen)

Revisit **only if a genuinely range-bound real instrument becomes available** (length ≥ 3×
matched-span). Then **re-run the exact K1–K5 adjudication** on that instrument. **No redesign, no
new methodology, no re-litigation** of the frozen verdict otherwise. The LAG module file and
`centeredMA` are retained inert specifically to make this re-run cheap; the module is **not
re-registered** unless the re-run survives.

---

## 8. Disposition

- **Workbench:** LAG **de-registered** from navigation (`registry.ts`) — killed layers look killed.
- **Code:** `LagIllusion.tsx` **retained inert** (not deleted) for the §7 revisit trigger;
  `smoothers.ts` retained (REP dependency).
- **Stack:** #12 is **closed** and **does not block** upward movement. The equilibrium observatory
  remains lean: **REP survives**, **LAG killed**, **μ\* provisional/non-blocking**.

*Markers used: KILLED · FAILED · SUPPORTED · WEAKENED · STRENGTHENED.*
