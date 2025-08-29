"""This module defines the ParameterConfiguration class."""
import sys
import gi

from sbaid import common
from sbaid.model.algorithm.parameter_template import ParameterTemplate
from sbaid.model.algorithm_configuration.exporter_factory import ExporterFactory
from sbaid.model.algorithm_configuration.parameter import Parameter
from sbaid.model.algorithm_configuration.parser_factory import ParserFactory
from sbaid.model.database.project_database import ProjectDatabase
from sbaid.model.network.cross_section import CrossSection
from sbaid.model.network.network import Network, NoSuitableParserException
from sbaid.model.algorithm.algorithm import Algorithm

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GObject, GLib, Gio, Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class NoExporterAvailableException(Exception):
    """Raised when the chosen parameter export format doesn't
     have a compatible exporter in SBAid."""


class NoFormatException(Exception):
    """
    Raised when no format for exporting the parameter values was detected
    for the given file.
    """


class ParameterConfiguration(GObject.GObject):  # pylint: disable=too-many-instance-attributes
    """
    This class manages the parameters for an algorithm configuration. It automatically
    maps the template taken from the algorithm to actual parameters. If a parameter template
    is per cross section it builds a parameter for each cross section currently in the network.
    """

    __loaded: bool = False
    __network: Network
    __db: ProjectDatabase
    __algo_config_id: str
    __available_tags: Gio.ListModel
    __cs_params_map_model: Gtk.MapListModel
    __global_params_map_model: Gtk.MapListModel
    __parameters: Gtk.FlattenListModel

    parameters: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore

    @parameters.getter  # type: ignore
    def parameters(self) -> Gio.ListModel:
        """The list of global and per cross section parameters for each cross section."""
        return self.__parameters

    def __init__(self, network: Network, db: ProjectDatabase, algo_config_id: str,
                 available_tags: Gio.ListModel) -> None:
        super().__init__()
        self.__network = network
        self.__db = db
        self.__algo_config_id = algo_config_id
        self.__available_tags = available_tags

        self.__cs_params_map_model = Gtk.MapListModel.new(None, self.__map_cs_params)
        cs_params_flatten_model = Gtk.FlattenListModel.new(self.__cs_params_map_model)
        self.__global_params_map_model = Gtk.MapListModel.new(None, self.__map_global_params)
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
        if parser is None:
            raise NoSuitableParserException()
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

    async def export_parameter_configuration(self, file: Gio.File) -> None:
        """Saves this parameter configuration, exported to a file of a chosen format,
         to a path given by the user."""
        if file.get_basename() is None:
            raise NoFormatException("File name was None so no format could be detected.")

        split_name = file.get_basename().split('.')
        if not split_name:
            raise NoFormatException(f"No format detected in file name {file.get_basename()}")

        export_format = split_name[-1].lower()

        exporter = ExporterFactory().get_exporter(export_format)
        if exporter is None:
            raise NoExporterAvailableException(
                f"No exporter available for format {export_format}")
        await exporter.export_parameters(file, self.__parameters)

    async def load(self) -> None:
        """Loads the parameter values from the database."""
        if self.__loaded:
            return

        self.__loaded = True

        for param in common.list_model_iterator(self.__parameters):
            await param.load_from_db()

    def set_algorithm(self, algorithm: Algorithm) -> None:
        """
        Informs the param configuration about the currently used algorithm.
        It will then build the list of parameters from the algorithms template.
        """
        self.__global_params_map_model.set_model(algorithm.get_global_parameter_template())
        self.__cs_params_map_model.set_model(algorithm.get_cross_section_parameter_template())

    def __map_cs_params(self, template: ParameterTemplate) -> GObject.Object:
        return Gtk.MapListModel.new(self.__network.cross_sections, self.__map_cs_param, template)

    def __map_cs_param(self, cross_section: CrossSection,
                       template: ParameterTemplate) -> Parameter:
        return Parameter(template.name, template.value_type, template.default_value,
                         cross_section, self.__db, self.__algo_config_id, self.__available_tags)

    def __map_global_params(self, template: ParameterTemplate) -> GObject.Object:
        return Parameter(template.name, template.value_type, template.default_value,
                         None, self.__db, self.__algo_config_id, self.__available_tags)
