from graphviz import Digraph
from src.models import PipelineDef, steps_index


def build_graph(p: PipelineDef, annotated: bool) -> Digraph:
    g = Digraph()
    g.attr(rankdir="LR")

    idx = steps_index(p.steps)

    for step in p.steps:
        if annotated and step.annotation:
            label = f"{step.id}\n({step.annotation})"
        else:
            label = step.id
        g.node(step.id, label)

    for a, b in p.edges:
        # allow edges even if steps were misconfigured
        if a in idx and b in idx:
            g.edge(a, b)

    return g
