from typing import Callable, Dict
from collections import namedtuple

Arn = namedtuple(
    "Arn", ["partition", "service", "region", "resource_id", "resource_type"]
)


def parse_arn(arn):
    parts = arn.split(":")
    resource_type = ""
    resource_id = ""
    if len(parts) == 5:
        resource_type = parts[3]
        resource_id = parts[4]
    elif len(parts) == 4:
        resource_parts = parts[3].split("/")
        if len(resource_parts) == 2:
            resource_type = parts[0]
            resource_id = parts[1]
        else:
            resource_id = parts[3]

    return Arn(
        partition=parts[0],
        service=parts[1],
        region=parts[2],
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
