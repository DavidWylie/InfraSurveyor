import unittest
import surveyor_aws_icons

class TestAwsIconLoader(unittest.TestCase):
    def test_get_resource_icon(self):
        resource = surveyor_aws_icons.Resource(
            category=surveyor_aws_icons.Category.ANALYTICS,
            service="AWS-Glue",
            type="Crawler"
        )
        icon_path = surveyor_aws_icons.get_resource_icon(
            resource=resource,
            icon_set=surveyor_aws_icons.ResourceIconSet.LIGHT,
            image_format=surveyor_aws_icons.ImageFormat.PNG
        )
        self.assertTrue(icon_path.exists())

    def test_get_service_icon(self):
        icon_path = surveyor_aws_icons.get_service_icon(
            category=surveyor_aws_icons.Category.ANALYTICS,
            service="Amazon-EMR",
            icon_set=surveyor_aws_icons.ServiceIconSet.ARCH_48,
            image_format=surveyor_aws_icons.ImageFormat.SVG
        )
        self.assertTrue(icon_path.exists())

    def test_get_category_icon(self):
        icon_path = surveyor_aws_icons.get_category_icon(
            category=surveyor_aws_icons.Category.ANALYTICS,
            icon_set=surveyor_aws_icons.CategoryIconSet.ARCH_32,
            image_format=surveyor_aws_icons.ImageFormat.PNG
        )

        self.assertTrue(icon_path.exists())