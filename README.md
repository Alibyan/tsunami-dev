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

3. Run the Streamlit scaffold app:

```bash
streamlit run src/app.py
```
