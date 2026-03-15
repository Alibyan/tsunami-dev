# DATA_CONTRACTS

This file defines the expected data shapes passed between major layers of the app.

The purpose is to reduce churn between ingestion, validation, storage, scoring, and UI.

## Contract rules

- Every contract should have a stable field list.
- Optional fields must be clearly marked.
- Units and time formats must be explicit.
- Unknown fields should not silently flow across layers.
- Public UI contracts should contain safe wording-ready data, not raw surprises.

---

## 1. Raw event payload contract

Source: upstream earthquake or event feed

This is the raw JSON payload as received.

### Rules
- store a copy of the raw payload when practical
- do not treat raw field names as stable forever
- record source and retrieval timestamp alongside payloads

### Suggested wrapper

```json
{
  "source_name": "usgs_feed",
  "retrieved_at_utc": "2026-03-14T12:34:56Z",
  "payload": {"...raw upstream object...": "..."}
}
```

---

## 2. Normalized event record contract

Source: output of parsing and validation

This is the canonical event row used by cache, scoring, and UI.

### Required fields

```json
{
  "event_id": "string",
  "source": "string",
  "observed_at_utc": "ISO-8601 string",
  "updated_at_utc": "ISO-8601 string",
  "latitude": 0.0,
  "longitude": 0.0,
  "depth_km": 0.0,
  "magnitude": 0.0,
  "place": "string",
  "status": "string",
  "detail_url": "string"
}
```

### Optional fields

```json
{
  "felt_count": 0,
  "mmi": 0.0,
  "alert_level": "string",
  "tsunami_flag": 0,
  "event_type": "string",
  "title": "string"
}
```

### Rules
- timestamps must be UTC
- latitude and longitude must be numeric
- depth is in kilometers
- missing optional fields should stay null rather than inventing defaults unless defaults are intentional
- event_id must be stable enough for dedupe and upsert

---

## 3. Cached event row contract

Source: SQLite storage layer

This is the persisted version of the normalized event.

### Required metadata

```json
{
  "event_id": "string",
  "ingested_at_utc": "ISO-8601 string",
  "raw_payload_path": "string or null",
  "normalized_json": "JSON string or structured columns",
  "source": "string"
}
```

### Rules
- cache rows must support replay mode
- cache writes should be idempotent when the same event reappears
- updates should preserve the newest version intentionally

---

## 4. Feature row contract

Source: baseline scoring or ML prep

This is the feature table shape used to compute ranking.

### Suggested fields

```json
{
  "event_id": "string",
  "magnitude": 0.0,
  "depth_km": 0.0,
  "tsunami_flag": 0,
  "felt_count": 0,
  "mmi": 0.0,
  "recency_minutes": 0.0,
  "distance_proxy_km": 0.0,
  "alert_level_ord": 0,
  "missingness_count": 0
}
```

### Rules
- all derived fields must document how they were computed
- feature generation must be reproducible from cached records
- if a feature is heuristic, label it as such

---

## 5. Ranked event contract

Source: baseline scoring or model output

This is what the UI should consume when showing triage output.

### Required fields

```json
{
  "event_id": "string",
  "triage_score": 0.0,
  "rank": 1,
  "score_version": "string",
  "explanation_factors": [
    {"name": "magnitude", "value": 7.1, "impact": "+high"}
  ]
}
```

### Companion fields

```json
{
  "headline": "string",
  "summary": "string",
  "place": "string",
  "observed_at_utc": "ISO-8601 string",
  "detail_url": "string"
}
```

### Rules
- the ranked event should be sufficient for rendering the queue and detail card
- score explanations must be deterministic and inspectable
- wording should imply prioritization for review, not official threat certainty

---

## 6. UI detail contract

Source: ranked event + optional enrichments

This is the final display-layer contract.

### Suggested fields

```json
{
  "event_id": "string",
  "headline": "string",
  "summary": "string",
  "facts": {
    "magnitude": 0.0,
    "depth_km": 0.0,
    "time_utc": "ISO-8601 string",
    "location": "string"
  },
  "score": {
    "value": 0.0,
    "rank": 1,
    "version": "string"
  },
  "explanations": ["text"],
  "links": [{"label": "Official detail", "url": "string"}],
  "enrichments": []
}
```

### Rules
- links should be explicit and safe
- optional enrichments must not be required for the contract to render
- empty lists are preferred over missing keys in the UI layer when practical

---

## Contract change protocol

Whenever a contract changes:

1. update this file
2. update the affected parser, DB, or UI code
3. confirm replay mode still works
4. note the change in `DECISION_LOG.md` if it is meaningful
