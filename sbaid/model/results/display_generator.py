"""todo"""
from gi.repository import GLib
from sbaid.common.diagram_type import DiagramType
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.cross_section_diagram_generator import CrossSectionDiagramGenerator
from sbaid.model.results.result import Result


class DisplayGenerator(CrossSectionDiagramGenerator):
    """todo"""

    diagram_name = "Display-Diagram"
    diagram_id = GLib.uuid_string_random()

    # todo ask if this here is legal
    def get_diagram_type(self) -> DiagramType:  # pylint:disable=useless-parent-delegation
        """Return diagram type of the display generator"""
        return super().get_diagram_type()

    def get_diagram(self, result: Result, cross_section_id: str,
                    export_format: ImageFormat) -> None:
        pass
