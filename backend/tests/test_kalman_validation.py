"""
Anchored Kalman μ* — v1 validation, recording the REJECTION (KC4 primary, KC1 also).

▸ STATUS NOTE (2026-06-01): the v1 REJECTION verdict was OVERTURNED — see
docs/research/06_kalman_equilibrium_research_update.md (§6/§8) and 05's SUPERSEDED banner. The
KC4 "absorption" reading was confounded on synthetic ou_in_trend (centering and reversion are
entangled by construction). The assertions below are LEFT UNCHANGED ON PURPOSE: they lock a
*measurement* (corr/acf values on synthetic data) that is still true and still green — they are
NOT a current verdict on the estimator. Do NOT reframe them to assert "centering" (demoted, 06
§12) nor a causal-reversion gate until the §13 cross-instrument MVF returns a verdict (still
pending; the §15 freeze is provisional). Treat the REJECTION wording in this docstring as historical.

These tests are the runnable record of docs/research/05_kalman_v1_results_memo.md. The full
SNR sweep (scripts/calibrate_kalman.py over logspace(-9, 0, 28)) shows NO admissible SNR: the
signal gates occupy disjoint SNR regions and G-ABSORB fails at every SNR. The estimator is
well-formed (G0) and can recover OU half-life at very slow settings (H2), but at those settings
its velocity absorbs the deviation (G-ABSORB) and the random-walk null (H1) fails badly.

`test_gabsorb_fails_at_frozen_snr` and `test_h1_random_walk_fails` lock the kill in. If a future
change makes either pass, the test fails loudly — that is the signal to re-run the full G1 suite
and write a v2 memo, NOT to weaken the threshold. Thresholds here are the spec's, not negotiable.
"""
import numpy as np
import pandas as pd

from app.services import analytics, synthetic

SNR = analytics.KALMAN_SNR  # frozen 5.623e-3
N = 500
BURN = 100
LAM = -0.1
SIGMA = 1.0
TRUE_HL = -np.log(2) / LAM  # 6.93 bars


def _kalman_eps(prices: np.ndarray, snr: float = SNR) -> pd.Series:
    df = analytics.compute_kalman_mu_star(pd.Series(prices), snr=snr)
    return pd.Series(df["epsilon_kalman"].to_numpy()[BURN:])


# ── Gate G0: well-formed on every generator ───────────────────────────────────

class TestG0WellFormed:
    """compute_kalman_mu_star runs on all eight generators with no NaN/inf/divergence."""

    def test_all_generators_finite(self):
        gens = [
            synthetic.ou(seed=0),
            synthetic.random_walk(seed=0),
            synthetic.trend(seed=0),
            synthetic.ou_in_trend(seed=0),
            synthetic.regime_switch(seed=0),
            synthetic.structural_break(seed=0),
            synthetic.vol_cluster(seed=0),
            synthetic.jump(seed=0),
        ]
        for s in gens:
            df = analytics.compute_kalman_mu_star(pd.Series(s.prices), snr=SNR)
            assert df.shape[0] == len(s.prices)
            assert np.isfinite(df.to_numpy()).all(), (
                f"Non-finite Kalman output on generator {s.meta['kind']!r}"
            )

    def test_empty_series(self):
        df = analytics.compute_kalman_mu_star(pd.Series([], dtype=float))
        assert list(df.columns) == [
            "mu_star_kalman", "epsilon_kalman", "kalman_velocity",
            "kalman_gain", "kalman_state_var",
        ]
        assert len(df) == 0


# ── Causal firewall: innovation at t uses no data after t ──────────────────────

class TestKalmanCausalFirewall:
    """The published μ* and innovation at bar t must be bit-identical whether or not data
    after t exists (spec §3 inviolable firewall; mirrors test_diagnostics_no_future_data)."""

    def test_future_spike_does_not_change_past(self):
        base = synthetic.ou(seed=1).prices.copy()
        spiked = base.copy()
        spiked[300] += 5000.0  # huge future shock
        df_base = analytics.compute_kalman_mu_star(pd.Series(base[:300]), snr=SNR)
        df_full = analytics.compute_kalman_mu_star(pd.Series(spiked), snr=SNR)
        # μ* and innovation at bars 0..299 must be unaffected by the spike at 300.
        assert np.allclose(
            df_base["mu_star_kalman"].to_numpy(),
            df_full["mu_star_kalman"].to_numpy()[:300],
            atol=1e-9,
        ), "Future spike leaked into past μ* — temporal firewall violated."


# ── Gate H2: OU half-life recovery (PASSES) ───────────────────────────────────

class TestH2OURecovery:
    """At the frozen SNR, the innovation recovers the embedded OU half-life within ±25%."""

    def test_ou_halflife_within_25pct(self):
        errs = []
        for seed in range(10):
            s = synthetic.ou(lam=LAM, sigma=SIGMA, n=N, seed=seed)
            hl = analytics.compute_halflife(_kalman_eps(s.prices))
            if hl is not None:
                errs.append(abs(hl - TRUE_HL) / TRUE_HL)
        med = float(np.median(errs))
        assert med < 0.25, f"H2 should pass: OU half-life err {med:.1%} ≥ 25%."


# ── Gate G-ABSORB: alpha absorption (FAILS everywhere → KC4, the primary kill) ─

class TestGAbsorbKill:
    """G-ABSORB requires |corr(velocity, true_deviation)| < 0.20 on ou_in_trend. It fails at the
    frozen SNR, and the sweep shows it fails at EVERY SNR (min 0.208). This is KC4 — the velocity
    that makes the filter not-an-EMA is the same velocity that eats the deviation."""

    def test_gabsorb_fails_at_frozen_snr(self):
        corrs = []
        for seed in range(15):
            s = synthetic.ou_in_trend(lam=LAM, sigma=SIGMA, slope=0.1, n=N, seed=seed)
            vel = analytics.compute_kalman_mu_star(pd.Series(s.prices), snr=SNR)[
                "kalman_velocity"].to_numpy()[BURN:]
            dev = s.deviation[BURN:]
            if np.std(vel) > 1e-9 and np.std(dev) > 1e-9:
                corrs.append(abs(np.corrcoef(vel, dev)[0, 1]))
        med = float(np.median(corrs))
        assert med >= 0.20, (
            f"G-ABSORB absorption {med:.3f} < 0.20 at SNR={SNR:.3e}. If this fails, the "
            f"absorption kill (KC4) may no longer hold — re-run the full sweep and write a v2 "
            f"memo. Do NOT weaken this threshold."
        )


# ── Gate H1: random-walk null (FAILS → KC1) ───────────────────────────────────

class TestH1RandomWalkKill:
    """H1 requires acf<0.20 AND not-MR on ≥90% of seeds. It fails at the frozen (slow) SNR: a
    filter slow enough to recover OU lags a random walk, so its innovation inherits strong
    trend-following autocorrelation (acf ≈ 0.98). Secondary kill, KC1."""

    def test_h1_random_walk_fails(self):
        passes = 0
        seeds = list(range(20))
        for seed in seeds:
            rw = synthetic.random_walk(sigma=SIGMA, n=N, seed=seed)
            eps = _kalman_eps(rw.prices)
            acf1 = analytics.compute_acf(eps)["lag1"]
            not_mr = analytics.compute_halflife(eps) is None
            if acf1 < 0.20 and not_mr:
                passes += 1
        rate = passes / len(seeds)
        assert rate < 0.90, (
            f"H1 pass-rate {rate:.0%} ≥ 90% at SNR={SNR:.3e}. If this fails, Kalman may no "
            f"longer be KC1-rejected — re-run the full G1 suite and write a v2 memo."
        )
