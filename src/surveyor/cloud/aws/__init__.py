from . import lambda_functions, sqs_queues, sns_topics
from .. import models
from typing import List

REGION = "eu-west-2"


def survey_events() -> (List[models.Resource], List[models.Link]):
    global REGION

    nodes = []
    links = []
    # get eventRules
    lambda_functions.get(nodes, links, REGION)
    sqs_queues.get(nodes, links, REGION)
    sns_topics.get(nodes, links, REGION)

    return nodes, links
