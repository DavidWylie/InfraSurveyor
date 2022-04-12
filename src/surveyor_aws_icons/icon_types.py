from dataclasses import dataclass
from enum import Enum


@dataclass()
class CategoryData:
    name: str
    color: str


class Category(Enum):
    ANALYTICS = CategoryData("Analytics", "#9865F8")
    APPLICATION_INTEGRATION = CategoryData("Application-Integration", "#FF4F8B")
    AR_VR = CategoryData("AR-VR", "#FF4F8B")
    COMPUTE = CategoryData("Compute", "##FF9900")


@dataclass
class Resource:
    category: Category
    service: str
    resource_type: str
