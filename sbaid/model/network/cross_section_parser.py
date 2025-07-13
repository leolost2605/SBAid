"""TO DO"""
from typing import Tuple, Callable


class CrossSectionParser:
    """TO DO"""

    def can_handle_file(self, file) -> bool:
        """TO DO"""

    def foreach_cross_section(self, file: File,
                foreach_func: Callable[
                    [str, Coordinates, Common.CrossSectionType], bool]
    ) -> Tuple[int, int]:
         """TO DO"""
