from pathlib import Path
import streamlit as st

st.title("Ops & Observability")

md = Path("src/content/ops.md").read_text(encoding="utf-8")
st.markdown(md)
