# PROMPT_LIBRARY

This file contains copy-paste prompts for VS Code + Copilot when working with the agent pack.

Use these prompts with the relevant agent file open beside your code.

## Project lead prompts

### Scope the next task

> Using `../agents/AGENT_PROJECT_LEAD.md` and `../agents/AGENT_TASK_ROUTER.md`, take the current phase and propose the single best next task for the MVP. Include: objective, files likely to change, acceptance criteria, and handoff trigger.

### Prevent scope creep

> Review the current task against the active phase. Identify anything that belongs to a later phase, mark it as stretch work, and rewrite the task as the smallest shippable MVP step.

## Repo bootstrap prompts

### Create local project skeleton

> Using `../agents/AGENT_REPO_BOOTSTRAP.md`, propose a clean Python repo layout for this project with `src/`, `app/`, `data/`, `scripts/`, `tests/`, and `docs/`. Include `requirements.txt`, `.env.example`, and VS Code tasks.

### Add run commands

> Create minimal scripts and commands for: live ingest, historical backfill, local DB init, replay mode, and Streamlit app launch. Keep the commands simple and laptop-friendly.

## MCP workflow prompts

### Enforce MCP boundary

> Using `../agents/AGENT_MCP_WORKFLOW.md`, review this implementation and identify anything that incorrectly depends on MCP at runtime. Rewrite the design so MCP stays a build-time helper only.

### Free MCP setup summary

> Write a minimal setup note for filesystem MCP, fetch MCP, and optional SQLite MCP in VS Code. Emphasize what each one is allowed to do for this project.

## Ingestion prompts

### Build a fetcher

> Using `../agents/AGENT_API_INGESTION.md`, write a small Python module that fetches the live upstream event feed, logs request failures, and stores raw responses for debugging. Keep the code clean and testable.

### Historical pull path

> Create a historical backfill script that pages through the upstream catalog carefully, respects rate limits, and writes results to the local cache path without mixing runtime logic into the UI.

## Validation prompts

### Normalize one payload

> Using `../agents/AGENT_SCHEMA_VALIDATION.md`, turn this raw payload into a normalized event model. Show required fields, optional fields, type conversions, UTC timestamp handling, and null rules.

### Add parser safety

> Write validation logic that gracefully handles missing fields, malformed numbers, duplicate IDs, and unexpected event types. Return explicit parse errors rather than hiding failures.

## Cache prompts

### Create SQLite schema

> Using `../agents/AGENT_CACHE_DB.md`, propose a SQLite schema for normalized events, raw payload references, and replay-mode reads. Include keys, indexes, and idempotent upsert strategy.

### Replay-friendly read model

> Build a read function that returns the newest ranked or normalized events for the UI, and make sure the same path can serve replay mode when the network is unavailable.

## Baseline prompts

### Build explainable score

> Using `../agents/AGENT_FEATURE_BASELINE.md`, design a transparent triage score from the normalized fields. Include exact feature inputs, weighting logic, normalization notes, and a per-event explanation payload for the UI.

### Compare thresholds

> Propose two or three threshold schemes for converting the score into review priority tiers. Explain the tradeoffs in clarity, stability, and false positives.

## ML prompts

### Evaluate baseline first

> Using `../agents/AGENT_ML_EVALUATION.md`, define a historical evaluation plan for the rule-based baseline before adding any model. Include time-based splits, metrics, and failure analysis.

### Add lightweight model carefully

> Add a simple interpretable model candidate and compare it against the baseline. Do not overclaim results. Produce a table of metrics and a note on whether it is worth keeping.

## Streamlit prompts

### Build dashboard shell

> Using `../agents/AGENT_STREAMLIT_UI.md`, create a Streamlit layout with a ranked event list, map section, detail panel, score explanation area, and clear empty/error states.

### Detail card copy

> Write user-facing copy for the event detail panel that explains why an event ranked highly without implying official warning authority.

## Reliability prompts

### Add replay mode

> Using `../agents/AGENT_RELIABILITY_DEMO.md`, implement a replay mode that loads cached events and drives the same UI path as live mode. Include a switch and a fallback message.

### Graceful degradation

> Review the app for external dependencies and design degraded behavior for each one so the core demo still works if the network or optional enrichments fail.

## Enrichment prompts

### Add one safe enrichment

> Using `../agents/AGENT_ENRICHMENT_APIS.md`, propose one enrichment that improves the demo story without becoming a critical dependency. Include timeout policy, cache policy, and UI fallback behavior.

## Testing prompts

### Smoke test set

> Using `../agents/AGENT_TESTING_QA.md`, generate a minimal smoke test suite for live fetch, parsing, cache upsert, replay mode, and dashboard startup.

### Manual QA checklist

> Create a short manual pre-demo checklist that verifies the core click path, empty states, fallback path, and safe wording.

## Visual prompts

### Tighten the demo surface

> Using `../agents/AGENT_VISUAL_STORYTELLING.md`, simplify this Streamlit layout for judges. Reduce clutter, improve the visual hierarchy, and keep the top-ranked story obvious.

## Notebook prompts

### Quick profile notebook

> Using `../agents/AGENT_NOTEBOOK_EDA.md`, create a notebook outline that profiles missingness, magnitude distribution, recency, and the first baseline score outputs from cached data.

## Pitch and docs prompts

### README draft

> Using `../agents/AGENT_PITCH_DOCS.md`, write a concise README with problem framing, architecture, local run steps, limitations, and demo flow.

### Demo script draft

> Write a 3-minute demo script that starts with the problem, shows the ranked queue, opens one event detail card, demonstrates replay mode, and ends with limitations and next steps.

## Safety prompts

### Claims review

> Using `../agents/AGENT_SAFETY_DOMAIN.md`, review this UI text and README copy for overclaiming. Rewrite anything that sounds like a formal warning or official prediction.

## Router prompts

### Route the next task

> Using `../agents/AGENT_TASK_ROUTER.md`, classify this task by phase and task type, choose the primary owner agent, list support agents, state prerequisites, and give the next concrete implementation step.
