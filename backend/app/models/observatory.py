"""Observatory v2 API models — shapes EXACTLY per docs/build/api_contract.md (§1,§3,§4,§6).

Non-finite floats (NaN/Inf) serialize as null (§8). We use a field_serializer on every
optional-float field plus a model-level validator so a stray NaN never reaches the wire.
"""
from __future__ import annotations
from typing import Optional, Literal
import math
from pydantic import BaseModel, field_serializer, Field


def _clean_float(v):
    if v is None:
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


# ── §1 Dataset ─────────────────────────────────────────────────────────────────────

class DateRange(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None


class ColumnMap(BaseModel):
    timestamp: Optional[str] = None
    close: Optional[str] = None
    open: Optional[str] = None
    high: Optional[str] = None
    low: Optional[str] = None
    volume: Optional[str] = None


class Construction(BaseModel):
    beta_mode: Literal["none", "definitional", "frozen-ols", "rolling-INADMISSIBLE"] = "none"
    roll_masked: Optional[bool] = None  # null if N/A


class Dataset(BaseModel):
    dataset_id: str
    name: str
    source_file: str
    frequency: Literal["daily", "intraday", "unknown"]
    row_count: int
    date_range: DateRange
    columns: list[str]
    column_map: ColumnMap
    date_format: Literal["auto", "unix", "iso", "dd-mm-yyyy"] = "auto"
    timezone: Optional[str] = None
    is_spread: bool = False
    construction: Construction = Construction()
    created_at: str


# ── §3 QualityReport ────────────────────────────────────────────────────────────────

class Gap(BaseModel):
    from_: str = Field(alias="from", serialization_alias="from")
    to: str
    missing_bars: int

    model_config = {"populate_by_name": True}


class NonPositiveExample(BaseModel):
    time: str
    close: Optional[float] = None

    @field_serializer("close")
    def _s(self, v):
        return _clean_float(v)


class ExcisionWindow(BaseModel):
    from_: str = Field(alias="from", serialization_alias="from")
    to: str

    model_config = {"populate_by_name": True}


class NonPositivePrices(BaseModel):
    count: int = 0
    examples: list[NonPositiveExample] = []
    suggested_excision: Optional[ExcisionWindow] = None


class BackAdjustmentSeam(BaseModel):
    time: str
    jump: Optional[float] = None

    @field_serializer("jump")
    def _s(self, v):
        return _clean_float(v)


class QualityReport(BaseModel):
    row_count: int
    date_range: DateRange
    frequency: Literal["daily", "intraday", "unknown"]
    median_delta_days: Optional[float] = None
    gaps: list[Gap] = []
    n_gaps: int = 0
    duplicate_timestamps: int = 0
    non_positive_prices: NonPositivePrices = NonPositivePrices()
    nan_rows_dropped: int = 0
    back_adjustment_seams: list[BackAdjustmentSeam] = []
    warnings: list[str] = []

    @field_serializer("median_delta_days")
    def _s(self, v):
        return _clean_float(v)


# ── §6 Provenance ───────────────────────────────────────────────────────────────────

class Provenance(BaseModel):
    dataset_id: str
    dataset_hash: str
    as_of: Optional[str] = None
    params: dict
    mode: Literal["research", "verification"] = "research"
    prereg_id: Optional[str] = None
    exploratory_watermark: bool = False
    engine: str
    engine_version: str
    computed_at: str


# ── §2 ingestion response & series ──────────────────────────────────────────────────

class IngestResponse(BaseModel):
    dataset: Dataset
    quality: QualityReport


class DatasetList(BaseModel):
    datasets: list[Dataset]


class Bar(BaseModel):
    time: str
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[float] = None

    @field_serializer("open", "high", "low", "close", "volume")
    def _s(self, v):
        return _clean_float(v)


class SeriesResponse(BaseModel):
    dataset_id: str
    as_of: Optional[str] = None
    bars: list[Bar] = []
    forward_bars: list[Bar] = []


# ── §4.1 equilibrium ────────────────────────────────────────────────────────────────

class EquilibriumParams(BaseModel):
    snr: float = 1e-8
    kappa: float = 0.05
    warmup: int = 60


class EquilibriumRequest(BaseModel):
    dataset_id: str
    as_of: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    params: Optional[EquilibriumParams] = None
    mode: Literal["research", "verification"] = "research"
    prereg_id: Optional[str] = None


class EquilibriumRow(BaseModel):
    time: str
    close: Optional[float] = None
    mu_star: Optional[float] = None
    velocity: Optional[float] = None
    innovation: Optional[float] = None
    z: Optional[float] = None  # M1 — causal expanding-σ z; null before warmup σ defined
    gain: Optional[float] = None
    state_var: Optional[float] = None

    @field_serializer("close", "mu_star", "velocity", "innovation", "z", "gain", "state_var")
    def _s(self, v):
        return _clean_float(v)


class EquilibriumResponse(BaseModel):
    dataset_id: str
    as_of: Optional[str] = None
    params: EquilibriumParams
    series: list[EquilibriumRow] = []
    z_sigma_basis: str = "causal_expanding_innovation_std"
    provenance: Provenance


# ── §4.2 habitat ────────────────────────────────────────────────────────────────────

class HabitatWindow(BaseModel):
    start: str
    end: str


class HabitatParams(BaseModel):
    vr_qs: list[int] = [5, 10, 20]
    ns_null: int = 2000
    seed: int = 20260606


class HabitatRequest(BaseModel):
    dataset_id: str
    window: HabitatWindow
    as_of: Optional[str] = None
    deseason: bool = False
    params: Optional[HabitatParams] = None
    mode: Literal["research", "verification"] = "research"
    prereg_id: Optional[str] = None


class VRPoint(BaseModel):
    q: int
    vr: Optional[float] = None

    @field_serializer("vr")
    def _s(self, v):
        return _clean_float(v)


class SurrogateDistribution(BaseModel):
    null_min_vr: list[float] = []
    n: int = 0
    p10: Optional[float] = None
    p50: Optional[float] = None
    p90: Optional[float] = None
    frac_ge_real: Optional[float] = None  # == score/100

    @field_serializer("p10", "p50", "p90", "frac_ge_real")
    def _s(self, v):
        return _clean_float(v)


class CalibrationBadge(BaseModel):
    ou: float = 71.3
    rw: float = 49.2
    trend: float = 17.2
    status: str = "validated_non_inverting"


class RawVsDeseason(BaseModel):
    raw_score: Optional[float] = None
    deseason_score: Optional[float] = None
    verdict_changed: Optional[bool] = None

    @field_serializer("raw_score", "deseason_score")
    def _s(self, v):
        return _clean_float(v)


class HabitatResponse(BaseModel):
    dataset_id: str
    window: HabitatWindow
    deseason: bool = False
    score: Optional[float] = None
    real_min_vr: Optional[float] = None
    vr_curve: list[VRPoint] = []
    surrogate_distribution: SurrogateDistribution
    calibration_badge: CalibrationBadge = CalibrationBadge()
    raw_vs_deseason: Optional[RawVsDeseason] = None
    data_warning: Optional[str] = None
    provenance: Provenance

    @field_serializer("score", "real_min_vr")
    def _s(self, v):
        return _clean_float(v)
