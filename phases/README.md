# Tsunami Triage Phase Plan

This folder breaks the **Offshore Quake & Tsunami Triage** project into clear phases and task blocks.

## Sequencing principle

The project should move in this order:

1. foundation and repo setup
2. live ingest and local cache
3. validation and baseline scoring
4. dashboard and user-facing explanations
5. reliability, replay mode, and offline safety
6. historical backtest and optional ML
7. optional enrichments
8. pitch, QA, and release polish

This sequencing matches the project notes and the original agent pack philosophy: build the boring core first, then add the demo polish, then add optional improvements.

## How to use this folder

- Start with `PHASE_00_MASTER_PLAN.md`
- Open the current phase file
- Pull the matching specialist agent from `../agents/`
- Use `AGENT_TASK_ROUTER.md` to assign the current task to the right agent or sequence of agents


## Supporting control files

At the pack root, use these files alongside the phase documents:

- `../DEFINITION_OF_DONE.md` for acceptance criteria
- `../DECISION_LOG.md` for key tradeoffs
- `../TASK_DEPENDENCY_MATRIX.md` for blockers and sequencing
- `../DATA_CONTRACTS.md` for schema alignment
- `../PROMPT_LIBRARY.md` for copy-paste Copilot prompts
- `../DEMO_RUNBOOK.md` for live demo execution
- `../RISK_REGISTER.md` for fallback planning
