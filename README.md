# Offshore Quake & Tsunami Triage

A real-time seismic triage dashboard for offshore earthquake events. Fetches live data from the USGS earthquake feed, scores each event using an explainable baseline model, and presents a ranked priority queue with map visualization and optional marine context.

> **Important:** This tool provides triage support for human reviewers only. It is not an official warning system. All authoritative alerts remain at [tsunami.gov](https://www.tsunami.gov/).

---

## Architecture

```
USGS GeoJSON Feed (live)
	│
	▼
src/ingest_usgs.py          ← fetch raw feed
	│
	▼
src/normalize.py            ← validate & normalize via Pydantic
	│
	▼
src/cache.py (SQLite)       ← upsert events to local DB
	│
	├── src/score.py    ← baseline triage score (Mw + depth + recency)
	├── src/enrich_marine.py  ← optional wave context (Open-Meteo, no key)
	└── src/ml_evaluate.py   ← optional logistic regression evaluation
		│
		▼
	src/app.py (Streamlit)
	├── Global map (pydeck, color-coded by score)
	├── Ranked queue (sortable, click-to-select)
	└── Event detail (score breakdown, marine context, official link)
```

**Fallback chain:** Live feed → local sample (`data/sample_all_hour.geojson`) → empty-state message. The app always works, even with no network.

---

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Load events and launch:**

```bash
# Live fetch with automatic fallback to local sample on failure
python -m src.run_ingest_pipeline

# Launch the dashboard
streamlit run src/app.py
```

---

## All Run Commands

```bash
# Fetch a single USGS summary feed (quick test)
python -m src.ingest_usgs

# Ingest pipeline — live with fallback
python -m src.run_ingest_pipeline

# Replay mode — no network needed, uses local sample
python -m src.run_ingest_pipeline --replay

# Historical backfill — last 7 days, M6.0+ from USGS catalog API
python -m src.ingest_catalog --days 7 --min-magnitude 6.0

# Evaluate lightweight ML classifier on cached events
python -m src.ml_evaluate --db-path data/events.sqlite --output-json artifacts/metrics_latest.json

# Run tests
pytest tests/ -v

# Launch dashboard
streamlit run src/app.py
```

---

## Scoring Model

Each event receives a triage score from 0–100, computed from three factors:

| Factor | Weight | Logic |
|--------|--------|-------|
| Magnitude (Mw) | 0–50 pts | Linear scale from Mw 4.0 (0 pts) to Mw 9.0 (50 pts) |
| Depth | 0–30 pts | Shallow (<30 km) scores highest; deep (>300 km) scores lowest |
| Recency | 0–20 pts | Events within 1 hour score highest; beyond 24 hours score 0 |

Score bands: **Red ≥ 75** (high priority) · **Amber 45–74** (medium) · **Green < 45** (lower).

The score is fully explainable — every event shows a plain-English breakdown of why it received its score.

---

## Repository Layout

```
src/
  app.py                  ← Streamlit dashboard
  cache.py                ← SQLite schema and read/write
  enrich_marine.py        ← Open-Meteo marine API (optional)
  ingest_catalog.py       ← USGS catalog backfill
  ingest_usgs.py          ← USGS live feed fetch
  ml_evaluate.py          ← Logistic regression evaluation
  normalize.py            ← Pydantic event model
  run_ingest_pipeline.py  ← Orchestration with replay/fallback
  score.py                ← Baseline triage score
data/
  events.sqlite           ← Local event cache
  sample_all_hour.geojson ← Offline replay sample
artifacts/
  metrics_latest.json     ← ML evaluation output
tests/                    ← pytest suite (50+ test cases)
docs/
  agents/                 ← Agent specifications
  phases/                 ← Phase plans
  project/                ← Runbook, QA records, checklist
```

---

## Limitations

- **USGS labels are noisy:** The `tsunami` flag in the feed is set by automated systems and may contain false positives and false negatives. This is used as a training label for the optional ML model only.
- **Live API uptime:** The USGS feed and Open-Meteo marine API are third-party services. Both may be unavailable. The app falls back gracefully in all failure cases.
- **Historical coverage:** The catalog backfill is limited by the USGS FDSN API response limits. Events older than 30 days or below the magnitude threshold are not ingested.
- **Not a warning system:** Score rankings are for human triage support only. Do not use as a substitute for official alerts.
