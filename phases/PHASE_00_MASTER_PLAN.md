# PHASE_00_MASTER_PLAN

## Purpose

This file is the top-level build map for the project.

## Phase ladder

### Phase 1 — Foundation and repo bootstrap
Goal: create a clean repo, local environment, scripts, and MCP boundary.

### Phase 2 — Live ingest and local cache
Goal: fetch USGS live data reliably and persist it into SQLite.

### Phase 3 — Validation, profiling, and baseline triage
Goal: normalize records, inspect data quality, and build the first explainable score.

### Phase 4 — Dashboard v1 and user-facing explanations
Goal: ship a working Streamlit app with ranked queue, map, and detail panel.

### Phase 5 — Reliability, replay mode, and offline demo safety
Goal: make the project demo-safe even if the network or optional APIs fail.

### Phase 6 — Historical backtest and optional ML
Goal: evaluate the baseline on historical windows and optionally add a lightweight model.

### Phase 7 — Optional enrichments and storytelling polish
Goal: add one or more non-core enrichments that improve the story without risking stability.

### Phase 8 — Pitch, QA, and release package
Goal: rehearse the demo, tighten wording, run the checklist, and package artifacts.

## Phase exit rule

Do not advance a phase just because code exists. Advance when the phase output is **demo-usable** and the handoff artifacts are real.

## Core principle

The project is successful as soon as these five things exist together:

- live ingest
- local cache
- explainable baseline ranking
- clear Streamlit view
- safe offline replay path

Everything after that is optional upside.
