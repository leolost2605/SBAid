"""todo"""
from abc import abstractmethod
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.diagram_handler import DiagramHandler
from sbaid.model.results.result import Result


class CrossSectionDiagramGenerator(DiagramHandler):
    """todo"""
    is_global = False

    @abstractmethod
    def get_diagram(self, result: Result, cross_section_id: str,
                    export_format: ImageFormat) -> None:
        """todo"""
