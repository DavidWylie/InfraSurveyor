from typing import Callable, Dict


class BaseAwsCollector:
    def get_paginated_results(
        self,
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
