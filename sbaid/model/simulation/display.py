"""TODO"""

from gi.repository import GObject
from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay


class Display(GObject.GObject):
    """TODO"""

    def get_a_display(self, cross_section_id: str, lane_number: int) -> ADisplay:
        """TODO"""
        return ADisplay.OFF

    def get_b_display(self, cross_section_id: str) -> BDisplay:
        """TODO"""
        return BDisplay.OFF

    def set_a_display(self, cross_section_id: str, lane_number: int, display: ADisplay) -> None:
        """TODO"""

    def set_b_display(self, cross_section_id: str, display: BDisplay) -> None:
        """TODO"""
