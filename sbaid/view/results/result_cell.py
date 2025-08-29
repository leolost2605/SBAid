"""This module contains the ResultCell class."""
import sys
from enum import Enum

import gi

from sbaid.view_model.results.result import Result
from sbaid.common.i18n import i18n

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk, Gdk, Gio, GLib, GObject
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


class ResultCell(Adw.Bin):
    """
    This class displays a property of a result for use in a column view. It allows itself
    to be recycled for performance.
    """
    __type: ResultCellType
    __label: Gtk.Label

    __label_binding: GObject.Binding | None = None

    def __init__(self, cell_type: ResultCellType) -> None:
        super().__init__()
        self.__type = cell_type

        self.__menu_model = Gio.Menu()

        self.__menu = Gtk.PopoverMenu.new_from_model(self.__menu_model)
        self.__menu.set_has_arrow(False)
        self.__menu.set_halign(Gtk.Align.START)

        self.__label = Gtk.Label(xalign=0)

        gesture_click = Gtk.GestureClick(button=0, exclusive=True)
        gesture_click.connect("pressed", self.__on_clicked)

        self.set_child(self.__label)
        self.add_controller(gesture_click)

    def __on_clicked(self, click: Gtk.GestureClick, n_press: int, x: float, y: float) -> None:
        event = click.get_current_event()

        if not event:
            return

        if event.triggers_context_menu():
            click.set_state(Gtk.EventSequenceState.CLAIMED)
            click.reset()

            rect = Gdk.Rectangle()
            rect.x = int(x)
            rect.y = int(y)

            if not self.__menu.get_parent():
                self.__menu.set_parent(self)

            self.__menu.set_pointing_to(rect)
            self.__menu.popup()

    def bind(self, result: Result) -> None:
        """
        Binds the given result to this cell for display.
        :param result: the result to bind
        """
        if self.__label_binding:
            self.__label_binding.unbind()
            self.__label_binding = None

        match self.__type:
            case ResultCellType.RESULT_NAME:
                self.__label_binding = result.bind_property("name", self.__label, "label",
                                                            GObject.BindingFlags.SYNC_CREATE)
            case ResultCellType.PROJECT_NAME:
                self.__label.set_label(result.project_name)
            case ResultCellType.DATE:
                formatted_time = result.creation_date_time.format("%x %X")
                if formatted_time:
                    self.__label.set_label(formatted_time)
                else:
                    self.__label.set_label(i18n._("Unknown Time"))

        self.__menu_model.remove_all()
        self.__menu_model.append(i18n._("Rename"), Gio.Action.print_detailed_name(
            "result.rename", GLib.Variant.new_string(result.id)))
        self.__menu_model.append(i18n._("Delete"), Gio.Action.print_detailed_name(
            "result.delete", GLib.Variant.new_string(result.id)))
