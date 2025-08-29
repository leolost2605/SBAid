"""This module contains a factory to create exporter classes that allow parameter exporting
to a specified file type"""

import typing

from gi.repository import Gio
from gi.repository.Gio import ListStore

from sbaid.model.algorithm_configuration.parameter_export_format import ParameterExportFormat
from sbaid.model.algorithm_configuration.parameter_exporter import ParameterExporter
from sbaid.model.algorithm_configuration.csv_parameter_exporter import CSVParameterExporter
from sbaid.common import list_model_iterator


class ExporterFactoryMeta(type):
    """A metaclass to be used for the ExporterFactory class,
    allowing the implementation of the Singleton pattern."""
    _instances: dict[type, typing.Any] = {}

    def __call__(cls) -> 'ExporterFactory':
        if cls not in cls._instances:
            instance = super().__call__()
            cls._instances[cls] = instance
        return typing.cast(ExporterFactory, cls._instances[cls])


class ExporterFactory(metaclass=ExporterFactoryMeta):
    """SBAid's parameter configuration exporter factory.
    Used to find a suitable exporter for a given file type."""

    __exporters: Gio.ListStore

    # GObject.Property definitions
    parameter_exporters: Gio.ListModel = (
        GObject.Property(type=Gio.ListModel))  # type: ignore[assignment]

    @parameter_exporters.getter  # type: ignore
    def parameter_exporters(self) -> Gio.ListModel:
        """Returns ListModel of available diagram types"""
        return self.__exporters

    def __init__(self) -> None:
        super().__init__()
        self.__exporters = Gio.ListStore.new(ParameterExportFormat)
        self.__exporters.append(CSVParameterExporter().get_export_format())

    def get_exporter(self, export_format: str) -> ParameterExporter | None:
        """Looks for a suitable exporter for the given export format in the available exporters."""
        for param_exporter in list_model_iterator(self.__exporters):
            exporter_id = param_exporter.get_export_format().format_id
            if exporter_id == export_format:
                return param_exporter
        return None

    def get_all_formats(self) -> ListStore:
        """Returns a list of all available exporters."""
        return self.__exporters
