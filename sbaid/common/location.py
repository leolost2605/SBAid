"""This module contains the Location class."""
import math
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

    def distance(self, location: 'Location') -> float:
        """Calculates the distance in meters between this location and another given location,
         using the Haversine formula."""
        r = 6371000  # radius of the earth in meter

        lat1_rad = math.radians(self.x)
        lon1_rad = math.radians(self.y)
        lat2_rad = math.radians(location.x)
        lon2_rad = math.radians(location.y)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat/2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        distance = r * c
        return distance

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Location) and self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Location({self.x}, {self.y})"
