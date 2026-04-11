"""Tests for fetchers/proxies.py — TLT realized vol proxy."""

from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from macro_snapshot.schemas import STATUS_PROXY


class TestTLTRealizedVol:
    @patch("yfinance.download")
    def test_successful_computation(self, mock_download):
        dates = pd.bdate_range("2026-02-01", periods=40)
        np.random.seed(42)
        prices = 90 + np.cumsum(np.random.randn(40) * 0.5)
        mock_download.return_value = pd.DataFrame({"Close": prices}, index=dates)

        from macro_snapshot.fetchers.proxies import fetch_tlt_realized_vol

        mp = fetch_tlt_realized_vol()
        assert mp.name == "tlt_realized_vol_proxy"
        assert mp.status == STATUS_PROXY
        assert mp.value is not None
        assert mp.value > 0
        assert mp.quality_tier == "B"
        assert "realized_vol" in mp.methodology or "realized" in mp.methodology
        assert "Not ICE MOVE" in mp.notes or "not ICE MOVE" in mp.notes

    @patch("yfinance.download")
    def test_insufficient_data(self, mock_download):
        dates = pd.bdate_range("2026-04-01", periods=5)
        mock_download.return_value = pd.DataFrame({"Close": [90, 91, 92, 91, 90]}, index=dates)

        from macro_snapshot.fetchers.proxies import fetch_tlt_realized_vol

        mp = fetch_tlt_realized_vol()
        assert mp.value is None
        assert mp.is_stale is True

    @patch("yfinance.download")
    def test_empty_data(self, mock_download):
        mock_download.return_value = pd.DataFrame()

        from macro_snapshot.fetchers.proxies import fetch_tlt_realized_vol

        mp = fetch_tlt_realized_vol()
        assert mp.value is None
        assert mp.status == "no_data"
