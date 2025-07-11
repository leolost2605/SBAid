"""
This module contains the abstract Simulator class
which provides interfaces for loading files, cross section modification,
and runtime simulation operations.
"""
from gi.repository import Gio
from abc import ABC, abstractmethod
import datetime
from sbaid.common.simulator_type import SimulatorType
from sbaid.common.cross_section_type import CrossSectionType
from ..simulation import Input, Display


class Simulator(ABC):
    """This abstract class represents a simulator."""
    def __init__(self, simulator_type: SimulatorType):
        """Initialize the simulator object."""
        self.simulator_type = simulator_type

    @abstractmethod
    def load_file(self, file: Gio.File) -> None:
        """Load the simulation file."""
        pass

    @abstractmethod
    def create_cross_section(self, coordinates: "TODO",
                             cross_section_type: CrossSectionType) -> int:
        """
        Create a cross section object, add it to the cross section list
        and return its position within the list
        """
        # returns position of the new cross section
        return 0

    @abstractmethod
    def remove_cross_section(self, cross_section_id: str) -> None:
        """Remove the cross section object."""
        pass

    @abstractmethod
    def move_cross_section(self, cross_section_id: str, new_coordinates: "TODO") -> None:
        """Move the cross section object."""
        pass

    @abstractmethod
    def init_simulation(self) -> (datetime.datetime, datetime.timedelta):
        """
        Initialize the simulation object. Return the internal simulation start time
        and runtime.
        """
        # TODO timedelta instead of .NET TimeSpan
        #  (see https://pypi.org/project/timespan/ and
        #  https://docs.python.org/3/library/datetime.html#timedelta-objects)
        pass

    @abstractmethod
    def continue_simulation(self, span: datetime.timedelta) -> None:
        """
        Simulate the given timespan. If the timespan surpasses the simulation length
        only simulate until the end of the simulation length.
        """
        pass

    @abstractmethod
    def measure(self) -> Input:
        """Collect measurement data, return as an Input object."""
        return None

    @abstractmethod
    def set_display(self, display: Display) -> None:
        """Set the display."""
        pass

    @abstractmethod
    def stop_simulation(self) -> None:
        """Stop the simulation."""
        pass
