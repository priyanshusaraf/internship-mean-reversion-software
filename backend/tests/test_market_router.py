import duckdb
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import store
from app.services.store import _init_schema


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


def test_health(client):
    assert client.get("/health").status_code == 200


def test_load_valid_file(client, sample_csv):
    resp = client.post("/api/v1/market/load", json={
        "file_path": sample_csv, "instrument_id": "NIFTY"
    })
    assert resp.status_code == 200
    assert resp.json()["row_count"] == 3


def test_load_missing_file(client):
    resp = client.post("/api/v1/market/load", json={
        "file_path": "/nonexistent/file.csv", "instrument_id": "X"
    })
    assert resp.status_code == 422


def test_list_instruments_empty(client):
    assert client.get("/api/v1/market/instruments").json() == []


def test_list_instruments_after_load(client, sample_csv):
    client.post("/api/v1/market/load", json={"file_path": sample_csv, "instrument_id": "NIFTY"})
    assert len(client.get("/api/v1/market/instruments").json()) == 1


def test_get_ohlcv(client, sample_csv):
    client.post("/api/v1/market/load", json={"file_path": sample_csv, "instrument_id": "NIFTY"})
    resp = client.get("/api/v1/market/NIFTY/ohlcv")
    assert resp.status_code == 200
    bars = resp.json()["bars"]
    assert len(bars) == 3
    assert bars[0]["time"] == "2024-01-01"


def test_get_ohlcv_date_filter(client, sample_csv):
    client.post("/api/v1/market/load", json={"file_path": sample_csv, "instrument_id": "NIFTY"})
    resp = client.get("/api/v1/market/NIFTY/ohlcv?start=2024-01-02&end=2024-01-02")
    assert len(resp.json()["bars"]) == 1


def test_get_ohlcv_unknown_instrument(client):
    assert client.get("/api/v1/market/UNKNOWN/ohlcv").status_code == 404
