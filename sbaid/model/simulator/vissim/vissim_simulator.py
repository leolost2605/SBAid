"""This module contains the VissimCrossSection class."""
from gi.repository import GObject, Gio

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.simulation.input import Input
from sbaid.common.coordinate import Coordinate
from sbaid.model.simulation.display import Display
from sbaid.common.cross_section_type import CrossSectionType


class VissimSimulator(Simulator):
    """TODO"""

    @GObject.Property(type=SimulatorType)
    def type(self) -> SimulatorType:
        """TODO"""
        return None

    @GObject.Property(type=Gio.ListModel)
    def cross_sections(self) -> Gio.ListModel:
        """TODO"""
        return None

    def load_file(self, file: Gio.File) -> None:
        """TODO"""

    def create_cross_section(self, coordinate: Coordinate,
                             cross_section_type: CrossSectionType) -> int:
        """TODO"""
        return 0

    def remove_cross_section(self, cross_section_id: str) -> None:
        """TODO"""

    def move_cross_section(self, cross_section_id: str, new_position: Coordinate) -> None:
        """TODO"""

    def init_simulation(self) -> tuple[int, int]:
        return 0, 0

    def continue_simulation(self, span: int) -> None:
        """TODO"""

    def measure(self) -> Input:
        return None

    def set_display(self, display: Display) -> None:
        """TODO"""

    def stop_simulation(self) -> None:
        """TODO"""
