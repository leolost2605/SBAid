"""todo"""

from gi.repository import GLib
from abc import ABC, abstractmethod
from sbaid.common.diagram_type import DiagramType


class DiagramHandler(ABC):
    """todo"""
    diagram_name: str
    is_global: bool

    @abstractmethod
    def get_diagram_type(self) -> DiagramType:
        """todo"""
        return DiagramType(GLib.uuid_string_random(), self.diagram_name, is_global=self.is_global)
