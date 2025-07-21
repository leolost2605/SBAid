"""This module represents the interface ParameterParser"""
from abc import ABC, abstractmethod
from typing import Callable, Optional, Tuple
from gi.repository import Gio, GLib

ParameterParserForeachFunc = Callable[[str, Optional[str], GLib.Variant], bool]


class ParameterParser(ABC):
    """Handles the logic of parsing the parameters"""

    @abstractmethod
    def can_handle(self, file: Gio.File) -> bool:
        """todo"""
        # check if csv format valid
        # check if all qs numbers are valid
        # check if param names unique

    @abstractmethod
    def for_each_parameter(self, file: Gio.File,
                           callback: ParameterParserForeachFunc) -> Tuple[int, int]:
        """todo"""
