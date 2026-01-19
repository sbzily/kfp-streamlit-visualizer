from pathlib import Path
import streamlit as st

st.title("Ops & Observability")

md = Path("src/content/ops.md").read_text(encoding="utf-8")
st.markdown(md)

st.subheader("Ops checklist")
st.markdown(
    "- Alert on failed pipeline jobs and data quality checks.\n"
    "- Track run duration and cost per run.\n"
    "- Keep a rollback path (previous template + pinned image).\n"
    "- Document ownership and on-call rotation."
)
