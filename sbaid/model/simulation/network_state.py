"""This module contains the NetworkState class."""
from gi.repository import Gio, GObject
from sbaid.model.simulation.cross_section_state import CrossSectionState
from sbaid.common.location import Location


class NetworkState(GObject.GObject):
    """This class represents the network state of the simulation."""
    route = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    cross_section_states = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, route: list[Location],
                 cross_section_states: list[CrossSectionState]) -> None:
        """Construct a new NetworkState. Lists are turned into ListModels in O(n) time."""
        locations_list_model: Gio.ListStore = Gio.ListStore()
        cross_sections_list_model: Gio.ListStore = Gio.ListStore()
        for location in route:
            locations_list_model.append(location)

        for cross_section_state in cross_section_states:
            cross_sections_list_model.append(cross_section_state)
        super().__init__(route=locations_list_model,
                         cross_section_states=cross_sections_list_model)
