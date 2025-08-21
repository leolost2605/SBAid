from abc import ABC, abstractmethod
from gi.repository import GLib, Gio
from collections.abc import Callable
from typing import Any, Coroutine
from sbaid.model.network.cross_section import CrossSection

#ParameterExporterForeachFunc = Callable[[str, GLib.VariantType, GLib.Variant, CrossSection],Coroutine[Any, Any, bool]]

class ParameterExporter(ABC):

    @abstractmethod
    def can_handle_format(self, export_format: str) -> bool:
        """Takes in a file format and returns a boolean representing the exporter's capability
         to export the parameter configuration in the given format."""

    @abstractmethod
    async def for_each_parameter(self, file: Gio.File,  parameters: Gio.ListModel):
        """Iterates all parameters in the parameter configuration and writes them
        into the given file."""