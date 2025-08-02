"""todo"""


from abc import ABC, abstractmethod
from sbaid.common.diagram_type import DiagramType
from sbaid.model.results.result import Result
from sbaid.common.image_format import ImageFormat


class DiagramHandler(ABC):
    """todo"""
    @abstractmethod
    def get_diagram(self, result: Result, cross_section_ids: list, image_format: ImageFormat) -> DiagramType:
        """todo"""
