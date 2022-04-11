from pathlib import Path
from .icon_sets import ResourceIconSet, CategoryIconSet, ServiceIconSet
from .image_format import ImageFormat
from ._version import version
from .icon_types import Resource, Category


def _get_resource_dir():
    return Path(__file__).parent.resolve()


def get_resource_icon(resource: Resource, icon_set: ResourceIconSet = ResourceIconSet.LIGHT, image_format: ImageFormat = ImageFormat.SVG) -> Path:
    return Path(
        _get_resource_dir(),
        f"Resource-Icons_{version}",
        f"Res_{resource.category.value.name}",
        f"Res_{icon_set.value}",
        f"Res_{resource.service}_{resource.resource_type}_{icon_set.value}.{image_format.value}"
    )


def get_category_icon(category: Category, icon_set: CategoryIconSet, image_format: ImageFormat) -> Path:
    return Path(
        _get_resource_dir(),
        f"Category-Icons_{version}",
        f"Arch-Category_{icon_set.value}",
        f"Arch-Category_{category.value.name}_{icon_set.value}.{image_format.value}"
    )


def get_service_icon(category: Category, service, icon_set: ServiceIconSet, image_format: ImageFormat) -> Path:
    return Path(
        _get_resource_dir(),
        f"Architecture-Service-Icons_{version}",
        f"Arch_{category.value.name}",
        f"Arch_{icon_set.value}",
        f"Arch_{service}_{icon_set.value}.{image_format.value}"
    )
