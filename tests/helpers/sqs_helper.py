import boto3

class MotoSqsHelper:
    def __init__(self):
        self.sqs_client = boto3.resource("sqs", region_name="eu-west-2")

    def create_queue(self, queue_name):
        queue = self.sqs_client.create_queue(QueueName=queue_name)
        return queue.attributes["QueueArn"]