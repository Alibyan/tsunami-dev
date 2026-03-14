from datetime import datetime, timezone

from src.ingest_catalog import build_catalog_params, fetch_catalog


def test_build_catalog_params_defaults_shape():
    start = datetime(2026, 3, 1, tzinfo=timezone.utc)
    end = datetime(2026, 3, 8, tzinfo=timezone.utc)
    params = build_catalog_params(start, end)
    assert params["format"] == "geojson"
    assert params["starttime"] == "2026-03-01"
    assert params["endtime"] == "2026-03-08"
    assert params["minmagnitude"] == 6.0


def test_fetch_catalog_uses_fdsn_params(monkeypatch):
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"type": "FeatureCollection", "features": []}

    def fake_get(url, params, timeout):
        captured["url"] = url
        captured["params"] = params
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr("src.ingest_catalog.requests.get", fake_get)
    start = datetime(2026, 3, 1, tzinfo=timezone.utc)
    end = datetime(2026, 3, 8, tzinfo=timezone.utc)
    payload = fetch_catalog(start_time=start, end_time=end, min_magnitude=6.2, limit=123)

    assert payload["type"] == "FeatureCollection"
    assert "fdsnws/event/1/query" in captured["url"]
    assert captured["params"]["format"] == "geojson"
    assert captured["params"]["minmagnitude"] == 6.2
    assert captured["params"]["limit"] == 123
