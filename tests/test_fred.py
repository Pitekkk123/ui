"""Tests for fetchers/fred.py — mocked FRED API data."""

import json
from unittest.mock import MagicMock, patch

import pytest

from macro_snapshot.fetchers.fred import FRED_SERIES, fetch_fred_series
from macro_snapshot.schemas import STATUS_ERROR, STATUS_OK


def _mock_fred_response(sid: str, value: float = 3.5):
    """Create a mock FRED API JSON response."""
    return {
        "observations": [
            {"date": "2026-04-10", "value": str(value)},
            {"date": "2026-04-09", "value": str(value - 0.1)},
        ]
    }


class TestFetchFredSeries:
    @patch("macro_snapshot.fetchers.fred.requests.get")
    def test_successful_fetch(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.side_effect = [
            _mock_fred_response(sid) for sid in FRED_SERIES.values()
        ]
        mock_get.return_value = mock_resp

        results = fetch_fred_series(api_key="test_key")
        assert len(results) == len(FRED_SERIES)

        for mp in results:
            assert mp.status == STATUS_OK
            assert mp.value is not None
            assert mp.quality_tier == "A"
            assert mp.methodology == "official_series"
            assert mp.source.startswith("FRED:")

    @patch("macro_snapshot.fetchers.fred.requests.get")
    def test_missing_observations(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {
            "observations": [{"date": "2026-04-10", "value": "."}]
        }
        mock_get.return_value = mock_resp

        results = fetch_fred_series(api_key="test_key")
        for mp in results:
            assert mp.status == "no_data"
            assert mp.value is None
            assert mp.is_stale is True

    @patch("macro_snapshot.fetchers.fred.requests.get")
    def test_network_error(self, mock_get):
        mock_get.side_effect = ConnectionError("FRED unreachable")

        results = fetch_fred_series(api_key="test_key")
        for mp in results:
            assert mp.status == STATUS_ERROR
            assert "FRED unreachable" in mp.notes

    def test_no_api_key(self):
        """Without API key, all metrics should return error with registration info."""
        results = fetch_fred_series(api_key="")
        assert len(results) == len(FRED_SERIES)
        for mp in results:
            assert mp.status == STATUS_ERROR
            assert "FRED_API_KEY" in mp.notes
