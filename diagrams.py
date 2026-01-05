from graphviz import Digraph


def build_pipeline_graph():
    """Return a simple left-to-right ETL pipeline Graphviz Digraph."""
    g = Digraph()
    g.attr(rankdir="LR")

    g.node("Extract")
    g.node("Validate")
    g.node("Transform")
    g.node("Load")

    g.edges([
        ("Extract", "Validate"),
        ("Validate", "Transform"),
        ("Transform", "Load"),
    ])

    return g
