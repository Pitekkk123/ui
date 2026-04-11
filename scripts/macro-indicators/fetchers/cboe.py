"""
CBOE data fetcher.

Fetches VIX, VVIX historical data from CBOE CDN (free, unlimited CSV).
Also attempts to fetch VX futures (front and second month) for term structure.
"""

import io
import logging
from datetime import date, datetime, timedelta
from typing import Any

import pandas as pd
import requests

from config import CBOE_VIX_URL, CBOE_VVIX_URL, CBOE_VX_FUTURES_URL

logger = logging.getLogger(__name__)


def _fetch_cboe_csv(url: str, label: str) -> pd.DataFrame:
    """Download a CBOE CSV and return as DataFrame."""
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text), skiprows=1)
        # Normalize column names
        df.columns = [c.strip().upper() for c in df.columns]
        if "DATE" in df.columns:
            df["DATE"] = pd.to_datetime(df["DATE"])
            df = df.set_index("DATE").sort_index()
        return df
    except Exception as e:
        logger.warning("CBOE %s fetch failed: %s", label, e)
        return pd.DataFrame()


def _get_vx_contract_months(n: int = 2) -> list[str]:
    """
    Get the YYYYMM codes for the next N VX futures contract months.
    VX futures expire on the Wednesday 30 days before the third Friday
    of the contract month. We approximate by looking at upcoming months.
    """
    today = date.today()
    months = []
    current = today.replace(day=1)
    for _ in range(n + 2):  # grab extra in case current month expired
        ym = current.strftime("%Y%m")
        months.append(ym)
        # advance to next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    return months[:n + 1]  # return a few candidates


def fetch_vix_vvix() -> dict[str, Any]:
    """
    Fetch VIX and VVIX latest values + the VIX/VVIX matrix classification.

    Returns:
        {
            "vix": 18.5,
            "vvix": 95.2,
            "vix_zone": "15-22",
            "vvix_zone": "90-110",
            "vix_vvix_matrix": "moderate_vol_normal_vvix",
        }
    """
    logger.info("Fetching VIX/VVIX from CBOE CDN...")
    result: dict[str, Any] = {}

    # VIX
    vix_df = _fetch_cboe_csv(CBOE_VIX_URL, "VIX")
    if not vix_df.empty and "CLOSE" in vix_df.columns:
        vix_last = float(vix_df["CLOSE"].iloc[-1])
        result["vix"] = round(vix_last, 2)
        result["vix_date"] = str(vix_df.index[-1].date())
        if vix_last < 15:
            result["vix_zone"] = "<15 (complacency)"
        elif vix_last < 22:
            result["vix_zone"] = "15-22 (normal)"
        elif vix_last < 30:
            result["vix_zone"] = "22-30 (elevated)"
        else:
            result["vix_zone"] = ">30 (fear/panic)"
    else:
        result["vix"] = None

    # VVIX
    vvix_df = _fetch_cboe_csv(CBOE_VVIX_URL, "VVIX")
    if not vvix_df.empty and "CLOSE" in vvix_df.columns:
        vvix_last = float(vvix_df["CLOSE"].iloc[-1])
        result["vvix"] = round(vvix_last, 2)
        result["vvix_date"] = str(vvix_df.index[-1].date())
        if vvix_last < 90:
            result["vvix_zone"] = "<90 (low vol-of-vol)"
        elif vvix_last < 110:
            result["vvix_zone"] = "90-110 (normal)"
        elif vvix_last < 120:
            result["vvix_zone"] = "110-120 (elevated)"
        else:
            result["vvix_zone"] = ">120 (extreme)"
    else:
        result["vvix"] = None

    # VIX/VVIX matrix
    if result.get("vix") is not None and result.get("vvix") is not None:
        v, vv = result["vix"], result["vvix"]
        if v < 15 and vv < 90:
            result["vix_vvix_matrix"] = "complacent_calm"
        elif v < 15 and vv >= 110:
            result["vix_vvix_matrix"] = "complacent_but_hedging (watch out)"
        elif v >= 22 and vv < 90:
            result["vix_vvix_matrix"] = "elevated_vol_no_panic (potential opportunity)"
        elif v >= 30 and vv >= 120:
            result["vix_vvix_matrix"] = "full_panic (capitulation zone)"
        else:
            result["vix_vvix_matrix"] = "mixed"

    return result


def fetch_vx_term_structure() -> dict[str, Any]:
    """
    Fetch VX1/VX2 (front/second month futures) for term structure analysis.

    Returns:
        {
            "vx1": 19.5,
            "vx2": 21.0,
            "vx_ratio": 0.929,
            "term_structure": "contango",
        }
    """
    logger.info("Fetching VX futures term structure...")
    result: dict[str, Any] = {}
    contract_months = _get_vx_contract_months(3)
    settlements = []

    for ym in contract_months:
        url = CBOE_VX_FUTURES_URL.format(ym=ym)
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                continue
            df = pd.read_csv(io.StringIO(resp.text))
            df.columns = [c.strip().upper() for c in df.columns]
            # Look for settlement/close price column
            price_col = None
            for candidate in ["SETTLE", "SETTLEMENT PRICE", "CLOSE", "LAST"]:
                if candidate in df.columns:
                    price_col = candidate
                    break
            if price_col and not df.empty:
                last_price = pd.to_numeric(df[price_col], errors="coerce").dropna()
                if not last_price.empty:
                    settlements.append({
                        "contract": ym,
                        "price": float(last_price.iloc[-1]),
                    })
        except Exception as e:
            logger.debug("VX %s fetch failed: %s", ym, e)

    if len(settlements) >= 2:
        result["vx1"] = round(settlements[0]["price"], 2)
        result["vx1_contract"] = settlements[0]["contract"]
        result["vx2"] = round(settlements[1]["price"], 2)
        result["vx2_contract"] = settlements[1]["contract"]
        result["vx_ratio"] = round(settlements[0]["price"] / settlements[1]["price"], 4)
        if result["vx_ratio"] < 0.95:
            result["term_structure"] = "contango (normal, VX1 < VX2)"
        elif result["vx_ratio"] > 1.05:
            result["term_structure"] = "backwardation (fear, VX1 > VX2)"
        else:
            result["term_structure"] = "flat"
    elif len(settlements) == 1:
        result["vx1"] = round(settlements[0]["price"], 2)
        result["vx1_contract"] = settlements[0]["contract"]
        result["term_structure"] = "insufficient_data"
    else:
        result["term_structure"] = "no_data"
        logger.warning("Could not fetch VX futures data")

    return result
