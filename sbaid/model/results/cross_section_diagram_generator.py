"""This module defines the CrossSectionDiagramGenerator class """
from abc import ABC, abstractmethod
from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.diagram_handler import DiagramHandler
from sbaid.model.results.result import Result


class CrossSectionDiagramGenerator(DiagramHandler, ABC):
    """This class defines the get_diagram method for diagrams that
    only require a single cross-section as an input."""

    @abstractmethod
    def get_diagram(self, result: Result, cross_section_id: str,
                    export_format: ImageFormat) -> Image:
        """Returns image of generated diagram."""
