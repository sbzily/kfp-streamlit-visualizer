Scheduling is not the end — it’s the start of operations.

### Minimum ops story
- Where do logs go? (Cloud Logging)
- How do we detect failures? (alerts on failed pipeline jobs)
- Who gets notified? (on-call / Slack / email)
- What’s the rollback? (redeploy last known good template)

### Data engineering specifics
- Idempotency: reruns don’t corrupt targets
- Backfills: controlled historical reprocessing
- Data quality: “stop the line” behaviour when checks fail
- Concurrency: prevent overlapping runs from clobbering state

### SLOs worth tracking
- Freshness: how late is the data compared to the SLA.
- Completeness: percent of expected records delivered.
- Cost: run duration and spend per run.
