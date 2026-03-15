# PRESENTATION

## Purpose

Judge-ready 3-4 minute presentation plan for the Offshore Quake & Tsunami Triage project.

This file includes:
- 8-slide outline
- exact live demo click path
- short speaker script
- fallback script if live data fails

## Slide Outline (6-8 slides)

### Slide 1 - Problem

Title: "Triage, Not Prediction"

Key points:
- Seismic events arrive continuously; analysts need fast prioritization.
- Teams need explainable ranking, not black-box alarms.
- Goal: reduce time to first human review.

Speaker notes (15-20s):
"We built a triage support tool for incoming offshore earthquakes. It does not replace official warning agencies. It helps analysts decide what to review first."

### Slide 2 - Data and Architecture

Title: "Public Data to Explainable Queue"

Key points:
- Source: USGS feed (live) plus replay sample (offline-safe).
- Pipeline: ingest -> normalize -> SQLite cache -> scoring -> Streamlit UI.
- Reliability path: live mode with fallback to replay mode.

Speaker notes (20-25s):
"The system ingests USGS events, normalizes them, stores them locally, computes a transparent score, and renders a review queue. If live fetch fails, replay keeps the demo and workflow stable."

### Slide 3 - Scoring Logic

Title: "Explainable 0-100 Triage Score"

Key points:
- Magnitude (Mw): 0-50
- Depth: 0-30 (shallower = higher attention)
- Recency: 0-20 (newer = higher attention)
- Output includes explanation text and per-factor breakdown.

Speaker notes (20-25s):
"Each event gets a 0-100 priority score from three transparent factors. Reviewers can inspect exactly why an event is ranked high."

### Slide 4 - Live UI Walkthrough

Title: "From Queue to Decision Context"

Key points:
- Ranked Queue shows top items first.
- Map uses score colors for quick visual triage.
- Event Detail explains score and links to official alert source.

Speaker notes (15-20s):
"The queue surfaces priority, the map gives spatial context, and the detail panel gives explainability plus direct links to official sources."

### Slide 5 - Reliability and Replay

Title: "Demo-Safe by Design"

Key points:
- Replay mode keeps app usable offline.
- Fallback path protects against API issues.
- Same UI and operator flow in live and replay modes.

Speaker notes (15-20s):
"We designed reliability as a first-class feature so degraded network conditions do not break the analyst workflow."

### Slide 6 - Phase 6 Evaluation

Title: "Measured, Not Assumed"

Key points:
- Optional ML evaluation run on historical cached events.
- Metrics artifact surfaced in app diagnostics panel.
- Baseline remains explainable triage-first behavior.

Speaker notes (15-20s):
"We evaluated a lightweight classifier and surface PR-AUC and Precision@K, but we keep the product framing grounded: this is triage support."

### Slide 7 - Safety and Boundaries

Title: "What This Is / What This Is Not"

Key points:
- Is: priority support for human analysts.
- Is not: official warning authority.
- Official alerts remain authoritative: tsunami.gov.

Speaker notes (15-20s):
"We intentionally use calm, bounded language. The app prioritizes attention. Official agencies remain authoritative."

### Slide 8 - Next Steps

Title: "From Demo to Deployment Readiness"

Key points:
- Expand historical coverage and QA reporting.
- Add curated screenshot pack and release bundle.
- Complete final safety wording signoff and freeze scope.

Speaker notes (10-15s):
"The MVP is stable and demo-safe; the next step is packaging and governance polish for release readiness."

## Exact Demo Click Path (3-4 minutes)

### Pre-demo setup

1. Start app: `streamlit run src/app.py`
2. Confirm DB path: `data/events.sqlite`
3. Decide mode:
- Live demo: Replay toggle OFF
- Safe demo: Replay toggle ON

### Live sequence

1. In sidebar, click `Load events now`.
2. Point to success message: loaded count + source.
3. On main panel, show top rows in `Ranked Queue`.
4. Highlight one high-score event.
5. Use `Select event` in Event Detail.
6. Explain `Score`, `Mw`, `Depth`, and `Why this score`.
7. Point to `Official alerts` link.
8. Briefly show `Global Event Map` color legend.
9. (Optional) Enable `Show marine wave context (optional)` and show context.

### Reliability moment

1. Toggle `Replay mode (local sample)` ON.
2. Click `Load events now` again.
3. State that same workflow remains usable without live network dependence.

### Close

1. Re-state boundary: triage support, not official warning output.
2. Re-state value: faster first review, transparent reasoning.

## 3-4 Minute Speaker Script (Condensed)

"We built an offshore earthquake triage support tool to help analysts prioritize review under time pressure. The app ingests USGS events, normalizes and caches them locally, then computes an explainable score using magnitude, depth, and recency. In the queue, we can immediately focus on the highest-priority items. In Event Detail, we can see exactly why an event is ranked high, and we include direct links to official sources. The map adds fast spatial context. Reliability is built in: if live data is unstable, replay mode keeps the same interface and workflow working. We also run optional model evaluation and surface metrics, but we keep the product framing responsible: this tool prioritizes human attention and does not replace official warning agencies."

## Failure/Backup Script (30 seconds)

If live ingest fails:
- "We are switching to replay mode. Same interface, same ranking logic, same review path."
- Toggle replay ON, click `Load events now`, continue demo unchanged.

If optional enrichment fails:
- "Optional context is non-critical by design; core triage remains fully available."

## Claims to Use and Avoid

Use:
- triage support
- priority for human review
- explainable ranking
- official alerts are authoritative

Avoid:
- predicts tsunamis
- guarantees risk
- replaces official alerts
