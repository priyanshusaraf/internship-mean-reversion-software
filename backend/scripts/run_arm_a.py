"""
Arm A — cohort execution runner (doc 18 + doc 18a, frozen). Constructs the 7 pre-registered spreads from
RAW LEGS (never the contaminated on-disk precomputes), evaluates real−surrogate VR(q), applies the ratified
(martingale-null, multiplicity-corrected) decision rule, and emits the execution log + timestamp proofs +
Habitat Discovery Results. Reports the literal all-three and naive readings alongside the headline.

Run:  cd backend && .venv/bin/python scripts/run_arm_a.py
"""
from __future__ import annotations

import json
import os
import sys
import warnings
from dataclasses import replace

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
warnings.filterwarnings("ignore"); np.seterr(all="ignore")

from app.services import analytics_arm_a as A  # noqa: E402
from app.services.analytics_substrate import directional_efficiency  # noqa: E402

DATA = os.path.expanduser("~/Downloads/mean-reversion-data")


def leg(fname: str) -> str:
    return os.path.join(DATA, fname)


# (name, legA_file, legB_file, beta_mode, continuous_a, continuous_b, date_min, drop_flat_a, drop_flat_b, role)
COHORT = [
    ("HDFC-ICICI",       "BSE_DLY_HDFCBANK, 1D.csv", "BSE_DLY_ICICIBANK, 1D.csv", "rolling", False, False, None,         False, False, "DECISIVE"),
    ("Gold-Silver",      "COMEX_DL_GC2!, 1D.csv",    "COMEX_DL_SI2!, 1D.csv",     "rolling", True,  True,  None,         False, False, "DECISIVE"),
    ("USDINR-calendar",  "CME_MINI_DL_MIR1!, 1D.csv","CME_MINI_DL_MIR2!, 1D.csv", "one",     True,  True,  None,         False, False, "reference"),
    ("Gold-Copper",      "COMEX_DL_GC2!, 1D.csv",    "COMEX_DL_HG1!, 1D.csv",     "rolling", True,  True,  None,         False, False, "cohort"),
    ("Platinum-Palladium","TVC_PLATINUM, 1D.csv",    "NYMEX_DL_PA1!, 1D.csv",     "rolling", False, True,  None,         True,  False, "cohort"),
    ("WTI-Brent",        "CFI_WTI, 1D.csv",          "ICEEUR_DLY_BRN1!, 1D.csv",  "rolling", False, True,  "2011-01-01", False, False, "cohort"),
    ("TCS-INFY",         "BSE_DLY_TCS, 1D.csv",      "NSE_DLY_INFY, 1D.csv",      "rolling", False, False, None,         False, False, "cohort"),
]


def timestamp_proof(name, la, lb, beta_mode, ca, cb, dmin, fa, fb) -> bool:
    """C-3 acceptance test: detonate a FUTURE leg bar; assert the spread/β at all earlier bars is
    bit-identical. Returns True iff the construction is provably causal on this real spread."""
    base = A.construct_spread(name, A.load_leg(la), A.load_leg(lb), beta_mode=beta_mode,
                              continuous_a=ca, continuous_b=cb, date_min=dmin, drop_flat_a=fa, drop_flat_b=fb)
    da = A.load_leg(la).copy(); db = A.load_leg(lb).copy()
    k = int(len(base) * 0.6)
    fut = base.index[min(len(base) - 1, k + 30)]                 # a future timestamp
    da.loc[da.index >= fut, ["open", "close"]] *= -7.0
    da.loc[da.index >= fut, ["open", "close"]] += 12345.0
    db.loc[db.index >= fut, ["open", "close"]] += 999.0
    pert = A.construct_spread(name, da, db, beta_mode=beta_mode, continuous_a=ca, continuous_b=cb,
                              date_min=dmin, drop_flat_a=fa, drop_flat_b=fb)
    m = min(len(base), len(pert), k + 1)
    bclose = np.nan_to_num(base.s_close[:m], nan=-123.456)
    pclose = np.nan_to_num(pert.s_close[:m], nan=-123.456)
    bbeta = np.nan_to_num(base.beta[:m], nan=-123.456)
    pbeta = np.nan_to_num(pert.beta[:m], nan=-123.456)
    return bool(np.array_equal(bclose, pclose) and np.array_equal(bbeta, pbeta))


def run() -> dict:
    results = []
    for (name, la, lb, bm, ca, cb, dmin, fa, fb, role) in COHORT:
        sp = A.construct_spread(name, A.load_leg(leg(la)), A.load_leg(leg(lb)), beta_mode=bm,
                                continuous_a=ca, continuous_b=cb, date_min=dmin,
                                drop_flat_a=fa, drop_flat_b=fb)
        v = A.evaluate_spread(sp, seed=20260603)                  # headline (roll-clean)
        # robustness subsample: also trim flat (O=H=L=C) bars
        sp_ft = replace(sp, roll_transition=(sp.roll_transition | sp.flat_bar))
        v_ft = A.evaluate_spread(sp_ft, seed=20260603)
        # non-verdict robustness display: W=120
        if bm == "rolling":
            sp120 = A.construct_spread(name, A.load_leg(leg(la)), A.load_leg(leg(lb)), beta_mode=bm,
                                       window=A.ROLL_BETA_W_ROBUST, continuous_a=ca, continuous_b=cb,
                                       date_min=dmin, drop_flat_a=fa, drop_flat_b=fb)
            v120 = A.evaluate_spread(sp120, seed=20260603)
            vr120 = v120.real_vr
            conf120 = v120.confirmed_martingale
        else:
            vr120, conf120 = None, None

        invalid = sp.roll_transition | ~np.isfinite(sp.beta)
        clean_close = sp.s_close[np.isfinite(sp.s_close) & ~invalid]
        de = directional_efficiency(clean_close) if len(clean_close) > 2 else float("nan")
        robust = bool(v.confirmed_martingale and v_ft.confirmed_martingale)

        rec = {
            "name": name, "role": role, "beta_mode": bm,
            "legs": [la.split(",")[0], lb.split(",")[0]],
            "n_joined": sp.meta["n_joined"], "date_start": sp.meta["date_start"],
            "date_end": sp.meta["date_end"], "n_roll_masked": sp.meta["n_roll_masked"],
            "n_flat": sp.meta["n_flat"],
            "beta_median": float(np.nanmedian(sp.beta)), "beta_iqr": float(
                np.nanpercentile(sp.beta, 75) - np.nanpercentile(sp.beta, 25)),
            "spread_dir_eff": float(de),
            "real_vr": {q: round(v.real_vr[q], 4) for q in A.VR_Q_GRID},
            "real_min_vr": round(v.meta["real_min_vr"], 4),
            "real_z": {q: (round(v.real_z[q], 2) if np.isfinite(v.real_z[q]) else None) for q in A.VR_Q_GRID},
            "surr_p5": {fam: {q: round(v.per_family[fam]["per_horizon"][q]["p5"], 4) for q in A.VR_Q_GRID}
                        for fam in A.SURR_FAMILIES},
            "min_vr_p_value": {fam: round(v.per_family[fam]["min_vr_p_value"], 4) for fam in A.SURR_FAMILIES},
            "separated_corrected": {fam: v.per_family[fam]["separated_corrected"] for fam in A.SURR_FAMILIES},
            "HEADLINE_confirmed_martingale": v.confirmed_martingale,
            "confirmed_all_three": v.confirmed_all_three,
            "naive_martingale_horizons": v.separated_horizons["MARTINGALE_naive"],
            "flat_trim_confirmed": v_ft.confirmed_martingale,
            "robust_confirmed": robust,
            "W120_real_vr": ({q: round(vr120[q], 4) for q in A.VR_Q_GRID} if vr120 else None),
            "W120_confirmed": conf120,
            "timestamp_proof_causal": timestamp_proof(name, leg(la), leg(lb), bm, ca, cb, dmin, fa, fb),
        }
        results.append(rec)
        print(f"[{name:18s} {role:9s}] n={rec['n_joined']:5d} {rec['date_start']}..{rec['date_end']} "
              f"roll_masked={rec['n_roll_masked']:3d} flat={rec['n_flat']:4d} β~{rec['beta_median']:.3f} "
              f"DE={rec['spread_dir_eff']:.3f}")
        print(f"    VR(q)={rec['real_vr']}  min={rec['real_min_vr']}")
        print(f"    min-VR p: RW={rec['min_vr_p_value']['rw']} GARCH={rec['min_vr_p_value']['garch']} "
              f"OU={rec['min_vr_p_value']['ou']}")
        print(f"    HEADLINE confirmed(martingale,corrected)={v.confirmed_martingale}  robust(+flat-trim)={robust}"
              f"  all_three={v.confirmed_all_three}  naive_horizons={rec['naive_martingale_horizons']}"
              f"  causal_proof={rec['timestamp_proof_causal']}")
        print()

    decisive = [r for r in results if r["role"] == "DECISIVE"]
    any_conf = [r for r in results if r["robust_confirmed"]]
    summary = {
        "frozen_refs": ["doc 18", "doc 18a"], "seed": 20260603,
        "decision_rule": "martingale-null (RW & GARCH), multiplicity-corrected min-VR, 5th pct, robust roll-clean+flat-trim",
        "n_spreads": len(results),
        "n_robust_confirmed": len(any_conf),
        "robust_confirmed_names": [r["name"] for r in any_conf],
        "decisive_confirmed": {r["name"]: r["robust_confirmed"] for r in decisive},
        "KILL_triggered": len(any_conf) == 0,
        "decisive_both_fail": all(not r["robust_confirmed"] for r in decisive),
        "all_causal_proofs_pass": all(r["timestamp_proof_causal"] for r in results),
        "results": results,
    }
    os.makedirs("../data/processed", exist_ok=True)
    with open("../data/processed/arm_a_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("=" * 100)
    print(f"COHORT: {len(results)} spreads | robust-CONFIRMED: {len(any_conf)} {summary['robust_confirmed_names']}")
    print(f"DECISIVE: {summary['decisive_confirmed']}")
    print(f"KILL_triggered={summary['KILL_triggered']}  decisive_both_fail={summary['decisive_both_fail']}  "
          f"all_causal_proofs_pass={summary['all_causal_proofs_pass']}")
    print("→ wrote data/processed/arm_a_results.json")
    return summary


if __name__ == "__main__":
    run()
