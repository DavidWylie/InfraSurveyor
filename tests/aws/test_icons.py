import unittest
from infra_surveyor import icons
from infra_surveyor.cloud import models
from infra_surveyor_aws_icons.loader import _get_resource_dir


class TestIcon(unittest.TestCase):
    def test_load_empty_nodes(self):
        nodes = []
        expected_icons = []
        icons.load_icons(nodes)
        self.assertEqual(expected_icons, nodes)

    def test_load_existing_icon(self):
        nodes = [
            models.Resource(
                id="test-id",
                name="test",
                category="ANALYTICS",
                service="AWS-Glue",
                resource_type="Crawler",
            )
        ]
        expected_nodes = [
            models.Resource(
                id="test-id",
                name="test",
                category="ANALYTICS",
                service="AWS-Glue",
                resource_type="Crawler",
                image=f"{_get_resource_dir()}/Resource-Icons_01312022/Res_Analytics/Res_48_Light/Res_AWS-Glue_Crawler_48_Light.svg",
            )
        ]
        icons.load_icons(nodes)
        self.assertEqual(expected_nodes, nodes)


if __name__ == "__main__":
    unittest.main()
