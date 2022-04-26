import logging

import boto3
from .. import models
from .boto_utilities import BaseAwsCollector
from typing import List


class EventsCollector(BaseAwsCollector):
    def __init__(self, region):
        self.client = boto3.client("events", region_name=region)
        self.limit = 50

    def get_buses(self):
        return self.get_paginated_results(
            lambda marker: self.client.list_event_buses(
                NextToken=marker, Limit=self.limit
            )
            if marker
            else self.client.list_event_buses(Limit=self.limit),
            "NextToken",
            "EventBuses",
        )

    def get_rules(self, bus="default"):
        return self.get_paginated_results(
            lambda marker: self.client.list_rules(
                EventBusName=bus, NextToken=marker, Limit=self.limit
            )
            if marker
            else self.client.list_rules(EventBusName=bus, Limit=self.limit),
            "NextToken",
            "Rules",
        )

    def get_targets_for_rule(self, rule_name, event_bus):
        return self.get_paginated_results(
            lambda marker: self.client.list_targets_by_rule(
                NextToken=marker,
                Rule=rule_name,
                EventBusName=event_bus,
                Limit=self.limit,
            )
            if marker
            else self.client.list_targets_by_rule(
                Rule=rule_name, EventBusName=event_bus, Limit=self.limit
            ),
            "NextToken",
            "Targets",
        )


class EventsDataParser:
    def create_bus_nodes(self, items) -> List[models.Resource]:
        buses = []
        for item in items:
            buses.append(self.create_bus_node(item))

        return buses

    def create_bus_node(self, item) -> models.Resource:
        if item["Name"] == "default":
            return models.Resource(
                name="default",
                resource_type="Default-Event-Bus",
                id=item["Name"],
                service="Amazon-EventBridge",
                category="APPLICATION_INTEGRATION",
            )
        else:
            return models.Resource(
                name=item["Name"],
                resource_type="Custom-Event-Bus",
                id=item["Name"],
                service="Amazon-EventBridge",
                category="APPLICATION_INTEGRATION",
            )

    def create_rule_nodes(self, items) -> List[models.Resource]:
        rule_nodes = []
        for item in items:
            rule_nodes.append(self.create_rule_node(item))

        return rule_nodes

    @staticmethod
    def create_rule_node(item) -> models.Resource:
        return models.Resource(
            name=item["Name"],
            resource_type="Rule",
            id=item["Arn"],
            service="Amazon-EventBridge",
            category="APPLICATION_INTEGRATION",
        )

    def create_rule_target_links(self, items, rule_arn) -> List[models.Link]:
        target_links = []
        for item in items:
            target_links.append(self.create_rule_target_link(item, rule_arn))

        return target_links

    @staticmethod
    def create_rule_target_link(item, rule_arn) -> models.Link:
        return models.Link(source=rule_arn, destination=item["Arn"], link_type="")

    def create_rule_bus_links(self, items):
        bus_links = []
        for item in items:
            bus_links.append(self.create_rule_bus_link(item))
        return bus_links

    @staticmethod
    def create_rule_bus_link(item):
        return models.Link(
            source=item["EventBusName"], destination=item["Arn"], link_type=""
        )


def get(nodes, links, region):
    logging.info("Starting Event Collection")
    collector = EventsCollector(region)
    parser = EventsDataParser()
    buses = collector.get_buses()
    nodes.extend(parser.create_bus_nodes(buses))

    rules = []
    for bus in buses:
        rules.extend(collector.get_rules(bus=bus["Name"]))

    nodes.extend(parser.create_rule_nodes(rules))
    links.extend(parser.create_rule_bus_links(rules))
    for rule in rules:
        targets = collector.get_targets_for_rule(
            rule_name=rule["Name"], event_bus=rule["EventBusName"]
        )
        links.extend(parser.create_rule_target_links(targets, rule["Arn"]))

    logging.info("Event Collection Complete")
