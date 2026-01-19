import streamlit as st
from src.viz.diagrams import build_architecture_diagram

st.set_page_config(page_title="Vertex AI Pipelines Explainer", page_icon="🧩", layout="wide")

st.title("Vertex AI Pipelines: CI/CD + Visualizer")
st.caption(
    "A Streamlit explainer site that maps a production data-engineering workflow to "
    "Vertex AI Pipelines, from GitHub branches to scheduled runs."
)

intro_col, action_col = st.columns([3, 2])

with intro_col:
    st.subheader("What this is")
    st.write(
        "This site explains how a real-world data pipeline gets versioned, built, deployed, "
        "and operated. Use it as a portfolio walkthrough or a quick architecture explainer."
    )
    st.markdown(
        """
        **You will find:**
        - A pipeline DAG visualizer with multiple patterns.
        - CI/CD flow diagrams that mirror Cloud Build triggers.
        - Ops and environment promotion guidance.
        """
    )

with action_col:
    st.subheader("Quick tour")
    st.markdown(
        """
        1. Open **Visualizer** to explore pipeline DAGs.
        2. Visit **CI/CD Flow** to see how deployments happen.
        3. Use **Docker Explainer** to answer "why images?"
        """
    )
    st.info("Tip: Use the diagrams as talking points in interviews or demos.")

st.divider()

st.subheader("Workflow at a glance")
with st.expander("Show the architecture map"):
    include_ar = st.checkbox("Include Artifact Registry (Docker images)", value=True, key="home_ar")
    st.graphviz_chart(build_architecture_diagram(include_artifact_registry=include_ar))

metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)
metric_col_1.metric("Patterns", "5", "Incremental, backfill, CDC")
metric_col_2.metric("Environments", "3", "Dev / Test / Prod")
metric_col_3.metric("Artifacts", "4", "SQL, config, templates, images")
metric_col_4.metric("Ops focus", "3", "Alerts, retries, rollbacks")

st.divider()

st.subheader("Explore the site")
left, right = st.columns(2)

with left:
    st.markdown(
        """
        **Architecture**
        - How GitHub, Cloud Build, GCS, and Vertex fit together.

        **CI/CD Flow**
        - The branch-driven build loop and quality gates.

        **Visualizer**
        - A DAG view of real pipeline patterns.
        """
    )

with right:
    st.markdown(
        """
        **Data Engineering Patterns**
        - Incremental, backfill, CDC, snapshot diff.

        **Docker Explainer**
        - When to build images and how they are referenced.

        **Ops & Promotion**
        - What it takes to run this in production.
        """
    )

st.subheader("Key artifacts to highlight")
st.markdown(
    "- `cloudbuild.yaml` defining the build and deploy steps.\n"
    "- Versioned pipeline templates stored in environment buckets.\n"
    "- Optional container images in Artifact Registry.\n"
    "- Scheduled Vertex Pipeline runs with logged execution history."
)
