"""TODO"""
from typing import List

from gi.repository import GObject
from gi.repository import Gio

from sbaid.common.coordinate import Coordinate


class Route(GObject.GObject):
    """TODO"""
    points = GObject.Property(type=Gio.ListModel,
                              flags=GObject.ParamFlags.READABLE |
                              GObject.ParamFlags.WRITABLE |
                              GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, coordinates: List[Coordinate]) -> None:
        super().__init__()
        # TODO: turn list into listmodel
