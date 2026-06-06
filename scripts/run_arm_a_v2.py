"""
Arm A v2 — Cycle 1 runner. Executes doc 20 EXACTLY:
  PART A — §5a SYNTHETIC CALIBRATION GATE (must pass before the real verdict is credible).
  PART B — formal cohort execution (NG primary · RB reference · WTI-Brent context), full matrix + ablations.

Run: backend/.venv/bin/python scripts/run_arm_a_v2.py
"""
from __future__ import annotations
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
import numpy as np
import pandas as pd
from app.services.analytics_arm_a import Spread, level_vr, VR_Q_GRID
from app.services.analytics_arm_a_v2 import (
    spread_from_series, evaluate_v2, deseasonalize_causal, increment_jump_mask,
    SEED, JUMP_K_SWEEP, JUMP_W,
)
from app.services.analytics_arm_a import load_leg

NG_TRIM = "2006-07-28"        # frozen dense-era start (doc 20 §4; deterministic gap+nonfinite rule)


def _synth_spread(name, s_close, start="2005-01-03"):
    idx = pd.date_range(start, periods=len(s_close), freq="B", tz="UTC")
    s = np.asarray(s_close, float)
    return Spread(name=name, s_close=s, s_open=s.copy(), beta=np.ones(len(s)),
                  roll_transition=np.zeros(len(s), bool), flat_bar=np.zeros(len(s), bool),
                  index=idx, meta={"synthetic": True})


def gen_seasonal_ou(n, phi=0.9, sig=0.05, amp=0.30, period=252, seed=1):
    rng = np.random.default_rng(seed)
    x = np.empty(n); x[0] = 0.0
    e = rng.normal(0, sig, n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + e[t]
    seas = amp * np.sin(2 * np.pi * np.arange(n) / period)
    return x + seas


def gen_rw(n, sig=0.05, seed=1):
    rng = np.random.default_rng(seed)
    return np.concatenate([[0.0], np.cumsum(rng.normal(0, sig, n - 1))])


def gen_rw_plus_noise(n, sig_w=0.02, sig_eta=0.05, seed=1):
    """Latent martingale + i.i.d. observation noise (bid-ask bounce). NO mean reversion; strong negative
    increment ACF(1). RW/GARCH should SPURIOUSLY confirm; the MA(1) null must CATCH it."""
    rng = np.random.default_rng(seed)
    w = np.concatenate([[0.0], np.cumsum(rng.normal(0, sig_w, n - 1))])
    eta = rng.normal(0, sig_eta, n)
    return w + eta


def calibration_gate():
    print("=" * 100); print("PART A — §5a SYNTHETIC CALIBRATION GATE"); print("=" * 100)
    results = {}; passed = {}

    # (1) true seasonal-OU calendar → must CONFIRM (power)
    sp = _synth_spread("synth_seasonal_OU", gen_seasonal_ou(4969, seed=11))
    r = evaluate_v2(sp, seed=SEED)
    passed["1_seasonal_OU_confirms"] = bool(r["confirmed_gate_rw_garch_ma1"])
    results["seasonal_OU"] = {"VR": r["real_vr"], "gate": r["confirmed_gate_rw_garch_ma1"],
                              "p": {f: r["per_family"][f]["min_vr_p_value"] for f in ("rw", "garch", "ma1", "ou")}}
    print(f"(1) seasonal-OU: gate(rw∧garch∧ma1)={r['confirmed_gate_rw_garch_ma1']}  "
          f"p_rw={r['per_family']['rw']['min_vr_p_value']:.3f} p_garch={r['per_family']['garch']['min_vr_p_value']:.3f} "
          f"p_ma1={r['per_family']['ma1']['min_vr_p_value']:.3f}  EXPECT confirm → {'PASS' if passed['1_seasonal_OU_confirms'] else 'FAIL'}")

    # (2) true RW calendar → must NULL; FPR across seeds
    confs = []
    for sd in range(20):
        spr = _synth_spread(f"synth_RW_{sd}", gen_rw(4969, seed=100 + sd))
        confs.append(bool(evaluate_v2(spr, seed=SEED)["confirmed_gate_rw_garch_ma1"]))
    fpr = float(np.mean(confs))
    passed["2_RW_FPR_ok"] = bool(fpr <= 0.10)
    results["RW_FPR"] = {"fpr": fpr, "n": len(confs)}
    print(f"(2) RW calendar FPR over {len(confs)} seeds = {fpr:.3f}  EXPECT ≤0.10 → {'PASS' if passed['2_RW_FPR_ok'] else 'FAIL'}")

    # (3) RW + i.i.d. noise → RW/GARCH spurious-confirm but MA(1) catches it
    sp = _synth_spread("synth_RW_plus_noise", gen_rw_plus_noise(4969, seed=7))
    r = evaluate_v2(sp, seed=SEED)
    passed["3_ma1_catches_noise"] = bool(r["confirmed_rw_garch_only"] and not r["separated"]["ma1"])
    results["RW_plus_noise"] = {"VR": r["real_vr"], "sep": r["separated"],
                                "rw_garch_only": r["confirmed_rw_garch_only"], "gate": r["confirmed_gate_rw_garch_ma1"],
                                "ma1_fit": r["ma1_fit"]}
    print(f"(3) RW+noise: sep={r['separated']}  rw_garch_only_confirm={r['confirmed_rw_garch_only']}  "
          f"FULL gate={r['confirmed_gate_rw_garch_ma1']}  ma1_rho={r['ma1_fit']['rho']:.3f}  "
          f"EXPECT rw/garch confirm BUT ma1 kills → {'PASS' if passed['3_ma1_catches_noise'] else 'FAIL'}")

    # (4) no-seam no-op: jump filter at k=8 must not move VR on a clean OU
    s = gen_seasonal_ou(4969, amp=0.0, seed=21)   # pure OU, no seasonality, no seams
    invalid_none = np.zeros(len(s), bool)
    invalid_k8 = increment_jump_mask(s, k=8.0, window=JUMP_W)
    vr_none = level_vr(s, invalid_none, VR_Q_GRID)[20]["vr"]
    vr_k8 = level_vr(s, invalid_k8, VR_Q_GRID)[20]["vr"]
    shift = abs(vr_k8 - vr_none)
    passed["4_noseam_noop"] = bool(shift < 0.05)
    results["noop"] = {"vr20_unmasked": vr_none, "vr20_k8": vr_k8, "shift": shift, "n_masked": int(invalid_k8.sum())}
    print(f"(4) no-seam no-op: VR20 unmasked={vr_none:.3f} k8={vr_k8:.3f} shift={shift:.3f} "
          f"masked={int(invalid_k8.sum())}  EXPECT shift<0.05 → {'PASS' if passed['4_noseam_noop'] else 'FAIL'}")

    all_pass = all(passed.values())
    print(f"\nCALIBRATION GATE: {'ALL PASS ✓' if all_pass else 'FAIL ✗ — real verdict NOT credible'}  {passed}")
    return all_pass, {"passed": passed, "detail": results}


def open_close_check(sp):
    inv = sp.roll_transition | ~np.isfinite(sp.beta)
    vc = level_vr(sp.s_close, inv, VR_Q_GRID)
    vo = level_vr(sp.s_open, inv, VR_Q_GRID)
    return {q: {"close": vc[q]["vr"], "open": vo[q]["vr"]} for q in VR_Q_GRID}


def run_real():
    print("\n" + "=" * 100); print("PART B — FORMAL COHORT EXECUTION (doc 20 §3)"); print("=" * 100)
    out = {}

    # ── NG primary (dense-era trim, UNMASKED headline) ──
    ng_df = load_leg("data/raw/ng12_spread.csv")
    ng = spread_from_series("NG_calendar", ng_df, date_min=NG_TRIM, jump_k=float("inf"))
    ng_v = evaluate_v2(ng, seed=SEED)
    # deseasonalized companion (must survive)
    ng_des = Spread(name="NG_calendar_deseason", s_close=deseasonalize_causal(ng.s_close, ng.index),
                    s_open=deseasonalize_causal(ng.s_open, ng.index), beta=np.ones(len(ng)),
                    roll_transition=ng.roll_transition, flat_bar=ng.flat_bar, index=ng.index, meta=ng.meta)
    ng_des_v = evaluate_v2(ng_des, seed=SEED)
    # k-ablation sweep (reported, NEVER headline)
    ablation = {}
    for k in JUMP_K_SWEEP:
        spk = spread_from_series("NG_abl", ng_df, date_min=NG_TRIM, jump_k=k)
        rv = level_vr(spk.s_close, spk.roll_transition | ~np.isfinite(spk.beta), VR_Q_GRID)
        ablation[("inf" if k == float("inf") else int(k))] = {"VR": {q: rv[q]["vr"] for q in VR_Q_GRID},
                                                              "n_masked": int(spk.roll_transition.sum())}
    out["NG_primary"] = {"headline_unmasked": ng_v, "deseasonalized": ng_des_v,
                         "open_close": open_close_check(ng), "k_ablation": ablation,
                         "deseason_survives": bool(ng_des_v["confirmed_gate_rw_garch_ma1"])}

    # ── RB reference (expect NULL at q≤20; descriptive long-horizon read) ──
    rb_df = load_leg("data/raw/rb23_spread.csv")
    rb = spread_from_series("RB_calendar", rb_df, jump_k=float("inf"))
    rb_v = evaluate_v2(rb, seed=SEED)
    rb_long = evaluate_v2(rb, qs=(40, 60, 120), seed=SEED)         # non-verdict descriptive
    out["RB_reference"] = {"q_le_20": rb_v, "q_long_descriptive": {"VR": rb_long["real_vr"],
                           "p_rw": rb_long["per_family"]["rw"]["min_vr_p_value"],
                           "gate": rb_long["confirmed_gate_rw_garch_ma1"]}}

    # ── WTI-Brent context (hourly) ──
    try:
        wb_df = load_leg("data/raw/cl_brn_spread_60.csv")
        wb = spread_from_series("WTI_Brent_60m", wb_df, jump_k=float("inf"))
        wb_v = evaluate_v2(wb, seed=SEED)
        out["WTI_Brent_context"] = wb_v
    except Exception as e:
        out["WTI_Brent_context"] = {"ERROR": repr(e)}

    return out


def _fmt(v):  # pretty VR dict
    return ", ".join(f"q{q}={v[q]:.3f}" for q in v)


if __name__ == "__main__":
    np.seterr(all="ignore")
    gate_pass, gate = calibration_gate()
    real = run_real()

    print("\n" + "=" * 100); print("FORMAL VERDICT MATRIX (real − surrogate; multiplicity-corrected min-VR p)"); print("=" * 100)
    ng = real["NG_primary"]["headline_unmasked"]; ngd = real["NG_primary"]["deseasonalized"]
    rb = real["RB_reference"]["q_le_20"]
    print(f"NG (UNMASKED headline): VR[{_fmt(ng['real_vr'])}] min={ng['real_min_vr']:.3f}")
    print(f"   p_rw={ng['per_family']['rw']['min_vr_p_value']:.3f} p_garch={ng['per_family']['garch']['min_vr_p_value']:.3f} "
          f"p_ma1={ng['per_family']['ma1']['min_vr_p_value']:.3f} p_ou={ng['per_family']['ou']['min_vr_p_value']:.3f}  "
          f"GATE(rw∧garch∧ma1)={ng['confirmed_gate_rw_garch_ma1']}  (rw∧garch only={ng['confirmed_rw_garch_only']}, ma1_adds_kill={ng['ma1_adds_kill']})")
    print(f"NG deseasonalized: VR[{_fmt(ngd['real_vr'])}] min={ngd['real_min_vr']:.3f}  GATE={ngd['confirmed_gate_rw_garch_ma1']}  "
          f"p_rw={ngd['per_family']['rw']['min_vr_p_value']:.3f} p_ma1={ngd['per_family']['ma1']['min_vr_p_value']:.3f}  → SURVIVES={real['NG_primary']['deseason_survives']}")
    print(f"NG open/close: " + " | ".join(f"q{q}: c={real['NG_primary']['open_close'][q]['close']:.3f}/o={real['NG_primary']['open_close'][q]['open']:.3f}" for q in (2,5,10,20)))
    print(f"NG k-ablation VR(20): " + ", ".join(f"k={k}:{real['NG_primary']['k_ablation'][k]['VR'][20]:.3f}(m={real['NG_primary']['k_ablation'][k]['n_masked']})" for k in real['NG_primary']['k_ablation']))
    print(f"RB (reference, q≤20): VR[{_fmt(rb['real_vr'])}] min={rb['real_min_vr']:.3f} p_rw={rb['per_family']['rw']['min_vr_p_value']:.3f}  GATE={rb['confirmed_gate_rw_garch_ma1']}  (EXPECT null)")
    print(f"RB long-horizon (descriptive): VR[{_fmt(real['RB_reference']['q_long_descriptive']['VR'])}] p_rw={real['RB_reference']['q_long_descriptive']['p_rw']:.3f}")
    wb = real["WTI_Brent_context"]
    if "real_vr" in wb:
        print(f"WTI-Brent (context, hourly): VR[{_fmt(wb['real_vr'])}] min={wb['real_min_vr']:.3f} GATE={wb['confirmed_gate_rw_garch_ma1']} p_rw={wb['per_family']['rw']['min_vr_p_value']:.3f} p_ma1={wb['per_family']['ma1']['min_vr_p_value']:.3f}")

    blob = {"calibration_gate_pass": gate_pass, "calibration": gate, "cohort": real,
            "frozen": {"seed": SEED, "q_grid": list(VR_Q_GRID), "gate": "rw_and_garch_and_ma1",
                       "ng_trim": NG_TRIM}}
    with open("data/processed/arm_a_v2_results.json", "w") as f:
        json.dump(blob, f, indent=2, default=lambda x: None if (isinstance(x, float) and not np.isfinite(x)) else float(x) if isinstance(x, np.floating) else x)
    print("\nwrote data/processed/arm_a_v2_results.json")
