"""Tests for fetchers/breadth.py — indicator computations and placeholders."""

import pandas as pd
import pytest

from macro_snapshot.fetchers.breadth import (
    BreadthProvider,
    BreadthRow,
    compute_mcclellan_oscillator,
    compute_mcclellan_summation,
    compute_nhll,
    compute_trin,
    fetch_breadth_metrics,
)


class TestTRIN:
    def test_normal(self):
        # TRIN = (2000/1000) / (5e9/3e9) = 2.0 / 1.667 = 1.2
        result = compute_trin(2000, 1000, 5e9, 3e9)
        assert result is not None
        assert round(result, 2) == 1.2

    def test_zero_declines(self):
        assert compute_trin(2000, 0, 5e9, 3e9) is None

    def test_zero_declining_volume(self):
        assert compute_trin(2000, 1000, 5e9, 0) is None


class TestMcClellanOscillator:
    def test_basic(self):
        # Simple series of net advances
        net_adv = pd.Series([100, 150, 200, -50, 100, 250, 300, 100, -100, 50] * 5)
        osc = compute_mcclellan_oscillator(net_adv)
        assert len(osc) == len(net_adv)
        # EMA19 and EMA39 diverge, so oscillator should be non-trivial
        assert osc.std() > 0


class TestMcClellanSummation:
    def test_is_cumulative_not_rolling(self):
        """Summation must be cumulative total, not rolling window."""
        osc = pd.Series([10.0, 20.0, -5.0, 15.0, -10.0])
        summ = compute_mcclellan_summation(osc)

        # cumsum: 10, 30, 25, 40, 30
        assert summ.iloc[0] == 10.0
        assert summ.iloc[1] == 30.0
        assert summ.iloc[2] == 25.0
        assert summ.iloc[3] == 40.0
        assert summ.iloc[4] == 30.0


class TestNHLL:
    def test_basic(self):
        assert compute_nhll(200, 50) == 150
        assert compute_nhll(50, 200) == -150
        assert compute_nhll(100, 100) == 0


class TestFetchBreadthMetrics:
    def test_no_provider_returns_placeholders(self):
        results = fetch_breadth_metrics(provider=None)
        assert len(results) == 4
        for mp in results:
            assert mp.status == "no_data"
            assert mp.value is None
            assert mp.is_stale is True
            assert "No breadth provider" in mp.notes

    def test_with_provider(self):
        class MockProvider(BreadthProvider):
            def fetch_history(self, days=252):
                rows = []
                for i in range(50):
                    rows.append(
                        BreadthRow(
                            date=f"2026-02-{(i % 28) + 1:02d}",
                            advances=2000 + i * 10,
                            declines=1000 + i * 5,
                            advancing_volume=5e9,
                            declining_volume=3e9,
                            new_highs=200 + i,
                            new_lows=50 + i,
                        )
                    )
                return rows

        results = fetch_breadth_metrics(provider=MockProvider())
        names = {mp.name for mp in results}
        assert "trin" in names
        assert "mcclellan_oscillator" in names
        assert "mcclellan_summation" in names
        assert "new_highs_minus_lows" in names

        for mp in results:
            assert mp.value is not None
            assert mp.quality_tier == "B"
