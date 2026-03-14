# AGENT_STREAMLIT_UI

## Mission

Build the Streamlit demo app that turns the data pipeline into an understandable live product.

## When to use

- When there is enough data to show rankings
- When map, table, filters, or drill-down views need to be implemented
- When the app needs clearer user-facing explanations

## Inputs

- Cached event data
- Baseline or model scores
- Safety text
- Desired demo flow

## Outputs

- A working Streamlit app
- Ranked event list
- Map view
- Event detail panel
- Explanation text and filters

## Hard rules

- Optimize for demo clarity over visual excess
- The first screen should explain the product in under 10 seconds
- Every ranked event should have a visible reason
- Do not hide safety language in a corner
- The app must still make sense if optional enrichments are absent

## Workflow

- Build a ranked queue of recent events
- Add a map with event locations
- Add an event detail panel with factor breakdown and official-source pointers
- Provide lightweight filters such as time window or score threshold
- Keep the UI resilient to missing enrichment data
- Prepare the UI for a fast 3-minute walkthrough

## Handoff rules

- Hand off wording review to `AGENT_SAFETY_DOMAIN.md`
- Hand off screenshot and demo polish to `AGENT_VISUAL_STORYTELLING.md`
- Hand off app stability work to `AGENT_RELIABILITY_DEMO.md`

## Done criteria

- A judge can understand the product almost immediately
- The app supports a short live walkthrough
- Missing data does not wreck the screen
- The map, queue, and detail panel all reinforce the same story

## Agent prompt block

Essential screens:

- ranked queue
- map
- event detail panel
- score explanation
- official-alert pointer
