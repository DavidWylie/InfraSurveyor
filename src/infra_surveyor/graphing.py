import graphviz
from infra_surveyor.cloud import models
from typing import List


class Graph:
    def __init__(self):
        self.graph = graphviz.Graph(
            graph_attr={
                "directed": "true",
                "splines": "curved",
                "nodesep": "1",
                "ranksep": "1",
                "fontname": "Sans-Serif",
                "fontsize": "15",
                "fontcolor": "#2D3436",
                "rankdir": "LR",
            },
            node_attr={
                "shape": "none",
                "height": "0.75",
                "labelloc": "b",
                "imagepos": "tc",
                "fontname": "Sans-Serif",
                "fontsize": "13",
                "fontcolor": "#2D3436",
            },
        )

    def assemble_graph(self, nodes: List[models.Resource], links: List[models.Link]):
        for node in nodes:
            self.graph.node(node.id, node.name, image=node.image)

        for link in links:
            self.graph.edge(
                f"{link.source}:e",
                f"{link.destination}:w",
            )

    def render_graph(self, file_name, directory, output_format):
        self.graph.render(file_name, directory=directory, format=output_format)


def create_graph(nodes: List[models.Resource], links: List[models.Link]) -> Graph:
    graph = Graph()
    graph.assemble_graph(nodes, links)
    return graph
