"""This module defines the VehicleType enum."""
from gi.repository import GObject


class VehicleType(GObject.GEnum):
    """This enum represents the different types of vehicles."""
    CAR = 0
    LORRY = 1
