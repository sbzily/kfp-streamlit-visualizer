This project shows a practical deployment loop for **Vertex AI Pipelines**.

### What’s happening
- **GitHub** is the source of truth for SQL/config/pipeline code.
- **Cloud Build** runs on branch-based triggers and executes your `cloudbuild.yaml`.
- Build outputs (SQL, configs, compiled pipeline spec) land in **GCS buckets** per environment.
- **Vertex AI Pipelines** uses the compiled spec to run the pipeline.
- A **scheduler** triggers jobs on a cadence.
- **Monitoring/alerting** is the safety net: you don’t want “silent failures.”
