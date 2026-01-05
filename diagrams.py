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


def build_annotated_graph():
    """Return an annotated graph with KFP steps mapped to Vertex AI concepts."""
    g = Digraph()
    g.attr(rankdir="LR")

    # Annotated labels show the step and a typical Vertex AI mapping
    g.node("Extract", "Extract\n(CustomJob)", shape="box", style="filled", fillcolor="#E8F0FE")
    g.node("Validate", "Validate\n(Pipeline component)", shape="box", style="filled", fillcolor="#FFF4E5")
    g.node("Transform", "Transform\n(Dataflow / CustomJob)", shape="box", style="filled", fillcolor="#E8FFE8")
    g.node("Load", "Load\n(BigQuery / GCS)", shape="box", style="filled", fillcolor="#F0F7FF")

    g.edges([
        ("Extract", "Validate"),
        ("Validate", "Transform"),
        ("Transform", "Load"),
    ])

    return g
