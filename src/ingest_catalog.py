"""Historical backfill using USGS FDSN Event Web Service (catalog API)."""

import argparse
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

from src.run_ingest_pipeline import store_payload


CATALOG_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


def _iso_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def build_catalog_params(
    start_time: datetime,
    end_time: datetime,
    min_magnitude: float = 6.0,
    limit: int = 20000,
) -> dict[str, Any]:
    return {
        "format": "geojson",
        "starttime": _iso_date(start_time),
        "endtime": _iso_date(end_time),
        "minmagnitude": min_magnitude,
        "orderby": "time-asc",
        "limit": limit,
    }


def fetch_catalog(
    start_time: datetime,
    end_time: datetime,
    min_magnitude: float = 6.0,
    limit: int = 20000,
    url: str = CATALOG_URL,
) -> dict[str, Any]:
    params = build_catalog_params(
        start_time=start_time,
        end_time=end_time,
        min_magnitude=min_magnitude,
        limit=limit,
    )
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def backfill_last_days(
    days: int = 7,
    min_magnitude: float = 6.0,
    db_path: str = "data/events.sqlite",
    limit: int = 20000,
) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=days)

    payload = fetch_catalog(
        start_time=start,
        end_time=now,
        min_magnitude=min_magnitude,
        limit=limit,
    )
    stored = store_payload(payload, db_path=db_path)
    result = {
        "stored": stored,
        "db_path": db_path,
        "days": days,
        "min_magnitude": min_magnitude,
    }
    print(
        "Stored "
        f"{stored} catalog events to {db_path} "
        f"(window={days}d, min_magnitude={min_magnitude})"
    )
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="USGS catalog backfill")
    parser.add_argument("--days", type=int, default=7, help="Historical window in days")
    parser.add_argument(
        "--min-magnitude",
        type=float,
        default=6.0,
        help="Minimum magnitude to request",
    )
    parser.add_argument("--db-path", default="data/events.sqlite", help="SQLite path")
    parser.add_argument("--limit", type=int, default=20000, help="Catalog limit")
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    backfill_last_days(
        days=args.days,
        min_magnitude=args.min_magnitude,
        db_path=args.db_path,
        limit=args.limit,
    )
