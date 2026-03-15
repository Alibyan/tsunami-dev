"""SQLite cache helpers for Phase 00."""

from datetime import datetime, timezone
import os
import sqlite3
from typing import Any


def _ensure_ingested_at_column(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(events)")
    column_names = {row[1] for row in cur.fetchall()}
    if "ingested_at_utc" not in column_names:
        cur.execute("ALTER TABLE events ADD COLUMN ingested_at_utc TEXT")
        cur.execute(
            "UPDATE events SET ingested_at_utc = CURRENT_TIMESTAMP WHERE ingested_at_utc IS NULL"
        )


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
        ingested_at_utc TEXT DEFAULT CURRENT_TIMESTAMP,
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
    _ensure_ingested_at_column(conn)
    conn.commit()
    conn.close()
    return path


def insert_raw_event(
    conn: sqlite3.Connection, evt_id: str, raw_json: str, **fields
) -> None:
    cur = conn.cursor()
    cur.execute(
        """
    INSERT OR REPLACE INTO events (
        id, time, updated, ingested_at_utc, mag, depth, lat, lon, place, urls, tsunami, raw_json
    )
    VALUES (
        :id, :time, :updated, :ingested_at_utc, :mag, :depth, :lat, :lon, :place, :urls, :tsunami, :raw_json
    )
    """,
        {
            "id": evt_id,
            "time": fields.get("time"),
            "updated": fields.get("updated"),
            "ingested_at_utc": datetime.now(timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            ),
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
