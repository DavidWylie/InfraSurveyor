from typing import Callable, Dict
from collections import namedtuple

Arn = namedtuple(
    "Arn", ["partition", "service", "region", "account", "resource_id", "resource_type"]
)


def parse_arn(arn):
    parts = arn.split(":")
    resource_type = ""
    resource_id = ""
    if len(parts) == 7:
        resource_type = parts[5]
        resource_id = parts[6]
    elif len(parts) == 6:
        resource_parts = parts[5].split("/")
        if len(resource_parts) == 2:
            resource_type = resource_parts[0]
            resource_id = resource_parts[1]
        else:
            resource_id = parts[5]

    return Arn(
        partition=parts[1],
        service=parts[2],
        region=parts[3],
        account=parts[4],
        resource_type=resource_type,
        resource_id=resource_id,
    )


class BaseAwsCollector:
    @staticmethod
    def get_paginated_results(
        action_method: Callable[[str], Dict],
        marker_field_name: str,
        results_field_name: str,
    ):
        items = []
        result = action_method("")
        marker = result.get(marker_field_name, False)
        items.extend(result.get(results_field_name, []))
        while marker:
            result = action_method(marker)
            marker = result.get(marker_field_name, False)
            items.extend(result.get(results_field_name, []))

        return items
