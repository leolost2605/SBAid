"""This module contains the route class."""

from gi.repository import GObject
from gi.repository import Gio

from sbaid.common.location import Location


class Route(GObject.GObject):
    """This class represents a route on a motorway, consisting of a series of coordinates."""
    points = GObject.Property(type=Gio.ListModel,
                              flags=GObject.ParamFlags.READABLE |
                              GObject.ParamFlags.WRITABLE |
                              GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, points: list[Location]) -> None:

        points_lm = Gio.ListStore()
        for point in points:
            points_lm.append(point)
        super().__init__(points=points_lm)
