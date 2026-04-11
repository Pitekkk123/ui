"""Tests for fetchers/cboe.py — mocked Cboe CSV data."""

from unittest.mock import MagicMock, patch

import pytest

from macro_snapshot.fetchers.cboe import fetch_cboe_vix, fetch_cboe_vvix
from macro_snapshot.schemas import STATUS_ERROR, STATUS_OK

MOCK_VIX_CSV = """VIX History
DATE,OPEN,HIGH,LOW,CLOSE
04/08/2026,17.50,18.20,17.10,17.80
04/09/2026,17.80,19.00,17.60,18.50
04/10/2026,18.50,18.80,18.00,18.30
"""


class TestFetchCboeVix:
    @patch("macro_snapshot.fetchers.cboe.requests.get")
    def test_successful_fetch(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = MOCK_VIX_CSV
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        mp = fetch_cboe_vix()
        assert mp.name == "vix_close"
        assert mp.value == 18.3
        assert mp.asof == "2026-04-10"
        assert mp.quality_tier == "A"
        assert mp.methodology == "official_close"
        assert "Official Cboe" in mp.notes

    @patch("macro_snapshot.fetchers.cboe.requests.get")
    def test_network_error(self, mock_get):
        mock_get.side_effect = ConnectionError("Cboe unreachable")

        mp = fetch_cboe_vix()
        assert mp.status == STATUS_ERROR
        assert mp.value is None

    @patch("macro_snapshot.fetchers.cboe.requests.get")
    def test_vvix_fetch(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = MOCK_VIX_CSV.replace("VIX History", "VVIX History")
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        mp = fetch_cboe_vvix()
        assert mp.name == "vvix_close"
        assert mp.value == 18.3
