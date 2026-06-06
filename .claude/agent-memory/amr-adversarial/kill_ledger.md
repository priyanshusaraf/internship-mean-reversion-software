---
name: kill-ledger
description: Standing zombie-watch list for the AMR adversarial agent. Every killed/forbidden direction with why it died and its named reopen trigger. Cross-reference before approving any proposed direction.
metadata:
  type: project
---

## Kill Ledger — AMR Programme (as of 2026-06-04)

The zombie prohibition (CLAUDE.md §4) is absolute: a killed direction must not be silently resurrected. Before approving any proposed direction, check every entry below.

---

### 1. State T — pre-reversion stabilization morphology
**Status:** FALSIFIED-IN-FORM / KILLED (doc 11, 2026-06-02)

**Why it died:** The hypothesis that high-|z| windows precede reversions via rising κ, falling AR(1), declining variance was tested across 12 instruments in 5+ habitats. Result: 62/62 cross-habitat comparisons reject. High-|z| windows show directional continuation, not stabilization. The selection-on-deviation null reproduces every apparent "T-shape" — entering at |z|≥θ on a pure RW produces the morphology by construction.

**Reopen trigger:** A NEW, independent pre-registration (not a reskin of the existing morphology) that passes the §4 zombie-reopen test on all four clauses, with a fundamentally different theoretical basis (not just a new statistical costume for the same shape). No reskin of CUSUM, Markov-switching, run-length-VR, TAR/SETAR counts — these were explicitly enumerated as inheriting the same object-class error.

---

### 2. Predictive transition object — trend→MR transition probability / precursor
**Status:** §4-FORBIDDEN (doc 24, 2026-06-04) — object-class error, not a statistical failure

**Why it died:** A transition is *defined by the regime that follows* the candidate instant. No causally-definable transition label exists at bar t — the label is available only ex post. Every statistical costume inherits this error. "Causal escapes" were enumerated and each collapses: Markov-switching → future-label; CUSUM → forward-read; run-length-VR → rolling-manufacture (the doc-19 artifact); TAR/SETAR → selection-on-deviation. Three independent adversarial agents voted KILL; none found a valid causal formulation.

**Reopen trigger:** Acquisition of signed order flow (OFI), open interest (OI), or COT positioning data on a flow-driven instrument, PLUS a new pre-registration with a leak-free causal label (defined by a contemporaneous flow signal, not by the subsequent regime). Data, not a cleverer statistic.

---

### 3. NG selectivity — unconditional high-z entry on NG calendar
**Status:** A_FALSE_RESCUE / KILLED (doc 31, 2026-06-04)

**Why it died:** Pre-registered adversarial test (N=500, θ∈{1.0,1.5,2.0,2.5}, RW+GARCH+OU+Splice surrogates, episode-jackknife, OOS split). Primary θ=1.0: gross = −0.0006, p_rw = 0.551. θ=2.0: p_rw = 0.417 (46th pctile of RW null). p_ou = 1.000 at every θ — a constant-MR OU process with NG's own half-life (φ≈0.95) beats NG at every threshold. The mechanism: NG's MR is regime-conditional (switches off in storage-glut years); unconditional z-entry averages over glut+non-glut = loses the signal. Jackknife collapse >500% at high-θ (one trade drives the apparent edge). The only selectivity path requires a causal regime/inventory classifier = State-T-adjacent = FORBIDDEN (doc 24).

**Reopen trigger:** A fresh pre-registration on a NEW instrument (not NG) that has an inherently higher gross/cost ratio — where the selectivity test would not be dominated by regime-conditionality of the underlying MR. A new instrument that passes the pre-registered selectivity test independently reopens the question for that instrument only.

---

### 4. EIA conditioning on NG — storage_surplus_pct < 10% entry gate
**Status:** KILL_PVAL (doc 34, 2026-06-04)

**Why it died:** Pre-registered N=200 speed gate (doc 33, frozen before data touch). p_rw = 0.502 — the 50th percentile of the RW null. Conditional gross +0.0056 ≈ RW null median +0.0057. Selection-on-regime artifact: EIA conditioning improves gross equally in zero-MR surrogates (the conditioning selects low-vol / low-glut windows where gross is systematically higher regardless of MR). Data limitation: EIA DNAV only available 2010+; glut years 2009/2012 excluded from the test.

**Reopen conditions** (all required simultaneously): (1) full-vintage EIA data acquired (release-date timestamped, not current releases applied retroactively); (2) vol-controlled check demonstrates VR improves under conditioning, not just gross; (3) cross-habitat replication on BRN calendar passes the same conditioned surrogate test; (4) falsification check on a non-storage instrument (e.g. Gold calendar — should NOT respond to EIA) confirms the conditioning is specific to storage economics.

---

### 5. Rolling-OLS-β-on-levels
**Status:** INADMISSIBLE — not a kill with a reopen, a permanent construction ban

**Why it is inadmissible:** The spread increment decomposes as `ΔS_t = (ΔA_t − β_{t-1}·ΔB_t) − (β_{t-1}−β_{t-2})·B_{t-1}`. The second term (β-update-noise × trending price level) accounts for 82–97% of Var(ΔS) on trending legs (proven synthetically in doc 19). For a true OU spread with true VR < 1, W=60 rolling-OLS-β fabricates VR = 6.23. Any VR result from a rolling-OLS-β-on-levels spread is a measurement of the β-update artifact, not mean reversion. This is a STRUCTURAL defect — it cannot be mitigated by increasing N, changing nulls, or adjusting thresholds.

**Reopen trigger:** None. Use β=1 definitional spreads (same-unit calendars) or controlled/regularized β (once Cycle-2 apparatus is proven). Rolling-OLS-β-on-levels is closed as a VR test construction.

---

### 6. MRScore as a predictive signal
**Status:** ARCHIVED (doc 09, 2026-06-02)

**Why it died:** The MRScore engine is computationally correct and the code passes all tests. However, on real data (ADANIENT), the score inverts: a pure RW scored highest. Discrimination is reliable only in expectation across many windows, not in any single window. The score cannot be trusted to identify a specific moment as "MR-favorable."

**Current authorized use:** Observatory diagnostic only. The `GET /{id}/mrscore` endpoint is read-only, structurally terminal, and carries a prominent regime-warning gate in the UI. Never wired to an entry signal.

**Reopen trigger:** None for signal use. The observatory diagnostic use is permanent.

---

### 7. "Centering drives μ* usability" — Kalman centering as primary selection criterion
**Status:** DEMOTED (doc 06 §12, 2026-06-01)

**Why it was demoted:** The Kalman centering advantage over matched-span EMA is confounded by S1 (detrending tautology): Kalman carries an integrated velocity state, and any integrated drift term removes drift better than EMA by construction. The comparison is structurally tilted toward Kalman on the centering axis regardless of whether Kalman discovers anything real about equilibrium. The 1.6× real-market centering ratio survives neither the S1 control nor the C1–C6 contamination audit.

**What remains confirmed:** The EMA lag bias mechanism is analytic and frozen (`slope × span/2`, confirmed to 3 sig figs). What is unconfirmed: whether removing this bias constitutes better *reversion discovery* rather than generic detrending (S1) without signal absorption (S2).

**Reopen trigger:** A cross-instrument panel (≥3 real instruments spanning trend/pullback/sideways/volatile regimes) running the §13 walk-forward decay test with S1 (naive-detrend baseline) and S2 (surrogate-null) controls. The single-instrument ADANIENT result (R²ₒₒₛ ≈ 0) had insufficient power. Currently deprioritized — no Tier-1 question depends on it.
