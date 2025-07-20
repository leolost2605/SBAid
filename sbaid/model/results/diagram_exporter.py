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
    __global_gens: list[GlobalDiagramGenerator]
    __cross_section_gens: list[CrossSectionDiagramGenerator]
    __heatmap_gen: HeatmapGenerator
    __qv_gen: QVGenerator
    __display_gen: DisplayGenerator
    __velocity_gen: VelocityGenerator
    # GObject.Property definitions
    available_diagram_types = GObject.Property(type=Gio.ListModel,
                                               flags=GObject.ParamFlags.READABLE |
                                               GObject.ParamFlags.WRITABLE |
                                               GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self) -> None:
        """todo Initialize the diagram exporter"""
        super().__init__(available_diagram_types=Gio.ListStore.new(DiagramType))
        self.__add_available_types()

    def create_diagram(self, result: Result, cross_section_ids: list[str],
                       image_format: ImageFormat, diagram_type: DiagramType) -> None:
        """todo"""
        type_id = diagram_type.diagram_type_id

        for global_gen in self.__global_gens:
            if type_id == global_gen.get_diagram_type().diagram_type_id:
                global_gen.get_diagram(result, cross_section_ids, image_format)

        for cs_gen in self.__cross_section_gens:
            if type_id == cs_gen.get_diagram_type().diagram_type_id:
                cs_gen.get_diagram(result, cross_section_ids[0], image_format)

    def __add_available_types(self) -> None:
        """Gets available diagram types and initialize references"""
        self.__heatmap_gen = HeatmapGenerator()
        self.available_diagram_types.append(        # pylint:disable=no-member
            self.__heatmap_gen.get_diagram_type())
        self.__qv_gen = QVGenerator()
        self.available_diagram_types.append(        # pylint:disable=no-member
            self.__qv_gen.get_diagram_type())
        self.__display_gen = DisplayGenerator()
        self.available_diagram_types.append(        # pylint:disable=no-member
            self.__display_gen.get_diagram_type())
        self.__velocity_gen = VelocityGenerator()
        self.available_diagram_types.append(        # pylint:disable=no-member
            self.__velocity_gen.get_diagram_type())

        self.__cross_section_gens = [self.__qv_gen, self.__display_gen, self.__velocity_gen]
        self.__global_gens = [self.__heatmap_gen]
