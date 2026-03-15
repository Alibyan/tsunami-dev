# AGENT_REPO_BOOTSTRAP

## Mission

Create and maintain the initial repository structure, local developer workflow, and minimal dependencies required to build the project quickly in VS Code.

## When to use

- At project start
- When the repository needs to be normalized
- When the team needs scripts, folders, or dependency cleanup

## Inputs

- Project name and purpose
- Preferred stack
- Required scripts and app entrypoints
- Any existing repo contents

## Outputs

- A clean folder structure
- A minimal dependency list
- Run commands for ingest, train, and app
- VS Code-friendly task flow
- Environment examples and README starter

## Hard rules

- Do not over-engineer package layout
- Only add dependencies that support the MVP directly
- Prefer standard library + requests + sqlite3 where possible
- Keep the project runnable by one person on one laptop
- Make it obvious how to run the app in under two commands

## Workflow

- Create or verify folders such as `src/`, `data/`, `notebooks/`, `tests/`, and `docs/agents/`
- Establish the primary scripts: ingest, backfill, train, app
- Create `requirements.txt` or equivalent with minimal packages
- Create `.env.example` only if secrets or env-driven configuration are actually needed
- Add a starter README with run commands and a short architecture note
- Add sample data placeholders for replay mode if available

## Handoff rules

- Hand off MCP concerns to `AGENT_MCP_WORKFLOW.md`
- Hand off data pullers to `AGENT_API_INGESTION.md`
- Hand off test scaffolding to `AGENT_TESTING_QA.md`

## Done criteria

- A new teammate can understand the repo layout immediately
- The project can be installed and run locally without guessing
- File names and entrypoints match the actual architecture

## Agent prompt block

Target a structure like:

- src/
  - ingest_usgs.py
  - backfill_catalog.py
  - features.py
  - score.py
  - train_model.py
  - app.py
- data/
  - events.sqlite
  - sample_all_hour.geojson
- notebooks/
- tests/
- docs/agents/
