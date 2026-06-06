import os
from typing import Optional
import duckdb
import pandas as pd

_DB_PATH = os.environ.get("AMR_DB_PATH", "data/amr.duckdb")

# Test injection point. Tests set this to an in-memory connection so that
# get_db() uses it instead of opening a new file connection.
_conn: Optional[duckdb.DuckDBPyConnection] = None


def _init_schema(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS instruments (
            instrument_id VARCHAR PRIMARY KEY,
            display_name  VARCHAR,
            row_count     INTEGER,
            start_date    DATE,
            end_date      DATE,
            file_path     VARCHAR
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ohlcv (
            instrument_id VARCHAR,
            date          DATE,
            open          DOUBLE,
            high          DOUBLE,
            low           DOUBLE,
            close         DOUBLE,
            volume        DOUBLE,
            PRIMARY KEY (instrument_id, date)
        )
    """)


def init_db() -> None:
    """Create schema once at server startup. Safe to call multiple times."""
    os.makedirs(os.path.dirname(_DB_PATH) or ".", exist_ok=True)
    conn = duckdb.connect(_DB_PATH)
    _init_schema(conn)
    conn.close()


def open_connection() -> duckdb.DuckDBPyConnection:
    """Return the test-injected connection if present, otherwise a fresh file connection."""
    if _conn is not None:
        return _conn
    return duckdb.connect(_DB_PATH)


def store_instrument(
    conn: duckdb.DuckDBPyConnection,
    instrument_id: str,
    display_name: str,
    df: pd.DataFrame,
    file_path: str,
) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO instruments VALUES (?, ?, ?, ?, ?, ?)",
        [
            instrument_id,
            display_name,
            len(df),
            df.index.min().date().isoformat(),
            df.index.max().date().isoformat(),
            file_path,
        ],
    )
    conn.execute("DELETE FROM ohlcv WHERE instrument_id = ?", [instrument_id])
    tmp = df.copy()
    tmp.index.name = "date"
    records = tmp.reset_index()
    records["instrument_id"] = instrument_id
    records = records[["instrument_id", "date", "open", "high", "low", "close", "volume"]]
    conn.execute("INSERT INTO ohlcv SELECT * FROM records")


def list_instruments(conn: duckdb.DuckDBPyConnection) -> list[dict]:
    rows = conn.execute("""
        SELECT instrument_id, display_name, row_count,
               CAST(start_date AS VARCHAR), CAST(end_date AS VARCHAR),
               file_path
        FROM instruments ORDER BY instrument_id
    """).fetchall()
    return [
        {
            "instrument_id": r[0],
            "display_name": r[1],
            "row_count": r[2],
            "start_date": r[3],
            "end_date": r[4],
            "file_path": r[5],
        }
        for r in rows
    ]


def get_ohlcv(
    conn: duckdb.DuckDBPyConnection,
    instrument_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    q = "SELECT date, open, high, low, close, volume FROM ohlcv WHERE instrument_id = ?"
    params: list = [instrument_id]
    if start_date:
        q += " AND date >= ?"
        params.append(start_date)
    if end_date:
        q += " AND date <= ?"
        params.append(end_date)
    q += " ORDER BY date"
    return conn.execute(q, params).df()
