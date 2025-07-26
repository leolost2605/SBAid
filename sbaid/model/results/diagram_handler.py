"""todo"""

from abc import ABC, abstractmethod
from sbaid.common.diagram_type import DiagramType


class DiagramHandler(ABC):
    """todo"""
    diagram_name: str
    diagram_id: str

    @abstractmethod
    def get_diagram_type(self) -> DiagramType:
        """todo"""
        return DiagramType(self.diagram_id,  # pylint:disable=no-value-for-parameter
                           self.diagram_name)  # todo fix this GLib error above
