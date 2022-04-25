import unittest
from infra_surveyor.cloud.aws import boto_utilities


class MyTestCase(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
