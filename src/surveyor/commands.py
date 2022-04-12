import click
from . import cloud, icons, graphing


@click.group()
def cli():
    """Surveyor is a tool for generating diagrams from existing cloud infrastructure"""
    pass


@cli.group(name="survey-aws")
def survey_aws():
    """Create Node Graphs of AWS Infrastructure"""
    pass


@survey_aws.command(name="events")
@click.option("-o", "--out_dir", default=".")
@click.option("-f", "--out_file", default="aws-events")
@click.option("--out_ext", default="png")
def survey_aws_events(out_dir, out_file, out_ext):
    """Survey the AWS Events flow - Creates a Dot graph and an Image"""
    nodes, links = cloud.aws.survey_events()
    icons.load_icons(nodes)
    graph = graphing.create_graph(nodes, links)
    graph.render_graph(out_file, out_dir, out_ext)
