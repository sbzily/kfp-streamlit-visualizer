### The loop (high level)
1. **GitHub push** to an environment branch (dev/test/prod).
2. **Cloud Build trigger** fires for that branch.
3. Cloud Build runs the steps in `cloudbuild.yaml`:
   - validate/lint (recommended)
   - upload SQL + configs to the env bucket
   - compile the pipeline spec/template
4. **Deploy/update** the Vertex AI pipeline template (or submit a job).
5. **Schedule** it to run (and define concurrency/catch-up behaviour).
6. **Iterate**: changes go back through GitHub.

### What makes it “enterprise-grade”
- Quality gates before deployment (lint/tests/validation)
- Least-privilege IAM (separate build vs runtime identities)
- Monitoring + alerting + rollback story
- Versioning (git SHA ties to compiled templates and artifacts)

### What gets versioned
- `cloudbuild.yaml` stays stable; inputs change (SQL/config code).
- A single git SHA maps to a compiled template and uploaded artifacts.
- Optional: container image tags pin the runtime environment.

### Promotion models
- **Promote artifacts**: build once, deploy the same template to test/prod.
- **Rebuild per env**: repeat build steps for each environment (safer, slower).
