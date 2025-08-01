"""This module defines the CrossSectionSnapshot class."""
from gi.repository import Gio, GObject
from sbaid.common.b_display import BDisplay
from sbaid.model.database.global_database import GlobalDatabase
from sbaid.model.results.lane_snapshot import LaneSnapshot


class CrossSectionSnapshot(GObject.GObject):
    """This class defines the cross section snapshot class.
    Attributes:
        snapshot_id (str): The unique identifier of the snapshot this
            cross section snapshot belongs to.
        cs_snapshot_id (str): The unique identifier of the
            cross section the snapshot represents.
        cross_section_name (str): The name of the cross section the snapshot represents.
        b_display (BDisplay): The B display of the cross section this snapshot represents.
        __lane_snapshots (ListModel<LaneSnapshot>): The lane snapshots this
            cross section snapshot consists of.
    """

    # GObject Property definitions
    snapshot_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    cs_snapshot_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    cross_section_name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    cross_section_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)
    b_display = GObject.Property(
        type=BDisplay,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY,
        default=BDisplay.OFF)

    __lane_snapshots: Gio.ListStore
    __global_db: GlobalDatabase

    @GObject.Property(type=LaneSnapshot)
    def lane_snapshots(self) -> Gio.ListModel:
        """Returns ListModel of available diagram types"""
        return self.__lane_snapshots

    def __init__(self, snapshot_id: str, cross_section_snapshot_id: str, cross_section_name: str,
                 cross_section_id: str, b_display: BDisplay, global_db: GlobalDatabase) -> None:
        """Initialize the cross-section snapshot class."""
        self.__lane_snapshots = Gio.ListStore.new(LaneSnapshot)
        self.__global_db = global_db
        super().__init__(snapshot_id=snapshot_id,
                         cs_snapshot_id=cross_section_snapshot_id,
                         cross_section_name=cross_section_name,
                         cross_section_id=cross_section_id,
                         b_display=b_display)

    async def load_from_db(self) -> None:
        """Loads Lane Snapshots from the database and adds them to this class"""
        lane_snapshot_data = await self.__global_db.get_all_lane_snapshots(
            self.cs_snapshot_id)
        for lane_snapshot in lane_snapshot_data:
            new_lane_snapshot = LaneSnapshot(self.cs_snapshot_id,
                                             lane_snapshot[0], lane_snapshot[1],
                                             lane_snapshot[2], lane_snapshot[3],
                                             lane_snapshot[4], self.__global_db)

            await new_lane_snapshot.load_from_db()
            self.__lane_snapshots.append(new_lane_snapshot)

    def add_lane_snapshot(self, snapshot: LaneSnapshot) -> None:
        """Add a LaneSnapshot to this CrossSectionSnapshot."""
        self.__lane_snapshots.append(snapshot)

    def calculate_cs_average_speed(self) -> float:
        """Calculate the average of the average speed value from
        all lanes in this cross-section snapshot. """
        speed_sum = 0
        for snapshot in self.__lane_snapshots:
            assert isinstance(snapshot, LaneSnapshot)  # todo delete this and figure it out
            speed_sum += snapshot.average_speed
        return speed_sum / len(self.lane_snapshots)
