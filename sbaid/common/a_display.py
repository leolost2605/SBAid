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
