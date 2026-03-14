"""Optional marine enrichment via Open-Meteo Marine API (no API key required).

Fetches current wave conditions at a given lat/lon. Returns None on any failure
so callers never need to guard against exceptions — the enrichment is purely
optional and must not affect the core ranking pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"
_TIMEOUT = 8  # seconds — short so a slow network doesn't stall the UI


@dataclass
class MarineConditions:
    wave_height_m: float | None
    wave_period_s: float | None
    wave_direction_deg: float | None

    def summary(self) -> str:
        """Human-readable one-liner for display in the Streamlit detail panel."""
        parts = []
        if self.wave_height_m is not None:
            parts.append(f"Wave height: {self.wave_height_m:.1f} m")
        if self.wave_period_s is not None:
            parts.append(f"Period: {self.wave_period_s:.0f} s")
        if self.wave_direction_deg is not None:
            parts.append(f"Direction: {self.wave_direction_deg:.0f}°")
        return "  |  ".join(parts) if parts else "No wave data available."


def fetch_marine_conditions(
    lat: float,
    lon: float,
    url: str = MARINE_URL,
) -> MarineConditions | None:
    """Return current marine conditions at *lat/lon*, or None on any error.

    This function is intentionally silent on failure — network errors, out-of-
    bounds coordinates (land points), or API changes all return None so the app
    degrades gracefully.
    """
    try:
        response = requests.get(
            url,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "wave_height,wave_period,wave_direction",
            },
            timeout=_TIMEOUT,
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        current = data.get("current") or {}
        return MarineConditions(
            wave_height_m=current.get("wave_height"),
            wave_period_s=current.get("wave_period"),
            wave_direction_deg=current.get("wave_direction"),
        )
    except Exception:
        return None
