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

    __parameter: Parameter | None = None

    def __init__(self, cell_type: ParamCellType) -> None:
        super().__init__()

        self.__type = cell_type

        child = None
        match cell_type.value:
            case ParamCellType.NAME:
                self.__label = child = Gtk.Label()

            case ParamCellType.VALUE:
                self.__entry = child = Gtk.Entry(
                    primary_icon_name="confirm", primary_icon_activatable=True)
                self.__entry.connect("icon-release", self.__on_entry_icon_release)
                self.__entry.connect("activate", self.__update_value)

            case ParamCellType.TAGS:
                self.__label = child = Gtk.Label()

        if child:
            self.set_child(child)

    def __on_entry_icon_release(self, entry: Gtk.Entry, pos: Gtk.EntryIconPosition) -> None:
        self.__update_value(entry)

    def __update_value(self, entry: Gtk.Entry) -> None:
        variant = GLib.Variant.parse(None, entry.get_text())
        # TODO: Error handling
        self.__parameter.value = variant
        entry.set_text(self.__parameter.value.print_(True))

    def bind(self, param: Parameter) -> None:
        match self.__type.value:
            case ParamCellType.NAME:
                self.__label.set_label(param.name)

            case ParamCellType.VALUE:
                if param.inconsistent:
                    self.__entry.set_text("")
                else:
                    self.__entry.set_text(param.value.print_(True))

            case ParamCellType.TAGS:
                self.__label.set_label("tags")

        self.__parameter = param
