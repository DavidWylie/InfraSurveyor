import logging
from typing import List

import infra_surveyor_aws_icons
import infra_surveyor_aws_icons as aws_icons
from .cloud import models


def load_icons(nodes: List[models.Resource]):
    loader = aws_icons.IconLoader()
    for node in nodes:
        icon_resource = aws_icons.Resource(
            resource_type=node.resource_type,
            service=node.service,
            category=aws_icons.Category[node.category],
        )
        icon_path = loader.get_resource_icon(resource=icon_resource)
        node.image = str(icon_path)

    logging.info(f"AWS-19 Icons Applied version: {infra_surveyor_aws_icons.version}")
