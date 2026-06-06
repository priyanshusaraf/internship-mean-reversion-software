"""Observatory v2 — data-quality report + mapping-aware ingestion (contract §3, §2).

Additive and isolated: the default `loader.load_ohlcv` path is unchanged. `load_ohlcv_mapped`
applies an optional column_map / date_format override by renaming/reformatting the raw frame
BEFORE handing it to the existing loader, so the existing parse/resample/dedupe semantics are
reused verbatim. The quality report is descriptive-only over the parsed frame.
"""
from __future__ import annotations
from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd

from app.services.loader import load_ohlcv, LoaderError


# ── Mapping-aware ingestion (additive wrapper around load_ohlcv) ─────────────────────

def load_ohlcv_mapped(
    file_path: str,
    column_map: Optional[dict] = None,
    date_format: str = "auto",
) -> pd.DataFrame:
    """Parse OHLCV with an OPTIONAL explicit column mapping / date format.

    When column_map/date_format are absent (or "auto"), this is a thin pass-through to the
    existing auto-detecting `load_ohlcv` (default behavior preserved exactly). When an override
    is supplied, the raw CSV/Parquet is rewritten to canonical column names (+ optional explicit
    date parse) into a temp file, then run through the SAME `load_ohlcv` for identical
    resample/dedupe/NaN semantics.
    """
    has_map = bool(column_map) and any(column_map.get(k) for k in column_map)
    if not has_map and (date_format in (None, "auto")):
        return load_ohlcv(file_path)

    path = Path(file_path)
    if not path.exists():
        raise LoaderError(f"File not found: {file_path}")
    if path.suffix.lower() == ".parquet":
        raw = pd.read_parquet(path)
    elif path.suffix.lower() in (".csv", ".txt"):
        raw = pd.read_csv(path)
    else:
        raise LoaderError(f"Unsupported format: {path.suffix!r}. Use .csv or .parquet")

    cmap = column_map or {}
    rename = {}
    ts_src = cmap.get("timestamp")
    if ts_src:
        if ts_src not in raw.columns:
            raise LoaderError(f"mapped timestamp column {ts_src!r} not in file")
        rename[ts_src] = "timestamp"
    for canon in ("open", "high", "low", "close", "volume"):
        src = cmap.get(canon)
        if src:
            if src not in raw.columns:
                raise LoaderError(f"mapped {canon} column {src!r} not in file")
            rename[src] = canon
    raw = raw.rename(columns=rename)

    if "close" not in raw.columns:
        raise LoaderError("missing required close column after mapping")

    # Explicit date_format override applied here; loader handles "auto".
    ts_col = "timestamp" if "timestamp" in raw.columns else None
    if ts_col and date_format not in (None, "auto"):
        if date_format == "unix":
            raw[ts_col] = pd.to_datetime(raw[ts_col].astype(float), unit="s", utc=False)
        elif date_format == "iso":
            raw[ts_col] = pd.to_datetime(raw[ts_col], format="ISO8601", utc=False)
        elif date_format == "dd-mm-yyyy":
            raw[ts_col] = pd.to_datetime(raw[ts_col], dayfirst=True, utc=False)

    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tf:
        tmp_path = tf.name
    raw.to_csv(tmp_path, index=False)
    try:
        return load_ohlcv(tmp_path)
    finally:
        try:
            Path(tmp_path).unlink()
        except OSError:
            pass


# ── Quality report (descriptive only; contract §3) ──────────────────────────────────

def quality_report(df: pd.DataFrame) -> dict:
    """Descriptive quality report over a parsed OHLCV frame (DatetimeIndex 'date').

    Flags — never silently mutates. Non-positive prices are FLAGGED, not dropped.
    Returns a plain dict matching the QualityReport model shape.
    """
    n = len(df)
    idx = df.index
    warnings: list[str] = []

    date_range = {"start": None, "end": None}
    if n:
        date_range = {
            "start": idx.min().date().isoformat(),
            "end": idx.max().date().isoformat(),
        }

    # Frequency from median timestamp delta.
    median_delta_days = None
    frequency = "unknown"
    gaps: list[dict] = []
    if n >= 2:
        deltas = np.diff(idx.values).astype("timedelta64[s]").astype(float) / 86400.0
        median_delta_days = float(np.median(deltas))
        frequency = "daily" if median_delta_days <= 1.5 else "intraday"
        if median_delta_days <= 0:
            frequency = "intraday"
        # Modal delta for gap detection.
        modal = median_delta_days if median_delta_days > 0 else 1.0
        gap_threshold = max(modal * 1.5, modal + 1.0)
        for i in range(1, n):
            d = deltas[i - 1]
            if d > gap_threshold and modal > 0:
                missing = int(round(d / modal)) - 1
                gaps.append({
                    "from": idx[i - 1].date().isoformat(),
                    "to": idx[i].date().isoformat(),
                    "missing_bars": max(missing, 1),
                })

    # Duplicate timestamps (post-parse, day-level — loader resamples, so usually 0).
    duplicate_timestamps = int(idx.duplicated().sum())

    # Non-positive prices — FLAG, do not drop.
    npos = {"count": 0, "examples": [], "suggested_excision": None}
    if n and "close" in df.columns:
        nonpos_mask = df["close"] <= 0
        cnt = int(nonpos_mask.sum())
        npos["count"] = cnt
        if cnt > 0:
            ex_idx = df.index[nonpos_mask][:5]
            npos["examples"] = [
                {"time": t.date().isoformat(), "close": float(df.loc[t, "close"])}
                for t in ex_idx
            ]
            # Suggested excision = the contiguous run of non-positive bars (CL Apr-2020 case).
            runs = _contiguous_runs(nonpos_mask.values)
            if runs:
                s, e = max(runs, key=lambda r: r[1] - r[0])
                npos["suggested_excision"] = {
                    "from": df.index[s].date().isoformat(),
                    "to": df.index[e].date().isoformat(),
                }
            warnings.append(
                f"{cnt} non-positive close price(s) flagged — log-VR undefined; "
                f"flagged not dropped (spreads may legitimately go negative)."
            )

    # Back-adjustment seams — best-effort large single-bar jumps (contract: [] acceptable).
    seams: list[dict] = []
    if n >= 30 and "close" in df.columns:
        closes = df["close"].to_numpy(dtype=float)
        dlog = np.diff(np.log(np.where(closes > 0, closes, np.nan)))
        finite = dlog[np.isfinite(dlog)]
        if finite.size >= 20:
            sd = float(np.std(finite))
            if sd > 0:
                thr = 8.0 * sd  # very conservative — only egregious single-bar jumps
                for i in range(1, n):
                    if i - 1 < len(dlog) and np.isfinite(dlog[i - 1]) and abs(dlog[i - 1]) > thr:
                        seams.append({
                            "time": df.index[i].date().isoformat(),
                            "jump": float(closes[i] - closes[i - 1]),
                        })
        if seams:
            warnings.append(f"{len(seams)} large single-bar jump(s) — possible back-adjustment seam(s).")

    if gaps:
        warnings.append(f"{len(gaps)} calendar gap(s) larger than the modal bar spacing.")

    return {
        "row_count": n,
        "date_range": date_range,
        "frequency": frequency,
        "median_delta_days": median_delta_days,
        "gaps": gaps,
        "n_gaps": len(gaps),
        "duplicate_timestamps": duplicate_timestamps,
        "non_positive_prices": npos,
        "nan_rows_dropped": 0,  # loader drops NaN OHLC rows before persistence; not recoverable here
        "back_adjustment_seams": seams,
        "warnings": warnings,
    }


def _contiguous_runs(mask: np.ndarray) -> list[tuple[int, int]]:
    """Return [start, end] index pairs (inclusive) of contiguous True runs."""
    runs = []
    i = 0
    n = len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j + 1 < n and mask[j + 1]:
                j += 1
            runs.append((i, j))
            i = j + 1
        else:
            i += 1
    return runs
