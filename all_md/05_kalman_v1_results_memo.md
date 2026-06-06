# Anchored Kalman μ* — v1 Results Memo

> **▸ SUPERSEDED (status as of 2026-06-01).** The "REJECTED" verdict below was **overturned** by
> `docs/research/06_kalman_equilibrium_research_update.md` (Rev 1, §6/§8): the KC4 "alpha
> absorption" kill rested on a **confounded reading of synthetic data** — on `ou_in_trend`,
> centering and reversion are entangled by construction, so a high `corr(velocity, deviation)` is
> not evidence the velocity *absorbed* genuine reversion. The estimator was re-authorized for
> controlled real-market study and is now (06 §15, Rev 4) under a **PROVISIONAL / weak freeze**
> (research-only comparison estimator; EMA remains production μ\*). **This memo is retained
> unaltered as the Rev-0 historical record — do not cite its verdict as current.** The Kalman
> equations it pins (`x=[μ,v]`, `F=[[1,1],[0,1]]`, `Q=diag(κ·q_v,q_v)`, `κ=0.05`, innovation
> residual `P_t−μ_{t|t−1}`) remain **frozen** and correct; only the *verdict* changed. Read 06 for
> the current state.

> **Verdict: REJECTED for v1.** Primary kill-criterion **KC4 (alpha absorption)**; secondary
> **KC1 (no artifact reduction)**. Per the frozen spec, thresholds are pre-registered and may
> not be weakened to rescue a result. This memo records, per gate, the numeric outcome against
> its threshold. The verdict is binary; no "promising, needs tuning" outcome is permitted (§9).

**Date:** 2026-06-01
**Estimator:** 2-state local-linear-trend Kalman, `x = [μ, v]`, `F=[[1,1],[0,1]]`,
`Q=diag(κ·q_v, q_v)`, `κ=0.05` (frozen), `H=[1,0]`, research residual = one-step innovation
`P_t − μ_{t|t−1}`.
**Benchmark:** EMA μ\* (same diagnostics, same windows).
**Single knob:** `SNR = q_v / R_p`, swept once on synthetic OU over **`logspace(-9, 0, 28)`**
(9 orders of magnitude; effective span 1.6–250 bars).
**Reproduce:** `backend/scripts/calibrate_kalman.py` (full sweep → `/tmp/cal_table.txt`),
`backend/scripts/probe_h1.py` (focused H1/H2). Generators: `backend/app/services/synthetic.py`.
Estimator: `analytics.compute_kalman_mu_star`. Locked in by `tests/test_kalman_validation.py`.

---

## 1. What was tested and why it matters

Kalman exists to answer one question (§1): does a **velocity-aware** latent-equilibrium model
produce residuals **measurably superior to EMA** — finding mean reversion *inside trends*
(H3 / G-ABSORB) **without manufacturing it on a random walk** (H1)?

The velocity state is the *only* feature distinguishing this from an EMA (§2.1): a local-level
Kalman filter is algebraically an EMA at steady state. So the whole case for Kalman rests on
velocity being simultaneously (a) active enough to not be an EMA (G-IDENT) and (b) disciplined
enough not to chase/absorb the deviation we want to measure (G-ABSORB).

## 2. Gate G0 — well-formed estimator + calibration (PASS, with a null result)

- `compute_kalman_mu_star` runs on all eight generators with no NaN/inf/divergence
  (`TestG0WellFormed`, `TestKalmanCausalFirewall` — the temporal firewall holds: a future spike
  at bar 300 leaves μ\* at bars 0–299 bit-identical).
- **Calibration null result:** across all 28 SNRs, **no admissible SNR exists** (admissible =
  OU half-life ±25% **and** G-ABSORB **and** G-IDENT, all simultaneously). The three gates
  occupy **disjoint** SNR regions.

## 3. The disjoint-region finding (the heart of the rejection)

Verified sweep (15 seeds, n=500, burn=100, κ=0.05). OU truth: half-life 6.93, ACF(1) 0.90.

| SNR | effSpan | OU hlErr (H2 ✓<25%) | impulse_cos (G-IDENT ✓<0.99) | absorb (G-ABSORB ✓<0.20) | RW acf1 (H1 wants <0.20) | band |
|-----|--------:|--------------------:|-----------------------------:|-------------------------:|-------------------------:|------|
| 1.0e-9 | 251 | 17.9% ✓ | 0.991 ✗ | 0.208 ✗ | 0.976 | H.. |
| 4.6e-9 | 171 | 19.0% ✓ | 0.990 ✗ | 0.250 ✗ | 0.977 | H.I |
| 1.0e-8 (frozen) | 141 | 20.2% ✓ | 0.987 ✓ | 0.285 ✗ | 0.977 | H.I |
| 4.6e-7 | 54 | 23.6% ✓ | 0.980 ✓ | 0.515 ✗ | 0.952 | H.I |
| 1.0e-6 | 45 | 27.1% ✗ | 0.980 ✓ | 0.545 ✗ | 0.943 | ..I |
| 1.0e-2 | 4.5 | 76.9% ✗ | 0.980 ✓ | 0.584 ✗ | 0.593 | ..I |
| 1.0e+0 | 1.6 | 90.3% ✗ | 0.989 ✓ | 0.362 ✗ | −0.018 | ..I |

Reading the columns:
- **H2 (OU recovery)** passes only for **SNR ≲ 4.6e-7** (effective span ≳ 54 bars). A filter
  must be *slow* to let the OU deviation live in the innovation rather than the level.
- **G-IDENT (not-EMA)** *fails* at the slow end (SNR ≤ 2.15e-9, impulse_cos ≈ 0.991): there the
  velocity is so suppressed the filter has degenerated into an EMA — exactly KC3's warning.
- **G-ABSORB** **fails at every single SNR.** The minimum absorption across the whole 28-point
  sweep is **0.208 > 0.20**, at the slowest setting; it only rises from there.

There is no SNR where H2, G-IDENT, and G-ABSORB are simultaneously satisfied. The narrow window
where H2 and G-IDENT overlap (≈1e-8 to 5e-7) is precisely where absorption is already 0.29–0.52.

## 4. Gate outcomes vs thresholds

| Gate | Requirement | Best achievable | Pass? |
|------|-------------|-----------------|-------|
| **G0** well-formed + firewall | finite on all generators; no future leak | holds | ✅ |
| **H2** OU half-life | within ±25% | 17.9% (at slow SNR) | ✅ (in isolation) |
| **G-IDENT** not-EMA | impulse_cos < 0.99 AND trend bias < 0.3×EMA | cos 0.980, bias ≈0.002 | ✅ (in isolation) |
| **G-ABSORB** absorption | \|corr(v, dev)\| < 0.20 **at all SNR** | **0.208 minimum** | ❌ everywhere |
| **H1** RW null | acf < 0.20 AND not-MR on ≥90% seeds | acf ≈0.98 at OU-recovery SNR; H1 rate 0.00 | ❌ |
| **Joint admissibility** | H2 ∧ G-IDENT ∧ G-ABSORB | none of 28 SNRs | ❌ |

H3, the anchor contingency (§5.4), and Steps 2–4 were not reached: §5 gates the build, and §7
ends it on the first kill. The anchor contingency is gated on G-ABSORB being *marginal*; here it
fails outright at every SNR, and the anchor addresses absorption only via a second level
observation — it cannot move absorption below 0.20 without collapsing μ\* toward the anchor
(KC7). It is not a rescue.

## 5. Mechanism (why this is structural, not a tuning miss)

The constant-velocity state integrates innovations into a drift estimate. On `ou_in_trend`, a
mean-reverting excursion *looks locally like a slope change*, so the velocity state partially
tracks it — regardless of SNR. Slowing the filter (small SNR) reduces tracking but, past a
point, freezes velocity entirely and the filter becomes an EMA (G-IDENT fails, KC3). Speeding
it up (large SNR) lets velocity chase the deviation harder (absorption rises) and destroys OU
recovery (H2 fails). The deviation and a genuine slope change are not linearly separable by a
2-state Gaussian filter with frozen Q — so **the feature that justifies Kalman (velocity) is
the feature that disqualifies it (absorption).** That is a property of the model class, not of
the chosen constant.

## 6. Kill criteria triggered

- **KC4 — Alpha absorption (PRIMARY).** G-ABSORB fails at all 28 SNRs (min 0.208 ≥ 0.20). The
  velocity tracks the deviation; the filter degrades the signal it was meant to isolate.
- **KC1 — No artifact reduction (SECONDARY).** At the only SNRs that recover OU (slow, span
  ≳54), the RW innovation ACF is ≈0.95–0.98 — *worse* than EMA-20's ≈0.88, because a slow filter
  lags the walk and the innovation inherits the lag. H1 pass-rate is 0.00 there.

KC2 (trend penetration) and KC3 (EMA-with-math) are *not* triggered in the admissible-ish window
(velocity does reduce trend lag bias, impulse_cos < 0.99). KC5/6/7 were not evaluated — the build
stopped at the KC4 kill per §7.

## 7. Verdict and consequences

**Kalman REJECTED as a competing μ\* for v1 (KC4 primary, KC1 secondary).**

- Steps 3–4 (workbench compare-mode, full V-/OP- suite) are **not built** — the workbench exists
  to study an *admitted* estimator; §7 ends the build on a kill.
- The filter is **not wired** into `/estimator` or `/diagnostics`. EMA remains the sole
  production μ\*. The `EstimatorPanel` "Kalman" row stays a dimmed placeholder.
- Retained as the reproducible artifact behind this verdict:
  `analytics.compute_kalman_mu_star` (+ `KALMAN_SNR=1e-8`, the least-bad non-admissible point),
  `synthetic.py`, `scripts/calibrate_kalman.py`, `scripts/probe_h1.py`,
  `tests/test_kalman_validation.py` (6 tests, all green: they assert the kill is real and will
  fail loudly if a future change makes any gate pass).

## 8. Process note (integrity)

An earlier draft of this memo reported an admissible band and a KC1-only verdict. Those figures
were produced while the tool-output channel was intermittently truncating results; they were
**wrong** and have been retracted. Every number in this version comes from the clean
`/tmp/cal_table.txt` sweep and from green assertions in `test_kalman_validation.py`. The
pre-registered thresholds were not altered at any point.

## 9. If revisited

This memo does not weaken any v1 threshold. A different conclusion requires a new versioned spec
(`v2`) that re-derives thresholds from first principles — candidate directions: a *relative*
artifact-reduction criterion for H1, a different research-residual definition, an explicit
trend/deviation decomposition (e.g. observed slope as a second channel), or unfreezing `κ`.
Those are v2 design decisions, not v1 rescues.
