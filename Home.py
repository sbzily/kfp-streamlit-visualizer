import streamlit as st

st.set_page_config(page_title="KFP Pipeline Visualizer", page_icon="🧩", layout="wide")

st.title("KFP Pipeline Visualizer")
st.caption("Explore a minimal Kubeflow Pipelines-style DAG and common data engineering patterns.")

intro_col, action_col = st.columns([3, 2])

with intro_col:
    st.subheader("What you can do here")
    st.write(
        "This app demonstrates how pipeline steps map to execution concepts like dependencies, "
        "retries, caching, and idempotency. Use it as a quick visual reference for how KFP-style "
        "pipelines behave under different parameters."
    )
    st.markdown(
        """
        **In this demo you can:**
        - Inspect a simplified pipeline DAG.
        - Compare incremental vs. backfill paths.
        - See where caching, retries, and validation steps fit.
        """
    )

with action_col:
    st.subheader("Quick start")
    st.markdown(
        """
        1. Open **Visualizer** in the left sidebar.
        2. Toggle pipeline parameters to see the DAG update.
        3. Read the pipeline spec summary to map nodes to execution stages.
        """
    )
    st.info("Tip: Use this view as a checklist when explaining pipelines to stakeholders.")

st.divider()

metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
metric_col_1.metric("Pipeline nodes", "6", "Demo graph")
metric_col_2.metric("Execution modes", "2", "Incremental & backfill")
metric_col_3.metric("Key patterns", "5", "Caching, retries, validation")

st.divider()

st.subheader("What’s included")
left, right = st.columns(2)

with left:
    st.markdown(
        """
        **Visual concepts**
        - Directed acyclic graph (DAG) layout
        - Task dependencies and branching
        - Parameter-driven pipeline variants
        """
    )

with right:
    st.markdown(
        """
        **Execution concepts**
        - Incremental vs. backfill runs
        - Idempotent processing steps
        - Retry and caching behavior
        """
    )
