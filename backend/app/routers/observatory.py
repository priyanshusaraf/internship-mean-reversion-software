"""Observatory v2 router — /api/v2/* (contract docs/build/api_contract.md).

Additive and isolated: wraps the existing loader / store / frozen engines. Does NOT touch the
legacy /api/v1/market/* router, analytics.py Kalman code, or loader.py default semantics.

Every number (μ*, z, VR, habitat score, surrogate cloud) comes from a frozen engine. The only
new numerical code is the causal expanding-σ z (Python, contract M1) and the descriptive quality
report — no statistic is implemented in JS, and none is reimplemented here.
"""
from __future__ import annotations
import json
import hashlib
import datetime as _dt
from typing import Optional
import numpy as np
import pandas as pd
import duckdb
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

from app.models.observatory import (
    Dataset, DateRange, ColumnMap, Construction, QualityReport, IngestResponse,
    DatasetList, Bar, SeriesResponse, Provenance,
    EquilibriumRequest, EquilibriumParams, EquilibriumRow, EquilibriumResponse,
    HabitatRequest, HabitatParams, HabitatWindow, VRPoint, SurrogateDistribution,
    CalibrationBadge, RawVsDeseason, HabitatResponse,
)
from app.services import store, analytics
from app.services.observatory_quality import load_ohlcv_mapped, quality_report
from app.services.analytics_habitat import habitat_score_full
from app.services.analytics_arm_a_v2 import deseasonalize_causal
from app.services.loader import LoaderError

router = APIRouter(prefix="/api/v2", tags=["observatory"])

_ENGINE_VERSION = "observatory-v2-slice"
_KALMAN = analytics


def get_db():
    """Per-request DuckDB connection (same injection convention as the legacy router)."""
    is_injected = store._conn is not None
    conn = store.open_connection()
    _ensure_v2_meta(conn)
    try:
        yield conn
    finally:
        if not is_injected:
            conn.close()


# ── v2 metadata sidecar (additive table; does not touch store.py schema) ─────────────

def _ensure_v2_meta(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS v2_dataset_meta ("
        "  dataset_id VARCHAR PRIMARY KEY,"
        "  meta_json  VARCHAR"
        ")"
    )


def _save_meta(conn, dataset_id: str, meta: dict) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO v2_dataset_meta VALUES (?, ?)",
        [dataset_id, json.dumps(meta)],
    )


def _load_meta(conn, dataset_id: str) -> dict:
    row = conn.execute(
        "SELECT meta_json FROM v2_dataset_meta WHERE dataset_id = ?", [dataset_id]
    ).fetchone()
    return json.loads(row[0]) if row else {}


# ── helpers ──────────────────────────────────────────────────────────────────────────

def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def _dataset_hash(df: pd.DataFrame) -> str:
    h = hashlib.sha256()
    h.update(pd.util.hash_pandas_object(df, index=True).values.tobytes())
    return h.hexdigest()[:16]


def _resolve_as_of(df: pd.DataFrame, as_of: Optional[str]) -> Optional[str]:
    """M2 — as_of null ≡ last bar; the cap is ALWAYS applied for causal reads."""
    if df.empty:
        return as_of
    if not as_of:
        return df.index.max().date().isoformat()
    return as_of


def _get_full(conn, dataset_id: str) -> pd.DataFrame:
    """Full stored series, indexed by date. Raises 404 if unknown."""
    known = {r["instrument_id"] for r in store.list_instruments(conn)}
    if dataset_id not in known:
        raise HTTPException(status_code=404, detail=f"unknown dataset {dataset_id}")
    df = store.get_ohlcv(conn, dataset_id)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date").sort_index()
    return df


def _build_dataset_model(conn, dataset_id: str, df: pd.DataFrame) -> Dataset:
    meta = _load_meta(conn, dataset_id)
    insts = {r["instrument_id"]: r for r in store.list_instruments(conn)}
    rec = insts.get(dataset_id, {})
    freq = quality_report(df)["frequency"]
    return Dataset(
        dataset_id=dataset_id,
        name=meta.get("name") or rec.get("display_name") or dataset_id,
        source_file=meta.get("source_file", ""),
        frequency=freq,
        row_count=len(df),
        date_range=DateRange(
            start=df.index.min().date().isoformat() if len(df) else None,
            end=df.index.max().date().isoformat() if len(df) else None,
        ),
        columns=[c for c in ["open", "high", "low", "close", "volume"] if c in df.columns],
        column_map=ColumnMap(**meta.get("column_map", {})),
        date_format=meta.get("date_format", "auto"),
        timezone=meta.get("timezone"),
        is_spread=meta.get("is_spread", False),
        construction=Construction(**meta.get("construction", {"beta_mode": "none", "roll_masked": None})),
        created_at=meta.get("created_at", _now()),
    )


def _reject_inadmissible(conn, dataset_id: str) -> None:
    """M6 — block rolling-INADMISSIBLE β construction at the analysis boundary (422)."""
    meta = _load_meta(conn, dataset_id)
    beta_mode = meta.get("construction", {}).get("beta_mode", "none")
    if beta_mode == "rolling-INADMISSIBLE":
        raise HTTPException(status_code=422, detail="rolling-β is inadmissible for a gating read")


def _causal_z(close: np.ndarray, mu_star: np.ndarray, eps: np.ndarray) -> np.ndarray:
    """M1 — z[t] = (close[t] − mu_star[t]) / σ[t], σ[t] = causal EXPANDING std of innovations
    over t' ≤ t (min 2 obs; null/NaN before that). σ uses ONLY past innovations — never a single
    std over the whole array (which would scale interior-bar z by future volatility)."""
    n = len(close)
    z = np.full(n, np.nan)
    s = pd.Series(eps)
    sigma = s.expanding(min_periods=2).std(ddof=1).to_numpy()
    for t in range(n):
        sig = sigma[t]
        if np.isfinite(sig) and sig > 0 and np.isfinite(close[t]) and np.isfinite(mu_star[t]):
            z[t] = (close[t] - mu_star[t]) / sig
    return z


# ── ingestion & datasets ──────────────────────────────────────────────────────────────

@router.post("/datasets", response_model=IngestResponse)
async def create_dataset(
    file: UploadFile = File(...),
    mapping: Optional[str] = Form(None),
    conn: duckdb.DuckDBPyConnection = Depends(get_db),
):
    """Multipart upload: file + optional JSON `mapping` part. Parse → quality → persist."""
    try:
        m = json.loads(mapping) if mapping else {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="mapping is not valid JSON")

    import tempfile
    from pathlib import Path as _P
    suffix = _P(file.filename or "upload.csv").suffix or ".csv"
    raw_bytes = await file.read()
    with tempfile.NamedTemporaryFile(mode="wb", suffix=suffix, delete=False) as tf:
        tf.write(raw_bytes)
        tmp_path = tf.name

    column_map = m.get("column_map") or {}
    date_format = m.get("date_format", "auto")
    try:
        df = load_ohlcv_mapped(tmp_path, column_map=column_map, date_format=date_format)
    except LoaderError as e:
        raise HTTPException(status_code=422, detail=str(e))
    finally:
        try:
            _P(tmp_path).unlink()
        except OSError:
            pass

    if df.empty:
        raise HTTPException(status_code=422, detail="empty series after parse")

    stem = _P(file.filename or "DATASET").stem.upper()
    name = m.get("name") or stem
    dataset_id = stem

    store.store_instrument(conn, dataset_id, name, df, file.filename or "")

    # Echo back the mapping actually used (auto-detect → canonical names).
    echoed_map = {
        "timestamp": column_map.get("timestamp") or "date",
        "close": column_map.get("close") or "close",
        "open": column_map.get("open"),
        "high": column_map.get("high"),
        "low": column_map.get("low"),
        "volume": column_map.get("volume"),
    }
    meta = {
        "name": name,
        "source_file": file.filename or "",
        "column_map": echoed_map,
        "date_format": date_format,
        "timezone": m.get("timezone"),
        "is_spread": False,
        "construction": {"beta_mode": "none", "roll_masked": None},  # plain upload
        "created_at": _now(),
    }
    _save_meta(conn, dataset_id, meta)

    ds = _build_dataset_model(conn, dataset_id, df)
    q = QualityReport(**quality_report(df))
    return IngestResponse(dataset=ds, quality=q)


@router.get("/datasets", response_model=DatasetList)
def list_datasets(conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    out = []
    for rec in store.list_instruments(conn):
        did = rec["instrument_id"]
        df = store.get_ohlcv(conn, did)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date").sort_index()
        out.append(_build_dataset_model(conn, did, df))
    return DatasetList(datasets=out)


@router.get("/datasets/{dataset_id}", response_model=Dataset)
def get_dataset(dataset_id: str, conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    df = _get_full(conn, dataset_id)
    return _build_dataset_model(conn, dataset_id, df)


@router.get("/datasets/{dataset_id}/series", response_model=SeriesResponse)
def get_series(
    dataset_id: str,
    as_of: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    conn: duckdb.DuckDBPyConnection = Depends(get_db),
):
    df = _get_full(conn, dataset_id)
    resolved = _resolve_as_of(df, as_of)  # M2: null → last bar; cap always applied

    causal = df[df.index <= pd.Timestamp(resolved)] if resolved else df
    forward = df[df.index > pd.Timestamp(resolved)] if resolved else df.iloc[0:0]

    view = causal
    if start:
        view = view[view.index >= pd.Timestamp(start)]
    if end:
        view = view[view.index <= pd.Timestamp(end)]

    def _bar(t, row):
        return Bar(
            time=t.date().isoformat(),
            open=row.get("open"), high=row.get("high"), low=row.get("low"),
            close=row.get("close"), volume=row.get("volume"),
        )

    bars = [_bar(t, r) for t, r in view.iterrows()]
    fwd = [_bar(t, r) for t, r in forward.iterrows()]  # evaluation_only overlay
    return SeriesResponse(dataset_id=dataset_id, as_of=resolved, bars=bars, forward_bars=fwd)


@router.get("/datasets/{dataset_id}/quality", response_model=QualityReport)
def get_quality(dataset_id: str, conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    df = _get_full(conn, dataset_id)
    return QualityReport(**quality_report(df))


# ── analysis — equilibrium ─────────────────────────────────────────────────────────────

@router.post("/analysis/equilibrium", response_model=EquilibriumResponse)
def analysis_equilibrium(req: EquilibriumRequest, conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    _reject_inadmissible(conn, req.dataset_id)
    df = _get_full(conn, req.dataset_id)

    resolved = _resolve_as_of(df, req.as_of)
    causal = df[df.index <= pd.Timestamp(resolved)] if resolved else df  # slice BEFORE engine
    if causal.empty:
        raise HTTPException(status_code=422, detail="no data at or before as_of")

    params = req.params or EquilibriumParams()
    frozen = EquilibriumParams()
    watermark = (params.snr != frozen.snr or params.kappa != frozen.kappa or params.warmup != frozen.warmup)
    mode = "research"

    kf = _KALMAN.compute_kalman_mu_star(
        causal["close"], snr=params.snr, kappa=params.kappa, warmup=params.warmup
    )
    closes = causal["close"].to_numpy(dtype=float)
    mu = kf["mu_star_kalman"].to_numpy()
    eps = kf["epsilon_kalman"].to_numpy()
    vel = kf["kalman_velocity"].to_numpy()
    gain = kf["kalman_gain"].to_numpy()
    svar = kf["kalman_state_var"].to_numpy()
    z = _causal_z(closes, mu, eps)  # M1 causal expanding-σ z

    # view trim for display only (does not change causal computation)
    times = causal.index
    keep = np.ones(len(times), dtype=bool)
    if req.start:
        keep &= (times >= pd.Timestamp(req.start)).to_numpy()
    if req.end:
        keep &= (times <= pd.Timestamp(req.end)).to_numpy()

    series = []
    for i in range(len(times)):
        if not keep[i]:
            continue
        series.append(EquilibriumRow(
            time=times[i].date().isoformat(),
            close=closes[i], mu_star=mu[i], velocity=vel[i],
            innovation=eps[i], z=z[i], gain=gain[i], state_var=svar[i],
        ))

    prov = Provenance(
        dataset_id=req.dataset_id,
        dataset_hash=_dataset_hash(causal),
        as_of=resolved,
        params={"snr": params.snr, "kappa": params.kappa, "warmup": params.warmup},
        mode=mode,
        prereg_id=None,
        exploratory_watermark=bool(watermark),
        engine="compute_kalman_mu_star",
        engine_version=_ENGINE_VERSION,
        computed_at=_now(),
    )
    return EquilibriumResponse(
        dataset_id=req.dataset_id, as_of=resolved, params=params,
        series=series, z_sigma_basis="causal_expanding_innovation_std", provenance=prov,
    )


# ── analysis — habitat ──────────────────────────────────────────────────────────────────

def _window_and_presample(causal: pd.DataFrame, w: HabitatWindow, deseason: bool):
    """Return (window_levels, pre_sample_levels). Optionally causal-deseasonalize the FULL causal
    close series first, then window (deseason mean uses only ≤ t-1 — §6.1).

    pre_sample = causal levels STRICTLY before window.start. This is the only data the GARCH null
    is fit on (§6.1 temporal firewall — never the window under test). `causal` is already capped at
    ≤ as_of upstream, so the pre-sample is fully causal."""
    if deseason:
        ds = deseasonalize_causal(causal["close"].to_numpy(dtype=float), causal.index)
        s = pd.Series(ds, index=causal.index)
    else:
        s = causal["close"]
    start = pd.Timestamp(w.start)
    win = s[(s.index >= start) & (s.index <= pd.Timestamp(w.end))].to_numpy(dtype=float)
    pre = s[s.index < start].to_numpy(dtype=float)
    return win, pre


@router.post("/analysis/habitat", response_model=HabitatResponse)
def analysis_habitat(req: HabitatRequest, conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    _reject_inadmissible(conn, req.dataset_id)  # M6
    df = _get_full(conn, req.dataset_id)
    resolved = _resolve_as_of(df, req.as_of)

    # window.end must be <= as_of (422) — contract §5
    if resolved and pd.Timestamp(req.window.end) > pd.Timestamp(resolved):
        raise HTTPException(status_code=422, detail="window extends past as_of")

    causal = df[df.index <= pd.Timestamp(resolved)] if resolved else df  # slice BEFORE engine

    params = req.params or HabitatParams()
    seed = params.seed

    x_raw, pre_raw = _window_and_presample(causal, req.window, deseason=False)
    full_raw = habitat_score_full(x_raw, seed, pre_sample=pre_raw)

    # Non-positive series (spreads cross or sit below zero): the habitat null engine already
    # uses LEVEL-difference VR (analytics_habitat.vr_q; surrogates built from ΔS, never log),
    # so the score is computed normally and is NOT null. Emit an INFORMATIONAL note (ℹ), not a
    # warning — there is no degeneracy here; level-difference math is the correct path. (CHANGE 4)
    data_warning = None
    if np.any(x_raw <= 0):
        data_warning = (
            "ℹ spread/level instrument detected — using level-difference VR "
            "(log undefined on negative prices; this is expected for spread instruments)."
        )

    # deseason path (toggle field always present)
    raw_vs_deseason = None
    used = full_raw
    if req.deseason:
        x_ds, pre_ds = _window_and_presample(causal, req.window, deseason=True)
        full_ds = habitat_score_full(x_ds, seed, pre_sample=pre_ds)
        used = full_ds
        rs, ds_s = full_raw["score"], full_ds["score"]
        verdict_changed = None
        if np.isfinite(rs) and np.isfinite(ds_s):
            # contamination flag: a verdict flip across the 50 (beats-null) threshold
            verdict_changed = (rs >= 50.0) != (ds_s >= 50.0)
        raw_vs_deseason = RawVsDeseason(
            raw_score=rs, deseason_score=ds_s, verdict_changed=verdict_changed,
        )

    # GARCH gate defaulted (insufficient pre-sample) → conservative non-confirmatory notice.
    if used.get("garch_defaulted"):
        garch_msg = ("insufficient pre-sample for GARCH fit — GARCH gate defaulting to "
                     "non-confirmatory")
        data_warning = f"{data_warning} · {garch_msg}" if data_warning else garch_msg

    nulls = used["null_min_vr"]
    score = used["score"]
    if nulls:
        arr = np.array(nulls)
        p10, p50, p90 = (float(np.percentile(arr, p)) for p in (10, 50, 90))
    else:
        p10 = p50 = p90 = float("nan")
    frac_ge = (score / 100.0) if np.isfinite(score) else None

    surrogate = SurrogateDistribution(
        null_min_vr=nulls, n=len(nulls), p10=p10, p50=p50, p90=p90, frac_ge_real=frac_ge,
    )
    vr_curve = [VRPoint(q=p["q"], vr=p["vr"]) for p in used["vr_curve"]]

    prov = Provenance(
        dataset_id=req.dataset_id,
        dataset_hash=_dataset_hash(causal),
        as_of=resolved,
        params={"vr_qs": params.vr_qs, "ns_null": params.ns_null, "seed": seed, "deseason": req.deseason},
        mode="research",
        prereg_id=None,
        exploratory_watermark=False,
        engine="habitat_score_full",
        engine_version=_ENGINE_VERSION,
        computed_at=_now(),
    )
    return HabitatResponse(
        dataset_id=req.dataset_id,
        window=req.window,
        deseason=req.deseason,
        score=score,
        real_min_vr=used["real_min_vr"],
        vr_curve=vr_curve,
        surrogate_distribution=surrogate,
        calibration_badge=CalibrationBadge(),
        raw_vs_deseason=raw_vs_deseason,
        data_warning=data_warning,
        confirmed=bool(used.get("confirmed", False)),
        p_rw=used.get("p_rw"),
        p_garch=used.get("p_garch"),
        p_ma1=used.get("p_ma1"),
        gate_note=used.get("gate_note"),
        provenance=prov,
    )
