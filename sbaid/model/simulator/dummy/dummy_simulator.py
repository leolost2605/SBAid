"""This module contains the DummySimulator class."""
from gi.repository import Gio

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.simulation.input import Input
from sbaid.common.location import Location
from sbaid.model.simulation.display import Display
from sbaid.common.cross_section_type import CrossSectionType


class DummySimulator(Simulator):
    """TODO"""

    @Simulator.type.getter  # type: ignore
    def type(self) -> SimulatorType:
        """TODO"""
        return None

    @Simulator.route.getter  # type: ignore
    def route(self) -> Gio.ListModel:
        """TODO"""
        return None

    @Simulator.cross_sections.getter  # type: ignore
    def cross_sections(self) -> Gio.ListModel:
        """TODO"""
        return None

    async def load_file(self, file: Gio.File) -> None:
        """TODO"""

    async def create_cross_section(self, location: Location,
                                   cross_section_type: CrossSectionType) -> int:
        """TODO"""
        return 0

    async def remove_cross_section(self, cross_section_id: str) -> None:
        """TODO"""

    async def move_cross_section(self, cross_section_id: str, new_location: Location) -> None:
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
