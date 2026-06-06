"""Observatory v2 slice tests (contract docs/build/api_contract.md acceptance gates).

Covers: firewall bit-identity (M1/M2) for equilibrium & habitat, as_of null≡last-bar (M2),
habitat single-path bit-identity (M3), mandatory surrogate cloud, construction 422 (M6),
upload→quality non-positive flag.
"""
import io
import csv
import json
import importlib.util
from pathlib import Path

import numpy as np
import duckdb
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import store
from app.services.store import _init_schema
from app.services.analytics_habitat import habitat_score_full

# Load the calibration script's habitat_score (delegates to the single path) for M3.
_spec = importlib.util.spec_from_file_location(
    "cal_hab", str(Path(__file__).resolve().parents[2] / "scripts" / "calibrate_habitat_score.py")
)
_cal = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cal)


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


# ── data builders ──────────────────────────────────────────────────────────────────

def _make_csv(closes, start="2020-01-01"):
    dates = np.array(np.datetime64(start)) + np.arange(len(closes))
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["date", "open", "high", "low", "close", "volume"])
    for d, c in zip(dates, closes):
        w.writerow([str(d), c, c + 1, c - 1, c, 1000])
    return buf.getvalue().encode()


def _upload(client, closes, name="DS", start="2020-01-01", mapping=None):
    files = {"file": (f"{name.lower()}.csv", _make_csv(closes, start), "text/csv")}
    data = {}
    if mapping is not None:
        data["mapping"] = json.dumps(mapping)
    r = client.post("/api/v2/datasets", files=files, data=data)
    return r


def _mr_closes(n=120, seed=7):
    """A mean-reverting-ish OU level series, strictly positive."""
    rng = np.random.default_rng(seed)
    x = np.empty(n)
    x[0] = 104.0
    for t in range(1, n):
        x[t] = x[t - 1] + 0.25 * (100.0 - x[t - 1]) + 0.8 * rng.normal()
    return np.abs(x) + 1.0


# ── upload → quality ─────────────────────────────────────────────────────────────────

def test_upload_and_quality_flow(client):
    closes = [100.0, 101.0, 102.0, 101.5, 100.5, 99.0]
    r = _upload(client, closes, name="NIFTY")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["dataset"]["dataset_id"] == "NIFTY"
    assert body["dataset"]["construction"]["beta_mode"] == "none"
    assert body["quality"]["row_count"] == 6
    assert body["quality"]["frequency"] == "daily"


def test_quality_flags_non_positive(client):
    closes = [100.0, 50.0, -5.0, -4.0, 60.0, 70.0]  # contiguous negative run
    r = _upload(client, closes, name="CL")
    assert r.status_code == 200, r.text
    npos = r.json()["quality"]["non_positive_prices"]
    assert npos["count"] == 2
    assert npos["suggested_excision"] is not None
    # flagged, never dropped → all rows persisted
    assert r.json()["quality"]["row_count"] == 6


# ── M2 — as_of null ≡ last bar ────────────────────────────────────────────────────────

def test_series_as_of_null_is_last_bar(client):
    closes = list(np.linspace(100, 110, 20))
    _upload(client, closes, name="DS")
    r = client.get("/api/v2/datasets/DS/series")
    assert r.status_code == 200
    body = r.json()
    assert body["as_of"] is not None  # resolved to last bar
    assert body["as_of"] == "2020-01-20"
    assert body["forward_bars"] == []
    assert len(body["bars"]) == 20


def test_series_as_of_caps(client):
    closes = list(np.linspace(100, 110, 20))
    _upload(client, closes, name="DS")
    r = client.get("/api/v2/datasets/DS/series?as_of=2020-01-10")
    body = r.json()
    assert all(b["time"] <= "2020-01-10" for b in body["bars"])
    assert all(b["time"] > "2020-01-10" for b in body["forward_bars"])
    assert len(body["forward_bars"]) == 10


# ── M1/M2 firewall bit-identity — equilibrium ─────────────────────────────────────────

def test_equilibrium_firewall_bit_identity(client):
    closes = _mr_closes(120)
    _upload(client, closes, name="DS")
    as_of = "2020-03-01"  # ~ day 60

    r1 = client.post("/api/v2/analysis/equilibrium", json={"dataset_id": "DS", "as_of": as_of})
    assert r1.status_code == 200, r1.text
    s1 = {row["time"]: row for row in r1.json()["series"]}

    # Append forward rows and recompute with the same as_of.
    extra = list(closes) + list(_mr_closes(40, seed=99) + 5.0)
    _upload(client, extra, name="DS")  # overwrites with a longer series (same prefix)
    r2 = client.post("/api/v2/analysis/equilibrium", json={"dataset_id": "DS", "as_of": as_of})
    s2 = {row["time"]: row for row in r2.json()["series"]}

    assert set(s1) == set(s2)
    for t in s1:
        for k in ("mu_star", "velocity", "innovation", "z", "gain", "state_var"):
            a, b = s1[t][k], s2[t][k]
            assert a == b, f"firewall leak at {t}.{k}: {a} != {b}"


def test_equilibrium_has_causal_z_and_provenance(client):
    closes = _mr_closes(120)
    _upload(client, closes, name="DS")
    r = client.post("/api/v2/analysis/equilibrium", json={"dataset_id": "DS", "as_of": "2020-03-01"})
    body = r.json()
    assert body["z_sigma_basis"] == "causal_expanding_innovation_std"
    assert any(row["z"] is not None for row in body["series"])
    assert body["series"][0]["z"] is None  # expanding σ undefined at first bar
    prov = body["provenance"]
    assert prov["mode"] == "research"
    assert prov["prereg_id"] is None
    assert prov["exploratory_watermark"] is False
    assert prov["engine"] == "compute_kalman_mu_star"


def test_equilibrium_nonfrozen_params_watermark(client):
    closes = _mr_closes(120)
    _upload(client, closes, name="DS")
    r = client.post("/api/v2/analysis/equilibrium", json={
        "dataset_id": "DS", "as_of": "2020-03-01",
        "params": {"snr": 1e-6, "kappa": 0.05, "warmup": 60},
    })
    assert r.json()["provenance"]["exploratory_watermark"] is True


# ── M3 — habitat single null path bit-identity ────────────────────────────────────────

def test_habitat_single_path_bit_identity():
    x = _mr_closes(60, seed=3)
    seed = 20260606
    assert habitat_score_full(x, seed)["score"] == _cal.habitat_score(x, seed)


# ── M1/M2 firewall — habitat score over window ≤ as_of ────────────────────────────────

def test_habitat_firewall_bit_identity(client):
    closes = _mr_closes(120)
    _upload(client, closes, name="DS")
    as_of = "2020-03-01"
    window = {"start": "2020-01-15", "end": "2020-02-29"}
    body = {"dataset_id": "DS", "window": window, "as_of": as_of}

    r1 = client.post("/api/v2/analysis/habitat", json=body)
    assert r1.status_code == 200, r1.text
    score1 = r1.json()["score"]

    extra = list(closes) + list(_mr_closes(40, seed=99) + 5.0)
    _upload(client, extra, name="DS")
    r2 = client.post("/api/v2/analysis/habitat", json=body)
    score2 = r2.json()["score"]
    assert score1 == score2


# ── mandatory surrogate cloud ──────────────────────────────────────────────────────────

def test_habitat_surrogate_cloud_mandatory(client):
    closes = _mr_closes(120)
    _upload(client, closes, name="DS")
    r = client.post("/api/v2/analysis/habitat", json={
        "dataset_id": "DS",
        "window": {"start": "2020-01-15", "end": "2020-02-29"},
        "as_of": "2020-03-01",
    })
    body = r.json()
    sd = body["surrogate_distribution"]
    assert sd is not None
    assert len(sd["null_min_vr"]) > 0
    assert sd["n"] == len(sd["null_min_vr"])
    # frac_ge_real == score/100
    assert abs(sd["frac_ge_real"] - body["score"] / 100.0) < 1e-12
    assert body["calibration_badge"]["status"] == "validated_non_inverting"


def test_habitat_window_past_as_of_422(client):
    closes = _mr_closes(120)
    _upload(client, closes, name="DS")
    r = client.post("/api/v2/analysis/habitat", json={
        "dataset_id": "DS",
        "window": {"start": "2020-03-01", "end": "2020-04-29"},
        "as_of": "2020-03-01",
    })
    assert r.status_code == 422


def test_habitat_deseason_toggle(client):
    closes = _mr_closes(120)
    _upload(client, closes, name="DS")
    r = client.post("/api/v2/analysis/habitat", json={
        "dataset_id": "DS",
        "window": {"start": "2020-01-15", "end": "2020-02-29"},
        "as_of": "2020-03-01",
        "deseason": True,
    })
    body = r.json()
    assert body["deseason"] is True
    assert body["raw_vs_deseason"] is not None
    assert "raw_score" in body["raw_vs_deseason"]


# ── M6 — construction gate ─────────────────────────────────────────────────────────────

def _flag_inadmissible(conn, dataset_id):
    from app.routers.observatory import _ensure_v2_meta, _load_meta, _save_meta
    _ensure_v2_meta(conn)
    meta = _load_meta(conn, dataset_id)
    meta["construction"] = {"beta_mode": "rolling-INADMISSIBLE", "roll_masked": False}
    _save_meta(conn, dataset_id, meta)


def test_construction_inadmissible_422(client):
    closes = _mr_closes(120)
    _upload(client, closes, name="DS")
    _flag_inadmissible(store._conn, "DS")

    r_eq = client.post("/api/v2/analysis/equilibrium", json={"dataset_id": "DS", "as_of": "2020-03-01"})
    assert r_eq.status_code == 422
    r_hab = client.post("/api/v2/analysis/habitat", json={
        "dataset_id": "DS",
        "window": {"start": "2020-01-15", "end": "2020-02-29"},
        "as_of": "2020-03-01",
    })
    assert r_hab.status_code == 422


def test_unknown_dataset_404(client):
    assert client.get("/api/v2/datasets/NOPE").status_code == 404
