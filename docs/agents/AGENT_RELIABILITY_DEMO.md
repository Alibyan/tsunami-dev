# AGENT_RELIABILITY_DEMO

## Mission

Make the project stable enough to survive a live demo, weak Wi-Fi, API hiccups, and partial failures.

## When to use

- Before any live demo or judging session
- When building fallback mode
- When the team needs replay or degraded-mode behavior

## Inputs

- Current app behavior
- Known points of failure
- Available cached data
- Demo requirements

## Outputs

- Replay mode
- Fallback dataset strategy
- Error handling plan
- A demo checklist

## Hard rules

- Assume at least one live dependency will fail at the worst time
- Core demo must work from local data
- Optional enrichments must fail gracefully
- Error states should degrade cleanly, not explode visually
- Prepare one primary demo path and one offline backup path

## Workflow

- Bundle or create a local sample USGS payload
- Ensure the app can read from local cache without network access
- Hide or disable optional widgets when inputs are missing
- Log failures clearly for debugging but keep the user experience calm
- Test the app once with network on and once with network off
- Write a short operator checklist for the presenter

## Handoff rules

- Hand off sample-data storage to `AGENT_CACHE_DB.md`
- Hand off demo script adjustments to `AGENT_PITCH_DOCS.md`
- Hand off UI polish under degraded mode to `AGENT_STREAMLIT_UI.md`

## Done criteria

- The demo can run from cached data
- A live API failure does not kill the presentation
- The presenter knows what to click and what to avoid
- Optional enrichments no longer threaten the core story

## Agent prompt block

Minimum fallback expectations:

- local sample GeoJSON
- cached SQLite database
- replay path
- no-network rehearsal
