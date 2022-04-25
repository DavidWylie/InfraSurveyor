import unittest
import infra_surveyor_aws_icons


class TestAwsIconLoader(unittest.TestCase):
    def test_get_resource_icon(self):
        resource = infra_surveyor_aws_icons.Resource(
            category=infra_surveyor_aws_icons.Category.ANALYTICS,
            service="AWS-Glue",
            resource_type="Crawler",
        )

        loader = infra_surveyor_aws_icons.IconLoader()
        icon_path = loader.get_resource_icon(resource=resource)
        self.assertTrue(icon_path.exists())

    def test_get_service_icon(self):
        loader = infra_surveyor_aws_icons.IconLoader()
        icon_path = loader.get_service_icon(
            category=infra_surveyor_aws_icons.Category.ANALYTICS, service="Amazon-EMR"
        )
        self.assertTrue(icon_path.exists())

    def test_get_category_icon(self):
        loader = infra_surveyor_aws_icons.IconLoader()
        icon_path = loader.get_category_icon(
            category=infra_surveyor_aws_icons.Category.ANALYTICS,
        )

        self.assertTrue(icon_path.exists())
