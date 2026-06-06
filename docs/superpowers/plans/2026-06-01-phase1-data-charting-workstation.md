# Phase 1: Data + Charting Workstation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Load OHLCV data from CSV/Parquet and visualize it as an institutional-quality candlestick chart with zoom, pan, and interval selection. No equilibrium estimators yet.

**Architecture:** FastAPI backend stores validated OHLCV in DuckDB (in-memory); Next.js 15 frontend renders lightweight-charts candlestick with a Zustand store. The only user-visible data flow is: load a file path → instrument appears in sidebar → select it → candles appear → adjust date range.

**Tech Stack:** Python 3.13, FastAPI, Pandas, DuckDB, Pydantic v2 / Next.js 15, TypeScript, Tailwind, lightweight-charts v4, Zustand

---

## File Map

```
backend/
  pyproject.toml
  app/
    __init__.py
    main.py                  # FastAPI app + CORS + router registration
    models/
      __init__.py
      market.py              # OHLCVBar, InstrumentMeta, LoadRequest, LoadResponse, OHLCVResponse
    services/
      __init__.py
      loader.py              # load_ohlcv(file_path) -> pd.DataFrame; raises LoaderError
      store.py               # DuckDB singleton; store/list/query instruments+ohlcv
    routers/
      __init__.py
      market.py              # POST /load, GET /instruments, GET /{id}/ohlcv
  tests/
    __init__.py
    conftest.py              # sample_csv fixture
    test_loader.py
    test_store.py
    test_market_router.py

frontend/
  package.json
  next.config.ts
  tailwind.config.ts
  tsconfig.json
  src/
    app/
      layout.tsx
      page.tsx               # workstation shell: InstrumentPanel + IntervalBar + ChartWorkspace
      globals.css
    components/
      workspace/
        InstrumentPanel.tsx  # file-path input + loaded instrument list
        IntervalBar.tsx      # preset buttons (1M/3M/6M/1Y/ALL) + date range inputs
        ChartWorkspace.tsx   # lightweight-charts candlestick, resize-aware
    lib/
      types.ts               # OHLCVBar, InstrumentMeta, LoadRequest, LoadResponse, OHLCVResponse
      api.ts                 # typed fetch wrappers: loadInstrument, listInstruments, getOHLCV
      store.ts               # Zustand: selectedInstrumentId, dateRange, bars, loading, error
```

---

## Task 1: Backend — pyproject.toml + venv setup

**Files:**
- Create: `backend/pyproject.toml`

- [ ] **Step 1: Write pyproject.toml**

```toml
[project]
name = "amr-backend"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "pandas>=2.2.0",
    "pyarrow>=17.0.0",
    "duckdb>=1.1.0",
    "pydantic>=2.8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "httpx>=0.27.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]

[build-system]
requires = ["setuptools>=75"]
build-backend = "setuptools.backends.legacy:build"
```

- [ ] **Step 2: Install into existing venv**

```bash
cd backend
source .venv/bin/activate
pip install -e ".[dev]"
```

Expected: successfully installs fastapi, uvicorn, pandas, duckdb, etc.

---

## Task 2: Backend — app scaffold + health check

**Files:**
- Create: `backend/app/__init__.py`
- Create: `backend/app/main.py`
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/conftest.py`

- [ ] **Step 1: Write `backend/app/__init__.py`** (empty file)

- [ ] **Step 2: Write `backend/app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AMR Research Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}
```

- [ ] **Step 3: Write `backend/tests/__init__.py`** (empty)

- [ ] **Step 4: Write `backend/tests/conftest.py`**

```python
import csv
import pytest


@pytest.fixture
def sample_csv(tmp_path) -> str:
    path = tmp_path / "nifty.csv"
    rows = [
        ["date", "open", "high", "low", "close", "volume"],
        ["2024-01-01", "21000.0", "21200.0", "20900.0", "21100.0", "1000000"],
        ["2024-01-02", "21100.0", "21300.0", "21000.0", "21250.0", "1100000"],
        ["2024-01-03", "21250.0", "21400.0", "21100.0", "21150.0", "900000"],
    ]
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    return str(path)
```

- [ ] **Step 5: Write a health check test**

Create `backend/tests/test_health.py`:
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
```

- [ ] **Step 6: Run and verify**

```bash
cd backend && source .venv/bin/activate && python -m pytest tests/test_health.py -v
```
Expected: `test_health PASSED`

- [ ] **Step 7: Commit**
```bash
git add backend/
git commit -m "feat: backend scaffold with health check"
```

---

## Task 3: Backend — Pydantic models

**Files:**
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/market.py`

- [ ] **Step 1: Write `backend/app/models/__init__.py`** (empty)

- [ ] **Step 2: Write `backend/app/models/market.py`**

```python
from pydantic import BaseModel


class OHLCVBar(BaseModel):
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: float


class InstrumentMeta(BaseModel):
    instrument_id: str
    display_name: str
    row_count: int
    start_date: str
    end_date: str


class LoadRequest(BaseModel):
    file_path: str
    instrument_id: str
    display_name: str | None = None


class LoadResponse(BaseModel):
    instrument_id: str
    row_count: int
    start_date: str
    end_date: str
    columns: list[str]


class OHLCVResponse(BaseModel):
    instrument_id: str
    bars: list[OHLCVBar]
```

- [ ] **Step 3: Verify models import cleanly**

```bash
cd backend && source .venv/bin/activate && python -c "from app.models.market import OHLCVBar, InstrumentMeta; print('ok')"
```
Expected: `ok`

---

## Task 4: Backend — loader service

**Files:**
- Create: `backend/app/services/__init__.py`
- Create: `backend/app/services/loader.py`
- Create: `backend/tests/test_loader.py`

- [ ] **Step 1: Write `backend/app/services/__init__.py`** (empty)

- [ ] **Step 2: Write failing tests first** (`backend/tests/test_loader.py`)

```python
import csv
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
```

- [ ] **Step 3: Run tests — verify they fail**

```bash
cd backend && source .venv/bin/activate && python -m pytest tests/test_loader.py -v 2>&1 | head -20
```
Expected: `ImportError` (module doesn't exist yet)

- [ ] **Step 4: Write `backend/app/services/loader.py`**

```python
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"open", "high", "low", "close", "volume"}
DATE_COLUMN_ALIASES = {"date", "timestamp", "time", "datetime"}


class LoaderError(Exception):
    pass


def load_ohlcv(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise LoaderError(f"File not found: {file_path}")

    if path.suffix.lower() == ".parquet":
        df = pd.read_parquet(path)
    elif path.suffix.lower() in (".csv", ".txt"):
        df = pd.read_csv(path)
    else:
        raise LoaderError(f"Unsupported format: {path.suffix}. Use .csv or .parquet")

    df.columns = [c.lower().strip() for c in df.columns]

    date_col = next((c for c in df.columns if c in DATE_COLUMN_ALIASES), None)
    if date_col is None:
        raise LoaderError(f"No date column found. Expected one of: {DATE_COLUMN_ALIASES}")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise LoaderError(f"Missing required columns: {missing}")

    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col)
    df.index.name = "date"
    df = df.sort_index()

    for col in REQUIRED_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df[["open", "high", "low", "close", "volume"]]
```

- [ ] **Step 5: Run tests — verify they pass**

```bash
cd backend && source .venv/bin/activate && python -m pytest tests/test_loader.py -v
```
Expected: 7 tests PASSED

- [ ] **Step 6: Commit**
```bash
git add backend/app/services/ backend/tests/test_loader.py
git commit -m "feat: OHLCV loader service with validation"
```

---

## Task 5: Backend — DuckDB store service

**Files:**
- Create: `backend/app/services/store.py`
- Create: `backend/tests/test_store.py`

- [ ] **Step 1: Write failing tests** (`backend/tests/test_store.py`)

```python
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
            "open": [100.0, 101.0, 102.0],
            "high": [101.0, 102.0, 103.0],
            "low": [99.0, 100.0, 101.0],
            "close": [100.5, 101.5, 102.5],
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
```

- [ ] **Step 2: Run — verify fail**

```bash
cd backend && source .venv/bin/activate && python -m pytest tests/test_store.py -v 2>&1 | head -5
```
Expected: `ImportError`

- [ ] **Step 3: Write `backend/app/services/store.py`**

```python
import duckdb
import pandas as pd
from typing import Optional

_conn: Optional[duckdb.DuckDBPyConnection] = None


def get_connection() -> duckdb.DuckDBPyConnection:
    global _conn
    if _conn is None:
        _conn = duckdb.connect(":memory:")
        _init_schema(_conn)
    return _conn


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
    records = df.reset_index().copy()
    records["instrument_id"] = instrument_id
    records = records[["instrument_id", "date", "open", "high", "low", "close", "volume"]]
    conn.register("_tmp", records)
    conn.execute("INSERT INTO ohlcv SELECT * FROM _tmp")
    conn.unregister("_tmp")


def list_instruments(conn: duckdb.DuckDBPyConnection) -> list[dict]:
    rows = conn.execute("""
        SELECT instrument_id, display_name, row_count,
               CAST(start_date AS VARCHAR), CAST(end_date AS VARCHAR)
        FROM instruments ORDER BY instrument_id
    """).fetchall()
    return [
        {"instrument_id": r[0], "display_name": r[1], "row_count": r[2],
         "start_date": r[3], "end_date": r[4]}
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
```

- [ ] **Step 4: Run tests — verify pass**

```bash
cd backend && source .venv/bin/activate && python -m pytest tests/test_store.py -v
```
Expected: 5 tests PASSED

- [ ] **Step 5: Commit**
```bash
git add backend/app/services/store.py backend/tests/test_store.py
git commit -m "feat: DuckDB store service"
```

---

## Task 6: Backend — market router

**Files:**
- Create: `backend/app/routers/__init__.py`
- Create: `backend/app/routers/market.py`
- Modify: `backend/app/main.py`
- Create: `backend/tests/test_market_router.py`

- [ ] **Step 1: Write failing router tests** (`backend/tests/test_market_router.py`)

```python
import duckdb
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import store
from app.services.store import _init_schema


@pytest.fixture(autouse=True)
def fresh_store():
    c = duckdb.connect(":memory:")
    _init_schema(c)
    store._conn = c
    yield
    store._conn = None


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    assert client.get("/health").status_code == 200


def test_load_valid_file(client, sample_csv):
    resp = client.post("/api/v1/market/load", json={
        "file_path": sample_csv, "instrument_id": "NIFTY"
    })
    assert resp.status_code == 200
    assert resp.json()["row_count"] == 3


def test_load_missing_file(client):
    resp = client.post("/api/v1/market/load", json={
        "file_path": "/no/such/file.csv", "instrument_id": "X"
    })
    assert resp.status_code == 422


def test_list_instruments_empty(client):
    assert client.get("/api/v1/market/instruments").json() == []


def test_list_instruments_after_load(client, sample_csv):
    client.post("/api/v1/market/load", json={"file_path": sample_csv, "instrument_id": "NIFTY"})
    assert len(client.get("/api/v1/market/instruments").json()) == 1


def test_get_ohlcv(client, sample_csv):
    client.post("/api/v1/market/load", json={"file_path": sample_csv, "instrument_id": "NIFTY"})
    resp = client.get("/api/v1/market/NIFTY/ohlcv")
    assert resp.status_code == 200
    bars = resp.json()["bars"]
    assert len(bars) == 3
    assert bars[0]["time"] == "2024-01-01"


def test_get_ohlcv_date_filter(client, sample_csv):
    client.post("/api/v1/market/load", json={"file_path": sample_csv, "instrument_id": "NIFTY"})
    resp = client.get("/api/v1/market/NIFTY/ohlcv?start=2024-01-02&end=2024-01-02")
    assert len(resp.json()["bars"]) == 1


def test_get_ohlcv_unknown_instrument(client):
    assert client.get("/api/v1/market/UNKNOWN/ohlcv").status_code == 404
```

- [ ] **Step 2: Create `backend/app/routers/__init__.py`** (empty)

- [ ] **Step 3: Write `backend/app/routers/market.py`**

```python
from typing import Optional
import duckdb
from fastapi import APIRouter, Depends, HTTPException
from app.models.market import (
    LoadRequest, LoadResponse, InstrumentMeta, OHLCVBar, OHLCVResponse
)
from app.services import store
from app.services.loader import load_ohlcv, LoaderError

router = APIRouter(prefix="/api/v1/market", tags=["market"])


def get_db() -> duckdb.DuckDBPyConnection:
    return store.get_connection()


@router.post("/load", response_model=LoadResponse)
def load_instrument(req: LoadRequest, conn=Depends(get_db)):
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
def list_instruments(conn=Depends(get_db)):
    return [InstrumentMeta(**r) for r in store.list_instruments(conn)]


@router.get("/{instrument_id}/ohlcv", response_model=OHLCVResponse)
def get_ohlcv(
    instrument_id: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    conn=Depends(get_db),
):
    df = store.get_ohlcv(conn, instrument_id, start, end)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data for: {instrument_id}")
    bars = [
        OHLCVBar(
            time=row["date"].strftime("%Y-%m-%d"),
            open=row["open"],
            high=row["high"],
            low=row["low"],
            close=row["close"],
            volume=row["volume"],
        )
        for _, row in df.iterrows()
    ]
    return OHLCVResponse(instrument_id=instrument_id, bars=bars)
```

- [ ] **Step 4: Register router in `backend/app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import market

app = FastAPI(title="AMR Research Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market.router)


@app.get("/health")
def health():
    return {"status": "ok"}
```

- [ ] **Step 5: Run all backend tests**

```bash
cd backend && source .venv/bin/activate && python -m pytest -v
```
Expected: all tests PASSED (health + loader + store + router)

- [ ] **Step 6: Commit**
```bash
git add backend/app/routers/ backend/app/main.py backend/tests/test_market_router.py
git commit -m "feat: market router — load, list instruments, OHLCV query"
```

---

## Task 7: Frontend — scaffold

**Files:** All files under `frontend/`

- [ ] **Step 1: Scaffold Next.js 15 app**

```bash
cd /Users/priyanshusaraf/Desktop/internship-final-reports/frontend
npx create-next-app@15 . --typescript --tailwind --app --src-dir --no-eslint --import-alias "@/*" --yes
```
Expected: project created, `node_modules/` installed, `src/app/` present

- [ ] **Step 2: Install additional dependencies**

```bash
cd frontend
npm install lightweight-charts@4 zustand lucide-react
```
Expected: packages added to `node_modules/`

- [ ] **Step 3: Verify dev server starts**

```bash
cd frontend && npm run dev &
sleep 5 && curl -s http://localhost:3000 | head -5
kill %1
```
Expected: HTML response from Next.js dev server

- [ ] **Step 4: Commit**
```bash
git add frontend/
git commit -m "feat: Next.js 15 frontend scaffold"
```

---

## Task 8: Frontend — types + API client + Zustand store

**Files:**
- Create: `frontend/src/lib/types.ts`
- Create: `frontend/src/lib/api.ts`
- Create: `frontend/src/lib/store.ts`

- [ ] **Step 1: Write `frontend/src/lib/types.ts`**

```typescript
export interface OHLCVBar {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface InstrumentMeta {
  instrument_id: string;
  display_name: string;
  row_count: number;
  start_date: string;
  end_date: string;
}

export interface LoadRequest {
  file_path: string;
  instrument_id: string;
  display_name?: string;
}

export interface LoadResponse {
  instrument_id: string;
  row_count: number;
  start_date: string;
  end_date: string;
  columns: string[];
}

export interface OHLCVResponse {
  instrument_id: string;
  bars: OHLCVBar[];
}
```

- [ ] **Step 2: Write `frontend/src/lib/api.ts`**

```typescript
import type { LoadRequest, LoadResponse, InstrumentMeta, OHLCVResponse } from './types';

const BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error((err as { detail?: string }).detail ?? 'Request failed');
  }
  return res.json() as Promise<T>;
}

export const api = {
  loadInstrument: (body: LoadRequest) =>
    request<LoadResponse>('/api/v1/market/load', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  listInstruments: () =>
    request<InstrumentMeta[]>('/api/v1/market/instruments'),

  getOHLCV: (instrumentId: string, start?: string, end?: string) => {
    const params = new URLSearchParams();
    if (start) params.set('start', start);
    if (end) params.set('end', end);
    const qs = params.toString();
    return request<OHLCVResponse>(
      `/api/v1/market/${instrumentId}/ohlcv${qs ? `?${qs}` : ''}`
    );
  },
};
```

- [ ] **Step 3: Write `frontend/src/lib/store.ts`**

```typescript
import { create } from 'zustand';
import type { InstrumentMeta, OHLCVBar } from './types';

interface DateRange {
  start: string | null;
  end: string | null;
}

interface WorkstationState {
  instruments: InstrumentMeta[];
  selectedInstrumentId: string | null;
  dateRange: DateRange;
  bars: OHLCVBar[];
  isLoading: boolean;
  error: string | null;
  setInstruments: (instruments: InstrumentMeta[]) => void;
  selectInstrument: (id: string) => void;
  setDateRange: (range: DateRange) => void;
  setBars: (bars: OHLCVBar[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useWorkstationStore = create<WorkstationState>((set) => ({
  instruments: [],
  selectedInstrumentId: null,
  dateRange: { start: null, end: null },
  bars: [],
  isLoading: false,
  error: null,
  setInstruments: (instruments) => set({ instruments }),
  selectInstrument: (id) => set({ selectedInstrumentId: id }),
  setDateRange: (range) => set({ dateRange: range }),
  setBars: (bars) => set({ bars }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
}));
```

- [ ] **Step 4: Verify TypeScript**

```bash
cd frontend && npx tsc --noEmit 2>&1 | head -20
```
Expected: no errors (or only errors from default boilerplate we haven't cleaned yet)

- [ ] **Step 5: Commit**
```bash
git add frontend/src/lib/
git commit -m "feat: API client, types, and Zustand workstation store"
```

---

## Task 9: Frontend — InstrumentPanel component

**Files:**
- Create: `frontend/src/components/workspace/InstrumentPanel.tsx`

- [ ] **Step 1: Create directory**
```bash
mkdir -p frontend/src/components/workspace
```

- [ ] **Step 2: Write `frontend/src/components/workspace/InstrumentPanel.tsx`**

```tsx
'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import { useWorkstationStore } from '@/lib/store';

export function InstrumentPanel() {
  const [filePath, setFilePath] = useState('');
  const [instrumentId, setInstrumentId] = useState('');
  const [loadError, setLoadError] = useState<string | null>(null);
  const [loadingFile, setLoadingFile] = useState(false);

  const { instruments, selectedInstrumentId, selectInstrument, setInstruments } =
    useWorkstationStore();

  async function handleLoad() {
    if (!filePath.trim() || !instrumentId.trim()) return;
    setLoadingFile(true);
    setLoadError(null);
    try {
      await api.loadInstrument({
        file_path: filePath.trim(),
        instrument_id: instrumentId.trim().toUpperCase(),
      });
      const updated = await api.listInstruments();
      setInstruments(updated);
      setFilePath('');
      setInstrumentId('');
    } catch (e: unknown) {
      setLoadError(e instanceof Error ? e.message : 'Load failed');
    } finally {
      setLoadingFile(false);
    }
  }

  return (
    <div className="flex flex-col gap-3 p-4 bg-[#0d1117] border-r border-[#21262d] w-60 shrink-0 overflow-y-auto">
      <span className="text-[10px] font-semibold text-[#8b949e] uppercase tracking-widest">
        Instruments
      </span>

      <div className="flex flex-col gap-2">
        <input
          className="bg-[#161b22] border border-[#30363d] rounded px-2 py-1.5 text-xs text-[#c9d1d9] placeholder-[#484f58] focus:outline-none focus:border-[#58a6ff] transition-colors"
          placeholder="ID (e.g. NIFTY)"
          value={instrumentId}
          onChange={(e) => setInstrumentId(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleLoad()}
        />
        <input
          className="bg-[#161b22] border border-[#30363d] rounded px-2 py-1.5 text-xs text-[#c9d1d9] placeholder-[#484f58] focus:outline-none focus:border-[#58a6ff] transition-colors"
          placeholder="/path/to/data.csv"
          value={filePath}
          onChange={(e) => setFilePath(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleLoad()}
        />
        <button
          onClick={handleLoad}
          disabled={loadingFile || !filePath.trim() || !instrumentId.trim()}
          className="bg-[#21262d] hover:bg-[#30363d] disabled:opacity-40 disabled:cursor-not-allowed border border-[#30363d] rounded px-3 py-1.5 text-xs text-[#c9d1d9] transition-colors"
        >
          {loadingFile ? 'Loading…' : 'Load File'}
        </button>
        {loadError && (
          <span className="text-[11px] text-[#f85149] leading-tight">{loadError}</span>
        )}
      </div>

      <div className="h-px bg-[#21262d]" />

      <div className="flex flex-col gap-1">
        {instruments.length === 0 && (
          <span className="text-[11px] text-[#484f58] italic">No instruments loaded</span>
        )}
        {instruments.map((inst) => (
          <button
            key={inst.instrument_id}
            onClick={() => selectInstrument(inst.instrument_id)}
            className={`text-left px-2.5 py-2 rounded text-xs transition-colors ${
              selectedInstrumentId === inst.instrument_id
                ? 'bg-[#1f6feb33] border border-[#1f6feb] text-[#58a6ff]'
                : 'text-[#c9d1d9] hover:bg-[#161b22] border border-transparent'
            }`}
          >
            <div className="font-semibold">{inst.instrument_id}</div>
            <div className="text-[#8b949e] text-[10px] mt-0.5">
              {inst.start_date} → {inst.end_date}
            </div>
            <div className="text-[#484f58] text-[10px]">
              {inst.row_count.toLocaleString()} bars
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
```

---

## Task 10: Frontend — IntervalBar component

**Files:**
- Create: `frontend/src/components/workspace/IntervalBar.tsx`

- [ ] **Step 1: Write `frontend/src/components/workspace/IntervalBar.tsx`**

```tsx
'use client';

import { useWorkstationStore } from '@/lib/store';

const PRESETS = [
  { label: '1M', months: 1 },
  { label: '3M', months: 3 },
  { label: '6M', months: 6 },
  { label: '1Y', months: 12 },
  { label: '2Y', months: 24 },
  { label: 'ALL', months: null },
] as const;

function subtractMonths(dateStr: string, months: number): string {
  const d = new Date(dateStr);
  d.setMonth(d.getMonth() - months);
  return d.toISOString().slice(0, 10);
}

export function IntervalBar() {
  const { instruments, selectedInstrumentId, dateRange, setDateRange } =
    useWorkstationStore();

  const selected = instruments.find((i) => i.instrument_id === selectedInstrumentId);

  function applyPreset(months: number | null) {
    if (!selected) return;
    if (months === null) {
      setDateRange({ start: selected.start_date, end: selected.end_date });
    } else {
      setDateRange({
        start: subtractMonths(selected.end_date, months),
        end: selected.end_date,
      });
    }
  }

  return (
    <div className="flex items-center gap-3 px-4 py-2 bg-[#0d1117] border-b border-[#21262d] shrink-0">
      <div className="flex gap-1">
        {PRESETS.map((p) => (
          <button
            key={p.label}
            onClick={() => applyPreset(p.months)}
            disabled={!selected}
            className="px-2 py-0.5 text-[11px] rounded border border-[#30363d] text-[#8b949e] hover:text-[#c9d1d9] hover:border-[#58a6ff] disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
          >
            {p.label}
          </button>
        ))}
      </div>

      <div className="flex items-center gap-2 ml-auto">
        <input
          type="date"
          value={dateRange.start ?? ''}
          onChange={(e) =>
            setDateRange({ ...dateRange, start: e.target.value || null })
          }
          className="bg-[#161b22] border border-[#30363d] rounded px-2 py-0.5 text-[11px] text-[#c9d1d9] focus:outline-none focus:border-[#58a6ff]"
        />
        <span className="text-[#484f58] text-xs">→</span>
        <input
          type="date"
          value={dateRange.end ?? ''}
          onChange={(e) =>
            setDateRange({ ...dateRange, end: e.target.value || null })
          }
          className="bg-[#161b22] border border-[#30363d] rounded px-2 py-0.5 text-[11px] text-[#c9d1d9] focus:outline-none focus:border-[#58a6ff]"
        />
      </div>
    </div>
  );
}
```

---

## Task 11: Frontend — ChartWorkspace component

**Files:**
- Create: `frontend/src/components/workspace/ChartWorkspace.tsx`

- [ ] **Step 1: Write `frontend/src/components/workspace/ChartWorkspace.tsx`**

```tsx
'use client';

import { useEffect, useRef } from 'react';
import {
  createChart,
  ColorType,
  CrosshairMode,
  type IChartApi,
  type ISeriesApi,
  type CandlestickData,
  type Time,
} from 'lightweight-charts';
import { api } from '@/lib/api';
import { useWorkstationStore } from '@/lib/store';

export function ChartWorkspace() {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);

  const { selectedInstrumentId, dateRange, setBars, setLoading, setError, isLoading, error } =
    useWorkstationStore();

  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: '#010409' },
        textColor: '#8b949e',
        fontSize: 11,
      },
      grid: {
        vertLines: { color: '#161b22' },
        horzLines: { color: '#161b22' },
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: { color: '#30363d', labelBackgroundColor: '#21262d' },
        horzLine: { color: '#30363d', labelBackgroundColor: '#21262d' },
      },
      rightPriceScale: { borderColor: '#21262d' },
      timeScale: { borderColor: '#21262d', timeVisible: true },
      width: containerRef.current.clientWidth,
      height: containerRef.current.clientHeight,
    });

    const series = chart.addCandlestickSeries({
      upColor: '#3fb950',
      downColor: '#f85149',
      borderVisible: false,
      wickUpColor: '#3fb950',
      wickDownColor: '#f85149',
    });

    chartRef.current = chart;
    seriesRef.current = series;

    const ro = new ResizeObserver(() => {
      if (containerRef.current) {
        chart.applyOptions({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight,
        });
      }
    });
    ro.observe(containerRef.current);

    return () => {
      ro.disconnect();
      chart.remove();
      chartRef.current = null;
      seriesRef.current = null;
    };
  }, []);

  useEffect(() => {
    if (!selectedInstrumentId || !seriesRef.current) return;

    setLoading(true);
    setError(null);

    api
      .getOHLCV(
        selectedInstrumentId,
        dateRange.start ?? undefined,
        dateRange.end ?? undefined
      )
      .then((resp) => {
        setBars(resp.bars);
        const data: CandlestickData[] = resp.bars.map((b) => ({
          time: b.time as Time,
          open: b.open,
          high: b.high,
          low: b.low,
          close: b.close,
        }));
        seriesRef.current?.setData(data);
        chartRef.current?.timeScale().fitContent();
      })
      .catch((e: unknown) => setError(e instanceof Error ? e.message : 'Fetch failed'))
      .finally(() => setLoading(false));
  }, [selectedInstrumentId, dateRange.start, dateRange.end]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="flex-1 flex flex-col min-h-0 relative">
      {!selectedInstrumentId && (
        <div className="absolute inset-0 flex items-center justify-center text-[#484f58] text-sm pointer-events-none">
          Select an instrument to begin
        </div>
      )}
      {error && (
        <div className="absolute top-2 left-1/2 -translate-x-1/2 bg-[#3d1414] border border-[#f85149] rounded px-3 py-1.5 text-xs text-[#f85149] z-10">
          {error}
        </div>
      )}
      {isLoading && (
        <div className="absolute top-2 right-4 text-[11px] text-[#8b949e] z-10">
          Loading…
        </div>
      )}
      <div ref={containerRef} className="flex-1 min-h-0" />
    </div>
  );
}
```

---

## Task 12: Frontend — page assembly

**Files:**
- Modify: `frontend/src/app/globals.css`
- Modify: `frontend/src/app/layout.tsx`
- Modify: `frontend/src/app/page.tsx`

- [ ] **Step 1: Write `frontend/src/app/globals.css`**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  box-sizing: border-box;
}

html,
body {
  height: 100%;
  overflow: hidden;
}

input[type='date']::-webkit-calendar-picker-indicator {
  filter: invert(0.4);
}
```

- [ ] **Step 2: Write `frontend/src/app/layout.tsx`**

```tsx
import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AMR Research Workstation',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-[#010409] antialiased">{children}</body>
    </html>
  );
}
```

- [ ] **Step 3: Write `frontend/src/app/page.tsx`**

```tsx
import { InstrumentPanel } from '@/components/workspace/InstrumentPanel';
import { ChartWorkspace } from '@/components/workspace/ChartWorkspace';
import { IntervalBar } from '@/components/workspace/IntervalBar';

export default function WorkstationPage() {
  return (
    <div className="flex h-screen bg-[#010409] text-[#c9d1d9] overflow-hidden">
      <InstrumentPanel />
      <div className="flex flex-col flex-1 min-w-0">
        <IntervalBar />
        <ChartWorkspace />
      </div>
    </div>
  );
}
```

- [ ] **Step 4: Verify TypeScript compiles**

```bash
cd frontend && npx tsc --noEmit
```
Expected: no errors

- [ ] **Step 5: Commit**
```bash
git add frontend/src/
git commit -m "feat: workstation UI — InstrumentPanel, IntervalBar, ChartWorkspace"
```

---

## Task 13: End-to-end smoke test

**Goal:** Generate a synthetic OHLCV CSV, start both servers, load data, confirm chart renders.

- [ ] **Step 1: Generate synthetic CSV**

```bash
python3 - <<'EOF'
import csv, math, random
from datetime import date, timedelta

random.seed(42)
price = 21000.0
rows = [["date", "open", "high", "low", "close", "volume"]]
day = date(2022, 1, 3)
for _ in range(500):
    while day.weekday() >= 5:
        day += timedelta(1)
    o = price + random.gauss(0, 50)
    c = o + random.gauss(0, 80)
    h = max(o, c) + abs(random.gauss(0, 30))
    l = min(o, c) - abs(random.gauss(0, 30))
    v = random.randint(800_000, 2_000_000)
    rows.append([day.isoformat(), f"{o:.2f}", f"{h:.2f}", f"{l:.2f}", f"{c:.2f}", str(v)])
    price = c
    day += timedelta(1)

with open("data/raw/nifty_synthetic.csv", "w", newline="") as f:
    csv.writer(f).writerows(rows)
print("Written 500 rows to data/raw/nifty_synthetic.csv")
EOF
```

- [ ] **Step 2: Start backend**

```bash
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000 &
sleep 2 && curl -s http://localhost:8000/health
```
Expected: `{"status":"ok"}`

- [ ] **Step 3: Load instrument via API**

```bash
curl -s -X POST http://localhost:8000/api/v1/market/load \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/Users/priyanshusaraf/Desktop/internship-final-reports/data/raw/nifty_synthetic.csv", "instrument_id": "NIFTY_SYN"}' \
  | python3 -m json.tool
```
Expected: `{"instrument_id": "NIFTY_SYN", "row_count": 500, ...}`

- [ ] **Step 4: Start frontend**

```bash
cd frontend && npm run dev &
sleep 5 && curl -s http://localhost:3000 | grep -o '<title>[^<]*'
```
Expected: `<title>AMR Research Workstation`

- [ ] **Step 5: Open in browser**

Navigate to http://localhost:3000.

Manual checklist:
- [ ] Page loads with dark background, instrument panel on left
- [ ] Enter `NIFTY_SYN` + path to CSV → click Load → instrument appears in list
- [ ] Click instrument → candles render in main chart area
- [ ] Click `1Y` preset → chart updates to last year of data
- [ ] Zoom / pan within the chart works natively
- [ ] Date range inputs reflect the selected interval

- [ ] **Step 6: Final commit**
```bash
git add data/raw/nifty_synthetic.csv
git commit -m "feat: Phase 1 complete — data workstation with candlestick chart"
```

---

## Tradeoffs and known limitations

| Decision | Tradeoff |
|---|---|
| DuckDB in-memory | Data lost on server restart. Acceptable for research workstation. Add persistence (`:path:`) in Phase 2 if needed. |
| File path input instead of upload | Simpler — researcher knows where their files live. Avoids multipart complexity. |
| lightweight-charts v4 | Stable, well-documented. No built-in drag-select for custom ranges — IntervalBar fills this gap with date inputs + presets. |
| No React Query | Zustand manages all state including loading/error. React Query adds caching but is overkill until Phase 2 when we have multiple concurrent data streams. |
| No shadcn | Removed friction from init. Raw Tailwind is sufficient for Phase 1. Add in Phase 2 for diagnostic panels. |
