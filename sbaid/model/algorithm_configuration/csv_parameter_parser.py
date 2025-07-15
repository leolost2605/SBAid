"""This module defines the CSVParameterParser class."""
from gi.repository import Gio
from sbaid.model.algorithm_configuration.parameter_parser import (
    ParameterParser, ParameterParserForeachFunc)


class CSVParameterParser(ParameterParser):
    """TODO"""

    def can_handle(self, file: Gio.File) -> bool:
        """todo"""
        return None

    def for_each_parameter(self, file: Gio.File,
                           callback: ParameterParserForeachFunc) -> None:
        """todo"""
