# AGENT_ML_EVALUATION

## Mission

Add a lightweight, interpretable model only after the baseline is working and measurable.

## When to use

- After the baseline score works
- When historical backfill exists
- When the team wants evidence that the model improves ranking

## Inputs

- Historical dataset
- Feature candidates
- Label strategy
- Baseline performance

## Outputs

- A lightweight model
- Evaluation results
- A comparison against the baseline
- Notes on limitations and false positives

## Hard rules

- Baseline first, model second
- Prefer logistic regression or a similarly lightweight model
- Use a time-based split, not a random split, by default
- Focus on imbalance-aware metrics
- Do not present proxy labels as ground-truth tsunami occurrence

## Workflow

- Define the exact label and document its limitations
- Start with a tiny feature set and expand only if justified
- Train on earlier windows and validate on later windows
- Measure PR-AUC, Precision@K, Recall, and F1
- Inspect top false positives and false negatives
- Report whether the model adds value over the baseline

## Handoff rules

- Hand off score display or model comparison to `AGENT_STREAMLIT_UI.md`
- Hand off caveat wording to `AGENT_SAFETY_DOMAIN.md`
- Hand off experiments or visual summaries to `AGENT_NOTEBOOK_EDA.md`

## Done criteria

- The model is fast enough to run on a laptop
- Metrics are understandable and relevant
- The label limitations are explicit
- The team can justify whether to keep or drop the model from the demo

## Agent prompt block

Suggested first model path:

- features: mag, depth, a few validated derived terms
- model: LogisticRegression
- validation: time-based split
- metrics: PR-AUC, Precision@K, Recall, F1
