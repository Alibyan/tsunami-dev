# PHASE_07_OPTIONAL_ENRICHMENTS_AND_POLISH

## Goal

Add one or more optional enrichments only if the core demo is already stable.

## Primary agents

- `AGENT_ENRICHMENT_APIS.md`
- `AGENT_STREAMLIT_UI.md`
- `AGENT_VISUAL_STORYTELLING.md`
- `AGENT_RELIABILITY_DEMO.md`

## Tasks

### Task 7.1 — Rank enrichment candidates
- Choose by value versus integration risk
- Favor one strong enrichment over many weak ones

**Owner:** `AGENT_ENRICHMENT_APIS.md`

### Task 7.2 — Add one optional context layer
- Open-Meteo marine data, Wikimedia pageviews, OpenFEMA, OBIS, or NOAA context
- Keep the integration removable

**Owner:** `AGENT_ENRICHMENT_APIS.md`

### Task 7.3 — Add visual polish
- Improve hierarchy
- Make screenshots and slide captures look intentional
- Reduce clutter from secondary panels

**Owner:** `AGENT_VISUAL_STORYTELLING.md`

### Task 7.4 — Confirm graceful failure path
- Verify the enrichment can disappear without harming the core story

**Owner:** `AGENT_RELIABILITY_DEMO.md`

## Outputs

- one or more optional enrichments
- cleaner screens
- screenshot-ready states

## Exit criteria

- enrichments feel useful, not decorative
- the core demo remains intact if enrichments are disabled
- the visuals support the spoken story
