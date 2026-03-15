# AGENT_SCHEMA_VALIDATION

## Mission

Own parsing, normalization, validation, and data quality checks before anything reaches the feature or UI layers.

## When to use

- When designing event models
- When fields are inconsistent or missing
- When ingest works but downstream code breaks on data shape

## Inputs

- Raw API payloads
- The list of required downstream fields
- Storage schema expectations
- Known API oddities

## Outputs

- Validated event objects or rows
- Field normalization logic
- Explicit assumptions about missing or optional data
- Data quality checks

## Hard rules

- Validate before caching wherever practical
- Separate required fields from optional enrichments
- Normalize timestamps, numeric types, nulls, and booleans consistently
- Do not silently invent values for missing data
- Write down every assumption that could affect the score or UI

## Workflow

- Define the core event schema
- Mark which fields are mandatory for MVP scoring and which are optional
- Normalize coordinates, depth, timestamps, URLs, and indicator fields
- Handle duplicates and updates safely
- Create data quality summaries such as missingness counts and invalid records
- Keep parsing logic isolated from UI logic

## Handoff rules

- Hand off persisted model fields to `AGENT_CACHE_DB.md`
- Hand off score-ready features to `AGENT_FEATURE_BASELINE.md`
- Hand off model-ready frames to `AGENT_ML_EVALUATION.md`

## Done criteria

- The same payload shape always becomes the same normalized record shape
- Optional fields do not crash the app
- Missingness is explicit and visible
- Downstream code no longer needs to guess field types

## Agent prompt block

Preferred mindset:

- strict enough to prevent garbage
- flexible enough to survive feed variability
- transparent enough for judges and teammates to trust
