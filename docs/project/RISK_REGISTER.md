# RISK_REGISTER

Use this file to track practical project risks and their fallback plans.

## Scale

- **Likelihood:** low / medium / high
- **Impact:** low / medium / high
- **Response type:** avoid / reduce / accept / transfer

| ID | Risk | Likelihood | Impact | Trigger | Response type | Mitigation | Fallback owner |
|---|---|---|---|---|---|---|---|
| R-001 | Live feed unavailable during demo | medium | high | fetch timeouts or empty upstream response | reduce | keep local cache and replay mode always ready | Reliability Demo |
| R-002 | Upstream schema changes unexpectedly | medium | high | parser failures on new payloads | reduce | save raw payloads, validate explicitly, fail loudly in logs | Schema Validation |
| R-003 | SQLite schema drifts from parser output | medium | medium | insert errors or missing columns | reduce | document data contracts and keep migration notes | Cache DB |
| R-004 | Baseline score is hard to explain | medium | high | judges ask why a record ranked first and the answer is vague | reduce | keep score transparent and include factor breakdowns | Feature Baseline |
| R-005 | Public wording sounds like official warning authority | low | high | README or UI text overclaims | avoid | safety review all public text before release | Safety Domain |
| R-006 | Optional enrichments become critical path | medium | medium | UI breaks or slows badly when enrichment is down | avoid | isolate enrichments behind timeouts and optional panels | Enrichment APIs |
| R-007 | UI too busy for a short demo | medium | medium | presenter cannot explain screen quickly | reduce | simplify layout and keep top-ranked story dominant | Visual Storytelling |
| R-008 | Historical labels are weak or noisy | high | medium | evaluation results are unstable or hard to trust | accept | keep ML optional and compare to transparent baseline | ML Evaluation |
| R-009 | Hidden manual setup steps break portability | medium | high | app only runs on one machine | avoid | document all commands and test on a clean local path | Repo Bootstrap |
| R-010 | Team starts polish work before MVP is stable | high | medium | many cosmetic commits, core path still fragile | avoid | enforce phase order and task router discipline | Project Lead |
| R-011 | Replay mode becomes stale after schema changes | medium | high | cached data no longer renders in UI | reduce | update replay tests whenever data contracts change | Reliability Demo |
| R-012 | Demo depends on internet quality | medium | high | laggy live requests or failed enrichments | reduce | present from replay mode by default if the environment is risky | Project Lead |

## Active risk review ritual

Before moving to a new phase, review:

1. any risk now rated high impact
2. whether the fallback really exists in code, not only in theory
3. whether a new optional feature introduced a new failure mode

## Add-entry template

### R-000
- **Risk:**
- **Likelihood:**
- **Impact:**
- **Trigger:**
- **Response type:**
- **Mitigation:**
- **Fallback owner:**
- **Notes:**
