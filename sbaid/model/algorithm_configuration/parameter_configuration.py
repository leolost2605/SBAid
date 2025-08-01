"""This module defines the ParameterConfiguration class."""
import sys

import gi

from sbaid import common
from sbaid.model.algorithm.parameter_template import ParameterTemplate
from sbaid.model.algorithm_configuration.parameter import Parameter
from sbaid.model.algorithm_configuration.parser_factory import ParserFactory
from sbaid.model.network.network import Network
from sbaid.model.algorithm.algorithm import Algorithm

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GObject, GLib, Gio, Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ParameterConfiguration(GObject.GObject):
    """
    This class manages the parameters for an algorithm configuration. It automatically
    maps the template taken from the algorithm to actual parameters. If a parameter template
    is per cross section it builds a parameter for each cross section currently in the network.
    """

    __network: Network
    __cs_params_map_model: Gtk.MapListModel
    __global_params_map_model: Gtk.MapListModel
    __parameters: Gtk.FlattenListModel

    @GObject.Property(type=Gio.ListModel)
    def parameters(self) -> Gio.ListModel:
        """The list of global and per cross section parameters for each cross section."""
        return self.__parameters

    def __init__(self, network: Network) -> None:
        super().__init__()
        self.__network = network

        self.__cs_params_map_model = Gtk.MapListModel.new(None, self.__map_cs_params, self)
        cs_params_flatten_model = Gtk.FlattenListModel.new(self.__cs_params_map_model)
        self.__global_params_map_model = Gtk.MapListModel.new(None, self.__map_global_params, self)
        global_and_cs_list_store = Gio.ListStore.new(Gio.ListModel)
        global_and_cs_list_store.append(self.__global_params_map_model)
        global_and_cs_list_store.append(cs_params_flatten_model)
        self.__parameters = Gtk.FlattenListModel.new(global_and_cs_list_store)

    async def import_from_file(self, file: Gio.File) -> tuple[int, int]:
        """
        Imports parameter values from the given file. If the file or no parser for the file type
        exists, an exception is raised. If a parameter is invalid it will be skipped.
        :param file: The file to import
        :return: The number of valid parameters and the number of invalid parameters
        """
        parser = ParserFactory().get_parser(file)
        return await parser.for_each_parameter(file, self.__import_param_func)

    def __import_param_func(self, name: str, cross_section_id: str | None,
                            value: GLib.Variant) -> bool:
        # TODO: Maybe wrap the listmodel in a custom hashing implementation for fast access
        for param in common.list_model_iterator(self.__parameters):
            if (param.name == name and param.cross_section.id == cross_section_id
                    and value.is_of_type(param.value_type)):
                param.value = value
                return True

        return False

    def load(self) -> None:
        """Loads the parameter values from the database."""
        for param in common.list_model_iterator(self.__parameters):
            param.load_from_db()

    def set_algorithm(self, algorithm: Algorithm) -> None:
        """
        Informs the param configuration about the currently used algorithm.
        It will then build the list of parameters from the algorithms template.
        """
        self.__global_params_map_model.set_model(algorithm.get_global_parameter_template())
        self.__cs_params_map_model.set_model(algorithm.get_cross_section_parameter_template())

    def __map_cs_params(self, template: ParameterTemplate) -> GObject.Object:
        list_store = Gio.ListStore.new(Parameter)

        for cs in common.list_model_iterator(self.__network.cross_sections):
            list_store.append(Parameter(template.name, template.value_type,
                                        template.default_value, cs))

        return list_store

    def __map_global_params(self, template: ParameterTemplate) -> GObject.Object:
        return Parameter(template.name, template.value_type, template.default_value, None)
