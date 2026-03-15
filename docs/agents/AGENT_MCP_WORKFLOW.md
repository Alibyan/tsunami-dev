# AGENT_MCP_WORKFLOW

## Mission

Use free MCP servers effectively for build-time productivity while keeping the production application independent from MCP.

## When to use

- When setting up Copilot + VS Code workflow
- When choosing which MCP servers to use
- When an agent needs file ops, docs lookup, or DB inspection
- When there is a risk of relying on MCP at runtime

## Inputs

- Current tool needs
- Available free MCP servers
- Security or environment constraints
- Current build task

## Outputs

- A minimal MCP stack recommendation
- Clear guidance on which MCP server to use for each task
- A rule set separating build-time from runtime usage
- Safer alternatives when MCP adds unnecessary complexity

## Hard rules

- Default to filesystem + fetch; add sqlite only if it improves speed or debugging
- Do not design the deployed app to depend on MCP connectivity
- Avoid adding extra servers just because they are available
- Treat fetched docs as references, not runtime data sources
- Keep the system understandable to a hackathon judge in one sentence

## Workflow

- Map build tasks to MCP tools
- Use filesystem MCP for creating files, editing docs, saving artifacts, and organizing outputs
- Use fetch MCP for documentation lookup and endpoint reference checks
- Use sqlite MCP to inspect the local cache, validate schema, and debug records
- Write down the exact boundary between MCP-assisted development and the shipped app
- Remove or avoid any workflow that makes the demo depend on a live MCP server

## Handoff rules

- Hand off repository wiring to `AGENT_REPO_BOOTSTRAP.md`
- Hand off schema or DB details to `AGENT_CACHE_DB.md`
- Hand off documentation output to `AGENT_PITCH_DOCS.md`

## Done criteria

- The team can explain why each MCP server exists
- The runtime application can run without MCP
- No agent is trying to solve every problem with tooling

## Agent prompt block

Recommended free MCP stack for this project:

- filesystem: create and edit code, markdown, demo assets, and cached snapshots
- fetch: pull endpoint docs and API references during build
- sqlite: inspect `events.sqlite`, verify rows, and debug feature pipelines

One-line principle:

**MCP helps build the project; MCP is not the product.**
