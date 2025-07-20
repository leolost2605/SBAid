"""todo"""

from abc import ABC, abstractmethod
from gi.repository import GLib
from sbaid.common.diagram_type import DiagramType


class DiagramHandler(ABC):
    """todo"""
    diagram_name: str

    @abstractmethod
    def get_diagram_type(self) -> DiagramType:
        """todo"""
        return DiagramType(GLib.uuid_string_random(),  # pylint:disable=no-value-for-parameter
                           self.diagram_name)  # todo fix this GLib error above
