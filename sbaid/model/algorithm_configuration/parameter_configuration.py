"""This module defines the ParameterConfiguration class."""
from typing import Tuple
from gi.repository import GObject
from gi.repository import Gio
from sbaid.model.network import Network
from sbaid.model.algorithm import Algorithm


class ParameterConfiguration(GObject.GObject):
    """This class defines the ParameterConfiguration class."""

    # GObject property definition
    parameters = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    _network = Network

    def __init__(self, network: Network) -> None:
        """todo"""
        super().__init__()

    def import_from_file(self, file: Gio.File) -> Tuple[int, int]:
        """"todo"""

    def load(self) -> None:
        """todo"""

    def set_algorithm(self, algorithm: Algorithm) -> None:
        """todo"""
