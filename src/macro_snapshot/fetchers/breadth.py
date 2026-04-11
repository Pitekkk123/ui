"""Breadth indicators — intentionally conservative placeholders.

This module defines the interface and formulas for:
  - TRIN (Arms Index)
  - McClellan Oscillator  (19-EMA minus 39-EMA of net advances / ratio-adjusted)
  - McClellan Summation Index  (running cumulative total of the Oscillator)
  - NH/NL (New Highs minus New Lows)

CRITICAL DISTINCTIONS:
  - McClellan Summation Index = running cumulative total of Oscillator values.
    It is NOT a rolling window sum. Previous Summation + current Oscillator.
  - A rolling sum of the Oscillator is a different, non-standard indicator
    and must never be labeled "McClellan Summation Index".

These are currently PLACEHOLDER returns. Breadth metrics require a
verified feed of daily advances, declines, new highs, new lows,
advancing volume, and declining volume. Until that feed is confirmed,
breadth is excluded from the hard composite score.

Supported provider interface:
  - Implement BreadthProvider and register it to activate breadth.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from macro_snapshot.schemas import (
    STATUS_NO_DATA,
    TIER_B,
    MetricPoint,
)

logger = logging.getLogger(__name__)


# ── Breadth data contract ──────────────────────────────────────────

@dataclass
class BreadthRow:
    """Single day of raw breadth data."""

    date: str  # ISO date
    advances: int
    declines: int
    advancing_volume: float
    declining_volume: float
    new_highs: int
    new_lows: int


class BreadthProvider(ABC):
    """Abstract base for breadth data sources."""

    @abstractmethod
    def fetch_history(self, days: int = 252) -> list[BreadthRow]:
        """Return recent breadth rows, oldest first."""
        ...


# ── Indicator computations ─────────────────────────────────────────

def compute_trin(adv: int, dec: int, adv_vol: float, dec_vol: float) -> Optional[float]:
    """TRIN = (Advances/Declines) / (AdvancingVolume/DecliningVolume)."""
    if dec == 0 or dec_vol == 0:
        return None
    return (adv / dec) / (adv_vol / dec_vol)


def compute_mcclellan_oscillator(net_advances: pd.Series) -> pd.Series:
    """McClellan Oscillator = 19-EMA(net_adv) - 39-EMA(net_adv).

    Uses ratio-adjusted net advances if desired — caller is responsible
    for providing the correct input series.
    """
    ema19 = net_advances.ewm(span=19, adjust=False).mean()
    ema39 = net_advances.ewm(span=39, adjust=False).mean()
    return ema19 - ema39


def compute_mcclellan_summation(oscillator: pd.Series) -> pd.Series:
    """McClellan Summation Index = running cumulative total of Oscillator.

    This is the CLASSIC definition: previous Summation + current Oscillator.
    NOT a rolling window sum.
    """
    return oscillator.cumsum()


def compute_nhll(new_highs: int, new_lows: int) -> int:
    """New Highs minus New Lows."""
    return new_highs - new_lows


# ── Fetcher interface for the pipeline ─────────────────────────────

def fetch_breadth_metrics(
    provider: Optional[BreadthProvider] = None,
) -> list[MetricPoint]:
    """Fetch breadth metrics from provider, or return placeholders.

    Breadth is intentionally not included in hard composite score
    until a verified A/D + NH/NL feed is connected.
    """
    if provider is None:
        return _breadth_placeholders()

    try:
        rows = provider.fetch_history(days=252)
        if not rows:
            return _breadth_placeholders()

        df = pd.DataFrame([r.__dict__ for r in rows])
        df["net_advances"] = df["advances"] - df["declines"]

        latest = rows[-1]
        asof = latest.date

        # TRIN
        trin_val = compute_trin(
            latest.advances,
            latest.declines,
            latest.advancing_volume,
            latest.declining_volume,
        )

        # McClellan Oscillator
        osc_series = compute_mcclellan_oscillator(df["net_advances"])
        osc_val = float(osc_series.iloc[-1]) if not osc_series.empty else None

        # McClellan Summation (running cumulative total)
        summ_series = compute_mcclellan_summation(osc_series)
        summ_val = float(summ_series.iloc[-1]) if not summ_series.empty else None

        # NH/NL
        nhll_val = compute_nhll(latest.new_highs, latest.new_lows)

        return [
            MetricPoint(
                name="trin",
                value=round(trin_val, 4) if trin_val is not None else None,
                asof=asof,
                source="breadth_provider",
                status="ok" if trin_val is not None else "no_data",
                is_stale=False,
                notes="Arms Index. <1 = bullish, >1 = bearish.",
                quality_tier=TIER_B,
                methodology="computed_from_adv_dec_volume",
            ),
            MetricPoint(
                name="mcclellan_oscillator",
                value=round(osc_val, 2) if osc_val is not None else None,
                asof=asof,
                source="breadth_provider",
                status="ok" if osc_val is not None else "no_data",
                is_stale=False,
                notes="19-EMA minus 39-EMA of net advances.",
                quality_tier=TIER_B,
                methodology="ema19_minus_ema39_net_advances",
            ),
            MetricPoint(
                name="mcclellan_summation",
                value=round(summ_val, 2) if summ_val is not None else None,
                asof=asof,
                source="breadth_provider",
                status="ok" if summ_val is not None else "no_data",
                is_stale=False,
                notes=(
                    "Running cumulative total of McClellan Oscillator. "
                    "NOT a rolling sum."
                ),
                quality_tier=TIER_B,
                methodology="cumulative_total_of_oscillator",
            ),
            MetricPoint(
                name="new_highs_minus_lows",
                value=float(nhll_val),
                asof=asof,
                source="breadth_provider",
                status="ok",
                is_stale=False,
                notes="New 52-week highs minus new 52-week lows.",
                quality_tier=TIER_B,
                methodology="nh_minus_nl",
            ),
        ]
    except Exception as exc:
        logger.exception("Breadth computation failed")
        return [
            MetricPoint.error(
                name="breadth_error",
                source="breadth_provider",
                error_msg=str(exc),
                quality_tier=TIER_B,
            )
        ]


def _breadth_placeholders() -> list[MetricPoint]:
    """Return placeholder MetricPoints when no breadth provider is connected."""
    placeholder_note = (
        "No breadth provider connected. McClellan, TRIN, NH/NL require "
        "a verified daily A/D + NH/NL feed. Not included in composite score."
    )
    names = ["trin", "mcclellan_oscillator", "mcclellan_summation", "new_highs_minus_lows"]
    return [
        MetricPoint(
            name=n,
            value=None,
            asof=None,
            source="breadth_provider",
            status=STATUS_NO_DATA,
            is_stale=True,
            notes=placeholder_note,
            quality_tier=TIER_B,
            methodology="placeholder",
        )
        for n in names
    ]
