"""This module contains the route class."""

from gi.repository import GObject
from gi.repository import Gio

class Route(GObject.GObject):
    """This class represents a route on a motorway. It consists of coordinates and links between them."""
    points = GObject.Property(type=Gio.ListModel,
                              flags=GObject.ParamFlags.READABLE |
                              GObject.ParamFlags.WRITABLE |
                              GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, points: Gio.ListModel) -> None:
        self.points = points
        super().__init__()
