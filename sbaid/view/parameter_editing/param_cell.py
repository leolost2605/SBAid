import sys
from enum import Enum

import gi

from sbaid.view_model.algorithm_configuration.parameter import Parameter

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gio, Gtk, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ParamCellType(Enum):
    NAME = 0
    VALUE = 1
    TAGS = 2


class ParamCell(Adw.Bin):
    __type: ParamCellType
    __label: Gtk.Label
    __entry: Gtk.Entry

    def __init__(self, cell_type: ParamCellType) -> None:
        super().__init__()

        self.__type = cell_type

        child = None
        match cell_type.value:
            case ParamCellType.NAME:
                self.__label = child = Gtk.Label()

            case ParamCellType.VALUE:
                self.__entry = child = Gtk.Entry()

            case ParamCellType.TAGS:
                self.__label = child = Gtk.Label()

        if child:
            self.set_child(child)

    def bind(self, param: Parameter) -> None:
        match self.__type.value:
            case ParamCellType.NAME:
                self.__label.set_label(param.name)

            case ParamCellType.VALUE:
                self.__entry.set_placeholder_text(param.value.get_type_string())

            case ParamCellType.TAGS:
                self.__label.set_label("tags")
