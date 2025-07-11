from gi.repository import GObject
from sbaid.common.vehicle_type import VehicleType

"""This module defines the vehicle snapshot class."""

class VehicleSnapshot:
    """ This class represents a vehicle snapshot.
    Attributes:
        vehicle_type (VehicleType): The type of the vehicle the snapshot represents.
        speed (float): Speed of the vehicle.
        lane_snapshot_id (str): The unique identifier of the lane the vehicle snapshot belongs to.
    """

    #GObject.Property definitions
    vehicle_type = GObject.Property(type=VehicleType)
    speed = GObject.Property(type=float)
    lane_snapshot_id = GObject.Property(type=str)


    def __init__(self,lane_snapshot_id: str, vehicle_type: VehicleType, speed: float) -> None:
        """Initialize the vehicle snapshot class."""
        self.vehicle_type = vehicle_type
        self.speed = speed
        self.lane_snapshot_id = lane_snapshot_id


