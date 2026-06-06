"""
Synthetic data generators for the Anchored Kalman μ* validation harness (spec v1, §5.0).

Each generator produces a price series with KNOWN ground truth (true deviation, trend,
switch points, break location). The validation gates in §5 measure the estimator against
this ground truth — there is no way to recover mean reversion that was never injected, so
these generators are the falsification substrate.

Discrete-time conventions (T = 1 bar throughout):
  OU deviation:  d_t = d_{t-1} + lam * d_{t-1} + eps_t,   eps ~ N(0, sigma^2)
                 → AR(1) coefficient phi = 1 + lam,  ACF(1) = phi
                 → half-life = -ln(2) / lam   (matches analytics.compute_halflife)
  lam must be in (-1, 0) for stationary mean reversion.

All randomness flows through np.random.default_rng(seed) so every series is reproducible.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class SyntheticSeries:
    """A synthetic price path plus whatever ground truth the generator can expose.

    prices     : the observable close series (what the estimator consumes)
    deviation  : true mean-reverting deviation component, if one was injected (else None)
    trend      : true deterministic/level component, if one exists (else None)
    meta       : generator name + parameters + derived ground-truth scalars
    """
    prices: np.ndarray
    deviation: np.ndarray | None = None
    trend: np.ndarray | None = None
    meta: dict = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.prices)


def _ou_deviation(lam: float, sigma: float, n: int, rng: np.random.Generator) -> np.ndarray:
    """Zero-anchored OU deviation: d_t = d_{t-1} + lam*d_{t-1} + eps_t, d_0 = 0."""
    d = np.empty(n)
    d[0] = 0.0
    eps = rng.normal(0.0, sigma, n)
    for t in range(1, n):
        d[t] = d[t - 1] + lam * d[t - 1] + eps[t]
    return d


def ou(lam: float = -0.1, sigma: float = 1.0, n: int = 500, seed: int = 0,
       base: float = 100.0) -> SyntheticSeries:
    """Stationary OU process around a constant level `base`. No trend.

    Ground truth: deviation = OU component, half-life = -ln2/lam, acf1 = 1+lam.
    """
    rng = np.random.default_rng(seed)
    dev = _ou_deviation(lam, sigma, n, rng)
    prices = base + dev
    return SyntheticSeries(
        prices=prices,
        deviation=dev,
        trend=np.full(n, base),
        meta={
            "kind": "ou", "lam": lam, "sigma": sigma, "n": n, "seed": seed, "base": base,
            "true_halflife": -np.log(2) / lam,
            "true_acf1": 1.0 + lam,
        },
    )


def random_walk(sigma: float = 1.0, n: int = 500, seed: int = 0,
                base: float = 100.0) -> SyntheticSeries:
    """Pure random walk: P_t = P_{t-1} + eps_t. No mean reversion exists.

    The falsification benchmark: a correct estimator must NOT manufacture persistence here.
    """
    rng = np.random.default_rng(seed)
    steps = rng.normal(0.0, sigma, n)
    steps[0] = 0.0
    prices = base + np.cumsum(steps)
    return SyntheticSeries(
        prices=prices,
        deviation=None,
        trend=None,
        meta={"kind": "random_walk", "sigma": sigma, "n": n, "seed": seed, "base": base},
    )


def drift_random_walk(mu: float = 0.1, sigma: float = 1.0, n: int = 500, seed: int = 0,
                      base: float = 100.0) -> SyntheticSeries:
    """Random walk WITH constant drift: P_t = P_{t-1} + mu + eps_t.  No mean reversion exists.

    Distinct from `trend()`: `trend()` is trend-STATIONARY (price reverts to a deterministic
    line base+slope*t). This is a unit-root STOCHASTIC trend — the level wanders without bound
    and never reverts to any line. The #11 N2 null: a persistent trend whose causal-EMA lag can
    *look* like equilibrium structure even though no equilibrium exists.

    With mu=0 and the same seed this is bit-identical to `random_walk(...)` — drift is the only
    addition, so the underlying process is provably the pure RW (guards "null embeds MR").
    """
    rng = np.random.default_rng(seed)
    steps = mu + rng.normal(0.0, sigma, n)
    steps[0] = 0.0
    prices = base + np.cumsum(steps)
    return SyntheticSeries(
        prices=prices,
        deviation=None,
        trend=None,
        meta={"kind": "drift_random_walk", "mu": mu, "sigma": sigma, "n": n, "seed": seed,
              "base": base},
    )


def trend(slope: float = 0.1, sigma: float = 1.0, n: int = 500, seed: int = 0,
          base: float = 100.0) -> SyntheticSeries:
    """Deterministic linear drift + iid noise. No reversion: noise is white, not OU.

    Used by G-IDENT: a velocity-aware filter must remove the lag bias that EMA suffers
    here, otherwise it is "EMA with extra math".
    """
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    true_trend = base + slope * t
    noise = rng.normal(0.0, sigma, n)
    prices = true_trend + noise
    return SyntheticSeries(
        prices=prices,
        deviation=noise,
        trend=true_trend,
        meta={"kind": "trend", "slope": slope, "sigma": sigma, "n": n, "seed": seed,
              "base": base},
    )


def ou_in_trend(lam: float = -0.1, sigma: float = 1.0, slope: float = 0.1,
                n: int = 500, seed: int = 0, base: float = 100.0) -> SyntheticSeries:
    """OU deviation injected AROUND a linear trend. The core-thesis substrate.

    Ground truth: deviation = OU component (the tradable reversion), trend = base+slope*t.
    H3/G-ABSORB measure whether the filter recovers the embedded OU half-life while its
    velocity tracks the trend (and does NOT absorb the deviation).
    """
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    true_trend = base + slope * t
    dev = _ou_deviation(lam, sigma, n, rng)
    prices = true_trend + dev
    return SyntheticSeries(
        prices=prices,
        deviation=dev,
        trend=true_trend,
        meta={
            "kind": "ou_in_trend", "lam": lam, "sigma": sigma, "slope": slope,
            "n": n, "seed": seed, "base": base,
            "true_halflife": -np.log(2) / lam,
            "true_acf1": 1.0 + lam,
        },
    )


def regime_switch(segments: list[tuple[str, dict]] | None = None, seed: int = 0,
                  base: float = 100.0) -> SyntheticSeries:
    """Concatenated regimes (e.g. trend → OU → trend) with continuity at the joins.

    Each segment is (kind, params) where kind in {"trend", "ou"} and params carries the
    per-segment knobs (slope/lam/sigma/length). Each new segment starts at the previous
    segment's last level. Switch points and per-bar regime labels are returned in meta.
    """
    if segments is None:
        segments = [
            ("trend", {"slope": 0.3, "sigma": 1.0, "length": 150}),
            ("ou", {"lam": -0.15, "sigma": 1.5, "length": 200}),
            ("trend", {"slope": -0.25, "sigma": 1.0, "length": 150}),
        ]
    rng = np.random.default_rng(seed)
    prices: list[float] = []
    labels: list[str] = []
    switch_points: list[int] = []
    level = base

    for kind, p in segments:
        length = int(p.get("length", 150))
        if prices:
            switch_points.append(len(prices))
        if kind == "trend":
            slope = p.get("slope", 0.2)
            sigma = p.get("sigma", 1.0)
            noise = rng.normal(0.0, sigma, length)
            seg = level + slope * np.arange(1, length + 1) + noise
        elif kind == "ou":
            lam = p.get("lam", -0.1)
            sigma = p.get("sigma", 1.0)
            dev = _ou_deviation(lam, sigma, length, rng)
            seg = level + dev
        else:
            raise ValueError(f"Unknown regime kind: {kind!r}")
        prices.extend(seg.tolist())
        labels.extend([kind] * length)
        level = float(seg[-1])

    return SyntheticSeries(
        prices=np.asarray(prices),
        deviation=None,
        trend=None,
        meta={"kind": "regime_switch", "segments": segments, "seed": seed,
              "switch_points": switch_points, "labels": labels, "base": base},
    )


def structural_break(jump_size: float = 30.0, at: int = 250, n: int = 500,
                     lam: float = -0.1, sigma: float = 1.0, seed: int = 0,
                     base: float = 100.0) -> SyntheticSeries:
    """OU around a level that steps by `jump_size` at index `at`. Tests shock recovery.

    V-BRK requires μ* to recover within 3× effective span with no sustained ringing.
    """
    rng = np.random.default_rng(seed)
    dev = _ou_deviation(lam, sigma, n, rng)
    level = np.full(n, base)
    level[at:] += jump_size
    prices = level + dev
    return SyntheticSeries(
        prices=prices,
        deviation=dev,
        trend=level,
        meta={"kind": "structural_break", "jump_size": jump_size, "at": at, "lam": lam,
              "sigma": sigma, "n": n, "seed": seed, "base": base,
              "true_halflife": -np.log(2) / lam},
    )


def vol_cluster(base_sigma: float = 1.0, n: int = 500, seed: int = 0, lam: float = -0.1,
                omega: float = 0.1, alpha: float = 0.1, beta: float = 0.85,
                base: float = 100.0) -> SyntheticSeries:
    """OU deviation driven by GARCH(1,1)-like time-varying volatility.

    sigma2_t = omega + alpha*eps_{t-1}^2 + beta*sigma2_{t-1}. Tests whether the FROZEN
    (constant-Q/R) SNR survives heteroskedasticity without per-instrument refitting (V-VOL).
    """
    rng = np.random.default_rng(seed)
    sigma2 = np.empty(n)
    eps = np.empty(n)
    sigma2[0] = base_sigma ** 2
    eps[0] = rng.normal(0.0, np.sqrt(sigma2[0]))
    for t in range(1, n):
        sigma2[t] = omega + alpha * eps[t - 1] ** 2 + beta * sigma2[t - 1]
        eps[t] = rng.normal(0.0, np.sqrt(sigma2[t]))
    # OU recursion driven by the heteroskedastic innovations
    d = np.empty(n)
    d[0] = 0.0
    for t in range(1, n):
        d[t] = d[t - 1] + lam * d[t - 1] + eps[t]
    prices = base + d
    return SyntheticSeries(
        prices=prices,
        deviation=d,
        trend=np.full(n, base),
        meta={"kind": "vol_cluster", "base_sigma": base_sigma, "lam": lam, "omega": omega,
              "alpha": alpha, "beta": beta, "n": n, "seed": seed, "base": base,
              "true_halflife": -np.log(2) / lam},
    )


def jump(intensity: float = 0.02, jump_size: float = 10.0, n: int = 500, seed: int = 0,
         lam: float = -0.1, sigma: float = 1.0, base: float = 100.0) -> SyntheticSeries:
    """OU deviation plus Poisson-timed level jumps. OBSERVE-ONLY (no §5 gate).

    Jumps have random sign and ~Exp(jump_size) magnitude at Bernoulli(intensity) times.
    """
    rng = np.random.default_rng(seed)
    dev = _ou_deviation(lam, sigma, n, rng)
    jumps = np.zeros(n)
    occur = rng.random(n) < intensity
    signs = rng.choice([-1.0, 1.0], size=n)
    mags = rng.exponential(jump_size, size=n)
    jumps[occur] = (signs * mags)[occur]
    level = base + np.cumsum(jumps)
    prices = level + dev
    return SyntheticSeries(
        prices=prices,
        deviation=dev,
        trend=level,
        meta={"kind": "jump", "intensity": intensity, "jump_size": jump_size, "lam": lam,
              "sigma": sigma, "n": n, "seed": seed, "base": base,
              "jump_indices": np.flatnonzero(occur).tolist()},
    )
