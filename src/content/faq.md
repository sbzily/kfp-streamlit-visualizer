### Where does the code run?
In Vertex AI Pipelines jobs. Each step runs in its configured execution environment (often container-based).

### What happens when I change SQL/config?
A GitHub push triggers Cloud Build, which uploads artifacts and compiles/deploys an updated pipeline template.

### Why separate dev/test/prod?
To prevent experimental changes from impacting production data and to keep permissions scoped.

### What happens on failure?
The job fails, logs are available, and alerts should fire. Enterprise setups also define retry rules and rollback steps.

### Do we need Docker?
Not always. If you have custom components, it’s the standard approach. If you’re mostly orchestrating managed services, you can sometimes treat images as already-managed.

### Can we run this without Vertex?
Yes. The same concepts map to Airflow, Prefect, or Dagster. Vertex just provides a managed control plane.

### What do we show on a CV?
Focus on repeatability: CI/CD, versioned artifacts, branch promotion, and observability practices.
