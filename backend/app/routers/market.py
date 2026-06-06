import os
import glob as _glob
from pathlib import Path
from typing import Optional
import duckdb
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.models.market import (
    LoadRequest,
    LoadResponse,
    SpreadRequest,
    InstrumentMeta,
    OHLCVBar,
    OHLCVResponse,
    EstimatorBar,
    EstimatorResponse,
    ResearchRow,
    ResearchStats,
    ResearchResponse,
    DiagnosticsRow,
    DiagnosticsStats,
    DiagnosticsResponse,
    ReversionStat,
    VelocityAbsorptionRow,
    VelocityAbsorptionResponse,
    MRScoreRow,
    MRScoreStats,
    MRScoreResponse,
    SubstrateRow,
    SubstrateStats,
    SubstrateResponse,
)
from app.services import store, analytics, analytics_mrscore, analytics_substrate
from app.services.loader import load_ohlcv, LoaderError

# Observatory epistemic gate — surfaced in the MRScore payload and panel. MRScore is a DESCRIPTIVE
# falsification instrument, never a trade signal; and ADANIENT (the on-disk substrate) is trend-heavy
# while the deployment domain is mean-reverting, so a low score there is expected and NOT global evidence.
_MRSCORE_REGIME_WARNING = (
    "Observatory diagnostic — observe/falsify, NOT a signal. The self-ranked score is "
    "within-instrument relative; raw DRC/hit-rate are the cross-instrument discriminators. "
    "ADANIENT is trend-heavy (opposite of the deployment regime) — a low score there is "
    "expected and is not global evidence."
)

# Substrate Observatory epistemic gate. CHARACTER, not timing: scores say what the instrument
# *resembles* over the window, never that a regime is "igniting now" (State T detection — frozen).
_SUBSTRATE_REGIME_WARNING = (
    "Observatory diagnostic — what kind of market this RESEMBLES over the window, NOT a signal and "
    "NOT a claim that a regime is changing now (that is State T detection, deferred). ADANIENT is "
    "trend-heavy (opposite of the deployment regime), so a Trend-like read there is expected and is "
    "not global evidence about mean-reverting targets."
)
_SUBSTRATE_BUCKETS = ["ou_like", "trend_like", "rw_null", "ambiguous"]

router = APIRouter(prefix="/api/v1/market", tags=["market"])


def get_db():
    """Per-request DuckDB connection.
    In production: opens a fresh connection and closes it after the request.
    In tests: returns the injected in-memory connection without closing it.
    """
    is_injected = store._conn is not None
    conn = store.open_connection()
    try:
        yield conn
    finally:
        if not is_injected:
            conn.close()


@router.post("/load", response_model=LoadResponse)
def load_instrument(req: LoadRequest, conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    try:
        df = load_ohlcv(req.file_path)
    except LoaderError as e:
        raise HTTPException(status_code=422, detail=str(e))
    display_name = req.display_name or req.instrument_id
    store.store_instrument(conn, req.instrument_id, display_name, df, req.file_path)
    return LoadResponse(
        instrument_id=req.instrument_id,
        row_count=len(df),
        start_date=df.index.min().date().isoformat(),
        end_date=df.index.max().date().isoformat(),
        columns=df.columns.tolist(),
    )


@router.get("/instruments", response_model=list[InstrumentMeta])
def list_instruments(conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    return [InstrumentMeta(**r) for r in store.list_instruments(conn)]


@router.get("/suggest-paths")
def suggest_paths(prefix: str = "", limit: int = 12):
    """Return filesystem path completions for the given prefix (server-side glob)."""
    if len(prefix) < 1:
        return {"suggestions": []}
    expanded = os.path.expanduser(prefix)
    pattern = (os.path.join(expanded, "*") if os.path.isdir(expanded) else expanded + "*")
    try:
        matches = sorted(_glob.glob(pattern))
    except Exception:
        return {"suggestions": []}
    suggestions = []
    for m in matches:
        if os.path.isdir(m):
            suggestions.append(m.rstrip("/") + "/")
        elif m.lower().endswith((".csv", ".parquet", ".txt")):
            suggestions.append(m)
        if len(suggestions) >= limit:
            break
    return {"suggestions": suggestions}


_UPLOADS_DIR = Path(__file__).parent.parent / "uploads"


@router.post("/upload", response_model=list[LoadResponse])
async def upload_instruments(
    files: list[UploadFile] = File(...),
    conn: duckdb.DuckDBPyConnection = Depends(get_db),
):
    """Accept one or more uploaded CSV/Parquet files; instrument_id = filename stem (uppercased)."""
    _UPLOADS_DIR.mkdir(exist_ok=True)
    results = []
    errors = []
    for upload in files:
        filename = upload.filename or "upload"
        stem = Path(filename).stem.upper()
        dest = _UPLOADS_DIR / filename
        content = await upload.read()
        dest.write_bytes(content)
        try:
            df = load_ohlcv(str(dest))
        except LoaderError as e:
            errors.append(f"{filename}: {e}")
            continue
        store.store_instrument(conn, stem, stem, df, str(dest))
        results.append(LoadResponse(
            instrument_id=stem,
            row_count=len(df),
            start_date=df.index.min().date().isoformat(),
            end_date=df.index.max().date().isoformat(),
            columns=df.columns.tolist(),
        ))
    if not results and errors:
        raise HTTPException(status_code=422, detail="; ".join(errors))
    return results


@router.post("/spread", response_model=LoadResponse)
def create_spread(req: SpreadRequest, conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    """Construct a synthetic spread: close_A − β × close_B (applied to all OHLCV columns).

    Aligns legs on their shared date history (inner join). The spread is stored as a new
    instrument and appears in the sidebar like any loaded file. file_path is tagged
    `spread://...` for provenance. OHLC construction uses the symmetric formula
    (high_A − β×high_B etc.) — a practical approximation for daily research.
    """
    import pandas as pd

    df_a = store.get_ohlcv(conn, req.instrument_a)
    df_b = store.get_ohlcv(conn, req.instrument_b)

    if df_a.empty:
        raise HTTPException(status_code=422, detail=f"No data for instrument: {req.instrument_a}")
    if df_b.empty:
        raise HTTPException(status_code=422, detail=f"No data for instrument: {req.instrument_b}")

    df_a = df_a.set_index("date")
    df_b = df_b.set_index("date")
    df_a, df_b = df_a.align(df_b, join="inner")

    if df_a.empty:
        raise HTTPException(
            status_code=422,
            detail=f"No overlapping dates between {req.instrument_a} and {req.instrument_b}",
        )

    spread = pd.DataFrame(
        {
            "open":   df_a["open"]  - req.beta * df_b["open"],
            "high":   df_a["high"]  - req.beta * df_b["high"],
            "low":    df_a["low"]   - req.beta * df_b["low"],
            "close":  df_a["close"] - req.beta * df_b["close"],
            "volume": 0.0,
        },
        index=df_a.index,
    )
    spread.index.name = "date"

    beta_str = f"{req.beta:.6g}"
    spread_id = (req.spread_id.strip().upper() if req.spread_id else
                 f"{req.instrument_a}_{beta_str}x{req.instrument_b}")
    spread_path = f"spread://{req.instrument_a}-{beta_str}*{req.instrument_b}"

    store.store_instrument(conn, spread_id, spread_id, spread, spread_path)

    return LoadResponse(
        instrument_id=spread_id,
        row_count=len(spread),
        start_date=spread.index.min().date().isoformat(),
        end_date=spread.index.max().date().isoformat(),
        columns=spread.columns.tolist(),
    )


@router.get("/{instrument_id}/ohlcv", response_model=OHLCVResponse)
def get_ohlcv(
    instrument_id: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    conn: duckdb.DuckDBPyConnection = Depends(get_db),
):
    df = store.get_ohlcv(conn, instrument_id, start, end)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data for: {instrument_id}")
    df["time"] = df["date"].dt.strftime("%Y-%m-%d")
    bars = [OHLCVBar(**r) for r in df[["time", "open", "high", "low", "close", "volume"]].to_dict(orient="records")]
    return OHLCVResponse(instrument_id=instrument_id, bars=bars)


_SUPPORTED_ESTIMATORS = {"ema"}


@router.get("/{instrument_id}/estimator", response_model=EstimatorResponse)
def get_estimator(
    instrument_id: str,
    estimator: str = "ema",
    window: int = 20,
    start: Optional[str] = None,
    end: Optional[str] = None,
    conn: duckdb.DuckDBPyConnection = Depends(get_db),
):
    if estimator not in _SUPPORTED_ESTIMATORS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown estimator: {estimator!r}. Supported: {sorted(_SUPPORTED_ESTIMATORS)}",
        )
    df = store.get_ohlcv(conn, instrument_id, start, end)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data for: {instrument_id}")
    values = analytics.compute_ema(df["close"], span=window)
    df["time"] = df["date"].dt.strftime("%Y-%m-%d")
    df["value"] = values.values
    bars = [EstimatorBar(**r) for r in df[["time", "value"]].to_dict(orient="records")]
    return EstimatorResponse(instrument_id=instrument_id, estimator=estimator, window=window, bars=bars)


@router.get("/{instrument_id}/research", response_model=ResearchResponse)
def get_research(
    instrument_id: str,
    estimator: str = "ema",
    window: int = 20,
    start: Optional[str] = None,
    end: Optional[str] = None,
    conn: duckdb.DuckDBPyConnection = Depends(get_db),
):
    if estimator not in _SUPPORTED_ESTIMATORS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown estimator: {estimator!r}. Supported: {sorted(_SUPPORTED_ESTIMATORS)}",
        )
    df = store.get_ohlcv(conn, instrument_id, start, end)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data for: {instrument_id}")

    mu_star = analytics.compute_ema(df["close"], span=window)
    epsilon = analytics.compute_residual(df["close"], mu_star)

    df["date_str"] = df["date"].dt.strftime("%Y-%m-%d")
    df["mu_star"] = mu_star.values
    df["epsilon"] = epsilon.values

    rows = [
        ResearchRow(date=r["date_str"], close=r["close"], mu_star=r["mu_star"], epsilon=r["epsilon"])
        for r in df[["date_str", "close", "mu_star", "epsilon"]].to_dict(orient="records")
    ]

    stats = ResearchStats(
        epsilon_mean=float(epsilon.mean()),
        epsilon_std=float(epsilon.std()),
        n=len(df),
    )

    return ResearchResponse(
        instrument_id=instrument_id,
        estimator=estimator,
        window=window,
        rows=rows,
        stats=stats,
    )


@router.get("/{instrument_id}/diagnostics", response_model=DiagnosticsResponse)
def get_diagnostics(
    instrument_id: str,
    estimator: str = "ema",
    window: int = 20,
    start: Optional[str] = None,
    end: Optional[str] = None,
    conn: duckdb.DuckDBPyConnection = Depends(get_db),
):
    """Full diagnostic payload for the Research Workbench.
    Returns causal AND full-info estimator in one call — both are firewalled
    to data ≤ end. The difference between them is the look-ahead gap, not a
    temporal leak.
    """
    import math

    def _f(v: float) -> float | None:
        """Convert numpy float → Python float, returning None for NaN/Inf."""
        f = float(v)
        return None if (math.isnan(f) or math.isinf(f)) else f

    if estimator not in _SUPPORTED_ESTIMATORS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown estimator: {estimator!r}. Supported: {sorted(_SUPPORTED_ESTIMATORS)}",
        )
    df = store.get_ohlcv(conn, instrument_id, start, end)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data for: {instrument_id}")

    close = df["close"]

    mu_causal = analytics.compute_ema(close, span=window)
    mu_adj = analytics.compute_full_ema(close, span=window)
    epsilon = analytics.compute_residual(close, mu_causal)
    epsilon_adj = analytics.compute_residual(close, mu_adj)
    innovation = analytics.compute_innovation(close, mu_causal)

    # Kalman μ* — research comparison estimator (frozen spec). Causal by construction.
    kf = analytics.compute_kalman_mu_star(close)

    eps_roll_mean = epsilon.rolling(window=window, min_periods=1).mean()
    eps_roll_std = epsilon.rolling(window=window, min_periods=2).std()
    eps_zscore = (epsilon - eps_roll_mean) / eps_roll_std

    df["date_str"] = df["date"].dt.strftime("%Y-%m-%d")
    dates = df["date_str"].tolist()

    rows: list[DiagnosticsRow] = []
    for i in range(len(df)):
        rows.append(DiagnosticsRow(
            date=dates[i],
            close=float(close.iloc[i]),
            mu_star=float(mu_causal.iloc[i]),
            mu_star_adj=float(mu_adj.iloc[i]),
            mu_star_diff=float(mu_adj.iloc[i] - mu_causal.iloc[i]),
            epsilon=float(epsilon.iloc[i]),
            epsilon_adj=float(epsilon_adj.iloc[i]),
            epsilon_rolling_mean=float(eps_roll_mean.iloc[i]),
            epsilon_rolling_std=_f(eps_roll_std.iloc[i]) or 0.0,
            epsilon_zscore=_f(eps_zscore.iloc[i]),
            innovation=_f(innovation.iloc[i]),
            mu_star_kalman=float(kf["mu_star_kalman"].iloc[i]),
            epsilon_kalman=float(kf["epsilon_kalman"].iloc[i]),
            kalman_velocity=float(kf["kalman_velocity"].iloc[i]),
            kalman_gain=float(kf["kalman_gain"].iloc[i]),
            kalman_state_var=float(kf["kalman_state_var"].iloc[i]),
        ))

    acf = analytics.compute_acf(epsilon)
    halflife = analytics.compute_halflife(epsilon)
    mu_diff = mu_adj - mu_causal

    stats = DiagnosticsStats(
        epsilon_mean=float(epsilon.mean()),
        epsilon_std=float(epsilon.std()),
        epsilon_skew=float(epsilon.skew()),
        epsilon_kurt=float(epsilon.kurt()),
        acf_lag1=acf.get("lag1", 0.0),
        acf_lag5=acf.get("lag5", 0.0),
        acf_lag10=acf.get("lag10", 0.0),
        acf_lag20=acf.get("lag20", 0.0),
        halflife_bars=halflife,
        mu_star_diff_mean=float(mu_diff.mean()),
        mu_star_diff_max=float(mu_diff.abs().max()),
        n=len(df),
    )

    return DiagnosticsResponse(
        instrument_id=instrument_id,
        estimator=estimator,
        window=window,
        rows=rows,
        stats=stats,
    )


@router.get("/{instrument_id}/velocity-absorption", response_model=VelocityAbsorptionResponse)
def get_velocity_absorption(
    instrument_id: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    conn: duckdb.DuckDBPyConnection = Depends(get_db),
):
    """Step 2A structural instrumentation (read-only). Falsifies false centering: did the Kalman
    velocity state remove economically useful reversion signal?

    Compares the velocity-ON residual (Kalman innovation ε^K) against the velocity-OFF residual
    (ε^R = ε^K + δ ≡ matched-span EMA prediction residual) via a minimal walk-forward predictive-
    decay test. Does NOT touch the frozen estimator or the production /diagnostics path. The EMA
    here is matched to the Kalman's frozen steady-state responsiveness (fairness control), not the
    production window."""
    import math

    def _f(v: float) -> float | None:
        f = float(v)
        return None if (math.isnan(f) or math.isinf(f)) else f

    df = store.get_ohlcv(conn, instrument_id, start, end)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data for: {instrument_id}")

    va = analytics.compute_velocity_absorption(df["close"])
    df["date_str"] = df["date"].dt.strftime("%Y-%m-%d")
    dates = df["date_str"].tolist()
    delta = va["delta"]
    prices = va["price"]

    rows = [
        VelocityAbsorptionRow(date=dates[i], price=float(prices[i]), delta=_f(delta[i]))
        for i in range(len(df))
    ]

    def _stats(system: str) -> list[ReversionStat]:
        out = []
        for h in va["horizons"]:
            r = va["reversion"][system][h]
            out.append(ReversionStat(horizon=h, beta=_f(r["beta"]), r2=_f(r["r2"]), n=int(r["n"])))
        return out

    return VelocityAbsorptionResponse(
        instrument_id=instrument_id,
        matched_span=int(va["matched_span"]),
        steady_state_gain=float(va["steady_state_gain"]),
        burn=int(va["burn"]),
        n=int(va["n"]),
        horizons=[int(h) for h in va["horizons"]],
        reversion_kalman=_stats("kalman"),
        reversion_restored=_stats("restored"),
        rows=rows,
    )


@router.get("/{instrument_id}/mrscore", response_model=MRScoreResponse)
def get_mrscore(
    instrument_id: str,
    window: int = 20,
    start: Optional[str] = None,
    end: Optional[str] = None,
    conn: duckdb.DuckDBPyConnection = Depends(get_db),
):
    """MRScore observatory diagnostic — per-bar Mean Reversion Favorability (doc 01 §3, eq. 13–34).

    Causal-only (full-information mode deferred — no genuine future-using μ* exists yet). Built on the
    production causal EMA μ* (`window` = EMA span), DESCRIPTIVELY: this endpoint reads μ* and never
    feeds back into it, so it does not trip the μ* reversion-fidelity reopen trigger. Respects the
    `end` replay boundary (firewalled to data ≤ end). NOT a signal — see `regime_warning`."""
    import math

    def _f(v) -> float | None:
        f = float(v)
        return None if (math.isnan(f) or math.isinf(f)) else f

    df = store.get_ohlcv(conn, instrument_id, start, end)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data for: {instrument_id}")

    close = df["close"]

    # C1 guard — MRScore's Block-2/Block-3 use log-prices / log-returns (eq. 25, 29), which are
    # UNDEFINED on non-positive series. The frozen deployment domain (spreads · pairs · cross-asset
    # relative value, CLAUDE.md §1.1) routinely goes negative. Without this, such an instrument
    # silently returns an all-NaN score (n_scored=0) with no signal of incompatibility. Surface it
    # explicitly instead. (How to score spreads — level-diffs vs returns — is deferred research.)
    n_nonpos = int((close <= 0).sum())
    data_warning = None
    if n_nonpos > 0:
        data_warning = (
            f"Instrument has {n_nonpos} non-positive price(s) (min {float(close.min()):.4g}). "
            "MRScore's log-based features (realized vol, variance ratio, half-life on log-residual) "
            "are undefined on non-positive / spread series, so scores are unavailable here. This is "
            "structural incompatibility, NOT an unfavorable reading. Spread-domain scoring is deferred research."
        )

    mu_star = analytics.compute_ema(close, span=window)
    ms = analytics_mrscore.compute_mrscore(close, mu_star)

    df["date_str"] = df["date"].dt.strftime("%Y-%m-%d")
    dates = df["date_str"].tolist()
    cols = ["mrscore", "b1", "b2", "b3", "r_adf", "r_kpss", "r_msi", "r_vsi",
            "r_drc", "r_hit_rate", "r_vr", "r_hl", "r_vc", "r_tcf", "drc", "hit_rate", "vr_agg"]

    rows: list[MRScoreRow] = []
    for i in range(len(df)):
        rows.append(MRScoreRow(
            date=dates[i],
            close=float(close.iloc[i]),
            mu_star=float(mu_star.iloc[i]),
            **{c: _f(ms[c].iloc[i]) for c in cols},
        ))

    scored = ms["mrscore"].dropna()
    last = ms.iloc[-1] if len(ms) else None
    stats = MRScoreStats(
        n=len(df),
        n_scored=int(scored.shape[0]),
        mrscore_last=_f(last["mrscore"]) if last is not None else None,
        b1_last=_f(last["b1"]) if last is not None else None,
        b2_last=_f(last["b2"]) if last is not None else None,
        b3_last=_f(last["b3"]) if last is not None else None,
    )

    return MRScoreResponse(
        instrument_id=instrument_id,
        window=window,
        weights={"b1": 0.20, "b2": 0.60, "b3": 0.20},
        mode="causal",
        regime_warning=_MRSCORE_REGIME_WARNING,
        data_warning=data_warning,
        rows=rows,
        stats=stats,
    )


@router.get("/{instrument_id}/substrate", response_model=SubstrateResponse)
def get_substrate(
    instrument_id: str,
    window: int = 120,
    start: Optional[str] = None,
    end: Optional[str] = None,
    conn: duckdb.DuckDBPyConnection = Depends(get_db),
):
    """Substrate Observatory — per-bar instrument CHARACTER (docs/research/10): resemblance to the 4
    archetypes (OU-like · Trend-like · RW-Null · Ambiguous) from causal descriptors over a trailing
    `window`. Character, NOT timing — never a claim that a regime is igniting (State T, frozen).
    Causal-only (full-information deferred). Structurally terminal — reads OHLCV, feeds nothing back.
    Respects the `end` replay boundary (firewalled to data ≤ end). NOT a signal — see `regime_warning`."""
    import math

    def _f(v) -> float | None:
        f = float(v)
        return None if (math.isnan(f) or math.isinf(f)) else f

    df = store.get_ohlcv(conn, instrument_id, start, end)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data for: {instrument_id}")

    close = df["close"]

    # C1 guard — the variance-ratio descriptor uses log-prices (undefined on non-positive series). The
    # frozen deployment domain (spreads · pairs · cross-asset RV, CLAUDE.md §1.1) routinely goes
    # negative. Surface incompatibility explicitly rather than silently degrading the character read.
    # (Directional efficiency survives sign changes; raw-price VR for spreads is deferred research.)
    n_nonpos = int((close <= 0).sum())
    data_warning = None
    if n_nonpos > 0:
        data_warning = (
            f"Instrument has {n_nonpos} non-positive price(s) (min {float(close.min()):.4g}). "
            "The variance-ratio descriptor uses log-prices, which are undefined on non-positive / "
            "spread series, so the VR axis (OU vs RW) is unavailable here. This is structural "
            "incompatibility, NOT an unfavorable reading. Spread-domain scoring is deferred research."
        )

    sub_df = analytics_substrate.compute_substrate(close, window=window)

    df["date_str"] = df["date"].dt.strftime("%Y-%m-%d")
    dates = df["date_str"].tolist()
    num_cols = ["de", "vr", "rv", "vp", "ou_like", "trend_like", "rw_null", "ambiguous"]

    def _read(v) -> str | None:
        # dominant/confidence are strings; "ambiguous"-on-NaN-descriptors is a real read, but a row
        # with no defined descriptors (warmup) should report no read at all.
        return None if v is None or (isinstance(v, float) and math.isnan(v)) else str(v)

    rows: list[SubstrateRow] = []
    for i in range(len(df)):
        de_i = _f(sub_df["de"].iloc[i])
        scored = de_i is not None  # post-warmup once the trailing window is full
        rows.append(SubstrateRow(
            date=dates[i],
            close=float(close.iloc[i]),
            **{c: _f(sub_df[c].iloc[i]) for c in num_cols},
            dominant=_read(sub_df["dominant"].iloc[i]) if scored else None,
            confidence=_read(sub_df["confidence"].iloc[i]) if scored else None,
        ))

    n_scored = int(sub_df["de"].notna().sum())
    last = sub_df.iloc[-1] if len(sub_df) else None
    stats = SubstrateStats(
        n=len(df),
        n_scored=n_scored,
        dominant_last=_read(last["dominant"]) if last is not None and _f(last["de"]) is not None else None,
        confidence_last=_read(last["confidence"]) if last is not None and _f(last["de"]) is not None else None,
        ou_like_last=_f(last["ou_like"]) if last is not None else None,
        trend_like_last=_f(last["trend_like"]) if last is not None else None,
        rw_null_last=_f(last["rw_null"]) if last is not None else None,
        ambiguous_last=_f(last["ambiguous"]) if last is not None else None,
    )

    return SubstrateResponse(
        instrument_id=instrument_id,
        window=window,
        mode="causal",
        buckets=_SUBSTRATE_BUCKETS,
        regime_warning=_SUBSTRATE_REGIME_WARNING,
        data_warning=data_warning,
        rows=rows,
        stats=stats,
    )
