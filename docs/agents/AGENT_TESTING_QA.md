# AGENT_TESTING_QA

## Mission

Add the smallest high-value test coverage and QA checks needed to trust the demo.

## When to use

- Once core scripts exist
- When regressions appear
- Before judging or packaging the demo

## Inputs

- Current scripts and app screens
- Known fragile code paths
- Sample payloads
- Critical user flows

## Outputs

- Smoke tests
- Parser tests
- A short QA checklist
- Regression coverage for the most fragile logic

## Hard rules

- Test the highest-risk paths first
- Prefer a few strong tests over a broad, shallow test suite
- Use saved sample payloads to make tests stable
- Every critical script should have at least a smoke-level run path
- Manual QA still matters for Streamlit and demo mode

## Workflow

- Write parser tests for the core event schema
- Write smoke tests for ingest, scoring, and app startup where practical
- Check replay mode and no-network mode manually
- Verify score explanations match actual values
- Create a brief pre-demo QA checklist

## Handoff rules

- Hand sample payload management to `AGENT_RELIABILITY_DEMO.md`
- Hand schema expectations to `AGENT_SCHEMA_VALIDATION.md`
- Hand presentation QA to `AGENT_VISUAL_STORYTELLING.md`

## Done criteria

- The highest-risk breakages are covered
- A teammate can run a short QA pass quickly
- Parser regressions are less likely
- The team knows the difference between tested flows and hopeful flows

## Agent prompt block

Priority test targets:

- USGS payload parsing
- SQLite write/read roundtrip
- baseline score function
- replay mode startup
