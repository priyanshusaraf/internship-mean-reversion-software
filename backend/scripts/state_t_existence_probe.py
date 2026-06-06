"""State T existence — Phase 3 synthetic falsification battery (doc 11 §5).

Reproducible (fixed seeds). Measures effect sizes of high-|z| window morphology, real-candidate vs
pooled synthetic NULL, under identical causal Arm-1 extraction. Two questions:

  (1) NO-FALSE-POSITIVE: OU-as-real vs OU-null (disjoint seeds) must be ~0. If ordinary mean
      reversion alone reproduces "State T morphology", the thesis is falsified-by-construction.
  (2) SENSITIVITY (positive control): a process with PLANTED stabilization+chop inside high-|z|
      zones must show the pre-registered directions. If it doesn't, the descriptors are blind and a
      null real-data result would be uninterpretable.

Pre-registered directions (doc 11 §4), high-|z| vs null, IF a real T-like phenomenon exists:
  innov_var ↓ (negative d) · acf1 ↓ (negative d) · dir_eff ↓ (negative d).

Run:  .venv/bin/python scripts/state_t_existence_probe.py
"""
import numpy as np
import pandas as pd

from app.services import analytics_state_t as st
from app.services import synthetic

THETAS = (1.0, 1.5, 2.0)
W = 30
N = 800
NULL_SEEDS = range(200, 212)   # 12 disjoint null seeds (pooled)
REAL_SEEDS = range(0, 6)       # 6 disjoint real-candidate seeds (pooled)


def _ou(seed: int) -> pd.Series:
    return pd.Series(synthetic.ou(lam=-0.1, sigma=1.0, n=N, seed=seed).prices)


def _rw(seed: int) -> pd.Series:
    return pd.Series(synthetic.random_walk(sigma=1.0, n=N, seed=seed).prices)


def _planted(seed: int) -> pd.Series:
    """Positive control: a clean 'stabilize-then-revert' object. Innovation vol compresses
    MONOTONICALLY with |deviation| and reversion is always strong — so large-deviation windows show
    low innovation variance, strongly negative innovation autocorr, and low path efficiency (chop).
    This is the literal embodiment of the pre-registered signature (doc 11 §4).

    REJECTED first design (recorded, no revisionism — doc 11 §7): a two-regime OU with a compressed
    high-|dev| zone (σ=0.25,λ=−0.45) and a near-RW quiet zone (σ=1.0,λ=−0.04). It FAILED as a control:
    its high-|z| windows are dominated by the trendy quiet APPROACH, so it read +innov_var/+dir_eff
    (opposite sign) — it was not a clean instance of 'stabilization', not a method defect."""
    rng = np.random.default_rng(seed)
    d = np.zeros(N)
    for t in range(1, N):
        dev = d[t - 1]
        sigma = 1.0 / (1.0 + 0.30 * abs(dev))  # vol compresses as deviation grows
        d[t] = dev + (-0.40) * dev + rng.normal(0.0, sigma)  # always-strong reversion
    return pd.Series(100.0 + d)


def _pooled_descriptors(series_list: list[pd.Series], theta: float) -> dict[str, np.ndarray]:
    frames = [st.extract(s, theta=theta, W=W) for s in series_list]
    cat = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=st.DESCRIPTORS)
    return {d: cat[d].to_numpy(dtype=float) for d in st.DESCRIPTORS}


def _table(real_pool: dict, null_pool: dict, label: str) -> None:
    print(f"\n=== {label} ===")
    print(f"{'theta':>6} {'descriptor':>12} {'d(real-null)':>14} {'n_real':>8} {'n_null':>8}")
    for theta in THETAS:
        rp = _pooled_descriptors(real_pool, theta)
        npd = _pooled_descriptors(null_pool, theta)
        for desc in st.DESCRIPTORS:
            d = st.cohens_d(rp[desc], npd[desc])
            nr = int(np.isfinite(rp[desc]).sum())
            nn = int(np.isfinite(npd[desc]).sum())
            print(f"{theta:>6} {desc:>12} {d:>14.3f} {nr:>8} {nn:>8}")


def main() -> None:
    ou_null = [_ou(s) for s in NULL_SEEDS]
    rw_null = [_rw(s) for s in NULL_SEEDS]

    ou_real = [_ou(s) for s in REAL_SEEDS]      # no-false-positive: must be ~0 vs ou_null
    rw_real = [_rw(s) for s in REAL_SEEDS]
    planted = [_planted(s) for s in REAL_SEEDS]  # positive control: must show ↓↓↓

    _table(ou_real, ou_null, "(1) NO-FALSE-POSITIVE  OU-real vs OU-null   [expect d≈0]")
    _table(rw_real, rw_null, "(1) NO-FALSE-POSITIVE  RW-real vs RW-null   [expect d≈0]")
    _table(planted, ou_null, "(2) POSITIVE CONTROL   planted vs OU-null   [expect innov_var↓ acf1↓ dir_eff↓]")


if __name__ == "__main__":
    main()
