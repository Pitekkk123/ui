"""
yfinance-based data fetcher.

Handles: GEX (Gamma Exposure), Options Flow (P/C ratios), MOVE proxy (TLT realized vol).
All free, unlimited via Yahoo Finance.
"""

import logging
from typing import Any

import numpy as np
import yfinance as yf

from config import (
    GEX_NUM_EXPIRIES,
    GEX_TICKER,
    MOVE_PROXY_TICKER,
    MOVE_PROXY_WINDOW,
    OPTIONS_FLOW_TICKERS,
)

logger = logging.getLogger(__name__)


def fetch_gex() -> dict[str, Any]:
    """
    Calculate approximate Gamma Exposure (GEX) from SPY options chain.

    Formula: GEX = gamma * OI * 100 * spot^2 * 0.01
    Calls contribute positive gamma, puts contribute negative gamma.

    Positive GEX = market-stabilizing (dealers hedge by selling high, buying low)
    Negative GEX = volatility-amplifying (dealers hedge in same direction as market)

    Returns:
        {
            "gex_total_billions": 2.45,
            "gex_signal": "positive (stabilizing)",
            "gex_calls_billions": 4.2,
            "gex_puts_billions": -1.75,
            "spot_price": 450.5,
            "num_expiries_used": 3,
        }
    """
    logger.info("Calculating GEX from %s options chain...", GEX_TICKER)
    result: dict[str, Any] = {}

    try:
        ticker = yf.Ticker(GEX_TICKER)
        hist = ticker.history(period="1d")
        if hist.empty:
            logger.warning("Could not fetch %s spot price", GEX_TICKER)
            return {"gex_total_billions": None, "gex_signal": "no_data"}

        spot = float(hist["Close"].iloc[-1])
        result["spot_price"] = round(spot, 2)

        exp_dates = ticker.options[:GEX_NUM_EXPIRIES]
        result["num_expiries_used"] = len(exp_dates)

        total_call_gex = 0.0
        total_put_gex = 0.0

        for exp in exp_dates:
            try:
                chain = ticker.option_chain(exp)
                calls = chain.calls.copy()
                puts = chain.puts.copy()

                # GEX = gamma * OI * 100 * spot^2 * 0.01
                calls["gex"] = (
                    calls["gamma"].fillna(0)
                    * calls["openInterest"].fillna(0)
                    * 100
                    * spot**2
                    * 0.01
                )
                puts["gex"] = (
                    -puts["gamma"].fillna(0)
                    * puts["openInterest"].fillna(0)
                    * 100
                    * spot**2
                    * 0.01
                )

                total_call_gex += calls["gex"].sum()
                total_put_gex += puts["gex"].sum()
            except Exception as e:
                logger.debug("GEX chain error for %s: %s", exp, e)

        total_gex = total_call_gex + total_put_gex

        result["gex_calls_billions"] = round(total_call_gex / 1e9, 3)
        result["gex_puts_billions"] = round(total_put_gex / 1e9, 3)
        result["gex_total_billions"] = round(total_gex / 1e9, 3)

        if total_gex > 0:
            result["gex_signal"] = "positive (stabilizing — dealers sell rallies, buy dips)"
        else:
            result["gex_signal"] = "negative (amplifying — dealers chase momentum)"

    except Exception as e:
        logger.error("GEX calculation failed: %s", e)
        result["gex_total_billions"] = None
        result["gex_signal"] = "error"

    return result


def fetch_options_flow() -> dict[str, Any]:
    """
    Fetch options flow (put/call ratios) for hedge/fear tickers:
    TLT, SQQQ, UVXY, VXX, SDS.

    High P/C ratios on these tickers = hedging activity increasing.

    Returns:
        {
            "TLT": {"call_oi": 50000, "put_oi": 80000, "pc_ratio": 1.60},
            ...
        }
    """
    logger.info("Fetching options flow for %s...", OPTIONS_FLOW_TICKERS)
    results: dict[str, Any] = {}

    for symbol in OPTIONS_FLOW_TICKERS:
        try:
            t = yf.Ticker(symbol)
            exps = t.options[:2]  # 2 nearest expiries
            total_call_oi = 0
            total_put_oi = 0

            for exp in exps:
                chain = t.option_chain(exp)
                total_call_oi += int(chain.calls["openInterest"].fillna(0).sum())
                total_put_oi += int(chain.puts["openInterest"].fillna(0).sum())

            pc_ratio = total_put_oi / (total_call_oi + 0.001)

            results[symbol] = {
                "call_oi": total_call_oi,
                "put_oi": total_put_oi,
                "pc_ratio": round(pc_ratio, 3),
            }

            # Interpret signal
            if pc_ratio > 1.5:
                results[symbol]["signal"] = "heavy put buying (fear/hedging)"
            elif pc_ratio > 1.0:
                results[symbol]["signal"] = "moderate put bias"
            elif pc_ratio > 0.7:
                results[symbol]["signal"] = "balanced"
            else:
                results[symbol]["signal"] = "call-heavy (bullish/complacent)"

        except Exception as e:
            logger.warning("Options flow for %s failed: %s", symbol, e)
            results[symbol] = {"call_oi": None, "put_oi": None, "pc_ratio": None, "signal": "error"}

    return results


def fetch_move_proxy() -> dict[str, Any]:
    """
    Calculate MOVE index proxy using TLT 20-day realized volatility.

    The real MOVE index (ICE BofA) measures implied volatility of Treasury options.
    TLT realized vol is a weaker substitute but captures directional trends.

    Returns:
        {
            "tlt_realized_vol_20d": 14.5,
            "move_proxy_signal": "elevated",
            "tlt_last_close": 92.50,
        }
    """
    logger.info("Calculating MOVE proxy via %s realized vol...", MOVE_PROXY_TICKER)
    result: dict[str, Any] = {}

    try:
        tlt = yf.download(MOVE_PROXY_TICKER, period="90d", interval="1d", progress=False)
        if tlt.empty:
            return {"tlt_realized_vol_20d": None, "move_proxy_signal": "no_data"}

        # Handle MultiIndex columns from yfinance
        close_col = tlt["Close"]
        if hasattr(close_col, "columns"):
            close_col = close_col.iloc[:, 0]

        result["tlt_last_close"] = round(float(close_col.iloc[-1]), 2)

        returns = close_col.pct_change().dropna()
        realized_vol = float(
            returns.rolling(MOVE_PROXY_WINDOW).std().iloc[-1] * np.sqrt(252) * 100
        )
        result["tlt_realized_vol_20d"] = round(realized_vol, 2)

        if realized_vol < 10:
            result["move_proxy_signal"] = "calm (low bond vol)"
        elif realized_vol < 15:
            result["move_proxy_signal"] = "normal"
        elif realized_vol < 20:
            result["move_proxy_signal"] = "elevated (watch credit)"
        else:
            result["move_proxy_signal"] = "stress (high bond vol — risk-off)"

    except Exception as e:
        logger.error("MOVE proxy calculation failed: %s", e)
        result["tlt_realized_vol_20d"] = None
        result["move_proxy_signal"] = "error"

    return result
