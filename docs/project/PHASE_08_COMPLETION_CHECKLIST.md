# PHASE_08_COMPLETION_CHECKLIST

Status date: 2026-03-15
Scope: release-readiness checklist derived from `docs/phases/PHASE_08_PITCH_QA_AND_RELEASE.md`

## Overall status

- Phase 8 completion: `Partial`
- Estimated completion: `~60%`
- Core app/demo path: `Ready`
- Release package quality gate: `Not yet passed`

## Task-by-task status

### 8.1 Final README and architecture summary

- [x] README exists and includes run commands (`README.md`)
- [x] Live and replay modes documented (`README.md`)
- [ ] Architecture summary section explicitly written for judges (data flow diagram/text block)

Evidence:
- `README.md`
- `src/ingest_usgs.py`
- `src/run_ingest_pipeline.py`
- `src/app.py`

### 8.2 Slide outline and demo script

- [x] Demo script/run flow exists (`docs/project/DEMO_RUNBOOK.md`)
- [ ] Slide outline file (6-8 slides) exists
- [ ] Final 3-4 minute spoken script aligned to exact UI clicks

Evidence:
- Present: `docs/project/DEMO_RUNBOOK.md`
- Missing: `docs/project/PRESENTATION.md` (or equivalent)

### 8.3 Pre-demo QA pass

- [x] Automated tests passing: `22 passed, 1 warning`
- [x] Reliability/replay tests exist (`tests/test_reliability.py`)
- [ ] Explicit pre-demo QA run record captured (date/time + pass/fail notes)

Evidence:
- `tests/`
- `docs/project/DEMO_RUNBOOK.md`

### 8.4 Final wording review (safety)

- [x] UI includes safety language and official-source framing (`src/app.py`)
- [x] Safety agent standards exist (`docs/agents/AGENT_SAFETY_DOMAIN.md`)
- [ ] Written safety signoff note created (README or project doc)

Evidence:
- `src/app.py`
- `docs/agents/AGENT_SAFETY_DOMAIN.md`

### 8.5 Freeze release package

- [x] Scope and phase docs exist (`docs/phases/`, `docs/project/`)
- [x] Evaluation artifact exists (`artifacts/metrics_latest.json`)
- [ ] Screenshot pack saved for fallback demo path
- [ ] Release manifest/checklist marked complete and frozen

Evidence:
- `artifacts/metrics_latest.json`
- Missing: screenshot artifacts in `artifacts/`

## Release gate summary

Hard gate items before calling Phase 8 complete:

1. Create `docs/project/PRESENTATION.md` with 6-8 slide outline and exact demo click path.
2. Capture at least 2 fallback screenshots in `artifacts/` (queue view + detail view).
3. Add a one-page QA run record in `docs/project/` (what was tested, result, timestamp).
4. Add a safety wording signoff section in `README.md` or a dedicated note in `docs/project/`.
5. Mark this checklist fully complete and freeze scope.

## Suggested owners (agent mapping)

- Pitch and slides: `docs/agents/AGENT_PITCH_DOCS.md`
- QA pass record: `docs/agents/AGENT_TESTING_QA.md`
- Safety signoff: `docs/agents/AGENT_SAFETY_DOMAIN.md`
- Release freeze: `docs/agents/AGENT_PROJECT_LEAD.md`

## Completion declaration template

When all unchecked items are complete, append:

- Declared by:
- Date:
- Scope frozen at commit:
- Demo mode used in final rehearsal (live/replay):
- Remaining known limitations (if any):
