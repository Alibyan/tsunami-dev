# PHASE_04_DASHBOARD_V1

## Goal

Turn the pipeline into a working Streamlit product with a ranked queue, map, filters, and event details.

## Primary agents

- `../agents/AGENT_STREAMLIT_UI.md`
- `../agents/AGENT_SAFETY_DOMAIN.md`
- `../agents/AGENT_PROJECT_LEAD.md`

## Tasks

### Task 4.1 — Build the landing screen
- Show ranked recent events first
- Explain the product in one short paragraph
- Keep the first screen readable in under 10 seconds

**Owner:** `../agents/AGENT_STREAMLIT_UI.md`

### Task 4.2 — Add map and table views
- Plot event locations
- Show the ranked table with the key factors visible

**Owner:** `../agents/AGENT_STREAMLIT_UI.md`

### Task 4.3 — Add event detail panel
- Show the score breakdown
- Show core USGS fields
- Include official-source pointers and alert definitions

**Owner:** `../agents/AGENT_STREAMLIT_UI.md`

### Task 4.4 — Review screen wording
- Remove risky prediction language
- Keep safety and authority visible

**Owner:** `../agents/AGENT_SAFETY_DOMAIN.md`

## Outputs

- first working Streamlit app
- ranked list and map
- explanation-rich event detail panel
- reviewed language

## Exit criteria

- a teammate can do a one-minute walkthrough from the UI alone
- every rank has a visible reason
- the app still makes sense without optional enrichments
