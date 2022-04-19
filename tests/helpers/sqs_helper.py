import boto3


class MotoSqsHelper:
    def __init__(self):
        self.sqs_client = boto3.resource("sqs", region_name="eu-west-2")

    def create_queue(self, queue_name):
        queue = self.sqs_client.create_queue(QueueName=queue_name)
        return queue.attributes["QueueArn"]

    def create_queue_with_dlq(self, queue_name, dlq_arn):
        queue = self.sqs_client.create_queue(
            QueueName=queue_name,
            Attributes={
                "DelaySeconds": "900",
                "MaximumMessageSize": "262144",
                "MessageRetentionPeriod": "1209600",
                "ReceiveMessageWaitTimeSeconds": "20",
                "RedrivePolicy": f'{{"deadLetterTargetArn": "{dlq_arn}", "maxReceiveCount": 100}}',
                "VisibilityTimeout": "43200",
            },
        )
        return queue.attributes["QueueArn"]
