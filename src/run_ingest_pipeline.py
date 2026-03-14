"""End-to-end ingest pipeline with replay/fallback support.

Phase 5 reliability goals:
- explicit replay mode from local sample payload
- graceful fallback to local sample on live fetch failures
"""

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any, Optional

from src.ingest_usgs import fetch_summary
from src.normalize import normalize_feature
from src.cache import create_db, insert_raw_event


DEFAULT_SAMPLE_PATH = "data/sample_all_hour.geojson"


def load_local_payload(sample_path: str = DEFAULT_SAMPLE_PATH) -> dict[str, Any]:
    with open(sample_path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def store_payload(payload: dict[str, Any], db_path: str = "data/events.sqlite") -> int:
    features = payload.get("features", [])
    create_db(db_path)
    conn = sqlite3.connect(db_path)
    stored = 0
    for feature in features:
        try:
            evt = normalize_feature(feature)
        except Exception as exc:
            print(f"Skipping feature due to normalize error: {exc}")
            continue

        insert_raw_event(
            conn,
            evt.id,
            json.dumps(feature),
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
    return stored


def run(
    url: Optional[str] = None,
    db_path: str = "data/events.sqlite",
    replay_mode: bool = False,
    sample_path: str = DEFAULT_SAMPLE_PATH,
    fallback_on_error: bool = True,
) -> dict[str, Any]:
    source = "live"
    if replay_mode:
        payload = load_local_payload(sample_path)
        source = "replay"
    else:
        try:
            payload = fetch_summary(url) if url else fetch_summary()
        except Exception as exc:
            if not fallback_on_error:
                raise
            payload = load_local_payload(sample_path)
            source = "fallback"
            print(f"Live fetch failed ({exc}); using local replay payload.")

    stored = store_payload(payload, db_path=db_path)
    result = {
        "stored": stored,
        "db_path": db_path,
        "source": source,
        "sample_path": sample_path,
    }
    print(f"Stored {stored} events to {db_path} (source={source})")
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="USGS ingest with replay fallback")
    parser.add_argument("--url", default=None, help="Override live USGS feed URL")
    parser.add_argument("--db-path", default="data/events.sqlite", help="SQLite path")
    parser.add_argument(
        "--replay",
        action="store_true",
        help="Use local sample payload instead of live network fetch",
    )
    parser.add_argument(
        "--sample-path",
        default=DEFAULT_SAMPLE_PATH,
        help="Path to local sample GeoJSON for replay/fallback",
    )
    parser.add_argument(
        "--no-fallback",
        action="store_true",
        help="Disable fallback to local sample when live fetch fails",
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    if not Path(args.sample_path).exists() and (args.replay or not args.no_fallback):
        raise FileNotFoundError(
            f"Sample payload not found at {args.sample_path}. "
            "Create it or pass --sample-path to a valid file."
        )

    run(
        url=args.url,
        db_path=args.db_path,
        replay_mode=args.replay,
        sample_path=args.sample_path,
        fallback_on_error=not args.no_fallback,
    )
