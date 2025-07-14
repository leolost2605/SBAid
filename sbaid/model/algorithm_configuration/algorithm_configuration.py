"""This module defines the AlgorithmConfiguration class"""
from gi.repository import GObject
from sbaid.model.network import Network
from sbaid.model.algorithm import Algorithm
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
        """todo"""
        super().__init__(id=configuration_id)

    def load_from_db(self) -> None:
        """todo"""
