"""todo"""
from sbaid.common.diagram_type import DiagramType
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.global_diagram_generator import GlobalDiagramGenerator
from sbaid.model.results.result import Result


class HeatmapGenerator(GlobalDiagramGenerator):
    """todo"""
    diagram_name = "Heatmap-Diagram"

    def get_diagram(self, result: Result, cross_section_ids: list[str],
                    export_format: ImageFormat) -> None:
        pass

    # todo ask if this here is legal
    def get_diagram_type(self) -> DiagramType:  # pylint:disable=useless-parent-delegation
        """todo"""
        return super().get_diagram_type()
