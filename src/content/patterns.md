This page collects common data engineering patterns that show up in production pipelines.
Use the selector to explore how each pattern fits into a KFP-style DAG.

### Why patterns matter
- They make trade-offs explicit: cost, freshness, and operational complexity.
- They surface where state lives (watermarks, CDC logs, snapshots).
- They define the failure modes your on-call rotation will face.

### Patterns in this demo
- Incremental load with a watermark
- Partitioned backfill
- CDC merge into a serving table
- Snapshot diff and apply

### How to read the diagrams
- Each box maps to a pipeline component or managed service call.
- Dashed nodes are optional but common in production.
