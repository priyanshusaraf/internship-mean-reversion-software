"""
Step 2A — velocity-absorption instrumentation tests (minimal, structural).

These lock the three properties the false-centering falsification depends on:
  1. The restoration identity   ε^R = ε^K + δ = close − EMA_match(pred)   holds exactly.
  2. Causal firewall: a future bar cannot change δ / residuals at earlier bars.
  3. Sanity: on synthetic OU-in-trend, the walk-forward decay test runs and returns finite β.

The frozen estimator is NOT exercised for tuning here — only that compute_velocity_absorption
recovers μ_{t|t−1} from its output by subtraction without recomputation.
"""
import numpy as np
import pandas as pd

from app.services import analytics, synthetic


def test_restoration_identity():
    """ε^R = ε^K + δ, and ε^R = close − matched-EMA prediction, to numerical precision."""
    st = synthetic.ou_in_trend(lam=-0.1, sigma=1.0, slope=0.25, n=600, seed=3)
    close = pd.Series(st.prices)
    va = analytics.compute_velocity_absorption(close)

    eps_k = va["eps_kalman"]
    eps_r = va["eps_restored"]
    delta = va["delta"]

    # Identity holds wherever δ is defined (t ≥ 1).
    m = np.isfinite(delta)
    assert np.allclose(eps_r[m], eps_k[m] + delta[m], atol=1e-9)

    # ε^R equals close − matched-EMA one-step prediction, independently reconstructed.
    span_m = va["matched_span"]
    ema_m = analytics.compute_ema(close, span=span_m).to_numpy()
    emap = np.full(len(close), np.nan)
    emap[1:] = ema_m[:-1]
    assert np.allclose(eps_r[m], (st.prices - emap)[m], atol=1e-9)


def test_matched_span_from_frozen_gain():
    """Matched span derives from the frozen steady-state gain and is a fixed, sane number."""
    st = synthetic.ou_in_trend(lam=-0.1, sigma=1.0, slope=0.1, n=400, seed=1)
    va = analytics.compute_velocity_absorption(pd.Series(st.prices))
    g = analytics.kalman_steady_state_gain()
    assert 0.0 < g < 1.0
    assert va["matched_span"] == max(2, int(round(2.0 / g - 1.0)))
    assert va["matched_span"] > 1


def test_causal_firewall_on_delta():
    """δ and residuals at early bars are unchanged whether the series ends early or extends past
    a large future spike — no lookahead in the instrumentation."""
    st = synthetic.ou_in_trend(lam=-0.1, sigma=1.0, slope=0.2, n=400, seed=7)
    prices = st.prices.copy()

    short = analytics.compute_velocity_absorption(pd.Series(prices[:300]))
    long_prices = prices.copy()
    long_prices[350] += 100.0  # violent future spike beyond bar 300
    long = analytics.compute_velocity_absorption(pd.Series(long_prices))

    # Compare δ and ε^K on bars [1, 300): they must be bit-identical.
    ds, dl = short["delta"], long["delta"]
    ks, kl = short["eps_kalman"], long["eps_kalman"]
    sl = slice(1, 300)
    assert np.allclose(ds[sl], dl[sl], atol=1e-9, equal_nan=True)
    assert np.allclose(ks[sl], kl[sl], atol=1e-9)


def test_walk_forward_runs_and_is_finite():
    """On OU-in-trend the decay test returns finite β / R² for both systems at both horizons."""
    st = synthetic.ou_in_trend(lam=-0.1, sigma=1.0, slope=0.25, n=900, seed=11)
    va = analytics.compute_velocity_absorption(pd.Series(st.prices))
    for system in ("kalman", "restored"):
        for h in va["horizons"]:
            r = va["reversion"][system][h]
            assert r["n"] > 0
            assert np.isfinite(r["beta"]), f"{system} h={h} beta not finite"
            assert np.isfinite(r["r2"]), f"{system} h={h} r2 not finite"
