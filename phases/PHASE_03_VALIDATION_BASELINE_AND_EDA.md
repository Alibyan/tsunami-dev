# PHASE_03_VALIDATION_BASELINE_AND_EDA

## Goal

Inspect data quality and ship the first explainable triage score.

## Primary agents

- `AGENT_SCHEMA_VALIDATION.md`
- `AGENT_FEATURE_BASELINE.md`
- `AGENT_NOTEBOOK_EDA.md`
- `AGENT_SAFETY_DOMAIN.md`

## Tasks

### Task 3.1 — Profile the cached dataset
- Check missingness
- Check duplicates and update behavior
- Identify fields safe for MVP scoring

**Owner:** `AGENT_NOTEBOOK_EDA.md`

### Task 3.2 — Lock baseline features
- Choose 2 to 4 strong factors
- Prefer magnitude, depth, and recency first
- Keep enrichment-independent logic

**Owner:** `AGENT_FEATURE_BASELINE.md`

### Task 3.3 — Implement score and factor breakdown
- Define score range
- Compute factor contributions
- Return explanation-ready output

**Owner:** `AGENT_FEATURE_BASELINE.md`

### Task 3.4 — Validate wording and safety framing
- Confirm score means urgency of review, not official forecast
- Add what-it-is and what-it-is-not statements

**Owner:** `AGENT_SAFETY_DOMAIN.md`

## Outputs

- data quality notes
- baseline score function
- factor breakdown logic
- safe text for UI and docs

## Exit criteria

- at least one ranked list exists before any ML
- the team can explain the ranking in plain language
- the wording does not overclaim
