"""Polygon / Massive options chain fetcher — Tier B gamma-OI proxy.

Computes spy_gamma_oi_proxy and optionally spx_gamma_oi_proxy from
Polygon chain snapshot data.  The snapshot endpoint returns greeks,
implied_volatility and open_interest per contract.

IMPORTANT naming convention:
  - This is NOT "true GEX" / dealer gamma exposure.
  - It is a gamma * open_interest proxy from public chain snapshots.
  - The result is labeled *_gamma_oi_proxy, never "gex".
"""

from __future__ import annotations

import datetime as dt
import logging
import os
from typing import Optional

from macro_snapshot.schemas import (
    STATUS_ERROR,
    STATUS_NO_DATA,
    STATUS_PROXY,
    TIER_B,
    MetricPoint,
)

logger = logging.getLogger(__name__)


def _compute_gamma_oi_proxy(
    api_key: str,
    underlying: str,
    metric_name: str,
) -> MetricPoint:
    """Compute net gamma * OI proxy for a single underlying."""
    try:
        from polygon import RESTClient

        client = RESTClient(api_key)

        total_call_gamma_oi = 0.0
        total_put_gamma_oi = 0.0
        contract_count = 0

        for snap in client.list_snapshot_options_chain(underlying):
            greeks = getattr(snap, "greeks", None)
            oi = getattr(snap, "open_interest", None)
            details = getattr(snap, "details", None)

            if greeks is None or oi is None:
                continue

            gamma = getattr(greeks, "gamma", None)
            if gamma is None:
                continue

            contract_type = getattr(details, "contract_type", None) if details else None
            gamma_oi = gamma * oi
            contract_count += 1

            if contract_type == "call":
                total_call_gamma_oi += gamma_oi
            elif contract_type == "put":
                total_put_gamma_oi += gamma_oi
            else:
                total_call_gamma_oi += gamma_oi  # default bucket

        if contract_count == 0:
            return MetricPoint(
                name=metric_name,
                value=None,
                asof=None,
                source=f"POLYGON:{underlying}",
                status=STATUS_NO_DATA,
                is_stale=True,
                notes="No contracts with gamma and OI found in snapshot.",
                quality_tier=TIER_B,
                methodology="gamma_oi_proxy",
            )

        net_gamma_oi = total_call_gamma_oi - total_put_gamma_oi

        return MetricPoint(
            name=metric_name,
            value=net_gamma_oi,
            asof=dt.date.today().isoformat(),
            source=f"POLYGON:{underlying}",
            status=STATUS_PROXY,
            is_stale=False,
            notes=(
                f"Net gamma*OI proxy from {contract_count} contracts. "
                "Not dealer book, not full market GEX. "
                f"Call gamma*OI={total_call_gamma_oi:.2f}, "
                f"Put gamma*OI={total_put_gamma_oi:.2f}."
            ),
            quality_tier=TIER_B,
            methodology="gamma_oi_proxy",
        )
    except ImportError:
        return MetricPoint.error(
            name=metric_name,
            source=f"POLYGON:{underlying}",
            error_msg="polygon-api-client not installed.",
            quality_tier=TIER_B,
            methodology="gamma_oi_proxy",
        )
    except Exception as exc:
        logger.exception("Polygon options fetch failed for %s", underlying)
        return MetricPoint.error(
            name=metric_name,
            source=f"POLYGON:{underlying}",
            error_msg=str(exc),
            quality_tier=TIER_B,
            methodology="gamma_oi_proxy",
        )


def fetch_gamma_oi_proxies(
    api_key: Optional[str] = None,
) -> list[MetricPoint]:
    """Fetch gamma-OI proxy for SPY and optionally SPX.

    If POLYGON_API_KEY is not set, returns placeholder MetricPoints
    so the pipeline degrades gracefully.
    """
    key = api_key or os.environ.get("POLYGON_API_KEY", "")

    if not key:
        placeholder = MetricPoint(
            name="spy_gamma_oi_proxy",
            value=None,
            asof=None,
            source="POLYGON:SPY",
            status=STATUS_NO_DATA,
            is_stale=True,
            notes="POLYGON_API_KEY not configured. Set it in .env to enable gamma-OI proxy.",
            quality_tier=TIER_B,
            methodology="gamma_oi_proxy",
        )
        return [
            placeholder,
            MetricPoint(
                name="spx_gamma_oi_proxy",
                value=None,
                asof=None,
                source="POLYGON:I:SPX",
                status=STATUS_NO_DATA,
                is_stale=True,
                notes="POLYGON_API_KEY not configured.",
                quality_tier=TIER_B,
                methodology="gamma_oi_proxy",
            ),
        ]

    results = [
        _compute_gamma_oi_proxy(key, "SPY", "spy_gamma_oi_proxy"),
    ]

    # SPX options (index options) — may require higher Polygon tier
    spx = _compute_gamma_oi_proxy(key, "I:SPX", "spx_gamma_oi_proxy")
    results.append(spx)

    return results
