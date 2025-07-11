"""
This module contains the abstract SimulatorCrossSection class
which provides cross section GObject properties.
"""
from gi.repository import GObject
from sbaid.common import cross_section_type
from abc import ABC


class SimulatorCrossSection(GObject.GObject, ABC):
    """
    This class is used as a wrapper for a cross section within the simulator
    that contains several properties about the cross section.
    """
    # GObject.Property definitions
    simulator_cross_section_id = GObject.Property(type=str, default = "")
    position = GObject.Property(type="TODO", default=None)
    simulator_cross_section_type = GObject.Property(
        type=cross_section_type, default="")
    lanes = GObject.Property(type=int, default=1)
    hard_shoulder_available = GObject.Property(type=bool, default=False)
    hard_shoulder_active = GObject.Property(type=bool, default=False)
    b_display_active = GObject.Property(type=bool, default=False)

    def __init__(self, simulator_cross_section_id: str, position: "TODO",
                 simulator_cross_section_type: cross_section_type, lanes: int,
    hard_shoulder_available: bool, hard_shoulder_active: bool,
                 b_display_active: bool) -> None:
        """Initialize the cross section object."""
        self.simulator_cross_section_id = simulator_cross_section_id
        self.position = position
        self.simulator_cross_section_type = simulator_cross_section_type
        self.lanes = lanes
        self.hard_shoulder_available = hard_shoulder_available
        self.hard_shoulder_active = hard_shoulder_active
        self.b_display_active = b_display_active
