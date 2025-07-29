"""This module contains the VissimCrossSection class."""
from gi.repository import GLib, Gio

from sbaid import common
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.simulation.input import Input
from sbaid.common.location import Location
from sbaid.model.simulation.display import Display
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.vissim.vissim import VissimConnector
from sbaid.model.simulator.vissim.vissim_cross_section import VissimCrossSection


class VissimSimulator(Simulator):
    """TODO"""

    __type: SimulatorType
    __route: Gio.ListStore
    __cross_sections: Gio.ListStore
    __connector: VissimConnector

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

    def __init__(self) -> None:
        self.__type = SimulatorType("com.ptvgroup.vissim", "PTV Vissim")
        self.__route = Gio.ListStore.new(Location)
        self.__cross_sections = Gio.ListStore.new(VissimCrossSection)
        self.__connector = VissimConnector()

    async def load_file(self, file: Gio.File) -> None:
        path = file.get_path()

        if not path:
            raise FileNotFoundError("Path not found")

        route, cross_sections = await self.__connector.load_file(path)

        for coord in route:
            self.__route.append(coord)

        for cs in cross_sections:
            self.__cross_sections.append(VissimCrossSection(cs))

    async def create_cross_section(self, location: Location,
                                   cross_section_type: CrossSectionType) -> int:
        """
        Creates a new cross section at the given location with the given type if possible.
        :param location: the location of the new cross section
        :param cross_section_type: the type of the new cross section
        :return: the position of the new cross section in self.cross_sections
        """
        new_cs_state = await self.__connector.create_cross_section(location, cross_section_type)
        self.__cross_sections.append(VissimCrossSection(new_cs_state))
        return self.__cross_sections.get_n_items() - 1

    async def remove_cross_section(self, cross_section_id: str) -> None:
        """
        Removes the cross section with the given id.
        :param cross_section_id: the id of the cross section to remove
        """
        await self.__connector.remove_cross_section(cross_section_id)

        for i, cross_section in enumerate(common.list_model_iterator(self.__cross_sections)):
            if cross_section.id == cross_section_id:
                self.__cross_sections.remove(i)
                return

        assert False

    async def move_cross_section(self, cross_section_id: str, new_location: Location) -> None:
        """
        Moves the cross section with the given id to the given new location.
        :param cross_section_id: the id of the cross section to move
        :param new_location: the new location to move the cross section to
        """
        new_cs_state = await self.__connector.move_cross_section(cross_section_id, new_location)

        for cross_section in common.list_model_iterator(self.__cross_sections):
            if cross_section.id == cross_section_id:
                cross_section.set_state(new_cs_state)
                return

        assert False

    async def init_simulation(self) -> tuple[GLib.DateTime, int]:
        """
        Initializes the simulation.
        :return: the in simulation time of the simulation start and the simulation
        duration in seconds
        """
        return await self.__connector.init_simulation(60)

    async def continue_simulation(self, span: int) -> None:
        """
        Continues the simulation by specified amount of seconds.
        :param span: the amount of seconds to simulate
        """
        await self.__connector.continue_simulation(span)

    async def measure(self) -> Input:
        """
        Takes measurements in the simulation and returns the as an Input object.
        :return: the Input object containing the measurements
        """
        return await self.__connector.measure()

    async def set_display(self, display: Display) -> None:
        """
        Sets the display cross sections displays to the given values.
        :param display: information about the signs to display at the cross section
        """
        await self.__connector.set_display(display)

    async def stop_simulation(self) -> None:
        """
        Stops the simulation.
        """
        await self.__connector.stop_simulation()
