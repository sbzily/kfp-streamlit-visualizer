This project shows a practical deployment loop for **Vertex AI Pipelines**.

### What is happening
- **GitHub** is the source of truth for SQL, config, and pipeline code.
- **Cloud Build** runs on branch-based triggers and executes your `cloudbuild.yaml`.
- Build outputs (SQL, configs, compiled pipeline spec) land in **GCS buckets** per environment.
- **Vertex AI Pipelines** uses the compiled spec to run the pipeline.
- A **scheduler** triggers jobs on a cadence.
- **Monitoring/alerting** is the safety net: you do not want silent failures.

### Artifact inventory
- Source: SQL, config, and pipeline code in GitHub.
- Build outputs: compiled pipeline template + versioned artifacts in GCS.
- Runtime: container images in Artifact Registry (optional).
- Execution: Vertex AI Pipeline jobs, logs, and metrics.

### Control plane vs data plane
- **Control plane**: GitHub, Cloud Build, Vertex AI (orchestrates, schedules, tracks).
- **Data plane**: BigQuery, Dataflow, GCS, and Custom Jobs (does the heavy lifting).

### Why this layout works in production
- Enforces environment separation with clear promotion steps.
- Keeps artifacts versioned by git SHA for traceability.
- Makes it easy to audit deployments and roll back safely.
