import json
import sqlite3
import tempfile
import os
import pytest

from src.normalize import normalize_feature
from src.cache import create_db, insert_raw_event
from src.score import baseline_score


def make_feature(id: str = "f1", mag=1.0, coords=None, extra_props=None):
    if coords is None:
        coords = [-122.0, 37.0, 10.0]
    props = {"mag": mag, "place": "test place"}
    if extra_props:
        props.update(extra_props)
    return {
        "type": "Feature",
        "id": id,
        "properties": props,
        "geometry": {"type": "Point", "coordinates": coords},
    }


def test_normalize_missing_coords_and_values():
    # coords missing -> lat/lon/depth should be None
    f = make_feature(id="no_coords", coords=[])
    evt = normalize_feature(f)
    assert evt.lat is None and evt.lon is None and evt.depth is None


def test_normalize_missing_id_raises():
    f = make_feature(id=None)
    # remove id key entirely to simulate broken payload
    del f["id"]
    with pytest.raises(Exception):
        normalize_feature(f)


def test_cache_upsert_updates_row():
    with tempfile.TemporaryDirectory() as td:
        db_path = os.path.join(td, "events.sqlite")
        create_db(db_path)
        conn = sqlite3.connect(db_path)

        f1 = make_feature(id="dup1", mag=2.0)
        evt1 = normalize_feature(f1)
        insert_raw_event(
            conn,
            evt1.id,
            json.dumps(f1),
            time=evt1.time,
            updated=evt1.updated,
            mag=evt1.mag,
            depth=evt1.depth,
            lat=evt1.lat,
            lon=evt1.lon,
            place=evt1.place,
            urls=json.dumps(evt1.urls) if evt1.urls else None,
            tsunami=evt1.tsunami,
        )

        # upsert same id with different mag
        f2 = make_feature(id="dup1", mag=4.5)
        evt2 = normalize_feature(f2)
        insert_raw_event(
            conn,
            evt2.id,
            json.dumps(f2),
            time=evt2.time,
            updated=evt2.updated,
            mag=evt2.mag,
            depth=evt2.depth,
            lat=evt2.lat,
            lon=evt2.lon,
            place=evt2.place,
            urls=json.dumps(evt2.urls) if evt2.urls else None,
            tsunami=evt2.tsunami,
        )

        cur = conn.cursor()
        cur.execute("SELECT COUNT(*), mag FROM events WHERE id = ?", ("dup1",))
        row = cur.fetchone()
        assert row[0] == 1
        assert pytest.approx(row[1], rel=1e-3) == 4.5
        conn.close()


def test_score_edgecases_missing_time_and_extremes():
    record = {"mag": 0.0, "depth": 500.0}
    res = baseline_score(record)
    assert "score" in res and "factors" in res and "explanation" in res
    assert 0.0 <= res["score"] <= 100.0
    # recency factor should drop to zero when there is no timestamp.
    assert res["factors"]["recency_factor"] == 0.0


def test_score_magnitude_weight_rises_above_m6():
    base = {"depth": 10.0, "time": 0, "updated": 0}
    s59 = baseline_score({**base, "mag": 5.9})
    s65 = baseline_score({**base, "mag": 6.5})
    assert s65["factors"]["magnitude_factor"] > s59["factors"]["magnitude_factor"]
    assert s65["factors"]["magnitude_factor"] - s59["factors"]["magnitude_factor"] >= 4.0


def test_score_factor_caps():
    # Extreme event should still respect 50/30/20 caps and total <= 100.
    res = baseline_score({"mag": 9.9, "depth": 0.0, "time": 9999999999999, "updated": 9999999999999})
    assert res["factors"]["magnitude_factor"] <= 50.0
    assert res["factors"]["depth_factor"] <= 30.0
    assert res["factors"]["recency_factor"] <= 20.0
    assert 0.0 <= res["score"] <= 100.0
