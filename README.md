# KFP Pipeline Visualizer (V0)

Minimal Streamlit app that renders a simple Graphviz DAG representing a KFP-style ETL pipeline. This small V0 project is intended as a learning playground for building Streamlit sites that explain Kubeflow Pipelines (KFP) and Vertex AI workflows.

Requirements
- Python 3.8+
- Install Python deps:

```bash
python -m pip install -r requirements.txt
```

- Install the Graphviz system package (macOS):

```bash
brew install graphviz
```

Run

```bash
streamlit run app.py
```

Files
- `app.py` — Streamlit app entry point
- `diagrams.py` — graph-building helper(s)
- `assets/` — optional images / exports

Notes
- This is intentionally minimal. Want me to add more nodes, labels, or a sidebar explanation of how KFP maps to Vertex AI? Reply with features you'd like.
# KFP Streamlit Visualizer (V0)

Small Streamlit app that visualizes a simple data-engineering pipeline DAG (KFP-inspired).

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

#### this is a test