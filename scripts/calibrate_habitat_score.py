"""
MR Habitat Score — Calibration Gate
Runs ONLY on synthetic ground truth. Must pass BEFORE real-data use.

Calibration criteria (pre-committed):
  OU process        → score HIGH  (≥ 65)
  Random walk       → score NEUTRAL (~50, accept 35–65)
  Pure trend        → score NOT HIGH  (≤ 65)

If any criterion inverts → STOP; fix score before T2.5.

Score definition:
  On a price window of length H, compute min VR over q ∈ {5,10,20}.
  Build matched RW nulls (vol-matched iid) + MA(1) nulls from the window's own increments.
  Habitat score = fraction of nulls LESS sub-diffusive than real (i.e. fraction with VR ≥ real_VR),
  mapped to 0–100. High = more reverting than null.

Note: score is never self-ranked against the instrument's own history (avoids MRScore inversion bug).
"""
from __future__ import annotations
import sys, os
import numpy as np

# Import shim — single null-generating code path lives in the backend engine (contract M3).
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
from app.services.analytics_habitat import (  # noqa: E402
    habitat_score_full,
    vr_q,
    min_vr,
    VR_QS,
    NS_NULL,
    SEED_CAL,
)

VENV_PYTHON = True  # running in backend venv

# Synthetic ground-truth parameters
H           = 40                    # forward window length (same as live test)
N_TRIALS    = 200                   # synthetic trials per process type


# ── Habitat score ─────────────────────────────────────────────────────────────────
# VR helpers (vr_q, min_vr) and the null loop now live in the single engine code path
# `app.services.analytics_habitat` (contract M3). They are imported above.

def habitat_score(x: np.ndarray, seed: int = SEED_CAL) -> float:
    """
    Surrogate-relative MR habitat score for window x.
    Returns 0–100; high = more reverting than null.

    Delegates to the single null-generating code path (contract M3) so the calibration
    badge and live scoring can never drift apart.
    """
    return habitat_score_full(x, seed)["score"]


# ── Synthetic process generators ──────────────────────────────────────────────────

def gen_ou(n: int, theta: float, mu: float, sigma: float, x0: float,
           rng: np.random.Generator) -> np.ndarray:
    """OU process (mean-reverting)."""
    x = np.empty(n)
    x[0] = x0
    for t in range(1, n):
        x[t] = x[t-1] + theta * (mu - x[t-1]) + sigma * rng.normal()
    return x


def gen_rw(n: int, mu: float, sigma: float, x0: float,
           rng: np.random.Generator) -> np.ndarray:
    """Random walk."""
    return np.concatenate([[x0], x0 + np.cumsum(rng.normal(mu, sigma, n - 1))])


def gen_trend_momentum(n: int, phi: float, sigma: float, x0: float,
                       rng: np.random.Generator) -> np.ndarray:
    """
    Trend via positively autocorrelated (momentum) increments: AR(1) with phi > 0.
    VR(q) > 1 for positively autocorrelated increments — correctly super-diffusive.
    NOTE: a deterministic-mean trend + iid noise is NOT the right model here.
    With a deterministic trend, np.var's mean-correction removes the slope, leaving
    only iid noise → VR = 1/q (appears as MR). Use AR(1) increments instead.
    """
    dr = np.zeros(n - 1)
    dr[0] = rng.normal(0, sigma)
    noise_scale = sigma * np.sqrt(max(1 - phi**2, 1e-6))
    for t in range(1, n - 1):
        dr[t] = phi * dr[t-1] + rng.normal(0, noise_scale)
    return np.concatenate([[x0], x0 + np.cumsum(dr)])


# ── Calibration runner ────────────────────────────────────────────────────────────

def run_calibration() -> dict:
    rng = np.random.default_rng(SEED_CAL)

    # Synthetic process parameters (representative price-like dynamics)
    ou_params  = {"theta": 0.25, "mu": 100.0, "sigma": 0.8, "x0": 104.0}  # clear MR (displaced from mean)
    rw_params  = {"mu": 0.0, "sigma": 0.8, "x0": 100.0}
    tr_params  = {"phi": 0.70, "sigma": 0.8, "x0": 100.0}  # momentum — AR(1) positive increments → VR>1

    scores = {"ou": [], "rw": [], "trend": []}

    for trial in range(N_TRIALS):
        seed_t = int(rng.integers(0, 1_000_000))

        # OU
        x_ou = gen_ou(H + 10, rng=np.random.default_rng(seed_t), **ou_params)
        s_ou = habitat_score(x_ou[-H:], seed=seed_t + 1)
        if np.isfinite(s_ou):
            scores["ou"].append(s_ou)

        # RW
        x_rw = gen_rw(H + 10, rng=np.random.default_rng(seed_t + 2), **rw_params)
        s_rw = habitat_score(x_rw[-H:], seed=seed_t + 3)
        if np.isfinite(s_rw):
            scores["rw"].append(s_rw)

        # Trend (momentum — AR(1) positive increments)
        x_tr = gen_trend_momentum(H + 10, rng=np.random.default_rng(seed_t + 4), **tr_params)
        s_tr = habitat_score(x_tr[-H:], seed=seed_t + 5)
        if np.isfinite(s_tr):
            scores["trend"].append(s_tr)

    results = {}
    for k, vals in scores.items():
        results[k] = {
            "mean": round(float(np.mean(vals)), 2),
            "median": round(float(np.median(vals)), 2),
            "p10": round(float(np.percentile(vals, 10)), 2),
            "p90": round(float(np.percentile(vals, 90)), 2),
            "n": len(vals),
        }
    return results


# ── Main ─────────────────────────────────────────────────────────────────────────

def main() -> bool:
    print("MR Habitat Score — Synthetic Calibration Gate")
    print(f"Parameters: VR_QS={VR_QS}, H={H}, NS_NULL={NS_NULL}, N_TRIALS={N_TRIALS}")
    print("=" * 60)

    results = run_calibration()

    # Pre-committed calibration criteria
    ou_mean    = results["ou"]["mean"]
    rw_mean    = results["rw"]["mean"]
    trend_mean = results["trend"]["mean"]

    print(f"\nProcess | mean score | median | p10  | p90")
    print(f"--------|------------|--------|------|-----")
    for k in ["ou", "rw", "trend"]:
        r = results[k]
        print(f"{k:7s} | {r['mean']:10.1f} | {r['median']:6.1f} | {r['p10']:4.1f} | {r['p90']:4.1f}")

    print("\nCalibration criteria:")
    pass_ou    = ou_mean >= 65.0
    pass_rw    = 35.0 <= rw_mean <= 65.0
    pass_trend = trend_mean <= 65.0

    print(f"  OU    mean ≥ 65   : {ou_mean:.1f}  → {'PASS' if pass_ou else 'FAIL'}")
    print(f"  RW    mean ∈[35,65]: {rw_mean:.1f}  → {'PASS' if pass_rw else 'FAIL'}")
    print(f"  TREND mean ≤ 65   : {trend_mean:.1f}  → {'PASS' if pass_trend else 'FAIL'}")

    gate_pass = pass_ou and pass_rw and pass_trend
    print(f"\nCALIBRATION GATE: {'PASS — score is well-behaved' if gate_pass else 'FAIL — fix score before real-data use'}")

    return gate_pass


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
