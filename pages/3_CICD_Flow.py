from pathlib import Path
import streamlit as st
from src.viz.diagrams import build_cicd_cycle_diagram

st.title("CI/CD Flow (GitHub → Cloud Build → Vertex Pipelines)")

st.sidebar.header("Diagram toggles")
include_gates = st.sidebar.checkbox("Show quality gates", value=True)
include_docker = st.sidebar.checkbox("Show Docker lane", value=True)
include_ops = st.sidebar.checkbox("Show ops loop", value=True)

st.graphviz_chart(
    build_cicd_cycle_diagram(
        include_docker_lane=include_docker,
        include_quality_gates=include_gates,
        include_observability=include_ops,
    )
)

md = Path("src/content/cicd_flow.md").read_text(encoding="utf-8")
st.markdown(md)
