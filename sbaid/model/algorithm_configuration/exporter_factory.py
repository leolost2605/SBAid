"""This module contains a factory to create exporter classes that allow parameter exporting
to a specified file type"""

import typing

from sbaid.model.algorithm_configuration.parameter_exporter import ParameterExporter
from sbaid.model.algorithm_configuration.csv_parameter_exporter import CSVParameterExporter


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

    __exporters: list[ParameterExporter] = []

    def __init__(self) -> None:
        self.__exporters.append(CSVParameterExporter())

    def get_exporter(self, export_format: str) -> ParameterExporter | None:
        """Looks for a suitable parser for the given export format in the available parsers."""
        for param_exporter in self.__exporters:
            exporter_id = param_exporter.get_export_format().format_id
            if exporter_id == export_format:
                return param_exporter
        return None

    def get_all_formats(self) -> list[ParameterExporter]:
        """Returns a list of all available exporters."""
        return self.__exporters
