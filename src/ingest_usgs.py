"""Simple USGS ingest helper (scaffold).

This is a minimal, testable entrypoint used during Phase 00 to verify
we can fetch a summary feed and parse features.
"""

import requests
from typing import Dict, Any

DEFAULT_URL = (
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
)


def fetch_summary(url: str = DEFAULT_URL) -> Dict[str, Any]:
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


def main(url: str = DEFAULT_URL):
    data = fetch_summary(url)
    features = data.get("features", [])
    print(
        f"Fetched {len(features)} features from {data.get('metadata', {}).get('url', url)}"
    )


if __name__ == "__main__":
    main()
