"""This module contains the ResultCell class."""
import sys
from enum import Enum

import gi

from sbaid.model.context import Context

#from sbaid.view_model.results.result import Result

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

class ResultCellType(Enum):
    """The result property to be shown in the cell."""
    RESULT_NAME = 0
    PROJECT_NAME = 1
    DATE = 2
    TAGS = 3

class ResultCell(Adw.NavigationPage):

    __type = ResultCellType
    __label = Gtk.Label

    def __init__(self, cell_type: ResultCellType) -> None:
        super().__init__()
        self.__type = cell_type
        self.__label = child = Gtk.Label(xalign=0)
        self.set_child(child)

    def bind(self, result: Result) -> None:
        self.__result = result

        match self.__type:
            case ResultCellType.RESULT_NAME:
                self.__label.set_label(result.name)
            case ResultCellType.PROJECT_NAME:
                self.__label.set_label(result.project_name)
            case ResultCellType.DATE:
                self.__label.set_label(result.creation_date_time.format_iso8601())
            case ResultCellType.TAGS:
                self.__label.set_label(result.selected_tags)  #TODO: ist liste, muss wsl formatted werden für string


