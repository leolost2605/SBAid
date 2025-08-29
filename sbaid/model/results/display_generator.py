"""This module defines the DisplayGenerator class."""
from sbaid.common.diagram_type import DiagramType
from sbaid.common.i18n import i18n
from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.cross_section_diagram_generator import CrossSectionDiagramGenerator
from sbaid.model.results.result import Result


class DisplayGenerator(CrossSectionDiagramGenerator):
    """Contains methods for generating the 'Display-Diagram'."""
    # TODO

    def get_diagram_type(self) -> DiagramType:
        """Return diagram type of the display generator"""
        return DiagramType("Display-Diagram", i18n._("Display-Diagram"))

    def get_diagram(self, result: Result, cross_section_id: str,  # type: ignore[empty-body]
                    export_format: ImageFormat) -> Image:
        """Returns the 'Display-Diagram' corresponding to the given result."""
