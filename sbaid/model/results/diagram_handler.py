"""todo"""


from abc import ABC, abstractmethod
from sbaid.common.diagram_type import DiagramType


class DiagramHandler(ABC):
    """todo"""
    @abstractmethod
    def get_diagram_type(self) -> DiagramType:
        """todo"""
