from pathlib import Path
import streamlit as st
from src.viz.diagrams import build_env_promotion_diagram

st.title("Environment promotion (dev → test → prod)")

st.sidebar.header("Promotion toggles")
include_approval = st.sidebar.checkbox("Manual approval between test/prod", value=True)
include_projects = st.sidebar.checkbox("Separate projects per env", value=True)
include_rebuild = st.sidebar.checkbox("Rebuild per environment", value=False)

st.graphviz_chart(
    build_env_promotion_diagram(
        include_manual_approval=include_approval,
        include_project_split=include_projects,
        include_rebuild_per_env=include_rebuild,
    )
)

md = Path("src/content/env_promotion.md").read_text(encoding="utf-8")
st.markdown(md)

st.subheader("Quick checklist")
st.markdown(
    "- Separate **buckets** per env (you do this)\n"
    "- Separate **service accounts** per env (strongly recommended)\n"
    "- Protect prod branch + require PR approvals\n"
    "- Version everything: git SHA → artifacts → compiled template\n"
)
