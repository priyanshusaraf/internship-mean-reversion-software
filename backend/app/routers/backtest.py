"""
Backtest router — POST /api/v2/backtest/run.

Wires the strictly-causal backtest engine to the existing instrument store and the FROZEN causal
z-score (`analytics_mrscore.causal_zscore`). It reuses existing engines and never recomputes a
statistic.

z-SOURCE NOTE (reconciliation): the build directive says "fetch z from GET /{id}/mrscore". That
endpoint does NOT expose a z column — it returns blocks/ranks/raw Block-2 features. The causal z
it consumes internally is `analytics_mrscore.causal_zscore` over the EMA-μ* residual (engine line
~245). We therefore call that same frozen function here (close → causal EMA μ* → residual →
causal_zscore, z_window=60). This is reuse of the existing engine path, not a reimplementation,
and honours "do not recompute it" (same formula, same shift convention).
"""
from __future__ import annotations

import duckdb
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException

from app.services import store, analytics, analytics_mrscore
from app.services.backtest_engine import BacktestConfig, BacktestResult, run_backtest

router = APIRouter(prefix="/api/v2/backtest", tags=["backtest"])

# Frozen z construction constants (mirror the production /diagnostics + /mrscore defaults).
_EMA_SPAN = 20        # causal EMA μ* span (matches /diagnostics and /mrscore window default)
_Z_WINDOW = 60        # causal_zscore trailing window (matches analytics_mrscore default)
_MIN_BARS = 60        # insufficient for z-score warmup below this
_MAX_GAP_BARS = 5     # alignment guard: no inter-bar gap may exceed this many bars


def get_db():
    is_injected = store._conn is not None
    conn = store.open_connection()
    try:
        yield conn
    finally:
        if not is_injected:
            conn.close()


def _verification_gate(config: BacktestConfig) -> None:
    """API-contract M4 param-freeze gate. In verification mode, every pinned param present in
    `prereg_params` must equal the incoming config value; any mismatch is a 422. (The directive
    prose names round_trip_cost AND strategy_id; we enforce per-key over whatever is pinned, which
    is what test 6 — pinning only round_trip_cost — requires.)"""
    if config.mode != "verification":
        return
    for key, expected in config.prereg_params.items():
        if not hasattr(config, key):
            continue
        actual = getattr(config, key)
        if actual != expected:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"VERIFICATION_MODE_MISMATCH: param {key} is {actual}, "
                    f"pre-registered as {expected}"
                ),
            )


@router.post("/run", response_model=BacktestResult)
def run(config: BacktestConfig, conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    # ── verification param-freeze gate (before any computation) ──
    _verification_gate(config)

    # ── window validation ──
    if config.start >= config.end:
        raise HTTPException(status_code=422, detail="start must be < end")

    df = store.get_ohlcv(conn, config.instrument_id, config.start, config.end)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data for: {config.instrument_id}")

    if len(df) < _MIN_BARS:
        raise HTTPException(
            status_code=422,
            detail=f"insufficient bars in window ({len(df)} < {_MIN_BARS}) for z-score warmup",
        )

    # Index by date (firewall already applied by the store date filter ≤ end).
    df = df.set_index("date").sort_index()
    close = df["close"]

    # ── causal z from the frozen engine path (NOT recomputed) ──
    mu_star = analytics.compute_ema(close, span=_EMA_SPAN)          # causal EMA μ*
    residual = analytics.compute_residual(close, mu_star)
    z_scores = analytics_mrscore.causal_zscore(residual, window=_Z_WINDOW)  # shifted μ,σ

    # ── alignment validation ──
    if not z_scores.index.equals(close.index):
        raise HTTPException(status_code=500, detail="alignment failure: z index ≠ ohlcv index")
    gaps = close.index.to_series().diff().dropna()
    if len(gaps) and (gaps.dt.days > _MAX_GAP_BARS).any():
        worst = gaps.max()
        raise HTTPException(
            status_code=500,
            detail=f"alignment failure: inter-bar gap {worst.days}d exceeds {_MAX_GAP_BARS} bars",
        )

    # Attach μ* so the engine can compute the entry-bar cost basis (0.003 × μ*).
    ohlcv = df[["open", "high", "low", "close", "volume"]].copy()
    ohlcv["mu_star"] = mu_star

    return run_backtest(config, ohlcv, z_scores)
