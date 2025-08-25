"""
This module contains the class that represents the parameter configuration of an algorithm.
"""

import sys
from typing import Any, cast
from weakref import WeakValueDictionary

import gi

from sbaid import common

from sbaid.model.algorithm_configuration.parameter_configuration import (
    ParameterConfiguration as ModelParameterConfiguration)
from sbaid.model.algorithm_configuration.parameter import Parameter as ModelParameter

from sbaid.view_model.algorithm_configuration.cross_section_parameter import CrossSectionParameter
from sbaid.view_model.algorithm_configuration.global_parameter import GlobalParameter
from sbaid.view_model.algorithm_configuration.parameter import Parameter
from sbaid.view_model.network.network import Network

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GObject, GLib, Gtk, Gio
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ParameterConfiguration(GObject.Object):
    """
    This class represents the parameter configuration of an algorithm.
    """
    __configuration: ModelParameterConfiguration
    __available_tags: Gio.ListModel
    __sort_model: Gtk.SortListModel
    __slice_models_by_parameters: WeakValueDictionary[str, Gtk.SliceListModel]

    selected_cross_sections: Gtk.MultiSelection = GObject.Property(  # type: ignore
        type=Gtk.MultiSelection,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    parameters: Gio.ListModel = GObject.Property(  # type: ignore
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, configuration: ModelParameterConfiguration, network: Network,
                 available_tags: Gio.ListModel):
        self.__configuration = configuration
        self.__available_tags = available_tags
        self.__slice_models_by_parameters = WeakValueDictionary()

        self.__sort_model = Gtk.SortListModel.new(configuration.parameters)
        self.__sort_model.set_section_sorter(Gtk.CustomSorter.new(self.__sort_func))
        self.__sort_model.connect("items-changed", self.__on_items_changed)

        filter_model = Gtk.FilterListModel.new(self.__sort_model,
                                               Gtk.CustomFilter.new(self.__filter_func))

        # We can only start mapping after super().__init__() because we need selected cs
        # so keep model as None for now
        map_model = Gtk.MapListModel.new(None, self.__map_func)

        selection_filter = Gtk.CustomFilter.new(self.__selection_filter_func)

        selection_filter_model = Gtk.FilterListModel.new(map_model, selection_filter)

        super().__init__(selected_cross_sections=Gtk.MultiSelection.new(network.cross_sections),
                         parameters=selection_filter_model)

        map_model.set_model(filter_model)

        self.selected_cross_sections.connect(
            "selection-changed",
            lambda model, pos, n_items: selection_filter.changed(Gtk.FilterChange.DIFFERENT))

    async def load(self) -> None:
        """
        Loads the parameter configuration from the db.
        """
        await self.__configuration.load()

    async def import_parameter_values(self, file: Gio.File) -> tuple[int, int]:
        """
        Imports values for parameters from the given file.
        :param file: the file to import values from
        :return: the number of successful imports and the number of failed imports
        """
        return await self.__configuration.import_from_file(file)

    async def export_parameter_values(self, file: Gio.File) -> None:
        """Exports the parameter configuration to a given file.
        :param file: the file to export values to
        """
        export_file = Gio.File.get_child(file, "param_config.csv")
        await self.__configuration.export_parameter_configuration(export_file)

    def __sort_func(self, first: ModelParameter, second: ModelParameter, data: Any) -> int:
        if first.cross_section is None and second.cross_section is not None:
            return -1

        if second.cross_section is None and first.cross_section is not None:
            return 1

        return GLib.strcmp0(first.name, second.name)

    def __filter_func(self, parameter: ModelParameter) -> bool:
        for i, param in enumerate(common.list_model_iterator(self.__sort_model)):
            if param.name == parameter.name and param.cross_section == parameter.cross_section:
                return self.__sort_model.get_section(i)[0] == i

        assert False

    def __map_func(self, model_parameter: ModelParameter) -> Parameter:
        if model_parameter.cross_section is None:
            return GlobalParameter(model_parameter, self.__available_tags)

        pos = Gtk.INVALID_LIST_POSITION
        for i, param in enumerate(self.__sort_model):
            if param == model_parameter:
                pos = i

        start, end = self.__sort_model.get_section(pos)

        slice_model = Gtk.SliceListModel.new(self.__sort_model, start, end - start)
        self.__slice_models_by_parameters[model_parameter.name] = slice_model
        return CrossSectionParameter(slice_model, self.selected_cross_sections,
                                     self.__available_tags)

    def __on_items_changed(self, model: Gtk.SortListModel, position: int,
                           removed: int, added: int) -> None:
        for i in range(model.get_n_items()):
            param = cast(ModelParameter, model.get_item(i))
            if param.cross_section is None:
                continue

            slice_model = self.__slice_models_by_parameters.get(param.name)

            if slice_model is None:
                continue

            start, end = self.__sort_model.get_section(position)
            slice_model.set_offset(start)
            slice_model.set_size(end - start)

    def __selection_filter_func(self, param: Parameter) -> bool:
        if self.selected_cross_sections.get_selection().is_empty():
            return isinstance(param, GlobalParameter)

        return isinstance(param, CrossSectionParameter)
