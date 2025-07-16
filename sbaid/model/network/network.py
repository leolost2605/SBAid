"""TODO"""

from gi.repository import Gio, GObject, Gtk
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.common.coordinate import Coordinate
from sbaid.model.network.route import Route
from sbaid.model.network.parser_factory import ParserFactory
from sbaid.model.network.cross_section import CrossSection


class Network(GObject.Object):
    """TODO"""
    cross_sections = GObject.Property(type=Gio.ListModel,
                                      flags=GObject.ParamFlags.READABLE |
                                      GObject.ParamFlags.WRITABLE |
                                      GObject.ParamFlags.CONSTRUCT_ONLY)
    route = GObject.Property(type=Route,
                             flags=GObject.ParamFlags.READABLE |
                             GObject.ParamFlags.WRITABLE |
                             GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, simulator: Simulator) -> None:
        """TODO"""
        self.simulator = simulator
        super().__init__(cross_sections = Gtk.MapListModel(simulator.cross_sections,
                       self.__map_func(SimulatorCrossSection), self), route = Gio.ListStore())

    def load(self) -> None:
        """TODO"""

    def import_from_file(self, file: Gio.File) -> tuple[int, int]:
        """TODO:
        - parse the file, call the create cross section method ??
        """
        parser_for_file = ParserFactory().get_parser(file)
        #parser_for_file.foreach_cross_section(self, self.create_cross_section())

        return None

    def create_cross_section(self, name: str, coordinates: Coordinate,
                             cs_type: CrossSectionType) -> None:
        """TODO:
        - create_cross_section aufrufen in simulator
        - cross section muss nicht extra zum ListModel hier hinzugefügt werden,
            wird in Simulator geadded und propagated weil listmodels
        - extra daten in datenbank speichern (mit set_name gemacht)
        """
        if not self.__cross_section_location_exists(coordinates):  # if cross section input is valid
            position = self.simulator.create_cross_section(coordinates, cs_type)
            network_cross_section = self.cross_sections.get_item(position)
            network_cross_section.set_name(name)

    def delete_cross_section(self, cs_id: str) -> None:
        """TODO"""

    def move_cross_section(self, cs_id: str, new_coordinates: Coordinate) -> None:
        """TODO"""

    def __foreach_func(self, name: str, coordinates: Coordinate, cross_section: CrossSectionType) -> bool:
        """TODO:
        - creates a new cross section and handles exceptions:
            - already existing location
            - already existing name
        """

    def __cross_section_location_exists(self, coordinate: Coordinate) -> bool:
        """to be used in the create_cross_section method bcs has to be checked for imports and non-import adding to network"""
        for CrossSection in self.cross_sections:
            if CrossSection.coordinate == coordinate:
                return True
        return False

    def __map_func(self, sim_cross_section: SimulatorCrossSection) -> CrossSection | None:
        # mappt simulatorCrossSections zu network cross sections
        for cross_section in self.cross_sections:
            if cross_section.id == sim_cross_section.id:
                return cross_section
        return None
