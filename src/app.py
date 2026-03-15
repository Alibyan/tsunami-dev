"""Streamlit app: ranked scored events from local SQLite cache."""

from datetime import datetime, timezone
import json
import os
from statistics import fmean

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

        st.divider()
        marine_enrichment = st.toggle(
            "Show marine wave context (optional)",
            value=False,
            help="Fetches live wave height/period from Open-Meteo for the selected event. Fails silently if unavailable.",
        )

        with st.expander("Model Evaluation (Phase 6)", expanded=False):
            metrics = _load_metrics_artifact()
            if not metrics:
                st.info(
                    "No metrics artifact found yet. Run: "
                    "`python -m src.ml_evaluate --db-path data/events.sqlite`"
                )
            else:
                st.write(
                    {
                        "target_label": metrics.get("target_label"),
                        "split_mode_used": metrics.get("split_mode_used"),
                        "rows_total": metrics.get("rows_total"),
                        "train_rows": metrics.get("train_rows"),
                        "test_rows": metrics.get("test_rows"),
                        "pr_auc": metrics.get("pr_auc"),
                        "positive_rate_test": metrics.get("positive_rate_test"),
                        "note": metrics.get("note"),
                    }
                )
                p_at_k = metrics.get("precision_at_k") or {}
                if p_at_k:
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Precision@5", p_at_k.get("k5"))
                    c2.metric("Precision@10", p_at_k.get("k10"))
                    c3.metric("Precision@20", p_at_k.get("k20"))

    records = fetch_recent_events(path=db_path, limit=max_rows)
    scored = [r for r in _score_records(records) if r["score"] >= min_score]

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
        tooltip = {
            "html": "<b>{place}</b><br/>Score: <b>{score}</b><br/><small>{id}</small>",
            "style": {"backgroundColor": "#111", "color": "#fff"},
        }
        st.pydeck_chart(
            pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
        )

    st.divider()

    # --- Ranked queue (left) + event detail (right) ---
    left, right = st.columns([3, 2])
    with left:
        st.subheader("Ranked Queue")
        st.caption(f"{len(scored)} events · sorted by triage score (highest first)")
        rows = [
            {
                "score": r["score"],
                "place": r.get("place"),
                "Mw": r.get("mag"),
                "depth (km)": r.get("depth"),
                "tsunami \u26a0": r.get("tsunami"),
                "time (UTC)": r.get("time_iso"),
                "id": r["id"],
            }
            for r in scored
        ]
        st.dataframe(rows, hide_index=True, use_container_width=True)

    with right:
        st.subheader("Event Detail")
        selected_id = st.selectbox("Select event", options=[r["id"] for r in scored])
        selected = next(r for r in scored if r["id"] == selected_id)

        c1, c2, c3 = st.columns(3)
        c1.metric("Score", selected["score"])
        c2.metric("Mw", selected.get("mag"))
        c3.metric("Depth (km)", selected.get("depth"))

        st.markdown(f"**Place:** {selected.get('place') or 'unknown'}")
        st.markdown(f"**Time:** {selected.get('time_iso') or 'unknown'}")
        st.markdown(f"**Why this score:** {selected.get('explanation') or '—'}")

        if marine_enrichment and selected.get("lat") and selected.get("lon"):
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
