from graphviz import Digraph


def build_architecture_diagram(include_artifact_registry: bool = True) -> Digraph:
    """
    High-level system diagram:
    GitHub -> Cloud Build -> (GCS) -> Vertex AI Pipelines -> Scheduler -> Monitoring/Alerting

    If include_artifact_registry=True, show optional container image build/push.
    """
    g = Digraph()
    g.attr(rankdir="LR")

    g.node("GitHub", "GitHub\n(dev/test/prod branches)", shape="box")
    g.node("CB", "Cloud Build\n(trigger + steps)", shape="box")
    g.node("GCS", "GCS Buckets\n(SQL + config + compiled spec)", shape="box")
    g.node("Vertex", "Vertex AI Pipelines\n(template/job)", shape="box")
    g.node("Sched", "Scheduler\n(Cron / cadence)", shape="box")
    g.node("Obs", "Monitoring & Alerting\n(Logs/metrics/on-failure)", shape="box")

    g.edge("GitHub", "CB", label="push/merge")
    g.edge("CB", "GCS", label="upload artifacts")
    g.edge("CB", "Vertex", label="deploy/update")
    g.edge("Sched", "Vertex", label="runs on schedule")
    g.edge("Vertex", "Obs", label="logs/metrics")

    if include_artifact_registry:
        g.node("AR", "Artifact Registry\n(container images)", shape="box")
        g.edge("CB", "AR", label="optional: build/push")
        g.edge("Vertex", "AR", label="pull images")

    return g


def build_cicd_cycle_diagram(
    include_docker_lane: bool = True,
    include_quality_gates: bool = True,
    include_observability: bool = True,
) -> Digraph:
    """
    Circular CI/CD loop intended for data scientists.
    Uses a 'cycle' with optional lanes for Docker, gates, and ops.
    """
    g = Digraph(engine="circo")  # circular layout
    g.attr(overlap="false")

    # Core loop nodes
    g.node("1", "1) GitHub\npush to branch", shape="box")
    g.node("2", "2) Cloud Build\ntrigger fires", shape="box")
    g.node("3", "3) Cloud Build\nruns cloudbuild.yaml", shape="box")
    g.node("4", "4) Deploy Vertex\npipeline template/job", shape="box")
    g.node("5", "5) Schedule\n(run cadence)", shape="box")
    g.node("6", "6) Iterate\nchange code/config", shape="box")

    # Core edges (cycle)
    g.edge("1", "2")
    g.edge("2", "3")
    g.edge("3", "4")
    g.edge("4", "5")
    g.edge("5", "6")
    g.edge("6", "1", label="next change")

    if include_quality_gates:
        g.node("G", "Quality gates\n(lint/test/validate)", shape="note")
        g.edge("2", "G", style="dashed")
        g.edge("G", "3", style="dashed")

    if include_docker_lane:
        g.node("D", "Optional Docker lane\nbuild/push images", shape="note")
        g.edge("3", "D", style="dashed")
        g.edge("D", "4", style="dashed")

    if include_observability:
        g.node("O", "Ops loop\nmonitor + alert + rollback", shape="note")
        g.edge("4", "O", style="dashed")
        g.edge("O", "6", style="dashed")

    return g
