from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import market, observatory, backtest
from app.services import store


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Schema init runs once at startup — not per request
    store.init_db()
    yield


app = FastAPI(title="AMR Research Backend", version="0.1.0", lifespan=lifespan)

_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market.router)
app.include_router(observatory.router)
app.include_router(backtest.router)


@app.get("/health")
def health():
    return {"status": "ok"}
