import graphviz
from infra_surveyor.cloud import models
from typing import List
import hashlib


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
                "height": "0.9",
                "labelloc": "b",
                "imagepos": "tc",
                "fontname": "Sans-Serif",
                "fontsize": "13",
                "fontcolor": "#2D3436",
            },
        )

    def _hash_id(self, id: str) -> str:
        return hashlib.sha256(id.encode()).hexdigest()

    def assemble_graph(self, nodes: List[models.Resource], links: List[models.Link]):
        for node in nodes:
            safe_id = self._hash_id(node.id)
            neat_name = node.name
            self.graph.node(safe_id, neat_name, image=node.image)

        for link in links:
            safe_source = self._hash_id(link.source)
            safe_dest = self._hash_id(link.destination)
            self.graph.edge(
                f"{safe_source}:e",
                f"{safe_dest}:w",
            )

    def render_graph(self, file_name, directory, output_format):
        self.graph.render(file_name, directory=directory, format=output_format)


def create_graph(nodes: List[models.Resource], links: List[models.Link]) -> Graph:
    graph = Graph()
    graph.assemble_graph(nodes, links)
    return graph
