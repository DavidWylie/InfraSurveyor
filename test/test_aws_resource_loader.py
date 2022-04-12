import unittest
import surveyor_aws_icons


class TestAwsIconLoader(unittest.TestCase):
    def test_get_resource_icon(self):
        resource = surveyor_aws_icons.Resource(
            category=surveyor_aws_icons.Category.ANALYTICS,
            service="AWS-Glue",
            resource_type="Crawler",
        )

        loader = surveyor_aws_icons.IconLoader()
        icon_path = loader.get_resource_icon(resource=resource)
        self.assertTrue(icon_path.exists())

    def test_get_service_icon(self):
        loader = surveyor_aws_icons.IconLoader()
        icon_path = loader.get_service_icon(
            category=surveyor_aws_icons.Category.ANALYTICS, service="Amazon-EMR"
        )
        self.assertTrue(icon_path.exists())

    def test_get_category_icon(self):
        loader = surveyor_aws_icons.IconLoader()
        icon_path = loader.get_category_icon(
            category=surveyor_aws_icons.Category.ANALYTICS,
        )

        self.assertTrue(icon_path.exists())
