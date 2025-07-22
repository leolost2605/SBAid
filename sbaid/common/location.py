"""This module contains the Location class."""
from gi.repository import GObject


class Location(GObject.GObject):
    """Represents a location, consisting of a pair of cartesian coordinates."""
    x = GObject.Property(
        type=float,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    y = GObject.Property(
        type=float,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, x: float, y: float) -> None:
        """Creates a new Location object."""
        super().__init__(x=x, y=y)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Location) and self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Location({self.x}, {self.y})"
