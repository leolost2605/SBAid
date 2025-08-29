"""This module contains a class for mocking a parameter configuration, so testing the export
 of one can be done more easily."""

from gi.repository import Gio

from sbaid.model.algorithm_configuration.exporter_factory import ExporterFactory

class MockParameterConfiguration:
    """A mock parameter configuration, with the functionalities needed to test parameter exporting."""
    def __init__(self, params: Gio.ListModel):
        self.__parameters = params

    async def export_parameter_configuration(self, path: str, export_format: str):
        file = Gio.File.new_for_path(path)
        factory = ExporterFactory()
        exporter = factory.get_exporter(export_format)
        await exporter.export_parameters(file, self.__parameters)