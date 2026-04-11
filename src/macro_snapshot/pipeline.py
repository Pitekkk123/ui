"""Pipeline orchestrator — assembles the daily macro risk snapshot.

Two-phase design:
  Phase 1 (prelim_snapshot): run after US close.
    Collects FRED, Cboe VIX/VVIX, TLT proxy, Polygon gamma-OI proxy,
    breadth placeholders.

  Phase 2 (official_reconcile): run next business day ~10:00 CT.
    Updates VX settlement curve with official Cboe futures data.

Each MetricPoint carries its own status, quality_tier and methodology,
so the snapshot never silently mixes official and proxy data.
"""

from __future__ import annotations

import logging
from typing import Optional

from macro_snapshot.fetchers.breadth import BreadthProvider, fetch_breadth_metrics
from macro_snapshot.fetchers.cboe import fetch_cboe_vol_stack, fetch_vx_settlement_curve
from macro_snapshot.fetchers.fred import fetch_fred_series
from macro_snapshot.fetchers.polygon_options import fetch_gamma_oi_proxies
from macro_snapshot.fetchers.proxies import fetch_tlt_realized_vol
from macro_snapshot.schemas import MetricPoint, Snapshot
from macro_snapshot.signals import compute_signals

logger = logging.getLogger(__name__)


def build_prelim_snapshot(
    polygon_api_key: Optional[str] = None,
    breadth_provider: Optional[BreadthProvider] = None,
    skip_network: bool = False,
) -> Snapshot:
    """Build the preliminary (same-day) macro snapshot.

    Args:
        polygon_api_key: Polygon/Massive API key for gamma-OI proxy.
        breadth_provider: Optional breadth data provider.
        skip_network: If True, return an empty snapshot (for testing).
    """
    snap = Snapshot(phase="prelim")

    if skip_network:
        return snap

    # ── Tier A: FRED ───────────────────────────────────────────────
    logger.info("Fetching FRED series...")
    for pt in fetch_fred_series():
        snap.add(pt)

    # ── Tier A: Cboe VIX / VVIX ───────────────────────────────────
    logger.info("Fetching Cboe VIX/VVIX...")
    for pt in fetch_cboe_vol_stack():
        snap.add(pt)

    # ── Tier B: TLT realized vol proxy ────────────────────────────
    logger.info("Fetching TLT realized vol proxy...")
    snap.add(fetch_tlt_realized_vol())

    # ── Tier B: Polygon gamma-OI proxy ────────────────────────────
    logger.info("Fetching Polygon gamma-OI proxies...")
    for pt in fetch_gamma_oi_proxies(api_key=polygon_api_key):
        snap.add(pt)

    # ── Tier B: Breadth (placeholder until verified feed) ─────────
    logger.info("Fetching breadth metrics...")
    for pt in fetch_breadth_metrics(provider=breadth_provider):
        snap.add(pt)

    # ── Signals / composite score ─────────────────────────────────
    logger.info("Computing signals...")
    for pt in compute_signals(snap):
        snap.add(pt)

    return snap


def build_reconciled_snapshot(
    base: Optional[Snapshot] = None,
) -> Snapshot:
    """Build the T+1 official reconciliation snapshot.

    Updates VX settlement data with official Cboe futures stats
    published the next business day.
    """
    snap = base or Snapshot(phase="official_reconciled")
    snap.phase = "official_reconciled"

    logger.info("Fetching VX settlement curve (T+1 reconcile)...")
    for pt in fetch_vx_settlement_curve():
        snap.add(pt)

    return snap
