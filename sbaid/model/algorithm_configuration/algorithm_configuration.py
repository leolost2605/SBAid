"""This module defines the AlgorithmConfiguration class"""
from gi.repository import GObject
from sbaid.model.network.network import Network
from sbaid.model.algorithm.algorithm import Algorithm
from sbaid.model.algorithm_configuration.parameter_configuration import (
    ParameterConfiguration)


class AlgorithmConfiguration(GObject.GObject):
    """Todo"""

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

    parameter_configuration = GObject.Property(
        type=ParameterConfiguration,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, configuration_id: str, algorithm: Algorithm, netowork: Network) -> None:
        """todo"""
        super().__init__(id=configuration_id)
        self.algorithm = algorithm

    def load_from_db(self) -> None:
        """todo"""

    # not a GObject.Property in order to avoid Algorithm implementation GObject inheritance
    def get_algorithm(self) -> Algorithm:
        """Gets the algorithm."""
        return self.algorithm
