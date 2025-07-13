"""This module defines the vehicle snapshot class."""

from gi.repository import GObject
from sbaid.common.vehicle_type import VehicleType


class VehicleSnapshot(GObject.GObject):
    """ This class represents a vehicle snapshot.
    Attributes:
        vehicle_type (VehicleType): The type of the vehicle the snapshot represents.
        speed (float): Speed of the vehicle.
        lane_snapshot_id (str): The unique identifier of the lane the vehicle snapshot belongs to.
    """

    # GObject.Property definitions
    vehicle_type = GObject.Property(
        type=VehicleType,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    speed = GObject.Property(
        type=float,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    lane_snapshot_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, lane_snapshot_id: str, vehicle_type: VehicleType, speed: float) -> None:
        """Initialize the vehicle snapshot class."""
        super().__init__(vehicle_type=vehicle_type,
                         speed=speed,
                         lane_snapshot_id=lane_snapshot_id)
