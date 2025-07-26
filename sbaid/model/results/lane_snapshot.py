"""This module defines the lane snapshot class."""


from gi.repository import Gio, GObject
from sbaid.common.a_display import ADisplay
from sbaid.model.results.vehicle_snapshot import VehicleSnapshot


class LaneSnapshot(GObject.GObject):
    """ This class represents a lane snapshot, which contains data collected from a specific
     traffic lane at a specific time in the simulation.
     Attributes:
         cross_section_snapshot_id (str): The unique identifier of the cross section snapshot
         this lane snapshot belongs to.
         id (str): The unique identifier of this lane snapshot.
         lane (int): The lane this snapshot represents.
         average_speed (float): The average speed of the vehicles in the lane snapshot.
         traffic_volume (int): The amount of vehicles that pass through the lane per hour.
         a_display (ADisplay): The display the snapshot's lane is showing
            at the time of the snapshot.
         vehicle_snapshots (ListModel<VehicleSnapshots>): A ListModel of the
            lane's vehicle snapshots.
    """

    # GObject.Property definitions

    cross_section_snapshot_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    lane = GObject.Property(
        type=int,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    average_speed = GObject.Property(
        type=float,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    traffic_volume = GObject.Property(
        type=int,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    a_display = GObject.Property(
        type=ADisplay,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY,
        default=ADisplay.OFF)
    vehicle_snapshots = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, cross_section_snapshot_id: str, lane_snapshot_id: str, lane: int,
                 average_speed: float, traffic_volume: int, a_display: ADisplay) -> None:
        """ Initialize the lane snapshot object."""
        super().__init__(cross_section_snapshot_id=cross_section_snapshot_id,
                         id=lane_snapshot_id,
                         lane=lane,
                         average_speed=average_speed,
                         traffic_volume=traffic_volume,
                         a_display=a_display,
                         vehicle_snapshots=Gio.ListStore.new(VehicleSnapshot))

    def load_from_db(self) -> None:
        """todo"""

    def add_vehicle_snapshot(self, snapshot: VehicleSnapshot) -> None:
        """Adds a vehicle snapshot to the list in this lane snapshot."""
        self.vehicle_snapshots.append(snapshot)  # pylint:disable=no-member
