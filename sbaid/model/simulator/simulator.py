# mypy: disable-error-code="empty-body"
"""
This module contains the abstract Simulator class
which provides interfaces for loading files, cross section modification,
and runtime simulation operations.
"""
from gi.repository import GObject, Gio, GLib

from sbaid.common.simulator_type import SimulatorType
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location
from sbaid.model.simulation.input import Input
from sbaid.model.simulation.display import Display


class Simulator(GObject.GObject):
    """TODO"""

    type: SimulatorType = GObject.Property(type=SimulatorType,  # type: ignore
                                           flags=GObject.ParamFlags.READABLE)

    route: Gio.ListModel = GObject.Property(type=Gio.ListModel,  # type: ignore
                                            flags=GObject.ParamFlags.READABLE)

    cross_sections: Gio.ListModel = GObject.Property(type=Gio.ListModel,  # type: ignore
                                                     flags=GObject.ParamFlags.READABLE)

    async def load_file(self, file: Gio.File) -> None:
        """Load the simulation file."""

    async def create_cross_section(self, location: Location,
                                   cross_section_type: CrossSectionType) -> int:
        """
        Create a cross section object, add it to the cross section list
        and return its location within the list
        """

    async def remove_cross_section(self, cross_section_id: str) -> None:
        """Remove the cross section object."""

    async def move_cross_section(self, cross_section_id: str,
                                 new_location: Location) -> None:
        """Move the cross section object."""

    async def init_simulation(self) -> tuple[GLib.DateTime, int]:
        """
        Initialize the simulation object. Return the internal simulation start time
        and runtime.
        """
        # TODO GLib.TimeSpan is an alias for int in PyGObject, is this a problem?

    async def continue_simulation(self, span: int) -> None:
        """
        Simulate the given timespan. If the timespan surpasses the simulation length
        only simulate until the end of the simulation length.
        """

    async def measure(self) -> Input:
        """Collect measurement data, return as an Input object."""

    async def set_display(self, display: Display) -> None:
        """Set the display."""

    async def stop_simulation(self) -> None:
        """Stop the simulation."""
