# Doc 41 — GC2!-PL2! Gold-Platinum Spread: Non-Energy Cross-Habitat Attempt

**Document class:** Permanent AMR research record (institutional memory).
**Date:** 2026-06-05. **Mode:** Research — non-energy cross-habitat replication attempt (§11.7).
**Protocol:** Same crack-β protocol as docs 39-40. No pre-registration (named next action in doc 40).
**Data:** COMEX GC2! (gold, $/toz) vs NYMEX PL2! (platinum, $/toz). Both $/toz — same units.
**Status:** CONDITIONAL_CONFIRM — structural break ~2015 prevents clean cross-era confirmation.

---

## Prior Belief

GC-PL is a well-studied precious metals spread. Prior probability of clean confirm: MEDIUM (~45%). Key concern pre-noted: the GC/PL ratio inverted dramatically around 2015-2016 (platinum demand collapsed as electric vehicle adoption reduced ICE catalytic converter use). This structural break was expected to complicate the F5 OLS pre-sample β and potentially the full-period F6 result.

---

## Data & Construction

| Item | Value |
|---|---|
| Pair | A = COMEX GC2! ($/troy oz), B = NYMEX PL2! ($/troy oz) |
| Date range | 2001-01-01 → 2026-06-03 |
| N bars (merged) | 6,373 |
| OOS split | 70/30 — IS: 4,461 bars (≤2018-10-23), OOS: 1,912 bars (≥2018-10-24) |
| F5 pre-sample β | 0.3255 (OLS on first 1,593 bars ≈ 2001-2007, when PL ≈ 3× GC) |
| F6 β | 1.0 (fixed) |
| Roll masked | F6: 44 bars; F5: ~43 post-pre-sample |
| Negative values | Zero in both legs |

---

## Structural Context (non-negotiable for interpretation)

GC/PL price ratio through time:

| Era | GC/PL ratio | GC−PL spread (F6 raw) |
|---|---|---|
| 2001-2007 (pre-sample for F5) | ~0.35 (PL ≈ 3× GC) | ~ −900 to −100 |
| 2007-2015 | ~0.7-1.0 (approaching parity) | ~ −300 to +100 |
| 2015-2016 | Regime break — GC/PL crosses 1.0 | Persistent sign change |
| 2016-2026 (OOS) | ~1.2-3.0 (GC >> PL) | ~ +700 to +2000 |

Era means of raw GC−PL spread: early-IS=+250, mid-IS=+158, late-IS=+640, OOS=+1,526.

The GC/PL structural break is driven by: (1) EV adoption reducing platinum demand for ICE catalysts; (2) gold retaining monetary/safe-haven demand. This is not a temporary regime — it is a structural shift with a plausible permanent mechanism.

---

## Results

### Full Period (2001-2026)

| Family | VR(20) | p_rw | p_garch | p_ma1 | p_ou | CONFIRM |
|---|---|---|---|---|---|---|
| F6 (β=1.0) | 0.8171 | **0.005** | **0.030** | **0.040** | **0.020** | **YES** |
| F5 (β=0.325) | 0.3987 | **0.005** | **0.010** | 0.204 | 1.000 | **NO** |

### OOS Period (2018-10-24 → 2026-06-03)

| Family | VR(20) | p_rw | p_garch | p_ma1 | p_ou | CONFIRM |
|---|---|---|---|---|---|---|
| F6 (β=1.0) | 0.6709 | **0.005** | **0.005** | 0.055 | **0.005** | **NO** (p_ma1 marginal) |
| F5 (β=0.325) | 0.6741 | **0.005** | **0.010** | **0.020** | **0.005** | **YES** |

f_βupdate = 0.000 both families. Construction-controlled corroboration: **AGREE** (both show VR20 < 1.0).

---

## Key Findings

**Finding 1 — CROSS-FAMILY SWAP: STRUCTURAL BREAK SIGNATURE:**
F6 confirms full / fails OOS; F5 fails full / confirms OOS. This swap is the direct signature of a structural break. F6 (β=1) detects sub-diffusion over the full 25-year sample because within each regime (pre-2015 and post-2015) the GC−PL spread oscillates — but it never reverts to the same mean across regimes. F5's pre-sample β=0.325 (estimated when PL ≈ 3× GC) is structurally wrong post-2015; the full-period MA1 null (p=0.204) catches the resulting level-drift-induced negative autocorrelation. F5's OOS confirmation is within-OOS-regime MR after deseasonalization adapts to the new level.

**Finding 2 — F6 OOS p_ma1 = 0.055 (MARGINAL MISS):**
F6 OOS is tantalizingly close: VR20=0.671, p_rw=0.005, p_garch=0.005, p_ma1=0.055. The MA1 null at 5.5% suggests marginal negative autocorrelation in increments that the MA1 null just barely explains. In the OOS era (2018-2026), GC−PL oscillated significantly (COVID crash, Ukraine war, EV-demand updates) around a high positive mean — there is within-regime MR, but the MA1 null catches residual bid-ask/roll autocorrelation. This near-miss is not a confirmation per the pre-registered headline gate (RW∧GARCH∧MA1 at 5%).

**Finding 3 — F5 FULL p_ma1 = 0.204 (CLEAR FAIL):**
The frozen pre-sample β=0.325 creates a spread that drifts dramatically through the full sample (from −900 to +1500 as the GC/PL ratio shifted). After deseasonalization, the increments of this spread carry strong MA1-like autocorrelation from the secular level drift, which the MA1 null correctly identifies as not genuine MR. This is NOT the doc-19 β-update artifact — f_βupdate=0.000. It is structural β-drift that the frozen F5 construction cannot handle.

**Finding 4 — NOT A CLEAN §11.7 NON-ENERGY CONFIRMATION:**
For §11.7 cross-habitat replication to be satisfied, we need stable, cross-era confirmation — the same family passing both full-period and OOS, as in HO-CL and RB-CL. The GC-PL result shows regime-conditional within-era sub-diffusion but not stable cross-era cointegration. The physical reason is clear: the GC/PL relationship lacks a stable production/conversion constraint (unlike crude-to-refined-product). Two assets with different demand drivers (industrial vs monetary) do not form a stable cointegrating relationship when those demand structures change.

**Finding 5 — POSITIVE DIAGNOSTIC VALUE:**
The result is not a failure of the apparatus — it is the apparatus working correctly. The MA1 null correctly rejects F5 full-period (drift artifact) and barely catches F6 OOS (marginal autocorrelation). The apparatus discriminates between genuine stable MR (HO-CL, RB-CL) and regime-conditional-but-structurally-broken MR (GC-PL). This is exactly what a well-designed falsification apparatus should do.

---

## Verdict

```
VERDICT:          CONDITIONAL_CONFIRM (not a clean §11.7 non-energy confirmation)
F6:               FULL CONFIRM (p_ma1=0.040); OOS NO_CONFIRM (p_ma1=0.055 marginal miss)
F5:               OOS CONFIRM; FULL NO_CONFIRM (p_ma1=0.204, structural β-drift)
STRUCTURAL BREAK: ~2015-2016 — GC/PL ratio permanently inverted; mechanism is structural
                  (EV adoption → platinum demand collapse), not temporary regime
§11.7 STATUS:     NOT SATISFIED by GC-PL — cross-family swap + OOS marginal miss fails
                  the "stable cross-era confirmation" requirement
f_βupdate:        0.000 both — apparatus/construction clean; structural break is market reality
```

---

## Confidence Update

| Dimension | Prior | Posterior |
|---|---|---|
| Precious metals spread MR (general) | MEDIUM | **CONDITIONAL** — within-regime MR likely real, but cross-era cointegration structurally broken post-2015 |
| F6 admissibility on structural-break pairs | HIGH | **CAUTIONARY** — β=1 can confirm full-period when within-era MR exists but misses OOS when regime shifted; not a false positive of the apparatus, a true structural property |
| §11.7 non-energy cross-habitat gate | OPEN | **STILL OPEN** — GC-PL insufficient; need a pair with a stable physical production constraint |

---

## Next Actions

§11.7 gate remains open. The most promising remaining candidates from the folder survey:

1. **LE-GF (Live Cattle vs Feeder Cattle)**: feedlot margin = physical production constraint (feeder in, live out) analogous to refinery crack. β more stable. **RECOMMENDED NEXT.**
2. **KE-ZW (KC Wheat vs CBOT Wheat)**: geographic/quality basis, same commodity, tight spread. High-correlation risk (MA1 hard to beat), but cleanest data.
3. **HG-GC (Copper×400 vs Gold)**: Dr. Copper / monetary gold ratio — but same structural instability risk as GC-PL (competing demand drivers). Lower priority.

---

*Append-only. Run 2026-06-05 using same protocol as docs 39-40.*
