You’re already using:
- separate **branches** (dev/test/prod)
- separate **buckets** per environment

That’s a good start.

### Recommended additions
- Separate **service accounts** per environment (least privilege).
- Prefer separate **GCP projects** for prod vs non-prod if your org does that.
- Protect the prod branch and require PR approvals.
- Tie deployments to immutable versions (git SHA → artifact version → pipeline template version).

### Promotion options
- **Build once, promote artifacts**: fastest feedback, strongest traceability.
- **Rebuild per environment**: safest when configs differ a lot across envs.

### Why this matters
Promotion is not just “copy code to prod.” It’s a controlled change with traceability and a rollback path.
