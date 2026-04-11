"""
FRED API data fetcher.

Fetches all macro/credit/yield indicators from the Federal Reserve Economic Data API.
Free, unlimited, JSON responses.
Endpoint: https://api.stlouisfed.org/fred/series/observations
"""

import logging
from datetime import date
from typing import Any

import pandas as pd
import requests

from config import FRED_API_KEY, FRED_SERIES, DATA_START_DATE

logger = logging.getLogger(__name__)

FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


def _fetch_single_series(series_id: str, start: date) -> float | None:
    """Fetch the latest observation for a single FRED series."""
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start.isoformat(),
        "sort_order": "desc",
        "limit": 5,
    }
    try:
        resp = requests.get(FRED_BASE_URL, params=params, timeout=15)
        resp.raise_for_status()
        observations = resp.json().get("observations", [])
        for obs in observations:
            val = obs.get("value", ".")
            if val != ".":
                return float(val)
        return None
    except Exception as e:
        logger.warning("FRED fetch failed for %s: %s", series_id, e)
        return None


def _fetch_series_history(series_id: str, start: date) -> pd.DataFrame:
    """Fetch full history for a single FRED series as a DataFrame."""
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start.isoformat(),
    }
    try:
        resp = requests.get(FRED_BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        observations = resp.json().get("observations", [])
        records = []
        for obs in observations:
            val = obs.get("value", ".")
            if val != ".":
                records.append({"date": obs["date"], "value": float(val)})
        df = pd.DataFrame(records)
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date").sort_index()
        return df
    except Exception as e:
        logger.warning("FRED history fetch failed for %s: %s", series_id, e)
        return pd.DataFrame()


def fetch_fred_snapshot() -> dict[str, Any]:
    """
    Fetch latest values for all configured FRED series.

    Returns dict like:
        {"hy_oas": 3.45, "ig_oas": 1.12, "nfci": -0.32, ...}
    """
    logger.info("Fetching FRED snapshot (%d series)...", len(FRED_SERIES))
    results: dict[str, Any] = {}
    for name, series_id in FRED_SERIES.items():
        val = _fetch_single_series(series_id, DATA_START_DATE)
        results[name] = val
        if val is not None:
            logger.debug("  %s (%s): %.4f", name, series_id, val)
        else:
            logger.warning("  %s (%s): NO DATA", name, series_id)
    return results


def fetch_fred_history() -> dict[str, pd.DataFrame]:
    """Fetch full history for all FRED series. Returns dict of DataFrames."""
    logger.info("Fetching FRED history (%d series)...", len(FRED_SERIES))
    history: dict[str, pd.DataFrame] = {}
    for name, series_id in FRED_SERIES.items():
        df = _fetch_series_history(series_id, DATA_START_DATE)
        history[name] = df
        logger.debug("  %s: %d rows", name, len(df))
    return history
