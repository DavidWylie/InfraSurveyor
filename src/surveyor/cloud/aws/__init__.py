from .lambda_functions import get_lambdas
from .. import models
from typing import List

REGION = "eu-west-2"

def survey_events() -> (List[models.Resource], List[models.Link]):
    nodes = []
    links = []
    # get eventRules
    get_lambdas(nodes, links)

    # get sqs
    # get sns
    return nodes, links
