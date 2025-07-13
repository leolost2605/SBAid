"""This module defines the ParameterConfiguration class."""
import gi
from gi.repository import GObject
from gi.repository import Gio
from sbaid.model.network import Network
from sbaid.model.algorithm import Algorithm

class ParameterConfiguration(GObject.GObject):
    """This class defines the ParameterConfiguration class."""

    parameters = GObject.property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)

    __network = GObject.property(
        type=Network,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY
    )

    def __init__(self, network: Network) -> None:
        """todo"""
        self.network = network
        pass

    def import_from_file(self, file: Gio.File) -> [int, int]:
        """"todo"""
        pass

    def load(self) -> None:
        """todo"""
        pass

    def set_algorithm(self, algorithm: Algorithm) -> None:
        """todo"""
        pass
