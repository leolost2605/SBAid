from gi.repository import GObject, Gio, GLib
import random
from sbaid.common.simulator_type import SimulatorType
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location
from tests.MockCrossSection import MockCrossSection
from sbaid.common import list_model_iterator
from sbaid.model.simulator.simulator import Simulator


class MockSimulator(Simulator):
    """Mocks a Simulator, for testing purposes."""

    __type: SimulatorType
    __route: Gio.ListStore
    __cross_sections: Gio.ListStore


    @Simulator.type.getter  # type: ignore
    def type(self) -> SimulatorType:
        """
        Returns the simulator type, in this case PTV Vissim.
        :return: the type of this simulator
        """
        return self.__type

    @Simulator.route.getter  # type: ignore
    def route(self) -> Gio.ListModel:
        """
        Returns the route of this simulation file as a list of locations.
        :return: The route as a listmodel of locations
        """
        return self.__route

    @Simulator.cross_sections.getter  # type: ignore
    def cross_sections(self) -> Gio.ListModel:
        """
        Returns a Gio.ListModel containing the cross sections in this simulator file.
        Returns an empty model if no file was loaded yet. The model is guaranteed to be
        the same over the lifetime of this.
        :return: A Gio.ListModel containing the cross sections in this simulator file.
        """
        return self.__cross_sections

    def __init__(self):
        super().__init__()
        self.__cross_sections.append(MockCrossSection("id", "cross_section_0",
                                                      CrossSectionType.COMBINED, Location(0, 0), 4))
        self.__cross_sections.append(MockCrossSection("id", "cross_section_1",
                                                      CrossSectionType.COMBINED, Location(5.7389, 7.3859), 10))

    async def create_cross_section(self, location: Location,
                                   cross_section_type: CrossSectionType) -> int:
        """
        Create a cross section object, add it to the cross section list
        and return its location within the list
        """
        cs_id = GLib.uuid_string_random()
        name = "test_name"
        lanes = 4
        self.__cross_sections.append(MockCrossSection(cs_id, name, cross_section_type, location, lanes))
        return self.__cross_sections.get_n_items() - 1

    async def remove_cross_section(self, cross_section_id: str) -> None:
        """Remove the cross section object."""
        for i, cross_section in enumerate(list_model_iterator(self.__cross_sections)):
            assert(isinstance(cross_section, MockCrossSection))
            if cross_section.id == cross_section_id:
                self.__cross_sections.remove(i)

    async def move_cross_section(self, cross_section_id: str,
                                 new_location: Location) -> None:
        """Move the cross section object to any given location. Does not check if location is on the route."""
        for i, cross_section in enumerate(list_model_iterator(self.__cross_sections)):
            assert(isinstance(cross_section, MockCrossSection))
            if cross_section.id == cross_section_id:
                cross_section.location = new_location
