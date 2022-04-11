import unittest
from surveyor import models, graphing
import surveyor_aws_icons


class TestGraphing(unittest.TestCase):
    def test_create_simple_graph(self):
        image_1 = str(surveyor_aws_icons.get_resource_icon(
            surveyor_aws_icons.Resource(
                category=surveyor_aws_icons.Category.COMPUTE,
                resource_type="Lambda-Function",
                service="AWS-Lambda"
            ),
            icon_set=surveyor_aws_icons.ResourceIconSet.LIGHT,
            image_format=surveyor_aws_icons.ImageFormat.SVG
        ))
        nodes = [
            models.Resource("First", "Aws-Lambda", "test-1-arn", image_1),
            models.Resource("Second", "Aws-Lambda", "test-2-arn", image_1),
            models.Resource("Third", "Aws-Lambda", "test-3-arn", image_1),
            models.Resource("Forth", "Aws-Lambda", "test-4-arn", image_1),
            models.Resource("Fith", "Aws-Lambda", "test-5-arn", image_1)
        ]

        links = [
            models.Link("test-1-arn", "test-2-arn", "testing"),
            models.Link("test-1-arn", "test-3-arn", "testing"),
            models.Link("test-1-arn", "test-4-arn", "testing"),
            models.Link("test-1-arn", "test-5-arn", "testing"),

            models.Link("test-2-arn", "test-4-arn", "testing"),
            models.Link("test-3-arn", "test-5-arn", "testing")
        ]
        graph = graphing.Graph()
        graph.assemble_graph(nodes, links)
        graph.render_graph("test-chart", ".", "png")
        # Check graph creation doesnt cause code error.
        self.assertTrue(True)
