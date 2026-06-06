"""
MRScore v1 — observatory diagnostic test suite.

MRScore is a DESCRIPTIVE falsification instrument (CLAUDE.md §10 freeze-break, this session):
it observes whether conditions are favourable for mean reversion. It is NOT a signal and is
structurally terminal — never wired into a validity gate, RFI, or μ* recalibration.

Canonical spec: docs/research/01_amr_framework.md §3 (eq. 13–34). Formulas are FROZEN; these
tests pin faithful behaviour, the causal firewall, and synthetic discrimination.

Temporal-honesty invariants under test (the things that would let us fool ourselves):
  • causal z uses only data strictly before t (no contemporaneous σ contamination)
  • forward-return features (DRC, HitRate) never read bars > t
  • percentile ranks compare against PRIOR bars only
  • bit-identical future-injection: any value at bar t is unchanged when later bars change
"""
import math

import numpy as np
import pandas as pd

from app.services import analytics_mrscore as mrs


# ── Synthetic helpers (mirror test_analytics_validation conventions) ──────────

def _ou_series(n: int, lam: float, sigma: float, base: float = 100.0, seed: int = 42) -> pd.Series:
    """OU around `base`: Δd = λ·d + ε. Stationary mean-reverter for lam ∈ (-1, 0)."""
    rng = np.random.default_rng(seed)
    d = [0.0]
    for _ in range(n - 1):
        d.append(d[-1] + lam * d[-1] + rng.normal(0, sigma))
    return pd.Series(base + np.asarray(d))


def _rw_series(n: int, sigma: float = 1.0, base: float = 100.0, seed: int = 42) -> pd.Series:
    """Pure random walk: no mean reversion exists."""
    rng = np.random.default_rng(seed)
    steps = rng.normal(0, sigma, n)
    steps[0] = 0.0
    return pd.Series(base + np.cumsum(steps))


# ── P1: primitives + causal z ─────────────────────────────────────────────────

class TestCausalZScore:
    """z_t must use μ,σ from data strictly before t (doc 01 lines 622–625)."""

    def test_current_value_at_trailing_mean_gives_zero(self):
        # trailing window [10,12,14,16] mean=13; current=13 → z=0
        r = pd.Series([10.0, 12.0, 14.0, 16.0, 13.0])
        z = mrs.causal_zscore(r, window=4)
        assert abs(z.iloc[4] - 0.0) < 1e-12

    def test_positive_deviation_gives_positive_z(self):
        r = pd.Series([10.0, 12.0, 14.0, 16.0, 18.0])
        z = mrs.causal_zscore(r, window=4)
        # trailing mean 13, sample std sqrt(20/3)=2.582 → (18-13)/2.582 ≈ 1.936
        assert abs(z.iloc[4] - (18.0 - 13.0) / math.sqrt(20.0 / 3.0)) < 1e-9

    def test_excludes_current_bar_bit_identical(self):
        """z at every shared bar is unchanged when later bars are appended."""
        s = _rw_series(300, seed=7)
        z_full = mrs.causal_zscore(s, window=20)
        z_pref = mrs.causal_zscore(s.iloc[:150], window=20)
        a = z_full.iloc[:150].to_numpy()
        b = z_pref.to_numpy()
        both = np.isfinite(a) & np.isfinite(b)
        assert both.sum() > 50
        assert np.array_equal(a[both], b[both])


class TestRollingPercentileRank:
    def test_increasing_series_ranks_top(self):
        s = pd.Series(np.arange(50.0))
        r = mrs.rolling_percentile_rank(s, window=10, min_periods=3)
        # each current value exceeds all prior → rank 100
        assert r.dropna().iloc[-1] == 100.0

    def test_decreasing_series_ranks_bottom(self):
        s = pd.Series(np.arange(50.0)[::-1])
        r = mrs.rolling_percentile_rank(s, window=10, min_periods=3)
        assert r.dropna().iloc[-1] == 0.0

    def test_constant_feature_ranks_mid_not_zero(self):
        """Saturated/constant features must rank ~50 (neutral), NOT 0 (worst). Strict-< would put a
        perfectly-stable feature (e.g. MeanStab capped at 1.0) at rank 0 — inverting its meaning."""
        s = pd.Series([5.0] * 60)
        r = mrs.rolling_percentile_rank(s, window=30, min_periods=5)
        assert abs(r.dropna().iloc[-1] - 50.0) < 1e-9

    def test_bounds_and_excludes_current_bit_identical(self):
        s = _rw_series(300, seed=11)
        r_full = mrs.rolling_percentile_rank(s, window=50, min_periods=10)
        r_pref = mrs.rolling_percentile_rank(s.iloc[:150], window=50, min_periods=10)
        vals = r_full.dropna()
        assert vals.min() >= 0.0 and vals.max() <= 100.0
        a, b = r_full.iloc[:150].to_numpy(), r_pref.to_numpy()
        both = np.isfinite(a) & np.isfinite(b)
        assert both.sum() > 50
        assert np.array_equal(a[both], b[both])


class TestRealizedVol:
    def test_constant_log_return_recovers_annualized_vol(self):
        c = 0.01
        closes = pd.Series(100.0 * np.exp(c * np.arange(100)))  # constant log-return c
        rv = mrs.realized_vol(closes, window=20)
        # RV = sqrt(252/w · Σ r²) = sqrt(252)·|c| when every return == c
        assert abs(rv.dropna().iloc[-1] - math.sqrt(252.0) * abs(c)) < 1e-9


class TestVolPercentile:
    def test_monotone_rising_vol_ends_high(self):
        rv = pd.Series(np.arange(1.0, 101.0))
        vp = mrs.vol_percentile(rv, window=252, min_periods=10)
        v = vp.dropna()
        assert v.min() >= 0.0 and v.max() <= 100.0
        assert v.iloc[-1] >= 95.0  # latest vol is near the top of its history


# ── P2: Block 2 — DRC / HitRate / VR (highest temporal risk) ───────────────────

from app.services import analytics  # noqa: E402


def _prep(series: pd.Series, span: int = 20, zwin: int = 60):
    """EMA μ* → residual → causal z, plus log-prices. Returns (z_array, logprice_array, price_array)."""
    mu = analytics.compute_ema(series, span)
    resid = series - mu
    z = mrs.causal_zscore(resid, zwin)
    return z.to_numpy(), np.log(series.to_numpy()), series.to_numpy()


class TestNeweyWestTStat:
    def test_strong_negative_relationship(self):
        rng = np.random.default_rng(1)
        x = rng.normal(0, 1, 400)
        y = -1.0 * x + rng.normal(0, 0.1, 400)
        t = mrs.newey_west_tstat(x, y, lag=1)
        assert t < -5.0

    def test_no_relationship_not_significant(self):
        rng = np.random.default_rng(2)
        x = rng.normal(0, 1, 400)
        y = rng.normal(0, 1, 400)  # independent
        t = mrs.newey_west_tstat(x, y, lag=1)
        assert abs(t) < 3.0


class TestDRCWindow:
    def test_ou_has_significant_negative_drc(self):
        z, logp, _ = _prep(_ou_series(500, lam=-0.2, sigma=0.5, seed=42))
        drc = mrs.drc_window(z, logp, min_obs=120)
        assert drc < -2.86, f"OU should show significant reversion (DRC={drc:.2f})"

    def test_random_walk_drc_not_significant(self):
        """NW-HAC must NOT manufacture significant −DRC on a random walk (forward returns are white)."""
        z, logp, _ = _prep(_rw_series(500, seed=42))
        drc = mrs.drc_window(z, logp, min_obs=120)
        assert drc > -2.86, f"RW must not be significantly mean-reverting (DRC={drc:.2f})"

    def test_ou_drc_more_negative_than_rw(self):
        z_o, lp_o, _ = _prep(_ou_series(500, lam=-0.2, sigma=0.5, seed=42))
        z_r, lp_r, _ = _prep(_rw_series(500, seed=42))
        assert mrs.drc_window(z_o, lp_o) < mrs.drc_window(z_r, lp_r) - 1.0


class TestHitRateWindow:
    def test_ou_hit_rate_above_half(self):
        z, _, price = _prep(_ou_series(600, lam=-0.2, sigma=0.5, seed=42))
        hr = mrs.hit_rate_window(z, price, theta=1.0, h=5)
        assert hr > 0.5, f"OU deviations should revert more often than not (hit={hr})"

    def test_too_few_events_returns_nan(self):
        # z below threshold everywhere → 0 qualifying events → excluded
        hr = mrs.hit_rate_window(np.zeros(100), np.ones(100), theta=1.0, h=5, min_events=20)
        assert np.isnan(hr)


class TestVarianceRatio:
    def test_random_walk_vr_near_one(self):
        _, logp, _ = _prep(_rw_series(800, seed=42))
        vr = mrs.variance_ratios(logp, qs=(2,))
        assert 0.75 < vr[2] < 1.25, f"RW VR(2) should be ≈1, got {vr[2]:.3f}"

    def test_ou_vr_agg_below_random_walk(self):
        _, lp_o, _ = _prep(_ou_series(800, lam=-0.2, sigma=0.5, seed=42))
        _, lp_r, _ = _prep(_rw_series(800, seed=42))
        assert mrs.variance_ratio_agg(lp_o) < mrs.variance_ratio_agg(lp_r)


class TestBlock2CausalFirewall:
    def test_block2_bit_identical_under_future_spike(self):
        """A spike at bar t0 must not change ANY Block-2 value at bars < t0 (causal firewall)."""
        base = _ou_series(400, lam=-0.2, sigma=0.5, seed=42)
        spiked = base.copy()
        spiked.iloc[350] = base.iloc[350] * 5.0  # violent future bar

        mu_base = analytics.compute_ema(base, 20)
        mu_spk = analytics.compute_ema(spiked, 20)
        f_base = mrs.block2_features(base, mu_base, window=200, min_obs=120)
        f_spk = mrs.block2_features(spiked, mu_spk, window=200, min_obs=120)

        for col in ("drc", "hit_rate", "vr_agg"):
            a = f_base[col].to_numpy()[:350]
            b = f_spk[col].to_numpy()[:350]
            both = np.isfinite(a) & np.isfinite(b)
            assert both.sum() > 30, f"{col}: too few pre-spike values to test ({both.sum()})"
            assert np.array_equal(a[both], b[both]), f"{col}: future spike leaked into bars < t0"


# ── P3: Block 1 (Mean Reliability) & Block 3 (Tradability) ─────────────────────

class TestMeanStability:
    def test_flat_noisy_more_stable_than_trend(self):
        flat = _ou_series(400, lam=-0.2, sigma=0.5, seed=42)          # reverts around a level
        trend = pd.Series(100.0 + 0.5 * np.arange(400))              # strong drift
        ms_flat = mrs.mean_stability(flat, analytics.compute_ema(flat, 20))
        ms_trend = mrs.mean_stability(trend, analytics.compute_ema(trend, 20))
        assert ms_flat.dropna().mean() > ms_trend.dropna().mean()

    def test_stability_bounded_unit_interval(self):
        s = _ou_series(400, lam=-0.2, sigma=0.5, seed=3)
        ms = mrs.mean_stability(s, analytics.compute_ema(s, 20)).dropna()
        assert ms.min() >= 0.0 and ms.max() <= 1.0


class TestVarianceStability:
    def test_constant_vol_high_stability(self):
        s = _ou_series(400, lam=-0.2, sigma=0.5, seed=7)
        vs = mrs.variance_stability(s, analytics.compute_ema(s, 20)).dropna()
        assert vs.min() >= 0.0 and vs.max() <= 1.0
        assert vs.mean() > 0.4

    def test_vol_doubling_drives_stability_down(self):
        rng = np.random.default_rng(9)
        calm = rng.normal(0, 0.5, 200)
        wild = rng.normal(0, 2.0, 200)  # vol quadruples
        s = pd.Series(100.0 + np.cumsum(np.concatenate([calm, wild]) * 0.0) + np.concatenate([calm, wild]))
        vs = mrs.variance_stability(s, analytics.compute_ema(s, 20), w=20, k=20).dropna()
        assert vs.min() < 0.3, "a sharp vol regime change must push VarStab toward 0"


class TestStationarityPValues:
    def test_ou_more_stationary_than_rw(self):
        ou = _ou_series(150, lam=-0.3, sigma=0.5, seed=42)
        rw = _rw_series(150, seed=42)
        p_ou = mrs.adf_kpss_pvalues(ou, w=120)
        p_rw = mrs.adf_kpss_pvalues(rw, w=120)
        # ADF: lower p = stronger unit-root rejection = more stationary
        assert p_ou["p_adf"].dropna().iloc[-1] < p_rw["p_adf"].dropna().iloc[-1]


class TestHalflifeProximity:
    def test_scoring_matches_doc_anchor_points(self):
        # doc 01 §B3.1 prose band: peak at HL_opt=10, zeros at 2.5 and 40, half at 5 and 20.
        assert mrs.hl_proximity_value(10.0) == 1.0
        assert mrs.hl_proximity_value(2.5) < 1e-9
        assert mrs.hl_proximity_value(40.0) < 1e-9
        assert abs(mrs.hl_proximity_value(5.0) - 0.5) < 1e-9
        assert abs(mrs.hl_proximity_value(20.0) - 0.5) < 1e-9
        assert mrs.hl_proximity_value(None) == 0.0  # κ̂≤0 → not mean-reverting

    def test_random_walk_inherits_ema_residual_artifact(self):
        """DOCUMENTS A KNOWN LIMITATION: B3.1 reads half-life off the EMA RESIDUAL, which carries the
        EMA smoothing artifact (RW residual HL ≈ 6 bars — see test_analytics_validation). That HL lands
        inside the tradable band, so a pure random walk earns a moderate (NON-zero) half-life-proximity
        score. This is exactly why B2's forward-return DRC (artifact-resistant) carries 60% and B3 only
        20%. The researcher must NOT read a high B3.1 as evidence of genuine reversion."""
        rw = _rw_series(400, seed=42)
        hs = mrs.halflife_proximity(rw, analytics.compute_ema(rw, 20), window=200).dropna()
        assert (hs >= 0.0).all() and (hs <= 1.0).all()
        assert hs.mean() > 0.3, "the EMA-residual artifact gives RW a non-trivial HL-proximity score"


class TestVolCompression:
    def test_falling_vol_positive_rising_vol_negative(self):
        # high vol early, low vol late → late VC > 0 (compression)
        rng = np.random.default_rng(5)
        wild = rng.normal(0, 2.0, 200)
        calm = rng.normal(0, 0.3, 200)
        s = pd.Series(100.0 + np.cumsum(np.concatenate([wild, calm])))
        vc = mrs.vol_compression(s)
        assert vc["vc"].dropna().iloc[-1] > 0  # vol fell → compression positive


class TestTCF:
    def test_bounds_and_high_vol_low_score(self):
        rng = np.random.default_rng(6)
        calm = rng.normal(0, 0.3, 200)
        wild = rng.normal(0, 2.0, 200)
        s = pd.Series(100.0 + np.cumsum(np.concatenate([calm, wild])))
        tcf = mrs.tcf_score(s).dropna()
        assert tcf.min() >= 0.0 and tcf.max() <= 1.0
        # latest bar sits in a high-vol regime → TCF (=1−VP/100) should be low
        assert tcf.iloc[-1] < 0.5


# ── P4: master aggregation + API ───────────────────────────────────────────────

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


def _ou_csv(tmp_path, n=600, lam=-0.2, sigma=0.5, seed=42) -> str:
    s = _ou_series(n, lam=lam, sigma=sigma, seed=seed)
    path = tmp_path / "ou.csv"
    start = pd.Timestamp("2015-01-01")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "open", "high", "low", "close", "volume"])
        for i, v in enumerate(s):
            d = (start + pd.Timedelta(days=i)).strftime("%Y-%m-%d")
            w.writerow([d, v, v, v, v, 1000])
    return str(path)


class TestComputeMRScore:
    def test_master_equation_and_bounds(self):
        s = _ou_series(700, lam=-0.2, sigma=0.5, seed=42)
        mu = analytics.compute_ema(s, 20)
        df = mrs.compute_mrscore(s, mu)
        ok = df.dropna(subset=["mrscore", "b1", "b2", "b3"])
        assert len(ok) > 50
        # MRScore_t = 0.20·B1 + 0.60·B2 + 0.20·B3 (eq. 13), all in [0,100]
        recomposed = 0.20 * ok["b1"] + 0.60 * ok["b2"] + 0.20 * ok["b3"]
        assert np.allclose(ok["mrscore"], recomposed)
        assert ok["mrscore"].min() >= 0.0 and ok["mrscore"].max() <= 100.0

    def test_bit_identical_under_future_spike(self):
        """STANDING ACCEPTANCE BAR: a violent future bar must not change ANY MRScore at earlier bars."""
        base = _ou_series(450, lam=-0.2, sigma=0.5, seed=42)
        spiked = base.copy()
        spiked.iloc[420] = base.iloc[420] * 6.0
        kw = dict(rank_window=150, est_window=160, hl_window=120, adf_w=60, min_obs=120)
        a = mrs.compute_mrscore(base, analytics.compute_ema(base, 20), **kw)["mrscore"].to_numpy()[:420]
        b = mrs.compute_mrscore(spiked, analytics.compute_ema(spiked, 20), **kw)["mrscore"].to_numpy()[:420]
        both = np.isfinite(a) & np.isfinite(b)
        assert both.sum() > 30
        assert np.array_equal(a[both], b[both]), "future spike leaked into earlier MRScore values"

    def test_raw_drc_exposed_and_discriminates(self):
        """Per the normalization finding: the RAW DRC (artifact-resistant) must be carried in the
        output and must separate a reverter from a random walk (the self-ranked score does not)."""
        ou = _ou_series(700, lam=-0.2, sigma=0.5, seed=42)
        rw = _rw_series(700, seed=42)
        d_ou = mrs.compute_mrscore(ou, analytics.compute_ema(ou, 20))["drc"].dropna().mean()
        d_rw = mrs.compute_mrscore(rw, analytics.compute_ema(rw, 20))["drc"].dropna().mean()
        assert d_ou < d_rw - 1.0


class TestMRScoreAPI:
    def test_endpoint_shape_and_values(self, tmp_path, client, fresh_store):
        path = _ou_csv(tmp_path, n=600)
        client.post("/api/v1/market/load", json={"file_path": path, "instrument_id": "OU_T"})
        resp = client.get("/api/v1/market/OU_T/mrscore")
        assert resp.status_code == 200
        body = resp.json()
        assert body["instrument_id"] == "OU_T"
        assert len(body["rows"]) == 600
        scored = [r for r in body["rows"] if r["mrscore"] is not None]
        assert len(scored) > 30, "a 600-bar series should yield scored bars after warmup"
        r = scored[-1]
        for k in ("b1", "b2", "b3", "drc", "hit_rate", "vr_agg"):
            assert k in r
        assert 0.0 <= r["mrscore"] <= 100.0

    def test_end_param_respects_temporal_firewall(self, tmp_path, client, fresh_store):
        path = _ou_csv(tmp_path, n=600)
        client.post("/api/v1/market/load", json={"file_path": path, "instrument_id": "OU_E"})
        end = (pd.Timestamp("2015-01-01") + pd.Timedelta(days=549)).strftime("%Y-%m-%d")
        resp = client.get(f"/api/v1/market/OU_E/mrscore?end={end}")
        assert resp.status_code == 200
        assert len(resp.json()["rows"]) == 550

    def _spread_csv(self, tmp_path, n=600):
        # spread-like series crossing zero (the deployment domain — log-price is undefined here)
        vals = np.sin(np.linspace(0, 25, n)) * 5.0
        path = tmp_path / "spread.csv"
        start = pd.Timestamp("2015-01-01")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["date", "open", "high", "low", "close", "volume"])
            for i, v in enumerate(vals):
                d = (start + pd.Timedelta(days=i)).strftime("%Y-%m-%d")
                w.writerow([d, v, v, v, v, 1000])
        return str(path)

    def test_non_positive_prices_emit_explicit_warning(self, tmp_path, client, fresh_store):
        """C1: a spread/negative-price series must NOT silently return a blank score — it must carry
        an explicit data_warning so 'incompatible instrument' is distinguishable from 'unfavorable'."""
        path = self._spread_csv(tmp_path, n=600)
        client.post("/api/v1/market/load", json={"file_path": path, "instrument_id": "SPREAD_T"})
        resp = client.get("/api/v1/market/SPREAD_T/mrscore")
        assert resp.status_code == 200
        body = resp.json()
        assert body["data_warning"] is not None
        assert "non-positive" in body["data_warning"].lower()

    def test_positive_prices_have_no_data_warning(self, tmp_path, client, fresh_store):
        path = _ou_csv(tmp_path, n=600)
        client.post("/api/v1/market/load", json={"file_path": path, "instrument_id": "POS_T"})
        body = client.get("/api/v1/market/POS_T/mrscore").json()
        assert body["data_warning"] is None
