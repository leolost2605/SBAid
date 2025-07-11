from gi.repository import GObject
from sbaid.common import cross_section_type


class SimulatorCrossSection(GObject.GObject):
    # GObject.Property definitions
    id = GObject.Property(type=str, default = "")
    position = GObject.Property(type=Coordinates, default=None)
    type = GObject.Property(type=cross_section_type, default="")
    lanes = GObject.Property(type=int, default=1)
    hard_shoulder_available = GObject.Property(type=bool, default=False)
    hard_shoulder_active = GObject.Property(type=bool, default=False)
    b_display_active = GObject.Property(type=bool, default=False)

    def __init__(self, id: str, position: Coordinates, type: cross_section_type, lanes: int,
    hard_shoulder_available: bool, hard_shoulder_active: bool, b_display_active: bool) -> None:
        self.id = id
        self.position = position
        self.type = type
        self.lanes = lanes
        self.hard_shoulder_available = hard_shoulder_available
        self.hard_shoulder_active = hard_shoulder_active
        self.b_display_active = b_display_active

