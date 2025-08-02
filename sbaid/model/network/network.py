"""This module contains the Network class and exceptions related to cross section importing."""

import sys
import asyncio
import typing
import gi
from sbaid.common import list_model_iterator
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator import Simulator
from sbaid.common.location import Location
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.model.network.route import Route
from sbaid.model.network.parser_factory import ParserFactory
from sbaid.model.network.cross_section import CrossSection
from sbaid.model.database.project_database import ProjectDatabase

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import Gio, GObject, Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class Network(GObject.Object):
    """This class represents a network, consisting of the route and the cross sections on it."""

    cross_sections: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore[assignment]

    @cross_sections.getter  # type: ignore
    def cross_sections(self) -> Gio.ListModel:
        """Returns the MapListModel containing the model cross sections
        and the simulator cross sections."""
        return self.__cross_sections

    route: Route = GObject.Property(type=Route,  # type: ignore
                                    flags=GObject.ParamFlags.READABLE |
                                    GObject.ParamFlags.WRITABLE |
                                    GObject.ParamFlags.CONSTRUCT_ONLY)



    __background_tasks: set[asyncio.Task[None]]
    __cross_sections: Gtk.MapListModel

    def __init__(self, simulator: Simulator, project_db: ProjectDatabase) -> None:
        """Constructs a Network."""
        self.__simulator = simulator
        self.__project_db = project_db
        self.__background_tasks = set()
        self.__cross_sections = Gtk.MapListModel.new(None, self.__map_func)
        super().__init__(route=simulator.route)

    async def load(self) -> None:
        """Loads the network data."""
        self.__cross_sections.set_model(self.__simulator.cross_sections)

    async def import_from_file(self, file: Gio.File) -> tuple[int, int]:
        """Parses the given file and creates the cross sections defined in it."""
        factory = ParserFactory()
        parser_for_file = factory.get_parser(file)
        if not parser_for_file:
            raise NoSuitableParserException()
        return await (parser_for_file.
                      foreach_cross_section(file, self.__check_cross_section_creation_success))

    async def __check_cross_section_creation_success(self, name: str, location: Location,
                                                     cross_section_type: CrossSectionType) -> bool:
        try:
            await self.create_cross_section(name, location, cross_section_type)
            return True
        except FailedCrossSectionCreationException:
            return False

    async def create_cross_section(self, name: str, location: Location,
                                   cs_type: CrossSectionType) -> int:
        """Checks if the received cross section can be added to the Network
        and how it is to be added. Creates a combined cross section if the preexisting & incoming
        cross sections can be combined (of types DISPLAY-MEASURING or MEASURING-DISPLAY)."""
        cross_section_addable, combination_needed, clashing_cross_section \
            = self.__cross_sections_compatible(location, cs_type)
        if cross_section_addable is not None:  # cross section can be added
            if combination_needed:  # cross section can be added by combination
                existing_cross_section = clashing_cross_section
                assert isinstance(existing_cross_section, CrossSection)
                await self.delete_cross_section(existing_cross_section.id)
                position = await self.__simulator.create_cross_section(location,
                                                                       CrossSectionType.COMBINED)
                incoming_cross_section = self.cross_sections.get_item(position)
                model_cross_section = typing.cast(CrossSection, incoming_cross_section)
                model_cross_section.name = (existing_cross_section.name + "_"
                                            + model_cross_section.name)
                return position
            try:
                position = await self.__simulator.create_cross_section(location, cs_type)
            except Exception as exc:
                raise FailedCrossSectionCreationException(
                    "Cross section creation in simulator failed.") from exc
            model_cross_section = typing.cast(CrossSection,
                                              self.cross_sections.get_item(position))
            model_cross_section.name = name
            return position
        raise FailedCrossSectionCreationException()

    async def delete_cross_section(self, cs_id: str) -> None:
        """Deletes a cross section by calling the simulator's remove_cross_section method."""
        await self.__simulator.remove_cross_section(cs_id)

    async def move_cross_section(self, cs_id: str, new_coordinates: Location) -> None:
        """Calls the simulator's move_cross_section method, updating the simulator's
        cross section's location, automatically updating it for the network's cross section."""
        await self.__simulator.move_cross_section(cs_id, new_coordinates)

    def __cross_sections_compatible(self, location: Location,
                                    incoming_cross_section_type: CrossSectionType)\
            -> tuple[bool, bool, CrossSection | None]:
        """Checks if the incoming cross section can be added, and if so if it can be added by
        itself or if it must be combined with a preexisting one. Returns a tuple with 3 elements:
        - bool: the cross section can be added,
        - bool: the cross section is to be added through combination/ location was valid,
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
        task = asyncio.create_task(model_cross_section.load_from_db())
        self.__background_tasks.add(task)
        task.add_done_callback(self.__background_tasks.discard)
        return model_cross_section



class FailedCrossSectionCreationException(Exception):
    """Exception raised when the creation of a cross section fails."""


class NoSuitableParserException(Exception):
    """Exception raised when a file SBAid has no parser for is input."""
    def __init__(self) -> None:
        self.message = "Input file format not supported by SBAid."
