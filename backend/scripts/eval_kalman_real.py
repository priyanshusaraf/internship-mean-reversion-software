"""
STEP 1 — REAL-MARKET RESEARCH PASS (falsification, not promotion).

Question: does the SYNTHETIC trend-centering advantage of Kalman μ* (doc 06) survive real markets?
We do NOT assume it does. We look for the conditions under which it fails — especially FALSE
CENTERING in violent regime changes (velocity absorbing a real displacement).

Method mirrors the confirmatory test's fairness control: compare Kalman against an EMA at the
MATCHED effective span (so responsiveness is held fixed and only the velocity state differs).
Real instruments are auto-segmented into regime windows (strong trend / sideways / volatile /
break) by rolling slope and volatility, and centering metrics are reported per window.

Reproducible. Writes full tables to /tmp/eval_real.txt; prints a compact summary.
"""
from __future__ import annotations
import sys, os, warnings
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd  # noqa: E402
import duckdb  # noqa: E402
from app.services import analytics  # noqa: E402

np.seterr(all="ignore")
DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "amr.duckdb")


def matched_ema_span(snr=analytics.KALMAN_SNR, kappa=analytics.KALMAN_KAPPA) -> int:
    """Steady-state level gain α (R_p=1 Riccati) → matched EMA span = 2/α − 1."""
    R = 1.0; q_v = snr * R; q_mu = kappa * q_v
    F = np.array([[1.0, 1.0], [0.0, 1.0]]); Q = np.array([[q_mu, 0.0], [0.0, q_v]])
    H = np.array([1.0, 0.0]); I2 = np.eye(2); P = np.diag([10.0, 10.0]); K = np.zeros(2)
    for _ in range(8000):
        Pp = F @ P @ F.T + Q; S = Pp[0, 0] + R; Kn = (Pp @ H) / S
        P = (I2 - np.outer(Kn, H)) @ Pp
        if np.max(np.abs(Kn - K)) < 1e-13: K = Kn; break
        K = Kn
    return max(2, int(round(2.0 / float(K[0]) - 1.0)))


def sign_runs(v: np.ndarray):
    if len(v) < 2: return 0.0, len(v)
    s = v >= 0; crosses = int(np.sum(s[1:] != s[:-1]))
    runs, cur = [], 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]: cur += 1
        else: runs.append(cur); cur = 1
    runs.append(cur)
    return crosses / (len(v) - 1), max(runs)


def centering(eps: np.ndarray) -> dict:
    cr, mr = sign_runs(eps)
    return dict(abs_mean=abs(float(np.mean(eps))), std=float(np.std(eps)),
                frac_pos=float(np.mean(eps > 0)), cross=cr, max_run=int(mr))


def classify(prices: np.ndarray, span: int):
    """Return regime label per bar from rolling slope (trend) and rolling vol (turbulence)."""
    s = pd.Series(prices)
    ret = s.pct_change()
    win = span
    slope = s.diff(win) / win / s.shift(win)            # normalized per-bar drift over window
    vol = ret.rolling(win).std()
    slope_a = slope.abs()
    # thresholds from the series' own distribution (robust, data-driven)
    st = slope_a.quantile(0.70); vt = vol.quantile(0.80)
    lab = np.full(len(prices), "transition", dtype=object)
    for i in range(len(prices)):
        sa, vv = slope_a.iloc[i], vol.iloc[i]
        if not np.isfinite(sa) or not np.isfinite(vv):
            lab[i] = "warmup"; continue
        if vv >= vt and sa < st: lab[i] = "volatile_sideways"
        elif vv >= vt and sa >= st: lab[i] = "volatile_trend"
        elif sa >= st: lab[i] = "strong_trend"
        else: lab[i] = "sideways"
    return lab, slope, vol


def eval_instrument(conn, iid: str, span: int, out: list):
    df = conn.execute(
        "select date, close from ohlcv where instrument_id=? order by date", [iid]
    ).fetch_df()
    if len(df) < 3 * span:
        out.append(f"[{iid}] too short ({len(df)} bars)"); return None
    close = df["close"]
    prices = close.to_numpy(float)
    ema = analytics.compute_ema(close, span=span).to_numpy()
    eps_ema = prices - ema
    kf = analytics.compute_kalman_mu_star(close)
    eps_kal = kf["epsilon_kalman"].to_numpy()

    burn = span  # drop warmup for both
    lab, slope, vol = classify(prices, span)
    out.append(f"\n=== {iid}  n={len(df)}  matched EMA span={span}  "
               f"({df['date'].iloc[0].date()}…{df['date'].iloc[-1].date()}) ===")
    out.append(f"  {'regime':<18} {'bars':>5} {'|mean|EMA':>10} {'|mean|KAL':>10} "
               f"{'stdEMA':>8} {'stdKAL':>8} {'runEMA':>7} {'runKAL':>7} {'xEMA':>6} {'xKAL':>6}")
    summary = {}
    for reg in ["strong_trend", "volatile_trend", "sideways", "volatile_sideways"]:
        m = (lab == reg)
        m[:burn] = False
        if m.sum() < span:
            out.append(f"  {reg:<18} {int(m.sum()):>5}  (too few bars)"); continue
        ce = centering(eps_ema[m]); ck = centering(eps_kal[m])
        out.append(f"  {reg:<18} {int(m.sum()):>5} {ce['abs_mean']:>10.3f} {ck['abs_mean']:>10.3f} "
                   f"{ce['std']:>8.3f} {ck['std']:>8.3f} {ce['max_run']:>7d} {ck['max_run']:>7d} "
                   f"{ce['cross']:>6.3f} {ck['cross']:>6.3f}")
        summary[reg] = (ce, ck)

    # ── FALSE-CENTERING PROBE: behaviour around the largest structural displacements ──
    # A true regime break is a real, persistent level shift. A faithful estimator's residual
    # should show a LARGE transient that decays slowly. If Kalman's ε transient is much smaller
    # than EMA's at a true break, the velocity absorbed a real displacement = FALSE CENTERING.
    ret = np.abs(np.diff(prices, prepend=prices[0]) / np.maximum(prices, 1e-9))
    k = max(3, len(prices) // 200)
    break_idx = np.argsort(ret)[-k:]
    break_idx = [int(i) for i in break_idx if i > burn and i < len(prices) - 10]
    probe = []
    for bi in sorted(break_idx):
        w = slice(bi, bi + 10)  # 10-bar response after the shock
        pe = float(np.max(np.abs(eps_ema[w]))); pk = float(np.max(np.abs(eps_kal[w])))
        probe.append((df["date"].iloc[bi].date(), ret[bi], pe, pk, pk / (pe + 1e-9)))
    out.append("  false-centering probe (largest single-bar moves; ε peak in 10 bars after):")
    out.append(f"    {'date':<12} {'move':>7} {'εpkEMA':>8} {'εpkKAL':>8} {'KAL/EMA':>8}")
    ratios = []
    for d, mv, pe, pk, r in probe:
        ratios.append(r)
        out.append(f"    {str(d):<12} {mv:>7.3f} {pe:>8.3f} {pk:>8.3f} {r:>8.3f}")
    med_ratio = float(np.median(ratios)) if ratios else float("nan")
    out.append(f"    → median KAL/EMA ε-peak ratio at breaks = {med_ratio:.3f}  "
               f"(≪1 ⇒ velocity absorbing real displacement = FALSE CENTERING risk)")
    return summary, med_ratio


def main():
    span = matched_ema_span()
    out = [f"REAL-MARKET RESEARCH PASS — Kalman μ* vs matched-span EMA (span={span})",
           f"SNR={analytics.KALMAN_SNR:.1e} κ={analytics.KALMAN_KAPPA}  "
           f"(matched span isolates the velocity state, per doc 06 §7.1)"]
    conn = duckdb.connect(DB, read_only=True)
    iids = [r[0] for r in conn.execute(
        "select distinct instrument_id from ohlcv order by 1").fetchall()]
    headline = []
    for iid in iids:
        res = eval_instrument(conn, iid, span, out)
        if res:
            summ, mr = res
            st = summ.get("strong_trend"); sw = summ.get("sideways")
            if st:
                ce, ck = st
                ratio = ce["abs_mean"] / (ck["abs_mean"] + 1e-9)
                headline.append(f"{iid}: strong_trend |mean ε| EMA={ce['abs_mean']:.2f} "
                                f"KAL={ck['abs_mean']:.2f} ({ratio:.1f}× more centered); "
                                f"break ε-ratio={mr:.2f}")
            if sw:
                ce, ck = sw
                headline.append(f"{iid}: sideways |mean ε| EMA={ce['abs_mean']:.2f} "
                                f"KAL={ck['abs_mean']:.2f} (collapse-to-EMA check)")
    conn.close()
    open("/tmp/eval_real.txt", "w").write("\n".join(out) + "\n")
    print("\n".join(headline))
    print("full tables: /tmp/eval_real.txt")


if __name__ == "__main__":
    main()
