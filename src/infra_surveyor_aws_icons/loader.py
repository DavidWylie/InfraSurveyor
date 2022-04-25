from pathlib import Path
from .icon_sets import ResourceIconSet, CategoryIconSet, ServiceIconSet
from .image_format import ImageFormat
from ._version import version
from .icon_types import Resource, Category


def _get_resource_dir():
    return Path(__file__).parent.resolve()


class IconLoader:
    def __init__(self):
        self.image_format = ImageFormat.SVG
        self.resource_icon_set = ResourceIconSet.LIGHT
        self.category_icon_set = CategoryIconSet.ARCH_48
        self.service_icon_set = ServiceIconSet.ARCH_48

    def get_resource_icon(self, resource: Resource) -> Path:
        return Path(
            _get_resource_dir(),
            f"Resource-Icons_{version}",
            f"Res_{resource.category.value.name}",
            f"Res_{self.resource_icon_set.value}",
            f"Res_{resource.service}_{resource.resource_type}_{self.resource_icon_set.value}.{self.image_format.value}",
        )

    def get_category_icon(self, category: Category) -> Path:
        return Path(
            _get_resource_dir(),
            f"Category-Icons_{version}",
            f"Arch-Category_{self.category_icon_set.value}",
            f"Arch-Category_{category.value.name}_{self.category_icon_set.value}.{self.image_format.value}",
        )

    def get_service_icon(self, category: Category, service) -> Path:
        return Path(
            _get_resource_dir(),
            f"Architecture-Service-Icons_{version}",
            f"Arch_{category.value.name}",
            f"Arch_{self.service_icon_set.value}",
            f"Arch_{service}_{self.service_icon_set.value}.{self.image_format.value}",
        )
