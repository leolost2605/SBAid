"""This module represents the class AlgorithmConfigurationManager"""
from gi.repository import GObject, Gio
from sbaid.model.network import Network

class AlgorithmConfigurationManager(GObject.GObject):

    # GObject property definition
    selected_algorithm_configuration_id = GObject.property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT)

    available_tags = GObject.property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)

    algorithm_configuration = GObject.property(
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

    def __init__(self, id: str, network: Network) -> None:
        """todo"""
        self.id = id
        self.network = network
        pass

    def load(self) -> None:
        """todo"""
        pass

    def create_algorithm_configuration(self) -> int: #algorithm_configuration_list_position
        """todo"""
        pass

    def delete_algorithm_configuration(self) -> None:
        """todo"""
        pass

    def create_tag(name: str) -> int: #list position
        """todo"""
        pass

    def delete_tag(id: str) -> None:
        """todo"""
        pass

