# AGENT_FEATURE_BASELINE

## Mission

Build the first transparent triage score before any machine learning is attempted.

## When to use

- After validated records are available
- When the team needs an explainable baseline
- When there is pressure to add ML too early

## Inputs

- Normalized event data
- Project safety framing
- Target factors for the score
- User-facing explanation needs

## Outputs

- A working baseline score
- Score factor breakdowns
- Threshold logic
- Human-readable explanation text

## Hard rules

- Baseline must be explainable in plain language
- Do not imply the app predicts tsunami occurrence
- Prefer 2 to 4 strong factors over a long hidden formula
- Every score should be decomposable for UI display
- The baseline should work without enrichments

## Workflow

- Choose a small factor set such as magnitude, depth, and recency
- Define the score range and how each factor contributes
- Create a factor breakdown for every event
- Write text explanations that match the actual score logic
- Test a few example events by hand to confirm the score is intuitive
- Document what the score means: urgency of human review, not a forecast

## Handoff rules

- Hand off ranking display to `AGENT_STREAMLIT_UI.md`
- Hand off label and wording review to `AGENT_SAFETY_DOMAIN.md`
- Hand off comparison experiments to `AGENT_ML_EVALUATION.md`

## Done criteria

- The app can rank events without ML
- The score is easy to explain to a judge
- The factor breakdown matches the implementation
- A user can see why one event ranked above another

## Agent prompt block

Recommended MVP factors:

- magnitude
- depth / shallowness
- recency

Optional later factors:

- offshore proxy
- historical proxy score
- selected enrichment signals
