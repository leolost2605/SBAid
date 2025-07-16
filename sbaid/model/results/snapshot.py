""" This module represents the Snapshot class."""

from gi.repository import Gio, GLib, GObject
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

    cross_section_snapshots = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, snapshot_id: str, capture_timestamp: GLib.DateTime) -> None:
        """Initialize the Snapshot class."""
        super().__init__(id=snapshot_id,
                         capture_timestamp=capture_timestamp,
                         cross_section_snapshots=Gio.ListStore.new(CrossSectionSnapshot))

    def load_from_db(self) -> None:
        """todo"""

    def add_cross_section_snapshot(self, snapshot: CrossSectionSnapshot) -> None:
        """This method adds a cross section snapshot."""
        self.cross_section_snapshots.append(snapshot)
