import streamlit as st
from src.viz.diagrams import build_architecture_diagram

st.set_page_config(
    page_title="Vertex AI Pipelines Explainer",
    page_icon="🧩",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Apply Helvetica and add a subtle background.
st.markdown(
    """
    <style>
    * { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; }
    .stApp {
        background: radial-gradient(circle at top, #f8fbff 0%, #f3f6fb 55%, #edf1f7 100%);
    }
    .block-container { max-width: 900px; padding-top: 2.5rem; }
    h1 { letter-spacing: -0.02em; }
    .stage-card { border-radius: 12px; padding: 14px 16px; margin-bottom: 14px; color: #0b1f44; }
    details summary { font-size: 1.02rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("Stage Pages")
sections = [
    "Overview",
    "GitHub (source of truth)",
    "Cloud Build (CI/CD)",
    "Artifact Registry (images)",
    "GCS (artifacts & templates)",
    "Vertex AI Pipelines",
    "Scheduler",
    "Monitoring & Alerting",
]
selected = st.sidebar.radio("Navigate", sections, index=0)
st.sidebar.info("Single-page mode for now. Sidebar jumps between stage sections.")

st.title("Vertex AI Pipelines, explained clearly")
st.caption("A polished, interview-ready walkthrough of a production data engineering workflow.")
st.write(
    "For many data engineers, Vertex AI can feel unfamiliar because it arrives from the ML world. "
    "Under the hood it is built on Kubeflow Pipelines (KFP), which means you get the same DAG-based "
    "orchestration concepts—components, templates, parameters, and runs—wrapped in a managed Google control plane."
)
st.write(
    "This single-page explainer shows how code changes travel from GitHub to scheduled pipeline runs, "
    "with traceable artifacts, clear ownership, and a production-ready CI/CD loop."
)


st.divider()

st.subheader("Architecture walkthrough")
st.caption("Use the sidebar to jump between stages.")

if selected == "Overview":
    st.graphviz_chart(build_architecture_diagram())

    stages = [
        {
            "title": "GitHub (source of truth)",
            "color": "#e8f5e9",
            "points": [
                "Environment branches (dev/test/prod) drive promotion strategy.",
                "Pull requests enforce review, tests, and approvals.",
                "Holds SQL, configs, pipeline code, and Dockerfiles tied to a git SHA.",
            ],
        },
        {
            "title": "Cloud Build (CI/CD)",
            "color": "#e3f2fd",
            "points": [
                "Triggers on branch updates and executes `cloudbuild.yaml` steps.",
                "Builds and pushes container images for custom components.",
                "Compiles pipeline templates and tags outputs with the git SHA.",
            ],
        },
        {
            "title": "Artifact Registry (images)",
            "color": "#e0f7fa",
            "points": [
                "Stores immutable images tagged with git SHA or release version.",
                "Vertex pulls the exact image referenced in the template.",
                "Pinned base images keep dependencies stable across environments.",
            ],
        },
        {
            "title": "GCS (artifacts & templates)",
            "color": "#fff8e1",
            "points": [
                "Environment buckets store SQL/config artifacts and compiled templates.",
                "Every upload is tied to a git SHA for traceability and rollback.",
                "Creates a durable audit trail of what actually ran.",
            ],
        },
        {
            "title": "Vertex AI Pipelines",
            "color": "#ede7f6",
            "points": [
                "Deploys or updates pipeline templates built by CI.",
                "Runs jobs that pull images and configs from versioned artifacts.",
                "Tracks run lineage, metadata, and execution history.",
            ],
        },
        {
            "title": "Scheduler",
            "color": "#fce4ec",
            "points": [
                "Runs on cadence and controls concurrency and catch-up behavior.",
                "Pins jobs to specific template versions for repeatability.",
                "Separates incremental runs from heavy backfill workloads.",
            ],
        },
        {
            "title": "Monitoring & Alerting",
            "color": "#f3e5f5",
            "points": [
                "Alerts on failed runs, data quality checks, and SLO breaches.",
                "Dashboards for freshness, completeness, duration, and cost.",
                "Rollback path to a known-good template + pinned image.",
            ],
        },
    ]

    col_left, col_right = st.columns(2)
    for idx, stage in enumerate(stages):
        col = col_left if idx % 2 == 0 else col_right
        points_html = "".join([f"<li>{p}</li>" for p in stage["points"]])
        col.markdown(
            f"""
            <details style="background:{stage['color']};" class="stage-card">
                <summary style="font-weight:700; cursor:pointer;">{stage['title']}</summary>
                <ul style="margin-top:8px;">{points_html}</ul>
            </details>
            """,
            unsafe_allow_html=True,
        )

if selected == "GitHub (source of truth)":
    st.subheader("GitHub as the source of truth")
    st.write(
        "Treat GitHub as the control plane for your data platform. Every change to SQL, configs, "
        "or pipeline code begins here and is tied to a git SHA."
    )
    st.markdown(
        "- Branch-per-environment aligns directly with dev/test/prod buckets and runtime identities.\n"
        "- Pull requests enforce review, tests, and approvals before deployment.\n"
        "- Tags and releases provide stable versions for backfills and audits.\n"
        "- Store infra-as-code (Cloud Build triggers, IAM) alongside pipeline code."
    )
    st.info("Good interview hook: show how a single git SHA maps to artifacts, templates, and images.")

if selected == "Cloud Build (CI/CD)":
    st.subheader("Cloud Build for CI/CD")
    st.write(
        "Cloud Build is the automation backbone. It validates, packages, and publishes everything "
        "the pipeline will need to run."
    )
    st.markdown(
        "- Validates SQL/configs and runs unit/integration checks early.\n"
        "- Builds container images when you own runtime code.\n"
        "- Compiles the KFP pipeline template with pinned image tags.\n"
        "- Uploads artifacts to environment-specific GCS buckets.\n"
        "- Emits build metadata used for traceability and rollback."
    )
    st.code(
        "steps:\n"
        "  - name: python\n"
        "    entrypoint: bash\n"
        "    args: ['-c', 'pytest && python compile_pipeline.py']\n"
        "  - name: gcr.io/cloud-builders/gsutil\n"
        "    args: ['cp', 'dist/template.json', 'gs://$ENV_BUCKET/templates/$SHORT_SHA.json']\n",
        language="yaml",
    )

if selected == "Artifact Registry (images)":
    st.subheader("Artifact Registry for runtime images")
    st.write(
        "Container images make pipeline components reproducible. They capture code + dependencies "
        "as a single deployable unit."
    )
    st.markdown(
        "- Tag images with git SHA or release version to lock the runtime.\n"
        "- Enforce pull permissions for the runtime service account.\n"
        "- Standardize base images to keep dependencies consistent.\n"
        "- Use vulnerability scanning and provenance where possible."
    )

if selected == "GCS (artifacts & templates)":
    st.subheader("GCS as the artifact store")
    st.write(
        "GCS buckets hold the versioned artifacts that the pipeline consumes: SQL, configs, and "
        "compiled templates."
    )
    st.markdown(
        "- One bucket per environment to avoid cross-env contamination.\n"
        "- Folder structure by git SHA for deterministic rollbacks.\n"
        "- Keep raw inputs and compiled templates immutable.\n"
        "- Store data contracts or schema snapshots alongside artifacts."
    )

if selected == "Vertex AI Pipelines":
    st.subheader("Vertex AI Pipelines execution")
    st.write(
        "Vertex AI runs KFP templates as managed pipeline jobs. Think of it as a hosted "
        "orchestrator with logs, lineage, and scheduling."
    )
    st.markdown(
        "- Templates reference GCS artifacts and container images built in CI.\n"
        "- Components map to data engineering steps: extract, validate, transform, load.\n"
        "- Metadata capture enables lineage and auditability.\n"
        "- Retry behavior and caching are configured at the component level."
    )

if selected == "Scheduler":
    st.subheader("Scheduler and orchestration cadence")
    st.write(
        "Scheduling is where data engineering becomes operations. The scheduler decides when "
        "and how often your pipelines run."
    )
    st.markdown(
        "- Cadence tied to SLAs (hourly, daily, weekly).\n"
        "- Controls concurrency to avoid clobbering shared tables.\n"
        "- Backfills run on separate schedules or one-off jobs.\n"
        "- Pin scheduler to specific template versions for repeatability."
    )

if selected == "Monitoring & Alerting":
    st.subheader("Monitoring and alerting")
    st.write(
        "Observability keeps pipelines reliable. This is where you prove the pipeline is healthy "
        "and the data is trustworthy."
    )
    st.markdown(
        "- Alerts on failed runs, data quality checks, and SLA breaches.\n"
        "- Dashboards for freshness, completeness, duration, and cost.\n"
        "- Define ownership: on-call, escalation, and rollback playbooks.\n"
        "- Track data incidents just like application incidents."
    )
