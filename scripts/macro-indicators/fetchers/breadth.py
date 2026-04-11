"""
Market breadth data fetcher.

Covers: TRIN (Arms Index), HLLI (High-Low Leadership Index),
McClellan Oscillator & Summation Index.

Primary source: Stooq.com (free, daily CSVs).
Fallback: manual calculation from advancing/declining data.
"""

import io
import logging
from datetime import date, timedelta
from typing import Any

import numpy as np
import pandas as pd
import requests

from config import STOOQ_TRIN_URL

logger = logging.getLogger(__name__)


def _stooq_download(url: str, label: str) -> pd.DataFrame:
    """Download CSV from Stooq and return DataFrame."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text))
        df.columns = [c.strip().upper() for c in df.columns]
        if "DATE" in df.columns:
            df["DATE"] = pd.to_datetime(df["DATE"])
            df = df.set_index("DATE").sort_index()
        return df
    except Exception as e:
        logger.warning("Stooq %s fetch failed: %s", label, e)
        return pd.DataFrame()


def fetch_trin() -> dict[str, Any]:
    """
    Fetch TRIN (Arms Index) from Stooq.

    TRIN = (Advancing / Declining Issues) / (Advancing / Declining Volume)
    TRIN < 0.5 → extreme bullish
    TRIN 0.8-1.2 → neutral
    TRIN > 2.0 → extreme panic / selling climax

    Returns:
        {
            "trin": 1.05,
            "trin_signal": "neutral",
            "trin_5d_avg": 1.12,
        }
    """
    logger.info("Fetching TRIN from Stooq...")
    result: dict[str, Any] = {}

    end = date.today()
    start = end - timedelta(days=90)
    url = STOOQ_TRIN_URL.format(
        start=start.strftime("%Y%m%d"),
        end=end.strftime("%Y%m%d"),
    )
    df = _stooq_download(url, "TRIN")

    if not df.empty and "CLOSE" in df.columns:
        trin_last = float(df["CLOSE"].iloc[-1])
        result["trin"] = round(trin_last, 3)
        result["trin_date"] = str(df.index[-1].date())

        # 5-day average
        if len(df) >= 5:
            result["trin_5d_avg"] = round(float(df["CLOSE"].iloc[-5:].mean()), 3)

        # Signal
        if trin_last < 0.5:
            result["trin_signal"] = "extreme bullish (heavy buying pressure)"
        elif trin_last < 0.8:
            result["trin_signal"] = "bullish"
        elif trin_last <= 1.2:
            result["trin_signal"] = "neutral"
        elif trin_last <= 2.0:
            result["trin_signal"] = "bearish (selling pressure)"
        else:
            result["trin_signal"] = "extreme panic / selling climax (potential reversal)"
    else:
        result["trin"] = None
        result["trin_signal"] = "no_data"
        logger.warning("TRIN data unavailable from Stooq")

    return result


def fetch_hlli() -> dict[str, Any]:
    """
    Calculate HLLI (High-Low Leadership Index, Fosback 1976).

    HLLI = (NH - NL) / (NH + NL + 0.001)
    where: NH = new 52-week highs NYSE, NL = new 52-week lows

    HLLI > 0.5 → strong bullish breadth
    HLLI < -0.5 → strong bearish breadth
    Near 0 → mixed/transitional

    Uses Stooq for NYSE new highs/lows.
    """
    logger.info("Calculating HLLI (High-Low Leadership Index)...")
    result: dict[str, Any] = {}

    end = date.today()
    start = end - timedelta(days=90)

    # Fetch new highs
    nh_url = f"https://stooq.com/q/d/l/?s=$nyhl&d1={start.strftime('%Y%m%d')}&d2={end.strftime('%Y%m%d')}&i=d"
    nh_df = _stooq_download(nh_url, "NYSE New Highs")

    # Fetch new lows
    nl_url = f"https://stooq.com/q/d/l/?s=$nylo&d1={start.strftime('%Y%m%d')}&d2={end.strftime('%Y%m%d')}&i=d"
    nl_df = _stooq_download(nl_url, "NYSE New Lows")

    if not nh_df.empty and not nl_df.empty and "CLOSE" in nh_df.columns and "CLOSE" in nl_df.columns:
        nh_last = float(nh_df["CLOSE"].iloc[-1])
        nl_last = float(nl_df["CLOSE"].iloc[-1])

        hlli = (nh_last - nl_last) / (nh_last + nl_last + 0.001)

        result["new_highs"] = int(nh_last)
        result["new_lows"] = int(nl_last)
        result["hlli"] = round(hlli, 4)

        if hlli > 0.5:
            result["hlli_signal"] = "strong bullish breadth (highs dominate)"
        elif hlli > 0.1:
            result["hlli_signal"] = "moderate bullish"
        elif hlli > -0.1:
            result["hlli_signal"] = "mixed / transitional"
        elif hlli > -0.5:
            result["hlli_signal"] = "moderate bearish"
        else:
            result["hlli_signal"] = "strong bearish breadth (lows dominate)"

        # Also compute a 10-day smoothed HLLI
        merged = nh_df[["CLOSE"]].rename(columns={"CLOSE": "NH"}).join(
            nl_df[["CLOSE"]].rename(columns={"CLOSE": "NL"}), how="inner"
        )
        if len(merged) >= 10:
            merged["HLLI"] = (merged["NH"] - merged["NL"]) / (merged["NH"] + merged["NL"] + 0.001)
            result["hlli_10d_avg"] = round(float(merged["HLLI"].iloc[-10:].mean()), 4)
    else:
        result["hlli"] = None
        result["hlli_signal"] = "no_data"
        logger.warning("NYSE highs/lows data unavailable")

    return result


def fetch_mcclellan() -> dict[str, Any]:
    """
    Calculate McClellan Oscillator and Summation Index from NYSE advancing/declining data.

    McClellan Oscillator = EMA(19) - EMA(39) of breadth ratio
    Breadth ratio = (Advancing - Declining) / (Advancing + Declining)

    McClellan > +100 → overbought
    McClellan < -100 → oversold (potential bounce)
    Summation Index tracks cumulative breadth momentum.

    Uses Stooq for NYSE advancing/declining issues.
    """
    logger.info("Calculating McClellan Oscillator & Summation...")
    result: dict[str, Any] = {}

    end = date.today()
    start = end - timedelta(days=365)  # need ~1 year for EMA warmup

    # Fetch advancing issues
    adv_url = f"https://stooq.com/q/d/l/?s=$nyad&d1={start.strftime('%Y%m%d')}&d2={end.strftime('%Y%m%d')}&i=d"
    adv_df = _stooq_download(adv_url, "NYSE Advancing")

    # Fetch declining issues
    dec_url = f"https://stooq.com/q/d/l/?s=$nyde&d1={start.strftime('%Y%m%d')}&d2={end.strftime('%Y%m%d')}&i=d"
    dec_df = _stooq_download(dec_url, "NYSE Declining")

    if not adv_df.empty and not dec_df.empty and "CLOSE" in adv_df.columns and "CLOSE" in dec_df.columns:
        merged = adv_df[["CLOSE"]].rename(columns={"CLOSE": "ADV"}).join(
            dec_df[["CLOSE"]].rename(columns={"CLOSE": "DEC"}), how="inner"
        )

        if len(merged) >= 39:
            # Breadth ratio (sometimes called "net advances ratio")
            merged["RATIO"] = (merged["ADV"] - merged["DEC"]) / (merged["ADV"] + merged["DEC"])

            # McClellan Oscillator = EMA(19) - EMA(39)
            ema19 = merged["RATIO"].ewm(span=19, adjust=False).mean()
            ema39 = merged["RATIO"].ewm(span=39, adjust=False).mean()
            mcclellan = ema19 - ema39

            mco_last = float(mcclellan.iloc[-1])
            result["mcclellan_oscillator"] = round(mco_last, 4)

            # Summation = cumulative sum of McClellan Oscillator
            summation = mcclellan.cumsum()
            result["mcclellan_summation"] = round(float(summation.iloc[-1]), 2)

            # Signal
            if mco_last > 0.05:
                result["mcclellan_signal"] = "overbought (breadth expanding)"
            elif mco_last > 0:
                result["mcclellan_signal"] = "mildly bullish"
            elif mco_last > -0.05:
                result["mcclellan_signal"] = "mildly bearish"
            else:
                result["mcclellan_signal"] = "oversold (breadth contracting — watch for bounce)"
        else:
            result["mcclellan_oscillator"] = None
            result["mcclellan_signal"] = "insufficient_data (need 39+ days)"
    else:
        result["mcclellan_oscillator"] = None
        result["mcclellan_signal"] = "no_data"
        logger.warning("NYSE advancing/declining data unavailable")

    return result
