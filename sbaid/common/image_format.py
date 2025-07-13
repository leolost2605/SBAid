"""This module defines the ImageFormat enum,
which represents the different types of image formats that are available."""
from gi.repository import GObject


class ImageFormat(GObject.GEnum):
    """This enum represents the different types of image formats."""
    PNG = 0
    SVG = 1
