from gi.repository import GLib, GObject
from sbaid.common.a_display import ADisplay
from sbaid.results.vehicle_snapshot import VehicleSnapshot

"""This module defines the lane snapshot class."""

class LaneSnapshot:
    """ This class represents a lane snapshot, which contains data collected from a specific
     traffic lane at a specific time in the simulation.
     Attributes:
         cross_section_snapshot_id (str): The unique identifier of the cross section snapshot
         this lane snapshot belongs to.
         lane_snapshot_id (str): The unique identifier of this lane snapshot.
         lane (int): The lane this snapshot represents.
         average_speed (float): The average speed of the vehicles in the lane snapshot.
         traffic_volume (int): The amount of vehicles that pass through the lane per hour.
         a_display (ADisplay): The display the snapshot's lane is showing at the time of the snapshot.
         vehicle_snapshots (ListModel<VehicleSnapshots>): A ListModel of the lane's vehicle snapshots.
    """

    #GObject.Property definitions

    cross_section_snapshot_id = GObject.Property(type=str, default = "")
    lane_snapshot_id = GObject.Property(type=str, default = "")
    lane = GObject.Property(type=int, default = None)
    average_speed = GObject.Property(type=float, default=None)
    traffic_volume = GObject.Property(type=int, default=None)
    a_display = GObject.Property(type=ADisplay, default=None)
    vehicle_snapshots = GObject.Property(type=GLib.ListModel, default=None)

    def __init__(self, cross_section_snapshot_id: str, lane_snapshot_id: str, lane: int,
                 average_speed: float, traffic_volume: int, a_display: ADisplay) -> None:
        """ Initialize the lane snapshot object."""
        self.cross_section_snapshot_id = cross_section_snapshot_id
        self.lane_snapshot_id = lane_snapshot_id
        self.lane = lane
        self.average_speed = average_speed
        self.traffic_volume = traffic_volume
        self.a_display = a_display

    def load_from_db(self) -> None:
        """todo"""
        pass

    def add_vehicle_snapshot(self, snapshot: VehicleSnapshot) -> None:
        """todo"""
        pass
