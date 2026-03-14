# DEMO_RUNBOOK

This file is the live-demo operating guide.

The goal is to make the demo calm, predictable, and resilient.

## Demo objective

Show that the app can:

1. ingest or replay event data
2. rank events for analyst attention
3. explain why an event is ranked highly
4. stay usable even if optional services fail
5. communicate its limits honestly

## Demo modes

### Preferred mode
- app running normally
- live feed reachable
- local DB populated
- optional enrichments enabled only if stable

### Safe mode
- replay mode enabled
- cached sample dataset loaded
- optional enrichments disabled or hidden
- exact event examples preselected

## Pre-demo checklist

- app launches locally
- database file exists and is readable
- at least one strong cached example exists
- replay mode toggle works
- event detail panel renders without live network
- UI text has been reviewed for safe wording
- one backup screenshot exists in case the UI crashes
- one terminal is ready with clean startup logs

## Demo flow

### Step 1 — Problem framing
Say what problem the tool solves:

- many events can arrive quickly
- analysts need triage support
- the app helps prioritize which events deserve review first

Do **not** say it replaces official warnings.

### Step 2 — Show the ranked queue
Open the main screen and point to:

- top ranked event
- key facts
- rank or score
- why this event stands out

### Step 3 — Open one detail view
Show:

- event metadata
- score explanation factors
- official detail link
- any optional enrichment only if it is stable

### Step 4 — Show reliability path
Switch to replay mode or explain that the same UI works from cached data.

This is the trust-building moment of the demo.

### Step 5 — Close with boundaries
State clearly:

- this is a triage support tool
- official agencies remain the authority
- future work includes broader history, better labels, and stronger evaluation

## Timing guide

- 30–45 seconds: problem framing
- 60–90 seconds: ranked queue and detail view
- 30–45 seconds: replay mode or degraded mode
- 20–30 seconds: limitations and next steps

## Failure playbook

### If the live feed fails
- switch to replay mode immediately
- say the app supports offline demonstration using cached records
- keep the rest of the demo identical

### If an enrichment fails
- hide or skip that panel
- say optional context is non-critical by design
- keep focus on ranking and explanation

### If the UI partially fails
- show the cached screenshot briefly
- explain the intended click path
- return to the working part of the app if possible

### If the DB is empty
- load the prepared sample dataset
- confirm replay mode reads it correctly

## Suggested speaking lines

### Opening
“We built a triage support tool that helps surface which incoming seismic events deserve analyst attention first.”

### Ranking explanation
“This score is not a formal warning. It is an explainable prioritization signal based on event features and recent context.”

### Replay explanation
“We designed the app so the same interface can run from cached local data, which makes the demo and the workflow more reliable.”

### Closing
“The value here is not replacing official judgment. The value is reducing time to first review and making the reasoning visible.”

## Presenter roles

If multiple people are presenting:

- Presenter 1: problem framing and architecture
- Presenter 2: live app walkthrough
- Presenter 3: reliability path, limits, and next steps

## Post-demo note

After every practice run, write down:

- where the explanation felt unclear
- where the app looked slow or noisy
- what failed or nearly failed
- what should be removed before the real demo
