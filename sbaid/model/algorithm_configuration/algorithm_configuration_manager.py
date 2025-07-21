"""This module represents the class AlgorithmConfigurationManager"""
import uuid
from gi.repository import GObject, Gio

from sbaid.model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.model.algorithm_configuration.parameter_configuration import ParameterConfiguration
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
        super().__init__(network=network)
        self.network = network

    def load(self) -> None:
        for algorithm_configuration in self.algorithm_configurations:
            algorithm_configuration.load()

    def create_algorithm_configuration(self) -> int:
        algo_config = AlgorithmConfiguration(str(uuid.uuid4()), self.network)
        param_config = ParameterConfiguration(algo_config.network)
        parameters = param_config.import_from_file()  # create the list of params, file?
        return None

    def delete_algorithm_configuration(self) -> None:
        selected_id = self.selected_algorithm_configuration_id
        selected_algo_config = self.algorithm_configurations.get_by_id(selected_id)
        self.algorithm_configurations.delete(selected_algo_config)

    def create_tag(self, name: str) -> int:
        """todo"""
        return None

    def delete_tag(self, tag_id: str) -> None:
        """todo"""
