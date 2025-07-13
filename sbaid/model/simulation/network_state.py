"""TODO"""
from gi.repository import Gio, GObject
from sbaid.model.simulation.cross_section_state import CrossSectionState
from sbaid.common.coordinate import Coordinate


class NetworkState(GObject.GObject):
    """TODO"""
    route = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    cross_section_states = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, route: list[Coordinate],
                 cross_section_states: list[CrossSectionState]) -> None:
        """TODO"""
        # TODO: convert lists to listmodels aka stores
        super().__init__()
