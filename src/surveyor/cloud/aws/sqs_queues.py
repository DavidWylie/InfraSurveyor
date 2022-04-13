import boto3

def get_queues(region):
    client = boto3.resource("sqs", region_name=region)

