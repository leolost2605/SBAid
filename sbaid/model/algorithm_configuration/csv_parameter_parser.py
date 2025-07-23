"""This module defines the CSVParameterParser class."""
from typing import Tuple

from gi.repository import Gio
from sbaid.model.algorithm_configuration.parameter_parser import (
    ParameterParser, ParameterParserForeachFunc)


class CSVParameterParser(ParameterParser):
    """TODO"""

    def can_handle(self, file: Gio.File) -> bool:
        """todo"""
        return None

    async def for_each_parameter(self, file: Gio.File,
                                 callback: ParameterParserForeachFunc) -> Tuple[int, int]:
        """TODO"""
        return 0, 0
