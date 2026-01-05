# KFP Pipeline Visualizer (Streamlit)

A small Streamlit app that visualizes **KFP-style** pipelines and explains common **data engineering** patterns
(incremental loads, backfills, retries, idempotency, caching).

## Live demo
Coming soon (Streamlit Community Cloud).

## What it shows
- Pipeline DAG visualization
- Parameter-driven pipeline variants (e.g. incremental vs backfill)
- A simplified “pipeline spec” view (V0), ready to be replaced by real KFP compilation output later

## Screenshots
(Add 1–2 screenshots here once the UI stabilizes.)

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
