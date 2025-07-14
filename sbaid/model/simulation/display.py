"""TODO"""

from gi.repository import GObject
from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay


class Display(GObject.GObject):
    """
    This class provides record-like funcionality of a display that contains a displays
    per cross section per lane and b displays per cross section
    """
    _a_display: dict[str, dict[int, ADisplay]] = {}
    _b_display: dict[str, BDisplay] = {}

    def __init__(self) -> None:
        super().__init__()
        self._a_display = {}
        self._b_display = {}

    def get_a_display(self, cross_section_id: str, lane_number: int) -> ADisplay:
        """Get the A Display for the given cross section id and lane number. None if not found."""
        return self._a_display.get(cross_section_id, {}).get(lane_number)

    def get_b_display(self, cross_section_id: str) -> BDisplay:
        """Get the B Display for the given cross section id. None if not found."""
        return self._b_display.get(cross_section_id)

    def set_a_display(self, cross_section_id: str, lane_number: int, display: ADisplay) -> None:
        """Set the A Display for the given cross section id and lane number."""
        if cross_section_id not in self._a_display:
            self._a_display[cross_section_id] = {}
        self._a_display[cross_section_id][lane_number] = display

    def set_b_display(self, cross_section_id: str, display: BDisplay) -> None:
        """Set the B Display for the given cross section id."""
        if cross_section_id not in self._a_display:
            self._b_display[cross_section_id] = display
        self._b_display[cross_section_id] = display
