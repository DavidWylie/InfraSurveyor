import logging

import boto3
from .. import models
from .boto_utilities import BaseAwsCollector


class SQSCollector(BaseAwsCollector):
    def __init__(self, region):
        self.sqs = boto3.resource("sqs", region_name=region)

    def get_queues(self):
        result = self.sqs.queues.all()
        return result


class SQSDataParser:
    @staticmethod
    def create_sqs_nodes(queues):
        queue_nodes = []
        for queue in queues:
            queue_nodes.append(
                models.Resource(
                    name=queue.attributes["QueueArn"].split(":")[-1],
                    resource_type="Queue",
                    id=queue.attributes["QueueArn"],
                    service="Amazon-Simple-Queue-Service",
                    category="APPLICATION_INTEGRATION",
                )
            )
        return queue_nodes

    @staticmethod
    def create_sqs_dlq_links(queues):
        dlq_links = []
        for queue in queues:
            sources = queue.dead_letter_source_queues.all()
            for source in sources:
                dlq_links.append(
                    models.Link(
                        source=source.attributes["QueueArn"],
                        destination=queue.attributes["QueueArn"],
                        link_type="DLQ",
                    )
                )
        return dlq_links


def get(nodes, links, region):
    logging.info("Starting SQS collection")
    collector = SQSCollector(region)
    data = collector.get_queues()
    parser = SQSDataParser()
    nodes.extend(parser.create_sqs_nodes(data))
    links.extend(parser.create_sqs_dlq_links(data))
    logging.info("SQS Collection Complete")
