"""This module represents the class AlgorithmConfigurationManager"""
from gi.repository import GObject, Gio
from sbaid.model.network.network import Network


class AlgorithmConfigurationManager(GObject.GObject):
    """todo"""
    # GObject property definition
    selected_algorithm_configuration_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    available_tags = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    algorithm_configurations = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, network: Network) -> None:
        """todo"""
        super().__init__()

    def load(self) -> None:
        """todo"""

    def create_algorithm_configuration(self) -> int:
        """todo"""
        return None

    def delete_algorithm_configuration(self) -> None:
        """todo"""

    def create_tag(self, name: str) -> int:
        """todo"""
        return None

    def delete_tag(self, tag_id: str) -> None:
        """todo"""
