from pathlib import Path
import streamlit as st
from src.viz.diagrams import PATTERN_DEFINITIONS, build_pattern_diagram

st.title("Data Engineering Patterns")

md = Path("src/content/patterns.md").read_text(encoding="utf-8")
st.markdown(md)

st.sidebar.header("Pattern explorer")
pattern = st.sidebar.selectbox("Pattern", list(PATTERN_DEFINITIONS.keys()), index=0)
include_quality = st.sidebar.checkbox("Include data quality checks", value=True)
include_metrics = st.sidebar.checkbox("Include metrics + alerts", value=True)
include_metadata = st.sidebar.checkbox("Include metadata/lineage", value=True)

PATTERN_DETAILS = {
    "Incremental Load (Watermark)": {
        "when": "High-frequency updates where late-arriving data is expected.",
        "focus": "Track a watermark and keep merges idempotent.",
        "watch": "Watermark drift, duplicates, and partial retries.",
    },
    "Backfill (Partitioned)": {
        "when": "Reprocess historical partitions or rebuild a table.",
        "focus": "Partition planning and concurrency controls.",
        "watch": "Cost spikes and partial failures by partition.",
    },
    "CDC Merge": {
        "when": "Streaming change data capture feeds a serving table.",
        "focus": "De-duplication and merge correctness.",
        "watch": "Out-of-order events and schema drift.",
    },
    "Snapshot Diff": {
        "when": "Upstream only provides full snapshots.",
        "focus": "Diff computation and efficient delta writes.",
        "watch": "Large diffs and late snapshot arrivals.",
    },
}

left, right = st.columns([2, 1])

with left:
    st.graphviz_chart(
        build_pattern_diagram(
            pattern,
            include_quality_checks=include_quality,
            include_metrics=include_metrics,
            include_metadata=include_metadata,
        )
    )

with right:
    details = PATTERN_DETAILS[pattern]
    st.subheader("Pattern notes")
    st.markdown(f"**When to use**: {details['when']}")
    st.markdown(f"**Design focus**: {details['focus']}")
    st.markdown(f"**Watch-outs**: {details['watch']}")
    st.info("Tip: Treat each box as a component or managed service call.")

st.subheader("Pattern checklist")
st.markdown(
    "- Define state clearly (watermark table, CDC log, or snapshot store).\n"
    "- Make retry behavior safe and idempotent.\n"
    "- Add metrics that prove completeness and freshness."
)
