import os

from src.cache import fetch_recent_events
from src.run_ingest_pipeline import run


def test_replay_mode_loads_sample(tmp_path):
    db_path = str(tmp_path / "events.sqlite")
    result = run(
        db_path=db_path,
        replay_mode=True,
        sample_path="data/sample_all_hour.geojson",
    )
    assert result["source"] == "replay"
    assert result["stored"] > 0
    rows = fetch_recent_events(path=db_path, limit=10)
    assert len(rows) > 0


def test_live_failure_fallbacks_to_sample(monkeypatch, tmp_path):
    db_path = str(tmp_path / "events.sqlite")

    def _boom(*args, **kwargs):
        raise RuntimeError("network down")

    monkeypatch.setattr("src.run_ingest_pipeline.fetch_summary", _boom)
    result = run(
        db_path=db_path,
        replay_mode=False,
        sample_path="data/sample_all_hour.geojson",
        fallback_on_error=True,
    )
    assert result["source"] == "fallback"
    assert result["stored"] > 0


def test_fetch_recent_events_missing_db_is_safe(tmp_path):
    missing = str(tmp_path / "missing.sqlite")
    assert not os.path.exists(missing)
    rows = fetch_recent_events(path=missing, limit=5)
    assert rows == []
