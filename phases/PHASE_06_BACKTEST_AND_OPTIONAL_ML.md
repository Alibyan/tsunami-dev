# PHASE_06_BACKTEST_AND_OPTIONAL_ML

## Goal

Use historical USGS data to evaluate the baseline and optionally add a lightweight model.

## Primary agents

- `AGENT_API_INGESTION.md`
- `AGENT_ML_EVALUATION.md`
- `AGENT_FEATURE_BASELINE.md`
- `AGENT_NOTEBOOK_EDA.md`

## Tasks

### Task 6.1 — Pull historical backfill windows
- Use the USGS catalog API
- Store training-ready historical records
- Document pagination and reproducibility

**Owner:** `AGENT_API_INGESTION.md`

### Task 6.2 — Build evaluation frame
- Select features and labels
- Use time-based splits
- Compare against the baseline first

**Owner:** `AGENT_ML_EVALUATION.md`

### Task 6.3 — Train lightweight model
- Prefer logistic regression first
- Add a slightly richer model only if there is clear value

**Owner:** `AGENT_ML_EVALUATION.md`

### Task 6.4 — Summarize model limits
- Record false positives
- Confirm that model output still means triage priority, not certainty

**Owner:** `AGENT_ML_EVALUATION.md`

## Outputs

- historical dataset
- baseline vs model comparison
- evaluation metrics and plots
- limitation notes

## Exit criteria

- the team can say whether ML helped or not
- the model remains interpretable enough for a short demo
- no one confuses proxy labels with real official alerts
