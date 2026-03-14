# Offshore Quake & Tsunami Triage (scaffold)

Phase 00 scaffold: minimal repo layout and starter scripts.

Quick start

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Fetch a USGS summary feed (quick test):

```bash
python -m src.ingest_usgs
```

3. Run ingest pipeline with reliability modes:

```bash
# Live fetch with automatic fallback to local sample on failure
python -m src.run_ingest_pipeline

# Forced replay mode (no network needed)
python -m src.run_ingest_pipeline --replay

# Historical backfill (last 7 days, M6.0+ from USGS catalog API)
python -m src.ingest_catalog --days 7 --min-magnitude 6.0

# Phase 6: evaluate lightweight classifier using cached historical data
python -m src.ml_evaluate --db-path data/events.sqlite
```

4. Run the Streamlit app:

```bash
streamlit run src/app.py
```
