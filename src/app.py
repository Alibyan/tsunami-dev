"""Streamlit app: ranked scored events from local SQLite cache."""

from datetime import datetime, timezone
import json
import os
from statistics import fmean
import time
from typing import Any
from zoneinfo import ZoneInfo

import streamlit as st
import pydeck as pdk

from src.cache import create_db, fetch_recent_events
from src.enrich_marine import fetch_marine_conditions
from src.run_ingest_pipeline import run as run_ingest
from src.score import baseline_score


def _to_iso(ms: int | None) -> str:
    if not ms:
        return "unknown"
    try:
        return datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc).strftime(
            "%d %b %Y  %I:%M %p UTC"
        )
    except Exception:
        return "unknown"


TIMEZONE_OPTIONS = [
    "UTC",
    "America/Los_Angeles",
    "America/Denver",
    "America/Chicago",
    "America/New_York",
    "Europe/London",
    "Europe/Paris",
    "Asia/Tokyo",
    "Australia/Sydney",
]


def _resolve_timezone(tz_name: str):
    try:
        return ZoneInfo(tz_name)
    except Exception:
        return timezone.utc


def _to_display_time(ms: int | None, tz_name: str = "UTC") -> str:
    if not ms:
        return "unknown"
    try:
        tz_obj = _resolve_timezone(tz_name)
        dt = datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc).astimezone(tz_obj)
        tz_label = dt.tzname() or tz_name
        return dt.strftime("%d %b %Y  %I:%M %p ") + tz_label
    except Exception:
        return "unknown"


def _score_records(records: list[dict], display_tz: str = "UTC") -> list[dict]:
    scored = []
    for r in records:
        result = baseline_score(r)
        row = dict(r)
        row["score"] = result["score"]
        row["explanation"] = result.get("explanation")
        row["factors"] = result["factors"]
        row["time_iso"] = _to_display_time(row.get("time"), tz_name=display_tz)
        scored.append(row)
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


st.set_page_config(page_title="Offshore Quake Triage", layout="wide")

TSUNAMI_GOV_URL = "https://www.tsunami.gov/"
METRICS_ARTIFACT_PATH = "artifacts/metrics_latest.json"


def _nws_alert_definitions_markdown() -> str:
    return "\n".join(
        [
            "**Warning**: Inundating wave possible or already occurring; urgent protective action needed.",
            "**Advisory**: Strong currents and dangerous waves possible; stay out of water and away from coasts.",
            "**Watch**: Potential hazard under evaluation; stay alert and prepare to act.",
            "**Information Statement**: No major threat expected, issued for situational awareness.",
        ]
    )


def _score_color(score: float) -> list[int]:
    """Map score bands to RGB colors for visual triage at a glance."""
    if score >= 75:
        return [220, 53, 69]  # red
    if score >= 45:
        return [255, 193, 7]  # amber
    return [40, 167, 69]  # green


def _load_metrics_artifact(path: str = METRICS_ARTIFACT_PATH) -> dict | None:
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


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
        max_rows_raw = st.text_input("Max events", value="100")
        st.caption("Min: 10   Max: 500")
        try:
            max_rows = int(max_rows_raw)
        except Exception:
            max_rows = 100
            st.warning("Max events must be a whole number. Using default 100.")
        max_rows = max(10, min(500, max_rows))

        min_magnitude_raw = st.text_input("Minimum magnitude (Mw)", value="0.0")
        st.caption("Min: 0.0   Max: 10.0")
        try:
            min_magnitude = float(min_magnitude_raw)
        except Exception:
            min_magnitude = 0.0
            st.warning("Minimum magnitude must be numeric. Using default 0.0.")
        min_magnitude = max(0.0, min(10.0, min_magnitude))
        display_tz = st.selectbox(
            "Display timezone",
            options=TIMEZONE_OPTIONS,
            index=0,
            help="Controls how event and refresh timestamps are shown in the UI.",
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
        st.subheader("Auto Refresh")
        auto_refresh_enabled = st.toggle(
            "Auto-ingest new events",
            value=False,
            help="Periodically fetches the USGS feed and updates the local cache.",
        )
        refresh_interval_sec = st.selectbox(
            "Refresh interval",
            options=[15, 30, 60, 120],
            index=1,
            format_func=lambda s: f"{s} seconds",
            disabled=not auto_refresh_enabled,
        )
        st.caption(
            "Recommended: 60s for normal use, 30s for live demos, 15s only for short single-user testing."
        )

        last_auto_iso = st.session_state.get("last_auto_ingest_iso")
        if last_auto_iso:
            st.caption(f"Last auto refresh: {last_auto_iso}")
        last_auto_source = st.session_state.get("last_auto_ingest_source")
        if last_auto_source:
            st.caption(f"Last auto source: {last_auto_source}")
        last_auto_error = st.session_state.get("last_auto_ingest_error")
        if last_auto_error:
            st.warning(f"Last auto refresh failed: {last_auto_error}")

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

    if auto_refresh_enabled:

        @st.fragment(run_every=f"{refresh_interval_sec}s")
        def _auto_refresh_tick() -> None:
            # Guardrail: avoid back-to-back ingest calls if reruns happen rapidly.
            now_ts = time.time()
            last_ts = float(st.session_state.get("last_auto_ingest_ts", 0.0))
            if now_ts - last_ts < refresh_interval_sec:
                return

            try:
                result = run_ingest(
                    db_path=db_path,
                    replay_mode=replay_mode,
                    sample_path=sample_path,
                    fallback_on_error=True,
                )
                st.session_state["last_auto_ingest_source"] = result.get("source")
                st.session_state["last_auto_ingest_error"] = ""
            except Exception as exc:
                st.session_state["last_auto_ingest_error"] = str(exc)
            finally:
                st.session_state["last_auto_ingest_ts"] = now_ts
                st.session_state["last_auto_ingest_iso"] = _to_display_time(
                    int(now_ts * 1000), tz_name=display_tz
                )

            st.rerun()

        _auto_refresh_tick()

    records = fetch_recent_events(path=db_path, limit=max_rows)
    scored = [
        r
        for r in _score_records(records, display_tz=display_tz)
        if float(r.get("mag") or 0.0) >= min_magnitude
    ]

    if not scored:
        st.warning("No events found in cache yet.")
        st.code("python -m src.run_ingest_pipeline --replay")
        st.stop()

    # --- Map: global picture first ---
    map_points = [
        {
            "lat": r.get("lat"),
            "lon": r.get("lon"),
            "score": r.get("score"),
            "color": _score_color(float(r.get("score", 0.0))),
            "radius": 12000 + int(float(r.get("score", 0.0)) * 180),
            "id": r.get("id"),
            "place": r.get("place", ""),
        }
        for r in scored
        if r.get("lat") is not None and r.get("lon") is not None
    ]
    if map_points:
        st.subheader("Global Event Map")
        st.caption(
            "Red \u2265 75 (high priority) \u00b7 Amber 45\u201374 (medium) \u00b7 Green < 45 (lower). "
            "Hover for event ID and score."
        )
        view_state = pdk.ViewState(
            latitude=fmean([p["lat"] for p in map_points]),
            longitude=fmean([p["lon"] for p in map_points]),
            zoom=2.5,
            pitch=25,
        )
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_points,
            get_position="[lon, lat]",
            get_fill_color="color",
            get_radius="radius",
            pickable=True,
            auto_highlight=True,
        )
        tooltip: Any = {
            "html": "<b>{place}</b><br/>Score: <b>{score}</b><br/><small>{id}</small>",
            "style": {"backgroundColor": "#111", "color": "#fff"},
        }
        st.pydeck_chart(
            pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
        )

    st.divider()

    # --- Ranked queue (full width) + event detail ---
    st.subheader("Ranked Queue")
    if "time_sort_desc" not in st.session_state:
        st.session_state["time_sort_desc"] = True

    sort_left, sort_right = st.columns([1, 5])
    with sort_left:
        if st.button("time", help="Toggle time ordering"):
            st.session_state["time_sort_desc"] = not st.session_state["time_sort_desc"]

    sort_desc = bool(st.session_state["time_sort_desc"])
    queue_events = list(scored)
    queue_events.sort(
        key=lambda r: (r.get("time") if r.get("time") is not None else r.get("updated") or 0),
        reverse=sort_desc,
    )

    with sort_right:
        st.caption(
            f"{len(queue_events)} events · "
            f"{'newest to oldest' if sort_desc else 'oldest to newest'}"
        )
    st.caption(
        "Tip: click a row in the table to auto-select that event in Event Detail."
    )
    st.caption(f"Times shown in {display_tz}")

    rows = [
        {
            "score": r["score"],
            "place": r.get("place"),
            "Mw": r.get("mag"),
            "depth (km)": r.get("depth"),
            "tsunami": r.get("tsunami"),
            "time": r.get("time_iso"),
            "id": r["id"],
        }
        for r in queue_events
    ]
    queue_selection = st.dataframe(
        rows,
        hide_index=True,
        width="stretch",
        on_select="rerun",
        selection_mode="single-row",
        key="ranked_queue_table",
    )

    selected_rows = queue_selection.get("selection", {}).get("rows", [])
    if selected_rows:
        selected_idx = selected_rows[0]
        if 0 <= selected_idx < len(rows):
            st.session_state["selected_event_id"] = rows[selected_idx]["id"]

    st.subheader("Event Detail")
    event_ids = [r["id"] for r in queue_events]
    current_selected_id = st.session_state.get("selected_event_id", event_ids[0])
    if current_selected_id not in event_ids:
        current_selected_id = event_ids[0]

    selected_id = st.selectbox(
        "Select event",
        options=event_ids,
        index=event_ids.index(current_selected_id),
    )
    st.session_state["selected_event_id"] = selected_id
    selected = next(r for r in queue_events if r["id"] == selected_id)

    c1, c2, c3 = st.columns(3)
    c1.metric("Score", selected["score"])
    c2.metric("Mw", selected.get("mag"))
    c3.metric("Depth (km)", selected.get("depth"))

    st.markdown(f"**Place:** {selected.get('place') or 'unknown'}")
    st.markdown(f"**Time ({display_tz}):** {selected.get('time_iso') or 'unknown'}")
    st.markdown(f"**Why this score:** {selected.get('explanation') or '—'}")

    if selected.get("lat") and selected.get("lon"):
        with st.spinner("Fetching marine conditions\u2026"):
            conditions = fetch_marine_conditions(
                lat=selected["lat"], lon=selected["lon"]
            )
        if conditions is not None:
            st.info(f"\U0001f30a Marine context: {conditions.summary()}")
        else:
            st.caption("Marine data unavailable for this location.")

    st.markdown(f"**Official alerts:** [{TSUNAMI_GOV_URL}]({TSUNAMI_GOV_URL})")


if __name__ == "__main__":
    main()
