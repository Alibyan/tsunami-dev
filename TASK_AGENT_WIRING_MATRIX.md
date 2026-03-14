# TASK_AGENT_WIRING_MATRIX

This file is the quick-reference wiring map between project tasks and the existing specialist agents.

| Task family | Primary agent | Secondary agents | Notes |
|---|---|---|---|
| Repo setup | `AGENT_REPO_BOOTSTRAP.md` | `AGENT_PROJECT_LEAD.md`, `AGENT_MCP_WORKFLOW.md` | Start here |
| MCP setup and policy | `AGENT_MCP_WORKFLOW.md` | `AGENT_REPO_BOOTSTRAP.md` | Build-time only |
| Live feed ingest | `AGENT_API_INGESTION.md` | `AGENT_SCHEMA_VALIDATION.md`, `AGENT_CACHE_DB.md` | Core path |
| Historical backfill | `AGENT_API_INGESTION.md` | `AGENT_CACHE_DB.md`, `AGENT_ML_EVALUATION.md` | Phase 6 |
| Schema and parsing | `AGENT_SCHEMA_VALIDATION.md` | `AGENT_API_INGESTION.md`, `AGENT_NOTEBOOK_EDA.md` | Before scoring |
| SQLite design | `AGENT_CACHE_DB.md` | `AGENT_API_INGESTION.md`, `AGENT_RELIABILITY_DEMO.md` | Needed for replay |
| Baseline triage score | `AGENT_FEATURE_BASELINE.md` | `AGENT_SCHEMA_VALIDATION.md`, `AGENT_SAFETY_DOMAIN.md` | Before ML |
| Streamlit UI | `AGENT_STREAMLIT_UI.md` | `AGENT_FEATURE_BASELINE.md`, `AGENT_SAFETY_DOMAIN.md` | Demo surface |
| Reliability and replay | `AGENT_RELIABILITY_DEMO.md` | `AGENT_CACHE_DB.md`, `AGENT_TESTING_QA.md` | Must exist before demo |
| Historical evaluation | `AGENT_ML_EVALUATION.md` | `AGENT_API_INGESTION.md`, `AGENT_NOTEBOOK_EDA.md` | Optional but strong |
| Optional enrichments | `AGENT_ENRICHMENT_APIS.md` | `AGENT_STREAMLIT_UI.md`, `AGENT_RELIABILITY_DEMO.md` | Only after core works |
| Notebook profiling | `AGENT_NOTEBOOK_EDA.md` | `AGENT_SCHEMA_VALIDATION.md`, `AGENT_ML_EVALUATION.md` | Quick insight work |
| QA and smoke tests | `AGENT_TESTING_QA.md` | `AGENT_RELIABILITY_DEMO.md`, `AGENT_STREAMLIT_UI.md` | Pre-demo |
| Pitch/docs | `AGENT_PITCH_DOCS.md` | `AGENT_PROJECT_LEAD.md`, `AGENT_SAFETY_DOMAIN.md` | Last mile |
| Wording/disclaimers | `AGENT_SAFETY_DOMAIN.md` | owning feature agent | Always include for public text |
| Visual polish | `AGENT_VISUAL_STORYTELLING.md` | `AGENT_STREAMLIT_UI.md`, `AGENT_PITCH_DOCS.md` | After UI is stable |
