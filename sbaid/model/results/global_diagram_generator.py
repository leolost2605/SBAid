"""This module defines the GlobalDiagramGenerator class."""

from abc import abstractmethod
from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.diagram_handler import DiagramHandler
from sbaid.model.results.result import Result


class GlobalDiagramGenerator(DiagramHandler):
    """This class defines the get_diagram method for diagrams that
    only require a list of cross-sections as an input."""

    @abstractmethod
    def get_diagram(self, result: Result, cross_section_ids: list[str],
                    export_format: ImageFormat) -> Image:
        """Returns image of generated diagram."""
