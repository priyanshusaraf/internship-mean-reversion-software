"""
#11 Synthetic Null Testing — null materialization & registration (FROZEN spec).

Generates the minimal frozen null set, scale-matched to a SCALE-STATIONARY WINDOW of ADANIENT,
and registers each as an ORDINARY instrument in the live DuckDB so it flows through the existing
observatory (/diagnostics -> REP / RES / CMP) with ZERO new endpoints and ZERO new frontend.

Frozen null set (only):
  N1  NULL_RW      pure random walk          P_t = P_{t-1} + eps_t            (no reversion)
  N2  NULL_DRIFT   drifted random walk       P_t = P_{t-1} + mu + eps_t       (no reversion)
  A0  ANCHOR_OU    OU / AR(1) positive anchor (genuine reversion — NOT a null; the F1 contrast)

HARDENED BLIND PROTOCOL (frozen): 5 opaque close-only instruments BLIND_1..BLIND_5 (real ADANIENT
segment + N1 + N2 + A0 + an extra null, fresh independent seeds, shuffled), identity mapping SEALED
in data/blind_key.json. Classify each via REP/RES/CMP BEFORE opening it.

WHY A WINDOW (decision 2026-06-01): the frozen arithmetic RW (P_t=P_{t-1}+eps_t) with constant
absolute sigma cannot be scale-matched to ADANIENT's FULL history — its volatility is multiplicative
(100x ramp), so full-history constant-sigma nulls go negative and stay tiny while the real series
reaches 3800, making the blind separable by scale/sign alone (an invalid confound). Restricting to a
~600-bar scale-stationary segment (max/min ~2.6x) keeps the frozen arithmetic form (n was never
frozen) and lets the real segment blend with the synthetics.

POSITIVITY FILTER (disclosed): even in-window, 3.1%/bar vol gives terminal RW dispersion ~0.76*base,
so a driftless arithmetic RW can still dip below zero (an obvious 'synthetic' tell). We therefore
select the lowest seed whose realized path stays strictly positive. Selecting on POSITIVITY is a
realism constraint orthogonal to reversion dynamics — it does NOT bias the discrimination question.
The chosen seed is recorded.

NO variance-ratio / threshold / metric surface is produced (frozen modification): nulls are correct
BY CONSTRUCTION; discrimination is REP-first, visual, blind. Idempotent (INSERT OR REPLACE); ids are
clearly prefixed and removable.

Run:  backend/.venv/bin/python backend/scripts/generate_nulls.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import duckdb  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from app.services import synthetic, store  # noqa: E402

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "amr.duckdb")
KEY_PATH = os.path.join(os.path.dirname(DB), "blind_key.json")

REF = "ADANIENT"          # scale + date reference
WIN_START = 650           # scale-stationary segment (2015-06 .. 2017-11, max/min ~2.6x)
WIN_LEN = 600
ANCHOR_LAM = -0.05        # OU reversion for A0: slow/realistic -> adversarial (not trivially distinct)
POS_FLOOR = 0.5           # strictly-positive realism floor for null paths
MAX_SEED_TRIES = 200
BLIND_MASTER_SEED = 20260601


def _series_to_ohlcv(prices: np.ndarray, dates: pd.Series) -> pd.DataFrame:
    """Close-only OHLCV frame on the reference dates. O=H=L=C (no fabricated intraday range);
    the observatory consumes close only. Indexed by date, as store_instrument expects."""
    return pd.DataFrame(
        {"open": prices, "high": prices, "low": prices, "close": prices, "volume": 0.0},
        index=pd.DatetimeIndex(dates, name="date"),
    )


def _positive(gen, base_seed: int, **kw):
    """Lowest seed >= base_seed whose realized path stays strictly positive (>= POS_FLOOR).
    Disclosed realism filter; orthogonal to reversion dynamics. Returns (series, seed)."""
    for s in range(base_seed, base_seed + MAX_SEED_TRIES):
        ser = gen(seed=s, **kw)
        if ser.prices.min() >= POS_FLOOR:
            return ser, s
    raise SystemExit(f"no positive path for {gen.__name__} within {MAX_SEED_TRIES} seeds "
                     f"(vol too high for window) — shorten WIN_LEN")


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
    sigma_ret = float(np.std(rets))
    rbar = float(np.mean(rets))
    sigma_abs = sigma_ret * base
    mu_abs = rbar * base

    print(f"[window] {REF}[{WIN_START}:{WIN_START + n}]  {dates.iloc[0].date()}..{dates.iloc[-1].date()}  "
          f"n={n}  price {close.min():.1f}..{close.max():.1f}  (max/min={close.max()/close.min():.2f}x)")
    print(f"[scale]  base={base:.2f} sigma_ret={sigma_ret:.5f} rbar={rbar:.6f} "
          f"-> sigma_abs={sigma_abs:.4f} mu_abs={mu_abs:.4f}")

    def register(instrument_id: str, display_name: str, prices: np.ndarray) -> None:
        store.store_instrument(conn, instrument_id, display_name,
                               _series_to_ohlcv(prices, dates), f"synthetic://{instrument_id}")
        print(f"  registered {instrument_id:14s} n={len(prices)} "
              f"price {prices.min():.1f}..{prices.max():.1f}")

    # ---- LABELED set (open study) ----
    print("\n[labeled] N1 / N2 / A0 (scale-matched to window, positivity-filtered):")
    n1, s1 = _positive(synthetic.random_walk, 11, sigma=sigma_abs, n=n, base=base)
    n2, s2 = _positive(synthetic.drift_random_walk, 12, mu=mu_abs, sigma=sigma_abs, n=n, base=base)
    a0, s3 = _positive(synthetic.ou, 13, lam=ANCHOR_LAM, sigma=sigma_abs, n=n, base=base)
    register("NULL_RW", f"N1 pure random walk - no reversion (seed {s1})", n1.prices)
    register("NULL_DRIFT", f"N2 drifted random walk - no reversion (seed {s2})", n2.prices)
    register("ANCHOR_OU", f"A0 OU positive anchor - genuine reversion (seed {s3})", a0.prices)

    # ---- BLIND packet (F4; fresh seeds, opaque ids, close-only, length-matched) ----
    print("\n[blind] 5-instrument blind packet (fresh seeds, same window):")
    bn1, bs1 = _positive(synthetic.random_walk, 101, sigma=sigma_abs, n=n, base=base)
    bn2, bs2 = _positive(synthetic.drift_random_walk, 102, mu=mu_abs, sigma=sigma_abs, n=n, base=base)
    ba0, bs3 = _positive(synthetic.ou, 103, lam=ANCHOR_LAM, sigma=sigma_abs, n=n, base=base)
    bn1b, bs4 = _positive(synthetic.random_walk, 104, sigma=sigma_abs, n=n, base=base)
    pool = [
        ("real_ADANIENT_seg", close.copy(),
         "real instrument segment (ground truth UNKNOWN — the open question)"),
        (f"N1_rw_seed{bs1}", bn1.prices, "pure random walk — non-reverting (mechanical residual only)"),
        (f"N2_drift_seed{bs2}", bn2.prices, "drifted random walk — non-reverting (trend-lag)"),
        (f"A0_ou_seed{bs3}", ba0.prices, "OU anchor — genuinely reverting"),
        (f"N1b_rw_seed{bs4}", bn1b.prices, "pure random walk (duplicate null; defeats one-of-each)"),
    ]
    rng = np.random.default_rng(BLIND_MASTER_SEED)
    order = rng.permutation(len(pool))
    mapping, ground_truth = {}, {}
    for slot, idx in enumerate(order, start=1):
        bid = f"BLIND_{slot}"
        truth_id, prices, desc = pool[idx]
        register(bid, f"blind packet #{slot}", prices)
        mapping[bid] = truth_id
        ground_truth[truth_id] = desc

    key = {
        "_DO_NOT_OPEN_UNTIL": "you have classified every BLIND_* instrument as "
                              "reverting / non-reverting / uncertain using ONLY REP, RES, CMP.",
        "protocol": "Hardened blind protocol, #11 F4 (replay seduction). Record classifications "
                    "first; then open to score. 'Residual reverts on a random walk' is EXPECTED "
                    "mechanics — NOT a kill. The test is DISCRIMINATION.",
        "window": {"ref": REF, "start": WIN_START, "len": n,
                   "dates": f"{dates.iloc[0].date()}..{dates.iloc[-1].date()}"},
        "positivity_filter": f"null seeds chosen as lowest >= base with min price >= {POS_FLOOR} "
                             f"(realism constraint, orthogonal to reversion).",
        "mapping": mapping,
        "ground_truth": ground_truth,
        "master_seed": BLIND_MASTER_SEED,
    }
    with open(KEY_PATH, "w") as f:
        json.dump(key, f, indent=2)

    conn.close()
    print(f"\n[blind] sealed mapping -> {KEY_PATH}")
    print("[done] Inspect via REP / RES / CMP as ordinary instruments.")
    print("       Labeled: NULL_RW, NULL_DRIFT, ANCHOR_OU.  Blind: BLIND_1..BLIND_5.")


if __name__ == "__main__":
    main()
