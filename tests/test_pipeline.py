"""Tests for pipeline.py — orchestrator."""

from unittest.mock import patch

import pytest

from macro_snapshot.pipeline import build_prelim_snapshot, build_reconciled_snapshot
from macro_snapshot.schemas import MetricPoint, Snapshot


class TestBuildPrelimSnapshot:
    def test_skip_network(self):
        """skip_network should return an empty snapshot."""
        snap = build_prelim_snapshot(skip_network=True)
        assert isinstance(snap, Snapshot)
        assert snap.phase == "prelim"
        assert len(snap.metrics) == 0

    @patch("macro_snapshot.pipeline.fetch_breadth_metrics")
    @patch("macro_snapshot.pipeline.fetch_gamma_oi_proxies")
    @patch("macro_snapshot.pipeline.fetch_tlt_realized_vol")
    @patch("macro_snapshot.pipeline.fetch_cboe_vol_stack")
    @patch("macro_snapshot.pipeline.fetch_fred_series")
    def test_full_pipeline_assembly(
        self,
        mock_fred,
        mock_cboe,
        mock_tlt,
        mock_polygon,
        mock_breadth,
    ):
        """Verify all fetchers are called and results assembled."""
        mock_fred.return_value = [
            MetricPoint(name="hy_oas", value=3.5, asof="2026-04-10", source="FRED:TEST")
        ]
        mock_cboe.return_value = [
            MetricPoint(name="vix_close", value=18.0, asof="2026-04-10", source="CBOE:VIX")
        ]
        mock_tlt.return_value = MetricPoint(
            name="tlt_realized_vol_proxy", value=12.5, asof="2026-04-10", source="yfinance/TLT",
            status="proxy", quality_tier="B",
        )
        mock_polygon.return_value = [
            MetricPoint(
                name="spy_gamma_oi_proxy", value=50000.0, asof="2026-04-10",
                source="POLYGON:SPY", status="proxy", quality_tier="B",
            )
        ]
        mock_breadth.return_value = [
            MetricPoint(name="trin", value=None, asof=None, source="breadth_provider", status="no_data")
        ]

        snap = build_prelim_snapshot()
        assert snap.phase == "prelim"
        assert "hy_oas" in snap.metrics
        assert "vix_close" in snap.metrics
        assert "tlt_realized_vol_proxy" in snap.metrics
        assert "spy_gamma_oi_proxy" in snap.metrics
        # Signals are also computed
        assert "environment_score" in snap.metrics


class TestBuildReconciledSnapshot:
    @patch("macro_snapshot.pipeline.fetch_vx_settlement_curve")
    def test_reconcile_adds_vx(self, mock_vx):
        mock_vx.return_value = [
            MetricPoint(
                name="vx1_settlement", value=19.5, asof="2026-04-10",
                source="CBOE:VX_SETTLEMENT",
            )
        ]
        snap = build_reconciled_snapshot()
        assert snap.phase == "official_reconciled"
        assert "vx1_settlement" in snap.metrics
