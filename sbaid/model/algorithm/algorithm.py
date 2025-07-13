"""todo"""

from abc import ABC, abstractmethod
from gi.repository import Gio
from sbaid.model.simulation.parameter_configuration_state import ParameterConfigurationState
from sbaid.model.simulation.input import Input
from sbaid.model.simulation.display import Display
from sbaid.model.network.network import Network


class Algorithm(ABC):
    """todo"""

    @abstractmethod
    def get_global_parameter_template(self) -> Gio.ListModel:
        """todo"""

    @abstractmethod
    def get_cross_section_parameter_template(self) -> Gio.ListModel:
        """todo"""

    @abstractmethod
    def init(self, parameter_configuration_state: ParameterConfigurationState,
             network_state: Network) -> None:
        """todo"""

    @abstractmethod
    def calculate_display(self, algorithm_input: list[Input]) -> Display:
        """todo"""
