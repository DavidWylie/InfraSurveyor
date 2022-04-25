from .icon_sets import CategoryIconSet, ServiceIconSet, ResourceIconSet
from .icon_types import Resource, Category
from .image_format import ImageFormat
from .loader import IconLoader
from ._version import version


__version__ = version
__all__ = [Resource, IconLoader, Category]
