"""This module defines the CrossSectionType enum
which represents the differnet types of cross sections."""
from enum import Enum


class CrossSectionType(Enum):
    """This enum represents the different types of cross sections."""
    DISPLAY = 0
    MEASURING = 1
    COMBINED = 2
