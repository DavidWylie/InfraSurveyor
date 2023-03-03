import unittest
from infra_surveyor.cloud.aws import boto_utilities


class BotoUtilsTest(unittest.TestCase):
    def test_get_paginated_results_single_page(self):
        collector = boto_utilities.BaseAwsCollector()
        data = [{"b": "b"}, {"b": "b"}]
        result = collector.get_paginated_results(
            lambda marker: {"Functions": data},
            "NextMarker",
            "Functions",
        )
        self.assertEqual(data, result)

    def test_get_paginated_results_double_page(self):
        collector = boto_utilities.BaseAwsCollector()
        data = {
            "page_1": {"Targets": [{"b": "a"}, {"b": "b"}], "NextToken": "page_2"},
            "page_2": {"Targets": [{"b": "c"}, {"b": "d"}]},
        }

        data_expected = [
            {"b": "a"},
            {"b": "b"},
            {"b": "c"},
            {"b": "d"},
        ]

        result = collector.get_paginated_results(
            lambda marker: data.get(marker, data.get("page_1")),
            "NextToken",
            "Targets",
        )
        self.assertEqual(data_expected, result)

    def test_get_paginated_results_multi_page(self):
        collector = boto_utilities.BaseAwsCollector()
        data = {
            "page_1": {"Targets": [{"b": "a"}, {"b": "b"}], "NextToken": "page_2"},
            "page_2": {"Targets": [{"b": "c"}, {"b": "d"}], "NextToken": "page_3"},
            "page_3": {"Targets": [{"b": "e"}, {"b": "f"}]},
        }

        data_expected = [
            {"b": "a"},
            {"b": "b"},
            {"b": "c"},
            {"b": "d"},
            {"b": "e"},
            {"b": "f"},
        ]

        result = collector.get_paginated_results(
            lambda marker: data.get(marker, data.get("page_1")),
            "NextToken",
            "Targets",
        )
        self.assertEqual(data_expected, result)

    def test_get_paginated_results_none(self):
        collector = boto_utilities.BaseAwsCollector()
        data = []
        result = collector.get_paginated_results(
            lambda marker: {"Functions": data},
            "NextMarker",
            "Functions",
        )
        self.assertEqual(data, result)

    def test_parse_arn_service(self):
        test_arn = "arn:aws:autoscaling:eu-west-2::"
        arn = boto_utilities.parse_arn(test_arn)
        self.assertEqual("eu-west-2",arn.region)
        self.assertEqual("autoscaling", arn.service)
        self.assertEqual("aws", arn.partition)

    def test_parse_arn_resource_type(self):
        "arn:aws:events:eu-west-2:870594606895:rule/AutoScalingManagedRule"
        test_arn = "arn:aws:lambda:eu-west-2:<accountNo>:function:exampleFunction"
        arn = boto_utilities.parse_arn(test_arn)
        self.assertEqual("eu-west-2",arn.region)
        self.assertEqual("lambda", arn.service)
        self.assertEqual("aws", arn.partition)
        self.assertEqual("<accountNo>", arn.account)
        self.assertEqual("function", arn.resource_type)
        self.assertEqual("exampleFunction", arn.resource_id)

    def test_parse_arn_resource_type_slash(self):

        test_arn = "arn:aws:events:eu-west-2:<accountNo>:rule/ExampleRule"
        arn = boto_utilities.parse_arn(test_arn)
        self.assertEqual("eu-west-2",arn.region)
        self.assertEqual("events", arn.service)
        self.assertEqual("aws", arn.partition)
        self.assertEqual("<accountNo>", arn.account)
        self.assertEqual("ExampleRule", arn.resource_id)
        self.assertEqual("rule", arn.resource_type)

    def test_parse_arn_resource(self):
        test_arn = "arn:aws:autoscaling:eu-west-2:<accountNo>:<exampleId>"
        arn = boto_utilities.parse_arn(test_arn)
        self.assertEqual("eu-west-2",arn.region)
        self.assertEqual("autoscaling", arn.service)
        self.assertEqual("aws", arn.partition)
        self.assertEqual("<exampleId>", arn.resource_id)


if __name__ == "__main__":
    unittest.main()
