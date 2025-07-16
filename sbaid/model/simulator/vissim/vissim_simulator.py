"""This module contains the VissimCrossSection class."""
from gi.repository import GObject, Gio

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.simulation.input import Input
from sbaid.common.coordinate import Coordinate
from sbaid.model.simulation.display import Display
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection


class VissimSimulator(Simulator):
    """TODO"""

    _type: SimulatorType
    _cross_sections: Gio.ListModel

    def __init__(self) -> None:
        self._type = SimulatorType("com.ptvgroup.vissim", "PTV Vissim")
        self._cross_sections = Gio.ListStore.new(SimulatorCrossSection)

    @GObject.Property(type=SimulatorType)
    def type(self) -> SimulatorType:
        """
        Returns the simulator type, in this case PTV Vissim.
        :return: the type of this simulator
        """
        return self._type

    @GObject.Property(type=Gio.ListModel)
    def cross_sections(self) -> Gio.ListModel:
        """
        Returns a Gio.ListModel containing the cross sections in this simulator file.
        Returns an empty model if no file was loaded yet. The model is guaranteed to be
        the same over the lifetime of this.
        :return: A Gio.ListModel containing the cross sections in this simulator file.
        """
        return self._cross_sections

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
