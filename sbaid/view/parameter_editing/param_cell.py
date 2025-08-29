"""
This module contains the ParamCell class and its auxiliary enum, which are used
as recyclable widgets in a column view.
"""

import sys
from enum import Enum

import gi

from sbaid.view_model.algorithm_configuration.parameter import Parameter
from sbaid.common.i18n import i18n
try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gtk, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ParamCellType(Enum):
    """
    The parameter property to show in a param cell.
    """
    NAME = 0
    VALUE = 1
    VALUE_TYPE = 3


class ParamCell(Adw.Bin):
    """
    A widget displaying and/or allowing to change a specific property of a
    parameter depending on its ParamCellType.
    """
    __type: ParamCellType
    __label: Gtk.Label
    __entry: Gtk.Entry

    __parameter: Parameter | None = None
    __value_binding: GObject.Binding | None = None

    def __init__(self, cell_type: ParamCellType) -> None:
        super().__init__()

        self.__type = cell_type

        child: Gtk.Widget | None = None
        match cell_type:
            case ParamCellType.NAME:
                self.__label = child = Gtk.Label(xalign=0)

            case ParamCellType.VALUE_TYPE:
                self.__label = child = Gtk.Label(xalign=0)

            case ParamCellType.VALUE:
                self.__entry = child = Gtk.Entry(
                    secondary_icon_name="selection-mode-symbolic", secondary_icon_activatable=True)
                self.__entry.connect("icon-release", self.__on_entry_icon_release)
                self.__entry.connect("activate", self.__update_value)

        if child:
            self.set_child(child)

    def __on_entry_icon_release(self, entry: Gtk.Entry, pos: Gtk.EntryIconPosition) -> None:
        self.__update_value(entry)

    def __update_value(self, entry: Gtk.Entry) -> None:
        if self.__parameter is None:
            return

        try:
            variant = GLib.Variant.parse(None, entry.get_text())
            self.__parameter.update_value(variant)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(i18n._("Invalid value given"), e)
            self.__parameter.notify("value")  # Retrigger the binding

    def bind(self, param: Parameter) -> None:
        """
        Binds the given param to this cell
        :param param: the param to display in this cell
        """
        if self.__value_binding:
            self.__value_binding.unbind()
            self.__value_binding = None

        self.__parameter = param

        match self.__type:
            case ParamCellType.NAME:
                self.__label.set_label(param.name)

            case ParamCellType.VALUE_TYPE:
                self.__label.set_label(param.value_type.dup_string())

            case ParamCellType.VALUE:
                self.__value_binding = param.bind_property(
                    "value", self.__entry, "text",
                    GObject.BindingFlags.SYNC_CREATE, self.__value_transform_func)

    @staticmethod
    def __value_transform_func(binding: GObject.Binding, value: GLib.Variant | None) -> str:
        if value is None:
            return ""

        return value.print_(True)
