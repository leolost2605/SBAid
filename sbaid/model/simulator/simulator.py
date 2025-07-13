"""
This module contains the abstract Simulator class
which provides interfaces for loading files, cross section modification,
and runtime simulation operations.
"""
from abc import ABC, abstractmethod
from gi.repository import GObject, Gio
from sbaid.common.simulator_type import SimulatorType
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.coordinate import Coordinate
from sbaid.model.simulation.input import Input
from sbaid.model.simulation.display import Display


class Simulator(GObject.GObject, ABC):
    """TODO"""
    type = GObject.Property(type=SimulatorType, flags=GObject.ParamFlags.READABLE |
    GObject.ParamFlags.WRITABLE | GObject.ParamFlags.CONSTRUCT_ONLY)
    cross_sections = GObject.Property(type=Gio.ListModel, flags=GObject.ParamFlags.READABLE |
    GObject.ParamFlags.WRITABLE | GObject.ParamFlags.CONSTRUCT_ONLY)
    """This abstract class represents a simulator."""

    @abstractmethod
    def load_file(self, file: Gio.File) -> None:
        """Load the simulation file."""

    @abstractmethod
    def create_cross_section(self, coordinate: Coordinate,
                             cross_section_type: CrossSectionType) -> int:
        """
        Create a cross section object, add it to the cross section list
        and return its position within the list
        """

    @abstractmethod
    def remove_cross_section(self, cross_section_id: str) -> None:
        """Remove the cross section object."""

    @abstractmethod
    def move_cross_section(self, cross_section_id: str,
    new_coordinate: Coordinate) -> None:
        """Move the cross section object."""

    @abstractmethod
    def init_simulation(self) -> (int, int):
        """
        Initialize the simulation object. Return the internal simulation start time
        and runtime.
        """
        # TODO GLib.TimeSpan is an alias for int in PyGObject, is this a problem?

    @abstractmethod
    def continue_simulation(self, span: int) -> None:
        """
        Simulate the given timespan. If the timespan surpasses the simulation length
        only simulate until the end of the simulation length.
        """

    @abstractmethod
    def measure(self) -> Input:
        """Collect measurement data, return as an Input object."""

    @abstractmethod
    def set_display(self, display: Display) -> None:
        """Set the display."""

    @abstractmethod
    def stop_simulation(self) -> None:
        """Stop the simulation."""
