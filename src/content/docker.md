Docker shows up in CI/CD for one reason: **reproducibility**.

### What Docker is doing here
Vertex AI Pipelines ultimately executes steps in containerized environments. Building and pushing a Docker image lets you package:
- your component code
- Python dependencies
- system dependencies

That makes the runtime consistent across dev/test/prod and across time.

### Two valid patterns
**A) Compile-only (lighter)**
- Works when your runtime images are already stable/published or when steps mostly orchestrate managed services.
- CI uploads artifacts + compiles pipeline spec + deploys.

**B) Build + push + compile (more complete)**
- Preferred when you have custom components.
- CI builds images → pushes to Artifact Registry → compiles spec referencing those images → deploys/schedules.

### What to tell data scientists
- Docker is not “extra complexity for fun.”
- It’s how you guarantee the same code runs the same way tomorrow as it does today.
