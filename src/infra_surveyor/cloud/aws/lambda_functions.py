import logging

import boto3
from .. import models
from .boto_utilities import BaseAwsCollector


class LambdaDataCollector(BaseAwsCollector):
    def __init__(self, region):
        self.client = boto3.client("lambda", region_name=region)

    def get_functions(self):
        return self.get_paginated_results(
            lambda marker: self.client.list_functions(Marker=marker, MaxItems=20)
            if marker
            else self.client.list_functions(MaxItems=20),
            "NextMarker",
            "Functions",
        )

    def get_event_source_mappings(self):
        return self.get_paginated_results(
            lambda marker: self.client.list_event_source_mappings(
                Marker=marker, MaxItems=20
            )
            if marker
            else self.client.list_event_source_mappings(MaxItems=20),
            "NextMarker",
            "EventSourceMappings",
        )


class LambdaResultsParser:
    def create_function_nodes(self, items):
        function_nodes = []
        for item in items:
            function_nodes.append(self.create_function_node(item))
        return function_nodes

    @staticmethod
    def create_function_node(function):
        return models.Resource(
            name=function["FunctionName"],
            resource_type="Lambda-Function",
            id=function["FunctionArn"],
            service="AWS-Lambda",
            category="COMPUTE",
        )

    def create_event_source_links(self, items):
        event_source_links = []
        for event_source in items:
            event_source_links.append(self.create_event_source_link(event_source))
            event_source_links.extend(
                self.create_destination_config_links(event_source)
            )
        return event_source_links

    @staticmethod
    def create_event_source_link(event_source):
        return models.Link(
            source=event_source["EventSourceArn"],
            destination=event_source["FunctionArn"],
            link_type="",
        )

    def create_destination_config_links(self, item):
        config_links = []
        config = item.get("DestinationConfig", {})
        self._create_config_link(config, "OnSuccess", config_links, "")
        self._create_config_link(config, "OnFailure", config_links, "DLQ")

        return config_links

    @staticmethod
    def _create_config_link(item, config_name, config_links, link_name):
        config = item.get(config_name, {})
        if config:
            config_links.append(
                models.Link(
                    source=config["FunctionArn"],
                    destination=config["Destination"],
                    link_type=link_name,
                )
            )


def get(nodes, links, region):
    logging.info("Starting Lambda collection")
    collector = LambdaDataCollector(region)
    items = collector.get_functions()

    parser = LambdaResultsParser()
    nodes.extend(parser.create_function_nodes(items))

    event_sources = collector.get_event_source_mappings()
    links.extend(parser.create_event_source_links(event_sources))
    logging.info("Lambda Collection Complete")
