"""This module contains the CrossSectionState class."""
from gi.repository import GObject
from sbaid.common.cross_section_type import CrossSectionType


class CrossSectionState(GObject.GObject):
    """This class represents the state of a single cross section."""

    id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    type = GObject.Property(
        type=CrossSectionType,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY,
        default=CrossSectionType.DISPLAY)
    lanes = GObject.Property(
        type=int,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    b_display_available = GObject.Property(
        type=bool,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY,
        default=False)
    hard_shoulder_available = GObject.Property(
        type=bool,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY,
        default=False)

    def __init__(self, cross_section_state_id: str, cross_section_type: CrossSectionType,
                 lanes: int, b_display_available: bool, hard_shoulder_available: bool) -> None:
        """Construct a new CrossSectionState."""
        super().__init__(id=cross_section_state_id, type=cross_section_type,
                         lanes=lanes, b_display_available=b_display_available,
                         hard_shoulder_available=hard_shoulder_available)