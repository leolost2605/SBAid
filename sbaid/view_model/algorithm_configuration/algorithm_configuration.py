"""
This module contains the algorithm configuration class.
"""

from gi.repository import GObject, Gio

from sbaid.model.algorithm_configuration.algorithm_configuration import (
    AlgorithmConfiguration as ModelAlgorithmConfiguration)
from sbaid.view_model.algorithm_configuration.parameter_configuration import ParameterConfiguration
from sbaid.view_model.network.network import Network


class AlgorithmConfiguration(GObject.Object):
    """
    This class represents an algorithm configuration consisting of a script path where the script
    for the algorithm is, a name, and evaluation and display intervals.
    """
    __configuration: ModelAlgorithmConfiguration
    __network: Network
    __available_tags: Gio.ListModel

    id: str = GObject.Property(type=str)  # type: ignore

    @id.getter  # type: ignore
    def id(self) -> str:
        """Returns the id of the algorithm configuration."""
        return self.__configuration.id

    name: str = GObject.Property(type=str)  # type: ignore

    @name.getter  # type: ignore
    def name(self) -> str:
        """Returns the name of the algorithm configuration."""
        return self.__configuration.name

    @name.setter  # type: ignore
    def name(self, name: str) -> None:
        """Sets the name of the algorithm configuration."""
        self.__configuration.name = name

    evaluation_interval: int = GObject.Property(type=int)  # type: ignore

    @evaluation_interval.getter  # type: ignore
    def evaluation_interval(self) -> int:
        """Returns the evaluation interval of the algorithm configuration."""
        return self.__configuration.evaluation_interval

    @evaluation_interval.setter  # type: ignore
    def evaluation_interval(self, value: int) -> None:
        """Sets the evaluation interval of the algorithm configuration."""
        self.__configuration.evaluation_interval = value

    display_interval: int = GObject.Property(type=int)  # type: ignore

    @display_interval.getter  # type: ignore
    def display_interval(self) -> int:
        """Returns the display interval of the algorithm configuration."""
        return self.__configuration.display_interval

    @display_interval.setter  # type: ignore
    def display_interval(self, value: int) -> None:
        """Sets the display interval of the algorithm configuration."""
        self.__configuration.display_interval = value

    script_path: str = GObject.Property(type=str)  # type: ignore

    @script_path.getter  # type: ignore
    def script_path(self) -> str:
        """Returns the script path of the algorithm configuration."""
        return self.__configuration.script_path

    @script_path.setter  # type: ignore
    def script_path(self, value: str) -> None:
        """Sets the script path of the algorithm configuration."""
        self.__configuration.script_path = value

    parameter_configuration: ParameterConfiguration = GObject.Property(  # type: ignore
        type=ParameterConfiguration,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, configuration: ModelAlgorithmConfiguration,
                 network: Network, available_tags: Gio.ListModel) -> None:
        parameter_configuration = ParameterConfiguration(configuration.parameter_configuration,
                                                         network, available_tags)
        super().__init__(parameter_configuration=parameter_configuration)
        self.__configuration = configuration
