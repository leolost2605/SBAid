"""TODO"""
from abc import ABC, abstractmethod
from typing import Tuple, Callable
from gi.repository import Gio
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.coordinate import Coordinate


class CrossSectionParser(ABC):
    """TODO"""
    CrossSectionParserForeachFunc = Callable[[str, Coordinate, CrossSectionType], bool]

    @abstractmethod
    def can_handle_file(self, file: Gio.File) -> bool:
        return False  # TODO

    @abstractmethod
    def foreach_cross_section(
            self,
            file: Gio.File,
            foreach_func: CrossSectionParserForeachFunc
    ) -> Tuple[int, int]:
        return [0, 0]  # TODO
