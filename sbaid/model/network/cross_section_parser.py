"""TODO"""
from typing import Tuple, Callable
from common import CrossSectionType
from model import Coordinates
from gi.repository.Gio import File


class CrossSectionParser:
    """TODO"""

    def can_handle_file(self, file) -> bool:
        """TODO"""

    def foreach_cross_section(
        self,
        file: File,
        foreach_func: Callable[[str, Coordinates, CrossSectionType], bool]
    ) -> Tuple[int, int]:
         """TODO"""
