"""This module defines the AlgorithmConfiguration class"""
from gi.repository import GObject

from sbaid.model.database.project_database import ProjectDatabase
from sbaid.model.network.network import Network
from sbaid.model.algorithm.algorithm import Algorithm
from sbaid.model.algorithm_configuration.parameter_configuration import (
    ParameterConfiguration)


class AlgorithmConfiguration(GObject.GObject):
    """This class defines the AlgorithmConfiguration class."""

    # GObject property definition
    id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    script_path = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    evaluation_interval = GObject.Property(
        type=int,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    display_interval = GObject.Property(
        type=int,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    algorithm = GObject.Property(
        type=Algorithm,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    parameter_configuration = GObject.Property(
        type=ParameterConfiguration,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, configuration_id: str, network: Network) -> None:
        """Constructs a new algorithm configuration and automatically configures the parameters.
        Does not yet load anything from the database."""
        super().__init__(id=configuration_id, network=network)
        self.network = network

    def load_from_db(self) -> None:
        """Loads attributes such as name and intervals from the database"""
        self.parameter_configuration.load()
        for parameter in self.parameter_configuration.parameters:
            parameter.load_from_db()
            param_value = ProjectDatabase.get_parameter_value(self.id, self.name)  # crossSection?
            parameter.set_parameter_value(self.id, param_value)
