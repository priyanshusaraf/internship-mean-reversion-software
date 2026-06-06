import csv
import math
import duckdb
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import store, analytics
from app.services.store import _init_schema
import pandas as pd


@pytest.fixture(autouse=True)
def fresh_store():
    c = duckdb.connect(":memory:")
    _init_schema(c)
    store._conn = c
    yield
    store._conn = None


@pytest.fixture
def client():
    return TestClient(app)


# --- analytics unit tests ---

def test_compute_ema_basic():
    closes = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0])
    result = analytics.compute_ema(closes, span=3)
    assert len(result) == 5
    assert not result.isna().any()
    assert all(math.isfinite(v) for v in result)


def test_compute_ema_span_1_equals_close():
    closes = pd.Series([100.0, 200.0, 300.0])
    result = analytics.compute_ema(closes, span=1)
    # span=1 means alpha=1: EMA_t = close_t exactly
    pd.testing.assert_series_equal(result, closes, check_names=False)


# --- router tests ---

def test_estimator_endpoint_returns_bars(client, sample_csv):
    client.post("/api/v1/market/load", json={"file_path": sample_csv, "instrument_id": "NIFTY"})
    resp = client.get("/api/v1/market/NIFTY/estimator?estimator=ema&window=2")
    assert resp.status_code == 200
    body = resp.json()
    assert body["estimator"] == "ema"
    assert body["window"] == 2
    assert len(body["bars"]) == 3
    for bar in body["bars"]:
        assert "time" in bar and "value" in bar
        assert math.isfinite(bar["value"])


def test_estimator_unknown_estimator_returns_400(client, sample_csv):
    client.post("/api/v1/market/load", json={"file_path": sample_csv, "instrument_id": "NIFTY"})
    resp = client.get("/api/v1/market/NIFTY/estimator?estimator=kalman")
    assert resp.status_code == 400


def test_estimator_unknown_instrument_returns_404(client):
    resp = client.get("/api/v1/market/UNKNOWN/estimator")
    assert resp.status_code == 404


def test_estimator_end_blocks_future_spike(tmp_path, client):
    """
    Adversarial temporal integrity test.
    Bar 4 has a huge price spike (5000). Querying with end=bar3 must:
    1. Return only 3 bars (bar 4 is excluded)
    2. Return EMA values at bar 3 identical to when computed without bar 4 in scope
    No future price can contaminate past EMA values.
    """
    path = tmp_path / "spike.csv"
    rows = [
        ["date", "open", "high", "low", "close", "volume"],
        ["2024-01-01", "100.0", "101.0",  "99.0",  "100.0", "1000"],
        ["2024-01-02", "101.0", "102.0", "100.0",  "101.0", "1000"],
        ["2024-01-03", "102.0", "103.0", "101.0",  "102.0", "1000"],
        ["2024-01-04", "5000.0", "5001.0", "4999.0", "5000.0", "1000"],  # future spike
    ]
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows(rows)

    client.post("/api/v1/market/load", json={"file_path": str(path), "instrument_id": "spike"})

    # Causal query: end=2024-01-03 — spike must not influence any returned value
    resp_capped = client.get("/api/v1/market/spike/estimator?estimator=ema&window=3&end=2024-01-03")
    # Full query: no end — spike is included
    resp_full = client.get("/api/v1/market/spike/estimator?estimator=ema&window=3")

    assert resp_capped.status_code == 200
    assert resp_full.status_code == 200

    capped_bars = resp_capped.json()["bars"]
    full_bars = resp_full.json()["bars"]

    # Capped response must contain exactly 3 bars (spike bar excluded)
    assert len(capped_bars) == 3

    # Full response has all 4 bars
    assert len(full_bars) == 4

    # EMA at 2024-01-03 must be identical in both responses:
    # the forward-only EMA at t cannot be changed by data added after t.
    capped_t3 = next(b for b in capped_bars if b["time"] == "2024-01-03")
    full_t3 = next(b for b in full_bars if b["time"] == "2024-01-03")
    assert abs(capped_t3["value"] - full_t3["value"]) < 1e-10

    # Sanity: no capped bar should be anywhere near the spike value
    assert all(b["value"] < 500 for b in capped_bars)
