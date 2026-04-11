"""Tests for schemas.py — MetricPoint and Snapshot."""

import pytest

from macro_snapshot.schemas import (
    TIER_A,
    TIER_B,
    MetricPoint,
    Snapshot,
    STATUS_ERROR,
    STATUS_NO_DATA,
    STATUS_OK,
)


class TestMetricPoint:
    def test_basic_creation(self):
        mp = MetricPoint(
            name="test_metric",
            value=42.0,
            asof="2026-04-10",
            source="TEST",
            status=STATUS_OK,
        )
        assert mp.name == "test_metric"
        assert mp.value == 42.0
        assert mp.is_stale is False
        assert mp.quality_tier == TIER_A

    def test_to_dict(self):
        mp = MetricPoint(
            name="hy_oas",
            value=3.5,
            asof="2026-04-10",
            source="FRED:BAMLH0A0HYM2",
            status=STATUS_OK,
            quality_tier=TIER_A,
            methodology="official_series",
        )
        d = mp.to_dict()
        assert d["name"] == "hy_oas"
        assert d["value"] == 3.5
        assert d["quality_tier"] == "A"
        assert d["methodology"] == "official_series"

    def test_error_factory(self):
        mp = MetricPoint.error(
            name="broken",
            source="TEST",
            error_msg="Connection timeout",
            quality_tier=TIER_B,
        )
        assert mp.status == STATUS_ERROR
        assert mp.value is None
        assert mp.is_stale is True
        assert "Connection timeout" in mp.notes

    def test_no_data_factory(self):
        mp = MetricPoint.no_data(
            name="empty",
            source="TEST",
        )
        assert mp.status == STATUS_NO_DATA
        assert mp.value is None
        assert mp.is_stale is True


class TestSnapshot:
    def test_add_and_to_dict(self):
        snap = Snapshot(phase="prelim")
        snap.add(
            MetricPoint(
                name="vix_close",
                value=18.5,
                asof="2026-04-10",
                source="CBOE:VIX",
            )
        )
        d = snap.to_dict()
        assert d["phase"] == "prelim"
        assert "vix_close" in d["metrics"]
        assert d["metrics"]["vix_close"]["value"] == 18.5

    def test_multiple_metrics(self):
        snap = Snapshot()
        for i in range(5):
            snap.add(
                MetricPoint(name=f"m{i}", value=float(i), asof=None, source="TEST")
            )
        assert len(snap.metrics) == 5
