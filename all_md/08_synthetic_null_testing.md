# Synthetic Null Testing (#11) — Research Verdict

**Document class:** Permanent AMR research record (institutional memory — appended, not rewritten).
**Status:** **CLOSED. Verdict: B — SURVIVES PROVISIONALLY** on available adversarial evidence. The
observatory survived an adversarial null attack, but **conditionally** — survival depends on a
specific discipline, a real seduction surface exists, and the evidence is a single blind packet on
the ADANIENT placeholder substrate. This is recorded as a **successful result** (the layer earned
its place by surviving falsification), not as a clean win.
**Date opened / closed:** 2026-06-01.
**Scope:** the v0 "synthetic null testing" item (CLAUDE.md §10 #11) — built as a minimal frozen null
set materialized as ordinary instruments, classified blind through REP/RES/CMP only, then
adjudicated against pre-registered kill criteria F1–F5. No new endpoints, no new frontend.

> Uses **prior thesis → instrumentation → blind result → adjudication → what survived**. The verdict
> is frozen at **B**. This record preserves *why we feared hallucinated reversion, how we tested for
> it, what the blind packet showed, why it survived only conditionally, and what discipline the
> survival requires* — not a clean narrative. **No retroactive editing of the blind reasoning or the
> reveal.**

> **▸ CONTEXT (placeholder framing — frozen).** All findings here are **architecture-level** or
> **ADANIENT-substrate-conditioned**, never globally empirical. The synthetic nulls are scale-matched
> to a window of ADANIENT — a **placeholder visual substrate, not the deployment domain**
> (commodities · pairs · cross-asset relative value · spreads — expected materially more
> mean-reverting). No market truth is inferred from synthetic paths or from the one real segment in
> the packet. See `CONTINUATION_STATE.md` §0.

---

## 1. Prior Thesis — the fear that motivated #11

**Claim (working concern, entering #11).** The equilibrium observatory (REP replay + RES residual +
CMP estimator-compare) might **manufacture the appearance of mean reversion where none exists** — i.e.
on a pure random walk, the causal residual `ε = P − μ*` reverts toward zero as a *mechanical*
consequence of μ\* tracking price, and a researcher scrubbing replay could mistake this for genuine
equilibrium behavior. If true, the observatory would be epistemically dangerous: it would *confirm*
the AMR thesis on data that contains no reversion at all.

**The load-bearing question (frozen).** *"Can a disciplined researcher, using only REP + RES + CMP,
distinguish genuine mean reversion from mechanical pseudo-reversion on scale-matched data?"* The
burden of proof was **survival**, not usefulness-by-default.

**Frozen guardrail (do NOT reinterpret).** *"Residual reverts on a random walk"* is **expected
mechanics** — it is what an EMA/Kalman estimator does by construction. It is **NOT evidence** of
genuine reversion and **NOT a kill**. The layer lives or dies on **discrimination**, not on whether
mechanical reversion appears (it always does).

**The discrimination boundary (frozen conceptual distinction).**
- **Genuine mean reversion.** Price returns to a *persistent* equilibrium; μ\* stays put as price
  oscillates around it. The equilibrium has a stable home.
- **Mechanical pseudo-reversion.** μ\* *chases* a wandering price; the "equilibrium" roams to levels
  it never revisits. Residual reverts (mechanics) but the equilibrium itself wanders.
- **Bad question:** *did price come back?* — a random walk round-trips by chance and will pass this.
- **Good question:** *did the equilibrium stay put?* — only genuine reversion passes this.

---

## 2. Why the layer was built — objective & instrumentation

**Objective.** Stage a controlled adversarial test in which known-non-reverting processes are made
visually indistinguishable from a genuine reverter at the surface level, then check whether the
observatory (and a disciplined researcher driving it) separates them — and, critically, whether
replay *seduces* the researcher into false conviction.

**Frozen null set (minimal — only these; D1/D2 deferred).**
```
N1  NULL_RW      pure random walk          P_t = P_{t-1} + eps_t            (no reversion)
N2  NULL_DRIFT   drifted random walk       P_t = P_{t-1} + mu + eps_t       (unit-root stochastic trend; NOT trend-stationary)
A0  ANCHOR_OU    OU / AR(1) positive anchor (genuine reversion — NOT a null; the F1 contrast)
```
A0 is deliberately **not** a null: it is the positive control. Without a genuine reverter in the
mix, "everything looks non-reverting" would be uninformative. `lam = −0.05` was chosen *slow* so A0
is adversarial (not trivially distinct from a wandering walk).

**Frozen modification (applied).** **No variance-ratio / no metric discriminator / no threshold /
no score surface.** Nulls are correct *by construction*; discrimination is **REP-first, visual,
blind**. A metric gate would have answered a different (easier) question than the one frozen.

**Hardened blind protocol (F4 — replay seduction).** Five opaque close-only instruments
`BLIND_1..5` on the shared window dates: real ADANIENT segment + N1 + N2 + A0 + a **duplicate null**
(second independent RW — defeats one-of-each elimination). All flattened to close-only (O=H=L=C) so
the real series cannot be betrayed by candle wicks. Fresh independent seeds. Order shuffled by a
sealed master seed; identity mapping sealed in `backend/data/blind_key.json`, **not opened until
every blind was classified**.

**Zero new surface.** `synthetic.drift_random_walk` added (N2; `random_walk`=N1 and `ou`=A0 reused);
`backend/scripts/generate_nulls.py` materializes all instruments into the live DuckDB so they flow
through the existing `/diagnostics` → REP/RES/CMP with **zero new endpoints, zero new frontend**.
`backend/tests/test_synthetic_nulls.py` (3 metric-free construction tests, green) guards only that
the generators are what they claim (e.g. `drift_rw(mu=0)` ≡ pure RW bit-for-bit; N2 ≠
trend-stationary `trend()`).

**Scale-match decision (2026-06-01, frozen rationale).** The frozen arithmetic RW with constant
absolute σ cannot be scale-matched to ADANIENT's *full* 2463-bar history — ADANIENT's volatility is
multiplicative (~100× ramp), so full-history constant-σ nulls go negative and stay tiny while the
real series reaches ~3800, making the blind separable by **scale/sign alone** (an invalid confound).
Resolution: restrict to a **scale-stationary ~600-bar window** (idx 650–1250, 2015-06-08 →
2017-11-09, max/min ≈ 2.6×). The frozen arithmetic form is preserved (`n` was never frozen). A
**disclosed positivity filter** (lowest seed whose path stays strictly positive) is a realism
constraint **orthogonal to reversion dynamics** — it does not bias discrimination.

---

## 3. Blind adjudication (frozen — classifications recorded BEFORE the reveal)

Surfaces reconstructed read-only for `BLIND_1..5` without opening the key. Observatory-native visual
descriptors used (NOT threshold verdicts): equilibrium roam / price-range ratio (low = stable home =
reverting; high = wandering), EMA-crossing count, `|mean ε| / std ε` (persistent one-sidedness =
trend lag), Kalman terminal/mean velocity (CMP).

**Frozen blind calls (verbatim — no retroactive edit):**

| Blind | Frozen call | Confidence | Frozen reasoning |
|---|---|---|---|
| BLIND_1 | **reverting** | MED-HIGH | Equilibrium roams least (roam/range ≈ 0.60); symmetric oscillation (89 EMA crossings, mean ε ≈ 0); lowest Kalman velocity — a **stable home**. |
| BLIND_2 | **non-reverting** | MED | μ\* roams ≈ 0.89 of range; mild downward lean; no stable home (RW-like). |
| BLIND_3 | **uncertain → lean non-reverting** | LOW-MED | Large up-excursion to ~93 then return near start (~48) — an RW **round-trip masquerading as reversion** (the seduction case). |
| BLIND_4 | **non-reverting** | MED-HIGH | Strongest one-sidedness (`|mean ε|/std` ≈ 0.30); highest mean velocity (≈ 0.101) — trend/drift. |
| BLIND_5 | **non-reverting / trend** | MED-HIGH | Clear uptrend ~54 → ~84; strongest terminal velocity (≈ +0.121). |

**Reveal (frozen — `blind_key.json`, opened only after the above were frozen):**

| Blind | Truth | Outcome |
|---|---|---|
| BLIND_1 | `A0_ou_seed103` — genuinely reverting | ✅ **HIT** — the single true reverter, isolated correctly |
| BLIND_2 | `N2_drift_seed102` — non-reverting (drift RW) | ✅ correct |
| BLIND_3 | `N1b_rw_seed104` — pure RW (duplicate null) | ✅ **not seduced** — flagged the exact trap, leaned correct |
| BLIND_4 | `N1_rw_seed101` — pure RW | ✅ correct |
| BLIND_5 | `real_ADANIENT_seg` — **ground truth UNKNOWN** | visually consistent (trend); not a scored item |

**Score (frozen).** The single genuine reverter (A0) was isolated; **zero nulls were called
reverting**; the textbook seduction case (round-trip RW, BLIND_3) was resisted — flagged uncertain,
not "reverting." No false positives. This is a strong discrimination result. The discriminator that
worked was **equilibrium stability** (does μ\* hold a home), **not** residual reversion (which
appeared on every series, as expected).

---

## 4. F1–F5 Adjudication

Each criterion is a **kill** — "supported" means it argues for *survival* (the kill did not fire).

| Criterion | Verdict | Evidence |
|---|---|---|
| **F1 — indistinguishability (primary)** | **SUPPORTED** | A0 was separable from N1/N2 without false positives. Working cue was architecture-native: equilibrium roam/range (A0 ≈ 0.60 vs nulls 0.71–0.89) + residual symmetry + Kalman velocity. **The discriminator was equilibrium stability, NOT residual reversion** (residual reverted everywhere — expected mechanics, not a kill). |
| **F2 — fake equilibrium** | **SUPPORTED** | μ\* did **not** manufacture a basin convincing enough to force a false-reversion call. BUT BLIND_3 (RW round-trip) is a genuine *near-basin*: the mechanism to forge one exists. Survival held only because the roam/stability check exposed that the "level" itself wandered. *Preserve the lesson: ask "did equilibrium stay put?", not "did price come back?"* |
| **F3 — misleading production surface** | **SUPPORTED (conditional)** | REP + CMP led toward *correct* narratives (CMP Kalman velocity flagged drift; RES residual symmetry separated trend-lag from symmetric wander). **Caveat (institutional warning):** RES autocorr / half-life numbers are **smoother-manufactured** (doc 06 C5) and *would* report "reversion structure" on a pure RW. Survival is conditional on **not** trusting RES persistence stats as ground truth. No redesign implied — documented caveat only. |
| **F4 — replay seduction (most important)** | **SUPPORTED (weakened)** | Replay did **not** seduce: the acid-test case (BLIND_3) was flagged as the trap; no null was called reverting. BUT the seduction exerted **measurable pull** — BLIND_3 reached only "uncertain," not confident rejection — and the surfaces were reconstructed computationally, likely making the analysis *more* disciplined than a human eyeballing a replay scrub. The seduction surface is real and architecture-level (true of any RW). |
| **F5 — observatory survival** | **SUPPORTED (conditional)** | No hallucination forced a wrong verdict; no major skepticism downgrade required. Survival is **conditional** on three frozen disciplines: (i) equilibrium-stability / μ\*-roam check, (ii) Kalman-velocity context, (iii) skepticism toward RES persistence stats. No false positives occurred. |

---

## 5. Why B — not A, not C

**Not C (fails).** The observatory genuinely discriminated: it isolated the one true reverter,
called zero nulls reverting, and resisted the seduction trap. No redesign is needed; it did not
hallucinate its way to a wrong verdict. C would misrepresent a real success.

**Not A (survives strongly).** Survival is **conditional**, not clean:
```
discipline required      — works only with the equilibrium-stability check + Kalman velocity;
                           residual-reversion alone would mislead
seduction surface exists — round-trip RW (BLIND_3) exerted real pull; reached "uncertain"
RES-stats vulnerability  — autocorr/half-life look convincing on pure RWs (doc 06 C5)
n = 1 packet             — single blind packet, single seed each, single (placeholder) substrate
```
A would overstate robustness that one packet cannot support.

**B is the honest call:** *useful but vulnerable, requires stronger caveats* — survived
falsification, conditionally. **Do NOT upgrade to A. Do NOT downgrade to C.** The verdict is frozen.

---

## 6. What survived (banked explicitly)

```
equilibrium stability > residual reversion   — the discriminator that actually worked;
                                               residual reversion is mechanics, not evidence
round-trip RW trap resisted                  — the seduction case was flagged, not believed
μ* less fragile than feared                  — the observatory did not confirm reversion on nulls
observatory survived adversarial test        — no false positives across four nulls
```

**Architecture-level findings (structural / global to the machinery):**
```
equilibrium stability > residual reversion       (the working discriminator)
round-trip-RW seduction exists                    (exists for any RW; not dataset-specific)
RES persistence metrics can mislead on a RW       (smoother mechanics; doc 06 C5)
the observatory CAN discriminate with discipline
```

**ADANIENT-substrate-conditioned observations (local / provisional — NOT market claims):**
```
the specific synthetic paths and seeds
the difficulty / ease of the individual blind calls
the trend interpretation of the real BLIND_5 segment
"one packet discriminated cleanly" — this is n=1, not a robustness claim
```

No global market claims. No commodities/pairs/cross-asset inference. Placeholder-substrate framing
maintained throughout.

---

## 7. Institutional warnings (frozen — high leverage)

```
do NOT trust RES persistence metrics (autocorr / half-life) blindly —
  they look convincing on a pure random walk (smoother-manufactured; doc 06 C5)

when judging reversion, ask:  "did the equilibrium stay put?"
  NOT:                        "did price come back?"
  (a random walk round-trips by chance and passes the bad question)
```

---

## 8. Surviving uncertainty (caveats — NOT grounds to reopen)

```
single blind packet           (one packet, one seed per process — n=1)
ADANIENT-substrate-conditioned (nulls scale-matched to a placeholder window, not deployment data)
deployment regime untested     (deployment targets expected more mean-reverting; not observed here)
seduction surface is real      (round-trip RW exerted measurable pull; human eyeballing may resist less)
RES-stats vulnerability        (documented, not redesigned away)
```

Confidence in the verdict: **B — survives provisionally**. Multi-criterion and clear on this packet,
but conditional and single-substrate.

---

## 9. Reopen trigger (frozen)

Reopen **only if**:
```
cross-substrate ambiguity                  — the discrimination fails to replicate on another substrate
deployment-domain evidence contradicts      — a real mean-reverting instrument disagrees
F1 robustness weakens materially            — the indistinguishability kill starts to fire elsewhere
```
**No redesign by default. No new methodology. No re-litigation** of the frozen B verdict otherwise.
The null generators, the blind protocol, and `blind_key.json` are retained to make a re-run cheap on
a new substrate.

---

## 10. Disposition

- **Instrumentation:** retained — `synthetic.drift_random_walk`, `generate_nulls.py`,
  `test_synthetic_nulls.py`, and the materialized labeled/blind instruments in the live DB. Nulls are
  ordinary instruments; no surface to de-register.
- **Stack:** #11 is **closed** and **does not block** upward movement. The equilibrium observatory
  remains lean: **REP survives**, **LAG killed (doc 07)**, **Synthetic Null survives provisionally**,
  **μ\* provisional/non-blocking**.
- **Equilibrium Observatory v0:** with #11 closed, the observatory / epistemics phase is **formally
  complete**. The project transitions toward **model logic — State T planning** (no State T
  implementation yet; transition marker only, see CLAUDE.md §4/§10).
- **Known backlog (audit, not actioned):** `generate_nulls.py` hardcodes ADANIENT as the
  scale/date reference — parameterize before reusing on another substrate; re-baseline researcher
  intuition on a reverting instrument (e.g. `ANCHOR_OU`) per CONTINUATION_STATE §0.

*Markers used: SUPPORTED · WEAKENED · STRENGTHENED.*
