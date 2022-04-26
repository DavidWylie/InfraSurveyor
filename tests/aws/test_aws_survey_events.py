import unittest
from helpers import MotoEventsHelper, MotoSnsHelper
from infra_surveyor.cloud.aws.event_rules import EventsCollector, EventsDataParser
from infra_surveyor.cloud.aws import event_rules
from moto import mock_events, mock_sns
from infra_surveyor.cloud.models import Resource, Link
import json


class TestAWSSurveyEvents(unittest.TestCase):
    DEFAULT_REGION = "eu-west-2"

    @mock_events
    def test_collector_get_rules(self):
        helper = MotoEventsHelper()
        event_pattern = {"source": ["test-source"]}
        rule_name = "test-rule-1"
        rule_arn = helper.create_rule(
            name=rule_name,
            schedule="rate(5 minutes)",
            event_pattern=json.dumps(event_pattern),
        )

        collector = EventsCollector("eu-west-2")
        rules = collector.get_rules()
        self.assertEqual(1, len(rules))
        self.assertEqual(rule_arn, rules[0]["Arn"])
        self.assertEqual(rule_name, rules[0]["Name"])

    @mock_events
    @mock_sns
    def test_Collector_get_targets(self):
        helper = MotoEventsHelper()
        event_pattern = {"source": ["test-source"]}
        rule_name = "test-rule-1"
        rule_arn = helper.create_rule(
            name=rule_name,
            schedule="rate(5 minutes)",
            event_pattern=json.dumps(event_pattern),
        )
        sns_helper = MotoSnsHelper()
        topic_arn = sns_helper.create_topic("test-topic")

        helper.add_target_to_rule(
            rule_name, [{"Id": "test-tarted-id", "Arn": topic_arn}]
        )
        collector = EventsCollector("eu-west-2")
        targets = collector.get_targets_for_rule(rule_name, "default")
        self.assertEqual(1, len(targets))
        self.assertEqual(topic_arn, targets[0]["Arn"])

    @mock_events
    @mock_sns
    def test_parser_add_nodes(self):
        helper = MotoEventsHelper()
        event_pattern = {"source": ["test-source"]}
        rule_name = "test-rule-1"
        rule_arn = helper.create_rule(
            name=rule_name,
            schedule="rate(5 minutes)",
            event_pattern=json.dumps(event_pattern),
        )

        expected_nodes = [
            Resource(
                id=rule_arn,
                name=rule_name,
                resource_type="Rule",
                service="Amazon-EventBridge",
                category="APPLICATION_INTEGRATION",
            )
        ]

        collector = EventsCollector("eu-west-2")
        rules = collector.get_rules()
        parser = EventsDataParser()
        nodes = parser.create_rule_nodes(rules)

        self.assertEqual(expected_nodes, nodes)

    @mock_events
    @mock_sns
    def test_parser_add_links(self):
        helper = MotoEventsHelper()
        event_pattern = {"source": ["test-source"]}
        rule_name = "test-rule-1"
        rule_arn = helper.create_rule(
            name=rule_name,
            schedule="rate(5 minutes)",
            event_pattern=json.dumps(event_pattern),
        )
        sns_helper = MotoSnsHelper()
        topic_arn = sns_helper.create_topic("test-topic")
        topic_arn_2 = sns_helper.create_topic("test-topic-2")

        helper.add_target_to_rule(
            rule_name,
            [
                {"Id": "test-tarted-id", "Arn": topic_arn},
                {"Id": "test-tarted-id-2", "Arn": topic_arn_2},
            ],
        )

        expected_links = [
            Link(source=rule_arn, destination=topic_arn, link_type=""),
            Link(source=rule_arn, destination=topic_arn_2, link_type=""),
        ]

        collector = EventsCollector("eu-west-2")
        targets = collector.get_targets_for_rule(rule_name, "default")

        parser = EventsDataParser()
        links = parser.create_rule_target_links(targets, rule_arn)

        self.assertEqual(expected_links, links)

    @mock_sns
    @mock_events
    def test_get(self):
        helper = MotoEventsHelper()
        event_pattern = {"source": ["test-source"]}
        rule_name = "test-rule-1"
        rule_arn = helper.create_rule(
            name=rule_name,
            schedule="rate(5 minutes)",
            event_pattern=json.dumps(event_pattern),
        )
        sns_helper = MotoSnsHelper()
        topic_arn = sns_helper.create_topic("test-topic")

        helper.add_target_to_rule(
            rule_name, [{"Id": "test-tarted-id", "Arn": topic_arn}]
        )

        expected_links = [
            Link(source="default", destination=rule_arn, link_type=""),
            Link(source=rule_arn, destination=topic_arn, link_type=""),
        ]

        expected_nodes = [
            Resource(
                id="default",
                name="default",
                resource_type="Default-Event-Bus",
                service="Amazon-EventBridge",
                category="APPLICATION_INTEGRATION",
            ),
            Resource(
                id=rule_arn,
                name=rule_name,
                resource_type="Rule",
                service="Amazon-EventBridge",
                category="APPLICATION_INTEGRATION",
            ),
        ]

        nodes = []
        links = []
        event_rules.get(nodes, links, self.DEFAULT_REGION)
        self.assertEqual(links, expected_links)
        self.assertEqual(nodes, expected_nodes)
