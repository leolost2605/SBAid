"""TODO"""
from gi.repository import GObject
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.common.coordinate import Coordinate
from sbaid.common.cross_section_type import CrossSectionType


class CrossSection(GObject.GObject):
    """TODO"""

    id = GObject.Property(type=str,
                          flags=GObject.ParamFlags.READABLE |
                          GObject.ParamFlags.WRITABLE |
                          GObject.ParamFlags.CONSTRUCT_ONLY)
    name = GObject.Property(type=str,
                            flags=GObject.ParamFlags.READABLE |
                            GObject.ParamFlags.WRITABLE |
                            GObject.ParamFlags.CONSTRUCT_ONLY)
    position = GObject.Property(type=Coordinate,
                                flags=GObject.ParamFlags.READABLE |
                                GObject.ParamFlags.WRITABLE |
                                GObject.ParamFlags.CONSTRUCT_ONLY)
    type = GObject.Property(type=CrossSectionType, default=CrossSectionType.COMBINED,
                            flags=GObject.ParamFlags.READABLE |
                            GObject.ParamFlags.WRITABLE |
                            GObject.ParamFlags.CONSTRUCT_ONLY)
    lanes = GObject.Property(type=int,
                             flags=GObject.ParamFlags.READABLE |
                             GObject.ParamFlags.WRITABLE |
                             GObject.ParamFlags.CONSTRUCT_ONLY)
    hard_shoulder_available = GObject.Property(type=bool, default=False,
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
        """TODO"""

    def load_from_db(self) -> None:
        """TODO"""
