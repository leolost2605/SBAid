"""This module defines the ADisplay enum."""
from gi.repository import GObject


class ADisplay(GObject.GEnum):
    """This enum represents the different types of A Display signals."""
    OFF = 0
    SPEED_LIMIT_60 = 1
    SPEED_LIMIT_80 = 2
    SPEED_LIMIT_100 = 3
    SPEED_LIMIT_110 = 4
    SPEED_LIMIT_120 = 5
    SPEED_LIMIT_130 = 6
    SPEED_LIMIT_LIFTED = 7
    CLOSED_LANE = 8

def get_by_number(key):
    match key:
        case '0': return ADisplay.OFF
        case '1': return ADisplay.SPEED_LIMIT_60
        case '2': return ADisplay.SPEED_LIMIT_80
        case '3': return ADisplay.SPEED_LIMIT_100
        case '4': return ADisplay.SPEED_LIMIT_110
        case '5': return ADisplay.SPEED_LIMIT_120
        case '6': return ADisplay.SPEED_LIMIT_130
        case '7': return ADisplay.SPEED_LIMIT_LIFTED
        case '8': return ADisplay.CLOSED_LANE
    return None
