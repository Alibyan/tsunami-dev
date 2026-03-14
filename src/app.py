"""Streamlit app: ranked scored events from local SQLite cache."""

from datetime import datetime, timezone

import streamlit as st

from src.cache import create_db, fetch_recent_events
from src.run_ingest_pipeline import run as run_ingest
from src.score import baseline_score


def _to_iso(ms: int | None) -> str:
    if not ms:
        return "unknown"
    try:
        return datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc).isoformat()
    except Exception:
        return "unknown"


def _score_records(records: list[dict]) -> list[dict]:
    scored = []
    for r in records:
        result = baseline_score(r)
        row = dict(r)
        row["score"] = result["score"]
        row["explanation"] = result.get("explanation")
        row["factors"] = result["factors"]
        row["time_iso"] = _to_iso(row.get("time"))
        scored.append(row)
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


st.set_page_config(page_title="Offshore Quake Triage", layout="wide")

TSUNAMI_GOV_URL = "https://www.tsunami.gov/"


def _nws_alert_definitions_markdown() -> str:
    return "\n".join(
        [
            "**Warning**: Inundating wave possible or already occurring; urgent protective action needed.",
            "**Advisory**: Strong currents and dangerous waves possible; stay out of water and away from coasts.",
            "**Watch**: Potential hazard under evaluation; stay alert and prepare to act.",
            "**Information Statement**: No major threat expected, issued for situational awareness.",
        ]
    )


def main() -> None:
    st.title("Offshore Quake & Tsunami Triage")
    st.caption(
        "Priority ranking for human review. Official alerts remain authoritative."
    )

    with st.sidebar:
        st.header("Controls")
        db_path = st.text_input("SQLite path", value="data/events.sqlite")
        replay_mode = st.toggle("Replay mode (local sample)", value=False)
        sample_path = st.text_input(
            "Replay sample path", value="data/sample_all_hour.geojson"
        )
        max_rows = st.slider(
            "Max events", min_value=10, max_value=500, value=100, step=10
        )
        min_score = st.slider(
            "Minimum score",
            min_value=-1000.0,
            max_value=20.0,
            value=-1000.0,
            step=0.5,
        )
        if st.button("Ensure local DB"):
            path = create_db(db_path)
            st.success(f"Created SQLite DB at {path}")

        if st.button("Load events now"):
            try:
                result = run_ingest(
                    db_path=db_path,
                    replay_mode=replay_mode,
                    sample_path=sample_path,
                    fallback_on_error=True,
                )
                st.success(
                    f"Loaded {result['stored']} events (source={result['source']})"
                )
            except Exception as exc:
                st.error(f"Load failed: {exc}")

        st.divider()
        st.subheader("Mode")
        st.info("Replay mode active" if replay_mode else "Live mode with fallback")

        with st.expander("Demo Operator Checklist", expanded=False):
            st.markdown(
                "\n".join(
                    [
                        "- Confirm local DB path is correct.",
                        "- Click **Load events now** before presenting.",
                        "- If live fetch is unstable, enable **Replay mode**.",
                        "- Keep focus on ranked queue and factor explanation.",
                        "- Reminder: this is triage support, not an official warning system.",
                    ]
                )
            )

        with st.expander("NWS Alert Definitions", expanded=False):
            st.markdown(_nws_alert_definitions_markdown())
            st.markdown(
                f"**Official alerts live here:** [{TSUNAMI_GOV_URL}]({TSUNAMI_GOV_URL})"
            )

    records = fetch_recent_events(path=db_path, limit=max_rows)
    scored = [r for r in _score_records(records) if r["score"] >= min_score]

    if not scored:
        st.warning("No events found in cache yet.")
        st.code("python -m src.run_ingest_pipeline --replay")
        st.stop()

    left, right = st.columns([2, 1])
    with left:
        st.subheader("Ranked Queue")
        rows = [
            {
                "id": r["id"],
                "score": r["score"],
                "explanation": r.get("explanation"),
                "mag": r.get("mag"),
                "depth": r.get("depth"),
                "tsunami": r.get("tsunami"),
                "time": r.get("time_iso"),
                "place": r.get("place"),
            }
            for r in scored
        ]
        st.dataframe(rows, width="stretch", hide_index=True)

    with right:
        st.subheader("Summary")
        st.metric("Events shown", len(scored))
        st.metric("Top score", scored[0]["score"])

    st.subheader("Event Detail")
    selected_id = st.selectbox("Select event", options=[r["id"] for r in scored])
    selected = next(r for r in scored if r["id"] == selected_id)

    st.write(
        {
            "id": selected["id"],
            "place": selected.get("place"),
            "score": selected["score"],
            "explanation": selected.get("explanation"),
            "time": selected.get("time_iso"),
            "factors": selected["factors"],
        }
    )
    st.markdown(
        f"### Official alerts live here: [{TSUNAMI_GOV_URL}]({TSUNAMI_GOV_URL})"
    )

    st.subheader("Top Event Cards")
    for event in scored[:5]:
        with st.container(border=True):
            st.markdown(
                f"**{event.get('id', 'unknown')}** | score: **{event.get('score')}**"
            )
            st.markdown(event.get("place") or "Unknown location")
            st.markdown(event.get("explanation") or "No explanation available.")
            st.markdown(
                f"**Official alerts live here:** [{TSUNAMI_GOV_URL}]({TSUNAMI_GOV_URL})"
            )

    map_points = [
        {"lat": r.get("lat"), "lon": r.get("lon")}
        for r in scored
        if r.get("lat") is not None and r.get("lon") is not None
    ]
    if map_points:
        st.subheader("Map")
        st.map(map_points)


if __name__ == "__main__":
    main()
