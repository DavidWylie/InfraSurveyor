import boto3


class MotoSnsHelper:
    def __init__(self):
        self.sns_client = boto3.client("sns", region_name="eu-west-2")

    def create_topic(self, topic_name):
        result = self.sns_client.create_topic(Name=topic_name)
        return result["TopicArn"]

    def create_subscription_to_queue(self, topic_arn, queue_arn):
        self.sns_client.subscribe(
            TopicArn=topic_arn, Protocol="sqs", Endpoint=queue_arn
        )
