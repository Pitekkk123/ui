"""Tests for signals.py — composite scoring logic."""

import pytest

from macro_snapshot.schemas import TIER_A, TIER_B, MetricPoint, Snapshot
from macro_snapshot.signals import compute_signals


def _make_snapshot(**metric_values) -> Snapshot:
    """Create a snapshot with given metric values (all Tier A, status ok)."""
    snap = Snapshot(phase="prelim")
    for name, value in metric_values.items():
        snap.add(
            MetricPoint(
                name=name,
                value=value,
                asof="2026-04-10",
                source="TEST",
                status="ok",
                quality_tier=TIER_A,
                methodology="test",
            )
        )
    return snap


class TestCompositeScore:
    def test_benign_environment(self):
        """All metrics in benign range should produce positive score."""
        snap = _make_snapshot(
            hy_oas=3.0,
            ig_oas=0.8,
            nfci=-0.7,
            spread_2s10s=1.5,
            spread_3m10y=2.0,
            vix_close=13.0,
            vvix_close=85.0,
        )
        signals = compute_signals(snap)
        env_score = next(s for s in signals if s.name == "environment_score")
        assert env_score.value > 0
        assert env_score.value <= 1.0

    def test_stress_environment(self):
        """All metrics in stress range should produce negative score."""
        snap = _make_snapshot(
            hy_oas=6.0,
            ig_oas=2.5,
            nfci=0.8,
            spread_2s10s=-0.5,
            spread_3m10y=-0.3,
            vix_close=35.0,
            vvix_close=130.0,
        )
        signals = compute_signals(snap)
        env_score = next(s for s in signals if s.name == "environment_score")
        assert env_score.value < 0

    def test_empty_snapshot(self):
        """Empty snapshot should still return a score (0.0)."""
        snap = Snapshot(phase="prelim")
        signals = compute_signals(snap)
        env_score = next(s for s in signals if s.name == "environment_score")
        assert env_score.value == 0.0

    def test_flag_counts(self):
        """Verify bullish and bearish flag counts."""
        snap = _make_snapshot(
            hy_oas=3.0,  # benign
            vix_close=35.0,  # stress
        )
        signals = compute_signals(snap)

        bullish = next(s for s in signals if s.name == "bullish_flags")
        bearish = next(s for s in signals if s.name == "bearish_flags")
        assert bullish.value >= 1  # at least HY OAS benign
        assert bearish.value >= 1  # at least VIX stress

    def test_proxy_metrics_not_scored(self):
        """Proxy metrics should appear in proxy_flags, not affect score."""
        snap = Snapshot(phase="prelim")
        snap.add(
            MetricPoint(
                name="spy_gamma_oi_proxy",
                value=100000.0,
                asof="2026-04-10",
                source="POLYGON:SPY",
                status="proxy",
                quality_tier=TIER_B,
                methodology="gamma_oi_proxy",
            )
        )
        signals = compute_signals(snap)
        proxy_flags = next(s for s in signals if s.name == "proxy_flags")
        assert proxy_flags.value >= 1

    def test_stale_metrics_flagged(self):
        """Stale metrics should appear in stale_flags."""
        snap = Snapshot(phase="prelim")
        snap.add(
            MetricPoint(
                name="hy_oas",
                value=4.0,
                asof="2026-03-01",
                source="FRED:BAMLH0A0HYM2",
                status="stale",
                is_stale=True,
                quality_tier=TIER_A,
            )
        )
        signals = compute_signals(snap)
        stale_flags = next(s for s in signals if s.name == "stale_flags")
        assert stale_flags.value >= 1

    def test_all_signal_names_present(self):
        """Verify all expected signal names are returned."""
        snap = Snapshot(phase="prelim")
        signals = compute_signals(snap)
        names = {s.name for s in signals}
        assert names == {
            "environment_score",
            "bullish_flags",
            "bearish_flags",
            "proxy_flags",
            "stale_flags",
        }
