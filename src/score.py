"""Baseline scoring utilities (explainable triage)."""

from datetime import datetime, timezone


def baseline_score(record: dict) -> dict:
    """Compute a simple explainable score using mag, depth, and recency.

    Returns a dict with `score` and `factors` for UI display.
    """
    mag = record.get("mag") or 0.0
    depth = record.get("depth") if record.get("depth") is not None else 100.0
    time = record.get("time") or 0
    now_ms = datetime.now(timezone.utc).timestamp() * 1000
    recency_hours = max(0.0, (now_ms - time) / 3600000) if time else 9999.0

    # Simple linear combination tuned for explainability
    score = mag * 2.0 + max(0.0, (100.0 - depth) / 100.0) - recency_hours * 0.1
    return {
        "score": round(score, 3),
        "factors": {
            "mag": mag,
            "depth": depth,
            "recency_hours": round(recency_hours, 2),
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
