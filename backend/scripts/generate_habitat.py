"""
State T Native-Habitat Substrate — OU_IN_TREND materialization + blind packet (FROZEN spec).

WHY THIS EXISTS (Rank-1 illusion audit, 2026-06-01). The #11 null set tested OU-around-a-FLAT
level (ANCHOR_OU) and unit-root trends (NULL_RW / NULL_DRIFT) — but never genuine OU reversion
around a genuinely MOVING equilibrium, which is literally State T's target environment. This
script adds that one missing substrate so the EXACT #11 blind protocol (REP / CMP / RES,
metric-free, sealed key) can be re-run in State T's native habitat, answering one gate:

    Can a disciplined researcher separate genuine reversion ignition from mu*-catch-up illusion
    when the equilibrium itself is moving?

SCOPE — this script ONLY materializes an already-existing generator and seals a blind packet.
No detector, no MRScore, no scoring, no new endpoint/frontend/observatory surface, no generator
redesign, no parameter tuning. Strong reuse: it imports #11's own helpers and window constants
from generate_nulls.py and does NOT modify that frozen script or its sealed blind_key.json.

PARAMETERIZATION (no tuning — every value reused from #11 conventions; see generate_nulls.py):
  lam   = ANCHOR_LAM (-0.05)  -> IDENTICAL reversion to ANCHOR_OU; isolates "added trend" as the
                                 only difference vs the flat-equilibrium reverter.
  sigma = sigma_abs           -> IDENTICAL noise scale to every #11 synthetic; no scale tell.
  slope = mu_abs              -> IDENTICAL per-bar drift to NULL_DRIFT; OU_IN_TREND and the drifted
                                 RWs trend the SAME direction, so "it goes up" reveals nothing and
                                 the researcher must use EQUILIBRIUM STABILITY to find the genuine
                                 reverter. This is the crux of the mu*-catch-up test.
  n/base/dates                -> same 600-bar scale-stationary ADANIENT window as #11.

OU_IN_TREND is thus the exact crossbreed of ANCHOR_OU (reversion) and NULL_DRIFT (drift).

BLIND PACKET (mirrors #11 F4 exactly): fresh independent seeds, shuffled by a new master seed,
sealed to data/blind_key_habitat.json (SEPARATE from the #11 seal). Pool of 5: OU_IN_TREND,
ANCHOR_OU, NULL_RW, NULL_DRIFT, + a second NULL_DRIFT (different seed) to defeat "one-of-each"
and force genuine OU_IN_TREND-vs-drifted-RW discrimination. Classify each via REP/RES/CMP BEFORE
opening the key. "Residual reverts on a random walk" is EXPECTED mechanics, NOT a kill — the test
is DISCRIMINATION. Idempotent (INSERT OR REPLACE); ids clearly prefixed and removable.

Run:  backend/.venv/bin/python backend/scripts/generate_habitat.py
"""
from __future__ import annotations

import json
import os
import sys

# backend/ on path (for app.services) and scripts/ on path (to reuse generate_nulls helpers)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import duckdb  # noqa: E402
import numpy as np  # noqa: E402

from app.services import synthetic, store  # noqa: E402
# Reuse #11's frozen helpers + window/scale constants verbatim — do NOT modify generate_nulls.py.
from generate_nulls import (  # noqa: E402
    _positive, _series_to_ohlcv, DB, REF, WIN_START, WIN_LEN, ANCHOR_LAM,
)

KEY_PATH = os.path.join(os.path.dirname(DB), "blind_key_habitat.json")
HABITAT_MASTER_SEED = 20260602   # distinct from #11's 20260601 (independent shuffle)


def main() -> None:
    conn = duckdb.connect(DB)
    store._init_schema(conn)

    ref = conn.execute(
        "SELECT date, close FROM ohlcv WHERE instrument_id = ? ORDER BY date", [REF]
    ).df()
    if ref.empty:
        raise SystemExit(f"Reference instrument {REF!r} not found in {DB}")

    seg = ref.iloc[WIN_START:WIN_START + WIN_LEN].reset_index(drop=True)
    dates = seg["date"]
    close = seg["close"].to_numpy(float)
    n = len(close)
    base = float(close[0])

    rets = np.diff(close) / close[:-1]
    sigma_abs = float(np.std(rets)) * base    # IDENTICAL scale to #11
    mu_abs = float(np.mean(rets)) * base      # IDENTICAL drift to NULL_DRIFT

    print(f"[window] {REF}[{WIN_START}:{WIN_START + n}]  {dates.iloc[0].date()}..{dates.iloc[-1].date()}  "
          f"n={n}  base={base:.2f}  sigma_abs={sigma_abs:.4f}  mu_abs={mu_abs:.4f}  lam={ANCHOR_LAM}")

    def register(instrument_id: str, display_name: str, prices: np.ndarray, *, quiet=False) -> None:
        store.store_instrument(conn, instrument_id, display_name,
                               _series_to_ohlcv(prices, dates), f"synthetic://{instrument_id}")
        if quiet:
            print(f"  registered {instrument_id:12s} n={len(prices)}  (sealed)")
        else:
            print(f"  registered {instrument_id:12s} n={len(prices)}  price {prices.min():.1f}..{prices.max():.1f}")

    # ---- LABELED substrate (open inspection): the missing native-habitat case ----
    print("\n[labeled] OU_IN_TREND (genuine OU reversion around a moving equilibrium):")
    h0, hs = _positive(synthetic.ou_in_trend, 14,
                       lam=ANCHOR_LAM, sigma=sigma_abs, slope=mu_abs, n=n, base=base)
    register("OU_IN_TREND",
             f"H0 OU reversion around linear trend - State T native habitat (seed {hs})", h0.prices)

    # ---- BLIND packet (fresh seeds, distinct from #11; ambiguity under discipline) ----
    print("\n[blind] 5-instrument habitat blind packet (fresh seeds, same window):")
    bh0, bh0s = _positive(synthetic.ou_in_trend, 201,
                          lam=ANCHOR_LAM, sigma=sigma_abs, slope=mu_abs, n=n, base=base)
    ba0, ba0s = _positive(synthetic.ou, 202, lam=ANCHOR_LAM, sigma=sigma_abs, n=n, base=base)
    bn1, bn1s = _positive(synthetic.random_walk, 203, sigma=sigma_abs, n=n, base=base)
    bd1, bd1s = _positive(synthetic.drift_random_walk, 204, mu=mu_abs, sigma=sigma_abs, n=n, base=base)
    bd2, bd2s = _positive(synthetic.drift_random_walk, 205, mu=mu_abs, sigma=sigma_abs, n=n, base=base)
    pool = [
        (f"H0_ou_in_trend_seed{bh0s}", bh0.prices,
         "OU reversion around a MOVING equilibrium - genuine reversion (State T native habitat)"),
        (f"A0_ou_seed{ba0s}", ba0.prices,
         "OU around a FLAT level - genuine reversion (flat-equilibrium contrast)"),
        (f"N1_rw_seed{bn1s}", bn1.prices,
         "pure random walk - non-reverting (mechanical residual only)"),
        (f"N2_drift_seed{bd1s}", bd1.prices,
         "drifted random walk - non-reverting (trend-lag / mu*-catch-up only)"),
        (f"N2b_drift_seed{bd2s}", bd2.prices,
         "drifted random walk (duplicate non-reverting trend; defeats one-of-each)"),
    ]
    rng = np.random.default_rng(HABITAT_MASTER_SEED)
    order = rng.permutation(len(pool))
    mapping, ground_truth = {}, {}
    for slot, idx in enumerate(order, start=1):
        hid = f"HABITAT_{slot}"
        truth_id, prices, desc = pool[idx]
        register(hid, f"habitat blind packet #{slot}", prices, quiet=True)
        mapping[hid] = truth_id
        ground_truth[truth_id] = desc

    key = {
        "_DO_NOT_OPEN_UNTIL": "you have classified every HABITAT_* instrument as "
                              "reverting / non-reverting / uncertain using ONLY REP, RES, CMP, "
                              "asking 'did the equilibrium stay put?' (NOT 'did price come back?').",
        "protocol": "State T native-habitat blind adjudication (Rank-1 mu*-catch-up gate). Mirrors "
                    "#11 F4 exactly: metric-free, REP-first, sealed. The decisive case is whether "
                    "OU_IN_TREND (genuine reversion around a moving equilibrium) is separable from "
                    "the drifted random walks (mu*-catch-up theater). 'Residual reverts on a RW' is "
                    "EXPECTED mechanics, NOT a kill. The test is DISCRIMINATION.",
        "window": {"ref": REF, "start": WIN_START, "len": n,
                   "dates": f"{dates.iloc[0].date()}..{dates.iloc[-1].date()}"},
        "scale": {"base": base, "sigma_abs": sigma_abs, "mu_abs": mu_abs, "lam": ANCHOR_LAM},
        "positivity_filter": "null/synthetic seeds chosen as lowest >= base with min price >= "
                             "POS_FLOOR (realism constraint, orthogonal to reversion).",
        "mapping": mapping,
        "ground_truth": ground_truth,
        "master_seed": HABITAT_MASTER_SEED,
        "note": "SEPARATE from #11's blind_key.json; #11 BLIND_* packet untouched.",
    }
    with open(KEY_PATH, "w") as f:
        json.dump(key, f, indent=2)

    conn.close()
    print(f"\n[blind] sealed mapping -> {KEY_PATH}  (mapping NOT printed)")
    print("[done] Inspect via REP / CMP / RES as ordinary instruments.")
    print("       Labeled: OU_IN_TREND.  Blind: HABITAT_1..HABITAT_5.")


if __name__ == "__main__":
    main()
