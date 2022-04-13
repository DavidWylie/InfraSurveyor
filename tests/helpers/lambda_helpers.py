import boto3
import zipfile
import io
from botocore.exceptions import ClientError
from moto import mock_iam


class MotoLambdaHelper:
    def __init__(self):
        self.lambda_client = boto3.client("lambda", region_name="eu-west-2")

    def get_test_zip_file1(self):
        pfunc = """
def lambda_handler(event, context):
    print("custom log event")
    return event
"""
        return self._process_lambda(pfunc)

    def create_fake_lambda(self, function_name):
        zip_content = self.get_test_zip_file1()
        result = self.lambda_client.create_function(
            FunctionName=function_name,
            Runtime="python2.7",
            Role=self.get_role_name(),
            Handler="lambda_function.lambda_handler",
            Code={"ZipFile": zip_content},
            Description="test lambda function",
            Timeout=3,
            MemorySize=128,
            Publish=True,
        )
        return result["FunctionArn"]

    def get_role_name(self):
        with mock_iam():
            iam = boto3.client("iam", region_name="eu-west-2")
            try:
                return iam.get_role(RoleName="my-role")["Role"]["Arn"]
            except ClientError:
                return iam.create_role(
                    RoleName="my-role",
                    AssumeRolePolicyDocument="some policy",
                    Path="/my-path/",
                )["Role"]["Arn"]

    def _process_lambda(self, func_str):
        zip_output = io.BytesIO()
        zip_file = zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED)
        zip_file.writestr("lambda_function.py", func_str)
        zip_file.close()
        zip_output.seek(0)
        return zip_output.read()

    def create_event_source(self, source_arn, function_name):
        response = self.lambda_client.create_event_source_mapping(
            EventSourceArn=source_arn, FunctionName=function_name
        )
