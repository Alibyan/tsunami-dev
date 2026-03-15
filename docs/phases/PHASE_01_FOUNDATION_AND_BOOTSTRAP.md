# PHASE_01_FOUNDATION_AND_BOOTSTRAP

## Goal

Create the repo, environment, folder structure, task runners, and a clean development workflow in VS Code.

## Primary agents

- `../agents/AGENT_PROJECT_LEAD.md`
- `../agents/AGENT_REPO_BOOTSTRAP.md`
- `../agents/AGENT_MCP_WORKFLOW.md`

## Tasks

### Task 1.1 — Define repository shape
- Create `src/`, `app/`, `data/`, `notebooks/`, `tests/`, `docs/`, and `scripts/`
- Add `requirements.txt`
- Add `.env.example`
- Add `README.md`

**Owner:** `../agents/AGENT_REPO_BOOTSTRAP.md`

### Task 1.2 — Define local run commands
- Add script entry points for ingest, app, and training/backtest
- Add VS Code tasks if helpful
- Keep command names obvious

**Owner:** `../agents/AGENT_REPO_BOOTSTRAP.md`

### Task 1.3 — Set MCP boundary
- Decide which MCP servers are used in development
- Document filesystem, fetch, and optional sqlite use
- Explicitly state that runtime does not depend on MCP

**Owner:** `../agents/AGENT_MCP_WORKFLOW.md`

### Task 1.4 — Freeze MVP scope
- Confirm the core MVP is live ingest + cache + baseline + Streamlit + replay
- Push non-core items into later phases

**Owner:** `../agents/AGENT_PROJECT_LEAD.md`

## Outputs

- runnable repo skeleton
- basic local commands
- documented MCP policy
- frozen MVP scope

## Exit criteria

- a teammate can clone and run the skeleton
- the next phase can start without re-arguing scope
- MCP usage is documented in one short section
