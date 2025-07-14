"""TODO"""
from gi.repository import GObject
from model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.common.coordinate import Coordinate
from sbaid.common import CrossSectionType


class CrossSection:
    """TODO"""

    cs_id = GObject.Property(type=str,
                             flags=GObject.ParamFlags.READABLE |
                             GObject.ParamFlags.WRITABLE |
                             GObject.ParamFlags.CONSTRUCT_ONLY)
    cs_name = GObject.Property(type=str,
                               flags=GObject.ParamFlags.READABLE |
                               GObject.ParamFlags.WRITABLE |
                               GObject.ParamFlags.CONSTRUCT_ONLY)
    position = GObject.Property(type=Coordinate,
                                flags=GObject.ParamFlags.READABLE |
                                GObject.ParamFlags.WRITABLE |
                                GObject.ParamFlags.CONSTRUCT)
    cs_type = GObject.Property(type=CrossSectionType,
                               flags=GObject.ParamFlags.READABLE |
                               GObject.ParamFlags.WRITABLE |
                               GObject.ParamFlags.CONSTRUCT_ONLY)
    lanes = GObject.Property(type=int,
                             flags=GObject.ParamFlags.READABLE |
                             GObject.ParamFlags.WRITABLE |
                             GObject.ParamFlags.CONSTRUCT)
    hard_shoulder_available = GObject.Property(type=bool,
                                               flags=GObject.ParamFlags.READABLE |
                                               GObject.ParamFlags.WRITABLE |
                                               GObject.ParamFlags.CONSTRUCT)
    hard_shoulder_active = GObject.Property(type=bool,
                                            flags=GObject.ParamFlags.READABLE |
                                            GObject.ParamFlags.WRITABLE |
                                            GObject.ParamFlags.CONSTRUCT)
    b_display_active = GObject.Property(type=bool,
                                        flags=GObject.ParamFlags.READABLE |
                                        GObject.ParamFlags.WRITABLE |
                                        GObject.ParamFlags.CONSTRUCT)

    def __init__(self, simulator_cross_section: SimulatorCrossSection):
        self.cs_id: str
        self.cs_name: str
        self.position: Coordinate
        self.cs_type: CrossSectionType
        self.lanes: int
        self.hard_shoulder_available: bool
        self.hard_shoulder_active: bool
        self.b_display_active: bool

    def load_from_db(self):
        """TODO"""
