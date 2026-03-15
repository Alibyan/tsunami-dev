# AGENT_API_INGESTION

## Mission

Implement reliable, boring, testable ingestion for USGS live feeds and historical catalog backfills.

## When to use

- When building the live ingest script
- When adding USGS catalog backfills
- When debugging API pulls, retries, or feed changes

## Inputs

- Target endpoints
- Polling cadence requirements
- Fields needed downstream
- Failure handling requirements
- Storage target

## Outputs

- Working ingestion scripts
- Parsed event rows or raw snapshots
- Retry and logging behavior
- A documented poll/backfill strategy

## Hard rules

- Prefer official USGS feeds first
- Respect feed cadence; do not hammer endpoints
- Save raw payloads when parsing fails
- Differentiate live feed ingest from historical catalog backfill
- Make every ingest step idempotent when possible

## Workflow

- Implement feed fetch for a selected USGS GeoJSON summary endpoint
- Extract only the fields required for the MVP first: id, time, updated, magnitude, coordinates, depth, place, URLs, tsunami flag
- Persist raw JSON when parsing errors occur
- Add backfill support through the USGS catalog API for historical windows
- Log counts, duplicates, and failures
- Document expected cadence and limits

## Handoff rules

- Hand off schema enforcement to `AGENT_SCHEMA_VALIDATION.md`
- Hand off persistence details to `AGENT_CACHE_DB.md`
- Hand off downstream feature logic to `AGENT_FEATURE_BASELINE.md`

## Done criteria

- A live pull succeeds and produces rows
- A failed parse does not destroy the payload
- The system can backfill a historical window reproducibly
- The ingest script can be demonstrated independently

## Agent prompt block

Primary targets:

- live feed: USGS GeoJSON summary feed
- historical pull: USGS Earthquake Catalog / FDSN event query
- behavior: polite polling, snapshot fallback, replay readiness
