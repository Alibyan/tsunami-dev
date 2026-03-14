# AGENT_CACHE_DB

## Mission

Design and maintain the SQLite cache, upsert behavior, indexing, and replay-ready local data storage.

## When to use

- When creating the local database
- When ingest needs durable storage
- When replay mode or offline demo mode is being added
- When DB queries feel slow or confusing

## Inputs

- Validated event schema
- Ingestion behavior
- Replay requirements
- Expected read patterns from the app and training scripts

## Outputs

- SQLite schema
- Upsert logic
- Indexes
- Query helpers
- Replay-friendly local data

## Hard rules

- SQLite is the source of truth for the demo cache
- Schema must reflect the actual scoring and UI needs
- Store enough raw data for debugging or replay, but avoid bloating the MVP
- Use upserts instead of duplicate inserts where possible
- Design reads for ranking and recent-event queries first

## Workflow

- Create the `events` table with a stable primary key
- Add indexes for recent-time queries and other frequent reads
- Implement upserts for changed event details
- Persist a raw JSON column or snapshot file where helpful
- Support a simple replay mode from cached records or sample files
- Document a few useful SQL queries for debugging and demo prep

## Handoff rules

- Hand off feature-ready reads to `AGENT_FEATURE_BASELINE.md` and `AGENT_ML_EVALUATION.md`
- Hand off sqlite inspection flow to `AGENT_MCP_WORKFLOW.md`
- Hand off sample data strategy to `AGENT_RELIABILITY_DEMO.md`

## Done criteria

- Live ingest can be resumed safely
- Recent events can be queried quickly
- The local cache supports offline demo mode
- A teammate can inspect the DB without reverse engineering the schema

## Agent prompt block

Minimum DB concerns:

- primary key: event id
- useful columns: time, updated, mag, depth, lat, lon, place, urls, tsunami flag, raw_json
- operational goals: upsert, query latest, support replay
