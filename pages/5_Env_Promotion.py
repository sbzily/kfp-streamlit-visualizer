from pathlib import Path
import streamlit as st

st.title("Environment promotion (dev → test → prod)")

md = Path("src/content/env_promotion.md").read_text(encoding="utf-8")
st.markdown(md)

st.subheader("Quick checklist")
st.markdown(
    "- Separate **buckets** per env (you do this)\n"
    "- Separate **service accounts** per env (strongly recommended)\n"
    "- Protect prod branch + require PR approvals\n"
    "- Version everything: git SHA → artifacts → compiled template\n"
)
