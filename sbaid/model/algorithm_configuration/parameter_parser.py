"""This module represents the interface ParameterParser"""
from abc import ABC, abstractmethod
from typing import Callable, Optional, Tuple
from gi.repository import Gio, GLib

ParameterParserForeachFunc = Callable[[str, Optional[str], GLib.Variant], bool]


class ParameterParser(ABC):
    """This interface defines the methods for parameters objects"""

    @abstractmethod
    def can_handle(self, file: Gio.File) -> bool:
        """Takes in a file and returns a boolean indicating if the specific
        implementation can parse the given file."""

    @abstractmethod
    def for_each_parameter(self, file: Gio.File,
                           callback: ParameterParserForeachFunc) -> Tuple[int, int]:
        """Calls a function that returns the success boolean of creating a parameter
         and returns the amount of valid parameter added to the network and
         the amount of invalid ones that were skipped."""
