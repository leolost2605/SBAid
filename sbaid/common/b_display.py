"""This module defines the BDisplay enum."""
from enum import Enum

class BDisplay(Enum):
    """This enum represents the different types of B Display signals."""
    OFF = 0
    TRAFFIC_JAM = 1
    CONSTRUCTION = 2
    CAUTION_ACCIDENT = 3
    CAUTION_FOG = 4
    SNOW = 5
    SLIPPERY_ROAD = 6
