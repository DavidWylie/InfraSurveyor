import boto3


class MotoEventsHelper:
    def __init__(self):
        self.client = boto3.client("events", region_name="eu-west-2")

    def create_rule(self, name, schedule, event_pattern):
        result = self.client.put_rule(
            Name=name,
            ScheduleExpression=schedule,
            EventPattern=event_pattern,
        )

        return result["RuleArn"]

    def add_target_to_rule(self, rule_name, targets):
        self.client.put_targets(Rule=rule_name, Targets=targets)
