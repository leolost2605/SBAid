"""TODO"""
from typing import List

from gi.repository import GObject
from gi.repository import Gio

from sbaid.common.location import Location


class Route:
    """TODO"""
    points = GObject.Property(type=Gio.ListModel,
                              flags=GObject.ParamFlags.READABLE |
                              GObject.ParamFlags.WRITABLE |
                              GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, coordinates: List[Location]) -> None:
        # TODO: turn list into listmodel
        """TODO"""
