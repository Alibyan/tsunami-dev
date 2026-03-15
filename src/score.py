"""Baseline scoring utilities (explainable triage)."""

from datetime import datetime, timezone


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


# Mw scoring range: Mw 4.0 -> 0 pts, Mw 9.0 -> 50 pts (linear in Mw).
# Linear-in-Mw is the physically correct choice: Mw is already a base-10 log
# scale of seismic moment, so each unit represents ~32x more energy. A uniform
# mapping honours that scale without introducing artificial kinks.
_MW_MIN = 4.0
_MW_MAX = 9.0


def _magnitude_factor(mag: float) -> float:
    """Moment Magnitude (Mw) contribution in range 0-50.

    Uses the Mw value reported by USGS. Linear mapping over Mw 4.0-9.0 is
    appropriate because Mw is itself logarithmic — equal steps in Mw represent
    equal multiplicative steps in seismic moment (~32x energy per unit).
    """
    if mag <= 0:
        return 0.0
    return _clamp(50.0 * (mag - _MW_MIN) / (_MW_MAX - _MW_MIN), 0.0, 50.0)


def _depth_factor(depth_km: float | None) -> float:
    """Depth contribution in range 0-30, prioritizing shallow events."""
    if depth_km is None:
        # Conservative midpoint when depth is missing.
        return 15.0
    # 0 km -> 30 points, 300 km+ -> 0 points.
    return _clamp(30.0 * (1.0 - (depth_km / 300.0)), 0.0, 30.0)


def _recency_factor(time_ms: int | None, updated_ms: int | None) -> tuple[float, float]:
    """Recency contribution in range 0-20 using event/updated timestamps."""
    ref_ms = max(time_ms or 0, updated_ms or 0)
    if ref_ms <= 0:
        return 0.0, 9999.0

    now_ms = datetime.now(timezone.utc).timestamp() * 1000
    age_hours = max(0.0, (now_ms - ref_ms) / 3600000.0)
    # 0h -> 20 points, 48h+ -> 0 points.
    recency = _clamp(20.0 * (1.0 - (age_hours / 48.0)), 0.0, 20.0)
    return recency, age_hours


def _priority_label(total_score: float) -> str:
    if total_score >= 75:
        return "High"
    if total_score >= 45:
        return "Medium"
    return "Lower"


def _explanation_text(
    mag: float, depth: float | None, age_hours: float, total_score: float
) -> str:
    level = _priority_label(total_score)

    if mag >= 7.0:
        mag_phrase = f"a significant Mw{mag:.1f}"
    elif mag >= 6.0:
        mag_phrase = f"an elevated Mw{mag:.1f}"
    else:
        mag_phrase = f"a moderate Mw{mag:.1f}"

    if depth is None:
        depth_phrase = "an unknown depth"
    elif depth <= 30:
        depth_phrase = f"a very shallow depth of {depth:.1f} km"
    elif depth <= 70:
        depth_phrase = f"a shallow depth of {depth:.1f} km"
    else:
        depth_phrase = f"a deeper depth of {depth:.1f} km"

    if age_hours <= 6:
        recency_phrase = "a very recent update"
    elif age_hours <= 24:
        recency_phrase = "a recent update"
    else:
        recency_phrase = "an older update"

    return (
        f"{level} priority due to {mag_phrase}, {depth_phrase}, "
        f"and {recency_phrase}."
    )


def baseline_score(record: dict) -> dict:
    """Compute an explainable 0-100 triage score.

    Factor weights:
    - Magnitude: 0-50
    - Depth: 0-30
    - Recency: 0-20

    Returns a dict with `score`, factor breakdown, and explanation text.
    """
    mag = record.get("mag") or 0.0
    depth = record.get("depth")
    time_ms = record.get("time")
    updated_ms = record.get("updated")

    magnitude_factor = _magnitude_factor(float(mag))
    depth_factor = _depth_factor(depth)
    recency_factor, age_hours = _recency_factor(time_ms, updated_ms)

    score = _clamp(magnitude_factor + depth_factor + recency_factor, 0.0, 100.0)
    explanation = _explanation_text(float(mag), depth, age_hours, score)

    return {
        "score": round(score, 2),
        "explanation": explanation,
        "factors": {
            "magnitude_factor": round(magnitude_factor, 2),
            "depth_factor": round(depth_factor, 2),
            "recency_factor": round(recency_factor, 2),
            "mag": mag,
            "depth": depth,
            "age_hours": round(age_hours, 2),
        },
    }


if __name__ == "__main__":
    # quick self-check
    sample = {
        "mag": 5.2,
        "depth": 10.0,
        "time": int(datetime.now(timezone.utc).timestamp() * 1000),
    }
    print(baseline_score(sample))
