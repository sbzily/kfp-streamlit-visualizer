from pathlib import Path
import streamlit as st

st.title("FAQ")

md = Path("src/content/faq.md").read_text(encoding="utf-8")
st.markdown(md)
