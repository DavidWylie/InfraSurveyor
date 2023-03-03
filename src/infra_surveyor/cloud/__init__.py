from . import aws, models
import json, logging

__all__ = [aws, models]


def write_survey(file_name, nodes, links):
    with open(file_name, mode="w+") as f:
        survey = {"nodes": nodes, "links": links}
        f.write(json.dumps(survey, cls=models.EnhancedJSONEncoder, indent=3))
    logging.info(f"Written Survey to {file_name}.json")
