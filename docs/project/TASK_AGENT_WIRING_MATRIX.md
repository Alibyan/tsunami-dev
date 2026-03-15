# TASK_AGENT_WIRING_MATRIX

This file is the quick-reference wiring map between project tasks and the existing specialist agents.

| Task family | Primary agent | Secondary agents | Notes |
|---|---|---|---|
| Repo setup | `../agents/AGENT_REPO_BOOTSTRAP.md` | `../agents/AGENT_PROJECT_LEAD.md`, `../agents/AGENT_MCP_WORKFLOW.md` | Start here |
| MCP setup and policy | `../agents/AGENT_MCP_WORKFLOW.md` | `../agents/AGENT_REPO_BOOTSTRAP.md` | Build-time only |
| Live feed ingest | `../agents/AGENT_API_INGESTION.md` | `../agents/AGENT_SCHEMA_VALIDATION.md`, `../agents/AGENT_CACHE_DB.md` | Core path |
| Historical backfill | `../agents/AGENT_API_INGESTION.md` | `../agents/AGENT_CACHE_DB.md`, `../agents/AGENT_ML_EVALUATION.md` | Phase 6 |
| Schema and parsing | `../agents/AGENT_SCHEMA_VALIDATION.md` | `../agents/AGENT_API_INGESTION.md`, `../agents/AGENT_NOTEBOOK_EDA.md` | Before scoring |
| SQLite design | `../agents/AGENT_CACHE_DB.md` | `../agents/AGENT_API_INGESTION.md`, `../agents/AGENT_RELIABILITY_DEMO.md` | Needed for replay |
| Baseline triage score | `../agents/AGENT_FEATURE_BASELINE.md` | `../agents/AGENT_SCHEMA_VALIDATION.md`, `../agents/AGENT_SAFETY_DOMAIN.md` | Before ML |
| Streamlit UI | `../agents/AGENT_STREAMLIT_UI.md` | `../agents/AGENT_FEATURE_BASELINE.md`, `../agents/AGENT_SAFETY_DOMAIN.md` | Demo surface |
| Reliability and replay | `../agents/AGENT_RELIABILITY_DEMO.md` | `../agents/AGENT_CACHE_DB.md`, `../agents/AGENT_TESTING_QA.md` | Must exist before demo |
| Historical evaluation | `../agents/AGENT_ML_EVALUATION.md` | `../agents/AGENT_API_INGESTION.md`, `../agents/AGENT_NOTEBOOK_EDA.md` | Optional but strong |
| Optional enrichments | `../agents/AGENT_ENRICHMENT_APIS.md` | `../agents/AGENT_STREAMLIT_UI.md`, `../agents/AGENT_RELIABILITY_DEMO.md` | Only after core works |
| Notebook profiling | `../agents/AGENT_NOTEBOOK_EDA.md` | `../agents/AGENT_SCHEMA_VALIDATION.md`, `../agents/AGENT_ML_EVALUATION.md` | Quick insight work |
| QA and smoke tests | `../agents/AGENT_TESTING_QA.md` | `../agents/AGENT_RELIABILITY_DEMO.md`, `../agents/AGENT_STREAMLIT_UI.md` | Pre-demo |
| Pitch/docs | `../agents/AGENT_PITCH_DOCS.md` | `../agents/AGENT_PROJECT_LEAD.md`, `../agents/AGENT_SAFETY_DOMAIN.md` | Last mile |
| Wording/disclaimers | `../agents/AGENT_SAFETY_DOMAIN.md` | owning feature agent | Always include for public text |
| Visual polish | `../agents/AGENT_VISUAL_STORYTELLING.md` | `../agents/AGENT_STREAMLIT_UI.md`, `../agents/AGENT_PITCH_DOCS.md` | After UI is stable |
