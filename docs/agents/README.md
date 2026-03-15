# Tsunami Triage Agent Pack

This pack contains a practical set of markdown agents for building the **Offshore Quake & Tsunami Triage** project in **VS Code with Copilot** and **free MCP servers**.

## Design assumptions

- Build for a **2-day hackathon MVP**
- Keep runtime simple: **Python + requests + SQLite + Streamlit**
- Use MCP only as a **build-time assistant**, not as a production dependency
- Default free MCP stack:
  - filesystem
  - fetch
  - sqlite (optional but recommended)

## Recommended build order

1. `AGENT_PROJECT_LEAD.md`
2. `AGENT_REPO_BOOTSTRAP.md`
3. `AGENT_MCP_WORKFLOW.md`
4. `AGENT_API_INGESTION.md`
5. `AGENT_SCHEMA_VALIDATION.md`
6. `AGENT_CACHE_DB.md`
7. `AGENT_FEATURE_BASELINE.md`
8. `AGENT_STREAMLIT_UI.md`
9. `AGENT_RELIABILITY_DEMO.md`
10. `AGENT_ML_EVALUATION.md`
11. `AGENT_ENRICHMENT_APIS.md`
12. `AGENT_TESTING_QA.md`
13. `AGENT_VISUAL_STORYTELLING.md`
14. `AGENT_NOTEBOOK_EDA.md`
15. `AGENT_PITCH_DOCS.md`
16. `AGENT_SAFETY_DOMAIN.md`
17. `AGENT_TASK_ROUTER.md`

## How to use in Copilot / VS Code

Open the file for the agent you want, then use its content as the standing instruction for the task in front of you.

Suggested pattern:

1. Start with `AGENT_PROJECT_LEAD.md`
2. Let it decide the next concrete task
3. Switch to the matching specialist agent
4. Finish with `AGENT_RELIABILITY_DEMO.md`, `AGENT_PITCH_DOCS.md`, and `AGENT_SAFETY_DOMAIN.md`

## File format

Every agent in this pack includes:

- mission
- when to use
- inputs
- outputs
- hard rules
- workflow
- handoff rules
- done criteria

## Optional agents

The last 4 specialist agents are optional, but they are included in this pack because they meaningfully improve the build:

- `AGENT_ENRICHMENT_APIS.md`
- `AGENT_TESTING_QA.md`
- `AGENT_VISUAL_STORYTELLING.md`
- `AGENT_NOTEBOOK_EDA.md`

## New coordination files

- `AGENT_TASK_ROUTER.md` routes a concrete task to the right specialist agent(s)
- `../phases/PHASE_00_MASTER_PLAN.md` defines the phase ladder
- `../project/TASK_AGENT_WIRING_MATRIX.md` is the quick lookup table for task ownership


## Execution-control files at pack root

These files sit at the pack root and help coordinate the build across all phases:

- `../project/DEFINITION_OF_DONE.md`
- `../project/DECISION_LOG.md`
- `../project/TASK_DEPENDENCY_MATRIX.md`
- `../project/DATA_CONTRACTS.md`
- `../project/PROMPT_LIBRARY.md`
- `../project/DEMO_RUNBOOK.md`
- `../project/RISK_REGISTER.md`

Use them together with the agent files when you want stronger execution discipline, clearer handoffs, and a safer demo path.
