import logging

from infra_surveyor.cloud.aws.boto_utilities import parse_arn
from infra_surveyor.cloud.models import Link, Resource


class AutoScalingParser:
    def add_static_service_if_required(self, nodes, links):
        arns = self.get_linked_arns(links)
        for arn in arns:
            if not self.has_node(arn, nodes):
                nodes.append(self.create_service_node(arn))

    def has_node(self, arn, nodes: list[Resource]):
        for node in nodes:
            if node.id == arn:
                return True
        return False

    def get_linked_arns(self, links: list[Link]) -> list[str]:
        arns = []
        for link in links:
            if "arn:aws:autoscaling:" in link.destination:
                arns.append(link.destination)
        return arns

    def create_service_node(self, arn):
        parsed_arn = parse_arn(arn)
        return Resource(
            name=f"Auto Scaling {parsed_arn.region}",
            resource_type="",
            id=arn,
            service="Amazon-EC2-Auto-Scaling",
            category="COMPUTE",
            node_type="service",
        )


def create_linked_services(nodes, links):
    parser = AutoScalingParser()
    parser.add_static_service_if_required(nodes, links)
    logging.info("Auto Scaling Services Complete")
