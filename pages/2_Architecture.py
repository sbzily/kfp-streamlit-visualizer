from pathlib import Path
import streamlit as st
from src.viz.diagrams import build_architecture_diagram

st.title("Architecture")
st.caption("How code, artifacts, and pipeline runs move through the system.")

col1, col2 = st.columns([2, 1])

with col2:
    include_ar = st.checkbox("Show Artifact Registry (Docker images)", value=True)

with col1:
    st.graphviz_chart(build_architecture_diagram(include_artifact_registry=include_ar))

md = Path("src/content/architecture.md").read_text(encoding="utf-8")
st.markdown(md)

st.subheader("Key decisions")
st.markdown(
    "- Artifacts are versioned by git SHA and stored per environment.\n"
    "- Build identity is separate from runtime identity.\n"
    "- Observability is treated as a first-class output."
)
