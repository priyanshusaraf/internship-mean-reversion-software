"""#11 null-generator construction checks (metric-free; guards 'null embeds MR').

No variance-ratio / statistical reversion test here (frozen modification: no metric surface).
We only verify the generators are what they claim BY CONSTRUCTION.
"""
import numpy as np

from app.services import synthetic


def test_drift_rw_zero_drift_is_pure_random_walk():
    """mu=0 must reproduce the pure random walk bit-for-bit → drift is the ONLY addition,
    so the base process is provably the unit-root RW (no injected reversion)."""
    rw = synthetic.random_walk(sigma=2.0, n=300, seed=7, base=500.0)
    drw = synthetic.drift_random_walk(mu=0.0, sigma=2.0, n=300, seed=7, base=500.0)
    np.testing.assert_allclose(drw.prices, rw.prices)
    assert drw.deviation is None and drw.trend is None  # no equilibrium component exists


def test_drift_rw_is_cumsum_of_drift_plus_noise():
    """Exact construction: P = base + cumsum(mu + eps), first step zeroed (P_0 = base)."""
    mu, sigma, n, seed, base = 0.5, 1.5, 250, 3, 100.0
    drw = synthetic.drift_random_walk(mu=mu, sigma=sigma, n=n, seed=seed, base=base)
    rng = np.random.default_rng(seed)
    steps = mu + rng.normal(0.0, sigma, n)
    steps[0] = 0.0
    np.testing.assert_allclose(drw.prices, base + np.cumsum(steps))
    assert drw.prices[0] == base


def test_drift_rw_differs_from_trend_stationary():
    """N2 (unit-root stochastic trend) must NOT equal trend() (trend-stationary), even though
    both 'go up' — they are different processes (one reverts to a line, one does not)."""
    drw = synthetic.drift_random_walk(mu=0.3, sigma=1.0, n=400, seed=1, base=100.0)
    tr = synthetic.trend(slope=0.3, sigma=1.0, n=400, seed=1, base=100.0)
    assert not np.allclose(drw.prices, tr.prices)
