from . import lambda_functions, sqs_queues, sns_topics, event_rules
from .. import models
from typing import List

REGION = "eu-west-2"
services = [sqs_queues, sns_topics, event_rules, lambda_functions]


def survey_events() -> (List[models.Resource], List[models.Link]):
    global REGION

    nodes = []
    links = []
    for service in services:
        service.get(nodes, links, REGION)

    return nodes, links
