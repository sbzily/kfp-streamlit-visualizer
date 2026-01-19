from pathlib import Path
import streamlit as st
from src.viz.diagrams import build_docker_flow_diagram

st.title("Why Docker shows up in the YAML")

st.sidebar.header("Diagram toggles")
include_base = st.sidebar.checkbox("Include base image", value=True)
include_cache = st.sidebar.checkbox("Include build cache", value=True)

st.graphviz_chart(
    build_docker_flow_diagram(
        include_base_image=include_base,
        include_build_cache=include_cache,
    )
)

md = Path("src/content/docker.md").read_text(encoding="utf-8")
st.markdown(md)

st.subheader("Rule of thumb")
st.markdown(
    "- If your pipeline steps run **custom Python**: build/push images in CI.\n"
    "- If your pipeline mostly orchestrates **managed services** (SQL engines, Dataflow templates, etc.): "
    "compile/deploy can be enough, as long as your runtime is controlled.\n"
)

st.subheader("Sample build step")
st.code(
    "steps:\n"
    "  - name: 'gcr.io/cloud-builders/docker'\n"
    "    args: ['build', '-t', '$IMAGE_URI:$SHORT_SHA', '.']\n"
    "  - name: 'gcr.io/cloud-builders/docker'\n"
    "    args: ['push', '$IMAGE_URI:$SHORT_SHA']\n",
    language="yaml",
)
