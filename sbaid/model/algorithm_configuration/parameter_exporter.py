"""This module contains the ParameterExporter interface."""

from abc import ABC, abstractmethod
from gi.repository import Gio


class ParameterExporter(ABC):
    """This interface defines the functions a parameter exporter is capable of."""

    @abstractmethod
    def can_handle_format(self, export_format: str) -> bool:
        """Takes in a file format and returns a boolean representing the exporter's capability
         to export the parameter configuration in the given format."""

    @abstractmethod
    async def for_each_parameter(self, file: Gio.File,  parameters: Gio.ListModel) -> None:
        """Iterates all parameters in the parameter configuration and writes them
        into the given file."""
