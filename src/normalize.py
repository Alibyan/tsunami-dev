"""Normalization and schema helpers using pydantic for Phase 00."""

from pydantic import BaseModel, validator
from typing import Optional, Dict, Any


class EventModel(BaseModel):
    id: str
    time: Optional[int]
    updated: Optional[int]
    mag: Optional[float]
    depth: Optional[float]
    lat: Optional[float]
    lon: Optional[float]
    place: Optional[str]
    urls: Optional[Dict[str, str]]
    tsunami: Optional[int] = 0

    @validator("time", "updated", pre=True)
    def to_int(cls, v):
        if v is None:
            return None
        try:
            return int(v)
        except Exception:
            raise ValueError("timestamp must be an int or parseable as int")


def normalize_feature(feature: Dict[str, Any]) -> EventModel:
    props = feature.get("properties", {})
    geom = feature.get("geometry", {})
    coords = geom.get("coordinates", [None, None, None])
    return EventModel(
        id=feature.get("id"),
        time=props.get("time"),
        updated=props.get("updated"),
        mag=props.get("mag"),
        depth=coords[2] if len(coords) > 2 else None,
        lon=coords[0] if len(coords) > 0 else None,
        lat=coords[1] if len(coords) > 1 else None,
        place=props.get("place"),
        urls={"detail": props.get("detail")} if props.get("detail") else None,
        tsunami=props.get("tsunami", 0),
    )
