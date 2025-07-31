"""todo"""
from sbaid.common.diagram_type import DiagramType
from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.global_diagram_generator import GlobalDiagramGenerator
from sbaid.model.results.result import Result


class HeatmapGenerator(GlobalDiagramGenerator):
    """todo"""

    def get_diagram(self, result: Result, cross_section_ids: list[str],  # type: ignore[empty-body]
                    export_format: ImageFormat) -> Image:
        pass

    def get_diagram_type(self) -> DiagramType:
        """todo"""
        return DiagramType("Heatmap-Diagram", "Heatmap-Diagram")
