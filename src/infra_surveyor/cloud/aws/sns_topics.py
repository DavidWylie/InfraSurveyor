import logging

import boto3
from .. import models
from .boto_utilities import BaseAwsCollector


class SNSCollector(BaseAwsCollector):
    def __init__(self, region):
        self.sns = boto3.client("sns", region_name=region)

    def get_topics(self):
        return self.get_paginated_results(
            lambda marker: self.sns.list_topics(NextToken=marker), "NextToken", "Topics"
        )

    def get_subscriptions(self):
        return self.get_paginated_results(
            lambda marker: self.sns.list_subscriptions(NextToken=marker),
            "NextToken",
            "Subscriptions",
        )


class SNSResultsParser:
    def create_topic_nodes(self, items):
        topic_nodes = []
        for item in items:
            topic_nodes.append(self.create_topic_node(item))
        return topic_nodes

    @staticmethod
    def create_topic_node(item):
        return models.Resource(
            name=item["TopicArn"].split(":")[-1],
            resource_type="Topic",
            id=item["TopicArn"],
            service="Amazon-Simple-Notification-Service",
            category="APPLICATION_INTEGRATION",
        )

    def create_subscription_links(self, items):
        subscription_links = []
        for item in items:
            subscription_links.append(self.create_subscription_link(item))
        return subscription_links

    @staticmethod
    def create_subscription_link(item):
        return models.Link(
            source=item["TopicArn"],
            destination=item["Endpoint"],
            link_type="subscription",
        )

    def create_subscription_nodes(self, items):
        topic_nodes = []
        for item in items:
            if item["Protocol"] in ["email", "http"]:
                topic_nodes.append(self.create_subscription_node(item))
        return topic_nodes

    @staticmethod
    def create_subscription_node(item):
        resource_types = {"email": "Email-Notification", "http": "HTTP-Notification"}
        return models.Resource(
            name=item["Endpoint"],
            resource_type=resource_types.get(item["Protocol"], item["Protocol"]),
            id=item["Endpoint"],
            service="Amazon-Simple-Notification-Service",
            category="APPLICATION_INTEGRATION",
        )


def get(nodes, links, region):
    logging.info("Starting SNS Collection")
    collector = SNSCollector(region)
    parser = SNSResultsParser()

    topics = collector.get_topics()
    nodes.extend(parser.create_topic_nodes(topics))

    subscriptions = collector.get_subscriptions()
    nodes.extend(parser.create_subscription_nodes(subscriptions))
    links.extend(parser.create_subscription_links(subscriptions))
    logging.info("SNS Collection Complete")
