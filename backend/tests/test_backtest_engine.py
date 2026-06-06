"""
Backtest engine tests — causal firewall, trade mechanics, time stop, no-overlap, metrics
sanity, and the verification-mode param-freeze gate.

Strategy under test = MR_PLACEHOLDER_V1 (frozen): enter when |z|≥1 (fade), exit when |z|<0.05
(Z_CROSS) or after 20 bars (TIME_STOP); fill = close[t+1]; cost = 0.003 × μ* at entry bar.
"""
import duckdb
import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import store
from app.services.store import _init_schema
from app.services import synthetic
from app.services.backtest_engine import BacktestConfig, run_backtest


# ── builders ──────────────────────────────────────────────────────────────────

def _dates(n, start="2020-01-01"):
    return pd.DatetimeIndex(pd.Timestamp(start) + pd.to_timedelta(np.arange(n), unit="D"))


def _ohlcv(closes, mu_star=None, start="2020-01-01"):
    """OHLCV frame with consecutive daily DatetimeIndex; mu_star column for the cost basis."""
    closes = np.asarray(closes, dtype=float)
    n = len(closes)
    idx = _dates(n, start)
    if mu_star is None:
        mu_star = np.full(n, 100.0)
    df = pd.DataFrame(
        {
            "open": closes,
            "high": closes + 1.0,
            "low": closes - 1.0,
            "close": closes,
            "volume": np.full(n, 1000.0),
            "mu_star": np.asarray(mu_star, dtype=float),
        },
        index=idx,
    )
    df.index.name = "date"
    return df


def _cfg(**kw):
    base = dict(instrument_id="TEST", start="2020-01-01", end="2099-01-01")
    base.update(kw)
    return BacktestConfig(**base)


# ── 1. CAUSAL FIREWALL ──────────────────────────────────────────────────────────

def test_causal_firewall_no_reference_beyond_window():
    """OU bars 0..N-1 in-window; a price spike at bar N is OUTSIDE the window and must never be
    touched. The window is sliced before run_backtest, so no trade may reference a bar > N-1 and
    the equity curve must have exactly N entries."""
    N = 120
    ou = synthetic.ou(lam=-0.15, sigma=1.0, n=N + 1, seed=7)
    full_close = ou.prices.copy()
    full_close[N] = full_close[N] + 500.0          # spike at bar N (outside the in-window slice)

    # In-window slice: first N bars only (firewall enforced by the caller).
    in_close = full_close[:N]
    df = _ohlcv(in_close)
    resid = pd.Series(in_close - df["mu_star"].to_numpy(), index=df.index)
    from app.services.analytics_mrscore import causal_zscore
    z = causal_zscore(resid, window=60)

    res = run_backtest(_cfg(), df, z)

    assert len(res.equity_curve) == N
    last_in_window = df.index[-1].strftime("%Y-%m-%d")
    for t in res.trades:
        assert t.entry_bar <= last_in_window
        assert t.exit_bar <= last_in_window
    # every equity-curve date is in-window
    assert all(pt["date"] <= last_in_window for pt in res.equity_curve)


# ── 2. TRADE MECHANICS ────────────────────────────────────────────────────────

def test_trade_mechanics_single_short_z_cross():
    """z crosses +1 at bar 10, returns to ~0 at bar 15 → exactly one SHORT trade, Z_CROSS exit,
    entry_bar = bar10, exit_bar = bar15, net = gross − cost."""
    N = 30
    z = np.zeros(N)
    z[10:15] = 1.5                                 # entry at 10, held through 14
    z[15] = 0.0                                    # z-cross exit at 15
    closes = 100.0 + np.arange(N) * 0.0            # flat-ish; make fills distinct
    closes = np.linspace(100.0, 90.0, N)           # monotonic decline → SHORT profits
    mu = np.full(N, 100.0)
    df = _ohlcv(closes, mu_star=mu)
    zs = pd.Series(z, index=df.index)

    res = run_backtest(_cfg(), df, zs)

    shorts = [t for t in res.trades if t.direction == "SHORT"]
    assert res.n_trades == 1
    assert len(shorts) == 1
    tr = shorts[0]
    assert tr.entry_bar == df.index[10].strftime("%Y-%m-%d")
    assert tr.exit_bar == df.index[15].strftime("%Y-%m-%d")
    assert tr.exit_reason == "Z_CROSS"
    assert tr.entry_price == pytest.approx(closes[11])   # fill = close[entry+1]
    assert tr.exit_price == pytest.approx(closes[16])    # fill = close[exit+1]
    assert tr.gross_pnl == pytest.approx(closes[11] - closes[16])  # SHORT: entry − exit
    assert tr.cost == pytest.approx(0.003 * mu[10])
    assert tr.net_pnl == pytest.approx(tr.gross_pnl - tr.cost)
    assert tr.bars_held == 5


# ── 3. TIME STOP ──────────────────────────────────────────────────────────────

def test_time_stop_exit_at_20_bars():
    """z crosses +1 at bar 10 and never returns to 0 → TIME_STOP exit at bar 30 (held 20)."""
    N = 40
    z = np.zeros(N)
    z[10:] = 1.5                                    # never re-enters the ±0.05 band
    closes = np.linspace(100.0, 95.0, N)
    df = _ohlcv(closes, mu_star=np.full(N, 100.0))
    zs = pd.Series(z, index=df.index)

    res = run_backtest(_cfg(), df, zs)

    assert res.n_trades == 1
    tr = res.trades[0]
    assert tr.exit_reason == "TIME_STOP"
    assert tr.entry_bar == df.index[10].strftime("%Y-%m-%d")
    assert tr.exit_bar == df.index[30].strftime("%Y-%m-%d")
    assert tr.bars_held == 20


# ── 4. NO OVERLAP ───────────────────────────────────────────────────────────────

def test_no_overlapping_positions():
    """z crosses ±1 on consecutive bars; the engine must hold one position at a time. Verified
    externally: every recorded trade's [entry,exit] interval is pairwise disjoint."""
    N = 60
    z = np.zeros(N)
    sign = 1.0
    for i in range(10, N):
        z[i] = sign * 1.5
        sign *= -1.0                                # alternate ±1.5 every bar
    closes = 100.0 + np.sin(np.arange(N) * 0.3)
    df = _ohlcv(closes, mu_star=np.full(N, 100.0))
    zs = pd.Series(z, index=df.index)

    res = run_backtest(_cfg(), df, zs)

    assert res.n_trades >= 1
    date_to_pos = {d.strftime("%Y-%m-%d"): i for i, d in enumerate(df.index)}
    intervals = sorted(
        (date_to_pos[t.entry_bar], date_to_pos[t.exit_bar]) for t in res.trades
    )
    for (a_lo, a_hi), (b_lo, b_hi) in zip(intervals, intervals[1:]):
        assert a_hi < b_lo, f"overlap: trade [{a_lo},{a_hi}] vs [{b_lo},{b_hi}]"


# ── 5. METRICS SANITY ────────────────────────────────────────────────────────

def test_metrics_sanity_on_ou():
    """Run on a real causal pipeline over an OU series; sanity-bound every headline metric."""
    from app.services import analytics
    from app.services.analytics_mrscore import causal_zscore

    N = 500
    ou = synthetic.ou(lam=-0.12, sigma=1.0, n=N, seed=3)
    closes = pd.Series(ou.prices, index=_dates(N))
    mu_star = analytics.compute_ema(closes, span=20)
    resid = analytics.compute_residual(closes, mu_star)
    z = causal_zscore(resid, window=60)

    df = _ohlcv(closes.to_numpy(), mu_star=mu_star.to_numpy())
    res = run_backtest(_cfg(), df, pd.Series(z.to_numpy(), index=df.index))

    assert 0.0 <= res.win_rate <= 1.0
    assert np.isfinite(res.sharpe_ratio)
    assert res.max_drawdown <= 0.0
    assert len(res.equity_curve) == res.n_bars == N


# ── 6. VERIFICATION MODE (HTTP gate) ────────────────────────────────────────────

@pytest.fixture
def client_with_data():
    c = duckdb.connect(":memory:")
    _init_schema(c)
    store._conn = c
    ou = synthetic.ou(lam=-0.12, sigma=1.0, n=200, seed=11)
    df = _ohlcv(ou.prices)[["open", "high", "low", "close", "volume"]]
    store.store_instrument(c, "VERIF", "VERIF", df, "synthetic://verif")
    yield TestClient(app)
    store._conn = None


def test_verification_mode_match_and_mismatch(client_with_data):
    client = client_with_data
    body = {
        "instrument_id": "VERIF",
        "start": "2020-01-01",
        "end": "2099-01-01",
        "mode": "verification",
        "prereg_params": {"round_trip_cost": 0.003},
        "round_trip_cost": 0.003,
    }
    ok = client.post("/api/v2/backtest/run", json=body)
    assert ok.status_code == 200, ok.text
    assert ok.json()["verification_watermark"] is True

    body_bad = dict(body)
    body_bad["round_trip_cost"] = 0.005
    bad = client.post("/api/v2/backtest/run", json=body_bad)
    assert bad.status_code == 422
    assert "VERIFICATION_MODE_MISMATCH" in bad.json()["detail"]
