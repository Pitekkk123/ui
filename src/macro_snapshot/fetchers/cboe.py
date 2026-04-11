"""Cboe fetcher — Tier A official VIX/VVIX and VX settlement data.

Downloads official historical CSV files published by Cboe:
  - VIX daily history
  - VVIX daily history

Also provides a VX settlement curve parser for the two-phase
prelim / official_reconciled pipeline.

Note: Cboe publishes daily futures stats/settlements with a delay —
approximately 10:00 a.m. CT the next business day. The pipeline
should therefore run VX reconciliation as a T+1 step.
"""

from __future__ import annotations

import datetime as dt
import io
import logging
from typing import Any

import pandas as pd
import requests

from macro_snapshot.schemas import (
    TIER_A,
    MetricPoint,
)

logger = logging.getLogger(__name__)

# ── Official Cboe CSV endpoints ────────────────────────────────────
CBOE_VIX_CSV = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv"
CBOE_VVIX_CSV = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VVIX_History.csv"

STALE_DAYS = 5
REQUEST_TIMEOUT = 30


def _check_stale(last_date: dt.date) -> bool:
    return (dt.date.today() - last_date).days > STALE_DAYS


def _fetch_cboe_index_csv(url: str, metric_name: str) -> MetricPoint:
    """Download one official Cboe index CSV and return the latest close."""
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        df = pd.read_csv(io.StringIO(resp.text), skiprows=1)
        df["DATE"] = pd.to_datetime(df["DATE"])
        df = df.dropna(subset=["CLOSE"]).sort_values("DATE")

        if df.empty:
            return MetricPoint.no_data(
                name=metric_name,
                source=f"CBOE:{metric_name.upper()}",
                quality_tier=TIER_A,
                methodology="official_close",
            )

        last = df.iloc[-1]
        last_date = last["DATE"].date()
        is_stale = _check_stale(last_date)

        return MetricPoint(
            name=metric_name,
            value=float(last["CLOSE"]),
            asof=last_date.isoformat(),
            source=f"CBOE:{metric_name.upper()}",
            status="stale" if is_stale else "ok",
            is_stale=is_stale,
            notes="Official Cboe historical CSV close."
            + (f" Stale: last obs {last_date}" if is_stale else ""),
            quality_tier=TIER_A,
            methodology="official_close",
        )
    except Exception as exc:
        logger.exception("Cboe fetch failed for %s", metric_name)
        return MetricPoint.error(
            name=metric_name,
            source=f"CBOE:{metric_name.upper()}",
            error_msg=str(exc),
            quality_tier=TIER_A,
            methodology="official_close",
        )


def fetch_cboe_vix() -> MetricPoint:
    """Fetch official VIX close from Cboe CSV."""
    return _fetch_cboe_index_csv(CBOE_VIX_CSV, "vix_close")


def fetch_cboe_vvix() -> MetricPoint:
    """Fetch official VVIX close from Cboe CSV."""
    return _fetch_cboe_index_csv(CBOE_VVIX_CSV, "vvix_close")


def fetch_cboe_vol_stack() -> list[MetricPoint]:
    """Fetch both VIX and VVIX from official Cboe CSVs."""
    return [fetch_cboe_vix(), fetch_cboe_vvix()]


# ── VX Settlement Curve (T+1 reconciliation) ──────────────────────

def fetch_vx_settlement_curve() -> list[MetricPoint]:
    """Placeholder for VX futures settlement curve reconciliation.

    In production this should:
    1. Download the official Cboe VX settlement CSV/page for the
       most recent settlement date.
    2. Parse VX1, VX2 (and optionally further months) settlement prices.
    3. Compute vx1_settlement, vx2_settlement, vx1_vx2_ratio,
       vx_term_structure_state.

    This is intentionally a T+1 operation because Cboe daily futures
    stats are published approximately 10:00 a.m. CT the next business day.
    """
    return [
        MetricPoint(
            name="vx1_settlement",
            value=None,
            asof=None,
            source="CBOE:VX_SETTLEMENT",
            status="no_data",
            is_stale=True,
            notes="VX settlement reconciliation not yet configured. "
            "Requires T+1 official data from Cboe CFE.",
            quality_tier=TIER_A,
            methodology="official_settlement",
        ),
        MetricPoint(
            name="vx2_settlement",
            value=None,
            asof=None,
            source="CBOE:VX_SETTLEMENT",
            status="no_data",
            is_stale=True,
            notes="VX settlement reconciliation not yet configured.",
            quality_tier=TIER_A,
            methodology="official_settlement",
        ),
        MetricPoint(
            name="vx1_vx2_ratio",
            value=None,
            asof=None,
            source="CBOE:VX_SETTLEMENT",
            status="no_data",
            is_stale=True,
            notes="Requires VX1 and VX2 settlements.",
            quality_tier=TIER_A,
            methodology="derived_from_official_settlement",
        ),
    ]
