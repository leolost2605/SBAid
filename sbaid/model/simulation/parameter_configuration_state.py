"""This module contains the ParameterConfigurationState class."""
from gi.repository import Gio
from gi.repository import GObject
from sbaid.model.simulation.parameter_state import ParameterState


class ParameterConfigurationState(GObject.GObject):
    """This class represents a single parameter configuration state.
    It contains multiple parameter states."""
    parameter_states = GObject.Property(type=Gio.ListModel,
                                        flags=GObject.ParamFlags.READABLE |
                                        GObject.ParamFlags.WRITABLE |
                                        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, parameter_states: list[ParameterState]) -> None:
        """Construct a new ParameterConfigurationState.
        The parameter_states list is turned into ListModels in O(n) time."""
        parameter_states_list_model: Gio.ListStore = Gio.ListStore()
        for parameter_state in parameter_states:
            parameter_states_list_model.append(parameter_state)

        super().__init__(parameter_states=parameter_states_list_model)
