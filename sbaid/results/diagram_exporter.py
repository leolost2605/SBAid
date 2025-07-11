from gi.repository import GLib, GObject
from sbaid.results.result import Result
from sbaid.common.image_format import ImageFormat
from sbaid.common.diagram_type import DiagramType

"""todo"""

class DiagramExporter:
    """todo"""

    #GObject.Property definitions
    available_diagram_types = GObject.Property(type=GLib.ListModel)

    def create_diagram(self, result: Result, cross_section_ids: list, image_format: ImageFormat, diagram_type: DiagramType):
        """todo"""
        pass
