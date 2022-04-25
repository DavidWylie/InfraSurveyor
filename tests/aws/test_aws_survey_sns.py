import unittest
from moto import mock_sns, mock_sqs
from helpers import MotoSnsHelper, MotoSqsHelper

from infra_surveyor.cloud.aws.sns_topics import SNSCollector, SNSResultsParser
from infra_surveyor.cloud.aws import sns_topics
from infra_surveyor.cloud.models import Resource, Link


class TestAWSSurveySNS(unittest.TestCase):
    DEFAULT_REGION = "eu-west-2"

    @mock_sns
    def test_collector_get_sns_topics(self):
        helper = MotoSnsHelper()
        topic_arn = helper.create_topic("firstTopic")

        collector = SNSCollector("eu-west-2")
        topics = collector.get_topics()
        self.assertEqual(1, len(topics))
        self.assertEqual(topic_arn, topics[0]["TopicArn"])

    @mock_sns
    @mock_sqs
    def test_collector_get_sns_subscriptions(self):
        sqs_helper = MotoSqsHelper()
        sqs_arn = sqs_helper.create_queue("firstQueue")
        sns_helper = MotoSnsHelper()
        topic_arn = sns_helper.create_topic("firstTopic")
        sns_helper.create_subscription_to_queue(topic_arn=topic_arn, queue_arn=sqs_arn)

        collector = SNSCollector("eu-west-2")
        subscriptions = collector.get_subscriptions()

        self.assertEqual(topic_arn, subscriptions[0]["TopicArn"])
        self.assertEqual(sqs_arn, subscriptions[0]["Endpoint"])  # add assertion here

    @mock_sns
    def test_parser_create_topic_nodes(self):
        sns_helper = MotoSnsHelper()
        topic_arn_1 = sns_helper.create_topic("firstTopic")
        topic_arn_2 = sns_helper.create_topic("secondTopic")

        expected_nodes = [
            Resource(
                name="firstTopic",
                id=topic_arn_1,
                resource_type="Topic",
                service="Amazon-Simple-Notification-Service",
                category="APPLICATION_INTEGRATION",
            ),
            Resource(
                name="secondTopic",
                id=topic_arn_2,
                resource_type="Topic",
                service="Amazon-Simple-Notification-Service",
                category="APPLICATION_INTEGRATION",
            ),
        ]

        collector = SNSCollector("eu-west-2")
        data = collector.get_topics()

        parser = SNSResultsParser()
        nodes = parser.create_topic_nodes(data)
        self.assertEqual(expected_nodes, nodes)

    @mock_sqs
    @mock_sns
    def test_parser_create_subscription_links(self):
        sqs_helper = MotoSqsHelper()
        sqs_arn = sqs_helper.create_queue("firstQueue")
        sns_helper = MotoSnsHelper()
        topic_arn = sns_helper.create_topic("firstTopic")
        sns_helper.create_subscription_to_queue(topic_arn=topic_arn, queue_arn=sqs_arn)

        expected_links = [
            Link(source=topic_arn, destination=sqs_arn, link_type="subscription")
        ]

        collector = SNSCollector("eu-west-2")
        data = collector.get_subscriptions()

        parser = SNSResultsParser()
        links = parser.create_subscription_links(data)
        self.assertEqual(expected_links, links)

    @mock_sns
    @mock_sqs
    def test_get(self):
        sqs_helper = MotoSqsHelper()
        sqs_arn = sqs_helper.create_queue("firstQueue")
        sns_helper = MotoSnsHelper()
        topic_arn = sns_helper.create_topic("firstTopic")
        sns_helper.create_subscription_to_queue(topic_arn=topic_arn, queue_arn=sqs_arn)

        expected_nodes = [
            Resource(
                name="firstTopic",
                id=topic_arn,
                resource_type="Topic",
                service="Amazon-Simple-Notification-Service",
                category="APPLICATION_INTEGRATION",
            )
        ]

        expected_links = [
            Link(source=topic_arn, destination=sqs_arn, link_type="subscription")
        ]

        nodes = []
        links = []
        sns_topics.get(nodes, links, self.DEFAULT_REGION)

        self.assertEqual(links, expected_links)
        self.assertEqual(nodes, expected_nodes)


if __name__ == "__main__":
    unittest.main()
