# TASK_DEPENDENCY_MATRIX

This file shows the major dependencies between project tasks.

Use it before starting work that feels attractive but may actually be blocked.

## Dependency legend

- **hard dependency**: must be completed first
- **soft dependency**: strongly recommended first
- **parallel possible**: can proceed carefully in parallel

| Task | Depends on | Dependency type | Why |
|---|---|---|---|
| Repo structure and environment | none | hard | Starting point |
| MCP policy and dev workflow | repo structure and environment | soft | Easier to keep boundaries clean |
| Live feed fetch | repo structure and environment | hard | Needs scripts and dependencies |
| Raw payload capture | live feed fetch | hard | No payload without fetch |
| Parsing and normalization | raw payload capture | hard | Needs real payload examples |
| Schema validation rules | parsing and normalization | hard | Must know normalized shape |
| SQLite schema | parsing and normalization | soft | Best defined after record shape is known |
| Upsert and cache logic | SQLite schema, parsing and normalization | hard | Needs table design and stable row format |
| Replay mode reads | upsert and cache logic | hard | Needs cached records to replay |
| Baseline score | parsing and normalization | hard | Needs stable fields |
| Score explanation panel | baseline score | hard | Needs factor outputs |
| Dashboard list and map | replay mode reads or live reads | hard | Needs readable records |
| Empty and error states | dashboard list and map | soft | Best added once UI exists |
| Reliability fallback logic | live feed fetch, replay mode reads | hard | Needs both live and offline paths |
| Smoke tests | baseline score, cache logic, UI entry points | soft | More useful once key surfaces exist |
| Historical backfill | cache schema | soft | Better once storage path is stable |
| Backtest evaluation | historical backfill, baseline score | hard | Needs history and a measurable baseline |
| Optional ML | backtest evaluation | soft | Should not happen before baseline is measured |
| Optional enrichments | dashboard list and map, reliability fallback logic | soft | Core demo should be stable first |
| README and architecture summary | repo structure and MVP path | soft | Better once the shape is real |
| Demo script | dashboard, reliability path, safe wording | hard | Needs real click path |
| Release packaging | demo script, smoke tests, README | hard | Final polish step |

## Critical path

The MVP critical path is:

1. repo setup
2. live fetch
3. payload capture
4. parsing and normalization
5. SQLite cache
6. baseline score
7. UI list and detail flow
8. replay mode
9. safe wording
10. demo runbook

## Anti-patterns to avoid

Do not start these too early:

- optional enrichments before replay mode exists
- ML before the baseline is measurable
- polished visuals before the UI click path is stable
- release packaging before smoke testing
- extra APIs before the core ingest is trustworthy
