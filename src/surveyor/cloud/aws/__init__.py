from . import lambda_functions, sqs_queues
from .. import models
from typing import List

REGION = "eu-west-2"

def survey_events() -> (List[models.Resource], List[models.Link]):
    global REGION

    nodes = []
    links = []
    # get eventRules
    lambda_functions.get_lambdas(nodes, links, REGION)
    sqs_queues.get_queues(nodes, links, REGION)

    # get sns

    return nodes, links
