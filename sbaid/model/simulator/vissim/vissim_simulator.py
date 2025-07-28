"""This module contains the VissimCrossSection class."""
from gi.repository import GObject, Gio

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

    def __init__(self) -> None:
        self.__type = SimulatorType("com.ptvgroup.vissim", "PTV Vissim")
        self.__route = Gio.ListStore.new(Location)
        self.__cross_sections = Gio.ListStore.new(VissimCrossSection)
        self.__connector = VissimConnector()

    @GObject.Property(type=SimulatorType)
    def type(self) -> SimulatorType:
        """
        Returns the simulator type, in this case PTV Vissim.
        :return: the type of this simulator
        """
        return self.__type

    @GObject.Property(type=Gio.ListModel)
    def route(self):
        """TODO"""
        return self.__route

    @GObject.Property(type=Gio.ListModel)
    def cross_sections(self) -> Gio.ListModel:
        """
        Returns a Gio.ListModel containing the cross sections in this simulator file.
        Returns an empty model if no file was loaded yet. The model is guaranteed to be
        the same over the lifetime of this.
        :return: A Gio.ListModel containing the cross sections in this simulator file.
        """
        return self.__cross_sections

    async def load_file(self, file: Gio.File) -> None:
        route, cross_sections = await self.__connector.load_file(file.get_path())

        for coord in route:
            self.__route.append(coord)

        for cs in cross_sections:
            self.__cross_sections.append(VissimCrossSection(cs))

    async def create_cross_section(self, location: Location,
                                   cross_section_type: CrossSectionType) -> int:
        """TODO"""
        new_cs_state = await self.__connector.create_cross_section(location, cross_section_type)
        self.__cross_sections.append(VissimCrossSection(new_cs_state))
        return self.__cross_sections.get_n_items() - 1

    async def remove_cross_section(self, cross_section_id: str) -> None:
        """TODO"""
        #TODO: Remove from store
        await self.__connector.remove_cross_section(cross_section_id)

    async def move_cross_section(self, cross_section_id: str, new_position: Location) -> None:
        """TODO"""
        new_cs_state = await self.__connector.move_cross_section(cross_section_id, new_position)
        # TODO: update state

    async def init_simulation(self) -> tuple[int, int]:
        """TODO"""
        return await self.__connector.init_simulation(60)

    async def continue_simulation(self, span: int) -> None:
        """TODO"""
        await self.__connector.continue_simulation(span)

    async def measure(self) -> Input:
        """TODO"""
        return await self.__connector.measure()

    async def set_display(self, display: Display) -> None:
        """TODO"""
        await self.__connector.set_display(display)

    async def stop_simulation(self) -> None:
        """TODO"""
        await self.__connector.stop_simulation()
