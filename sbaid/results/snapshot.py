""" This module represents the Snapshot class."""

from xmlrpc.client import DateTime
from gi.repository import Gio, GObject
from sbaid.results.cross_section_snapshot import CrossSectionSnapshot


class Snapshot:
    """ This class represents a snapshot, containing cross section snapshots
            with the same timestamp.
    Attributes:
        snapshot_id (str): The unique identifier of the snapshot.
        capture_timestamp (DateTime): The timestamp of the snapshot capture.
        cross_section_snapshots (ListModel<CrossSectionSnapshot>): The list of cross section
         snapshots the snapshot consists of.
    """

    #GObject.Property definitions
    snapshot_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    capture_timestamp = GObject.Property(
        type=DateTime,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    cross_section_snapshots = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, snapshot_id: str, capture_timestamp: DateTime) -> None:
        """Initialize the Snapshot class."""
        self.snapshot_id = snapshot_id
        self.capture_timestamp = capture_timestamp

    def load_from_db(self) -> None:
        """todo"""

    def add_cross_section_snapshot(self, snapshot: CrossSectionSnapshot) -> None:
        """todo"""
