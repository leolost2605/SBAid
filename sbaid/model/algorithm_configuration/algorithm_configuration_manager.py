"""This module represents the class AlgorithmConfigurationManager"""
import uuid
from zoneinfo import available_timezones

from gi.repository import GObject, Gio, Gtk
from numpy.ma.core import empty

from sbaid.model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.model.algorithm_configuration.parameter_configuration import ParameterConfiguration
from sbaid.model.network.network import Network


class AlgorithmConfigurationManager(GObject.GObject):
    """This class defines the AlgorithmConfigurationManager class."""
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
        GObject.ParamFlags.CONSTRUCT)

    network = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    def __init__(self, network: Network) -> None:
        """todo"""
        super().__init__(network=network)
        self.algorithm_configurations = Gio.ListModel().__init__()
        self.network = network

    def load(self) -> None:
        """todo"""
        for algorithm_configuration in self.algorithm_configurations:
            algorithm_configuration.load_from_db()

    def create_algorithm_configuration(self) -> int:
        """todo"""
        algo_config = AlgorithmConfiguration(str(uuid.uuid4()), self.network)
        algo_config.parameter_configuration = ParameterConfiguration(algo_config.network)
        algo_config.parameter_configuration.import_from_file(algo_config.script_path)
        self.algorithm_configurations.append(algo_config)
        return self.algorithm_configurations.index(algo_config)

    def delete_algorithm_configuration(self) -> None:
        """todo"""
        selected_algo_id = self.selected_algorithm_configuration_id
        selected_algo_config = self.algorithm_configurations.get_by_id(selected_algo_id)
        self.algorithm_configurations.delete(selected_algo_config)

    def create_tag(self, name: str) -> int:
        """todo"""
        self.available_tags.append(name)
        return self.available_tags.index(name)

    def delete_tag(self, tag_id: str) -> None:
        """todo"""
        exists, tag = self.available_tags.find(tag_id)
        if exists:
            self.available_tags.remove(tag)
