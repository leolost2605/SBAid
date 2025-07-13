"""This module contains the DummySimulator class."""
from gi.repository import Gio

from sbaid.model.simulator.simulator import Simulator
from sbaid.model.simulation.input import Input
from sbaid.common.coordinate import Coordinate
from sbaid.model.simulation.display import Display
from sbaid.common.cross_section_type import CrossSectionType


class DummySimulator(Simulator):
    """TODO"""
    def load_file(self, file: Gio.File) -> None:
        """TODO"""

    def create_cross_section(self, coordinate: Coordinate,
    cross_section_type: CrossSectionType) -> None:
        """TODO"""

    def remove_cross_section(self, cross_section_id: str) -> None:
        """TODO"""

    def move_cross_section(self, cross_section_id: str, new_position: Coordinate) -> None:
        """TODO"""

    def init_simulation(self):
        return 0,0

    def continue_simulation(self, span: int) -> None:
        """TODO"""

    def measure(self) -> Input:
        return None

    def set_display(self, display: Display) -> None:
        """TODO"""

    def stop_simulation(self) -> None:
        """TODO"""
