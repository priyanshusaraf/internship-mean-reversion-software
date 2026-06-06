from pathlib import Path
import pandas as pd

# Columns needed for candlestick chart and all current analytics
REQUIRED_OHLC = {"open", "high", "low", "close"}
DATE_COLUMN_ALIASES = {"date", "timestamp", "time", "datetime"}
VOLUME_ALIASES = {"volume", "vol", "tottrdqty", "qty", "quantity", "contracts", "trdqty"}


class LoaderError(Exception):
    pass


def load_ohlcv(file_path: str) -> pd.DataFrame:
    """
    Load OHLCV data from CSV or Parquet.

    Returns DataFrame indexed by 'date', columns: open, high, low, close, volume.
    - Volume is optional; missing volume is filled with 0.
    - Rows with NaN in OHLC are dropped (not a hard failure).
    - Duplicate timestamps are rejected — they corrupt DuckDB primary key.
    - Timezone info is stripped; dates are stored as naive UTC-day values.
    """
    path = Path(file_path)
    if not path.exists():
        raise LoaderError(f"File not found: {file_path}")

    if path.suffix.lower() == ".parquet":
        df = pd.read_parquet(path)
    elif path.suffix.lower() in (".csv", ".txt"):
        df = pd.read_csv(path)
    else:
        raise LoaderError(f"Unsupported format: {path.suffix!r}. Use .csv or .parquet")

    df.columns = [c.lower().strip() for c in df.columns]

    # Resolve date column
    date_col = next((c for c in df.columns if c in DATE_COLUMN_ALIASES), None)
    if date_col is None:
        raise LoaderError(
            f"No date column found. Expected one of: {sorted(DATE_COLUMN_ALIASES)}. "
            f"Found: {sorted(df.columns.tolist())}"
        )

    # Resolve volume alias (e.g. NSE tottrdqty -> volume)
    if "volume" not in df.columns:
        vol_col = next((c for c in df.columns if c in VOLUME_ALIASES), None)
        if vol_col:
            df = df.rename(columns={vol_col: "volume"})
        else:
            # Volume is not required for any current analytics — fill with 0
            df["volume"] = 0.0

    # Check required OHLC columns
    missing = REQUIRED_OHLC - set(df.columns)
    if missing:
        present = sorted(c for c in df.columns if c not in {date_col})
        raise LoaderError(
            f"Missing required columns: {sorted(missing)}. "
            f"Found: {present}"
        )

    # Parse dates — ISO 8601 first, fall back to dayfirst for DD-MM-YYYY vendor formats
    try:
        df[date_col] = pd.to_datetime(df[date_col], format="ISO8601", utc=False)
    except (ValueError, TypeError):
        df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, utc=False)

    if hasattr(df[date_col].dtype, "tz") and df[date_col].dtype.tz is not None:
        df[date_col] = df[date_col].dt.tz_localize(None)

    df = df.set_index(date_col)
    df.index.name = "date"
    df = df.sort_index()

    # Coerce OHLCV to numeric
    for col in list(REQUIRED_OHLC) + ["volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill volume NaN with 0 (volume is optional)
    df["volume"] = df["volume"].fillna(0.0)

    # Drop rows where any OHLC value is NaN — don't hard-fail, just skip bad rows
    ohlc_nan_mask = df[list(REQUIRED_OHLC)].isna().any(axis=1)
    n_dropped = int(ohlc_nan_mask.sum())
    if n_dropped > 0:
        df = df[~ohlc_nan_mask]
        if df.empty:
            raise LoaderError(
                f"All {n_dropped} rows had NaN values in OHLC columns after parsing. "
                f"Check that open/high/low/close columns contain numeric price data."
            )

    # Truncate to day precision — DuckDB stores DATE (day-level).
    df.index = df.index.normalize()

    # If day-level duplicates exist (intraday data: multiple bars on the same calendar day),
    # resample to daily OHLCV rather than rejecting the file.
    if df.index.duplicated().any():
        df = df.resample('D').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum',
        }).dropna(subset=['open', 'high', 'low', 'close'])

    # Reject genuine duplicate day-level timestamps that survive resampling (shouldn't happen,
    # but guard against malformed files).
    dupes = df.index.duplicated()
    if dupes.any():
        n = int(dupes.sum())
        examples = [str(d.date()) for d in df.index[dupes][:3]]
        raise LoaderError(
            f"{n} duplicate date(s) at day level (e.g. {examples}). "
            f"Check the file for genuine duplicate rows."
        )

    return df[["open", "high", "low", "close", "volume"]]
