"""Level-series (spread / non-positive price) handling.

Context (verified empirically before writing): the habitat null engine
(`analytics_habitat.vr_q` / `habitat_score_full`) and the Kalman μ* / z-score were
ALREADY level-difference math — no log is taken on prices anywhere. So a negative-price
spread already scores finitely; the prior defect was only a MISLEADING router warning that
claimed "score may be null". These tests pin the correct behaviour:

  1. is_level_series detector
  2. level_variance_ratio sanity (OU sub-diffusive < 1; RW ≈ 1)
  3. habitat score on an all-negative series → finite, in [0,100]; router note is informational
  4. surrogate parity — surrogates are built from level differences (ΔS), so on a negative
     series they also go negative (NOT strictly positive like log-return surrogates), and the
     null cloud is non-empty / finite (impossible if a log had been taken on negative prices).
"""
import io
import csv

import numpy as np
import pandas as pd
import duckdb
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import store
from app.services.store import _init_schema
from app.services import synthetic
from app.services.analytics import (
    is_level_series, level_difference_returns, level_variance_ratio,
)
from app.services.analytics_habitat import habitat_score_full, VR_QS, NS_NULL


# ── fixtures (mirror test_observatory_v2.py) ─────────────────────────────────────────

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


def _make_csv(closes, start="2020-01-01"):
    dates = np.array(np.datetime64(start)) + np.arange(len(closes))
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["date", "open", "high", "low", "close", "volume"])
    for d, c in zip(dates, closes):
        w.writerow([str(d), c, c + 1, c - 1, c, 1000])
    return buf.getvalue().encode()


def _upload(client, closes, name="NEGSPREAD", start="2020-01-01"):
    files = {"file": (f"{name.lower()}.csv", _make_csv(closes, start), "text/csv")}
    r = client.post("/api/v2/datasets", files=files)
    assert r.status_code == 200, r.text
    return r.json()["dataset"]["dataset_id"]


# ── 1. LEVEL DETECTOR ────────────────────────────────────────────────────────────────

def test_detector_all_positive_false():
    assert is_level_series(pd.Series([1.0, 2.0, 3.0, 100.0])) is False


def test_detector_one_zero_true():
    assert is_level_series(pd.Series([1.0, 2.0, 0.0, 3.0])) is True


def test_detector_one_negative_true():
    assert is_level_series(pd.Series([1.0, 2.0, -0.5, 3.0])) is True


# ── 2. LEVEL VR SANITY ───────────────────────────────────────────────────────────────

def test_level_vr_ou_subdiffusive():
    """OU (mean-reverting) → VR(q) < 1.0 (sub-diffusive)."""
    s = pd.Series(synthetic.ou(lam=-0.1, sigma=1.0, n=2000, seed=3).prices)
    vr = level_variance_ratio(s, q=10)
    assert np.isfinite(vr)
    assert vr < 1.0


def test_level_vr_random_walk_near_one():
    """Pure random walk → VR(q) ≈ 1.0 (±0.2)."""
    s = pd.Series(synthetic.random_walk(sigma=1.0, n=3000, seed=7).prices)
    vr = level_variance_ratio(s, q=10)
    assert np.isfinite(vr)
    assert abs(vr - 1.0) < 0.2


def test_level_vr_insufficient_data_nan():
    assert np.isnan(level_variance_ratio(pd.Series([1.0, 2.0, 3.0]), q=10))


# ── 3. HABITAT SCORE ON NEGATIVE SERIES ──────────────────────────────────────────────

def _negative_series(seed=11, n=500):
    """OU shifted down by 2× its mean → every bar non-positive (like coffee−cocoa)."""
    p = synthetic.ou(lam=-0.1, sigma=1.0, n=n, seed=seed, base=100.0).prices
    shifted = p - 2.0 * float(np.mean(p))
    assert (shifted <= 0).all()           # genuinely a non-positive instrument
    return shifted


def test_habitat_score_finite_on_negative_engine():
    """Engine: all-negative window → finite score in [0,100] (proves NO log is taken)."""
    x = _negative_series()
    res = habitat_score_full(x, seed=42)
    assert res["score"] is not None
    assert np.isfinite(res["score"])
    assert 0.0 <= res["score"] <= 100.0
    assert np.isfinite(res["real_min_vr"])


def test_habitat_negative_series_router_note(client):
    """Router: negative spread → 200, finite score, INFORMATIONAL note (not a 'null' warning)."""
    closes = _negative_series(seed=5, n=400)
    ds = _upload(client, closes, name="NEGSPREAD")
    body = {
        "dataset_id": ds,
        "window": {"start": "2020-01-15", "end": "2021-01-31"},
        "as_of": "2021-01-31",
        "deseason": False,
        "params": {"vr_qs": [2, 5, 10, 20], "ns_null": 200, "seed": 42},
    }
    r = client.post("/api/v2/analysis/habitat", json=body)
    assert r.status_code == 200, r.text
    d = r.json()
    assert d["score"] is not None and np.isfinite(d["score"])
    assert 0.0 <= d["score"] <= 100.0
    warn = d["data_warning"] or ""
    assert "score may be null" not in warn
    assert ("level-difference" in warn) or warn.startswith("ℹ")


# ── 4. SURROGATE PARITY (level diffs, not log-returns) ────────────────────────────────

def test_surrogate_cloud_nonempty_on_negative_series():
    """A non-empty / finite null cloud on an all-negative series is only possible if the
    surrogates were built from LEVEL differences. Log-return surrogates of negative prices
    would be NaN throughout → empty null list → NaN score."""
    x = _negative_series(seed=9)
    res = habitat_score_full(x, seed=42)
    nulls = res["null_min_vr"]
    assert len(nulls) > 0
    assert all(np.isfinite(v) for v in nulls)


def test_surrogates_go_negative_like_real_series():
    """Reconstruct the engine's RW-null path construction VERBATIM (analytics_habitat.py:
    path = x[0] + cumsum(level-diff draws)). On a negative series the surrogates also go
    negative — the discriminating signature of ΔS surrogates vs strictly-positive
    log-return surrogates."""
    x = _negative_series(seed=13)
    x_fin = x[np.isfinite(x)]
    dr = np.diff(x_fin)
    mu_dr, sig_dr = float(np.mean(dr)), float(np.std(dr, ddof=1))
    rng = np.random.default_rng(42)
    n = len(x_fin)
    went_negative = 0
    trials = 50
    for _ in range(trials):
        path = np.concatenate([[x_fin[0]], x_fin[0] + np.cumsum(rng.normal(mu_dr, sig_dr, n - 1))])
        if path.min() < 0:
            went_negative += 1
    # every surrogate starts at the (negative) real x[0]; essentially all go negative.
    assert went_negative >= int(0.9 * trials)


def test_real_and_surrogate_use_same_vr_function():
    """Real VR and surrogate VR are the SAME math: both go through analytics_habitat.min_vr/
    vr_q on levels. Pin that the standalone analytics.level_variance_ratio agrees with the
    frozen vr_q on a shared lag (no divergent second estimator)."""
    from app.services.analytics_habitat import vr_q
    x = _negative_series(seed=17)
    q = VR_QS[-1]
    a = level_variance_ratio(pd.Series(x), q)
    b = vr_q(np.asarray(x, dtype=float), q)
    assert np.isfinite(a) and np.isfinite(b)
    assert abs(a - b) < 1e-9
