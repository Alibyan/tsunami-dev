# QA_RUN_RECORD

## Run metadata

- Run timestamp (UTC): `2026-03-15 14:19:08 UTC`
- Branch: `master`
- Commit: `c1be7bf`
- Operator: `GitHub Copilot`
- Mode tested: `Live + Replay`

## Automated test evidence

- Command: `pytest -q`
- Result: `22 passed, 1 warning`
- Warning noted:
  - `src/normalize.py:19` pydantic v1 `@validator` deprecation warning (non-blocking)

## Pre-demo checklist results

### Startup and ingest

- [x] App launches locally (`streamlit run src/app.py`)
- [x] DB path is valid (`data/events.sqlite`)
- [x] Live ingest command path works (`python -m src.ingest_usgs`)
- [x] Replay pipeline path works (`python -m src.run_ingest_pipeline --replay`)

### UI and interaction

- [x] Ranked queue renders
- [x] Event detail panel renders
- [x] Map renders with color-coded markers
- [x] Official alerts link visible

### Reliability and fallback

- [x] Replay mode path exists and is documented
- [x] Fallback behavior exists in ingest pipeline
- [x] Core UI remains usable without optional enrichment

### Safety and wording

- [x] UI uses triage framing
- [x] UI states official alerts are authoritative
- [x] No deterministic tsunami-prediction claims in operator path

### Remaining checklist item

- [x] Backup screenshot exists in `artifacts/demo_screenshots/`

## Issues found

- No blocking issues found during this run.
- One non-blocking deprecation warning remains (`pydantic` validator style migration).

## Go/No-Go decision

- Decision: `GO (Demo-ready)`
- Conditions:
  - Keep fallback/replay mode ready during live presentation.
  - Keep optional enrichments disabled if network is unstable.

## Signoff

- QA owner: GitHub Copilot
- Date: 2026-03-15
- Notes: Live fetch, replay ingest, Streamlit startup path, and automated tests all passed on this run. Backup screenshots saved in `artifacts/demo_screenshots/01-overview-full.png`, `artifacts/demo_screenshots/02-queue-map.png`, and `artifacts/demo_screenshots/03-event-detail.png`.
