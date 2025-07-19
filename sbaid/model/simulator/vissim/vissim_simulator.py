"""This module contains the VissimCrossSection class."""
from threading import Thread

from gi.repository import GObject, Gio

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.simulation.input import Input
from sbaid.common.coordinate import Coordinate
from sbaid.model.simulation.display import Display
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.model.simulator.vissim.vissim import CommandQueue, VissimConnector


class VissimSimulator(Simulator):
    """TODO"""

    __type: SimulatorType
    __cross_sections: Gio.ListModel
    __command_queue: CommandQueue
    __thread: Thread

    def __init__(self) -> None:
        self.__type = SimulatorType("com.ptvgroup.vissim", "PTV Vissim")
        self.__cross_sections = Gio.ListStore.new(SimulatorCrossSection)
        self.__command_queue = CommandQueue()

        self.__thread = Thread(target=VissimConnector, args=(self.__command_queue,), daemon=True)
        self.__thread.start()

    @GObject.Property(type=SimulatorType)
    def type(self) -> SimulatorType:
        """
        Returns the simulator type, in this case PTV Vissim.
        :return: the type of this simulator
        """
        return self.__type

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
        """TODO"""

    async def create_cross_section(self, coordinate: Coordinate,
                                   cross_section_type: CrossSectionType) -> int:
        """TODO"""
        return 0

    async def remove_cross_section(self, cross_section_id: str) -> None:
        """TODO"""

    async def move_cross_section(self, cross_section_id: str, new_position: Coordinate) -> None:
        """TODO"""

    async def init_simulation(self) -> tuple[int, int]:
        return 0, 0

    async def continue_simulation(self, span: int) -> None:
        """TODO"""

    async def measure(self) -> Input:
        return None

    async def set_display(self, display: Display) -> None:
        """TODO"""

    async def stop_simulation(self) -> None:
        """TODO"""
