from collections import namedtuple

Resource = namedtuple("Resource", ["name", "resource_type", "id", "image"])
Link = namedtuple("Link", ["source", "destination", "link_type"])
