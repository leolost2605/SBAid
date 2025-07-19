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
                       self.__map_func(SimulatorCrossSection), self), route = Gio.ListStore())  #TODO fix simulator cross section thing

    def load(self) -> None:
        """TODO"""

    def import_from_file(self, file: Gio.File) -> tuple[int, int]:
        """TODO:
        - parse the file, call the create cross section method ??
        """
        parser_for_file = ParserFactory().get_parser(file)
        parser_for_file.foreach_cross_section(self, file, ("""???"""))  # TODO nao sei como isto funciona :'(

        return None

    def create_cross_section(self, name: str, coordinates: Coordinate,
                             cs_type: CrossSectionType) -> None:
        """Checks if the received cross section can be added to the Network
        and how it is to be added. Creates a combined cross section if the preexisting and incoming cross
        sections can be combined (of types DISPLAY-MEASURING or MEASURING-DISPLAY)."""
        compatible_tuple = self.__cross_sections_compatible(coordinates, cs_type)
        if compatible_tuple[0]:  # CS can be added
            if compatible_tuple[1]:
                existing_cross_section = compatible_tuple[2]
                self.simulator.remove_cross_section(existing_cross_section.id)
                position = self.simulator.create_cross_section(coordinates, CrossSectionType.COMBINED)
                network_cross_section = self.cross_sections.get_item(position)
                network_cross_section.set_name(name + existing_cross_section.name)
            else:
                # cross section is added without combination
                position = self.simulator.create_cross_section(coordinates, cs_type)
                network_cross_section = self.cross_sections.get_item(position)
                network_cross_section.set_name(name)

    def delete_cross_section(self, cs_id: str) -> None:
        """Deletes a cross section by calling the simulator's remove_cross_section method."""
        self.simulator.remove_cross_section(cs_id)

    def move_cross_section(self, cs_id: str, new_coordinates: Coordinate) -> None:
        """Calls the simulator's move_cross_section method, updating the simulator's
        cross section's location, automatically updating it for the network's cross section."""
        self.simulator.move_cross_section(cs_id, new_coordinates)

    def __cross_sections_compatible(self, location: Coordinate,
                                    incoming_cross_section_type: CrossSectionType)\
            -> tuple[bool, bool, CrossSection | None]:
        """Checks if the incoming cross section can be added, and if so if it can be added by
        itself or if it must be combined with a preexisting one. Accepts the combination and returns the
        preexisting cross section in the given location if one of the cross sections is of type DISPLAY and the other one MEASURING, discards the
         incoming one in any other cases."""
        clashing_cross_section = self.__get_cross_section_in_location(location)
        if clashing_cross_section:
            if ((clashing_cross_section.type.value == 1 and incoming_cross_section_type.value == 2)
                    or (clashing_cross_section.type.value == 2
                        and incoming_cross_section_type.value == 1)):
                    # location is taken, CS can be added by combination
                    return True, True, clashing_cross_section
            # location is taken, CSs cannot be combined
            return False, False, None
        # location is not taken, CS can be added without combination
        return True, False, None

    def __get_cross_section_in_location(self, coordinate: Coordinate) -> CrossSection | None:
        for cross_section in self.cross_sections:
            if cross_section.coordinate == coordinate:
                return cross_section
        return None

    def __map_func(self, sim_cross_section: SimulatorCrossSection) -> CrossSection | None:
        # maps simulator cross sections to network cross sections
        for cross_section in self.cross_sections:
            if cross_section.id == sim_cross_section.id:
                return cross_section
        return None
