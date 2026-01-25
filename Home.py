import streamlit as st
from src.viz.diagrams import build_architecture_diagram

st.set_page_config(
    page_title="Vertex AI Pipelines Explainer",
    page_icon="🧩",
    layout="wide",
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
    .block-container { max-width: 1280px; padding-top: 2.5rem; }
    h1 { letter-spacing: -0.02em; }
    .stage-card { border-radius: 12px; padding: 14px 16px; margin-bottom: 14px; color: #0b1f44; }
    details summary { font-size: 1.02rem; }
    .detail-block p { margin-bottom: 0.6rem; }
    .stage-card p { margin: 0.45rem 0; }
    div[data-testid="stGraphViz"] { overflow: visible; }
    div[data-testid="stGraphViz"] svg {
        width: 100% !important;
        height: auto !important;
        max-width: none !important;
    }
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


st.title("Vertex AI Pipelines for Data Engineering")
st.caption("A practical walkthrough of how production data pipelines are built, deployed, and operated.")
st.write(
    "Vertex AI can feel unfamiliar because it is branded for ML, yet the mechanics are classic pipeline "
    "orchestration. Under the hood it is Kubeflow Pipelines (KFP): a DAG of containerized steps compiled "
    "into a template and run by a managed control plane."
)
st.write(
    "This explainer connects the dots for data engineering"
)

st.divider()

st.subheader("Architecture walkthrough")
st.write(
    "Here is an end-to-end workflow on Vertex AI Pipelines. Each stage expands with concrete, "
    "data engineering detail so you can explain what happens and why it matters."
)
st.caption("Use the sidebar to jump between stages.")

if selected == "Overview":
    st.graphviz_chart(build_architecture_diagram(), use_container_width=True)

    stages = [
    {
        "title": "GitHub",
        "color": "#e8f5e9",
        "points": [
            "Branches map to dev/test/prod so promoting a change is a merge, not a manual copy.",
            "Pull requests are the checkpoint where reviews, tests, and policy checks happen before anything lands.",
            "The repo keeps the SQL, configs, pipeline definitions, and Dockerfiles together so the pipeline’s behaviour is versioned as one unit.",
            "Branch protections and CODEOWNERS make it clear who owns what and who must approve changes.",
            "Every merge produces a git SHA, which is just a unique ID for that exact commit; it’s the version stamp you can trace across templates, images, and uploaded artifacts.",
        ],

        },
        {
            "title": "Cloud Build (CI/CD)",
            "color": "#e3f2fd",
            "points": [
                "Branch triggers kick off `cloudbuild.yaml` with env-specific substitutions.",
                "Validation runs first: SQL linting, schema checks, and unit tests.",
                "Custom components are built into images and pushed to Artifact Registry.",
                "Pipeline templates are compiled with pinned image tags and parameters.",
                "Artifacts are uploaded to GCS under deterministic SHA paths.",
            ],
        },
        {
            "title": "Artifact Registry (images)",
            "color": "#e0f7fa",
            "points": [
                "Images are immutable and tagged with git SHA or a release version.",
                "Vertex pulls the exact image referenced in the compiled template.",
                "Pinned base images keep dependencies stable across environments.",
                "Build and runtime permissions are split to reduce risk.",
            ],
        },
        {
            "title": "GCS (artifacts & templates)",
            "color": "#fff8e1",
            "points": [
                "Environment buckets store SQL, configs, and compiled templates.",
                "Every upload is tied to a git SHA for traceability and rollback.",
                "Folder structure by SHA makes audits and reproductions simple.",
                "Schema snapshots or data contracts can live alongside inputs.",
            ],
        },
        {
            "title": "Vertex AI Pipelines",
            "color": "#ede7f6",
            "points": [
                "Deploys templates built in CI and executes pipeline jobs.",
                "Components pull images and configs from versioned artifacts.",
                "Run metadata and lineage make troubleshooting and audits easier.",
                "Caching, retries, and timeouts are set per component.",
            ],
        },
        {
            "title": "Scheduler",
            "color": "#fce4ec",
            "points": [
                "Cadence is tied to SLAs, not convenience.",
                "Concurrency limits prevent overlapping runs on shared tables.",
                "Backfills run as separate jobs with larger resource profiles.",
                "Schedules pin template versions to keep runs reproducible.",
            ],
        },
        {
            "title": "Monitoring & Alerting",
            "color": "#f3e5f5",
            "points": [
                "Alerts fire on failed runs, data quality checks, and SLA breaches.",
                "Dashboards track freshness, completeness, duration, and cost.",
                "Runbooks define rollback to a known-good template + image.",
                "Ownership and on-call rotation keep the pipeline supported.",
            ],
        },
    ]

    col_left, col_right = st.columns(2)
    for idx, stage in enumerate(stages):
        col = col_left if idx % 2 == 0 else col_right
        points_html = "".join([f"<p>{p}</p>" for p in stage["points"]])
        col.markdown(
            f"""
            <details style="background:{stage['color']};" class="stage-card">
                <summary style="font-weight:700; cursor:pointer;">{stage['title']}</summary>
                <div style="margin-top:8px;">{points_html}</div>
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
        """
        <div class="detail-block">
            <p><strong>Branch strategy:</strong> Align dev/test/prod branches with buckets and runtime identities.</p>
            <p><strong>Change control:</strong> Pull requests enforce review, tests, and approvals before merge.</p>
            <p><strong>Versioning:</strong> Tags and releases provide stable references for audits and backfills.</p>
            <p><strong>Ownership:</strong> CODEOWNERS and branch protections make accountability clear.</p>
            <p><strong>Infrastructure:</strong> Keep Cloud Build triggers, IAM, and configs in the same repo.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("Good interview hook: show how a single git SHA maps to artifacts, templates, and images.")

if selected == "Cloud Build (CI/CD)":
    st.subheader("Cloud Build for CI/CD")
    st.write(
        "Cloud Build is the automation backbone. It validates, packages, and publishes everything "
        "the pipeline will need to run."
    )
    st.markdown(
        """
        <div class="detail-block">
            <p><strong>Validation:</strong> SQL linting, data contract checks, and tests fail fast.</p>
            <p><strong>Packaging:</strong> Custom component code becomes a container image with pinned deps.</p>
            <p><strong>Compilation:</strong> KFP templates are built with explicit image tags and parameters.</p>
            <p><strong>Publishing:</strong> Artifacts are uploaded to env buckets under the git SHA.</p>
            <p><strong>Traceability:</strong> Build metadata links commits to templates and images.</p>
        </div>
        """,
        unsafe_allow_html=True,
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
        """
        <div class="detail-block">
            <p><strong>Tagging:</strong> Use git SHA or release tags so the runtime is immutable.</p>
            <p><strong>Permissions:</strong> Runtime service accounts must have pull access to the registry.</p>
            <p><strong>Base images:</strong> Standardize images to reduce drift across environments.</p>
            <p><strong>Security:</strong> Enable scanning and provenance to catch vulnerable builds early.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if selected == "GCS (artifacts & templates)":
    st.subheader("GCS as the artifact store")
    st.write(
        "GCS buckets hold the versioned artifacts that the pipeline consumes: SQL, configs, and "
        "compiled templates."
    )
    st.markdown(
        """
        <div class="detail-block">
            <p><strong>Isolation:</strong> One bucket per environment prevents cross-env contamination.</p>
            <p><strong>Rollback:</strong> Folder structure by git SHA makes rollbacks deterministic.</p>
            <p><strong>Immutability:</strong> Treat compiled templates and inputs as append-only artifacts.</p>
            <p><strong>Contracts:</strong> Store schema snapshots or data contracts with the inputs.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if selected == "Vertex AI Pipelines":
    st.subheader("Vertex AI Pipelines execution")
    st.write(
        "Vertex AI runs KFP templates as managed pipeline jobs. Think of it as a hosted "
        "orchestrator with logs, lineage, and scheduling."
    )
    st.markdown(
        """
        <div class="detail-block">
            <p><strong>Templates:</strong> Reference GCS artifacts and container images built in CI.</p>
            <p><strong>Components:</strong> Map to extract, validate, transform, and load steps.</p>
            <p><strong>Lineage:</strong> Metadata and run history support auditability.</p>
            <p><strong>Reliability:</strong> Retries, caching, and timeouts are set per component.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if selected == "Scheduler":
    st.subheader("Scheduler and orchestration cadence")
    st.write(
        "Scheduling is where data engineering becomes operations. The scheduler decides when "
        "and how often your pipelines run."
    )
    st.markdown(
        """
        <div class="detail-block">
            <p><strong>Cadence:</strong> Schedules reflect SLAs (hourly, daily, weekly).</p>
            <p><strong>Concurrency:</strong> Limits prevent overlapping runs on shared targets.</p>
            <p><strong>Backfills:</strong> Separate schedules or one-off jobs with larger resources.</p>
            <p><strong>Versioning:</strong> Schedulers pin template versions for repeatable runs.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if selected == "Monitoring & Alerting":
    st.subheader("Monitoring and alerting")
    st.write(
        "Observability keeps pipelines reliable. This is where you prove the pipeline is healthy "
        "and the data is trustworthy."
    )
    st.markdown(
        """
        <div class="detail-block">
            <p><strong>Alerts:</strong> Failed runs, data quality checks, and SLA breaches.</p>
            <p><strong>Dashboards:</strong> Freshness, completeness, duration, and cost.</p>
            <p><strong>Ownership:</strong> On-call, escalation, and rollback playbooks.</p>
            <p><strong>Incidents:</strong> Track data issues with the same rigor as app outages.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
