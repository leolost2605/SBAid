"""This module contains the VehicleInfo class."""
from typing import Any

from gi.repository import GObject
from sbaid.common.vehicle_type import VehicleType


class VehicleInfo(GObject.GObject):
    """This class represents information about a single vehicle."""
    vehicle_type = GObject.Property(
        type=VehicleType,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY,
        default=VehicleType.CAR)
    speed = GObject.Property(
        type=float,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, vehicle_type: VehicleType, speed: float) -> None:
        """Construct a new VehicleInfo."""
        super().__init__(vehicle_type=vehicle_type, speed=speed)

    def __eq__(self, other: Any) -> bool:
        """Override."""
        return (isinstance(other, VehicleInfo) and other.speed == self.speed
                and other.vehicle_type == self.vehicle_type)

    def __hash__(self) -> int:
        """Override."""
        return hash((self.vehicle_type, self.speed))
