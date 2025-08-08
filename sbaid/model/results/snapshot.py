""" This module represents the Snapshot class."""

from gi.repository import Gio, GLib, GObject
from sbaid.model.database.global_database import GlobalDatabase
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot


class Snapshot(GObject.GObject):
    """ This class represents a snapshot, containing cross section snapshots
            with the same timestamp.
    Attributes:
        id (str): The unique identifier of the snapshot.
        capture_timestamp (DateTime): The timestamp of the snapshot capture.
        cross_section_snapshots (ListModel<CrossSectionSnapshot>): The list of cross section
         snapshots the snapshot consists of.
    """

    # GObject.Property definitions
    id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    capture_timestamp = GObject.Property(
        type=GLib.DateTime,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    cross_section_snapshots: Gio.ListModel = GObject.Property(
        type=Gio.ListModel)  # type: ignore[assignment]

    @cross_section_snapshots.getter  # type: ignore
    def cross_section_snapshots(self) -> Gio.ListModel:
        """Getter for the cross section snapshots."""
        return self.__cross_section_snapshots

    __global_database: GlobalDatabase
    __cross_section_snapshots: Gio.ListStore

    def __init__(self, snapshot_id: str, capture_timestamp: GLib.DateTime,
                 global_db: GlobalDatabase) -> None:
        """Initialize the Snapshot class."""
        super().__init__(id=snapshot_id,
                         capture_timestamp=capture_timestamp)

        self.__cross_section_snapshots = Gio.ListStore.new(CrossSectionSnapshot)
        self.__global_database = global_db

    async def load_from_db(self) -> None:
        """Loads the snapshot with the cross-section snapshots."""
        cross_section_ids = await self.__global_database.get_all_cross_section_snapshots(self.id)
        for cross_section in cross_section_ids:
            cross_section_snapshot = (CrossSectionSnapshot
                                      (cross_section[1], cross_section[0], cross_section[2],
                                       cross_section[3], cross_section[4], self.__global_database))
            await cross_section_snapshot.load_from_db()
            self.add_cross_section_snapshot(cross_section_snapshot)

    def add_cross_section_snapshot(self, snapshot: CrossSectionSnapshot) -> None:
        """This method adds a cross-section snapshot to the existing list."""
        self.__cross_section_snapshots.append(snapshot)
