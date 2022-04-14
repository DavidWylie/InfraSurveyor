import boto3
from .. import models
from .boto_utilities import BaseAwsCollector


class EventsCollector(BaseAwsCollector):
    def __init__(self, region):
        self.client = boto3.client("events", region_name=region)

    def get_rules(self):
        return self.get_paginated_results(
            lambda marker: self.client.list_rules(NextToken=marker)
            if marker
            else self.client.list_rules(),
            "NextToken",
            "Rules",
        )

    def get_targets_for_rule(self, rule_name):
        return self.get_paginated_results(
            lambda marker: self.client.list_targets_by_rule(
                NextToken=marker, Rule=rule_name
            )
            if marker
            else self.client.list_targets_by_rule(Rule=rule_name),
            "NextToken",
            "Targets",
        )


class EventsDataParser:
    def create_rule_nodes(self, items):
        rule_nodes = []
        for item in items:
            rule_nodes.append(self.create_rule_node(item))

        return rule_nodes

    @staticmethod
    def create_rule_node(item):
        return models.Resource(
            name=item["Name"],
            resource_type="Rule",
            id=item["Arn"],
            service="Amazon-EventBridge",
            category="APPLICATION_INTEGRATION",
        )

    def create_rule_target_links(self, items, rule_arn):
        target_links = []
        for item in items:
            target_links.append(self.create_rule_target_link(item, rule_arn))

        return target_links

    @staticmethod
    def create_rule_target_link(item, rule_arn):
        return models.Link(source=rule_arn, destination=item["Arn"], link_type="")


def get(nodes, links, region):
    collector = EventsCollector(region)
    parser = EventsDataParser()

    rules = collector.get_rules()
    nodes.extend(parser.create_rule_nodes(rules))
    for rule in rules:
        targets = collector.get_targets_for_rule(rule["Name"])
        links.extend(parser.create_rule_target_links(targets, rule["Arn"]))
