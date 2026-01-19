import streamlit as st
from src.pipelines.definitions import PIPELINES
from src.viz.graphviz_dag import build_graph
from src.utils.text import MAPPING_MARKDOWN

st.title("Pipeline Visualizer")
st.caption("Explore pipeline shapes and map steps to real execution concepts.")
st.markdown(MAPPING_MARKDOWN)

st.sidebar.header("Pipeline")
pattern = st.sidebar.selectbox("Pattern", list(PIPELINES.keys()), index=0)

PATTERN_SUMMARIES = {
    "Simple ETL": "Baseline extract → validate → transform → load flow.",
    "Incremental Load": "Watermark-driven delta processing with idempotent merges.",
    "Backfill": "Partitioned reprocessing with metrics at the end.",
    "CDC Merge": "Change feed plus de-duplication before merge.",
    "Snapshot Diff": "Full snapshot compare with applied deltas.",
}

st.sidebar.subheader("Pattern summary")
st.sidebar.markdown(PATTERN_SUMMARIES.get(pattern, "Pipeline pattern overview."))

st.sidebar.header("View")
view = st.sidebar.selectbox("Diagram view", ["Basic", "Annotated"], index=0)
annotated = view == "Annotated"

p = PIPELINES[pattern]

tab_dag, tab_spec = st.tabs(["DAG", "Spec (V0)"])

@st.cache_data
def get_graph(name: str, annotated_flag: bool):
    return build_graph(PIPELINES[name], annotated_flag)

with tab_dag:
    st.graphviz_chart(get_graph(pattern, annotated))

with tab_spec:
    st.subheader("Steps")
    st.table(
        [{"step": s.id, "description": s.description, "annotation": s.annotation or ""} for s in p.steps]
    )
    st.subheader("Edges")
    st.code("\n".join([f"{a} -> {b}" for a, b in p.edges]))
