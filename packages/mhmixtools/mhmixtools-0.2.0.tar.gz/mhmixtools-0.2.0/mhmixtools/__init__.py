from . import decorators, folder_structure_generator, image_utils, template_sync

__version__ = "0.2.0"
__all__ = [
    "decorators",
    "folder_structure_generator",
    "image_utils",
    "template_sync"
]
from .decorators import *
from .folder_structure_generator import *
from .image_utils import *
from .template_sync import *
from . import __version__
__author__ = "Md. Mahmud Hasan"
__email__ = "mahadymahamudh472@gmail.com"
__license__ = "MIT"
__description__ = "This package contains various automation tools for Python developers."
