import streamlit as st

st.set_page_config(page_title="KFP Pipeline Visualizer", layout="centered")

st.title("KFP Pipeline Visualizer")

st.write(
    "A small Streamlit project that visualizes **KFP-style** pipelines and "
    "highlights data-engineering patterns (incremental loads, backfills, retries, idempotency)."
)

st.subheader("Pages")
st.markdown(
    "- **Intro**: KFP concepts, how to think about components, artifacts, caching\n"
    "- **Visualizer**: pick a pipeline pattern and see the DAG + a simplified spec\n"
    "- **DE Patterns**: practical patterns and pitfalls for production pipelines"
)

st.subheader("Run locally")
st.code(
    "python3 -m venv .venv\n"
    "source .venv/bin/activate\n"
    "pip install -r requirements.txt\n"
    "streamlit run app.py",
    language="bash",
)

st.caption("Tip: the main visualizer logic lives in `pages/2_Visualizer.py` and `src/`.")
