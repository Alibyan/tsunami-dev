"""Tests for the optional Open-Meteo marine enrichment module."""

from unittest.mock import MagicMock, patch

from src.enrich_marine import MarineConditions, fetch_marine_conditions


def test_marine_conditions_summary_full():
    c = MarineConditions(
        wave_height_m=2.3, wave_period_s=12.0, wave_direction_deg=270.0
    )
    summary = c.summary()
    assert "2.3 m" in summary
    assert "12 s" in summary
    assert "270°" in summary


def test_marine_conditions_summary_partial():
    c = MarineConditions(wave_height_m=1.0, wave_period_s=None, wave_direction_deg=None)
    summary = c.summary()
    assert "1.0 m" in summary
    assert "Period" not in summary


def test_marine_conditions_summary_empty():
    c = MarineConditions(
        wave_height_m=None, wave_period_s=None, wave_direction_deg=None
    )
    assert c.summary() == "No wave data available."


def test_fetch_marine_conditions_success(monkeypatch):
    fake_response = MagicMock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {
        "current": {
            "wave_height": 1.5,
            "wave_period": 10.0,
            "wave_direction": 90.0,
        }
    }

    with patch("src.enrich_marine.requests.get", return_value=fake_response):
        result = fetch_marine_conditions(lat=35.0, lon=139.0)

    assert result is not None
    assert result.wave_height_m == 1.5
    assert result.wave_period_s == 10.0
    assert result.wave_direction_deg == 90.0


def test_fetch_marine_conditions_returns_none_on_error():
    with patch(
        "src.enrich_marine.requests.get", side_effect=Exception("network error")
    ):
        result = fetch_marine_conditions(lat=35.0, lon=139.0)
    assert result is None


def test_fetch_marine_conditions_returns_none_on_bad_status(monkeypatch):
    fake_response = MagicMock()
    fake_response.raise_for_status.side_effect = Exception("404")

    with patch("src.enrich_marine.requests.get", return_value=fake_response):
        result = fetch_marine_conditions(lat=35.0, lon=139.0)

    assert result is None
