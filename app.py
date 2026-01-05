import streamlit as st
from graphviz import Digraph

st.set_page_config(page_title="KFP Pipeline Visualizer (V0)", layout="centered")

st.title("KFP Pipeline Visualizer (V0)")

st.write("A minimal DAG preview for a simple ETL pipeline.")

g = Digraph()
g.attr(rankdir="LR")

g.node("Extract")
g.node("Validate")
g.node("Transform")
g.node("Load")

g.edges([
    ("Extract", "Validate"),
    ("Validate", "Transform"),
    ("Transform", "Load"),
])

st.graphviz_chart(g)##