"""This module defines the CrossSectionType enum,
which represents the different types of cross sections."""
from gi.repository import GObject


class CrossSectionType(GObject.GEnum):
    """This enum represents the different types of cross sections."""
    DISPLAY = 0
    MEASURING = 1
    COMBINED = 2
