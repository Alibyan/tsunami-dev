import json
import sqlite3
import tempfile
import os

from src.normalize import normalize_feature
from src.cache import create_db, insert_raw_event
from src.score import baseline_score


def test_pipeline_smoke():
    sample_path = os.path.join("data", "sample_all_hour.geojson")
    with open(sample_path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)

    features = payload.get("features", [])
    assert len(features) > 0, "Sample payload must contain at least one feature"

    with tempfile.TemporaryDirectory() as td:
        db_path = os.path.join(td, "events.sqlite")
        # create DB and write normalized features
        create_db(db_path)
        conn = sqlite3.connect(db_path)
        stored = 0
        for f in features:
            evt = normalize_feature(f)
            insert_raw_event(
                conn,
                evt.id,
                json.dumps(f),
                time=evt.time,
                updated=evt.updated,
                mag=evt.mag,
                depth=evt.depth,
                lat=evt.lat,
                lon=evt.lon,
                place=evt.place,
                urls=json.dumps(evt.urls) if evt.urls else None,
                tsunami=evt.tsunami,
            )
            stored += 1

        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM events")
        count = cur.fetchone()[0]
        assert count == stored

        # fetch one row and verify raw_json roundtrip
        cur.execute("SELECT id, raw_json FROM events LIMIT 1")
        row = cur.fetchone()
        assert row is not None
        row_id, raw = row
        raw_obj = json.loads(raw)
        assert raw_obj.get("id") == row_id

        # test scoring function on the first normalized record
        first_evt = normalize_feature(features[0])
        res = baseline_score(first_evt.model_dump())
        assert "score" in res and "factors" in res and "explanation" in res

        conn.close()
