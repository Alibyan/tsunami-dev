# DECISION_LOG

Use this file to record meaningful build decisions as the project evolves.

The goal is not bureaucracy. The goal is to prevent the team from re-arguing the same thing and to preserve the reasoning behind important tradeoffs.

## How to use

Add one entry whenever you make a decision that affects:

- architecture
- scope
- data sources
- evaluation approach
- claims or wording
- fallback behavior
- demo flow

## Decision entry template

### D-000
- **Date:** YYYY-MM-DD
- **Phase:**
- **Decision:**
- **Status:** proposed / accepted / superseded
- **Owner:**
- **Context:**
- **Options considered:**
- **Chosen option:**
- **Why this option won:**
- **Tradeoffs accepted:**
- **Files affected:**
- **Follow-up required:**

---

## Starter decisions for this project

### D-001
- **Date:** 2026-03-14
- **Phase:** Phase 0 / Phase 1
- **Decision:** Keep runtime simple and local-first.
- **Status:** accepted
- **Owner:** Project Lead
- **Context:** The project needs to be shippable in hackathon conditions.
- **Options considered:**
  - heavier service architecture
  - simple Python app with local cache
- **Chosen option:** Python + requests + SQLite + Streamlit
- **Why this option won:** Fastest path to a stable MVP with an understandable local demo.
- **Tradeoffs accepted:** Less scalability and fewer deployment features in exchange for speed and clarity.
- **Files affected:** repo bootstrap, cache, UI, runbook
- **Follow-up required:** Keep optional services out of the critical path.

### D-002
- **Date:** 2026-03-14
- **Phase:** Phase 1
- **Decision:** Use MCP as a build-time helper only.
- **Status:** accepted
- **Owner:** MCP Workflow
- **Context:** MCP is useful for file editing, reference lookup, and local database inspection, but should not become a production dependency.
- **Options considered:**
  - MCP in runtime flow
  - MCP only during development
- **Chosen option:** MCP only during development
- **Why this option won:** It preserves a clean production path and keeps the app portable.
- **Tradeoffs accepted:** Some convenience is given up in exchange for a simpler runtime.
- **Files affected:** agent docs, repo setup, README
- **Follow-up required:** Enforce this in prompts and agent rules.

### D-003
- **Date:** 2026-03-14
- **Phase:** Phase 3
- **Decision:** Start with an explainable triage score before optional ML.
- **Status:** accepted
- **Owner:** Feature Baseline
- **Context:** The MVP needs an auditable score even if historical labels are imperfect.
- **Options considered:**
  - immediate lightweight model
  - transparent rule-based score first
- **Chosen option:** Transparent baseline first
- **Why this option won:** Faster to explain, easier to debug, safer for demo claims.
- **Tradeoffs accepted:** Lower possible accuracy ceiling at first.
- **Files affected:** baseline scoring, UI explanation panel, pitch docs
- **Follow-up required:** Compare future ML additions against the baseline rather than replacing it blindly.

### D-004
- **Date:** 2026-03-14
- **Phase:** Phase 4 / Phase 5
- **Decision:** The demo must work in replay mode.
- **Status:** accepted
- **Owner:** Reliability Demo
- **Context:** Live feeds can fail or change during the demo.
- **Options considered:**
  - live-only demo
  - live plus offline replay fallback
- **Chosen option:** live plus replay fallback
- **Why this option won:** The team keeps a stable demo path even if APIs fail.
- **Tradeoffs accepted:** Slightly more build work early on.
- **Files affected:** cache, sample payloads, Streamlit app, runbook
- **Follow-up required:** Keep replay mode up to date as schemas evolve.

### D-005
- **Date:** 2026-03-14
- **Phase:** All public-facing phases
- **Decision:** Describe the system as triage support, not official prediction or warning.
- **Status:** accepted
- **Owner:** Safety Domain
- **Context:** The project ranks events for attention; it does not replace official agencies.
- **Options considered:**
  - aggressive predictive wording
  - support-tool wording with clear claim boundaries
- **Chosen option:** support-tool wording
- **Why this option won:** More honest, safer, and easier to defend in a demo.
- **Tradeoffs accepted:** Less flashy positioning.
- **Files affected:** UI text, README, slides, runbook, disclaimers
- **Follow-up required:** Review all public copy before release.
