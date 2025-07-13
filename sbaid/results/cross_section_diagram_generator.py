"""todo"""


from sbaid.common.diagram_type import DiagramType
from sbaid.results.diagram_handler import DiagramHandler


class CrossSectionDiagramGenerator(DiagramHandler):
    """todo"""
    def get_diagram_type(self) -> DiagramType:
        """todo"""
        diagram_type = DiagramType("todo", "todo")
        return diagram_type
