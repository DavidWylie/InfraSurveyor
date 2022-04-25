import unittest
from infra_surveyor import graphing
from infra_surveyor.cloud.models import Resource, Link
import os


class TestGraphing(unittest.TestCase):
    def _create_test_nodes(self):
        test_dir = os.path.dirname(__file__)
        image_1 = (
            f"{test_dir}/../"
            "src/"
            "infra_surveyor_aws_icons/"
            "Resource-Icons_01312022/"
            "Res_Quantum-Technologies/Res_48_Light/"
            "Res_Amazon-Braket_QPU _48_Light.svg"
        )
        nodes = [
            Resource(
                name="First",
                resource_type="Aws-Lambda",
                id="test-1-arn",
                service="test",
                category="test",
                image=image_1,
            ),
            Resource(
                name="Second",
                resource_type="Aws-Lambda",
                id="test-2-arn",
                service="test",
                category="test",
                image=image_1,
            ),
            Resource(
                name="Third",
                resource_type="Aws-Lambda",
                id="test-3-arn",
                service="test",
                category="test",
                image=image_1,
            ),
            Resource(
                name="Forth",
                resource_type="Aws-Lambda",
                id="test-4-arn",
                service="test",
                category="test",
                image=image_1,
            ),
            Resource(
                name="Fifth",
                resource_type="Aws-Lambda",
                id="test-5-arn",
                service="test",
                category="test",
                image=image_1,
            ),
        ]
        return nodes

    def test_create_simple_graph(self):
        nodes = self._create_test_nodes()
        links = [
            Link("test-1-arn", "test-2-arn", "testing"),
            Link("test-1-arn", "test-3-arn", "testing"),
            Link("test-1-arn", "test-4-arn", "testing"),
            Link("test-1-arn", "test-5-arn", "testing"),
        ]
        graph = graphing.Graph()
        graph.assemble_graph(nodes, links)
        graph.render_graph("test-chart", "out", "png")
        # Check graph creation doesnt cause code error.
        self.assertTrue(True)

    def test_create_graph(self):
        nodes = self._create_test_nodes()
        links = [
            Link("test-1-arn", "test-2-arn", "testing"),
            Link("test-1-arn", "test-3-arn", "testing"),
            Link("test-1-arn", "test-4-arn", "testing"),
            Link("test-1-arn", "test-5-arn", "testing"),
        ]
        graph = graphing.create_graph(nodes, links)
        self.assertIsInstance(graph, graphing.Graph)
