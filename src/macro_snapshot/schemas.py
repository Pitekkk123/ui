"""Core data schemas for the macro risk overlay engine.

Every metric in the system returns a MetricPoint — a value bundled with
full provenance metadata so the pipeline never silently hides data-quality
issues.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import asdict, dataclass, field
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Quality tiers
# ---------------------------------------------------------------------------
TIER_A = "A"  # Official, auditable source (FRED, Cboe official files)
TIER_B = "B"  # Useful proxy or delayed public source
TIER_C = "C"  # Exploratory / unverified


# ---------------------------------------------------------------------------
# Status codes
# ---------------------------------------------------------------------------
STATUS_OK = "ok"
STATUS_STALE = "stale"
STATUS_NO_DATA = "no_data"
STATUS_ERROR = "error"
STATUS_PROXY = "proxy"


# ---------------------------------------------------------------------------
# MetricPoint
# ---------------------------------------------------------------------------
@dataclass
class MetricPoint:
    """Single observation of a macro metric with full provenance."""

    name: str
    value: Optional[float]
    asof: Optional[str]  # ISO date string e.g. "2026-04-10"
    source: str
    status: str = STATUS_OK  # ok | stale | no_data | error | proxy
    is_stale: bool = False
    notes: str = ""
    quality_tier: str = TIER_A  # A | B | C
    methodology: str = ""  # e.g. official_series, official_close, proxy_realized_vol

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def error(cls, name: str, source: str, error_msg: str, **kw: Any) -> MetricPoint:
        return cls(
            name=name,
            value=None,
            asof=None,
            source=source,
            status=STATUS_ERROR,
            is_stale=True,
            notes=error_msg,
            quality_tier=kw.get("quality_tier", TIER_A),
            methodology=kw.get("methodology", ""),
        )

    @classmethod
    def no_data(cls, name: str, source: str, notes: str = "", **kw: Any) -> MetricPoint:
        return cls(
            name=name,
            value=None,
            asof=None,
            source=source,
            status=STATUS_NO_DATA,
            is_stale=True,
            notes=notes or "Empty series after dropna().",
            quality_tier=kw.get("quality_tier", TIER_A),
            methodology=kw.get("methodology", ""),
        )


# ---------------------------------------------------------------------------
# Snapshot
# ---------------------------------------------------------------------------
@dataclass
class Snapshot:
    """Complete daily macro risk snapshot."""

    timestamp: str = field(default_factory=lambda: dt.datetime.utcnow().isoformat())
    phase: str = "prelim"  # prelim | official_reconciled
    metrics: dict[str, dict[str, Any]] = field(default_factory=dict)

    def add(self, point: MetricPoint) -> None:
        self.metrics[point.name] = point.to_dict()

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "phase": self.phase,
            "metrics": self.metrics,
        }
