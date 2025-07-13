"""TODO"""
from gi.repository import GObject
from sbaid.model.simulation.parameter_state import ParameterState


class Parameter(GObject.GObject):
    """TODO"""

    def __init__(self, parameter_states: list[ParameterState]) -> None:
        """TODO"""
        super().__init__()
