"""
Arm A engine — causal-firewall + ground-truth acceptance tests (doc 18 / doc 18a).

These GATE execution: no real-cohort VR is trusted until every test here is green. They prove the engine
is (a) causal (future cannot move an earlier β/spread — C-3), (b) negative-safe (VR defined through zero —
NP-1), (c) roll-aware (ADR_003 seam detection), and (d) not blind (recovers known OU<1 / RW≈1 / momentum>1
and separates a strong reverter from its matched RW surrogate while a pure RW does NOT separate).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.services import analytics_arm_a as A


# ── helpers ───────────────────────────────────────────────────────────────────

def _leg(prices: np.ndarray, start: str = "2000-01-03") -> pd.DataFrame:
    idx = pd.bdate_range(start, periods=len(prices), tz="UTC")
    p = np.asarray(prices, float)
    return pd.DataFrame({"open": p, "high": p, "low": p, "close": p}, index=idx)


def _spread_from_level(s: np.ndarray) -> A.Spread:
    n = len(s)
    return A.Spread(name="synthetic", s_close=np.asarray(s, float), s_open=np.asarray(s, float),
                    beta=np.ones(n), roll_transition=np.zeros(n, bool), flat_bar=np.zeros(n, bool),
                    index=pd.bdate_range("2000-01-03", periods=n, tz="UTC"), meta={})


def _ou_level(n, phi=0.9, sigma=1.0, seed=0):
    rng = np.random.default_rng(seed)
    s = np.empty(n); s[0] = 0.0
    e = rng.normal(0, sigma, n)
    for t in range(1, n):
        s[t] = phi * s[t - 1] + e[t]      # AR(1) around 0, stationary, sign-crossing
    return s


def _rw_level(n, sigma=1.0, seed=0, drift=0.0):
    rng = np.random.default_rng(seed)
    return np.concatenate([[0.0], np.cumsum(drift + rng.normal(0, sigma, n - 1))])


def _momentum_level(n, ar=0.4, sigma=1.0, seed=0):
    rng = np.random.default_rng(seed)
    incr = np.empty(n - 1); incr[0] = rng.normal(0, sigma)
    for t in range(1, n - 1):
        incr[t] = ar * incr[t - 1] + rng.normal(0, sigma)   # positively autocorrelated increments
    return np.concatenate([[0.0], np.cumsum(incr)])


# ── C-3: causal firewall (future-injection bit-identity) ───────────────────────

def test_rolling_beta_is_causal_under_future_injection():
    rng = np.random.default_rng(1)
    b = _rw_level(800, sigma=1.0, seed=2) + 100.0
    a = 1.7 * b + rng.normal(0, 1.0, 800) + 5.0
    leg_a, leg_b = _leg(a), _leg(b)
    base = A.construct_spread("t", leg_a, leg_b, beta_mode="rolling")
    k = 500
    a2 = a.copy(); a2[700:] += 9999.0           # detonate a FUTURE leg bar
    b2 = b.copy(); b2[700:] *= -3.0
    pert = A.construct_spread("t", _leg(a2), _leg(b2), beta_mode="rolling")
    np.testing.assert_array_equal(base.beta[:k + 1], pert.beta[:k + 1])      # β bit-identical ≤ k
    np.testing.assert_array_equal(base.s_close[:k + 1], pert.s_close[:k + 1])  # spread bit-identical ≤ k


def test_warmup_is_masked_not_imputed():
    b = _rw_level(400, seed=3) + 50.0
    a = 2.0 * b + 1.0
    sp = A.construct_spread("t", _leg(a), _leg(b), beta_mode="rolling", window=60)
    assert np.all(np.isnan(sp.beta[:60]))       # C-2: first W β are NaN
    assert np.all(np.isfinite(sp.beta[80:]))    # and finite once warmed up


# ── ADR_003: roll-seam detection ──────────────────────────────────────────────

def test_roll_transition_catches_seam_and_spares_normal_moves():
    s = _rw_level(400, sigma=0.5, seed=4) + 200.0
    s[250] += 60.0                              # ~30% raw-stitch seam (a roll jump)
    mask = A.roll_transition_mask(s)
    assert mask[250]                            # seam caught
    assert mask.sum() <= 3                      # and it is not flagging ordinary bars wholesale


# ── NP-1: negative-safe VR through zero ───────────────────────────────────────

def test_vr_is_finite_on_sign_crossing_spread():
    s = _ou_level(1000, phi=0.85, seed=5)       # crosses zero constantly
    assert (s < 0).any() and (s > 0).any()
    vr = A.level_vr(s, np.zeros(len(s), bool))
    for q in A.VR_Q_GRID:
        assert np.isfinite(vr[q]["vr"])         # no log-of-negative NaN


# ── "not blind": known character recovery ─────────────────────────────────────

def test_vr_recovers_known_character():
    ou = A.level_vr(_ou_level(4000, phi=0.9, seed=6), np.zeros(4000, bool))
    rw = A.level_vr(_rw_level(4000, seed=7), np.zeros(4000, bool))
    mom = A.level_vr(_momentum_level(4000, ar=0.4, seed=8), np.zeros(4000, bool))
    assert ou[10]["vr"] < 0.7                    # mean reversion → sub-diffusive
    assert 0.85 < rw[10]["vr"] < 1.15            # random walk → ≈ 1
    assert mom[10]["vr"] > 1.3                    # persistent increments → super-diffusive


# ── surrogate machinery: sensitivity + false-positive control ─────────────────

def test_rw_surrogate_ensemble_is_centered_near_one():
    sp = _spread_from_level(_rw_level(2000, seed=9))
    ens = A.surrogate_vr_ensemble(sp, "rw", n_draws=200, seed=0)
    for q in A.VR_Q_GRID:
        assert abs(np.median(ens[q]) - 1.0) < 0.1      # RW null VR centered at 1


def test_strong_reverter_separates_from_martingale_nulls():
    # positive control: a strong OU spread must separate (multiplicity-corrected) from the RW + GARCH
    # MARTINGALE nulls. It is EXPECTED *not* to beat a self-similar OU surrogate — documenting why
    # "must beat all three" cannot be the verdict gate without making the test vacuous.
    sp = _spread_from_level(_ou_level(3000, phi=0.8, seed=11))
    v = A.evaluate_spread(sp, seed=0)
    assert v.confirmed_martingale
    assert v.per_family["rw"]["min_vr_p_value"] < 0.05
    assert not v.confirmed_all_three


def test_pure_random_walk_does_not_confirm():
    # false-positive control: a pure RW must NOT confirm under the multiplicity-CORRECTED rule, even at
    # the seed where the NAIVE ≥1-of-4 rule false-positives at q=20 (this is the whole point of the fix).
    sp = _spread_from_level(_rw_level(3000, seed=12))
    v = A.evaluate_spread(sp, seed=0)
    assert not v.confirmed_martingale
    assert not v.confirmed_all_three
    assert v.per_family["rw"]["min_vr_p_value"] >= 0.05      # corrected p-value is NOT significant


def test_naive_per_horizon_rule_is_fpr_inflated():
    # documents the multiplicity problem the corrected statistic fixes: the naive ≥1-of-4 rule DOES
    # fire on this pure-RW draw (at q=20), which is exactly why it is not the verdict rule.
    sp = _spread_from_level(_rw_level(3000, seed=12))
    v = A.evaluate_spread(sp, seed=0)
    assert 20 in v.separated_horizons["rw"]                  # naive per-horizon false-positive present
