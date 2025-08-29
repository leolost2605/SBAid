"""This module contains the ParameterExporter interface."""

from abc import ABC, abstractmethod
from gi.repository import Gio

from sbaid.model.algorithm_configuration.parameter_export_format import ParameterExportFormat


class ParameterExporter(ABC):
    """This interface defines the functions a parameter exporter is capable of."""

    @abstractmethod
    def get_export_format(self) -> ParameterExportFormat:
        """Returns the export format."""

    @abstractmethod
    async def export_parameters(self, file: Gio.File, parameters: Gio.ListModel) -> None:
        """Iterates all parameters in the parameter configuration and writes them
        into the given file."""
