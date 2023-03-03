from . import (
    lambda_functions,
    sqs_queues,
    sns_topics,
    event_rules,
    ec2_autoscaling,
    states,
    code_guru,
)
from .. import models
from typing import List

REGION = "eu-west-2"
services = [sqs_queues, sns_topics, event_rules, lambda_functions]
static_services = [ec2_autoscaling, states, code_guru]


def survey_events() -> (List[models.Resource], List[models.Link]):
    global REGION

    nodes = []
    links = []
    for service in services:
        service.get(nodes, links, REGION)
    for static_service in static_services:
        static_service.create_linked_services(nodes, links)
    return nodes, links
