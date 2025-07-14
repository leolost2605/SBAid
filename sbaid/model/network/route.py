"""TODO"""
from gi.repository import GObject
from gi.repository import Gio


class Route:
    """TODO"""
    points = GObject.Property(type=Gio.ListModel,
                              flags=GObject.ParamFlags.READABLE |
                              GObject.ParamFlags.WRITABLE |
                              GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self):
        """TODO"""
