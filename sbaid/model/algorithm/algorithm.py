# mypy: disable-error-code="empty-body"
"""
This module defines the algorithm interface that has to be implemented by algorithms used
as an SBA.
"""

from gi.repository import Gio, GObject

from sbaid.model.simulation.parameter_configuration_state import ParameterConfigurationState
from sbaid.model.simulation.input import Input
from sbaid.model.simulation.display import Display
from sbaid.model.simulation.network_state import NetworkState


class Algorithm(GObject.GObject):
    """
    This interface should be implemented by a SBA. To do that, define a class `AlgorithmImpl`
    that extends Algorithm. Then implement the methods defined below.
    """

    def get_global_parameter_template(self) -> Gio.ListModel:
        """
        Returns a list of ParameterTemplate objects that define the parameters that apply
        globally to your algorithm.
        :return: a ListModel of ParameterTemplate objects
        """

    def get_cross_section_parameter_template(self) -> Gio.ListModel:
        """
        Returns a list of ParameterTemplate objects that define the parameters that apply
        for each cross section.
        :return: a ListModel of ParameterTemplate objects
        """

    def init(self, parameter_configuration_state: ParameterConfigurationState,
             network_state: NetworkState) -> None:
        """
        Initializes your algorithm. The given parameter configuration contains information about
        the cross section on the route and the network state contains information about the route.
        :param parameter_configuration_state:
        :param network_state:
        """

    def calculate_display(self, algorithm_input: Input) -> Display:
        """
        Calculates the display for the cross sections based on the given input.
        :param algorithm_input: the input as measurements to base your calculations on
        :return: the signs to display for each cross section
        """
