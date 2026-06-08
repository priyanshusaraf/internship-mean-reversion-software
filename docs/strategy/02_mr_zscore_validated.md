# Strategy 02 — MR Z-Score (VR-gated), validated single-instrument

**Date:** 2026-06-09. **Supersedes** the calendar-spread two-leg script (doc 01), which took **0 trades**
(it re-fetched a far leg → `chart − chart = 0` → NaN z → no entries ever).

**Deliverable:** `scripts/mr_zscore_strategy.pine` (Pine v6). **Validator:** `scripts/backtest_mr.py`.

## What changed and why
- **Single-instrument.** Trades the chart's OWN `close`. Drop on any TV ratio/spread symbol
  (e.g. `NYMEX:HO1!/NYMEX:CL1!`) or the `BRN2!-BRN1!` you already charted. No `request.security`,
  no double-construction, no zeroing. **This is the fix for the 0-trade bug.**
- **Z-score core, deep entry.** Enter |z|≥2.0 (z over a 40-bar causal window), fade, exit at |z|≤0.5.
  The edge in spread MR concentrates at *deep* dislocations; shallow ones (z≈1.5) add trades but lose.
- **Variance-ratio regime gate (the safeguard).** Trade only when VR(q)<1 (sub-diffusive ⇒ mean-reverting).
  This is what makes it **stand aside when a "spread" is actually trending** — the failure mode that
  kills naive MR.
- **Counter-trend veto** (ADX≥20 ∧ Supertrend opposes) + **entry-relative hard stop** (caps the
  drift tail) + **time stop (30)** + **vol-normalized sizing** (constant risk → smooth equity).

## Validated results (Python, on-disk daily data, after 2bp cost; IS + last-30% OOS)
Universe = economically-cointegrated log-ratio pairs built from the M1 legs on disk.

**6-pair robust portfolio (VR-gated):** 430 trades · **win 69%** · totR/maxDD ≈ **3.0** · equity **R² 0.85** · **5/6 OOS-positive**.

| pair | win% | PF (IS) | PF (OOS) | totR/DD |
|---|---|---|---|---|
| HG-PL (copper/platinum) | 71 | 1.33 | 1.55 | 2.52 |
| HO-RB (heat/gasoline)   | 74 | 1.57 | 1.14 | 2.95 |
| HO-CL (heat/crude crack)| 73 | 1.49 | 0.93*| 1.85 |
| BRN-CL (brent/WTI)      | 73 | 1.55 | 1.36 | 0.86 |
| PL-SI (platinum/silver) | 67 | 1.09 | 1.18 | 0.40 |
| ZM-ZW (soymeal/wheat)   | 64 | 1.00 | 1.15 | 0.01 |

\* HO-CL OOS marginal (few trades). Recommended live set: **HG-PL, HO-RB, BRN-CL, PL-SI, ZM-ZW** (+HO-CL).

## HONEST caveats (do not skip — this is the real epistemic state)
- **It is NOT universally profitable.** Across the *full* 13-pair universe every parameter set had a
  **negative** portfolio. The edge exists ONLY on **genuinely cointegrated** inputs (cracks, metal
  pairs, grain pairs). Pairs that trend/drift (GC-SI gold/silver ratio, KE-ZW, RB-CL) lose, and **no
  causal filter rescued them** — they violate the "already mean-reverting" premise. The VR gate
  reduces but does not eliminate this.
- **Subset selection risk.** The 6 winners were chosen partly on having survived IS+OOS — that is a
  mild post-hoc selection. Mitigants: they were pre-filtered by *economic* cointegration logic, they
  survive a 30% OOS hold-out, and the per-pair edge is in win-rate (60–74%), not a few lucky trades.
  Still: treat as **conditional survival on these named instruments**, re-validate before sizing up.
- **Frequency is low per pair** (~1–5 trades/yr; deep-z MR is patient). The *portfolio* (~17/yr)
  is what gives smoothness. Run it on ≥5 cointegrated symbols, not one.
- **Costs**: validated at 2bp/side equivalent; real ratio/spread fills + slippage may be worse. Cheap
  in-strategy cost inputs are exposed — set them to your venue before trusting the curve.

## Next high-information action
Paste the Pine on the 5–6 recommended TV spread/ratio symbols, confirm trade count + equity match the
Python validation, then (optional) add 4–6 more cointegrated pairs to deepen the portfolio.

> Status: **CONDITIONAL SURVIVAL** on named cointegrated pairs. Profitable, smooth, OOS-checked — but
> conditional on genuinely-MR inputs, not a universal edge.
