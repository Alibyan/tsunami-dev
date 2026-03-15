# AGENT_NOTEBOOK_EDA

## Mission

Use notebooks for fast exploratory analysis, feature sanity checks, and chart generation without turning the notebook into the application.

## When to use

- When exploring distributions or missingness
- When testing candidate features
- When generating quick plots for the pitch or validation

## Inputs

- Cached local data
- Hypotheses about the data
- Candidate features or labels
- Current evaluation questions

## Outputs

- Compact exploratory notebooks
- Feature sanity checks
- Plots or tables worth promoting to docs or slides
- Notes on what should move into production scripts

## Hard rules

- Notebooks are for exploration, not final architecture
- Keep each notebook focused on one question
- Promote stable logic back into scripts once proven
- Avoid hidden state and one-off notebook magic
- Every notebook should be reproducible from cached local data

## Workflow

- Explore missingness, score distributions, and feature relationships
- Prototype candidate features and inspect their behavior
- Generate clear plots for metrics and false positives
- Write short conclusions under each chart
- Identify which logic belongs in scripts versus which belongs only in analysis

## Handoff rules

- Hand stable feature logic to `AGENT_FEATURE_BASELINE.md` or `AGENT_ML_EVALUATION.md`
- Hand presentation-worthy figures to `AGENT_PITCH_DOCS.md` and `AGENT_VISUAL_STORYTELLING.md`

## Done criteria

- The notebook answers a real question
- Interesting results are summarized, not buried
- Useful logic is migrated into scripts
- The analysis can be rerun from local cached data

## Agent prompt block

Good notebook topics:

- missing fields by event type
- score distribution over recent events
- proxy label balance over time
- false positive inspection
