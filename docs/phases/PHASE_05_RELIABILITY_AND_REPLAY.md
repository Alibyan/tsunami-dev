# PHASE_05_RELIABILITY_AND_REPLAY

## Goal

Make the project safe to demo live, under poor network conditions, or with optional API failures.

## Primary agents

- `../agents/AGENT_RELIABILITY_DEMO.md`
- `../agents/AGENT_CACHE_DB.md`
- `../agents/AGENT_TESTING_QA.md`

## Tasks

### Task 5.1 — Add replay mode
- Ship a cached feed snapshot or a replay dataset
- Make replay launchable with one command or one toggle

**Owner:** `../agents/AGENT_RELIABILITY_DEMO.md`

### Task 5.2 — Add degraded-mode rules
- Hide broken optional panels gracefully
- Keep the core queue, map, and detail view alive

**Owner:** `../agents/AGENT_RELIABILITY_DEMO.md`

### Task 5.3 — Add logging and health checks
- Log ingest success, failure, and record counts
- Expose enough info to debug quickly without cluttering the demo

**Owner:** `../agents/AGENT_RELIABILITY_DEMO.md`

### Task 5.4 — Run high-value QA
- Smoke test ingest
- Smoke test app startup
- Verify replay mode works without network

**Owner:** `../agents/AGENT_TESTING_QA.md`

## Outputs

- replay mode
- degraded behavior policy
- basic logs
- short QA checklist

## Exit criteria

- the project can still be shown if Wi-Fi fails
- optional APIs can fail without collapsing the app
- the team knows the demo-safe run path
