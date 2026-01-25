from graphviz import Digraph


def build_architecture_diagram(include_artifact_registry: bool = True) -> Digraph:
    """
    High-level system diagram:
    GitHub -> Cloud Build -> (GCS) -> Vertex AI Pipelines -> Scheduler -> Monitoring/Alerting

    If include_artifact_registry=True, show optional container image build/push.
    """
    g = Digraph()
    g.attr(
        rankdir="TB",
        bgcolor="#f8fafc",
        nodesep="0.2",
        ranksep="0.25",
        pad="0.08",
        ratio="compress",
        size="5.5,6.5!",
        dpi="65",
    )
    g.attr(
        "node",
        style="filled",
        fontname="Helvetica",
        color="#0f5fa8",
        fontcolor="#0b1f44",
        fillcolor="#e6f0fb",
        penwidth="1.4",
        fontsize="15",
        margin="0.06,0.04",
    )
    g.attr("edge", color="#5b7bc6", penwidth="1.0", fontsize="15")

    g.node("GitHub", "GitHub\n(dev/test/prod)", shape="box", fillcolor="#e8f5e9")
    g.node("CB", "Cloud Build\n(CI/CD)", shape="box", fillcolor="#e3f2fd")
    g.node("GCS", "GCS Buckets\n(artifacts)", shape="box", fillcolor="#fff8e1")
    g.node("Vertex", "Vertex Pipelines\n(KFP Components with ETL/ELT Steps)", shape="box", fillcolor="#ede7f6")
    g.node("Sched", "Scheduler", shape="box", fillcolor="#fce4ec")
    g.node("Obs", "Monitoring\n(alerts)", shape="box", fillcolor="#f3e5f5")

    g.edge("GitHub", "CB", label="push/merge")
    g.edge("CB", "GCS", label="upload artifacts")
    g.edge("CB", "Vertex", label="deploy/update")
    g.edge("Sched", "Vertex", label="runs on schedule")
    g.edge("Vertex", "Obs", label="logs/metrics")

    if include_artifact_registry:
        g.node("AR", "Artifact Registry\n(images)", shape="box", fillcolor="#e0f7fa")
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


PATTERN_DEFINITIONS = {
    "Incremental Load (Watermark)": {
        "nodes": {
            "watermark": "Read Watermark",
            "extract": "Extract Delta",
            "validate": "Validate",
            "merge": "Merge Upsert",
            "update": "Update Watermark",
        },
        "edges": [
            ("watermark", "extract"),
            ("extract", "validate"),
            ("validate", "merge"),
            ("merge", "update"),
        ],
        "anchors": {"quality": "validate", "metrics": "merge", "metadata": "update"},
    },
    "Backfill (Partitioned)": {
        "nodes": {
            "plan": "Plan Partitions",
            "extract": "Extract Partition",
            "transform": "Transform",
            "load": "Load",
            "publish": "Publish Metrics",
        },
        "edges": [
            ("plan", "extract"),
            ("extract", "transform"),
            ("transform", "load"),
            ("load", "publish"),
        ],
        "anchors": {"quality": "transform", "metrics": "publish", "metadata": "plan"},
    },
    "CDC Merge": {
        "nodes": {
            "read": "Read Change Feed",
            "dedupe": "De-duplicate",
            "merge": "Apply Merge",
            "audit": "Write Audit Log",
        },
        "edges": [
            ("read", "dedupe"),
            ("dedupe", "merge"),
            ("merge", "audit"),
        ],
        "anchors": {"quality": "dedupe", "metrics": "audit", "metadata": "merge"},
    },
    "Snapshot Diff": {
        "nodes": {
            "snapshot": "Extract Snapshot",
            "compare": "Compare Snapshots",
            "apply": "Apply Diffs",
            "publish": "Publish Metrics",
        },
        "edges": [
            ("snapshot", "compare"),
            ("compare", "apply"),
            ("apply", "publish"),
        ],
        "anchors": {"quality": "compare", "metrics": "publish", "metadata": "snapshot"},
    },
}


def build_pattern_diagram(
    pattern: str,
    include_quality_checks: bool = True,
    include_metrics: bool = True,
    include_metadata: bool = True,
) -> Digraph:
    g = Digraph()
    g.attr(rankdir="LR")

    spec = PATTERN_DEFINITIONS.get(pattern)
    if not spec:
        first_key = next(iter(PATTERN_DEFINITIONS))
        spec = PATTERN_DEFINITIONS[first_key]

    for node_id, label in spec["nodes"].items():
        g.node(node_id, label, shape="box")

    for a, b in spec["edges"]:
        g.edge(a, b)

    anchors = spec["anchors"]
    if include_quality_checks:
        g.node("dq", "Data quality checks", shape="note")
        g.edge(anchors["quality"], "dq", style="dashed")
    if include_metrics:
        g.node("metrics", "Metrics + alerts", shape="note")
        g.edge(anchors["metrics"], "metrics", style="dashed")
    if include_metadata:
        g.node("metadata", "Lineage/metadata", shape="note")
        g.edge(anchors["metadata"], "metadata", style="dashed")

    return g


def build_docker_flow_diagram(
    include_base_image: bool = True,
    include_build_cache: bool = True,
) -> Digraph:
    g = Digraph()
    g.attr(rankdir="LR")

    g.node("repo", "Repo (components + Dockerfile)", shape="box")
    g.node("build", "Cloud Build\nbuild image", shape="box")
    g.node("ar", "Artifact Registry\nimage tag", shape="box")
    g.node("template", "Pipeline template\n(image refs)", shape="box")
    g.node("vertex", "Vertex Pipeline Job\n(run container)", shape="box")

    g.edge("repo", "build")
    g.edge("build", "ar")
    g.edge("ar", "template")
    g.edge("template", "vertex")

    if include_base_image:
        g.node("base", "Base image\n(Python/OS)", shape="note")
        g.edge("base", "repo", style="dashed")

    if include_build_cache:
        g.node("cache", "Build cache", shape="note")
        g.edge("cache", "build", style="dashed")

    return g


def build_env_promotion_diagram(
    include_manual_approval: bool = True,
    include_project_split: bool = True,
    include_rebuild_per_env: bool = False,
) -> Digraph:
    g = Digraph()
    g.attr(rankdir="LR")

    g.node("dev", "Dev\n(branch + bucket)", shape="box")
    g.node("test", "Test\n(branch + bucket)", shape="box")
    g.node("prod", "Prod\n(branch + bucket)", shape="box")

    g.node("artifact", "Versioned artifacts\n(SHA + template)", shape="box")
    g.edge("dev", "artifact")

    if include_rebuild_per_env:
        g.node("build_test", "Rebuild in test", shape="box")
        g.node("build_prod", "Rebuild in prod", shape="box")
        g.edge("artifact", "build_test")
        g.edge("build_test", "test")
        g.edge("test", "build_prod")
        g.edge("build_prod", "prod")
    else:
        g.edge("artifact", "test")
        g.edge("test", "prod")

    if include_manual_approval:
        g.node("approve", "Manual approval", shape="note")
        g.edge("test", "approve", style="dashed")
        g.edge("approve", "prod", style="dashed")

    if include_project_split:
        g.node("projects", "Separate projects\n(optional)", shape="note")
        g.edge("dev", "projects", style="dashed")

    return g
