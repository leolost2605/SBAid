from gi.repository import GLib, GObject
from xmlrpc.client import DateTime
from sbaid.results.cross_section_snapshot import CrossSectionSnapshot

""" This module represents the Snapshot class."""

class Snapshot:
    """ This class represents a snapshot, containing cross section snapshots with the same timestamp.
    Attributes:
        snapshot_id (str): The unique identifier of the snapshot.
        capture_timestamp (DateTime): The timestamp of the snapshot capture.
        cross_section_snapshots (ListModel<CrossSectionSnapshot>): The list of cross section snapshots
            the snapshot consists of.
    """

    #GObject.Property definitions
    snapshot_id = GObject.Property(type=str)
    capture_timestamp = GObject.Property(type=DateTime)
    cross_section_snapshots = GObject.Property(type=GLib.ListModel)

    def __init__(self, snapshot_id: str, capture_timestamp: DateTime) -> None:
        """Initialize the Snapshot class."""
        self.snapshot_id = snapshot_id
        self.capture_timestamp = capture_timestamp

    def load_from_db(self) -> None:
        """todo"""
        pass

    def add_cross_section_snapshot(self, snapshot: CrossSectionSnapshot) -> None:
        """todo"""
        pass
