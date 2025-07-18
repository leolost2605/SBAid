"""This module defines the BDisplay enum."""
from gi.repository import GObject


class BDisplay(GObject.GEnum):
    """This enum represents the different types of B Display signals."""
    OFF = 0
    TRAFFIC_JAM = 1
    CONSTRUCTION = 2
    CAUTION_ACCIDENT = 3
    CAUTION_FOG = 4
    SNOW = 5
    SLIPPERY_ROAD = 6

def get_by_number(key):
    match key:
        case '0': return BDisplay.OFF
        case '1': return BDisplay.TRAFFIC_JAM
        case '2': return BDisplay.CONSTRUCTION
        case '3': return BDisplay.CAUTION_ACCIDENT
        case '4': return BDisplay.CAUTION_FOG
        case '5': return BDisplay.SNOW
        case '6': return BDisplay.SLIPPERY_ROAD
    return None
