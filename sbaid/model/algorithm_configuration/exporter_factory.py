import typing

from sbaid.model.algorithm_configuration.parameter_exporter import ParameterExporter
from sbaid.model.algorithm_configuration.csv_parameter_exporter import CSVParameterExporter

class ExporterFactoryMeta(type):
    _instances: dict[type, typing.Any] = {}

    def __call__(cls) -> 'ExporterFactory':
        if cls not in cls._instances:
            instance = super().__call__()
            cls._instances[cls] = instance
        return typing.cast(ExporterFactory, cls._instances[cls])


class ExporterFactory(metaclass=ExporterFactoryMeta):

    __exporters: list[ParameterExporter] = []

    def __init__(self):
        self.__exporters.append(CSVParameterExporter())

    def get_exporter(self, export_format: str) -> ParameterExporter | None:
        for exporter in self.__exporters:
            if exporter.can_handle_format(export_format):
                return exporter
        return None
