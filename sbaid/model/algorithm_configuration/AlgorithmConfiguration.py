"""This module defines the AlgorithmConfiguration class"""
from gi.repository import GObject, Gio
from sbaid.model.network import Network
from sbaid.model.algorithm import Algorithm
from sbaid.model.algorithm_configuration import ParameterConfiguration


class AlgorithmConfiguration(GObject.GObject):
    """Todo"""

    id = GObject.property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)

    name = GObject.property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT)

    script_path = GObject.property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT)

    evaluation_interval = GObject.property(
        type=int,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT)

    display_interval = GObject.property(
        type=int,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT)

    algorithm = GObject.property(
        type=Algorithm,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)

    __network = GObject.property(
        type=Network,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY
    )

    parameter_configuration = GObject.property(
        type=ParameterConfiguration,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, id: str, network: Network) -> None:
        """todo"""
        self.id = id
        self.network = network
        pass

    def load_from_db(self) -> None:
        """todo"""
        pass

