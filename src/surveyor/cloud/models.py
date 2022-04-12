from collections import namedtuple
from dataclasses import dataclass

Link = namedtuple("Link", ["source", "destination", "link_type"])


@dataclass()
class Resource:
    name: str
    resource_type: str
    service: str
    category: str
    id: str
    image: str = None
