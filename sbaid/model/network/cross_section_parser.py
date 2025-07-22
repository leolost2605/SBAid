"""This module defines the CrossSectionParser interface."""
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Coroutine
from gi.repository import Gio
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.coordinate import Coordinate

CrossSectionParserForeachFunc = Callable[[str, Coordinate, CrossSectionType],
                                         Coroutine[Any, Any, bool]]


class CrossSectionParser(ABC):
    """This interface defines the methods cross section parsers must implement."""

    @abstractmethod
    def can_handle_file(self, file_path: str) -> bool:
        """Takes in a file and returns a boolean indicating if the specific
        implementation can parse the given file."""

    @abstractmethod
    async def foreach_cross_section(self, file: Gio.File,
                                    foreach_func: CrossSectionParserForeachFunc) \
            -> tuple[int, int]:
        """Calls create_cross_section function and returns the amount of valid cross sections
        added to the network and the amount of invalid ones. TODO"""
