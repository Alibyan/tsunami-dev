# QA_RUN_RECORD

## Run metadata

- Run timestamp (UTC): `2026-03-15 13:32:03 UTC`
- Branch: `master`
- Commit: `8b367eb`
- Operator: `TBD`
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
- [x] Pipeline path available (`python -m src.run_ingest_pipeline`)

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

## Issues found

- No blocking issues found during this run.
- One non-blocking deprecation warning remains (`pydantic` validator style migration).

## Go/No-Go decision

- Decision: `GO (Demo-ready)`
- Conditions:
  - Keep fallback/replay mode ready during live presentation.
  - Keep optional enrichments disabled if network is unstable.

## Signoff

- QA owner:
- Date:
- Notes:
