# PHASE_02_LIVE_INGEST_AND_CACHE

## Goal

Fetch real-time USGS earthquake data, parse the required fields, and persist it safely into SQLite.

## Primary agents

- `AGENT_API_INGESTION.md`
- `AGENT_SCHEMA_VALIDATION.md`
- `AGENT_CACHE_DB.md`

## Tasks

### Task 2.1 — Select live feed and core fields
- Choose the initial USGS summary feed
- Lock the MVP field list: event id, time, updated, magnitude, coordinates, depth, place, URLs, tsunami flag

**Owner:** `AGENT_API_INGESTION.md`

### Task 2.2 — Implement fetch and parse loop
- Fetch the feed politely
- Parse features into normalized rows
- Save raw payload on parse failure

**Owner:** `AGENT_API_INGESTION.md`

### Task 2.3 — Define event schema
- Mark required vs optional fields
- Normalize timestamps, numbers, booleans, URLs, and coordinates
- Record assumptions

**Owner:** `AGENT_SCHEMA_VALIDATION.md`

### Task 2.4 — Create SQLite schema and upserts
- Create `events` table
- Add time-oriented indexes
- Implement idempotent upserts

**Owner:** `AGENT_CACHE_DB.md`

### Task 2.5 — Verify recent-event query path
- Add one query for “most recent events”
- Add one query for “top-ranked recent events” placeholder

**Owner:** `AGENT_CACHE_DB.md`

## Outputs

- live ingest script
- normalized event schema
- SQLite cache with upsert behavior
- raw snapshot fallback path

## Exit criteria

- running ingest produces rows in SQLite
- malformed payloads do not erase evidence
- the DB can serve recent events without manual cleanup
