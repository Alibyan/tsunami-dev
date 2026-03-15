# AGENT_TASK_ROUTER

## Mission

Route each project task to the correct specialist agent, in the correct order, with the correct handoffs.

## When to use

- When starting a new task and the owner is unclear
- When a task spans multiple agents
- When work is being duplicated or done out of order
- When the team needs a simple coordination layer inside Copilot or VS Code

## Inputs

- the current phase
- the exact task statement
- current project state
- blockers or missing prerequisites
- available time remaining

## Outputs

- one primary owner agent
- any required supporting agents
- a recommended execution order
- a stop condition for handoff
- a note on whether the task is MVP, reliability, stretch, or presentation work

## Hard rules

- Always assign one primary owner first
- Do not skip prerequisite phases just because a later task sounds exciting
- Keep the core path ahead of optional enrichments
- If a task touches user-facing claims, always involve `AGENT_SAFETY_DOMAIN.md`
- If a task changes the demo path, always consider `AGENT_RELIABILITY_DEMO.md`
- If a task only exists because of polish, do not let it block the MVP

## Routing table

### Foundation and setup tasks
Primary owner: `AGENT_REPO_BOOTSTRAP.md`
Support: `AGENT_PROJECT_LEAD.md`, `AGENT_MCP_WORKFLOW.md`
Examples:
- repo structure
- requirements and environment
- VS Code tasks
- MCP setup policy

### Live API fetch or backfill tasks
Primary owner: `AGENT_API_INGESTION.md`
Support: `AGENT_SCHEMA_VALIDATION.md`, `AGENT_CACHE_DB.md`
Examples:
- USGS feed polling
- historical catalog pulls
- retry logic
- raw snapshot storage

### Schema, parsing, and data quality tasks
Primary owner: `AGENT_SCHEMA_VALIDATION.md`
Support: `AGENT_API_INGESTION.md`, `AGENT_NOTEBOOK_EDA.md`
Examples:
- pydantic models
- null handling
- timestamp normalization
- missingness profiling

### SQLite and local cache tasks
Primary owner: `AGENT_CACHE_DB.md`
Support: `AGENT_API_INGESTION.md`, `AGENT_RELIABILITY_DEMO.md`
Examples:
- table design
- indexes
- upserts
- replay-friendly reads

### Baseline scoring tasks
Primary owner: `AGENT_FEATURE_BASELINE.md`
Support: `AGENT_SCHEMA_VALIDATION.md`, `AGENT_SAFETY_DOMAIN.md`
Examples:
- transparent score formula
- factor breakdowns
- threshold logic

### Historical analysis and model tasks
Primary owner: `AGENT_ML_EVALUATION.md`
Support: `AGENT_API_INGESTION.md`, `AGENT_NOTEBOOK_EDA.md`, `AGENT_FEATURE_BASELINE.md`, `AGENT_SAFETY_DOMAIN.md`
Examples:
- backtest splits
- logistic regression
- metrics
- error analysis

### Streamlit app tasks
Primary owner: `AGENT_STREAMLIT_UI.md`
Support: `AGENT_FEATURE_BASELINE.md`, `AGENT_SAFETY_DOMAIN.md`, `AGENT_VISUAL_STORYTELLING.md`
Examples:
- ranked queue
- map
- event detail panel
- filters

### Reliability and offline-demo tasks
Primary owner: `AGENT_RELIABILITY_DEMO.md`
Support: `AGENT_CACHE_DB.md`, `AGENT_TESTING_QA.md`, `AGENT_STREAMLIT_UI.md`
Examples:
- replay mode
- degraded mode
- logging
- sample payloads

### Optional enrichment tasks
Primary owner: `AGENT_ENRICHMENT_APIS.md`
Support: `AGENT_STREAMLIT_UI.md`, `AGENT_RELIABILITY_DEMO.md`, `AGENT_PITCH_DOCS.md`
Examples:
- Open-Meteo panel
- Wikimedia sparkline
- OpenFEMA context
- OBIS context

### Notebook and exploratory tasks
Primary owner: `AGENT_NOTEBOOK_EDA.md`
Support: `AGENT_SCHEMA_VALIDATION.md`, `AGENT_ML_EVALUATION.md`
Examples:
- quick profiling notebooks
- feature sanity checks
- chart drafts for slides

### Testing and pre-demo verification tasks
Primary owner: `AGENT_TESTING_QA.md`
Support: `AGENT_RELIABILITY_DEMO.md`, `AGENT_SCHEMA_VALIDATION.md`, `AGENT_STREAMLIT_UI.md`
Examples:
- parser tests
- smoke tests
- manual QA checklist

### Pitch, documentation, and packaging tasks
Primary owner: `AGENT_PITCH_DOCS.md`
Support: `AGENT_PROJECT_LEAD.md`, `AGENT_SAFETY_DOMAIN.md`, `AGENT_VISUAL_STORYTELLING.md`
Examples:
- README
- demo script
- architecture summary
- release notes

### Claim-boundary and wording tasks
Primary owner: `AGENT_SAFETY_DOMAIN.md`
Support: whichever agent owns the feature being described
Examples:
- wording review
- disclaimers
- what-it-is / what-it-is-not sections

## Routing algorithm

Use this exact order:

1. Identify the phase.
2. Identify whether the task is core, reliability, optional, or presentation.
3. Check prerequisites from earlier phases.
4. Assign one primary owner.
5. Add at most two support agents unless the task truly spans more.
6. State the handoff trigger explicitly.
7. Refuse to route optional work ahead of a broken core path.

## Handoff triggers

Use these handoff triggers when routing:

- hand off to validation when raw payloads exist
- hand off to cache when normalized rows exist
- hand off to baseline when stable fields exist
- hand off to UI when ranked records exist
- hand off to reliability when the first end-to-end demo works
- hand off to ML only after the baseline is measurable
- hand off to pitch/docs only after the click path is stable

## Done criteria

- every task has an owner
- no two agents are solving the same step blindly
- phase order stays intact
- optional work no longer crowds out the MVP

## Agent prompt block

When I give you a task, answer in this exact format:

- phase
- task type
- primary owner
- support agents
- why this routing is correct
- prerequisites
- concrete next step
- handoff trigger
