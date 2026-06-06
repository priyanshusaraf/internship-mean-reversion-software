"""
State T — Observational Existence Programme v1 (doc 11). ARM 1 (CAUSAL, verdict-bearing) only.

We are testing whether a phenomenon EXISTS — not building the phenomenon. This is NOT State T, NOT a
detector, NOT timing, NOT hazard. Output is a distributional comparison (real high-|z| window
morphology vs matched synthetic nulls), never a per-bar quantity, never a score/label.

Binding architecture (doc 11 §2): Arm 1 selects windows by a multi-θ SYMMETRIC partition on the
CAUSAL z-score (|z| ≥ θ), evaluable at t — no forward outcome selection, no reversion anchoring.

Temporal-honesty invariant under test (the way we could fool ourselves): a window anchored at bar t,
and its descriptors, depend ONLY on data ≤ t. Perturbing bars > t must not change anything at t.
"""
import numpy as np
import pandas as pd

from app.services import analytics_state_t as st


# ── synthetic habitats (mirror test_substrate / test_synthetic_nulls conventions) ──

def _ou_series(n: int, lam: float = -0.1, sigma: float = 1.0, base: float = 100.0, seed: int = 42) -> pd.Series:
    rng = np.random.default_rng(seed)
    d = [0.0]
    for _ in range(n - 1):
        d.append(d[-1] + lam * d[-1] + rng.normal(0, sigma))
    return pd.Series(base + np.asarray(d))


def _rw_series(n: int, sigma: float = 1.0, base: float = 100.0, seed: int = 42) -> pd.Series:
    rng = np.random.default_rng(seed)
    steps = rng.normal(0, sigma, n)
    steps[0] = 0.0
    return pd.Series(base + np.cumsum(steps))


# ── P2.1: symmetric partition anchors ─────────────────────────────────────────

class TestPartitionAnchors:
    def test_selects_both_signs_above_theta(self):
        z = pd.Series([0.0, 1.5, -2.0, 0.5, -0.9, 3.0])
        idx = st.partition_anchors(z, theta=1.0)
        assert list(idx) == [1, 2, 5]  # symmetric: |z| ≥ θ regardless of sign

    def test_higher_theta_is_subset(self):
        z = pd.Series([0.0, 1.2, -1.7, 2.5, -0.3, 1.05])
        lo = set(st.partition_anchors(z, theta=1.0).tolist())
        hi = set(st.partition_anchors(z, theta=2.0).tolist())
        assert hi.issubset(lo)

    def test_nan_z_never_anchored(self):
        z = pd.Series([np.nan, np.nan, 5.0, np.nan])
        idx = st.partition_anchors(z, theta=1.0)
        assert list(idx) == [2]


# ── P2.2: causal pre-windows ──────────────────────────────────────────────────

class TestCausalWindows:
    def test_window_is_trailing_inclusive_length_W(self):
        v = np.arange(10.0)
        wins = st.causal_windows(v, anchors=np.array([5]), W=3)
        assert len(wins) == 1
        np.testing.assert_array_equal(wins[0], np.array([3.0, 4.0, 5.0]))  # [t-W+1, t]

    def test_anchor_with_insufficient_history_dropped(self):
        v = np.arange(10.0)
        wins = st.causal_windows(v, anchors=np.array([1, 5]), W=3)
        assert len(wins) == 1  # anchor t=1 has < W bars of history → dropped


# ── P2.3: window descriptors ──────────────────────────────────────────────────

class TestWindowDescriptors:
    def test_keys_present(self):
        d = st.window_descriptors(np.array([1.0, -1.0, 1.0, -1.0]), np.array([100.0, 101.0, 100.0, 101.0]))
        assert set(d) == {"innov_var", "acf1", "dir_eff"}

    def test_innov_var_matches_numpy(self):
        eps = np.array([1.0, 2.0, 3.0, 2.0, 1.0])
        d = st.window_descriptors(eps, np.arange(5.0))
        assert abs(d["innov_var"] - float(np.std(eps, ddof=1))) < 1e-12

    def test_dir_eff_one_on_straight_path(self):
        d = st.window_descriptors(np.zeros(5), np.linspace(100.0, 110.0, 5))
        assert abs(d["dir_eff"] - 1.0) < 1e-12

    def test_acf1_in_range(self):
        rng = np.random.default_rng(0)
        d = st.window_descriptors(rng.normal(0, 1, 50), np.cumsum(rng.normal(0, 1, 50)) + 100)
        assert -1.0 <= d["acf1"] <= 1.0


# ── P2.4: extract pipeline (causal) ───────────────────────────────────────────

class TestExtract:
    def test_returns_one_row_per_valid_anchor(self):
        close = _ou_series(600, seed=1)
        df = st.extract(close, theta=1.0, W=30)
        assert set(["anchor", "innov_var", "acf1", "dir_eff"]).issubset(df.columns)
        assert len(df) > 0
        assert df["anchor"].is_monotonic_increasing

    def test_freeze_causal_invariance_to_future(self):
        """THE freeze test. Descriptors at anchor t must be bit-identical when bars > t change."""
        close = _ou_series(600, seed=7)
        close_mod = close.copy()
        close_mod.iloc[400:] = close_mod.iloc[400:] + 50.0  # perturb the future only

        a = st.extract(close, theta=1.0, W=30)
        b = st.extract(close_mod, theta=1.0, W=30)

        cut = 380  # anchors strictly before the perturbation (z-window=60, well clear)
        a_pre = a[a["anchor"] <= cut].reset_index(drop=True)
        b_pre = b[b["anchor"] <= cut].reset_index(drop=True)

        assert len(a_pre) > 0
        pd.testing.assert_frame_equal(a_pre, b_pre)


# ── P2.5: distributional comparison vs nulls ──────────────────────────────────

class TestNullComparison:
    def test_cohens_d_zero_for_identical(self):
        x = np.array([1.0, 2.0, 3.0, 4.0])
        assert abs(st.cohens_d(x, x)) < 1e-12

    def test_cohens_d_sign(self):
        lo = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
        hi = np.array([5.0, 5.1, 4.9, 5.0, 5.0])
        assert st.cohens_d(hi, lo) > 0
        assert st.cohens_d(lo, hi) < 0

    def test_compare_to_nulls_structure(self):
        real = _ou_series(600, seed=1)
        nulls = {"ou": _ou_series(600, seed=99), "rw": _rw_series(600, seed=99)}
        res = st.compare_to_nulls(real, nulls=nulls, thetas=(1.0, 1.5, 2.0), W=30)
        # one effect-size row per (theta, null, descriptor)
        assert set(["theta", "null", "descriptor", "d", "n_real", "n_null"]).issubset(res.columns)
        assert set(res["theta"].unique()) == {1.0, 1.5, 2.0}
        assert set(res["null"].unique()) == {"ou", "rw"}
        assert set(res["descriptor"].unique()) == {"innov_var", "acf1", "dir_eff"}
