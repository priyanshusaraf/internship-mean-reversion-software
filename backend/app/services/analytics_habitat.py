"""Habitat score engine — the SINGLE null-generating code path (contract M3, D3).

The VR + RW + MA(1) null math here is copied VERBATIM from the frozen
`scripts/calibrate_habitat_score.py` (NS_NULL=2000, the exact seed/order/vol-matching).
`habitat_score_full` is the one place the null cloud is built;
`scripts/calibrate_habitat_score.py::habitat_score` calls into here so there is ONE path
(contract M3 — a second null loop would let the calibration badge drift from live scoring).

DOC-20 RECONCILIATION (doc 25 §1, 2026-06-07). The live scorer had drifted below its own
validated positive-control prereg (doc 20). Four divergences fixed here, all ADDITIVE:
  • q-grid: VR_QS now {2,5,10,20} (q=2 was missing) — applied to real AND every surrogate family.
  • GARCH(1,1) null ADDED — the third martingale-class gate doc 20 §5 requires. The fit/sim are
    IMPORTED VERBATIM from the validated `analytics_arm_a` primitives (`_fit_garch`/`_sim_garch`),
    not reinvented. GARCH is fit CAUSALLY on the pre-sample (data strictly < window start),
    never on the window under test (§6.1 temporal firewall). <60 pre-sample bars ⇒ the GARCH
    gate defaults to p_garch=0.5 (non-confirmatory) with a warning.
  • `confirmed` gate ADDED — the frozen rejection rule the continuous percentile lacked:
    confirmed = real_min_vr < 1 AND p_rw<α AND p_garch<α AND p_ma1<α  (α=0.05).
  • N kept at 2000 (doc 25 §1 DIVERGENCE-4: more conservative; correct to keep).

The DISPLAY `score` (0–100 continuous percentile) is UNCHANGED in role: it remains the
RW+MA(1) pool percentile (`100·mean(pool_min_vr ≥ real_min_vr)`), so the API invariant
`surrogate.frac_ge_real == score/100` still holds. GARCH is a SEPARATE per-family draw used
ONLY for `p_garch`/`confirmed` — it is deliberately NOT folded into the display cloud.
"""
from __future__ import annotations
import numpy as np

# Port the VALIDATED GARCH(1,1) fit/sim verbatim (doc 20 §5; analytics_arm_a — frozen v1
# primitives). Zero-mean GARCH QMLE on increments → martingale level (no reversion injected),
# isolating whether sub-diffusion is a volatility-clustering artifact.
from app.services.analytics_arm_a import _fit_garch, _sim_garch

# Habitat score parameters — FROZEN.
VR_QS = [2, 5, 10, 20]       # lags for min-VR (doc 20 §5: q∈{2,5,10,20})
NS_NULL = 2000               # surrogates per score evaluation (per pooled display cloud)
SEED_CAL = 20260606          # calibration seed (default)
ALPHA_GATE = 0.05            # frozen 5th-percentile rejection rule (doc 20 §6)
GARCH_MIN_PRESAMPLE = 60     # min pre-sample bars to fit GARCH; below this the gate defaults
_GATE_NOTE_OK = "RW∧GARCH∧MA(1) triple gate, α=0.05, q∈{2,5,10,20}, real_min_vr<1 required"
_GATE_NOTE_DEFAULT = "GARCH gate defaulted — insufficient pre-sample (<60 bars)"


# ── VR helpers (VERBATIM from calibrate_habitat_score.py) ──────────────────────────

def vr_q(x: np.ndarray, q: int) -> float:
    """Variance ratio at lag q. x is a level series."""
    x = x[np.isfinite(x)]
    n = len(x)
    if n < q + 5:
        return float("nan")
    dr = np.diff(x)
    var1 = np.var(dr, ddof=1)
    if var1 <= 1e-14:
        return float("nan")
    ret_q = x[q:] - x[:-q]
    return float(np.var(ret_q, ddof=1) / (q * var1))


def min_vr(x: np.ndarray, qs: list[int] = VR_QS) -> float:
    """Min VR over a set of lags."""
    vals = [vr_q(x, q) for q in qs]
    vals = [v for v in vals if np.isfinite(v)]
    return min(vals) if vals else float("nan")


# ── Habitat score (full) — the SINGLE null path ────────────────────────────────────

def _p_lower_tail(surr: list[float], real: float) -> float:
    """p = fraction of a family's surrogate min-VRs that are <= the real min-VR (lower tail —
    the proportion of the null that is AT LEAST AS sub-diffusive as the real). Lower p ⇒ the
    real reverts more than the null can manufacture. NaN if the family produced no draws."""
    a = np.asarray(surr, dtype=float)
    a = a[np.isfinite(a)]
    if a.size == 0:
        return float("nan")
    return float(np.mean(a <= real))


def _empty_result(real_mvr: float, vr_curve: list, n: int, gate_note: str) -> dict:
    return {
        "score": float("nan"), "real_min_vr": real_mvr, "null_min_vr": [],
        "vr_curve": vr_curve, "n": int(n),
        "confirmed": False, "p_rw": float("nan"), "p_garch": float("nan"),
        "p_ma1": float("nan"), "gate_note": gate_note, "garch_defaulted": True,
    }


def habitat_score_full(x: np.ndarray, seed: int = SEED_CAL, *,
                       pre_sample: np.ndarray | None = None,
                       ns_null: int = NS_NULL) -> dict:
    """Surrogate-relative MR habitat score for window x, returning the FULL cloud + the doc-20
    triple-gate verdict.

    Returns {score, real_min_vr, null_min_vr (list), vr_curve, n, confirmed, p_rw, p_garch,
             p_ma1, gate_note, garch_defaulted}.

    DISPLAY score = 100 * mean(pool_min_vr >= real_min_vr) over the RW+MA(1) pool (unchanged role;
    high = more reverting than null). The doc-20 `confirmed` gate is computed ALONGSIDE and is the
    frozen rejection rule:
        confirmed = real_min_vr < 1  AND  p_rw < α  AND  p_garch < α  AND  p_ma1 < α   (α=0.05)
    where each p_* is the lower-tail fraction of that family's surrogate min-VRs <= real_min_vr.

    GARCH(1,1) is fit CAUSALLY on `pre_sample` (levels strictly before the window; §6.1 firewall),
    never on x. If `pre_sample` is None or has < GARCH_MIN_PRESAMPLE finite bars, the GARCH gate
    defaults to p_garch = 0.5 (conservative — cannot contribute a confirm) and garch_defaulted=True.

    RW/MA(1) generation is VERBATIM the frozen `habitat_score` body (same rng order/vol-matching),
    so the display score is deterministic and the calibration delegation (contract M3) is intact.
    GARCH draws use a SEPARATE rng (seed+991) so they never perturb the RW/MA(1) stream.
    """
    x = np.asarray(x, dtype=float)
    real_mvr = min_vr(x)

    # vr_curve over the real window (per-q), for rendering — does not affect the score.
    vr_curve = [{"q": int(q), "vr": vr_q(x, q)} for q in VR_QS]

    x_fin = x[np.isfinite(x)]
    n = len(x_fin)

    if not np.isfinite(real_mvr) or n < max(VR_QS) + 5:
        return _empty_result(real_mvr, vr_curve, n, _GATE_NOTE_DEFAULT)

    dr = np.diff(x_fin)
    mu_dr = float(np.mean(dr))
    sig_dr = float(np.std(dr, ddof=1))
    rng = np.random.default_rng(seed)
    half = ns_null // 2

    # ── Null 1: RW (iid, vol-matched) — own family list (for p_rw) AND the display pool ──
    rw_mvrs: list[float] = []
    for _ in range(half):
        path = np.concatenate([[x_fin[0]], x_fin[0] + np.cumsum(rng.normal(mu_dr, sig_dr, n - 1))])
        v = min_vr(path)
        if np.isfinite(v):
            rw_mvrs.append(v)

    # ── Null 2: MA(1) (vol-matched, decorrelation-free at q>=2 asymptotically) ──
    if len(dr) > 5:
        acf1 = float(np.corrcoef(dr[:-1], dr[1:])[0, 1])
        theta_ma = np.clip(acf1, -0.95, 0.95)
    else:
        theta_ma = 0.0

    ma1_mvrs: list[float] = []
    for _ in range(half):
        eps = rng.normal(0, sig_dr, n + 1)
        ma1_rets = eps[1:] + theta_ma * eps[:-1]
        ma1_rets *= sig_dr / (np.std(ma1_rets, ddof=1) + 1e-12)  # re-scale to match vol
        path = np.concatenate([[x_fin[0]], x_fin[0] + np.cumsum(ma1_rets[:n - 1])])
        v = min_vr(path)
        if np.isfinite(v):
            ma1_mvrs.append(v)

    # DISPLAY pool = RW + MA(1) (UNCHANGED). frac_ge_real == score/100 holds on this pool.
    pool = rw_mvrs + ma1_mvrs
    if not pool:
        return _empty_result(real_mvr, vr_curve, n, _GATE_NOTE_DEFAULT)
    score = 100.0 * float(np.mean(np.array(pool) >= real_mvr))

    # ── Null 3: GARCH(1,1) — CAUSAL pre-sample fit only (§6.1); separate rng (no pool) ──
    garch_defaulted = True
    p_garch = 0.5                       # conservative default (cannot contribute a confirm)
    gate_note = _GATE_NOTE_DEFAULT
    if pre_sample is not None:
        ps = np.asarray(pre_sample, dtype=float)
        ps = ps[np.isfinite(ps)]
        if ps.size >= GARCH_MIN_PRESAMPLE:
            garch_params = _fit_garch(np.diff(ps))      # fit on PRE-SAMPLE increments only
            rng_g = np.random.default_rng(seed + 991)   # separate stream — RW/MA(1) untouched
            garch_mvrs: list[float] = []
            for _ in range(half):
                surr = _sim_garch(garch_params, n, rng_g)   # length-n martingale level path
                v = min_vr(surr)                             # IDENTICAL extraction / q-grid
                if np.isfinite(v):
                    garch_mvrs.append(v)
            if garch_mvrs:
                p_garch = _p_lower_tail(garch_mvrs, real_mvr)
                garch_defaulted = False
                gate_note = _GATE_NOTE_OK

    p_rw = _p_lower_tail(rw_mvrs, real_mvr)
    p_ma1 = _p_lower_tail(ma1_mvrs, real_mvr)

    confirmed = bool(
        np.isfinite(real_mvr) and real_mvr < 1.0
        and np.isfinite(p_rw) and p_rw < ALPHA_GATE
        and np.isfinite(p_garch) and p_garch < ALPHA_GATE
        and np.isfinite(p_ma1) and p_ma1 < ALPHA_GATE
    )

    return {
        "score": float(score),
        "real_min_vr": float(real_mvr),
        "null_min_vr": [float(v) for v in pool],
        "vr_curve": vr_curve,
        "n": int(n),
        "confirmed": confirmed,
        "p_rw": float(p_rw) if np.isfinite(p_rw) else float("nan"),
        "p_garch": float(p_garch) if np.isfinite(p_garch) else float("nan"),
        "p_ma1": float(p_ma1) if np.isfinite(p_ma1) else float("nan"),
        "gate_note": gate_note,
        "garch_defaulted": bool(garch_defaulted),
    }
