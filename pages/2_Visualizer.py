import streamlit as st
from src.pipelines.definitions import PIPELINES
from src.viz.graphviz_dag import build_graph
from src.utils.text import MAPPING_MARKDOWN

st.title("Pipeline Visualizer")
st.markdown(MAPPING_MARKDOWN)

st.sidebar.header("Pipeline")
pattern = st.sidebar.selectbox("Pattern", list(PIPELINES.keys()), index=0)

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
