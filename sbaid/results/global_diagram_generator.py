"""todo"""

from abc import abstractmethod
from sbaid.results.diagram_handler import DiagramHandler
from sbaid.results.result import Result
from sbaid.common.image_format import ImageFormat
from sbaid.common.image import Image


class GlobalDiagramGenerator(DiagramHandler):
    """todo"""
    @abstractmethod
    def get_diagram_type(self) -> None:
        """todo"""

    def get_diagram(self, result: Result, cross_section_ids: list,
                    image_format: ImageFormat) -> Image:
        """todo"""
