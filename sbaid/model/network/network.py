"""This module contains the Network class and exceptions related to cross section importing."""

import asyncio
from gi.events import GLibEventLoopPolicy
from gi.repository import Gio, GObject, Gtk, GLib
from sbaid.common import list_model_iterator
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator import Simulator
from sbaid.common.location import Location
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.model.network.route import Route
from sbaid.model.network.parser_factory import ParserFactory
from sbaid.model.network.cross_section import CrossSection
from sbaid.model.database.project_database import ProjectDatabase


class Network(GObject.Object):
    """This class represents a network, consisting of the route and the cross sections on it."""
    cross_sections: Gio.ListModel = GObject.Property(type=Gio.ListModel,
                                      flags=GObject.ParamFlags.READABLE |
                                      GObject.ParamFlags.WRITABLE |
                                      GObject.ParamFlags.CONSTRUCT_ONLY)
    route: Route = GObject.Property(type=Route,
                             flags=GObject.ParamFlags.READABLE |
                             GObject.ParamFlags.WRITABLE |
                             GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, simulator: Simulator, project_db: ProjectDatabase) -> None:
        """Constructs a Network."""
        self.simulator = simulator
        self.__project_db = project_db
        super().__init__(cross_sections=Gtk.MapListModel.new(simulator.cross_sections,
                         self.__map_func, self), route=Gio.ListStore())

    def load(self) -> None:
        """Loads the network from the database."""
        self.cross_sections = self.simulator.cross_sections
        for sim_cross_section in list_model_iterator(self.cross_sections):
            model_cross_section = self.__map_func(sim_cross_section)
            model_cross_section.load_from_db()
            self.cross_sections.append(model_cross_section)

    async def import_from_file(self, file: Gio.File) -> tuple[int, int]:
        """Parses the given file and creates the cross sections defined in it."""
        factory = ParserFactory()
        parser_for_file = factory.get_parser(file)
        if not parser_for_file:
            raise NoSuitableParserException()
        import_result = await (parser_for_file.
                               foreach_cross_section(file,
                                                     self.__successful_cross_section_creation))
        return import_result

    async def __successful_cross_section_creation(self, name: str, location: Location,
                                                  cross_section_type: CrossSectionType) -> bool:
        try:
            await self.create_cross_section(name, location, cross_section_type)
            return True
        except FailedCrossSectionCreationException:
            return False

    async def create_cross_section(self, name: str, location: Location,
                                   cs_type: CrossSectionType) -> None:
        """Checks if the received cross section can be added to the Network
        and how it is to be added. Creates a combined cross section if the preexisting & incoming
        cross sections can be combined (of types DISPLAY-MEASURING or MEASURING-DISPLAY)."""
        compatible_tuple = self.__cross_sections_compatible(location, cs_type)
        if compatible_tuple[0] is not None:  # cross section can be added
            if compatible_tuple[1]:  # cross section can be added by combination
                existing_cross_section = compatible_tuple[2]
                assert isinstance(existing_cross_section, CrossSection)
                await self.delete_cross_section(existing_cross_section.id)
                position = await self.simulator.create_cross_section(location,
                                                                     CrossSectionType.COMBINED)
                network_cross_section = self.cross_sections.get_item(position)
                network_cross_section.set_name(name + existing_cross_section.name)
            else:  # cross section can be added without combination
                try:
                    position = await self.simulator.create_cross_section(location, cs_type)
                except Exception as exc:  # TODO: catch simulator exception for this
                    raise FailedCrossSectionCreationException() from exc
                network_cross_section = self.cross_sections.get_item(position)
                network_cross_section.set_name(name)
        else:  # cross section cannot be added
            raise FailedCrossSectionCreationException()

    async def delete_cross_section(self, cs_id: str) -> None:
        """Deletes a cross section by calling the simulator's remove_cross_section method."""
        await self.simulator.remove_cross_section(cs_id)

    async def move_cross_section(self, cs_id: str, new_coordinates: Location) -> None:
        """Calls the simulator's move_cross_section method, updating the simulator's
        cross section's location, automatically updating it for the network's cross section."""
        await self.simulator.move_cross_section(cs_id, new_coordinates)

    def __cross_sections_compatible(self, location: Location,
                                    incoming_cross_section_type: CrossSectionType)\
            -> tuple[bool, bool, CrossSection | None]:
        """Checks if the incoming cross section can be added, and if so if it can be added by
        itself or if it must be combined with a preexisting one. Returns a tuple with 3 elements:
        - bool: the cross section can be added,
        - bool: the cross section is to be added through combination or if the location was valid,
        - cross section | None: the cross section in a 25m radius of the incoming one, or None"""
        clashing_cross_section = self.__get_cross_section_in_radius(location)
        if clashing_cross_section is not None:
            if ((clashing_cross_section.type.value == 1 and incoming_cross_section_type.value == 2)
                    or (clashing_cross_section.type.value == 2
                        and incoming_cross_section_type.value == 1)):
                # another cross section in a 25m radius, cross section can be added by combination
                return True, True, clashing_cross_section
            # another cross section in a 25m radius, cross sections cannot be combined
            return False, False, None
        # no other cross section in a 25m radius, cross section can be added without combination
        return True, False, None

    def __get_cross_section_in_radius(self, location: Location) -> CrossSection | None:
        for cross_section in list_model_iterator(self.cross_sections):
            assert isinstance(cross_section, CrossSection)
            if cross_section.location.distance(location) <= 25:
                return cross_section
        return None

    def __map_func(self, sim_cross_section: SimulatorCrossSection) -> CrossSection:
        """Creates a new network cross section from the given simulator cross section,
        to be mapped to the given simulator cross section in the MapListModel.
        Starts the loading of cross section metadata form the database."""
        model_cross_section = CrossSection(sim_cross_section, self.__project_db)
        asyncio.set_event_loop_policy(GLib.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._load_cross_section_from_db(model_cross_section))
        loop.run_until_complete(task)
        return model_cross_section

    async def _load_cross_section_from_db(self, model_cross_section: CrossSection) -> None:
        model_cross_section.load_from_db()


class FailedCrossSectionCreationException(Exception):
    """Exception raised when the creation of a cross section fails.
    No error message needed as the exception doesn't show up to the user as an error."""


class NoSuitableParserException(Exception):
    """Exception raised when a file SBAid has no parser for is input."""
    def __init__(self) -> None:
        self.message = "Input file format not supported by SBAid."
