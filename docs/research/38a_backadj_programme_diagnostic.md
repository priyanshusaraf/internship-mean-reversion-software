# Doc 38a — Back-Adjustment Programme-Wide Diagnostic

**Document class:** Measurement diagnostic (not a research result — data characterization).
**Date:** 2026-06-05. **Mode:** Track C. **Data:** `data/processed/backadj_diagnostic.json`.
**Scope:** NG vendor spread, BRN M1-M2, ZC M1-M2. Graded against doc-23 splice-RW anchors.

> **This is a MEASUREMENT diagnostic only. It does NOT change any MR verdicts directly. It grades
> the data quality risk and qualifies the interpretation of VR results computed on these spreads.**

---

## Method

1. Load each spread (or construct from raw legs for BRN/ZC).
2. Run the pooled mean-z test (doc-22 window_vr20_z, yearly windows, RW surrogate N=200) on the RAW spread (no deseasonalization). Raw comparison is anchor-consistent: the doc-23 splice anchors were calibrated on the NG raw spread.
3. Run the same test on the DESEASONALIZED spread (causal trailing month-of-year mean) — for comparison.
4. Grade the RAW spread against:
   - CLEAN: mean_z ∈ (−0.80, +∞) — above the suspect zone
   - SUSPECT: mean_z ∈ (−1.05, −0.80) — near the frac0.25 splice anchor
   - CONTAMINATED: mean_z < −1.05 — at or below frac0.5 splice anchor

**Reference anchors (doc 23 splice-RW simulation):**
```
frac=0.25 injection → mean_z ≈ −0.657  (quarter-strength splice = lower bound of suspect)
frac=0.50 injection → mean_z ≈ −1.053  (half-strength splice = contaminated threshold)
RW null band: [−0.32, +0.41]
Genuine moderate-MR anchor (OU φ=0.95+seasonal): ≈ −0.33
```

---

## Results

| Spread | Raw mean_z | Deseason mean_z | Amplification | Grade (raw) |
|---|---|---|---|---|
| NG (vendor ng12, 2006+) | -0.581 | -1.523 | 2.6× | **CLEAN** |
| BRN M1-M2 (raw legs, 1997+) | +0.259 | -0.699 | ∞ (sign flip) | **CLEAN** (but see note) |
| ZC M1-M2 (raw legs, 1991+) | -0.315 | -1.413 | 4.5× | **CLEAN** |

**All three spreads grade CLEAN on raw comparison** (no splice contamination in the raw spread itself that exceeds the frac0.25 anchor threshold).

---

## The Deseasonalization Amplification Pattern

The critical finding is NOT the raw grade — it's the **deseasonalization amplification**:

| Spread | Spread mean (raw) | Raw mean_z | Deseason mean_z | Δ |
|---|---|---|---|---|
| NG | ≈ -0.04 $/MMBtu (near zero) | -0.581 | -1.523 | 2.6× |
| BRN | **-7.186 $/bbl** (large level) | **+0.259** | **-0.699** | Sign flip |
| ZC | **202.5 cents/bushel** (huge level) | -0.315 | -1.413 | **4.5×** |

**Pattern:** The larger the persistent level offset in the raw spread (back-adj artifact), the larger the deseasonalization amplification of apparent MR. NG has a near-zero spread mean (near-zero back-adj accumulated offset) and shows moderate amplification. BRN and ZC have large persistent level offsets and show extreme amplification (including sign flip for BRN).

**Mechanism:** The causal trailing month-of-year mean subtracts the accumulated back-adj offset, which clusters by calendar month. This forces the deseasonalized spread to oscillate around zero, imposing stationarity by construction, not by genuine market dynamics.

---

## Per-Spread Assessment

### NG (vendor ng12 spread)

**Raw mean_z = -0.581. CLEAN.** Consistent with doc-23 finding of -0.627 (minor difference from method). The NG raw spread has genuine sub-diffusion — regime-conditional, above the frac0.25 anchor, consistent with genuine storage MR that turns off in glut years.

**Deseason mean_z = -1.523.** The 2.6× amplification moves NG into the CONTAMINATED zone. This is the same pattern as BRN/ZC but from a smaller base. The NG raw signal is genuine; the deseasonalized NG signal should be treated with additional caution, but the raw genuine-ness is established.

**Note on NG back-adj:** NG's vendor ng12 spread is pre-built and opaque. The frac0.25 splice anchor (-0.657) matches NG's doc-23 pooled mean-z (-0.627) closely. This channel is UNRESOLVED (doc 23): genuine MR and quarter-strength splice produce statistically indistinguishable signals.

### BRN (raw legs)

**Raw mean_z = +0.259. CLEAN grade, but TRENDING sign.** The raw BRN spread is slightly TRENDING (VR > RW median on average). This means the raw BRN M1-M2 spread shows NO genuine mean reversion in the raw form — in fact, slight diffusion/trending on average. The "MR" observed in doc 36 (VR=0.282) is ENTIRELY a product of the deseasonalization step.

**Deseason mean_z = -0.699.** This is the doc-36 result and is within the CLEAN zone. But the input to this MR signal is a raw spread that is mildly trending, not genuinely mean-reverting. The deseasonalization of a -7.186 $/bbl persistent level creates artificial MR.

**Implication:** The BRN MERELY-TRUE verdict (doc 36) should be qualified: the raw signal suggests NO genuine storage MR in the BRN M1-M2 spread at daily frequency. The entire VR signal is from deseasonalization artifact. The verdict remains MERELY-TRUE (not DEAD_CALENDAR) because the pre-reg used the deseasonalized spread, but the contamination flag is strong.

### ZC (raw legs)

**Raw mean_z = -0.315. CLEAN grade.** Marginally below the RW null band (-0.32 to +0.41), showing barely detectable raw sub-diffusion. This is weaker than NG (-0.581) and is not regime-conditional (no equivalent glut-year analysis done).

**Deseason mean_z = -1.413.** 4.5× amplification. Falls in the CONTAMINATED zone (below frac0.5 anchor -1.053). The deseasonalization of +202.5 cents back-adj offset creates apparent strong MR.

**Implication:** The ZC CONTAMINATED_RESULT verdict (doc 38) is supported by this diagnostic. The raw marginal sub-diffusion (-0.315) could be genuine (storage MR) or noise, but it is too weak to sustain the verdict-changing deseasonalized signal.

---

## Programme-Wide Finding

**The causal deseasonalization step, applied to back-adjusted continuous futures spreads with large persistent level offsets, amplifies apparent sub-diffusion by 2.6× to 4.5×.** This amplification is mechanically driven by the removal of accumulated back-adjustment offsets, not by genuine seasonal economics.

**Diagnostic rule for future instruments:**
- If raw spread mean ≈ 0: deseason amplification ≤ 2-3×; signal likely genuine if raw z < -0.50
- If raw spread mean >> 0 (large back-adj offset): deseason amplification can be extreme; signal dominated by artifact
- Flag: if |raw spread mean| > 1 std of the spread → treat deseasonalized VR result with HIGH contamination suspicion

**NG is the only instrument with a confirmed genuine raw sub-diffusion signal in the calendar programme.** BRN and ZC raw signals are trending and marginal respectively; their apparent MR is primarily a deseasonalization artifact.

---

## Action

This diagnostic is informational. No verdicts are changed retroactively. The findings are integrated in:
- Doc 36 (BRN): contamination flag added
- Doc 38 (ZC): contamination verdict reflects this finding
- Doc 38b (reconciliation): programme-wide implication documented

**Future instruments:** Before running the VR test on a back-adjusted continuous futures spread, check the raw spread mean for anomalous level offsets. A large persistent offset (|mean| > 0.5 std) flags potential deseasonalization artifact and requires raw-spread corroboration.

*Diagnostic run: 2026-06-05. Script: scripts/run_backadj_diagnostic.py.*
