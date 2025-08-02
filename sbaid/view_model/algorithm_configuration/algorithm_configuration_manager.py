import sys
import gi

from sbaid.model.algorithm_configuration.algorithm_configuration_manager import (
    AlgorithmConfigurationManager as ModelAlgorithmConfigurationManager)
from sbaid.model.algorithm_configuration.algorithm_configuration import (
    AlgorithmConfiguration as ModelAlgorithmConfiguration)

from sbaid.view_model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.view_model.network.network import Network

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GObject, Gtk, Gio
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class AlgorithmConfigurationManager(GObject.Object):
    __manager: ModelAlgorithmConfigurationManager
    __network: Network
    __algorithm_configurations: Gio.ListStore

    available_tags: Gio.ListModel = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    algorithm_configurations: Gtk.SingleSelection = GObject.Property(
        type=Gtk.SingleSelection,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, manager: ModelAlgorithmConfigurationManager, network: Network):
        self.__manager = manager
        self.__network = network

        algo_configs = Gtk.MapListModel.new(manager.algorithm_configurations,
                                            self.__algo_config_map_func)

        super().__init__(available_tags=manager.available_tags,
                         algorithm_configurations=Gtk.SingleSelection.new(algo_configs))

    def __algo_config_map_func(self, algorithm_configuration:
                               ModelAlgorithmConfiguration) -> AlgorithmConfiguration:
        return AlgorithmConfiguration(algorithm_configuration, self.__network, self.available_tags)

    async def create_algorithm_configuration(self) -> int:
        return await self.__manager.create_algorithm_configuration()

    async def delete_algorithm_configuration(self, algorithm_configuration_id: str) -> None:
        await self.__manager.delete_algorithm_configuration(algorithm_configuration_id)

    async def create_tag(self, name: str) -> int:
        return await self.__manager.create_tag(name)

    async def delete_tag(self, tag_id: str) -> None:
        await self.__manager.delete_tag(tag_id)
