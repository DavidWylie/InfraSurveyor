import unittest
from surveyor.cloud  import aws
from surveyor.cloud.models import Resource, Link
from moto import mock_lambda, mock_sqs
from helpers import MotoLambdaHelper, MotoSqsHelper
import boto3


class TestAWSSurveyLambda(unittest.TestCase):

    def _get_expected_nodes(self):
        nodes = [
            Resource(
                name="First",
                id="arn:aws:lambda:eu-west-2:123456789012:function:First",
                resource_type="Lambda-Function",
                service="AWS-Lambda",
                category="COMPUTE",
            ),
            Resource(
                name="Second",
                id="arn:aws:lambda:eu-west-2:123456789012:function:Second",
                resource_type="Lambda-Function",
                service="AWS-Lambda",
                category="COMPUTE",
            ),
        ]
        return nodes

    @mock_lambda
    def test_get_lambdas_no_lambdas(self):
        """ Test Get lambda function where no lambdas exist in the account"""
        nodes = []
        links = []

        expected_nodes = []
        expected_links = []
        aws.get_lambdas(nodes, links)
        self.assertEqual(expected_nodes, nodes)
        self.assertEqual(expected_links, links)

    @mock_lambda
    def test_get_lambdas_no_links(self):
        """ Test Get lambda function where lambdas exist in the account but do not have event or destination config"""
        nodes = []
        links = []
        helper = MotoLambdaHelper()
        helper.create_fake_lambda("First")
        helper.create_fake_lambda("Second")
        expected_nodes = self._get_expected_nodes()
        expected_links = []
        aws.get_lambdas(nodes, links)
        self.assertEqual(expected_nodes, nodes)
        self.assertEqual(expected_links, links)

    @mock_lambda
    @mock_sqs
    def test_get_lambdas_sqs_invoke(self):
        """ Test Get lambda function where lambdas exist in the account but do not have event or destination config"""
        nodes = []
        links = []
        helper = MotoLambdaHelper()
        function_arn = helper.create_fake_lambda("First")
        sqs_helper = MotoSqsHelper()
        sqs_arn = sqs_helper.create_queue("First_queue")
        helper.create_event_source(sqs_arn, function_arn)

        expected_nodes = [Resource(
            name="First",
            id="arn:aws:lambda:eu-west-2:123456789012:function:First",
            resource_type="Lambda-Function",
            service="AWS-Lambda",
            category="COMPUTE",
        )]
        expected_links = [
            Link(
                source=sqs_arn,
                destination=function_arn,
                link_type=""
            )
        ]
        aws.get_lambdas(nodes, links)
        self.assertEqual(expected_nodes, nodes)
        self.assertEqual(expected_links, links)


if __name__ == '__main__':
    unittest.main()
