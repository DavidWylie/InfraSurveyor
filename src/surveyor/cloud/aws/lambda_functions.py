import boto3
from .. import models


def get_lambdas(nodes, links):
    client = boto3.client("lambda")
    functions = client.list_functions()
    for function in functions:
        function_name = function["FunctionName"]
        create_function_nodes(function, function_name, nodes)
        create_invoke_links(client, function_name, links)


def create_function_nodes(function, function_name, nodes):
    node = models.Resource(
        name=function_name,
        resource_type="Lambda-Function",
        id=function["FunctionArn"],
        service="AWS-Lambda",
        category="COMPUTE",
    )
    nodes.append(node)


def create_invoke_links(client, function_name, links):
    invoke_configs = client.list_function_event_invoke_configs(
        FunctionName=function_name
    )
    for invoke_config in invoke_configs:
        config = invoke_config.get("DestinationConfig")
        success_config = config.get("OnSuccess", {})

        if success_config:
            links.append(
                models.Link(
                    source=config["FunctionArn"],
                    destination=success_config["Destination"],
                    link_type="OnSuccess",
                )
            )

        failure_config = config.get("OnFailure", {})
        if failure_config:
            links.append(
                models.Link(
                    source=config["FunctionArn"],
                    destination=success_config["Destination"],
                    link_type="OnFailure",
                )
            )
