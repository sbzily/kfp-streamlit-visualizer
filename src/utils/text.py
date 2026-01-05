"""Text and small UI helpers for the app."""

MAPPING_MARKDOWN = """
- **Extract**: a KFP component (container) — often a Vertex AI CustomJob that pulls data
- **Validate**: small pipeline component or container that runs data quality checks
- **Transform**: heavier compute — Dataflow jobs or CustomJobs/Batch Prediction
- **Load**: sink step — BigQuery, Cloud Storage, or Vertex AI managed dataset

This V0 is intentionally simple; use the Visualizer page to switch views.
"""


def navigation():
    """Return a minimal navigation selection (kept for compatibility)."""
    # Streamlit pages will provide site navigation automatically when using the `pages/` folder,
    # but this helper is retained for programmatic selection if needed.
    return "Diagram"
