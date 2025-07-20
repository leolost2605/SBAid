"""This module defines the DiagramExporter class"""

from gi.repository import Gio, GObject
from sbaid.model.results.cross_section_diagram_generator import CrossSectionDiagramGenerator
from sbaid.model.results.display_generator import DisplayGenerator
from sbaid.model.results.global_diagram_generator import GlobalDiagramGenerator
from sbaid.model.results.heatmap_generator import HeatmapGenerator
from sbaid.model.results.qv_generator import QVGenerator
from sbaid.model.results.result import Result
from sbaid.common.image_format import ImageFormat
from sbaid.common.diagram_type import DiagramType
from sbaid.model.results.velocity_generator import VelocityGenerator


class DiagramExporter(GObject.GObject):
    """Handles logic for the configuration and exporting of results, """
    __generator_instances: list[CrossSectionDiagramGenerator | GlobalDiagramGenerator]

    # GObject.Property definitions
    available_diagram_types = GObject.Property(type=Gio.ListModel,
                                               flags=GObject.ParamFlags.READABLE |
                                               GObject.ParamFlags.WRITABLE |
                                               GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self):
        """todo Initialize the diagram exporter"""
        super().__init__(available_diagram_types=Gio.ListStore.new(DiagramType))

        self.__generator_instances = []
        self.__generator_instances.append(HeatmapGenerator())
        self.__generator_instances.append(QVGenerator())
        self.__generator_instances.append(VelocityGenerator())
        self.__generator_instances.append(DisplayGenerator())

        self.__add_available_types()

    def create_diagram(self, result: Result, cross_section_ids: list[str],
                       image_format: ImageFormat, diagram_type: DiagramType) -> None:
        """todo"""
        for generator in self.__generator_instances:
            if diagram_type == generator.get_diagram_type():
                if diagram_type.is_diagram_global:
                    generator.get_diagram(result, cross_section_ids, image_format)
                else:
                    generator.get_diagram(result, cross_section_ids[0], image_format)

    def __add_available_types(self) -> None:
        """Gets available diagram types"""
        for diagram_handler in self.__generator_instances:
            self.available_diagram_types.append(diagram_handler.get_diagram_type())  # pylint: disable=no-member
