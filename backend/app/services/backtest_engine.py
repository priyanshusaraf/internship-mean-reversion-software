"""
Backtest engine — strictly causal, event-driven, bar-by-bar P&L simulation.

CONSTITUTIONAL STATUS (CLAUDE.md):
  This is an EXECUTION/MEASUREMENT layer, NOT a strategy-discovery or optimization surface. The
  strategy rule below is a FROZEN PLACEHOLDER (MR_PLACEHOLDER_V1) — hardcoded, not configurable,
  no optimization hooks. It exists to exercise the engine, not to be deployed. The response is
  explicitly stamped `slippage=0, placeholder rule, not deployable`.

  This module imports nothing from the frozen analytics engines and never recomputes a statistic.
  The causal z-score is produced upstream by `analytics_mrscore.causal_zscore` (shifted μ,σ) and
  passed IN. This engine only consumes (close, μ*, z) and runs the trade loop.

TEMPORAL FIREWALL (§6.1 — the ways we could fool ourselves, each guarded by a test):
  • At signal bar t the loop reads only z[t], close[0..t], mu_star[0..t]. Decisions never read t+1.
  • The ONE and ONLY forward read is the FILL PRICE close[t+1] — a next-bar-open proxy for daily
    bars, documented here and surfaced in `slippage_note`. If t+1 does not exist (last bar), the
    entry/exit cannot fill and the trade is not taken.
  • The window is sliced to [start, end] by the CALLER before this function is entered; anything
    beyond `end` is physically absent from `ohlcv` (caller-enforced firewall).

The P&L loop logic is ported from scripts/run_brn_calendar_test.py (195–228) and
scripts/run_arm_a_v2_rolling.py (49–64): in_pos ∈ {+1 SHORT, −1 LONG}, gross = sign·(entry−exit).
"""
from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field


# ── FROZEN strategy constants (MR_PLACEHOLDER_V1) — NOT configurable, NO optimization hooks ──────
_ENTRY_Z = 1.0      # |z| ≥ 1.0 → enter (fade the deviation)
_EXIT_Z = 0.05      # |z| < 0.05 → z-cross exit
_TIME_STOP = 20     # bars held ≥ 20 → time-stop exit
_ANN = 252          # annualization factor for Sharpe


class BacktestConfig(BaseModel):
    instrument_id: str
    start: str                          # ISO date
    end: str                            # ISO date — the hard firewall upper bound
    strategy_id: str = "MR_PLACEHOLDER_V1"
    round_trip_cost: float = 0.003      # frozen: cost = round_trip_cost × μ* at entry bar
    # ── Verification mode gate (API contract M4 — minimal but real param freeze) ──
    mode: str = "research"              # "research" | "verification"
    prereg_params: dict = Field(default_factory=dict)  # populated by verification mode only


class Trade(BaseModel):
    trade_id: int
    direction: str          # "LONG" or "SHORT"
    entry_bar: str          # ISO date of the SIGNAL bar (where |z| crossed the entry band)
    entry_price: float      # fill = close[entry_signal_bar + 1]
    exit_bar: str           # ISO date of the SIGNAL bar (where exit condition fired)
    exit_price: float       # fill = close[exit_signal_bar + 1]
    exit_reason: str        # "Z_CROSS" or "TIME_STOP"
    gross_pnl: float        # price units
    cost: float             # price units
    net_pnl: float          # gross - cost
    bars_held: int          # exit_signal_index - entry_signal_index
    entry_z: float
    exit_z: float


class BacktestResult(BaseModel):
    instrument_id: str
    strategy_id: str
    start: str
    end: str
    n_bars: int
    n_trades: int
    win_rate: float
    avg_net_pnl: float
    total_net_pnl: float
    sharpe_ratio: float
    max_drawdown: float
    profit_factor: float
    avg_bars_held: float
    pct_time_stop: float
    trades: List[Trade]
    equity_curve: List[dict]            # [{date: str, cumulative_pnl: float}] — one per bar
    slippage_note: str
    strategy_params: dict
    verification_watermark: bool = False


_SLIPPAGE_NOTE = "slippage=0, placeholder rule, not deployable"


def _frozen_params(config: BacktestConfig) -> dict:
    """Audit trail of the exact frozen rule used (no user-tunable knobs)."""
    return {
        "strategy_id": config.strategy_id,
        "entry_z_threshold": _ENTRY_Z,
        "exit_z_threshold": _EXIT_Z,
        "time_stop_bars": _TIME_STOP,
        "direction_rule": "fade deviation (z>+1 → SHORT, z<-1 → LONG)",
        "sizing": "1 unit flat, one position at a time, no pyramiding",
        "round_trip_cost": config.round_trip_cost,
        "cost_basis": "round_trip_cost × mu_star at entry signal bar",
        "fill_rule": "close[t+1] (next-bar proxy, daily bars)",
        "slippage": 0.0,
    }


def run_backtest(
    config: BacktestConfig,
    ohlcv: pd.DataFrame,
    z_scores: pd.Series,
) -> BacktestResult:
    """Bar-by-bar event loop. `ohlcv` has a DatetimeIndex and columns including `close`; if a
    `mu_star` column is present it is used as the cost basis, else `close` is the fallback basis.
    `z_scores` is aligned to the same index. Both MUST already be sliced to [config.start,
    config.end] — the temporal firewall is enforced by the caller, not here.

    Causal contract inside the loop: at signal bar i we read z[i] and data ≤ i only. The single
    forward read is the fill close[i+1]; a signal on the last bar cannot fill and is dropped.
    """
    closes = ohlcv["close"].to_numpy(dtype=float)
    mu = (ohlcv["mu_star"].to_numpy(dtype=float)
          if "mu_star" in ohlcv.columns else closes.copy())
    z = z_scores.to_numpy(dtype=float)
    dates = [pd.Timestamp(d).strftime("%Y-%m-%d") for d in ohlcv.index]
    n = len(closes)

    trades: List[Trade] = []
    realized = np.zeros(n)   # net P&L attributed to the bar on which the trade exits

    in_pos = 0               # 0 flat · +1 SHORT (fade up) · −1 LONG (fade down)
    entry_i = -1
    entry_price = 0.0
    entry_mu = 0.0
    entry_z = 0.0
    trade_id = 0

    for i in range(n):
        zi = z[i]
        if not np.isfinite(zi):
            # No causal z available at this bar (warmup / gap): make no decision. An open
            # position simply persists — we never act on a non-finite signal.
            continue

        if in_pos == 0:
            # ── entry: trigger on bar i, fill at close[i+1] (requires a next bar) ──
            if i + 1 >= n:
                continue                       # last bar: cannot fill an entry
            if zi >= _ENTRY_Z:
                in_pos = +1                    # SHORT — price above μ*, fade down
            elif zi <= -_ENTRY_Z:
                in_pos = -1                    # LONG — price below μ*, fade up
            else:
                continue
            entry_i = i
            entry_price = closes[i + 1]        # next-bar fill proxy (the only forward read)
            entry_mu = mu[i]                   # μ* at the SIGNAL bar (cost basis)
            entry_z = zi
        else:
            # ── exit: evaluate on bar i, fill at close[i+1] ──
            bars_held = i - entry_i
            reason = None
            if abs(zi) < _EXIT_Z:
                reason = "Z_CROSS"
            elif bars_held >= _TIME_STOP:
                reason = "TIME_STOP"
            if reason is None:
                continue
            if i + 1 >= n:
                # exit condition met on the last bar — cannot fill; position stays open and is
                # dropped (no trade recorded). Causally honest: we never fill on a bar we lack.
                continue
            exit_price = closes[i + 1]
            gross = (entry_price - exit_price) if in_pos == +1 else (exit_price - entry_price)
            cost = config.round_trip_cost * entry_mu
            net = gross - cost
            trade_id += 1
            trades.append(Trade(
                trade_id=trade_id,
                direction="SHORT" if in_pos == +1 else "LONG",
                entry_bar=dates[entry_i],
                entry_price=float(entry_price),
                exit_bar=dates[i],
                exit_price=float(exit_price),
                exit_reason=reason,
                gross_pnl=float(gross),
                cost=float(cost),
                net_pnl=float(net),
                bars_held=int(bars_held),
                entry_z=float(entry_z),
                exit_z=float(zi),
            ))
            realized[i] += net
            in_pos = 0
            entry_i = -1

    # ── equity curve: one point per bar (realized P&L accrues at exit bars) ──
    equity_curve: List[dict] = []
    cum = 0.0
    for i in range(n):
        cum += realized[i]
        equity_curve.append({"date": dates[i], "cumulative_pnl": float(cum)})

    # ── metrics ──
    nets = np.array([t.net_pnl for t in trades], dtype=float)
    n_trades = len(trades)

    if n_trades > 0:
        win_rate = float(np.mean(nets > 0.0))
        avg_net = float(nets.mean())
        total_net = float(nets.sum())
        avg_bars_held = float(np.mean([t.bars_held for t in trades]))
        pct_time_stop = float(np.mean([t.exit_reason == "TIME_STOP" for t in trades]))
    else:
        win_rate = avg_net = total_net = avg_bars_held = pct_time_stop = 0.0

    # Sharpe on per-trade net series, annualized. Finite by construction: <2 trades or zero
    # dispersion → 0.0 (no information, not NaN/inf).
    if n_trades >= 2:
        sd = float(nets.std(ddof=1))
        sharpe = float((nets.mean() / sd) * np.sqrt(_ANN)) if sd > 0.0 else 0.0
    else:
        sharpe = 0.0

    # Profit factor: Σwins / |Σlosses|; inf if there are wins and no losses (per spec).
    wins = float(nets[nets > 0.0].sum()) if n_trades else 0.0
    losses = float(nets[nets < 0.0].sum()) if n_trades else 0.0
    if losses != 0.0:
        profit_factor = float(wins / abs(losses))
    elif wins > 0.0:
        profit_factor = float("inf")
    else:
        profit_factor = 0.0

    # Max drawdown: most-negative peak-to-trough on the cumulative curve (≤ 0, a loss magnitude).
    max_dd = 0.0
    peak = float("-inf")
    for pt in equity_curve:
        v = pt["cumulative_pnl"]
        if v > peak:
            peak = v
        dd = v - peak
        if dd < max_dd:
            max_dd = dd

    return BacktestResult(
        instrument_id=config.instrument_id,
        strategy_id=config.strategy_id,
        start=config.start,
        end=config.end,
        n_bars=n,
        n_trades=n_trades,
        win_rate=win_rate,
        avg_net_pnl=avg_net,
        total_net_pnl=total_net,
        sharpe_ratio=sharpe,
        max_drawdown=float(max_dd),
        profit_factor=profit_factor,
        avg_bars_held=avg_bars_held,
        pct_time_stop=pct_time_stop,
        trades=trades,
        equity_curve=equity_curve,
        slippage_note=_SLIPPAGE_NOTE,
        strategy_params=_frozen_params(config),
        verification_watermark=(config.mode == "verification"),
    )
