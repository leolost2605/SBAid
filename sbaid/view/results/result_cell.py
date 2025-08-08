"""This module contains the ResultCell class."""
import sys
from enum import Enum

import gi

from sbaid.view_model.results.result import Result

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

class ResultCellType(Enum):
    """
    The result property to be shown in the cell.
    """
    RESULT_NAME = 0
    PROJECT_NAME = 1
    DATE = 2
    TAGS = 3

class ResultCell(Adw.Bin):
    """
    This class displays a property of a result for use in a column view. It allows itself
    to be recycled for performance.
    """
    __type: ResultCellType
    __label: Gtk.Label

    def __init__(self, cell_type: ResultCellType) -> None:
        super().__init__()
        self.__type = cell_type
        self.__label = Gtk.Label(xalign=0)
        self.set_child(self.__label)

    def bind(self, result: Result) -> None:
        """
        Binds the given result to this cell for display.
        :param result: the result to bind
        """
        match self.__type:
            case ResultCellType.RESULT_NAME:
                self.__label.set_label(result.name)
            case ResultCellType.PROJECT_NAME:
                self.__label.set_label(result.project_name)
            case ResultCellType.DATE:
                formatted_time = result.creation_date_time.format("%x %X")
                if formatted_time:
                    self.__label.set_label(formatted_time)
                else:
                    self.__label.set_label("Unknown Time")
            case ResultCellType.TAGS:
                self.__label.set_label("Tags appear here")  # TODO
