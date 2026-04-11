"""FRED fetcher — Tier A official macro series.

Uses the FRED public API (no key required for basic access) for:
  - HY OAS (BAMLH0A0HYM2)
  - IG OAS (BAMLC0A0CM)
  - NFCI (Chicago Fed National Financial Conditions Index)
  - 2s10s spread (T10Y2Y)
  - 3m10y spread (T10Y3M)
  - Real 10Y yield (DFII10)
  - 10Y breakeven inflation (T10YIE)
  - VIX from FRED (VIXCLS)
  - Broad DXY (DTWEXBGS)
"""

from __future__ import annotations

import datetime as dt
import logging
import os
from typing import Any

import pandas as pd
import requests

from macro_snapshot.schemas import (
    TIER_A,
    MetricPoint,
)

logger = logging.getLogger(__name__)

# ── FRED series map ────────────────────────────────────────────────
FRED_SERIES: dict[str, str] = {
    "hy_oas": "BAMLH0A0HYM2",
    "ig_oas": "BAMLC0A0CM",
    "nfci": "NFCI",
    "spread_2s10s": "T10Y2Y",
    "spread_3m10y": "T10Y3M",
    "real_10y": "DFII10",
    "breakeven_10y": "T10YIE",
    "vix_fred_close": "VIXCLS",
    "dxy_broad": "DTWEXBGS",
}

FRED_API_BASE = "https://api.stlouisfed.org/fred/series/observations"
STALE_DAYS = 5
REQUEST_TIMEOUT = 30


def _check_stale(last_date: dt.date) -> bool:
    return (dt.date.today() - last_date).days > STALE_DAYS


def _fetch_single_fred(
    name: str,
    sid: str,
    api_key: str,
    start: dt.date,
) -> MetricPoint:
    """Fetch a single FRED series via the public API."""
    try:
        params = {
            "series_id": sid,
            "api_key": api_key,
            "file_type": "json",
            "observation_start": start.isoformat(),
            "sort_order": "desc",
            "limit": 10,
        }
        resp = requests.get(FRED_API_BASE, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        observations = data.get("observations", [])
        # Find latest non-missing observation
        for obs in observations:
            val = obs.get("value", ".")
            if val != ".":
                last_date = dt.date.fromisoformat(obs["date"])
                is_stale = _check_stale(last_date)
                return MetricPoint(
                    name=name,
                    value=float(val),
                    asof=last_date.isoformat(),
                    source=f"FRED:{sid}",
                    status="stale" if is_stale else "ok",
                    is_stale=is_stale,
                    notes=f"Stale: last obs {last_date}" if is_stale else "",
                    quality_tier=TIER_A,
                    methodology="official_series",
                )

        return MetricPoint.no_data(
            name=name,
            source=f"FRED:{sid}",
            quality_tier=TIER_A,
            methodology="official_series",
        )
    except Exception as exc:
        logger.exception("FRED fetch failed for %s (%s)", name, sid)
        return MetricPoint.error(
            name=name,
            source=f"FRED:{sid}",
            error_msg=str(exc),
            quality_tier=TIER_A,
            methodology="official_series",
        )


def fetch_fred_series(
    start: dt.date = dt.date(2020, 1, 1),
    api_key: str | None = None,
) -> list[MetricPoint]:
    """Fetch all configured FRED series and return MetricPoints.

    Uses FRED_API_KEY from environment if not provided.
    A FRED API key is free to register at https://fred.stlouisfed.org/docs/api/api_key.html
    """
    key = api_key or os.environ.get("FRED_API_KEY", "")
    if not key:
        return [
            MetricPoint.error(
                name=name,
                source=f"FRED:{sid}",
                error_msg=(
                    "FRED_API_KEY not configured. "
                    "Register free at https://fred.stlouisfed.org/docs/api/api_key.html "
                    "and set FRED_API_KEY in .env"
                ),
                quality_tier=TIER_A,
                methodology="official_series",
            )
            for name, sid in FRED_SERIES.items()
        ]

    return [
        _fetch_single_fred(name, sid, key, start)
        for name, sid in FRED_SERIES.items()
    ]
