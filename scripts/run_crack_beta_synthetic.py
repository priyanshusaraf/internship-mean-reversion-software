"""
Track B — Crack-β Synthetic Calibration Gate.
Executes the synthetic controls (P, Z1, Z2, Z3) for each β family (F6, F5, F1, F3, F2).
SYNTHETIC DATA ONLY — no real HO2!/CL2! data touched.

Per crack_beta_execution_prereg.md §C:
  P (positive control): true OU pair → family must CONFIRM
  Z1 (martingale): true RW spread → must NULL, VR(20) ∈ [0.80, 1.20], f_βupdate < 0.10
  Z2 (stress null): strongly trending B → must NOT manufacture super-diffusion
  Z3 (independent): independent RWs → must NOT invent cointegration

Output: data/processed/crack_beta_synthetic_gate.json
        PASS/FAIL per family per cell, + admissibility verdict.
"""
from __future__ import annotations
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
import numpy as np
from app.services.analytics_arm_a_v2_beta import run_synthetic_calibration_gate, TAU_FUPDATE, NO_MFG_BAND

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
N_SYNTH = 5000
N_DRAWS = 200
SEED = 20260604


def print_family_summary(fname: str, fr: dict) -> None:
    print(f"\n  {fname}:")
    print(f"    Admissible: {'✓ YES' if fr['admissible'] else '✗ NO'}")
    print(f"    P (positive control confirms): {'PASS' if fr['P_pass'] else 'FAIL'}")
    print(f"    N (no manufacture on Z1/Z2/Z3): {'PASS' if fr['N_pass'] else 'FAIL'}")
    print(f"    M (f_βupdate < τ={TAU_FUPDATE}): {'PASS' if fr['M_pass'] else 'FAIL'}")
    for cname, cv in fr["per_control"].items():
        vr20 = cv.get("vr20", "n/a")
        p_rw = cv.get("p_rw", "n/a")
        f_bu = cv.get("f_betaupdate", "n/a")
        in_band = cv.get("vr20_in_band")
        band_str = f" [in_band={in_band}]" if in_band is not None else ""
        confirmed = cv.get("confirmed_rw_garch_ma1", False)
        vr20_s = f"{vr20:.4f}" if isinstance(vr20, float) else str(vr20)
        p_rw_s = f"{p_rw:.4f}" if isinstance(p_rw, float) else str(p_rw)
        f_bu_s = f"{f_bu:.4f}" if isinstance(f_bu, float) else str(f_bu)
        print(f"    {cname}: VR(20)={vr20_s}  p_rw={p_rw_s}  f_bu={f_bu_s}  confirmed={confirmed}{band_str}")


if __name__ == "__main__":
    np.seterr(all="ignore")
    print("=" * 80)
    print("Crack-β Synthetic Calibration Gate — doc 30 §2.2-2.3")
    print(f"n={N_SYNTH} bars, N_draws={N_DRAWS}, seed={SEED}")
    print(f"No-manufacture band: VR(20) ∈ {NO_MFG_BAND}, τ={TAU_FUPDATE}")
    print("=" * 80)
    print("\nRunning synthetic controls (5 families × 4 controls = 20 cells)...")

    results = run_synthetic_calibration_gate(n=N_SYNTH, n_draws=N_DRAWS, seed=SEED)

    print("\n" + "=" * 80)
    print("RESULTS PER FAMILY:")
    for fname, fr in results.items():
        print_family_summary(fname, fr)

    print("\n" + "=" * 80)
    print("ADMISSIBILITY SUMMARY:")
    admissible_families = []
    for fname, fr in results.items():
        status = "ADMISSIBLE" if fr["admissible"] else "INADMISSIBLE"
        print(f"  {fname}: {status}")
        if fr["admissible"]:
            admissible_families.append(fname)

    if admissible_families:
        print(f"\nFamilies cleared for real-data execution: {admissible_families}")
        gate_pass = True
    else:
        print("\nNO families cleared. ALL families inadmissible on synthetic controls.")
        gate_pass = False

    # Permanent demotion check: if every family fails P (cannot confirm positive control),
    # the issue is the apparatus, not the β families.
    p_passes = [fr["P_pass"] for fr in results.values()]
    if not any(p_passes):
        print("\nWARNING: ALL families fail P (positive control). May be apparatus issue, not β-family demotion.")
        gate_verdict = "APPARATUS_SUSPECT"
    elif not gate_pass:
        print("\nVERDICT: All admissible-in-principle families fail N∧M trilemma with P passing. PERMANENT DEMOTION triggered if no family clears.")
        gate_verdict = "PERMANENT_DEMOTION_CANDIDATE"
    else:
        gate_verdict = "CLEARED_FOR_REAL_DATA"

    print(f"\nGATE VERDICT: {gate_verdict}")

    out = {
        "meta": {
            "n_synth": N_SYNTH, "n_draws": N_DRAWS, "seed": SEED,
            "tau_fupdate": TAU_FUPDATE, "no_manufacture_band": list(NO_MFG_BAND),
            "families_tested": list(results.keys()),
            "controls_tested": ["P_positive_control","Z1_martingale","Z2_stress_null","Z3_independent"],
        },
        "gate_verdict": gate_verdict,
        "admissible_families": admissible_families,
        "per_family": results,
    }
    out_path = os.path.join(ROOT, "data", "processed", "crack_beta_synthetic_gate.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, allow_nan=True)
    print(f"\nResults written to: {out_path}")
