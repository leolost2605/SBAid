"""TODO"""
from gi.repository import GObject
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.common.coordinate import Coordinate
from sbaid.common.cross_section_type import CrossSectionType


class CrossSection(GObject.GObject):
    """This class defines a cross section in the network."""

    id = GObject.Property(type=str,
                          flags=GObject.ParamFlags.READABLE |
                          GObject.ParamFlags.WRITABLE |
                          GObject.ParamFlags.CONSTRUCT_ONLY)
    name = GObject.Property(type=str,
                            flags=GObject.ParamFlags.READABLE |
                            GObject.ParamFlags.WRITABLE |
                            GObject.ParamFlags.CONSTRUCT_ONLY)
    location = GObject.Property(type=Coordinate,
                                flags=GObject.ParamFlags.READABLE |
                                GObject.ParamFlags.WRITABLE |
                                GObject.ParamFlags.CONSTRUCT_ONLY)
    type = GObject.Property(type=CrossSectionType,
                            flags=GObject.ParamFlags.READABLE |
                            GObject.ParamFlags.WRITABLE |
                            GObject.ParamFlags.CONSTRUCT_ONLY)
    lanes = GObject.Property(type=int,
                             flags=GObject.ParamFlags.READABLE |
                             GObject.ParamFlags.WRITABLE |
                             GObject.ParamFlags.CONSTRUCT_ONLY)
    hard_shoulder_available = GObject.Property(type=bool,
                                               flags=GObject.ParamFlags.READABLE |
                                               GObject.ParamFlags.WRITABLE |
                                               GObject.ParamFlags.CONSTRUCT_ONLY)
    hard_shoulder_active = GObject.Property(type=bool, default=False,
                                            flags=GObject.ParamFlags.READABLE |
                                            GObject.ParamFlags.WRITABLE |
                                            GObject.ParamFlags.CONSTRUCT)
    b_display_active = GObject.Property(type=bool, default=False,
                                        flags=GObject.ParamFlags.READABLE |
                                        GObject.ParamFlags.WRITABLE |
                                        GObject.ParamFlags.CONSTRUCT)

    def __init__(self, simulator_cross_section: SimulatorCrossSection) -> None:
        """Constructs a new cross section with the given simulator cross section data."""
        super().__init__(location=simulator_cross_section.position,
                         type=simulator_cross_section.type)

    def load_from_db(self) -> None:
        """TODO"""

    def set_name(self, name: str) -> None:
        """Sets the cross section's name."""
        self.name = name

    def toggle_hard_shoulder(self) -> None:
        """Toggles the hard shoulder status."""
        self.hard_shoulder_active = not self.hard_shoulder_active

    def toggle_b_display_active(self) -> None:
        """Toggles the b display status."""
        self.b_display_active = not self.b_display_active
