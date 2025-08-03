"""
This module contains the algorithm configuration manager class.
"""

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
    """
    This class manages the algorithm configuration and allows to create new ones
    as well as delete old ones.
    """
    __manager: ModelAlgorithmConfigurationManager
    __network: Network
    __algorithm_configurations: Gio.ListStore

    available_tags: Gio.ListModel = GObject.Property(  # type: ignore
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    algorithm_configurations: Gtk.SingleSelection = GObject.Property(  # type: ignore
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
        """
        Creates a new algorithm configuration.
        :return: the position in the list of algo configs where the new configuration is
        """
        return await self.__manager.create_algorithm_configuration()

    async def delete_algorithm_configuration(self, algorithm_configuration_id: str) -> None:
        """
        Deletes the algorithm configuration with the given id.
        :param algorithm_configuration_id: the id of the algorithm configuration to delete.
        """
        self.__manager.delete_algorithm_configuration(algorithm_configuration_id)

    async def create_tag(self, name: str) -> int:
        """
        Creates a tag with the given name.
        :param name: the name of the tag to create.
        :return: the position in the list of tags where the new tag is
        """
        return await self.__manager.create_tag(name)

    async def delete_tag(self, tag_id: str) -> None:
        """
        Deletes the tag with the given id.
        :param tag_id: the id of the tag to delete
        """
        self.__manager.delete_tag(tag_id)
