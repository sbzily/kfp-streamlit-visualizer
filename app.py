import streamlit as st
from diagrams import build_pipeline_graph

st.set_page_config(page_title="KFP Pipeline Visualizer (V0)", layout="centered")

st.title("KFP Pipeline Visualizer (V0)")

st.write("A minimal DAG preview for a simple ETL pipeline.")

g = build_pipeline_graph()

st.graphviz_chart(g)