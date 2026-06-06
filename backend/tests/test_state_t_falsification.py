"""State T existence — Phase 3 falsification GUARDS (doc 11 §5). Deterministic (fixed seeds).

These are standing method-validity assertions, NOT a State-T claim:
  (1) NO-FALSE-POSITIVE — OU/RW real vs same-process null produce ~0 effect. The method must not
      manufacture "State-T morphology" out of ordinary mean reversion or random walk.
  (2) SENSITIVITY (positive control) — a clean stabilize-then-revert object MUST show the
      pre-registered directions (innov_var↓, acf1↓, dir_eff↓). Guards against blind descriptors;
      without it a null real-data result would be uninterpretable.

If (1) ever fails → the existence machinery hallucinates and any real finding is void.
If (2) ever fails → the descriptors are blind and a null real-data result means nothing.
"""
import numpy as np
import pandas as pd

from app.services import analytics_state_t as st
from app.services import synthetic

N, W = 800, 30
NULL_SEEDS = range(200, 212)
REAL_SEEDS = range(0, 6)
THETAS = (1.0, 1.5, 2.0)


def _ou(s: int) -> pd.Series:
    return pd.Series(synthetic.ou(lam=-0.1, sigma=1.0, n=N, seed=s).prices)


def _rw(s: int) -> pd.Series:
    return pd.Series(synthetic.random_walk(sigma=1.0, n=N, seed=s).prices)


def _clean_control(seed: int) -> pd.Series:
    """Clean positive control: vol compresses monotonically with |dev|, reversion always strong."""
    rng = np.random.default_rng(seed)
    d = np.zeros(N)
    for t in range(1, N):
        dev = d[t - 1]
        d[t] = dev + (-0.40) * dev + rng.normal(0.0, 1.0 / (1.0 + 0.30 * abs(dev)))
    return pd.Series(100.0 + d)


def _pooled(series_list, theta, desc):
    cat = pd.concat([st.extract(s, theta=theta, W=W) for s in series_list], ignore_index=True)
    return cat[desc].to_numpy(dtype=float)


def _effect(real_list, null_list, theta, desc):
    return st.cohens_d(_pooled(real_list, theta, desc), _pooled(null_list, theta, desc))


class TestNoFalsePositive:
    """Ordinary mean reversion / random walk must NOT look like State T."""

    def test_ou_real_indistinguishable_from_ou_null(self):
        real = [_ou(s) for s in REAL_SEEDS]
        null = [_ou(s) for s in NULL_SEEDS]
        for theta in THETAS:
            for desc in st.DESCRIPTORS:
                d = _effect(real, null, theta, desc)
                assert abs(d) < 0.3, f"OU false positive: {desc}@θ={theta} d={d:.3f}"

    def test_rw_real_indistinguishable_from_rw_null(self):
        real = [_rw(s) for s in REAL_SEEDS]
        null = [_rw(s) for s in NULL_SEEDS]
        for theta in THETAS:
            for desc in st.DESCRIPTORS:
                d = _effect(real, null, theta, desc)
                assert abs(d) < 0.3, f"RW false positive: {desc}@θ={theta} d={d:.3f}"


class TestSensitivity:
    """A genuine stabilize-then-revert object MUST show the pre-registered directions."""

    def test_positive_control_shows_preregistered_directions(self):
        real = [_clean_control(s) for s in REAL_SEEDS]
        null = [_ou(s) for s in NULL_SEEDS]
        for theta in THETAS:
            d_iv = _effect(real, null, theta, "innov_var")
            d_acf = _effect(real, null, theta, "acf1")
            d_de = _effect(real, null, theta, "dir_eff")
            assert d_iv < -0.8, f"innov_var not ↓ @θ={theta}: d={d_iv:.3f}"
            assert d_acf < -0.8, f"acf1 not ↓ @θ={theta}: d={d_acf:.3f}"
            assert d_de < -0.4, f"dir_eff not ↓ @θ={theta}: d={d_de:.3f}"

    def test_positive_control_clearly_exceeds_ou_baseline(self):
        """Planted signal must dominate the OU-vs-OU sampling baseline (separability)."""
        ctrl = [_clean_control(s) for s in REAL_SEEDS]
        ou_real = [_ou(s) for s in REAL_SEEDS]
        null = [_ou(s) for s in NULL_SEEDS]
        for desc in st.DESCRIPTORS:
            baseline = abs(_effect(ou_real, null, 1.5, desc))
            signal = abs(_effect(ctrl, null, 1.5, desc))
            assert signal > baseline + 0.3, f"{desc}: signal {signal:.3f} not clear of baseline {baseline:.3f}"
