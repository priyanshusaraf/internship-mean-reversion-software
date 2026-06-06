import duckdb
import pandas as pd
import pytest
from app.services.store import _init_schema, store_instrument, list_instruments, get_ohlcv


@pytest.fixture
def conn():
    c = duckdb.connect(":memory:")
    _init_schema(c)
    yield c
    c.close()


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "open":   [100.0, 101.0, 102.0],
            "high":   [101.0, 102.0, 103.0],
            "low":    [99.0,  100.0, 101.0],
            "close":  [100.5, 101.5, 102.5],
            "volume": [1000.0, 1100.0, 900.0],
        },
        index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
    )


def test_store_and_list(conn, sample_df):
    store_instrument(conn, "NIFTY", "NIFTY50", sample_df, "/data/nifty.csv")
    instruments = list_instruments(conn)
    assert len(instruments) == 1
    assert instruments[0]["instrument_id"] == "NIFTY"
    assert instruments[0]["row_count"] == 3


def test_get_ohlcv_all(conn, sample_df):
    store_instrument(conn, "NIFTY", "NIFTY50", sample_df, "/data/nifty.csv")
    df = get_ohlcv(conn, "NIFTY")
    assert len(df) == 3


def test_get_ohlcv_date_filter(conn, sample_df):
    store_instrument(conn, "NIFTY", "NIFTY50", sample_df, "/data/nifty.csv")
    df = get_ohlcv(conn, "NIFTY", start_date="2024-01-02", end_date="2024-01-02")
    assert len(df) == 1


def test_overwrite_on_reload(conn, sample_df):
    store_instrument(conn, "NIFTY", "NIFTY50", sample_df, "/data/nifty.csv")
    store_instrument(conn, "NIFTY", "NIFTY50", sample_df.iloc[:2], "/data/nifty.csv")
    df = get_ohlcv(conn, "NIFTY")
    assert len(df) == 2


def test_empty_for_unknown_instrument(conn):
    df = get_ohlcv(conn, "UNKNOWN")
    assert len(df) == 0
