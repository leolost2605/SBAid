"""This module contains the Coordinate class."""
from gi.repository import GObject


class Coordinate(GObject.GObject):
    """Represents a two-dimensional cartesian coordinate."""
    x = GObject.Property(
        type=float,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    y = GObject.Property(
        type=float,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, x: float, y: float) -> None:
        """Creates a new Coordinate object."""
        super().__init__(x=x, y=y)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Coordinate) and self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Coordinate({self.x}, {self.y})"
