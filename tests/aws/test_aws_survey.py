from unittest import TestCase
from unittest.mock import patch, Mock
from infra_surveyor.cloud import aws
from infra_surveyor.cloud.models import Resource, Link


class MockService:
    def get(self, nodes, links, region):
        nodes.append(
            Resource(
                id="exampleId",
                resource_type="exampleType",
                service="exampleservice",
                category="exampleCategory",
                name="exampleName",
            )
        )
        links.append(
            Link(
                source="exampleSource",
                destination="exampleDestination",
                link_type="exampleLink",
            )
        )
        links.append(
            Link(
                source="exampleSource2",
                destination="exampleDestination2",
                link_type="exampleLink2",
            )
        )


class TestAWSSurvey(TestCase):
    def test_survey_services_called(self):
        aws.services = [
            MockService(),
            MockService(),
            MockService(),
            MockService(),
        ]

        nodes, links = aws.survey_events()
        self.assertEqual(4, len(nodes))
        self.assertEqual(8, len(links))
