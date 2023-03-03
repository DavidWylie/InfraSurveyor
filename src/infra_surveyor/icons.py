import logging
from typing import List

import infra_surveyor_aws_icons as aws_icons
from .cloud import models


def load_icons(nodes: List[models.Resource]):
    loader = aws_icons.IconLoader()
    for node in nodes:
        if node.node_type == "resource":
            icon_resource = aws_icons.Resource(
                resource_type=node.resource_type,
                service=node.service,
                category=aws_icons.Category[node.category],
            )
            icon_path = loader.get_resource_icon(resource=icon_resource)
            node.image = str(icon_path)
        elif node.node_type == "service":
            icon_path = loader.get_service_icon(
                category=aws_icons.Category[node.category], service=node.service
            )
            node.image = str(icon_path)
        else:
            icon_resource = aws_icons.Resource(
                resource_type=node.resource_type,
                service=node.service,
                category=aws_icons.Category.GENERAL,
            )
            icon_path = loader.get_resource_icon(resource=icon_resource)
            node.image = str(icon_path)

    logging.info(f"AWS-19 Icons Applied version: {aws_icons.version}")
