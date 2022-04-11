import click
from .commands import aws


@click.group()
def cli():
    """Surveyor is a tool for generating diagrams from existing cloud infrastructure"""
    pass


@cli.group(name="survey-aws")
def survey_aws():
    """Create Node Graphs of AWS Infrastructure"""
    pass


@survey_aws.command(name="events")
def survey_aws_events():
    """Survey the AWS Events flow"""
    aws.survey_events()
