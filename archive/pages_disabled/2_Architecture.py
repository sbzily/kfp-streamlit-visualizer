import streamlit as st
from src.viz.diagrams import build_architecture_diagram

st.set_page_config(page_title="Architecture", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")

# Apply Helvetica and hide the default sidebar nav.
st.markdown(
    """
    <style>
    * { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    .stage-card { border-radius: 10px; padding: 12px 14px; margin-bottom: 12px; color: #0b1f44; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.link_button("← Back to home", "/")

st.title("Architecture walkthrough")
st.caption("Click through each stage to see what happens from code commit to scheduled runs.")

st.graphviz_chart(build_architecture_diagram())

st.subheader("Stages (click to expand)")

stages = [
    {
        "title": "GitHub (source of truth)",
        "color": "#e8f5e9",
        "points": [
            "Branching model mirrors environments (dev/test/prod).",
            "PRs gate what reaches Cloud Build triggers.",
            "Artifacts: SQL, configs, pipeline code, Dockerfile.",
        ],
    },
    {
        "title": "Cloud Build (CI/CD)",
        "color": "#e3f2fd",
        "points": [
            "Runs `cloudbuild.yaml` on branch triggers.",
            "Builds/pushes images if components are custom.",
            "Compiles pipeline template and versions it by git SHA.",
        ],
    },
    {
        "title": "Artifact Registry (images)",
        "color": "#e0f7fa",
        "points": [
            "Stores versioned images (tagged by git SHA).",
            "Runtime pulls images referenced in the template.",
            "Keeps base image pinned for reproducibility.",
        ],
    },
    {
        "title": "GCS (artifacts & templates)",
        "color": "#fff8e1",
        "points": [
            "Env-specific buckets store SQL/config and compiled templates.",
            "Versioning ties uploads to the triggering git SHA.",
            "Provides traceability for rollback and audits.",
        ],
    },
    {
        "title": "Vertex AI Pipelines",
        "color": "#ede7f6",
        "points": [
            "Deploys/updates pipeline templates from Cloud Build.",
            "Executes jobs that reference uploaded artifacts and images.",
            "Emits lineage and run history for observability.",
        ],
    },
    {
        "title": "Scheduler",
        "color": "#fce4ec",
        "points": [
            "Runs jobs on cadence; controls catch-up and concurrency.",
            "Ties to specific template versions for repeatability.",
            "Starts backfills separately from incremental runs.",
        ],
    },
    {
        "title": "Monitoring & Alerting",
        "color": "#f3e5f5",
        "points": [
            "Alerts on failed runs, DQ checks, and SLO breaches.",
            "Dashboards for run duration, cost, freshness, completeness.",
            "Rollback story: redeploy last known good template/image.",
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
