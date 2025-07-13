"""
This module contains the abstract SimulatorCrossSection class
which provides cross section GObject properties.
"""
from abc import ABC
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.coordinate import Coordinate

from gi.repository import GObject, Shumate



class SimulatorCrossSection(GObject.GObject, ABC):
    """
    This class is used as a wrapper for a cross section within the simulator
    that contains several properties about the cross section.
    """
    # GObject.Property definitions
    simulator_cross_section_id = GObject.Property(type=str,
    flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
    GObject.ParamFlags.CONSTRUCT_ONLY)
    simulator_cross_section_type = GObject.Property(
    type=CrossSectionType,
    flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
    GObject.ParamFlags.CONSTRUCT_ONLY)
    position = GObject.Property(type=Coordinate,
    flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
    GObject.ParamFlags.CONSTRUCT)
    lanes = GObject.Property(type=int, default=1,
    flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
    GObject.ParamFlags.CONSTRUCT)
    hard_shoulder_available = GObject.Property(type=bool, default=False,
    flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
    GObject.ParamFlags.CONSTRUCT)
    hard_shoulder_active = GObject.Property(type=bool, default=False,
    flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
    GObject.ParamFlags.CONSTRUCT)
    b_display_active = GObject.Property(type=bool, default=False,
    flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
    GObject.ParamFlags.CONSTRUCT)

    def __init__(self, simulator_cross_section_id: str, position: Coordinate,
                 simulator_cross_section_type: CrossSectionType, lanes: int,
    hard_shoulder_available: bool, hard_shoulder_active: bool,
                 b_display_active: bool) -> None:
        """TODO"""
        super().__init__(simulator_cross_section_id = simulator_cross_section_id,
        position = position, simulator_cross_section_type = simulator_cross_section_type,
        lanes = lanes, hard_shoulder_available = hard_shoulder_available,
        hard_shoulder_active = hard_shoulder_active, b_display_active = b_display_active)
