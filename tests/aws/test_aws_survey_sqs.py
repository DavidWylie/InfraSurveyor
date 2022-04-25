import unittest
from helpers import MotoSqsHelper
from infra_surveyor.cloud.aws.sqs_queues import SQSCollector, SQSDataParser
from infra_surveyor.cloud.aws import sqs_queues
from moto import mock_sqs
from infra_surveyor.cloud.models import Resource, Link


class TestAWSSurveySQS(unittest.TestCase):
    DEFAULT_REGION = "eu-west-2"

    @mock_sqs
    def test_collector_get_queues(self):
        sqs_helper = MotoSqsHelper()
        sqs_arn_1 = sqs_helper.create_queue("First_queue")
        sqs_arn_2 = sqs_helper.create_queue("Second_queue")

        collector = SQSCollector("eu-west-2")
        result = collector.get_queues()
        self.assertEqual(2, len(list(result)))

    @mock_sqs
    def test_parser_create_sqs_nodes(self):
        sqs_helper = MotoSqsHelper()
        sqs_arn_1 = sqs_helper.create_queue("First_queue")
        sqs_arn_2 = sqs_helper.create_queue("Second_queue")

        expected_nodes = [
            Resource(
                name="First_queue",
                resource_type="Queue",
                id=sqs_arn_1,
                service="Amazon-Simple-Queue-Service",
                category="APPLICATION_INTEGRATION",
            ),
            Resource(
                name="Second_queue",
                resource_type="Queue",
                id=sqs_arn_2,
                service="Amazon-Simple-Queue-Service",
                category="APPLICATION_INTEGRATION",
            ),
        ]
        collector = SQSCollector("eu-west-2")
        data = collector.get_queues()
        parser = SQSDataParser()
        nodes = parser.create_sqs_nodes(data)
        self.assertEqual(nodes, expected_nodes)

    @mock_sqs
    def test_parser_create_sqs_dlq_links(self):
        sqs_helper = MotoSqsHelper()

        sqs_arn_dlq = sqs_helper.create_queue("First_DLQ")
        sqs_arn_1 = sqs_helper.create_queue_with_dlq("First_queue", sqs_arn_dlq)

        expected_links = [
            Link(source=sqs_arn_1, destination=sqs_arn_dlq, link_type="DLQ")
        ]
        collector = SQSCollector("eu-west-2")
        data = collector.get_queues()
        parser = SQSDataParser()
        links = parser.create_sqs_dlq_links(data)
        self.assertEqual(links, expected_links)

    @mock_sqs
    def test_get(self):
        sqs_helper = MotoSqsHelper()

        sqs_arn_dlq = sqs_helper.create_queue("First_DLQ")
        sqs_arn_1 = sqs_helper.create_queue_with_dlq("First_queue", sqs_arn_dlq)

        expected_nodes = [
            Resource(
                name="First_DLQ",
                resource_type="Queue",
                id=sqs_arn_dlq,
                service="Amazon-Simple-Queue-Service",
                category="APPLICATION_INTEGRATION",
            ),
            Resource(
                name="First_queue",
                resource_type="Queue",
                id=sqs_arn_1,
                service="Amazon-Simple-Queue-Service",
                category="APPLICATION_INTEGRATION",
            ),
        ]

        expected_links = [
            Link(source=sqs_arn_1, destination=sqs_arn_dlq, link_type="DLQ")
        ]

        nodes = []
        links = []
        sqs_queues.get(nodes, links, self.DEFAULT_REGION)
        self.assertEqual(links, expected_links)
        self.assertEqual(nodes, expected_nodes)


if __name__ == "__main__":
    unittest.main()
