# AGENT_ENRICHMENT_APIS

## Mission

Integrate optional enrichment APIs carefully so they enhance the story without destabilizing the core demo.

## When to use

- After the core pipeline is working
- When adding ocean, public-attention, or context layers
- When deciding which optional API is worth the time

## Inputs

- Current app status
- Available time
- Target enrichment source
- User value for the enrichment

## Outputs

- A prioritized enrichment choice
- One or more optional API integrations
- Failure handling behavior
- A note explaining whether each enrichment is core or optional

## Hard rules

- Do not add enrichment until the core demo works
- Each enrichment must earn its place in the story
- Every enrichment must fail gracefully
- Prefer publicly documented, no-key, low-friction endpoints
- Do not let enrichment change the safety framing of the product

## Workflow

- Rank enrichment options by demo value versus integration cost
- Consider Open-Meteo marine data for wave context
- Consider Wikimedia pageviews as a public-attention proxy, with proper User-Agent handling
- Consider OpenFEMA as regional context rather than a causal signal
- Consider OBIS as biodiversity context only, not as a predictive claim
- Expose enrichments as optional layers or side panels

## Handoff rules

- Hand UI presentation to `AGENT_STREAMLIT_UI.md`
- Hand fallback handling to `AGENT_RELIABILITY_DEMO.md`
- Hand narrative usage to `AGENT_PITCH_DOCS.md`

## Done criteria

- At least one enrichment can be removed without harming the core demo
- Every enrichment has a clear user-facing purpose
- Failed enrichment calls do not break ranking or navigation
- The team can explain why each optional API was added

## Agent prompt block

Recommended enrichment order:

1. Open-Meteo marine context
2. Wikimedia pageviews
3. NOAA / NWS reference text
4. OpenFEMA context
5. OBIS context
