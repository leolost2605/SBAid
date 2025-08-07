"""This module defines the DiagramExporter class"""
from gi.repository import Gio, GObject
from sbaid.common.image import Image
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
    __diagram_types: Gio.ListStore

    # GObject.Property definitions
    available_diagram_types: Gio.ListModel = (
        GObject.Property(type=Gio.ListModel))  # type: ignore[assignment]

    @available_diagram_types.getter  # type: ignore
    def available_diagram_types(self) -> Gio.ListModel:
        """Returns ListModel of available diagram types"""
        return self.__diagram_types

    def __init__(self) -> None:
        """Initialize the diagram exporter"""
        super().__init__()
        self.__diagram_types = Gio.ListStore.new(DiagramType)
        self.__add_available_types()

    def get_diagram(self, result: Result, cross_section_ids: list[str],
                    image_format: ImageFormat, diagram_type: DiagramType) -> Image | None:
        """Attempts to generate a diagram based on the provided diagram type."""

        type_id = diagram_type.diagram_type_id

        for global_gen in self.__global_gens:
            gen_type_id = global_gen.get_diagram_type().diagram_type_id
            if type_id == gen_type_id:
                return global_gen.get_diagram(result, cross_section_ids, image_format)

        for cs_gen in self.__cross_section_gens:
            gen_type_id = cs_gen.get_diagram_type().diagram_type_id
            if type_id == gen_type_id:
                return cs_gen.get_diagram(result, cross_section_ids[0], image_format)

        return None

    def __add_available_types(self) -> None:
        """Gets available diagram types and initialize references"""
        heatmap_gen = HeatmapGenerator()
        self.__diagram_types.append(heatmap_gen.get_diagram_type())
        qv_gen = QVGenerator()
        self.__diagram_types.append(qv_gen.get_diagram_type())
        # display_gen = DisplayGenerator()
        # self.__diagram_types.append(display_gen.get_diagram_type())
        velocity_gen = VelocityGenerator()
        self.__diagram_types.append(velocity_gen.get_diagram_type())

        self.__cross_section_gens = [qv_gen, velocity_gen]
        self.__global_gens = [heatmap_gen]
