import boto3
from .. import models


def get_lambdas(nodes, links):
    client = boto3.client("lambda")
    result = client.list_functions()
    for function in result["Functions"]:
        function_name = function["FunctionName"]
        create_function_nodes(function, function_name, nodes)
        # Not mocked at present via moto
        # create_invoke_links(client, function_name, links)
    create_event_source_links(client, links)


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


def create_event_source_links(client, links):
    response = client.list_event_source_mappings(
        MaxItems=123
    )
    items = response["EventSourceMappings"]
    marker = response.get("NextMarker", False)
    while marker:
        items.extend(response["EventSourceMappings"])
        marker = response.get("NextMarker", False)

    for item in items:
        links.append(
            models.Link(
              source=item["EventSourceArn"],
              destination=item["FunctionArn"],
              link_type=""
            )
        )
        dlq = item.get("DestinationConfig",{}).get("OnFailure",{})
        if dlq:
            links.append(
                models.Link(
                    source=item["FunctionArn"],
                    destination=dlq["Destination"],
                    link_type="DLQ"
                )
            )
