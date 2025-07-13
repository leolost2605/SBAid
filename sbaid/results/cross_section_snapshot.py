"""This module defines the cross section snapshot class."""

from gi.repository import Gio, GObject
from sbaid.common.b_display import BDisplay
from sbaid.results.lane_snapshot import LaneSnapshot


class CrossSectionSnapshot(GObject.GObject):
    """This class defines the cross section snapshot class.
    Attributes:
        snapshot_id (str): The unique identifier of the snapshot this
            cross section snapshot belongs to.
        cross_section_snapshot_id (str): The unique identifier of the
            cross section the snapshot represents.
        cross_section_name (str): The name of the cross section the snapshot represents.
        b_display (BDisplay): The B display of the cross section this snapshot represents.
        lane_snapshots (ListModel<LaneSnapshot>): The lane snapshots this
            cross section snapshot consists of.
    """

    # GObject Property definitions
    snapshot_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    cross_section_snapshot_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    cross_section_name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    b_display = GObject.Property(
        type=BDisplay,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    lane_snapshots = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, snapshot_id: str, cross_section_snapshot_id: str, cross_section_name: str,
                 b_display: BDisplay) -> None:
        """todo"""
        super().__init__(snapshot_id=snapshot_id,
                         cross_section_snapshot_id=cross_section_snapshot_id,
                         cross_section_name=cross_section_name,
                         b_display=b_display)

    def load_from_db(self) -> None:
        """todo"""

    def add_lane_snapshots(self, snapshot: LaneSnapshot) -> None:
        """todo"""
