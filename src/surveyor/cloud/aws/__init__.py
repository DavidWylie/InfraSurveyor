from .lambda_functions import get_lambdas

def survey_events():
    nodes = []
    links = []
    # get eventRules
    get_lambdas(nodes, links)

    # get sqs
    # get sns
    return nodes, links
