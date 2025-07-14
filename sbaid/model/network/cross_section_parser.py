"""TODO"""
from typing import Tuple, Callable
from gi.repository import Gio
from sbaid.common import CrossSectionType
from sbaid.common.coordinate import Coordinate
from sbaid.model.network.csv_cross_section_parser import CSVCrossSectionParser


class CrossSectionParser(CSVCrossSectionParser):
    """TODO"""
    CrossSectionParserForeachFunc = Callable[[str, Coordinate, CrossSectionType], bool]

    def can_handle_file(self, file) -> bool:
        """TODO"""

    def foreach_cross_section(
            self,
            file: Gio.File,
            foreach_func: CrossSectionParserForeachFunc
    ) -> Tuple[int, int]:
        """TODO"""
