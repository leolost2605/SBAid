"""todo"""

from gi.repository import Gio, GObject
from sbaid.model.simulation.parameter_configuration_state import ParameterConfigurationState
from sbaid.model.simulation.input import Input
from sbaid.model.simulation.display import Display
from sbaid.model.simulation.network_state import NetworkState


class Algorithm(GObject.GInterface):
    """todo"""

    def get_global_parameter_template(self) -> Gio.ListModel:
        """todo"""
        return None

    def get_cross_section_parameter_template(self) -> Gio.ListModel:
        """todo"""
        return None

    def init(self, parameter_configuration_state: ParameterConfigurationState,
             network_state: NetworkState) -> None:
        """todo"""
        return None

    def calculate_display(self, algorithm_input: list[Input]) -> Display:
        """todo"""
        return None
