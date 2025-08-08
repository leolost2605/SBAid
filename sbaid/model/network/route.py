"""This module contains the route class."""

from gi.repository import GObject
from gi.repository import Gio


class Route(GObject.GObject):
    """This class represents a route on a motorway, consisting of a series of coordinates."""
    points: Gio.ListModel = GObject.Property(type=Gio.ListModel,  # type: ignore
                                             flags=GObject.ParamFlags.READABLE |
                                             GObject.ParamFlags.WRITABLE |
                                             GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, points: Gio.ListModel) -> None:
        super().__init__(points=points)
