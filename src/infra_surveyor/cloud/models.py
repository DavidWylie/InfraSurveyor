from collections import namedtuple
import dataclasses, json

Link = namedtuple("Link", ["source", "destination", "link_type"])

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

@dataclasses.dataclass()
class Resource:
    name: str
    resource_type: str
    service: str
    category: str
    id: str
    image: str = None
