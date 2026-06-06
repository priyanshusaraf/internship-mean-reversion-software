import pytest
from app.services.loader import load_ohlcv, LoaderError


def test_load_valid_csv(sample_csv):
    df = load_ohlcv(sample_csv)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert len(df) == 3
    assert df.index.name == "date"


def test_load_missing_file():
    with pytest.raises(LoaderError, match="File not found"):
        load_ohlcv("/nonexistent/does_not_exist.csv")


def test_load_missing_ohlcv_columns(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("date,open,close\n2024-01-01,100,101\n")
    with pytest.raises(LoaderError, match="Missing required columns"):
        load_ohlcv(str(path))


def test_load_no_date_column(tmp_path):
    path = tmp_path / "nodatecol.csv"
    path.write_text("idx,open,high,low,close,volume\n1,100,101,99,100,1000\n")
    with pytest.raises(LoaderError, match="No date column found"):
        load_ohlcv(str(path))


def test_load_unsupported_format(tmp_path):
    path = tmp_path / "data.xlsx"
    path.write_bytes(b"fake content")
    with pytest.raises(LoaderError, match="Unsupported format"):
        load_ohlcv(str(path))


def test_load_case_insensitive_columns(tmp_path):
    path = tmp_path / "upper.csv"
    path.write_text("Date,Open,High,Low,Close,Volume\n2024-01-01,100,101,99,100,1000\n")
    df = load_ohlcv(str(path))
    assert "open" in df.columns


def test_sorted_by_date(tmp_path):
    path = tmp_path / "unsorted.csv"
    path.write_text(
        "date,open,high,low,close,volume\n"
        "2024-01-03,102,103,101,102,1000\n"
        "2024-01-01,100,101,99,100,1000\n"
        "2024-01-02,101,102,100,101,1000\n"
    )
    df = load_ohlcv(str(path))
    assert df.index.tolist() == sorted(df.index.tolist())


# --- New tests covering C1, C2, H4 fixes ---

def test_volume_alias_tottrdqty(tmp_path):
    """NSE Bhavcopy uses TOTTRDQTY instead of volume."""
    path = tmp_path / "nse.csv"
    path.write_text("TIMESTAMP,OPEN,HIGH,LOW,CLOSE,TOTTRDQTY\n2024-01-01,100,101,99,100,50000\n")
    df = load_ohlcv(str(path))
    assert "volume" in df.columns
    assert df["volume"].iloc[0] == 50000.0


def test_volume_alias_vol(tmp_path):
    path = tmp_path / "vol.csv"
    path.write_text("date,open,high,low,close,vol\n2024-01-01,100,101,99,100,1000\n")
    df = load_ohlcv(str(path))
    assert "volume" in df.columns


def test_duplicate_timestamps_rejected(tmp_path):
    """Duplicate dates must raise LoaderError, not silently pass to DuckDB."""
    path = tmp_path / "dupes.csv"
    path.write_text(
        "date,open,high,low,close,volume\n"
        "2024-01-01,100,101,99,100,1000\n"
        "2024-01-01,102,103,101,102,2000\n"
        "2024-01-02,103,104,102,103,1500\n"
    )
    with pytest.raises(LoaderError, match="duplicate"):
        load_ohlcv(str(path))


def test_nan_rows_are_dropped(tmp_path):
    """Rows with NaN in OHLC columns are silently dropped rather than hard-failing.
    Volume NaN is filled with 0."""
    path = tmp_path / "nans.csv"
    path.write_text(
        "date,open,high,low,close,volume\n"
        "2024-01-01,100,101,99,100,1000\n"
        "2024-01-02,,103,101,,2000\n"   # NaN open and close — dropped
        "2024-01-03,105,106,104,105,\n" # NaN volume — kept, volume=0
    )
    df = load_ohlcv(str(path))
    assert len(df) == 2  # row 2 dropped, row 3 kept
    assert df.loc["2024-01-03", "volume"] == 0.0


def test_all_nan_rows_raises(tmp_path):
    """If every row has NaN in OHLC, raise LoaderError."""
    path = tmp_path / "all_nan.csv"
    path.write_text(
        "date,open,high,low,close,volume\n"
        "2024-01-01,,101,99,,1000\n"
        "2024-01-02,,103,101,,2000\n"
    )
    with pytest.raises(LoaderError, match="All"):
        load_ohlcv(str(path))


def test_timezone_aware_index_stripped(tmp_path):
    """Timezone-aware timestamps must be stripped to naive dates."""
    path = tmp_path / "tz.csv"
    path.write_text(
        "date,open,high,low,close,volume\n"
        "2024-01-01T00:00:00+05:30,100,101,99,100,1000\n"
        "2024-01-02T00:00:00+05:30,102,103,101,102,2000\n"
    )
    df = load_ohlcv(str(path))
    assert df.index.tz is None
    assert str(df.index[0].date()) == "2024-01-01"
