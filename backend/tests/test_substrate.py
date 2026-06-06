"""
Substrate Observatory v1 — test suite.

The Substrate Observatory answers ONE observational question: *what kind of market are we currently
looking at?* — as instrument CHARACTER over a trailing window, never as episode timing. It is the
substrate layer beneath State T (docs/research/10_substrate_observatory.md; CLAUDE.md §10 freeze-break,
this session). OBSERVATORY ONLY — observe/falsify, NOT a signal; structurally terminal (never wired
into μ*, MRScore, or any gate). Character, not timing: it describes what an instrument *resembles*,
never whether a regime is "igniting" (that is State T detection, FROZEN — doc 04 §1.2.2/§1.3.1).

v1 SCOPE (frozen this session): causal mode only; 3 descriptors (directional efficiency, variance
ratio, realized-vol percentile-as-context); 4 coarse buckets (OU-like · Trend-like · RW-Null ·
Ambiguous); frozen transparent monotone score map (NO fitting, NO HMM, NO DL). Exhaustion/etiology
deferred to State T (episode timing). Hurst removed (noisy estimator).

Temporal-honesty invariants under test (the ways we could fool ourselves):
  • each descriptor at bar t uses only data in [t-W+1, t] — never reads bars > t
  • realized-vol percentile compares against the trailing window only
  • bit-identical future-injection: any value at bar t is unchanged when later bars change
"""
import numpy as np
import pandas as pd

from app.services import analytics_substrate as sub


# ── Synthetic habitats (mirror test_mrscore conventions) ──────────────────────

def _ou_series(n: int, lam: float, sigma: float, base: float = 100.0, seed: int = 42) -> pd.Series:
    """OU around `base`: Δd = λ·d + ε. Stationary mean-reverter for lam ∈ (-1, 0)."""
    rng = np.random.default_rng(seed)
    d = [0.0]
    for _ in range(n - 1):
        d.append(d[-1] + lam * d[-1] + rng.normal(0, sigma))
    return pd.Series(base + np.asarray(d))


def _rw_series(n: int, sigma: float = 1.0, base: float = 100.0, seed: int = 42) -> pd.Series:
    """Pure random walk: no mean reversion, no persistent drift."""
    rng = np.random.default_rng(seed)
    steps = rng.normal(0, sigma, n)
    steps[0] = 0.0
    return pd.Series(base + np.cumsum(steps))


def _trend_series(n: int, slope: float = 0.4, sigma: float = 0.5, base: float = 100.0, seed: int = 42) -> pd.Series:
    """Persistent drift + small noise: a structurally trending substrate (the ADANIENT regime)."""
    rng = np.random.default_rng(seed)
    return pd.Series(base + slope * np.arange(n) + np.cumsum(rng.normal(0, sigma, n)))


# ── P1: descriptor primitives ─────────────────────────────────────────────────

class TestDirectionalEfficiency:
    """DE = |net move| / total path length ∈ [0,1]. 1 = perfectly straight, ~0 = pure chop."""

    def test_straight_line_efficiency_one(self):
        p = np.linspace(100.0, 200.0, 50)
        assert abs(sub.directional_efficiency(p) - 1.0) < 1e-12

    def test_round_trip_efficiency_zero(self):
        # 100 → 110 → 100: ends exactly where it started → net move 0 → DE 0
        p = np.concatenate([np.arange(0.0, 11.0), np.arange(9.0, -1.0, -1.0)]) + 100.0
        assert p[0] == p[-1]
        assert sub.directional_efficiency(p) < 1e-9

    def test_bounded_unit_interval(self):
        de = sub.directional_efficiency(_rw_series(300, seed=3).to_numpy())
        assert 0.0 <= de <= 1.0

    def test_trend_more_efficient_than_ou(self):
        de_tr = sub.directional_efficiency(_trend_series(300, seed=42).to_numpy())
        de_ou = sub.directional_efficiency(_ou_series(300, lam=-0.2, sigma=0.5, seed=42).to_numpy())
        assert de_tr > de_ou


class TestVarianceRatioMean:
    """Representative VR over horizons: <1 mean-reverting, ≈1 random walk, >1 trending."""

    def test_random_walk_near_one(self):
        vr = sub.variance_ratio_mean(np.log(_rw_series(800, seed=42).to_numpy()))
        assert 0.75 < vr < 1.25

    def test_ou_below_one(self):
        vr = sub.variance_ratio_mean(np.log(_ou_series(800, lam=-0.2, sigma=0.5, seed=42).to_numpy()))
        assert vr < 0.9

    def test_trend_above_one(self):
        vr = sub.variance_ratio_mean(np.log(_trend_series(800, seed=42).to_numpy()))
        assert vr > 1.1


class TestRealizedVolPercentile:
    def test_bounds_and_rising_vol_ends_high(self):
        rng = np.random.default_rng(5)
        calm = rng.normal(0, 0.3, 200)
        wild = rng.normal(0, 2.0, 200)
        s = pd.Series(100.0 + np.cumsum(np.concatenate([calm, wild])))
        vp = sub.realized_vol_percentile(s).dropna()
        assert vp.min() >= 0.0 and vp.max() <= 100.0
        assert vp.iloc[-1] > 50.0  # latest (wild) vol sits high in its own history


# ── P2: character map (pure, frozen, monotone — no windowing) ──────────────────

class TestCharacterMap:
    """resemblance(de, vr) — transparent monotone map to 4 buckets, each ∈ [0,1]. Frozen, never fit."""

    def test_bounds(self):
        for de in (0.0, 0.5, 1.0):
            for vr in (0.3, 1.0, 1.8, 3.0):
                c = sub.character_scores(de, vr)
                for k in ("ou_like", "trend_like", "rw_null", "ambiguous"):
                    assert 0.0 <= c[k] <= 1.0

    def test_trend_profile_dominant_trend(self):
        c = sub.character_scores(de=0.9, vr=1.8)
        assert c["dominant"] == "trend_like"
        assert c["trend_like"] > c["ou_like"] and c["trend_like"] > c["rw_null"]

    def test_ou_profile_dominant_ou(self):
        c = sub.character_scores(de=0.1, vr=0.5)
        assert c["dominant"] == "ou_like"
        assert c["ou_like"] > c["trend_like"] and c["ou_like"] > c["rw_null"]

    def test_rw_profile_dominant_rw(self):
        c = sub.character_scores(de=0.15, vr=1.0)
        assert c["dominant"] == "rw_null"
        assert c["rw_null"] > c["ou_like"] and c["rw_null"] > c["trend_like"]

    def test_conflicting_profile_is_ambiguous_or_weak(self):
        # mid efficiency, VR mildly >1: sits between Trend and RW-Null → no archetype dominates
        c = sub.character_scores(de=0.45, vr=1.1)
        assert c["confidence"] in ("weak", "ambiguous")

    def test_trend_monotone_in_efficiency(self):
        lo = sub.character_scores(de=0.3, vr=1.6)["trend_like"]
        hi = sub.character_scores(de=0.9, vr=1.6)["trend_like"]
        assert hi > lo

    def test_nan_descriptors_yield_ambiguous(self):
        c = sub.character_scores(de=float("nan"), vr=float("nan"))
        assert c["dominant"] == "ambiguous" or c["confidence"] == "ambiguous"


# ── P3: per-bar descriptors + causal firewall ──────────────────────────────────

class TestSubstrateDescriptors:
    def test_columns_and_causality_bit_identical(self):
        """A violent future bar must not change ANY descriptor at earlier bars (causal firewall)."""
        base = _ou_series(400, lam=-0.2, sigma=0.5, seed=42)
        spiked = base.copy()
        spiked.iloc[360] = base.iloc[360] * 5.0
        f_base = sub.substrate_descriptors(base, window=120)
        f_spk = sub.substrate_descriptors(spiked, window=120)
        for col in ("de", "vr", "rv", "vp"):
            a = f_base[col].to_numpy()[:360]
            b = f_spk[col].to_numpy()[:360]
            both = np.isfinite(a) & np.isfinite(b)
            assert both.sum() > 30, f"{col}: too few pre-spike values ({both.sum()})"
            assert np.array_equal(a[both], b[both]), f"{col}: future spike leaked into bars < t0"


# ── P4: master compute + synthetic discrimination ──────────────────────────────

class TestComputeSubstrate:
    def test_columns_present_and_bounded(self):
        s = _ou_series(500, lam=-0.2, sigma=0.5, seed=42)
        df = sub.compute_substrate(s, window=120)
        for col in ("de", "vr", "rv", "vp", "ou_like", "trend_like", "rw_null", "ambiguous",
                    "dominant", "confidence"):
            assert col in df.columns
        ok = df.dropna(subset=["ou_like"])
        assert len(ok) > 50
        for col in ("ou_like", "trend_like", "rw_null", "ambiguous"):
            assert ok[col].min() >= 0.0 and ok[col].max() <= 1.0

    def test_ou_habitat_reads_ou_like(self):
        s = _ou_series(600, lam=-0.25, sigma=0.5, seed=42)
        df = sub.compute_substrate(s, window=150).dropna(subset=["dominant"])
        top = df["dominant"].value_counts().idxmax()
        assert top == "ou_like", f"OU habitat should read OU-like, got {top}"

    def test_trend_habitat_reads_trend_like(self):
        s = _trend_series(600, slope=0.4, sigma=0.5, seed=42)
        df = sub.compute_substrate(s, window=150).dropna(subset=["dominant"])
        top = df["dominant"].value_counts().idxmax()
        assert top == "trend_like", f"trend habitat should read Trend-like, got {top}"

    def test_random_walk_habitat_reads_rw_null(self):
        s = _rw_series(600, seed=42)
        df = sub.compute_substrate(s, window=150).dropna(subset=["dominant"])
        top = df["dominant"].value_counts().idxmax()
        assert top == "rw_null", f"RW habitat should read RW-Null, got {top}"

    def test_bit_identical_under_future_spike(self):
        """STANDING ACCEPTANCE BAR: a violent future bar must not change ANY earlier character score."""
        base = _ou_series(450, lam=-0.2, sigma=0.5, seed=42)
        spiked = base.copy()
        spiked.iloc[420] = base.iloc[420] * 6.0
        a = sub.compute_substrate(base, window=150)["trend_like"].to_numpy()[:420]
        b = sub.compute_substrate(spiked, window=150)["trend_like"].to_numpy()[:420]
        both = np.isfinite(a) & np.isfinite(b)
        assert both.sum() > 30
        assert np.array_equal(a[both], b[both]), "future spike leaked into earlier character scores"


# ── P5: endpoint ───────────────────────────────────────────────────────────────

import csv  # noqa: E402

import duckdb  # noqa: E402
import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.services import store  # noqa: E402
from app.services.store import _init_schema  # noqa: E402


@pytest.fixture
def fresh_store():
    c = duckdb.connect(":memory:")
    _init_schema(c)
    store._conn = c
    yield
    store._conn = None


@pytest.fixture
def client():
    return TestClient(app)


def _series_csv(tmp_path, series: pd.Series, name: str) -> str:
    path = tmp_path / f"{name}.csv"
    start = pd.Timestamp("2015-01-01")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "open", "high", "low", "close", "volume"])
        for i, v in enumerate(series):
            d = (start + pd.Timedelta(days=i)).strftime("%Y-%m-%d")
            w.writerow([d, v, v, v, v, 1000])
    return str(path)


class TestSubstrateAPI:
    def test_endpoint_shape_and_values(self, tmp_path, client, fresh_store):
        path = _series_csv(tmp_path, _ou_series(600, lam=-0.2, sigma=0.5, seed=42), "ou")
        client.post("/api/v1/market/load", json={"file_path": path, "instrument_id": "OU_S"})
        resp = client.get("/api/v1/market/OU_S/substrate")
        assert resp.status_code == 200
        body = resp.json()
        assert body["instrument_id"] == "OU_S"
        assert body["mode"] == "causal"
        assert len(body["rows"]) == 600
        scored = [r for r in body["rows"] if r["ou_like"] is not None]
        assert len(scored) > 30
        r = scored[-1]
        for k in ("de", "vr", "rv", "vp", "ou_like", "trend_like", "rw_null", "ambiguous",
                  "dominant", "confidence"):
            assert k in r

    def test_end_param_respects_temporal_firewall(self, tmp_path, client, fresh_store):
        path = _series_csv(tmp_path, _ou_series(600, lam=-0.2, sigma=0.5, seed=42), "ou_e")
        client.post("/api/v1/market/load", json={"file_path": path, "instrument_id": "OU_SE"})
        end = (pd.Timestamp("2015-01-01") + pd.Timedelta(days=549)).strftime("%Y-%m-%d")
        resp = client.get(f"/api/v1/market/OU_SE/substrate?end={end}")
        assert resp.status_code == 200
        assert len(resp.json()["rows"]) == 550

    def test_non_positive_prices_emit_explicit_warning(self, tmp_path, client, fresh_store):
        """A spread/negative-price series must NOT silently blank the VR-based character — it must
        carry an explicit data_warning (structural incompatibility ≠ unfavorable reading)."""
        vals = pd.Series(np.sin(np.linspace(0, 25, 600)) * 5.0)  # crosses zero
        path = _series_csv(tmp_path, vals, "spread")
        client.post("/api/v1/market/load", json={"file_path": path, "instrument_id": "SPR_S"})
        body = client.get("/api/v1/market/SPR_S/substrate").json()
        assert body["data_warning"] is not None
        assert "non-positive" in body["data_warning"].lower()

    def test_positive_prices_have_no_data_warning(self, tmp_path, client, fresh_store):
        path = _series_csv(tmp_path, _ou_series(600, lam=-0.2, sigma=0.5, seed=42), "pos")
        client.post("/api/v1/market/load", json={"file_path": path, "instrument_id": "POS_S"})
        body = client.get("/api/v1/market/POS_S/substrate").json()
        assert body["data_warning"] is None
