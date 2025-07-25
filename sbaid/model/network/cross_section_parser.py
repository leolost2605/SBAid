"""This module defines the CrossSectionParser interface."""
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Coroutine
from gi.repository import Gio
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location

CrossSectionParserForeachFunc = Callable[[str, Location, CrossSectionType],
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
        """Calls a function that returns the success boolean of creating a a cross section
         and returns the amount of valid cross sections added to the network and
         the amount of invalid ones that were skipped."""
