"""SQLite cache helpers for Phase 00."""

import os
import sqlite3
from typing import Any


def create_db(path: str = "data/events.sqlite") -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        time INTEGER,
        updated INTEGER,
        mag REAL,
        depth REAL,
        lat REAL,
        lon REAL,
        place TEXT,
        urls TEXT,
        tsunami INTEGER,
        raw_json TEXT
    )
    """
    )
    conn.commit()
    conn.close()
    return path


def insert_raw_event(
    conn: sqlite3.Connection, evt_id: str, raw_json: str, **fields
) -> None:
    cur = conn.cursor()
    cur.execute(
        """
    INSERT OR REPLACE INTO events (id, time, updated, mag, depth, lat, lon, place, urls, tsunami, raw_json)
    VALUES (:id, :time, :updated, :mag, :depth, :lat, :lon, :place, :urls, :tsunami, :raw_json)
    """,
        {
            "id": evt_id,
            "time": fields.get("time"),
            "updated": fields.get("updated"),
            "mag": fields.get("mag"),
            "depth": fields.get("depth"),
            "lat": fields.get("lat"),
            "lon": fields.get("lon"),
            "place": fields.get("place"),
            "urls": fields.get("urls"),
            "tsunami": fields.get("tsunami", 0),
            "raw_json": raw_json,
        },
    )
    conn.commit()


def fetch_recent_events(
    path: str = "data/events.sqlite", limit: int = 200
) -> list[dict[str, Any]]:
    """Return latest cached events for UI and scoring flows."""
    if not os.path.exists(path):
        return []

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, time, updated, mag, depth, lat, lon, place, urls, tsunami
        FROM events
        ORDER BY time DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
