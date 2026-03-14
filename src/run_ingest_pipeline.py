"""End-to-end ingest pipeline: fetch USGS summary, normalize, and store in SQLite."""
import json
import sqlite3
from typing import Optional

from src.ingest_usgs import fetch_summary
from src.normalize import normalize_feature
from src.cache import create_db, insert_raw_event


def run(url: Optional[str] = None, db_path: str = "data/events.sqlite") -> None:
    data = fetch_summary(url) if url else fetch_summary()
    features = data.get("features", [])
    create_db(db_path)
    conn = sqlite3.connect(db_path)
    stored = 0
    for f in features:
        try:
            evt = normalize_feature(f)
        except Exception as e:
            print(f"Skipping feature due to normalize error: {e}")
            continue
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
    conn.close()
    print(f"Stored {stored} events to {db_path}")


if __name__ == "__main__":
    run()
