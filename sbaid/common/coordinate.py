"""TODO"""
from gi.repository import GObject


class Coordinate(GObject.GObject):
    """TODO"""
    x = GObject.Property(
        type=float,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    y = GObject.Property(
        type=float,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, x: float, y: float) -> None:
        """TODO"""
        super().__init__(x=x, y=y)
