"""This module contains the DummySimulator class."""
from gi.repository import GObject, Gio

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.simulation.input import Input
from sbaid.common.coordinate import Coordinate
from sbaid.model.simulation.display import Display
from sbaid.common.cross_section_type import CrossSectionType


class DummySimulator(Simulator):
    """TODO"""

    @GObject.Property(type=SimulatorType)
    def type(self) -> SimulatorType:
        """TODO"""
        return None

    @GObject.Property(type=Gio.ListModel)
    def cross_sections(self) -> Gio.ListModel:
        """TODO"""
        return None

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
