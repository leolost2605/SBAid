"""todo"""

from gi.repository import Gio, GObject
from sbaid.model.results.result import Result
from sbaid.common.image_format import ImageFormat
from sbaid.common.diagram_type import DiagramType


class DiagramExporter:
    """todo"""

    # GObject.Property definitions
    available_diagram_types = GObject.Property(type=Gio.ListModel,
                                               flags=GObject.ParamFlags.READABLE |
                                               GObject.ParamFlags.WRITABLE |
                                               GObject.ParamFlags.CONSTRUCT_ONLY)

    def create_diagram(self, result: Result, cross_section_ids: list[str],
                       image_format: ImageFormat, diagram_type: DiagramType) -> None:
        """todo"""
