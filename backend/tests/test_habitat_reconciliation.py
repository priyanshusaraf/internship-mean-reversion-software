"""Doc-20 reconciliation calibration gate for the LIVE habitat scorer (doc 25 §1).

Mirrors doc-20 §5a. The reconciled `habitat_score_full` adds the GARCH(1,1) martingale null
(causal pre-sample fit), the q=2 horizon, and the explicit `confirmed` triple-gate
(real_min_vr<1 ∧ p_rw<.05 ∧ p_garch<.05 ∧ p_ma1<.05). These four tests prove the reconciled
gate has POWER (confirms a true reverter), SIZE (does not confirm a random walk), NOISE
DISCRIMINATION (does not confirm pure microstructure bounce), and NO-SEAM NO-OP (the live path
applies no jump filter, so it cannot alter the VR of a clean series).

All four must pass before the fix is considered complete (handoff to amr-rigor-qa).
"""
from __future__ import annotations

import numpy as np

from app.services.analytics_habitat import habitat_score_full, min_vr, GARCH_MIN_PRESAMPLE
from app.services import synthetic

# Smaller surrogate budget than the live N=2000 — keeps the suite fast while leaving p-value
# resolution (1/half) fine enough for the α=0.05 gate. The live default stays 2000.
NS_TEST = 400


def _split(prices: np.ndarray, n_window: int):
    """(window, pre_sample): the last n_window bars are the scored window; everything strictly
    before is the causal pre-sample the GARCH null is fit on. Disjoint by construction (§6.1)."""
    return prices[-n_window:], prices[:-n_window]


# ── TEST 1 — POWER: a true (seasonal-)OU reverter must CONFIRM ─────────────────────────

def test_power_true_ou_confirms():
    """A strongly mean-reverting OU (with a mild deterministic annual cycle) must trip the full
    RW∧GARCH∧MA(1) gate. If it does not, a null is over-powered and the apparatus is too blunt."""
    rng = np.random.default_rng(20260607)
    ou = synthetic.ou(lam=-0.35, sigma=1.0, n=800, seed=7).prices  # phi=0.65, fast reversion
    t = np.arange(ou.size)
    seasonal = 0.4 * np.sin(2.0 * np.pi * t / 252.0)               # slow annual cycle (doc-20 flavor)
    prices = ou + seasonal
    window, pre = _split(prices, n_window=400)
    assert pre.size >= GARCH_MIN_PRESAMPLE

    res = habitat_score_full(window, seed=11, pre_sample=pre, ns_null=NS_TEST)

    assert not res["garch_defaulted"], "GARCH should be active (pre-sample is ample)"
    assert res["real_min_vr"] < 1.0, f"OU must be sub-diffusive, got {res['real_min_vr']}"
    assert res["p_garch"] < 0.05, f"OU must beat GARCH null, p_garch={res['p_garch']}"
    assert res["p_rw"] < 0.05 and res["p_ma1"] < 0.05, (
        f"OU must beat RW & MA(1), p_rw={res['p_rw']} p_ma1={res['p_ma1']}")
    assert res["confirmed"] is True, "POWER FAIL: true OU did not confirm"


# ── TEST 2 — SIZE: pure RW must NOT confirm (FPR ≤ 10%, target ≤ 5%) ───────────────────

def test_size_random_walk_fpr():
    """100 pure random walks. `confirmed` must be False in ≥ 90 (FPR ≤ 10%); target ≤ 5%.
    A martingale beaten by its own martingale nulls only by chance — and only when ALL THREE
    families AND real<1 align — so the realized FPR should be ~0%."""
    n_series = 100
    confirms = 0
    for i in range(n_series):
        prices = synthetic.random_walk(sigma=1.0, n=400, seed=1000 + i).prices
        window, pre = _split(prices, n_window=200)
        res = habitat_score_full(window, seed=1000 + i, pre_sample=pre, ns_null=NS_TEST)
        if res["confirmed"]:
            confirms += 1
    fpr = confirms / n_series
    print(f"\n[TEST 2 SIZE] RW false-confirm rate (FPR) = {fpr:.1%} ({confirms}/{n_series})")
    assert fpr <= 0.10, f"SIZE FAIL: FPR {fpr:.1%} > 10%"


# ── TEST 3 — NOISE DISCRIMINATION: pure bounce (zero MR) must NOT confirm ──────────────

def test_noise_discrimination_ma1_bounce():
    """Latent RW + i.i.d. observation noise (bid-ask bounce) → negative increment ACF(1), VR<1,
    but ZERO mean reversion. The MA(1) null reproduces the bounce, so `confirmed` must be False.
    If it confirms, the MA(1) gate is not working on the reconciled path."""
    rng = np.random.default_rng(424242)
    n = 600
    sigma_w, sigma_eta = 1.0, 1.0
    latent = np.concatenate([[0.0], np.cumsum(rng.normal(0.0, sigma_w, n - 1))])  # latent RW
    obs = latent + rng.normal(0.0, sigma_eta, n)                                  # + iid noise
    window, pre = _split(obs, n_window=300)

    res = habitat_score_full(window, seed=5, pre_sample=pre, ns_null=NS_TEST)

    # Sub-diffusive by construction (bounce), but must be CAUGHT by the MA(1) null.
    assert res["real_min_vr"] < 1.0, "bounce should look sub-diffusive (that is the trap)"
    assert res["confirmed"] is False, (
        f"NOISE-DISCRIM FAIL: pure bounce confirmed; p_ma1={res['p_ma1']} (MA(1) gate not biting)")


# ── TEST 4 — NO-SEAM NO-OP: the live path applies no jump filter ───────────────────────

def test_no_seam_no_op():
    """A clean OU series has no roll seams. The live habitat path applies NO jump/seam filter
    (the increment-MAD mask lives only in the doc-20 ablation path, not here), so the VR it
    reports must be bit-identical to a direct min_vr on the raw window — i.e. |Δ VR| = 0 ≤ 0.01."""
    ou = synthetic.ou(lam=-0.2, sigma=1.0, n=500, seed=99).prices
    window, pre = _split(ou, n_window=300)

    res = habitat_score_full(window, seed=3, pre_sample=pre, ns_null=NS_TEST)
    direct = min_vr(np.asarray(window, dtype=float))

    assert np.isfinite(res["real_min_vr"]) and np.isfinite(direct)
    assert abs(res["real_min_vr"] - direct) <= 0.01, (
        f"NO-SEAM FAIL: engine VR {res['real_min_vr']} != direct VR {direct} "
        "(a seam filter is altering the VR)")
