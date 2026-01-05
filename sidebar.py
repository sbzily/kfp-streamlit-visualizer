import streamlit as st


def navigation():
    """Render a minimal navigation-only sidebar and return the selected page.

    Currently keeps a single "Diagram" page to expand later.
    """
    page = st.sidebar.selectbox("Page", ["Diagram"], index=0)
    return page
