"""TODO"""
from gi.repository import GObject
from cross_section_state import CrossSectionState
from sbaid.common.coordinate import Coordinate


class NetworkState(GObject.GObject):
    """TODO"""
    route = GObject.Property(
        type=list[Coordinate],
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    cross_section_states = GObject.Property(
        type=list[CrossSectionState],
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, route: list[Coordinate], cross_section_states: list[CrossSectionState]) -> None:
        super().__init__(route=route, cross_section_states=cross_section_states)
