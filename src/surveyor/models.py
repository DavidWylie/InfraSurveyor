from collections import namedtuple

Resource = namedtuple("Resource", ["name", "type", "invoked_by", "sends_to", "container"])
Container = namedtuple("Container", ["name", "type"])
