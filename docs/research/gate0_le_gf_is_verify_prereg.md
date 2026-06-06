# Gate 0 — LE-GF IS-Only Anchor Verification (Pre-Registration)

**Written:** 2026-06-06. **Status:** FROZEN BEFORE EXECUTION.
**Motivation:** Doc 45 proved that full-period VR can mask IS-non-significance (RB-CL: full-period
p=0.015 → IS-only p=0.313). The entire programme's "MR exists in trendy markets" claim now rests on
LE-GF as §11.8 anchor. Before anything proceeds (Track 1, Track 2), LE-GF must survive the same lens
that downgraded RB-CL.

---

## Instrument

LE-GF: CME_DL_LE2!_1D (Live Cattle continuous) vs CME_DL_GF2!_1D (Feeder Cattle continuous).
β-mode: **F5** (presample OLS, first 25% of full dataset, frozen; f_βupdate = 0.000).
Scaling: LE raw close × 1.0 (¢/lb); GF raw close × 1.0 (¢/lb). No unit normalization needed
(both legs same unit). Cost: 0.20 ¢/lb round-trip.

---

## IS / OOS Definition (frozen)

```
OOS_SPLIT     = 0.70        # first 70% = IS; last 30% = OOS
DATE_MIN_LEGF = "1995-01-01"
DATE_MAX      = "2026-06-03"
```

IS period = first floor(0.70 × N) bars of the merged LE2!-GF2! dataset after β pre-sample.
OOS period = remaining 30%. Pre-sample (first 25% for β estimation) is NOT part of the IS
period for VR testing.

---

## Primary test

**VR(20) — raw spread, IS-only.**

This is the test RB-CL failed (IS p=0.313). Gate criterion is IDENTICAL to the one that
downgraded RB-CL. No softening for LE-GF's stronger full-period signal.

Surrogates (n=500 each, seed=20260606, identical IS-window conditioning):
1. **RW** — random walk with same IS mean/σ of first differences
2. **GARCH(1,1)** — GARCH fit on IS residuals, resimulated
3. **MA(1)-noise** — MA(1) fit on IS first differences, resimulated
4. **OU** — OU process fit on IS spread (θ_ou, μ_ou, σ_ou from MLE), resimulated

VR(20) = Var(20-bar returns) / (20 × Var(1-bar returns)), one-sided (tests VR < 1).

p_rw   = fraction of RW surrogates with VR ≤ observed (lower = more sub-diffusive; PASS if small).
p_garch, p_ma1, p_ou = same for their respective nulls.

---

## Pre-committed pass / fail criteria

| Criterion | Required | Consequence if fails |
|---|---|---|
| IS-only VR(20) p_rw < 0.050 | mandatory | FAIL → STOP + escalate to owner |
| IS-only VR(20) p_garch < 0.100 | supporting | note as weakness if fails |
| IS-only VR(20) p_ma1 < 0.100 | supporting | note as weakness if fails |
| IS-only VR(20) p_ou < 0.100 | supporting; OU is the favourable null | note if fails |
| IS mean_net (fade, θ=1.0) > 0 | supporting (sanity) | note if fails |

**PASS:** p_rw < 0.050. LE-GF anchor holds. Proceed to Track 1 + Track 2.
**FAIL (p_rw ≥ 0.050):** STOP IMMEDIATELY. Do not start Track 1, Track 2, or any build.
Escalate to owner: "LE-GF IS-only VR failed; §11.8 anchor unverified; programme premise
requires re-examination before pivot."

Adjudication: named agents (adversarial, statistical, trader) + independent Codex/o3-pro
re-implementation on same data (cross-model adversary).

---

## Secondary characterisation (not gating; reported regardless)

- IS VR(5), VR(10), VR(20), VR(40) — multi-lag profile
- Full-period vs IS-only VR(20) comparison (replicates the RB-CL doc-45 lens)
- IS fade economics: n_trades, mean_net, Sharpe (θ=1.0, LB=60, MH=40, cost=0.20)
- Power analysis: SE = √(2q/N_IS), z-statistic, implied power at α=0.05
- IS vs OOS VR comparison (informational)
- Deseasonalized IS VR (informational; not the primary gate — raw VR is the gate)

---

## What this does NOT test (scope freeze)

- No re-estimation of β (F5 frozen after pre-sample; any β-update is INADMISSIBLE)
- No threshold tuning on IS (θ=1.0 is frozen from sleeve_verification_prereg.md)
- No OOS evaluation (OOS is held out; IS sanity only)
- No new pair testing
- No deseasonalized VR as the primary gating criterion (raw = gate; DS = informational)

---

## Adjudication protocol

Three named agents run AFTER script results:
1. **Adversarial** — attempt to kill the anchor (data mining, power, artifact, construction)
2. **Statistical** — assess power, p-value quality, surrogate coverage
3. **Trader/PM** — IS-strong/OOS-weak pattern; economic plausibility

Plus: one independent re-implementation (different code path, same data).

If agents disagree, research lead synthesizes a verdict, explicitly stating which objection
was decisive and why.

---

## Frozen parameters (cannot change after this line)

```python
SEED_GATE0    = 20260606
OOS_SPLIT     = 0.70
PRE_FRAC      = 0.25
JUMP_K        = 8.0
JUMP_W        = 60
LB            = 60
MH            = 40
PRIMARY_THETA = 1.0
COST_LEGF     = 0.20       # ¢/lb
NS_SURR       = 500        # surrogates per null
DATE_MIN_LEGF = "1995-01-01"
DATE_MAX      = "2026-06-03"
VR_Q_PRIMARY  = 20
VR_Q_SECONDARY = [5, 10, 40]
PASS_P_RW     = 0.050      # HARD gate
WARN_P_OTHER  = 0.100      # supporting gates
```
