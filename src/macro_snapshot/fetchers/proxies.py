"""Proxy fetchers — Tier B derived metrics.

Currently provides:
  - tlt_realized_vol_proxy  (20d annualized realized vol of TLT)

This is NOT the ICE MOVE Index. MOVE is an implied vol index for
rates/swaptions. TLT realized vol measures realized price volatility
of a long-Treasury ETF. They are correlated but semantically different.
"""

from __future__ import annotations

import datetime as dt
import logging
from typing import Optional

import numpy as np

from macro_snapshot.schemas import (
    STATUS_PROXY,
    TIER_B,
    MetricPoint,
)

logger = logging.getLogger(__name__)

# Trading days in a year for annualization
TRADING_DAYS = 252
REALIZED_VOL_WINDOW = 20


def fetch_tlt_realized_vol(
    window: int = REALIZED_VOL_WINDOW,
    lookback_days: int = 60,
) -> MetricPoint:
    """Compute 20-day annualized realized vol of TLT via yfinance.

    This is a directional rate-vol proxy, not ICE MOVE.
    """
    name = "tlt_realized_vol_proxy"
    source = "yfinance/TLT"

    try:
        import yfinance as yf

        end = dt.date.today()
        start = end - dt.timedelta(days=lookback_days)

        tlt = yf.download("TLT", start=start, end=end, progress=False)
        if tlt.empty or len(tlt) < window + 1:
            return MetricPoint.no_data(
                name=name,
                source=source,
                notes=f"Insufficient TLT data (got {len(tlt)} rows, need {window + 1}).",
                quality_tier=TIER_B,
                methodology="proxy_realized_vol",
            )

        close = tlt["Close"].squeeze()
        log_returns = np.log(close / close.shift(1)).dropna()

        if len(log_returns) < window:
            return MetricPoint.no_data(
                name=name,
                source=source,
                notes=f"Insufficient return data after dropna ({len(log_returns)} < {window}).",
                quality_tier=TIER_B,
                methodology="proxy_realized_vol",
            )

        realized_vol = float(log_returns.tail(window).std() * np.sqrt(TRADING_DAYS) * 100)
        last_date = close.index[-1]
        asof = last_date.date().isoformat() if hasattr(last_date, "date") else str(last_date)[:10]

        return MetricPoint(
            name=name,
            value=round(realized_vol, 2),
            asof=asof,
            source=source,
            status=STATUS_PROXY,
            is_stale=False,
            notes=(
                f"{window}d realized vol annualized. "
                "Directional proxy for rate-vol; not ICE MOVE. "
                "MOVE is implied vol on rates/swaptions."
            ),
            quality_tier=TIER_B,
            methodology="proxy_realized_vol",
        )
    except ImportError:
        return MetricPoint.error(
            name=name,
            source=source,
            error_msg="yfinance not installed.",
            quality_tier=TIER_B,
            methodology="proxy_realized_vol",
        )
    except Exception as exc:
        logger.exception("TLT realized vol fetch failed")
        return MetricPoint.error(
            name=name,
            source=source,
            error_msg=str(exc),
            quality_tier=TIER_B,
            methodology="proxy_realized_vol",
        )
