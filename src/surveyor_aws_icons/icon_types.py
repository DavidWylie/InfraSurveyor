from dataclasses import dataclass
from enum import Enum


class Category(Enum):
    ANALYTICS = "Analytics"
    APPLICATION_INTEGRATION = "Application-Integration"


@dataclass
class Resource:
    category: Category
    service: str
    type: str
