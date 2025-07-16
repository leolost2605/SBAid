"""This module contains the Cross Section class. TODO"""
from gi.repository import GObject
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.common.coordinate import Coordinate
from sbaid.common.cross_section_type import CrossSectionType


class CrossSection:
    """This class defines a cross section in the network."""

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
    type = GObject.Property(type=CrossSectionType,
                            flags=GObject.ParamFlags.READABLE |
                            GObject.ParamFlags.WRITABLE |
                            GObject.ParamFlags.CONSTRUCT_ONLY,
                            default=CrossSectionType.COMBINED)
    lanes = GObject.Property(type=int,
                             flags=GObject.ParamFlags.READABLE |
                             GObject.ParamFlags.WRITABLE |
                             GObject.ParamFlags.CONSTRUCT_ONLY)
    hard_shoulder_available = GObject.Property(type=bool,
                                               flags=GObject.ParamFlags.READABLE |
                                               GObject.ParamFlags.WRITABLE |
                                               GObject.ParamFlags.CONSTRUCT_ONLY,
                                               default=False)
    hard_shoulder_active = GObject.Property(type=bool,
                                            flags=GObject.ParamFlags.READABLE |
                                            GObject.ParamFlags.WRITABLE |
                                            GObject.ParamFlags.CONSTRUCT,
                                            default=False)
    b_display_active = GObject.Property(type=bool,
                                        flags=GObject.ParamFlags.READABLE |
                                        GObject.ParamFlags.WRITABLE |
                                        GObject.ParamFlags.CONSTRUCT,
                                        default=False)

    def __init__(self, simulator_cross_section: SimulatorCrossSection) -> None:
        """TODO"""

    def load_from_db(self) -> None:
        """TODO"""

    def set_name(self, name: str) -> None:
        self.name = name
        #TODO: save name and id in database