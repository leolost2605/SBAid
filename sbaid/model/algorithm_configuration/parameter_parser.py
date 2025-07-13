"""This module represents the interface ParameterParser"""
from abc import ABC, abstractmethod
from gi.repository import Gio, GLib
from typing import Callable, Optional

ParameterParserForeachFunc = Callable[[str, Optional[str], GLib.Variant], bool]

class ParameterParser(ABC):

    @abstractmethod
    def can_handle(self, file: Gio.File) -> bool:
        """todo"""
        pass


    @abstractmethod
    def for_each_parameter(self, file: Gio.File, callback: ParameterParserForeachFunc) -> None:
        """todo"""
        pass